# ChangeLog

## Purpose
Represents a single audit record capturing the state delta of any tracked domain entity. Exists to provide a centralized, queryable trail of who modified what, when, and the before/after serialized payloads.

## Business Responsibility
Owns the domain model for system-wide audit logging. Critical for compliance, forensic debugging, and operational transparency. Contains zero behavioral logic; purely a structured payload consumed exclusively by the `IChangeLogGenerator` pipeline and persisted via EF Core contexts. High write volume, read-optimized.

---

## Members

### 1. Id — Audit record primary identifier
```csharp