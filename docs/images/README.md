# Dashboard Images

Static dashboard visuals for the prototype.

## Included assets

| File | Description |
|------|-------------|
| `dashboard_overview.svg` | Executive KPI overview |
| `supplier_risk_chart.svg` | Supplier disruption risk tiers |
| `simulation_impact.svg` | Baseline vs disrupted throughput |
| `demand_forecast.svg` | Distribution hub demand forecast |
| `supply_network_graph.svg` | Supply network topology |
| `web_dashboard_preview.png` | Streamlit dashboard preview |

## Regenerate PNG charts from live data

```bash
python scripts/generate_dashboard_images.py
```

This writes high-resolution PNG versions of all charts using the current synthetic network data.
