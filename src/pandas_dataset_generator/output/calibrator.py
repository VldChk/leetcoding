"""Size calibration for hitting target dataset size."""

from dataclasses import dataclass
from typing import Dict
import math

import pandas as pd

from .csv_writer import measure_csv_size, estimate_header_bytes


@dataclass
class CalibrationResult:
    """Results from size calibration."""
    base_bytes: int
    bytes_per_deal_row: float
    target_deals_rows: int
    pilot_rows: int
    target_bytes: int
    estimated_total_bytes: int


class SizeCalibrator:
    """Calibrate deal count to hit target size."""

    def __init__(
        self,
        target_size_mb: float,
        min_deals_rows: int = 50000,
        include_truth_in_target: bool = False,
    ):
        """
        Initialize calibrator.

        Args:
            target_size_mb: Target total size in MB
            min_deals_rows: Minimum deals rows
            include_truth_in_target: Include truth file in target calculation
        """
        self.target_size_mb = target_size_mb
        self.min_deals_rows = min_deals_rows
        self.include_truth_in_target = include_truth_in_target

    def calibrate(
        self,
        base_sizes: Dict[str, int],
        pilot_deals: pd.DataFrame,
        pilot_truth: pd.DataFrame,
    ) -> CalibrationResult:
        """
        Calculate required deals row count.

        Args:
            base_sizes: Dict of filename -> size for dimension tables
            pilot_deals: Pilot deals DataFrame
            pilot_truth: Pilot truth DataFrame

        Returns:
            Calibration result with target row count
        """
        # Calculate base bytes (dimension tables + aliases)
        base_bytes = sum(base_sizes.values())

        # Measure pilot deal size
        pilot_deal_bytes = measure_csv_size(pilot_deals)
        pilot_rows = len(pilot_deals)

        # Calculate bytes per deal row (excluding header)
        deal_header_bytes = estimate_header_bytes(pilot_deals.columns)
        bytes_per_deal_row = (pilot_deal_bytes - deal_header_bytes) / max(1, pilot_rows)

        # If including truth, calculate truth ratio
        if self.include_truth_in_target:
            truth_bytes = measure_csv_size(pilot_truth)
            truth_ratio = truth_bytes / max(1, pilot_deal_bytes)
            # Adjust bytes per row to include truth
            bytes_per_row_total = bytes_per_deal_row * (1 + truth_ratio)
        else:
            bytes_per_row_total = bytes_per_deal_row

        # Calculate target
        target_bytes = int(self.target_size_mb * 1024 * 1024)
        available_for_deals = target_bytes - base_bytes

        # Calculate row count
        if available_for_deals > 0 and bytes_per_row_total > 0:
            target_deals_rows = int(math.ceil(available_for_deals / bytes_per_row_total))
        else:
            target_deals_rows = self.min_deals_rows

        # Apply minimum
        target_deals_rows = max(self.min_deals_rows, target_deals_rows)

        # Estimate total bytes
        estimated_deal_bytes = int(bytes_per_deal_row * target_deals_rows) + deal_header_bytes
        estimated_total = base_bytes + estimated_deal_bytes

        return CalibrationResult(
            base_bytes=base_bytes,
            bytes_per_deal_row=bytes_per_deal_row,
            target_deals_rows=target_deals_rows,
            pilot_rows=pilot_rows,
            target_bytes=target_bytes,
            estimated_total_bytes=estimated_total,
        )

    def quick_estimate(
        self,
        base_bytes: int,
        estimated_bytes_per_row: float = 450,
    ) -> int:
        """
        Quick estimate without pilot generation.

        Args:
            base_bytes: Base dimension table bytes
            estimated_bytes_per_row: Estimated bytes per deal row

        Returns:
            Estimated deals row count
        """
        target_bytes = int(self.target_size_mb * 1024 * 1024)
        available = target_bytes - base_bytes

        if available > 0:
            rows = int(math.ceil(available / estimated_bytes_per_row))
            return max(self.min_deals_rows, rows)

        return self.min_deals_rows
