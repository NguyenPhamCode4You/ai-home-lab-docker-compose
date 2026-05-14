# EstimateCreatedFromVoyageExtensions

## Purpose
Provides a domain-level extension method to evaluate whether an estimate originated from a voyage. Encapsulates the `VoyageId` null-check to keep calling code expressive and decoupled from DTO internals.

## Business Responsibility
Low-impact utility owned by the domain layer to branch logic for voyage-sourced estimates. It owns no state, side-effects, or transactions; its sole responsibility is exposing the voyage-association flag through a readable API. Critical for downstream features like voyage linkage validation, estimate duplication prevention, or pricing rule gating, but carries zero computational cost.

## Members
### 1. IsCreatedFromVoyage — Determines voyage association
```csharp
public static bool IsCreatedFromVoyage(this EstimateCrudDto estimate)
{
    return estimate.VoyageId.HasValue;
}
```
**Explanation**: Checks if the `VoyageId` property is non-null. Returns `true` when the estimate was explicitly linked to a voyage during creation. Used to branch business rules that should only apply to voyage-backed estimates, preventing null reference exceptions in calling code and abstracting away direct property access from domain services.

## Dependencies
- `EstimateCrudDto` — Required to extend the estimate DTO; references the `VoyageId` field that determines voyage linkage and drives downstream voyage-association logic.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]