# BaseQueryFilterModel

## Purpose
Defines the base contract for paginated and filtered list requests. Centralizes pagination, sorting, and status filtering parameters to ensure consistent query shaping across the domain.

## Business Responsibility
Owns the contract for generic list/view operations that require pagination and filtering. It standardizes how API consumers express search scope, page boundaries, sort direction, and active/inactive filtering. Critical for maintaining consistent UI experience and predictable query performance across all aggregate list endpoints.

---

## Members

### 1. `PropertyName` — Default sort target for list queries
```csharp
public string PropertyName { get; set; } = "CreatedDate";
```
**Explanation**: Defines the default entity field used for ordering when the client omits sort instructions. Ensures deterministic result ordering and prevents database-level undefined sort behavior when combined with `Ascending`.

### 2. `Ascending` — Default sort direction
```csharp
public string Ascending { get; set; } = "desc";
```
**Explanation**: Controls sort direction string passed to query builders. Defaults to descending to show latest records first, aligning with typical audit/list view expectations. Must be paired with `PropertyName` to form a valid sort clause.

### 3. Constructor — Initializes default pagination to domain conventions
```csharp
public BaseQueryFilterModel()
{
    PageNumber = QueryFilter.DefaultPageNumber;
    PageSize = QueryFilter.DefaultPageSize;
}
```
**Explanation**: Overrides implicit default value of `0` for `int` properties to prevent negative/zero page indexing. Directly references the centralized `QueryFilter` configuration to ensure all list operations respect the agreed-upon maximum page size and baseline pagination offset.

---

## Dependencies
- `QueryFilter` — References its `DefaultPageNumber` and `DefaultPageSize` to enforce domain-wide pagination constraints instead of using hardcoded literals.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]