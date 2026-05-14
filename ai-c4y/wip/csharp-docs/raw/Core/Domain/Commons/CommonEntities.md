# Core.Domain.Commons Base Hierarchy

## Purpose
Defines the foundational inheritance chain for all domain entities (`TrackedEntity` → `BaseEntity` → `TenantedEntity`) and their corresponding DTOs (`IdBasedDto` → `BaseDto` / `HeadlessDto`). Enforces a unified contract for auditing, soft-deletion, multi-tenancy, and optimistic concurrency across the BVMS domain model.

## Business Responsibility
Core infrastructure for the domain model and API contracts. Every entity in BVMS inherits from this hierarchy, and all DTOs mirror the audit/status fields. **Critical**: `SoftDelete` is the canonical deletion operation ensuring physical data retention; `[VersionIgnore]` prevents audit field updates from triggering false-positive concurrency exceptions. Changes to these base types cascade to all entities, DTOs, EF Core mappings, and serialization pipelines.

---
IF DOMAIN/DTO:

## Members

### SoftDelete — Canonical soft-deletion operation
```csharp
public void SoftDelete()
{
    IsDeleted = true;
}
```
**Explanation**: Explicitly marks the entity as deleted. Called by application logic to trigger soft-deletion. Allows the caller to manage `DeletedOn`/`DeletedById` atomically within a transaction or batch operation, rather than forcing immediate timestamp/identity assignment inside this method.

### IVersionedEntity — Optimistic concurrency contract
```csharp
public interface IVersionedEntity
{
    uint VersionNumber { get; }
    void IncreaseVersion();
}
```
**Explanation**: Interface required for entities participating in row-versioning. `VersionNumber` holds the concurrency token; `IncreaseVersion` increments the counter. Implemented by aggregates to enable EF Core or middleware to detect concurrent modifications and prevent lost updates.

## Dependencies
- `VersionIgnoreAttribute` — Applied to `ModifiedOn` and `ModifiedById` on `TrackedEntity`. Excludes these tracking fields from the versioning comparison logic, ensuring that routine audit updates do not cause spurious concurrency failures.
- `NotMappedAttribute` — Applied to `TrackedEntity` class. Prevents EF Core from treating this base class as a mapped table, ensuring it functions purely as an abstract base contract in TPH/TPT inheritance scenarios.