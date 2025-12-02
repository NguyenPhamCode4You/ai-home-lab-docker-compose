# Day 7: Binary Trees - Tree Fundamentals & Traversals

## Tree Node Definition

```csharp
public class TreeNode
{
    public int val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(int val = 0, TreeNode left = null, TreeNode right = null)
    {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

## Problem 1: Maximum Depth of Binary Tree (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given the root of a binary tree, return its maximum depth. Maximum depth is the number of nodes along the longest path from root to the farthest leaf.

**Example:**

```
    3
   / \
  9  20
    /  \
   15   7

Output: 3
```

### Solution 1: Recursive DFS (Simple & Optimal)

```csharp
public class Solution
{
    public int MaxDepth(TreeNode root)
    {
        // Base case: empty tree has depth 0
        if (root == null)
        {
            return 0;
        }

        // Recursively find depth of left and right subtrees
        int leftDepth = MaxDepth(root.left);
        int rightDepth = MaxDepth(root.right);

        // Current depth is 1 + maximum of subtree depths
        return 1 + Math.Max(leftDepth, rightDepth);
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(h) - Recursion stack, h = height (worst case O(n) for skewed tree)

**Explanation:**

- Classic recursive approach
- For each node, depth = 1 + max(left depth, right depth)
- Base case: null node has depth 0
- Very intuitive and commonly used in interviews

### Solution 2: Iterative BFS (Alternative)

```csharp
public class Solution
{
    public int MaxDepth(TreeNode root)
    {
        if (root == null) return 0;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        int depth = 0;

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            depth++;

            // Process all nodes at current level
            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }
        }

        return depth;
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(w) - Queue holds one level, w = max width

**Explanation:**

- Level-order traversal (BFS)
- Count number of levels
- More code but shows understanding of BFS
- Useful when need to process level by level

---

## Problem 2: Validate Binary Search Tree (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST is defined as:

- Left subtree contains only nodes with values less than node's value
- Right subtree contains only nodes with values greater than node's value
- Both left and right subtrees must also be BSTs

**Example:**

```
Valid BST:       Invalid BST:
    2                 5
   / \               / \
  1   3             1   4
                       / \
                      3   6
```

### Solution 1: Incorrect Approach (Common Mistake)

```csharp
// WRONG! Only checks immediate children
public class Solution
{
    public bool IsValidBST(TreeNode root)
    {
        if (root == null) return true;

        // This only validates immediate children!
        if (root.left != null && root.left.val >= root.val)
            return false;
        if (root.right != null && root.right.val <= root.val)
            return false;

        return IsValidBST(root.left) && IsValidBST(root.right);
    }
}
```

**Why it's wrong:**

```
     5
    / \
   1   6
      / \
     3   7

This would pass but is invalid!
3 is in right subtree of 5 but 3 < 5
```

### Solution 2: Range Validation (Optimal)

```csharp
public class Solution
{
    public bool IsValidBST(TreeNode root)
    {
        return IsValidBST(root, long.MinValue, long.MaxValue);
    }

    private bool IsValidBST(TreeNode node, long min, long max)
    {
        // Empty tree is valid
        if (node == null)
        {
            return true;
        }

        // Check if current node violates constraints
        if (node.val <= min || node.val >= max)
        {
            return false;
        }

        // Check left subtree: all values must be < node.val
        // Check right subtree: all values must be > node.val
        return IsValidBST(node.left, min, node.val) &&
               IsValidBST(node.right, node.val, max);
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(h) - Recursion stack

**Explanation:**

- Pass valid range (min, max) down the recursion
- Each node must be in valid range
- Left child: range (min, node.val)
- Right child: range (node.val, max)
- Use long for min/max to handle int.MinValue and int.MaxValue edge cases
- This correctly validates entire subtrees

### Solution 3: Inorder Traversal (Alternative)

```csharp
public class Solution
{
    private TreeNode prev = null;

    public bool IsValidBST(TreeNode root)
    {
        if (root == null)
        {
            return true;
        }

        // Check left subtree
        if (!IsValidBST(root.left))
        {
            return false;
        }

        // Check current node
        if (prev != null && prev.val >= root.val)
        {
            return false;
        }

        prev = root;

        // Check right subtree
        return IsValidBST(root.right);
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(h)

**Explanation:**

- Inorder traversal of BST produces sorted sequence
- Keep track of previous node
- Current should always be greater than previous
- Elegant solution using BST property

---

## Problem 3: Lowest Common Ancestor (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes. The LCA is the lowest node that has both nodes as descendants (a node can be a descendant of itself).

**Example:**

```
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4

LCA(5, 1) = 3
LCA(5, 4) = 5
LCA(6, 4) = 5
```

### Solution 1: Recursive (Optimal)

```csharp
public class Solution
{
    public TreeNode LowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q)
    {
        // Base case: reached null or found one of the nodes
        if (root == null || root == p || root == q)
        {
            return root;
        }

        // Search in left and right subtrees
        TreeNode left = LowestCommonAncestor(root.left, p, q);
        TreeNode right = LowestCommonAncestor(root.right, p, q);

        // If both left and right are non-null, current node is LCA
        if (left != null && right != null)
        {
            return root;
        }

        // Otherwise, return the non-null side
        return left != null ? left : right;
    }
}
```

**Time Complexity:** O(n) - May visit all nodes  
**Space Complexity:** O(h) - Recursion stack

**Explanation:**

- Post-order traversal: check children before processing current
- Three cases:
  1. Both nodes in different subtrees → current is LCA
  2. Both in left subtree → LCA is in left
  3. Both in right subtree → LCA is in right
- If we find p or q, return it immediately
- If both subtrees return non-null, current is LCA
- Elegant single-pass solution

**Step-by-step walkthrough:**

```
Tree:      3
          / \
         5   1
        / \
       6   2

Finding LCA(6, 2):

At node 3:
  Search left (5):
    At node 5:
      Search left (6): found 6, return 6
      Search right (2): found 2, return 2
      Both non-null! return 5 (LCA)
  left = 5, right = null
  Return 5

LCA(6, 2) = 5
```

### Solution 2: Store Path and Compare (Alternative)

```csharp
public class Solution
{
    public TreeNode LowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q)
    {
        var pathP = new List<TreeNode>();
        var pathQ = new List<TreeNode>();

        FindPath(root, p, pathP);
        FindPath(root, q, pathQ);

        TreeNode lca = null;
        int i = 0;

        // Find last common node in both paths
        while (i < pathP.Count && i < pathQ.Count && pathP[i] == pathQ[i])
        {
            lca = pathP[i];
            i++;
        }

        return lca;
    }

    private bool FindPath(TreeNode root, TreeNode target, List<TreeNode> path)
    {
        if (root == null)
        {
            return false;
        }

        path.Add(root);

        if (root == target)
        {
            return true;
        }

        if (FindPath(root.left, target, path) || FindPath(root.right, target, path))
        {
            return true;
        }

        path.RemoveAt(path.Count - 1); // Backtrack
        return false;
    }
}
```

**Time Complexity:** O(n) - Two passes  
**Space Complexity:** O(h) - Store paths

**Explanation:**

- Find path from root to each node
- Compare paths to find last common node
- More intuitive but uses extra space
- Two passes instead of one

---

## Key Takeaways for Day 7

### Tree Traversal Methods

#### 1. **Depth-First Search (DFS)**

**Preorder (Root → Left → Right):**

```csharp
void Preorder(TreeNode root)
{
    if (root == null) return;
    Process(root);           // Visit root first
    Preorder(root.left);
    Preorder(root.right);
}
```

**Use:** Copy tree, expression tree evaluation

**Inorder (Left → Root → Right):**

```csharp
void Inorder(TreeNode root)
{
    if (root == null) return;
    Inorder(root.left);
    Process(root);           // Visit root in middle
    Inorder(root.right);
}
```

**Use:** BST sorted traversal, validation

**Postorder (Left → Right → Root):**

```csharp
void Postorder(TreeNode root)
{
    if (root == null) return;
    Postorder(root.left);
    Postorder(root.right);
    Process(root);           // Visit root last
}
```

**Use:** Delete tree, post-fix expression

#### 2. **Breadth-First Search (BFS)**

**Level Order:**

```csharp
void LevelOrder(TreeNode root)
{
    if (root == null) return;
    var queue = new Queue<TreeNode>();
    queue.Enqueue(root);

    while (queue.Count > 0)
    {
        int levelSize = queue.Count;
        for (int i = 0; i < levelSize; i++)
        {
            TreeNode node = queue.Dequeue();
            Process(node);
            if (node.left != null) queue.Enqueue(node.left);
            if (node.right != null) queue.Enqueue(node.right);
        }
    }
}
```

**Use:** Level-by-level processing, shortest path in tree

### Tree Problem Patterns

| Pattern       | When to Use             | Example                      |
| ------------- | ----------------------- | ---------------------------- |
| Recursive DFS | Most tree problems      | Max depth, path sum          |
| Iterative DFS | Avoiding recursion      | Preorder with stack          |
| BFS           | Level-by-level, width   | Level order, right side view |
| Two Pointers  | Compare trees/subtrees  | Same tree, symmetric         |
| Bottom-up     | Need info from children | Diameter, balanced check     |

### Common Tree Properties

- **Full Binary Tree:** Every node has 0 or 2 children
- **Complete Binary Tree:** All levels filled except possibly last, filled left to right
- **Perfect Binary Tree:** All internal nodes have 2 children, all leaves at same level
- **Balanced Binary Tree:** Height of left and right subtrees differ by at most 1

### Complexity Cheat Sheet

| Operation          | Time | Space                |
| ------------------ | ---- | -------------------- |
| Traverse all nodes | O(n) | O(h) recursion       |
| Search in BST      | O(h) | O(h) recursion       |
| Insert in BST      | O(h) | O(h) recursion       |
| DFS (iterative)    | O(n) | O(h) stack           |
| BFS                | O(n) | O(w) queue (w=width) |

**h = height:**

- Best case: O(log n) for balanced tree
- Worst case: O(n) for skewed tree

### Interview Tips

1. **Always handle null:**

   ```csharp
   if (root == null) return ...;
   ```

2. **Draw the tree:**

   - Visualize recursion flow
   - Track what each call returns

3. **Common patterns:**

   - Divide and conquer: solve for left, right, combine
   - Pass information down: use parameters
   - Return information up: return values

4. **Edge cases:**

   - Empty tree (null)
   - Single node
   - Skewed tree (all left or all right)
   - Perfect binary tree

5. **BST vs Binary Tree:**
   - BST has ordering property
   - Can use inorder for sorted sequence
   - Can prune search space

---

## Additional Practice Problems

1. **Invert Binary Tree** (Easy) - Swap left and right
2. **Diameter of Binary Tree** (Easy) - Longest path
3. **Path Sum** (Easy) - Root to leaf path
4. **Binary Tree Level Order Traversal** (Medium) - BFS
5. **Serialize and Deserialize Binary Tree** (Hard) - Tree encoding

**Tomorrow:** Day 8 - BST & Advanced Tree Traversals
