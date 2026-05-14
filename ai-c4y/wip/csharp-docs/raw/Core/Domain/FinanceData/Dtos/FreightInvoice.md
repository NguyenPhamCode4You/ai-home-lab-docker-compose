# FreightInvoicePercentageReducedDto

## Purpose
Represents a financial data transfer object for freight invoices that have been adjusted or reduced by a calculated percentage. Used to propagate reduction metadata and final amounts across domain services, application handlers, and UI presentation layers without leaking entity internals.

## Business Responsibility
Owns the contract for reduced invoice line items during voyage cost reconciliation and financial audit pipelines. Critical for accurate freight cost finalization, as it preserves the delta between original billed amounts and approved reductions. Consumed directly by AutoMapper mapping profiles and shipment cost aggregators; changes to its shape directly impact list views and finance reporting outputs.

---
## Members

### 1. Currency — Default financial denomination for invoice line
```csharp
public string Currency { get; set; } = CurrencyCodeEnum.USD.ToString();
```
**Explanation**: Enforces a domain-standard USD fallback when no currency is explicitly resolved during mapping or DTO initialization. Prevents downstream monetary aggregation failures in voyage cost calculations by guaranteeing a non-null currency string. All other properties (`ShipmentId`, `InvoiceId`, `Type`, `Status`, `InvoiceDate`, etc.) are standard structural/metadata fields consumed directly by mappers and UI grids without transformation or conditional logic.

---
## Dependencies
`BaseDto` — provides shared lifecycle tracking (e.g., `Id`, `CreatedAt`) expected by domain repositories, mapper configurations, and audit pipelines.
`CurrencyCodeEnum` — referenced in the default initializer to enforce domain-standard currency string conventions and prevent validation gaps in financial aggregations.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]