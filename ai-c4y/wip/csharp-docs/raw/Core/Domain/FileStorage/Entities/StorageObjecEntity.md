# StorageObjectEntity

## Purpose
Domain entity representing a file or directory node within the BVMS storage abstraction. Provides a structured data carrier for file metadata consumed by ingestion pipelines, billing calculations, and persistence layers.

## Business Responsibility
Owns the canonical representation of storage objects for the FileManage aggregate. Critical path for file/folder creation workflows and acts as the projection source for financial data binding (`InvoiceEntity`). Serves as the primary EF Core entity and AutoMapper target for all storage operations.

---

## Members
The class contains only scalar data properties with no computed fields, fallback chains, or domain methods. All members are direct data carriers mapped to database columns or object graphs, strictly adhering to the skip rule for auto-properties.

---

## Dependencies
- `BaseEntity` — supplies shared identifier, audit timestamps, and base lifecycle hooks required by EF Core mapping and the domain repository contracts.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]