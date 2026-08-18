"""Streamlit web dashboard for the supply chain resilience prototype."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.prepare_energy_data import prepare_energy_data
from scripts.prepare_week1_data import prepare_processed_data
from src.pipeline import run_prototype_pipeline
from src.simulation.supply_chain_simulator import DisruptionScenario, run_simulation
from src.utils.config import ENERGY_DATA_DIR, SEMICONDUCTOR_DATA_DIR
from src.utils.graph_builder import build_supply_network
from src.visualization.plotly_charts import (
    demand_forecast_chart,
    mitigation_chart,
    network_graph_plotly,
    node_risk_chart,
    resilience_kpi_row,
    simulation_chart,
    supplier_risk_chart,
)

st.set_page_config(
    page_title="Supply Chain Resilience AI",
    page_icon="🛡️",
    layout="wide",
)

INDUSTRY_OPTIONS = {
    "Semiconductor": {
        "prepare": prepare_processed_data,
        "data_dir": SEMICONDUCTOR_DATA_DIR,
        "caption": "Semiconductor fabrication and packaging network",
    },
    "Energy Infrastructure": {
        "prepare": prepare_energy_data,
        "data_dir": ENERGY_DATA_DIR,
        "caption": "Grid transformers and energy equipment network",
    },
}


@st.cache_data
def load_report(industry: str):
    config = INDUSTRY_OPTIONS[industry]
    config["prepare"]()
    return run_prototype_pipeline(data_dir=config["data_dir"])


@st.cache_data
def load_graph(industry: str):
    config = INDUSTRY_OPTIONS[industry]
    config["prepare"]()
    return build_supply_network(config["data_dir"])


def main() -> None:
    st.sidebar.title("Navigation")
    st.sidebar.info(
        "**Live dashboard** — charts are built from the analytics pipeline on each run. "
        "README/PowerPoint PNGs are static exports of this same engine."
    )
    if st.sidebar.button("Refresh pipeline data"):
        st.cache_data.clear()
        st.rerun()

    industry = st.sidebar.selectbox("Industry network", list(INDUSTRY_OPTIONS.keys()))
    config = INDUSTRY_OPTIONS[industry]

    report = load_report(industry)
    graph = load_graph(industry)

    st.title("Critical Supply Chain Resilience AI")
    st.caption(config["caption"])

    st.plotly_chart(resilience_kpi_row(report), use_container_width=True, key="chart_kpi_row")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Suppliers", report.network_summary["supplier_count"])
    col2.metric("Factories", report.network_summary["factory_count"])
    col3.metric("Single-Source Links", report.network_summary["single_source_edge_count"])
    col4.metric("Network Risk Index", f"{report.resilience.network_risk_index:.3f}")

    tab_overview, tab_risk, tab_sim, tab_mitigate, tab_network, tab_forecast = st.tabs(
        ["Overview", "Risk Analysis", "Simulations", "Mitigations", "Network Map", "Forecast"]
    )

    with tab_overview:
        left, right = st.columns([1.1, 1])
        with left:
            st.plotly_chart(node_risk_chart(report), use_container_width=True, key="chart_overview_node_risk")
        with right:
            st.plotly_chart(mitigation_chart(report), use_container_width=True, key="chart_overview_mitigation")
        st.dataframe(report.resilience.node_risks, use_container_width=True)

    with tab_risk:
        st.plotly_chart(supplier_risk_chart(report), use_container_width=True, key="chart_supplier_risk")
        st.dataframe(report.disruption_predictions, use_container_width=True)

    with tab_sim:
        st.plotly_chart(simulation_chart(report), use_container_width=True, key="chart_simulation")
        sim_rows = []
        for result in report.simulations:
            sim_rows.append(
                {
                    "Scenario": result.scenario.description,
                    "Service Level": f"{result.service_level:.1%}",
                    "Baseline Throughput": result.baseline_throughput,
                    "Disrupted Throughput": result.disrupted_throughput,
                    "Recovery Days": result.recovery_days_estimate,
                    "Bottlenecks": ", ".join(result.bottleneck_materials) or "None",
                }
            )
        st.dataframe(pd.DataFrame(sim_rows), use_container_width=True)

        st.subheader("Interactive What-If Scenario")
        node_options = {
            f"{data.get('name', node)} ({node})": node for node, data in graph.nodes(data=True)
        }
        selected_label = st.selectbox("Disrupt node", list(node_options.keys()), key="sim_disrupt_node")
        severity = st.slider("Severity", 0.0, 1.0, 1.0, 0.05, key="sim_severity")
        if st.button("Run Custom Simulation", type="primary", key="sim_run_button"):
            custom = run_simulation(
                graph,
                DisruptionScenario(
                    node_id=node_options[selected_label],
                    severity=severity,
                    description=f"Custom disruption: {selected_label}",
                ),
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Service Level", f"{custom.service_level:.1%}")
            c2.metric("Disrupted Throughput", f"{custom.disrupted_throughput:,.0f}")
            c3.metric("Baseline Throughput", f"{custom.baseline_throughput:,.0f}")

    with tab_mitigate:
        st.plotly_chart(mitigation_chart(report), use_container_width=True, key="chart_mitigation_tab")
        for item in report.mitigations:
            st.info(f"**{item.priority}. {item.action}** — {item.rationale}")

    with tab_network:
        st.plotly_chart(network_graph_plotly(graph), use_container_width=True, key="chart_network_map")
        st.dataframe(report.resilience.single_source_exposure, use_container_width=True)

    with tab_forecast:
        st.plotly_chart(demand_forecast_chart(report), use_container_width=True, key="chart_demand_forecast")
        st.dataframe(report.demand_forecast, use_container_width=True)


if __name__ == "__main__":
    main()
