# GeneralAccountDto / GeneralAccountUpdateDto

## Purpose
Flat data contracts mapping the `GeneralAccount` domain entity across the finance master data boundary. Separates domain models from API/request payloads and provides distinct shapes for read operations (`GeneralAccountDto`) versus mutation (`GeneralAccountUpdateDto`).

## Business Responsibility
Owned by the Finance Master Data domain. `GeneralAccountDto` is the read contract consumed by list queries, detail fetches, cross-module lookups, and AutoMapper profiles. `GeneralAccountUpdateDto` isolates mutable state for patching, preventing over-posting and ensuring only explicit account metadata reaches the application service. Critical for financial chart-of-accounts integrity and dimensional filtering.

---
IF DOMAIN/DTO:

## Members
The file contains only flat data carriers with no computed logic or fallback chains. Documented below by business meaning per domain requirements.

### 1. AccountCode / AccountName — Core identifier fields
```csharp
public required string AccountCode { get; set; }
public required string AccountName { get; set; }
```
**Explanation**: Mandatory chart-of-accounts keys. `AccountCode` acts as the unique posting/reconciliation identifier; `AccountName` is the human-readable label. Enforced as `required` to guarantee non-null binding in downstream AutoMapper mappings and API validation, preventing null-boundary exceptions during transaction posting or reporting.

### 2. Category / SubCategory — Hierarchical grouping fields
```csharp
public string? Category { get; set; }
public string? SubCategory { get; set; }
```
**Explanation**: Optional dimension tags used for financial statement grouping and ledger aggregation. Nullable to accommodate accounts that operate outside a secondary hierarchy. Directly projected to database columns for indexing and reporting filters.

### 3. Relationship Flags — Target dimension applicability
```csharp
public bool IsBusinessSpecific { get; set; }
public bool IsVesselRelated { get; set; }
public bool IsVoyageRelated { get; set; }
public bool IsPortRelated { get; set; }
public bool IsDepartmentRelated { get; set; }
public bool IsIntercompany { get; set; }
```
**Explanation**: Boolean switches indicating which operational dimensions the account supports. Consumed by `BusinessRuleDtos.cs`, `SelectionController.cs`, and posting workflows to enforce dimensional applicability rules. Defaults to `false` to prevent accidental over-allocation of accounts to unrelated operational contexts.

## Dependencies
`BaseDto` — Provides inherited audit/metadata properties (Id, timestamps, tenant/context tracking) ensuring consistent lifecycle tracking and base contract alignment across all finance domain DTOs without requiring manual property duplication.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]