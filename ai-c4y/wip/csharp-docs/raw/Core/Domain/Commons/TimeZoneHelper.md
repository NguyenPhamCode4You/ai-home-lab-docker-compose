# DateTimeHelper & TimeZoneHelper

## Purpose
Provides domain-level date boundary calculations and timezone conversion utilities for cross-system datetime normalization. Exposes safe, predictable extensions for boundary math and Business Central display-timezone reconciliation.

## Business Responsibility
Owns the canonical date boundary logic and timezone resolution used across domain services and integration adapters. Critical for report generation, SLA calculations, and accurately rendering port/local times in Business Central. Non-critical for core transaction processing but essential for consistent data presentation and external system contracts.

---

## Members

### StartOfDayAtTimeZone — Compute start-of-day boundary for a given UTC date in a specific timezone, returning as UTC
```csharp
public static DateTime? StartOfDayAtTimeZone(this DateTime? utcDate, string timeZone = "UTC")
{
    if (utcDate == null)
    {
        return null;
    }
    
    TimeZoneInfo tzInfo = TZConvert.GetTimeZoneInfo(timeZone);
    var localStartOfDay = new DateTime(utcDate.Value.Year, utcDate.Value.Month, utcDate.Value.Day, 0, 0, 0);
    localStartOfDay = DateTime.SpecifyKind(localStartOfDay, DateTimeKind.Unspecified);
    var utcResult = TimeZoneInfo.ConvertTimeToUtc(localStartOfDay, tzInfo);
    
    return utcResult;
}
```
**Explanation**: Extracts the Y/M/D from a UTC value, forces a 00:00:00 local time in the target zone, then converts back to UTC. Prevents off-by-one errors when filtering events by day in non-UTC zones. Skipping this causes daily boundaries to drift across system clocks.

### StartOfQuarter / EndOfQuarter — Calculate calendar quarter boundaries
```csharp
public static DateTime? StartOfQuarter(this DateTime? date)
{
    if (date == null)
    {
        return null;
    }
    var quarter = (date.Value.Month - 1) / 3 + 1;
    var firstDayOfQuarter = new DateTime(date.Value.Year, (quarter - 1) * 3 + 1, 1);
    return firstDayOfQuarter;
}

public static DateTime? EndOfQuarter(this DateTime? date)
{
    if (date == null)
    {
        return null;
    }
    var quarter = (date.Value.Month - 1) / 3 + 1;
    var lastDayOfQuarter = new DateTime(date.Value.Year, quarter * 3, 1).AddMonths(1).AddDays(-1);
    return lastDayOfQuarter;
}
```
**Explanation**: Derives quarter index via integer division, then constructs exact first/last day of that quarter. Used for fiscal reporting windows and quarterly aggregation queries. Bypassing these methods forces downstream services to reimplement calendar math or risk boundary mismatches.

### BusinessCentralTimeZone — Hardcoded timezone reference for BC display logic
```csharp
public static readonly string BusinessCentralTimeZone = "Europe/Berlin";
```
**Explanation**: Constant defining the timezone Business Central is configured to use for all incoming datetime rendering. Required by `ConvertToLocalTimeForBcDisplay` to calculate the inverse UTC mapping. Changing this constant without updating BC configuration breaks time display parity.

### GetTimeZoneByLatLong — Resolve timezone from geographic coordinates via external GeoTimeZone library
```csharp
public static string GetTimeZoneByLatLong(double? lat, double? lon)
{
    if (lat == null || lon == null) return "UTC";
    return GeoTimeZone.TimeZoneLookup.GetTimeZone(lat.Value, lon.Value).Result;
}
```
**Explanation**: Blocks the calling thread to resolve a timezone string from lat/lon. Falls back to `"UTC"` when coordinates are missing, preventing null-ref crashes in adapters. The synchronous `.Result` wrapper trades responsiveness for simplicity in coordination-layer calls.

### ConvertToLocalTimeForBcDisplay — Calculate the exact UTC timestamp that Business Central will render as the target port local time
```csharp
public static DateTime ConvertToLocalTimeForBcDisplay(this DateTime utcDateTime, string portTimeZone, string bcTimeZone)
{
    var portLocalTime = ConvertToLocalTime(utcDateTime, portTimeZone);
    var portLocalUnspecified = DateTime.SpecifyKind(portLocalTime, DateTimeKind.Unspecified);
    TimeZoneInfo bcTzInfo = TZConvert.GetTimeZoneInfo(bcTimeZone);
    if (bcTzInfo.IsInvalidTime(portLocalUnspecified))
    {
        var postGapOffset = bcTzInfo.GetUtcOffset(portLocalUnspecified.AddHours(1));
        return DateTime.SpecifyKind(portLocalUnspecified - postGapOffset, DateTimeKind.Utc);
    }
    return TimeZoneInfo.ConvertTimeToUtc(portLocalUnspecified, bcTzInfo);
}
```
**Explanation**: Business Central applies its configured timezone to *incoming UTC* values for display. This method reverses that process: it converts UTC → port local time, then finds the UTC value that, when BC applies its timezone, yields the original port local time. The DST gap handler subtracts the post-transition offset to avoid `DateTimeKind` mismatches during spring-forward transitions. Skipping this produces misaligned timestamps in BC audit trails.

### ConvertInputToDateTime — Parse raw datetime strings into a culture-neutral, kind-unspecified instance
```csharp
public static DateTime ConvertInputToDateTime(string input)
{
    DateTime dt = DateTime.Parse(
        input,
        CultureInfo.InvariantCulture,
        DateTimeStyles.None
    );
    return DateTime.SpecifyKind(dt, DateTimeKind.Unspecified);
}
```
**Explanation**: Strips culture-specific parsing quirks and forces `Unspecified` kind, ensuring downstream `TimeZoneInfo` conversions are the sole determinant of time semantics. Prevents `Kind` mismatch exceptions during cross-service DTO mapping.

---

## Dependencies
- `GeoTimeZone.TimeZoneLookup` — Synchronous coordinate-to-timezone resolution; no internal geo-lookup exists, making this the sole source for lat/lon timezone derivation.
- `TimeZoneConverter.TZConvert` — Cross-platform `TimeZoneInfo` factory; required to avoid OS registry dependency on Linux containers and ensure consistent DST rules across deployments.
- `System.Globalization.CultureInfo.InvariantCulture` — Enforced for `ConvertInputToDateTime` to eliminate culture-driven parsing variance in distributed service boundaries.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]