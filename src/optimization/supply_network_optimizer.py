"""Supply network optimization recommendations."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import pandas as pd

from src.resilience_metrics.risk_index import ResilienceReport, compute_risk_index
from src.simulation.supply_chain_simulator import DisruptionScenario, SimulationResult, run_simulation


@dataclass
class MitigationRecommendation:
    """Suggested action to improve supply network resilience."""

    priority: int
    action: str
    target_node: str
    material: str
    expected_service_level_gain: float
    rationale: str


def recommend_mitigations(
    graph: nx.DiGraph,
    resilience_report: ResilienceReport | None = None,
    top_n: int = 5,
) -> list[MitigationRecommendation]:
    """Rank mitigation actions from single-source exposure and simulation impact."""
    report = resilience_report or compute_risk_index(graph)
    recommendations: list[MitigationRecommendation] = []

    for rank, row in enumerate(report.single_source_exposure.itertuples(index=False), start=1):
        scenario = DisruptionScenario(
            node_id=row.source_id,
            event_type="node_failure",
            severity=1.0,
            description=f"Single-source failure for {row.material}",
        )
        simulation = run_simulation(graph, scenario)
        gain = round(1.0 - simulation.service_level, 3)

        recommendations.append(
            MitigationRecommendation(
                priority=rank,
                action="Add alternate supplier",
                target_node=row.source_name,
                material=row.material,
                expected_service_level_gain=gain,
                rationale=(
                    f"{row.source_name} is the only source of {row.material} for "
                    f"{row.target_name}. Failure drops service level to "
                    f"{simulation.service_level:.1%}."
                ),
            )
        )

    recommendations.sort(key=lambda item: item.expected_service_level_gain, reverse=True)
    for idx, recommendation in enumerate(recommendations[:top_n], start=1):
        recommendation.priority = idx

    return recommendations[:top_n]


def optimize_supply_network(graph: nx.DiGraph) -> pd.DataFrame:
    """Return a ranked mitigation plan for the supply network."""
    recommendations = recommend_mitigations(graph)
    return pd.DataFrame([rec.__dict__ for rec in recommendations])
