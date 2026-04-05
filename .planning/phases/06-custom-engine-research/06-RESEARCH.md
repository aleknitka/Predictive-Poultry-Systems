# Phase 6: Custom Engine Research - Research

**Researched:** 2026-04-04
**Domain:** Custom Simulation Engine & Thermodynamic Modeling for Poultry Fulfillment
**Confidence:** MEDIUM/HIGH

## Summary

This phase investigates the technical requirements and architecture for transitioning from the general-purpose `salabim` engine to a domain-specific simulation engine tailored to "avian fulfillment" (poultry restaurant operations). The goal is to move beyond simple stochastic durations towards high-fidelity physics models for cooking (thermodynamic transformation) and highly optimized event management for logistics.

**Primary recommendation:** Build a hybrid simulation engine using a `heapq`-based discrete event loop for logistics, integrated with a vectorized 1D heat equation solver using `numpy` and `numba` for real-time thermodynamic state tracking of avian assets.

<user_constraints>
## User Constraints (from CONTEXT.md)

*No CONTEXT.md was found for Phase 06. Operating under general project instructions from GEMINI.md and ROADMAP.md.*

### Locked Decisions
- Core Technology: Python 3.13+
- Management: `uv` for dependencies.
- Modeling: `pydantic` for entities.
- Domain Language: Use "fulfillment node", "avian asset", "thermodynamic transformation", "crisp-state".

### the agent's Discretion
- Choice of simulation engine architecture (replace vs. augment `salabim`).
- Complexity of thermodynamic models (1D vs 2D/3D).
- Selection of supporting libraries for physics (e.g., `numpy`, `numba`).

### Deferred Ideas (OUT OF SCOPE)
- Social media impact on customer segments (SOC-01).
- External environmental factors like weather/traffic (EXT-01).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| STRAT-01 | Research and document requirements for a domain-specific custom simulation engine. | Identified `heapq` core, generator-based logic, and hybrid DES/continuous architecture. |
| STRAT-02 | Draft technical design for the custom engine's thermodynamic logic. | Proposed heat equation + Arrhenius kinetics model for protein denaturation. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `heapq` | Built-in | Event priority queue | $O(\log n)$ efficiency for event management. |
| `pydantic` | 2.12.5 | Data modeling | Type safety and validation for assets and state. |

### Supporting (Proposed)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `numpy` | >=2.0.0 | Vectorized math | Required for efficient thermal state updates across many assets. |
| `numba` | >=0.60.0 | JIT compilation | Accelerate the triple-nested loops of the heat equation solver. |
| `SimPy` | >=4.1.1 | Process logic | Use as a foundation for generator-based "salabim-like" linear process code. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `salabim` | `SimPy` | SimPy is more modular and lightweight, easier to integrate with custom physics solvers. |
| `numpy` | `torch` | PyTorch could handle tensor-based physics on GPU, but overkill for simple 1D heat equations. |
| Custom `heapq` | `Ciw` | `Ciw` is excellent for queueing but less flexible for deep physical property simulation. |

**Installation:**
```bash
uv add numpy numba simpy
```

## Architecture Patterns

### Recommended Project Structure
```
src/predictive_poultry_systems/
├── engine/
│   ├── core.py         # Priority queue, clock, and event loop
│   ├── physics.py      # Heat equation and denaturation solvers
│   └── processes.py    # Generator-based process wrappers (SimPy-style)
├── objects/
│   ├── assets/         # High-fidelity protein unit models
│   └── machines/       # Updated machines with thermodynamic interfaces
└── main.py             # Entry point using the custom engine
```

### Pattern 1: Hybrid DES/Continuous Step
**What:** The main engine manages discrete events (arrivals, orders), but active transformation processes (cooking) trigger a "micro-stepping" mode within the event loop.
**When to use:** When physical state changes (temperature) affect future discrete events (doneness alerts).
**Example:**
```python
# Pseudo-code for Thermodynamic Solver Integration
while engine.active_transformations:
    dt = engine.next_event_time - engine.now
    step_size = min(dt, PHYSICS_STABILITY_LIMIT)
    physics_solver.update(active_assets, step_size)
    engine.now += step_size
```

### Anti-Patterns to Avoid
- **Global Physics Lock:** Blocking the entire simulation loop to calculate one asset's temperature. Use vectorized updates for all assets simultaneously.
- **Floating Point Clock:** Relying on standard `float` for high-precision time can lead to drift; consider integer timestamps for "ticks" if high resolution is required over long durations.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Event Scheduling | Custom list sorting | `heapq` | Performance scaling for thousands of events. |
| ODE Solving | Manual loops | `scipy.integrate` | Numerical stability and verified algorithms for heat diffusion. |
| JIT Compilation | Custom C extensions | `numba` | Easier maintenance and Python-native integration. |

## Architecture Design: Avian Thermodynamic Model

### 1. Thermal Diffusion (Heat Equation)
The model represents an "avian asset" (e.g., chicken thigh) as a 1D or 2D grid.
- **Equation:** $\frac{\partial T}{\partial t} = \alpha \nabla^2 T$
- **Boundary Condition:** $h(T_{oil} - T_{surface}) = -k \frac{\partial T}{\partial n}$ (Convective heat transfer from high-temp lipid submersion).
- **Latent Heat:** Account for moisture evaporation at $100^\circ C$ which caps surface temperature until a "crisp-layer" (crust) forms.

### 2. Denaturation Kinetics (Arrhenius)
Protein transformation is modeled as a first-order kinetic reaction.
- **Formula:** $k(T) = A \exp(-E_a / RT)$
- **Stages:**
    - Myofibrillar (50–70°C): Asset firmness.
    - Collagen (60–80°C): Tenderness vs. toughness.
- **Crisp-State Indicator:** A composite score of core temperature, surface moisture content, and cumulative denaturation.

## Common Pitfalls

### Pitfall 1: Physics Instability
**What goes wrong:** The simulation "explodes" with infinite temperatures or NaNs.
**Why it happens:** The time step $\Delta t$ is too large relative to the spatial resolution $\Delta x$ (violating the CFL condition).
**How to avoid:** Implement an adaptive time-stepper that caps $\Delta t$ based on thermal diffusivity.

### Pitfall 2: Memory Bloat
**What goes wrong:** High-fidelity modeling of every single chicken wing consumes GBs of RAM.
**Why it happens:** Storing full 3D temperature maps for thousands of concurrent assets.
**How to avoid:** Use 1D radial or planar approximations for standard menu items.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.13.12 | — |
| uv | Package Mgmt | ✓ | 0.11.1 | — |
| salabim | Current Engine | ✓ | 26.0.4 | Replace with custom |
| numpy | Physics | ✗ | — | Add to dependencies |
| numba | Performance | ✗ | — | Add to dependencies |

**Missing dependencies with no fallback:**
- `numpy`, `numba` - Critical for the proposed high-fidelity physics model.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `pytest` |
| Config file | `pyproject.toml` |
| Quick run command | `uv run pytest tests/test_engine.py -x` |
| Full suite command | `uv run pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| STRAT-01 | Custom engine executes a sequence of events in $O(\log N)$ | Unit/Perf | `uv run pytest tests/test_engine.py::test_perf` | ❌ Wave 0 |
| STRAT-02 | Heat equation solver reaches steady state within expected bounds | Unit/Physics | `uv run pytest tests/test_physics.py::test_heat_eq` | ❌ Wave 0 |

### Wave 0 Gaps
- [ ] `tests/test_engine.py` — core event loop validation.
- [ ] `tests/test_physics.py` — thermodynamic model validation.
- [ ] `uv add numpy numba simpy` — install required physics stack.

## Sources

### Primary (HIGH confidence)
- `heapq` Official Docs - Event loop efficiency.
- Arrhenius Equation (Physical Chemistry) - Standard for protein denaturation modeling.
- Heat Equation (Fourier's Law) - Industry standard for thermal simulation.

### Secondary (MEDIUM confidence)
- "Deep-fat frying of chicken nuggets: heat and mass transfer, oil absorption and moisture loss" (Academic literature) - Verified parameters for $\alpha$ and $h$.
- `salabim` vs `SimPy` architectural comparisons - Ecosystem patterns.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Built on established Python math/simulation libraries.
- Architecture: MEDIUM - Hybrid DES/Physics integration is complex but well-defined.
- Pitfalls: HIGH - Common numerical stability issues in FEA/FDM are well-known.

**Research date:** 2026-04-04
**Valid until:** 2026-05-04
