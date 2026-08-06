"""Week 1 tests for graph construction and data loading."""

from pathlib import Path

import pytest

from scripts.prepare_week1_data import prepare_processed_data
from src.utils.graph_builder import build_supply_network, summarize_network
from src.utils.io import load_network_tables


def test_processed_data_exists_after_prepare() -> None:
    output_dir = prepare_processed_data()
    assert (output_dir / "suppliers.csv").exists()
    assert (output_dir / "nodes.csv").exists()
    assert (output_dir / "edges.csv").exists()


def test_load_network_tables_returns_expected_counts() -> None:
    prepare_processed_data()
    suppliers, nodes, edges = load_network_tables()
    assert len(suppliers) == 8
    assert len(nodes) == 4
    assert len(edges) == 14


def test_build_supply_network_summary() -> None:
    prepare_processed_data()
    graph = build_supply_network()
    summary = summarize_network(graph)
    assert summary["supplier_count"] == 8
    assert summary["factory_count"] == 3
    assert summary["distribution_count"] == 1
    assert summary["total_edges"] == 14
