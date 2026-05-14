# ConstantsTaskAlert

## Purpose
Defines strongly-typed enumerations and a static container for task, alert, and rule-set domain metadata. Provides a single source of truth for workflow states, priority levels, and routing targets across the domain.

## Business Responsibility
Owns the domain vocabulary for lifecycle states (`TaskStatusEnum`, `AlertStatus`), escalation levels (`Priority`), and entity/user routing (`TargetObjectType`, `TargetUser`). Critical for consistent state tracking, rule evaluation, and UI/domain mapping. Used as constraints in queries, domain events, and configuration without introducing runtime allocation.

---
## Members
### 1. `ConstantsTaskAlert` — Static container for domain constants (currently unused)
```csharp
public static class ConstantsTaskAlert { }
```
**Explanation**: Reserved namespace for future constant aggregation related to the task/alert subsystem. Currently empty to avoid tight coupling or premature abstraction. No side-effects.

### 2. `TargetObjectType` — Supported aggregate roots for task/alert routing
```csharp
public enum TargetObjectType { Voyage, Shipment, Estimate }
```
**Explanation**: Maps directly to the entity types that can trigger or receive task/alert workflows. Ensures rule-set evaluations only apply to valid domain aggregates and prevents cross-aggregate routing errors.

### 3. `Priority` — Escalation severity levels for alerts and tasks
```csharp
public enum Priority { Low, Medium, Important, Urgent }
```
**Explanation**: Defines the four-tier severity model used for filtering, sorting, and SLA tracking. Directly influences notification routing, dashboard grouping, and timeout thresholds.

### 4. `TargetUser` — Role-based recipients for task/alert assignment
```csharp
public enum TargetUser { Operator, RegOperatorLoading, RegOperatorDischarging, MarineAccountant, Documentor, CharteringBroker }
```
**Explanation**: Maps domain roles to specific operational responsibilities. Used by the rule engine and assignment logic to direct work items to the correct functional teams without hardcoding string lookups.

### 5. `TaskStatusEnum` — Lifecycle states for task execution
```csharp
public enum TaskStatusEnum { NotStarted, InProgress, Completed }
```
**Explanation**: Tracks progression through the task workflow. Drives UI state rendering, history logging, and completion gating for downstream processes like settlement or reporting.

### 6. `AlertStatus` — Acknowledgment state for alerts
```csharp
public enum AlertStatus { Unacknowledged, Acknowledged }
```
**Explanation**: Manages the read/acknowledged lifecycle of alerts. Prevents duplicate notifications, supports audit trails for incident response, and drives dashboard unread counters.

### 7. `RuleSetStatusEnum` — Activation state for rule definitions
```csharp
public enum RuleSetStatusEnum { Active, Inactive }
```
**Explanation**: Controls whether a rule-set participates in evaluation cycles. Allows runtime toggling without deleting rule definitions or breaking historical references in audit logs.

### 8. `RuleSetResultType` — Output classification for rule evaluations
```csharp
public enum RuleSetResultType { Task, Alert, TaskAlert }
```
**Explanation**: Specifies which downstream entity a rule-match generates. Ensures the evaluation engine routes matches to the correct creation pathway (standalone task, standalone alert, or linked pair).

---
## Dependencies
- None — Pure value-object/constants file with no external dependencies, injected services, or base classes.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]