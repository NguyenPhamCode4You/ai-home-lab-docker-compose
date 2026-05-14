# ChangeDetailDto

## Purpose
Acts as a lightweight data carrier for representing a single field-level modification (field name, original value, and new value) during audit trail and changelog generation.

## Business Responsibility
Owned exclusively by the domain changelog infrastructure (Shipment, Tco, and Voyage change log generators). It serves as the atomic unit for diff tracking, ensuring every modified entity property is captured consistently for downstream audit consumption. Low-complexity carrier with zero business logic.

---
## Members
Contains only trivial auto-properties (`FieldName`, `OriginalValue`, `NewValue`). All are skipped per documentation guidelines as they lack computed logic, fallback chains, or domain behavior.

## Dependencies
None (pure data carrier; population and serialization are handled by the consuming changelog infrastructure).

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]