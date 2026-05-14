# BunkerOverviewSummaryDto

## Purpose
Aggregate DTO projecting voyage-level bunker data across three operational dimensions: type consumption, active orders, and physical lifting events. Exists to flatten CQRS read-model data into a single UI/API-ready payload.

## Business Responsibility
Owns the read-side projection for the bunker overview dashboard. Critical for voyage planning and cost tracking, as it consolidates forecasted quantities, actual lift receipts, and order statuses into one contract. Serves as the primary data contract for the `GetBunkerOverviewSummaryByVoyageId` workflow.

---

## Members
*(Note: All properties are flat auto-properties serving as direct projection targets. No computed fields, fallback chains, or domain logic present. Documented here for business mapping clarity.)*

### 1. BunkerTypeSummaries — Type-level consumption and pricing rollup
```csharp
public List<BunkerTypeSummaryDto> BunkerTypeSummaries { get; set; } = [];
```
**Explanation**: Collects per-fuel-type metrics across the voyage. Maps initial states (`InitialQty`, `InitialPrice`) through operational deltas (`TotalConsumption`, `ReceivedQty`) to current states (`EndQty`, `EndPrice`). Provides the financial and inventory backbone for bunkering cost analysis. Contains nested quantity breakdowns via `BunkerTypeQuantityDto`.

### 2. BunkerOrderSummaries — Active requisition tracking
```csharp
public List<BunkerOrderSummaryDto> BunkerOrderSummaries { get; set; } = [];
```
**Explanation**: Groups open/pending/finalized orders by port and itinerary item. Tracks requested vs. received quantities, order status lifecycle, and last update timestamp. Enables planners to audit request fulfillment and port-specific logistics. Maps directly to order request tables.

### 3. BunkerLiftingSummaries — Physical receipt events
```csharp
public List<BunkerLiftingSummaryDto> BunkerLiftingSummaries { get; set; } = [];
```
**Explanation**: Represents actual delivery events tied to itinerary stops. Links `PortId` and `ItineraryItemId` to confirmed `ReceivedQuantities` per fuel type. Used to reconcile order promises against physical stock changes and verify port execution accuracy.

## Dependencies
- `List<T>` — Standard collection used to flatten 1:N relational bunker data into a single JSON payload.
- `BunkerTypeSummaryDto`, `BunkerOrderSummaryDto`, `BunkerLiftingSummaryDto`, `BunkerTypeQuantityDto` — Direct projection targets; no cross-cutting dependencies or base classes used.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]