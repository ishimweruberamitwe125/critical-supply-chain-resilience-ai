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
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
    section.main > div {
        max-width: 100%;
    }
    [data-testid="stVerticalBlock"] > div.right-panel {
        border-left: 1px solid #e2e8f0;
        padding-left: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

PAGES = [
    "Overview",
    "Risk Analysis",
    "Simulations",
    "Mitigations",
    "Network Map",
    "Forecast",
]


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


def render_navigation_panel(industry: str, page: str) -> tuple[str, str, dict | None]:
    st.subheader("Navigation")

    if st.button("Refresh pipeline data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    selected_industry = st.selectbox(
        "Industry network",
        list(INDUSTRY_OPTIONS.keys()),
        index=list(INDUSTRY_OPTIONS.keys()).index(industry),
    )

    st.markdown("---")
    selected_page = st.radio("Dashboard views", PAGES, index=PAGES.index(page))

    simulation_controls = None
    if selected_page == "Simulations":
        graph = load_graph(selected_industry)
        st.markdown("---")
        st.subheader("Scenario controls")
        node_options = {
            f"{data.get('name', node)} ({node})": node for node, data in graph.nodes(data=True)
        }
        selected_label = st.selectbox("Disrupt node", list(node_options.keys()), key="sim_disrupt_node")
        severity = st.slider("Severity", 0.0, 1.0, 1.0, 0.05, key="sim_severity")
        run_custom = st.button("Run Custom Simulation", type="primary", key="sim_run_button", use_container_width=True)
        simulation_controls = {
            "node_label": selected_label,
            "node_id": node_options[selected_label],
            "severity": severity,
            "run_custom": run_custom,
        }

    return selected_industry, selected_page, simulation_controls


def render_overview(report) -> None:
    left, right = st.columns([1.1, 1])
    with left:
        st.plotly_chart(node_risk_chart(report), use_container_width=True, key="chart_overview_node_risk")
    with right:
        st.plotly_chart(mitigation_chart(report), use_container_width=True, key="chart_overview_mitigation")
    st.dataframe(report.resilience.node_risks, use_container_width=True)


def render_risk_analysis(report) -> None:
    st.plotly_chart(supplier_risk_chart(report), use_container_width=True, key="chart_supplier_risk")
    st.dataframe(report.disruption_predictions, use_container_width=True)


def render_simulations(report, graph, simulation_controls: dict | None = None) -> None:
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

    if not simulation_controls:
        return

    st.subheader("Interactive What-If Scenario")
    if simulation_controls["run_custom"]:
        custom = run_simulation(
            graph,
            DisruptionScenario(
                node_id=simulation_controls["node_id"],
                severity=simulation_controls["severity"],
                description=f"Custom disruption: {simulation_controls['node_label']}",
            ),
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Service Level", f"{custom.service_level:.1%}")
        c2.metric("Disrupted Throughput", f"{custom.disrupted_throughput:,.0f}")
        c3.metric("Baseline Throughput", f"{custom.baseline_throughput:,.0f}")


def render_mitigations(report) -> None:
    st.plotly_chart(mitigation_chart(report), use_container_width=True, key="chart_mitigation_tab")
    for item in report.mitigations:
        st.info(f"**{item.priority}. {item.action}** — {item.rationale}")


def render_network_map(report, graph) -> None:
    st.plotly_chart(network_graph_plotly(graph), use_container_width=True, key="chart_network_map")
    st.dataframe(report.resilience.single_source_exposure, use_container_width=True)


def render_forecast(report) -> None:
    st.plotly_chart(demand_forecast_chart(report), use_container_width=True, key="chart_demand_forecast")
    st.dataframe(report.demand_forecast, use_container_width=True)


def render_page_content(page: str, report, graph, simulation_controls: dict | None) -> None:
    if page == "Overview":
        render_overview(report)
    elif page == "Risk Analysis":
        render_risk_analysis(report)
    elif page == "Simulations":
        render_simulations(report, graph, simulation_controls)
    elif page == "Mitigations":
        render_mitigations(report)
    elif page == "Network Map":
        render_network_map(report, graph)
    elif page == "Forecast":
        render_forecast(report)


def main() -> None:
    if "industry" not in st.session_state:
        st.session_state.industry = list(INDUSTRY_OPTIONS.keys())[0]
    if "page" not in st.session_state:
        st.session_state.page = PAGES[0]

    content_col, nav_col = st.columns([3.2, 1], gap="large")

    with nav_col:
        industry, page, simulation_controls = render_navigation_panel(
            st.session_state.industry,
            st.session_state.page,
        )
        st.session_state.industry = industry
        st.session_state.page = page

    config = INDUSTRY_OPTIONS[industry]
    report = load_report(industry)
    graph = load_graph(industry)

    with content_col:
        st.title("Critical Supply Chain Resilience AI")
        st.caption(config["caption"])

        st.plotly_chart(resilience_kpi_row(report), use_container_width=True, key="chart_kpi_row")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Suppliers", report.network_summary["supplier_count"])
        col2.metric("Factories", report.network_summary["factory_count"])
        col3.metric("Single-Source Links", report.network_summary["single_source_edge_count"])
        col4.metric("Network Risk Index", f"{report.resilience.network_risk_index:.3f}")

        render_page_content(page, report, graph, simulation_controls)


if __name__ == "__main__":
    main()
