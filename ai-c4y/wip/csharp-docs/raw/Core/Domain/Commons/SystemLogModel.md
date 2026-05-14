# SystemLogModel

## Purpose
Domain model representing a granular system log entry, extending `EvidenceTraceLog` with action-specific metadata, execution timing, and a collection of associated action details.

## Business Responsibility
Owns the data contract for auditing and tracing system actions. Captures the full context of an action including identity, device, performance duration, and the nested details of the action execution. Critical for audit trails and performance monitoring; serves as the persistence/transfer structure for action logs.

## Members

### ListAction — Aggregation of nested action details
```csharp
public List<ActionDetail> ListAction { get; set; }
```
**Explanation**: Container for granular detail items related to the logged action. Populated during action construction to provide a structural breakdown of the operation; persists the detailed payload in the trace entry.

### TimeExecution — Performance duration capture
```csharp
public long TimeExecution { get; set; }
```
**Explanation**: Stores execution duration for the action (likely milliseconds). Captures performance metrics for monitoring slow operations; value is calculated and populated by the action pipeline prior to log finalization.

## Dependencies
- `EvidenceTraceLog` — Base trace structure; provides core logging fields and inheritance hierarchy to ensure consistency across trace types and avoid duplication.
- `ActionDetail` — Referenced by `ListAction`; defines the structure of nested detail items included in the log entry.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]