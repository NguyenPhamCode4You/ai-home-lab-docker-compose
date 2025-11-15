# Day 5: Linked Lists - Pointers & List Manipulation

## Linked List Node Definition

```csharp
public class ListNode
{
    public int val;
    public ListNode next;

    public ListNode(int val = 0, ListNode next = null)
    {
        this.val = val;
        this.next = next;
    }
}
```

## Problem 1: Reverse Linked List (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given the head of a singly linked list, reverse the list and return the reversed list.

**Example:**

```
Input: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
Output: 5 -> 4 -> 3 -> 2 -> 1 -> NULL
```

### Solution 1: Iterative (Optimal)

```csharp
public class Solution
{
    public ListNode ReverseList(ListNode head)
    {
        ListNode prev = null;
        ListNode current = head;

        while (current != null)
        {
            // Save next node
            ListNode nextTemp = current.next;

            // Reverse current node's pointer
            current.next = prev;

            // Move pointers forward
            prev = current;
            current = nextTemp;
        }

        return prev; // prev is the new head
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(1) - Only using pointers

**Explanation:**

- Use three pointers: prev, current, next
- For each node, reverse its next pointer to point backward
- Move all pointers forward
- When current reaches null, prev is the new head
- This is the standard iterative approach

**Step-by-step visualization:**

```
Initial: null <- prev  1 -> 2 -> 3 -> NULL
                      ^
                   current

Step 1:  null <- 1    2 -> 3 -> NULL
              prev   ^
                   current

Step 2:  null <- 1 <- 2    3 -> NULL
                   prev   ^
                        current

Step 3:  null <- 1 <- 2 <- 3    NULL
                        prev   ^
                             current

Result: prev points to 3 (new head)
```

### Solution 2: Recursive

```csharp
public class Solution
{
    public ListNode ReverseList(ListNode head)
    {
        // Base case: empty list or single node
        if (head == null || head.next == null)
        {
            return head;
        }

        // Recursively reverse the rest of the list
        ListNode newHead = ReverseList(head.next);

        // Reverse the link between current and next node
        head.next.next = head;
        head.next = null;

        return newHead;
    }
}
```

**Time Complexity:** O(n) - Visit each node once  
**Space Complexity:** O(n) - Recursion call stack

**Explanation:**

- Recursively reverse from the second node to end
- After recursion returns, reverse link between current and next
- The recursive call returns the new head
- Less intuitive but elegant

---

## Problem 2: Linked List Cycle (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

Given a linked list, determine if it has a cycle. Return true if there is a cycle, false otherwise.

**Example:**

```
Input: 3 -> 2 -> 0 -> -4 ─┐
           ^               │
           └───────────────┘
Output: true
```

### Solution 1: Hash Set (Simple)

```csharp
public class Solution
{
    public bool HasCycle(ListNode head)
    {
        var visited = new HashSet<ListNode>();
        ListNode current = head;

        while (current != null)
        {
            // If we've seen this node before, there's a cycle
            if (visited.Contains(current))
            {
                return true;
            }

            visited.Add(current);
            current = current.next;
        }

        return false; // Reached end, no cycle
    }
}
```

**Time Complexity:** O(n) - Visit each node at most once  
**Space Complexity:** O(n) - Store nodes in HashSet

**Explanation:**

- Track visited nodes in HashSet
- If we encounter a node we've seen, there's a cycle
- If we reach null, no cycle exists
- Simple but uses extra space

### Solution 2: Floyd's Cycle Detection (Optimal)

```csharp
public class Solution
{
    public bool HasCycle(ListNode head)
    {
        if (head == null || head.next == null)
        {
            return false;
        }

        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null)
        {
            slow = slow.next;           // Move 1 step
            fast = fast.next.next;      // Move 2 steps

            if (slow == fast)
            {
                return true; // Pointers met, cycle detected
            }
        }

        return false; // Fast reached end, no cycle
    }
}
```

**Time Complexity:** O(n) - Fast pointer traverses at most 2n steps  
**Space Complexity:** O(1) - Only using two pointers

**Explanation:**

- Use two pointers: slow (1 step) and fast (2 steps)
- If there's a cycle, fast will eventually catch up to slow
- Like runners on a circular track, faster one will lap slower one
- If fast reaches null, no cycle exists
- This is the optimal solution (constant space)

**Follow-up: Find where cycle begins**

```csharp
public class Solution
{
    public ListNode DetectCycle(ListNode head)
    {
        if (head == null || head.next == null)
        {
            return null;
        }

        // First, detect if cycle exists
        ListNode slow = head;
        ListNode fast = head;
        bool hasCycle = false;

        while (fast != null && fast.next != null)
        {
            slow = slow.next;
            fast = fast.next.next;

            if (slow == fast)
            {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle)
        {
            return null;
        }

        // Find cycle start: move slow to head, advance both one step at a time
        slow = head;
        while (slow != fast)
        {
            slow = slow.next;
            fast = fast.next;
        }

        return slow; // The node where cycle begins
    }
}
```

**Mathematical proof:** When pointers meet, they are equidistant from cycle start.

---

## Problem 3: Merge K Sorted Lists (Hard)

**Difficulty:** ⭐⭐⭐ Hard

### Problem Statement

You are given an array of k linked lists, each sorted in ascending order. Merge all lists into one sorted list and return it.

**Example:**

```
Input: [[1->4->5], [1->3->4], [2->6]]
Output: 1->1->2->3->4->4->5->6
```

### Solution 1: Brute Force - Merge One by One (Simple)

```csharp
public class Solution
{
    public ListNode MergeKLists(ListNode[] lists)
    {
        if (lists == null || lists.Length == 0)
        {
            return null;
        }

        ListNode result = lists[0];

        // Merge lists one by one
        for (int i = 1; i < lists.Length; i++)
        {
            result = MergeTwoLists(result, lists[i]);
        }

        return result;
    }

    private ListNode MergeTwoLists(ListNode l1, ListNode l2)
    {
        var dummy = new ListNode(0);
        ListNode current = dummy;

        while (l1 != null && l2 != null)
        {
            if (l1.val <= l2.val)
            {
                current.next = l1;
                l1 = l1.next;
            }
            else
            {
                current.next = l2;
                l2 = l2.next;
            }
            current = current.next;
        }

        current.next = l1 ?? l2;
        return dummy.next;
    }
}
```

**Time Complexity:** O(k × N) - where N is total nodes, k is number of lists  
**Space Complexity:** O(1) - Not counting output

**Explanation:**

- Merge first two lists, then merge result with third, and so on
- Each merge operation processes all nodes merged so far
- Inefficient because we process nodes multiple times

### Solution 2: Priority Queue (Min Heap) (Better)

```csharp
public class Solution
{
    public ListNode MergeKLists(ListNode[] lists)
    {
        if (lists == null || lists.Length == 0)
        {
            return null;
        }

        // C# doesn't have built-in min heap, use PriorityQueue (.NET 6+)
        var pq = new PriorityQueue<ListNode, int>();

        // Add first node of each list to priority queue
        foreach (var list in lists)
        {
            if (list != null)
            {
                pq.Enqueue(list, list.val);
            }
        }

        var dummy = new ListNode(0);
        ListNode current = dummy;

        while (pq.Count > 0)
        {
            // Get node with minimum value
            ListNode minNode = pq.Dequeue();
            current.next = minNode;
            current = current.next;

            // Add next node from same list to queue
            if (minNode.next != null)
            {
                pq.Enqueue(minNode.next, minNode.next.val);
            }
        }

        return dummy.next;
    }
}
```

**Time Complexity:** O(N log k) - N nodes, each pushed/popped from heap of size k  
**Space Complexity:** O(k) - Priority queue holds at most k nodes

**Explanation:**

- Use min heap to always get the smallest node among k lists
- Initially add first node from each list
- Extract minimum, add to result, insert next node from that list
- Heap operations are O(log k), done N times
- This is efficient for large k

### Solution 3: Divide and Conquer (Optimal)

```csharp
public class Solution
{
    public ListNode MergeKLists(ListNode[] lists)
    {
        if (lists == null || lists.Length == 0)
        {
            return null;
        }

        return MergeKListsHelper(lists, 0, lists.Length - 1);
    }

    private ListNode MergeKListsHelper(ListNode[] lists, int start, int end)
    {
        // Base case: single list
        if (start == end)
        {
            return lists[start];
        }

        // Base case: two lists
        if (start + 1 == end)
        {
            return MergeTwoLists(lists[start], lists[end]);
        }

        // Divide: split into two halves
        int mid = start + (end - start) / 2;
        ListNode left = MergeKListsHelper(lists, start, mid);
        ListNode right = MergeKListsHelper(lists, mid + 1, end);

        // Conquer: merge two halves
        return MergeTwoLists(left, right);
    }

    private ListNode MergeTwoLists(ListNode l1, ListNode l2)
    {
        if (l1 == null) return l2;
        if (l2 == null) return l1;

        if (l1.val <= l2.val)
        {
            l1.next = MergeTwoLists(l1.next, l2);
            return l1;
        }
        else
        {
            l2.next = MergeTwoLists(l1, l2.next);
            return l2;
        }
    }
}
```

**Time Complexity:** O(N log k) - Similar to merge sort  
**Space Complexity:** O(log k) - Recursion depth

**Explanation:**

- Divide k lists into pairs and merge each pair
- Repeat until one list remains
- Similar to merge sort strategy
- Tree has log k levels, each level processes N nodes
- More efficient than merging one by one
- This is the most optimal solution

**Merge tree visualization for k=4:**

```
Level 0:  [L1]  [L2]  [L3]  [L4]
           │     │     │     │
Level 1:  [L1+L2]     [L3+L4]
             │           │
Level 2:    [L1+L2+L3+L4]
```

---

## Key Takeaways for Day 5

### Linked List Techniques

#### 1. **Dummy Node Pattern**

```csharp
var dummy = new ListNode(0);
ListNode current = dummy;
// ... build list ...
return dummy.next; // Skip dummy
```

**Use for:** Simplify edge cases when building new lists

#### 2. **Two Pointers (Fast & Slow)**

```csharp
ListNode slow = head;
ListNode fast = head;
while (fast != null && fast.next != null)
{
    slow = slow.next;
    fast = fast.next.next;
}
// slow is at middle (or cycle detection)
```

**Use for:** Find middle, detect cycles, find kth from end

#### 3. **Reverse Links**

```csharp
ListNode prev = null;
while (current != null)
{
    ListNode next = current.next;
    current.next = prev;
    prev = current;
    current = next;
}
```

**Use for:** Reversing lists or portions of lists

#### 4. **Merge Two Sorted Lists**

```csharp
while (l1 != null && l2 != null)
{
    if (l1.val <= l2.val)
    {
        current.next = l1;
        l1 = l1.next;
    }
    else
    {
        current.next = l2;
        l2 = l2.next;
    }
    current = current.next;
}
current.next = l1 ?? l2;
```

**Use for:** Merging sorted lists

### Common Linked List Patterns

| Problem Type        | Technique                 | Time   | Space |
| ------------------- | ------------------------- | ------ | ----- |
| Reverse             | Iterative with 3 pointers | O(n)   | O(1)  |
| Find Middle         | Fast & Slow pointers      | O(n)   | O(1)  |
| Detect Cycle        | Floyd's algorithm         | O(n)   | O(1)  |
| Remove Nth from End | Two pointers with gap     | O(n)   | O(1)  |
| Merge Sorted        | Two pointers              | O(n+m) | O(1)  |

### Interview Tips for Linked Lists

1. **Always check for null:**

   ```csharp
   if (head == null || head.next == null)
       return head;
   ```

2. **Draw it out:**

   - Visualize pointer movements
   - Track 2-3 nodes at a time
   - Show before/after states

3. **Use dummy node:**

   - Simplifies edge cases
   - Easier to return head
   - Avoids special handling for first node

4. **Common edge cases:**

   - Empty list (null)
   - Single node
   - Two nodes
   - Cycle vs no cycle

5. **Space optimization:**
   - Most linked list problems can be solved in O(1) space
   - Avoid using extra data structures when possible
   - Think about in-place manipulation

### Linked List vs Array

| Feature                    | Array           | Linked List       |
| -------------------------- | --------------- | ----------------- |
| Access                     | O(1) random     | O(n) sequential   |
| Insert/Delete at beginning | O(n)            | O(1)              |
| Insert/Delete at end       | O(1) amortized  | O(n) without tail |
| Insert/Delete at middle    | O(n)            | O(1) with pointer |
| Memory                     | Contiguous      | Scattered         |
| Cache                      | Better locality | Worse locality    |

---

## Additional Practice Problems

1. **Remove Nth Node From End** (Medium) - Two pointers with gap
2. **Palindrome Linked List** (Easy) - Fast/slow + reverse
3. **Intersection of Two Linked Lists** (Easy) - Two pointers
4. **Add Two Numbers** (Medium) - Simulate addition
5. **Copy List with Random Pointer** (Medium) - Hash map or interleaving

**Tomorrow:** Day 6 - Stacks & Queues (LIFO & FIFO Patterns)
