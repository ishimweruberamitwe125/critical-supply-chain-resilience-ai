# Methodology

This document defines data schemas and analytical methodology for the project.

## Week 1 datasets

Week 1 uses a **synthetic semiconductor supply network** for development and demos.

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

## Week 1 analytics

The Week 1 example script reports:

- Node and edge counts
- In-degree and out-degree per node
- Single-source edge count
- Average supplier reliability and geopolitical risk

These baseline statistics feed resilience metrics in Week 2.

## Later-week methodology (preview)

| Week | Focus |
|------|-------|
| 2 | Resilience metrics (dependency, propagation, risk index) |
| 3 | Disruption simulation engine |
| 4–5 | Forecasting and disruption prediction models |
| 6–7 | OR-Tools optimization and end-to-end demos |

## Assumptions

- Synthetic data is deterministic and small enough for local development.
- Reliability and geopolitical risk are normalized proxies, not live intelligence feeds.
- Capacities and lead times are monthly averages unless otherwise noted.
