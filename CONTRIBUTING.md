# Contributing

Thank you for your interest in **Critical Supply Chain Resilience AI**.

## Getting started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```

3. Run the Week 1 validation script:

   ```bash
   python examples/week1_network_overview.py
   ```

## Development workflow

- Keep changes focused on a single capability (forecasting, simulation, optimization, etc.).
- Place reusable logic under `src/` and runnable demos under `examples/`.
- Add or update notebooks in `notebooks/` for case-study narratives.
- Document design decisions in `docs/`.

## Code style

- Use Python 3.10+ type hints where practical.
- Prefer small, testable functions over large scripts.
- Match existing naming and module layout.

## Pull requests

1. Describe the problem and your approach.
2. Note how you tested the change (command, notebook, or pytest).
3. Link related issues when applicable.

## Reporting issues

Include:

- Steps to reproduce
- Expected vs. actual behavior
- Python version and OS

## Contact

**David Ishimwe Ruberamitwe**
