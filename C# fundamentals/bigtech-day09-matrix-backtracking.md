# Day 9: Matrix Backtracking & Word Search 🎯

## Overview

**Matrix backtracking** problems appear in approximately **10-15%** of big tech interviews, testing your ability to explore all possible paths. These problems combine:

- Backtracking fundamentals
- 2D array traversal
- State management (visited tracking)
- Pruning optimization

**Key Insight:** Backtracking explores all possibilities but prunes invalid paths early. For matrices, mark cells as visited, explore neighbors, then unmark (backtrack).

---

## Backtracking Template for Matrix

```csharp
public class Solution
{
    private int[][] directions = {
        new int[] {-1, 0},  // Up
        new int[] {1, 0},   // Down
        new int[] {0, -1},  // Left
        new int[] {0, 1}    // Right
    };

    private bool Backtrack(char[][] board, int row, int col)
    {
        // Base case: check if solution found
        if (/* solution found */)
            return true;

        // Check boundaries and validity
        if (row < 0 || row >= board.Length ||
            col < 0 || col >= board[0].Length ||
            /* invalid condition */)
            return false;

        // Mark as visited
        char temp = board[row][col];
        board[row][col] = '#';  // Or use visited array

        // Explore all 4 directions
        foreach (var dir in directions)
        {
            int newRow = row + dir[0];
            int newCol = col + dir[1];

            if (Backtrack(board, newRow, newCol))
                return true;
        }

        // Backtrack: unmark
        board[row][col] = temp;

        return false;
    }
}
```

---

## Problem 1: Word Search ⭐⭐⭐ (Medium)

### Problem Statement

Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.

The word can be constructed from letters of sequentially **adjacent cells**, where adjacent cells are horizontally or vertically neighboring. The same letter cell may **not be used more than once**.

### Example

```
Input: board =
[["A","B","C","E"],
 ["S","F","C","S"],
 ["A","D","E","E"]],
word = "ABCCED"

Output: true

Input: board =
[["A","B","C","E"],
 ["S","F","C","S"],
 ["A","D","E","E"]],
word = "SEE"

Output: true

Input: board =
[["A","B","C","E"],
 ["S","F","C","S"],
 ["A","D","E","E"]],
word = "ABCB"

Output: false
Explanation: Cannot reuse the same cell
```

---

### Solution: Backtracking with In-Place Marking (Optimal)

```csharp
public class Solution
{
    private int[][] directions = {
        new int[] {-1, 0}, new int[] {1, 0},
        new int[] {0, -1}, new int[] {0, 1}
    };

    public bool Exist(char[][] board, string word)
    {
        int m = board.Length, n = board[0].Length;

        // Try starting from each cell
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (board[i][j] == word[0])
                {
                    if (Backtrack(board, i, j, word, 0))
                        return true;
                }
            }
        }

        return false;
    }

    private bool Backtrack(char[][] board, int row, int col, string word, int index)
    {
        // Found complete word
        if (index == word.Length)
            return true;

        // Check boundaries
        if (row < 0 || row >= board.Length ||
            col < 0 || col >= board[0].Length ||
            board[row][col] != word[index])
            return false;

        // Mark as visited
        char temp = board[row][col];
        board[row][col] = '#';

        // Explore all 4 directions
        foreach (var dir in directions)
        {
            int newRow = row + dir[0];
            int newCol = col + dir[1];

            if (Backtrack(board, newRow, newCol, word, index + 1))
            {
                board[row][col] = temp;  // Restore before returning
                return true;
            }
        }

        // Backtrack: unmark
        board[row][col] = temp;

        return false;
    }
}
```

**Time Complexity:** O(m × n × 4^L) where L is word length

- Try all cells: O(m × n)
- Each cell: up to 4^L paths (4 directions, L depth)
- Pruning reduces actual runtime significantly

**Space Complexity:** O(L) - Recursion stack depth

**Explanation:**

1. **Try each cell as starting point**
2. **Backtrack:** Mark visited, explore neighbors, unmark
3. **In-place marking:** Use '#' instead of separate visited array
4. **Early termination:** Return true immediately when word found
5. **Pruning:** Stop if character doesn't match

---

### Solution 2: With Separate Visited Array (Alternative)

```csharp
public class Solution
{
    public bool Exist(char[][] board, string word)
    {
        int m = board.Length, n = board[0].Length;
        bool[,] visited = new bool[m, n];

        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (Backtrack(board, i, j, word, 0, visited))
                    return true;
            }
        }

        return false;
    }

    private bool Backtrack(char[][] board, int row, int col,
                           string word, int index, bool[,] visited)
    {
        if (index == word.Length)
            return true;

        if (row < 0 || row >= board.Length ||
            col < 0 || col >= board[0].Length ||
            visited[row, col] ||
            board[row][col] != word[index])
            return false;

        visited[row, col] = true;

        // Try all 4 directions
        bool found = Backtrack(board, row - 1, col, word, index + 1, visited) ||
                     Backtrack(board, row + 1, col, word, index + 1, visited) ||
                     Backtrack(board, row, col - 1, word, index + 1, visited) ||
                     Backtrack(board, row, col + 1, word, index + 1, visited);

        visited[row, col] = false;  // Backtrack

        return found;
    }
}
```

**Time Complexity:** O(m × n × 4^L)  
**Space Complexity:** O(m × n + L) - Visited array + stack

**Explanation:**

- Separate visited array instead of modifying board
- More space but cleaner separation of concerns

---

## Problem 2: Number of Islands ⭐⭐ (Medium)

### Problem Statement

Given an `m x n` 2D binary grid which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

### Example

```
Input: grid =
[["1","1","1","1","0"],
 ["1","1","0","1","0"],
 ["1","1","0","0","0"],
 ["0","0","0","0","0"]]

Output: 1

Input: grid =
[["1","1","0","0","0"],
 ["1","1","0","0","0"],
 ["0","0","1","0","0"],
 ["0","0","0","1","1"]]

Output: 3
```

---

### Solution: DFS with In-Place Marking

```csharp
public class Solution
{
    public int NumIslands(char[][] grid)
    {
        if (grid == null || grid.Length == 0)
            return 0;

        int m = grid.Length, n = grid[0].Length;
        int count = 0;

        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (grid[i][j] == '1')
                {
                    count++;
                    DFS(grid, i, j);  // Mark entire island
                }
            }
        }

        return count;
    }

    private void DFS(char[][] grid, int row, int col)
    {
        // Check boundaries and if it's land
        if (row < 0 || row >= grid.Length ||
            col < 0 || col >= grid[0].Length ||
            grid[row][col] != '1')
            return;

        // Mark as visited
        grid[row][col] = '0';  // Or use '#'

        // Explore all 4 directions
        DFS(grid, row - 1, col);  // Up
        DFS(grid, row + 1, col);  // Down
        DFS(grid, row, col - 1);  // Left
        DFS(grid, row, col + 1);  // Right
    }
}
```

**Time Complexity:** O(m × n) - Visit each cell once  
**Space Complexity:** O(m × n) - Recursion stack in worst case

**Explanation:**

1. Scan entire grid
2. When find '1', increment count and mark entire island
3. DFS marks all connected '1's as '0'
4. This is graph traversal on implicit grid graph

---

## Problem 3: Surrounded Regions ⭐⭐ (Medium)

### Problem Statement

Given an `m x n` matrix `board` containing `'X'` and `'O'`, capture all regions that are **4-directionally surrounded** by `'X'`.

A region is captured by flipping all `'O'`s into `'X'`s in that surrounded region.

**Note:** Regions connected to the border cannot be captured.

### Example

```
Input: board =
[["X","X","X","X"],
 ["X","O","O","X"],
 ["X","X","O","X"],
 ["X","O","X","X"]]

Output:
[["X","X","X","X"],
 ["X","X","X","X"],
 ["X","X","X","X"],
 ["X","O","X","X"]]

Explanation: O's connected to border (bottom-left) are not surrounded
```

---

### Solution: Mark Border-Connected Regions

```csharp
public class Solution
{
    public void Solve(char[][] board)
    {
        if (board == null || board.Length == 0)
            return;

        int m = board.Length, n = board[0].Length;

        // Step 1: Mark all O's connected to border as safe (use 'T')

        // Top and bottom borders
        for (int j = 0; j < n; j++)
        {
            if (board[0][j] == 'O')
                MarkSafe(board, 0, j);
            if (board[m - 1][j] == 'O')
                MarkSafe(board, m - 1, j);
        }

        // Left and right borders
        for (int i = 0; i < m; i++)
        {
            if (board[i][0] == 'O')
                MarkSafe(board, i, 0);
            if (board[i][n - 1] == 'O')
                MarkSafe(board, i, n - 1);
        }

        // Step 2: Flip all remaining O's to X's (surrounded)
        //         Flip all T's back to O's (safe)
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (board[i][j] == 'O')
                    board[i][j] = 'X';
                else if (board[i][j] == 'T')
                    board[i][j] = 'O';
            }
        }
    }

    private void MarkSafe(char[][] board, int row, int col)
    {
        if (row < 0 || row >= board.Length ||
            col < 0 || col >= board[0].Length ||
            board[row][col] != 'O')
            return;

        board[row][col] = 'T';  // Temporary marker for safe

        MarkSafe(board, row - 1, col);
        MarkSafe(board, row + 1, col);
        MarkSafe(board, row, col - 1);
        MarkSafe(board, row, col + 1);
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n) - Recursion stack

**Explanation:**

1. **Key insight:** O's on border or connected to border cannot be surrounded
2. **Step 1:** DFS from border O's, mark them as 'T' (safe)
3. **Step 2:** Flip remaining O's to X's (they're surrounded)
4. **Step 3:** Flip T's back to O's
5. Reverse thinking: find what NOT to capture

---

## Problem 4: Pacific Atlantic Water Flow ⭐⭐⭐ (Medium)

### Problem Statement

Given an `m x n` matrix of non-negative integers representing the height of each cell. The "Pacific ocean" touches the left and top edges, and the "Atlantic ocean" touches the right and bottom edges.

Water can flow from a cell to another **directly** adjacent cell (north, south, east, or west) if the adjacent cell's height is **less than or equal to** the current cell's height.

Find all cells where water can flow to **both** the Pacific and Atlantic oceans.

### Example

```
Input: heights =
[[1,2,2,3,5],
 [3,2,3,4,4],
 [2,4,5,3,1],
 [6,7,1,4,5],
 [5,1,1,2,4]]

Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

---

### Solution: Two DFS from Ocean Borders

```csharp
public class Solution
{
    public IList<IList<int>> PacificAtlantic(int[][] heights)
    {
        var result = new List<IList<int>>();
        if (heights == null || heights.Length == 0)
            return result;

        int m = heights.Length, n = heights[0].Length;
        bool[,] pacific = new bool[m, n];
        bool[,] atlantic = new bool[m, n];

        // DFS from Pacific borders (top and left)
        for (int i = 0; i < m; i++)
            DFS(heights, i, 0, pacific, heights[i][0]);
        for (int j = 0; j < n; j++)
            DFS(heights, 0, j, pacific, heights[0][j]);

        // DFS from Atlantic borders (bottom and right)
        for (int i = 0; i < m; i++)
            DFS(heights, i, n - 1, atlantic, heights[i][n - 1]);
        for (int j = 0; j < n; j++)
            DFS(heights, m - 1, j, atlantic, heights[m - 1][j]);

        // Find cells reachable from both oceans
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (pacific[i, j] && atlantic[i, j])
                {
                    result.Add(new List<int> { i, j });
                }
            }
        }

        return result;
    }

    private void DFS(int[][] heights, int row, int col,
                     bool[,] visited, int prevHeight)
    {
        if (row < 0 || row >= heights.Length ||
            col < 0 || col >= heights[0].Length ||
            visited[row, col] ||
            heights[row][col] < prevHeight)  // Water flows downhill
            return;

        visited[row, col] = true;

        DFS(heights, row - 1, col, visited, heights[row][col]);
        DFS(heights, row + 1, col, visited, heights[row][col]);
        DFS(heights, row, col - 1, visited, heights[row][col]);
        DFS(heights, row, col + 1, visited, heights[row][col]);
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n)

**Explanation:**

1. **Reverse thinking:** Instead of "can flow TO ocean", think "can flow FROM ocean"
2. DFS from Pacific borders, mark reachable cells
3. DFS from Atlantic borders, mark reachable cells
4. Cells marked by both can flow to both oceans
5. Water flows from high to low, so DFS only continues if `height >= prevHeight`

---

## Key Takeaways

### 1. Matrix Backtracking Patterns

| Problem Type           | Key Technique                        |
| ---------------------- | ------------------------------------ |
| **Word Search**        | Backtrack with visited marking       |
| **Islands**            | DFS/BFS to mark connected components |
| **Surrounded Regions** | Mark from border, flip rest          |
| **Water Flow**         | Reverse DFS from destination         |

### 2. Common Techniques

```csharp
// In-place marking
char temp = board[row][col];
board[row][col] = '#';
// ... explore ...
board[row][col] = temp;  // Restore

// Separate visited array
bool[,] visited = new bool[m, n];
visited[row, col] = true;
// ... explore ...
visited[row, col] = false;  // Backtrack

// 4-direction exploration
int[][] dirs = {
    new int[] {-1,0}, {1,0}, {0,-1}, {0,1}
};
foreach (var dir in dirs)
{
    int nr = row + dir[0], nc = col + dir[1];
    DFS(board, nr, nc);
}
```

### 3. When to Use Each Approach

✅ **In-place marking:** When allowed to modify input (space optimization)  
✅ **Visited array:** When must preserve original board  
✅ **Reverse DFS:** When easier to think from destination  
✅ **BFS:** When need shortest path or level-by-level

### 4. Interview Tips

✅ **Ask about modification:** Can I modify the input board?  
✅ **Boundary checking:** Always validate row/col bounds first  
✅ **Base case first:** Check termination before recursion  
✅ **Restore state:** Remember to backtrack (unmark)  
✅ **Direction array:** Cleaner than 4 separate calls

---

## Practice Problems

### Medium

1. **Word Search** ✓ (Covered above)
2. **Number of Islands** ✓ (Covered above)
3. **Surrounded Regions** ✓ (Covered above)
4. **Pacific Atlantic Water Flow** ✓ (Covered above)
5. **Max Area of Island** - Similar to Number of Islands
6. **Shortest Path in Binary Matrix** - BFS variation

### Hard

7. **Word Search II** - Trie + backtracking
8. **Robot Room Cleaner** - Backtracking with unknown grid

---

## Common Mistakes to Avoid

❌ **Not restoring state** - Forgetting to backtrack/unmark  
❌ **Wrong boundary check** - Off-by-one errors  
❌ **Modifying during iteration** - Can cause incorrect results  
❌ **Infinite recursion** - Not marking visited  
❌ **Wrong direction** - Water flow vs path finding logic

---

## Time Complexity Summary

| Problem                | Time       | Space  | Notes                |
| ---------------------- | ---------- | ------ | -------------------- |
| **Word Search**        | O(m×n×4^L) | O(L)   | L = word length      |
| **Number of Islands**  | O(m×n)     | O(m×n) | DFS stack worst case |
| **Surrounded Regions** | O(m×n)     | O(m×n) | DFS from borders     |
| **Pacific Atlantic**   | O(m×n)     | O(m×n) | Two DFS passes       |

---

## Next Steps

- ✅ Master backtracking template
- 📚 Practice with Trie for Word Search II
- 🎯 Study graph traversal on implicit grids
- 💡 Learn BFS for shortest path variants

**Remember:** Matrix backtracking is about exploring paths while maintaining state. Always mark visited, explore neighbors, then unmark (backtrack)!
