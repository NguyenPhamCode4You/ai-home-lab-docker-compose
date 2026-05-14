# Logs

## Purpose
Direct-mapping domain entity for persisting application-level log entries. Exists to expose structured telemetry (level, message, exception details, timestamp) to the persistence layer without encapsulating business workflow.

## Business Responsibility
Captures and stores diagnostic/application telemetry for system observability and troubleshooting. Low criticality to core transactional paths, but essential for backend diagnostics and integration test/report generation workflows.

---
## Members
### 1. StackTrace — Explicit DB column type override
```csharp
[Column(TypeName = "text")] public string? StackTrace {get;set;}
```
**Explanation**: Forces the persistence provider to map this property to a `TEXT` database column, preventing `VARCHAR` truncation on deep call stacks and ensuring cross-DB compatibility. All other properties are direct state-carrier auto-properties with zero business logic.

---
## Dependencies
`System.ComponentModel.DataAnnotations.Schema` — Required solely for the `[Column]` attribute to control ORM persistence schema generation for the `StackTrace` field. No injected services, interfaces, or domain dependencies.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]