"""Public company entity generator."""

import string
from typing import Dict, Any, Optional

from .base import BaseEntityGenerator
from ..utils.distributions import NumericDistributions


class PublicCompanyGenerator(BaseEntityGenerator):
    """Generate public company entities."""

    ID_PREFIX = "PUB"
    ID_DIGITS = 7

    # Column order for output
    COLUMNS = [
        "public_company_id",
        "company_name_canonical",
        "isin",
        "ticker",
        "exchange",
        "ticker_exchange_key",
        "country",
        "sector",
        "market_cap_raw",
        "ipo_date_raw",
        "status",
        "source_system",
    ]

    def __init__(self, *args, **kwargs):
        """Initialize public company generator."""
        super().__init__(*args, **kwargs)
        self.distributions = NumericDistributions(self.rng)
        self._used_tickers: set = set()

    def generate_one(self, index: int) -> Dict[str, Any]:
        """Generate a single public company entity."""
        company_id = self.generate_id()

        # Source system (determined first for consistent date formatting)
        source_system = self.sample_from_distribution(self.config.public_source_dist)

        # Generate name
        canonical_name, _ = self.name_generator.generate_company_name(
            include_legal_suffix=False
        )

        # Exchange
        exchange = self.rng.choice(self.config.exchanges)
        exchange = self.maybe_null(exchange, "missing_exchange")

        # Country (related to exchange) - uses public company-specific rate (0.008)
        country = self._get_country_for_exchange(exchange)
        country = self.maybe_null(country, "missing_country_public")

        # ISIN
        isin = self._generate_isin(country)

        # Ticker
        ticker = self._generate_ticker(canonical_name)
        ticker = self.maybe_null(ticker, "missing_ticker")

        # Ticker:Exchange key
        if ticker and exchange:
            ticker_exchange_key = f"{ticker}:{exchange}"
        else:
            ticker_exchange_key = None

        # Sector
        sector = self.sample_from_distribution(self.config.sector_dist)
        sector = self.maybe_null(sector, "missing_sector")

        # Market cap
        market_cap = self._generate_market_cap()

        # IPO date - uses row's source_system for formatting
        ipo_date = self._generate_ipo_date(source_system)

        # Status
        status = "ACTIVE" if self.rng.random() < 0.93 else "DELISTED"

        return {
            "public_company_id": company_id,
            "company_name_canonical": canonical_name,
            "isin": isin,
            "ticker": ticker,
            "exchange": exchange,
            "ticker_exchange_key": ticker_exchange_key,
            "country": country,
            "sector": sector,
            "market_cap_raw": market_cap,
            "ipo_date_raw": ipo_date,
            "status": status,
            "source_system": source_system,
        }

    def _get_country_for_exchange(self, exchange: Optional[str]) -> str:
        """Get country code based on exchange."""
        exchange_country_map = {
            "NYSE": "US",
            "NASDAQ": "US",
            "LSE": "GB",
            "Euronext": "NL",
            "XETRA": "DE",
            "SIX": "CH",
            "HKEX": "HK",
            "SGX": "SG",
        }
        if exchange and exchange in exchange_country_map:
            return exchange_country_map[exchange]
        return self.rng.choice(self.config.countries)

    def _generate_isin(self, country: Optional[str]) -> Optional[str]:
        """
        Generate ISIN code.

        Format: 2 letter country code + 10 alphanumeric characters
        """
        # Maybe missing
        if self.dirtiness.should_inject("missing_isin"):
            return None

        # Maybe invalid
        if self.dirtiness.should_inject("bad_isin"):
            # Invalid length or format
            bad_patterns = [
                "INVALID",
                "US12345",  # Too short
                "US1234567890123",  # Too long
                "12US34567890AB",  # Wrong order
            ]
            return self.rng.choice(bad_patterns)

        # Generate valid-ish ISIN
        prefix = country[:2] if country else "US"
        chars = string.ascii_uppercase + string.digits
        suffix = "".join(self.rng.choice(list(chars)) for _ in range(10))

        return prefix + suffix

    def _generate_ticker(self, company_name: str) -> str:
        """Generate ticker symbol from company name."""
        # Extract first letters of words
        words = company_name.split()
        if len(words) >= 3:
            ticker = "".join(w[0] for w in words[:3]).upper()
        elif len(words) >= 2:
            ticker = (words[0][:2] + words[1][0]).upper()
        else:
            ticker = words[0][:4].upper()

        # Ensure uniqueness
        base_ticker = ticker
        counter = 1
        while ticker in self._used_tickers:
            ticker = f"{base_ticker}{counter}"
            counter += 1

        self._used_tickers.add(ticker)
        return ticker

    def _generate_market_cap(self) -> Optional[str]:
        """Generate market cap with formatting noise."""
        # N/A
        if self.dirtiness.should_inject("mcap_na"):
            return "N/A"

        # Sample value
        value = self.distributions.sample_market_cap_usd_m()

        # Format with noise
        add_commas = self.dirtiness.should_inject("mcap_commas")
        add_symbol = self.dirtiness.should_inject("mcap_symbol")

        return self.numeric_formatter.format_value(
            value,
            decimals=0,
            add_commas=add_commas,
            add_symbol=add_symbol,
            currency="USD",
        )

    def _generate_ipo_date(self, source_system: str) -> Optional[str]:
        """Generate IPO date with possible anomalies."""
        # Invalid date
        if self.dirtiness.should_inject("invalid_ipo_date"):
            return self.date_formatter.generate_invalid_date()

        # Generate valid date
        date = self.date_formatter.generate_random_date(
            start_year=1990,
            end_year=2023
        )

        # Use the row's source_system for consistent formatting
        return self.date_formatter.format_date(date, source_system)
