"""Logistics route optimization prototype."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def optimize_logistics_routes(graph: nx.DiGraph, origin: str, destination: str) -> pd.DataFrame:
    """
    Find the lowest lead-time route between two nodes.
    Prototype uses shortest path by lead time edge weight.
    """
    if origin not in graph or destination not in graph:
        raise ValueError("Origin or destination not found in supply network.")

    def lead_time_weight(source: str, target: str, data: dict) -> float:
        return float(data.get("lead_time_days", 1))

    path = nx.dijkstra_path(graph, origin, destination, weight=lead_time_weight)
    total_lead_time = nx.dijkstra_path_length(graph, origin, destination, weight=lead_time_weight)

    rows = []
    for idx in range(len(path) - 1):
        source, target = path[idx], path[idx + 1]
        edge_data = graph.edges[source, target]
        rows.append(
            {
                "step": idx + 1,
                "source_id": source,
                "source_name": graph.nodes[source].get("name", source),
                "target_id": target,
                "target_name": graph.nodes[target].get("name", target),
                "material": edge_data.get("material", "unknown"),
                "lead_time_days": edge_data.get("lead_time_days", 0),
            }
        )

    summary = pd.DataFrame(rows)
    summary.attrs["total_lead_time_days"] = total_lead_time
    summary.attrs["path"] = path
    return summary
