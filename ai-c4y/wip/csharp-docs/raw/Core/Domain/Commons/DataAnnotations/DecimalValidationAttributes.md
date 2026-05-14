# DecimalValidationAttribute

## Purpose
Provides a family of Data Annotation validation attributes (`StandardDecimal`, `PrecisionDecimal`, `HighPrecisionDecimal`, `GeoGraphicDecimal`) that enforce domain-specific numeric ranges and type constraints on decorated model properties.

## Business Responsibility
Owns numeric data integrity for financial, scientific, and geographic fields across BVMS. Critical for preventing precision loss, overflow, and invalid coordinate entries during model binding and persistence. Serves as the central enforcement point for decimal boundaries, ensuring consistent validation feedback across UI binding and backend model state.

## Validation Rules
### StandardDecimal, PrecisionDecimal, HighPrecisionDecimal, GeoGraphicDecimal
- Rule: Attributes inherit from `DecimalValidationAttribute` and delegate to distinct `INumberLimits` configurations via constructor injection.
- Business constraint: Enforces tiered precision boundaries. Standard/Precision handle accounting/monetary values, High-Precision handles engineering/scientific measurements, and Geographic handles latitude/longitude constraints. Prevents invalid type casting or out-of-bounds numeric entries at the model-binding layer.

### IsValid (Range & Type Enforcement)
- Rule: Overrides `NumberValidationAttribute.IsValid` to check for `null` (returns success), enforce `value is decimal`, validate against `MinValue`/`MaxValue`, and format failures using `GetDisplayName` and `GetValueRangeAsString`.
- Business constraint: Guarantees strict decimal type compliance and range adherence. Skips null checks (delegates existence validation to `[Required]`). Rejects non-decimal inputs with a typed error message. Fails fast on out-of-range values, providing clear, property-name-scoped feedback to prevent invalid entities from proceeding to persistence.

## Dependencies
- `INumberLimits` — Injected to resolve concrete range/precision limits at runtime; replaces hardcoded constants and enables environment-specific limit tuning.
- `NumberValidationAttribute` — Base Data Annotation class providing `MinValue`, `MaxValue`, `ValidationResult`, and attribute wiring infrastructure; avoids reinventing attribute lifecycle management.
- `StandardDecimalLimit`, `PrecisionDecimalLimit`, `HighPrecisionDecimalLimit`, `GeographicDecimalLimit` — Sealed limit configurations injected into derived attributes to isolate domain-specific boundaries and prevent cross-contamination of validation rules.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]