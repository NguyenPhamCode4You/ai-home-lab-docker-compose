# DataSync DTOs

## Purpose
Defines the read-side data contracts for the data synchronization module. Provides flattened, query-friendly views of sync job execution, granular logs, and entity-level sync status without carrying infrastructure or tracking overhead.

## Business Responsibility
Owns the query/response shapes for data sync monitoring and debugging. Critical for DaDesk job tracking, support incident troubleshooting, and API surfaces exposing sync progress. Read-only impact; used exclusively in projection paths and dashboard rendering.

---

## Members

### 1. `SynchronizationType` — Identifies the sync provider or mechanism used
```csharp
public string SynchronizationType { get; set; }
```
**Explanation**: Classifies the integration source (e.g., `Force`, `EDI`, `Internal`). Drives routing logic in monitoring pipelines and allows filtering jobs by system origin. Must align with registered sync provider enums.

### 2. `SynchronizeDirection` — Dictates data flow orientation
```csharp
public string SynchronizeDirection { get; set; }
```
**Explanation**: Specifies whether data moves `Source→Target` or `Target→Source`. Required for correct audit trails and for handlers that branch logic based on data ownership.

### 3. `Status` — Current lifecycle state of the job
```csharp
public string Status { get; set; }
```
**Explanation**: Tracks progression (`Pending`, `Running`, `Completed`, `Failed`, `RolledBack`). UI components and downstream status aggregators poll this field to update dashboards and trigger retry workflows.

### 4. `StartTime` & `CompletedTime` — Job duration boundaries
```csharp
public DateTime StartTime { get; set; }
public DateTime CompletedTime { get; set; }
```
**Explanation**: `StartTime` marks handler entry; `CompletedTime` marks exit or failure. Used to calculate execution duration, detect timeouts, and enforce SLA monitoring. Nullable/zero checks handled by callers.

### 5. `ExecutionCount` — Retry attempt counter
```csharp
public int ExecutionCount { get; set; }
```
**Explanation**: Increments on transient failures. Enforces max-retry limits and helps diagnose flaky endpoints versus permanent business validation failures.

### 6. `Payload` & `PayloadDatatype` — Serialized data and format metadata
```csharp
public string Payload { get; set; }
public string PayloadDatatype { get; set; }
```
**Explanation**: `Payload` holds the raw JSON/CSV/record data for the sync operation. `PayloadDatatype` tells the deserializer how to parse it. Retained for forensic debugging when transformations fail mid-pipeline.

### 7. `DataSyncJobLogs` — Step-level execution history
```csharp
public List<DataSyncJobLogDto> DataSyncJobLogs { get; set; } = [];
```
**Explanation**: Denormalized collection of sub-steps for a single job. Enables drill-down debugging without cross-table joins. Initialized to empty collection to prevent null-reference in UI consumers.

### 8. `StepName` & `Order` — Pipeline stage identity and sequencing
```csharp
public string StepName { get; set; }
public int Order { get; set; }
```
**Explanation**: `StepName` maps to defined pipeline phases (e.g., `Validate`, `Transform`, `Push`). `Order` guarantees chronological reconstruction of the job's processing history for replay or audit.

### 9. `Message` — Contextual error or informational text
```csharp
public string? Message { get; set; }
```
**Explanation**: Captures exception details, provider rejection codes, or validation notes. Nullable; optional for successful steps. Primary source for automated alerting and support ticket generation.

### 10. `ForceSupport` — Override bypass flag
```csharp
public bool ForceSupport { get; set; } = false;
```
**Explanation**: When `true`, signals the sync handler to skip standard validation/routing and prioritize reconciliation. Used for manual data fixes or emergency overrides. Defaults to `false` to prevent accidental bypass.

### 11. `EntityId` & `Identifier` — Target business entity reference
```csharp
public Guid EntityId { get; set; }
public string Identifier { get; set; }
```
**Explanation**: Primary keys for tracking sync state per business entity (Invoice, Voyage, etc.). `Identifier` provides human-readable or external-system reference. Used to group jobs under a single entity view.

### 12. `LastJobStatus` & `RecordedTime` — Aggregate sync health snapshot
```csharp
public string LastJobStatus { get; set; }
public DateTime RecordedTime { get; set; }
```
**Explanation**: Cached summary of the most recent job state for this entity. Drives "last synced X minutes ago" indicators and stale-data alerts. Updated on job completion/failure.

### 13. `EntityLastSyncedDate` — Success boundary timestamp
```csharp
public DateTime? EntityLastSyncedDate { get; set; }
```
**Explanation**: Only updates on successful syncs. Defines the reconciliation window and distinguishes between "never synced" and "sync failed". Nullable until first success.

### 14. `VoyageId`, `TimeCharterId`, `LaytimeGroupId`, `InvoiceType`, `InvoiceNo` — Commercial context bindings
```csharp
public Guid? VoyageId { get; set; } = null;
public Guid? TimeCharterId { get; set; } = null;
public Guid? LaytimeGroupId { get; set; } = null;
public string? InvoiceType { get; set; } = null;
public string? InvoiceNo { get; set; } = null;
```
**Explanation**: Bridges sync status to financial/voyage domains. Enables filtering and aggregation by commercial contracts. Nullable to accommodate non-invoice sync types without schema pollution.

### 15. `DataSyncJobs` — Aggregated job history for detail views
```csharp
public List<DataSyncJobDto> DataSyncJobs { get; set; } = [];
```
**Explanation**: Denormalizes related jobs into the status DTO for list/detail screens. Eliminates N+1 queries by prefetching job records scoped to `EntityId`. Initialized to empty collection for safe UI binding.

---

## Dependencies
- `IdBasedDto` — Base class inherited by `ForceSupportDto`; provides the `Id` property baseline ensuring consistent primary key handling across all sync entities.
- `List<T>` — Standard generic collection used for `DataSyncJobLogs` and `DataSyncJobs`; avoids EF Core change-tracking overhead and lazy-loading traps in DTO projection paths.
- *(No injected services, external clients, or heavy infrastructure dependencies. Pure data contracts.)*

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]