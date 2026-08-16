# Presentations

Grant, research, and industry presentation materials for **Critical Supply Chain Resilience AI**.

## Download the prototype presentation

**[Critical_Supply_Chain_Resilience_AI.pptx](Critical_Supply_Chain_Resilience_AI.pptx)**

Use this deck when presenting to:

- University researchers and labs
- Manufacturing and supply chain teams
- Grant funders and policy stakeholders
- Industry partners evaluating pilot collaborations

## Slide outline (22 slides)

1. Title — project overview
2. Who This Project Is For
3. Business Value for Companies
4. The Challenge
5. Research Gap
6. Project Vision
7. System Architecture
8. Core Capabilities
9. Methodology
10. Prototype Scope (Current vs Planned)
11. Interactive Prototype Dashboard *(image)*
12. Executive Resilience Overview *(image)*
13. Supplier Disruption Risk *(image)*
14. Simulation & Mitigation Insights *(image)*
15. Supply Network Topology *(image)*
16. Semiconductor Case Study
17. Energy Infrastructure Case Study
18. Policy & Strategic Impact
19. Future Research Directions
20. How to Run the Prototype
21. Collaboration & Next Steps
22. Thank You

## Regenerate the presentation

After updating dashboard images or project content:

```bash
pip install -r requirements.txt
python scripts/generate_presentation.py
```

Or generate images and the deck together:

```bash
python scripts/generate_all_assets.py
```

## Presentation tips

- **For companies:** emphasize slides 2–3, 11–15, and 20 (business value, dashboards, how to run).
- **For researchers:** emphasize slides 5–10 and 18–19 (methodology, architecture, future work).
- **For funders:** lead with slides 4–6 and 21 (problem, vision, collaboration).
- Run the live Streamlit dashboard during Q&A: `streamlit run dashboard/app.py`
