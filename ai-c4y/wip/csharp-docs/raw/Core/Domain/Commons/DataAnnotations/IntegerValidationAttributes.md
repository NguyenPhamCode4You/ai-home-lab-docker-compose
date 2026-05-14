# NumberValidationAttribute & IntegerValidationAttribute

## Purpose
Base DataAnnotations validation attributes that enforce numeric range constraints defined by injected `INumberLimits` settings. `IntegerValidationAttribute` extends this to strictly validate `int` type and bounds before domain persistence.

## Business Responsibility
Owns cross-cutting data integrity enforcement for integer fields across domain models. Critical for preventing out-of-range or type-mismatched values from entering business workflows or storage. Acts as the single source of truth for integer range validation, error formatting, and boundary checking. The concrete classes (`TinyInteger`, `SmallInteger`, `StandardInteger`) exist solely to swap `INumberLimits` implementations, mirroring the pattern in `DecimalValidationAttributes.cs`.

---
## Members

### MinValue / MaxValue / TypeName — Injected range configuration
```csharp
public string TypeName { get; } = setting.DataType;
public decimal? MinValue { get; } = setting.MinValue;
public decimal? MaxValue { get; } = setting.MaxValue;
```
**Explanation**: Read-only properties mapped directly from `INumberLimits`. Supply the validation boundaries and data type label consumed by `IsValid` and string formatters. Immutable to guarantee consistent validation state throughout the attribute lifecycle.

### GetValueRangeAsString — Human-readable range descriptor
```csharp
public string GetValueRangeAsString()
{
    var minString = FormatDecimalString(MinValue);
    var maxString = FormatDecimalString(MaxValue);
    if (MinValue.HasValue && MaxValue.HasValue) return $"from {minString} to {maxString}";
    else if (MinValue.HasValue) return $">= {minString}";
    else if (MaxValue.HasValue) return $"<= {maxString}";
    return string.Empty;
}
```
**Explanation**: Formats the active min/max boundaries into a consistent user-facing string. Uses conditional priority to handle exclusive ranges and single-sided limits. Drives all validation error messages to ensure uniform boundary presentation across UI and API layers.

### FormatDecimalString — Numeric formatting helper
```csharp
public static string FormatDecimalString(decimal? decimalValue) =>
    !decimalValue.HasValue ? "unspecified" : decimalValue.Value.ToString("N");
```
**Explanation**: Normalizes nullable decimal limits into standardized strings with locale-aware number formatting. Returns "unspecified" when limits are unset, preventing null reference issues and keeping range strings clean when only one bound is defined.

### GetDisplayName — Contextual property resolver
```csharp
public static string GetDisplayName(ValidationContext validationContext) =>
    validationContext.DisplayName ?? validationContext.MemberName ?? "This field";
```
**Explanation**: Resolves the display name from validation metadata, falling back to the C# property name, then a generic placeholder. Ensures error messages reference the exact UI-friendly field name without requiring custom data annotations on every model property.

### IsValid — Core integer validation enforcement
```csharp
protected override ValidationResult? IsValid(object? value, ValidationContext validationContext)
{
    var rangeInfo = GetValueRangeAsString();
    var displayName = GetDisplayName(validationContext);
    if (value == null) return ValidationResult.Success;
    if (value is not int intValue) return new ValidationResult($"{displayName}: must be an integer ({rangeInfo}).");
    if (MinValue.HasValue && intValue < MinValue.Value) return new ValidationResult($"{displayName}: must be {rangeInfo}");
    if (MaxValue.HasValue && intValue > MaxValue.Value) return new ValidationResult($"{displayName}: must be {rangeInfo}");
    return ValidationResult.Success;
}
```
**Explanation**: Overrides base validation to enforce type and range constraints on `int` values. Short-circuits on `null` to allow nullable integers per domain rules. Rejects non-`int` values with a type mismatch error. Validates lower/upper bounds using injected limits. Returns structured `ValidationResult` on failure, otherwise success. Skipped validation means the field is intentionally nullable or omitted in the model.

---

## Dependencies
`INumberLimits` — Injected via constructor to supply the exact `MinValue`, `MaxValue`, and `DataType` constraints. This file contains no hardcoded bounds; it strictly delegates limit definitions to this interface to maintain separation of validation logic from configuration and allow environment-specific limit swapping.
`ValidationAttribute` — Base framework class providing the `ValidationResult` return type and integration with `System.ComponentModel.DataAnnotations` model binding pipeline.
`TinyIntegerLimit / SmallIntegerLimit / StandardIntegerLimit` — Instantiated in the parameterless concrete classes to bind specific domain integer width constraints to the validation logic.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]