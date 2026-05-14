# LoadingShipmentTermCode / DischargingShipmentTermCode

## Purpose
Defines strongly-typed enumerations for vessel loading and discharging contract terms. Exists to centralize maritime trade codes and attach human-readable labels via `[Description]` attributes for consistent UI/reporting output.

## Business Responsibility
Owns the canonical representation of Free In/Free Out (FI/FO) shipping terms for load/discharge operations. Critical for freight calculation engines, charter party alignment, and client-facing billing statements. Eliminates hardcoded string mismatches across estimation, execution, and accounting pipelines.

---

## Members

### 1. LoadingShipmentTermCode — Enum mapping loading trade terms to machine-readable constants
```csharp
public enum LoadingShipmentTermCode
{
  [Description("Liner in hook")]
  LIH,

  [Description("Free in LSD merchants account")]
  FI_LSD_MA,

  [Description("Free in LSD carriers account")]
  FI_LSD_CA,

  [Description("Free in stowed trimmed")]
  FI_ST,
}
```
**Explanation**: Covers standard load-side allocations. `LIH` indicates carrier responsibility from hook-in. `FI_LSD_*` splits Lighterage/Special Discharge cost burden between merchant (`MA`) or carrier (`CA`). `FI_ST` shifts stowing/trimming liability to the merchant. Descriptions are consumed by reflection at binding/report time to avoid switch-case duplication.

### 2. DischargingShipmentTermCode — Enum mapping discharging trade terms to machine-readable constants
```csharp
public enum DischargingShipmentTermCode
{
  [Description("Liner out hook")]
  LOH,
  [Description("Free out LSD merchants account")]
  FO_LSD_MA,
  [Description("Free out LSD carriers account")]
  FO_LSD_CA,
  [Description("Free out stowed trimmed")]
  FO_ST
}
```
**Explanation**: Mirrors loading terms for discharge operations. `LOH` denotes carrier responsibility through hook-out. `FO_LSD_*` and `FO_ST` apply the same cost-allocation logic as loading but against discharge services. Ensures symmetry in voyage cost modeling and prevents directional billing errors.

---

## Dependencies
- `System.ComponentModel.DescriptionAttribute` — Required to attach display strings directly to enum values, enabling the presentation layer to render terms without separate lookup tables or localization files.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]