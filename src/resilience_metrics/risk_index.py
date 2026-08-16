"""Resilience metrics for supply chain risk assessment."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import pandas as pd


@dataclass
class ResilienceReport:
    """Aggregate resilience metrics for a supply network."""

    network_risk_index: float
    supplier_dependency_score: float
    avg_propagation_probability: float
    estimated_recovery_days: float
    node_risks: pd.DataFrame
    single_source_exposure: pd.DataFrame


def _factory_nodes(graph: nx.DiGraph) -> list[str]:
    return [node for node, data in graph.nodes(data=True) if data.get("node_kind") == "factory"]


def _distribution_nodes(graph: nx.DiGraph) -> list[str]:
    return [node for node, data in graph.nodes(data=True) if data.get("node_kind") == "distribution"]


def compute_supplier_dependency(graph: nx.DiGraph) -> float:
    """
    Measure supplier concentration across factories using a Herfindahl-style index.
    Higher values indicate greater dependency on fewer suppliers.
    """
    scores: list[float] = []

    for factory_id in _factory_nodes(graph):
        incoming = list(graph.in_edges(factory_id, data=True))
        if not incoming:
            continue

        by_material: dict[str, list[float]] = {}
        for source, _, data in incoming:
            material = data["material"]
            weight = 1.0 if data.get("is_single_source") else 0.5
            by_material.setdefault(material, []).append(weight)

        material_hhis = []
        for weights in by_material.values():
            total = sum(weights)
            shares = [weight / total for weight in weights]
            material_hhis.append(sum(share**2 for share in shares))

        if material_hhis:
            scores.append(sum(material_hhis) / len(material_hhis))

    return round(sum(scores) / len(scores), 3) if scores else 0.0


def compute_propagation_probability(graph: nx.DiGraph, failed_node: str) -> dict[str, float]:
    """
    Estimate downstream disruption probability after a node failure.
    Supplier failures use reliability; operational nodes propagate deterministically.
    """
    if failed_node not in graph:
        raise ValueError(f"Unknown node: {failed_node}")

    failed_data = graph.nodes[failed_node]
    if failed_data.get("node_kind") == "supplier":
        base_failure_prob = 1.0 - float(failed_data.get("reliability_score", 0.5))
    else:
        base_failure_prob = 1.0

    propagation: dict[str, float] = {failed_node: round(base_failure_prob, 3)}

    for target in nx.descendants(graph, failed_node):
        paths = list(nx.all_simple_paths(graph, failed_node, target))
        if not paths:
            continue

        path_probs = []
        for path in paths:
            path_prob = base_failure_prob
            for node in path[1:]:
                node_data = graph.nodes[node]
                if node_data.get("node_kind") == "supplier":
                    path_prob *= 1.0 - float(node_data.get("reliability_score", 0.5))
                else:
                    path_prob *= 0.85
            path_probs.append(path_prob)

        propagation[target] = round(min(1.0, max(path_probs)), 3)

    return propagation


def _path_lead_time(graph: nx.DiGraph, path: list[str]) -> float:
    total = 0.0
    for idx in range(len(path) - 1):
        total += float(graph.edges[path[idx], path[idx + 1]].get("lead_time_days", 7))
    return total


def estimate_recovery_days(graph: nx.DiGraph, failed_node: str) -> float:
    """Estimate recovery time using alternate path lead times and supplier reliability."""
    if failed_node not in graph:
        raise ValueError(f"Unknown node: {failed_node}")

    node_data = graph.nodes[failed_node]
    base_lead_time = float(node_data.get("lead_time_days", 14))

    downstream = nx.descendants(graph, failed_node)
    if not downstream:
        return round(base_lead_time * 1.5, 1)

    recovery_times: list[float] = []
    for target in downstream:
        best_alternate = None
        for source in graph.nodes:
            if source == failed_node:
                continue
            if not nx.has_path(graph, source, target):
                continue
            try:
                path = nx.shortest_path(graph, source, target)
            except nx.NetworkXNoPath:
                continue
            if failed_node in path:
                continue
            lead_time = _path_lead_time(graph, path)
            if best_alternate is None or lead_time < best_alternate:
                best_alternate = lead_time

        recovery_times.append(best_alternate + 7.0 if best_alternate is not None else base_lead_time + 14.0)

    return round(sum(recovery_times) / len(recovery_times), 1)


def compute_node_risk_scores(graph: nx.DiGraph) -> pd.DataFrame:
    """Compute per-node risk scores combining reliability, geo risk, and centrality."""
    rows: list[dict[str, float | str | int]] = []

    for node_id, data in graph.nodes(data=True):
        in_degree = graph.in_degree(node_id)
        out_degree = graph.out_degree(node_id)
        centrality = (in_degree + out_degree) / max(graph.number_of_nodes() - 1, 1)

        single_source_inputs = sum(
            1 for _, _, edge_data in graph.in_edges(node_id, data=True) if edge_data.get("is_single_source")
        )

        if data.get("node_kind") == "supplier":
            base_risk = (
                (1.0 - float(data.get("reliability_score", 0.5))) * 0.45
                + float(data.get("geopolitical_risk", 0.0)) * 0.35
                + centrality * 0.20
            )
        else:
            base_risk = centrality * 0.5 + single_source_inputs * 0.1

        downstream_impact = len(nx.descendants(graph, node_id))
        risk_score = round(min(1.0, base_risk + downstream_impact * 0.02), 3)

        rows.append(
            {
                "node_id": node_id,
                "name": data.get("name", node_id),
                "node_kind": data.get("node_kind", "unknown"),
                "risk_score": risk_score,
                "downstream_nodes": downstream_impact,
                "single_source_inputs": single_source_inputs,
            }
        )

    return pd.DataFrame(rows).sort_values("risk_score", ascending=False).reset_index(drop=True)


def single_source_exposure_table(graph: nx.DiGraph) -> pd.DataFrame:
    """List single-source material dependencies."""
    rows: list[dict[str, str | bool]] = []
    for source, target, data in graph.edges(data=True):
        if data.get("is_single_source"):
            rows.append(
                {
                    "source_id": source,
                    "source_name": graph.nodes[source].get("name", source),
                    "target_id": target,
                    "target_name": graph.nodes[target].get("name", target),
                    "material": data["material"],
                    "lead_time_days": data["lead_time_days"],
                }
            )
    return pd.DataFrame(rows)


def compute_risk_index(graph: nx.DiGraph) -> ResilienceReport:
    """Compute aggregate resilience metrics for the full supply network."""
    node_risks = compute_node_risk_scores(graph)
    single_source = single_source_exposure_table(graph)
    dependency = compute_supplier_dependency(graph)

    propagation_probs: list[float] = []
    recovery_days: list[float] = []
    high_risk_nodes = node_risks.head(3)["node_id"].tolist()

    for node_id in high_risk_nodes:
        propagation = compute_propagation_probability(graph, node_id)
        propagation_probs.extend(prob for node, prob in propagation.items() if node != node_id)
        recovery_days.append(estimate_recovery_days(graph, node_id))

    avg_propagation = round(sum(propagation_probs) / len(propagation_probs), 3) if propagation_probs else 0.0
    avg_recovery = round(sum(recovery_days) / len(recovery_days), 1) if recovery_days else 0.0
    avg_node_risk = float(node_risks["risk_score"].mean())

    network_risk_index = round(
        avg_node_risk * 0.35 + dependency * 0.25 + avg_propagation * 0.25 + min(avg_recovery / 30.0, 1.0) * 0.15,
        3,
    )

    return ResilienceReport(
        network_risk_index=network_risk_index,
        supplier_dependency_score=dependency,
        avg_propagation_probability=avg_propagation,
        estimated_recovery_days=avg_recovery,
        node_risks=node_risks,
        single_source_exposure=single_source,
    )
