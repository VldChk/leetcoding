"""Anomaly rate definitions for controlled data dirtiness."""

from dataclasses import dataclass
from typing import Dict
import json
from pathlib import Path


@dataclass
class AnomalyRates:
    """
    Configuration for all anomaly injection rates.

    Each rate is a probability (0.0 to 1.0) that an anomaly
    of that type will be injected for a given field/row.
    """

    # === Investor table anomalies ===
    p_missing_investor_type: float = 0.01
    p_missing_country_investor: float = 0.008  # Investors use 0.008
    p_missing_country_private: float = 0.01    # Private companies use 0.01
    p_missing_country_public: float = 0.008    # Public companies use 0.008
    p_future_founded_year: float = 0.002
    p_very_old_founded_year: float = 0.001
    p_aum_commas: float = 0.05
    p_aum_dollar_sign: float = 0.02
    p_aum_na_string: float = 0.005
    p_duplicate_investor_name: float = 0.003
    p_near_duplicate_investor_name: float = 0.006

    # === Private company table anomalies ===
    p_missing_legal_name: float = 0.02
    p_missing_sector: float = 0.015
    p_missing_stage: float = 0.01
    p_employees_unknown: float = 0.01
    p_employees_negative: float = 0.001
    p_revenue_na: float = 0.01
    p_revenue_commas: float = 0.07
    p_founded_after_first_deal: float = 0.004

    # === Public company table anomalies ===
    p_missing_isin: float = 0.01
    p_bad_isin: float = 0.003
    p_missing_ticker: float = 0.02
    p_missing_exchange: float = 0.02
    p_mcap_commas: float = 0.08
    p_mcap_na: float = 0.01
    p_mcap_symbol: float = 0.02

    # === Deals table anomalies ===
    p_closed_before_announced: float = 0.01
    p_wrong_party1_type_hint: float = 0.03
    p_missing_party2_hint: float = 0.25
    p_wrong_party2_hint: float = 0.08
    p_undisclosed_value: float = 0.08
    p_missing_currency: float = 0.03
    p_missing_stake: float = 0.10
    p_stake_over_100: float = 0.003
    p_stake_negative: float = 0.002
    p_stake_zero: float = 0.004
    p_pre_greater_than_post: float = 0.006
    p_missing_terms: float = 0.60
    p_corrupt_terms_json: float = 0.01
    p_duplicate_deal_row: float = 0.004
    p_bad_party1_id: float = 0.002
    p_value_outlier_huge: float = 0.002
    p_value_negative: float = 0.001
    p_value_zero: float = 0.003
    p_value_commas: float = 0.05
    p_value_symbol: float = 0.01
    p_missing_notes: float = 0.65

    # === Date anomalies ===
    p_invalid_date_string: float = 0.006
    p_invalid_ipo_date: float = 0.003
    p_invalid_founded_date: float = 0.003
    p_missing_announced_date: float = 0.02

    # === Alias anomalies ===
    p_alias_collision: float = 0.002

    # === investors_json consistency ===
    p_investor_list_stale_drop: float = 0.07
    p_investor_list_phantom_add: float = 0.03
    p_investor_list_duplicates: float = 0.02

    def get_rate(self, anomaly_type: str) -> float:
        """Get rate for an anomaly type."""
        attr_name = f"p_{anomaly_type}"
        if hasattr(self, attr_name):
            return getattr(self, attr_name)
        # Also try without p_ prefix
        if hasattr(self, anomaly_type):
            return getattr(self, anomaly_type)
        return 0.0

    def to_dict(self) -> Dict[str, float]:
        """Convert all rates to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if k.startswith("p_")}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "AnomalyRates":
        """Create AnomalyRates from a dictionary."""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})

    @classmethod
    def from_json(cls, path: Path) -> "AnomalyRates":
        """Load anomaly rates from a JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls.from_dict(data)

    def validate(self) -> None:
        """Validate all rates are in [0, 1]."""
        for name, value in self.__dict__.items():
            if name.startswith("p_"):
                if not (0.0 <= value <= 1.0):
                    raise ValueError(
                        f"Anomaly rate {name} must be in [0, 1], got {value}"
                    )
