"""Alias transformation functions for name variations."""

from enum import Enum
from typing import List, Optional, Tuple
import re

from ..rng import RNGManager
from .templates import SUFFIX_EXPANSIONS, DROPPABLE_TOKENS


class AliasType(Enum):
    """Types of alias transformations."""
    SUFFIX_VARIANT = "SUFFIX_VARIANT"
    PUNCTUATION_VARIANT = "PUNCTUATION_VARIANT"
    CASING_VARIANT = "CASING_VARIANT"
    TOKEN_DROP = "TOKEN_DROP"
    ABBREVIATION = "ABBREVIATION"
    LEGAL_NAME = "LEGAL_NAME"


class AliasTransformer:
    """Transforms canonical names into alias variants."""

    def __init__(self, rng: RNGManager):
        """
        Initialize transformer.

        Args:
            rng: Random number generator
        """
        self.rng = rng

    def generate_alias(
        self,
        canonical_name: str,
        legal_name: Optional[str] = None,
    ) -> Tuple[str, AliasType, str]:
        """
        Generate a single alias for a canonical name.

        Args:
            canonical_name: The canonical entity name
            legal_name: Optional legal name for LEGAL_NAME type

        Returns:
            Tuple of (alias_name, alias_type, rule_description)
        """
        # Choose transformation type
        available_types = [
            AliasType.SUFFIX_VARIANT,
            AliasType.PUNCTUATION_VARIANT,
            AliasType.CASING_VARIANT,
            AliasType.TOKEN_DROP,
            AliasType.ABBREVIATION,
        ]

        # Add legal name option if available and different
        if legal_name and legal_name != canonical_name:
            available_types.append(AliasType.LEGAL_NAME)

        alias_type = self.rng.choice(available_types)

        if alias_type == AliasType.LEGAL_NAME and legal_name:
            return legal_name, alias_type, "use_legal_name"

        if alias_type == AliasType.SUFFIX_VARIANT:
            result, rule = self._apply_suffix_variant(canonical_name)
        elif alias_type == AliasType.PUNCTUATION_VARIANT:
            result, rule = self._apply_punctuation_variant(canonical_name)
        elif alias_type == AliasType.CASING_VARIANT:
            result, rule = self._apply_casing_variant(canonical_name)
        elif alias_type == AliasType.TOKEN_DROP:
            result, rule = self._apply_token_drop(canonical_name)
        elif alias_type == AliasType.ABBREVIATION:
            result, rule = self._apply_abbreviation(canonical_name)
        else:
            result, rule = canonical_name, "no_change"

        # If transformation didn't change anything, try a different one
        if result == canonical_name:
            # Fallback to punctuation variant
            result, rule = self._apply_punctuation_variant(canonical_name)
            alias_type = AliasType.PUNCTUATION_VARIANT

        return result, alias_type, rule

    def _apply_suffix_variant(self, name: str) -> Tuple[str, str]:
        """Apply suffix expansion/contraction."""
        words = name.split()
        if not words:
            return name, "no_words"

        last_word = words[-1]

        # Check if last word has an expansion
        for suffix, expansions in SUFFIX_EXPANSIONS.items():
            if last_word == suffix:
                # Expand
                new_suffix = self.rng.choice(expansions)
                words[-1] = new_suffix
                return " ".join(words), f"expand_{suffix}_to_{new_suffix}"

            # Check if last word is an expansion
            if last_word in expansions:
                # Contract
                words[-1] = suffix
                return " ".join(words), f"contract_{last_word}_to_{suffix}"

        return name, "no_suffix_match"

    def _apply_punctuation_variant(self, name: str) -> Tuple[str, str]:
        """Apply punctuation changes."""
        transforms = [
            (lambda s: s.replace(",", ""), "remove_commas"),
            (lambda s: s.replace(".", ""), "remove_dots"),
            (lambda s: s.replace("'", ""), "remove_apostrophes"),
            (lambda s: s.replace("-", " "), "dash_to_space"),
            (lambda s: s.replace("  ", " "), "normalize_spaces"),
            (lambda s: s.replace(" & ", " and "), "ampersand_to_and"),
            (lambda s: s.replace(" and ", " & "), "and_to_ampersand"),
        ]

        transform_fn, rule = self.rng.choice(transforms)
        result = transform_fn(name)

        # If no change, add/remove a period
        if result == name:
            if name.endswith("."):
                result = name[:-1]
                rule = "remove_trailing_period"
            else:
                result = name + "."
                rule = "add_trailing_period"

        return result, rule

    def _apply_casing_variant(self, name: str) -> Tuple[str, str]:
        """Apply casing changes."""
        transforms = [
            (lambda s: s.upper(), "uppercase"),
            (lambda s: s.lower(), "lowercase"),
            (lambda s: s.title(), "titlecase"),
            (lambda s: s.capitalize(), "capitalize"),
        ]

        transform_fn, rule = self.rng.choice(transforms)
        return transform_fn(name), rule

    def _apply_token_drop(self, name: str) -> Tuple[str, str]:
        """Drop droppable tokens from the name."""
        words = name.split()
        if len(words) < 2:
            return name, "too_few_words"

        # Find droppable tokens in the name
        droppable_indices = []
        for i, word in enumerate(words):
            # Don't drop first word
            if i > 0 and word in DROPPABLE_TOKENS:
                droppable_indices.append(i)

        if not droppable_indices:
            return name, "no_droppable_tokens"

        # Drop one random token
        drop_idx = self.rng.choice(droppable_indices)
        dropped_word = words[drop_idx]
        new_words = [w for i, w in enumerate(words) if i != drop_idx]

        return " ".join(new_words), f"drop_{dropped_word}"

    def _apply_abbreviation(self, name: str) -> Tuple[str, str]:
        """Apply abbreviation mappings."""
        abbreviations = {
            "International": "Intl",
            "Technologies": "Tech",
            "Technology": "Tech",
            "Management": "Mgmt",
            "Corporation": "Corp",
            "Company": "Co",
            "Holdings": "Hldgs",
            "Services": "Svcs",
            "Industries": "Ind",
            "Incorporated": "Inc",
            "Limited": "Ltd",
        }

        # Also support reverse (expansion)
        expansions = {v: k for k, v in abbreviations.items()}

        words = name.split()
        changed = False
        rule = "no_abbreviation"

        for i, word in enumerate(words):
            # Try abbreviation
            if word in abbreviations:
                words[i] = abbreviations[word]
                rule = f"abbreviate_{word}"
                changed = True
                break
            # Try expansion
            if word in expansions:
                words[i] = expansions[word]
                rule = f"expand_{word}"
                changed = True
                break

        if changed:
            return " ".join(words), rule
        return name, rule

    def introduce_typo(self, name: str) -> Tuple[str, str]:
        """
        Introduce a single-character typo.

        Args:
            name: Original name

        Returns:
            Tuple of (typo_name, typo_description)
        """
        if len(name) < 3:
            return name, "too_short"

        # Choose position (avoid first and last character)
        pos = self.rng.integers(1, len(name) - 1)
        typo_types = ["drop", "swap", "replace", "double"]
        typo_type = self.rng.choice(typo_types)

        if typo_type == "drop":
            result = name[:pos] + name[pos + 1:]
            return result, f"drop_char_at_{pos}"

        elif typo_type == "swap" and pos < len(name) - 1:
            chars = list(name)
            chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
            return "".join(chars), f"swap_chars_at_{pos}"

        elif typo_type == "replace":
            char = self.rng.choice(list("abcdefghijklmnopqrstuvwxyz"))
            result = name[:pos] + char + name[pos + 1:]
            return result, f"replace_char_at_{pos}"

        elif typo_type == "double":
            result = name[:pos] + name[pos] + name[pos:]
            return result, f"double_char_at_{pos}"

        return name, "no_typo"

    def normalize_name(self, name: str) -> Tuple[str, str]:
        """
        Apply normalization (for NORMALIZED_VARIANT match class).

        Args:
            name: Original name

        Returns:
            Tuple of (normalized_name, normalization_description)
        """
        normalizations = [
            # Remove punctuation
            (lambda s: re.sub(r'[,.\'-]', '', s), "strip_punctuation"),
            # Normalize whitespace
            (lambda s: ' '.join(s.split()), "normalize_whitespace"),
            # Add extra space
            (lambda s: s.replace(" ", "  "), "double_spaces"),
            # Lowercase
            (lambda s: s.lower(), "lowercase"),
            # Uppercase
            (lambda s: s.upper(), "uppercase"),
        ]

        transform_fn, rule = self.rng.choice(normalizations)
        return transform_fn(name), rule
