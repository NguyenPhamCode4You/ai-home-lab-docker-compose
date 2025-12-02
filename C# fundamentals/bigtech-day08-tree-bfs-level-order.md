# Day 8: Tree BFS & Level Order Traversal 🎯

## Overview

**Binary Tree Level Order Traversal** (BFS on trees) appears in approximately **15-20%** of big tech interviews. These problems test:

- BFS traversal patterns
- Queue usage
- Level-by-level processing
- Tree structure understanding

**Key Insight:** BFS on trees uses a queue to process nodes level by level. Track level boundaries to distinguish between levels or process entire levels at once.

---

## BFS Template for Trees

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

// Basic BFS Template
public void BFS(TreeNode root)
{
    if (root == null) return;

    var queue = new Queue<TreeNode>();
    queue.Enqueue(root);

    while (queue.Count > 0)
    {
        int levelSize = queue.Count;  // Nodes in current level

        for (int i = 0; i < levelSize; i++)
        {
            TreeNode node = queue.Dequeue();

            // Process node
            Console.WriteLine(node.val);

            // Add children for next level
            if (node.left != null)
                queue.Enqueue(node.left);
            if (node.right != null)
                queue.Enqueue(node.right);
        }
    }
}
```

---

## Problem 1: Binary Tree Level Order Traversal ⭐⭐ (Medium)

### Problem Statement

Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

### Example

```
Input: root = [3,9,20,null,null,15,7]
    3
   / \
  9  20
    /  \
   15   7

Output: [[3],[9,20],[15,7]]
```

---

### Solution 1: BFS with Level Tracking (Optimal)

```csharp
public class Solution
{
    public IList<IList<int>> LevelOrder(TreeNode root)
    {
        var result = new List<IList<int>>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            var currentLevel = new List<int>();

            // Process all nodes at current level
            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();
                currentLevel.Add(node.val);

                // Add children for next level
                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }

            result.Add(currentLevel);
        }

        return result;
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(w) where w is max width (for queue)

**Explanation:**

1. Use queue for BFS
2. **Key technique:** Process entire level at once using `levelSize`
3. Track current level nodes separately
4. Add children to queue for next level

---

### Solution 2: BFS with Null Marker (Alternative)

```csharp
public class Solution
{
    public IList<IList<int>> LevelOrder(TreeNode root)
    {
        var result = new List<IList<int>>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        queue.Enqueue(null);  // Level marker

        var currentLevel = new List<int>();

        while (queue.Count > 0)
        {
            TreeNode node = queue.Dequeue();

            if (node == null)
            {
                // End of level
                result.Add(currentLevel);
                currentLevel = new List<int>();

                // Add marker for next level if queue not empty
                if (queue.Count > 0)
                    queue.Enqueue(null);
            }
            else
            {
                currentLevel.Add(node.val);

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

- Use `null` as level separator
- When dequeue null, current level is complete

---

## Problem 2: Binary Tree Zigzag Level Order ⭐⭐⭐ (Medium)

### Problem Statement

Given the root of a binary tree, return the zigzag level order traversal (i.e., left to right, then right to left for the next level and alternate).

### Example

```
Input: root = [3,9,20,null,null,15,7]
    3
   / \
  9  20
    /  \
   15   7

Output: [[3],[20,9],[15,7]]
Explanation: Level 0: left-to-right, Level 1: right-to-left, Level 2: left-to-right
```

---

### Solution 1: BFS with Reverse (Simple)

```csharp
public class Solution
{
    public IList<IList<int>> ZigzagLevelOrder(TreeNode root)
    {
        var result = new List<IList<int>>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        bool leftToRight = true;

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            var currentLevel = new List<int>();

            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();
                currentLevel.Add(node.val);

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }

            // Reverse if right-to-left level
            if (!leftToRight)
            {
                currentLevel.Reverse();
            }

            result.Add(currentLevel);
            leftToRight = !leftToRight;
        }

        return result;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

- Standard BFS with level tracking
- Alternate direction flag
- Reverse every other level

---

### Solution 2: Deque with Direction (Optimal)

```csharp
public class Solution
{
    public IList<IList<int>> ZigzagLevelOrder(TreeNode root)
    {
        var result = new List<IList<int>>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        bool leftToRight = true;

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            var currentLevel = new LinkedList<int>();

            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();

                // Add to appropriate end based on direction
                if (leftToRight)
                {
                    currentLevel.AddLast(node.val);
                }
                else
                {
                    currentLevel.AddFirst(node.val);
                }

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }

            result.Add(new List<int>(currentLevel));
            leftToRight = !leftToRight;
        }

        return result;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

- Use LinkedList for O(1) AddFirst/AddLast
- Add to front or back based on direction
- No need for reverse operation

---

## Problem 3: Binary Tree Right Side View ⭐⭐ (Medium)

### Problem Statement

Given the root of a binary tree, imagine yourself standing on the **right side** of it. Return the values of the nodes you can see ordered from top to bottom.

### Example

```
Input: root = [1,2,3,null,5,null,4]
     1
   /   \
  2     3
   \     \
    5     4

Output: [1,3,4]
Explanation: View from right side
```

---

### Solution 1: BFS - Last Node Per Level (Optimal)

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

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

1. BFS level by level
2. **Key insight:** Last node at each level is visible from right
3. Track position in level

---

### Solution 2: DFS with Level Tracking (Alternative)

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

        // First time visiting this level
        if (level == result.Count)
        {
            result.Add(node.val);
        }

        // Visit right first (so it's added to result first)
        DFS(node.right, level + 1, result);
        DFS(node.left, level + 1, result);
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(h) - Recursion stack height

**Explanation:**

- DFS with right subtree first
- First node at each level is rightmost
- Clever alternative to BFS

---

## Problem 4: Average of Levels in Binary Tree ⭐ (Easy)

### Problem Statement

Given the root of a binary tree, return the average value of the nodes on each level as an array.

### Example

```
Input: root = [3,9,20,null,null,15,7]
    3
   / \
  9  20
    /  \
   15   7

Output: [3.0, 14.5, 11.0]
Explanation:
Level 0: 3 → avg = 3.0
Level 1: (9 + 20) / 2 → avg = 14.5
Level 2: (15 + 7) / 2 → avg = 11.0
```

---

### Solution: Standard BFS

```csharp
public class Solution
{
    public IList<double> AverageOfLevels(TreeNode root)
    {
        var result = new List<double>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            double sum = 0;

            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();
                sum += node.val;

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }

            result.Add(sum / levelSize);
        }

        return result;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

- Standard BFS template
- Accumulate sum per level
- Calculate average

---

## Problem 5: Maximum Level Sum ⭐⭐ (Medium)

### Problem Statement

Given the root of a binary tree, the level of its root is `1`, the level of its children is `2`, and so on.

Return the **smallest level** x such that the sum of all the values of nodes at level x is **maximal**.

### Example

```
Input: root = [1,7,0,7,-8,null,null]
      1
    /   \
   7     0
  / \
 7  -8

Output: 2
Explanation:
Level 1: sum = 1
Level 2: sum = 7 + 0 = 7
Level 3: sum = 7 + (-8) = -1
Maximum sum is 7 at level 2
```

---

### Solution: BFS with Sum Tracking

```csharp
public class Solution
{
    public int MaxLevelSum(TreeNode root)
    {
        if (root == null) return 0;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);

        int maxSum = int.MinValue;
        int maxLevel = 1;
        int currentLevel = 1;

        while (queue.Count > 0)
        {
            int levelSize = queue.Count;
            int levelSum = 0;

            for (int i = 0; i < levelSize; i++)
            {
                TreeNode node = queue.Dequeue();
                levelSum += node.val;

                if (node.left != null)
                    queue.Enqueue(node.left);
                if (node.right != null)
                    queue.Enqueue(node.right);
            }

            // Update max if current level sum is larger
            if (levelSum > maxSum)
            {
                maxSum = levelSum;
                maxLevel = currentLevel;
            }

            currentLevel++;
        }

        return maxLevel;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(w)

**Explanation:**

- Track current level number
- Calculate sum per level
- Update max sum and level when needed
- Return level with maximum sum

---

## Key Takeaways

### 1. BFS on Trees Pattern

```csharp
var queue = new Queue<TreeNode>();
queue.Enqueue(root);

while (queue.Count > 0)
{
    int levelSize = queue.Count;  // KEY: snapshot current level size

    for (int i = 0; i < levelSize; i++)
    {
        TreeNode node = queue.Dequeue();

        // Process node

        // Add children
        if (node.left != null) queue.Enqueue(node.left);
        if (node.right != null) queue.Enqueue(node.right);
    }

    // End of level - can do level-specific processing here
}
```

### 2. Common BFS Variations

| Problem Type          | Technique                         |
| --------------------- | --------------------------------- |
| **Level order**       | Standard BFS with level tracking  |
| **Zigzag**            | Alternate direction or LinkedList |
| **Right side view**   | Last node per level               |
| **Left side view**    | First node per level              |
| **Level average/sum** | Aggregate values per level        |
| **Min depth**         | Stop at first leaf                |

### 3. BFS vs DFS for Trees

| Aspect               | BFS           | DFS                  |
| -------------------- | ------------- | -------------------- |
| **Structure**        | Queue         | Recursion/Stack      |
| **Space**            | O(width)      | O(height)            |
| **Level processing** | Natural       | Need level parameter |
| **Right side view**  | Last in level | Visit right first    |
| **Min depth**        | Stops early   | Must visit all       |

### 4. Interview Tips

✅ **Level size trick:** Save `queue.Count` before loop  
✅ **Edge cases:** Empty tree, single node, complete tree  
✅ **Space complexity:** Width can be O(n) in complete tree  
✅ **Optimization:** Early termination (min depth, target sum)  
✅ **Variations:** Zigzag, vertical order, right/left views

---

## Practice Problems

### Easy

1. **Binary Tree Level Order** ✓ (Covered above)
2. **Average of Levels** ✓ (Covered above)
3. **Minimum Depth** - BFS stops at first leaf
4. **Maximum Depth** - Count levels

### Medium

5. **Zigzag Level Order** ✓ (Covered above)
6. **Binary Tree Right Side View** ✓ (Covered above)
7. **Maximum Level Sum** ✓ (Covered above)
8. **Level Order Traversal II** - Bottom-up
9. **Populating Next Right Pointers** - Level linking
10. **All Nodes Distance K** - BFS from target

### Hard

11. **Vertical Order Traversal** - Column-based BFS
12. **Binary Tree Maximum Path Sum** - DFS but good to know

---

## Common Mistakes to Avoid

❌ **Not saving level size** - Queue changes during iteration  
❌ **Checking null after enqueue** - Check before enqueue  
❌ **Wrong space complexity** - Width, not height, for BFS  
❌ **Forgetting empty tree** - Always check `root == null`  
❌ **Mixing BFS levels** - Use for loop with saved levelSize

---

## Time & Space Complexity

| Problem             | Time | Space | Notes                   |
| ------------------- | ---- | ----- | ----------------------- |
| **Level Order**     | O(n) | O(w)  | w = max width           |
| **Zigzag**          | O(n) | O(w)  | With or without reverse |
| **Right Side View** | O(n) | O(w)  | Last node per level     |
| **Level Sum**       | O(n) | O(w)  | Standard BFS            |

**Note:** For complete binary tree, width w = n/2 in worst case (last level)

---

## Next Steps

- ✅ Master the level size snapshot technique
- 📚 Practice vertical order traversal
- 🎯 Study N-ary tree BFS
- 💡 Learn bidirectional BFS for shortest path

**Remember:** The key to tree BFS is capturing `queue.Count` before the level loop. This lets you process entire levels as units!
