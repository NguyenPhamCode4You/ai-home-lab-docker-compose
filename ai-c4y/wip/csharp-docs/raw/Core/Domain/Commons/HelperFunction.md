# StringHelper / ListHelper / EnumHelper / JsonHelper / CountryMappingHelper

## Purpose
A collection of domain-agnostic static utility classes providing helper methods for string manipulation, list deduplication, enum description/acronym resolution, recursive JSON serialization with depth limits, and country code mapping.

## Business Responsibility
Supports core business operations in PDF exports, DTO mapping, and data synchronization by providing safe formatting, deduplication, and serialization utilities. The depth-limited JSON serializer is critical for preventing payload bloat during voyage/estimate exports. Country mapping supports international shipping compliance data. Low-impact, high-reuse domain utilities.

---

## Members

### 1. RandomEstimateCode() — Generates placeholder estimate code for temporary states or PDF exports
```csharp
public static string RandomEstimateCode()
{
    var officeCodes = new List<string> { "HOU", "LER", "SIN" };
    var userCodes = new List<string> { "AP", "PA", "MA" };

    var countOfficeCodes = officeCodes.Count;
    var countUserCodes = userCodes.Count;

    return $"{officeCodes[new Random().Next(0, countOfficeCodes)]}-{userCodes[new Random().Next(0, countUserCodes)]}";
}
```
**Explanation**: Creates a synthetic estimate code by combining a random office prefix with a random user prefix. Used exclusively as a fallback or placeholder during estimate creation, PDF generation, or temporary state handling where a real code isn't available yet. No external state is mutated.

### 2. GetShortName() — Extracts initials from a full person name
```csharp
public static string GetShortName(string fullName)
{
    if (string.IsNullOrWhiteSpace(fullName))
        return string.Empty;

    var names = fullName.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);

    return string.Concat(names.Select(n => char.ToUpper(n[0])));
}
```
**Explanation**: Splits the input by spaces, filters empty entries, and concatenates the uppercase first character of each word. Used in UI lists and PDF exports to display compact user/agent names. Handles multi-part names (first, middle, last) by capturing all initials.

### 3. Truncate() — Safely limits string length for display/export constraints
```csharp
public static string Truncate(string? value, int maxLength = 30)
{
    if (string.IsNullOrEmpty(value)) return string.Empty;
    return value.Length > maxLength ? value.Substring(0, maxLength) : value;
}
```
**Explanation**: Prevents `ArgumentOutOfRangeException` by returning early on null/empty inputs, otherwise returns the exact substring up to `maxLength`. Critical for layout-sensitive PDF exports and DTO contracts where field widths are strictly bounded.

### 4. FilterUniqueBy() — Deduplicates a list based on a calculated key
```csharp
public static List<T> FilterUniqueBy<T>(this List<T> items, Func<T, object> aggregate) where T : class
{
    return items.GroupBy(aggregate).Select(x => x.First()).ToList();
}
```
**Explanation**: LINQ-based extension that groups by the provided selector and keeps the first occurrence. Used in data synchronization and DTO mapping to remove duplicate records before export or PDF generation without requiring explicit HashSet management.

### 5. GetDescription<TEnum>() — Retrieves the [Description] attribute value for an enum
```csharp
public static string GetDescription<TEnum>(TEnum value) where TEnum : struct, Enum
{
    var memberInfo = typeof(TEnum).GetMember(value.ToString());
    var descriptionAttribute = (DescriptionAttribute?)memberInfo[0].GetCustomAttributes(typeof(DescriptionAttribute), false).FirstOrDefault();
    return descriptionAttribute?.Description ?? string.Empty;
}
```
**Explanation**: Uses reflection to extract the human-readable description attached to an enum member. Acts as the canonical fallback for display names when attributes are missing. Used extensively in dropdowns, logs, and export reports.

### 6. GetAcronym(string) — Resolves a string to the description of a specific port visit enum
```csharp
public static string GetAcronym(string text)
{
    try
    {
        var enumValue = Enum.Parse<ReasonForVisitPortEnum>(text);
        return GetDescription(enumValue);
    }
    catch (Exception)
    {
        return text;
    }
}
```
**Explanation**: Attempts to parse `text` into `ReasonForVisitPortEnum` and returns its `[Description]`. If parsing fails (malformed data, mismatched enum value), it gracefully falls back to the original string. Ensures exports and UI never crash on invalid enum strings.

### 7. GetAcronym<TEnum>() — Generic overload that delegates to the string-based resolver
```csharp
public static string GetAcronym<TEnum>(TEnum value) where TEnum : struct, Enum
{
    return GetAcronym(value.ToString());
}
```
**Explanation**: Simplifies calling code by accepting the enum directly, converting it to a string first. Maintains consistency with the string overload's exception-handling fallback pattern.

### 8. ToEnumerable<T>() — Wraps a single item in an IEnumerable for fluent chaining
```csharp
public static IEnumerable<T> ToEnumerable<T>(this T t)
{
    yield return t;
}
```
**Explanation**: Converts a single value into an enumerable sequence. Primarily used to unify single-item and multi-item scenarios in LINQ pipelines or collection-based APIs without requiring conditional `ToList()` calls.

### 9. GetEnumByAcronym<TEnum>() — Reverse lookup from description text back to enum value
```csharp
public static TEnum? GetEnumByAcronym<TEnum>(string acronym) where TEnum : struct, Enum
{
    foreach (var value in Enum.GetValues<TEnum>())
    {
        if (GetDescription(value) == acronym)
            return value;
    }
    return null;
}
```
**Explanation**: Iterates all values of the generic enum type and matches against the `[Description]` attribute. Returns the matching enum or `null` if not found. Used for inbound data normalization where external systems send human-readable descriptions instead of enum codes.

### 10. GetDisplayName(this Enum) — Reads the [Display] attribute Name fallback
```csharp
public static string GetDisplayName(this Enum enumValue)
{
    return enumValue.GetType()
                .GetMember(enumValue.ToString())[0]
                .GetCustomAttribute<DisplayAttribute>()?.Name ?? enumValue.ToString();
}
```
**Explanation**: Similar to `GetDescription` but targets `[Display]` attributes instead. Falls back to the raw enum name if no attribute exists. Used alongside description resolution to provide UI-friendly labels.

### 11. SerializeToJsonNode() — Standard serialization to JsonNode with cycle protection
```csharp
public static JsonNode SerializeToJsonNode(object obj)
{
    if (obj == null)
        throw new ArgumentNullException(nameof(obj));

    var options = new JsonSerializerOptions 
    { 
        ReferenceHandler = ReferenceHandler.IgnoreCycles
    };
    var json = JsonSerializer.Serialize(obj, options);
    return JsonNode.Parse(json)!;
}
```
**Explanation**: Converts objects to `JsonNode` for dynamic querying or transformation. Explicitly configures `IgnoreCycles` to prevent `JsonException` on self-referencing domain models. Throws on null to force upstream handling.

### 12. DeserializeFromJsonNode<T>() — Standard deserialization from JsonNode to typed object
```csharp
public static T DeserializeFromJsonNode<T>(JsonNode node)
{
    if (node == null)
        throw new ArgumentNullException(nameof(node));

    var options = new JsonSerializerOptions
    {
        ReferenceHandler = ReferenceHandler.IgnoreCycles
    };

    return node.Deserialize<T>(options)!;
}
```
**Explanation**: Reverses `SerializeToJsonNode` for round-trip scenarios. Shares the same cycle-avoidance options. Used in data synchronization and DTO mapping layers to materialize intermediate JSON representations back into strongly-typed objects.

### 13. SerializeToJsonNodeWithDepthLimit() — Serializes with configurable depth capping to prevent payload bloat
```csharp
public static JsonNode SerializeToJsonNodeWithDepthLimit(object obj, int maxDepth = 3)
{
    if (obj == null)
        throw new ArgumentNullException(nameof(obj));

    using var stream = new MemoryStream();
    using var writer = new Utf8JsonWriter(stream);

    var options = new JsonSerializerOptions 
    { 
        ReferenceHandler = ReferenceHandler.IgnoreCycles,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };

    SerializeWithDepthLimit(writer, obj, options, currentDepth: 0, maxDepth: maxDepth);
    writer.Flush();
    
    var json = Encoding.UTF8.GetString(stream.ToArray());
    return JsonNode.Parse(json)!;
}
```
**Explanation**: Custom serializer for scenarios requiring bounded memory/CPU, primarily PDF exports and DTO mappings where deep navigation properties cause exponential growth. Default depth is 3; objects beyond this threshold are silently truncated to `null`. Bypasses `JsonSerializer.Serialize` to enforce traversal logic.

### 14. SerializeWithDepthLimit() — Recursive traversal implementation with type-aware depth tracking
```csharp
private static void SerializeWithDepthLimit(
    Utf8JsonWriter writer, 
    object? obj, 
    JsonSerializerOptions options,
    int currentDepth,
    int maxDepth)
{
    if (obj == null)
    {
        writer.WriteNullValue();
        return;
    }

    var type = obj.GetType();

    // Handle primitives and simple types - always serialize regardless of depth
    if (type.IsPrimitive || type == typeof(string) || 
        type == typeof(DateTime) || type == typeof(Guid) || 
        type == typeof(decimal) || type.IsEnum)
    {
        JsonSerializer.Serialize(writer, obj, type, options);
        return;
    }

    // Check depth limit ONLY for complex objects and collections
    if (currentDepth >= maxDepth)
    {
        // Truncate: write null instead of deep nested objects
        writer.WriteNullValue();
        return;
    }

    // Handle collections - don't increase depth for the collection itself, only for items
    if (obj is System.Collections.IEnumerable enumerable && type != typeof(string))
    {
        writer.WriteStartArray();
        foreach (var item in enumerable)
        {
            // Use same depth for items - collection is just a container
            SerializeWithDepthLimit(writer, item, options, currentDepth, maxDepth);
        }
        writer.WriteEndArray();
        return;
    }

    // Handle complex objects
    writer.WriteStartObject();

    // Deduplicate properties by name (happens when derived class shadows base class property)
    var properties = type.GetProperties(System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance)
        .GroupBy(p => p.Name)
        .Select(g => g.First())
        .ToList();

    foreach (var prop in properties)
    {
        // Skip properties with [JsonIgnore]
        if (prop.GetCustomAttribute<JsonIgnoreAttribute>() != null)
            continue;

        try
        {
            var value = prop.GetValue(obj);
            writer.WritePropertyName(prop.Name);
            SerializeWithDepthLimit(writer, value, options, currentDepth + 1, maxDepth);
        }
        catch
        {
            // Skip properties that can't be accessed
            writer.WriteNullValue();
        }
    }
    writer.WriteEndObject();
}
```
**Explanation**: Core recursive engine that manually walks object graphs. Primitives and value types bypass depth checks. Collections and objects increment depth. Deduplicates properties by reflection to handle inheritance shadowing safely. Catches inaccessible properties to prevent export failures. Silently writes `null` when max depth is breached, ensuring PDF generators and DTO mappers receive bounded payloads.

### 15. MapCountryName() — Translates ISO 3166-1 alpha-2 codes to full country names
```csharp
public static string? MapCountryName(string? countryCode)
{
    if (string.IsNullOrWhiteSpace(countryCode))
        return null;

    return _map.TryGetValue(countryCode.Trim(), out var country)
        ? country
        : null;
}
```
**Explanation**: Performs case-insensitive dictionary lookup using a static in-memory map of ~130 ISO country codes. Used in voyage exports, PDF reports, and DTOs to standardize location strings. Returns `null` for missing codes rather than throwing, allowing upstream fallback logic.

---

## Dependencies
- `System.ComponentModel.DescriptionAttribute` — Required to read enum display descriptions.
- `System.ComponentModel.DataAnnotations.DisplayAttribute` — Required for fallback enum display names.
- `System.Text.Json.JsonSerializer`, `JsonNode`, `Utf8JsonWriter`, `ReferenceHandler`, `JsonIgnoreCondition` — Core for dynamic object serialization/deserialization and cycle/depth management.
- `System.Reflection` — Used to extract attributes from enum types and deduplicate property shadows.
- `ReasonForVisitPortEnum` — Hardcoded in `GetAcronym(string)` for specific port visit text resolution; tightly coupled to this enum despite utility nature.
- `Core.Domain.Constants` — Referenced in using directives (likely holds related constant definitions for this namespace).

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]