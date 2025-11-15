# Day 4: String DP & Decode Ways 🎯

## Overview

**String Dynamic Programming** is a critical topic in big tech interviews, appearing in approximately **15-20%** of coding rounds, especially at Meta, Amazon, and Google. These problems test:

- 1D dynamic programming fundamentals
- Decision tree thinking
- State transition design
- Boundary condition handling

**Key Insight:** String DP problems often involve making decisions at each character: "Should I take this character alone, or combine it with the previous/next one?"

---

## Problem 1: Decode Ways ⭐⭐⭐ (Medium)

### Problem Statement

A message containing letters from `A-Z` can be **encoded** into numbers using the following mapping:

```
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

To **decode** an encoded message, all the digits must be grouped and then mapped back into letters. However, there can be multiple ways to decode a message.

Given a string `s` containing only digits, return the **number of ways to decode it**.

### Example

```
Input: s = "12"
Output: 2
Explanation: "12" can be decoded as "AB" (1 2) or "L" (12)

Input: s = "226"
Output: 3
Explanation: Could be "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6)

Input: s = "06"
Output: 0
Explanation: "06" cannot be decoded (no letter maps to "06")
```

---

### Solution 1: Recursive (Understanding the Problem)

```csharp
public class Solution
{
    public int NumDecodings(string s)
    {
        return Decode(s, 0);
    }

    private int Decode(string s, int index)
    {
        // Base case: reached end successfully
        if (index == s.Length)
            return 1;

        // Leading zero is invalid
        if (s[index] == '0')
            return 0;

        // Option 1: Take single digit
        int ways = Decode(s, index + 1);

        // Option 2: Take two digits (if valid)
        if (index + 1 < s.Length)
        {
            int twoDigit = int.Parse(s.Substring(index, 2));
            if (twoDigit >= 10 && twoDigit <= 26)
            {
                ways += Decode(s, index + 2);
            }
        }

        return ways;
    }
}
```

**Time Complexity:** O(2^n) - Each position branches into 2 choices  
**Space Complexity:** O(n) - Recursion stack

**Explanation:**

- At each position, we have 2 choices: take 1 digit or 2 digits
- Invalid cases: leading zero or two-digit number > 26
- Too slow due to overlapping subproblems

---

### Solution 2: Recursion with Memoization (Better)

```csharp
public class Solution
{
    private int[] memo;

    public int NumDecodings(string s)
    {
        memo = new int[s.Length];
        Array.Fill(memo, -1);
        return Decode(s, 0);
    }

    private int Decode(string s, int index)
    {
        if (index == s.Length)
            return 1;

        if (s[index] == '0')
            return 0;

        if (memo[index] != -1)
            return memo[index];

        // Single digit
        int ways = Decode(s, index + 1);

        // Two digits
        if (index + 1 < s.Length)
        {
            int twoDigit = (s[index] - '0') * 10 + (s[index + 1] - '0');
            if (twoDigit <= 26)
            {
                ways += Decode(s, index + 2);
            }
        }

        memo[index] = ways;
        return ways;
    }
}
```

**Time Complexity:** O(n) - Each subproblem solved once  
**Space Complexity:** O(n) - Memoization array + recursion stack

**Explanation:**

- Cache results to avoid recomputation
- Much faster than pure recursion

---

### Solution 3: Bottom-Up DP (Optimal)

```csharp
public class Solution
{
    public int NumDecodings(string s)
    {
        if (s[0] == '0') return 0;

        int n = s.Length;
        int[] dp = new int[n + 1];

        // Base cases
        dp[0] = 1;  // Empty string
        dp[1] = 1;  // First character (already checked not '0')

        for (int i = 2; i <= n; i++)
        {
            // Single digit decode
            int oneDigit = s[i - 1] - '0';
            if (oneDigit >= 1 && oneDigit <= 9)
            {
                dp[i] += dp[i - 1];
            }

            // Two digit decode
            int twoDigits = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
            if (twoDigits >= 10 && twoDigits <= 26)
            {
                dp[i] += dp[i - 2];
            }
        }

        return dp[n];
    }
}
```

**Time Complexity:** O(n) - Single pass  
**Space Complexity:** O(n) - DP array

**Explanation:**

1. `dp[i]` = number of ways to decode `s[0..i-1]`
2. At each position, check if we can decode:
   - **Single digit:** `s[i-1]` is 1-9 → add `dp[i-1]`
   - **Two digits:** `s[i-2..i-1]` is 10-26 → add `dp[i-2]`
3. Similar to Fibonacci pattern

**Visual Example for s="226":**

```
Index:  0  1  2  3
s:         2  2  6
dp:    [1, 1, 2, 3]

i=2: '2' valid (add dp[1]=1), '22' valid (add dp[0]=1) → dp[2]=2
i=3: '6' valid (add dp[2]=2), '26' valid (add dp[1]=1) → dp[3]=3
```

---

### Solution 4: Space-Optimized DP (Most Optimal)

```csharp
public class Solution
{
    public int NumDecodings(string s)
    {
        if (s[0] == '0') return 0;

        int prev2 = 1;  // dp[i-2]
        int prev1 = 1;  // dp[i-1]

        for (int i = 2; i <= s.Length; i++)
        {
            int current = 0;

            // Single digit
            int oneDigit = s[i - 1] - '0';
            if (oneDigit >= 1 && oneDigit <= 9)
            {
                current += prev1;
            }

            // Two digits
            int twoDigits = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
            if (twoDigits >= 10 && twoDigits <= 26)
            {
                current += prev2;
            }

            // Shift window
            prev2 = prev1;
            prev1 = current;
        }

        return prev1;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1) - Only two variables

**Explanation:**

- Only need last 2 DP values (like Fibonacci)
- Use two variables instead of array

---

## Problem 2: Climbing Stairs ⭐ (Easy)

### Problem Statement

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb **1 or 2 steps**. In how many distinct ways can you climb to the top?

### Example

```
Input: n = 2
Output: 2
Explanation: 1+1 or 2

Input: n = 3
Output: 3
Explanation: 1+1+1, 1+2, or 2+1
```

---

### Solution 1: DP Array (Simple)

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

- `dp[i]` = ways to reach step i
- Can reach step i from step i-1 (climb 1) or i-2 (climb 2)
- Formula: `dp[i] = dp[i-1] + dp[i-2]` (Fibonacci!)

---

### Solution 2: Space-Optimized (Optimal)

```csharp
public class Solution
{
    public int ClimbStairs(int n)
    {
        if (n <= 2) return n;

        int prev2 = 1, prev1 = 2;

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
**Space Complexity:** O(1)

**Explanation:**

- Same logic, but only track last 2 values
- This is actually computing Fibonacci numbers!

---

## Problem 3: Word Break ⭐⭐⭐ (Medium)

### Problem Statement

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

**Note:** The same word in the dictionary may be reused multiple times.

### Example

```
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: "leetcode" can be segmented as "leet code"

Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: "applepenapple" can be segmented as "apple pen apple"

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
```

---

### Solution 1: DP Array (Optimal)

```csharp
public class Solution
{
    public bool WordBreak(string s, IList<string> wordDict)
    {
        var wordSet = new HashSet<string>(wordDict);
        int n = s.Length;
        bool[] dp = new bool[n + 1];
        dp[0] = true;  // Empty string is valid

        for (int i = 1; i <= n; i++)
        {
            for (int j = 0; j < i; j++)
            {
                // If s[0..j-1] is valid AND s[j..i-1] is in dictionary
                if (dp[j] && wordSet.Contains(s.Substring(j, i - j)))
                {
                    dp[i] = true;
                    break;  // Found one valid segmentation
                }
            }
        }

        return dp[n];
    }
}
```

**Time Complexity:** O(n² × m) where m is average word length  
**Space Complexity:** O(n + k) where k is dictionary size

**Explanation:**

1. `dp[i]` = true if `s[0..i-1]` can be segmented
2. For each position i, try all possible last words
3. Check if prefix is valid (`dp[j]`) and suffix is in dictionary
4. Use HashSet for O(1) word lookup

**Visual Example for s="leetcode":**

```
s:      l e e t c o d e
dp: [T, F, F, F, T, F, F, F, T]
     0  1  2  3  4  5  6  7  8

dp[4] = true because dp[0]=true and "leet" in dict
dp[8] = true because dp[4]=true and "code" in dict
```

---

### Solution 2: DP with Optimization (Better)

```csharp
public class Solution
{
    public bool WordBreak(string s, IList<string> wordDict)
    {
        var wordSet = new HashSet<string>(wordDict);
        int maxLen = wordDict.Max(w => w.Length);

        int n = s.Length;
        bool[] dp = new bool[n + 1];
        dp[0] = true;

        for (int i = 1; i <= n; i++)
        {
            // Only check words within maxLen
            for (int j = Math.Max(0, i - maxLen); j < i; j++)
            {
                if (dp[j] && wordSet.Contains(s.Substring(j, i - j)))
                {
                    dp[i] = true;
                    break;
                }
            }
        }

        return dp[n];
    }
}
```

**Time Complexity:** O(n × maxLen × m)  
**Space Complexity:** O(n + k)

**Explanation:**

- Optimization: Only check substrings up to max dictionary word length
- Reduces unnecessary substring checks

---

### Solution 3: BFS Approach (Alternative)

```csharp
public class Solution
{
    public bool WordBreak(string s, IList<string> wordDict)
    {
        var wordSet = new HashSet<string>(wordDict);
        var queue = new Queue<int>();
        var visited = new HashSet<int>();

        queue.Enqueue(0);

        while (queue.Count > 0)
        {
            int start = queue.Dequeue();

            if (start == s.Length)
                return true;

            if (visited.Contains(start))
                continue;

            visited.Add(start);

            // Try all possible words from this position
            for (int end = start + 1; end <= s.Length; end++)
            {
                string word = s.Substring(start, end - start);
                if (wordSet.Contains(word))
                {
                    queue.Enqueue(end);
                }
            }
        }

        return false;
    }
}
```

**Time Complexity:** O(n² × m)  
**Space Complexity:** O(n)

**Explanation:**

- Treat as graph problem: positions are nodes
- Edge exists if substring is in dictionary
- BFS to find path from 0 to n

---

## Key Takeaways

### 1. String DP Patterns

| Pattern           | State Definition                                    | Transition               |
| ----------------- | --------------------------------------------------- | ------------------------ |
| **Decode Ways**   | `dp[i]` = ways to decode `s[0..i-1]`                | Check 1 digit + 2 digits |
| **Word Break**    | `dp[i]` = can segment `s[0..i-1]`                   | Try all splits           |
| **Edit Distance** | `dp[i][j]` = min edits for `s1[0..i]` to `s2[0..j]` | Insert/delete/replace    |
| **Palindrome**    | `dp[i][j]` = is `s[i..j]` palindrome                | Check ends match         |

### 2. Common DP Frameworks

```csharp
// 1D DP with lookback
for (int i = 1; i <= n; i++)
{
    dp[i] = Process(dp[i-1], dp[i-2], ...);
}

// Space optimization (Fibonacci-like)
int prev2 = base1, prev1 = base2;
for (int i = start; i <= n; i++)
{
    int curr = prev1 + prev2;
    prev2 = prev1;
    prev1 = curr;
}

// Split point DP
for (int i = 1; i <= n; i++)
{
    for (int j = 0; j < i; j++)
    {
        if (ValidPrefix(j) && ValidSuffix(j, i))
            dp[i] = true;
    }
}
```

### 3. Decision Tree Thinking

For Decode Ways:

```
"226"
  ├─ "2" + decode("26") → ways from "26"
  └─ "22" + decode("6") → ways from "6"

Each position: try single char OR two chars (if valid)
```

### 4. Interview Tips

✅ **Start with recursion:** Understand the decision tree first  
✅ **Identify overlapping subproblems:** Signals DP solution  
✅ **Define state clearly:** What does `dp[i]` represent?  
✅ **Handle edge cases:** Empty strings, leading zeros, invalid inputs  
✅ **Optimize space:** If only need last k values, use variables

---

## Practice Problems

### Easy

1. **Climbing Stairs** ✓ (Covered above)
2. **Fibonacci Number** - Same pattern as stairs

### Medium

3. **Decode Ways** ✓ (Covered above)
4. **Word Break** ✓ (Covered above)
5. **Decode Ways II** - With wildcards ('\*')
6. **Unique Paths** - Grid DP
7. **Coin Change** - Classic DP

### Hard

8. **Word Break II** - Return all possible segmentations
9. **Edit Distance** - Two-string DP
10. **Distinct Subsequences** - Advanced string DP

---

## Common Mistakes to Avoid

❌ **Forgetting base cases** - `dp[0]` initialization is critical  
❌ **Off-by-one errors** - String indexing vs DP array indexing  
❌ **Not handling leading zeros** - "06" is invalid in Decode Ways  
❌ **Wrong boundary checks** - Two-digit decode: check both range and bounds  
❌ **Substring inefficiency** - Consider using indices instead of substrings

---

## Time Complexity Summary

| Problem         | Recursive | DP    | Space-Optimized |
| --------------- | --------- | ----- | --------------- |
| Decode Ways     | O(2^n)    | O(n)  | O(1)            |
| Climbing Stairs | O(2^n)    | O(n)  | O(1)            |
| Word Break      | O(2^n)    | O(n²) | O(n)            |

---

## Next Steps

- ✅ Master the Fibonacci-like DP pattern
- 📚 Practice two-string DP (Edit Distance, LCS)
- 🎯 Try palindrome substring problems
- 💡 Learn when to use DP vs greedy

**Remember:** String DP is about making choices at each position. Draw the decision tree, find overlapping subproblems, then convert to DP!
