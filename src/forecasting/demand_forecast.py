"""Demand forecasting module (prototype placeholder)."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def forecast_demand(graph: nx.DiGraph, horizon_months: int = 3) -> pd.DataFrame:
    """
    Prototype demand forecast using distribution hub capacity as baseline demand.
    """
    distribution_nodes = [
        (node_id, data)
        for node_id, data in graph.nodes(data=True)
        if data.get("node_kind") == "distribution"
    ]
    if not distribution_nodes:
        return pd.DataFrame(columns=["month", "forecast_units"])

    hub_id, hub_data = distribution_nodes[0]
    baseline = float(hub_data.get("capacity_units_per_month", 100_000)) * 0.85

    rows = [
        {"month": month, "forecast_units": round(baseline * (1.0 + 0.02 * month), 1)}
        for month in range(1, horizon_months + 1)
    ]
    rows[0]["hub_id"] = hub_id
    return pd.DataFrame(rows)
