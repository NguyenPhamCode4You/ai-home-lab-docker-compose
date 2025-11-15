# Day 2: Matrix Manipulation 🎯

## Overview

**Matrix manipulation** problems are extremely common at big tech companies, appearing in approximately **25% of interviews**. These problems test:

- 2D array traversal and indexing
- In-place modifications with space constraints
- Boundary condition handling
- Pattern recognition in 2D space

**Key Insight:** Many matrix problems require thinking about transformations (rotation, transposition) or layer-by-layer processing.

---

## Problem 1: Rotate Image ⭐⭐ (Medium)

### Problem Statement

You are given an `n x n` 2D matrix representing an image. Rotate the image by **90 degrees clockwise**.

You have to rotate the image **in-place**, which means you have to modify the input 2D matrix directly. **DO NOT** allocate another 2D matrix.

### Example

```
Input: matrix =
[[1,2,3],
 [4,5,6],
 [7,8,9]]

Output:
[[7,4,1],
 [8,5,2],
 [9,6,3]]

Explanation:
Rotate 90° clockwise: first column becomes first row
```

---

### Solution 1: Using Extra Space (Not Optimal)

```csharp
public class Solution
{
    public void Rotate(int[][] matrix)
    {
        int n = matrix.Length;
        int[][] temp = new int[n][];

        // Create copy
        for (int i = 0; i < n; i++)
        {
            temp[i] = new int[n];
            for (int j = 0; j < n; j++)
            {
                temp[i][j] = matrix[n - 1 - j][i];
            }
        }

        // Copy back
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                matrix[i][j] = temp[i][j];
            }
        }
    }
}
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(n²) - Extra matrix

**Explanation:**

- New position: `matrix[i][j] → temp[j][n-1-i]`
- Simple but violates in-place requirement
- Use this to understand the transformation first

---

### Solution 2: Transpose + Reverse (Optimal)

```csharp
public class Solution
{
    public void Rotate(int[][] matrix)
    {
        int n = matrix.Length;

        // Step 1: Transpose (swap across diagonal)
        for (int i = 0; i < n; i++)
        {
            for (int j = i + 1; j < n; j++)
            {
                // Swap matrix[i][j] with matrix[j][i]
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }

        // Step 2: Reverse each row
        for (int i = 0; i < n; i++)
        {
            Array.Reverse(matrix[i]);
        }
    }
}
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(1) - In-place

**Explanation:**

1. **Transpose:** Swap elements across main diagonal (i,j) ↔ (j,i)
2. **Reverse rows:** Flip each row left to right

**Visual Example:**

```
Original:       Transpose:      Reverse rows:
[1,2,3]         [1,4,7]         [7,4,1]
[4,5,6]   →     [2,5,8]   →     [8,5,2]
[7,8,9]         [3,6,9]         [9,6,3]
```

---

### Solution 3: Rotate Layer by Layer (Alternative)

```csharp
public class Solution
{
    public void Rotate(int[][] matrix)
    {
        int n = matrix.Length;

        // Process outer to inner layers
        for (int layer = 0; layer < n / 2; layer++)
        {
            int first = layer;
            int last = n - 1 - layer;

            for (int i = first; i < last; i++)
            {
                int offset = i - first;

                // Save top
                int top = matrix[first][i];

                // Left → Top
                matrix[first][i] = matrix[last - offset][first];

                // Bottom → Left
                matrix[last - offset][first] = matrix[last][last - offset];

                // Right → Bottom
                matrix[last][last - offset] = matrix[i][last];

                // Top → Right
                matrix[i][last] = top;
            }
        }
    }
}
```

**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

**Explanation:**

- Process matrix in concentric layers (rings)
- For each layer, rotate 4 elements at a time
- More complex but demonstrates layer-by-layer technique

---

## Problem 2: Spiral Matrix ⭐⭐⭐ (Medium)

### Problem Statement

Given an `m x n` matrix, return all elements of the matrix in **spiral order** (clockwise from outside to inside).

### Example

```
Input: matrix =
[[1,2,3],
 [4,5,6],
 [7,8,9]]

Output: [1,2,3,6,9,8,7,4,5]

Explanation: Start top-left, go right → down → left → up → repeat
```

---

### Solution 1: Layer by Layer (Optimal)

```csharp
public class Solution
{
    public IList<int> SpiralOrder(int[][] matrix)
    {
        var result = new List<int>();
        if (matrix.Length == 0) return result;

        int top = 0, bottom = matrix.Length - 1;
        int left = 0, right = matrix[0].Length - 1;

        while (top <= bottom && left <= right)
        {
            // Traverse right
            for (int col = left; col <= right; col++)
            {
                result.Add(matrix[top][col]);
            }
            top++;

            // Traverse down
            for (int row = top; row <= bottom; row++)
            {
                result.Add(matrix[row][right]);
            }
            right--;

            // Traverse left (check if row still exists)
            if (top <= bottom)
            {
                for (int col = right; col >= left; col--)
                {
                    result.Add(matrix[bottom][col]);
                }
                bottom--;
            }

            // Traverse up (check if column still exists)
            if (left <= right)
            {
                for (int row = bottom; row >= top; row--)
                {
                    result.Add(matrix[row][left]);
                }
                left++;
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(m × n) - Visit each element once  
**Space Complexity:** O(1) - Not counting output array

**Explanation:**

1. Use four boundaries: top, bottom, left, right
2. Process one direction at a time, then shrink boundary
3. **Critical:** Check boundaries before left and up traversal (avoid duplicates)
4. Continue until boundaries cross

---

### Solution 2: Direction Vectors (Alternative)

```csharp
public class Solution
{
    public IList<int> SpiralOrder(int[][] matrix)
    {
        var result = new List<int>();
        if (matrix.Length == 0) return result;

        int m = matrix.Length, n = matrix[0].Length;
        bool[,] visited = new bool[m, n];

        // Direction vectors: right, down, left, up
        int[] dr = { 0, 1, 0, -1 };
        int[] dc = { 1, 0, -1, 0 };

        int r = 0, c = 0, dir = 0;

        for (int i = 0; i < m * n; i++)
        {
            result.Add(matrix[r][c]);
            visited[r, c] = true;

            // Try to continue in current direction
            int nr = r + dr[dir];
            int nc = c + dc[dir];

            // If out of bounds or visited, turn right
            if (nr < 0 || nr >= m || nc < 0 || nc >= n || visited[nr, nc])
            {
                dir = (dir + 1) % 4;  // Turn right
                nr = r + dr[dir];
                nc = c + dc[dir];
            }

            r = nr;
            c = nc;
        }

        return result;
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n) - For visited array

**Explanation:**

- Use direction vectors and rotation
- Track visited cells
- More intuitive but uses extra space

---

## Problem 3: Set Matrix Zeroes ⭐⭐⭐ (Medium)

### Problem Statement

Given an `m x n` integer matrix, if an element is 0, set its entire row and column to 0. Do it **in-place**.

### Example

```
Input: matrix =
[[1,1,1],
 [1,0,1],
 [1,1,1]]

Output:
[[1,0,1],
 [0,0,0],
 [1,0,1]]

Input: matrix =
[[0,1,2,0],
 [3,4,5,2],
 [1,3,1,5]]

Output:
[[0,0,0,0],
 [0,4,5,0],
 [0,3,1,0]]
```

---

### Solution 1: Using Extra Space (Simple)

```csharp
public class Solution
{
    public void SetZeroes(int[][] matrix)
    {
        int m = matrix.Length, n = matrix[0].Length;
        var zeroRows = new HashSet<int>();
        var zeroCols = new HashSet<int>();

        // Find all zero positions
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (matrix[i][j] == 0)
                {
                    zeroRows.Add(i);
                    zeroCols.Add(j);
                }
            }
        }

        // Set rows to zero
        foreach (int row in zeroRows)
        {
            for (int j = 0; j < n; j++)
            {
                matrix[row][j] = 0;
            }
        }

        // Set columns to zero
        foreach (int col in zeroCols)
        {
            for (int i = 0; i < m; i++)
            {
                matrix[i][col] = 0;
            }
        }
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m + n) - Sets for rows and columns

**Explanation:**

- First pass: record which rows/columns have zeros
- Second pass: set those rows/columns to zero
- Simple but uses extra space

---

### Solution 2: Using First Row/Column as Markers (Optimal)

```csharp
public class Solution
{
    public void SetZeroes(int[][] matrix)
    {
        int m = matrix.Length, n = matrix[0].Length;
        bool firstRowZero = false, firstColZero = false;

        // Check if first row has zero
        for (int j = 0; j < n; j++)
        {
            if (matrix[0][j] == 0)
            {
                firstRowZero = true;
                break;
            }
        }

        // Check if first column has zero
        for (int i = 0; i < m; i++)
        {
            if (matrix[i][0] == 0)
            {
                firstColZero = true;
                break;
            }
        }

        // Use first row and column as markers
        for (int i = 1; i < m; i++)
        {
            for (int j = 1; j < n; j++)
            {
                if (matrix[i][j] == 0)
                {
                    matrix[i][0] = 0;  // Mark row
                    matrix[0][j] = 0;  // Mark column
                }
            }
        }

        // Set matrix cells to zero based on markers
        for (int i = 1; i < m; i++)
        {
            for (int j = 1; j < n; j++)
            {
                if (matrix[i][0] == 0 || matrix[0][j] == 0)
                {
                    matrix[i][j] = 0;
                }
            }
        }

        // Handle first row
        if (firstRowZero)
        {
            for (int j = 0; j < n; j++)
            {
                matrix[0][j] = 0;
            }
        }

        // Handle first column
        if (firstColZero)
        {
            for (int i = 0; i < m; i++)
            {
                matrix[i][0] = 0;
            }
        }
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(1) - In-place using matrix itself

**Explanation:**

1. **Key trick:** Use first row and column as markers
2. Check first row/column separately (they're overwritten as markers)
3. Mark zeros in rest of matrix using first row/column
4. Process matrix based on markers
5. Finally handle first row and column

---

### Solution 3: One-Pass with Marker Value (Alternative)

```csharp
public class Solution
{
    public void SetZeroes(int[][] matrix)
    {
        int m = matrix.Length, n = matrix[0].Length;
        const int MARKER = int.MinValue;

        // Mark rows and columns (use special marker)
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (matrix[i][j] == 0)
                {
                    // Mark row
                    for (int k = 0; k < n; k++)
                    {
                        if (matrix[i][k] != 0)
                            matrix[i][k] = MARKER;
                    }
                    // Mark column
                    for (int k = 0; k < m; k++)
                    {
                        if (matrix[k][j] != 0)
                            matrix[k][j] = MARKER;
                    }
                }
            }
        }

        // Replace markers with zero
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (matrix[i][j] == MARKER)
                {
                    matrix[i][j] = 0;
                }
            }
        }
    }
}
```

**Time Complexity:** O((m × n) × (m + n)) - Inefficient  
**Space Complexity:** O(1)

**Explanation:**

- Use special marker value (int.MinValue)
- Works only if that value won't appear in input
- Less efficient but conceptually simpler

---

## Key Takeaways

### 1. Matrix Transformation Patterns

| Pattern                 | Technique                       | Example         |
| ----------------------- | ------------------------------- | --------------- |
| **90° rotation**        | Transpose + Reverse rows        | Rotate Image    |
| **Spiral traversal**    | Layer by layer with boundaries  | Spiral Matrix   |
| **In-place marking**    | Use first row/column as markers | Set Zeroes      |
| **4-direction BFS/DFS** | Direction vectors `[dx, dy]`    | Island problems |

### 2. Common Matrix Operations

```csharp
// Transpose (flip across diagonal)
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        Swap(matrix[i][j], matrix[j][i]);

// Reverse rows (flip horizontally)
for (int i = 0; i < n; i++)
    Array.Reverse(matrix[i]);

// 4-direction vectors
int[] dr = { -1, 1, 0, 0 };  // Up, Down, Left, Right
int[] dc = { 0, 0, -1, 1 };
```

### 3. Space Optimization Tricks

✅ **Use matrix itself for markers** (first row/column technique)  
✅ **Process in layers** (spiral, rotation)  
✅ **Direction vectors** instead of multiple if-else  
✅ **Transpose trick** for rotation problems

### 4. Interview Tips

✅ **Clarify dimensions:** Is it square (n×n) or rectangular (m×n)?  
✅ **Ask about constraints:** Can values be negative? What's the range?  
✅ **Start with extra space:** Then optimize to in-place  
✅ **Draw examples:** Visualize transformations on paper  
✅ **Check boundaries:** Off-by-one errors are common in matrix problems

---

## Practice Problems

### Easy

1. **Transpose Matrix** - Flip along diagonal
2. **Reshape Matrix** - Convert m×n to r×c

### Medium

3. **Rotate Image** ✓ (Covered above)
4. **Spiral Matrix** ✓ (Covered above)
5. **Set Matrix Zeroes** ✓ (Covered above)
6. **Spiral Matrix II** - Generate spiral matrix
7. **Search a 2D Matrix** - Binary search in sorted matrix

### Hard

8. **Spiral Matrix III** - Spiral walk from center
9. **Longest Increasing Path in Matrix** - DFS with memoization

---

## Common Mistakes to Avoid

❌ **Modifying while iterating** - Mark first, then modify  
❌ **Forgetting boundary checks** - Always validate `i < m && j < n`  
❌ **Off-by-one in loops** - Be careful with `<` vs `<=`  
❌ **Not handling edge cases** - Empty matrix, single row/column  
❌ **Using wrong indices** - Transpose: swap `[i][j]` with `[j][i]`

---

## Time Complexity Summary

| Problem       | Approach              | Time   | Space |
| ------------- | --------------------- | ------ | ----- |
| Rotate Image  | Transpose + Reverse   | O(n²)  | O(1)  |
| Spiral Matrix | Layer by layer        | O(m×n) | O(1)  |
| Set Zeroes    | First row/col markers | O(m×n) | O(1)  |

---

## Next Steps

- ✅ Master in-place transformations
- 📚 Practice spiral and boundary management
- 🎯 Try 2D DP problems (paths, islands)
- 💡 Recognize when to use first row/column trick

**Remember:** Matrix problems reward careful boundary handling and visualization. Always draw the transformation!
