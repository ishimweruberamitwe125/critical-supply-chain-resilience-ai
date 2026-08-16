"""End-to-end prototype pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from pathlib import Path

import networkx as nx
import pandas as pd

from src.forecasting.demand_forecast import forecast_demand
from src.forecasting.disruption_prediction import predict_disruption_risk
from src.optimization.logistics_optimizer import optimize_logistics_routes
from src.optimization.supply_network_optimizer import recommend_mitigations
from src.resilience_metrics.risk_index import ResilienceReport, compute_risk_index, estimate_recovery_days
from src.simulation.supply_chain_simulator import DisruptionScenario, SimulationResult, run_scenario_suite
from src.utils.graph_builder import build_supply_network, summarize_network


@dataclass
class PrototypeReport:
    """Full output from the prototype decision-support pipeline."""

    network_summary: dict[str, float | int | str]
    resilience: ResilienceReport
    disruption_predictions: pd.DataFrame
    demand_forecast: pd.DataFrame
    simulations: list[SimulationResult]
    mitigations: list
    logistics_route: pd.DataFrame


def default_scenarios(graph: nx.DiGraph) -> list[DisruptionScenario]:
    """Build a standard set of prototype disruption scenarios."""
    node_ids = set(graph.nodes)
    if any(node.startswith("ESUP-") for node in node_ids):
        scenarios = [
            DisruptionScenario("ESUP-005", description="Permanent magnet supplier outage"),
            DisruptionScenario("ESUP-004", description="Grid control software supplier outage"),
            DisruptionScenario("EFAC-002", description="Gulf Coast assembly plant shutdown"),
        ]
    else:
        scenarios = [
            DisruptionScenario("SUP-001", description="Silicon wafer supplier outage"),
            DisruptionScenario("SUP-004", description="Packaging supplier outage"),
            DisruptionScenario("FAC-002", description="East coast factory shutdown"),
        ]
    return [scenario for scenario in scenarios if scenario.node_id in graph]


def run_prototype_pipeline(graph: nx.DiGraph | None = None, data_dir: Path | None = None) -> PrototypeReport:
    """Execute the full prototype analytics pipeline on the supply network."""
    network = graph or build_supply_network(data_dir)
    resilience = compute_risk_index(network)
    predictions = predict_disruption_risk(network)
    demand = forecast_demand(network)

    scenarios = default_scenarios(network)
    simulations = run_scenario_suite(
        network,
        [
            DisruptionScenario(
                scenario.node_id,
                description=scenario.description,
                severity=scenario.severity,
            )
            for scenario in scenarios
        ],
    )

    for simulation in simulations:
        simulation.recovery_days_estimate = estimate_recovery_days(network, simulation.scenario.node_id)

    mitigations = recommend_mitigations(network, resilience)

    factory_nodes = [node for node, data in network.nodes(data=True) if data.get("node_kind") == "factory"]
    hub_nodes = [node for node, data in network.nodes(data=True) if data.get("node_kind") == "distribution"]
    logistics_route = optimize_logistics_routes(network, factory_nodes[0], hub_nodes[0])

    return PrototypeReport(
        network_summary=summarize_network(network),
        resilience=resilience,
        disruption_predictions=predictions,
        demand_forecast=demand,
        simulations=simulations,
        mitigations=mitigations,
        logistics_route=logistics_route,
    )
