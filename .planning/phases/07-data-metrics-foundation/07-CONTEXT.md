# Phase 7: Data & Metrics Foundation - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement extensive logging for events and actions, feeding simulation metrics into a SQLite database for downstream analysis. This foundation enables reporting on throughput, satisfaction, and operational efficiency in later phases.

</domain>

<decisions>
## Implementation Decisions

### Logging Infrastructure
- **D-01: loguru.** Use `loguru` for all simulation logging, providing modern, easy-to-use, and visually descriptive output.
- **D-02: salabim monitors.** Leverage `salabim`'s built-in monitor components for efficient data collection from simulation actors and resources.

### Database Architecture
- **D-03: direct sqlite3.** Use the standard `sqlite3` library for database interaction to minimize external dependencies and ensure simplicity.
- **D-04: relational/normalized schema.** Implement a structured relational schema in SQLite with dedicated tables for different entity types (e.g., `customers`, `staff`, `machines`, `events`).
- **D-05: real-time synchronous writes.** Metrics will be written to the database synchronously as events occur to ensure data integrity and simple implementation.

### Claude's Discretion
- Exact table schemas and column definitions.
- Formatting of log messages (colors, level mapping).
- File rotation and retention policies for log files.

</decisions>

<specifics>
## Specific Ideas

- "Feed metrics into a database sqlite for later analysis of simulation."
- Ensure logs include the `salabim` simulation time (env.now()) for temporal context.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Core Requirements
- `.planning/REQUIREMENTS.md` — MET-* requirements for metrics and optimization.
- `.planning/ROADMAP.md` — Phase 7 goal and success criteria.

### External Libraries
- [loguru documentation](https://github.com/Delgan/loguru) — Logging library usage.
- [sqlite3 standard library docs](https://docs.python.org/3/library/sqlite3.html) — Database interaction.
- [salabim monitor documentation](https://www.salabim.org/manual/Monitor.html) — Built-in simulation data collection.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The simulation environment (`env`) in `main.py` is the central hub for monitors.

### Integration Points
- `src/predictive_poultry_systems/objects/` — Models here will need monitor integration.
- `src/predictive_poultry_systems/agents/` — Customer and Staff agents will need to be logged/monitored.
- `main.py` — The primary simulation loop where DB connections should be initialized and closed.

</code_context>

<deferred>
## Deferred Ideas

- Advanced visualization (dashboards) of the collected metrics (Phase 5).
- Complex fiscal yield reporting (Phase 5).

</deferred>

---

*Phase: 07-data-metrics-foundation*
*Context gathered: 2026-04-04*
