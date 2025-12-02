# Day 11: Dynamic Programming - Advanced Patterns

## Problem 1: Coin Change (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given coins of different denominations and a total amount, return the fewest number of coins needed to make up that amount. If impossible, return -1.

**Example:**

```
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1
```

### Solution: Bottom-Up DP

```csharp
public class Solution
{
    public int CoinChange(int[] coins, int amount)
    {
        int[] dp = new int[amount + 1];
        Array.Fill(dp, amount + 1); // Initialize with impossible value
        dp[0] = 0; // Base case: 0 coins for amount 0

        for (int i = 1; i <= amount; i++)
        {
            foreach (int coin in coins)
            {
                if (i >= coin)
                {
                    dp[i] = Math.Min(dp[i], dp[i - coin] + 1);
                }
            }
        }

        return dp[amount] > amount ? -1 : dp[amount];
    }
}
```

**Time Complexity:** O(amount × coins)  
**Space Complexity:** O(amount)

**Explanation:**

- dp[i] = minimum coins needed for amount i
- Try each coin, take minimum
- Build from 0 to target amount
- Classic unbounded knapsack variant

---

## Problem 2: Longest Common Subsequence (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given two strings, find the length of their longest common subsequence. A subsequence doesn't need to be contiguous.

**Example:**

```
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: "ace" is the longest common subsequence
```

### Solution: 2D DP

```csharp
public class Solution
{
    public int LongestCommonSubsequence(string text1, string text2)
    {
        int m = text1.Length;
        int n = text2.Length;
        int[,] dp = new int[m + 1, n + 1];

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (text1[i - 1] == text2[j - 1])
                {
                    // Characters match: extend LCS
                    dp[i, j] = dp[i - 1, j - 1] + 1;
                }
                else
                {
                    // No match: take max from excluding one character
                    dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
                }
            }
        }

        return dp[m, n];
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n)

**Explanation:**

- dp[i,j] = LCS length of text1[0..i-1] and text2[0..j-1]
- If characters match, add 1 to previous LCS
- Otherwise, take max of excluding one character
- Classic two-sequence DP pattern

---

## Problem 3: Word Break (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given a string `s` and a dictionary of words, return true if `s` can be segmented into a space-separated sequence of dictionary words.

**Example:**

```
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: "leetcode" = "leet" + "code"

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
```

### Solution: DP with Word Set

```csharp
public class Solution
{
    public bool WordBreak(string s, IList<string> wordDict)
    {
        var wordSet = new HashSet<string>(wordDict);
        bool[] dp = new bool[s.Length + 1];
        dp[0] = true; // Empty string can be segmented

        for (int i = 1; i <= s.Length; i++)
        {
            for (int j = 0; j < i; j++)
            {
                // If s[0..j-1] can be segmented and s[j..i-1] is a word
                if (dp[j] && wordSet.Contains(s.Substring(j, i - j)))
                {
                    dp[i] = true;
                    break;
                }
            }
        }

        return dp[s.Length];
    }
}
```

**Time Complexity:** O(n² × m) - n = string length, m = average word length  
**Space Complexity:** O(n + k) - k = words in dictionary

**Explanation:**

- dp[i] = can s[0..i-1] be segmented?
- Try all possible last words ending at i
- If previous position segmentable and current word exists, true
- Optimization: use HashSet for O(1) word lookup

---

## Key Takeaways for Day 11

### 2D DP Patterns

**When to use:** Two sequences, 2D grid, two choices

**Template:**

```csharp
int[,] dp = new int[m + 1, n + 1];
// Initialize base cases
for (int i = 1; i <= m; i++)
{
    for (int j = 1; j <= n; j++)
    {
        // Recurrence based on dp[i-1][j], dp[i][j-1], dp[i-1][j-1]
    }
}
```

### Common 2D DP Problems

- **Edit Distance:** Transform one string to another
- **LCS:** Longest common subsequence
- **Unique Paths:** Grid path counting
- **Minimum Path Sum:** Grid with costs

### Optimization Techniques

1. **Space:** Use 1D array if only need previous row
2. **Time:** Memoization for sparse problems
3. **Pruning:** Skip impossible states early

**Tomorrow:** Day 12 - Backtracking & Recursion
