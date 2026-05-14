# TagEntity

## Purpose
Represents a reusable tag definition scoped to a specific entity type, inheriting tenant isolation and lifecycle tracking from `TenantedEntity`.

## Business Responsibility
Defines the structural contract and validation boundaries for tag metadata before assignment. Critical for ensuring tags are only applied to compatible domain entities during creation and assignment workflows. Supports list views, dropdown population, and tag assignment validation.

## Members
Since the entity only contains constrained auto-properties, the business logic is enforced via data annotations and inheritance.

### 1. Name — Human-readable label for the tag.
```csharp
[Required]
[MaxLength(100)]
public string Name { get; set; } = string.Empty;
```
**Explanation**: Enforces a non-empty display name with a strict 100-character limit. Guarantees valid text for UI lists, assignment forms, and database constraints. Defaulting to `string.Empty` prevents null-reference issues during entity instantiation and EF Core change tracking.

### 2. EntityType — Target entity type this tag applies to.
```csharp
[Required]
[MaxLength(50)]
public string EntityType { get; set; } = string.Empty;
```
**Explanation**: Enforces a non-empty target type identifier limited to 50 characters. Ensures correct metadata routing and assignment validation during tag application. Defaulting to `string.Empty` maintains safe initialization. The value is cross-referenced against `EntityTypeConstants` to guarantee type-safe tag assignment.

## Dependencies
`TenantedEntity` — Provides tenant isolation, audit tracking, and base identity fields required for multi-tenant tag scoping and lifecycle management.
`EntityTypeConstants` — Referenced via documentation to guarantee `EntityType` values align with the system's registered domain types.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]