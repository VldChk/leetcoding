"""Date and timestamp formatting with source-system-aware patterns."""

from datetime import date, datetime
from typing import Dict, List

from ..rng import RNGManager


# Date formats by source system
DATE_FORMATS_BY_SOURCE: Dict[str, Dict[str, float]] = {
    "DEALS_FEED_US": {
        "MM/DD/YYYY": 0.80,
        "YYYY-MM-DD": 0.15,
        "Mon DD, YYYY": 0.05,
    },
    "DEALS_FEED_EU": {
        "DD/MM/YYYY": 0.80,
        "YYYY-MM-DD": 0.15,
        "DD Mon YYYY": 0.05,
    },
    "DEALS_MANUAL": {
        "YYYY-MM-DD": 0.60,
        "YYYY/MM/DD": 0.20,
        "Mon DD, YYYY": 0.20,
    },
    "REF_FEED_A": {
        "YYYY-MM-DD": 0.90,
        "YYYYMMDD": 0.10,
    },
    "REF_FEED_B": {
        "DD-MMM-YYYY": 0.70,
        "YYYY-MM-DD": 0.30,
    },
    "PRIVATE_DB_A": {
        "YYYY-MM-DD": 0.85,
        "MM/DD/YYYY": 0.15,
    },
    "PRIVATE_DB_B": {
        "DD/MM/YYYY": 0.70,
        "YYYY-MM-DD": 0.30,
    },
    "LISTINGS_A": {
        "YYYY-MM-DD": 0.90,
        "YYYYMMDD": 0.10,
    },
    "LISTINGS_B": {
        "DD-MMM-YYYY": 0.60,
        "YYYY-MM-DD": 0.40,
    },
    "MANUAL": {
        "YYYY-MM-DD": 0.50,
        "MM/DD/YYYY": 0.30,
        "DD/MM/YYYY": 0.20,
    },
}

# Timestamp formats by source system
TIMESTAMP_FORMATS_BY_SOURCE: Dict[str, Dict[str, float]] = {
    "DEALS_FEED_US": {
        "YYYY-MM-DD HH:MM:SS": 0.60,
        "MM/DD/YYYY HH:MM:SS": 0.30,
        "epoch_ms": 0.10,
    },
    "DEALS_FEED_EU": {
        "YYYY-MM-DD HH:MM:SS": 0.60,
        "DD/MM/YYYY HH:MM:SS": 0.30,
        "ISO8601": 0.10,
    },
    "DEALS_MANUAL": {
        "YYYY-MM-DD HH:MM:SS": 0.80,
        "ISO8601": 0.20,
    },
    "REF_FEED_A": {
        "YYYY-MM-DD HH:MM:SS": 0.90,
        "epoch_ms": 0.10,
    },
    "REF_FEED_B": {
        "DD-MMM-YYYY HH:MM:SS": 0.70,
        "YYYY-MM-DD HH:MM:SS": 0.30,
    },
    "PRIVATE_DB_A": {
        "YYYY-MM-DD HH:MM:SS": 0.90,
        "ISO8601": 0.10,
    },
    "PRIVATE_DB_B": {
        "DD/MM/YYYY HH:MM:SS": 0.70,
        "YYYY-MM-DD HH:MM:SS": 0.30,
    },
    "LISTINGS_A": {
        "YYYY-MM-DD HH:MM:SS": 0.95,
        "epoch_ms": 0.05,
    },
    "LISTINGS_B": {
        "YYYY-MM-DD HH:MM:SS": 0.80,
        "ISO8601": 0.20,
    },
    "MANUAL": {
        "YYYY-MM-DD HH:MM:SS": 0.70,
        "MM/DD/YYYY HH:MM:SS": 0.20,
        "DD/MM/YYYY HH:MM:SS": 0.10,
    },
}

# Format string mappings
FORMAT_PATTERNS: Dict[str, str] = {
    "YYYY-MM-DD": "%Y-%m-%d",
    "MM/DD/YYYY": "%m/%d/%Y",
    "DD/MM/YYYY": "%d/%m/%Y",
    "Mon DD, YYYY": "%b %d, %Y",
    "DD Mon YYYY": "%d %b %Y",
    "YYYY/MM/DD": "%Y/%m/%d",
    "YYYYMMDD": "%Y%m%d",
    "DD-MMM-YYYY": "%d-%b-%Y",
    "YYYY-MM-DD HH:MM:SS": "%Y-%m-%d %H:%M:%S",
    "MM/DD/YYYY HH:MM:SS": "%m/%d/%Y %H:%M:%S",
    "DD/MM/YYYY HH:MM:SS": "%d/%m/%Y %H:%M:%S",
    "DD-MMM-YYYY HH:MM:SS": "%d-%b-%Y %H:%M:%S",
    "ISO8601": "%Y-%m-%dT%H:%M:%S",
}

# Invalid date strings for anomaly injection
INVALID_DATE_STRINGS: List[str] = [
    "2021-02-30",   # Feb 30 doesn't exist
    "2022-13-15",   # Month 13
    "13/40/2020",   # Day 40
    "2099-07-15",   # Far future
    "00/00/0000",   # All zeros
    "2021-00-15",   # Month 0
    "not_a_date",   # Text
    "N/A",
    "TBD",
    "UNKNOWN",
    "",
    "31/02/2021",   # Feb 31
    "2020-04-31",   # Apr 31
]


class DateFormatter:
    """Format dates based on source system conventions."""

    def __init__(self, rng: RNGManager):
        """
        Initialize date formatter.

        Args:
            rng: Random number generator
        """
        self.rng = rng

    def format_date(self, d: date, source_system: str) -> str:
        """
        Format a date according to source system conventions.

        Args:
            d: Date to format
            source_system: Source system name

        Returns:
            Formatted date string
        """
        formats = DATE_FORMATS_BY_SOURCE.get(source_system, {"YYYY-MM-DD": 1.0})

        # Sample format based on distribution
        format_name = self.rng.choice(formats)
        pattern = FORMAT_PATTERNS.get(format_name, "%Y-%m-%d")

        return d.strftime(pattern)

    def format_timestamp(self, dt: datetime, source_system: str) -> str:
        """
        Format a timestamp according to source system conventions.

        Args:
            dt: Datetime to format
            source_system: Source system name

        Returns:
            Formatted timestamp string
        """
        formats = TIMESTAMP_FORMATS_BY_SOURCE.get(
            source_system,
            {"YYYY-MM-DD HH:MM:SS": 1.0}
        )

        # Sample format based on distribution
        format_name = self.rng.choice(formats)

        if format_name == "epoch_ms":
            return str(int(dt.timestamp() * 1000))

        pattern = FORMAT_PATTERNS.get(format_name, "%Y-%m-%d %H:%M:%S")
        return dt.strftime(pattern)

    def generate_invalid_date(self) -> str:
        """
        Generate an invalid date string for anomaly injection.

        Returns:
            Invalid date string
        """
        return self.rng.choice(INVALID_DATE_STRINGS)

    def generate_random_date(
        self,
        start_year: int = 2015,
        end_year: int = 2024,
    ) -> date:
        """
        Generate a random date within range.

        Args:
            start_year: Start year (inclusive)
            end_year: End year (inclusive)

        Returns:
            Random date
        """
        year = self.rng.integers(start_year, end_year + 1)
        month = self.rng.integers(1, 13)

        # Days per month
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days_in_month[1] = 29  # Leap year

        day = self.rng.integers(1, days_in_month[month - 1] + 1)

        return date(year, month, day)

    def generate_random_timestamp(
        self,
        start_year: int = 2020,
        end_year: int = 2024,
    ) -> datetime:
        """
        Generate a random timestamp within range.

        Args:
            start_year: Start year (inclusive)
            end_year: End year (inclusive)

        Returns:
            Random datetime
        """
        d = self.generate_random_date(start_year, end_year)
        hour = self.rng.integers(0, 24)
        minute = self.rng.integers(0, 60)
        second = self.rng.integers(0, 60)

        return datetime(d.year, d.month, d.day, hour, minute, second)

    def generate_future_year(self) -> int:
        """Generate a future year for anomaly injection."""
        return self.rng.integers(2026, 2033)

    def generate_very_old_year(self) -> int:
        """Generate a very old year for anomaly injection."""
        return self.rng.integers(1800, 1900)
