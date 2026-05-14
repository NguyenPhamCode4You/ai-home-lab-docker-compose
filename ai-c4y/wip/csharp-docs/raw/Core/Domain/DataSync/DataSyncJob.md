# DataSyncJob

## Purpose
Core domain entity representing a data synchronization job record. Tracks job configuration, execution timestamps, lifecycle state, and serialized payload for the BVMS data synchronization pipeline.

## Business Responsibility
Owns the state and configuration contract for all system-initiated data sync operations. Critical for job tracking, retry/reverse workflows, and dashboard reporting. Acts as the authoritative state carrier between the data sync service layer and downstream processing components (`SynchronizationDataService`, `DataSyncJobService`).

---

## Members
*Note: This entity contains only simple auto-properties. The following fields carry enum validation constraints or drive sync routing/state-machine logic.*

### 1. SynchronizationType — Enum constraint defining target module
```csharp
[EnumDataType(typeof(SynchronizationType))]
[StringLength(50)]
public string SynchronizationType { get; set; }
```
**Explanation**: Stores the target system as a string but validated against `SynchronizationType`. Enforces that only registered sync targets are accepted, preventing routing failures in `SynchronizationDataService` and policy evaluation in `Policies.cs`.

### 2. SynchronizeDirection — Enum constraint defining sync flow direction
```csharp
[EnumDataType(typeof(SynchronizationDirection))]
[StringLength(10)]
public string SynchronizeDirection { get; set; }
```
**Explanation**: Captures bidirectional flow intent (e.g., Inbound/Outbound). Required by `Policies.cs` and job handlers to apply direction-specific transformation and authorization rules during execution.

### 3. Source — Enum constraint identifying origin system
```csharp
[EnumDataType(typeof(SynchronizationSource))]
[StringLength(15)]
public string Source { get; set; }
```
**Explanation**: Specifies the originating application. Used by `GetDataSyncJobById` and `SearchDataSyncJob` to route queries and validate source-destination pairing before dispatch.

### 4. Status — Enum constraint tracking job lifecycle state
```csharp
[EnumDataType(typeof(DataSyncJobStatus))]
[StringLength(15)]
public string Status { get; set; }
```
**Explanation**: Core state machine field (e.g., Pending, Running, Completed, Failed). Dictates workflow branching in `RetriggerDataSyncJob` and `ReverseDataSyncJob`. Enforced by `DataSyncJobStatus` enum to maintain transactional consistency and prevent invalid state transitions.

### 5. StartTime / CompletedTime / RecordedTime — Timestamps tracking execution window
```csharp
public DateTime StartTime { get; set; }
public DateTime CompletedTime { get; set; }
public DateTime RecordedTime { get; set; } = DateTime.UtcNow;
```
**Explanation**: `RecordedTime` defaults to UTC now at instantiation to anchor creation. `StartTime` and `CompletedTime` mark the active execution window. Used for SLA tracking, retry backoff calculations, and audit trails in `GetSyncStatusById` and `SearchSyncStatus`.

### 6. Payload / PayloadDatatype — Container for serialized sync data
```csharp
public string Payload { get; set; }
[StringLength(200)]
public string PayloadDatatype { get; set; }
```
**Explanation**: `Payload` holds the serialized business data to be processed. `PayloadDatatype` indicates serialization format. Consumed directly by `SynchronizationDataService` to deserialize and execute the actual data mutation against the target system.

---

## Dependencies
- `SynchronizationType` / `SynchronizationDirection` / `SynchronizationSource` / `DataSyncJobStatus` — Enum types referenced by `[EnumDataType]` attributes to enforce strict validation on the string-backed fields. Required by AutoMapper mapping profile and sync service to cast/compare against known state/values.
- `System.ComponentModel.DataAnnotations` — Provides validation attributes used by EF Core model configuration and API request validation pipelines.
- `DateTime` / `Guid` — Core types for identity and temporal tracking.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]