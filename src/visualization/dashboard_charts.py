"""Shared chart builders for notebooks, dashboard, and exported images."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.figure import Figure

from src.pipeline import PrototypeReport, run_prototype_pipeline
from src.utils.graph_builder import build_supply_network

NODE_COLORS = {
    "supplier": "#2563eb",
    "factory": "#059669",
    "distribution": "#d97706",
}


def _style_axes(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def build_overview_figure(report: PrototypeReport) -> Figure:
    """Multi-panel executive overview dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Supply Chain Resilience Dashboard — Overview", fontsize=14, fontweight="bold")

    metrics = {
        "Network Risk Index": report.resilience.network_risk_index,
        "Supplier Dependency": report.resilience.supplier_dependency_score,
        "Propagation Risk": report.resilience.avg_propagation_probability,
        "Recovery Days": report.resilience.estimated_recovery_days,
    }
    axes[0, 0].bar(metrics.keys(), metrics.values(), color=["#dc2626", "#ea580c", "#ca8a04", "#2563eb"])
    axes[0, 0].tick_params(axis="x", rotation=20)
    _style_axes(axes[0, 0], "Resilience KPIs")

    predictions = report.disruption_predictions.head(8)
    axes[0, 1].barh(predictions["name"], predictions["disruption_probability"], color="#7c3aed")
    axes[0, 1].invert_yaxis()
    _style_axes(axes[0, 1], "Top Supplier Disruption Risk")

    sim_labels = [result.scenario.description for result in report.simulations]
    service_levels = [result.service_level * 100 for result in report.simulations]
    axes[1, 0].bar(sim_labels, service_levels, color="#0891b2")
    axes[1, 0].set_ylim(0, 105)
    axes[1, 0].set_ylabel("Service Level (%)")
    axes[1, 0].tick_params(axis="x", rotation=15)
    _style_axes(axes[1, 0], "Disruption Scenario Impact")

    mitigations = pd.DataFrame([item.__dict__ for item in report.mitigations])
    if not mitigations.empty:
        axes[1, 1].barh(
            mitigations["material"],
            mitigations["expected_service_level_gain"] * 100,
            color="#16a34a",
        )
        axes[1, 1].invert_yaxis()
        axes[1, 1].set_xlabel("Potential Service Gain (%)")
    _style_axes(axes[1, 1], "Mitigation Priority")

    fig.tight_layout()
    return fig


def build_supplier_risk_figure(report: PrototypeReport) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    predictions = report.disruption_predictions.copy()
    colors = predictions["risk_tier"].map({"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"})
    ax.bar(predictions["name"], predictions["disruption_probability"], color=colors)
    ax.set_ylabel("Disruption Probability")
    ax.tick_params(axis="x", rotation=30)
    _style_axes(ax, "Supplier Disruption Risk by Tier")
    fig.tight_layout()
    return fig


def build_simulation_figure(report: PrototypeReport) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    rows = []
    for result in report.simulations:
        rows.append(
            {
                "scenario": result.scenario.description,
                "baseline": result.baseline_throughput,
                "disrupted": result.disrupted_throughput,
            }
        )
    df = pd.DataFrame(rows)
    x = range(len(df))
    width = 0.35
    ax.bar([idx - width / 2 for idx in x], df["baseline"], width, label="Baseline", color="#94a3b8")
    ax.bar([idx + width / 2 for idx in x], df["disrupted"], width, label="Disrupted", color="#ef4444")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["scenario"], rotation=15)
    ax.set_ylabel("Throughput (units/month)")
    ax.legend()
    _style_axes(ax, "Simulation: Baseline vs Disrupted Throughput")
    fig.tight_layout()
    return fig


def build_demand_forecast_figure(report: PrototypeReport) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    forecast = report.demand_forecast
    ax.plot(forecast["month"], forecast["forecast_units"], marker="o", linewidth=2, color="#2563eb")
    ax.set_xlabel("Month")
    ax.set_ylabel("Forecast Units")
    _style_axes(ax, "Distribution Hub Demand Forecast")
    fig.tight_layout()
    return fig


def build_network_graph_figure(graph: nx.DiGraph | None = None) -> Figure:
    network = graph or build_supply_network()
    fig, ax = plt.subplots(figsize=(12, 8))

    pos = nx.spring_layout(network, seed=42, k=1.4)
    node_colors = [NODE_COLORS.get(network.nodes[node].get("node_kind", "supplier"), "#64748b") for node in network.nodes]
    labels = {node: network.nodes[node].get("name", node).split()[0] for node in network.nodes}

    nx.draw_networkx_nodes(network, pos, node_color=node_colors, node_size=900, alpha=0.92, ax=ax)
    nx.draw_networkx_edges(network, pos, edge_color="#94a3b8", arrows=True, arrowsize=16, ax=ax)
    nx.draw_networkx_labels(network, pos, labels=labels, font_size=8, ax=ax)

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10, label=kind.title())
        for kind, color in NODE_COLORS.items()
    ]
    ax.legend(handles=legend_handles, loc="upper left")
    ax.set_title("Semiconductor Supply Network Topology", fontsize=12, fontweight="bold")
    ax.axis("off")
    fig.tight_layout()
    return fig


def build_web_dashboard_preview(report: PrototypeReport) -> Figure:
    """Static preview mimicking the Streamlit dashboard layout."""
    fig = plt.figure(figsize=(14, 9))
    fig.suptitle("Critical Supply Chain Resilience AI — Web Dashboard Preview", fontsize=15, fontweight="bold")

    gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35)

    ax_kpi = fig.add_subplot(gs[0, :])
    kpis = [
        ("Risk Index", report.resilience.network_risk_index, "#dc2626"),
        ("Dependency", report.resilience.supplier_dependency_score, "#ea580c"),
        ("Suppliers", report.network_summary["supplier_count"], "#2563eb"),
        ("Single Source", report.network_summary["single_source_edge_count"], "#9333ea"),
    ]
    ax_kpi.axis("off")
    for idx, (label, value, color) in enumerate(kpis):
        ax_kpi.text(
            idx * 0.24 + 0.02,
            0.55,
            label,
            fontsize=11,
            color="#475569",
            transform=ax_kpi.transAxes,
        )
        ax_kpi.text(
            idx * 0.24 + 0.02,
            0.15,
            f"{value}",
            fontsize=20,
            fontweight="bold",
            color=color,
            transform=ax_kpi.transAxes,
        )

    ax_risk = fig.add_subplot(gs[1, 0])
    top = report.disruption_predictions.head(5)
    ax_risk.barh(top["name"], top["disruption_probability"], color="#7c3aed")
    ax_risk.invert_yaxis()
    _style_axes(ax_risk, "Supplier Risk")

    ax_sim = fig.add_subplot(gs[1, 1])
    ax_sim.bar(
        [result.scenario.description.split()[0] for result in report.simulations],
        [result.service_level * 100 for result in report.simulations],
        color="#0891b2",
    )
    _style_axes(ax_sim, "Scenario Service Level")

    ax_forecast = fig.add_subplot(gs[1, 2])
    ax_forecast.plot(
        report.demand_forecast["month"],
        report.demand_forecast["forecast_units"],
        marker="o",
        color="#2563eb",
    )
    _style_axes(ax_forecast, "Demand Forecast")

    ax_network = fig.add_subplot(gs[2, :])
    network = build_supply_network()
    pos = nx.spring_layout(network, seed=42, k=1.3)
    node_colors = [NODE_COLORS.get(network.nodes[node].get("node_kind", "supplier"), "#64748b") for node in network.nodes]
    nx.draw_networkx_nodes(network, pos, node_color=node_colors, node_size=700, ax=ax_network)
    nx.draw_networkx_edges(network, pos, edge_color="#cbd5e1", arrows=True, arrowsize=12, ax=ax_network)
    ax_network.set_title("Live Network Map", fontsize=11, fontweight="bold")
    ax_network.axis("off")

    return fig


def save_dashboard_images(output_dir: Path | None = None) -> list[Path]:
    """Generate and save all dashboard images to docs/images/."""
    output = output_dir or Path(__file__).resolve().parents[2] / "docs" / "images"
    output.mkdir(parents=True, exist_ok=True)

    report = run_prototype_pipeline()
    figures = {
        "dashboard_overview.png": build_overview_figure(report),
        "supplier_risk_chart.png": build_supplier_risk_figure(report),
        "simulation_impact.png": build_simulation_figure(report),
        "demand_forecast.png": build_demand_forecast_figure(report),
        "supply_network_graph.png": build_network_graph_figure(),
        "web_dashboard_preview.png": build_web_dashboard_preview(report),
    }

    saved: list[Path] = []
    for filename, figure in figures.items():
        path = output / filename
        figure.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(figure)
        saved.append(path)

    return saved
