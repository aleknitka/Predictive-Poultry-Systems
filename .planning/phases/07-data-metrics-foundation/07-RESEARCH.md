# Phase 7: Data & Metrics Foundation - Research

**Researched:** 2026-04-04
**Domain:** Logging, Metrics Persistence, SQLite, salabim
**Confidence:** HIGH

## Summary

This phase establishes the long-term data foundation for Predictive Poultry Systems by implementing high-fidelity logging and relational metrics persistence. We will transition from simple console reports to a persistent SQLite-backed analytics engine.

**Primary recommendation:** Use `loguru` patched with `env.now()` for simulation-aware logging and `sqlite3` in WAL mode for performant, real-time synchronous writes to a normalized relational schema.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01: loguru.** Use `loguru` for all simulation logging, providing modern, easy-to-use, and visually descriptive output.
- **D-02: salabim monitors.** Leverage `salabim`'s built-in monitor components for efficient data collection from simulation actors and resources.
- **D-03: direct sqlite3.** Use the standard `sqlite3` library for database interaction to minimize external dependencies and ensure simplicity.
- **D-04: relational/normalized schema.** Implement a structured relational schema in SQLite with dedicated tables for different entity types (e.g., `customers`, `staff`, `machines`, `events`).
- **D-05: real-time synchronous writes.** Metrics will be written to the database synchronously as events occur to ensure data integrity and simple implementation.

### the agent's Discretion
- Exact table schemas and column definitions.
- Formatting of log messages (colors, level mapping).
- File rotation and retention policies for log files.

### Deferred Ideas (OUT OF SCOPE)
- Advanced visualization (dashboards) of the collected metrics (Phase 5).
- Complex fiscal yield reporting (Phase 5).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| MET-INF-01 | Implement `loguru` with simulation time integration. | `logger.patch()` pattern discovered for injecting `env.now()`. |
| MET-INF-02 | Design and implement a relational SQLite schema. | Normalized schema design with `runs`, `logs`, `agent_states`, and `resource_metrics` tables. |
| MET-INF-03 | Develop a `DatabaseManager` for real-time synchronous writes. | `PRAGMA journal_mode=WAL` and `synchronous=NORMAL` identified as performance enablers. |
| MET-INF-04 | Create a `salabim` component for periodic monitor data sinking. | Pattern for periodic sampling of `Resource` and `Monitor` objects into SQLite. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| loguru | ^0.7.2 | Structured Logging | Modern, cleaner than `logging`, easy formatting and patching. |
| sqlite3 | (Stdlib) | Metrics Persistence | Zero-config, single-file, relational, standard across environments. |
| salabim | 26.0.4 | Simulation Engine | Current project engine, provides powerful `Monitor` and `Resource` statistics. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pydantic | 2.12.5 | Data Validation | Validating metric payloads before database insertion. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| loguru | logging | `logging` is more complex to configure for simulation-time injection. |
| sqlite3 | postgres | PostgreSQL requires external setup; SQLite is self-contained. |
| synchronous writes | async/batch | Async writes add complexity and risk of data loss if the simulation crashes. |

**Installation:**
```bash
uv add loguru
```

**Version verification:**
Verified `salabim` 26.0.4 and Python 3.13.12. `loguru` needs to be added to `pyproject.toml`.

## Architecture Patterns

### Recommended Project Structure
```
src/predictive_poultry_systems/
├── analytics/
│   ├── database.py      # DatabaseManager and schema definitions
│   ├── logging.py       # Loguru configuration and simulation patching
│   └── sinks.py         # Salabim components for data persistence
└── ...
```

### Pattern 1: Simulation-Aware Logging (Patching)
**What:** Injecting the simulation clock (`env.now()`) into every log record.
**When to use:** All simulation events.
**Example:**
```python
# Source: https://github.com/Delgan/loguru
from loguru import logger
import salabim as sim

def setup_simulation_logger(env: sim.Environment):
    logger.remove()
    # Inject sim_time into extra record
    logger.patch(lambda r: r["extra"].update({"sim_time": env.now()}))
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | [{extra[sim_time]:>8.2f}] <level>{level: <8}</level> | {message}"
    )
```

### Pattern 2: Database Manager (WAL Mode)
**What:** A singleton or shared manager that handles the SQLite connection with performance-optimized PRAGMAs.
**When to use:** Initializing simulation metrics storage.
**Example:**
```python
import sqlite3

class DatabaseManager:
    def __init__(self, db_path="metrics.sqlite"):
        self.conn = sqlite3.connect(db_path)
        # Performance optimization for real-time writes
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA synchronous = NORMAL;")
        self._init_schema()
```

### Anti-Patterns to Avoid
- **Implicit Commits:** Letting SQLite handle autocommits for every single insert (extremely slow).
- **String Formatting SQL:** Using `f-strings` for SQL queries (SQL injection risk and slower than parameterized queries).
- **Global Env Access:** Hardcoding `sim.default_env` in logging; better to pass the specific environment.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Time Injection | Custom log wrappers | `logger.patch()` | Built-in, efficient, thread-safe. |
| Data Collection | Custom counters | `salabim.Monitor` | Built-in statistics, histograms, and time-weighted analysis. |
| Schema Migration | Custom SQL scripts | (Keep simple for now) | For this phase, manual schema initialization is fine, but avoid complex migration logic yet. |

## Common Pitfalls

### Pitfall 1: Database Locking
**What goes wrong:** "database is locked" errors when multiple processes or threads try to write.
**Why it happens:** SQLite's default journal mode (DELETE) locks the whole file during writes.
**How to avoid:** Use `PRAGMA journal_mode = WAL;`.
**Warning signs:** Random `OperationalError` during high-frequency events.

### Pitfall 2: Simulation Slowdown
**What goes wrong:** Simulation time slows down significantly when logging is enabled.
**Why it happens:** Synchronous disk I/O on every event.
**How to avoid:** Use `PRAGMA synchronous = NORMAL;` and minimize disk flushes.

### Pitfall 3: Run Ambiguity
**What goes wrong:** Hard to tell which metrics belong to which simulation run.
**Why it happens:** Storing everything in flat tables without a `run_id`.
**How to avoid:** Create a `runs` metadata table and foreign key every entry to a `run_id`.

## Code Examples

### Relational Schema (DDL)
```sql
-- Source: Design Discretion
CREATE TABLE runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    seed INTEGER,
    config_json TEXT
);

CREATE TABLE simulation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    sim_time REAL,
    level TEXT,
    message TEXT,
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE resource_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    sim_time REAL,
    resource_name TEXT,
    available INTEGER,
    claimed INTEGER,
    queue_len INTEGER,
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| standard `logging` | `loguru` | Recent | Much simpler API, built-in color, easier contextual logs. |
| CSV export | SQLite (WAL) | - | Enables complex SQL queries and real-time dashboarding. |
| Manual Statistics | Salabim Monitors | - | Automated time-weighted means and histograms. |

## Open Questions

1. **Transaction Frequency:**
   - What we know: Synchronous writes are requested.
   - What's unclear: Should we commit after every action, or at the end of every simulation step?
   - Recommendation: Use a context manager that commits on successful agent action completion.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.13.12 | — |
| sqlite3 | Data Layer | ✓ | 3.45.3 | — |
| salabim | Simulation | ✓ | 26.0.4 | — |
| loguru | Logging | ✗ | — | Add via `uv add loguru` |

**Missing dependencies with no fallback:**
- `loguru`: Required for Phase 7 implementation as per D-01.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | pyproject.toml |
| Quick run command | `uv run pytest tests/test_data_metrics.py` |
| Full suite command | `uv run pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MET-INF-01 | Logs contain sim_time | integration | `uv run pytest tests/test_logging.py` | ❌ Wave 0 |
| MET-INF-02 | SQLite file created | unit | `uv run pytest tests/test_db.py` | ❌ Wave 0 |
| MET-INF-03 | Synchronous writes | performance | `uv run pytest tests/test_db_perf.py` | ❌ Wave 0 |

### Wave 0 Gaps
- [ ] `tests/test_data_metrics.py` — Covers DB initialization and log patching.
- [ ] `src/predictive_poultry_systems/analytics/database.py` — Schema and manager.
- [ ] `src/predictive_poultry_systems/analytics/logging.py` — Loguru setup.

## Sources

### Primary (HIGH confidence)
- [sqlite3 standard library docs](https://docs.python.org/3/library/sqlite3.html) - PRAGMA and WAL mode details.
- [loguru documentation](https://github.com/Delgan/loguru) - Patching and formatting.
- [salabim monitor documentation](https://www.salabim.org/manual/Monitor.html) - Monitor attributes.

### Secondary (MEDIUM confidence)
- SQLite Performance Tuning (WebSearch) - Confirmed WAL + NORMAL impact.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Libraries are standard and well-documented.
- Architecture: HIGH - Patching and Manager patterns are robust.
- Pitfalls: HIGH - Database locking and performance are classic SQLite issues.

**Research date:** 2026-04-04
**Valid until:** 2026-05-04
