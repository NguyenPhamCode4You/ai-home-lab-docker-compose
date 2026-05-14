# Constants and Enum Definitions

## Purpose
Defines the canonical set of domain enumerations, static financial constants, and extension helpers that standardize state representation, coding conventions, and display formatting across the BVMS maritime domain. Centralizes business vocabulary for vessel operations, estimates, voyages, invoicing, and regulatory compliance to eliminate magic strings and ensure consistent state handling.

## Business Responsibility
Owns the definitive mapping between internal domain models and industry/port authority standards (e.g., IMO port call codes, bunker ISO grades, EU ETS multipliers). Used by every calculation engine, report generator, and UI form for status transitions, unit normalization, and regulatory compliance. Changing any value here propagates directly to P&L calculations, routing scenarios, and external EDI exchanges, making it a high-priority source of truth.

---

## Members

### 1. CargoQuantityUnitEnumExtensions.getTextForPrintout — Standardizes unit abbreviations for reporting and exports
```csharp
public static string getTextForPrintout(this string CargoQuantityUnit) =>
    CargoQuantityUnit switch
{
    nameof(CargoQuantityUnitEnum.MetricTon) => "MT",
    nameof(CargoQuantityUnitEnum.Piece) => "pcs",
    nameof(CargoQuantityUnitEnum.CubicMeter) => string.Format("m{0}", (char)0xB3),
    nameof(CargoQuantityUnitEnum.Unit) => "unit",
    nameof(CargoQuantityUnitEnum.USBarrels) => "bbl",
    nameof(CargoQuantityUnitEnum.LiquidMT) => "LMT",
    nameof(CargoQuantityUnitEnum.LTons) => "LT",
    nameof(CargoQuantityUnitEnum.SquareMeter) => "m2",
    nameof(CargoQuantityUnitEnum.Revenue) => "revenue",
    nameof(CargoQuantityUnitEnum.STons) => "ST",
    _ => CargoQuantityUnit
};
```
**Explanation**: Maps internal domain unit names to legacy/industry-standard printout abbreviations. Uses Unicode `0xB3` for cubic meters to match financial reporting conventions. Falls back to the raw input if no mapping exists, preventing format crashes during PDF/CSV generation.

### 2. ReasonForVisitPortEnumExtensions.getReasonForVisitCode — Extracts legacy/port-calling code for external systems
```csharp
public static string getReasonForVisitCode(this string reason) =>
    reason switch
{
    nameof(ReasonForVisitPortEnum.Commencing) => "C",
    nameof(ReasonForVisitPortEnum.Loading) => "L",
    nameof(ReasonForVisitPortEnum.Discharging) => "D",
    nameof(ReasonForVisitPortEnum.Fueling) => "F",
    nameof(ReasonForVisitPortEnum.Passing) => "P",
    nameof(ReasonForVisitPortEnum.InTransitting) => "I",
    nameof(ReasonForVisitPortEnum.Repositioning) => "T",
    nameof(ReasonForVisitPortEnum.Waiting) => "W",
    nameof(ReasonForVisitPortEnum.Repairing) => "R",
    nameof(ReasonForVisitPortEnum.Delivery) => "Y",
    nameof(ReasonForVisitPortEnum.Redelivery) => "Z",
    nameof(ReasonForVisitPortEnum.TcoLoadingOrDischarging) => "LD",
    nameof(ReasonForVisitPortEnum.Other) => "O",
    _ => reason
};
```
**Explanation**: Converts the verbose enum name to the 1-2 character standard used in EDI, port call reports, and vessel performance logs. Critical for ensuring data sent to external terminals, agents, and routing APIs matches port authority expectations.

### 3. ReasonForVisitPortEnumExtensions.GetValueFromDescription — Reverse-lookup enum from display text via reflection
```csharp
public static ReasonForVisitPortEnum? GetValueFromDescription(string description)
{
    var type = typeof(ReasonForVisitPortEnum);
    foreach (var field in type.GetFields())
    {
        var attr = field.GetCustomAttribute<DescriptionAttribute>();
        if (attr != null &&
            string.Equals(attr.Description, description, StringComparison.OrdinalIgnoreCase))
        {
            return (ReasonForVisitPortEnum)field.GetValue(null)!;
        }
    }
    return null;
}
```
**Explanation**: Iterates enum fields at runtime to match user-facing descriptions (defined via `[Description]`) back to the underlying enum value. Used when validating UI dropdown selections or parsing external payloads that carry display text rather than raw enum integers.

### 4. TcoStatusEnum — Defines the lifecycle and validation rules for Time Charter Contracts
```csharp
public enum TcoStatusEnum
{
    /// <summary>
    /// Initial phase when a TC is created.
    /// </summary>
    Inquiry,
    /// <summary>
    /// Quoted stage before confirmation.
    /// Users can switch between Quoted and Archived manually.
    /// </summary>
    Quoted,
    /// <summary>
    /// Archived (pre-confirmation only).
    /// </summary>
    Archived,
    /// <summary>
    /// Contract confirmed after all required information is validated.
    /// Once confirmed, general data becomes read-only,
    /// and only high-access users can modify it.
    /// </summary>
    Confirmed,
    /// <summary>
    /// Automatically set if the contract is confirmed but not on a voyage,
    /// and the laycan end date has passed the current date.
    /// </summary>
    Delayed,
    /// <summary>
    /// Manually set if the contract is confirmed but not on a voyage.
    /// </summary>
    Cancelled,
    /// <summary>
    /// Automatically set when a tco is added to a voyage.
    /// </summary>
    Nominated,
    /// <summary>
    /// Automatically set when the delivery date is earlier than the current date.
    /// </summary>
    Delivered,
    /// <summary>
    /// Automatically set when the redelivery date is earlier than the current date.
    /// </summary>
    Redelivered,
    /// <summary>
    /// Automatically set when all invoices are paid.
    /// </summary>
    Completed
}
```
**Explanation**: Governs the complete TCO operational lifecycle. Enforces strict state transitions: `Confirmed` locks general data and triggers role-based edit restrictions. `Delayed`, `Nominated`, `Delivered`, and `Redelivered` are machine-triggered based on temporal and voyage-linkage checks, preventing manual status manipulation outside valid business windows.

### 5. BunkerPriceConstants — Provides default financial assumptions for emissions and cost calculations
```csharp
public const decimal DefaultEtsPriceInUsds = 85m;
public const decimal Co2MultiplierForCh4InEts = 28m;
public const decimal Co2MultiplierForN2oInEts = 265m;
public const decimal DefaultBioFuelPriceInUsds = 200.0m;
public const decimal Co2MultiplierForCh4InFuelEu = 25m;
public const decimal Co2MultiplierForN2oInFuelEu = 298m;
```
**Explanation**: Hardcoded baselines for EU ETS and FuelEU Maritime compliance engines. Directly impacts voyage P&L, carbon penalty projections, and bunker procurement benchmarks. These values align with regulatory benchmarks and should only be updated upon formal policy or market shifts.

### 6. AlternativeRouteEnum — Standardizes major maritime chokepoints and passages
```csharp
public static readonly string Suez = "Suez Canal";
public static readonly string Panama = "Panama Canal";
public static readonly string Kiel = "Kiel Canal";
public static readonly string Corinth = "Corinth Canal";
public static readonly string TorresCanal = "Torres Canal";
public static readonly string Magellan = "Magellan Strait";
public static readonly string Torres = "Torres Strait";
public static readonly string CapeHorn = "Cape Horn";
public static readonly string GoodHope = "Cape of Good Hope";
public static readonly string Skaw = "Skaw";
```
**Explanation**: Used by routing scenarios and estimate builders to reference canonical waterways. Ensures distance, transit-fee, and risk calculations reference consistent strings across voyage planners and reporting dashboards.

---

## Dependencies
- `System.ComponentModel.DataAnnotations` — Required for `[Description]` and `[Display]` attributes on enums, enabling UI binding and reflection-based reverse lookups.
- `System.Reflection` — Used exclusively by `GetValueFromDescription` to iterate enum metadata at runtime without hardcoding switch mappings.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]