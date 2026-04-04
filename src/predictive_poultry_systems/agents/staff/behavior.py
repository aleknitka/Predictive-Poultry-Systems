from typing import Any
from pydantic import BaseModel
from ..behavior.bt.base import Status, Node
from ..behavior.bt.leaves import ActionNode
from ..behavior.bt.composites import Sequence

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
