"""Statistical distributions for realistic data generation."""

import numpy as np
from typing import Dict, Tuple

from ..rng import RNGManager


class NumericDistributions:
    """Statistical distributions for numeric fields."""

    def __init__(self, rng: RNGManager):
        """
        Initialize distributions.

        Args:
            rng: Random number generator
        """
        self.rng = rng

    def sample_aum_usd_m(self) -> float:
        """
        Sample AUM (Assets Under Management) in USD millions.

        Distribution: lognormal, median ~3000 ($3B), range 50-200000.

        Returns:
            AUM value in millions
        """
        value = self.rng.lognormal(mean=np.log(3000), sigma=1.2)
        return float(np.clip(value, 50, 200000))

    def sample_employees(self) -> int:
        """
        Sample employee count.

        Distribution: lognormal, median ~120, range 5-50000.

        Returns:
            Employee count
        """
        value = self.rng.lognormal(mean=np.log(120), sigma=1.5)
        return int(np.clip(value, 5, 50000))

    def sample_revenue_usd_m(self) -> float:
        """
        Sample revenue in USD millions.

        Distribution: lognormal, median ~30, range 0.1-20000.

        Returns:
            Revenue in millions
        """
        value = self.rng.lognormal(mean=np.log(30), sigma=1.8)
        return float(np.clip(value, 0.1, 20000))

    def sample_market_cap_usd_m(self) -> float:
        """
        Sample market cap in USD millions.

        Distribution: lognormal, median ~12000 ($12B), range 200-4000000.

        Returns:
            Market cap in millions
        """
        value = self.rng.lognormal(mean=np.log(12000), sigma=1.3)
        return float(np.clip(value, 200, 4000000))

    def sample_deal_value_usd_m(self, deal_type: str) -> float:
        """
        Sample deal value in USD millions by deal type.

        Args:
            deal_type: Type of deal

        Returns:
            Deal value in millions
        """
        params: Dict[str, Tuple[float, float, float, float]] = {
            "INVESTMENT": (15, 1.5, 0.1, 500),
            "ACQUISITION": (250, 1.8, 1, 50000),
            "MERGER": (400, 1.6, 10, 80000),
            "MINORITY_STAKE": (30, 1.4, 0.5, 1000),
            "JOINT_VENTURE": (100, 1.5, 5, 5000),
        }

        median, sigma, min_val, max_val = params.get(deal_type, (100, 1.5, 1, 10000))
        value = self.rng.lognormal(mean=np.log(median), sigma=sigma)
        return float(np.clip(value, min_val, max_val))

    def sample_stake_pct(self, deal_type: str) -> float:
        """
        Sample stake percentage by deal type.

        Args:
            deal_type: Type of deal

        Returns:
            Stake percentage (0-100)
        """
        if deal_type in ("ACQUISITION", "MERGER"):
            # Mostly 100%, sometimes partial
            if self.rng.random() < 0.92:
                return 100.0
            else:
                return self.rng.uniform(50, 99)

        elif deal_type == "INVESTMENT":
            # Beta-ish in 1-35%
            return self.rng.beta(2, 6) * 34 + 1

        elif deal_type == "MINORITY_STAKE":
            return self.rng.uniform(1, 49)

        else:  # JOINT_VENTURE
            jv_stakes = [50.0, 49.0, 51.0, 33.33, 25.0]
            return self.rng.choice(jv_stakes)

    def sample_pre_post_valuation(
        self,
        deal_value: float,
        stake_pct: float,
    ) -> Tuple[float, float]:
        """
        Calculate pre-money and post-money valuations from deal value and stake.

        Formula:
            post_money = deal_value / (stake_pct / 100)
            pre_money = post_money - deal_value

        Args:
            deal_value: Deal value in USD millions
            stake_pct: Stake percentage

        Returns:
            Tuple of (pre_money, post_money) in millions
        """
        if stake_pct <= 0:
            return 0.0, 0.0

        post_money = deal_value / (stake_pct / 100)
        pre_money = post_money - deal_value

        return pre_money, post_money

    def sample_founded_year(
        self,
        entity_type: str = "company",
        min_year: int = 1950,
        max_year: int = 2023,
    ) -> int:
        """
        Sample a founded year.

        Args:
            entity_type: Type of entity
            min_year: Minimum year
            max_year: Maximum year

        Returns:
            Founded year
        """
        if entity_type == "investor":
            # Investors tend to be older
            return self.rng.integers(min_year, max_year)
        else:
            # Companies more recent, skewed towards recent years
            years = list(range(min_year, max_year + 1))
            # Weight recent years more heavily
            weights = [(y - min_year + 1) ** 1.5 for y in years]
            total = sum(weights)
            probs = [w / total for w in weights]
            return int(self.rng.choice(years, p=probs))


class EntitySampler:
    """Sample entities with Zipfian weighting for realistic distributions."""

    def __init__(self, rng: RNGManager):
        """
        Initialize entity sampler.

        Args:
            rng: Random number generator
        """
        self.rng = rng

    def compute_zipf_weights(self, n: int, alpha: float = 1.5) -> np.ndarray:
        """
        Compute Zipfian weights for n items.

        Args:
            n: Number of items
            alpha: Zipf exponent (higher = more skewed)

        Returns:
            Array of normalized weights
        """
        weights = np.array([1.0 / (i ** alpha) for i in range(1, n + 1)])
        return weights / weights.sum()

    def sample_with_zipf(
        self,
        items: list,
        alpha: float = 1.5,
        size: int = 1,
    ) -> list:
        """
        Sample items with Zipfian distribution.

        This creates a "power law" distribution where a small number
        of items appear very frequently (e.g., top investors do many deals).

        Args:
            items: List of items to sample from
            alpha: Zipf exponent
            size: Number of samples

        Returns:
            List of sampled items
        """
        if not items:
            return []

        weights = self.compute_zipf_weights(len(items), alpha)
        indices = self.rng.rng.choice(len(items), size=size, replace=True, p=weights)

        return [items[i] for i in indices]

    def sample_one_with_zipf(self, items: list, alpha: float = 1.5):
        """
        Sample a single item with Zipfian distribution.

        Args:
            items: List of items
            alpha: Zipf exponent

        Returns:
            Single sampled item
        """
        result = self.sample_with_zipf(items, alpha, size=1)
        return result[0] if result else None
