# Phase 05: Throughput Optimization - Research

**Researched:** 2026-04-04
**Domain:** Discrete Event Simulation (DES) Metrics, QSR Performance Analysis, Thermodynamics of Frying.
**Confidence:** HIGH

## Summary

This phase focuses on defining, implementing, and reporting critical performance indicators (KPIs) for the "avian asset" (poultry) fulfillment lifecycle. Research confirms that `salabim` provides robust built-in monitoring tools (`sim.Monitor`, `sim.LevelMonitor`) that should be leveraged to track stochastic variables over time.

The primary optimization goal is to balance **throughput** (fulfilled orders per hour) with **quality** (adherence to "Crisp-state" thermodynamic optima) and **stakeholder friction** (customer satisfaction vs. staff morale). We will implement a centralized `FulfillmentManager` to aggregate these metrics and generate a simulation-end "Fulfillment Audit."

**Primary recommendation:** Use `salabim`'s built-in Monitors to track real-time agent state transitions and define "Crisp-state" as a Gaussian function of cook duration to reward adherence to thermodynamic optima.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| MET-01 | Track and report operational throughput and fiscal yield. | Defined throughput (TPH) and profit formulas based on labor/revenue modeling. |
| MET-02 | Measure and mitigate "stakeholder friction" (customer satisfaction levels). | Identified exponentially decaying satisfaction curves based on wait time (SoS). |
| MET-03 | Analyze "crisp-state" metrics for thermodynamic fulfillment optimization. | Defined thermodynamic "Crisp-state" based on energy/mass transfer research. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| salabim | 26.0.4.post0 | Discrete Event Simulation | High-performance, built-in monitoring and animation. |
| pydantic | 2.12.5 | Data Modeling | Strict typing for agent state and metric reporting. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| loguru | [latest] | Event Logging | Recommended by Phase 7 for persistent event tracking. |
| faker | 40.12.0 | Data Generation | Creating varied agent profiles for stochastic stress tests. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sim.Monitor | pandas.DataFrame | Pandas is better for post-hoc analysis but `sim.Monitor` is faster for real-time simulation updates and animation. |

**Installation:**
```bash
uv add salabim pydantic faker
```

## Architecture Patterns

### Recommended Project Structure
```
src/predictive_poultry_systems/
├── agents/
│   ├── simulation.py        # Centralized FulfillmentManager & Environment helpers
│   └── behavior/
│       └── metrics.py       # Formulae for Satisfaction, Morale, and Crisp-state
└── analytics/
    └── reporter.py          # Aggregates Monitors into human-readable reports
```

### Pattern 1: Centralized Fulfillment Monitoring
The `FulfillmentManager` (currently a minimal class in `main.py`) should be promoted to a core orchestrator that holds all global monitors.

```python
# Source: https://www.salabim.org/manual/Monitor.html
class FulfillmentManager(sim.Component):
    def setup(self):
        # Level monitors for variables over time
        self.satisfaction_monitor = sim.Monitor("Average Satisfaction", level=True)
        self.morale_monitor = sim.Monitor("Staff Morale", level=True)

        # Non-level monitors for discrete events
        self.sos_monitor = sim.Monitor("Speed of Service")
        self.crispness_monitor = sim.Monitor("Crisp Compliance")

        self.revenue_cumulative = 0
```

### Anti-Patterns to Avoid
- **Manual List Appending:** Don't use `list.append(env.now())` for tracking; use `sim.Monitor.tally()` to benefit from built-in statistical methods (`mean()`, `std()`, `print_histogram()`).
- **Global Variable Metrics:** Avoid keeping counters in global scope; attach them to the `sim.Environment` or `FulfillmentManager` for simulation isolation.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Time-weighted averaging | Custom accumulation logic | `sim.Monitor(level=True)` | Handles non-uniform time steps in DES automatically. |
| Resource tracking | Custom occupancy counters | `Resource.occupancy.mean()` | Salabim resources track arrival, usage, and wait-time statistics out-of-the-box. |
| Histogram generation | Manual binning logic | `Monitor.print_histogram()` | Built-in, efficient, and formatted for console display. |

## Common Pitfalls

### Pitfall 1: Warm-up Bias
**What goes wrong:** Initial simulation state (empty queues) skews averages downward.
**Why it happens:** "Empty and Idle" state is not representative of steady-state fulfillment.
**How to avoid:** Use `env.reset_monitors()` after a defined warm-up period or ignore the first $N$ arrivals in your tallies.

### Pitfall 2: High Sampling Frequency for Level Monitors
**What goes wrong:** Performance degradation if tallying on every micro-step.
**Why it happens:** Excessive state updates for variables that change slowly (like morale).
**How to avoid:** Tally only on state *changes* or at fixed operational intervals (e.g., every 5 minutes of sim time).

## Code Examples

### Thermodynamic "Crisp-state" Metric
```python
import math

def calculate_crisp_state(cook_time: float) -> float:
    """
    Quantifies the thermodynamic optimum for protein transformation.
    Center: 240s (4 min), StdDev: 20s.
    """
    mu = 240
    sigma = 20
    # Gaussian scoring (0.0 to 1.0)
    score = math.exp(-((cook_time - mu)**2) / (2 * sigma**2))
    return score
```

### Customer Satisfaction (Stakeholder Friction)
```python
def update_satisfaction(wait_time: float, base_satisfaction: float) -> float:
    """
    Decay satisfaction based on Speed of Service (SoS).
    k=0.005 implies satisfaction drops by half after ~138 seconds of extra waiting.
    """
    k = 0.005
    expected_sos = 180 # 3 minutes
    penalty = math.exp(-k * max(0, wait_time - expected_sos))
    return base_satisfaction * penalty
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Fixed Cook Times | Stochastic Variance | DES standard | Higher fidelity modeling of "burnt" or "raw" assets. |
| Static Efficiency | Dynamic Fatigue/Morale | Agent-based sim | Captures the cost of labor churn and "fulfillment burnout." |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.13.12 | — |
| uv | Package Mgmt | ✓ | 0.11.1 | pip |
| salabim | Simulation | ✓ | 26.0.4.post0 | — |
| pydantic | Data Validation | ✓ | 2.12.5 | — |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | None |
| Quick run command | `uv run pytest -x` |
| Full suite command | `uv run pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MET-01 | Throughput & Fiscal Yield reporting | integration | `uv run pytest tests/test_metrics.py` | ❌ Wave 0 |
| MET-02 | Stakeholder Friction (Satisfaction) tracking | unit | `uv run pytest tests/test_agent_metrics.py` | ❌ Wave 0 |
| MET-03 | Crisp-state compliance calculation | unit | `uv run pytest tests/test_thermodynamics.py` | ❌ Wave 0 |

### Wave 0 Gaps
- [ ] `tests/test_metrics.py` — Integration test for `FulfillmentManager` report output.
- [ ] `tests/test_thermodynamics.py` — Unit tests for the `calculate_crisp_state` formula.

## Sources

### Primary (HIGH confidence)
- [Salabim Monitor Documentation](https://www.salabim.org/manual/Monitor.html) - Verified monitor types and tallying logic.
- [Salabim Component Reference](https://www.salabim.org/manual/Component.html) - Verified process and resource interaction.

### Secondary (MEDIUM confidence)
- "The Science of Deep Frying" (Various QSR sources) - Derived thermodynamic optimum cook windows for poultry assets.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Core libraries already in use and documented.
- Architecture: HIGH - Salabim patterns are well-established for this domain.
- Pitfalls: MEDIUM - Warm-up bias is common but requires careful tuning.

**Research date:** 2026-04-04
**Valid until:** 2026-05-04
