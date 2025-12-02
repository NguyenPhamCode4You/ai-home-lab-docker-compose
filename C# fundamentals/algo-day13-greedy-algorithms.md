# Day 13: Greedy Algorithms

## Greedy Strategy

**Core Idea:** Make locally optimal choice at each step, hoping to find global optimum.

**When Greedy Works:**

- Problem has optimal substructure
- Greedy choice leads to optimal solution
- No need to reconsider previous choices

## Problem 1: Best Time to Buy and Sell Stock II (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

Given stock prices over time, find maximum profit. You can buy and sell multiple times (but must sell before buying again).

**Example:**

```
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy day 2 (1), sell day 3 (5) = 4
             Buy day 4 (3), sell day 5 (6) = 3
             Total = 7
```

### Solution: Greedy - Capture All Gains

```csharp
public class Solution
{
    public int MaxProfit(int[] prices)
    {
        int maxProfit = 0;

        for (int i = 1; i < prices.Length; i++)
        {
            // If price increases, capture the gain
            if (prices[i] > prices[i - 1])
            {
                maxProfit += prices[i] - prices[i - 1];
            }
        }

        return maxProfit;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

**Explanation:**

- Key insight: capture every upward movement
- If tomorrow > today, buy today and sell tomorrow
- Equivalent to buying/selling optimally
- Greedy works because we can decompose any profit into daily gains

---

## Problem 2: Jump Game (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given an array where each element represents maximum jump length from that position, determine if you can reach the last index.

**Example:**

```
Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step to index 1, then 3 steps to last index

Input: nums = [3,2,1,0,4]
Output: false
Explanation: Always land at index 3 (max jump 0)
```

### Solution: Greedy - Track Max Reach

```csharp
public class Solution
{
    public bool CanJump(int[] nums)
    {
        int maxReach = 0;

        for (int i = 0; i < nums.Length; i++)
        {
            // If current position unreachable, return false
            if (i > maxReach)
            {
                return false;
            }

            // Update max reachable position
            maxReach = Math.Max(maxReach, i + nums[i]);

            // Early termination
            if (maxReach >= nums.Length - 1)
            {
                return true;
            }
        }

        return maxReach >= nums.Length - 1;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

**Explanation:**

- Track farthest position reachable
- At each position, update max reach
- If current position > max reach, stuck
- Greedy: always try to reach as far as possible

---

## Problem 3: Meeting Rooms II (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given an array of meeting time intervals, return the minimum number of conference rooms required.

**Example:**

```
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
Explanation: [0,30] and [5,10] overlap, need 2 rooms
```

### Solution: Greedy with Min Heap

```csharp
public class Solution
{
    public int MinMeetingRooms(int[][] intervals)
    {
        if (intervals.Length == 0) return 0;

        // Sort by start time
        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));

        // Min heap to track end times of ongoing meetings
        var endTimes = new PriorityQueue<int, int>();
        endTimes.Enqueue(intervals[0][1], intervals[0][1]);

        for (int i = 1; i < intervals.Length; i++)
        {
            // If earliest ending meeting finishes before current starts
            if (intervals[i][0] >= endTimes.Peek())
            {
                endTimes.Dequeue(); // Reuse room
            }

            // Add current meeting's end time
            endTimes.Enqueue(intervals[i][1], intervals[i][1]);
        }

        return endTimes.Count;
    }
}
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

**Explanation:**

- Sort meetings by start time
- Use min heap to track room availability
- If room available, reuse it
- Otherwise, need new room
- Heap size = rooms needed

### Alternative: Two Arrays (More Optimal)

```csharp
public class Solution
{
    public int MinMeetingRooms(int[][] intervals)
    {
        int[] starts = new int[intervals.Length];
        int[] ends = new int[intervals.Length];

        for (int i = 0; i < intervals.Length; i++)
        {
            starts[i] = intervals[i][0];
            ends[i] = intervals[i][1];
        }

        Array.Sort(starts);
        Array.Sort(ends);

        int rooms = 0;
        int endIdx = 0;

        for (int i = 0; i < starts.Length; i++)
        {
            if (starts[i] < ends[endIdx])
            {
                rooms++; // Need new room
            }
            else
            {
                endIdx++; // Reuse room
            }
        }

        return rooms;
    }
}
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

**Explanation:**

- Separate and sort start/end times
- Match starts with ends
- If start < earliest end, need new room
- More elegant, no heap needed

---

## Key Takeaways for Day 13

### Greedy vs DP

| Feature   | Greedy                      | DP                |
| --------- | --------------------------- | ----------------- |
| Choice    | Local optimal               | All possibilities |
| Backtrack | No                          | Yes (implicit)    |
| Guarantee | Not always optimal          | Always optimal    |
| Speed     | Usually faster              | Usually slower    |
| Problems  | Activity selection, Huffman | Knapsack, LCS     |

### Proving Greedy Works

1. **Greedy Choice Property:** Local optimal → global optimal
2. **Optimal Substructure:** Optimal solution contains optimal subsolutions
3. **Exchange Argument:** Show greedy ≥ any other solution

### Common Greedy Patterns

- **Interval Problems:** Sort by start/end, process in order
- **Minimize/Maximize:** Sort, pick best choices first
- **Two Pointers:** Process from both ends
- **Prefix/Suffix:** Process left to right or right to left

### When to Use Greedy

**Good signs:**

- Problem asks for "maximum" or "minimum"
- Making local choice doesn't affect future
- Can sort to reveal structure

**Bad signs:**

- Need to try all possibilities
- Previous choices affect future options
- Need exact optimal for complex constraints

**Tomorrow:** Day 14 - Advanced Data Structures
