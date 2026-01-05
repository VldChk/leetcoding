"""JSON output writer for meta.json."""

import json
import os
from pathlib import Path
from typing import Any

from ..stats import StatisticsTracker


class JSONWriter:
    """Write JSON files with consistent formatting."""

    def __init__(self, output_dir: Path):
        """
        Initialize JSON writer.

        Args:
            output_dir: Output directory path
        """
        self.output_dir = output_dir

    def ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_meta(self, stats: StatisticsTracker, filename: str = "meta.json") -> int:
        """
        Write meta.json from statistics tracker.

        Args:
            stats: Statistics tracker with generation data
            filename: Output filename

        Returns:
            File size in bytes
        """
        self.ensure_output_dir()
        filepath = self.output_dir / filename

        content = stats.to_dict()

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, default=str, ensure_ascii=False)
            f.write("\n")

        return os.path.getsize(filepath)

    def write_json(self, data: Any, filename: str, indent: int = 2) -> int:
        """
        Write arbitrary data to JSON file.

        Args:
            data: Data to write
            filename: Output filename
            indent: Indentation level

        Returns:
            File size in bytes
        """
        self.ensure_output_dir()
        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, default=str, ensure_ascii=False)
            f.write("\n")

        return os.path.getsize(filepath)
