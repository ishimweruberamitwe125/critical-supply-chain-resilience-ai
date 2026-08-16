# Presentations

Grant and research presentation materials for **Critical Supply Chain Resilience AI**.

## Generate the PowerPoint deck

```bash
pip install -r requirements.txt
python scripts/generate_all_assets.py
```

This creates:

- Dashboard PNG charts in `docs/images/`
- **`Critical_Supply_Chain_Resilience_AI.pptx`** in this folder

## Presentation outline (17 slides)

1. Title
2. The Challenge
3. Research Gap
4. Project Vision
5. System Architecture
6. Core Capabilities
7. Methodology
8. Interactive Prototype Dashboard (image)
9. Executive Resilience Overview (image)
10. Simulation & Mitigation Insights (image)
11. Semiconductor Case Study
12. Energy Infrastructure Case Study
13. Policy & Strategic Impact
14. Future Research Directions
15. Collaboration & Funding Opportunity
16. Thank You

## Tips for grant and research audiences

- Lead with **national impact** and the **research gap** (slides 2–3).
- Demo the **Streamlit dashboard** live if possible: `streamlit run dashboard/app.py`
- Emphasize the **open, reproducible** Python platform and dual industry case studies.
- Close with concrete **collaboration and funding** needs (slide 15).
