"""
M&A / Private Deals Pandas Practice Dataset Generator.

A tool for generating realistic M&A/Private Deals datasets with
controlled data quality issues for practicing Pandas skills.
"""

from .config import Config
from .generator import DatasetGenerator
from .dirtiness.rates import AnomalyRates
from .rng import RNGManager

__version__ = "1.0.0"

__all__ = [
    "Config",
    "DatasetGenerator",
    "AnomalyRates",
    "RNGManager",
    "__version__",
]
