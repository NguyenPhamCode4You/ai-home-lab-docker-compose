# Day 1: Merge Intervals Pattern 🎯

## Overview

The **Merge Intervals** pattern is one of the most frequently tested topics at Google, Amazon, Microsoft, and Meta. It appears in approximately **30% of coding interviews** and tests your ability to:

- Sort and process interval data
- Handle edge cases and overlapping conditions
- Optimize in-place operations
- Think about greedy approaches

**Key Insight:** Most interval problems require sorting first, then processing intervals sequentially while tracking the current merged interval.

---

## Problem 1: Merge Intervals ⭐⭐ (Medium)

### Problem Statement

Given an array of intervals where `intervals[i] = [starti, endi]`, merge all overlapping intervals and return an array of the non-overlapping intervals.

### Example

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: [1,3] and [2,6] overlap, so merge them into [1,6]

Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping
```

---

### Solution 1: Sort + Merge (Optimal)

```csharp
public class Solution
{
    public int[][] Merge(int[][] intervals)
    {
        if (intervals.Length <= 1)
            return intervals;

        // Sort by start time
        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));

        var result = new List<int[]>();
        int[] current = intervals[0];

        for (int i = 1; i < intervals.Length; i++)
        {
            // If overlapping, merge by extending end
            if (intervals[i][0] <= current[1])
            {
                current[1] = Math.Max(current[1], intervals[i][1]);
            }
            else
            {
                // No overlap, add current and start new
                result.Add(current);
                current = intervals[i];
            }
        }

        // Add last interval
        result.Add(current);

        return result.ToArray();
    }
}
```

**Time Complexity:** O(n log n) - Dominated by sorting  
**Space Complexity:** O(n) - For result list

**Explanation:**

1. Sort intervals by start time
2. Use greedy approach: keep extending current interval while overlapping
3. Key condition: `intervals[i][0] <= current[1]` means overlap
4. Update end with `Math.Max` to handle contained intervals

---

### Solution 2: Sort with Cleaner Logic

```csharp
public class Solution
{
    public int[][] Merge(int[][] intervals)
    {
        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));

        var merged = new List<int[]> { intervals[0] };

        foreach (var interval in intervals)
        {
            var last = merged[^1];  // C# 8+ index from end

            if (interval[0] <= last[1])
            {
                // Merge: extend the end
                last[1] = Math.Max(last[1], interval[1]);
            }
            else
            {
                // No overlap: add new interval
                merged.Add(interval);
            }
        }

        return merged.ToArray();
    }
}
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

**Explanation:**

- Cleaner code using collection initialization
- Direct modification of last element in list
- Uses C# 8+ index from end operator `^1`

---

## Problem 2: Insert Interval ⭐⭐⭐ (Medium-Hard)

### Problem Statement

You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [starti, endi]` sorted by `starti`. Insert a new interval `newInterval` into intervals such that intervals is still sorted and has no overlapping intervals. Merge if necessary.

### Example

```
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]

Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: [4,8] merges with [3,5], [6,7], and [8,10]
```

---

### Solution 1: Three-Phase Approach (Simple)

```csharp
public class Solution
{
    public int[][] Insert(int[][] intervals, int[] newInterval)
    {
        var result = new List<int[]>();
        int i = 0;
        int n = intervals.Length;

        // Phase 1: Add all intervals that come before newInterval
        while (i < n && intervals[i][1] < newInterval[0])
        {
            result.Add(intervals[i]);
            i++;
        }

        // Phase 2: Merge all overlapping intervals with newInterval
        while (i < n && intervals[i][0] <= newInterval[1])
        {
            newInterval[0] = Math.Min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.Max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.Add(newInterval);

        // Phase 3: Add all remaining intervals
        while (i < n)
        {
            result.Add(intervals[i]);
            i++;
        }

        return result.ToArray();
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

1. **Phase 1:** Add intervals ending before new interval starts (no overlap)
2. **Phase 2:** Merge all intervals that overlap with new interval by expanding boundaries
3. **Phase 3:** Add remaining intervals that start after new interval ends

---

### Solution 2: Single Pass with Conditions (Optimal)

```csharp
public class Solution
{
    public int[][] Insert(int[][] intervals, int[] newInterval)
    {
        var result = new List<int[]>();

        foreach (var interval in intervals)
        {
            // New interval comes before current (no overlap)
            if (newInterval[1] < interval[0])
            {
                result.Add(newInterval);
                newInterval = interval;  // Swap: now processing current
            }
            // Current interval comes before new (no overlap)
            else if (interval[1] < newInterval[0])
            {
                result.Add(interval);
            }
            // Overlapping: merge into newInterval
            else
            {
                newInterval[0] = Math.Min(newInterval[0], interval[0]);
                newInterval[1] = Math.Max(newInterval[1], interval[1]);
            }
        }

        // Add the final merged interval
        result.Add(newInterval);

        return result.ToArray();
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

- Single pass through intervals
- Three cases: before, after, overlapping
- Clever swap trick: when new comes before current, add new and process current next
- Always tracking the "active" interval to insert

---

## Problem 3: Non-Overlapping Intervals ⭐⭐⭐ (Medium-Hard)

### Problem Statement

Given an array of intervals, return the **minimum number of intervals you need to remove** to make the rest of the intervals non-overlapping.

### Example

```
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: Remove [1,3] and the rest don't overlap

Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: Remove 2 intervals, keep 1

Input: intervals = [[1,2],[2,3]]
Output: 0
Explanation: Already non-overlapping
```

---

### Solution 1: Greedy by End Time (Optimal)

```csharp
public class Solution
{
    public int EraseOverlapIntervals(int[][] intervals)
    {
        if (intervals.Length <= 1)
            return 0;

        // Sort by END time (greedy choice)
        Array.Sort(intervals, (a, b) => a[1].CompareTo(b[1]));

        int count = 0;
        int prevEnd = intervals[0][1];

        for (int i = 1; i < intervals.Length; i++)
        {
            // If current starts before previous ends -> overlap
            if (intervals[i][0] < prevEnd)
            {
                count++;  // Remove current interval
            }
            else
            {
                // No overlap, update end
                prevEnd = intervals[i][1];
            }
        }

        return count;
    }
}
```

**Time Complexity:** O(n log n) - Sorting  
**Space Complexity:** O(1) - Constant extra space

**Explanation:**

1. **Key Insight:** Sort by END time (not start!)
2. Greedy strategy: Always keep interval with earliest end time
3. If overlap detected (start < prevEnd), increment removal count
4. This maximizes the number of non-overlapping intervals we can keep

---

### Solution 2: Greedy by Start Time (Alternative)

```csharp
public class Solution
{
    public int EraseOverlapIntervals(int[][] intervals)
    {
        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));

        int count = 0;
        int prevEnd = intervals[0][1];

        for (int i = 1; i < intervals.Length; i++)
        {
            // Overlap detected
            if (intervals[i][0] < prevEnd)
            {
                count++;
                // Keep interval with earlier end (remove the longer one)
                prevEnd = Math.Min(prevEnd, intervals[i][1]);
            }
            else
            {
                prevEnd = intervals[i][1];
            }
        }

        return count;
    }
}
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(1)

**Explanation:**

- Sort by start time
- When overlap: keep interval with earlier end
- Need to track which one to keep with `Math.Min`
- Slightly more complex than Solution 1

---

## Key Takeaways

### 1. Interval Problem Patterns

| Pattern               | Approach                          | Example          |
| --------------------- | --------------------------------- | ---------------- |
| **Merge overlapping** | Sort by start, extend end         | Merge Intervals  |
| **Insert single**     | Three-phase (before/merge/after)  | Insert Interval  |
| **Minimize removals** | Sort by end, greedy keep earliest | Non-Overlapping  |
| **Count overlaps**    | Sort + sweep line algorithm       | Meeting Rooms II |

### 2. Common Strategies

- **Always sort first** (by start or end depending on problem)
- **Track current/previous interval** for comparison
- **Greedy approach** usually optimal for interval problems
- **End time sorting** for maximizing non-overlapping intervals

### 3. Edge Cases to Consider

```csharp
// Empty or single interval
if (intervals.Length <= 1) return intervals;

// Contained intervals: [1,5] contains [2,3]
// Use Math.Max for end time

// Adjacent intervals: [1,2] and [2,3]
// Usually considered overlapping (check problem statement)

// Negative ranges: [-5, -3], [-2, 0]
// Still works with same logic
```

### 4. Interview Tips

✅ **Ask clarifying questions:**

- Are intervals sorted?
- Can intervals have the same start/end?
- Are adjacent intervals ([1,2], [2,3]) considered overlapping?

✅ **Start with brute force:**

- "I could check every pair (O(n²)) but sorting gives us O(n log n)"

✅ **Explain greedy choice:**

- "Sorting by end time lets us keep maximum intervals"

✅ **Test edge cases:**

- Empty array, single interval, all overlapping, none overlapping

---

## Practice Problems

### Easy

1. **Meeting Rooms** - Can attend all meetings?

### Medium

2. **Merge Intervals** ✓ (Covered above)
3. **Insert Interval** ✓ (Covered above)
4. **Non-Overlapping Intervals** ✓ (Covered above)
5. **Interval List Intersections** - Find intersection of two interval lists

### Hard

6. **Meeting Rooms II** - Minimum conference rooms needed
7. **Employee Free Time** - Find common free time slots
8. **My Calendar I/II/III** - Booking system with k-overlapping

---

## Common Mistakes to Avoid

❌ **Forgetting to sort** - Most interval problems need sorted input  
❌ **Wrong comparison** - Using `<` vs `<=` for overlap detection  
❌ **Not handling contained intervals** - Need `Math.Max` for end time  
❌ **Off-by-one errors** - Carefully handle boundary cases  
❌ **Sorting by wrong attribute** - Start vs end matters!

---

## Time Complexity Summary

| Problem          | Brute Force | Optimal    | Space |
| ---------------- | ----------- | ---------- | ----- |
| Merge Intervals  | O(n²)       | O(n log n) | O(n)  |
| Insert Interval  | O(n²)       | O(n)       | O(n)  |
| Non-Overlapping  | O(n²)       | O(n log n) | O(1)  |
| Meeting Rooms II | O(n²)       | O(n log n) | O(n)  |

---

## Next Steps

- ✅ Master these 3 core interval problems
- 📚 Practice "Meeting Rooms II" with heap/sorting
- 🎯 Try interval problems from different companies
- 💡 Recognize when to sort by start vs end

**Remember:** Interval problems reward clean code and edge case handling. Take time to understand the greedy choice!
