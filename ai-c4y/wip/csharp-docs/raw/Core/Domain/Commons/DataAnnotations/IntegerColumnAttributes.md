# NumberColumnAttribute & Integer Configuration Classes

## Purpose
Configuration attributes that enforce specific integer data type limits at the column level. They exist to decouple column metadata from hard-coded type strings, enabling centralized limit management for schema generation and ORM mapping.

## Business Responsibility
Owns the column metadata definition for integer-typed database fields. Critical for database schema generation and storage consistency. These attributes ensure that integer columns across the system adhere to predefined byte-width limits without scattering type constants throughout the domain. The pattern is explicitly inherited by `DecimalColumnAttributes.cs`, making this the foundational template for all numeric column definitions.

## Members

### 1. NumberColumnAttribute — [Set column type name from limit configuration]
```csharp
public NumberColumnAttribute(INumberLimits setting) : base()
{
    TypeName = setting.DataType;
}
```
**Explanation**: Accepts an `INumberLimits` instance at attribute instantiation. Extracts the canonical database type name (e.g., "TINYINT", "SMALLINT", "INT") via `setting.DataType` and assigns it to the inherited `TypeName` property. This decouples attribute syntax from underlying string literals, allowing limit definitions to be updated in a single location without touching attribute consumers or consumers of the attributes.

### 2. TinyInteger — [1-byte integer column alias]
```csharp
public class TinyInteger() : NumberColumnAttribute(new TinyIntegerLimit()) { }
```
**Explanation**: Instantiates `NumberColumnAttribute` with `TinyIntegerLimit`. Maps to 1-byte signed integer columns. Zero custom logic; serves as a compile-time type alias for consistent schema definition and readability across domain models.

### 3. SmallInteger — [2-byte integer column alias]
```csharp
public class SmallInteger() : NumberColumnAttribute(new SmallIntegerLimit()) { }
```
**Explanation**: Instantiates `NumberColumnAttribute` with `SmallIntegerLimit`. Maps to 2-byte signed integer columns. Acts as a standardized alias to prevent inconsistent byte-width usage and accidental 4-byte allocation for sparse counters or status flags.

### 4. StandardInteger — [4-byte integer column alias]
```csharp
public class StandardInteger() : NumberColumnAttribute(new StandardIntegerLimit()) { }
```
**Explanation**: Instantiates `NumberColumnAttribute` with `StandardIntegerLimit`. Maps to 4-byte signed integer columns. Provides a consistent alias for standard integer columns, replacing ad-hoc type annotations and ensuring alignment with ORM conventions.

## Dependencies
`ColumnAttribute` — Base class providing the `TypeName` property consumed by the schema generator/ORM to dictate column metadata and storage sizing.
`INumberLimits` — Interface supplying the canonical database type name (`DataType`) for each integer width. Centralizes type mapping logic and prevents hard-coded strings in attributes.
`TinyIntegerLimit`, `SmallIntegerLimit`, `StandardIntegerLimit` — Concrete limit configurations that define the exact string representation for each byte width. Ensure type safety and enable cross-cutting updates without recompiling attribute consumers.
`DecimalColumnAttributes.cs` (Known Caller) — Inherits and extends this pattern for decimal/fixed-point columns, confirming this class as the foundational template for all numeric column definitions.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]