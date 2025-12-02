# Day 7: Topological Sort & Graph Ordering 🎯

## Overview

**Topological sorting** is essential for dependency resolution problems and appears in approximately **10-15%** of big tech interviews. These problems test:

- Directed Acyclic Graph (DAG) understanding
- DFS postorder traversal
- Kahn's algorithm (BFS approach)
- Cycle detection in directed graphs

**Key Insight:** Topological sort orders vertices such that for every directed edge u→v, u comes before v in the ordering. Only possible for DAGs (no cycles).

---

## Topological Sort Algorithms

### Method 1: DFS Postorder

```csharp
public class TopologicalSort
{
    public List<int> SortDFS(int n, List<(int from, int to)> edges)
    {
        // Build adjacency list
        var graph = new List<int>[n];
        for (int i = 0; i < n; i++)
            graph[i] = new List<int>();

        foreach (var (from, to) in edges)
        {
            graph[from].Add(to);
        }

        var visited = new bool[n];
        var result = new Stack<int>();

        for (int i = 0; i < n; i++)
        {
            if (!visited[i])
            {
                DFS(i, graph, visited, result);
            }
        }

        return result.ToList();  // Reverse postorder
    }

    private void DFS(int node, List<int>[] graph, bool[] visited, Stack<int> result)
    {
        visited[node] = true;

        foreach (int neighbor in graph[node])
        {
            if (!visited[neighbor])
            {
                DFS(neighbor, graph, visited, result);
            }
        }

        result.Push(node);  // Add after visiting all descendants
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

---

### Method 2: Kahn's Algorithm (BFS)

```csharp
public class TopologicalSort
{
    public List<int> SortBFS(int n, List<(int from, int to)> edges)
    {
        var graph = new List<int>[n];
        var inDegree = new int[n];

        for (int i = 0; i < n; i++)
            graph[i] = new List<int>();

        // Build graph and count in-degrees
        foreach (var (from, to) in edges)
        {
            graph[from].Add(to);
            inDegree[to]++;
        }

        // Queue all nodes with 0 in-degree
        var queue = new Queue<int>();
        for (int i = 0; i < n; i++)
        {
            if (inDegree[i] == 0)
            {
                queue.Enqueue(i);
            }
        }

        var result = new List<int>();

        while (queue.Count > 0)
        {
            int node = queue.Dequeue();
            result.Add(node);

            // Reduce in-degree of neighbors
            foreach (int neighbor in graph[node])
            {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0)
                {
                    queue.Enqueue(neighbor);
                }
            }
        }

        // If result.Count < n, there's a cycle
        return result.Count == n ? result : new List<int>();
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

---

## Problem 1: Course Schedule ⭐⭐ (Medium)

### Problem Statement

There are a total of `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` first before course `ai`.

Return `true` if you can finish all courses, otherwise return `false`.

### Example

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: Take course 0, then course 1

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: Circular dependency
```

---

### Solution 1: DFS with Cycle Detection (Optimal)

```csharp
public class Solution
{
    public bool CanFinish(int numCourses, int[][] prerequisites)
    {
        // Build adjacency list
        var graph = new List<int>[numCourses];
        for (int i = 0; i < numCourses; i++)
            graph[i] = new List<int>();

        foreach (var prereq in prerequisites)
        {
            graph[prereq[1]].Add(prereq[0]);  // prereq[1] -> prereq[0]
        }

        // 0 = unvisited, 1 = visiting, 2 = visited
        int[] state = new int[numCourses];

        for (int i = 0; i < numCourses; i++)
        {
            if (HasCycle(i, graph, state))
            {
                return false;
            }
        }

        return true;
    }

    private bool HasCycle(int course, List<int>[] graph, int[] state)
    {
        if (state[course] == 1)  // Currently visiting - cycle detected
            return true;

        if (state[course] == 2)  // Already visited
            return false;

        state[course] = 1;  // Mark as visiting

        foreach (int nextCourse in graph[course])
        {
            if (HasCycle(nextCourse, graph, state))
            {
                return true;
            }
        }

        state[course] = 2;  // Mark as visited
        return false;
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

**Explanation:**

1. **Three states:** Unvisited (0), Visiting (1), Visited (2)
2. **Cycle detection:** If we reach a node currently being visited → cycle
3. DFS from each unvisited node
4. If any path has cycle, return false

---

### Solution 2: Kahn's Algorithm (BFS)

```csharp
public class Solution
{
    public bool CanFinish(int numCourses, int[][] prerequisites)
    {
        var graph = new List<int>[numCourses];
        var inDegree = new int[numCourses];

        for (int i = 0; i < numCourses; i++)
            graph[i] = new List<int>();

        foreach (var prereq in prerequisites)
        {
            graph[prereq[1]].Add(prereq[0]);
            inDegree[prereq[0]]++;
        }

        var queue = new Queue<int>();
        for (int i = 0; i < numCourses; i++)
        {
            if (inDegree[i] == 0)
            {
                queue.Enqueue(i);
            }
        }

        int completed = 0;

        while (queue.Count > 0)
        {
            int course = queue.Dequeue();
            completed++;

            foreach (int nextCourse in graph[course])
            {
                inDegree[nextCourse]--;
                if (inDegree[nextCourse] == 0)
                {
                    queue.Enqueue(nextCourse);
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

1. Count in-degree (number of prerequisites) for each course
2. Start with courses having 0 prerequisites
3. Process each course, reducing in-degree of dependent courses
4. If we can process all courses, no cycle exists

---

## Problem 2: Course Schedule II ⭐⭐ (Medium)

### Problem Statement

Same as Course Schedule, but return the ordering of courses you should take to finish all courses. If impossible, return empty array.

### Example

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3] or [0,1,2,3]
Explanation: Multiple valid orderings exist

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: []
Explanation: Impossible due to cycle
```

---

### Solution: Kahn's Algorithm (Returns Order)

```csharp
public class Solution
{
    public int[] FindOrder(int numCourses, int[][] prerequisites)
    {
        var graph = new List<int>[numCourses];
        var inDegree = new int[numCourses];

        for (int i = 0; i < numCourses; i++)
            graph[i] = new List<int>();

        foreach (var prereq in prerequisites)
        {
            graph[prereq[1]].Add(prereq[0]);
            inDegree[prereq[0]]++;
        }

        var queue = new Queue<int>();
        for (int i = 0; i < numCourses; i++)
        {
            if (inDegree[i] == 0)
            {
                queue.Enqueue(i);
            }
        }

        var order = new List<int>();

        while (queue.Count > 0)
        {
            int course = queue.Dequeue();
            order.Add(course);

            foreach (int nextCourse in graph[course])
            {
                inDegree[nextCourse]--;
                if (inDegree[nextCourse] == 0)
                {
                    queue.Enqueue(nextCourse);
                }
            }
        }

        return order.Count == numCourses ? order.ToArray() : new int[0];
    }
}
```

**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

**Explanation:**

- Same as Course Schedule, but collect the order
- BFS naturally gives valid topological ordering
- Empty result indicates cycle

---

## Problem 3: Alien Dictionary ⭐⭐⭐ (Hard)

### Problem Statement

There is a new alien language that uses the English alphabet. However, the order among letters is different. You receive a list of **non-empty** words from the dictionary in sorted order.

Derive the order of letters in this alien language.

### Example

```
Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"

Input: words = ["z","x"]
Output: "zx"

Input: words = ["z","x","z"]
Output: ""
Explanation: Invalid (z before x, but also x before z)
```

---

### Solution: Build Graph + Topological Sort

```csharp
public class Solution
{
    public string AlienOrder(string[] words)
    {
        // Build graph
        var graph = new Dictionary<char, HashSet<char>>();
        var inDegree = new Dictionary<char, int>();

        // Initialize all characters
        foreach (string word in words)
        {
            foreach (char c in word)
            {
                if (!graph.ContainsKey(c))
                {
                    graph[c] = new HashSet<char>();
                    inDegree[c] = 0;
                }
            }
        }

        // Build edges from adjacent words
        for (int i = 0; i < words.Length - 1; i++)
        {
            string word1 = words[i];
            string word2 = words[i + 1];

            // Check for invalid case: prefix word comes after full word
            if (word1.Length > word2.Length && word1.StartsWith(word2))
            {
                return "";
            }

            // Find first different character
            int minLen = Math.Min(word1.Length, word2.Length);
            for (int j = 0; j < minLen; j++)
            {
                if (word1[j] != word2[j])
                {
                    // word1[j] comes before word2[j]
                    if (!graph[word1[j]].Contains(word2[j]))
                    {
                        graph[word1[j]].Add(word2[j]);
                        inDegree[word2[j]]++;
                    }
                    break;  // Only first difference matters
                }
            }
        }

        // Kahn's algorithm
        var queue = new Queue<char>();
        foreach (var c in inDegree.Keys)
        {
            if (inDegree[c] == 0)
            {
                queue.Enqueue(c);
            }
        }

        var result = new StringBuilder();

        while (queue.Count > 0)
        {
            char c = queue.Dequeue();
            result.Append(c);

            foreach (char next in graph[c])
            {
                inDegree[next]--;
                if (inDegree[next] == 0)
                {
                    queue.Enqueue(next);
                }
            }
        }

        // Check if all characters processed (no cycle)
        return result.Length == inDegree.Count ? result.ToString() : "";
    }
}
```

**Time Complexity:** O(C) where C is total characters in all words  
**Space Complexity:** O(1) since at most 26 letters

**Explanation:**

1. **Build graph:** Compare adjacent words to find character order
2. **Edge case:** "abc" before "ab" is invalid
3. **Only first difference matters:** Once characters differ, that determines order
4. **Topological sort:** Find valid character ordering
5. **Cycle detection:** If can't process all characters, cycle exists

---

## Key Takeaways

### 1. Topological Sort Patterns

| Problem Type             | Approach                     | Key Point                    |
| ------------------------ | ---------------------------- | ---------------------------- |
| **Can finish all tasks** | Cycle detection              | DFS with 3 states or Kahn's  |
| **Find task order**      | Kahn's algorithm             | BFS naturally gives ordering |
| **Character ordering**   | Build graph from comparisons | Only first diff matters      |
| **Minimum time**         | Topological sort + DP        | Process in dependency order  |

### 2. Two Algorithms Comparison

| Aspect              | DFS (Postorder)           | Kahn's (BFS)               |
| ------------------- | ------------------------- | -------------------------- |
| **Implementation**  | Recursive                 | Iterative with queue       |
| **Order**           | Reverse postorder         | Direct from BFS            |
| **Cycle detection** | 3 states                  | Check final count          |
| **Intuition**       | Finish dependencies first | Process nodes with no deps |

### 3. Common Templates

```csharp
// DFS with cycle detection
int[] state = new int[n];  // 0=unvisited, 1=visiting, 2=visited
bool HasCycle(int node)
{
    if (state[node] == 1) return true;  // Cycle!
    if (state[node] == 2) return false;

    state[node] = 1;
    foreach (int next in graph[node])
        if (HasCycle(next)) return true;

    state[node] = 2;
    return false;
}

// Kahn's algorithm template
int[] inDegree = new int[n];
// ... build inDegree ...

var queue = new Queue<int>();
for (int i = 0; i < n; i++)
    if (inDegree[i] == 0)
        queue.Enqueue(i);

var result = new List<int>();
while (queue.Count > 0)
{
    int node = queue.Dequeue();
    result.Add(node);

    foreach (int next in graph[node])
    {
        inDegree[next]--;
        if (inDegree[next] == 0)
            queue.Enqueue(next);
    }
}

// If result.Count < n, there's a cycle
```

### 4. Interview Tips

✅ **Ask about cycles:** Can there be circular dependencies?  
✅ **Multiple valid orders:** Is any valid order acceptable?  
✅ **Directed vs undirected:** Topological sort only for directed graphs  
✅ **DAG requirement:** Must be acyclic for topological sort to exist  
✅ **Edge direction:** Clarify which way prerequisites point

---

## Practice Problems

### Medium

1. **Course Schedule** ✓ (Covered above)
2. **Course Schedule II** ✓ (Covered above)
3. **Minimum Height Trees** - Find graph center
4. **Parallel Courses** - Task scheduling with time
5. **Sort Items by Groups** - Two-level topological sort

### Hard

6. **Alien Dictionary** ✓ (Covered above)
7. **Sequence Reconstruction** - Unique topological order
8. **Course Schedule IV** - Reachability queries

---

## Common Mistakes to Avoid

❌ **Wrong edge direction** - Prerequisites point backwards (prerequisite → course)  
❌ **Forgetting cycle check** - Must verify all nodes processed  
❌ **Not handling empty graph** - All nodes isolated is valid  
❌ **Comparing full words** - Only first character difference matters (Alien Dictionary)  
❌ **Invalid prefix case** - "abc" before "ab" is impossible

---

## Time Complexity Summary

| Algorithm         | Time   | Space | Best For         |
| ----------------- | ------ | ----- | ---------------- |
| **DFS Postorder** | O(V+E) | O(V)  | Detecting cycles |
| **Kahn's (BFS)**  | O(V+E) | O(V)  | Getting ordering |

Both algorithms have same complexity, choose based on:

- **DFS:** More intuitive for recursion, easier cycle detection
- **BFS:** More intuitive ordering, easier to understand iteratively

---

## Cycle Detection Methods

```csharp
// Method 1: Three states (DFS)
// 0 = white (unvisited)
// 1 = gray (visiting - on current path)
// 2 = black (visited - done)
// Cycle if we reach gray node

// Method 2: Kahn's algorithm
// If processed nodes < total nodes → cycle exists

// Method 3: Union-Find (undirected graphs only)
// If union fails → cycle exists
```

---

## Next Steps

- ✅ Master both DFS and Kahn's approaches
- 📚 Practice dependency resolution problems
- 🎯 Study critical path in project scheduling
- 💡 Learn about lexicographically smallest topological sort

**Remember:** Topological sort is about ordering tasks respecting dependencies. Use DFS for cycle detection, Kahn's for natural ordering!
