# QueryBuilderFieldConfig

## Purpose
Defines the runtime configuration schema for dynamic query builder fields, including identity metadata, validation constraints, and hierarchical nesting. Acts as a lightweight configuration model bridging backend field definitions with frontend rendering and expression evaluation.

## Business Responsibility
Owns the metadata contract passed to the UI query builder component and the expression evaluation engine. Enables dynamic constraint injection (numeric ranges, string limits, dropdown enumerations) and nested field grouping without hardcoding domain schema. Critical for master data-driven rule configuration and cross-service field metadata distribution.

## Members

### 1. FieldName, Label, Type — Core field identity and type contract
```csharp
public string FieldName { get; set; }
public string Label { get; set; }
public string Type { get; set; }
```
**Explanation**: Maps to the underlying database column/property, user-facing label, and serialized CLR/type identifier. Drives how the query builder resolves expressions, casts input values, and generates SQL or in-memory filters. Omission breaks field resolution and type coercion during query compilation.

### 2. FieldSettings — Validation and constraint container
```csharp
public QueryBuilderFieldSettings FieldSettings { get; set; } = new();
```
**Explanation**: Groups all optional constraints for the field. The non-null default initializer prevents null reference exceptions when traversing the config tree or deserializing partial JSON. Allows consumers to check constraints without defensive null-coalescing at runtime.

### 3. QueryBuilderFieldSettings — Constraint definitions
```csharp
public class QueryBuilderFieldSettings
{
    public List<QueryBuilderListValue>? ListValues { get; set; }
    public int? MaxLength { get; set; }
    public decimal? Min { get; set; }
    public decimal? Max { get; set; }
}
```
**Explanation**: Defines optional input boundaries. `ListValues` populates dropdown enumerations; `MaxLength` caps string input; `Min`/`Max` enforce numeric bounds. Nullable types permit constraint omission per field, preserving schema flexibility while enabling strict validation during query parameter binding.

### 4. Children — Hierarchical field grouping
```csharp
public Dictionary<string, QueryBuilderFieldConfig>? Children { get; set; }
```
**Explanation**: Represents nested or related sub-fields (e.g., joined entity properties or multi-part address fields). Enables tree-based UI rendering and recursive query path generation. Nullability cleanly separates flat from hierarchical field definitions.

### 5. QueryBuilderListValue — Dropdown option mapping
```csharp
public class QueryBuilderListValue
{
    public string Value { get; set; }
    public string Title { get; set; }
}
```
**Explanation**: Maps a persisted storage value to a user-readable display string. Decouples UI labels from backend constants, allowing master data or localization updates without regenerating query evaluation logic or breaking expression trees.

## Dependencies
- None — Pure configuration POCOs with no injected services, base classes, or interface dependencies.
- `System.Collections.Generic` — Required for `Dictionary` and `List` collection support.
- `Core.Domain.Commons.Extensions.QueryBuilderExtensions` (Caller) — Consumes this config to generate expression trees and type-safe predicates.
- `Core.Business.TaskAlert.GetFieldsForEntity` (Caller) — Retrieves database schema/metadata and serializes it into this structure.
- `APIs/MasterData/TaskAlert.RuleSetsController` (Caller) — Exposes configuration endpoints that read/write this model.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]