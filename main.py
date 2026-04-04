import salabim as sim


class SimulationManager(sim.Component):
    """
    Component to manage the lifecycle of the fulfillment node simulation.
    """

    def process(self):
        print("Fulfillment node simulation initializing...")
        # Placeholder for future agentic interactions
        yield self.hold(100)
        print("Simulation finished")


def run_simulation(till: int = 100):
    """
    Initialize and run the poultry fulfillment node simulation.
    """
    env = sim.Environment(trace=True, yieldless=False)
    SimulationManager()
    env.run(till=till)
    return env


def main():
    run_simulation()


if __name__ == "__main__":
    main()
