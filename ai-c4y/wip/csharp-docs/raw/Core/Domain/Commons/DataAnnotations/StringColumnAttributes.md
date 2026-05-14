# StringColumnAttribute

## Purpose
Defines a family of ORM column attributes that standardize string type configuration (length, Unicode/ANSI switching, enum validation) across the domain layer. Exists to decouple database schema conventions from entity definitions.

## Business Responsibility
Owns the technical contract for string column definitions in the persistence layer. Low business logic, but critical for data consistency and cross-environment schema generation. Applied via metadata attributes on domain models to enforce length caps and type mapping automatically during migrations or model initialization.

---
## Members

### 1. Constructor (`StringColumnAttribute`) — Initializes string column metadata with validation and type resolution
```csharp
public StringColumnAttribute(IStringLimits stringLimit, bool useUnicode = false, Type? enumType = null) : base()
{
    var maxLength = stringLimit.MaxLength;
    if (enumType != null && !enumType.IsEnum)
    {
        throw new ArgumentException($"Type '{enumType.Name}' is not an enum type.");
    }

    MaxLength = maxLength;
    UseUnicode = useUnicode;
    EnumType = enumType;
    TypeName = useUnicode ? $"nvarchar({maxLength})" : $"varchar({maxLength})";
}
```
**Explanation**: Accepts a limit interface to resolve the maximum allowed length, preventing hardcoded string lengths in entities. Validates that `enumType` is strictly an enum, failing fast if misconfigured. Composes `TypeName` dynamically: switches between `nvarchar` (UTF-16) and `varchar` (ASCII) based on `useUnicode`, directly influencing storage size and database collation behavior downstream during model building.

### 2. Derived Length Attributes (`TinyString`, `SmallString`, `StandardString`, `LongString`) — Preconfigured length constraints
```csharp
public class TinyString(bool useUnicode = false) : StringColumnAttribute(new TinyStringLimit(), useUnicode) { }
public class SmallString(bool useUnicode = false) : StringColumnAttribute(new SmallStringLimit(), useUnicode) { }
public class StandardString(bool useUnicode = false) : StringColumnAttribute(new StandardStringLimit(), useUnicode) { }
public class LongString(bool useUnicode = false) : StringColumnAttribute(new LongStringLimit(), useUnicode) { }
```
**Explanation**: Zero-logic subclasses that lock in specific `IStringLimits` implementations. Allow developers to annotate properties with semantic length buckets instead of magic numbers. Enforce uniform column sizing across the domain model without repeating limit configuration or risking schema drift.

### 3. `EnumString` — Attribute shorthand for strongly-typed enum-to-string mapping
```csharp
public class EnumString(Type enumType, bool useUnicode = false) : StringColumnAttribute(new SmallStringLimit(), useUnicode, enumType) { }
```
**Explanation**: Provides a focused attribute for enum-backed string columns. Binds to `SmallStringLimit` by default but passes `enumType` to the base constructor, enabling downstream model builders or validators to enforce that persisted strings match the specified enum's defined values. Prevents invalid enum string storage without requiring manual validation logic on every property.

## Dependencies
- `IStringLimits` (via `stringLimit` parameter) — Provides the canonical maximum length for the column; centralizes length policy so changing a limit updates all annotated fields at once without touching entity classes.
- `ColumnAttribute` (base class) — Inherits shared database column metadata structure (e.g., ordering, nullable flags) to ensure uniform attribute handling in model configuration pipelines.
- `System.Type` (for `EnumType` and `IsEnum`) — Required to defer enum validation and enable reflection-based constraint resolution or type-checking during model initialization.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]