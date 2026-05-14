# BunkerOrderResponsibilityEnum

## Purpose
Defines the enumeration of responsibility types for bunker orders, distinguishing between Charterer, Owner, and Operator ownership.

## Business Responsibility
Core domain constant used to classify bunker cost ownership across voyage management and order processing. Drives financial accountability, cost center assignment, and downstream reporting. Referenced by Dtos, Entities, and Business helpers throughout the codebase.

## Members
### TCOCharterer — TCO Charterer responsibility
```csharp
[Description("TCO Charterer (Owned by External Charterer)")]
TCOCharterer,
```
**Explanation**: Indicates the bunker order is the responsibility of the TCO Charterer. Signifies ownership by an external charterer, triggering specific cost allocation logic and reporting paths for charterer-borne expenses.

### TCIOwner — TCI Owner responsibility
```csharp
[Description("TCI Owner (Owned by Vessel Owner)")]
TCIOwner,
```
**Explanation**: Indicates the bunker order is the responsibility of the TCI Owner. Signifies ownership by the vessel owner, affecting cost accounting for owned assets and operator-borne expenses.

### Operator — Operator responsibility
```csharp
[Description("Operator (Owned by BBC)")]
Operator
```
**Explanation**: Indicates the bunker order is the responsibility of the Operator (BBC). Used for internal operational costs managed directly by the company.

## Dependencies
`System.ComponentModel` — Required for `[Description]` attributes used to provide human-readable labels for the enum values.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]