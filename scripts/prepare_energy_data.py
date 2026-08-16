"""Prepare processed energy-sector datasets."""

from __future__ import annotations

import shutil
from pathlib import Path

from src.utils.config import EDGES_FILE, ENERGY_DATA_DIR, ENERGY_RAW_DATA_DIR, NODES_FILE, SUPPLIERS_FILE


def prepare_energy_data() -> Path:
    """Copy raw energy CSV files into the processed energy data directory."""
    ENERGY_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in (SUPPLIERS_FILE, NODES_FILE, EDGES_FILE):
        source = ENERGY_RAW_DATA_DIR / filename
        target = ENERGY_DATA_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing raw energy dataset: {source}")
        shutil.copy2(source, target)

    return ENERGY_DATA_DIR


if __name__ == "__main__":
    output_dir = prepare_energy_data()
    print(f"Energy datasets written to: {output_dir}")
