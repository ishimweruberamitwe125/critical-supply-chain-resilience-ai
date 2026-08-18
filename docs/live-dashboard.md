# Live Dashboard Guide

## Static screenshots vs live dashboard

| Type | What it is | Where |
|------|------------|--------|
| **Static PNG screenshots** | Snapshots for README, PowerPoint, and GitHub | `docs/images/*.png` |
| **Live dashboard** | Interactive app; charts rebuild from pipeline code on each run | `streamlit run streamlit_app.py` |

**Answer for reviewers:** README and slide screenshots are **static exports**. The **live prototype dashboard** runs from the same analytics pipeline and can be shared as a URL after deployment.

---

## Option 1 — Run live on your computer (5 minutes)

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/prepare_week1_data.py
python scripts/prepare_energy_data.py
streamlit run streamlit_app.py
```

Your browser opens at `http://localhost:8501`.

What is live:
- KPI metrics from `run_prototype_pipeline()`
- Plotly charts (hover, zoom, filter)
- Industry switch (Semiconductor / Energy)
- Custom what-if simulation slider

---

## Option 2 — Deploy a public live URL (Streamlit Community Cloud)

1. Push this repository to GitHub (already done).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**.
4. Set:
   - **Repository:** `ishimweruberamitwe125/critical-supply-chain-resilience-ai`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **Deploy**.

After deploy, copy the URL (example: `https://your-app-name.streamlit.app`) and add it to your README and presentation.

---

## Option 3 — Regenerate PNG screenshots from live pipeline data

Static images in the repo should be refreshed from the **same code** the live dashboard uses:

```powershell
pip install -r requirements.txt
python scripts/prepare_week1_data.py
python scripts/prepare_energy_data.py
python scripts/generate_dashboard_images.py
```

This writes data-driven PNGs to `docs/images/` and a metadata file `docs/images/generation_metadata.json` with timestamp and source network.

Then commit updated PNGs if you want GitHub README to match the latest pipeline output.

---

## What to tell researchers and companies

> "The images in our README and slides are static snapshots for documentation. The **live dashboard** runs our analytics pipeline in real time—you can switch industries, run disruption scenarios, and explore mitigation recommendations interactively."

Offer either:
- A **live demo** on your laptop (`streamlit run streamlit_app.py`), or
- A **public Streamlit URL** after Option 2.
