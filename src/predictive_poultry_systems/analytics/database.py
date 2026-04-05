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
        config_json = json.dumps(config) if config else None
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

    def close(self) -> None:
        """Closes the database connection."""
        self.conn.close()
