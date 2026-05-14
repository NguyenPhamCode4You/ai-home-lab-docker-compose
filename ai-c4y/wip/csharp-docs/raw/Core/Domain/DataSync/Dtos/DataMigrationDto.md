# DataMigrationRequestDto

## Purpose
Defines the request and response payloads for the data synchronization pipeline. Exists to enforce a consistent, versionable contract between the API controller, business services, and downstream migration processors.

## Business Responsibility
Serves as the state carrier for migration executions. Low-impact structural DTOs that track execution mode (`DryRun`), aggregate progress (`TotalRecords`, `RecordsUpdated`), and decompose sync outcomes by strategy. Critical for API contract stability and auditability, but contain zero business logic.

---
## Members
### 1. DryRun — Controls simulation vs. execution mode
```csharp
public bool DryRun { get; set; } = true;
```
**Explanation**: Defaults to `true` to enforce safe preview behavior. Set to `false` only when explicitly authorizing actual data mutations. Prevents accidental writes during integration or ad-hoc testing.

### 2. TotalRecords — Baseline dataset size
```csharp
public int TotalRecords { get; set; }
```
**Explanation**: Captures the full scope of records identified for processing. Serves as the denominator for progress calculations and percentage metrics downstream.

### 3. RecordsNeedingMigration — Filtered workload count
```csharp
public int RecordsNeedingMigration { get; set; }
```
**Explanation**: Represents records that actually require sync logic (excluding already aligned records). Used to scope processing effort and track filtered throughput.

### 4. RecordsUpdated — Committed mutation counter
```csharp
public int RecordsUpdated { get; set; }
```
**Explanation**: Tracks successfully persisted changes. Used for completion reporting and success-rate validation against `RecordsNeedingMigration`.

### 5. IsDryRun — Execution mode echo
```csharp
public bool IsDryRun { get; set; }
```
**Explanation**: Mirrors the request mode into the response for audit trails and client-side UI state synchronization.

### 6. MatchingStrategies — Strategy breakdown collection
```csharp
public List<DataMigrationStrategyDto> MatchingStrategies { get; set; } = new();
```
**Explanation**: Populated with `DataMigrationStrategyDto` instances to detail how records were mapped. Default empty collection prevents null-reference errors during JSON serialization and UI rendering.

### 7. Statistics — Extensible counter map
```csharp
public Dictionary<string, int> Statistics { get; set; } = new();
```
**Explanation**: Holds arbitrary key-value metrics (e.g., `skipped`, `conflicted`, `matched`). Default empty dictionary ensures safe serialization and allows incremental metric additions without DTO versioning.

### 8. LinkType — Mapping rule classification
```csharp
public string LinkType { get; set; } = string.Empty;
```
**Explanation**: Categorizes the synchronization relationship (e.g., `MasterData`, `Transaction`). Defaults to empty string to satisfy JSON contract requirements without forcing callers to guess.

### 9. Strategy — Assigned sync algorithm identifier
```csharp
public string Strategy { get; set; } = string.Empty;
```
**Explanation**: Names the specific matching/updating algorithm applied to the record set. Enables clients to distinguish between strategy variants (e.g., `ExactMatch`, `FuzzySearch`).

### 10. RecordCount — Strategy-specific volume
```csharp
public int RecordCount { get; set; }
```
**Explanation**: Number of records processed by this specific `LinkType`/`Strategy` pair. Used for granular progress tracking and load balancing analysis.

### 11. Percentage — Strategy coverage ratio
```csharp
public decimal Percentage { get; set; }
```
**Explanation**: Represents the proportion of `TotalRecords` handled by this strategy. Defaults to `0` (implicit) and is calculated downstream to normalize reporting across varying dataset sizes.

---
## Dependencies
`DataMigrationStrategyDto` — Required to structure the `MatchingStrategies` list and maintain type-safe composition between request/result DTOs without circular references.
*(No injected services or external dependencies; strictly internal domain contracts.)*

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]