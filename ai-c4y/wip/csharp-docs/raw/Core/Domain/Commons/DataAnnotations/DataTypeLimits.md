FILE TYPE: OTHER

# DataTypeLimits Configuration Classes

## Purpose
Centralizes compile-time enforced constraints for string lengths and numeric ranges across the BVMS domain model. Provides the canonical definitions for data shape and validation boundaries.

## Business Responsibility
Acts as the single source of truth for column constraints, directly driving EF Core data annotation generation and database schema validation. Prevents runtime data truncation, SQL type mismatches, and inconsistent validation rules. Critical for data integrity during entity persistence and external API ingestion.

---
## Members

### 1. IStringLimits — Contract for string length constraints
```csharp
public interface IStringLimits
{
    public int MaxLength { get; }
    public int MinLength { get; }
}
```
**Explanation**: Defines the shape for string validation limits. Implemented by concrete classes to ensure type-safe limit injection during annotation generation or model validation.

### 2. String Limit Implementations — Fixed-length constraints for text columns
```csharp
public class TinyStringLimit : IStringLimits { public int MaxLength => 30; public int MinLength => 0; }
public class SmallStringLimit : IStringLimits { public int MaxLength => 150; public int MinLength => 0; }
public class StandardStringLimit : IStringLimits { public int MaxLength => 550; public int MinLength => 0; }
public class LongStringLimit : IStringLimits { public int MaxLength => 2500; public int MinLength => 0; }
```
**Explanation**: Concrete implementations mapping to standard database varchar/text column sizes. `MaxLength` aligns with typical DB constraints (e.g., `NVARCHAR(30)` to `NVARCHAR(2500)`). `MinLength` is uniformly 0. Directly consumed by `StringColumnAttributes.cs` and `StringValidationAttributes.cs` to generate `[MaxLength]`/`[MinLength]` DataAnnotations automatically.

### 3. INumberLimits — Contract for numeric range and SQL type constraints
```csharp
public interface INumberLimits
{
    public string DataType { get; }
    public decimal? MinValue { get; }
    public decimal? MaxValue { get; }
}
```
**Explanation**: Defines the shape for numeric constraints. `DataType` exposes the exact SQL Server type string, while `MinValue`/`MaxValue` enforce CLR-to-DB range checks.

### 4. Number Limit Implementations — Precise range and type definitions for numeric columns
```csharp
public class StandardIntegerLimit : INumberLimits { public string DataType => "int"; public decimal? MinValue => -2147483648m; public decimal? MaxValue => 2147483647m; }
public class StandardDecimalLimit : INumberLimits { public string DataType => "decimal(18, 2)"; public decimal? MinValue => -9999999999999999.99m; public decimal? MaxValue => 9999999999999999.99m; }
public class PrecisionDecimalLimit : INumberLimits { public string DataType => "decimal(25, 5)"; public decimal? MinValue => -99999999999999999999.99999m; public decimal? MaxValue => 99999999999999999999.99999m; }
public class HighPrecisionDecimalLimit : INumberLimits { public string DataType => "decimal(30, 10)"; public decimal? MinValue => -99999999999999999999999999.9999999999m; public decimal? MaxValue => 99999999999999999999999999.9999999999m; }
public class GeographicDecimalLimit : INumberLimits { public string DataType => "decimal(12, 6)"; public decimal? MinValue => -999999.999999m; public decimal? MaxValue => 999999.999999m; }
public class TinyIntegerLimit : INumberLimits { public string DataType => "tinyint"; public decimal? MinValue => 0m; public decimal? MaxValue => 255m; }
public class SmallIntegerLimit : INumberLimits { public string DataType => "smallint"; public decimal? MinValue => -32768m; public decimal? MaxValue => 32767m; }
```
**Explanation**: Implements `INumberLimits` with exact boundaries matching SQL Server types. `StandardIntegerLimit` covers full `INT` range. `StandardDecimalLimit` (18,2) matches currency/amount fields. `PrecisionDecimalLimit` (25,5) and `HighPrecisionDecimalLimit` (30,10) support financial/scientific calculations requiring extended precision. `GeographicDecimalLimit` (12,6) constrains lat/long values to valid geographic ranges. `TinyIntegerLimit` (tinyint) and `SmallIntegerLimit` (smallint) provide space-optimized integer ranges.

## Dependencies
`IStringLimits` — Base contract enforced across the codebase to guarantee type-safe string length injection into DataAnnotations and validation pipelines.
`INumberLimits` — Base contract ensuring numeric range and SQL type strings are centrally defined, preventing drift between C# models and database schema generation.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]