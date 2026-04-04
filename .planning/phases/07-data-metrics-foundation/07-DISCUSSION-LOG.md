# Phase 7: Data & Metrics Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in 07-CONTEXT.md — this log preserves the analysis.

**Date:** 2026-04-04
**Phase:** 07-data-metrics-foundation
**Mode:** discuss

## Discussion Summary

### Gray Area 1: Logging Library
- **Options presented:** Standard 'logging', loguru, structlog.
- **Decision:** **loguru**.
- **Reasoning:** Modern, easy to use, beautiful output.

### Gray Area 2: Database Interaction
- **Options presented:** Direct 'sqlite3', SQLAlchemy (Core/ORM), Peewee.
- **Decision:** **Direct 'sqlite3'**.
- **Reasoning:** Simple, no extra dependencies.

### Gray Area 3: Data Schema Strategy
- **Options presented:** Relational/Normalized, Schema-less (JSON blobs), Hybrid (Structured + JSON).
- **Decision:** **Relational/Normalized**.
- **Reasoning:** Structured tables for Customers, Staff, Machines, etc. Good for queries.

### Gray Area 4: Salabim Integration
- **Options presented:** Salabim Monitors, Manual Process Triggers, Observer Pattern.
- **Decision:** **Salabim Monitors**.
- **Reasoning:** Built-in salabim monitors are fast and specifically designed for this purpose.

### Gray Area 5: Writing Strategy
- **Options presented:** Real-time synchronous, Buffered/Batch writes.
- **Decision:** **Real-time synchronous**.
- **Reasoning:** Simple, safe, ensures data integrity.

## Decisions Made
- [D-01] loguru for logging.
- [D-02] salabim monitors for data collection.
- [D-03] direct sqlite3 for database.
- [D-04] relational/normalized schema in SQLite.
- [D-05] real-time synchronous database writes.
