# Predictive Poultry Systems - Context & Instructions

This project is a high-fidelity Digital Twin simulation designed to optimize the end-to-end lifecycle of a localized fulfillment node (fast-food poultry restaurant). It models the thermodynamic transformation of protein units (cooking) and logistics to mitigate stakeholder friction (customer satisfaction).

## Project Overview

- **Core Technology:** Python 3.13+
- **Primary Libraries:**
    - `salabim`: Discrete event simulation engine with built-in animation and statistics.
    - `pydantic`: Data modeling and validation for entities.
    - `faker`: Generation of synthetic customer and operational data.
    - `ruff`: Linting and formatting.
    - `prek`: Fast, Rust-based replacement for `pre-commit` hooks.
- **Management:** This project uses `uv` for dependency and environment management.

## Strategic Direction: Custom Simulation Engine
While `salabim` is the current engine, a core goal is to explore and potentially implement a custom, domain-specific simulation engine tailored to the unique thermodynamic and logic requirements of avian fulfillment.

## Architecture & Structure

The codebase is organized within `src/predictive_poultry_systems/`:

- **`agents/`**: Contains simulation actors.
    - `customers/`: Customer behavior models, including loyalty (`loyalty.py`), segmentation (`segments.py`), and RFM analysis (`rfm.py`).
    - `staff/`: Staffing and labor logic.
- **`objects/`**: Physical and operational entities.
    - `facilities/`: Store layout and infrastructure.
    - `machines/`: Equipment models (cooking, refrigeration, ordering kiosks) with resource consumption and fault rates.
    - `menu/`: Menu items and ingredient definitions.
- **`main.py`**: The entry point for the simulation execution.

## Building and Running

Since this project uses `uv`, all commands should be prefixed accordingly:

- **Environment Setup:** `uv sync`
- **Run Simulation:** `uv run main.py`
- **Linting & Formatting:** `uv run ruff check .` and `uv run ruff format .`
- **Pre-commit Hooks:** `uv run prek run --all-files`
- **TODO: Testing:** Unit tests should be added to `tests/` using `pytest`. Run tests with `uv run pytest`.

## Development Conventions

1.  **Strict Typing:** Use Python type hints and `pydantic` models for all entity definitions to ensure data integrity during simulation steps.
2.  **Simulation Cycles:** Adhere to the `salabim` process-based modeling pattern while researching requirements for a custom engine.
3.  **Hooks:** Use `prek` to ensure all commits meet quality standards (linting, formatting).
4.  **Domain Language:** Use the established "fulfillment node" and "avian asset" terminology found in the README when describing operational optimizations.
5.  **Linting:** Maintain compliance with the `ruff` configuration defined in `pyproject.toml`.
