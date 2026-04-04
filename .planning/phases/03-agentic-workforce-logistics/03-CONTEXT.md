# Phase 3: Agentic Workforce & Logistics - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement behavior models for customers and staff. Customers must exhibit loyalty/segment-based arrival and queueing patterns. Staff agents successfully execute fulfillment tasks with efficiency metrics. This phase focuses on the logic ("brain") of the agents within the existing `salabim` environment.

</domain>

<decisions>
## Implementation Decisions

### Behavioral Architecture
- **D-01: Custom Minimal Behavior Tree (BT).** A lightweight, custom implementation of Behavior Trees will be used for agent logic to minimize external dependencies and ensure tight integration with Pydantic models.
- **D-02: Decoupled Logic and Time.** The BT nodes will handle decision-making logic ("what to do next"), while `salabim` processes will handle the simulation clock and resource management ("how long it takes"). The BT will NOT contain `yield self.hold()` directly.

### LLM Integration Strategy
- **D-03: Hybrid (Rules + LLM).** A hybrid approach where BT nodes handle standard operational rules, and LLM handles complex "vibe" decisions.
- **D-04: LLM-Managed Complex Decisions.** The LLM (smol models) will specifically handle:
    - Menu item choices (complex selection).
    - Satisfaction updates (nuanced feedback).
    - Staff morale & conflict resolution.
    - Interaction quality (staff-customer).
- **D-05: Pydantic-AI Abstraction.** Use `pydantic-ai` for all LLM interactions, as it aligns with the project's existing usage of Pydantic.
- **D-06: Provider-Agnostic Inference.** Support for self-hosted (Ollama, LM Studio) and cloud (OpenRouter, HF) backends via a configurable interface.

### Data Modeling
- **D-07: Integrated with Pydantic Models.** Behavior tree structures and behavioral parameters will be defined/stored within the `BaseCustomer` and `BaseStaff` models (or specialized behavior-centric extensions).

### Claude's Discretion
- Exact structure of the minimal Behavior Tree implementation (nodes, decorators, control flow).
- Specific prompts for `pydantic-ai` agents.
- Fallback logic when LLM inference fails or is too slow.

</decisions>

<specifics>
## Specific Ideas

- "We can use either self hosted ollama, lm studio, openrouter, or HF endpoints."
- Use "smol" models (like `smol-vlm` or `smol-llm`) to enable complex decisions without massive overhead.
- "Integrated with Pydantic Models" - Ensure BT nodes are serializable or can be instantiated from Pydantic schemas.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Roadmap
- `.planning/REQUIREMENTS.md` — Core AGT-* requirements for actors.
- `.planning/ROADMAP.md` — Phase 3 goal and success criteria.

### Existing Agent Objects
- `src/predictive_poultry_systems/agents/customers/base.py` — Base customer model.
- `src/predictive_poultry_systems/agents/staff/base.py` — Base staff model.

### External Libraries
- [pydantic-ai documentation](https://ai.pydantic.dev/) — Framework for LLM integration.
- [salabim documentation](https://www.salabim.org/manual/) — Current simulation engine.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BaseCustomer` and `BaseStaff` (Pydantic models) — These are the primary anchors for behavior integration.
- `CustomerLoyalty` and `CustomerSegment` — Existing enums/models that should drive BT decisions.

### Established Patterns
- High-fidelity modeling using Pydantic in `src/predictive_poultry_systems/objects/`.
- Process-based simulation in `salabim` (requires careful integration with BT "ticks").

### Integration Points
- `src/predictive_poultry_systems/agents/` — New behavioral logic files should be organized here.
- `main.py` — The simulation loop where agents are instantiated and "ticked".

</code_context>

<deferred>
## Deferred Ideas

### Custom Simulation Engine
- The user expressed interest in a custom engine ("Don't know what is best here, maybe we should write our own engine?"). This remains scheduled for Phase 6, but Phase 3 implementation should be as modular as possible to facilitate a future migration.

</deferred>

---

*Phase: 03-agentic-workforce-logistics*
*Context gathered: 2026-04-04*
