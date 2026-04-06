# Economic & Management Design: ECONOMIC_DESIGN.md

## Overview
This document defines the mathematical business models and technical implementation strategies for simulating the management and economic operations of a poultry fast-food restaurant (Predictive Poultry Systems). The focus is entirely on financial modeling, inventory logistics, and labor scheduling.

## 1. Business & Economic Models

### 1.1 Profit and Loss (P&L) Ledger
The simulation's core economic engine is a double-entry ledger that tracks profitability in real-time.
- **Revenue ($R$)**: Generated stochastically based on customer orders.
- **Cost of Goods Sold (COGS)**: Calculated upon order fulfillment (e.g., cost of raw chicken + cost of oil consumed).
- **Labor Costs ($L$)**: Calculated hourly based on active staff shifts, including overtime multipliers.
- **Gross Margin**: $R - COGS$
- **Net Operating Income**: $R - (COGS + L + Overhead)$

### 1.2 Inventory Logistics & Spoilage
Raw materials degrade over simulation time if not stored or used correctly.
- **Spoilage Model**: Modeled as a simple discrete step function where items exceeding their `shelf_life_hours` must be discarded (logging a write-off expense to the ledger).
- **Reorder Points**: When `current_inventory < reorder_threshold`, a supply delivery event is scheduled. Deliveries incur a fixed transport cost plus variable item costs.

### 1.3 Labor Scheduling & Fatigue Economics
Labor is the primary variable expense. Staff productivity and costs fluctuate over time.
- **Wage Multipliers**: $W_t = W_{base} \times (1.5 \text{ if } t > 8 \text{ hours else } 1.0)$
- **Fatigue Economics**: As staff fatigue increases (from Phase 3 behaviors), processing times increase, lowering throughput and causing potential revenue loss due to customer balking.

## 2. Technical Data Structures

### 2.1 Physics-Informed Business Assets (Pydantic)
```python
from pydantic import BaseModel
from datetime import datetime

class LedgerTransaction(BaseModel):
    transaction_id: str
    timestamp: float # Simulation time
    category: str # 'REVENUE', 'COGS', 'LABOR', 'WASTE'
    amount: float
    description: str

class InventoryItem(BaseModel):
    item_id: str
    cost_basis: float
    received_at: float
    shelf_life_hours: float
```

### 2.2 Manager Interfaces
- `LedgerManager`: Exposes `post_transaction(category, amount, description)`.
- `InventoryManager`: Evaluates spoilage every $X$ simulation hours and triggers supply events.

## 3. Solver Implementation

### 3.1 End-of-Day Reconciliation
Unlike continuous thermodynamic physics, the economic solver runs on a discrete pulse (e.g., `sim.hold(24 * 60)`). At the end of the day, it aggregates the `LedgerTransaction` objects, applies overhead costs, and generates a daily P&L statement.

## 4. Requirement Mapping
- **STRAT-02**: "Technical design for custom business and management logic." -> Fully satisfied by this specification.
