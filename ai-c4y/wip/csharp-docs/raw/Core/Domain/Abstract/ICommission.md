# ICommission

## Purpose
Defines the contract for commission data transfer and domain entities across Voyage Management and Time Charter modules. Serves as the shared abstraction for AutoMapper profiles, DTOs, and calculation helpers.

## Business Responsibility
Central data contract for commission definitions. Enables polymorphic handling of commissions across Estimate, Shipment, and Time Charter contexts. Critical for consistent mapping, storage, and processing of financial rates, currency conversions, and partner associations.

---
IF OTHER (helper/extension/utility):

## Members
No members with non-trivial logic. All properties are simple accessors defining the commission data schema.

## Dependencies
None. Relies only on standard primitive types.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]