# Architecture

This document describes the system design for **Critical Supply Chain Resilience AI** as implemented in the current research prototype.

## System overview

The platform is organized as a layered pipeline:

```
Data ingestion → Graph model → Metrics → Forecasting → Simulation → Optimization → Reporting
```

Each layer is an independent Python module under `src/`. Shared configuration, I/O, and visualization utilities support demos, notebooks, and the web dashboard.

## Core components

| Layer | Module | Status | Responsibility |
|-------|--------|--------|----------------|
| Data | `data/raw`, `data/processed` | Implemented | Semiconductor and energy CSV datasets |
| Graph | `src/utils/graph_builder.py` | Implemented | Build NetworkX supply network from CSV |
| Metrics | `src/resilience_metrics/` | Implemented | Risk index, dependency, propagation, recovery |
| Forecasting | `src/forecasting/` | Prototype | Demand forecast and disruption prediction (sklearn) |
| Simulation | `src/simulation/` | Implemented | What-if disruption scenarios |
| Optimization | `src/optimization/` | Prototype | Mitigation ranking and shortest-path logistics |
| Orchestration | `src/pipeline.py` | Implemented | End-to-end prototype report |
| Visualization | `src/visualization/` | Implemented | Matplotlib and Plotly chart builders |
| Presentation | `examples/`, `notebooks/`, `dashboard/` | Implemented | CLI demo, case studies, Streamlit UI |

## Supply network model

The supply chain is represented as a **directed graph**:

- **Supplier nodes** provide raw materials and components.
- **Factory nodes** transform inputs into intermediate or finished goods.
- **Distribution nodes** deliver products to downstream customers.

Edges encode material flow with attributes such as lead time, capacity, unit cost, and single-source flags.

## Prototype data flow

1. Raw CSV files live in `data/raw/` (semiconductor) and `data/raw/energy/` (energy infrastructure).
2. Preparation scripts write processed CSVs to `data/processed/` and `data/processed/energy/`.
3. `build_supply_network()` loads processed data into NetworkX.
4. `run_prototype_pipeline()` executes metrics, prediction, simulation, and optimization.
5. Results are exposed through CLI demos, Jupyter notebooks, dashboard images, and the Streamlit app.

## Interfaces

| Interface | Entry point | Purpose |
|-----------|-------------|---------|
| CLI demo | `examples/semiconductor_supply_chain_demo.py` | Full terminal report |
| Web dashboard | `dashboard/app.py` | Interactive Plotly analytics |
| Notebooks | `notebooks/*.ipynb` | Research walkthroughs |
| Presentation | `scripts/generate_presentation.py` | Grant/research PowerPoint deck |

## Technology choices (current prototype)

| Technology | Role in prototype |
|------------|-------------------|
| **Python** | Core language |
| **Pandas / NumPy** | Data loading and numerical operations |
| **NetworkX** | Graph construction, paths, and topology analysis |
| **Scikit-learn** | Supplier disruption risk classifier |
| **Matplotlib / Plotly** | Static and interactive charts |
| **Streamlit** | Web dashboard |
| **Jupyter** | Case study notebooks |
| **pytest** | Automated tests |

## Planned technology (not yet integrated)

| Technology | Planned role |
|------------|--------------|
| **PyTorch** | Deep learning models for time-series and graph-based prediction |
| **Google OR-Tools** | Constrained supplier selection and logistics optimization |
| **Live data feeds** | Real-time logistics and macroeconomic indicators |

These are research roadmap items. They are documented in the README but not required to run the current prototype.

## Prototype limitations

- Uses **synthetic benchmark networks**, not live operational data.
- Disruption prediction uses **prototype labels** derived from supplier features.
- Optimization returns **heuristic mitigation rankings**, not full mathematical programming solutions.
- `models/predictive_models/` and `models/optimization_models/` are reserved for future trained artifacts.
- Medical device, aerospace, and defense case studies are described in the README but not yet implemented.

## Future extensions

- Digital twin integration with live logistics feeds
- Reinforcement learning for adaptive routing
- Multi-agent coordination across suppliers
- REST/API layer for external decision-support tools
- OR-Tools and PyTorch integration for production-grade models
