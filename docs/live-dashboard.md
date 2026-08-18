# Live Dashboard Guide

## Live app URL

**[https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/](https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/)**

**User guide:** [dashboard-user-guide.md](dashboard-user-guide.md)

## Static screenshots vs live dashboard

| Type | What it is | Where |
|------|------------|--------|
| **Static PNG screenshots** | Snapshots for README, PowerPoint, and GitHub | `docs/images/*.png` |
| **Live dashboard** | Interactive app; charts rebuild from pipeline code on each run | [Live URL](https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/) |

**Answer for reviewers:** README and slide screenshots are **static exports**. The **live prototype dashboard** runs from the same analytics pipeline at the URL above.

---

## Option 1 — Use the public live app (easiest)

Open: [https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/](https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/)

Follow [dashboard-user-guide.md](dashboard-user-guide.md) for tab-by-tab instructions.

---

## Option 2 — Run live on your computer

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

---

## Option 3 — Redeploy or update Streamlit Cloud

App settings on [share.streamlit.io](https://share.streamlit.io):

- **Repository:** `ishimweruberamitwe125/critical-supply-chain-resilience-ai`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`

Click **Reboot app** after pushing GitHub updates.

---

## Option 4 — Regenerate PNG screenshots from live pipeline data

```powershell
pip install -r requirements.txt
python scripts/prepare_week1_data.py
python scripts/prepare_energy_data.py
python scripts/generate_dashboard_images.py
```

This writes data-driven PNGs to `docs/images/` and `docs/images/generation_metadata.json`.

---

## What to tell researchers and companies

> "The images in our README and slides are static snapshots. Our **live dashboard** runs the analytics pipeline in real time—you can explore it here: https://critical-supply-chain-resilience-ai-by7jr2dvkuxue3doembshj.streamlit.app/"

Share the [user guide](dashboard-user-guide.md) so they know how to navigate each tab.
