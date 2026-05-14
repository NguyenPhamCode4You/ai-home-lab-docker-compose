# BusinessRuleDto / BusinessRuleUpdateDto

## Purpose
Data transfer contracts for reading, creating, and updating BVMS financial business rules. Decouple domain configuration payloads from persistence models and API surface.

## Business Responsibility
Owns the configuration payload for finance business rules that drive billing, accounting, and intercompany reconciliation. Critical for master data integrity; all CRUD operations for business rules serialize to/from these DTOs. `BusinessRuleUpdateDto` specifically isolates mutation requests to prevent accidental overwrites of unmodifiable identity fields.

---

## Members
No computed fields, fallback chains, or domain logic. All members