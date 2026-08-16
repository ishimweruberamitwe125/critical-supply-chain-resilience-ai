# Dashboard Images

Static and generated dashboard visuals for the **Critical Supply Chain Resilience AI** prototype.

## PNG files (recommended for GitHub README)

GitHub does not reliably render SVG images in README files. Use the PNG files below for documentation and presentations.

| File | Description |
|------|-------------|
| `web_dashboard_preview.png` | Streamlit dashboard preview |
| `dashboard_overview.png` | Executive KPI overview |
| `supplier_risk_chart.png` | Supplier disruption risk tiers |
| `simulation_impact.png` | Baseline vs disrupted throughput |
| `demand_forecast.png` | Distribution hub demand forecast |
| `supply_network_graph.png` | Supply network topology |

## SVG files (optional local use)

SVG versions are also available for local viewing and editing:

- `dashboard_overview.svg`
- `supplier_risk_chart.svg`
- `simulation_impact.svg`
- `demand_forecast.svg`
- `supply_network_graph.svg`

## How to regenerate PNG charts from live pipeline data

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

This overwrites the PNG files listed above using live prototype analytics output.

## Interactive dashboard

For live interactive charts instead of static images:

```bash
streamlit run dashboard/app.py
```

## Generate images and PowerPoint together

```bash
python scripts/generate_all_assets.py
```
