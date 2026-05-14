# BunkerOverviewDto, BunkerOrderReducedDto, BunkerOrderDto, VesselBunkerDeliveryDto, BunkerOrderWithItemsReducedDto

## Purpose
These classes define the read-side projection contracts for bunker voyage data. They exist to serialize domain aggregates into flat, UI-friendly payloads that eliminate N+1 database queries and circular reference serialization issues.

## Business Responsibility
Owns the data shape for bunker overview screens and order/delivery list views. Critical for read-performance: consumers (`GetBunkerOverviewByVoyageId`, `VoyageController`) rely on these DTOs to render port sequences, fuel lots, order summaries, and delivery transactions in single API responses without domain traversal.

---
IF DOMAIN/DTO:

## Members
*Note: All properties are simple auto-properties mapped directly to JSON serialization. Business meaning is derived from aggregate composition and denormalized fields.*

### 1. BunkerOverviewDto — Composite read-side projection container
```csharp
public List<MinimalPortDto> Ports { get; set; } = [];
public List<BunkerLotBaseDto> BunkerLots { get; set; } = [];
public List<BunkerOrderWithItemsReducedDto> BunkerOrders { get; set; } = [];
public List<BaseIteneraryItemDto> ItineraryItems { get; set; } = [];
public List<VesselBunkerDeliveryDto> VesselBunkerDeliveries { get; set; } = [];
```
**Explanation**: Bundles five distinct read-model aggregates into one serializable object. Eliminates round-trips by delivering all voyage-related bunker context in a single payload for the overview UI.

### 2. BunkerOrderDto — Full bunker order projection
```csharp
public string? PortName { get; set; }
public string? OrderCode { get; set; }
public Guid? VoyageId { get; set; }
public string? VoyageNo { get; set; }
public Guid? PortId { get; set; }
public Guid? VoyageIteneraryItemId { get; set; }
public string? Status { get; set; }
public string? VesselName { get; set; }
public decimal? TotalRequestedQuantity { get; set; }
public decimal? TotalActuallyReceivedQuantity { get; set; }
public decimal? TotalEstimateAmountUSD { get; set; }
public decimal? TotalInvoiceAmountUSD { get; set; }
public Guid? AgentId { get; set; }
public string? AgentName { get; set; }
public Guid? BrokerId { get; set; }
public string? BrokerName { get; set; }
public string? BunkerTypes { get; set; }
public List<TagDto> Tags { get; set; } = [];
```
**Explanation**: Denormalized order payload carrying financial summaries and pre-joined reference data. `TotalRequestedQuantity` and `TotalActuallyReceivedQuantity` enable consumption tracking. `TotalEstimateAmountUSD` and `TotalInvoiceAmountUSD` provide direct ledger values for reporting. Reference fields (`PortName`, `VesselName`, `AgentName`, `BrokerName`, `BunkerTypes`) bypass domain lookups during grid rendering.

### 3. BunkerOrderReducedDto & BunkerOrderWithItemsReducedDto — Lightweight order identifiers
```csharp
public Guid? Id { get; set; }
public string? OrderCode { get; set; }
public Guid? VoyageId { get; set; }
public Guid? PortId { get; set; }
public Guid? VoyageIteneraryItemId { get; set; }
public string? Status { get; set; }
public DateTime? ModifiedOn { get; set; }
```
**Explanation**: Stripped order records optimized for list views, dropdowns, and routing. `BunkerOrderWithItemsReducedDto` extends this by attaching `Items`, enabling detail expansion without loading full order graphs. `Status` and `ModifiedOn` drive client-side sorting and filtering.

### 4. VesselBunkerDeliveryDto — Delivery transaction record
```csharp
public Guid? Id { get; set; }
public string? BunkerTypeCode { get; set; }
public Guid? BunkerLotId { get; set; }
public string? BunkerLotCode { get; set; }
public Guid? PortId { get; set; }
public string? PortName { get; set; }
public DateTime? ReportDate { get; set; }
public decimal? PricePerMetricTonInUsd { get; set; }
public decimal? QuantityInMetricTons { get; set; }
public decimal? ValueUsd { get; set; }
public DateTime? LastUpdate { get; set; }
```
**Explanation**: Represents a single fuel delivery transaction. Maps directly to ledger/reporting outputs via `ValueUsd` (price × quantity), `ReportDate`, and lot/port references. Used for consumption tracking, invoice reconciliation, and delivery confirmation workflows.

---
IF DOMAIN/DTO:

## Dependencies
- `BaseDto` — Inherited by `BunkerOrderDto` for common audit/metadata properties (e.g., base `Id`, timestamps).
- `MinimalPortDto`, `BunkerLotBaseDto`, `BaseIteneraryItemDto`, `TagDto`, `BunkerOrderItemDto` — Referenced via collection properties to enable composite serialization without circular references or deep entity traversal during projection.

---
IF DOMAIN/DTO:

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]