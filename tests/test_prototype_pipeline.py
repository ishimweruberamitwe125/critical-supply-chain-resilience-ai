"""Prototype integration tests."""

from scripts.prepare_week1_data import prepare_processed_data
from src.forecasting.demand_forecast import forecast_demand
from src.forecasting.disruption_prediction import predict_disruption_risk
from src.optimization.logistics_optimizer import optimize_logistics_routes
from src.optimization.supply_network_optimizer import recommend_mitigations
from src.pipeline import run_prototype_pipeline
from src.resilience_metrics.risk_index import compute_risk_index
from src.simulation.supply_chain_simulator import DisruptionScenario, run_simulation
from src.utils.graph_builder import build_supply_network


def test_prototype_pipeline_runs() -> None:
    prepare_processed_data()
    report = run_prototype_pipeline()
    assert report.network_summary["supplier_count"] == 8
    assert report.resilience.network_risk_index >= 0.0
    assert not report.disruption_predictions.empty
    assert len(report.simulations) == 3
    assert len(report.mitigations) >= 1


def test_resilience_metrics() -> None:
    graph = build_supply_network()
    report = compute_risk_index(graph)
    assert 0.0 <= report.network_risk_index <= 1.5
    assert report.supplier_dependency_score > 0.0
    assert len(report.single_source_exposure) >= 1


def test_simulation_reduces_service_level_on_supplier_failure() -> None:
    graph = build_supply_network()
    result = run_simulation(
        graph,
        DisruptionScenario("SUP-001", description="Wafer outage"),
    )
    assert result.service_level < 1.0
    assert result.disrupted_throughput <= result.baseline_throughput


def test_disruption_prediction_outputs_tiers() -> None:
    graph = build_supply_network()
    predictions = predict_disruption_risk(graph)
    assert "disruption_probability" in predictions.columns
    assert set(predictions["risk_tier"]).issubset({"low", "medium", "high"})


def test_optimizer_and_logistics() -> None:
    graph = build_supply_network()
    mitigations = recommend_mitigations(graph)
    assert mitigations[0].expected_service_level_gain >= 0.0

    route = optimize_logistics_routes(graph, "FAC-001", "DIST-001")
    assert len(route) >= 1
    assert route.attrs["total_lead_time_days"] > 0


def test_demand_forecast() -> None:
    graph = build_supply_network()
    forecast = forecast_demand(graph, horizon_months=2)
    assert len(forecast) == 2
