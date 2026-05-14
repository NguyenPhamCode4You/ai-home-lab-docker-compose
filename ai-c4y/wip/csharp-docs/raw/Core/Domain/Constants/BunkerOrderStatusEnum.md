# Bunker Constants

## Purpose
Defines strongly-typed enumeration values for bunker order lifecycle, payment calculation models, and invoice line items. Exists to replace magic numbers and strings in the domain layer with compile-safe, explicit state and value representations.

## Business Responsibility
Owns the canonical state machine for bunker orders, standardizes financial settlement logic, and categorizes fixed invoice line items. Critical for consistent order tracking, financial reporting accuracy, and UI/dashboard rendering across the BVMS platform. Errors or mismatches in these constants directly corrupt financial ledgers and order status dashboards.

---

## Members

### 1. `BunkerOrderStatusEnum` — Order lifecycle tracking
```csharp
Draft = 0, Inquiry = 1, Ordered = 2, Received = 3, Invoiced = 4, Paid = 5, Cancelled = 6
```
**Explanation**: Represents the strict progression of a bunker order from creation to financial closure. `Draft`/`Inquiry` indicate pre-contract phases. `Ordered` confirms procurement placement. `Received` triggers physical asset intake and quantity reconciliation. `Invoiced`/`Paid` mark financial settlement. `Cancelled` halts the lifecycle. Integer backing ensures deterministic sorting in queries and UI status filters.

### 2. `BunkerPaymentTypeEnum` — Payment calculation model
```csharp
LumpSum, PercentageOfCost, RatePerMT
```
**Explanation**: Defines how the bunker supplier or service provider is compensated. `LumpSum` applies a fixed fee regardless of volume. `PercentageOfCost` scales compensation with actual procurement spend. `RatePerMT` ties payment directly to received metric tons. Used by pricing engines and billing modules to configure supplier contracts and financial projections.

### 3. `InvoiceItemEnum` — Invoice line item classification
```csharp
BunkerCommission = 1, BunkerBarging = 2, BunkerVAT = 3, BunkerOtherExpenses = 4
```
**Explanation**: Standardizes financial line items specifically for bunker-related invoices. Used to group, total, and report bunker ancillary costs separately from main fuel purchases. The explicit integer backing (1-4) ensures deterministic ordering in ledger exports, GL mapping, and compliance reporting modules.

## Dependencies
- `Core.Domain.Constants` namespace context — ensures these enums are resolved purely within domain boundaries without crossing into application or infrastructure layers.
- None — purely declarative constants with zero runtime dependencies, injected services, or external consumers.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]