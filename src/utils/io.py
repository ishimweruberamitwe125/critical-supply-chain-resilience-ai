"""CSV loading and validation helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.config import (
    EDGES_FILE,
    NODES_FILE,
    PROCESSED_DATA_DIR,
    REQUIRED_EDGE_COLUMNS,
    REQUIRED_NODE_COLUMNS,
    REQUIRED_SUPPLIER_COLUMNS,
    SUPPLIERS_FILE,
)


def _validate_columns(df: pd.DataFrame, required: list[str], dataset_name: str) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} is missing columns: {missing}")


def load_network_tables(data_dir: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load supplier, node, and edge tables from the processed data directory."""
    base_dir = data_dir or PROCESSED_DATA_DIR

    suppliers = pd.read_csv(base_dir / SUPPLIERS_FILE)
    nodes = pd.read_csv(base_dir / NODES_FILE)
    edges = pd.read_csv(base_dir / EDGES_FILE)

    _validate_columns(suppliers, REQUIRED_SUPPLIER_COLUMNS, "suppliers")
    _validate_columns(nodes, REQUIRED_NODE_COLUMNS, "nodes")
    _validate_columns(edges, REQUIRED_EDGE_COLUMNS, "edges")

    edges["is_single_source"] = edges["is_single_source"].astype(bool)

    return suppliers, nodes, edges
