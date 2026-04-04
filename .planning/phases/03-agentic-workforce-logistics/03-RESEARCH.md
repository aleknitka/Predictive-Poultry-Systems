# Phase 03: Agentic Workforce & Logistics - Research

**Researched:** 2026-04-04
**Domain:** Behavior Trees, Agentic Decision-Making (LLMs), Discrete Event Simulation Integration
**Confidence:** HIGH

## Summary

This phase implements the "brains" for the fulfillment node's agents (customers and staff). We will use a custom, Pydantic-native Behavior Tree (BT) implementation to manage high-level logic, decoupled from the simulation clock managed by `salabim`. Complex, "vibe-based" decisions (menu choice, satisfaction, morale) will be handled by `pydantic-ai` using "smol" LLMs (e.g., Nemotron-Nano-4B or Phi-4-mini).

**Primary recommendation:** Use a Pydantic-based `Node` model for BTs that returns `Status.RUNNING` when an action is triggered, allowing the `salabim.Component` process to handle the actual time delay (`hold()`).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01: Custom Minimal Behavior Tree (BT).** A lightweight, custom implementation of Behavior Trees will be used for agent logic to minimize external dependencies and ensure tight integration with Pydantic models.
- **D-02: Decoupled Logic and Time.** The BT nodes will handle decision-making logic ("what to do next"), while `salabim` processes will handle the simulation clock and resource management ("how long it takes"). The BT will NOT contain `yield self.hold()` directly.
- **D-03: Hybrid (Rules + LLM).** A hybrid approach where BT nodes handle standard operational rules, and LLM handles complex "vibe" decisions.
- **D-04: LLM-Managed Complex Decisions.** The LLM (smol models) will specifically handle: Menu item choices, Satisfaction updates, Staff morale & conflict resolution, Interaction quality.
- **D-05: Pydantic-AI Abstraction.** Use `pydantic-ai` for all LLM interactions.
- **D-06: Provider-Agnostic Inference.** Support for self-hosted (Ollama, LM Studio) and cloud (OpenRouter, HF) backends via a configurable interface.
- **D-07: Integrated with Pydantic Models.** BT structures and behavioral parameters will be defined/stored within the `BaseCustomer` and `BaseStaff` models.

### the agent's Discretion
- Exact structure of the minimal Behavior Tree implementation (nodes, decorators, control flow).
- Specific prompts for `pydantic-ai` agents.
- Fallback logic when LLM inference fails or is too slow.

### Deferred Ideas (OUT OF SCOPE)
- **Custom Simulation Engine.** Phase 3 implementation should be as modular as possible to facilitate a future migration, but `salabim` remains the engine for now.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AGT-CUST-01 | Implement customer segmentation (loyalty, RFM, sensitivity models) | BT logic will use these models as context for decision nodes. |
| AGT-CUST-02 | Model customer arrival patterns and decision-making logic in queues | Selector nodes will evaluate queue length vs. patience. |
| AGT-STAF-01 | Define staff agents with labor efficiency and operational tasks | Staff BTs will prioritize tasks based on role and efficiency. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `pydantic-ai` | 1.77.0 | LLM Agent abstraction | Native Pydantic support, type-safe agent outputs. |
| `pydantic` | 2.12.5 | Data modeling | Project standard for entity definitions. |
| `salabim` | 24.0.12 | Simulation Engine | Existing DES engine for the project. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| `ollama` | Latest | Local LLM hosting | When running "smol" models locally (Nemotron-Nano-4B). |
| `openrouter` | API | Cloud LLM aggregation | When scaling to higher-performance models (Claude 3.5). |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom BT | `py_trees` | `py_trees` is powerful but ROS-centric and harder to serialize with Pydantic. |
| Custom BT | Finite State Machines | FSMs become "spaghetti" quickly as complexity (loyalty, segments) grows. |

**Installation:**
```bash
uv add pydantic-ai
```

## Architecture Patterns

### Recommended Project Structure
```
src/predictive_poultry_systems/agents/
├── behavior/
│   ├── bt/
│   │   ├── base.py       # Minimal BT Node models
│   │   ├── composites.py # Sequence, Selector, etc.
│   │   └── leaves.py     # Action and Condition nodes
│   └── llm/
│       ├── agents.py     # Pydantic-AI agent definitions
│       └── providers.py  # Model/Provider configuration
├── customers/
│   ├── behavior.py       # Customer-specific BT trees
│   └── ...
└── staff/
    ├── behavior.py       # Staff-specific BT trees
    └── ...
```

### Pattern: BT-Salabim Decoupling
**What:** The BT determines "What to do next" (State), while the `salabim.Component` process executes "How long it takes" (Time).
**When to use:** All agent behavior cycles.
**Example:**
```python
# BT Action Node (Returns RUNNING until action finishes)
class OrderAction(ActionNode):
    type: str = "order_poultry"

    def tick(self, agent) -> Status:
        if not agent.is_action_active(self.type):
            agent.start_action(self.type) # Tell salabim to start
            return Status.RUNNING
        if agent.is_action_complete(self.type):
            return Status.SUCCESS
        return Status.RUNNING

# Salabim Component
class Customer(sim.Component):
    def process(self):
        while True:
            status = self.bt.tick(self)
            if status == Status.RUNNING and self.pending_action:
                yield self.hold(self.pending_action.duration)
                self.finalize_action()
            elif status == Status.SUCCESS:
                yield self.hold(0) # Next tick
            else:
                yield self.hold(1) # Wait/Idle
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| LLM Response Parsing | Custom RegEx/JSON loads | `pydantic-ai` | Handles structured output validation and retries automatically. |
| Provider Switching | Multiple API clients | `pydantic-ai` Models | Standardized interface for OpenAI, Ollama, Anthropic, etc. |
| DES Scheduling | Manual event loops | `salabim` | Built-in time management and resource contention handling. |

## Common Pitfalls

### Pitfall 1: Blocking the Simulation
**What goes wrong:** Calling a remote LLM (OpenRouter) inside a `salabim` process without consideration for simulation time.
**Why it happens:** Real-world wall clock time != Simulation time.
**How to avoid:** Perform LLM calls in a way that allows the simulation to either "pause" or account for the decision latency as a simulation delay.
**Warning signs:** Simulation "stuttering" or non-deterministic results based on network speed.

### Pitfall 2: Infinite BT Loops
**What goes wrong:** A BT node returns `SUCCESS` instantly, and the `salabim` loop re-ticks it immediately without a `hold()`.
**Why it happens:** BT logic doesn't consume simulation time by default.
**How to avoid:** Ensure the `salabim` process loop always `yield self.hold()` with at least a tiny duration (or 0 to allow other components to run) between ticks.

## Code Examples

### Minimal Pydantic BT Node
```python
from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field

class Status(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

class Node(BaseModel):
    name: str
    def tick(self, context) -> Status:
        raise NotImplementedError

class Sequence(Node):
    children: List[Node] = Field(default_factory=list)
    def tick(self, context) -> Status:
        for child in self.children:
            status = child.tick(context)
            if status != Status.SUCCESS: return status
        return Status.SUCCESS
```

### Pydantic-AI Agent (Menu Choice)
```python
from pydantic_ai import Agent
from pydantic import BaseModel

class MenuSelection(BaseModel):
    item_id: str
    justification: str

menu_agent = Agent(
    'ollama:nemotron-nano',
    result_type=MenuSelection,
    system_prompt="You are a customer at a poultry restaurant. Choose an item based on your loyalty and hunger."
)

# Usage in a BT Node:
# result = await menu_agent.run("Loyalty: Champion, Hunger: High", deps=menu_context)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Large FSMs | Behavior Trees | 2010s (Games) | Better modularity and reusability. |
| Hard-coded Logic | LLM-Driven Decisions | 2023+ | Nuanced, "human-like" behavior without complex branching. |
| LangChain | `pydantic-ai` | 2024 | Tighter integration with Pydantic 2.0 type safety. |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | ✓ | 3.12.3 | Use 3.13 via uv if needed |
| `uv` | Dependency Mgmt | ✓ | 0.11.1 | — |
| `salabim` | Simulation | ✓ | 24.0.12 | — |
| `ollama` | Local LLM | ✗ | — | Use OpenRouter/HF |
| `openrouter.ai` | Cloud LLM | ✓ | — | — |

**Missing dependencies with no fallback:**
- None.

**Missing dependencies with fallback:**
- `ollama` (Local LLM): Use OpenRouter or Hugging Face serverless inference.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `pytest` |
| Config file | `pyproject.toml` |
| Quick run command | `uv run pytest tests/test_agents.py` |
| Full suite command | `uv run pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AGT-BT-01 | Minimal BT Node Logic (Success/Failure/Sequence) | unit | `uv run pytest tests/test_behavior.py` | ❌ Wave 0 |
| AGT-LLM-01| Pydantic-AI mock integration | integration | `uv run pytest tests/test_ai_agents.py` | ❌ Wave 0 |
| AGT-SIM-01| Decoupled BT/Salabim tick coordination | integration | `uv run pytest tests/test_bt_salabim.py` | ❌ Wave 0 |

### Wave 0 Gaps
- [ ] `tests/test_behavior.py` — Covers core BT node logic.
- [ ] `tests/test_ai_agents.py` — Covers LLM agent mocks.
- [ ] `tests/test_bt_salabim.py` — Covers simulation timing.

## Sources

### Primary (HIGH confidence)
- [Pydantic-AI Documentation](https://ai.pydantic.dev/) - Agent and Provider configuration.
- [Salabim Documentation](https://www.salabim.org/manual/) - Process and time management.
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/) - Model structure and validation.

### Secondary (MEDIUM confidence)
- Web search for "Behavior Trees in Python" patterns.
- Web search for "Small Language Models 2026".

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Libraries are mature and well-documented.
- Architecture: HIGH - BT decoupling is a standard pattern in game dev/robotics.
- Pitfalls: MEDIUM - Async/LLM timing in a synchronous DES can be tricky.

**Research date:** 2026-04-04
**Valid until:** 2026-05-04
