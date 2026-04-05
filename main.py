import salabim as sim
from loguru import logger
from predictive_poultry_systems.agents.customers.behavior import Customer
from predictive_poultry_systems.agents.staff.behavior import Staff
from predictive_poultry_systems.agents.staff.base import StaffRoles
from predictive_poultry_systems.agents.factories import (
    create_customer_data,
    create_staff_data,
)
from predictive_poultry_systems.agents.simulation import FulfillmentManager
from predictive_poultry_systems.analytics.reporter import generate_fulfillment_audit
from predictive_poultry_systems.analytics.database import DatabaseManager
from predictive_poultry_systems.analytics.logging import setup_simulation_logger
from predictive_poultry_systems.analytics.sinks import MetricSink
from predictive_poultry_systems.config import DEFAULT_DB_PATH


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


def run_simulation(till: int = 100, seed: int = 42):
    """
    Initialize and run the poultry fulfillment node simulation with behavioral agents.
    """
    # Initialize Database and Run Metadata
    db = DatabaseManager(DEFAULT_DB_PATH)
    try:
        run_id = db.create_run(seed=seed)

        # Initialize Salabim Environment
        env = sim.Environment(trace=False, yieldless=False, random_seed=seed)
        setup_simulation_logger(env)

        # Add a loguru sink to persist all simulation logs to SQLite
        def db_log_sink(message):
            record = message.record
            db.log_event(
                run_id=run_id,
                sim_time=record["extra"].get("sim_time", env.now()),
                level=record["level"].name,
                message=record["message"],
            )

        db_sink_id = logger.add(db_log_sink, level="INFO")

        # Initialize Physical Resources
        env.kiosks = sim.Resource("Kiosks", capacity=2)
        env.fryers = sim.Resource("Fryers", capacity=3)

        # Initialize Operational Stores
        env.holding_cabinet = sim.Store("HoldingCabinet", capacity=20)

        # Initialize Managers
        env.fulfillment_manager = FulfillmentManager()

        # Initialize Metric Sink for periodic monitor persistence
        MetricSink(db=db, run_id=run_id, interval=5.0)

        # Initialize Staff using factory
        for i in range(2):
            staff_data = create_staff_data(name=f"Staff_{i}", role=StaffRoles.FRY_COOK)
            Staff(name=f"Staff.{i}", agent_data=staff_data)

        # Initialize Customer Generator
        AgentGenerator()

        logger.info(f"Starting simulation run {run_id} till {till}...")
        env.run(till=till)

        # Generate Performance Audit
        generate_fulfillment_audit(env)
        logger.info(f"Simulation run {run_id} completed.")

    finally:
        # Cleanup sinks and close database
        logger.remove(db_sink_id)
        db.close()

    return env


def main():
    run_simulation(till=200)


if __name__ == "__main__":
    main()
