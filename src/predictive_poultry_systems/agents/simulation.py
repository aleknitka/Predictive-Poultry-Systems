import salabim as sim
from typing import Union
from .customers.base import BaseCustomer
from .staff.base import BaseStaff
from .behavior.bt.base import Status


class BehavioralComponent(sim.Component):
    """
    Salabim component that is driven by a Pydantic agent model (BT-based).
    """

    def setup(self, agent_data: Union[BaseCustomer, BaseStaff]):
        self.agent_data = agent_data
        # Ensure agent_data has a root_node to drive behavior
        if not self.agent_data.root_node:
            raise ValueError(f"Agent {self.agent_data} must have a root_node defined.")

    def process(self):
        while True:
            # 1. Tick the Behavior Tree
            status = self.agent_data.root_node.tick(self.agent_data)

            # 2. Coordinate with Salabim timeline
            if status == Status.RUNNING:
                # If the BT is RUNNING, it means an action is in progress.
                # In a real scenario, we'd check for specific action durations in memory.
                # For Phase 3, we'll use a default 'action_duration' if set, otherwise 1.0.
                duration = self.agent_data.memory.get("action_duration", 1.0)
                yield self.hold(duration)

                # After holding, we might want to mark the action as finished in memory
                # so the next tick can proceed.
                self.agent_data.memory["action_complete"] = True

            elif status == Status.SUCCESS:
                # Decision finished successfully, yield 0 to allow other components to run
                # but basically continue the loop in the same "logical" time if needed,
                # or a small delta to prevent tight loops.
                yield self.hold(0.1)

            elif status == Status.FAILURE:
                # Decision failed, maybe wait longer before retrying or idling
                yield self.hold(1.0)


class CustomerComponent(BehavioralComponent):
    """Specialized component for customers."""

    pass


class StaffComponent(BehavioralComponent):
    """Specialized component for staff."""

    pass
