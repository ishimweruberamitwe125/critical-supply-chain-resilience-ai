# Methodology

This document defines data schemas, analytical methodology, and the current prototype scope for the project.

## Datasets

The prototype includes two synthetic benchmark networks:

| Network | Raw data | Processed data | Use case |
|---------|----------|----------------|----------|
| Semiconductor | `data/raw/` | `data/processed/` | Chip fabrication and packaging |
| Energy infrastructure | `data/raw/energy/` | `data/processed/energy/` | Grid transformers and deployment |

### `suppliers.csv`

| Column | Type | Description |
|--------|------|-------------|
| `supplier_id` | string | Unique supplier identifier |
| `name` | string | Supplier display name |
| `component` | string | Material or component supplied |
| `country` | string | Supplier country |
| `reliability_score` | float | Historical reliability (0–1) |
| `lead_time_days` | int | Average lead time in days |
| `geopolitical_risk` | float | External risk proxy (0–1) |

### `nodes.csv`

| Column | Type | Description |
|--------|------|-------------|
| `node_id` | string | Unique node identifier |
| `name` | string | Facility name |
| `node_type` | string | `factory` or `distribution` |
| `region` | string | Geographic region |
| `capacity_units_per_month` | int | Monthly throughput capacity |

### `edges.csv`

| Column | Type | Description |
|--------|------|-------------|
| `edge_id` | string | Unique edge identifier |
| `source_id` | string | Upstream node or supplier ID |
| `target_id` | string | Downstream node ID |
| `material` | string | Material flowing on the edge |
| `lead_time_days` | int | Transit or processing lead time |
| `capacity_units_per_month` | int | Monthly flow capacity |
| `cost_per_unit` | float | Unit logistics/material cost |
| `is_single_source` | bool | True if no alternate supplier exists |

## Graph construction

1. Load processed CSV files with Pandas.
2. Add supplier and factory/distribution nodes with metadata attributes.
3. Add directed edges with flow attributes.
4. Validate referential integrity (every edge endpoint must exist).

## Prototype analytics pipeline

| Stage | Method | Output |
|-------|--------|--------|
| Resilience metrics | Graph centrality, dependency HHI, propagation paths | Network risk index, node risk table |
| Disruption prediction | Scikit-learn logistic regression on supplier features | Risk tiers (low / medium / high) |
| Simulation | Capacity-based throughput model with node failures | Service level, bottlenecks, recovery estimate |
| Optimization | Rank single-source mitigations by simulated service impact | Prioritized action list |
| Logistics | NetworkX shortest path by lead time | Fastest factory-to-hub route |

## Implemented vs planned methodology

| Capability | Prototype status | Notes |
|------------|------------------|-------|
| Resilience metrics | Implemented | Risk index, dependency, propagation, recovery |
| Disruption simulation | Implemented | Supplier outages and factory shutdowns |
| Disruption prediction | Prototype | Uses synthetic labels, not historical disruption data |
| Demand forecasting | Prototype | Baseline forecast from hub capacity |
| Network optimization | Prototype | Heuristic mitigation ranking |
| OR-Tools optimization | Planned | Full constrained supplier selection |
| PyTorch models | Planned | Deep learning for time-series and graph signals |
| Economic indicator feeds | Planned | External macro/geopolitical data integration |

## Assumptions

- Synthetic data is deterministic and small enough for local development.
- Reliability and geopolitical risk are normalized proxies, not live intelligence feeds.
- Capacities and lead times are monthly averages unless otherwise noted.
- Prototype outputs support research demos and decision-support exploration, not operational deployment.
