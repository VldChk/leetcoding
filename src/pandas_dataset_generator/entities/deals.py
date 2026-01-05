"""Deal entity generator - the main fact table."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd

from ..config import Config
from ..rng import RNGManager
from ..dirtiness.engine import DirtinessEngine
from ..names.generator import NameGenerator
from ..names.transforms import AliasTransformer
from ..formatters.dates import DateFormatter
from ..formatters.numerics import NumericFormatter
from ..formatters.json_fields import JsonFieldGenerator
from ..utils.distributions import NumericDistributions, EntitySampler
from .base import EntityRegistry
from .aliases import AliasGenerator


# Party1 selection by deal type
PARTY1_TYPE_BY_DEAL = {
    "INVESTMENT": {"INVESTOR": 0.95, "PUBLIC": 0.05},
    "MINORITY_STAKE": {"INVESTOR": 0.70, "PUBLIC": 0.30},
    "ACQUISITION": {"PUBLIC": 0.60, "PRIVATE": 0.35, "INVESTOR": 0.05},
    "MERGER": {"PUBLIC": 0.40, "PRIVATE": 0.60},
    "JOINT_VENTURE": {"PUBLIC": 0.50, "PRIVATE": 0.50},
}

# Party2 type by deal type (INVESTOR can be a target in acquisitions/JVs)
PARTY2_TYPE_BY_DEAL = {
    "INVESTMENT": {"PRIVATE": 0.92, "PUBLIC": 0.06, "UNKNOWN": 0.02},
    "ACQUISITION": {"PRIVATE": 0.70, "PUBLIC": 0.18, "INVESTOR": 0.07, "UNKNOWN": 0.05},
    "MERGER": {"PRIVATE": 0.48, "PUBLIC": 0.45, "INVESTOR": 0.02, "UNKNOWN": 0.05},
    "MINORITY_STAKE": {"PRIVATE": 0.70, "PUBLIC": 0.25, "UNKNOWN": 0.05},
    "JOINT_VENTURE": {"PRIVATE": 0.55, "PUBLIC": 0.35, "INVESTOR": 0.05, "UNKNOWN": 0.05},
}

# Party2 name match class distribution (spec: EXACT|ALIAS|NORMALIZED|TYPO|UNKNOWN)
MATCH_CLASS_DIST = {
    "EXACT": 0.55,
    "ALIAS": 0.25,
    "NORMALIZED": 0.10,
    "TYPO": 0.05,
    "UNKNOWN": 0.05,
}


@dataclass
class TruthMapping:
    """Truth mapping for party2 resolution."""
    deal_id: str
    party2_resolved_entity_id: Optional[str]
    party2_resolved_entity_type: Optional[str]
    match_class: str
    match_confidence: float
    resolver_notes: Optional[str] = None


class DealGenerator:
    """Generate deal entities with truth mapping."""

    ID_PREFIX = "D"
    ID_DIGITS = 9

    COLUMNS = [
        "deal_id",
        "source_system",
        "ingestion_ts_raw",
        "deal_type",
        "deal_status",
        "announced_date_raw",
        "closed_date_raw",
        "party1_id",
        "party1_type_hint",
        "party2_name_raw",
        "party2_entity_hint",
        "deal_value_raw",
        "deal_currency",
        "stake_pct_raw",
        "post_money_valuation_raw",
        "pre_money_valuation_raw",
        "deal_terms_json",
        "notes",
    ]

    TRUTH_COLUMNS = [
        "deal_id",
        "party2_resolved_entity_id",
        "party2_resolved_entity_type",
        "match_class",
        "match_confidence",
        "resolver_notes",
    ]

    def __init__(
        self,
        config: Config,
        rng: RNGManager,
        dirtiness: DirtinessEngine,
        name_generator: NameGenerator,
        date_formatter: DateFormatter,
        numeric_formatter: NumericFormatter,
        entity_registry: EntityRegistry,
        alias_generator: AliasGenerator,
    ):
        """Initialize deal generator."""
        self.config = config
        self.rng = rng
        self.dirtiness = dirtiness
        self.name_generator = name_generator
        self.date_formatter = date_formatter
        self.numeric_formatter = numeric_formatter
        self.entity_registry = entity_registry
        self.alias_generator = alias_generator

        self.distributions = NumericDistributions(rng)
        self.entity_sampler = EntitySampler(rng)
        self.json_generator = JsonFieldGenerator(rng, dirtiness=dirtiness)
        self.alias_transformer = AliasTransformer(rng)

        self._current_id = 0
        self._deals: List[Dict[str, Any]] = []
        self._truth_mappings: List[TruthMapping] = []

        # Precompute Zipf weights for entity sampling
        self._investor_weights = self.entity_sampler.compute_zipf_weights(
            len(entity_registry.investor_list), alpha=1.5
        )
        self._private_weights = self.entity_sampler.compute_zipf_weights(
            len(entity_registry.private_list), alpha=1.3
        )
        self._public_weights = self.entity_sampler.compute_zipf_weights(
            len(entity_registry.public_list), alpha=1.4
        )

    def generate_id(self) -> str:
        """Generate unique deal ID."""
        self._current_id += 1
        return f"{self.ID_PREFIX}{self._current_id:0{self.ID_DIGITS}d}"

    def generate(self, n: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Generate n deals with truth mappings.

        Args:
            n: Number of deals

        Returns:
            Tuple of (deals_df, truth_df)
        """
        self._deals = []
        self._truth_mappings = []
        self._current_id = 0

        for _ in range(n):
            deal, truth = self._generate_one()
            self._deals.append(deal)
            self._truth_mappings.append(truth)

        # Inject duplicate deals
        self._inject_duplicates()

        # Shuffle deals (important: destroy ordering)
        indices = self.rng.permutation(len(self._deals))
        self._deals = [self._deals[i] for i in indices]
        self._truth_mappings = [self._truth_mappings[i] for i in indices]

        deals_df = pd.DataFrame(self._deals, columns=self.COLUMNS)
        truth_df = pd.DataFrame([
            {
                "deal_id": t.deal_id,
                "party2_resolved_entity_id": t.party2_resolved_entity_id,
                "party2_resolved_entity_type": t.party2_resolved_entity_type,
                "match_class": t.match_class,
                "match_confidence": str(t.match_confidence),
                "resolver_notes": t.resolver_notes,
            }
            for t in self._truth_mappings
        ], columns=self.TRUTH_COLUMNS)

        return deals_df, truth_df

    def _generate_one(self) -> Tuple[Dict[str, Any], TruthMapping]:
        """Generate a single deal with truth mapping."""
        deal_id = self.generate_id()

        # Core deal attributes
        deal_type = self.rng.choice(self.config.deal_type_dist)
        deal_status = self.rng.choice(self.config.deal_status_dist)
        source_system = self.rng.choice(self.config.deal_source_dist)

        # Timestamps
        ingestion_ts = self.date_formatter.generate_random_timestamp(2022, 2024)
        ingestion_ts_raw = self.date_formatter.format_timestamp(ingestion_ts, source_system)

        # Dates
        announced_date, closed_date = self._generate_deal_dates(deal_status, source_system)

        # Party1
        party1_id, party1_type = self._select_party1(deal_type)
        party1_type_hint = self._generate_party1_type_hint(party1_id, party1_type)

        # Party2
        party2_name, party2_hint, truth = self._generate_party2(deal_id, deal_type)

        # Values
        deal_value, currency = self._generate_deal_value(deal_type)
        stake_pct = self._generate_stake_pct(deal_type)
        pre_money, post_money = self._generate_valuations(deal_type, deal_value, stake_pct)

        # Deal terms
        deal_terms = self.json_generator.generate_deal_terms_json(
            p_missing=self.dirtiness.rates.p_missing_terms,
            p_corrupt=self.dirtiness.rates.p_corrupt_terms_json,
        )

        # Notes
        notes = self._generate_notes()

        deal = {
            "deal_id": deal_id,
            "source_system": source_system,
            "ingestion_ts_raw": ingestion_ts_raw,
            "deal_type": deal_type,
            "deal_status": deal_status,
            "announced_date_raw": announced_date,
            "closed_date_raw": closed_date,
            "party1_id": party1_id,
            "party1_type_hint": party1_type_hint,
            "party2_name_raw": party2_name,
            "party2_entity_hint": party2_hint,
            "deal_value_raw": deal_value,
            "deal_currency": currency,
            "stake_pct_raw": stake_pct,
            "post_money_valuation_raw": post_money,
            "pre_money_valuation_raw": pre_money,
            "deal_terms_json": deal_terms,
            "notes": notes,
        }

        return deal, truth

    def _select_party1(self, deal_type: str) -> Tuple[str, str]:
        """Select party1 entity based on deal type."""
        type_dist = PARTY1_TYPE_BY_DEAL.get(deal_type, {"INVESTOR": 1.0})
        party_type = self.rng.choice(type_dist)

        # Check for bad reference injection
        if self.dirtiness.should_inject("bad_party1_id"):
            return self._generate_bad_party1_id(party_type), party_type

        # Select entity with Zipf weighting
        if party_type == "INVESTOR" and self.entity_registry.investor_list:
            entity = self.entity_sampler.sample_one_with_zipf(
                self.entity_registry.investor_list, alpha=1.5
            )
            return entity["investor_id"], party_type

        elif party_type == "PRIVATE" and self.entity_registry.private_list:
            entity = self.entity_sampler.sample_one_with_zipf(
                self.entity_registry.private_list, alpha=1.3
            )
            return entity["private_company_id"], party_type

        elif party_type == "PUBLIC" and self.entity_registry.public_list:
            entity = self.entity_sampler.sample_one_with_zipf(
                self.entity_registry.public_list, alpha=1.4
            )
            return entity["public_company_id"], party_type

        # Fallback
        return "INV0000001", "INVESTOR"

    def _generate_bad_party1_id(self, party_type: str) -> str:
        """Generate an invalid party1 ID."""
        prefixes = {"INVESTOR": "INV", "PRIVATE": "PVT", "PUBLIC": "PUB"}
        prefix = prefixes.get(party_type, "INV")

        bad_patterns = [
            f"{prefix}9999999",
            f"{prefix}{prefix}0000001",
            f"{prefix.lower()}0000001",
            "INVALID_ID",
        ]
        return self.rng.choice(bad_patterns)

    def _generate_party1_type_hint(self, party1_id: str, actual_type: str) -> str:
        """Generate party1 type hint (may be wrong)."""
        if self.dirtiness.should_inject("wrong_party1_type_hint"):
            # Return wrong type
            all_types = ["INVESTOR", "PRIVATE", "PUBLIC"]
            wrong_types = [t for t in all_types if t != actual_type]
            return self.rng.choice(wrong_types)
        return actual_type

    def _generate_party2(
        self,
        deal_id: str,
        deal_type: str,
    ) -> Tuple[str, Optional[str], TruthMapping]:
        """Generate party2 name and truth mapping."""
        # Select party2 type
        type_dist = PARTY2_TYPE_BY_DEAL.get(deal_type, {"PRIVATE": 1.0})
        party2_type = self.rng.choice(type_dist)

        # Select match class
        match_class = self.rng.choice(MATCH_CLASS_DIST)

        # Handle UNKNOWN type
        if party2_type == "UNKNOWN" or match_class == "UNKNOWN":
            name = self.name_generator.generate_unknown_company_name()
            hint = self._generate_party2_hint("UNKNOWN")
            return name, hint, TruthMapping(
                deal_id=deal_id,
                party2_resolved_entity_id=None,
                party2_resolved_entity_type=None,
                match_class="UNKNOWN",
                match_confidence=0.0,
            )

        # Select actual entity
        entity_list = self.entity_registry.get_list_by_type(party2_type)
        if not entity_list:
            name = self.name_generator.generate_unknown_company_name()
            hint = self._generate_party2_hint("UNKNOWN")
            return name, hint, TruthMapping(
                deal_id=deal_id,
                party2_resolved_entity_id=None,
                party2_resolved_entity_type=None,
                match_class="UNKNOWN",
                match_confidence=0.0,
            )

        entity = self.rng.choice(entity_list)
        entity_id = self._get_entity_id(entity, party2_type)
        canonical_name = self._get_canonical_name(entity, party2_type)

        # Generate name based on match class
        name, confidence = self._generate_party2_name(
            entity_id, canonical_name, match_class
        )

        hint = self._generate_party2_hint(party2_type)

        return name, hint, TruthMapping(
            deal_id=deal_id,
            party2_resolved_entity_id=entity_id,
            party2_resolved_entity_type=party2_type,
            match_class=match_class,
            match_confidence=confidence,
        )

    def _generate_party2_name(
        self,
        entity_id: str,
        canonical_name: str,
        match_class: str,
    ) -> Tuple[str, float]:
        """Generate party2 name based on match class."""
        if match_class == "EXACT":
            return canonical_name, 1.0

        elif match_class == "ALIAS":
            alias = self.alias_generator.get_random_alias(entity_id)
            if alias:
                return alias, 0.95
            return canonical_name, 1.0

        elif match_class == "NORMALIZED":
            name, _ = self.alias_transformer.normalize_name(canonical_name)
            return name, 0.85

        elif match_class == "TYPO":
            name, _ = self.alias_transformer.introduce_typo(canonical_name)
            return name, 0.70

        return canonical_name, 1.0

    def _generate_party2_hint(self, actual_type: str) -> Optional[str]:
        """Generate party2 entity hint (may be missing or wrong)."""
        if self.dirtiness.should_inject("missing_party2_hint"):
            return None

        if self.dirtiness.should_inject("wrong_party2_hint"):
            all_types = ["INVESTOR", "PRIVATE", "PUBLIC", "UNKNOWN"]
            wrong_types = [t for t in all_types if t != actual_type]
            return self.rng.choice(wrong_types)

        return actual_type

    def _get_entity_id(self, entity: Dict, entity_type: str) -> str:
        """Get entity ID from entity dict."""
        if entity_type == "INVESTOR":
            return entity["investor_id"]
        elif entity_type == "PRIVATE":
            return entity["private_company_id"]
        elif entity_type == "PUBLIC":
            return entity["public_company_id"]
        return ""

    def _get_canonical_name(self, entity: Dict, entity_type: str) -> str:
        """Get canonical name from entity dict."""
        if entity_type == "INVESTOR":
            return entity["investor_name_canonical"]
        else:
            return entity["company_name_canonical"]

    def _generate_deal_dates(
        self,
        deal_status: str,
        source_system: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Generate announced and closed dates."""
        # Maybe missing announced date
        if self.dirtiness.should_inject("missing_announced_date"):
            announced = None
        else:
            # Check for invalid date
            if self.dirtiness.should_inject("invalid_date_string"):
                announced = self.date_formatter.generate_invalid_date()
            else:
                ann_date = self.date_formatter.generate_random_date(2018, 2024)
                announced = self.date_formatter.format_date(ann_date, source_system)

        # Closed date logic
        if deal_status == "ANNOUNCED":
            closed = None
        elif deal_status == "WITHDRAWN":
            closed = None
        else:  # COMPLETED
            # Check for invalid date injection on closed_date
            if self.dirtiness.should_inject("invalid_date_string"):
                closed = self.date_formatter.generate_invalid_date()
            elif announced and self.dirtiness.should_inject("closed_before_announced"):
                # Inject closed before announced
                early_date = date(2015, 1, 1)
                closed = self.date_formatter.format_date(early_date, source_system)
            elif announced:
                # Closed after announced
                close_date = self.date_formatter.generate_random_date(2019, 2024)
                closed = self.date_formatter.format_date(close_date, source_system)
            else:
                closed = None

        return announced, closed

    def _generate_deal_value(self, deal_type: str) -> Tuple[Optional[str], Optional[str]]:
        """Generate deal value and currency."""
        # Undisclosed
        if self.dirtiness.should_inject("undisclosed_value"):
            currency = None if self.rng.random() < 0.5 else self.rng.choice(self.config.currencies)
            return None, currency

        # Sample value
        value = self.distributions.sample_deal_value_usd_m(deal_type)

        # Anomalies
        if self.dirtiness.should_inject("value_outlier_huge"):
            value = value * self.rng.uniform(100, 1000)
        elif self.dirtiness.should_inject("value_negative"):
            value = -abs(value)
        elif self.dirtiness.should_inject("value_zero"):
            value = 0

        # Currency
        currency = self.rng.choice(self.config.currencies)
        if self.dirtiness.should_inject("missing_currency"):
            currency = None

        # Format with noise
        add_commas = self.dirtiness.should_inject("value_commas")
        add_symbol = self.dirtiness.should_inject("value_symbol")

        value_str = self.numeric_formatter.format_value(
            value,
            decimals=2,
            add_commas=add_commas,
            add_symbol=add_symbol,
            currency=currency or "USD",
        )

        return value_str, currency

    def _generate_stake_pct(self, deal_type: str) -> Optional[str]:
        """Generate stake percentage."""
        if self.dirtiness.should_inject("missing_stake"):
            return None

        stake = self.distributions.sample_stake_pct(deal_type)

        # Anomalies
        if self.dirtiness.should_inject("stake_over_100"):
            stake = self.rng.uniform(101, 200)
        elif self.dirtiness.should_inject("stake_negative"):
            stake = -self.rng.uniform(1, 50)
        elif self.dirtiness.should_inject("stake_zero"):
            stake = 0

        return self.numeric_formatter.format_percentage(stake, decimals=2)

    def _generate_valuations(
        self,
        deal_type: str,
        deal_value_str: Optional[str],
        stake_str: Optional[str],
    ) -> Tuple[Optional[str], Optional[str]]:
        """Generate pre-money and post-money valuations."""
        # Only for investment deals
        if deal_type not in ("INVESTMENT", "MINORITY_STAKE"):
            return None, None

        if not deal_value_str or not stake_str:
            return None, None

        try:
            # Parse value (remove formatting)
            value_clean = deal_value_str.replace(",", "").replace("$", "")
            deal_value = float(value_clean)

            stake_clean = stake_str.replace("%", "")
            stake_pct = float(stake_clean)

            if stake_pct <= 0:
                return None, None

            pre_money, post_money = self.distributions.sample_pre_post_valuation(
                deal_value, stake_pct
            )

            # Maybe inject contradiction
            if self.dirtiness.should_inject("pre_greater_than_post"):
                pre_money, post_money = post_money * 1.5, post_money

            pre_str = self.numeric_formatter.format_value(pre_money, decimals=2)
            post_str = self.numeric_formatter.format_value(post_money, decimals=2)

            return pre_str, post_str

        except (ValueError, ZeroDivisionError):
            return None, None

    def _generate_notes(self) -> Optional[str]:
        """Generate deal notes."""
        if self.dirtiness.should_inject("missing_notes"):
            return None

        notes = [
            "Strategic investment",
            "Follow-on round",
            "Lead investor",
            "Co-investment",
            "Syndicated deal",
            "Growth capital",
            "Expansion funding",
            "Bridge financing",
            "Series extension",
            "Platform acquisition",
        ]
        return self.rng.choice(notes)

    def _inject_duplicates(self) -> None:
        """Inject duplicate deal rows."""
        n_dups = int(len(self._deals) * self.dirtiness.rates.p_duplicate_deal_row)

        for _ in range(n_dups):
            if not self._deals:
                break

            # Pick a random deal to duplicate
            idx = self.rng.integers(0, len(self._deals))
            original = self._deals[idx].copy()
            original_truth = self._truth_mappings[idx]

            # Change only the deal_id
            new_id = self.generate_id()
            original["deal_id"] = new_id

            new_truth = TruthMapping(
                deal_id=new_id,
                party2_resolved_entity_id=original_truth.party2_resolved_entity_id,
                party2_resolved_entity_type=original_truth.party2_resolved_entity_type,
                match_class=original_truth.match_class,
                match_confidence=original_truth.match_confidence,
                resolver_notes="DUPLICATE_OF_" + self._deals[idx]["deal_id"],
            )

            self._deals.append(original)
            self._truth_mappings.append(new_truth)
            self.dirtiness.record_anomaly("duplicate_deal_row")
