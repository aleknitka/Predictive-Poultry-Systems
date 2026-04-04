# Phase 04: Cycle Integration - Research

**Researched:** 2025-03-24
**Domain:** Discrete Event Simulation (DES) / Operational Integration
**Confidence:** HIGH

## Summary

This phase focuses on the end-to-end integration of the "avian fulfillment" lifecycle. Using `salabim` as the core engine, we will connect behavioral agents (Customers and Staff) with physical and operational resources (Machines and Facilities). The simulation cycle follows a "Process Chaining" pattern where entities move through stages: Arrival -> Ordering -> Cooking -> Fulfillment -> Consumption.

**Primary recommendation:** Use `salabim.Component` for the lifecycle of a protein unit (avian asset) and `salabim.Store` to decouple kitchen production from customer demand (holding cabinets).

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SIM-LOOP-01 | Create integrated simulation loop in `main.py` connecting agents and objects. | Verified `salabim.Environment` and `Component` interaction patterns. |
| SIM-LOOP-02 | Enable process-based modeling for avian asset fulfillment cycles. | Mapped lifecycle to `request()`, `hold()`, and `to_store()` operations. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| salabim | 26.0.4 | DES Engine | Built-in animation, statistics, and process-based modeling. |
| pydantic | 2.12.5 | Data Models | Strict typing and validation for entities and processes. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| Faker | 40.12.0 | Data Generation | Creating synthetic customer profiles and arrival times. |

**Installation:**
```bash
uv add salabim pydantic faker
```

## Architecture Patterns

### Recommended Project Structure
The integration will leverage existing modules:
- `src/predictive_poultry_systems/agents/customers/`: Decision logic.
- `src/predictive_poultry_systems/agents/staff/`: Labor resources.
- `src/predictive_poultry_systems/objects/machines/`: Transformation resources.
- `src/predictive_poultry_systems/objects/processes/`: Logic definitions.

### Pattern 1: Process Chaining (The "Relay" Pattern)
The `ProteinUnit` or `Customer` drives its own lifecycle.
```python
# Source: salabim.org
class Customer(sim.Component):
    def process(self):
        yield self.request(ordering_kiosk)
        yield self.hold(order_time)
        self.release()
        # Wait for order...
```

### Pattern 2: Store-Mediated Buffering (Holding Cabinet)
Decouples "Cooking" from "Ordering" to simulate fast-food batch production.
```python
holding_cabinet = sim.Store("Cabinet", capacity=20)
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Time-series statistics | Custom lists/counters | `sim.Monitor` | Automated time-weighted averages and histograms. |
| Queue priority | Custom sorting | `sim.Resource` | `salabim` handles priority and preemption out of the box. |
| Inter-arrival times | `random.uniform` | `sim.Exponential` | Better models real-world arrival patterns (Poisson process). |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.13.12 | — |
| salabim | Simulation engine | ✓ | 26.0.4 | — |
| pydantic | Data validation | ✓ | 2.12.5 | — |
| uv | Dependency management | ✓ | 0.11.1 | — |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | pyproject.toml |
| Quick run command | `uv run pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SIM-LOOP-01 | Full cycle completion | Smoke | `uv run pytest tests/test_main.py` | ✅ |
| SIM-LOOP-02 | Resource utilization | Integration | `uv run pytest tests/test_objects.py` | ✅ |

## Sources

### Primary (HIGH confidence)
- Official Salabim Documentation (salabim.org) - Process patterns, Resources, Stores.
- Project Source Code - `predictive_poultry_systems` objects and agents.

## Metadata
**Confidence breakdown:**
- Standard stack: HIGH - Verified in environment.
- Architecture: HIGH - Standard salabim patterns.
- Pitfalls: MEDIUM - Based on common DES challenges.

**Research date:** 2025-03-24
**Valid until:** 2025-04-23
