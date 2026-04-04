import salabim as sim
from predictive_poultry_systems.agents.simulation import BehavioralComponent
from predictive_poultry_systems.agents.customers.base import BaseCustomer
from predictive_poultry_systems.agents.customers.loyalty import (
    CustomerLoyalty,
    CustomerLoyaltyLevel,
)
from predictive_poultry_systems.agents.customers.segments import (
    CustomerSegment,
    CustomerSegmentTypes,
)
from predictive_poultry_systems.agents.customers.rfm import CustomerRFMProfile
from predictive_poultry_systems.agents.behavior.bt.base import Status
from predictive_poultry_systems.agents.behavior.bt.leaves import ActionNode


class SimpleHoldAction(ActionNode):
    duration: float = 1.0

    def tick(self, agent) -> Status:
        if agent.memory.get("action_complete"):
            agent.memory["action_complete"] = False  # Reset for next potential use
            return Status.SUCCESS

        agent.memory["action_duration"] = self.duration
        return Status.RUNNING


def test_bt_salabim_timing():
    env = sim.Environment(trace=False, yieldless=False)

    # Setup agent with a simple hold action
    tree = SimpleHoldAction(name="hold_1s", duration=1.0)

    agent_data = BaseCustomer(
        segment=CustomerSegment(
            name=CustomerSegmentTypes.MILENNIALS, profile="", preferences=""
        ),
        satisfaction=5.0,
        price_sensitivity=0.5,
        promo_sensitivity=0.5,
        loyalty=CustomerLoyalty(
            level=CustomerLoyaltyLevel.LOYAL,
            rfm=CustomerRFMProfile(recency=3, frequency=3, monetary=3),
        ),
        root_node=tree,
    )

    BehavioralComponent(env=env, agent_data=agent_data)

    # Run for a bit
    env.run(till=0.5)
    # At 0.5, it should be in the middle of the first hold
    assert env.now() == 0.5
    assert agent_data.memory.get("action_duration") == 1.0

    env.run(till=1.5)
    # At 1.5, the first hold should have finished, and it should have ticked again.
    # The BehavioralComponent.process loop:
    # tick -> RUNNING -> hold(1.0) -> set action_complete=True -> loop -> tick -> SUCCESS -> hold(0.1) -> loop

    assert env.now() == 1.5
    # The action_complete was set to True at t=1.0
    # Then at t=1.0, it looped, ticked, got SUCCESS (because action_complete was True),
    # then did hold(0.1).
    # Then at t=1.1, it looped, ticked, got RUNNING again (because action_complete was reset to False),
    # then did hold(1.0) scheduled for t=2.1.

    # So at t=1.5, it should be holding until t=2.1.
    assert agent_data.memory.get("action_duration") == 1.0
