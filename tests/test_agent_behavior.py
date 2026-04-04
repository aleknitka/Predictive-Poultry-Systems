import pytest
from predictive_poultry_systems.agents.customers.base import BaseCustomer
from predictive_poultry_systems.agents.staff.base import BaseStaff, StaffRoles
from predictive_poultry_systems.agents.customers.loyalty import (
    CustomerLoyalty,
    CustomerLoyaltyLevel,
)
from predictive_poultry_systems.agents.customers.segments import (
    CustomerSegment,
    CustomerSegmentTypes,
)
from predictive_poultry_systems.agents.customers.rfm import CustomerRFMProfile
from predictive_poultry_systems.agents.customers.behavior import (
    get_default_customer_tree,
)
from predictive_poultry_systems.agents.staff.behavior import get_default_staff_tree
from predictive_poultry_systems.agents.behavior.bt.base import Status


@pytest.fixture
def champion_loyalty():
    return CustomerLoyalty(
        level=CustomerLoyaltyLevel.CHAMPION,
        rfm=CustomerRFMProfile(recency=5, frequency=5, monetary=5),
    )


@pytest.fixture
def family_segment():
    return CustomerSegment(
        name=CustomerSegmentTypes.MILENNIALS,  # Use existing type
        profile="Family oriented",
        preferences="Nuggets and Fries",
    )


def test_customer_behavior_flow(family_segment, champion_loyalty):
    customer = BaseCustomer(
        segment=family_segment,
        satisfaction=8.0,
        price_sensitivity=0.5,
        promo_sensitivity=0.5,
        loyalty=champion_loyalty,
        root_node=get_default_customer_tree(),
    )

    # Simulate first tick (arrival)
    status = customer.root_node.tick(customer)
    assert status == Status.SUCCESS
    assert customer.memory.get("is_at_facility") is True

    # Simulate second tick (queue decision with long queue)
    customer.memory["current_queue_length"] = 10
    # The default tree has a QueueDecisionNode with threshold 5
    status = customer.root_node.tick(customer)
    assert status == Status.FAILURE


def test_staff_behavior_flow():
    staff = BaseStaff(
        name="Bob",
        role=StaffRoles.FRY_COOK,
        hourly_wage=15.0,
        skill_level=0.9,
        fatigue_rate=0.1,
        shift_hours=8.0,
        root_node=get_default_staff_tree(),
    )

    # Simulate tick
    status = staff.root_node.tick(staff)
    assert status == Status.SUCCESS
    assert staff.memory.get("current_task") == "grilling_poultry"


def test_pydantic_bt_integration(family_segment, champion_loyalty):
    # Verify we can define a customer with a BT and it validates
    tree = get_default_customer_tree()
    customer = BaseCustomer(
        segment=family_segment,
        satisfaction=8.0,
        price_sensitivity=0.5,
        promo_sensitivity=0.5,
        loyalty=champion_loyalty,
        root_node=tree,
    )
    assert customer.root_node.name == "customer_root"
