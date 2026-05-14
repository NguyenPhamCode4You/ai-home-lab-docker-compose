**FILE TYPE IDENTIFICATION**: DOMAIN/DTO

# Response & Pagination DTOs

## Purpose
Defines the standardized response envelope, pagination metadata, HTTP status code enum, and auxiliary result models used across the BVMS domain layer to encapsulate API responses, tracking updates/deletions, and scroll-based search results.

## Business Responsibility
Owns the contract for all domain-to-adapter responses. Critical for maintaining consistent error handling (`ResponseError`), typed data wrapping (`ResponseObject<T>`, `ResponseList<T>`), and pagination metadata (`Pagination<T>`). Called by export services, import synchronizers, and audit/history handlers to structure outgoing data without leaking infrastructure concerns into the domain.

---
## Members

### 1. Response — Base response envelope
```csharp
public Response(Code code, string message) { Code = code; Message = message; }
public Response(string message) { Message = message; }
public Response() { }
public Code Code { get; set; } = Code.Success;
public string Message { get; set; } = "Thành công";
public long RequestDuration { get; set; }
```
**Explanation**: Establishes the baseline contract for all API responses. Defaults to `Success` and a localized success message. `RequestDuration` captures execution time for telemetry and SLA monitoring. Inherits `EvidenceTraceLog` to automatically propagate audit trails across all responses.

### 2. ResponseError — Structured error payload
```csharp
public IList<Dictionary<string, string>> ErrorDetail { get; set; }
```
**Explanation**: Carries field-level or validation-specific error dictionaries. Enables clients to map localized validation messages directly to form fields without parsing generic exception strings or relying on brittle message patterns.

### 3. Pagination<T> — Grid/endpoint pagination state
```csharp
public Pagination() { Size = 20; Page = 1; }
public int Page { get; set; }
public int TotalPages { get; set; }
public int Size { get; set; }
public int NumberOfElements { get; set; }
public int TotalElements { get; set; }
public IEnumerable<T> Content { get; set; }
```
**Explanation**: Defines the complete state required for UI pagination controls. Defaults to page 1/size 20. `TotalElements` vs `NumberOfElements` distinguishes between the database total count and the current page result count, preventing frontend miscalculations when filters are applied dynamically.

### 4. ResponseUpdate / ResponseDelete — Single-entity mutation confirmations
```csharp
public ResponseUpdate(Guid id) { Data = new ResponseUpdateModel { Id = id }; }
public ResponseDelete(Guid id, string name) { Data = new ResponseDeleteModel { Id = id, Name = name }; }
```
**Explanation**: Standardizes mutation outcomes. Carries the affected entity’s ID and, for deletions, its name for audit UI confirmation. Decouples domain business logic from UI-specific success messages and ensures consistent response shaping across CUD operations.

### 5. ResponseScroll<T> — Search context & highlight preservation
```csharp
public string ScrollId { get; set; }
public string ScrollTime { get; set; }
public List<string> ListHighlightOtherField { get; set; }
```
**Explanation**: Preserves low-level search engine context (`ScrollId`, `ScrollTime`) to resume deep pagination without re-executing expensive filters. `ListHighlightOtherField` returns matched text snippets for UI rendering, enabling instant visual feedback during complex search workflows.

### 6. ResponeDeleteModel / ResponeUpdateItemsModel — Batch operation status
```csharp
public bool Result { get; set; }
public string Message { get; set; }
```
**Explanation**: Used for multi-item operations where individual records may succeed or fail independently. `Result` flags allow granular UI rendering (partial success states) rather than triggering a blanket API failure, improving user experience during bulk imports/exports.

### 7. BaseObject — Audit metadata carrier
```csharp
public DateTime Modified { get; set; }
public string Modifier { get; set; }
```
**Explanation**: Base class for domain entities requiring last-modified tracking. Ensures consistent audit timestamps and user identifiers across writable models, feeding directly into compliance and history retrieval services.

### 8. Code — HTTP status mapping
```csharp
public enum Code { Success = 200, Created = 201, BadRequest = 400, Unauthorized = 401, Forbidden = 403, NotFound = 404, MethodNotAllowed = 405, Conflict = 409, ServerError = 500 }
```
**Explanation**: Maps domain operations to standard HTTP semantics. Ensures consistency across API contracts and enables frontend routing/error handling based on status codes without relying on string matching or magic numbers.

### 9. DropdownListModel / PaginationList<T> — UI renderers
```csharp
public Guid Id { get; set; }
public string Name { get; set; }
// PaginationList<T>
public int PageNumber { get; set; }
public int PageSize { get; set; }
public int TotalCount { get; set; }
public int DataCount { get; set; }
public List<T> Data { get; set; }
```
**Explanation**: `DropdownListModel` strips domain complexity to lightweight ID/Name pairs for form selects, preventing payload bloat. `PaginationList<T>` provides a flatter, UI-optimized pagination structure (using `PageNumber`/`PageSize`) for frontend grids that lack full envelope support.

---
## Dependencies
- `EvidenceTraceLog` — Inherited by `Response` to automatically attach audit/context metadata without duplicating trace logic in the domain layer.
- `Pagination<T>` — Consumed by `ResponsePagination<T>` and `ResponseScroll<T>` to unify cursor/page-based navigation contracts.
- `Code` — Enum used across all response wrappers to enforce consistent HTTP status signaling without string parsing.
- `IList<T>` / `IEnumerable<T>` / `List<T>` — Generic collection types used to maintain type safety while decoupling DTOs from specific ORM or EF projections.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]