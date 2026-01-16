"""Reproducible random number generation management."""

from typing import Optional, List, Any, Dict, Tuple
import numpy as np


class RNGManager:
    """
    Manages reproducible random number generation.

    Uses numpy's new Generator API for better reproducibility
    and statistical properties.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize RNG manager.

        Args:
            seed: Random seed. If None, a random seed is generated.
        """
        if seed is None:
            # Generate a random seed and store it for reproducibility
            self._seed = np.random.default_rng().integers(0, 2**31)
        else:
            self._seed = seed

        self._rng = np.random.default_rng(self._seed)
        self._call_count = 0
        self._choice_cache: Dict[int, Tuple[List[Any], List[float]]] = {}

    @property
    def seed(self) -> int:
        """Return the seed used for this RNG."""
        return self._seed

    @property
    def rng(self) -> np.random.Generator:
        """Return the underlying numpy Generator."""
        return self._rng

    def random(self) -> float:
        """Generate a random float in [0, 1)."""
        self._call_count += 1
        return self._rng.random()

    def integers(self, low: int, high: Optional[int] = None) -> int:
        """Generate a random integer in [low, high)."""
        self._call_count += 1
        return int(self._rng.integers(low, high))

    def choice(
        self,
        a: Any,
        size: Optional[int] = None,
        replace: bool = True,
        p: Optional[List[float]] = None,
    ) -> Any:
        """
        Generate a random sample from a given array.

        Args:
            a: Array or int to sample from
            size: Output shape
            replace: Whether to sample with replacement
            p: Probability weights

        Returns:
            Random sample(s)
        """
        self._call_count += 1
        if isinstance(a, dict):
            # Handle dictionary input (keys as choices, values as probabilities)
            cache_key = id(a)
            cached = self._choice_cache.get(cache_key)
            if cached is None or len(cached[0]) != len(a):
                keys = list(a.keys())
                probs = list(a.values())
                self._choice_cache[cache_key] = (keys, probs)
            else:
                keys, probs = cached
            return self._rng.choice(keys, size=size, replace=replace, p=probs)
        return self._rng.choice(a, size=size, replace=replace, p=p)

    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        """Generate a random float in [low, high)."""
        self._call_count += 1
        return float(self._rng.uniform(low, high))

    def lognormal(self, mean: float, sigma: float) -> float:
        """Generate a lognormal random value."""
        self._call_count += 1
        return float(self._rng.lognormal(mean, sigma))

    def normal(self, loc: float = 0.0, scale: float = 1.0) -> float:
        """Generate a normal random value."""
        self._call_count += 1
        return float(self._rng.normal(loc, scale))

    def beta(self, a: float, b: float) -> float:
        """Generate a beta random value."""
        self._call_count += 1
        return float(self._rng.beta(a, b))

    def poisson(self, lam: float) -> int:
        """Generate a Poisson random value."""
        self._call_count += 1
        return int(self._rng.poisson(lam))

    def shuffle(self, x: List) -> List:
        """Shuffle a list in place and return it."""
        self._call_count += 1
        self._rng.shuffle(x)
        return x

    def permutation(self, x: Any) -> np.ndarray:
        """Return a shuffled copy of the input."""
        self._call_count += 1
        return self._rng.permutation(x)

    def sample_weighted(self, items: List, weights: List[float], size: int = 1) -> List:
        """
        Sample items with weights (Zipfian-style sampling).

        Args:
            items: List of items to sample from
            weights: Weights for each item
            size: Number of samples

        Returns:
            List of sampled items
        """
        self._call_count += 1
        # Normalize weights to probabilities
        total = sum(weights)
        probs = [w / total for w in weights]
        indices = self._rng.choice(len(items), size=size, replace=True, p=probs)
        return [items[i] for i in indices]

    def zipf_weights(self, n: int, alpha: float = 1.5) -> List[float]:
        """
        Generate Zipfian weights for n items.

        Args:
            n: Number of items
            alpha: Zipf exponent (higher = more skewed)

        Returns:
            List of weights summing to 1.0
        """
        weights = [1.0 / (i ** alpha) for i in range(1, n + 1)]
        total = sum(weights)
        return [w / total for w in weights]

    def get_call_count(self) -> int:
        """Return the number of RNG calls made."""
        return self._call_count

    def spawn(self, name: str) -> "RNGManager":
        """
        Create a child RNG with a deterministic sub-seed.

        This allows different tables to have independent but
        reproducible random streams.

        Args:
            name: Name for the child RNG (used to derive sub-seed)

        Returns:
            New RNGManager with derived seed
        """
        # Derive sub-seed from parent seed and name
        name_hash = hash(name) & 0x7FFFFFFF  # Ensure positive
        sub_seed = (self._seed + name_hash) & 0x7FFFFFFF
        return RNGManager(seed=sub_seed)
