# ActionDetail

## Purpose
Lightweight domain model for capturing granular audit/action metadata during system operations. Acts as a pure data carrier to transport context (object, user, action, and optional payload) across the Domain layer.

## Business Responsibility
Owns the structural contract for discrete action records emitted during BVMS workflows. Critical for maintaining immutable audit trails and supporting operational debugging. Specifically consumed by `SystemLogModel` to map transient action context into persistent log entries, ensuring consistent metadata formatting across all logging pathways.

---
IF DOMAIN/DTO:

## Members

### 1. CreatedDate — Audit timestamp initialization
```csharp
public DateTime? CreatedDate { get; set; } = DateTime.Now;
```
**Explanation**: Initializes a baseline creation timestamp at object instantiation while preserving nullability for explicit overrides during manual mapping or deserialization. Guarantees that every action record carries a chronological anchor even when constructed programmatically without explicit date assignment. Downstream log processors, timeline viewers, and compliance retention schedulers depend on this field for ordering and cutoff enforcement.

## Dependencies
None. This class relies exclusively on standard .NET primitives and contains no injected services, base classes, interfaces, or external framework dependencies.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]