# Phase 01: Foundation & Baseline - Validation Strategy

**Date:** 2025-03-24
**Status:** Active

## Phase Goal
Establish a stable environment for discrete event simulation with `salabim`.

## Dimension 8: Validation Requirements
Downstream executor MUST verify these criteria to complete the phase.

### Environment & Dependencies
- [ ] `uv sync` installs all dependencies including `salabim`, `greenlet`, and `Pillow`.
- [ ] `uv run python --version` returns 3.13.x.

### Code Quality
- [ ] `uv run ruff check .` returns no errors.
- [ ] `uv run prek run --all-files` exits with 0.

### Simulation Baseline
- [ ] `uv run main.py` executes a minimal simulation and prints start/finish times.
- [ ] `tests/test_env.py` exists and passes, verifying `salabim.Environment` and `pydantic` models.

### Integration
- [ ] `salabim` trace shows components being created and scheduled.
