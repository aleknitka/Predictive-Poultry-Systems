import salabim as sim
from typing import Any
from pydantic import BaseModel
from ..behavior.bt.base import Status, Node
from ..behavior.bt.leaves import ActionNode
from ..behavior.bt.composites import Sequence
from .base import BaseCustomer

# --- CUSTOMER LEAF NODES ---


class ArriveNode(ActionNode):
    """Handles facility entry logic."""

    def tick(self, agent: Any) -> Status:
        # Use agent memory for state
        if not agent.memory.get("is_at_facility"):
            agent.memory["is_at_facility"] = True
            return Status.SUCCESS
        return Status.SUCCESS


class QueueDecisionNode(ActionNode):
    """
    Hybrid node: BT rules for queue length, LLM for "patience vibe".
    """

    queue_threshold: int = 10

    def tick(self, agent: Any) -> Status:
        # Rule-based fast failure
        # We assume simulation environment will inject this into memory or it's an attribute
        current_queue = agent.memory.get("current_queue_length", 0)
        if current_queue > self.queue_threshold:
            return Status.FAILURE

        return Status.SUCCESS


class MenuSelection(BaseModel):
    item_id: str
    justification: str


class OrderDecisionNode(ActionNode):
    """LLM-driven menu selection."""

    def tick(self, agent: Any) -> Status:
        # In Wave 3 this will call agent.brain.decide
        if not agent.memory.get("selected_item"):
            agent.memory["selected_item"] = "simulated_nuggets"
        return Status.SUCCESS


# --- FACTORY FUNCTIONS ---


def get_default_customer_tree() -> Node:
    """Returns the default behavior tree for a customer agent."""
    return Sequence(
        name="customer_root",
        children=[
            ArriveNode(name="arrive"),
            QueueDecisionNode(name="decide_queue", queue_threshold=5),
            OrderDecisionNode(name="choose_menu"),
        ],
    )


# --- SALABIM COMPONENTS ---


class Customer(sim.Component):
    """
    Active customer component driving its own fulfillment lifecycle.
    """

    def setup(self, agent_data: BaseCustomer):
        self.agent_data = agent_data

    def process(self):
        # 1. Arrival
        yield self.hold(sim.Exponential(1).sample())

        # 2. Ordering
        yield self.request(self.env.kiosks)
        yield self.hold(sim.Uniform(1, 3).sample())
        self.release()

        # Notify staff that an order is placed
        self.env.orders.append(self)
        self.env.order_available_signal.set(True)

        # 3. Waiting for Food (from Holding Cabinet)
        # In this simplified model, customers pull from the cabinet
        yield self.from_store(self.env.holding_cabinet)

        # 4. Consumption
        yield self.hold(sim.Uniform(5, 15).sample())

        # 5. Exit
        pass
