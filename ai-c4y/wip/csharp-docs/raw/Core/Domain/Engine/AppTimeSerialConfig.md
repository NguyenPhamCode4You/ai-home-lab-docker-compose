# AppTimeSerialConfig

## Purpose
Entity representing time-variant application configuration entries, keyed by a restricted set of enum values, with explicit activation and validity date management.

## Business Responsibility
Stores runtime application settings that may evolve over time (e.g., default pricing constants). Critical for configuration management; supports soft lifecycle via `IsActive` and temporal resolution via `ValidFrom`. The enum constraint ensures only supported configuration parameters are persisted, preventing arbitrary key injection.

---
IF DOMAIN/DTO:

## Members

### AppTimeSerialConfigKey
```csharp
public enum AppTimeSerialConfigKey
{
    VOY_DEFAULT_ETS_PRICE_IN_USD
}
```
**Explanation**: Defines the closed set of supported configuration keys. Enforces type safety and restricts the configuration space to `VOY_DEFAULT_ETS_PRICE_IN_USD`, preventing consumers from querying or creating unknown settings.

### ConfigKey
```csharp
[StringLength(100)]
[EnumDataType(typeof(AppTimeSerialConfigKey))]
public string ConfigKey { get; set; }
```
**Explanation**: Identifies the configuration parameter. Enforced via `[EnumDataType]` to restrict values to `AppTimeSerialConfigKey`. Length capped at 100 for DB consistency, though the enum constraint is the primary validation mechanism.

### ConfigValue
```csharp
[StringLength(2048)]
public string ConfigValue { get; set; }
```
**Explanation**: Holds the setting value. Supports up to 2048 characters, indicating the value may store structured data (e.g., JSON payloads) or detailed text, rather than simple scalar values.

### ValidFrom
```csharp
public DateTime ValidFrom { get; set; }
```
**Explanation**: Effective start date for the configuration. Enables time-series configuration where the value changes over time. Consumers must resolve the config using the current date against `ValidFrom` to determine the applicable value.

### IsActive
```csharp
public bool IsActive { get; set; } = false;
```
**Explanation**: Soft active flag. Defaults to `false`, meaning new configurations are inactive by default until explicitly activated. Allows disabling a config version without deleting it, preserving history for auditing or rollback.

---

## Dependencies
* `TrackedEntity` — Base class providing standard audit fields (CreatedBy, ModifiedBy, etc.) managed by `DataContext`; this entity inherits auditing without declaring explicit properties.
* `AppTimeSerialConfigKey` — Enum type referenced by `[EnumDataType]` attribute to enforce valid key values at the domain level.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]