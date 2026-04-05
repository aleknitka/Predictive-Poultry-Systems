# Roadmap: Predictive Poultry Systems

## Phases
- [x] **Phase 1: Foundation & Baseline** - Integrated simulation environment and core engine.
- [x] **Phase 2: Operational Assets** - Models for facilities, equipment, and menus.
- [x] **Phase 3: Agentic Workforce & Logistics** - Customer and staff behavior logic.
- [x] **Phase 4: Cycle Integration** - End-to-end fulfillment loop execution.
- [x] **Phase 5: Throughput Optimization** - Metrics, analysis, and fulfillment tuning.
- [x] **Phase 6: Custom Engine Research** - Strategy for domain-specific simulation logic.
- [ ] **Phase 7: Data & Metrics Foundation** - Logging, event tracking, and SQLite integration.

## Phase Details

### Phase 1: Foundation & Baseline
**Goal**: Establish a stable environment for discrete event simulation with `salabim`.
**Depends on**: Nothing
**Requirements**: [SETUP-01, SETUP-02, SETUP-03, SIM-CORE-01]
**Success Criteria** (what must be TRUE):
  1. `uv sync` correctly installs all dependencies including `salabim`, `greenlet`, and `Pillow`.
  2. `uv run main.py` executes a minimal `salabim` simulation without errors.
  3. `ruff` and `prek` hooks are actively enforcing project standards.
**Plans**:
- [x] 01-PLAN.md — Foundation & Simulation Baseline
**UI hint**: yes

### Phase 2: Operational Assets
**Goal**: Define the physical and procedural constraints of the fulfillment node.
**Depends on**: Phase 1
**Requirements**: [OBJ-FAC-01, OBJ-MAC-01, OBJ-MAC-02, OBJ-MENU-01]
**Success Criteria** (what must be TRUE):
  1. Facilities have capacity-constrained layouts.
  2. Machines accurately model resource consumption and fault probabilities.
**Plans**:
- [x] 02-PLAN.md — Operational Assets

### Phase 3: Agentic Workforce & Logistics
**Goal**: Implement behavior models for customers and staff.
**Depends on**: Phase 2
**Requirements**: [AGT-CUST-01, AGT-CUST-02, AGT-STAF-01]
**Success Criteria** (what must be TRUE):
  1. Customers exhibit loyalty/segment-based arrival and queueing patterns.
  2. Staff agents successfully execute fulfillment tasks with efficiency metrics.
**Plans**:
- [x] 03-01-PLAN.md — Core Behavior Framework (BT + pydantic-ai)
- [x] 03-02-PLAN.md — Agent Behavior Definitions (Customer + Staff)
- [x] 03-03-PLAN.md — Simulation Loop Integration

### Phase 4: Cycle Integration
**Goal**: Execute the full simulation cycle end-to-end.
**Depends on**: Phase 3
**Requirements**: [SIM-LOOP-01, SIM-LOOP-02]
**Success Criteria** (what must be TRUE):
  1. `main.py` runs a full cycle: customer arrival -> ordering -> cooking -> delivery.
  2. The simulation accurately tracks events across the `salabim` timeline.
**Plans**:
- [x] 04-01-PLAN.md — Agent Behavioral Lifecycle Logic
- [x] 04-02-PLAN.md — End-to-End Simulation Loop Integration

### Phase 5: Throughput Optimization
**Goal**: Analyze performance and optimize the "avian asset" lifecycle.
**Depends on**: Phase 4
**Requirements**: [MET-01, MET-02, MET-03]
**Success Criteria** (what must be TRUE):
  1. The system outputs throughput and fiscal yield reports.
  2. Customer satisfaction (CSI) and Staff Morale (SMI) are quantified and tracked.
  3. "Crisp-state" metrics identify the thermodynamic optimum for cooking.
  4. Salabim monitors are integrated into FulfillmentManager.
**Plans**:
- [x] 05-01-PLAN.md — Metrics Foundations
- [x] 05-02-PLAN.md — Fulfillment Manager & Monitoring
- [x] 05-03-PLAN.md — Analytics Reporting & System Validation
**UI hint**: yes

### Phase 6: Custom Engine Research
**Goal**: Prepare for the transition to an economic and management-focused simulation engine.
**Depends on**: Phase 5
**Requirements**: [STRAT-01, STRAT-02]
**Success Criteria** (what must be TRUE):
  1. A detailed requirements document for the custom engine is finalized.
  2. Technical design for the economic and management logic is approved.
**Plans**:
- [x] 06-01-PLAN.md — Custom Engine Requirements Specification
- [x] 06-02-PLAN.md — Economic & Management Design Specification

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Baseline | 1/1 | Completed | 2026-04-04 |
| 2. Operational Assets | 1/1 | Completed | 2026-04-04 |
| 3. Agentic Workforce & Logistics | 3/3 | Completed | 2026-04-04 |
| 4. Cycle Integration | 2/2 | Completed | 2026-04-04 |
| 5. Throughput Optimization | 3/3 | Completed | 2026-04-04 |
| 6. Custom Engine Research | 2/2 | Completed | 2026-04-04 |
| 7. Data & Metrics Foundation | 0/2 | Not started | - |

### Phase 7: Data & Metrics Foundation
**Goal:** Implement extensive logging for events, actions, and feed metrics into SQLite.
**Requirements**: [MET-INF-01, MET-INF-02, MET-INF-03, MET-INF-04, MET-01, MET-02, MET-03]
**Depends on:** Phase 6
**Success Criteria** (what must be TRUE):
  1. Simulation events are logged using `loguru` with accurate `env.now()` time stamps.
  2. A relational SQLite schema persists simulation runs, logs, and resource metrics.
  3. Real-time metrics are synced from salabim monitors to the database during execution.
**Plans**:
- [ ] 07-01-PLAN.md — Foundation - Logging & Database
- [ ] 07-02-PLAN.md — Integration - Persistence & Monitors
