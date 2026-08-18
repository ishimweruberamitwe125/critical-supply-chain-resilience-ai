"""Generate static dashboard images from the live analytics pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization.dashboard_charts import save_dashboard_images


def main() -> None:
    saved = save_dashboard_images()
    print("Live pipeline dashboard images saved:")
    for path in saved:
        print(f"  - {path}")
    print("\nThese PNGs are exports from the same engine as: streamlit run streamlit_app.py")


if __name__ == "__main__":
    main()
