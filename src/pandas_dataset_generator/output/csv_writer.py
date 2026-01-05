"""CSV output writer with proper formatting."""

import os
from pathlib import Path
from typing import Dict

import pandas as pd


class CSVWriter:
    """Write DataFrames to CSV with consistent formatting."""

    def __init__(self, output_dir: Path):
        """
        Initialize CSV writer.

        Args:
            output_dir: Output directory path
        """
        self.output_dir = output_dir
        self._file_sizes: Dict[str, int] = {}

    def ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, df: pd.DataFrame, filename: str) -> int:
        """
        Write DataFrame to CSV file.

        Args:
            df: DataFrame to write
            filename: Output filename

        Returns:
            File size in bytes
        """
        self.ensure_output_dir()
        filepath = self.output_dir / filename

        # Write with consistent CSV formatting
        df.to_csv(
            filepath,
            index=False,
            encoding="utf-8",
            quotechar='"',
            doublequote=True,
            lineterminator="\n",
        )

        # Get file size
        size = os.path.getsize(filepath)
        self._file_sizes[filename] = size

        return size

    def write_chunked(
        self,
        df: pd.DataFrame,
        filename: str,
        chunk_size: int = 100000,
    ) -> int:
        """
        Write large DataFrame to CSV in chunks.

        Args:
            df: DataFrame to write
            filename: Output filename
            chunk_size: Rows per chunk

        Returns:
            File size in bytes
        """
        self.ensure_output_dir()
        filepath = self.output_dir / filename

        # Write header first
        mode = "w"
        header = True

        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size]
            chunk.to_csv(
                filepath,
                mode=mode,
                index=False,
                header=header,
                encoding="utf-8",
                quotechar='"',
                doublequote=True,
                lineterminator="\n",
            )
            mode = "a"
            header = False

        # Get file size
        size = os.path.getsize(filepath)
        self._file_sizes[filename] = size

        return size

    def get_file_size(self, filename: str) -> int:
        """Get size of written file."""
        return self._file_sizes.get(filename, 0)

    def get_all_sizes(self) -> Dict[str, int]:
        """Get all file sizes."""
        return self._file_sizes.copy()


def measure_csv_size(df: pd.DataFrame) -> int:
    """
    Measure CSV size without writing to disk.

    Args:
        df: DataFrame to measure

    Returns:
        Size in bytes
    """
    import io

    buffer = io.StringIO()
    df.to_csv(
        buffer,
        index=False,
        encoding="utf-8",
        quotechar='"',
        doublequote=True,
        lineterminator="\n",
    )
    return len(buffer.getvalue().encode("utf-8"))


def estimate_header_bytes(columns: list) -> int:
    """
    Estimate header row bytes.

    Args:
        columns: List of column names

    Returns:
        Header size in bytes
    """
    header = ",".join(str(c) for c in columns) + "\n"
    return len(header.encode("utf-8"))
