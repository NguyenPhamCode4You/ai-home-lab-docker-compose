# Day 6: Union-Find & Disjoint Sets 🎯

## Overview

**Union-Find (Disjoint Set Union - DSU)** is a specialized data structure appearing in approximately **10-15%** of big tech interviews, especially for graph connectivity problems. It tests:

- Understanding of disjoint sets
- Path compression optimization
- Union by rank/size
- Connected components analysis

**Key Insight:** Union-Find excels at dynamically tracking connected components with nearly O(1) union and find operations after optimization.

---

## Union-Find Data Structure Basics

### Core Operations

```csharp
public class UnionFind
{
    private int[] parent;
    private int[] rank;  // or size
    private int count;   // number of disjoint sets

    public UnionFind(int n)
    {
        parent = new int[n];
        rank = new int[n];
        count = n;

        // Initially, each element is its own parent
        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    // Find with path compression
    public int Find(int x)
    {
        if (parent[x] != x)
        {
            parent[x] = Find(parent[x]);  // Path compression
        }
        return parent[x];
    }

    // Union by rank
    public bool Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);

        if (rootX == rootY)
            return false;  // Already connected

        // Attach smaller tree under larger tree
        if (rank[rootX] < rank[rootY])
        {
            parent[rootX] = rootY;
        }
        else if (rank[rootX] > rank[rootY])
        {
            parent[rootY] = rootX;
        }
        else
        {
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        count--;
        return true;
    }

    public bool IsConnected(int x, int y)
    {
        return Find(x) == Find(y);
    }

    public int GetCount()
    {
        return count;
    }
}
```

**Time Complexity:** O(α(n)) ≈ O(1) per operation (with both optimizations)  
**Space Complexity:** O(n)

**Optimizations:**

1. **Path Compression:** Make every node point directly to root
2. **Union by Rank:** Attach smaller tree under larger tree

---

## Problem 1: Number of Connected Components ⭐⭐ (Medium)

### Problem Statement

You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [ai, bi]` indicates there is an edge between `ai` and `bi`.

Return the number of connected components in the graph.

### Example

```
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
Explanation: 0-1-2 is one component, 3-4 is another, total 2

Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1
Explanation: All connected in one component
```

---

### Solution 1: Union-Find (Optimal)

```csharp
public class Solution
{
    public int CountComponents(int n, int[][] edges)
    {
        var uf = new UnionFind(n);

        foreach (var edge in edges)
        {
            uf.Union(edge[0], edge[1]);
        }

        return uf.GetCount();
    }
}

public class UnionFind
{
    private int[] parent;
    private int[] rank;
    private int count;

    public UnionFind(int n)
    {
        parent = new int[n];
        rank = new int[n];
        count = n;

        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    public int Find(int x)
    {
        if (parent[x] != x)
        {
            parent[x] = Find(parent[x]);
        }
        return parent[x];
    }

    public void Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);

        if (rootX == rootY) return;

        if (rank[rootX] < rank[rootY])
        {
            parent[rootX] = rootY;
        }
        else if (rank[rootX] > rank[rootY])
        {
            parent[rootY] = rootX;
        }
        else
        {
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        count--;
    }

    public int GetCount()
    {
        return count;
    }
}
```

**Time Complexity:** O(E × α(n)) ≈ O(E) where E is number of edges  
**Space Complexity:** O(n)

**Explanation:**

1. Start with n components (each node is separate)
2. For each edge, union the two nodes
3. Union decrements count if nodes weren't connected
4. Final count is number of components

---

### Solution 2: DFS (Alternative)

```csharp
public class Solution
{
    public int CountComponents(int n, int[][] edges)
    {
        // Build adjacency list
        var graph = new List<int>[n];
        for (int i = 0; i < n; i++)
            graph[i] = new List<int>();

        foreach (var edge in edges)
        {
            graph[edge[0]].Add(edge[1]);
            graph[edge[1]].Add(edge[0]);
        }

        bool[] visited = new bool[n];
        int count = 0;

        for (int i = 0; i < n; i++)
        {
            if (!visited[i])
            {
                DFS(i, graph, visited);
                count++;
            }
        }

        return count;
    }

    private void DFS(int node, List<int>[] graph, bool[] visited)
    {
        visited[node] = true;

        foreach (int neighbor in graph[node])
        {
            if (!visited[neighbor])
            {
                DFS(neighbor, graph, visited);
            }
        }
    }
}
```

**Time Complexity:** O(n + E) - Visit each node and edge once  
**Space Complexity:** O(n + E) - Graph storage + recursion stack

---

## Problem 2: Redundant Connection ⭐⭐ (Medium)

### Problem Statement

Given a graph with `n` nodes where `n` edges are added one by one. Initially, the graph is a tree (connected, acyclic). One edge is added that creates a cycle.

Return the edge that can be removed so the result is a tree. If multiple answers exist, return the one that occurs last in the input.

### Example

```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
Explanation: Removing [2,3] gives tree: 1-2, 1-3

Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
Explanation: [1,4] is the last edge that creates a cycle
```

---

### Solution: Union-Find (Optimal)

```csharp
public class Solution
{
    public int[] FindRedundantConnection(int[][] edges)
    {
        int n = edges.Length;
        var uf = new UnionFind(n + 1);  // Nodes are 1-indexed

        foreach (var edge in edges)
        {
            int u = edge[0], v = edge[1];

            // If already connected, this edge creates a cycle
            if (!uf.Union(u, v))
            {
                return edge;
            }
        }

        return new int[0];  // Should never reach here
    }
}

public class UnionFind
{
    private int[] parent;
    private int[] rank;

    public UnionFind(int n)
    {
        parent = new int[n];
        rank = new int[n];

        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    public int Find(int x)
    {
        if (parent[x] != x)
        {
            parent[x] = Find(parent[x]);
        }
        return parent[x];
    }

    public bool Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);

        if (rootX == rootY)
            return false;  // Already connected - would create cycle

        if (rank[rootX] < rank[rootY])
        {
            parent[rootX] = rootY;
        }
        else if (rank[rootX] > rank[rootY])
        {
            parent[rootY] = rootX;
        }
        else
        {
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        return true;
    }
}
```

**Time Complexity:** O(n × α(n)) ≈ O(n)  
**Space Complexity:** O(n)

**Explanation:**

1. Process edges in order
2. Try to union each edge's two nodes
3. If union fails (already connected), this edge creates cycle
4. Return first such edge
5. **Key insight:** Union-Find detects cycles efficiently

---

## Problem 3: Accounts Merge ⭐⭐⭐ (Medium)

### Problem Statement

Given a list of `accounts` where each element `accounts[i]` is a list of strings, where the first element is a name and the rest are emails.

Two accounts belong to the same person if they share at least one common email. Merge accounts that belong to the same person.

Return the merged accounts in any order.

### Example

```
Input: accounts = [
  ["John","john@mail.com","john_work@mail.com"],
  ["John","johnsmith@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","john@mail.com","john_home@mail.com"]
]

Output: [
  ["John","john@mail.com","john_home@mail.com","john_work@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnsmith@mail.com"]
]
```

---

### Solution: Union-Find with Email Mapping

```csharp
public class Solution
{
    public IList<IList<string>> AccountsMerge(IList<IList<string>> accounts)
    {
        var uf = new UnionFind(accounts.Count);
        var emailToIndex = new Dictionary<string, int>();

        // Step 1: Map emails to account indices and union accounts with common emails
        for (int i = 0; i < accounts.Count; i++)
        {
            for (int j = 1; j < accounts[i].Count; j++)
            {
                string email = accounts[i][j];

                if (emailToIndex.ContainsKey(email))
                {
                    // This email seen before, union accounts
                    uf.Union(i, emailToIndex[email]);
                }
                else
                {
                    emailToIndex[email] = i;
                }
            }
        }

        // Step 2: Group emails by root account
        var rootToEmails = new Dictionary<int, HashSet<string>>();

        foreach (var (email, index) in emailToIndex)
        {
            int root = uf.Find(index);

            if (!rootToEmails.ContainsKey(root))
            {
                rootToEmails[root] = new HashSet<string>();
            }

            rootToEmails[root].Add(email);
        }

        // Step 3: Build result
        var result = new List<IList<string>>();

        foreach (var (root, emails) in rootToEmails)
        {
            var account = new List<string> { accounts[root][0] };  // Name
            account.AddRange(emails.OrderBy(e => e));  // Sorted emails
            result.Add(account);
        }

        return result;
    }
}

public class UnionFind
{
    private int[] parent;
    private int[] rank;

    public UnionFind(int n)
    {
        parent = new int[n];
        rank = new int[n];

        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    public int Find(int x)
    {
        if (parent[x] != x)
        {
            parent[x] = Find(parent[x]);
        }
        return parent[x];
    }

    public void Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);

        if (rootX == rootY) return;

        if (rank[rootX] < rank[rootY])
        {
            parent[rootX] = rootY;
        }
        else if (rank[rootX] > rank[rootY])
        {
            parent[rootY] = rootX;
        }
        else
        {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
    }
}
```

**Time Complexity:** O(n × k × α(n) + n × k log k) where k is max emails per account  
**Space Complexity:** O(n × k)

**Explanation:**

1. Map each email to first account index it appears in
2. When email seen again, union that account with previous one
3. Group emails by root account
4. Build result with sorted emails per account
5. **Key insight:** Use Union-Find to merge accounts with shared emails

---

## Key Takeaways

### 1. Union-Find Patterns

| Problem Type              | Union-Find Application          |
| ------------------------- | ------------------------------- |
| **Connected components**  | Union edges, count components   |
| **Cycle detection**       | Union fails → cycle exists      |
| **Account/group merging** | Union by shared attributes      |
| **Minimum spanning tree** | Kruskal's algorithm             |
| **Percolation**           | Union nodes, check connectivity |

### 2. Implementation Template

```csharp
public class UnionFind
{
    private int[] parent;
    private int[] rank;  // or size
    private int count;

    public UnionFind(int n)
    {
        parent = new int[n];
        rank = new int[n];
        count = n;
        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    public int Find(int x)
    {
        if (parent[x] != x)
            parent[x] = Find(parent[x]);  // Path compression
        return parent[x];
    }

    public bool Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);
        if (rootX == rootY) return false;

        // Union by rank
        if (rank[rootX] < rank[rootY])
            parent[rootX] = rootY;
        else if (rank[rootX] > rank[rootY])
            parent[rootY] = rootX;
        else
        {
            parent[rootY] = rootX;
            rank[rootX]++;
        }

        count--;
        return true;
    }
}
```

### 3. When to Use Union-Find

✅ **Dynamic connectivity queries** - Check if nodes connected as edges added  
✅ **Connected components** - Count or identify components  
✅ **Cycle detection** - In undirected graphs  
✅ **Grouping by equivalence** - Merge groups with common elements  
✅ **Nearly constant time** - Need O(1) amortized operations

### 4. Interview Tips

✅ **Mention optimizations:** Path compression + union by rank give O(α(n))  
✅ **Alpha function:** α(n) < 5 for all practical n (inverse Ackermann)  
✅ **Alternative to DFS/BFS:** Often simpler for connectivity problems  
✅ **Track component count:** Decrement in Union, initialize to n  
✅ **Index mapping:** Sometimes need to map values to indices

---

## Practice Problems

### Medium

1. **Number of Connected Components** ✓ (Covered above)
2. **Redundant Connection** ✓ (Covered above)
3. **Accounts Merge** ✓ (Covered above)
4. **Satisfiability of Equality Equations** - Union equal variables
5. **Most Stones Removed** - Union stones in same row/column
6. **Regions Cut by Slashes** - Union grid cells

### Hard

7. **Number of Islands II** - Dynamic island addition
8. **Smallest String With Swaps** - Group swappable indices
9. **Minimize Malware Spread** - Union-Find with size tracking

---

## Common Mistakes to Avoid

❌ **Forgetting path compression** - Leads to O(n) per operation  
❌ **Not using union by rank** - Tree becomes unbalanced  
❌ **Wrong initialization** - parent[i] should start as i  
❌ **Forgetting to find roots** - Must call Find() before comparing  
❌ **Off-by-one for 1-indexed** - Some problems use 1-indexed nodes

---

## Time Complexity Summary

| Operation       | Without Optimization | With Optimization |
| --------------- | -------------------- | ----------------- |
| **Find**        | O(n) worst           | O(α(n)) ≈ O(1)    |
| **Union**       | O(n) worst           | O(α(n)) ≈ O(1)    |
| **IsConnected** | O(n) worst           | O(α(n)) ≈ O(1)    |

**Note:** α(n) is inverse Ackermann function, grows extremely slowly (< 5 for n < 2^65536)

---

## Union-Find vs DFS/BFS

| Aspect               | Union-Find                    | DFS/BFS                |
| -------------------- | ----------------------------- | ---------------------- |
| **Best for**         | Dynamic connectivity          | Static graph traversal |
| **Time per query**   | O(α(n)) ≈ O(1)                | O(V + E)               |
| **Online algorithm** | Yes (handle edges one by one) | Usually offline        |
| **Cycle detection**  | O(1) per edge                 | O(V + E)               |
| **Shortest path**    | No                            | Yes (BFS)              |

---

## Next Steps

- ✅ Implement Union-Find from scratch
- 📚 Practice dynamic connectivity problems
- 🎯 Learn Kruskal's MST algorithm
- 💡 Study weighted Union-Find variants

**Remember:** Union-Find is the go-to structure for dynamic connectivity. With path compression and union by rank, operations are nearly O(1)!
