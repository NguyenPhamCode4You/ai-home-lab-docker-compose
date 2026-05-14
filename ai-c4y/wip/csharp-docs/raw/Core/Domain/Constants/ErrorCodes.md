# ErrorCode

## Purpose
Centralized enumeration of standardized error codes and their human-readable descriptions across the BVMS domain. Serves as the single source of truth for application-level failure states, enabling consistent API error responses, structured logging, and frontend error mapping.

## Business Responsibility
Owns the complete taxonomy of domain, commercial, and infrastructure failure points (voyage, TCO/TCI, laytime, invoicing, shipments, bunkers, snapshots, and identity). Critical for maintaining predictable error contracts across all API endpoints and background processes. Prevents scattered or inconsistent error messaging by forcing every handler to map outcomes to a predefined, versioned code. High-impact constant: modifications require cross-cutting review due to broad consumer base; additions are low-risk if they follow existing naming and description conventions.

---
## Members
*(Grouped by declaration region; each maps to a specific business constraint or lifecycle guard)*

### Global & Infrastructure
### TEST_ERROR_WITH_DESCRIPTION — Diagnostic test flag
```csharp
TEST_ERROR_WITH_DESCRIPTION
```
**Explanation**: Used in unit/integration tests to verify error parsing and Description attribute reflection. Provides a known payload for UI/test harness validation.

### TEST_ERROR_WITHOUT_DESCRIPTION — Fallback test flag
```csharp
TEST_ERROR_WITHOUT_DESCRIPTION
```
**Explanation**: Validates that the error contract degrades gracefully when no human-readable description is provided, ensuring backend logging still functions.

### FEATURE_DISABLED — Feature flag block
```csharp
FEATURE_DISABLED
```
**Explanation**: Triggers when a domain feature is toggled off at runtime. Forces graceful degradation rather than throwing unhandled exceptions.

### UNCATCHED_EXCEPTION — System-wide failure fallback
```csharp
UNCATCHED_EXCEPTION
```
**Explanation**: Captures exceptions escaping all handler layers. Ensures the API never returns 200/500 raw stack traces; instead returns a structured, safe response.

### API_ERROR — External API fault signal
```csharp
API_ERROR
```
**Explanation**: Wraps failures originating from third-party integrations or upstream services. Decouples external volatility from internal domain logic.

### MODEL_VALIDATION_ERROR — FluentValidation chain failure
```csharp
MODEL_VALIDATION_ERROR
```
**Explanation**: Returned when request DTOs fail `RuleFor` chains. Triggers 400 Bad Request with client-editable guidance; bypasses domain processing entirely.

### USER_NOT_FOUND, ROLE_NOT_FOUND, USER_ALREADY_EXISTS, CREATE_USER_FAILED, INVALID_CREDENTIALS, INVALID_REFRESH_TOKEN, INVALID_TOKEN, INVALID_USER — Identity & Auth guards
```csharp
USER_NOT_FOUND
```
**Explanation**: Covers the complete ASP.NET Core Identity/OIDC failure surface. Maps directly to authentication/authorization middleware outcomes and token lifecycle errors.

### INVALID_REQUEST — Base request contract violation
```csharp
INVALID_REQUEST
```
**Explanation**: Catches malformed HTTP verbs, missing headers, or deserialization failures before MediatR routing.

### DATA_INVALID, CREATE_OR_UPDATE_FALSE, DELETE_FAILED, DATA_ALREADY_EXIST — Generic CRUD outcomes
```csharp
DATA_INVALID
```
**Explanation**: Used when a specific domain code is unnecessary. Signals repository-layer failures or EF Core `SaveChanges` constraints without leaking DB schema details.

### STATUS_CHANGE_FORBIDDEN, FORBIDDEN, CONCURRENCY_CONFLICT, SEQUENCE_CONFLICT — State & concurrency locks
```csharp
STATUS_CHANGE_FORBIDDEN
```
**Explanation**: Enforces entity lifecycle immutability, RBAC restrictions, and optimistic concurrency (`ConcurrencyStamp`/row version) violations. Prevents data races in multi-user editing.

### LAT_LONG_NOT_FOUND, INSUFFICENT_CONSUMPTION_DATA, MISSING_IDLE_OR_CARGO_OPS_CONSUMPTION, INSUFFICENT_BUNKER_CHAINS_DATA, SELECTED_BUNKER_IS_NOT_CORRECT, MISSING_BUNKER_LOT_IN_CONSUMPTION_EVENT — Maritime data completeness guards
```csharp
LAT_LONG_NOT_FOUND
```
**Explanation**: Validates that voyage economics calculations have required spatial and consumption model data. Stops cost estimation and bunker allocation before invalid math propagates.

### INTERGRATION_ERROR, VOYAGE_DATA_INVALID, INVALID_UPDATE, VESSEL_REPORT_VALIDATION_ERROR, INVALID_VESSEL_REPORT_TYPE — External sync & reporting gates
```csharp
INTERGRATION_ERROR
```
**Explanation**: Wraps ETL/pipeline failures, vessel report schema mismatches, and update payload contradictions. Protects the voyage aggregate from corrupted external feeds.

### BUNKER_ORDER_LIFTED, CANNOT_DELETE_ITINERARY_ITEM, DELETE_VOYAGE_ERROR, WORK_SHEET_NAME_ALREADY_EXISTS, WORK_SHEET_NAME_INVALID, DUE_DATE_TERM_IS_USING, BUNKER_ORDER_PRICE_INVALID, BUNKER_ORDER_ITEM_ITINERARY_ITEM_NOT_FOUND — Commercial & UI constraints
```csharp
BUNKER_ORDER_LIFTED
```
**Explanation**: Enforces commercial workflow state (e.g., lifted orders cannot be edited), worksheet uniqueness, payment term locks, and itinerary linkage validation for bunker costing.

### voyage, shipment, commission, laytime, invoice, tco, tci, snapshot regions — Domain-specific lifecycle controllers
```csharp
VOYAGE_NOT_FOUND
```
**Explanation**: Each enum in these regions acts as a hard boundary for its entity's lifecycle. Example: `LAYTIME_MUST_BE_COMPLETED_BEFORE_INVOICING` prevents premature billing; `INVOICE_POSTED_CAN_NOT_BE_UPDATED` enforces accounting immutability; `SNAPSHOT_DATA_ERROR` handles serialization failures during audit restore. Collectively they guarantee transactional integrity across the maritime commercial stack.

## Dependencies
- `System.ComponentModel.Description` — Attaches user-facing error messages to each constant. Enables runtime reflection for API response localization and frontend error mapping without hardcoding strings in handlers.
- `Core.Domain.Commons.ApiResponse` — Primary consumer; maps `ErrorCode` values to structured HTTP responses and validation payload formatting.
- `Core.Domain.Commons.VersioningExtensions` — Likely referenced for backward-compatible error code routing or legacy response transformation.
- `Core.Business.Auditting.Snapshots.*` — Consumes `SNAPSHOT_*` codes for audit trail restore failures and deserialization errors.
- `Core.Business.BunkerOrder.*` — Consumes `BUNKER_ORDER_*`, `LAYTIME_*`, and `TCO/TCI_*` codes for commercial validation during order creation, cost calculation, and approval workflows.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]