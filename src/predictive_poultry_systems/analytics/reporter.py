def generate_fulfillment_audit(env):
    """
    Aggregates statistics from salabim monitors and prints a human-readable performance report.
    """
    manager = getattr(env, "fulfillment_manager", None)
    if not manager:
        print("\n[Audit Error] FulfillmentManager not found in environment.")
        return

    print("\n" + "=" * 50)
    print("       🐔 FULFILLMENT AUDIT REPORT 🐔")
    print("=" * 50)

    # 1. Throughput Calculation
    # Assuming till time is in minutes, throughput = (n_orders / till) * 60 (orders per hour)
    n_orders = manager.sos_monitor.number_of_entries()
    sim_time_h = env.now() / 60.0
    throughput = n_orders / sim_time_h if sim_time_h > 0 else 0

    print(f"Total Fulfillment Cycles: {n_orders}")
    print(f"System Throughput:        {throughput:.2f} units/hour")
    print("-" * 50)

    # 2. Performance Metrics
    print("KPI Breakdowns:")

    # Revenue (Level Monitor)
    print("\nRevenue ($):")
    print(f"  Total: {manager.revenue_monitor.get():.2f}")

    # Speed of Service
    print("\nSpeed of Service (SoS):")
    if n_orders > 0:
        print(f"  Mean:  {manager.sos_monitor.mean():.2f} min")
        print(f"  Std:   {manager.sos_monitor.std():.2f} min")
        print("Distribution:")
        manager.sos_monitor.print_histogram()
    else:
        print("  No data recorded.")

    # Customer Satisfaction
    print("\nCustomer Satisfaction Index (CSI):")
    print(f"  Current: {manager.satisfaction_monitor.get():.2f} / 10.0")
    print(f"  Mean:    {manager.satisfaction_monitor.mean():.2f}")

    # Staff Morale
    print("\nStaff Morale Index (SMI):")
    print(f"  Current: {manager.morale_monitor.get():.2f} / 10.0")
    print(f"  Mean:    {manager.morale_monitor.mean():.2f}")

    # 3. Thermodynamic Compliance
    print("-" * 50)
    print("Thermodynamic Summary (Crisp-state):")
    crisp_monitor = getattr(manager, "crispness_monitor", None)
    if crisp_monitor and crisp_monitor.number_of_entries() > 0:
        print(f"  Avg Crispness Score: {crisp_monitor.mean():.4f} (Ideal = 1.0)")
    else:
        print("  Crispness data not yet integrated.")

    print("=" * 50 + "\n")
