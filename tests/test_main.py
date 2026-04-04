from main import run_simulation


def test_simulation_reaches_till_value():
    till_value = 100
    env = run_simulation(till=till_value)
    assert env.now() == till_value


def test_full_simulation_cycle():
    """
    Verifies that the end-to-end cycle (Arrival -> Ordering -> Cooking -> Delivery) works.
    """
    till_value = 500  # Run long enough to ensure multiple cycles
    env = run_simulation(till=till_value)

    # Verify that customers entered and left the system

    # 1. Verify Kiosks were used
    assert env.kiosks.claimers().number_of_arrivals > 0

    # 2. Verify Fryers were used
    assert env.fryers.claimers().number_of_arrivals > 0

    # 3. Verify Holding Cabinet was used
    # Items enter when Staff finishes cooking, leave when Customer picks up
    assert env.holding_cabinet.number_of_arrivals > 0
    assert env.holding_cabinet.number_of_departures > 0

    # 4. Verify that time progressed
    assert env.now() == till_value
