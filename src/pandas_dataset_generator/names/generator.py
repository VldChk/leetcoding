"""Name generation for entities."""

from typing import Tuple, List, Dict

from ..rng import RNGManager
from .templates import (
    INVESTOR_PREFIXES,
    INVESTOR_SUFFIXES,
    COMPANY_PREFIXES,
    COMPANY_DOMAIN_SUFFIXES,
    LEGAL_SUFFIX_DIST,
    UNKNOWN_COMPANY_PREFIXES,
    UNKNOWN_COMPANY_SUFFIXES,
)


class NameGenerator:
    """Generates names for investors and companies."""

    def __init__(self, rng: RNGManager):
        """
        Initialize name generator.

        Args:
            rng: Random number generator
        """
        self.rng = rng
        self._used_investor_names: set = set()
        self._used_company_names: set = set()

    def generate_investor_name(self, allow_duplicate: bool = False) -> str:
        """
        Generate a canonical investor name.

        Pattern: {Prefix1} [Prefix2] {Suffix}
        Examples: "Summit Capital", "Northbridge Apex Partners"

        Args:
            allow_duplicate: If True, allows duplicate names

        Returns:
            Generated investor name
        """
        max_attempts = 100

        for _ in range(max_attempts):
            # Decide pattern complexity (1-2 prefix words)
            n_prefixes = self.rng.choice([1, 2], p=[0.7, 0.3])

            # Sample prefixes without replacement
            prefix_indices = self.rng.rng.choice(
                len(INVESTOR_PREFIXES),
                size=n_prefixes,
                replace=False
            )
            prefixes = [INVESTOR_PREFIXES[i] for i in prefix_indices]

            # Sample suffix
            suffix = self.rng.choice(INVESTOR_SUFFIXES)

            name = " ".join([*prefixes, suffix])

            if allow_duplicate or name not in self._used_investor_names:
                self._used_investor_names.add(name)
                return name

        # Fallback: add a numeric suffix
        base_name = " ".join([self.rng.choice(INVESTOR_PREFIXES), self.rng.choice(INVESTOR_SUFFIXES)])
        suffix_num = len(self._used_investor_names)
        return f"{base_name} {suffix_num}"

    def generate_company_name(
        self,
        include_legal_suffix: bool = True,
        allow_duplicate: bool = False,
    ) -> Tuple[str, str]:
        """
        Generate canonical and legal company names.

        Pattern: {Word1} [Word2] {DomainSuffix} [LegalSuffix]

        Args:
            include_legal_suffix: Whether to include legal suffix
            allow_duplicate: If True, allows duplicate names

        Returns:
            Tuple of (canonical_name, legal_name)
        """
        max_attempts = 100

        for _ in range(max_attempts):
            # Core name: 1-2 words + domain suffix
            n_words = self.rng.choice([1, 2], p=[0.4, 0.6])

            word_indices = self.rng.rng.choice(
                len(COMPANY_PREFIXES),
                size=n_words,
                replace=False
            )
            words = [COMPANY_PREFIXES[i] for i in word_indices]

            domain = self.rng.choice(COMPANY_DOMAIN_SUFFIXES)
            core_name = " ".join([*words, domain])

            if allow_duplicate or core_name not in self._used_company_names:
                self._used_company_names.add(core_name)

                # Legal suffix
                if include_legal_suffix:
                    legal_suffix = self.rng.choice(LEGAL_SUFFIX_DIST)
                    if legal_suffix:
                        legal_name = f"{core_name} {legal_suffix}"
                    else:
                        legal_name = core_name
                else:
                    legal_name = core_name

                return core_name, legal_name

        # Fallback
        base_name = " ".join([
            self.rng.choice(COMPANY_PREFIXES),
            self.rng.choice(COMPANY_DOMAIN_SUFFIXES)
        ])
        suffix_num = len(self._used_company_names)
        legal_suffix = self.rng.choice(LEGAL_SUFFIX_DIST) or ""
        legal_name = f"{base_name} {suffix_num} {legal_suffix}".strip()
        return f"{base_name} {suffix_num}", legal_name

    def generate_unknown_company_name(self) -> str:
        """
        Generate a synthetic company name for UNKNOWN party2 entries.

        These names are not in any dictionary and are used for
        fuzzy matching practice with no expected match.

        Returns:
            Synthetic company name
        """
        prefix = self.rng.choice(UNKNOWN_COMPANY_PREFIXES)
        suffix = self.rng.choice(UNKNOWN_COMPANY_SUFFIXES)

        # Sometimes add a second word
        if self.rng.random() < 0.3:
            second_word = self.rng.choice(UNKNOWN_COMPANY_PREFIXES)
            return f"{prefix} {second_word} {suffix}"

        return f"{prefix} {suffix}"

    def generate_near_duplicate_name(self, original: str) -> str:
        """
        Generate a near-duplicate of an existing name.

        Used for dedupe practice where names are similar but not identical.

        Args:
            original: Original name to base the duplicate on

        Returns:
            Similar but slightly different name
        """
        transforms = [
            # Add/remove "The"
            lambda s: f"The {s}" if not s.startswith("The ") else s[4:],
            # Add suffix number
            lambda s: f"{s} II",
            lambda s: f"{s} Group",
            lambda s: f"{s} Holdings",
            # Change last word slightly
            lambda s: s.replace("Capital", "Cap.") if "Capital" in s else s + " Capital",
            lambda s: s.replace("Partners", "Partner") if "Partners" in s else s,
            lambda s: s.replace("Ventures", "Venture") if "Ventures" in s else s,
        ]

        transform = self.rng.choice(transforms)
        return transform(original)

    def reset(self) -> None:
        """Reset used names (for testing)."""
        self._used_investor_names.clear()
        self._used_company_names.clear()
