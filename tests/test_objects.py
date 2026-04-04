import pytest
from predictive_poultry_systems.objects.menu.base import (
    BaseMenuItem,
    ComboMeal,
    MenuItemTypes,
    MenuItemSizes,
    IngredientTypes,
    PackagingTypes,
)
from predictive_poultry_systems.objects.machines.base import (
    BaseMachine,
    MachineTypes,
    MachineConsumptionTypes,
    OperationModes,
)
from predictive_poultry_systems.agents.staff.base import BaseStaff, StaffRoles
from predictive_poultry_systems.objects.processes.base import (
    ThermodynamicProcess,
    AssemblyProcess,
)
from predictive_poultry_systems.objects.facilities.base import (
    BaseFacility,
    FacilityTypes,
    StoreLayout,
)


def test_menu_item_creation():
    item = BaseMenuItem(
        type=MenuItemTypes.FRIES,
        size=MenuItemSizes.REGULAR,
        name="Large Fries",
        icon="🍟",
        wholesale_price=0.5,
        manu_price=2.5,
        ingredients={IngredientTypes.FROZEN_FRIES: 1.0, IngredientTypes.OIL: 0.1},
        packaging={PackagingTypes.BAG: 1},
        waste=0.05,
        corporate_name="fries_standard_v1",
    )
    assert item.name == "Large Fries"
    assert item.manu_price == 2.5


def test_combo_meal_validation():
    item1 = BaseMenuItem(
        type=MenuItemTypes.BURGER,
        size=MenuItemSizes.REGULAR,
        name="Burger",
        icon="🍔",
        wholesale_price=1.0,
        manu_price=5.0,
        ingredients={IngredientTypes.BURGER_BUNS: 1, IngredientTypes.RAW_PATTIES: 1},
        waste=0.1,
        corporate_name="burger_v1",
    )
    item2 = BaseMenuItem(
        type=MenuItemTypes.SODA,
        size=MenuItemSizes.REGULAR,
        name="Soda",
        icon="🥤",
        wholesale_price=0.2,
        manu_price=2.0,
        ingredients={IngredientTypes.SODA_SYRUP: 0.1, IngredientTypes.WATER: 0.4},
        waste=0.01,
        corporate_name="soda_v1",
    )

    # Valid combo
    combo = ComboMeal(
        name="Meal #1",
        icon="🍱",
        items=[item1, item2],
        manu_price=6.0,
        combo_packaging={PackagingTypes.BAG: 1},
    )
    assert combo.manu_price == 6.0

    # Invalid combo: price exceeds individual items
    with pytest.raises(
        ValueError, match="Combo price cannot exceed the sum of individual item prices"
    ):
        ComboMeal(
            name="Meal #2",
            icon="🍱",
            items=[item1, item2],
            manu_price=8.0,
            combo_packaging={PackagingTypes.BAG: 1},
        )


def test_machine_reliability_validation():
    modes = OperationModes(idle=0.1, working=1.0, off=0.0, faulted=0.05)

    # Valid machine
    machine = BaseMachine(
        name="Deep Fryer",
        icon="🔥",
        type=MachineTypes.COOKING,
        corporate_name="fryer_pro_500",
        inputs={MachineConsumptionTypes.POWER: modes},
        outputs={MenuItemTypes.FRIES: 5.0},
        fault_rate=0.01,
        repair_time_mean=10.0,
    )
    assert machine.repair_time_mean == 10.0

    # Invalid machine: fault_rate > 0 but repair_time_mean == 0
    with pytest.raises(
        ValueError,
        match="Machines with a non-zero fault rate must have a non-zero repair_time_mean",
    ):
        BaseMachine(
            name="Broken Fryer",
            icon="🔥",
            type=MachineTypes.COOKING,
            corporate_name="fryer_broken",
            inputs={MachineConsumptionTypes.POWER: modes},
            outputs={MenuItemTypes.FRIES: 5.0},
            fault_rate=0.01,
            repair_time_mean=0.0,
        )


def test_staff_creation():
    staff = BaseStaff(
        name="Alice",
        role=StaffRoles.FRY_COOK,
        hourly_wage=15.0,
        skill_level=0.9,
        fatigue_rate=0.05,
        shift_hours=8.0,
    )
    assert staff.name == "Alice"
    assert staff.role == StaffRoles.FRY_COOK


def test_processes_creation():
    # Thermodynamic
    tp = ThermodynamicProcess(
        name="Fry Fries",
        machine_type=MachineTypes.COOKING,
        ingredient_inputs={IngredientTypes.FROZEN_FRIES: 1.0},
        menu_outputs={MenuItemTypes.FRIES: 1.0},
        duration_mean=5.0,
        energy_intensity=1.2,
        target_temp_c=180.0,
    )
    assert tp.target_temp_c == 180.0

    # Assembly
    ap = AssemblyProcess(
        name="Make Meal",
        item_inputs=[MenuItemTypes.BURGER, MenuItemTypes.FRIES],
        output_item=MenuItemTypes.COMBO_MEAL,
        fte_requirement=0.5,
        duration_mean=2.0,
    )
    assert ap.fte_requirement == 0.5


def test_facility_creation():
    fac = BaseFacility(
        name="Front Counter Queue",
        type=FacilityTypes.QUEUE_AREA,
        capacity=10,
        occupied=2,
    )
    assert fac.available_capacity == 8

    layout = StoreLayout(node_id="NODE-01", total_area_sqm=150.0, facilities=[fac])
    assert len(layout.facilities) == 1
