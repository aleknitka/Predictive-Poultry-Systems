# Phase 1: Foundation & Baseline - Research

**Researched:** 2025-03-24
**Domain:** Discrete Event Simulation (DES) with Salabim, Project Setup
**Confidence:** HIGH

## Summary
Phase 1 focuses on establishing the core simulation environment using `salabim` and enforcing project standards with `uv`, `ruff`, and `prek`. The research confirms that while `salabim` is installed, its modern "yieldless" mode requires the `greenlet` package, which is currently missing from `pyproject.toml`. Animation support will also require `Pillow`.

**Primary recommendation:** Add `greenlet` and `Pillow` to dependencies, and initialize the `salabim.Environment` in `main.py` using the process-based modeling pattern.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| salabim | 26.0.4 | DES Engine | Powerful, built-in animation and statistics. |
| greenlet| 3.1.1+  | Yieldless support | Required for salabim's non-generator process style. |
| pydantic| 2.10+   | Data Modeling | Strict typing and validation for simulation entities. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| Pillow  | 10.0.0+ | Animation | Required for 2D animation in salabim. |
| faker   | 40.12.0 | Data Gen | Creating synthetic customer profiles. |
| prek    | 0.3.8   | Hooks | Faster Rust-based pre-commit replacement. |

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SETUP-01 | Python 3.13 / uv | Verified `uv run python --version` returns 3.13.12. |
| SETUP-02 | Code quality (ruff/prek) | `prek` confirmed compatible with `.pre-commit-config.yaml`. |
| SETUP-03 | Salabim integration | Tested `salabim.Environment()` and basic components. |
| SIM-CORE-01 | Sim Environment | Confirmed `salabim` yieldless mode requires `greenlet`. |

## Architecture Patterns

### Recommended Project Structure
The project already follows a solid structure:
- `src/predictive_poultry_systems/agents/`: For `salabim.Component` subclasses (Customers, Staff).
- `src/predictive_poultry_systems/objects/`: For `pydantic.BaseModel` entities (Machines, Menu).

### Pattern: Component-Process
Salabim uses a process-based pattern where each actor is a `Component` with a `process()` method.
```python
import salabim as sim
class Customer(sim.Component):
    def process(self):
        # Simulation logic here
        self.hold(5)
```

## Common Pitfalls
- **Missing Greenlet:** Salabim defaults to yieldless mode which fails with `ModuleNotFoundError: No module named 'greenlet'`.
- **Tkinter on Linux:** Animation requires `tkinter`. Research shows it is available in the environment but must be verified on deployment targets.
- **Prek Installation:** `prek` is a dependency but `prek install` must be run manually to activate git hooks.

## Code Examples

### Basic Simulation Baseline
```python
import salabim as sim

class SimulationManager(sim.Component):
    def process(self):
        print(f"Simulation started at {self.env.now()}")
        self.hold(100)
        print(f"Simulation finished at {self.env.now()}")

def run_sim():
    env = sim.Environment(trace=True)
    SimulationManager()
    env.run(till=100)
```

## Environment Availability
- **Python 3.13:** Available via `uv`.
- **uv:** Available (v0.11.1).
- **prek:** Available via `uv run prek`.
- **tkinter:** Available in current environment.

## Validation Architecture
- **Framework:** pytest (already in `pyproject.toml`).
- **Command:** `uv run pytest`.
- **Gap:** No `tests/` directory exists. Wave 0 should create `tests/test_env.py` to verify `salabim` and `pydantic` integration.
