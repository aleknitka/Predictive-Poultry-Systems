# Custom Simulation Engine: ENGINE_REQUIREMENTS.md

## Overview
This document specifies the requirements for a domain-specific simulation engine (or an architectural layer on top of `salabim`) tailored for the **economic and management operations** of a poultry fast-food restaurant (Predictive Poultry Systems).

The goal is to move beyond simple event queueing and introduce robust business logic, financial modeling, and resource management.

## 1. Core Engine Specifications

### 1.1 Functional Requirements
- **Financial Ledger**: A double-entry accounting system to track revenue, COGS (Cost of Goods Sold), labor costs, and overhead in real-time.
- **Inventory Management**: Continuous tracking of raw materials (chicken, oil, packaging) with automated reorder points and spoilage/waste modeling.
- **Labor Scheduling**: Shift management logic that handles staff fatigue, breaks, overtime costs, and dynamic routing based on store traffic.
- **Demand Generation**: Marketing and local event models that inject stochastic bursts of customer arrivals.

### 1.2 Non-Functional Requirements
- **Scalability**: The engine must support multi-day or multi-month simulations (e.g., simulating a full fiscal quarter) in seconds.
- **Extensibility**: Easy API to add new menu items, adjust pricing strategies, or change supplier costs.

## 2. Technical Architecture

### 2.1 Interface Definitions
- **Ledger**: Tracks all transactions. Every simulation event (e.g., selling a meal, paying a worker) posts to the ledger.
- **InventoryStore**: An extension of `sim.Store` that handles perishability and bulk deliveries.
- **ShiftManager**: Orchestrates staff availability and assignment based on economic constraints.

### 2.2 System Architecture Diagram
```mermaid
graph TD
    A[Simulation Loop (Salabim)] --> B[Event: Customer Order]
    B --> C[FulfillmentManager]
    C --> D[InventoryStore: Deduct Stock]
    C --> E[Ledger: Record Revenue]
    C --> F[Ledger: Record COGS]
    G[Time Event: Shift End] --> H[ShiftManager]
    H --> I[Ledger: Record Labor Cost]
```

## 3. Requirement Mapping
- **STRAT-01**: "Implement custom domain-specific simulation engine tailored to management and economics." -> Fully satisfied by this specification.
