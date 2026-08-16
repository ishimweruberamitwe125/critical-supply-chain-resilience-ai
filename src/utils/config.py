"""Shared configuration for Critical Supply Chain Resilience AI."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
PREDICTIVE_MODELS_DIR = MODELS_DIR / "predictive_models"
OPTIMIZATION_MODELS_DIR = MODELS_DIR / "optimization_models"

DEFAULT_NETWORK_NAME = "semiconductor_mini_network"
ENERGY_NETWORK_NAME = "energy_mini_network"

SEMICONDUCTOR_DATA_DIR = PROCESSED_DATA_DIR
ENERGY_DATA_DIR = PROCESSED_DATA_DIR / "energy"
ENERGY_RAW_DATA_DIR = RAW_DATA_DIR / "energy"

SUPPLIERS_FILE = "suppliers.csv"
NODES_FILE = "nodes.csv"
EDGES_FILE = "edges.csv"

REQUIRED_SUPPLIER_COLUMNS = [
    "supplier_id",
    "name",
    "component",
    "country",
    "reliability_score",
    "lead_time_days",
    "geopolitical_risk",
]

REQUIRED_NODE_COLUMNS = [
    "node_id",
    "name",
    "node_type",
    "region",
    "capacity_units_per_month",
]

REQUIRED_EDGE_COLUMNS = [
    "edge_id",
    "source_id",
    "target_id",
    "material",
    "lead_time_days",
    "capacity_units_per_month",
    "cost_per_unit",
    "is_single_source",
]
