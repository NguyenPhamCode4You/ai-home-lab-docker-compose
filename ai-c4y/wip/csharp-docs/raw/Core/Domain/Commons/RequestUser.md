# RequestUser

## Purpose
Represents the identity and context of the authenticated user initiating a business operation. Acts as a carrier for user claims and distributed tracing metadata passed through CQRS commands.

## Business Responsibility
Owns the transport of user identity (`UserId`, `UserName`) and request telemetry (`TraceId`) to command handlers. Essential for audit logging, user-scoped permission checks, and distributed trace correlation in the SednaEmail workflow.

---
IF DOMAIN/DTO:

## Members

### 1. TraceId — Auto-generated unique request identifier
```csharp
public string TraceId { get; set; } = Guid.NewGuid().ToString();
```
**Explanation**: Assigns a fresh GUID string immediately upon instantiation. Guarantees a valid trace ID exists for logging and auditing even if the consumer does not explicitly provide one. Critical for correlating log spans across async operations in the SednaEmail commands.

---
## Dependencies
None.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]