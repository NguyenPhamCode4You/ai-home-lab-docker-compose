# FileModel & FileUploadModel

## Purpose
Plain DTOs for representing file metadata (`FileModel`) and HTTP upload payloads (`FileUploadModel`). They exist to decouple transport-layer types from core domain logic while providing a stable contract for file-related operations.

## Business Responsibility
Lightweight, low-impact data transfer objects used exclusively for binding HTTP file streams to the application layer. They own no business rules, validations, or state mutations—act purely as passthrough contracts for upstream services and downstream handlers.

## Members
Both classes contain only trivial auto-properties and lack domain logic, computed fields, or fallback chains. Per documentation standards, non-trivial members are excluded. `FileModel` is intentionally empty for future extensibility. `FileUploadModel.File` is a direct binding to `IFormFile` and carries no domain semantics.

## Dependencies
`IFormFile` (Microsoft.AspNetCore.Http) — Provides the typed HTTP file stream binding without requiring `HttpContext` access in the domain layer. Eliminates coupling to ASP.NET Core pipeline types elsewhere in the codebase.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]