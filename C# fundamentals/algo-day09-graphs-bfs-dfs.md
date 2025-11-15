# Day 9: Graphs - BFS & DFS

## Graph Representations

```csharp
// Adjacency List (most common)
Dictionary<int, List<int>> graph = new Dictionary<int, List<int>>();

// Adjacency Matrix
int[,] graph = new int[n, n];

// Edge List
List<int[]> edges = new List<int[]>();
```

## Problem 1: Number of Islands (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given a 2D grid of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.

**Example:**

```
Input:
11110
11010
11000
00000

Output: 1

Input:
11000
11000
00100
00011

Output: 3
```

### Solution 1: DFS (Simple)

```csharp
public class Solution
{
    public int NumIslands(char[][] grid)
    {
        if (grid == null || grid.Length == 0) return 0;

        int rows = grid.Length;
        int cols = grid[0].Length;
        int count = 0;

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (grid[i][j] == '1')
                {
                    count++;
                    DFS(grid, i, j);
                }
            }
        }

        return count;
    }

    private void DFS(char[][] grid, int i, int j)
    {
        // Boundary check and water check
        if (i < 0 || i >= grid.Length || j < 0 || j >= grid[0].Length || grid[i][j] == '0')
        {
            return;
        }

        // Mark as visited by setting to '0'
        grid[i][j] = '0';

        // Explore 4 directions
        DFS(grid, i + 1, j); // Down
        DFS(grid, i - 1, j); // Up
        DFS(grid, i, j + 1); // Right
        DFS(grid, i, j - 1); // Left
    }
}
```

**Time Complexity:** O(m × n) - Visit each cell once  
**Space Complexity:** O(m × n) - Worst case recursion depth

**Explanation:**

- Scan grid for unvisited land ('1')
- When found, increment count and mark entire island
- DFS marks all connected land cells
- Modifies input to mark visited (can use separate visited array)

### Solution 2: BFS (Alternative)

```csharp
public class Solution
{
    public int NumIslands(char[][] grid)
    {
        if (grid == null || grid.Length == 0) return 0;

        int rows = grid.Length;
        int cols = grid[0].Length;
        int count = 0;

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (grid[i][j] == '1')
                {
                    count++;
                    BFS(grid, i, j);
                }
            }
        }

        return count;
    }

    private void BFS(char[][] grid, int startRow, int startCol)
    {
        int[] dx = { 0, 0, 1, -1 };
        int[] dy = { 1, -1, 0, 0 };

        var queue = new Queue<(int, int)>();
        queue.Enqueue((startRow, startCol));
        grid[startRow][startCol] = '0';

        while (queue.Count > 0)
        {
            var (row, col) = queue.Dequeue();

            for (int k = 0; k < 4; k++)
            {
                int newRow = row + dx[k];
                int newCol = col + dy[k];

                if (newRow >= 0 && newRow < grid.Length &&
                    newCol >= 0 && newCol < grid[0].Length &&
                    grid[newRow][newCol] == '1')
                {
                    queue.Enqueue((newRow, newCol));
                    grid[newRow][newCol] = '0';
                }
            }
        }
    }
}
```

**Time Complexity:** O(m × n)  
**Space Complexity:** O(min(m, n)) - Queue size

---

## Problem 2: Clone Graph (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

**Example:**

```
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]

Node 1 connects to 2,4
Node 2 connects to 1,3
Node 3 connects to 2,4
Node 4 connects to 1,3
```

```csharp
// Node definition
public class Node
{
    public int val;
    public IList<Node> neighbors;

    public Node() {
        val = 0;
        neighbors = new List<Node>();
    }

    public Node(int _val) {
        val = _val;
        neighbors = new List<Node>();
    }

    public Node(int _val, List<Node> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
}
```

### Solution: DFS with HashMap

```csharp
public class Solution
{
    private Dictionary<Node, Node> visited = new Dictionary<Node, Node>();

    public Node CloneGraph(Node node)
    {
        if (node == null) return null;

        // If already cloned, return clone
        if (visited.ContainsKey(node))
        {
            return visited[node];
        }

        // Create clone of current node
        Node cloneNode = new Node(node.val);
        visited[node] = cloneNode;

        // Recursively clone neighbors
        foreach (Node neighbor in node.neighbors)
        {
            cloneNode.neighbors.Add(CloneGraph(neighbor));
        }

        return cloneNode;
    }
}
```

**Time Complexity:** O(V + E) - V vertices, E edges  
**Space Complexity:** O(V) - Visited map and recursion

**Explanation:**

- Use HashMap to track original → clone mapping
- Prevents infinite loops and duplicate cloning
- DFS to traverse and clone recursively
- Add cloned neighbors to clone node

---

## Problem 3: Course Schedule (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

There are `numCourses` courses labeled 0 to numCourses-1. Given `prerequisites[i] = [a, b]` meaning course `a` requires course `b` first, return if all courses can be finished (no circular dependencies).

**Example:**

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: Take course 0, then course 1

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: Circular dependency
```

### Solution 1: DFS Cycle Detection (Optimal)

```csharp
public class Solution
{
    public bool CanFinish(int numCourses, int[][] prerequisites)
    {
        // Build adjacency list
        var graph = new Dictionary<int, List<int>>();
        for (int i = 0; i < numCourses; i++)
        {
            graph[i] = new List<int>();
        }

        foreach (var prereq in prerequisites)
        {
            graph[prereq[0]].Add(prereq[1]);
        }

        // 0 = unvisited, 1 = visiting, 2 = visited
        int[] visited = new int[numCourses];

        for (int i = 0; i < numCourses; i++)
        {
            if (HasCycle(graph, i, visited))
            {
                return false;
            }
        }

        return true;
    }

    private bool HasCycle(Dictionary<int, List<int>> graph, int course, int[] visited)
    {
        if (visited[course] == 1) return true;  // Cycle detected!
        if (visited[course] == 2) return false; // Already checked

        visited[course] = 1; // Mark as visiting

        foreach (int prereq in graph[course])
        {
            if (HasCycle(graph, prereq, visited))
            {
                return true;
            }
        }

        visited[course] = 2; // Mark as visited
        return false;
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

**Explanation:**

- Detect cycle in directed graph
- Three states: unvisited, visiting, visited
- If we encounter "visiting" node, cycle detected
- Use DFS to check all courses
- This is topological sort check

### Solution 2: BFS (Kahn's Algorithm)

```csharp
public class Solution
{
    public bool CanFinish(int numCourses, int[][] prerequisites)
    {
        var graph = new Dictionary<int, List<int>>();
        int[] indegree = new int[numCourses];

        // Build graph and calculate indegrees
        for (int i = 0; i < numCourses; i++)
        {
            graph[i] = new List<int>();
        }

        foreach (var prereq in prerequisites)
        {
            graph[prereq[1]].Add(prereq[0]);
            indegree[prereq[0]]++;
        }

        // Start with courses having no prerequisites
        var queue = new Queue<int>();
        for (int i = 0; i < numCourses; i++)
        {
            if (indegree[i] == 0)
            {
                queue.Enqueue(i);
            }
        }

        int completed = 0;

        while (queue.Count > 0)
        {
            int course = queue.Dequeue();
            completed++;

            foreach (int next in graph[course])
            {
                indegree[next]--;
                if (indegree[next] == 0)
                {
                    queue.Enqueue(next);
                }
            }
        }

        return completed == numCourses;
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

**Explanation:**

- Kahn's algorithm for topological sort
- Track indegree (number of prerequisites)
- Start with courses having no prerequisites
- Remove edges as we "complete" courses
- If can't complete all, cycle exists

---

## Key Takeaways for Day 9

### Graph Traversal

**DFS (Stack/Recursion):**

```csharp
void DFS(int node, HashSet<int> visited, Dictionary<int, List<int>> graph)
{
    visited.Add(node);
    foreach (int neighbor in graph[node])
    {
        if (!visited.Contains(neighbor))
            DFS(neighbor, visited, graph);
    }
}
```

**Use:** Cycle detection, path finding, topology

**BFS (Queue):**

```csharp
void BFS(int start, Dictionary<int, List<int>> graph)
{
    var visited = new HashSet<int>();
    var queue = new Queue<int>();
    queue.Enqueue(start);
    visited.Add(start);

    while (queue.Count > 0)
    {
        int node = queue.Dequeue();
        foreach (int neighbor in graph[node])
        {
            if (!visited.Contains(neighbor))
            {
                visited.Add(neighbor);
                queue.Enqueue(neighbor);
            }
        }
    }
}
```

**Use:** Shortest path (unweighted), level-by-level

### Graph Algorithms

| Algorithm        | Use Case                   | Time       | Space |
| ---------------- | -------------------------- | ---------- | ----- |
| DFS              | Cycle detection, paths     | O(V+E)     | O(V)  |
| BFS              | Shortest path (unweighted) | O(V+E)     | O(V)  |
| Dijkstra         | Shortest path (weighted)   | O(E log V) | O(V)  |
| Union-Find       | Connected components       | O(α(V))    | O(V)  |
| Topological Sort | Dependency order           | O(V+E)     | O(V)  |

### Common Graph Patterns

1. **Connected Components:** DFS/BFS from each unvisited node
2. **Cycle Detection:** DFS with three states or BFS with indegree
3. **Shortest Path:** BFS for unweighted, Dijkstra for weighted
4. **Topological Sort:** DFS postorder or Kahn's algorithm

**Tomorrow:** Day 10 - Dynamic Programming Basics
