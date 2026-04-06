import salabim as sim
import math
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from .database import DatabaseManager


class MetricSink(sim.Component):
    """Salabim component that periodically samples monitors and persists to DB."""

    def setup(self, db: "DatabaseManager", run_id: int, interval: float = 5.0):
        """Initializes the metric sink.

        Args:
            db: The DatabaseManager instance.
            run_id: The ID of the current simulation run.
            interval: Sampling interval in simulation time units.
        """
        self.db = db
        self.run_id = run_id
        self.interval = interval

    def process(self):
        """Main sampling loop."""
        while True:
            yield self.hold(self.interval)
            try:
                self._sample_resources()
                self._sample_kpis()
            except Exception as e:
                logger.error(f"Error in MetricSink: {e}")

    def _sample_resources(self):
        """Samples resource levels and queue lengths."""
        env = self.env

        # Store: holding_cabinet
        # Note: Must check 'is not None' because empty Store/Queue evaluates to False
        hc = getattr(env, "holding_cabinet", None)
        if hc is not None:
            self.db.log_resource(
                run_id=self.run_id,
                sim_time=env.now(),
                name="holding_cabinet",
                avail=int(hc.capacity() - len(hc)),
                claimed=len(hc),
                queue=len(hc.from_store_requesters()),
            )

        # Resources: kiosks, fryers
        for res_name in ["kiosks", "fryers"]:
            res = getattr(env, res_name, None)
            if res is not None:
                self.db.log_resource(
                    run_id=self.run_id,
                    sim_time=env.now(),
                    name=res_name,
                    avail=int(res.available_quantity()),
                    claimed=int(res.claimed_quantity()),
                    queue=len(res.requesters()),
                )

    def _sample_kpis(self):
        """Samples KPI monitors from the fulfillment manager."""
        fm = getattr(self.env, "fulfillment_manager", None)
        if fm is None:
            return

        # Map of internal monitor names to the names we want in DB
        kpi_map = {
            "satisfaction_monitor": "CSI",
            "morale_monitor": "SMI",
            "revenue_monitor": "Revenue",
            "sos_monitor": "SoS",
        }

        for monitor_attr, kpi_name in kpi_map.items():
            monitor = getattr(fm, monitor_attr, None)
            if monitor is not None:
                # Use duck typing: level monitors support .get(), others support .mean()
                try:
                    value = monitor.get()
                except (AttributeError, TypeError):
                    value = monitor.mean()

                # Handle cases where no data has been collected yet (NaN)
                if math.isnan(value):
                    value = 0.0
                self.db.log_kpi(
                    run_id=self.run_id,
                    sim_time=self.env.now(),
                    name=kpi_name,
                    value=float(value),
                )
