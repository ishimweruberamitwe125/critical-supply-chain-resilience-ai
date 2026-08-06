"""Week 1 setup validation and network overview demo."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.prepare_week1_data import prepare_processed_data
from src.utils.graph_builder import build_supply_network, node_degree_table, summarize_network


def main() -> None:
    prepare_processed_data()
    graph = build_supply_network()
    summary = summarize_network(graph)
    degrees = node_degree_table(graph)

    print("Critical Supply Chain Resilience AI — Week 1 Network Overview")
    print("=" * 62)
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title():32} {value}")

    print("\nNode Degree Table")
    print("-" * 62)
    print(degrees.to_string(index=False))

    single_source = [
        (source, target, data["material"])
        for source, target, data in graph.edges(data=True)
        if data.get("is_single_source")
    ]
    print("\nSingle-Source Dependencies")
    print("-" * 62)
    for source, target, material in single_source:
        source_name = graph.nodes[source]["name"]
        target_name = graph.nodes[target]["name"]
        print(f"{source_name} -> {target_name} ({material})")

    print("\nWeek 1 setup complete. Graph builder and datasets are ready.")


if __name__ == "__main__":
    main()
