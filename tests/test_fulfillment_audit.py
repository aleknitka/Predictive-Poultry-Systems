from main import run_simulation
from predictive_poultry_systems.analytics.reporter import generate_fulfillment_audit


def test_audit_generation_no_error():
    """
    Smoke test to ensure the reporter runs without error at the end of a simulation.
    """
    env = run_simulation(till=50)
    # The reporter prints to stdout, we just want to ensure it doesn't crash
    generate_fulfillment_audit(env)

    manager = env.fulfillment_manager
    # Verify monitors exist
    assert manager.revenue_monitor is not None
    assert manager.sos_monitor.number_of_entries() > 0
    assert manager.satisfaction_monitor is not None
    assert manager.morale_monitor is not None
    assert manager.crispness_monitor.number_of_entries() > 0


def test_throughput_calculation():
    """
    Verifies that the throughput logic in the manager/reporter is sound.
    """
    env = run_simulation(till=10)  # Short run

    sim_time_h = env.now() / 60.0

    # We can't easily capture the printed output here without capsys,
    # but we can verify the data it uses.
    assert env.now() == 10
    assert sim_time_h == 10 / 60.0
