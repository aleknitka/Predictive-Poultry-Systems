# Phase 3: Agentic Workforce & Logistics - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in 03-CONTEXT.md — this log preserves the analysis.

**Date:** 2026-04-04
**Phase:** 03-agentic-workforce-logistics
**Mode:** discuss

## Discussion Summary

### Gray Area 1: Behavioral Logic
- **Options presented:** State Machines / Rulesets, Behavior Trees, salabim Processes.
- **Decision:** **Behavior Trees**.
- **Reasoning:** User wanted a more flexible and agent-like structure for complex behavior.

### Gray Area 2: LLM Integration
- **Options presented:** Real-time Inference, Offline Generation, Hybrid (Rules + LLM).
- **Decision:** **Hybrid (Rules + LLM)**.
- **Reasoning:** Standard rules handle operations while LLM handles complex "vibe" decisions. User expanded this to include morale and interaction quality.

### Gray Area 3: Inference Backend
- **Options presented:** Local Hosting, Cloud API (OpenRouter/HF), Configurable / Provider-agnostic.
- **Decision:** **Configurable / Provider-agnostic**.
- **Reasoning:** User explicitly requested support for Ollama, LM Studio, OpenRouter, and HF endpoints.

### Gray Area 4: LLM Abstraction Layer
- **Options presented:** LiteLLM, Custom, Direct API.
- **User input:** **pydantic-ai**.
- **Reasoning:** Excellent alignment with existing codebase's heavy use of Pydantic.

### Gray Area 5: BT-Salabim Integration
- **Options presented:** Tick inside salabim process, BT nodes as components, Decoupled Logic and Time.
- **Decision:** **Decoupled Logic and Time**.
- **Reasoning:** Separation of concerns between decision logic and simulation time.

## User Suggestions & Feedback
- User expressed interest in potentially writing a custom engine ("maybe we should write our own engine?").
- Use of "smol" models (smol-vlm/smol-llm) suggested for efficiency.
- Integration of rulesets directly into Pydantic models for consistency.

## Decisions Made
- [D-01] Custom Minimal BT implementation.
- [D-02] Decoupled Logic and Time.
- [D-03] Hybrid LLM/Rules approach.
- [D-04] LLM for Menu, Satisfaction, Morale, and Interaction Quality.
- [D-05] pydantic-ai as the LLM interface.
- [D-06] Provider-agnostic inference support.
- [D-07] BT integrated with Pydantic models.
