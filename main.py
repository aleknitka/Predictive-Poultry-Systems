import salabim as sim
from predictive_poultry_systems.agents.simulation import (
    CustomerComponent,
    StaffComponent,
)
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
            CustomerComponent(
                name=f"Customer.{self.env.now()}", agent_data=customer_data
            )

            # Wait for next arrival (simulated fixed rate for now)
            yield self.hold(sim.Uniform(5, 15).sample())


def run_simulation(till: int = 100):
    """
    Initialize and run the poultry fulfillment node simulation with behavioral agents.
    """
    env = sim.Environment(trace=True, yieldless=False)

    # Initialize Staff
    staff_data = BaseStaff(
        name="Staff_1",
        role=StaffRoles.FRY_COOK,
        hourly_wage=15.0,
        skill_level=1.0,
        fatigue_rate=0.01,
        shift_hours=8.0,
        root_node=get_default_staff_tree(),
    )
    StaffComponent(name="Staff.1", agent_data=staff_data)

    # Initialize Customer Generator
    AgentGenerator()

    env.run(till=till)
    return env


def main():
    run_simulation(till=50)


if __name__ == "__main__":
    main()
