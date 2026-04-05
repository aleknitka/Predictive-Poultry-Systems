import os
import sqlite3
import pytest
from main import run_simulation
from predictive_poultry_systems.config import DEFAULT_DB_PATH


@pytest.fixture
def clean_db():
    """Ensure we start with a clean database and clean up after."""
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)
    yield
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)


def test_persistence_end_to_end(clean_db):
    """Verifies that running a simulation populates the database correctly."""
    seed = 123
    till = 20

    # Run a short simulation
    run_simulation(till=till, seed=seed)

    # Verify database existence
    assert os.path.exists(DEFAULT_DB_PATH)

    # Connect and verify content
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Verify 'runs' table
    cursor.execute("SELECT * FROM runs")
    runs = cursor.fetchall()
    assert len(runs) == 1
    assert runs[0]["seed"] == seed
    assert runs[0]["start_timestamp"] is not None
    run_id = runs[0]["run_id"]

    # 2. Verify 'simulation_logs' table
    cursor.execute("SELECT * FROM simulation_logs WHERE run_id = ?", (run_id,))
    logs = cursor.fetchall()
    assert len(logs) > 0
    # Verify sim_time consistency
    last_time = -0.1
    for log in logs:
        assert log["sim_time"] >= last_time
        last_time = log["sim_time"]

    # 3. Verify 'resource_metrics' table (MetricSink should have triggered at t=5, 10, 15, 20)
    cursor.execute("SELECT * FROM resource_metrics WHERE run_id = ?", (run_id,))
    metrics = cursor.fetchall()
    assert len(metrics) > 0

    # Check if we have entries for kiosks and fryers
    resource_names = [m["resource_name"] for m in metrics]
    assert "kiosks" in resource_names
    assert "fryers" in resource_names
    assert "holding_cabinet" in resource_names

    # 4. Verify 'kpi_metrics' table
    cursor.execute("SELECT * FROM kpi_metrics WHERE run_id = ?", (run_id,))
    kpis = cursor.fetchall()
    assert len(kpis) > 0
    kpi_names = [k["metric_name"] for k in kpis]
    assert "Revenue" in kpi_names
    assert "SMI" in kpi_names

    conn.close()


def test_multiple_runs(clean_db):
    """Verifies that multiple runs are tracked separately in the database."""
    run_simulation(till=10, seed=1)
    run_simulation(till=10, seed=2)

    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM runs")
    count = cursor.fetchone()[0]
    assert count == 2

    conn.close()
