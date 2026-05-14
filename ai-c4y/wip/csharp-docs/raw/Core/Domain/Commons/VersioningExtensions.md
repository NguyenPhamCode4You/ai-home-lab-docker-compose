# VersioningExtensions

## Purpose
A static extension utility that validates optimistic concurrency versioning on domain entities prior to persistence operations. Prevents lost updates by ensuring the client is acting on the latest entity state.

## Business Responsibility
Owns the optimistic concurrency control gate for any entity implementing `IVersionedEntity`. Critical for data integrity in concurrent editing and background process scenarios, blocking stale writes before they reach the repository layer. Called as a prerequisite in every save/update workflow to enforce last-write-wins semantics at the domain boundary.

---
## Members

### ValidateVersion<TEntity> — Validates optimistic locking state before persistence
```csharp
public static void ValidateVersion<TEntity>(this TEntity entity, uint expectedVersion)
    where TEntity : IVersionedEntity
{
    if (entity.VersionNumber != expectedVersion)
    {
        var entityName = typeof(TEntity).Name.Replace("Entity", "");
        throw new ApiException(
            ErrorCode.CONCURRENCY_CONFLICT,
            "Update not allowed. Data has been changed by another user or a background process. " +
            $"User want to save version {expectedVersion} but system already has version {entity.VersionNumber}");
    }
}
```
**Explanation**: Compares the client-supplied `expectedVersion` against the in-memory `VersionNumber` of the entity. If they mismatch, execution short-circuits and throws a structured `ApiException`. The method dynamically derives a clean entity name for the error message by stripping the `"Entity"` suffix, ensuring precise caller feedback about which resource experienced the collision. This enforces optimistic locking at the domain layer, guaranteeing that only concurrent-safe modifications proceed to repository commits.

## Dependencies
- `IVersionedEntity` — Provides the `VersionNumber` property contract that this utility validates against.
- `ApiException` (with `ErrorCode.CONCURRENCY_CONFLICT`) — Returns a standardized, domain-aware concurrency conflict response instead of raw runtime exceptions.
- `System.Type` (`typeof`) — Used to dynamically extract the entity's class name for contextual error messaging without requiring explicit type parameters in the call site.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]