from loguru import logger
from predictive_poultry_systems.config import MINUTES_PER_HOUR


def generate_fulfillment_audit(env):
    """
    Aggregates statistics from salabim monitors and logs a human-readable performance report.
    """
    manager = getattr(env, "fulfillment_manager", None)
    if not manager:
        logger.error("FulfillmentManager not found in environment.")
        return

    logger.info("=" * 50)
    logger.info("       🐔 FULFILLMENT AUDIT REPORT 🐔")
    logger.info("=" * 50)

    # 1. Throughput Calculation
    try:
        n_orders = manager.sos_monitor.number_of_entries()
    except (AttributeError, TypeError):
        n_orders = 0

    sim_time_h = env.now() / MINUTES_PER_HOUR
    throughput = (n_orders / sim_time_h) if sim_time_h > 0 else 0

    logger.info(f"Total Fulfillment Cycles: {n_orders}")
    logger.info(f"System Throughput:        {throughput:.2f} units/hour")
    logger.info("-" * 50)

    # 2. KPI Breakdowns
    logger.info("KPI Breakdowns:")

    # Revenue
    try:
        revenue = manager.revenue_monitor.get()
    except (AttributeError, TypeError):
        try:
            revenue = manager.revenue_monitor.mean()
        except (AttributeError, TypeError):
            revenue = 0.0
    logger.info(f"\nRevenue ($):\n  Total: {revenue:.2f}")

    # Speed of Service
    try:
        sos_mean = manager.sos_monitor.mean()
        sos_std = manager.sos_monitor.std()
    except (AttributeError, TypeError):
        sos_mean = 0.0
        sos_std = 0.0
    logger.info(
        f"\nSpeed of Service (SoS):\n  Mean:  {sos_mean:.2f} min\n  Std:   {sos_std:.2f} min"
    )

    # We log the SoS histogram info if available
    if n_orders > 0:
        logger.info("Distribution:")
        try:
            manager.sos_monitor.print_histogram()
        except (AttributeError, TypeError):
            pass

    # CSI
    try:
        csi_last = manager.satisfaction_monitor.get()
    except (AttributeError, TypeError):
        try:
            csi_last = manager.satisfaction_monitor.mean()
        except (AttributeError, TypeError):
            csi_last = 0.0

    try:
        csi_mean = manager.satisfaction_monitor.mean()
    except (AttributeError, TypeError):
        csi_mean = 0.0

    logger.info(
        f"\nCustomer Satisfaction Index (CSI):\n  Last: {csi_last:.2f} / 10.0\n  Mean: {csi_mean:.2f}"
    )

    # SMI
    try:
        smi_curr = manager.morale_monitor.get()
    except (AttributeError, TypeError):
        try:
            smi_curr = manager.morale_monitor.mean()
        except (AttributeError, TypeError):
            smi_curr = 0.0

    try:
        smi_mean = manager.morale_monitor.mean()
    except (AttributeError, TypeError):
        smi_mean = 0.0

    logger.info(
        f"\nStaff Morale Index (SMI):\n  Current: {smi_curr:.2f} / 10.0\n  Mean:    {smi_mean:.2f}"
    )

    logger.info("-" * 50)

    # 3. Thermodynamic State
    try:
        avg_crispness = manager.crispness_monitor.mean()
    except (AttributeError, TypeError):
        avg_crispness = 0.0
    logger.info(
        f"Thermodynamic Summary (Crisp-state):\n  Avg Crispness Score: {avg_crispness:.4f} (Ideal = 1.0)"
    )
    logger.info("=" * 50)
