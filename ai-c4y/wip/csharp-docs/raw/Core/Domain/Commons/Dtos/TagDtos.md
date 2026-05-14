# TagDto, CreateTagDto, UpdateEntityTagsDto

## Purpose
Plain Data Transfer Objects for tag metadata, creation requests, and bulk tag assignment. They exist to serialize tag-related data across CQRS boundaries and API layers without introducing domain logic or validation overhead.

## Business Responsibility
Serve as the contract surface for tag lifecycle operations across bunker orders, equipment, and other domain entities. Critical for UI rendering (`BunkerOverviewDto`, `GetTagsByEntityId/Type`) and command routing (`CreateTag`, `UpdateEntityTags`), but strictly passive—carry no validation, state transitions, or business rules.

---
## Members
None. All three classes contain only trivial auto-properties with empty-string defaults. No computed fields, fallback chains, conditional logic, or domain-specific behavior exist in this file.

## Dependencies
None. No injected services, base classes, interfaces, or non-primitive referenced types.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]