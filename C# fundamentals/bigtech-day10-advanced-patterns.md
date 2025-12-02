# Day 10: Advanced Mixed Patterns 🎯

## Overview

This final day covers **advanced problem-solving patterns** that combine multiple concepts. These appear in approximately **15-20%** of interviews and test your ability to:

- Recognize multiple patterns in one problem
- Optimize complex solutions
- Handle edge cases elegantly
- Think creatively about data structures

**Key Insight:** Advanced problems often require combining techniques: sliding window + hash map, binary search + DP, monotonic stack + DP, etc.

---

## Problem 1: Longest Increasing Path in Matrix ⭐⭐⭐ (Hard)

### Problem Statement

Given an `m x n` integers matrix, return the length of the **longest increasing path** in the matrix.

From each cell, you can move in four directions (up, down, left, right). You **cannot** move diagonally or outside the boundary.

### Example

```
Input: matrix =
[[9,9,4],
 [6,6,8],
 [2,1,1]]

Output: 4
Explanation: The longest path is [1, 2, 6, 9]

Input: matrix =
[[3,4,5],
 [3,2,6],
 [2,2,1]]

Output: 4
Explanation: The longest path is [3, 4, 5, 6]
```

---

### Solution: DFS + Memoization (Optimal)

```csharp
public class Solution
{
    private int[][] directions = {
        new int[] {-1, 0}, new int[] {1, 0},
        new int[] {0, -1}, new int[] {0, 1}
    };

    public int LongestIncreasingPath(int[][] matrix)
    {
        if (matrix == null || matrix.Length == 0)
            return 0;

        int m = matrix.Length, n = matrix[0].Length;
        int[,] memo = new int[m, n];  // Cache longest path from each cell
        int maxPath = 0;

        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                maxPath = Math.Max(maxPath, DFS(matrix, i, j, memo));
            }
        }

        return maxPath;
    }

    private int DFS(int[][] matrix, int row, int col, int[,] memo)
    {
        if (memo[row, col] != 0)
            return memo[row, col];

        int maxLength = 1;  // At least the cell itself

        foreach (var dir in directions)
        {
            int newRow = row + dir[0];
            int newCol = col + dir[1];

            // Check bounds and increasing condition
            if (newRow >= 0 && newRow < matrix.Length &&
                newCol >= 0 && newCol < matrix[0].Length &&
                matrix[newRow][newCol] > matrix[row][col])
            {
                int length = 1 + DFS(matrix, newRow, newCol, memo);
                maxLength = Math.Max(maxLength, length);
            }
        }

        memo[row, col] = maxLength;
        return maxLength;
    }
}
```

**Time Complexity:** O(m × n) - Each cell visited once due to memoization  
**Space Complexity:** O(m × n) - Memo array + recursion stack

**Explanation:**

1. **DFS from every cell** to find longest increasing path
2. **Memoization:** Cache result for each cell to avoid recomputation
3. **Increasing constraint:** Only move to cells with larger values
4. **No visited tracking needed:** Increasing constraint prevents cycles
5. Combines: DFS + DP memoization

---

## Problem 2: Sliding Window Maximum ⭐⭐⭐ (Hard)

### Problem Statement

You are given an array of integers `nums`, and an integer `k`. There is a sliding window of size `k` which is moving from the left to the right. You can only see the `k` numbers in the window.

Return the **max** sliding window (the maximum value in each window).

### Example

```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation:
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

---

### Solution: Monotonic Deque (Optimal)

```csharp
public class Solution
{
    public int[] MaxSlidingWindow(int[] nums, int k)
    {
        if (nums == null || nums.Length == 0 || k <= 0)
            return new int[0];

        int n = nums.Length;
        int[] result = new int[n - k + 1];
        var deque = new LinkedList<int>();  // Store indices

        for (int i = 0; i < n; i++)
        {
            // Remove indices outside current window
            while (deque.Count > 0 && deque.First.Value < i - k + 1)
            {
                deque.RemoveFirst();
            }

            // Remove indices of elements smaller than current
            // (they'll never be max in future windows)
            while (deque.Count > 0 && nums[deque.Last.Value] < nums[i])
            {
                deque.RemoveLast();
            }

            deque.AddLast(i);

            // Record result when window is full
            if (i >= k - 1)
            {
                result[i - k + 1] = nums[deque.First.Value];
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(n) - Each element added/removed at most once  
**Space Complexity:** O(k) - Deque size at most k

**Explanation:**

1. **Monotonic deque:** Keep indices in decreasing order of values
2. **Front = maximum:** First element is always current window max
3. **Remove outside window:** Pop front if index too old
4. **Maintain monotonic:** Pop back while current > back (they're useless)
5. Combines: Sliding window + monotonic deque

**Why monotonic?** If `nums[i] < nums[j]` and `i < j`, then `nums[i]` will never be maximum after `j` enters window.

---

## Problem 3: Trapping Rain Water ⭐⭐⭐ (Hard)

### Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Example

```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6

Visual:
       █
   █   ██ █
 █ ██ ███████
```

---

### Solution 1: Two Pointers (Optimal)

```csharp
public class Solution
{
    public int Trap(int[] height)
    {
        if (height == null || height.Length == 0)
            return 0;

        int left = 0, right = height.Length - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        while (left < right)
        {
            if (height[left] < height[right])
            {
                // Process left side
                if (height[left] >= leftMax)
                {
                    leftMax = height[left];
                }
                else
                {
                    water += leftMax - height[left];
                }
                left++;
            }
            else
            {
                // Process right side
                if (height[right] >= rightMax)
                {
                    rightMax = height[right];
                }
                else
                {
                    water += rightMax - height[right];
                }
                right--;
            }
        }

        return water;
    }
}
```

**Time Complexity:** O(n) - Single pass  
**Space Complexity:** O(1) - Constant space

**Explanation:**

1. **Two pointers:** Process from both ends
2. **Key insight:** Water at position depends on min(leftMax, rightMax)
3. **Greedy choice:** Process side with smaller height
4. If `height[left] < height[right]`, water at left is bounded by leftMax
5. Combines: Two pointers + greedy

---

### Solution 2: Stack (Alternative)

```csharp
public class Solution
{
    public int Trap(int[] height)
    {
        var stack = new Stack<int>();  // Store indices
        int water = 0;

        for (int i = 0; i < height.Length; i++)
        {
            // Pop bars that are shorter than current
            while (stack.Count > 0 && height[i] > height[stack.Peek()])
            {
                int top = stack.Pop();

                if (stack.Count == 0)
                    break;

                int distance = i - stack.Peek() - 1;
                int boundedHeight = Math.Min(height[i], height[stack.Peek()]) - height[top];
                water += distance * boundedHeight;
            }

            stack.Push(i);
        }

        return water;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n) - Stack

**Explanation:**

- Stack stores indices of bars
- Calculate water layer by layer horizontally
- When find taller bar, calculate trapped water

---

## Problem 4: Shortest Path in Binary Matrix ⭐⭐ (Medium)

### Problem Statement

Given an `n x n` binary matrix `grid`, return the length of the shortest **clear path** in the matrix. If there is no clear path, return `-1`.

A **clear path** is a path from top-left `(0, 0)` to bottom-right `(n-1, n-1)` such that:

- All visited cells are `0`
- All adjacent cells are **8-directionally** connected

The **length** of the path is the number of visited cells.

### Example

```
Input: grid =
[[0,1],
 [1,0]]
Output: 2

Input: grid =
[[0,0,0],
 [1,1,0],
 [1,1,0]]
Output: 4 (path: (0,0) → (0,1) → (0,2) → (1,2) → (2,2))
```

---

### Solution: BFS (Optimal for Shortest Path)

```csharp
public class Solution
{
    private int[][] directions = {
        new int[] {-1, -1}, new int[] {-1, 0}, new int[] {-1, 1},
        new int[] {0, -1},                     new int[] {0, 1},
        new int[] {1, -1},  new int[] {1, 0},  new int[] {1, 1}
    };

    public int ShortestPathBinaryMatrix(int[][] grid)
    {
        int n = grid.Length;

        // Check start and end
        if (grid[0][0] != 0 || grid[n - 1][n - 1] != 0)
            return -1;

        var queue = new Queue<(int row, int col, int dist)>();
        queue.Enqueue((0, 0, 1));
        grid[0][0] = 1;  // Mark as visited

        while (queue.Count > 0)
        {
            var (row, col, dist) = queue.Dequeue();

            // Reached destination
            if (row == n - 1 && col == n - 1)
                return dist;

            // Explore all 8 directions
            foreach (var dir in directions)
            {
                int newRow = row + dir[0];
                int newCol = col + dir[1];

                if (newRow >= 0 && newRow < n &&
                    newCol >= 0 && newCol < n &&
                    grid[newRow][newCol] == 0)
                {
                    queue.Enqueue((newRow, newCol, dist + 1));
                    grid[newRow][newCol] = 1;  // Mark visited
                }
            }
        }

        return -1;  // No path found
    }
}
```

**Time Complexity:** O(n²) - Visit each cell at most once  
**Space Complexity:** O(n²) - Queue size

**Explanation:**

1. **BFS for shortest path** in unweighted graph
2. **8-directional movement** (including diagonals)
3. Mark visited by changing grid value
4. Track distance with each cell
5. Return distance when reach destination

---

## Problem 5: Jump Game II ⭐⭐ (Medium)

### Problem Statement

You are given a **0-indexed** array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.

Each element `nums[i]` represents the maximum jump length from that position.

Return the **minimum number of jumps** to reach `nums[n - 1]`.

### Example

```
Input: nums = [2,3,1,1,4]
Output: 2
Explanation: Jump from index 0 to 1, then to last index

Input: nums = [2,3,0,1,4]
Output: 2
```

---

### Solution: Greedy with Range (Optimal)

```csharp
public class Solution
{
    public int Jump(int[] nums)
    {
        int jumps = 0;
        int currentEnd = 0;     // End of range for current jump
        int farthest = 0;       // Farthest we can reach

        // Don't need to jump from last position
        for (int i = 0; i < nums.Length - 1; i++)
        {
            // Update farthest reachable position
            farthest = Math.Max(farthest, i + nums[i]);

            // When reach end of current jump range
            if (i == currentEnd)
            {
                jumps++;
                currentEnd = farthest;

                // Early termination if can reach end
                if (currentEnd >= nums.Length - 1)
                    break;
            }
        }

        return jumps;
    }
}
```

**Time Complexity:** O(n) - Single pass  
**Space Complexity:** O(1)

**Explanation:**

1. **Greedy:** Always jump to position that lets us reach farthest
2. **Current range:** `[start, currentEnd]` - positions reachable with current jumps
3. **Farthest:** Maximum position reachable from current range
4. **When reach end of range:** Must make a jump, update range to farthest
5. Combines: Greedy + range tracking

**Visual Example for [2,3,1,1,4]:**

```
Index:  0  1  2  3  4
Nums:   2  3  1  1  4
        └──┘
Jump 1: Can reach 0-2, farthest = 4 (from index 1: 1+3)
        ↓
   currentEnd = 2

Index 2: i == currentEnd, make jump
Jump 2: Can reach 3-4, destination reached
```

---

## Key Takeaways

### 1. Pattern Combinations

| Problem                     | Patterns Combined                |
| --------------------------- | -------------------------------- |
| **Longest Increasing Path** | DFS + DP memoization             |
| **Sliding Window Max**      | Sliding window + monotonic deque |
| **Trapping Rain Water**     | Two pointers + greedy            |
| **Shortest Path Matrix**    | BFS + grid traversal             |
| **Jump Game II**            | Greedy + range tracking          |

### 2. Advanced Techniques

```csharp
// Monotonic Deque
var deque = new LinkedList<int>();
while (deque.Count > 0 && condition)
    deque.RemoveLast();
deque.AddLast(element);

// DFS + Memoization
int[,] memo = new int[m, n];
int DFS(int i, int j)
{
    if (memo[i, j] != 0) return memo[i, j];
    // ... compute ...
    return memo[i, j] = result;
}

// Greedy with Range
int currentEnd = 0, farthest = 0;
for (int i = 0; i < n; i++)
{
    farthest = Math.Max(farthest, i + nums[i]);
    if (i == currentEnd)
    {
        currentEnd = farthest;
        jumps++;
    }
}
```

### 3. Problem-Solving Strategy

✅ **Identify sub-patterns:** Break complex problem into known patterns  
✅ **Consider constraints:** What makes this problem unique?  
✅ **Optimize incrementally:** Start simple, then optimize  
✅ **Test edge cases:** Empty input, single element, max constraints

### 4. Interview Tips

✅ **Explain your thinking:** "This combines X pattern with Y optimization"  
✅ **Start with brute force:** Then optimize based on constraints  
✅ **Ask clarifying questions:** Understand all requirements first  
✅ **Consider time-space tradeoffs:** Often can trade one for other  
✅ **Test with examples:** Walk through your solution step by step

---

## Practice Problems

### Medium

1. **Longest Increasing Path** ✓ (Covered above)
2. **Shortest Path in Binary Matrix** ✓ (Covered above)
3. **Jump Game II** ✓ (Covered above)
4. **Course Schedule III** - Greedy + heap
5. **Task Scheduler** - Greedy + queue

### Hard

6. **Sliding Window Maximum** ✓ (Covered above)
7. **Trapping Rain Water** ✓ (Covered above)
8. **Longest Valid Parentheses** - DP or stack
9. **Maximal Rectangle** - Stack + DP
10. **Regular Expression Matching** - DP

---

## Common Mistakes to Avoid

❌ **Overcomplicating:** Sometimes simpler approach works  
❌ **Forgetting memoization:** DFS without cache → TLE  
❌ **Wrong data structure:** Deque vs queue vs stack matters  
❌ **Not testing edge cases:** Always check boundaries  
❌ **Premature optimization:** Understand problem first

---

## Time Complexity Summary

| Problem                  | Brute Force | Optimal | Key Optimization |
| ------------------------ | ----------- | ------- | ---------------- |
| **Longest Path Matrix**  | O(2^(m×n))  | O(m×n)  | Memoization      |
| **Sliding Window Max**   | O(n×k)      | O(n)    | Monotonic deque  |
| **Trapping Rain Water**  | O(n²)       | O(n)    | Two pointers     |
| **Shortest Path Matrix** | -           | O(n²)   | BFS (inherent)   |
| **Jump Game II**         | O(n²)       | O(n)    | Greedy range     |

---

## Final Interview Strategy

### Before Coding

1. **Understand the problem completely**
2. **Identify patterns** (array, string, tree, graph, DP, etc.)
3. **Think about constraints** (time/space limits)
4. **Discuss approach** with interviewer
5. **Consider edge cases**

### While Coding

1. **Write clean code** with good variable names
2. **Add comments** for complex logic
3. **Think out loud** - explain as you code
4. **Test as you go** - check small sections

### After Coding

1. **Dry run** with example
2. **Discuss time/space complexity**
3. **Mention optimizations** or alternatives
4. **Test edge cases** explicitly

---

## Next Steps

- ✅ Review all 10 days of patterns
- 📚 Practice mixing different techniques
- 🎯 Time yourself on LeetCode medium/hard
- 💡 Study company-specific problem trends

**Remember:** Advanced problems test pattern recognition and combination skills. Master individual patterns first, then practice combining them!
