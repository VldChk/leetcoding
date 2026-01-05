"""Alias entity generator for name variations."""

from typing import Dict, Any, List, Optional
from collections import defaultdict

import pandas as pd

from ..config import Config
from ..rng import RNGManager
from ..dirtiness.engine import DirtinessEngine
from ..names.transforms import AliasTransformer, AliasType


class AliasGenerator:
    """Generate name aliases for entities."""

    COLUMNS = [
        "canonical_entity_id",
        "canonical_entity_type",
        "canonical_name",
        "alias_name",
        "alias_type",
        "generated_by_rule",
        "is_high_confidence",
    ]

    def __init__(
        self,
        config: Config,
        rng: RNGManager,
        dirtiness: DirtinessEngine,
    ):
        """
        Initialize alias generator.

        Args:
            config: Configuration
            rng: Random number generator
            dirtiness: Dirtiness engine
        """
        self.config = config
        self.rng = rng
        self.dirtiness = dirtiness
        self.transformer = AliasTransformer(rng)

        # Registry for looking up aliases
        self._alias_by_entity: Dict[str, List[str]] = defaultdict(list)
        self._entity_by_alias: Dict[str, List[str]] = defaultdict(list)
        self._all_aliases: List[Dict[str, Any]] = []

    def generate_for_entity(
        self,
        entity_id: str,
        entity_type: str,
        canonical_name: str,
        legal_name: Optional[str] = None,
        avg_aliases: float = 1.2,
    ) -> List[Dict[str, Any]]:
        """
        Generate aliases for a single entity.

        Args:
            entity_id: Entity ID
            entity_type: Entity type (INVESTOR, PRIVATE, PUBLIC)
            canonical_name: Canonical entity name
            legal_name: Optional legal name
            avg_aliases: Average number of aliases

        Returns:
            List of alias dictionaries
        """
        # Sample number of aliases (Poisson distribution)
        n_aliases = self.rng.poisson(avg_aliases)
        n_aliases = max(0, min(n_aliases, 5))  # Cap at 5

        aliases = []
        used_alias_names = {canonical_name}

        for _ in range(n_aliases):
            alias_name, alias_type, rule = self.transformer.generate_alias(
                canonical_name,
                legal_name
            )

            # Skip if same as canonical or already used
            if alias_name in used_alias_names:
                continue

            used_alias_names.add(alias_name)

            # High confidence for certain types
            is_high_conf = alias_type in (
                AliasType.SUFFIX_VARIANT,
                AliasType.LEGAL_NAME,
                AliasType.ABBREVIATION,
            )

            alias_record = {
                "canonical_entity_id": entity_id,
                "canonical_entity_type": entity_type,
                "canonical_name": canonical_name,
                "alias_name": alias_name,
                "alias_type": alias_type.value,
                "generated_by_rule": rule,
                "is_high_confidence": "Y" if is_high_conf else "N",
            }

            aliases.append(alias_record)
            self._alias_by_entity[entity_id].append(alias_name)
            self._entity_by_alias[alias_name].append(entity_id)

        return aliases

    def generate_from_dataframes(
        self,
        investors_df: pd.DataFrame,
        private_df: pd.DataFrame,
        public_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate aliases for all entities in dataframes.

        Args:
            investors_df: Investors dataframe
            private_df: Private companies dataframe
            public_df: Public companies dataframe

        Returns:
            DataFrame with all aliases
        """
        self._all_aliases = []
        self._alias_by_entity = defaultdict(list)
        self._entity_by_alias = defaultdict(list)

        # Process investors
        for _, row in investors_df.iterrows():
            aliases = self.generate_for_entity(
                entity_id=row["investor_id"],
                entity_type="INVESTOR",
                canonical_name=row["investor_name_canonical"],
                avg_aliases=self.config.avg_aliases_investor,
            )
            self._all_aliases.extend(aliases)

        # Process private companies
        for _, row in private_df.iterrows():
            aliases = self.generate_for_entity(
                entity_id=row["private_company_id"],
                entity_type="PRIVATE",
                canonical_name=row["company_name_canonical"],
                legal_name=row.get("legal_name"),
                avg_aliases=self.config.avg_aliases_private,
            )
            self._all_aliases.extend(aliases)

        # Process public companies
        for _, row in public_df.iterrows():
            aliases = self.generate_for_entity(
                entity_id=row["public_company_id"],
                entity_type="PUBLIC",
                canonical_name=row["company_name_canonical"],
                avg_aliases=self.config.avg_aliases_public,
            )
            self._all_aliases.extend(aliases)

        # Inject controlled collisions
        self._inject_collisions()

        return pd.DataFrame(self._all_aliases, columns=self.COLUMNS)

    def _inject_collisions(self) -> None:
        """Inject controlled alias collisions."""
        # Find aliases that appear only once
        unique_aliases = [
            alias for alias, entities in self._entity_by_alias.items()
            if len(entities) == 1
        ]

        if len(unique_aliases) < 10:
            return

        # Number of collisions to inject (using configured rate)
        collision_rate = self.dirtiness.rates.p_alias_collision
        n_collisions = int(len(self._all_aliases) * collision_rate)

        for _ in range(n_collisions):
            if len(unique_aliases) < 2:
                break

            # Pick an alias to duplicate
            alias_to_dup = self.rng.choice(unique_aliases)

            # Find entities that don't have this alias yet
            existing_entities = set(self._entity_by_alias[alias_to_dup])
            candidates = [
                a for a in self._all_aliases
                if a["canonical_entity_id"] not in existing_entities
            ]

            if not candidates:
                continue

            # Pick a candidate entity
            target = self.rng.choice(candidates)

            # Create collision alias
            collision = {
                "canonical_entity_id": target["canonical_entity_id"],
                "canonical_entity_type": target["canonical_entity_type"],
                "canonical_name": target["canonical_name"],
                "alias_name": alias_to_dup,
                "alias_type": "COLLISION_INJECTED",
                "generated_by_rule": "collision_injection",
                "is_high_confidence": "N",
            }

            self._all_aliases.append(collision)
            self._entity_by_alias[alias_to_dup].append(target["canonical_entity_id"])
            unique_aliases.remove(alias_to_dup)

            self.dirtiness.record_anomaly("alias_collision")

    def get_aliases_for_entity(self, entity_id: str) -> List[str]:
        """Get all aliases for an entity."""
        return self._alias_by_entity.get(entity_id, [])

    def get_entities_for_alias(self, alias_name: str) -> List[str]:
        """Get all entity IDs that have a given alias."""
        return self._entity_by_alias.get(alias_name, [])

    def get_random_alias(self, entity_id: str) -> Optional[str]:
        """Get a random alias for an entity, or None if no aliases."""
        aliases = self._alias_by_entity.get(entity_id, [])
        if aliases:
            return self.rng.choice(aliases)
        return None
