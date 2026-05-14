# EntityTypeConstants

## Purpose
Serves as a centralized string literal registry for entity type identifiers across the domain layer. Eliminates magic strings and ensures consistent type resolution for tagging, filtering, and API contracts.

## Business Responsibility
Owns the canonical string representation of the `BunkerOrder` entity type. Critical for cross-layer type discrimination where string-based matching occurs (e.g., audit tagging, query predicates, and controller routing). Maintaining this single source of truth prevents type mismatch errors and eliminates duplication when entity naming conventions change.

## Members

### 1. BunkerOrder — Canonical string identifier for the BunkerOrder aggregate
```csharp
public const string BunkerOrder = "BunkerOrder";
```
**Explanation**: Exposes the exact string value used to identify the `BunkerOrder` entity across the system. Read by `TagEntity` for metadata tagging, `SearchBunkerOrders` for query filtering, and `BunkerOrderController` for request validation and response typing. Guarantees that all downstream consumers reference the identical literal, preventing silent breakages in type-switch logic or external integrations.

## Dependencies
- None (pure constant registry; no injected services, base classes, or runtime references)

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]