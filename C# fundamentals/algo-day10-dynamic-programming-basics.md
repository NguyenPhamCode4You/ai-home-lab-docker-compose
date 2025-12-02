# Day 10: Dynamic Programming - Fundamentals

## Dynamic Programming Basics

**Core Idea:** Break problem into overlapping subproblems, solve each once, reuse solutions.

**Two Approaches:**

1. **Top-Down (Memoization):** Recursion + caching
2. **Bottom-Up (Tabulation):** Iterative, fill table

## Problem 1: Climbing Stairs (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. How many distinct ways can you reach the top?

**Example:**

```
Input: n = 3
Output: 3
Explanation: Three ways: 1+1+1, 1+2, 2+1
```

### Solution 1: Recursion (TLE - Too Slow)

```csharp
public class Solution
{
    public int ClimbStairs(int n)
    {
        if (n <= 2) return n;

        return ClimbStairs(n - 1) + ClimbStairs(n - 2);
    }
}
```

**Time Complexity:** O(2^n) - Exponential!  
**Space Complexity:** O(n) - Recursion depth

**Explanation:**

- Pure recursion, many repeated calculations
- ClimbStairs(5) calculates ClimbStairs(3) multiple times
- Too slow for large n

### Solution 2: Top-Down DP (Memoization)

```csharp
public class Solution
{
    public int ClimbStairs(int n)
    {
        int[] memo = new int[n + 1];
        return Climb(n, memo);
    }

    private int Climb(int n, int[] memo)
    {
        if (n <= 2) return n;

        if (memo[n] != 0)
        {
            return memo[n];
        }

        memo[n] = Climb(n - 1, memo) + Climb(n - 2, memo);
        return memo[n];
    }
}
```

**Time Complexity:** O(n) - Each state calculated once  
**Space Complexity:** O(n) - Memo array + recursion

**Explanation:**

- Cache results in memo array
- Check cache before calculating
- Dramatically improves performance

### Solution 3: Bottom-Up DP (Optimal)

```csharp
public class Solution
{
    public int ClimbStairs(int n)
    {
        if (n <= 2) return n;

        int[] dp = new int[n + 1];
        dp[1] = 1;
        dp[2] = 2;

        for (int i = 3; i <= n; i++)
        {
            dp[i] = dp[i - 1] + dp[i - 2];
        }

        return dp[n];
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

- Build solution from bottom up
- No recursion needed
- Fill table iteratively

### Solution 4: Space Optimized

```csharp
public class Solution
{
    public int ClimbStairs(int n)
    {
        if (n <= 2) return n;

        int prev2 = 1; // dp[i-2]
        int prev1 = 2; // dp[i-1]

        for (int i = 3; i <= n; i++)
        {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }

        return prev1;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1) - Only two variables!

**Explanation:**

- Only need last two values
- This is actually Fibonacci sequence!
- Most optimal solution

---

## Problem 2: House Robber (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

You are a robber planning to rob houses along a street. Each house has money. Adjacent houses have security systems connected, so you can't rob two adjacent houses. Return maximum money you can rob.

**Example:**

```
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (2), 3 (9), and 5 (1) = 12
```

### Solution 1: Recursive with Memo

```csharp
public class Solution
{
    public int Rob(int[] nums)
    {
        int[] memo = new int[nums.Length];
        Array.Fill(memo, -1);
        return RobFrom(nums, 0, memo);
    }

    private int RobFrom(int[] nums, int index, int[] memo)
    {
        if (index >= nums.Length)
        {
            return 0;
        }

        if (memo[index] != -1)
        {
            return memo[index];
        }

        // Choice: rob current house or skip it
        int robCurrent = nums[index] + RobFrom(nums, index + 2, memo);
        int skipCurrent = RobFrom(nums, index + 1, memo);

        memo[index] = Math.Max(robCurrent, skipCurrent);
        return memo[index];
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

### Solution 2: Bottom-Up DP (Optimal)

```csharp
public class Solution
{
    public int Rob(int[] nums)
    {
        if (nums.Length == 0) return 0;
        if (nums.Length == 1) return nums[0];

        int[] dp = new int[nums.Length];
        dp[0] = nums[0];
        dp[1] = Math.Max(nums[0], nums[1]);

        for (int i = 2; i < nums.Length; i++)
        {
            // Max of: rob current + best until i-2, or best until i-1
            dp[i] = Math.Max(nums[i] + dp[i - 2], dp[i - 1]);
        }

        return dp[nums.Length - 1];
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

- dp[i] = max money robbing up to house i
- Either rob house i (can't rob i-1) or skip it
- Build from smaller problems

### Solution 3: Space Optimized

```csharp
public class Solution
{
    public int Rob(int[] nums)
    {
        if (nums.Length == 0) return 0;
        if (nums.Length == 1) return nums[0];

        int prev2 = nums[0];
        int prev1 = Math.Max(nums[0], nums[1]);

        for (int i = 2; i < nums.Length; i++)
        {
            int current = Math.Max(nums[i] + prev2, prev1);
            prev2 = prev1;
            prev1 = current;
        }

        return prev1;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

---

## Problem 3: Longest Increasing Subsequence (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given an integer array, return the length of the longest strictly increasing subsequence.

**Example:**

```
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: [2,3,7,101] or [2,3,7,18]
```

### Solution 1: DP O(n²)

```csharp
public class Solution
{
    public int LengthOfLIS(int[] nums)
    {
        if (nums.Length == 0) return 0;

        int[] dp = new int[nums.Length];
        Array.Fill(dp, 1); // Each element is a subsequence of length 1
        int maxLength = 1;

        for (int i = 1; i < nums.Length; i++)
        {
            for (int j = 0; j < i; j++)
            {
                if (nums[i] > nums[j])
                {
                    dp[i] = Math.Max(dp[i], dp[j] + 1);
                }
            }
            maxLength = Math.Max(maxLength, dp[i]);
        }

        return maxLength;
    }
}
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(n)

**Explanation:**

- dp[i] = length of LIS ending at index i
- For each position, check all previous positions
- If current > previous, can extend that subsequence

### Solution 2: Binary Search O(n log n) (Optimal)

```csharp
public class Solution
{
    public int LengthOfLIS(int[] nums)
    {
        var tails = new List<int>();

        foreach (int num in nums)
        {
            int pos = BinarySearch(tails, num);

            if (pos == tails.Count)
            {
                tails.Add(num);
            }
            else
            {
                tails[pos] = num;
            }
        }

        return tails.Count;
    }

    private int BinarySearch(List<int> tails, int target)
    {
        int left = 0, right = tails.Count;

        while (left < right)
        {
            int mid = left + (right - left) / 2;

            if (tails[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid;
            }
        }

        return left;
    }
}
```

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

**Explanation:**

- Maintain array of smallest tail values for each length
- Use binary search to find position for current number
- Either extend sequence or replace larger tail
- Advanced technique using patience sorting

---

## Key Takeaways for Day 10

### DP Problem Recognition

**Ask these questions:**

1. Can problem be broken into subproblems?
2. Do subproblems overlap?
3. Is there optimal substructure?

**Common indicators:**

- "Maximum/minimum"
- "How many ways"
- "Longest/shortest"
- "Can we do X?"

### DP Steps

1. **Define state:** What does dp[i] represent?
2. **Find recurrence:** How to compute dp[i] from smaller problems?
3. **Base cases:** What are the simplest cases?
4. **Order:** Which direction to fill table?
5. **Answer:** Where is final answer?

### Common DP Patterns

| Pattern       | Example         | Recurrence                                         |
| ------------- | --------------- | -------------------------------------------------- |
| Linear        | Climbing stairs | dp[i] = dp[i-1] + dp[i-2]                          |
| Subsequence   | LIS             | dp[i] = max(dp[j] + 1) for j < i                   |
| Two sequences | Edit distance   | dp[i][j] from dp[i-1][j], dp[i][j-1], dp[i-1][j-1] |
| Partition     | Coin change     | dp[i] = min(dp[i-coin] + 1)                        |

### Space Optimization

- If only need previous k states, use k variables
- Rolling array technique for 2D DP
- Trade-off: space vs complexity

**Tomorrow:** Day 11 - Dynamic Programming Advanced
