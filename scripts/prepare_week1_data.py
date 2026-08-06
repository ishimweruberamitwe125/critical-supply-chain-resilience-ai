"""Prepare processed datasets from raw CSV files (Week 1)."""

from __future__ import annotations

import shutil
from pathlib import Path

from src.utils.config import EDGES_FILE, NODES_FILE, PROCESSED_DATA_DIR, RAW_DATA_DIR, SUPPLIERS_FILE


def prepare_processed_data() -> Path:
    """Copy and normalize raw CSV files into the processed data directory."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in (SUPPLIERS_FILE, NODES_FILE, EDGES_FILE):
        source = RAW_DATA_DIR / filename
        target = PROCESSED_DATA_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing raw dataset: {source}")
        shutil.copy2(source, target)

    return PROCESSED_DATA_DIR


if __name__ == "__main__":
    output_dir = prepare_processed_data()
    print(f"Processed datasets written to: {output_dir}")
