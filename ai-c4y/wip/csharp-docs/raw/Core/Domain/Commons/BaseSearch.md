# BaseSearch, DynamicFilter

## Purpose
Shared domain DTOs for standardizing list/query input contracts across BVMS aggregates. `BaseSearch` defines pagination and free-text search parameters, while `DynamicFilter` carries structured field/operator/value criteria for programmatic filtering.

## Business Responsibility
These DTOs own the retrieval contract for frontend/backend list operations in Finance and Master Data modules. They decouple query parameters from underlying EF Core expressions, providing a consistent mechanism for the query pipeline to translate UI-driven search criteria into database filters. Structurally critical for all paginated list endpoints, though each invocation is stateless and low-risk.

---
## Members

### 1. KeySearch — Free-text search token
```csharp
public string? KeySearch { get; set; }
```
**Explanation**: Passes a user-entered string to the query handler. Applied via `LIKE` or full-text search across designated searchable aggregate fields. Omitting it skips the text match condition entirely.

### 2. CurrentPage — Pagination index
```csharp
public int CurrentPage { get; set; } = 1;
```
**Explanation**: Defines the page index for `Skip`/`Take` translation. Defaults to `1` to prevent zero-offset pagination errors in downstream consumers and align with UI pagination logic.

### 3. PageSize — Result batch size
```csharp
public int PageSize { get; set; } = 10;
```
**Explanation**: Defines the `Take` limit for query results. Defaults to `10` to cap memory consumption and enforce UI-driven batch sizes. Handled downstream; no clamping or validation is performed here.

### 4. Filters — Programmatic filter collection
```csharp
public List<DynamicFilter>? Filters { get; set; }
```
**Explanation**: Carries a collection of structured filter objects. The handler iterates this list to build dynamic `Where`/`OrderBy` clauses. Null by default; a populated list triggers programmatic filtering logic in the repository/query layer.

### 5. DynamicFilter Fields — Structured filter contract
```csharp
public string? FieldName { get; set; }
public string? Operator { get; set; }
public string? Value { get; set; }
public string? Sort { get; set; }
public string? Query { get; set; }
```
**Explanation**: Maps directly to dynamic LINQ/Expression builder conventions. `FieldName` targets the aggregate property, `Operator` specifies the comparison type (e.g., `eq`, `ne`, `gt`), and `Value` provides the operand. `Sort` and `Query` are optional extensions used by specific callers for ordering and secondary text matching. All fields are nullable to support optional filtering and sorting requirements across the caller base.

---
## Dependencies
`System.Collections.Generic.List<T>` — Required for holding the ordered collection of programmatic filter conditions passed to query builders.
`DynamicFilter` — Referenced type that defines the structured contract for field-based filtering; enables the query pipeline to construct dynamic expressions without hardcoding domain-specific fields.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]