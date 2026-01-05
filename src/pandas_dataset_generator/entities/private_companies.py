"""Private company entity generator."""

from typing import Dict, Any, Optional

from .base import BaseEntityGenerator
from ..utils.distributions import NumericDistributions
from ..formatters.json_fields import JsonFieldGenerator


class PrivateCompanyGenerator(BaseEntityGenerator):
    """Generate private company entities."""

    ID_PREFIX = "PVT"
    ID_DIGITS = 7

    # Column order for output
    COLUMNS = [
        "private_company_id",
        "company_name_canonical",
        "legal_name",
        "country",
        "sector",
        "stage",
        "founded_date_raw",
        "employees_est",
        "revenue_est_usd_m",
        "investors_json",
        "tags_json",
        "source_system",
        "last_updated_ts_raw",
    ]

    def __init__(self, *args, **kwargs):
        """Initialize private company generator."""
        super().__init__(*args, **kwargs)
        self.distributions = NumericDistributions(self.rng)
        self.json_generator = JsonFieldGenerator(self.rng)

    def generate_one(self, index: int) -> Dict[str, Any]:
        """Generate a single private company entity."""
        company_id = self.generate_id()

        # Generate names
        canonical_name, legal_name = self.name_generator.generate_company_name()

        # Maybe null legal name
        legal_name = self.maybe_null(legal_name, "missing_legal_name")

        # Country
        country = self.rng.choice(self.config.countries)
        country = self.maybe_null(country, "missing_country")

        # Sector
        sector = self.sample_from_distribution(self.config.sector_dist)
        sector = self.maybe_null(sector, "missing_sector")

        # Stage
        stage = self.sample_from_distribution(self.config.stage_dist)
        stage = self.maybe_null(stage, "missing_stage")

        # Founded date (with anomalies)
        founded_date = self._generate_founded_date()

        # Employees
        employees = self._generate_employees()

        # Revenue
        revenue = self._generate_revenue()

        # investors_json - initially empty, filled during post-processing
        investors_json = "[]"

        # Tags
        tags_json = self.json_generator.generate_tags_json(
            self.config.company_tags,
            min_tags=1,
            max_tags=4
        )

        # Source system
        source_system = self.sample_from_distribution(self.config.private_source_dist)

        # Last updated
        last_updated = self._generate_last_updated(source_system)

        return {
            "private_company_id": company_id,
            "company_name_canonical": canonical_name,
            "legal_name": legal_name,
            "country": country,
            "sector": sector,
            "stage": stage,
            "founded_date_raw": founded_date,
            "employees_est": employees,
            "revenue_est_usd_m": revenue,
            "investors_json": investors_json,
            "tags_json": tags_json,
            "source_system": source_system,
            "last_updated_ts_raw": last_updated,
        }

    def _generate_founded_date(self) -> Optional[str]:
        """Generate founded date with possible anomalies."""
        # Check for invalid date anomaly
        if self.dirtiness.should_inject("invalid_founded_date"):
            return self.date_formatter.generate_invalid_date()

        # Generate valid date
        date = self.date_formatter.generate_random_date(
            start_year=2000,
            end_year=2023
        )

        # Get source system for formatting (use a default)
        source = self.sample_from_distribution(self.config.private_source_dist)
        return self.date_formatter.format_date(date, source)

    def _generate_employees(self) -> Optional[str]:
        """Generate employee count with anomalies."""
        # Unknown string
        if self.dirtiness.should_inject("employees_unknown"):
            return "unknown"

        # Sample value
        value = self.distributions.sample_employees()

        # Negative anomaly
        if self.dirtiness.should_inject("employees_negative"):
            value = -abs(value)

        return str(value)

    def _generate_revenue(self) -> Optional[str]:
        """Generate revenue with formatting noise."""
        # N/A
        if self.dirtiness.should_inject("revenue_na"):
            return "N/A"

        # Sample value
        value = self.distributions.sample_revenue_usd_m()

        # Format with possible commas
        add_commas = self.dirtiness.should_inject("revenue_commas")

        return self.numeric_formatter.format_value(
            value,
            decimals=2,
            add_commas=add_commas,
        )

    def _generate_last_updated(self, source_system: str) -> Optional[str]:
        """Generate last updated timestamp."""
        dt = self.date_formatter.generate_random_timestamp(
            start_year=2022,
            end_year=2024
        )
        return self.date_formatter.format_timestamp(dt, source_system)
