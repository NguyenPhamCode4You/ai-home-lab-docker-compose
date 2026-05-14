# InvoiceItemDto

## Purpose
Data transfer object representing a finance invoice line item, aggregating vessel/voyage context, vendor details, pricing data, and shipment references.

## Business Responsibility
Defines the structural contract for invoice line items within the finance domain. Supports read/write operations for invoice processing, reporting, and integration with shipment and vendor contexts. Critical for financial accuracy as it carries amount, currency, percentage, and exchange rate fields required for settlement and commission calculations.

---

## Members
No members with non-trivial logic or computed expressions found. All properties are auto-properties used for data transfer.

---

## Dependencies
- `System.ComponentModel.DataAnnotations` — Required for `[MaxLength]` attributes applied to string properties, enforcing schema constraints during validation or ORM mapping.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]