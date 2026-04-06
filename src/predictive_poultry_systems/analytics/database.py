import sqlite3
import json
from typing import Optional, Any
from loguru import logger


class DatabaseManager:
    """Manages SQLite database for simulation metrics with WAL mode performance."""

    def __init__(self, db_path: str):
        """Initializes the database connection and schema.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        # Performance optimization for real-time writes
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA synchronous = NORMAL;")

        self._init_schema()

    def _init_schema(self) -> None:
        """Creates the normalized relational schema if it doesn't exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    seed INTEGER,
                    config_json TEXT
                );
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS simulation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    sim_time REAL,
                    level TEXT,
                    message TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                );
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS resource_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    sim_time REAL,
                    resource_name TEXT,
                    available INTEGER,
                    claimed INTEGER,
                    queue_len INTEGER,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                );
            """)

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS kpi_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    sim_time REAL,
                    metric_name TEXT,
                    value REAL,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                );
            """)

            # Performance Indexes
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_sim_logs_run ON simulation_logs(run_id)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_resource_run ON resource_metrics(run_id)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_kpi_run ON kpi_metrics(run_id)"
            )
        logger.info(f"Database schema initialized at {self.db_path}")

    def create_run(
        self, seed: Optional[int] = None, config: Optional[dict[str, Any]] = None
    ) -> int:
        """Creates a new simulation run entry.

        Args:
            seed: The random seed used for the simulation.
            config: A dictionary representing the simulation configuration.

        Returns:
            The unique run_id for this simulation.
        """
        config_json = json.dumps(config, default=str) if config else None
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO runs (seed, config_json) VALUES (?, ?)",
                (seed, config_json),
            )
            run_id = cursor.lastrowid
        if run_id is None:
            raise RuntimeError("Failed to create a new simulation run.")
        logger.info(f"Created new simulation run with ID: {run_id}")
        return run_id

    def log_event(self, run_id: int, sim_time: float, level: str, message: str) -> None:
        """Logs a simulation event to the database.

        Args:
            run_id: The ID of the current simulation run.
            sim_time: The simulation time at which the event occurred.
            level: The log level of the event.
            message: The event message.
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO simulation_logs (run_id, sim_time, level, message) VALUES (?, ?, ?, ?)",
                (run_id, sim_time, level, message),
            )

    def log_resource(
        self,
        run_id: int,
        sim_time: float,
        name: str,
        avail: int,
        claimed: int,
        queue: int,
    ) -> None:
        """Logs resource usage metrics to the database.

        Args:
            run_id: The ID of the current simulation run.
            sim_time: The simulation time at which the metrics were sampled.
            name: The name of the resource.
            avail: The number of available units of the resource.
            claimed: The number of claimed units of the resource.
            queue: The number of units in the resource's queue.
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO resource_metrics (run_id, sim_time, resource_name, available, claimed, queue_len) VALUES (?, ?, ?, ?, ?, ?)",
                (run_id, sim_time, name, avail, claimed, queue),
            )

    def log_kpi(self, run_id: int, sim_time: float, name: str, value: float) -> None:
        """Logs a KPI metric to the database.

        Args:
            run_id: The ID of the current simulation run.
            sim_time: The simulation time at which the KPI was sampled.
            name: The name of the KPI.
            value: The value of the KPI.
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO kpi_metrics (run_id, sim_time, metric_name, value) VALUES (?, ?, ?, ?)",
                (run_id, sim_time, name, value),
            )

    def close(self) -> None:
        """Closes the database connection."""
        self.conn.close()
