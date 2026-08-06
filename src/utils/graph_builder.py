"""Build NetworkX supply chain graphs from tabular data."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pandas as pd

from src.utils.config import PROCESSED_DATA_DIR
from src.utils.io import load_network_tables


def build_supply_network(data_dir: Path | None = None) -> nx.DiGraph:
    """Construct a directed supply network graph from processed CSV files."""
    suppliers, nodes, edges = load_network_tables(data_dir)

    graph = nx.DiGraph(name="semiconductor_supply_network")

    for row in suppliers.itertuples(index=False):
        graph.add_node(
            row.supplier_id,
            node_kind="supplier",
            name=row.name,
            component=row.component,
            country=row.country,
            reliability_score=float(row.reliability_score),
            lead_time_days=int(row.lead_time_days),
            geopolitical_risk=float(row.geopolitical_risk),
        )

    for row in nodes.itertuples(index=False):
        graph.add_node(
            row.node_id,
            node_kind=row.node_type,
            name=row.name,
            region=row.region,
            capacity_units_per_month=int(row.capacity_units_per_month),
        )

    known_nodes = set(graph.nodes)
    for row in edges.itertuples(index=False):
        if row.source_id not in known_nodes:
            raise ValueError(f"Edge {row.edge_id} references unknown source: {row.source_id}")
        if row.target_id not in known_nodes:
            raise ValueError(f"Edge {row.edge_id} references unknown target: {row.target_id}")

        graph.add_edge(
            row.source_id,
            row.target_id,
            edge_id=row.edge_id,
            material=row.material,
            lead_time_days=int(row.lead_time_days),
            capacity_units_per_month=int(row.capacity_units_per_month),
            cost_per_unit=float(row.cost_per_unit),
            is_single_source=bool(row.is_single_source),
        )

    return graph


def summarize_network(graph: nx.DiGraph) -> dict[str, float | int | str]:
    """Return basic network statistics used in Week 1 validation."""
    supplier_nodes = [node for node, data in graph.nodes(data=True) if data.get("node_kind") == "supplier"]
    factory_nodes = [node for node, data in graph.nodes(data=True) if data.get("node_kind") == "factory"]
    distribution_nodes = [
        node for node, data in graph.nodes(data=True) if data.get("node_kind") == "distribution"
    ]

    single_source_edges = sum(1 for _, _, data in graph.edges(data=True) if data.get("is_single_source"))

    reliabilities = [graph.nodes[node]["reliability_score"] for node in supplier_nodes]
    geo_risks = [graph.nodes[node]["geopolitical_risk"] for node in supplier_nodes]

    return {
        "network_name": str(graph.name),
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "supplier_count": len(supplier_nodes),
        "factory_count": len(factory_nodes),
        "distribution_count": len(distribution_nodes),
        "single_source_edge_count": single_source_edges,
        "avg_supplier_reliability": round(sum(reliabilities) / len(reliabilities), 3) if reliabilities else 0.0,
        "avg_geopolitical_risk": round(sum(geo_risks) / len(geo_risks), 3) if geo_risks else 0.0,
    }


def node_degree_table(graph: nx.DiGraph) -> pd.DataFrame:
    """Build a per-node in/out-degree table for inspection."""
    rows: list[dict[str, int | str]] = []
    for node_id, data in graph.nodes(data=True):
        rows.append(
            {
                "node_id": node_id,
                "name": data.get("name", node_id),
                "node_kind": data.get("node_kind", "unknown"),
                "in_degree": graph.in_degree(node_id),
                "out_degree": graph.out_degree(node_id),
            }
        )
    return pd.DataFrame(rows).sort_values(["node_kind", "node_id"]).reset_index(drop=True)
