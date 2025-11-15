# Day 8: BST & Advanced Tree Operations

## Problem 1: Kth Smallest Element in BST (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

Given the root of a binary search tree and an integer k, return the kth smallest element (1-indexed).

**Example:**

```
    3
   / \
  1   4
   \
    2

k = 1 → Output: 1
k = 2 → Output: 2
k = 3 → Output: 3
```

### Solution 1: Inorder Traversal with List (Simple)

```csharp
public class Solution
{
    public int KthSmallest(TreeNode root, int k)
    {
        var sorted = new List<int>();
        Inorder(root, sorted);
        return sorted[k - 1]; // k is 1-indexed
    }

    private void Inorder(TreeNode node, List<int> result)
    {
        if (node == null) return;

        Inorder(node.left, result);
        result.Add(node.val);
        Inorder(node.right, result);
    }
}
```

**Time Complexity:** O(n) - Visit all nodes  
**Space Complexity:** O(n) - Store all values

**Explanation:**

- Inorder traversal of BST gives sorted order
- Store all values then return kth
- Simple but uses O(n) space

### Solution 2: Inorder with Counter (Optimal)

```csharp
public class Solution
{
    private int count = 0;
    private int result = 0;

    public int KthSmallest(TreeNode root, int k)
    {
        count = 0;
        InorderSearch(root, k);
        return result;
    }

    private void InorderSearch(TreeNode node, int k)
    {
        if (node == null) return;

        InorderSearch(node.left, k);

        count++;
        if (count == k)
        {
            result = node.val;
            return; // Early termination
        }

        InorderSearch(node.right, k);
    }
}
```

**Time Complexity:** O(k) average, O(n) worst case  
**Space Complexity:** O(h) - Recursion stack only

**Explanation:**

- Count nodes during inorder traversal
- Stop when count reaches k
- More efficient when k is small
- Optimal for this problem

---

## Problem 2: Binary Tree Right Side View (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given a binary tree, return the values of nodes you can see when viewing the tree from the right side (top to bottom).

**Example:**

```
   1            <---
 /   \
2     3         <---
 \     \
  5     4       <---

Output: [1, 3, 4]
```

### Solution 1: BFS Level Order (Simple)

```csharp
public class Solution
{
    public IList<int> RightSideView(TreeNode root)
    {
        var result = new List<int>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;

            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();

                // Last node in level is rightmost
                if (i == levelSize - 1)
                {
                    result.Add(node.val);
                }

                if (node.left != null) queue.Enqueue(node.left);
                if (node.right != null) queue.Enqueue(node.right);
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(n) - Visit all nodes  
**Space Complexity:** O(w) - Queue width

**Explanation:**

- Level-order traversal
- Add last node of each level to result
- Straightforward BFS approach

### Solution 2: DFS (Optimal)

```csharp
public class Solution
{
    public IList<int> RightSideView(TreeNode root)
    {
        var result = new List<int>();
        DFS(root, 0, result);
        return result;
    }

    private void DFS(TreeNode node, int level, List<int> result)
    {
        if (node == null) return;

        // First time visiting this level, add to result
        if (level == result.Count)
        {
            result.Add(node.val);
        }

        // Visit right first (right side view)
        DFS(node.right, level + 1, result);
        DFS(node.left, level + 1, result);
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(h)

**Explanation:**

- DFS with depth tracking
- Visit right subtree before left
- First node at each level is rightmost visible
- More elegant with less space

---

## Problem 3: Construct Binary Tree from Preorder and Inorder (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given preorder and inorder traversal arrays, construct the binary tree.

**Example:**

```
preorder = [3,9,20,15,7]
inorder = [9,3,15,20,7]

    3
   / \
  9  20
    /  \
   15   7
```

### Solution: Recursive Construction (Optimal)

```csharp
public class Solution
{
    private Dictionary<int, int> inorderMap;
    private int preIndex;

    public TreeNode BuildTree(int[] preorder, int[] inorder)
    {
        // Build hash map for fast inorder index lookup
        inorderMap = new Dictionary<int, int>();
        for (int i = 0; i < inorder.Length; i++)
        {
            inorderMap[inorder[i]] = i;
        }

        preIndex = 0;
        return Build(preorder, 0, inorder.Length - 1);
    }

    private TreeNode Build(int[] preorder, int inStart, int inEnd)
    {
        if (inStart > inEnd) return null;

        // First element in preorder is root
        int rootVal = preorder[preIndex++];
        TreeNode root = new TreeNode(rootVal);

        // Find root position in inorder
        int inIndex = inorderMap[rootVal];

        // Elements left of root in inorder are left subtree
        root.left = Build(preorder, inStart, inIndex - 1);

        // Elements right of root in inorder are right subtree
        root.right = Build(preorder, inIndex + 1, inEnd);

        return root;
    }
}
```

**Time Complexity:** O(n) - Process each node once  
**Space Complexity:** O(n) - HashMap and recursion

**Explanation:**

- Preorder gives root node first
- Inorder tells us left vs right subtree
- Find root in inorder, split into left/right
- Recursively build subtrees
- HashMap makes root lookup O(1)

---

## Key Takeaways for Day 8

### BST Properties

- **Inorder traversal** produces sorted sequence
- **Search, Insert, Delete** in O(h) time
- Can find kth smallest by counting inorder nodes
- Range queries efficient with pruning

### Tree Construction Patterns

- **Preorder + Inorder** → Unique tree
- **Postorder + Inorder** → Unique tree
- **Preorder + Postorder** → Not unique (need inorder or structure info)

### Advanced Tree Techniques

1. **Morris Traversal** - O(1) space inorder traversal
2. **Threaded Trees** - Link null pointers to successors
3. **Segment Trees** - Range query optimization
4. **Fenwick Trees** - Efficient prefix sums

**Tomorrow:** Day 9 - Graphs (BFS & DFS)
