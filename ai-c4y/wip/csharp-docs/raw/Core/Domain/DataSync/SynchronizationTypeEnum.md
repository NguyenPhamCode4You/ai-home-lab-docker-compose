# SynchronizationTypeMapping

## Purpose
Centralized registry mapping synchronization event types to their source system and direction. Provides filtered string lists for specific sync categories used by monitoring, logging, and status aggregation services.

## Business Responsibility
Owns the canonical definition of how BVMS, Business Central, and DaDesk interact during data synchronization. Acts as the single source of truth for job routing, direction enforcement, and status categorization. Critical for accurate job monitoring, failure tracking, and downstream processor logic across the synchronization pipeline.

---

## Members

### SyncTypeMap — Canonical Type-to-Source/Direction Registry
```csharp
public static readonly Dictionary<SynchronizationType, (SynchronizationSource, SynchronizationDirection)> SyncTypeMap = new() { ... }
```
**Explanation**: Maps every `SynchronizationType` enum value to a tuple of target source and direction. Consumed by job processors to determine API routing and by status/monitoring services to categorize jobs. Omitting a type here breaks routing and prevents the job from being recognized or tracked.

### ImportDaSyncTypes — DaDesk Import Type Index
```csharp
public static readonly List<string> ImportDaSyncTypes = [ nameof(SynchronizationType.ImportPDA), nameof(SynchronizationType.ImportADR), nameof(SynchronizationType.ImportAPR), nameof(SynchronizationType.ImportFDA), nameof(SynchronizationType.ImportPSDA), nameof(SynchronizationType.ImportSDA), nameof(SynchronizationType.ImportVI), nameof(SynchronizationType.ImportPVI), ];
```
**Explanation**: Filtered list of DaDesk import events. Enables fast filtering and categorization for monitoring dashboards and logging services tracking inbound DaDesk jobs.

### ExportInvoiceSyncTypes — BVMS Invoice Export Index
```csharp
public static readonly List<string> ExportInvoiceSyncTypes = [ nameof(SynchronizationType.ExportInvoice), nameof(SynchronizationType.ExportReverseInvoice) ];
```
**Explanation**: Explicit list of BVMS outbound invoice sync types. Used by reconciliation and financial export tracking to aggregate status without parsing full job payloads.

### ImportInvoiceSyncTypes — BC Invoice Import Index
```csharp
public static readonly List<string> ImportInvoiceSyncTypes = [ nameof(SynchronizationType.ImportInvoice), nameof(SynchronizationType.ImportReverseInvoice) ];
```
**Explanation**: Explicit list of Business Central inbound invoice sync types. Maintains parity with the export list for end-to-end invoice synchronization visibility and failure isolation.

### ForceCreate / ForceUpdate — DTO Override Flags
```csharp
public bool ForceCreate { get; set; } = false;
public bool ForceUpdate { get; set; } = false;
```
**Explanation**: Flags injected into downstream sync processors to bypass standard upsert conflict resolution. `ForceCreate` takes explicit priority over `ForceUpdate` (per domain comment), ensuring records are inserted as new even when duplicates exist. Prevents silent skips during migration, retry, or forced re-sync scenarios.

---

## Dependencies
- `SynchronizationType` — exhaustive enum defining all recognized sync events; missing entries break the pipeline registry.
- `SynchronizationDirection` / `SynchronizationSource` — tuple values consumed by routing logic and job categorization.
- `DataSyncJobStatus` — referenced by callers (`GetSyncStatusById`, `SearchSyncStatus`) to classify job lifecycle states against mapped sync types.
- `ForceExportableDto` — passed to processors to override default conflict resolution during sync operations.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]