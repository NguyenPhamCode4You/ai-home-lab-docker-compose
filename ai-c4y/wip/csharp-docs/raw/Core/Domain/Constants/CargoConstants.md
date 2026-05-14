# CargoType

## Purpose
Enumerates the two primary commercial categories for cargo in the BVMS domain, distinguishing between ad-hoc budget cargo and pre-negotiated contract cargo.

## Business Responsibility
Owns the categorical branch point for cargo planning, costing, and financial reconciliation. It dictates which pricing rules, SLA tracking, and diagnostic workflows apply across the domain. Critical for separating spot-market operations from volume/commitment-based logistics, directly impacting invoicing accuracy, policy validation, and audit diagnostics.

---
## Members

### 1. Budget — Ad-hoc cargo category
```csharp
Budget
```
**Explanation**: Represents cargo without a standing commercial agreement. Used to trigger spot-market costing, standard invoicing pipelines, and baseline diagnostic checks. Skips contract-specific margin validations, volume commitment tracking, and dedicated audit paths referenced in `InvoiceUtil` and `VoyageDiagnostics`.

### 2. Contract — Pre-negotiated cargo category
```csharp
Contract
```
**Explanation**: Represents cargo bound by a master service agreement or standing rate. Activates contract-specific pricing logic, SLA compliance checks, and specialized voyage/invoice diagnostics. Alters downstream mapping in `EstimateShipmentDtos`, `FreightInvoiceUtil`, and claim policy resolution.

---
## Dependencies
None. Pure domain constant with zero runtime or interface dependencies.

---
# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]