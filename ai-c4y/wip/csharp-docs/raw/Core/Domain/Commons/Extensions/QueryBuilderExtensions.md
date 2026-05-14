# QueryBuilderExtensions

## Purpose
Converts reflection data from a .NET `Type` entity into a `QueryBuilderFieldConfig` hierarchy. Bridges the domain entity structure to the dynamic query builder UI metadata without requiring hardcoded schemas.

## Business Responsibility
Core metadata provider for BVMS search and filter capabilities. Enables dynamic field discovery, type inference, relationship traversal, and constraint mapping for any entity. Critical path for all query builder initialization; called on every entity query load.

---

## Members

### 1. ToQueryBuilderFields — Entry point: generates and sorts field configs
```csharp
public static Dictionary<string, QueryBuilderFieldConfig> ToQueryBuilderFields(Type entityType, int maxDepth)
{
    var allFields = new Dictionary<string, QueryBuilderFieldConfig>();
    // ... reflection loop creating configs ...
    var sortedFields = new Dictionary<string, QueryBuilderFieldConfig>();
    foreach (var field in allFields.Where(f => f.Value.Type == "navigation" || f.Value.Type == "array"))
        sortedFields[field.Key] = field.Value;
    foreach (var field in allFields.Where(f => f.Value.Type != "navigation" && f.Value.Type != "array"))
        sortedFields[field.Key] = field.Value;
    return sortedFields;
}
```
**Explanation**: Iterates all properties, delegates to `CreateFieldConfig` for recursive metadata extraction. Sorts results to prioritize navigation and array fields at the top. Ensures UI query builders present relational and collection fields before scalar fields, improving discoverability.

### 2. CreateFieldConfig — Recursive config builder with domain filters
```csharp
private static QueryBuilderFieldConfig? CreateFieldConfig(PropertyInfo property, ...)
{
    if (depth >= maxDepth) return null;
    if (IsRuleIgnored(property)) return null;
    if (IsGuidField(property)) return null;
    if (IsAuditField(property)) return null;
    if ((IsNavigationProperty(property) || IsCollectionProperty(property)) && depth >= maxDepth - 1) return null;
    // ... build config and dispatch to type setters ...
}
```
**Explanation**: Orchestrates field creation. Guards against excessive recursion (`maxDepth`). Filters out system/internal fields: ignores properties marked `[RuleBuilderIgnored]`, excludes `Guid` types, and strips audit columns (`CreatedOn`, `TenantId`, etc.). Prevents navigation/array expansion at `maxDepth - 1` to stop deeply nested UI queries. Constructs dot-separated `FieldName` paths (e.g., `Order.Customer.Name`) for nested queries.

### 3. SetEnumField — Enum resolution with hardcoded overrides
```csharp
private static void SetEnumField(PropertyInfo property, QueryBuilderFieldConfig fieldConfig, Type enumType)
{
    fieldConfig.Type = "select";
    // ... resolve enum type via [EnumDataType] or [EnumString] ...
    if (enumType.Name == "BillByEnum")
    {
        fieldConfig.FieldSettings.ListValues =
        [
            new() { Value = "BL Quantity", Title = "BL Quantity" },
            new() { Value = "CP Quantity", Title = "CP Quantity" },
            new() { Value = "Invoice Quantity", Title = "Invoice Quantity" }
        ];
        return;
    }
    // ... standard reflection loop for other enums ...
}
```
**Explanation**: Maps enums to UI "select" type. Reads `[EnumDataType]` or `[EnumString]` attributes to locate the enum type if decoupled from the property. **Hardcoded business rule**: `BillByEnum` is ignored and replaced with static list values ("BL/CP/Invoice Quantity"). This overrides reflection because the UI requires specific display strings that do not match enum names or domain evolution.

### 4. IsCollectionProperty — Type heuristics for collections
```csharp
private static bool IsCollectionProperty(PropertyInfo property)
{
    if (propertyType == typeof(string)) return false;
    if (propertyType.IsArray) return true;
    // ... checks IEnumerable, ICollection, List, Dictionary, etc. ...
    // ... fallback interface check ...
}
```
**Explanation**: Determines if a property should be rendered as an array/nested query builder. **Critical exclusion**: `string` implements `IEnumerable<char>` but must never be treated as a collection. Handles generic collections, arrays, and dictionaries. Includes fallback reflection checks for complex generic definitions to avoid `GetGenericTypeDefinition` exceptions on non-generic interfaces.

### 5. SetDateTimeField — Semantic time vs datetime inference
```csharp
private static void SetDateTimeField(PropertyInfo property, QueryBuilderFieldConfig fieldConfig)
{
    var isTimeOnly = property.Name.Contains("time", StringComparison.CurrentCultureIgnoreCase) 
                     && !property.Name.Contains("datetime", StringComparison.CurrentCultureIgnoreCase);
    fieldConfig.Type = isTimeOnly ? "time" : "datetime";
}
```
**Explanation**: Heuristic to distinguish `time` pickers from `datetime` pickers based on naming conventions. If the property name contains "time" but not "datetime" (e.g., `ArrivalTime` vs `CreatedDateTime`), maps to "time" type. Reduces UI confusion by auto-selecting the appropriate input widget.

### 6. SetBooleanField — Hardcoded Yes/No list values
```csharp
private static void SetBooleanField(QueryBuilderFieldConfig fieldConfig)
{
    fieldConfig.Type = "boolean";
    fieldConfig.FieldSettings.ListValues =
    [
        new() { Value = "true", Title = "Yes" },
        new() { Value = "false", Title = "No" }
    ];
}
```
**Explanation**: Standardizes boolean fields to "boolean" type with explicit `ListValues` mapping `true`/`false` to "Yes"/"No". Ensures consistent UI rendering for filters regardless of underlying boolean representation.

### 7. SetNavigationField — Recursive relation expansion
```csharp
private static void SetNavigationField(PropertyInfo property, QueryBuilderFieldConfig fieldConfig, ...)
{
    fieldConfig.Type = "navigation";
    // ... recursion into property.PropertyType.GetProperties() ...
    // ... populates fieldConfig.Children ...
}
```
**Explanation**: Recursively builds child configs for navigation properties. Sets `Type` to "navigation". Iterates the nested entity's properties, calls `CreateFieldConfig` with `depth + 1`, and populates `fieldConfig.Children`. Enables query builders to drill into related entities (e.g., filtering on `Customer.City`).

### 8. SetArrayField — Collection element reflection
```csharp
private static void SetArrayField(PropertyInfo property, QueryBuilderFieldConfig fieldConfig, ...)
{
    fieldConfig.Type = "array";
    // ... extracts elementType from T[] or IEnumerable<T> ...
    // ... recursively creates child fields from elementType ...
}
```
**Explanation**: Handles collections of complex types. Extracts the element type from arrays or generic `IEnumerable<T>`. Recursively processes the element's properties to create nested child configs. Allows query builders to filter inside collections (e.g., "Order Lines where UnitPrice > 100"). Skips non-object collections (like `List<string>`), which fall through to scalar handling.

### 9. SetValidation — Attribute-based constraints mapping
```csharp
private static void SetValidation(PropertyInfo property, QueryBuilderFieldConfig fieldConfig)
{
    // ... reads MaxLengthAttribute ...
    // ... reads RangeAttribute -> Min/Max ...
}
```
**Explanation**: Mirrors domain validation attributes to query builder settings. Reads `[MaxLength]` for string length constraints. Parses `[Range]` to extract decimal `Min` and `Max` bounds. Ensures query builder validation respects entity constraints.

### 10. GetDisplayName — Naming convention and typo correction
```csharp
private static string GetDisplayName(PropertyInfo property)
{
    var displayAttr = property.GetCustomAttribute<DisplayAttribute>();
    if (displayAttr?.Name != null) return displayAttr.Name;
    return Regex.Replace(property.Name, "([a-z])([A-Z])", "$1 $2")
        .Replace("Itenerary", "Itinerary");;
}
```
**Explanation**: Prioritizes `[Display]` attribute. Falls back to camelCase splitting regex (`Property` -> `Property`). Contains a **hardcoded typo fix** for "Itenerary" -> "Itinerary". Ensures readable labels in the UI despite legacy naming errors in the domain model.

### 11. GetMaxLength — Regex parsing of DB column size
```csharp
private static int? GetMaxLength(PropertyInfo property)
{
    // ... reads MaxLengthAttribute ...
    var columnAttr = property.GetCustomAttribute<System.ComponentModel.DataAnnotations.Schema.ColumnAttribute>();
    if (columnAttr?.TypeName != null)
    {
        var match = Regex.Match(columnAttr.TypeName, @"varchar\((\d+)\)");
        if (match.Success && int.TryParse(match.Groups[1].Value, out var length))
            return length;
    }
    return null;
}
```
**Explanation**: Retrieves max length from `[MaxLength]` attribute. If missing, falls back to parsing `[Column(TypeName = "varchar(N)")]` via regex. Extracts numeric length from SQL type strings. Provides accurate length hints for query builder text inputs.

---

## Dependencies
- `QueryBuilderFieldConfig`, `QueryBuilderFieldSettings`, `QueryBuilderListValue` — Output DTOs defining the query builder metadata schema.
- `RuleBuilderIgnoredAttribute` — Custom attribute to explicitly hide fields from query builders.
- `EnumDataTypeAttribute`, `EnumString` — Custom attributes for decoupled enum resolution.
- `DisplayAttribute`, `MaxLengthAttribute`, `RangeAttribute`, `ColumnAttribute` — Standard/Custom data annotation attributes providing type, constraint, and label metadata.
- `Type`, `PropertyInfo` — Reflection API for runtime entity introspection.
- `Regex` — Pattern matching for camelCase splitting, typo correction, and `varchar(N)` parsing.
- `IEnumerable`, `ICollection`, `Dictionary` types — Type hierarchy checks for collection vs scalar classification.