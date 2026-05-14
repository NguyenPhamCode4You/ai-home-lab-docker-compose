# BunkerTypeConstants

## Purpose
Centralizes baseline configuration values for ECA and Non-ECA bunker types, pricing, and initial quantities. Exists to eliminate magic numbers across seeding helpers, lot calculators, and default fallback logic.

## Business Responsibility
Owns the immutable default footprint for bunker lot initialization and voyage data seeding. Critical for consistent inventory baselines and cost estimation before live pricing or manual overrides are applied. Directly supports legacy type mapping (MGL→LSMGO, LSF→VLSFO) to maintain historical parity during automated seeding and codebase refactors.

---

## Members

### 1. DefaultEcaBunkerType / DefaultNormalBunkerType — Active and legacy bunker type codes
```csharp
public static readonly string DefaultEcaBunkerType = BunkerTypeCodeEnum.LSMGO; // old: MGL
public static readonly string DefaultNormalBunkerType = BunkerTypeCodeEnum.VLSFO; // old: LSF
```
**Explanation**: Anchors the system-default fuel specifications for ECA-compliant and standard zones. Ties directly to `BunkerTypeCodeEnum` to preserve domain type safety while retaining backward-compatible aliases for reporting and database seeding. Callers like `BunkerLotCodeHelper` and seeding services use these to auto-populate lot type fields without requiring explicit user selection.

### 2. DefaultEcaBunkerPrice / DefaultNormalBunkerPrice — Baseline cost per unit
```csharp
public static readonly decimal DefaultEcaBunkerPrice = 600;
public static readonly decimal DefaultNormalBunkerPrice = 500;
```
**Explanation**: Provides the initial monetary baseline for bunker costing in the system's base currency. Prevents zero/null propagation in financial calculations during lot creation and voyage planning. Serves as the fallback rate for cost projections until real-time pricing or contract-specific rates are resolved.

### 3. DefaultEcaBunkerInitQuantity / DefaultNormalBunkerInitQuantity — Starting volume thresholds
```csharp
public static readonly decimal DefaultEcaBunkerInitQuantity = 100;
public static readonly decimal DefaultNormalBunkerInitQuantity = 200;
```
**Explanation**: Defines the initial fuel inventory injected into new bunker lots by default. Establishes a consistent starting point for consumption tracking, voyage planning, and seeding pipelines (`BunkerChainSeedingService`, `BunkerOnboardSeedingService`). Eliminates scattered hardcoding across multiple initialization paths.

---

## Dependencies
`BunkerTypeCodeEnum` — Referenced to bind constant values to the domain's canonical fuel type enumeration; ensures type safety and aligns defaults with the single source of truth for bunker specifications.

*(No DI services, interfaces, or base classes are used. Primitives are omitted per convention.)*

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]