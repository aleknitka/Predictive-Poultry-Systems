from main import run_simulation


def test_simulation_reaches_till_value():
    till_value = 100
    env = run_simulation(till=till_value)
    assert env.now() == till_value
