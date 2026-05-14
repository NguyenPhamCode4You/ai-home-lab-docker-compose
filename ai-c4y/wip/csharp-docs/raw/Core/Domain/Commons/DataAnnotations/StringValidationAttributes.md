# EmailString, StringValidationAttribute & Size Limiters

## Purpose
Centralizes domain-level string validation for DTOs and entities using DataAnnotations. Enforces length budgets, character set restrictions, and format rules without leaking infrastructure concerns into the domain.

## Business Responsibility
Owns all input shape validation for string fields in Master Data and Vessel Specification flows. Prevents invalid data from progressing to persistence or downstream services. Critical for data integrity, preventing DB constraint violations, and ensuring legacy/system integrations receive ASCII-compatible payloads where required.

---
## Validation Rules

### EmailString
- Rule: Inherits `StandardString` length validation, then attempts `new MailAddress(strValue)` and verifies `addr.Address == strValue`. Skips format check for null/whitespace.
- Business constraint: Enforces strict RFC 5322 compliance at ingestion. The equality check prevents normalization/trimming, preserving exact user input while catching malformed addresses before they reach communication subsystems.

### StringValidationAttribute (Base)
- Rule: Validates type is `string` or `char`. Enforces `MinLength`/`MaxLength` from `IStringLimits`. Optionally rejects characters >127 when `useUnicode=false`. Optionally validates against `Enum.IsDefined(EnumType, strValue)`.
- Business constraint: Centralizes length enforcement to match database column definitions and API payload budgets. The `useUnicode` flag protects legacy integrations and ASCII-only indexes. Enum fallback ensures state fields only accept defined enumeration values, preventing phantom states from typos or external payloads.

### TinyString / SmallString / StandardString / LongString
- Rule: Concrete wrappers delegating to `StringValidationAttribute` with configured `IStringLimit` (Min/Max lengths).
- Business constraint: Maps directly to schema size tiers. `Tiny` (codes, flags), `Small` (names, short descriptors), `Standard` (descriptions, emails), `Long` (remarks, narratives). Prevents overflow and aligns validation with storage expectations before EF Core materialization.

### EnumString
- Rule: Extends `StringValidationAttribute` with `Enum.IsDefined` check on the configured `enumType` after length validation.
- Business constraint: Validates that string-represented enum values match domain definitions. Essential for DTOs receiving external strings that must map to internal enumerated states without parsing overhead.

## Dependencies
- `System.ComponentModel.DataAnnotations.ValidationAttribute` — Base framework for declarative property validation in DTOs and EF Core validation pipeline.
- `Core.Domain.Commons.DataTypeLimits.IStringLimits` — Provides schema-derived length boundaries (`MaxLength`, `MinLength`) ensuring validation aligns with actual database/DTO contracts.
- `System.Net.Mail.MailAddress` — Leverages built-in .NET email parsing for strict RFC compliance without external dependencies or regex overhead.
- `System.Enum.IsDefined` — Fast, runtime-safe lookup to validate string-to-enum mapping without reflection-heavy parsing.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]