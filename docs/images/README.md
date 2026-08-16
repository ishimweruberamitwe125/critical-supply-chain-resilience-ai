# Dashboard Images

Static and generated dashboard visuals for the **Critical Supply Chain Resilience AI** prototype.

## Files in this folder

| File | Type | Description |
|------|------|-------------|
| `web_dashboard_preview.png` | PNG | Streamlit dashboard preview |
| `dashboard_overview.svg` | SVG | Executive KPI overview |
| `supplier_risk_chart.svg` | SVG | Supplier disruption risk tiers |
| `simulation_impact.svg` | SVG | Baseline vs disrupted throughput |
| `demand_forecast.svg` | SVG | Distribution hub demand forecast |
| `supply_network_graph.svg` | SVG | Supply network topology |

## How to generate PNG charts from live data

1. Set up the project (from the repository root):

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python scripts/prepare_week1_data.py
python scripts/prepare_energy_data.py
```

2. Generate dashboard PNGs:

```bash
python scripts/generate_dashboard_images.py
```

3. Output PNG files:

- `dashboard_overview.png`
- `supplier_risk_chart.png`
- `simulation_impact.png`
- `demand_forecast.png`
- `supply_network_graph.png`
- `web_dashboard_preview.png`

## Interactive dashboard

For live interactive charts instead of static images:

```bash
streamlit run dashboard/app.py
```

## Generate images and PowerPoint together

```bash
python scripts/generate_all_assets.py
```
