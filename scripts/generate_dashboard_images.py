"""Generate static dashboard images for docs and notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.prepare_week1_data import prepare_processed_data
from src.visualization.dashboard_charts import save_dashboard_images


def main() -> None:
    prepare_processed_data()
    saved = save_dashboard_images()
    print("Dashboard images saved:")
    for path in saved:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
