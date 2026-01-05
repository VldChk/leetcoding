"""CLI interface for the dataset generator."""

import argparse
import sys
from pathlib import Path

from .config import Config
from .dirtiness.rates import AnomalyRates
from .generator import DatasetGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate M&A/Private Deals practice dataset for Pandas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with defaults (100MB, random seed)
  python -m pandas_dataset_generator -o ./data/

  # Generate with specific seed and size
  python -m pandas_dataset_generator -o ./data/ -s 42 --target-size-mb 50

  # Generate smaller dataset for testing
  python -m pandas_dataset_generator -o ./test_data/ -s 12345 --target-size-mb 10

  # Override entity counts
  python -m pandas_dataset_generator -o ./data/ --n-investors 50000 --n-private 70000
        """,
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output directory for generated files",
    )

    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: random)",
    )

    parser.add_argument(
        "--target-size-mb",
        type=float,
        default=100.0,
        help="Target total size in MB (default: 100)",
    )

    parser.add_argument(
        "--n-investors",
        type=int,
        default=25000,
        help="Number of investors (default: 25000)",
    )

    parser.add_argument(
        "--n-private",
        type=int,
        default=35000,
        help="Number of private companies (default: 35000)",
    )

    parser.add_argument(
        "--n-public",
        type=int,
        default=6000,
        help="Number of public companies (default: 6000)",
    )

    parser.add_argument(
        "--include-truth-in-target",
        action="store_true",
        help="Include truth_party2_mapping.csv in target size calculation",
    )

    parser.add_argument(
        "--anomaly-config",
        type=Path,
        help="JSON file with custom anomaly rates",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output",
    )

    return parser


def main(args: list = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    # Create config
    config = Config(
        output_dir=parsed.output,
        seed=parsed.seed,
        target_total_size_mb=parsed.target_size_mb,
        n_investors=parsed.n_investors,
        n_private=parsed.n_private,
        n_public=parsed.n_public,
        include_truth_in_target=parsed.include_truth_in_target,
    )

    # Load custom anomaly rates if provided
    anomaly_rates = None
    if parsed.anomaly_config:
        try:
            anomaly_rates = AnomalyRates.from_json(parsed.anomaly_config)
        except Exception as e:
            print(f"Error loading anomaly config: {e}", file=sys.stderr)
            return 1

    # Progress callback
    if parsed.quiet:
        progress = lambda msg: None
    else:
        progress = lambda msg: print(msg)

    # Run generator
    try:
        generator = DatasetGenerator(
            config=config,
            anomaly_rates=anomaly_rates,
            progress_callback=progress,
        )

        if not parsed.quiet:
            print("=" * 60)
            print("M&A Dataset Generator")
            print("=" * 60)
            print(f"Seed: {generator.seed}")
            print(f"Target size: {config.target_total_size_mb} MB")
            print(f"Output: {config.output_dir}")
            print("=" * 60)

        generator.generate()

        if not parsed.quiet:
            print("=" * 60)
            print("Generation complete!")
            print(f"Files written to: {config.output_dir}")
            print("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\nGeneration interrupted.", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if parsed.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
