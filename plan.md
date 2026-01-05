# M&A / Private Deals Pandas Practice Dataset Generator
## Implementation Plan v1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Module Design](#3-module-design)
4. [Data Model & Schemas](#4-data-model--schemas)
5. [Generation Pipeline](#5-generation-pipeline)
6. [Name Generation System](#6-name-generation-system)
7. [Data Dirtiness Engine](#7-data-dirtiness-engine)
8. [Date/Time Formatting System](#8-datetime-formatting-system)
9. [Numeric Generation & Formatting](#9-numeric-generation--formatting)
10. [Party2 Fuzzy Match Model](#10-party2-fuzzy-match-model)
11. [Size Calibration Algorithm](#11-size-calibration-algorithm)
12. [Implementation Phases](#12-implementation-phases)
13. [Testing Strategy](#13-testing-strategy)
14. [File Structure](#14-file-structure)
15. [Dependencies](#15-dependencies)
16. [CLI Interface](#16-cli-interface)

---

## 1. Executive Summary

### Goal
Build a Python-based deterministic dataset generator that produces realistic M&A/Private Deals data with controlled "dirtiness" for Pandas practice. The generator creates ~100MB of interconnected CSV files simulating Bloomberg-style reference data.

### Key Deliverables
| File | Purpose | Default Rows |
|------|---------|--------------|
| `investors.csv` | VC/PE/Angel investor dictionary | 25,000 |
| `private_companies.csv` | Private company dictionary | 35,000 |
| `public_companies.csv` | Public company dictionary | 6,000 |
| `deals.csv` | Main fact table (scaled to hit target size) | ~1.5-2M |
| `name_aliases.csv` | Canonical ↔ alias mapping | ~80,000 |
| `truth_party2_mapping.csv` | Answer key for fuzzy matching | Same as deals |
| `meta.json` | Generation parameters & statistics | 1 |

### Key Design Principles
1. **Determinism**: Same seed → byte-identical output
2. **Controlled Chaos**: Every anomaly has a known rate and diagnostic hook
3. **Realistic Distributions**: Zipfian/lognormal patterns matching real M&A data
4. **Solvable Problems**: Dirty data is messy but tractable with proper techniques

---

## 2. Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DatasetGenerator (Main)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │   Config     │  │  RNG Manager │  │  Statistics  │  │  Output Writer   │ │
│  │   Manager    │  │  (seeded)    │  │  Tracker     │  │  (CSV/JSON)      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│                            Entity Generators                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Investor    │  │   Private    │  │   Public     │  │   Deal           │ │
│  │  Generator   │  │   Company    │  │   Company    │  │   Generator      │ │
│  │              │  │   Generator  │  │   Generator  │  │                  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│                            Support Systems                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │    Name      │  │  Dirtiness   │  │    Date      │  │    Numeric       │ │
│  │  Generator   │  │   Engine     │  │  Formatter   │  │   Formatter      │ │
│  │  & Aliaser   │  │              │  │              │  │                  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GENERATION PIPELINE                                 │
│                                                                             │
│   Phase 1: Dimension Tables                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│   │  Investors  │    │   Private   │    │   Public    │                    │
│   │   25,000    │    │   35,000    │    │    6,000    │                    │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                    │
│          │                  │                  │                            │
│          └──────────────────┼──────────────────┘                            │
│                             ▼                                               │
│   Phase 2: Alias Generation                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Generate 1.1-1.3 aliases per entity → name_aliases.csv (~80K rows) │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│   Phase 3: Size Calibration                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Generate pilot deals (20K) → measure bytes/row → calculate target  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│   Phase 4: Deal Generation                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Generate deals.csv at calculated row count (~1.5-2M rows)          │  │
│   │  Simultaneously build truth_party2_mapping.csv                      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│   Phase 5: Post-Processing                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  - Update private_companies.investors_json from deals               │  │
│   │  - Inject staleness/phantom investors                               │  │
│   │  - Shuffle all tables                                               │  │
│   │  - Write meta.json with statistics                                  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Module Design

### 3.1 Core Modules

```
pandas_dataset_generator/
├── __init__.py
├── main.py                    # CLI entry point
├── generator.py               # Main DatasetGenerator class
├── config.py                  # Configuration management & defaults
├── rng.py                     # Reproducible RNG management
├── stats.py                   # Statistics tracking for meta.json
│
├── entities/
│   ├── __init__.py
│   ├── base.py               # BaseEntityGenerator abstract class
│   ├── investors.py          # InvestorGenerator
│   ├── private_companies.py  # PrivateCompanyGenerator
│   ├── public_companies.py   # PublicCompanyGenerator
│   ├── deals.py              # DealGenerator
│   └── aliases.py            # AliasGenerator
│
├── names/
│   ├── __init__.py
│   ├── generator.py          # Name generation logic
│   ├── templates.py          # Name templates and tokens
│   └── transforms.py         # Alias transformations
│
├── formatters/
│   ├── __init__.py
│   ├── dates.py              # Date formatting by source system
│   ├── numerics.py           # Numeric formatting with noise
│   └── json_fields.py        # JSON field generation
│
├── dirtiness/
│   ├── __init__.py
│   ├── engine.py             # DirtinessEngine main class
│   ├── anomalies.py          # Anomaly injection logic
│   └── rates.py              # Default anomaly rates
│
├── output/
│   ├── __init__.py
│   ├── csv_writer.py         # CSV output with proper escaping
│   ├── json_writer.py        # meta.json writer
│   └── calibrator.py         # Size calibration logic
│
└── utils/
    ├── __init__.py
    ├── distributions.py      # Statistical distributions
    └── validators.py         # Schema validation
```

### 3.2 Class Responsibilities

#### `DatasetGenerator` (generator.py)
- Main orchestrator class
- Manages generation pipeline phases
- Coordinates between entity generators
- Handles cross-table dependencies (deals → investors_json)

#### `ConfigManager` (config.py)
- Loads default configuration
- Merges user overrides
- Validates configuration parameters
- Exposes typed configuration access

#### `RNGManager` (rng.py)
- Wraps `numpy.random.Generator` with seed
- Provides named sub-streams for different tables
- Ensures reproducibility across runs

#### `DirtinessEngine` (dirtiness/engine.py)
- Central anomaly injection coordinator
- Tracks actual anomaly counts
- Provides `maybe_corrupt(field, value, anomaly_type)` interface

---

## 4. Data Model & Schemas

### 4.1 Entity ID Formats

| Entity Type | ID Format | Example |
|-------------|-----------|---------|
| Investor | `INV{7-digit}` | `INV0001234` |
| Private Company | `PVT{7-digit}` | `PVT0012345` |
| Public Company | `PUB{7-digit}` | `PUB0001001` |
| Deal | `D{9-digit}` | `D000001234` |

### 4.2 Schema Definitions (Python dataclasses)

```python
@dataclass
class InvestorSchema:
    investor_id: str                    # Non-null, unique
    investor_name_canonical: str        # Non-null
    investor_type: Optional[str]        # VC|PE|ANGEL|HEDGE_FUND|CORP_VENTURE|SOVEREIGN_FUND
    hq_country: Optional[str]           # ISO2
    founded_year: Optional[str]         # "1950"-"2022", some anomalies
    aum_usd_m: Optional[str]            # Numeric with formatting noise
    is_active: str                      # Y|N
    source_system: str                  # REF_FEED_A|REF_FEED_B|MANUAL
    last_updated_ts_raw: Optional[str]  # Mixed datetime formats

@dataclass
class PrivateCompanySchema:
    private_company_id: str
    company_name_canonical: str
    legal_name: Optional[str]
    country: Optional[str]
    sector: Optional[str]               # TECH|FINANCE|...|OTHER
    stage: Optional[str]                # SEED|SERIES_A|...|PRE_IPO
    founded_date_raw: Optional[str]
    employees_est: Optional[str]
    revenue_est_usd_m: Optional[str]
    investors_json: Optional[str]       # JSON array of investor names
    tags_json: Optional[str]            # JSON array of tags
    source_system: str
    last_updated_ts_raw: Optional[str]

@dataclass
class PublicCompanySchema:
    public_company_id: str
    company_name_canonical: str
    isin: Optional[str]                 # [A-Z]{2}[A-Z0-9]{10}
    ticker: Optional[str]
    exchange: Optional[str]             # LSE|NYSE|NASDAQ|...
    ticker_exchange_key: Optional[str]  # {ticker}:{exchange}
    country: Optional[str]
    sector: Optional[str]
    market_cap_raw: Optional[str]
    ipo_date_raw: Optional[str]
    status: str                         # ACTIVE|DELISTED
    source_system: str

@dataclass
class DealSchema:
    deal_id: str
    source_system: str                  # DEALS_FEED_US|DEALS_FEED_EU|DEALS_MANUAL
    ingestion_ts_raw: str
    deal_type: str                      # INVESTMENT|ACQUISITION|MERGER|...
    deal_status: str                    # ANNOUNCED|COMPLETED|WITHDRAWN
    announced_date_raw: Optional[str]
    closed_date_raw: Optional[str]
    party1_id: str                      # Reference to entity
    party1_type_hint: str               # INVESTOR|PRIVATE|PUBLIC
    party2_name_raw: str                # Fuzzy match target
    party2_entity_hint: Optional[str]   # INVESTOR|PRIVATE|PUBLIC|UNKNOWN
    deal_value_raw: Optional[str]
    deal_currency: Optional[str]
    stake_pct_raw: Optional[str]
    post_money_valuation_raw: Optional[str]
    pre_money_valuation_raw: Optional[str]
    deal_terms_json: Optional[str]
    notes: Optional[str]

@dataclass
class AliasSchema:
    canonical_entity_id: str
    canonical_entity_type: str          # INVESTOR|PRIVATE|PUBLIC
    canonical_name: str
    alias_name: str
    alias_type: str                     # SUFFIX_VARIANT|PUNCTUATION_VARIANT|...
    generated_by_rule: str
    is_high_confidence: str             # Y|N

@dataclass
class TruthMappingSchema:
    deal_id: str
    party2_resolved_entity_id: Optional[str]
    party2_resolved_entity_type: Optional[str]
    match_class: str                    # EXACT|ALIAS|NORMALIZED|TYPO|UNKNOWN
    match_confidence: str               # 0.0-1.0
    resolver_notes: Optional[str]
```

### 4.3 Categorical Value Distributions

#### Investor Types
```python
INVESTOR_TYPE_DIST = {
    "VC": 0.40,
    "PE": 0.25,
    "ANGEL": 0.12,
    "HEDGE_FUND": 0.08,
    "CORP_VENTURE": 0.10,
    "SOVEREIGN_FUND": 0.05
}
```

#### Company Sectors
```python
SECTOR_DIST = {
    "TECH": 0.33,
    "FINANCE": 0.10,
    "HEALTHCARE": 0.12,
    "INDUSTRIALS": 0.10,
    "CONSUMER": 0.12,
    "ENERGY": 0.06,
    "REAL_ESTATE": 0.05,
    "TELECOM": 0.04,
    "UTILITIES": 0.03,
    "OTHER": 0.05
}
```

#### Company Stages (Private)
```python
STAGE_DIST = {
    "SEED": 0.20,
    "SERIES_A": 0.22,
    "SERIES_B": 0.18,
    "SERIES_C": 0.15,
    "GROWTH": 0.12,
    "LATE_STAGE": 0.08,
    "PRE_IPO": 0.05
}
```

#### Deal Types
```python
DEAL_TYPE_DIST = {
    "INVESTMENT": 0.55,
    "ACQUISITION": 0.27,
    "MERGER": 0.10,
    "MINORITY_STAKE": 0.05,
    "JOINT_VENTURE": 0.03
}
```

#### Deal Status
```python
DEAL_STATUS_DIST = {
    "ANNOUNCED": 0.45,
    "COMPLETED": 0.45,
    "WITHDRAWN": 0.10
}
```

---

## 5. Generation Pipeline

### 5.1 Phase 1: Dimension Tables

```python
def generate_dimension_tables(self) -> DimensionTables:
    """Generate all entity dictionaries (dimension tables)."""

    # Generate in parallel (no dependencies)
    investors = self.investor_gen.generate(n=self.config.n_investors)
    private_cos = self.private_co_gen.generate(n=self.config.n_private)
    public_cos = self.public_co_gen.generate(n=self.config.n_public)

    # Build entity registry for deal generation
    self.entity_registry = EntityRegistry(investors, private_cos, public_cos)

    return DimensionTables(investors, private_cos, public_cos)
```

### 5.2 Phase 2: Alias Generation

```python
def generate_aliases(self) -> pd.DataFrame:
    """Generate name aliases for all entities."""

    all_aliases = []

    for entity_type, entities, avg_aliases in [
        ("INVESTOR", self.investors, 1.2),
        ("PRIVATE", self.private_cos, 1.3),
        ("PUBLIC", self.public_cos, 1.1)
    ]:
        for entity in entities:
            n_aliases = self.rng.poisson(avg_aliases)
            aliases = self.alias_gen.generate_aliases(
                entity_id=entity.id,
                entity_type=entity_type,
                canonical_name=entity.canonical_name,
                n_aliases=n_aliases
            )
            all_aliases.extend(aliases)

    # Inject controlled collisions
    all_aliases = self._inject_alias_collisions(all_aliases)

    return pd.DataFrame(all_aliases)
```

### 5.3 Phase 3: Size Calibration

```python
def calibrate_deal_count(self) -> int:
    """Determine deals row count to hit target size."""

    # Generate pilot sample
    pilot_deals = self.deal_gen.generate(n=self.config.pilot_deals_rows)

    # Write to temp file and measure
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        pilot_deals.to_csv(f, index=False)
        pilot_size = os.path.getsize(f.name)

    # Calculate bytes per row (excluding header)
    header_bytes = len(','.join(pilot_deals.columns).encode()) + 1
    bytes_per_row = (pilot_size - header_bytes) / len(pilot_deals)

    # Calculate target rows
    base_bytes = self._calculate_base_bytes()
    target_bytes = self.config.target_total_size_mb * 1024 * 1024
    available_bytes = target_bytes - base_bytes

    deals_rows = max(
        self.config.min_deals_rows,
        int(np.ceil(available_bytes / bytes_per_row))
    )

    return deals_rows
```

### 5.4 Phase 4: Deal Generation

```python
def generate_deals(self, n_rows: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate deals and truth mapping simultaneously."""

    deals = []
    truth_mappings = []

    for i in range(n_rows):
        deal, truth = self.deal_gen.generate_single_deal(
            deal_num=i,
            entity_registry=self.entity_registry,
            alias_registry=self.alias_registry
        )
        deals.append(deal)
        truth_mappings.append(truth)

    # Inject duplicate deals
    deals = self._inject_duplicate_deals(deals)

    # Shuffle (destroy ordering)
    deals = self.rng.permutation(deals)

    return pd.DataFrame(deals), pd.DataFrame(truth_mappings)
```

### 5.5 Phase 5: Post-Processing

```python
def post_process(self) -> None:
    """Update derived fields and finalize data."""

    # Build investors_json from deals
    self._build_investors_json_from_deals()

    # Inject staleness and phantoms
    self._inject_investor_list_inconsistencies()

    # Shuffle all dimension tables
    self.investors = self.investors.sample(frac=1, random_state=self.seed)
    self.private_cos = self.private_cos.sample(frac=1, random_state=self.seed)
    self.public_cos = self.public_cos.sample(frac=1, random_state=self.seed)

    # Collect final statistics
    self.stats.finalize()
```

---

## 6. Name Generation System

### 6.1 Name Templates

#### Investor Names
```python
INVESTOR_PREFIXES = [
    "Summit", "Northbridge", "Apex", "Horizon", "Vanguard", "Pinnacle",
    "Sterling", "Atlas", "Meridian", "Evergreen", "Lighthouse", "Keystone",
    "Granite", "Ironwood", "Redwood", "Bluerock", "Silverstone", "Goldpoint",
    "Blackridge", "Whitehorse", "Greenfield", "Oakwood", "Cedarpoint", "Pinehill",
    ...  # ~100 tokens
]

INVESTOR_SUFFIXES = [
    "Capital", "Partners", "Ventures", "Management", "Holdings", "Group",
    "Investments", "Advisors", "Equity", "Associates", "Fund", "Asset Management"
]

# Pattern: {Prefix1} [Prefix2] {Suffix}
# Examples: "Summit Capital", "Northbridge Apex Partners"
```

#### Company Names
```python
COMPANY_WORDS = [
    "Quantum", "Cyber", "Data", "Cloud", "Neural", "Vertex", "Nexus", "Synapse",
    "Vector", "Matrix", "Helix", "Prism", "Zenith", "Kinetic", "Dynamic", "Unified",
    "Global", "Integrated", "Advanced", "Smart", "Innovative", "Digital", "Modern",
    ...  # ~150 tokens
]

COMPANY_DOMAIN_SUFFIXES = [
    "Technologies", "Systems", "Labs", "Analytics", "Networks", "Health",
    "Energy", "Finance", "Solutions", "Services", "Dynamics", "Innovations",
    "Platforms", "Software", "AI", "Bio", "Med", "Pharma", "Therapeutics"
]

LEGAL_SUFFIXES = {
    "Inc": 0.25,
    "Ltd": 0.20,
    "PLC": 0.08,
    "LLC": 0.10,
    "GmbH": 0.05,
    "S.A.": 0.05,
    "": 0.27  # No suffix
}
```

### 6.2 Alias Transformations

```python
class AliasTransform(Enum):
    SUFFIX_VARIANT = "suffix_variant"           # Inc ↔ Incorporated
    PUNCTUATION_VARIANT = "punctuation_variant" # Remove/add commas, dots
    CASING_VARIANT = "casing_variant"           # UPPER/lower/Title
    TOKEN_DROP = "token_drop"                   # Remove Holdings/Group
    ABBREVIATION = "abbreviation"               # International → Intl
    LEGAL_NAME = "legal_name"                   # Use legal_name field

SUFFIX_EXPANSIONS = {
    "Inc": ["Incorporated", "Inc.", "INC"],
    "Ltd": ["Limited", "Ltd.", "LTD"],
    "Corp": ["Corporation", "Corp.", "CORP"],
    "Co": ["Company", "Co.", "CO"],
    "Intl": ["International", "Int'l", "INTL"],
    "Tech": ["Technologies", "Technology"],
    "Mgmt": ["Management"],
}

DROPPABLE_TOKENS = ["Holdings", "Group", "Partners", "The"]
```

### 6.3 Name Generation Algorithm

```python
def generate_investor_name(self) -> str:
    """Generate a canonical investor name."""

    # Decide pattern complexity (1-2 prefix words)
    n_prefixes = self.rng.choice([1, 2], p=[0.7, 0.3])

    # Sample prefixes without replacement
    prefixes = self.rng.choice(INVESTOR_PREFIXES, size=n_prefixes, replace=False)

    # Sample suffix
    suffix = self.rng.choice(INVESTOR_SUFFIXES)

    return " ".join([*prefixes, suffix])

def generate_company_name(self, include_legal_suffix: bool = True) -> Tuple[str, str]:
    """Generate canonical and legal company names."""

    # Core name: 1-2 words + domain suffix
    n_words = self.rng.choice([1, 2], p=[0.4, 0.6])
    words = self.rng.choice(COMPANY_WORDS, size=n_words, replace=False)
    domain = self.rng.choice(COMPANY_DOMAIN_SUFFIXES)

    core_name = " ".join([*words, domain])

    # Legal suffix
    if include_legal_suffix:
        legal_suffix = self.rng.choice(
            list(LEGAL_SUFFIXES.keys()),
            p=list(LEGAL_SUFFIXES.values())
        )
        legal_name = f"{core_name} {legal_suffix}".strip()
    else:
        legal_name = core_name

    return core_name, legal_name
```

---

## 7. Data Dirtiness Engine

### 7.1 Anomaly Rate Configuration

```python
@dataclass
class AnomalyRates:
    # Investor table
    p_missing_investor_type: float = 0.01
    p_missing_country: float = 0.008
    p_future_founded_year: float = 0.002
    p_very_old_founded_year: float = 0.001
    p_aum_commas: float = 0.05
    p_aum_dollar_sign: float = 0.02
    p_aum_na_string: float = 0.005
    p_duplicate_investor_name: float = 0.003
    p_near_duplicate_investor_name: float = 0.006

    # Private company table
    p_missing_legal_name: float = 0.02
    p_missing_sector: float = 0.015
    p_employees_unknown: float = 0.01
    p_employees_negative: float = 0.001
    p_founded_after_first_deal: float = 0.004

    # Public company table
    p_missing_isin: float = 0.01
    p_bad_isin: float = 0.003
    p_missing_ticker: float = 0.02
    p_mcap_commas: float = 0.08
    p_mcap_na: float = 0.01
    p_mcap_symbol: float = 0.02

    # Deals table
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

    # Date anomalies
    p_invalid_date_string: float = 0.006
    p_missing_announced_date: float = 0.02

    # Alias anomalies
    p_alias_collision: float = 0.002

    # investors_json consistency
    p_investor_list_stale_drop: float = 0.07
    p_investor_list_phantom_add: float = 0.03
    p_investor_list_duplicates: float = 0.02
```

### 7.2 Dirtiness Engine Interface

```python
class DirtinessEngine:
    """Centralized anomaly injection with tracking."""

    def __init__(self, rates: AnomalyRates, rng: np.random.Generator):
        self.rates = rates
        self.rng = rng
        self.anomaly_counts = defaultdict(int)

    def maybe_inject(self, anomaly_type: str, value: Any,
                     corrupt_fn: Callable) -> Any:
        """Conditionally inject an anomaly based on rate."""
        rate = getattr(self.rates, f"p_{anomaly_type}", 0.0)
        if self.rng.random() < rate:
            self.anomaly_counts[anomaly_type] += 1
            return corrupt_fn(value)
        return value

    def maybe_null(self, anomaly_type: str, value: Any) -> Optional[Any]:
        """Conditionally make a value null."""
        return self.maybe_inject(anomaly_type, value, lambda _: None)

    def maybe_format_numeric(self, value: float,
                             commas_type: str,
                             symbol_type: str,
                             na_type: str) -> str:
        """Apply numeric formatting noise."""
        # N/A string
        if self.rng.random() < getattr(self.rates, f"p_{na_type}", 0):
            self.anomaly_counts[na_type] += 1
            return "N/A"

        result = str(value)

        # Commas
        if self.rng.random() < getattr(self.rates, f"p_{commas_type}", 0):
            self.anomaly_counts[commas_type] += 1
            result = f"{value:,.0f}" if value == int(value) else f"{value:,.2f}"

        # Currency symbol
        if self.rng.random() < getattr(self.rates, f"p_{symbol_type}", 0):
            self.anomaly_counts[symbol_type] += 1
            result = "$" + result

        return result

    def get_statistics(self) -> Dict[str, int]:
        """Return anomaly counts for meta.json."""
        return dict(self.anomaly_counts)
```

### 7.3 Anomaly Injection Examples

```python
# Missing value injection
investor_type = self.dirtiness.maybe_null(
    "missing_investor_type",
    self._sample_investor_type()
)

# Numeric formatting noise
aum = self.dirtiness.maybe_format_numeric(
    value=self._sample_aum(),
    commas_type="aum_commas",
    symbol_type="aum_dollar_sign",
    na_type="aum_na_string"
)

# Outlier injection
deal_value = self.dirtiness.maybe_inject(
    "value_outlier_huge",
    base_value,
    lambda v: v * self.rng.uniform(100, 1000)  # Make it huge
)

# Invalid date injection
date_str = self.dirtiness.maybe_inject(
    "invalid_date_string",
    valid_date,
    lambda _: self.rng.choice(["2021-02-30", "13/40/2020", "2099-07-15"])
)
```

---

## 8. Date/Time Formatting System

### 8.1 Source System → Format Mapping

```python
DATE_FORMATS_BY_SOURCE = {
    "DEALS_FEED_US": {
        "MM/DD/YYYY": 0.80,  # 03/15/2023
        "YYYY-MM-DD": 0.15,  # 2023-03-15 (ISO)
        "Mon DD, YYYY": 0.05  # Mar 15, 2023
    },
    "DEALS_FEED_EU": {
        "DD/MM/YYYY": 0.80,  # 15/03/2023
        "YYYY-MM-DD": 0.15,  # ISO
        "DD Mon YYYY": 0.05  # 15 Mar 2023
    },
    "DEALS_MANUAL": {
        "YYYY-MM-DD": 0.60,  # ISO
        "YYYY/MM/DD": 0.20,  # 2023/03/15
        "Mon DD, YYYY": 0.20  # Mar 15, 2023
    },
    "REF_FEED_A": {
        "YYYY-MM-DD": 0.90,
        "YYYYMMDD": 0.10
    },
    "REF_FEED_B": {
        "DD-MMM-YYYY": 0.70,  # 15-Mar-2023
        "YYYY-MM-DD": 0.30
    },
    "MANUAL": {
        "YYYY-MM-DD": 0.50,
        "MM/DD/YYYY": 0.30,
        "DD/MM/YYYY": 0.20
    }
}

TIMESTAMP_FORMATS_BY_SOURCE = {
    "DEALS_FEED_US": {
        "YYYY-MM-DD HH:MM:SS": 0.60,
        "MM/DD/YYYY HH:MM:SS": 0.30,
        "epoch_ms": 0.10
    },
    "DEALS_FEED_EU": {
        "YYYY-MM-DD HH:MM:SS": 0.60,
        "DD/MM/YYYY HH:MM:SS": 0.30,
        "YYYY-MM-DDTHH:MM:SS": 0.10  # ISO 8601
    },
    ...
}
```

### 8.2 Date Formatter Implementation

```python
class DateFormatter:
    """Format dates based on source system."""

    def __init__(self, rng: np.random.Generator):
        self.rng = rng

    def format_date(self, date: datetime.date, source_system: str) -> str:
        """Format a date according to source system conventions."""
        formats = DATE_FORMATS_BY_SOURCE.get(source_system, {"YYYY-MM-DD": 1.0})

        # Sample format based on distribution
        format_str = self.rng.choice(
            list(formats.keys()),
            p=list(formats.values())
        )

        return self._apply_format(date, format_str)

    def _apply_format(self, date: datetime.date, format_str: str) -> str:
        """Apply specific format string."""
        format_map = {
            "YYYY-MM-DD": "%Y-%m-%d",
            "MM/DD/YYYY": "%m/%d/%Y",
            "DD/MM/YYYY": "%d/%m/%Y",
            "Mon DD, YYYY": "%b %d, %Y",
            "DD Mon YYYY": "%d %b %Y",
            "YYYY/MM/DD": "%Y/%m/%d",
            "YYYYMMDD": "%Y%m%d",
            "DD-MMM-YYYY": "%d-%b-%Y",
        }
        return date.strftime(format_map[format_str])

    def generate_invalid_date(self) -> str:
        """Generate an invalid date string for anomaly injection."""
        invalid_dates = [
            "2021-02-30",   # Feb 30 doesn't exist
            "2022-13-15",   # Month 13
            "13/40/2020",   # Day 40
            "2099-07-15",   # Far future
            "00/00/0000",   # All zeros
            "2021-00-15",   # Month 0
            "not_a_date",   # Text
            "N/A",
            "",
        ]
        return self.rng.choice(invalid_dates)
```

---

## 9. Numeric Generation & Formatting

### 9.1 Base Distributions

```python
class NumericDistributions:
    """Statistical distributions for numeric fields."""

    @staticmethod
    def sample_aum_usd_m(rng: np.random.Generator) -> float:
        """AUM: lognormal, median ~3000 ($3B), range 50-200000."""
        return np.clip(
            rng.lognormal(mean=np.log(3000), sigma=1.2),
            50, 200000
        )

    @staticmethod
    def sample_employees(rng: np.random.Generator) -> int:
        """Employees: lognormal, median ~120, range 5-50000."""
        return int(np.clip(
            rng.lognormal(mean=np.log(120), sigma=1.5),
            5, 50000
        ))

    @staticmethod
    def sample_revenue_usd_m(rng: np.random.Generator) -> float:
        """Revenue: lognormal, median ~30, range 0.1-20000."""
        return np.clip(
            rng.lognormal(mean=np.log(30), sigma=1.8),
            0.1, 20000
        )

    @staticmethod
    def sample_market_cap_usd_m(rng: np.random.Generator) -> float:
        """Market cap: lognormal, median ~12000 ($12B), range 200-4000000."""
        return np.clip(
            rng.lognormal(mean=np.log(12000), sigma=1.3),
            200, 4000000
        )

    @staticmethod
    def sample_deal_value_usd_m(rng: np.random.Generator, deal_type: str) -> float:
        """Deal value by type."""
        params = {
            "INVESTMENT": (15, 1.5, 0.1, 500),
            "ACQUISITION": (250, 1.8, 1, 50000),
            "MERGER": (400, 1.6, 10, 80000),
            "MINORITY_STAKE": (30, 1.4, 0.5, 1000),
            "JOINT_VENTURE": (100, 1.5, 5, 5000),
        }
        median, sigma, min_val, max_val = params.get(deal_type, (100, 1.5, 1, 10000))
        return np.clip(
            rng.lognormal(mean=np.log(median), sigma=sigma),
            min_val, max_val
        )

    @staticmethod
    def sample_stake_pct(rng: np.random.Generator, deal_type: str) -> float:
        """Stake percentage by deal type."""
        if deal_type in ("ACQUISITION", "MERGER"):
            # Mostly 100%, sometimes partial
            if rng.random() < 0.92:
                return 100.0
            else:
                return rng.uniform(50, 99)
        elif deal_type == "INVESTMENT":
            # Beta-ish in 1-35%
            return rng.beta(2, 6) * 34 + 1  # Range ~1-35
        elif deal_type == "MINORITY_STAKE":
            return rng.uniform(1, 49)
        else:  # JOINT_VENTURE
            return rng.choice([50, 49, 51, 33.33, 25])
```

### 9.2 Numeric Formatter

```python
class NumericFormatter:
    """Format numeric values with controlled noise."""

    def __init__(self, rng: np.random.Generator, dirtiness: DirtinessEngine):
        self.rng = rng
        self.dirtiness = dirtiness

    def format_monetary(self, value: float,
                        commas_rate_key: str,
                        symbol_rate_key: str,
                        na_rate_key: str,
                        currency: str = "USD") -> str:
        """Format monetary value with potential noise."""

        # Maybe return N/A
        if self.rng.random() < self.dirtiness.rates.__dict__.get(na_rate_key, 0):
            self.dirtiness.anomaly_counts[na_rate_key] += 1
            return "N/A"

        # Base formatting
        if value == int(value):
            result = str(int(value))
        else:
            result = f"{value:.2f}"

        # Maybe add commas
        if self.rng.random() < self.dirtiness.rates.__dict__.get(commas_rate_key, 0):
            self.dirtiness.anomaly_counts[commas_rate_key] += 1
            result = f"{value:,.0f}" if value == int(value) else f"{value:,.2f}"

        # Maybe add currency symbol
        if self.rng.random() < self.dirtiness.rates.__dict__.get(symbol_rate_key, 0):
            self.dirtiness.anomaly_counts[symbol_rate_key] += 1
            symbols = {"USD": "$", "GBP": "£", "EUR": "€", "CHF": "CHF ", "SGD": "S$"}
            result = symbols.get(currency, "$") + result

        return result
```

---

## 10. Party2 Fuzzy Match Model

### 10.1 Party2 Entity Type Selection

```python
PARTY2_TYPE_BY_DEAL_TYPE = {
    "INVESTMENT": {
        "PRIVATE": 0.92,
        "PUBLIC": 0.06,
        "UNKNOWN": 0.02
    },
    "ACQUISITION": {
        "PRIVATE": 0.75,
        "PUBLIC": 0.20,
        "UNKNOWN": 0.05
    },
    "MERGER": {
        "PRIVATE": 0.50,
        "PUBLIC": 0.45,
        "UNKNOWN": 0.05
    },
    "MINORITY_STAKE": {
        "PRIVATE": 0.70,
        "PUBLIC": 0.25,
        "UNKNOWN": 0.05
    },
    "JOINT_VENTURE": {
        "PRIVATE": 0.60,
        "PUBLIC": 0.35,
        "UNKNOWN": 0.05
    }
}
```

### 10.2 Name Match Class Distribution

```python
MATCH_CLASS_DIST = {
    "EXACT_CANONICAL": 0.55,   # Exact canonical name
    "ALIAS_FROM_TABLE": 0.25,  # Use an alias from name_aliases
    "NORMALIZED_VARIANT": 0.10, # Strip punctuation, suffix tweaks
    "TYPO_1_EDIT": 0.05,       # One character edit
    "UNKNOWN_EXTERNAL": 0.05   # Synthetic name not in any table
}
```

### 10.3 Party2 Name Generator

```python
class Party2NameGenerator:
    """Generate party2_name_raw with controlled fuzziness."""

    def __init__(self, rng: np.random.Generator,
                 alias_registry: AliasRegistry,
                 name_generator: NameGenerator):
        self.rng = rng
        self.alias_registry = alias_registry
        self.name_generator = name_generator

    def generate(self, deal_type: str,
                 entity_registry: EntityRegistry) -> Tuple[str, TruthMapping]:
        """Generate party2_name_raw and ground truth mapping."""

        # Step 1: Choose entity type
        type_dist = PARTY2_TYPE_BY_DEAL_TYPE[deal_type]
        party2_type = self.rng.choice(
            list(type_dist.keys()),
            p=list(type_dist.values())
        )

        # Step 2: Choose match class
        match_class = self.rng.choice(
            list(MATCH_CLASS_DIST.keys()),
            p=list(MATCH_CLASS_DIST.values())
        )

        # Step 3: Generate name based on class
        if party2_type == "UNKNOWN" or match_class == "UNKNOWN_EXTERNAL":
            # Generate synthetic unknown name
            name = self.name_generator.generate_unknown_company()
            return name, TruthMapping(
                entity_id=None,
                entity_type=None,
                match_class="UNKNOWN",
                confidence=0.0
            )

        # Select actual entity
        entity = entity_registry.sample_entity(party2_type, self.rng)

        if match_class == "EXACT_CANONICAL":
            name = entity.canonical_name
            confidence = 1.0

        elif match_class == "ALIAS_FROM_TABLE":
            aliases = self.alias_registry.get_aliases(entity.id)
            if aliases:
                name = self.rng.choice(aliases)
                confidence = 0.95
            else:
                name = entity.canonical_name
                confidence = 1.0

        elif match_class == "NORMALIZED_VARIANT":
            name = self._apply_normalization(entity.canonical_name)
            confidence = 0.85

        elif match_class == "TYPO_1_EDIT":
            name = self._introduce_typo(entity.canonical_name)
            confidence = 0.70

        return name, TruthMapping(
            entity_id=entity.id,
            entity_type=party2_type,
            match_class=match_class,
            confidence=confidence
        )

    def _apply_normalization(self, name: str) -> str:
        """Apply normalization transformations."""
        transforms = [
            lambda s: s.replace(",", ""),           # Remove commas
            lambda s: s.replace(".", ""),           # Remove dots
            lambda s: s.replace("  ", " "),         # Normalize spaces
            lambda s: s.lower(),                    # Lowercase
            lambda s: s.upper(),                    # Uppercase
            lambda s: self._swap_suffix(s),         # Inc -> Incorporated
        ]
        transform = self.rng.choice(transforms)
        return transform(name)

    def _introduce_typo(self, name: str) -> str:
        """Introduce a single-character typo."""
        if len(name) < 3:
            return name

        pos = self.rng.integers(1, len(name) - 1)
        typo_type = self.rng.choice(["drop", "swap", "replace", "double"])

        if typo_type == "drop":
            return name[:pos] + name[pos+1:]
        elif typo_type == "swap" and pos < len(name) - 1:
            return name[:pos] + name[pos+1] + name[pos] + name[pos+2:]
        elif typo_type == "replace":
            char = self.rng.choice(list("abcdefghijklmnopqrstuvwxyz"))
            return name[:pos] + char + name[pos+1:]
        elif typo_type == "double":
            return name[:pos] + name[pos] + name[pos:]

        return name
```

---

## 11. Size Calibration Algorithm

### 11.1 Calibration Process

```python
def calibrate_target_size(config: Config,
                          dimension_tables: DimensionTables,
                          rng: np.random.Generator) -> int:
    """Calculate required deals row count to hit target size."""

    # Step 1: Measure dimension table sizes
    base_sizes = {
        "investors": measure_csv_size(dimension_tables.investors),
        "private_companies": measure_csv_size(dimension_tables.private_companies),
        "public_companies": measure_csv_size(dimension_tables.public_companies),
        "name_aliases": measure_csv_size(dimension_tables.aliases),
    }
    base_bytes = sum(base_sizes.values())

    # Step 2: Generate pilot deals and measure
    pilot_deals = generate_pilot_deals(
        n=config.pilot_deals_rows,  # Default: 20,000
        dimension_tables=dimension_tables,
        rng=rng
    )
    pilot_bytes = measure_csv_size(pilot_deals)

    # Calculate bytes per row (excluding header)
    header_bytes = estimate_header_bytes(pilot_deals.columns)
    bytes_per_row = (pilot_bytes - header_bytes) / len(pilot_deals)

    # Step 3: Calculate target deals rows
    target_bytes = config.target_total_size_mb * 1024 * 1024
    available_for_deals = target_bytes - base_bytes

    # Account for truth mapping file (roughly same size as deals)
    if config.include_truth_in_target:
        # Truth file is ~30% size of deals (fewer columns)
        available_for_deals = available_for_deals / 1.3

    deals_rows = int(np.ceil(available_for_deals / bytes_per_row))

    # Apply bounds
    deals_rows = max(config.min_deals_rows, deals_rows)

    # Log calibration results
    logger.info(f"Calibration complete:")
    logger.info(f"  Base tables: {base_bytes / 1024 / 1024:.2f} MB")
    logger.info(f"  Bytes per deal row: {bytes_per_row:.1f}")
    logger.info(f"  Target deals rows: {deals_rows:,}")

    return deals_rows
```

### 11.2 Size Estimation Helper

```python
def measure_csv_size(df: pd.DataFrame) -> int:
    """Measure CSV size without writing to disk."""
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return len(buffer.getvalue().encode('utf-8'))

def estimate_header_bytes(columns: List[str]) -> int:
    """Estimate header row bytes."""
    return len(','.join(columns).encode('utf-8')) + 1  # +1 for newline
```

---

## 12. Implementation Phases

### Phase 1: Foundation (Core Infrastructure)
**Estimated Complexity: Medium**

1. **Project Setup**
   - Create package structure
   - Set up pyproject.toml / setup.py
   - Configure logging

2. **Configuration System** (`config.py`)
   - Define all default parameters
   - Create `Config` dataclass
   - Implement config loading/validation

3. **RNG Management** (`rng.py`)
   - Implement `RNGManager` with seed control
   - Create named sub-streams for tables
   - Ensure reproducibility

4. **Statistics Tracking** (`stats.py`)
   - Implement `StatisticsTracker`
   - Track row counts, anomaly counts
   - Prepare meta.json structure

### Phase 2: Name Generation System
**Estimated Complexity: Medium**

1. **Name Templates** (`names/templates.py`)
   - Define all token lists (prefixes, suffixes, words)
   - Define distribution weights

2. **Name Generator** (`names/generator.py`)
   - Implement investor name generation
   - Implement company name generation
   - Implement legal name generation

3. **Alias Transformations** (`names/transforms.py`)
   - Implement all transform types
   - Suffix expansions/contractions
   - Punctuation/casing variants
   - Token dropping
   - Typo introduction

### Phase 3: Formatters
**Estimated Complexity: Medium**

1. **Date Formatter** (`formatters/dates.py`)
   - Source-system-aware formatting
   - Invalid date generation
   - Timestamp formatting

2. **Numeric Formatter** (`formatters/numerics.py`)
   - Comma formatting
   - Currency symbols
   - N/A string injection

3. **JSON Field Generator** (`formatters/json_fields.py`)
   - Valid JSON array generation
   - Valid JSON object generation
   - Corrupt JSON injection

### Phase 4: Dirtiness Engine
**Estimated Complexity: Medium**

1. **Anomaly Rates** (`dirtiness/rates.py`)
   - Define `AnomalyRates` dataclass
   - All rate defaults

2. **Dirtiness Engine** (`dirtiness/engine.py`)
   - Implement `DirtinessEngine` class
   - `maybe_inject()` method
   - Anomaly tracking

3. **Specific Anomalies** (`dirtiness/anomalies.py`)
   - Outlier injection
   - Invalid reference injection
   - Duplicate injection

### Phase 5: Entity Generators
**Estimated Complexity: High**

1. **Base Generator** (`entities/base.py`)
   - Abstract `BaseEntityGenerator`
   - Common generation patterns

2. **Investor Generator** (`entities/investors.py`)
   - Full schema implementation
   - All investor-specific anomalies
   - Duplicate name injection

3. **Private Company Generator** (`entities/private_companies.py`)
   - Full schema implementation
   - `investors_json` placeholder (filled later)
   - Founded date vs deal date validation

4. **Public Company Generator** (`entities/public_companies.py`)
   - Full schema implementation
   - ISIN generation
   - Ticker/exchange key generation

5. **Alias Generator** (`entities/aliases.py`)
   - Generate aliases per entity
   - Controlled collision injection
   - Build alias registry

### Phase 6: Deal Generator
**Estimated Complexity: High**

1. **Party Selection Logic** (`entities/deals.py`)
   - Party1 selection by deal type
   - Zipfian weighting for frequent actors
   - Bad reference injection

2. **Party2 Name Generation**
   - Match class selection
   - Name variant generation
   - Truth mapping creation

3. **Value/Valuation Logic**
   - Deal value sampling by type
   - Pre/post money calculation
   - Contradiction injection

4. **Full Deal Generation**
   - All 18 columns
   - Date sequencing logic
   - Duplicate deal injection

### Phase 7: Pipeline Integration
**Estimated Complexity: High**

1. **Main Generator** (`generator.py`)
   - Orchestrate all phases
   - Size calibration integration
   - Cross-table updates

2. **Post-Processing**
   - Build `investors_json` from deals
   - Inject staleness/phantoms
   - Shuffle all tables

3. **Output Writing** (`output/csv_writer.py`)
   - Proper CSV escaping
   - UTF-8 encoding
   - Chunk writing for large files

### Phase 8: CLI and Testing
**Estimated Complexity: Medium**

1. **CLI Interface** (`main.py`)
   - Argument parsing
   - Progress reporting
   - Error handling

2. **Unit Tests**
   - Test each generator
   - Test formatters
   - Test dirtiness injection

3. **Integration Tests**
   - Full generation test
   - Size accuracy test
   - Reproducibility test

---

## 13. Testing Strategy

### 13.1 Unit Tests

```python
# tests/test_name_generator.py
def test_investor_name_format():
    """Investor names follow expected pattern."""
    rng = np.random.default_rng(42)
    gen = NameGenerator(rng)
    name = gen.generate_investor_name()
    assert len(name.split()) >= 2
    assert any(suffix in name for suffix in ["Capital", "Partners", "Ventures", ...])

def test_alias_transforms():
    """Alias transforms produce valid variants."""
    transforms = AliasTransforms()
    assert transforms.expand_suffix("Acme Inc") in ["Acme Incorporated", "Acme Inc."]
    assert transforms.drop_tokens("Acme Holdings Ltd") == "Acme Ltd"

# tests/test_date_formatter.py
def test_date_format_by_source():
    """Dates format according to source system."""
    formatter = DateFormatter(np.random.default_rng(42))
    date = datetime.date(2023, 3, 15)

    # US format tends toward MM/DD/YYYY
    us_formats = [formatter.format_date(date, "DEALS_FEED_US") for _ in range(100)]
    assert sum("03/15/2023" in f or "2023-03-15" in f for f in us_formats) > 80

# tests/test_dirtiness.py
def test_anomaly_rates():
    """Anomalies injected at expected rates."""
    engine = DirtinessEngine(AnomalyRates(), np.random.default_rng(42))

    results = [engine.maybe_null("missing_investor_type", "VC") for _ in range(10000)]
    null_rate = sum(r is None for r in results) / len(results)

    # Should be close to 0.01 (1%)
    assert 0.005 < null_rate < 0.02
```

### 13.2 Integration Tests

```python
# tests/test_generator.py
def test_full_generation_reproducibility():
    """Same seed produces identical output."""
    gen1 = DatasetGenerator(seed=12345, target_total_size_mb=10)
    gen2 = DatasetGenerator(seed=12345, target_total_size_mb=10)

    output1 = gen1.generate()
    output2 = gen2.generate()

    assert output1.investors.equals(output2.investors)
    assert output1.deals.equals(output2.deals)

def test_target_size_accuracy():
    """Generated data hits target size within 5%."""
    gen = DatasetGenerator(seed=42, target_total_size_mb=50)
    output = gen.generate()

    total_size = sum(
        measure_csv_size(df) for df in [
            output.investors, output.private_cos,
            output.public_cos, output.deals, output.aliases
        ]
    )

    target_bytes = 50 * 1024 * 1024
    assert abs(total_size - target_bytes) / target_bytes < 0.05

def test_referential_integrity():
    """Party1 IDs reference valid entities (except injected bad refs)."""
    gen = DatasetGenerator(seed=42)
    output = gen.generate()

    valid_ids = set(output.investors['investor_id']) | \
                set(output.private_cos['private_company_id']) | \
                set(output.public_cos['public_company_id'])

    bad_refs = output.deals[~output.deals['party1_id'].isin(valid_ids)]
    bad_ref_rate = len(bad_refs) / len(output.deals)

    # Should match p_bad_party1_id rate (~0.2%)
    assert bad_ref_rate < 0.01  # Allow some margin
```

### 13.3 Validation Tests

```python
# tests/test_validation.py
def test_anomaly_counts_match_meta():
    """meta.json anomaly counts match actual data."""
    gen = DatasetGenerator(seed=42, target_total_size_mb=10)
    output = gen.generate()
    meta = output.meta

    # Count actual invalid dates in deals
    deals = output.deals
    actual_invalid_dates = count_invalid_dates(deals['announced_date_raw'])

    assert abs(actual_invalid_dates - meta['anomaly_counts']['invalid_date_string']) < 10

def test_fuzzy_match_solvability():
    """Party2 names can be matched using truth file."""
    gen = DatasetGenerator(seed=42)
    output = gen.generate()

    # For non-UNKNOWN matches, verify the truth mapping is correct
    truth = output.truth_mapping
    known_matches = truth[truth['match_class'] != 'UNKNOWN']

    for _, row in known_matches.head(100).iterrows():
        entity_id = row['party2_resolved_entity_id']
        entity_type = row['party2_resolved_entity_type']

        if entity_type == 'INVESTOR':
            entity = output.investors[output.investors['investor_id'] == entity_id]
            assert len(entity) == 1
```

---

## 14. File Structure

```
pandas_dataset_generator/
├── pyproject.toml              # Package configuration
├── README.md                   # Usage documentation
├── LICENSE
│
├── src/
│   └── pandas_dataset_generator/
│       ├── __init__.py
│       ├── __main__.py         # python -m entry point
│       ├── main.py             # CLI implementation
│       ├── generator.py        # Main DatasetGenerator class
│       ├── config.py           # Configuration management
│       ├── rng.py              # RNG management
│       ├── stats.py            # Statistics tracking
│       │
│       ├── entities/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── investors.py
│       │   ├── private_companies.py
│       │   ├── public_companies.py
│       │   ├── deals.py
│       │   └── aliases.py
│       │
│       ├── names/
│       │   ├── __init__.py
│       │   ├── generator.py
│       │   ├── templates.py
│       │   └── transforms.py
│       │
│       ├── formatters/
│       │   ├── __init__.py
│       │   ├── dates.py
│       │   ├── numerics.py
│       │   └── json_fields.py
│       │
│       ├── dirtiness/
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── anomalies.py
│       │   └── rates.py
│       │
│       ├── output/
│       │   ├── __init__.py
│       │   ├── csv_writer.py
│       │   ├── json_writer.py
│       │   └── calibrator.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── distributions.py
│           └── validators.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_config.py
│   ├── test_name_generator.py
│   ├── test_date_formatter.py
│   ├── test_numeric_formatter.py
│   ├── test_dirtiness.py
│   ├── test_investors.py
│   ├── test_private_companies.py
│   ├── test_public_companies.py
│   ├── test_deals.py
│   ├── test_aliases.py
│   ├── test_generator.py       # Integration tests
│   └── test_validation.py
│
└── examples/
    ├── generate_small.py       # Generate 10MB test set
    ├── generate_full.py        # Generate 100MB full set
    └── custom_config.py        # Custom configuration example
```

---

## 15. Dependencies

### 15.1 Core Dependencies

```toml
[project]
dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
]
```

### 15.2 Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pandas-stubs>=2.0.0",
]
```

### 15.3 Why Minimal Dependencies?

- **NumPy**: Required for efficient random number generation (numpy.random.Generator) and statistical distributions (lognormal, beta, etc.)
- **Pandas**: Required for DataFrame operations and CSV output
- **No Faker**: We implement custom name generation for domain-specific control and reproducibility
- **No external libraries**: Keeps the generator self-contained and easy to install

---

## 16. CLI Interface

### 16.1 Command Line Usage

```bash
# Generate with defaults (100MB, seed=random)
python -m pandas_dataset_generator --output ./data/

# Generate with specific seed and size
python -m pandas_dataset_generator \
    --output ./data/ \
    --seed 42 \
    --target-size-mb 100

# Generate smaller dataset for testing
python -m pandas_dataset_generator \
    --output ./test_data/ \
    --seed 12345 \
    --target-size-mb 10

# Override specific parameters
python -m pandas_dataset_generator \
    --output ./data/ \
    --seed 42 \
    --n-investors 50000 \
    --n-private 70000 \
    --n-public 10000

# Exclude truth file from target size calculation
python -m pandas_dataset_generator \
    --output ./data/ \
    --include-truth-in-target

# Use custom anomaly rates (via JSON file)
python -m pandas_dataset_generator \
    --output ./data/ \
    --anomaly-config ./custom_rates.json
```

### 16.2 Argument Parser

```python
def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate M&A/Private Deals practice dataset for Pandas"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output directory for generated files"
    )

    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: random)"
    )

    parser.add_argument(
        "--target-size-mb",
        type=float,
        default=100.0,
        help="Target total size in MB (default: 100)"
    )

    parser.add_argument(
        "--n-investors",
        type=int,
        default=25000,
        help="Number of investors (default: 25000)"
    )

    parser.add_argument(
        "--n-private",
        type=int,
        default=35000,
        help="Number of private companies (default: 35000)"
    )

    parser.add_argument(
        "--n-public",
        type=int,
        default=6000,
        help="Number of public companies (default: 6000)"
    )

    parser.add_argument(
        "--include-truth-in-target",
        action="store_true",
        help="Include truth_party2_mapping.csv in target size calculation"
    )

    parser.add_argument(
        "--anomaly-config",
        type=Path,
        help="JSON file with custom anomaly rates"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser
```

### 16.3 Progress Reporting

```python
def generate_with_progress(self) -> None:
    """Generate dataset with progress reporting."""

    print(f"Generating M&A dataset (target: {self.config.target_size_mb}MB, seed: {self.seed})")
    print("-" * 60)

    # Phase 1
    print("Phase 1/5: Generating dimension tables...")
    self._generate_dimension_tables()
    print(f"  ✓ Investors: {len(self.investors):,} rows")
    print(f"  ✓ Private companies: {len(self.private_cos):,} rows")
    print(f"  ✓ Public companies: {len(self.public_cos):,} rows")

    # Phase 2
    print("Phase 2/5: Generating name aliases...")
    self._generate_aliases()
    print(f"  ✓ Aliases: {len(self.aliases):,} rows")

    # Phase 3
    print("Phase 3/5: Calibrating target size...")
    deals_rows = self._calibrate_deal_count()
    print(f"  ✓ Target deals rows: {deals_rows:,}")

    # Phase 4
    print(f"Phase 4/5: Generating deals ({deals_rows:,} rows)...")
    self._generate_deals(deals_rows)
    print(f"  ✓ Deals: {len(self.deals):,} rows")

    # Phase 5
    print("Phase 5/5: Post-processing...")
    self._post_process()
    print("  ✓ Updated investors_json")
    print("  ✓ Shuffled all tables")

    # Write output
    print("-" * 60)
    print("Writing files...")
    self._write_output()

    # Summary
    print("-" * 60)
    print("Generation complete!")
    self._print_summary()
```

---

## Summary

This plan provides a comprehensive blueprint for building the M&A/Private Deals Pandas Practice Dataset Generator. The design emphasizes:

1. **Reproducibility**: Single-seeded RNG ensures identical outputs
2. **Controlled Dirtiness**: Every anomaly has a known rate and type
3. **Realistic Distributions**: Zipfian/lognormal patterns match real M&A data
4. **Modular Architecture**: Clear separation of concerns for maintainability
5. **Testability**: Comprehensive testing strategy at unit and integration levels

The generator will produce ~100MB of interconnected data perfect for practicing:
- Multi-table joins and merges
- Fuzzy string matching
- Date parsing and cleaning
- Numeric data cleaning
- Anomaly detection
- JSON/semi-structured data handling
- Pivot/melt operations
- Deduplication

Ready to proceed with implementation following the phases outlined above.
