"""Generate dashboard images and the grant presentation deck."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.generate_dashboard_images import main as generate_images
from scripts.generate_presentation import main as generate_presentation


def main() -> None:
    generate_images()
    generate_presentation()
    print("All presentation assets generated.")


if __name__ == "__main__":
    main()
