# Phase 03-02 Summary: Agent Behavior Definitions

## Objective
Define specific behavior trees and hybrid decision logic for Customer and Staff agents. Update the base Pydantic models to incorporate these behavioral "brains".

## Deliverables
- `src/predictive_poultry_systems/agents/customers/behavior.py`: Customer-specific BT leaf nodes (`ArriveNode`, `QueueDecisionNode`, `OrderDecisionNode`) and default tree factory.
- `src/predictive_poultry_systems/agents/staff/behavior.py`: Staff-specific BT leaf nodes (`TaskPriorityNode`, `FulfillmentNode`, `MoraleNode`) and default tree factory.
- Updated `BaseCustomer` and `BaseStaff` models in their respective `base.py` files to include:
    - `root_node`: The Behavior Tree root.
    - `brain`: The `DecisionAgent` for complex tasks.
    - `memory`: A dictionary for transient agent state.
- `tests/test_agent_behavior.py`: Verification of behavioral flows and Pydantic integration.

## Verification Results
- All agent behavior tests passed.
- Customer behavior correctly handles rule-based queue decisions using threshold checks in memory.
- Staff behavior correctly simulates task picking and execution.
- Pydantic models successfully validate with `Node` objects (BTs) as fields.

## Decisions Implemented
- **[D-01]** Custom Minimal BT implementation.
- **[D-03]** Hybrid LLM/Rules approach structure established.
- **[D-07]** BT integrated with Pydantic models.

## Next Steps
- Execute **03-03-PLAN.md: Simulation Integration** to bridge the behavioral agents with the `salabim` discrete event simulation timeline.
