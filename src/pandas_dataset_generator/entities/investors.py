"""Investor entity generator."""

from typing import Dict, Any, Optional

from .base import BaseEntityGenerator
from ..utils.distributions import NumericDistributions


class InvestorGenerator(BaseEntityGenerator):
    """Generate investor entities (VC, PE, Angels, etc.)."""

    ID_PREFIX = "INV"
    ID_DIGITS = 7

    # Column order for output
    COLUMNS = [
        "investor_id",
        "investor_name_canonical",
        "investor_type",
        "hq_country",
        "founded_year",
        "aum_usd_m",
        "is_active",
        "source_system",
        "last_updated_ts_raw",
    ]

    def __init__(self, *args, **kwargs):
        """Initialize investor generator."""
        super().__init__(*args, **kwargs)
        self.distributions = NumericDistributions(self.rng)
        self._used_names: set = set()
        self._duplicate_candidates: list = []

    def generate_one(self, index: int) -> Dict[str, Any]:
        """Generate a single investor entity."""
        investor_id = self.generate_id()

        # Handle duplicate name injection
        if self._should_inject_duplicate():
            name = self._generate_duplicate_name()
        elif self._should_inject_near_duplicate():
            name = self._generate_near_duplicate_name()
        else:
            name = self.name_generator.generate_investor_name()
            self._used_names.add(name)
            # Track for future duplicates
            if len(self._duplicate_candidates) < 100:
                self._duplicate_candidates.append(name)

        # Investor type (with possible missing)
        investor_type = self.sample_from_distribution(self.config.investor_type_dist)
        investor_type = self.maybe_null(investor_type, "missing_investor_type")

        # Country (with possible missing) - uses investor-specific rate
        country = self.rng.choice(self.config.countries)
        country = self.maybe_null(country, "missing_country_investor")

        # Founded year (with anomalies)
        founded_year = self._generate_founded_year()

        # AUM (with formatting noise)
        aum = self._generate_aum()

        # Active status
        is_active = "Y" if self.rng.random() < 0.92 else "N"

        # Source system
        source_system = self.sample_from_distribution(self.config.investor_source_dist)

        # Last updated timestamp
        last_updated = self._generate_last_updated(source_system)

        return {
            "investor_id": investor_id,
            "investor_name_canonical": name,
            "investor_type": investor_type,
            "hq_country": country,
            "founded_year": founded_year,
            "aum_usd_m": aum,
            "is_active": is_active,
            "source_system": source_system,
            "last_updated_ts_raw": last_updated,
        }

    def _should_inject_duplicate(self) -> bool:
        """Check if we should inject an exact duplicate name."""
        if not self._duplicate_candidates:
            return False
        return self.dirtiness.should_inject("duplicate_investor_name")

    def _should_inject_near_duplicate(self) -> bool:
        """Check if we should inject a near-duplicate name."""
        if not self._duplicate_candidates:
            return False
        return self.dirtiness.should_inject("near_duplicate_investor_name")

    def _generate_duplicate_name(self) -> str:
        """Generate an exact duplicate of an existing name."""
        return self.rng.choice(self._duplicate_candidates)

    def _generate_near_duplicate_name(self) -> str:
        """Generate a near-duplicate of an existing name."""
        original = self.rng.choice(self._duplicate_candidates)
        return self.name_generator.generate_near_duplicate_name(original)

    def _generate_founded_year(self) -> Optional[str]:
        """Generate founded year with possible anomalies."""
        # Check for future year anomaly
        if self.dirtiness.should_inject("future_founded_year"):
            year = self.date_formatter.generate_future_year()
            return str(year)

        # Check for very old year anomaly
        if self.dirtiness.should_inject("very_old_founded_year"):
            year = self.date_formatter.generate_very_old_year()
            return str(year)

        # Normal year
        year = self.distributions.sample_founded_year(
            entity_type="investor",
            min_year=1950,
            max_year=2022
        )
        return str(year)

    def _generate_aum(self) -> Optional[str]:
        """Generate AUM with formatting noise."""
        # Sample base value
        value = self.distributions.sample_aum_usd_m()

        # Check for N/A
        if self.dirtiness.should_inject("aum_na_string"):
            return "N/A"

        # Format with possible noise
        add_commas = self.dirtiness.should_inject("aum_commas")
        add_symbol = self.dirtiness.should_inject("aum_dollar_sign")

        return self.numeric_formatter.format_value(
            value,
            decimals=0,
            add_commas=add_commas,
            add_symbol=add_symbol,
            currency="USD",
        )

    def _generate_last_updated(self, source_system: str) -> Optional[str]:
        """Generate last updated timestamp."""
        dt = self.date_formatter.generate_random_timestamp(
            start_year=2022,
            end_year=2024
        )
        return self.date_formatter.format_timestamp(dt, source_system)
