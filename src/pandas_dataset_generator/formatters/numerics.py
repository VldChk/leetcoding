"""Numeric formatting with controlled noise injection."""

from typing import Optional, Dict

from ..rng import RNGManager


# Currency symbols
CURRENCY_SYMBOLS: Dict[str, str] = {
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "CHF": "CHF ",
    "SGD": "S$",
    "JPY": "¥",
    "CNY": "¥",
    "CAD": "C$",
    "AUD": "A$",
}


class NumericFormatter:
    """Format numeric values with optional noise."""

    def __init__(self, rng: RNGManager):
        """
        Initialize numeric formatter.

        Args:
            rng: Random number generator
        """
        self.rng = rng

    def format_value(
        self,
        value: float,
        decimals: int = 2,
        add_commas: bool = False,
        add_symbol: bool = False,
        currency: str = "USD",
    ) -> str:
        """
        Format a numeric value.

        Args:
            value: Numeric value
            decimals: Decimal places
            add_commas: Add thousand separators
            add_symbol: Add currency symbol
            currency: Currency code

        Returns:
            Formatted string
        """
        # Round to specified decimals
        if decimals == 0:
            int_value = int(round(value))
            if add_commas:
                result = f"{int_value:,}"
            else:
                result = str(int_value)
        else:
            if add_commas:
                int_part = int(value)
                frac_part = abs(value - int_part)
                result = f"{int_part:,}" + f"{frac_part:.{decimals}f}"[1:]
            else:
                result = f"{value:.{decimals}f}"

        # Add currency symbol
        if add_symbol:
            symbol = CURRENCY_SYMBOLS.get(currency, "$")
            result = symbol + result

        return result

    def format_with_noise(
        self,
        value: float,
        p_commas: float = 0.0,
        p_symbol: float = 0.0,
        p_na: float = 0.0,
        currency: str = "USD",
        decimals: int = 2,
    ) -> str:
        """
        Format a numeric value with random noise injection.

        Args:
            value: Numeric value
            p_commas: Probability of adding commas
            p_symbol: Probability of adding currency symbol
            p_na: Probability of returning N/A
            currency: Currency code
            decimals: Decimal places

        Returns:
            Formatted string (possibly with noise)
        """
        # N/A
        if p_na > 0 and self.rng.random() < p_na:
            return "N/A"

        add_commas = p_commas > 0 and self.rng.random() < p_commas
        add_symbol = p_symbol > 0 and self.rng.random() < p_symbol

        return self.format_value(
            value,
            decimals=decimals,
            add_commas=add_commas,
            add_symbol=add_symbol,
            currency=currency,
        )

    def format_percentage(
        self,
        value: float,
        decimals: int = 2,
        include_symbol: bool = False,
    ) -> str:
        """
        Format a percentage value.

        Args:
            value: Percentage value (e.g., 25.5 for 25.5%)
            decimals: Decimal places
            include_symbol: Include % symbol

        Returns:
            Formatted string
        """
        if decimals == 0:
            result = str(int(round(value)))
        else:
            result = f"{value:.{decimals}f}"

        if include_symbol:
            result += "%"

        return result

    def format_integer_with_noise(
        self,
        value: int,
        p_commas: float = 0.0,
        p_unknown: float = 0.0,
        p_negative: float = 0.0,
    ) -> str:
        """
        Format an integer with random noise.

        Args:
            value: Integer value
            p_commas: Probability of adding commas
            p_unknown: Probability of returning "unknown"
            p_negative: Probability of making negative

        Returns:
            Formatted string
        """
        # Unknown
        if p_unknown > 0 and self.rng.random() < p_unknown:
            return "unknown"

        # Make negative
        if p_negative > 0 and self.rng.random() < p_negative:
            value = -abs(value)

        # Format with/without commas
        if p_commas > 0 and self.rng.random() < p_commas:
            return f"{value:,}"

        return str(value)

    def inject_outlier(
        self,
        value: float,
        p_outlier: float,
        multiplier_min: float = 100,
        multiplier_max: float = 1000,
    ) -> float:
        """
        Possibly inject an outlier by multiplying the value.

        Args:
            value: Original value
            p_outlier: Probability of outlier
            multiplier_min: Minimum multiplier
            multiplier_max: Maximum multiplier

        Returns:
            Original or outlier value
        """
        if p_outlier > 0 and self.rng.random() < p_outlier:
            multiplier = self.rng.uniform(multiplier_min, multiplier_max)
            return value * multiplier
        return value

    def inject_negative(self, value: float, p_negative: float) -> float:
        """
        Possibly make a value negative.

        Args:
            value: Original value
            p_negative: Probability of making negative

        Returns:
            Original or negated value
        """
        if p_negative > 0 and self.rng.random() < p_negative:
            return -abs(value)
        return value

    def inject_zero(self, value: float, p_zero: float) -> float:
        """
        Possibly replace value with zero.

        Args:
            value: Original value
            p_zero: Probability of zero

        Returns:
            Original or zero
        """
        if p_zero > 0 and self.rng.random() < p_zero:
            return 0.0
        return value
