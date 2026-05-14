**File Type Identified**: DOMAIN/DTO (Domain Entity / Polymorphic Join Table)

# EntityTagEntity

## Purpose
Serves as a polymorphic junction table linking any taggable domain entity to a `TagEntity`. Exists to normalize many-to-many relationships and enable type-safe discriminator routing for the tagging subsystem.

## Business Responsibility
Owns the association model for BVMS tag management, allowing dynamic categorization of disparate business entities without schema proliferation. Critical infrastructure for the `UpdateEntityTags` workflow and `DataContext` mappings — ensures tags resolve to the correct entity type and tenant scope. Without it, tag assignments lack referential safety and cross-entity contamination occurs.

---
## Members

### 1. EntityType — Discriminator for polymorphic entity routing
```csharp
[Required]
[MaxLength(50)]
public string EntityType { get; set; } = string.Empty;
```
**Explanation**: Stores the registered type identifier for the tagged entity (e.g., `Core.Domain.Bunkering.Models.BunkerOrderEntity`). Enforced by data annotations to guarantee valid discriminator values before persistence. Prevents cross-entity tag collisions and directs EF Core routing queries to the correct underlying table. Without this, the many-to-many mapping collapses into an ambiguous GUID pair.

---
## Dependencies
- `TenantedEntity` — base class supplying tenant isolation and soft-delete lifecycle; required so tag assignments inherit tenant scoping and audit compliance.
- `TagEntity` — referenced via `Tag` navigation and `TagId` FK; provides the canonical tag definition that `EntityTagEntity` anchors to.
- `System.ComponentModel.DataAnnotations` — `[Required]` and `[MaxLength(50)]` attributes enforce schema constraints and prevent discriminator injection/overflows at runtime.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]