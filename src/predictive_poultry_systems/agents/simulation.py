import salabim as sim
from typing import Union, List, Any
from .customers.base import BaseCustomer
from .staff.base import BaseStaff
from .behavior.bt.base import Status


class FulfillmentManager(sim.Component):
    """
    Centralized orchestrator for order tracking and performance monitoring.
    """

    def setup(self):
        self.orders: List[Any] = []
        self.order_available_signal = sim.State("OrderAvailable", value=False)

        # Performance Monitors
        self.revenue_monitor = sim.Monitor("Revenue", level=True)
        self.sos_monitor = sim.Monitor("Speed of Service")
        self.satisfaction_monitor = sim.Monitor("Customer Satisfaction", level=True)
        self.morale_monitor = sim.Monitor("Staff Morale", level=True)
        self.crispness_monitor = sim.Monitor("Crisp-state Compliance")

        # Initialize level monitors
        self.revenue_monitor.tally(0)
        self.satisfaction_monitor.tally(10.0)  # Start at max
        self.morale_monitor.tally(10.0)  # Start at max

    def add_order(self, customer: sim.Component):
        self.orders.append(customer)
        self.order_available_signal.set(True)

    def pop_order(self) -> Any:
        if not self.orders:
            return None
        order = self.orders.pop(0)
        if not self.orders:
            self.order_available_signal.set(False)
        return order

    def tally_revenue(self, amount: float):
        """Increments the total revenue."""
        current = self.revenue_monitor.get()
        self.revenue_monitor.tally(current + amount)

    def record_sos(self, duration: float):
        """Records a completed speed of service (SoS)."""
        self.sos_monitor.tally(duration)

    def update_satisfaction(self, value: float):
        """Updates the current aggregate customer satisfaction."""
        self.satisfaction_monitor.tally(value)

    def update_morale(self, value: float):
        """Updates the current aggregate staff morale."""
        self.morale_monitor.tally(value)

    def tally_crispness(self, value: float):
        """Records the crispness score of a finished product."""
        self.crispness_monitor.tally(value)


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
