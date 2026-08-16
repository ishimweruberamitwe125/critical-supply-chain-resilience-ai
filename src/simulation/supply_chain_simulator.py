"""Supply chain disruption simulation engine."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


@dataclass
class DisruptionScenario:
    """Defines a what-if disruption event."""

    node_id: str
    event_type: str = "node_failure"
    severity: float = 1.0
    description: str = ""


@dataclass
class SimulationResult:
    """Outcome metrics for a simulated disruption."""

    scenario: DisruptionScenario
    baseline_throughput: float
    disrupted_throughput: float
    service_level: float
    affected_nodes: list[str]
    bottleneck_materials: list[str]
    recovery_days_estimate: float


def _distribution_targets(graph: nx.DiGraph) -> list[str]:
    return [node for node, data in graph.nodes(data=True) if data.get("node_kind") == "distribution"]


def _effective_node_capacity(graph: nx.DiGraph, node_id: str, disabled_nodes: set[str]) -> float:
    if node_id in disabled_nodes:
        return 0.0

    data = graph.nodes[node_id]
    if data.get("node_kind") == "supplier":
        return float(data.get("reliability_score", 1.0)) * 100_000

    return float(data.get("capacity_units_per_month", 0))


def _factory_throughput(graph: nx.DiGraph, factory_id: str, disabled_nodes: set[str]) -> tuple[float, list[str]]:
    incoming = list(graph.in_edges(factory_id, data=True))
    if not incoming:
        return _effective_node_capacity(graph, factory_id, disabled_nodes), []

    material_caps: dict[str, float] = {}
    bottlenecks: list[str] = []

    for source, _, edge_data in incoming:
        if source in disabled_nodes:
            available = 0.0
            bottlenecks.append(edge_data["material"])
        else:
            source_cap = _effective_node_capacity(graph, source, disabled_nodes)
            available = min(source_cap, float(edge_data["capacity_units_per_month"]))

        material = edge_data["material"]
        material_caps[material] = material_caps.get(material, available) if source not in disabled_nodes else 0.0
        if available == 0.0:
            bottlenecks.append(material)

    inbound_capacity = min(material_caps.values()) if material_caps else 0.0
    factory_capacity = _effective_node_capacity(graph, factory_id, disabled_nodes)
    return min(inbound_capacity, factory_capacity), bottlenecks


def _network_throughput(graph: nx.DiGraph, disabled_nodes: set[str] | None = None) -> tuple[float, list[str], list[str]]:
    disabled = disabled_nodes or set()
    affected: list[str] = []
    bottlenecks: list[str] = []

    factory_outputs: dict[str, float] = {}
    for node_id, data in graph.nodes(data=True):
        if data.get("node_kind") != "factory":
            continue
        throughput, factory_bottlenecks = _factory_throughput(graph, node_id, disabled)
        factory_outputs[node_id] = throughput
        bottlenecks.extend(factory_bottlenecks)
        if throughput == 0.0:
            affected.append(node_id)

    total_factory_output = sum(factory_outputs.values())

    distribution_nodes = _distribution_targets(graph)
    if not distribution_nodes:
        return total_factory_output, affected, bottlenecks

    hub_capacity = min(
        _effective_node_capacity(graph, hub_id, disabled) for hub_id in distribution_nodes
    )
    inbound_to_hub = 0.0
    for factory_id, output in factory_outputs.items():
        for _, target, edge_data in graph.out_edges(factory_id, data=True):
            if target in distribution_nodes:
                inbound_to_hub += min(output, float(edge_data["capacity_units_per_month"]))

    throughput = min(hub_capacity, inbound_to_hub)
    for node_id in disabled:
        affected.append(node_id)
        for descendant in nx.descendants(graph, node_id):
            if descendant not in affected:
                affected.append(descendant)

    return throughput, sorted(set(affected)), sorted(set(bottlenecks))


def run_simulation(
    graph: nx.DiGraph,
    scenario: DisruptionScenario,
    recovery_days_estimate: float = 21.0,
) -> SimulationResult:
    """Simulate a disruption scenario and compare throughput against baseline."""
    if scenario.node_id not in graph:
        raise ValueError(f"Unknown node in scenario: {scenario.node_id}")

    baseline, _, _ = _network_throughput(graph)
    severity = max(0.0, min(1.0, scenario.severity))
    disabled = {scenario.node_id} if severity >= 0.99 else set()

    if severity < 0.99 and severity > 0.0:
        modified = graph.copy()
        node_data = modified.nodes[scenario.node_id]
        if "capacity_units_per_month" in node_data:
            node_data["capacity_units_per_month"] = int(
                node_data["capacity_units_per_month"] * (1.0 - severity)
            )
        disrupted, affected, bottlenecks = _network_throughput(modified)
    else:
        disrupted, affected, bottlenecks = _network_throughput(graph, disabled)

    service_level = 0.0 if baseline == 0 else round(disrupted / baseline, 3)

    return SimulationResult(
        scenario=scenario,
        baseline_throughput=round(baseline, 1),
        disrupted_throughput=round(disrupted, 1),
        service_level=service_level,
        affected_nodes=affected,
        bottleneck_materials=bottlenecks,
        recovery_days_estimate=recovery_days_estimate,
    )


def run_scenario_suite(graph: nx.DiGraph, scenarios: list[DisruptionScenario]) -> list[SimulationResult]:
    """Run multiple disruption scenarios."""
    return [run_simulation(graph, scenario) for scenario in scenarios]
