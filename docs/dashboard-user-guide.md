# Live Dashboard User Guide

Use the **live prototype dashboard** to explore supply chain risk, run disruption scenarios, and review mitigation recommendations.

**Live app:** [https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/](https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/)

No installation required — open the link in any modern browser.

---

## Quick start (2 minutes)

1. Open the live dashboard link above.
2. In the **sidebar**, choose an industry network:
   - **Semiconductor** — chip fabrication and packaging supply chain
   - **Energy Infrastructure** — grid transformers and deployment equipment
3. Review the **KPI row** at the top (risk index, suppliers, single-source links).
4. Click through the **tabs** below for detailed analysis.
5. Click **Refresh pipeline data** in the sidebar to reload results after switching industry.

---

## Sidebar controls

| Control | What it does |
|---------|----------------|
| **Industry network** | Switches between semiconductor and energy benchmark networks |
| **Refresh pipeline data** | Clears cache and reruns the analytics pipeline |
| Live dashboard note | Reminds you that charts are built from code, not static images |

---

## Tab-by-tab guide

### Overview

- **Node Risk Landscape** — scatter plot of node risk vs downstream impact
- **Mitigation Priority** — materials with the highest potential service-level gain
- **Node risk table** — sortable list of all nodes with risk scores

**Use this tab to:** get an executive summary of network vulnerability.

### Risk Analysis

- **Supplier Disruption Risk** — bar chart colored by risk tier (low / medium / high)
- **Predictions table** — supplier IDs, disruption probability, and predicted tier

**Use this tab to:** identify which suppliers to monitor or diversify first.

### Simulations

- **Disruption Simulation Impact** — baseline vs disrupted throughput and service level
- **Scenario table** — pre-built outages (e.g. wafer supplier, factory shutdown)
- **Interactive What-If Scenario** — pick any node, set severity, click **Run Custom Simulation**

**Use this tab to:** stress-test the network and answer “what happens if this supplier fails?”

### Mitigations

- **Mitigation Priority chart** — ranked by expected service-level improvement
- **Recommendation cards** — specific actions (e.g. add alternate supplier for silicon wafers)

**Use this tab to:** turn analysis into actionable resilience plans.

### Network Map

- **Interactive supply graph** — suppliers (blue), factories (green), hub (orange)
- **Single-source exposure table** — materials with no alternate supplier

**Use this tab to:** see structural dependencies in the network.

### Forecast

- **Demand forecast chart** — projected hub demand over upcoming months
- **Forecast table** — numeric values behind the chart

**Use this tab to:** review baseline demand assumptions for the distribution hub.

---

## Recommended workflows

### For researchers

1. Select **Semiconductor** → **Overview** → note risk index and top nodes  
2. **Risk Analysis** → export mental model of supplier tiers  
3. **Simulations** → compare three default scenarios  
4. Switch to **Energy Infrastructure** and repeat to compare sectors  

### For companies / supply chain teams

1. Start on **Overview** and **Mitigations** for executive talking points  
2. Use **Simulations** → custom what-if on your most critical supplier node  
3. Open **Network Map** → **single-source table** for sourcing meeting agenda  
4. Share the live URL in meetings instead of static slide screenshots  

### For grant or policy audiences

1. Show live URL on slide 1  
2. Demo **Overview** KPIs and one **Simulation** scenario live  
3. Explain static README images are exports of this same engine  

---

## Static images vs live dashboard

| | README / PowerPoint PNGs | Live dashboard |
|---|--------------------------|----------------|
| Updates | Fixed at commit time | Rebuilt from pipeline on each run |
| Interaction | None | Hover, zoom, tabs, what-if slider |
| Best for | Docs, email, offline slides | Demos, reviewers, collaborators |

---

## Run locally (optional)

Developers can run the same dashboard on their machine:

```bash
pip install -r requirements.txt
python scripts/prepare_week1_data.py
python scripts/prepare_energy_data.py
streamlit run streamlit_app.py
```

See [live-dashboard.md](live-dashboard.md) for deployment and developer details.

---

## Troubleshooting

| Issue | Try this |
|-------|----------|
| App is slow on first load | Wait 30–60 seconds — Streamlit Cloud cold-starts the pipeline |
| Charts look empty | Click **Refresh pipeline data** in the sidebar |
| Results differ from slides | Slides use static PNG exports; live app uses current pipeline code |
| App won't load | Check [Streamlit status](https://status.streamlit.io/) or retry later |

---

## Contact

**David Ishimwe Ruberamitwe** — ishimwerubera@gmail.com

For collaboration, pilots, or research partnerships, include the live dashboard URL in your message.
