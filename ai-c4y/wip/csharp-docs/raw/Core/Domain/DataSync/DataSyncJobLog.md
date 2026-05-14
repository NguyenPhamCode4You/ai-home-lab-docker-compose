# DataSyncJobLog

## Purpose
Represents a granular execution log entry for a specific phase within a data synchronization job. Exists to capture step-level outcomes, execution context, and diagnostic output for pipeline observability and auditability.

## Business Responsibility
Owns the persistence and state tracking for individual synchronization phases. Critical for monitoring, retry logic, and forensic analysis in the data pipeline. Each entry ties directly to one `DataSyncJob`, enabling granular progress tracking, SLA measurement, and failure isolation without polluting the parent job entity.

---
## Members

### 1. `StepName` — Identifies the specific synchronization phase (e.g., Extract, Transform, Load)
```csharp
[StringLength(50)]
public string StepName { get; set; }
```
**Explanation**: Constrained to 50 characters to enforce consistent, indexable step labels and prevent oversized payload bloat. Enforced at the domain boundary to guarantee that `SynchronizationLoggingService` and UI dashboards consume standardized phase identifiers.

### 2. `Order` — Determines execution sequence within a single `DataSyncJob`
```csharp
public int Order { get; set; }
```
**Explanation**: Numeric priority consumed by `SynchronizationBusinessBaseService` to sequence, resume, or skip phases during retry flows. Missing or out-of-order values break pipeline continuity and can cause phantom steps or corrupted execution graphs.

### 3. `Status` — Finalized outcome of the execution step
```csharp
[EnumDataType(typeof(DataSyncJobStatus))]
[StringLength(15)]
public string Status { get; set; }
```
**Explanation**: Restricted to 15 characters and locked to the `DataSyncJobStatus` enum via `[EnumDataType]`. Ensures downstream consumers (AutoMapper projections, reporting pipelines, and `SynchronizationDataService`) only read canonical, resolvable states. Prevents orphaned or undefined status values in persistence.

### 4. `CompletedTime` — Timestamp when the step finished executing
```csharp
public DateTime CompletedTime { get; set; }
```
**Explanation**: Provides precise duration calculation for performance monitoring and SLA tracking. Used by orchestrators and dashboards to compute step latency. Defaults to `DateTime` (epoch) if unassigned, but production paths always populate it on step completion.

### 5. `PayloadDatatype` — Defines the serialization format/schema for the stored data
```csharp
[StringLength(100)]
public string PayloadDatatype { get; set; }
```
**Explanation**: Caps format identifiers (e.g., JSON, CSV, ProtoBuf) to 100 characters to maintain lightweight indexing. Drives deserialization logic in downstream consumers; mismatched types cause payload read failures during audit or retry operations.

### 6. `Payload` — Stores serialized execution context or extracted data
```csharp
public string Payload { get; set; }
```
**Explanation**: Holds the actual data blob for retry deserialization, audit trails, or downstream processing. Bypasses navigation properties to keep the log entity flat and serializable for distributed tracing and database storage optimization.

### 7. `Message` — Optional error, warning, or diagnostic output
```csharp
[StringLength(500)]
public string? Message { get; set; }
```
**Explanation**: Nullable diagnostic field constrained to 500 characters to cap storage for verbose stack traces or warnings. Consumed by `SynchronizationLoggingService` for user-facing feedback and error aggregation. Skipped in successful paths to keep log rows lean.

## Dependencies
- `DataSyncJobStatus` — Enforced via `[EnumDataType]` on `Status`; domain contracts require alignment between log states and job lifecycle states.
- `DataContext` — Maps the entity for EF Core tracking and historical persistence; drives index creation on `JobId`, `Status`, and `CompletedTime`.
- `MappingProfile` — Consumed to project the entity into API DTOs and view models for monitoring dashboards.
- `SynchronizationBusinessBaseService` — Directly instantiates and populates log entries during phase execution and retry routing.
- `SynchronizationLoggingService` — Reads `Payload`, `Status`, and `Message` for audit trails, error aggregation, and UI rendering.
- `SynchronizationDataService` — Queries `Payload`/`Status` during retrieval, reprocessing, and forensic inspection.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]