"""Dirtiness engine for controlled anomaly injection."""

from collections import defaultdict
from typing import Any, Callable, Dict, Optional, TypeVar

from ..rng import RNGManager
from .rates import AnomalyRates

T = TypeVar("T")


class DirtinessEngine:
    """
    Central engine for injecting data anomalies with tracking.

    This engine provides a consistent interface for injecting
    various types of data quality issues while tracking counts
    for reporting in meta.json.
    """

    def __init__(self, rates: AnomalyRates, rng: RNGManager):
        """
        Initialize dirtiness engine.

        Args:
            rates: Anomaly rate configuration
            rng: Random number generator
        """
        self.rates = rates
        self.rng = rng
        self._anomaly_counts: Dict[str, int] = defaultdict(int)

    def maybe_inject(
        self,
        anomaly_type: str,
        value: T,
        corrupt_fn: Callable[[T], T],
    ) -> T:
        """
        Conditionally inject an anomaly based on configured rate.

        Args:
            anomaly_type: Type of anomaly (without p_ prefix)
            value: Original value
            corrupt_fn: Function to corrupt the value

        Returns:
            Original or corrupted value
        """
        rate = self.rates.get_rate(anomaly_type)
        if rate > 0 and self.rng.random() < rate:
            self._anomaly_counts[anomaly_type] += 1
            return corrupt_fn(value)
        return value

    def maybe_null(self, anomaly_type: str, value: T) -> Optional[T]:
        """
        Conditionally make a value null.

        Args:
            anomaly_type: Type of anomaly (e.g., "missing_investor_type")
            value: Original value

        Returns:
            Original value or None
        """
        return self.maybe_inject(anomaly_type, value, lambda _: None)

    def maybe_corrupt_with_rate(
        self,
        rate: float,
        anomaly_type: str,
        value: T,
        corrupt_fn: Callable[[T], T],
    ) -> T:
        """
        Inject anomaly with explicit rate (not from config).

        Args:
            rate: Probability of injection
            anomaly_type: Type name for tracking
            value: Original value
            corrupt_fn: Corruption function

        Returns:
            Original or corrupted value
        """
        if rate > 0 and self.rng.random() < rate:
            self._anomaly_counts[anomaly_type] += 1
            return corrupt_fn(value)
        return value

    def should_inject(self, anomaly_type: str) -> bool:
        """
        Check if an anomaly should be injected (without applying).

        Useful when the injection logic is more complex than a simple transform.

        Args:
            anomaly_type: Type of anomaly

        Returns:
            True if anomaly should be injected
        """
        rate = self.rates.get_rate(anomaly_type)
        if rate > 0 and self.rng.random() < rate:
            self._anomaly_counts[anomaly_type] += 1
            return True
        return False

    def record_anomaly(self, anomaly_type: str, count: int = 1) -> None:
        """
        Manually record an anomaly (when injection is done externally).

        Args:
            anomaly_type: Type of anomaly
            count: Number of occurrences
        """
        self._anomaly_counts[anomaly_type] += count

    def format_numeric_with_noise(
        self,
        value: float,
        commas_type: str,
        symbol_type: Optional[str] = None,
        na_type: Optional[str] = None,
        currency: str = "USD",
        decimals: int = 2,
    ) -> str:
        """
        Format a numeric value with potential noise injection.

        Args:
            value: Numeric value
            commas_type: Anomaly type for comma formatting
            symbol_type: Anomaly type for currency symbol (optional)
            na_type: Anomaly type for N/A string (optional)
            currency: Currency code for symbol
            decimals: Decimal places

        Returns:
            Formatted string
        """
        # Maybe return N/A
        if na_type:
            rate = self.rates.get_rate(na_type)
            if rate > 0 and self.rng.random() < rate:
                self._anomaly_counts[na_type] += 1
                return "N/A"

        # Base formatting
        if value == int(value):
            result = str(int(value))
        else:
            result = f"{value:.{decimals}f}"

        # Maybe add commas
        comma_rate = self.rates.get_rate(commas_type)
        add_commas = comma_rate > 0 and self.rng.random() < comma_rate
        if add_commas:
            self._anomaly_counts[commas_type] += 1
            if value == int(value):
                result = f"{int(value):,}"
            else:
                # Format with commas and decimals
                int_part = int(value)
                frac_part = value - int_part
                result = f"{int_part:,}" + f"{frac_part:.{decimals}f}"[1:]

        # Maybe add currency symbol
        if symbol_type:
            symbol_rate = self.rates.get_rate(symbol_type)
            if symbol_rate > 0 and self.rng.random() < symbol_rate:
                self._anomaly_counts[symbol_type] += 1
                symbols = {
                    "USD": "$",
                    "GBP": "£",
                    "EUR": "€",
                    "CHF": "CHF ",
                    "SGD": "S$",
                }
                result = symbols.get(currency, "$") + result

        return result

    def inject_outlier(
        self,
        value: float,
        anomaly_type: str,
        multiplier_range: tuple = (100, 1000),
    ) -> float:
        """
        Maybe inject an outlier by multiplying the value.

        Args:
            value: Original value
            anomaly_type: Type of outlier anomaly
            multiplier_range: (min, max) multiplier range

        Returns:
            Original or outlier value
        """
        rate = self.rates.get_rate(anomaly_type)
        if rate > 0 and self.rng.random() < rate:
            self._anomaly_counts[anomaly_type] += 1
            multiplier = self.rng.uniform(multiplier_range[0], multiplier_range[1])
            return value * multiplier
        return value

    def get_anomaly_counts(self) -> Dict[str, int]:
        """Get all recorded anomaly counts."""
        return dict(self._anomaly_counts)

    def reset_counts(self) -> None:
        """Reset all anomaly counts."""
        self._anomaly_counts = defaultdict(int)
