import salabim as sim
from predictive_poultry_systems.agents.customers.behavior import Customer
from predictive_poultry_systems.agents.staff.behavior import Staff
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


class AgentGenerator(sim.Component):
    """Component to spawn behavioral agents (customers) over time."""

    def process(self):
        while True:
            # Create a mock customer
            customer_data = BaseCustomer(
                segment=CustomerSegment(
                    name=CustomerSegmentTypes.MILENNIALS,
                    profile="Generic profile",
                    preferences="Generic preferences",
                ),
                satisfaction=5.0,
                price_sensitivity=0.5,
                promo_sensitivity=0.5,
                loyalty=CustomerLoyalty(
                    level=CustomerLoyaltyLevel.LOYAL,
                    rfm=CustomerRFMProfile(recency=3, frequency=3, monetary=3),
                ),
                root_node=get_default_customer_tree(),
            )

            # Spawn the customer component in the simulation
            Customer(name=f"Customer.{self.env.now()}", agent_data=customer_data)

            # Wait for next arrival (simulated fixed rate for now)
            yield self.hold(sim.Exponential(10).sample())


def run_simulation(till: int = 100):
    """
    Initialize and run the poultry fulfillment node simulation with behavioral agents.
    """
    env = sim.Environment(trace=True, yieldless=False)

    # Initialize Physical Resources
    env.kiosks = sim.Resource("Kiosks", capacity=2)
    env.fryers = sim.Resource("Fryers", capacity=3)

    # Initialize Operational Stores
    env.holding_cabinet = sim.Store("HoldingCabinet", capacity=20)

    # Initialize Signals
    env.order_available_signal = sim.State("OrderAvailable", value=False)
    env.orders = []  # Shared list for simplicity in this phase

    # Initialize Staff
    for i in range(2):
        staff_data = BaseStaff(
            name=f"Staff_{i}",
            role=StaffRoles.FRY_COOK,
            hourly_wage=15.0,
            skill_level=1.0,
            fatigue_rate=0.01,
            shift_hours=8.0,
            root_node=get_default_staff_tree(),
        )
        Staff(name=f"Staff.{i}", agent_data=staff_data)

    # Initialize Customer Generator
    AgentGenerator()

    env.run(till=till)
    return env


def main():
    run_simulation(till=100)


if __name__ == "__main__":
    main()
