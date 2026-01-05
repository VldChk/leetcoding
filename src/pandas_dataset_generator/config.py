"""Configuration management for the dataset generator."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json


@dataclass
class Config:
    """Configuration for dataset generation."""

    # Output settings
    output_dir: Path = field(default_factory=lambda: Path("./output"))

    # Seed for reproducibility
    seed: Optional[int] = None

    # Target size
    target_total_size_mb: float = 100.0
    include_truth_in_target: bool = False

    # Row counts for dimension tables
    n_investors: int = 25_000
    n_private: int = 35_000
    n_public: int = 6_000

    # Calibration settings
    pilot_deals_rows: int = 20_000
    min_deals_rows: int = 50_000

    # Alias generation
    avg_aliases_investor: float = 1.2
    avg_aliases_private: float = 1.3
    avg_aliases_public: float = 1.1

    # Categorical distributions - Investor types
    investor_type_dist: dict = field(default_factory=lambda: {
        "VC": 0.40,
        "PE": 0.25,
        "ANGEL": 0.12,
        "HEDGE_FUND": 0.08,
        "CORP_VENTURE": 0.10,
        "SOVEREIGN_FUND": 0.05,
    })

    # Categorical distributions - Sectors
    sector_dist: dict = field(default_factory=lambda: {
        "TECH": 0.33,
        "FINANCE": 0.10,
        "HEALTHCARE": 0.12,
        "INDUSTRIALS": 0.10,
        "CONSUMER": 0.12,
        "ENERGY": 0.06,
        "REAL_ESTATE": 0.05,
        "TELECOM": 0.04,
        "UTILITIES": 0.03,
        "OTHER": 0.05,
    })

    # Categorical distributions - Company stages
    stage_dist: dict = field(default_factory=lambda: {
        "SEED": 0.20,
        "SERIES_A": 0.22,
        "SERIES_B": 0.18,
        "SERIES_C": 0.15,
        "GROWTH": 0.12,
        "LATE_STAGE": 0.08,
        "PRE_IPO": 0.05,
    })

    # Categorical distributions - Deal types
    deal_type_dist: dict = field(default_factory=lambda: {
        "INVESTMENT": 0.55,
        "ACQUISITION": 0.27,
        "MERGER": 0.10,
        "MINORITY_STAKE": 0.05,
        "JOINT_VENTURE": 0.03,
    })

    # Categorical distributions - Deal status
    deal_status_dist: dict = field(default_factory=lambda: {
        "ANNOUNCED": 0.45,
        "COMPLETED": 0.45,
        "WITHDRAWN": 0.10,
    })

    # Categorical distributions - Source systems
    investor_source_dist: dict = field(default_factory=lambda: {
        "REF_FEED_A": 0.45,
        "REF_FEED_B": 0.35,
        "MANUAL": 0.20,
    })

    private_source_dist: dict = field(default_factory=lambda: {
        "PRIVATE_DB_A": 0.50,
        "PRIVATE_DB_B": 0.30,
        "MANUAL": 0.20,
    })

    public_source_dist: dict = field(default_factory=lambda: {
        "LISTINGS_A": 0.50,
        "LISTINGS_B": 0.35,
        "MANUAL": 0.15,
    })

    deal_source_dist: dict = field(default_factory=lambda: {
        "DEALS_FEED_US": 0.45,
        "DEALS_FEED_EU": 0.35,
        "DEALS_MANUAL": 0.20,
    })

    # Exchange list for public companies
    exchanges: list = field(default_factory=lambda: [
        "NYSE", "NASDAQ", "LSE", "Euronext", "XETRA", "SIX", "HKEX", "SGX"
    ])

    # Countries (ISO2)
    countries: list = field(default_factory=lambda: [
        "US", "GB", "DE", "FR", "NL", "CH", "SG", "AE", "IN", "CA",
        "JP", "CN", "AU", "IE", "LU", "SE", "DK", "NO", "FI", "BE"
    ])

    # Currencies
    currencies: list = field(default_factory=lambda: [
        "USD", "GBP", "EUR", "CHF", "SGD"
    ])

    # Tags for private companies
    company_tags: list = field(default_factory=lambda: [
        "AI", "B2B", "B2C", "SaaS", "Fintech", "Healthtech", "Edtech",
        "Cleantech", "Biotech", "Deeptech", "Marketplace", "Enterprise"
    ])

    # Legal suffixes distribution
    legal_suffix_dist: dict = field(default_factory=lambda: {
        "Inc": 0.25,
        "Ltd": 0.20,
        "PLC": 0.08,
        "LLC": 0.10,
        "GmbH": 0.05,
        "S.A.": 0.05,
        "": 0.27,
    })

    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.target_total_size_mb <= 0:
            raise ValueError("target_total_size_mb must be positive")
        if self.n_investors <= 0:
            raise ValueError("n_investors must be positive")
        if self.n_private <= 0:
            raise ValueError("n_private must be positive")
        if self.n_public <= 0:
            raise ValueError("n_public must be positive")

        # Validate distributions sum to ~1.0
        for name, dist in [
            ("investor_type_dist", self.investor_type_dist),
            ("sector_dist", self.sector_dist),
            ("stage_dist", self.stage_dist),
            ("deal_type_dist", self.deal_type_dist),
            ("deal_status_dist", self.deal_status_dist),
        ]:
            total = sum(dist.values())
            if abs(total - 1.0) > 0.01:
                raise ValueError(f"{name} must sum to 1.0, got {total}")

    @classmethod
    def from_json(cls, path: Path) -> "Config":
        """Load configuration from JSON file."""
        with open(path) as f:
            data = json.load(f)

        # Convert output_dir to Path if present
        if "output_dir" in data:
            data["output_dir"] = Path(data["output_dir"])

        return cls(**data)

    def to_dict(self) -> dict:
        """Convert config to dictionary for serialization."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Path):
                result[key] = str(value)
            else:
                result[key] = value
        return result
