"""JSON field generation for semi-structured data columns."""

import json
from typing import List, Dict, Any, Optional, TYPE_CHECKING

from ..rng import RNGManager

if TYPE_CHECKING:
    from ..dirtiness.engine import DirtinessEngine


# Deal terms keys and values
DEAL_TERMS_KEYS: Dict[str, List[str]] = {
    "board_seat": ["Y", "N"],
    "liquidation_pref": ["1x", "1.5x", "2x", "non-participating"],
    "participation": ["Y", "N", "capped"],
    "anti_dilution": ["broad-based", "narrow-based", "full-ratchet", "none"],
    "pro_rata": ["Y", "N"],
    "drag_along": ["Y", "N"],
    "tag_along": ["Y", "N"],
    "redemption": ["Y", "N"],
    "dividends": ["cumulative", "non-cumulative", "none"],
}

# Corrupt JSON examples
CORRUPT_JSON_EXAMPLES: List[str] = [
    '{"incomplete": "json',
    "{'single_quotes': 'invalid'}",
    '{"trailing_comma": "value",}',
    "not json at all",
    '{"missing": value}',
    '[unclosed array',
    '{"nested": {"broken": }',
    "",
    "null",
    "undefined",
]


class JsonFieldGenerator:
    """Generate JSON fields for semi-structured data."""

    def __init__(
        self,
        rng: RNGManager,
        dirtiness: Optional["DirtinessEngine"] = None,
    ):
        """
        Initialize JSON field generator.

        Args:
            rng: Random number generator
            dirtiness: Optional dirtiness engine for tracking anomalies
        """
        self.rng = rng
        self.dirtiness = dirtiness

    def generate_investors_json(
        self,
        investor_names: List[str],
        p_duplicates: float = 0.0,
    ) -> str:
        """
        Generate investors_json field (JSON array of investor names).

        Args:
            investor_names: List of investor names
            p_duplicates: Probability of including duplicates

        Returns:
            JSON array string
        """
        if not investor_names:
            return "[]"

        names = list(investor_names)

        # Maybe inject duplicates
        if p_duplicates > 0 and self.rng.random() < p_duplicates:
            # Duplicate a random name
            if names:
                dup_name = self.rng.choice(names)
                names.append(dup_name)

        return json.dumps(names)

    def generate_tags_json(
        self,
        available_tags: List[str],
        min_tags: int = 1,
        max_tags: int = 4,
    ) -> str:
        """
        Generate tags_json field (JSON array of tags).

        Args:
            available_tags: List of available tags
            min_tags: Minimum number of tags
            max_tags: Maximum number of tags

        Returns:
            JSON array string
        """
        n_tags = self.rng.integers(min_tags, max_tags + 1)
        n_tags = min(n_tags, len(available_tags))

        tag_indices = self.rng.rng.choice(
            len(available_tags),
            size=n_tags,
            replace=False
        )
        tags = [available_tags[i] for i in tag_indices]

        return json.dumps(tags)

    def generate_deal_terms_json(
        self,
        p_missing: float = 0.6,
        p_corrupt: float = 0.01,
    ) -> Optional[str]:
        """
        Generate deal_terms_json field (JSON object).

        Args:
            p_missing: Probability of returning None
            p_corrupt: Probability of returning corrupt JSON

        Returns:
            JSON object string or None
        """
        # Missing
        if self.rng.random() < p_missing:
            if self.dirtiness:
                self.dirtiness.record_anomaly("missing_terms")
            return None

        # Corrupt
        if self.rng.random() < p_corrupt:
            if self.dirtiness:
                self.dirtiness.record_anomaly("corrupt_terms_json")
            return self.rng.choice(CORRUPT_JSON_EXAMPLES)

        # Generate valid terms
        terms: Dict[str, str] = {}

        # Include 2-5 terms
        n_terms = self.rng.integers(2, 6)
        keys = list(DEAL_TERMS_KEYS.keys())
        self.rng.shuffle(keys)

        for key in keys[:n_terms]:
            terms[key] = self.rng.choice(DEAL_TERMS_KEYS[key])

        return json.dumps(terms)

    def generate_corrupt_json(self) -> str:
        """
        Generate a corrupt JSON string for anomaly injection.

        Returns:
            Invalid JSON string
        """
        return self.rng.choice(CORRUPT_JSON_EXAMPLES)

    def maybe_corrupt_json(
        self,
        valid_json: str,
        p_corrupt: float,
    ) -> str:
        """
        Maybe corrupt a valid JSON string.

        Args:
            valid_json: Valid JSON string
            p_corrupt: Probability of corruption

        Returns:
            Original or corrupted JSON
        """
        if self.rng.random() < p_corrupt:
            return self.generate_corrupt_json()
        return valid_json

    def update_investors_json(
        self,
        current_json: Optional[str],
        new_investor: str,
        p_stale_drop: float = 0.0,
        p_phantom_add: float = 0.0,
        phantom_names: Optional[List[str]] = None,
    ) -> str:
        """
        Update investors_json with a new investor.

        Used during post-processing to build investors list from deals.

        Args:
            current_json: Current JSON array or None
            new_investor: New investor name to add
            p_stale_drop: Probability of NOT adding (staleness)
            p_phantom_add: Probability of adding a phantom investor
            phantom_names: List of phantom names to choose from

        Returns:
            Updated JSON array string
        """
        # Parse current
        if current_json and current_json != "[]":
            try:
                investors = json.loads(current_json)
            except json.JSONDecodeError:
                investors = []
        else:
            investors = []

        # Maybe skip adding (staleness)
        if self.rng.random() >= p_stale_drop:
            if new_investor not in investors:
                investors.append(new_investor)

        # Maybe add phantom
        if p_phantom_add > 0 and phantom_names and self.rng.random() < p_phantom_add:
            phantom = self.rng.choice(phantom_names)
            if phantom not in investors:
                investors.append(phantom)

        return json.dumps(investors)
