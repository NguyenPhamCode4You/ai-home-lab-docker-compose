# AppTimeSerialConfigDto

## Purpose
Data transfer object representing application time/serial configuration records, encapsulating key-value pairs, validity windows, and active state for cross-layer serialization.

## Business Responsibility
Acts as the structural contract for configuration management operations (Create, Get, Search, Update) and the AutoMapper mapping pipeline. Carries zero domain logic; purely transports configuration state between the API controller, business handlers, and the infrastructure layer. Low computational impact, but critical for consistent configuration CRUD serialization and deserialization contracts.

---

## Members
Contains only simple auto-properties. Per instructions, trivial setters are skipped. The only non-trivial default is:

### 1. `IsActive` — Default active state override
```csharp
public bool IsActive { get; set; } = false;
```
**Explanation**: Explicitly initializes the active flag to `false` at instantiation to prevent accidental activation during DTO creation or JSON deserialization. Ensures all new configuration entries default to inactive until explicitly enabled via an update workflow, avoiding stale or unintended active records.

---

## Dependencies
`BaseDto` — Provides inherited identity, concurrency token, and audit fields (`Id`, `CreatedAt`, `ModifiedAt`, `IsDeleted`) required by the EF Core mapping pipeline, repository operations, and global query filters.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]