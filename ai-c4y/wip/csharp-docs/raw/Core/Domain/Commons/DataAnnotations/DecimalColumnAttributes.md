# Column Attribute Classes (StandardDecimal, PrecisionDecimal, HighPrecisionDecimal, GeoGraphicDecimal)

## Purpose
Marker/configuration attributes that enforce decimal precision and scale constraints on domain properties. Exists to centralize column metadata for persistence mapping and API serialization, removing repetitive attribute wiring across DTOs and Entities.

## Business Responsibility
Owns the metadata contract for decimal columns across MasterData and VoyageManagement aggregates. Low-impact structural utility; applies declaratively to ensure data fidelity during EF Core mapping, JSON serialization, and downstream reporting. Delegates all constraint logic to the `DataTypeLimits` configuration objects; this file only bridges syntax to implementation.

---
## Members

### 1. StandardDecimal — Marks properties for standard decimal precision
```csharp
public class StandardDecimal() : NumberColumnAttribute(new StandardDecimalLimit()) { }
```
**Explanation**: Inherits from `NumberColumnAttribute` and injects `StandardDecimalLimit` via a C# 12 primary constructor. Applied to general numeric fields (quantities, rates, flags) to enforce baseline precision/scale during database storage and DTO serialization. Prevents implicit truncation or over-precision in standard business flows.

### 2. PrecisionDecimal — Marks properties for precision decimals
```csharp
public class PrecisionDecimal() : NumberColumnAttribute(new PrecisionDecimalLimit()) { }
```
**Explanation**: Binds to `PrecisionDecimalLimit`. Used for financial metrics or calculated fields requiring explicit scale control. Ensures consistent rounding behavior across persistence layers and external integrations.

### 3. HighPrecisionDecimal — Marks properties for high-precision decimals
```csharp
public class HighPrecisionDecimal() : NumberColumnAttribute(new HighPrecisionDecimalLimit()) { }
```
**Explanation**: Configures `HighPrecisionDecimalLimit`. Reserved for engineering specs, detailed cost breakdowns, or KPIs where standard rounding introduces unacceptable error. Locks scale to prevent precision loss during type coercion or API contract translation.

### 4. GeoGraphicDecimal — Marks properties for geographic coordinate decimals
```csharp
public class GeoGraphicDecimal() : NumberColumnAttribute(new GeographicDecimalLimit()) { }
```
**Explanation**: Delegates to `GeographicDecimalLimit`. Tailored specifically for latitude/longitude and spatial coordinates. Enforces scale/precision rules aligned with geographic data standards, ensuring accurate distance calculations and mapping service compatibility.

## Dependencies
- `NumberColumnAttribute` — Base attribute providing the structural contract and metadata storage; required for the persistence mapper and serialization pipelines to recognize and apply these constraints.
- `StandardDecimalLimit` / `PrecisionDecimalLimit` / `HighPrecisionDecimalLimit` / `GeographicDecimalLimit` — Configuration objects defining actual scale/precision bounds; injected via primary constructors to keep attribute syntax decoupled from constraint implementation.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]