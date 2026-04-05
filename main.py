import salabim as sim
from predictive_poultry_systems.agents.customers.behavior import Customer
from predictive_poultry_systems.agents.staff.behavior import Staff
from predictive_poultry_systems.agents.staff.base import StaffRoles
from predictive_poultry_systems.agents.factories import (
    create_customer_data,
    create_staff_data,
)
from predictive_poultry_systems.agents.simulation import FulfillmentManager
from predictive_poultry_systems.analytics.reporter import generate_fulfillment_audit


class AgentGenerator(sim.Component):
    """Component to spawn behavioral agents (customers) over time."""

    def process(self):
        while True:
            # Create a mock customer using factory
            customer_data = create_customer_data()

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

    # Initialize Managers
    env.fulfillment_manager = FulfillmentManager()

    # Initialize Staff using factory
    for i in range(2):
        staff_data = create_staff_data(name=f"Staff_{i}", role=StaffRoles.FRY_COOK)
        Staff(name=f"Staff.{i}", agent_data=staff_data)

    # Initialize Customer Generator
    AgentGenerator()

    env.run(till=till)

    # Generate Performance Audit
    generate_fulfillment_audit(env)

    return env


def main():
    run_simulation(till=200)


if __name__ == "__main__":
    main()
