# BunkerOrder Domain DTOs

## Purpose
Provides strongly-typed data transfer structures for bunker order lifecycle operations, including CRUD payloads, cost calculations, invoice line items, email notifications, and approval workflows.

## Business Responsibility
Owns the contract for bunker order data shaping across the domain layer. These DTOs decouple internal domain entities from UI/API consumers and business handlers, carrying computed financials (`ActualTotalCostInUSD`), ownership tracking (`OwnedBy`/`PaidBy`), emissions factors, and nested invoice/line-item graphs. Critical for accurate cost aggregation, approval routing, and external system synchronization.

---

## Members

### 1. Status — Default lifecycle state
```csharp
public string Status { get; set; } = BunkerOrderStatusEnum.Draft.ToString();
```
**Explanation**: Sets the initial status for any newly instantiated bunker order. Prevents null references in downstream handlers that check state. If skipped, status remains null until explicitly assigned, causing potential validation failures or missing data in list views.

### 2. ActualQuantity — Resolved quantity for billing
```csharp
public decimal ActualQuantity => ActuallyReceivedQuantity ?? BunkerDeliveryNoteQuantity ?? RequestedQuantity;
```
**Explanation**: Falls back through receipt data sources in priority order (official delivery note > request) to determine the definitive quantity for cost calculations. Ensures downstream financial steps always operate on a non-null quantity, even if only requested quantities are available.

### 3. ActualTotalCostInUSD — Finalized USD cost for the line item
```csharp
public decimal ActualTotalCostInUSD =>
    ApprovedTotalCostInUSD
    ?? (ActuallyReceivedQuantity.HasValue
        ? ActualQuantity * TotalCostPerMetricTonsInUSD
        : TotalCostInUSD);
```
**Explanation**: Prioritizes the explicitly approved amount first. If unapproved, computes total by multiplying the resolved `ActualQuantity` by the unit rate when receipt data exists; otherwise falls back to the pre-calculated `TotalCostInUSD`. Prevents double-counting or stale estimates from affecting final approval totals.

### 4. ActualAvgUnitPriceInUSD — Derived unit price based on actuals or approval
```csharp
public decimal ActualAvgUnitPriceInUSD =>
    ActuallyReceivedQuantity.HasValue && !ApprovedTotalCostInUSD.HasValue
        ? TotalCostPerMetricTonsInUSD
        : ActualQuantity > 0
            ? ActualTotalCostInUSD / ActualQuantity
            : 0;
```
**Explanation**: Returns the unit rate directly if receipt data exists and no approval override is present. Otherwise calculates the true average price from the resolved total cost divided by actual quantity. Returns zero to avoid division-by-zero errors when quantity is zero. Critical for rate reconciliation in reporting.

### 5. PaidBy / OwnedBy — Ownership & payment responsibility assignment
```csharp
[EnumDataType(typeof(BunkerOrderResponsibilityEnum))]
public string? PaidBy { get; set; } = BunkerOrderResponsibilityEnum.Operator.ToString();

[EnumDataType(typeof(BunkerOrderResponsibilityEnum))]
public string? OwnedBy { get; set; } = BunkerOrderResponsibilityEnum.Operator.ToString();
```
**Explanation**: Enforces domain-constrained values for billing and ownership allocation using enum data annotations. Defaults to `Operator` to ensure audit trails and cost allocation handlers always have a valid responsibility target, preventing null reference exceptions during ownership transfer or approval workflows.

### 6. BioBlendOptions / OwnershipChangeLogs — Unmapped data transfer containers
```csharp
public List<BioBlendOptionDataStruct>? BioBlendOptions { get; set; }
public List<BunkerOwnershipChangeLog>? OwnershipChangeLogs { get; set; }
```
**Explanation**: Explicitly marked as non-DB-mapped. `BioBlendOptions` carries optional bio-fuel blending parameters for downstream calculation or UI display. `OwnershipChangeLogs` captures historical ownership transfers for audit/reconciliation. Loaded by business handlers that enrich the DTO after persistence, bypassing EF Core mapping constraints.

---

## Dependencies
- `BaseDto` — Shared identifier, audit, and concurrency metadata base class for all bunker order structures.
- `BunkerOrderStatusEnum` — Provides the canonical string representation for initial status assignment.
- `BunkerOrderResponsibilityEnum` / `FreightTypeEnum` — Enum types used for data annotation validation and default value assignment.
- `BunkerInvoiceDto`, `BunkerInvoiceItemDto`, `VesselRotationItem`, `BaseIteneraryItemDto` — Nested/related DTOs required to maintain referential integrity and graph completeness in single DTO payloads.
- `Core.Domain.BunkerOrder` namespace context — Houses domain constants and shared type definitions used across caller handlers.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]