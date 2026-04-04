# Predictive Poultry Systems

**Predictive Poultry Systems** is a high-fidelity Digital Twin simulation designed to optimize the end-to-end lifecycle of avian assets within a localized fulfillment node. Forget "cooking"—as the Node Operations Director, you must leverage advanced logistics to manage the thermodynamic transformation of protein units and mitigate stakeholder friction through real-time throughput analysis. From cryogenic ingredient retention to high-temp lipid submersion, every operational cycle is a data-driven pursuit of the optimum crisp-state and maximized fiscal yield.

## Project Overview

This simulation models the complex interactions between physical infrastructure, machinery, staff labor, and customer behavior within a poultry-focused fulfillment environment.

### Core Technology Stack

- **Python 3.13+**: Leveraging the latest language features and performance.
- **[salabim](https://www.salabim.org/)**: Discrete-event simulation engine with built-in animation and statistics.
- **[pydantic](https://docs.pydantic.dev/)**: Strict data modeling and validation for all simulation entities.
- **[uv](https://github.com/astral-sh/uv)**: Blazing fast Python package and project manager.
- **[faker](https://faker.readthedocs.io/)**: Generating synthetic customer and operational data.
- **[ruff](https://github.com/astral-sh/ruff)**: Extremely fast Python linter and code formatter.
- **[prek](https://github.com/astral-sh/prek)**: Fast, Rust-based replacement for pre-commit hooks.

## Simulation Domain Architecture

The simulation is built around several high-fidelity components located in `src/predictive_poultry_systems/`:

### 🏢 Objects & Physical Assets
- **Facilities (`objects/facilities/`)**: Models the spatial layout and capacity constraints of the fulfillment node.
- **Machines (`objects/machines/`)**: High-fidelity equipment models (fryers, refrigeration, kiosks) including resource consumption (power, water, gas), fault rates, and material transformation logic.
- **Menu Items (`objects/menu/`)**: Detailed definitions of avian assets and their constituent ingredients.
- **Processes (`objects/processes/`)**: Procedural logic for thermodynamic transformation and final assembly.

### 👥 Agents & Actors
- **Staff (`agents/staff/`)**: Labor modeling including fatigue, skill levels, and shift patterns.
- **Customers (`agents/customers/`)**: Behavioral models covering segmentation, loyalty, and RFM (Recency, Frequency, Monetary) analysis.

## Getting Started

### Prerequisites

Ensure you have [uv](https://github.com/astral-sh/uv) installed on your system.

### Installation

Clone the repository and sync the environment:

```bash
uv sync
```

### Running the Simulation

Execute the main simulation entry point:

```bash
uv run main.py
```

## Development & Quality Standards

We maintain high engineering standards to ensure simulation fidelity and codebase maintainability.

### Linting & Formatting

We use `ruff` for all linting and formatting tasks:

```bash
uv run ruff check .
uv run ruff format .
```

### Pre-commit Hooks

Ensure all commits pass quality checks using `prek`:

```bash
uv run prek run --all-files
```

### Testing

Unit tests are managed via `pytest` and should be added to the `tests/` directory:

```bash
uv run pytest
```

---
*Note: This project is in active development as part of a research effort to explore domain-specific simulation engines for avian fulfillment optimization.*
