"""Interactive Plotly charts for the Streamlit dashboard."""

from __future__ import annotations

import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.pipeline import PrototypeReport
from src.visualization.dashboard_charts import NODE_COLORS


def kpi_gauge(label: str, value: float, max_value: float, color: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": label, "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, max_value]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, max_value * 0.33], "color": "#dcfce7"},
                    {"range": [max_value * 0.33, max_value * 0.66], "color": "#fef9c3"},
                    {"range": [max_value * 0.66, max_value], "color": "#fee2e2"},
                ],
            },
        )
    )
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=50, b=10))
    return fig


def resilience_kpi_row(report: PrototypeReport) -> go.Figure:
    metrics = [
        ("Network Risk Index", report.resilience.network_risk_index, 1.0, "#dc2626"),
        ("Supplier Dependency", report.resilience.supplier_dependency_score, 1.0, "#ea580c"),
        ("Propagation Risk", report.resilience.avg_propagation_probability, 1.0, "#ca8a04"),
        ("Recovery Days", report.resilience.estimated_recovery_days, 40.0, "#2563eb"),
    ]
    fig = make_subplots(rows=1, cols=4, specs=[[{"type": "indicator"}] * 4])
    for idx, (label, value, max_value, color) in enumerate(metrics, start=1):
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=value,
                title={"text": label},
                number={"font": {"color": color, "size": 28}},
            ),
            row=1,
            col=idx,
        )
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def supplier_risk_chart(report: PrototypeReport) -> go.Figure:
    df = report.disruption_predictions.copy()
    color_map = {"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"}
    fig = px.bar(
        df,
        x="disruption_probability",
        y="name",
        color="risk_tier",
        color_discrete_map=color_map,
        orientation="h",
        hover_data=["supplier_id", "predicted_disruption"],
        title="Supplier Disruption Risk",
    )
    fig.update_layout(height=420, yaxis={"categoryorder": "total ascending"}, legend_title_text="Risk Tier")
    return fig


def simulation_chart(report: PrototypeReport) -> go.Figure:
    rows = []
    for result in report.simulations:
        rows.append(
            {
                "scenario": result.scenario.description,
                "baseline": result.baseline_throughput,
                "disrupted": result.disrupted_throughput,
                "service_level_pct": result.service_level * 100,
            }
        )
    df = pd.DataFrame(rows)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Baseline", x=df["scenario"], y=df["baseline"], marker_color="#94a3b8"))
    fig.add_trace(go.Bar(name="Disrupted", x=df["scenario"], y=df["disrupted"], marker_color="#ef4444"))
    fig.add_trace(
        go.Scatter(
            name="Service Level %",
            x=df["scenario"],
            y=df["service_level_pct"],
            mode="lines+markers",
            yaxis="y2",
            line={"color": "#2563eb", "width": 3},
        )
    )
    fig.update_layout(
        title="Disruption Simulation Impact",
        barmode="group",
        height=450,
        yaxis={"title": "Throughput (units/month)"},
        yaxis2={"title": "Service Level (%)", overlaying="y", side="right", range=[0, 105]},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
    )
    return fig


def mitigation_chart(report: PrototypeReport) -> go.Figure:
    df = pd.DataFrame([item.__dict__ for item in report.mitigations])
    if df.empty:
        return go.Figure()
    fig = px.bar(
        df,
        x="expected_service_level_gain",
        y="material",
        color="target_node",
        orientation="h",
        hover_data=["action", "rationale"],
        title="Mitigation Priority (Potential Service Gain)",
    )
    fig.update_layout(height=380, yaxis={"categoryorder": "total ascending"})
    return fig


def demand_forecast_chart(report: PrototypeReport) -> go.Figure:
    fig = px.line(
        report.demand_forecast,
        x="month",
        y="forecast_units",
        markers=True,
        title="Distribution Hub Demand Forecast",
    )
    fig.update_layout(height=360, xaxis={"title": "Month"}, yaxis={"title": "Forecast Units"})
    return fig


def node_risk_chart(report: PrototypeReport) -> go.Figure:
    df = report.resilience.node_risks.head(10)
    fig = px.scatter(
        df,
        x="downstream_nodes",
        y="risk_score",
        size="single_source_inputs",
        color="node_kind",
        hover_name="name",
        title="Node Risk Landscape",
    )
    fig.update_layout(height=420)
    return fig


def network_graph_plotly(graph: nx.DiGraph) -> go.Figure:
    pos = nx.spring_layout(graph, seed=42, k=1.4)
    edge_x, edge_y = [], []
    for source, target in graph.edges:
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line={"width": 1.2, "color": "#94a3b8"},
        hoverinfo="none",
        mode="lines",
    )

    node_x, node_y, texts, colors, sizes = [], [], [], [], []
    for node_id, data in graph.nodes(data=True):
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        texts.append(f"{data.get('name', node_id)}<br>{data.get('node_kind', 'node')}")
        colors.append(NODE_COLORS.get(data.get("node_kind", "supplier"), "#64748b"))
        sizes.append(26 if data.get("node_kind") == "distribution" else 18)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=[graph.nodes[n].get("name", n).split()[0] for n in graph.nodes],
        textposition="top center",
        hovertext=texts,
        hoverinfo="text",
        marker={"size": sizes, "color": colors, "line": {"width": 1, "color": "#ffffff"}},
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Interactive Supply Network Map",
        showlegend=False,
        height=520,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig
