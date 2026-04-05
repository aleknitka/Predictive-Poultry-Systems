import salabim as sim
from typing import Any
from pydantic import BaseModel
from ..behavior.bt.base import Status, Node
from ..behavior.bt.leaves import ActionNode
from ..behavior.bt.composites import Sequence
from .base import BaseStaff
from ..behavior.metrics import calculate_morale, calculate_crisp_state
from predictive_poultry_systems.config import SECONDS_PER_SIM_UNIT

# --- STAFF LEAF NODES ---


class TaskPriorityNode(ActionNode):
    """Determines next task based on role and facility needs."""

    def tick(self, agent: Any) -> Status:
        # For now, simulate picking a task
        if not agent.memory.get("current_task"):
            agent.memory["current_task"] = "grilling_poultry"
        return Status.SUCCESS


class FulfillmentNode(ActionNode):
    """Handles thermodynamic/assembly process steps."""

    def tick(self, agent: Any) -> Status:
        # Simulate working on a task
        if agent.memory.get("current_task"):
            return Status.SUCCESS
        return Status.FAILURE


class MoraleResponse(BaseModel):
    new_morale: float
    reason: str


class MoraleNode(ActionNode):
    """LLM-driven morale update based on fatigue and workload."""

    def tick(self, agent: Any) -> Status:
        # Simple rule-based morale update for now
        # Morale decreases with fatigue
        # BaseStaff doesn't have fatigue field, it has fatigue_rate
        return Status.SUCCESS


# --- FACTORY FUNCTIONS ---


def get_default_staff_tree() -> Node:
    """Returns the default behavior tree for a staff agent."""
    return Sequence(
        name="staff_root",
        children=[
            TaskPriorityNode(name="pick_task"),
            FulfillmentNode(name="execute_task"),
            MoraleNode(name="check_morale"),
        ],
    )


# --- SALABIM COMPONENTS ---


class ProteinUnit(sim.Component):
    """A data component representing a piece of poultry."""

    def setup(self, crispness: float = 1.0):
        self.crispness = crispness


class Staff(sim.Component):
    """
    Active staff component driving fulfillment tasks.
    """

    def setup(self, agent_data: BaseStaff):
        self.agent_data = agent_data
        self.fatigue = 0.0

    def process(self):
        while True:
            # --- MORALE UPDATE ---
            current_morale = calculate_morale(
                fatigue=self.fatigue, skill_level=self.agent_data.skill_level
            )
            self.env.fulfillment_manager.update_morale(self.name(), current_morale)

            # 1. Idle / Wait for Work
            if not self.env.fulfillment_manager.orders:
                yield self.wait(self.env.fulfillment_manager.order_available_signal)

            # Pick an order (FIFO for now)
            order = self.env.fulfillment_manager.pop_order()
            if not order:
                continue

            # 2. Production (Cooking)
            yield self.request(self.env.fryers)
            skill_mod = max(self.agent_data.skill_level, 0.1)

            # Simulate a ThermodynamicProcess (duration_mean ~ 4)
            cook_duration = sim.Uniform(3, 5).sample() / skill_mod
            yield self.hold(cook_duration)
            self.release()

            # --- CRISPNESS CALCULATION ---
            cook_time_s = cook_duration * SECONDS_PER_SIM_UNIT
            crispness = calculate_crisp_state(cook_time=cook_time_s)
            self.env.fulfillment_manager.tally_crispness(crispness)

            # 3. Fulfillment (Putting in cabinet)
            # Item is ready
            item = ProteinUnit(
                name=f"ProteinUnit.{self.env.now()}", crispness=crispness
            )
            yield self.to_store(self.env.holding_cabinet, item)

            # 4. Cleanup/Cycle reset & Fatigue increment
            yield self.hold(0.5)
            self.fatigue = min(1.0, self.fatigue + self.agent_data.fatigue_rate)
