# Day 12: Backtracking & Recursion

## Backtracking Template

```csharp
void Backtrack(state, choices, result)
{
    if (isGoal(state))
    {
        result.Add(new List<T>(state));
        return;
    }

    foreach (choice in choices)
    {
        if (isValid(choice))
        {
            makeChoice(choice);
            Backtrack(newState, newChoices, result);
            undoChoice(choice); // Backtrack!
        }
    }
}
```

## Problem 1: Subsets (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

Given an array of distinct integers, return all possible subsets (the power set).

**Example:**

```
Input: nums = [1,2,3]
Output: [[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]
```

### Solution: Backtracking

```csharp
public class Solution
{
    public IList<IList<int>> Subsets(int[] nums)
    {
        var result = new List<IList<int>>();
        var current = new List<int>();
        Backtrack(nums, 0, current, result);
        return result;
    }

    private void Backtrack(int[] nums, int start, List<int> current, List<IList<int>> result)
    {
        // Add current subset to result
        result.Add(new List<int>(current));

        for (int i = start; i < nums.Length; i++)
        {
            // Include nums[i]
            current.Add(nums[i]);

            // Recurse with next elements
            Backtrack(nums, i + 1, current, result);

            // Backtrack: remove nums[i]
            current.RemoveAt(current.Count - 1);
        }
    }
}
```

**Time Complexity:** O(2^n × n) - 2^n subsets, O(n) to copy each  
**Space Complexity:** O(n) - Recursion depth

**Explanation:**

- For each element: include it or skip it
- Add current subset at each step
- Backtrack by removing last element
- Classic backtracking pattern

---

## Problem 2: Permutations (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given an array of distinct integers, return all possible permutations.

**Example:**

```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Solution: Backtracking with Swap

```csharp
public class Solution
{
    public IList<IList<int>> Permute(int[] nums)
    {
        var result = new List<IList<int>>();
        Backtrack(nums, 0, result);
        return result;
    }

    private void Backtrack(int[] nums, int start, List<IList<int>> result)
    {
        if (start == nums.Length)
        {
            result.Add(new List<int>(nums));
            return;
        }

        for (int i = start; i < nums.Length; i++)
        {
            // Swap current element to start position
            Swap(nums, start, i);

            // Recurse with next position
            Backtrack(nums, start + 1, result);

            // Backtrack: swap back
            Swap(nums, start, i);
        }
    }

    private void Swap(int[] nums, int i, int j)
    {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

**Time Complexity:** O(n! × n)  
**Space Complexity:** O(n)

**Explanation:**

- Fix first position, permute rest
- Swap elements to try different orderings
- Backtrack by swapping back
- Generates all n! permutations

---

## Problem 3: N-Queens (Hard)

**Difficulty:** ⭐⭐⭐ Hard

### Problem Statement

Place n queens on an n×n chessboard so no two queens attack each other. Return all distinct solutions.

**Example:**

```
Input: n = 4
Output: [
 [".Q..",
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",
  "Q...",
  "...Q",
  ".Q.."]
]
```

### Solution: Backtracking with Validation

```csharp
public class Solution
{
    public IList<IList<string>> SolveNQueens(int n)
    {
        var result = new List<IList<string>>();
        var board = new char[n][];

        // Initialize board
        for (int i = 0; i < n; i++)
        {
            board[i] = new char[n];
            Array.Fill(board[i], '.');
        }

        Backtrack(board, 0, result);
        return result;
    }

    private void Backtrack(char[][] board, int row, List<IList<string>> result)
    {
        if (row == board.Length)
        {
            // Found valid solution
            result.Add(board.Select(r => new string(r)).ToList());
            return;
        }

        for (int col = 0; col < board.Length; col++)
        {
            if (IsValid(board, row, col))
            {
                board[row][col] = 'Q'; // Place queen
                Backtrack(board, row + 1, result);
                board[row][col] = '.'; // Backtrack
            }
        }
    }

    private bool IsValid(char[][] board, int row, int col)
    {
        int n = board.Length;

        // Check column
        for (int i = 0; i < row; i++)
        {
            if (board[i][col] == 'Q') return false;
        }

        // Check diagonal (top-left)
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--)
        {
            if (board[i][j] == 'Q') return false;
        }

        // Check diagonal (top-right)
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++)
        {
            if (board[i][j] == 'Q') return false;
        }

        return true;
    }
}
```

**Time Complexity:** O(n!)  
**Space Complexity:** O(n²)

**Explanation:**

- Place queens row by row
- Check if position is safe (no attacks)
- Backtrack if can't place queen
- Classic constraint satisfaction problem

---

## Key Takeaways for Day 12

### Backtracking vs DP

- **Backtracking:** Explore all possibilities, prune invalid paths
- **DP:** Optimal solution, overlapping subproblems
- **When:** Backtracking for "find all", DP for "find best"

### Common Backtracking Problems

- **Combinations/Subsets:** Choose or not choose
- **Permutations:** Different orderings
- **Constraint Satisfaction:** N-Queens, Sudoku
- **Path Finding:** Maze, word search

### Optimization Techniques

1. **Pruning:** Skip invalid branches early
2. **Ordering:** Try most constrained first
3. **Memoization:** Cache visited states

**Tomorrow:** Day 13 - Greedy Algorithms
