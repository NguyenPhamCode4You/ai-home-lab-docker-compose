# RuleBuilderIgnoredAttribute

## Purpose
A marker attribute applied to model/DTO properties to signal that the query builder or column generator should exclude that field from automatic filter or column generation. Exists to decouple domain contracts from dynamic UI/query metadata generation.

## Business Responsibility
Owns the suppression rule for metadata-driven query filter generation in dynamic list grids. Low-impact utility but structurally critical for preventing invalid or redundant filter rules on computed, navigation, or internally managed fields. Consumed during reflection scanning to shape grid column definitions and queryable constraints before API projection or persistence.

---
## Members
The class contains no custom members, properties, or methods. It relies entirely on the base `Attribute` implementation and `AttributeUsage` to function as a pure reflection marker.

## Dependencies
- `System.Attribute` — base type required to attach metadata to reflection targets
- `QueryBuilderExtensions.cs` — direct consumer that reads this attribute via reflection to skip property processing during column/query generation

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]