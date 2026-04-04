# Phase 04-01 Summary: Agent Behavioral Lifecycle Logic

## Objective
Implement the active simulation components for Customers and Staff using `salabim.Component`. This bridges static Pydantic models with process-based discrete event logic.

## Deliverables
- `src/predictive_poultry_systems/agents/customers/behavior.py`: Added `Customer` class inheriting from `sim.Component`.
- `src/predictive_poultry_systems/agents/staff/behavior.py`: Added `Staff` class inheriting from `sim.Component`.

## Verification Results
- `Customer` and `Staff` components are successfully importable.
- Components are designed to work with `BaseCustomer` and `BaseStaff` Pydantic models.
- Process logic templates (Arrival, Ordering, Fulfillment, Delivery) are established.

## Next Steps
- Execute **04-02-PLAN.md: End-to-End Simulation Loop Integration** to connect these agents with physical resources (Machines, Kiosks) in `main.py`.
