# Architecture

This document describes the high-level system design for **Critical Supply Chain Resilience AI**.

## System overview

The platform is organized as a layered pipeline:

```
Data ingestion → Graph model → Metrics → Simulation → Optimization → Reporting
```

Each layer is implemented as an independent Python module under `src/`, with shared configuration and I/O utilities in `src/utils/`.

## Core components

| Layer | Module | Responsibility |
|-------|--------|----------------|
| Data | `data/raw`, `data/processed` | Supplier, node, and edge datasets |
| Graph | `src/utils/graph_builder.py` | Build NetworkX supply network from CSV |
| Metrics | `src/resilience_metrics/` | Risk index, dependency, propagation |
| Forecasting | `src/forecasting/` | Demand and disruption prediction |
| Simulation | `src/simulation/` | What-if disruption scenarios |
| Optimization | `src/optimization/` | Resilient network and logistics planning |
| Presentation | `examples/`, `notebooks/` | Demos and case studies |

## Supply network model

The supply chain is represented as a **directed graph**:

- **Supplier nodes** provide raw materials and components.
- **Factory nodes** transform inputs into intermediate or finished goods.
- **Distribution nodes** deliver products to downstream customers.

Edges encode material flow with attributes such as lead time, capacity, unit cost, and single-source flags.

## Data flow (Week 1 baseline)

1. Raw CSV files live in `data/raw/`.
2. A preparation script normalizes types and writes processed CSVs.
3. `graph_builder.build_supply_network()` loads processed data into NetworkX.
4. Example scripts and notebooks compute basic network statistics.

## Technology choices

- **NetworkX** — graph construction and centrality analysis
- **Pandas** — tabular data loading and validation
- **Scikit-learn / PyTorch** — predictive models (Week 4+)
- **Google OR-Tools** — constrained optimization (Week 6+)

## Week 1 scope

Week 1 establishes project scaffolding only:

- Repository layout and dependencies
- Synthetic semiconductor mini-network (8 suppliers, 3 factories, 1 hub)
- Graph builder and setup validation script

Downstream modules (simulation, optimization, ML) are stubbed for later weeks.

## Future extensions

- Digital twin integration with live logistics feeds
- Reinforcement learning for adaptive routing
- Multi-agent coordination across suppliers
- API layer for external decision-support tools
