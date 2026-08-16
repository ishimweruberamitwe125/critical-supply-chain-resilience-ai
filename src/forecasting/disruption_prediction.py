"""Disruption prediction using supplier risk features."""

from __future__ import annotations

import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def _supplier_feature_frame(graph: nx.DiGraph) -> pd.DataFrame:
    rows: list[dict[str, float | str | bool]] = []
    for node_id, data in graph.nodes(data=True):
        if data.get("node_kind") != "supplier":
            continue

        single_source_outputs = any(
            edge_data.get("is_single_source")
            for _, _, edge_data in graph.out_edges(node_id, data=True)
        )
        downstream_nodes = len(nx.descendants(graph, node_id))

        rows.append(
            {
                "supplier_id": node_id,
                "name": data.get("name", node_id),
                "reliability_score": float(data.get("reliability_score", 0.5)),
                "geopolitical_risk": float(data.get("geopolitical_risk", 0.0)),
                "lead_time_days": float(data.get("lead_time_days", 14)),
                "single_source_flag": float(single_source_outputs),
                "downstream_nodes": float(downstream_nodes),
            }
        )
    return pd.DataFrame(rows)


def _synthetic_disruption_labels(features: pd.DataFrame) -> pd.Series:
    risk = (
        (1.0 - features["reliability_score"]) * 0.45
        + features["geopolitical_risk"] * 0.35
        + features["single_source_flag"] * 0.20
    )
    return (risk >= 0.35).astype(int)


def predict_disruption_risk(graph: nx.DiGraph) -> pd.DataFrame:
    """
    Predict supplier disruption risk using a lightweight logistic model.
    Prototype uses synthetic labels derived from reliability and geo-risk signals.
    """
    features = _supplier_feature_frame(graph)
    if features.empty:
        return pd.DataFrame()

    labels = _synthetic_disruption_labels(features)
    feature_cols = [
        "reliability_score",
        "geopolitical_risk",
        "lead_time_days",
        "single_source_flag",
        "downstream_nodes",
    ]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(features[feature_cols])

    model = LogisticRegression(max_iter=500)
    model.fit(x_scaled, labels)
    probabilities = model.predict_proba(x_scaled)[:, 1]

    result = features[["supplier_id", "name"]].copy()
    result["disruption_probability"] = probabilities.round(3)
    result["predicted_disruption"] = (probabilities >= 0.5).astype(int)
    result["risk_tier"] = pd.cut(
        probabilities,
        bins=[-0.001, 0.35, 0.6, 1.0],
        labels=["low", "medium", "high"],
    ).astype(str)

    return result.sort_values("disruption_probability", ascending=False).reset_index(drop=True)
