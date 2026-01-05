"""Base classes for entity generators."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

import pandas as pd

from ..config import Config
from ..rng import RNGManager
from ..dirtiness.engine import DirtinessEngine
from ..names.generator import NameGenerator
from ..formatters.dates import DateFormatter
from ..formatters.numerics import NumericFormatter


@dataclass
class Entity:
    """Base entity with common fields."""
    id: str
    canonical_name: str
    source_system: str


class BaseEntityGenerator(ABC):
    """Abstract base class for entity generators."""

    # ID prefix for this entity type
    ID_PREFIX: str = "ENT"
    ID_DIGITS: int = 7

    def __init__(
        self,
        config: Config,
        rng: RNGManager,
        dirtiness: DirtinessEngine,
        name_generator: NameGenerator,
        date_formatter: DateFormatter,
        numeric_formatter: NumericFormatter,
    ):
        """
        Initialize base entity generator.

        Args:
            config: Configuration
            rng: Random number generator
            dirtiness: Dirtiness engine for anomaly injection
            name_generator: Name generator
            date_formatter: Date formatter
            numeric_formatter: Numeric formatter
        """
        self.config = config
        self.rng = rng
        self.dirtiness = dirtiness
        self.name_generator = name_generator
        self.date_formatter = date_formatter
        self.numeric_formatter = numeric_formatter

        self._current_id = 0
        self._generated_entities: List[Dict[str, Any]] = []

    def generate_id(self) -> str:
        """Generate a unique ID for this entity type."""
        self._current_id += 1
        return f"{self.ID_PREFIX}{self._current_id:0{self.ID_DIGITS}d}"

    def generate_bad_id(self) -> str:
        """Generate a bad/invalid ID for anomaly injection."""
        bad_patterns = [
            f"{self.ID_PREFIX}9999999",  # Non-existent
            f"{self.ID_PREFIX}{self.ID_PREFIX}0000001",  # Double prefix
            f"{self.ID_PREFIX.lower()}0000001",  # Lowercase prefix
            "INVALID_ID",
            "",
        ]
        return self.rng.choice(bad_patterns)

    @abstractmethod
    def generate_one(self, index: int) -> Dict[str, Any]:
        """
        Generate a single entity.

        Args:
            index: Entity index (0-based)

        Returns:
            Dictionary of entity fields
        """
        pass

    def generate(self, n: int) -> pd.DataFrame:
        """
        Generate n entities.

        Args:
            n: Number of entities to generate

        Returns:
            DataFrame with all entities
        """
        self._generated_entities = []
        self._current_id = 0

        for i in range(n):
            entity = self.generate_one(i)
            self._generated_entities.append(entity)

        return pd.DataFrame(self._generated_entities)

    def get_entities(self) -> List[Dict[str, Any]]:
        """Get list of generated entities."""
        return self._generated_entities

    def sample_from_distribution(self, distribution: Dict[str, float]) -> str:
        """
        Sample a value from a distribution dictionary.

        Args:
            distribution: Dict mapping values to probabilities

        Returns:
            Sampled value
        """
        return self.rng.choice(distribution)

    def maybe_null(self, value: Any, anomaly_type: str) -> Optional[Any]:
        """
        Maybe make a value null based on anomaly rate.

        Args:
            value: Original value
            anomaly_type: Anomaly type name

        Returns:
            Value or None
        """
        return self.dirtiness.maybe_null(anomaly_type, value)


class EntityRegistry:
    """Registry for looking up entities by ID."""

    def __init__(self):
        """Initialize empty registry."""
        self.investors: Dict[str, Dict[str, Any]] = {}
        self.private_companies: Dict[str, Dict[str, Any]] = {}
        self.public_companies: Dict[str, Dict[str, Any]] = {}

        # Lists for sampling
        self.investor_list: List[Dict[str, Any]] = []
        self.private_list: List[Dict[str, Any]] = []
        self.public_list: List[Dict[str, Any]] = []

    def register_investors(self, df: pd.DataFrame) -> None:
        """Register investors from DataFrame."""
        for _, row in df.iterrows():
            entity = row.to_dict()
            self.investors[row["investor_id"]] = entity
            self.investor_list.append(entity)

    def register_private_companies(self, df: pd.DataFrame) -> None:
        """Register private companies from DataFrame."""
        for _, row in df.iterrows():
            entity = row.to_dict()
            self.private_companies[row["private_company_id"]] = entity
            self.private_list.append(entity)

    def register_public_companies(self, df: pd.DataFrame) -> None:
        """Register public companies from DataFrame."""
        for _, row in df.iterrows():
            entity = row.to_dict()
            self.public_companies[row["public_company_id"]] = entity
            self.public_list.append(entity)

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID."""
        if entity_id.startswith("INV"):
            return self.investors.get(entity_id)
        elif entity_id.startswith("PVT"):
            return self.private_companies.get(entity_id)
        elif entity_id.startswith("PUB"):
            return self.public_companies.get(entity_id)
        return None

    def get_entity_type(self, entity_id: str) -> Optional[str]:
        """Get entity type from ID prefix."""
        if entity_id.startswith("INV"):
            return "INVESTOR"
        elif entity_id.startswith("PVT"):
            return "PRIVATE"
        elif entity_id.startswith("PUB"):
            return "PUBLIC"
        return None

    def get_list_by_type(self, entity_type: str) -> List[Dict[str, Any]]:
        """Get entity list by type."""
        if entity_type == "INVESTOR":
            return self.investor_list
        elif entity_type == "PRIVATE":
            return self.private_list
        elif entity_type == "PUBLIC":
            return self.public_list
        return []
