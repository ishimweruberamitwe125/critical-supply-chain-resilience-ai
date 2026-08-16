"""Semiconductor supply chain prototype demo."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.prepare_week1_data import prepare_processed_data
from src.pipeline import run_prototype_pipeline


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


def main() -> None:
    prepare_processed_data()
    report = run_prototype_pipeline()

    print("Critical Supply Chain Resilience AI — Prototype Demo")
    print_section("Network Summary")
    for key, value in report.network_summary.items():
        print(f"{key.replace('_', ' ').title():32} {value}")

    print_section("Resilience Metrics")
    print(f"Network Risk Index               {report.resilience.network_risk_index}")
    print(f"Supplier Dependency Score        {report.resilience.supplier_dependency_score}")
    print(f"Avg Propagation Probability      {report.resilience.avg_propagation_probability}")
    print(f"Estimated Recovery Days          {report.resilience.estimated_recovery_days}")

    print("\nTop At-Risk Nodes")
    print(report.resilience.node_risks.head(5).to_string(index=False))

    print_section("Disruption Predictions")
    print(report.disruption_predictions.to_string(index=False))

    print_section("Demand Forecast")
    print(report.demand_forecast.to_string(index=False))

    print_section("Disruption Simulations")
    for result in report.simulations:
        print(
            f"- {result.scenario.description}: "
            f"service level {result.service_level:.1%}, "
            f"throughput {result.disrupted_throughput:,.0f}/{result.baseline_throughput:,.0f}, "
            f"recovery ~{result.recovery_days_estimate} days"
        )
        if result.bottleneck_materials:
            print(f"  Bottlenecks: {', '.join(result.bottleneck_materials)}")

    print_section("Mitigation Recommendations")
    for recommendation in report.mitigations:
        print(
            f"{recommendation.priority}. {recommendation.action} for {recommendation.target_node} "
            f"({recommendation.material}) — potential gain {recommendation.expected_service_level_gain:.1%}"
        )
        print(f"   {recommendation.rationale}")

    print_section("Logistics Route (Fastest Factory to Hub)")
    print(report.logistics_route.to_string(index=False))
    print(f"Total lead time: {report.logistics_route.attrs['total_lead_time_days']} days")

    print("\nPrototype pipeline complete.")


if __name__ == "__main__":
    main()
