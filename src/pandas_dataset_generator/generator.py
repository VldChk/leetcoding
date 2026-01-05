"""Main dataset generator orchestrator."""

import json
from pathlib import Path
from typing import Optional, Callable

import pandas as pd

from .config import Config
from .rng import RNGManager
from .stats import StatisticsTracker
from .dirtiness.rates import AnomalyRates
from .dirtiness.engine import DirtinessEngine
from .names.generator import NameGenerator
from .formatters.dates import DateFormatter
from .formatters.numerics import NumericFormatter
from .formatters.json_fields import JsonFieldGenerator
from .entities.base import EntityRegistry
from .entities.investors import InvestorGenerator
from .entities.private_companies import PrivateCompanyGenerator
from .entities.public_companies import PublicCompanyGenerator
from .entities.aliases import AliasGenerator
from .entities.deals import DealGenerator
from .output.csv_writer import CSVWriter, measure_csv_size
from .output.json_writer import JSONWriter
from .output.calibrator import SizeCalibrator


class DatasetGenerator:
    """
    Main orchestrator for dataset generation.

    Coordinates all entity generators and manages the generation pipeline.
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        seed: Optional[int] = None,
        target_size_mb: Optional[float] = None,
        output_dir: Optional[Path] = None,
        anomaly_rates: Optional[AnomalyRates] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize dataset generator.

        Args:
            config: Configuration (or use defaults)
            seed: Random seed (overrides config)
            target_size_mb: Target size in MB (overrides config)
            output_dir: Output directory (overrides config)
            anomaly_rates: Custom anomaly rates
            progress_callback: Optional callback for progress updates
        """
        self.config = config or Config()

        # Apply overrides
        if seed is not None:
            self.config.seed = seed
        if target_size_mb is not None:
            self.config.target_total_size_mb = target_size_mb
        if output_dir is not None:
            self.config.output_dir = output_dir

        self.config.validate()

        # Initialize RNG
        self.rng = RNGManager(seed=self.config.seed)
        self.seed = self.rng.seed

        # Initialize anomaly rates and dirtiness engine
        self.anomaly_rates = anomaly_rates or AnomalyRates()
        self.dirtiness = DirtinessEngine(self.anomaly_rates, self.rng)

        # Initialize statistics tracker
        self.stats = StatisticsTracker(self.seed, self.config.target_total_size_mb)

        # Initialize formatters
        self.name_generator = NameGenerator(self.rng)
        self.date_formatter = DateFormatter(self.rng)
        self.numeric_formatter = NumericFormatter(self.rng)
        self.json_generator = JsonFieldGenerator(self.rng)

        # Entity registry (populated during generation)
        self.entity_registry = EntityRegistry()

        # Output writers
        self.csv_writer = CSVWriter(self.config.output_dir)
        self.json_writer = JSONWriter(self.config.output_dir)

        # Progress callback
        self._progress = progress_callback or (lambda msg: None)

        # Generated data
        self.investors_df: Optional[pd.DataFrame] = None
        self.private_df: Optional[pd.DataFrame] = None
        self.public_df: Optional[pd.DataFrame] = None
        self.aliases_df: Optional[pd.DataFrame] = None
        self.deals_df: Optional[pd.DataFrame] = None
        self.truth_df: Optional[pd.DataFrame] = None

    def generate(self) -> None:
        """Run the full generation pipeline."""
        self._progress(f"Starting generation (seed={self.seed})")

        # Phase 1: Generate dimension tables
        self._generate_dimension_tables()

        # Phase 2: Generate aliases
        self._generate_aliases()

        # Phase 3: Calibrate size and generate deals
        self._generate_deals()

        # Phase 4: Post-process
        self._post_process()

        # Phase 5: Write output
        self._write_output()

        # Finalize stats
        self.stats.finalize()
        self._progress("Generation complete!")

    def _generate_dimension_tables(self) -> None:
        """Phase 1: Generate dimension tables."""
        self._progress("Phase 1: Generating dimension tables...")

        # Create entity generators
        gen_args = {
            "config": self.config,
            "rng": self.rng,
            "dirtiness": self.dirtiness,
            "name_generator": self.name_generator,
            "date_formatter": self.date_formatter,
            "numeric_formatter": self.numeric_formatter,
        }

        # Generate investors
        investor_gen = InvestorGenerator(**gen_args)
        self.investors_df = investor_gen.generate(self.config.n_investors)
        self._progress(f"  - Investors: {len(self.investors_df):,} rows")

        # Generate private companies
        private_gen = PrivateCompanyGenerator(**gen_args)
        self.private_df = private_gen.generate(self.config.n_private)
        self._progress(f"  - Private companies: {len(self.private_df):,} rows")

        # Generate public companies
        public_gen = PublicCompanyGenerator(**gen_args)
        self.public_df = public_gen.generate(self.config.n_public)
        self._progress(f"  - Public companies: {len(self.public_df):,} rows")

        # Register entities
        self.entity_registry.register_investors(self.investors_df)
        self.entity_registry.register_private_companies(self.private_df)
        self.entity_registry.register_public_companies(self.public_df)

    def _generate_aliases(self) -> None:
        """Phase 2: Generate name aliases."""
        self._progress("Phase 2: Generating name aliases...")

        alias_gen = AliasGenerator(self.config, self.rng, self.dirtiness)
        self.aliases_df = alias_gen.generate_from_dataframes(
            self.investors_df,
            self.private_df,
            self.public_df,
        )
        self._progress(f"  - Aliases: {len(self.aliases_df):,} rows")

        # Store reference to alias generator for deal generation
        self._alias_generator = alias_gen

    def _generate_deals(self) -> None:
        """Phase 3: Calibrate and generate deals."""
        self._progress("Phase 3: Calibrating size and generating deals...")

        # Calculate base sizes
        base_sizes = {
            "investors.csv": measure_csv_size(self.investors_df),
            "private_companies.csv": measure_csv_size(self.private_df),
            "public_companies.csv": measure_csv_size(self.public_df),
            "name_aliases.csv": measure_csv_size(self.aliases_df),
        }

        # Create deal generator for pilot
        deal_gen = DealGenerator(
            config=self.config,
            rng=self.rng,
            dirtiness=self.dirtiness,
            name_generator=self.name_generator,
            date_formatter=self.date_formatter,
            numeric_formatter=self.numeric_formatter,
            entity_registry=self.entity_registry,
            alias_generator=self._alias_generator,
        )

        # Generate pilot deals
        self._progress(f"  - Generating pilot ({self.config.pilot_deals_rows:,} rows)...")
        pilot_deals, pilot_truth = deal_gen.generate(self.config.pilot_deals_rows)

        # Calibrate
        calibrator = SizeCalibrator(
            target_size_mb=self.config.target_total_size_mb,
            min_deals_rows=self.config.min_deals_rows,
            include_truth_in_target=self.config.include_truth_in_target,
        )

        calibration = calibrator.calibrate(base_sizes, pilot_deals, pilot_truth)

        self._progress(f"  - Base size: {calibration.base_bytes / 1024 / 1024:.2f} MB")
        self._progress(f"  - Bytes per deal row: {calibration.bytes_per_deal_row:.1f}")
        self._progress(f"  - Target deals: {calibration.target_deals_rows:,} rows")

        # Record calibration
        self.stats.record_calibration(
            base_bytes=calibration.base_bytes,
            bytes_per_deal_row=calibration.bytes_per_deal_row,
            target_deals_rows=calibration.target_deals_rows,
            pilot_rows=calibration.pilot_rows,
        )

        # Reset deal generator and generate full dataset
        deal_gen = DealGenerator(
            config=self.config,
            rng=RNGManager(seed=self.seed),  # Fresh RNG for reproducibility
            dirtiness=DirtinessEngine(self.anomaly_rates, RNGManager(seed=self.seed + 1)),
            name_generator=self.name_generator,
            date_formatter=DateFormatter(RNGManager(seed=self.seed + 2)),
            numeric_formatter=NumericFormatter(RNGManager(seed=self.seed + 3)),
            entity_registry=self.entity_registry,
            alias_generator=self._alias_generator,
        )

        self._progress(f"  - Generating full deals ({calibration.target_deals_rows:,} rows)...")
        self.deals_df, self.truth_df = deal_gen.generate(calibration.target_deals_rows)

        # Update dirtiness reference for stats
        self.dirtiness = deal_gen.dirtiness

        self._progress(f"  - Deals generated: {len(self.deals_df):,} rows")

    def _post_process(self) -> None:
        """Phase 4: Post-processing."""
        self._progress("Phase 4: Post-processing...")

        # Build investors_json from deals
        self._build_investors_json()

        # Shuffle dimension tables
        self._progress("  - Shuffling tables...")
        self.investors_df = self.investors_df.sample(
            frac=1, random_state=self.seed
        ).reset_index(drop=True)

        self.private_df = self.private_df.sample(
            frac=1, random_state=self.seed + 1
        ).reset_index(drop=True)

        self.public_df = self.public_df.sample(
            frac=1, random_state=self.seed + 2
        ).reset_index(drop=True)

        self._progress("  - Post-processing complete")

    def _build_investors_json(self) -> None:
        """Build investors_json field from deals data."""
        self._progress("  - Building investors_json from deals...")

        # Find investment deals
        investment_deals = self.deals_df[
            self.deals_df["deal_type"].isin(["INVESTMENT", "MINORITY_STAKE"])
        ]

        # Group by party2 and collect investors
        company_investors = {}

        for _, deal in investment_deals.iterrows():
            party1_id = deal["party1_id"]
            party1_type = deal["party1_type_hint"]

            # Only include investor party1s
            if party1_type != "INVESTOR":
                continue

            # Get investor name
            investor = self.entity_registry.investors.get(party1_id)
            if not investor:
                continue

            investor_name = investor["investor_name_canonical"]

            # Find corresponding party2 in truth mapping
            deal_id = deal["deal_id"]
            truth_row = self.truth_df[self.truth_df["deal_id"] == deal_id]

            if truth_row.empty:
                continue

            party2_id = truth_row.iloc[0]["party2_resolved_entity_id"]
            party2_type = truth_row.iloc[0]["party2_resolved_entity_type"]

            if party2_type != "PRIVATE" or not party2_id:
                continue

            # Add investor to company
            if party2_id not in company_investors:
                company_investors[party2_id] = set()

            # Inject staleness (skip adding)
            if self.rng.random() < self.anomaly_rates.p_investor_list_stale_drop:
                self.dirtiness.record_anomaly("investor_list_stale_drop")
                continue

            company_investors[party2_id].add(investor_name)

        # Inject phantom investors
        phantom_names = ["Phantom Ventures", "Ghost Capital", "Unseen Partners"]

        for company_id in company_investors:
            if self.rng.random() < self.anomaly_rates.p_investor_list_phantom_add:
                phantom = self.rng.choice(phantom_names)
                company_investors[company_id].add(phantom)
                self.dirtiness.record_anomaly("investor_list_phantom_add")

        # Update private_companies.investors_json
        def update_investors_json(row):
            company_id = row["private_company_id"]
            investors = company_investors.get(company_id, set())

            if not investors:
                return "[]"

            investor_list = list(investors)

            # Maybe inject duplicates
            if self.rng.random() < self.anomaly_rates.p_investor_list_duplicates:
                if investor_list:
                    investor_list.append(investor_list[0])
                    self.dirtiness.record_anomaly("investor_list_duplicates")

            return json.dumps(investor_list)

        self.private_df["investors_json"] = self.private_df.apply(
            update_investors_json, axis=1
        )

    def _write_output(self) -> None:
        """Phase 5: Write output files."""
        self._progress("Phase 5: Writing output files...")

        # Write CSVs
        inv_size = self.csv_writer.write(self.investors_df, "investors.csv")
        self.stats.record_file_stats(
            "investors.csv", len(self.investors_df), inv_size, len(self.investors_df.columns)
        )
        self._progress(f"  - investors.csv: {inv_size / 1024 / 1024:.2f} MB")

        prv_size = self.csv_writer.write(self.private_df, "private_companies.csv")
        self.stats.record_file_stats(
            "private_companies.csv", len(self.private_df), prv_size, len(self.private_df.columns)
        )
        self._progress(f"  - private_companies.csv: {prv_size / 1024 / 1024:.2f} MB")

        pub_size = self.csv_writer.write(self.public_df, "public_companies.csv")
        self.stats.record_file_stats(
            "public_companies.csv", len(self.public_df), pub_size, len(self.public_df.columns)
        )
        self._progress(f"  - public_companies.csv: {pub_size / 1024 / 1024:.2f} MB")

        alias_size = self.csv_writer.write(self.aliases_df, "name_aliases.csv")
        self.stats.record_file_stats(
            "name_aliases.csv", len(self.aliases_df), alias_size, len(self.aliases_df.columns)
        )
        self._progress(f"  - name_aliases.csv: {alias_size / 1024 / 1024:.2f} MB")

        # Write deals (chunked for large files)
        deal_size = self.csv_writer.write_chunked(
            self.deals_df, "deals.csv", chunk_size=100000
        )
        self.stats.record_file_stats(
            "deals.csv", len(self.deals_df), deal_size, len(self.deals_df.columns)
        )
        self._progress(f"  - deals.csv: {deal_size / 1024 / 1024:.2f} MB")

        # Write truth mapping
        truth_size = self.csv_writer.write(self.truth_df, "truth_party2_mapping.csv")
        self.stats.record_file_stats(
            "truth_party2_mapping.csv", len(self.truth_df), truth_size, len(self.truth_df.columns)
        )
        self._progress(f"  - truth_party2_mapping.csv: {truth_size / 1024 / 1024:.2f} MB")

        # Update stats with anomaly counts
        self.stats.set_anomaly_counts(self.dirtiness.get_anomaly_counts())

        # Write meta.json
        meta_size = self.json_writer.write_meta(self.stats)
        self._progress(f"  - meta.json: {meta_size / 1024:.1f} KB")

        # Summary
        total_size = inv_size + prv_size + pub_size + alias_size + deal_size + truth_size
        self._progress(f"\nTotal size: {total_size / 1024 / 1024:.2f} MB")
