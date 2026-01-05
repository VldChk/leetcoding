"""Statistics tracking for meta.json generation."""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import json


@dataclass
class FileStats:
    """Statistics for a single output file."""
    row_count: int = 0
    size_bytes: int = 0
    column_count: int = 0


class StatisticsTracker:
    """
    Tracks generation statistics for meta.json output.

    Collects information about:
    - Row counts per file
    - File sizes
    - Anomaly counts
    - Distribution samples
    - Generation parameters
    """

    CONTRACT_VERSION = "1.0"

    def __init__(self, seed: int, target_size_mb: float):
        """
        Initialize statistics tracker.

        Args:
            seed: Random seed used for generation
            target_size_mb: Target total size in MB
        """
        self._seed = seed
        self._target_size_mb = target_size_mb
        self._start_time = datetime.now()
        self._end_time: Optional[datetime] = None

        # File statistics
        self._file_stats: Dict[str, FileStats] = {}

        # Anomaly counts (populated by DirtinessEngine)
        self._anomaly_counts: Dict[str, int] = defaultdict(int)

        # Distribution samples (for validation)
        self._distributions: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # Calibration info
        self._calibration: Dict[str, Any] = {}

        # Custom notes
        self._notes: list = []

    def record_file_stats(self, filename: str, row_count: int,
                          size_bytes: int, column_count: int) -> None:
        """Record statistics for an output file."""
        self._file_stats[filename] = FileStats(
            row_count=row_count,
            size_bytes=size_bytes,
            column_count=column_count
        )

    def record_anomaly(self, anomaly_type: str, count: int = 1) -> None:
        """Record anomaly occurrence."""
        self._anomaly_counts[anomaly_type] += count

    def set_anomaly_counts(self, counts: Dict[str, int]) -> None:
        """Set all anomaly counts at once (from DirtinessEngine)."""
        self._anomaly_counts = defaultdict(int, counts)

    def record_distribution_sample(self, dist_name: str, value: str) -> None:
        """Record a sample from a distribution (for validation)."""
        self._distributions[dist_name][value] += 1

    def record_calibration(self, base_bytes: int, bytes_per_deal_row: float,
                          target_deals_rows: int, pilot_rows: int) -> None:
        """Record calibration results."""
        self._calibration = {
            "base_bytes": base_bytes,
            "bytes_per_deal_row": bytes_per_deal_row,
            "target_deals_rows": target_deals_rows,
            "pilot_rows": pilot_rows,
        }

    def add_note(self, note: str) -> None:
        """Add a custom note to the metadata."""
        self._notes.append(note)

    def finalize(self) -> None:
        """Mark generation as complete."""
        self._end_time = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary for JSON output."""
        # Calculate totals
        total_size_bytes = sum(fs.size_bytes for fs in self._file_stats.values())
        total_rows = sum(fs.row_count for fs in self._file_stats.values())

        # File stats as dict
        file_stats_dict = {
            name: {
                "row_count": fs.row_count,
                "size_bytes": fs.size_bytes,
                "size_mb": round(fs.size_bytes / (1024 * 1024), 3),
                "column_count": fs.column_count,
            }
            for name, fs in self._file_stats.items()
        }

        # Duration
        if self._end_time:
            duration_seconds = (self._end_time - self._start_time).total_seconds()
        else:
            duration_seconds = None

        return {
            "contract_version": self.CONTRACT_VERSION,
            "generation": {
                "seed": self._seed,
                "target_total_size_mb": self._target_size_mb,
                "actual_total_size_mb": round(total_size_bytes / (1024 * 1024), 3),
                "total_rows": total_rows,
                "start_time": self._start_time.isoformat(),
                "end_time": self._end_time.isoformat() if self._end_time else None,
                "duration_seconds": duration_seconds,
            },
            "files": file_stats_dict,
            "calibration": self._calibration,
            "anomaly_counts": dict(self._anomaly_counts),
            "distributions": {
                name: dict(counts)
                for name, counts in self._distributions.items()
            },
            "notes": self._notes if self._notes else None,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert statistics to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
