# Phase 2: Operational Assets - Implementation Plan

## Objective
Establish a comprehensive, high-fidelity set of Pydantic models representing the core operational assets of the fulfillment node: Machines, Menu Items (including complex Meals), Staff, and the underlying Processes. This foundation will enable accurate simulation of thermodynamic transformation, resource consumption, waste generation, and labor utilization.

## Background & Motivation
To achieve a "hardcore" simulation, the models must accurately reflect real-world complexities: machines consume variable power based on state (idle vs. working), experience random faults, require human operators (FTEs), ingest raw materials (ingredients), and produce both finished goods and waste (which incurs disposal costs). Menu items range from single products to complex combo meals requiring assembly and packaging.

## Scope & Impact
This phase focuses purely on data modeling and relationship definition using `pydantic`. It will impact:
- `src/predictive_poultry_systems/objects/machines/`
- `src/predictive_poultry_systems/objects/menu/`
- `src/predictive_poultry_systems/agents/staff/`
- `src/predictive_poultry_systems/objects/processes/` (New)

## Proposed Solution

### 1. Enhance Menu & Ingredient Models (`objects/menu/base.py`)
- **Expanded Enums**: Add more `IngredientTypes` (e.g., frozen fries, potatoes, burger buns, raw patties, lettuce, soda syrup).
- **Packaging**: Introduce a specific `PackagingType` enum (e.g., box, cup, bag) to track packaging as a consumable resource.
- **`BaseMenuItem` Updates**: Ensure it accurately reflects the bill of materials (ingredients + packaging) required.
- **New `Meal` Model**: Create a `ComboMeal` class that aggregates multiple `BaseMenuItem` instances (e.g., Burger + Fries + Drink) into a single customer-facing product, including a bundled `manu_price` and specific combo packaging.

### 2. Overhaul Machine Models (`objects/machines/base.py`)
- **Raw Material Inputs**: Add an `ingredient_inputs: dict[IngredientTypes, float]` field to track what physical items the machine consumes per cycle.
- **Waste Generation**: Add a `waste_outputs: dict[MachineWasteTypes, float]` field.
- **Waste Disposal Costs**: Introduce a mapping of `MachineWasteTypes` to disposal cost per standardized unit to accurately model financial penalties of waste.
- **Stateful Consumption**: Refine `OperationModes` to explicitly tie to simulation states (Off, Idle, Working, Faulted).
- **Staffing Requirements**: Make FTE requirements dynamic based on the machine's state (e.g., requires 1 FTE to operate, 0 to idle, 0.5 to clean).

### 3. Create Staff Models (`agents/staff/base.py`)
- **`StaffRoles` Enum**: Define roles (e.g., Cashier, Fry Cook, Grill Master, Manager).
- **`BaseStaff` Model**:
  - `role: StaffRoles`
  - `hourly_wage: float`
  - `skill_level: float` (affects processing time or fault probability).
  - `fatigue_rate: float` (increases over shift, affecting performance).

### 4. Define Process Models (`objects/processes/base.py`)
- **`ThermodynamicProcess` Model**: Defines the time and energy required to transform specific `ingredient_inputs` into `outputs` using a specific `MachineType`.
- **`AssemblyProcess` Model**: Defines the time and FTE requirements to package and assemble `MenuItemTypes` into a final `ComboMeal` for the customer.

## Implementation Steps
1. **Update `menu/base.py`**: Add extended enums, refine `BaseMenuItem`, and introduce `ComboMeal`.
2. **Update `machines/base.py`**: Add ingredient inputs, waste outputs, and cost mappings to `BaseMachine`. Ensure `OperationModes` covers all states.
3. **Create `staff/base.py`**: Implement `StaffRoles` and `BaseStaff` Pydantic models.
4. **Create `processes/base.py`**: Implement `ThermodynamicProcess` and `AssemblyProcess` to link machines, staff, and menu items.
5. **Validation**: Write Pydantic `@model_validator` methods to ensure data consistency (e.g., a machine cannot produce an output without required inputs; combo meals must have >1 item).
6. **Testing**: Add `pytest` test cases in `tests/test_objects.py` to verify model instantiation, validation logic, and cost calculations.

## Alternatives Considered
- **Direct implementation in Salabim components**: Skipped in favor of strict Pydantic models first. Pydantic ensures all data relationships are validated *before* the simulation engine consumes them, preventing runtime errors during complex simulation scenarios.

## Verification & Testing
- All Pydantic models must instantiate without validation errors given valid synthetic data.
- Validation errors must trigger correctly for invalid states (e.g., negative waste, missing ingredients).
- Run `uv run pytest`, `uv run ruff check .`, and `uv run prek run --all-files` to ensure quality gates pass.
