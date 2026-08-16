"""Energy network prototype tests."""

from scripts.prepare_energy_data import prepare_energy_data
from src.pipeline import run_prototype_pipeline
from src.utils.config import ENERGY_DATA_DIR
from src.utils.graph_builder import build_supply_network


def test_energy_pipeline_runs() -> None:
    prepare_energy_data()
    report = run_prototype_pipeline(data_dir=ENERGY_DATA_DIR)
    assert report.network_summary["supplier_count"] == 8
    assert report.network_summary["factory_count"] == 3
    assert len(report.simulations) == 3


def test_energy_graph_loads() -> None:
    prepare_energy_data()
    graph = build_supply_network(ENERGY_DATA_DIR)
    assert graph.number_of_nodes() == 12
    assert graph.number_of_edges() == 14
