# Day 6: Stacks & Queues - LIFO & FIFO Patterns

## Problem 1: Valid Parentheses (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given a string containing just the characters `'(', ')', '{', '}', '[' and ']'`, determine if the input string is valid. Opening brackets must be closed by the same type of brackets in correct order.

**Example:**

```
Input: s = "()[]{}"
Output: true

Input: s = "([)]"
Output: false
```

### Solution 1: Using Stack (Optimal)

```csharp
public class Solution
{
    public bool IsValid(string s)
    {
        var stack = new Stack<char>();
        var pairs = new Dictionary<char, char>
        {
            { ')', '(' },
            { '}', '{' },
            { ']', '[' }
        };

        foreach (char c in s)
        {
            if (c == '(' || c == '{' || c == '[')
            {
                // Opening bracket: push to stack
                stack.Push(c);
            }
            else
            {
                // Closing bracket: check if matches top of stack
                if (stack.Count == 0 || stack.Pop() != pairs[c])
                {
                    return false;
                }
            }
        }

        // Valid if all brackets matched (stack empty)
        return stack.Count == 0;
    }
}
```

**Time Complexity:** O(n) - Process each character once  
**Space Complexity:** O(n) - Stack can hold up to n/2 characters

**Explanation:**

- Stack is perfect for matching pairs (LIFO behavior)
- Push opening brackets onto stack
- For closing brackets, check if top of stack matches
- After processing all characters, stack should be empty
- This is the standard solution for this classic problem

### Common Mistakes to Avoid

```csharp
// MISTAKE 1: Not checking empty stack before Pop
if (stack.Pop() != pairs[c]) // Crashes if stack empty!

// CORRECT:
if (stack.Count == 0 || stack.Pop() != pairs[c])

// MISTAKE 2: Not checking if stack is empty at end
return true; // Wrong! Might have unmatched opening brackets

// CORRECT:
return stack.Count == 0;
```

---

## Problem 2: Daily Temperatures (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given an array of integers `temperatures` representing daily temperatures, return an array `answer` where `answer[i]` is the number of days until a warmer temperature. If there is no future day with warmer temperature, put 0 instead.

**Example:**

```
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
Explanation: Next warmer day for 73 is tomorrow (74), etc.
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int[] DailyTemperatures(int[] temperatures)
    {
        int n = temperatures.Length;
        int[] result = new int[n];

        for (int i = 0; i < n; i++)
        {
            // Look for next warmer day
            for (int j = i + 1; j < n; j++)
            {
                if (temperatures[j] > temperatures[i])
                {
                    result[i] = j - i;
                    break;
                }
            }
            // If not found, result[i] stays 0 (default)
        }

        return result;
    }
}
```

**Time Complexity:** O(n²) - Nested loops  
**Space Complexity:** O(1) - Not counting output array

**Explanation:**

- For each day, scan forward to find warmer day
- Simple but inefficient for large inputs
- May timeout on large test cases

### Solution 2: Monotonic Stack (Optimal)

```csharp
public class Solution
{
    public int[] DailyTemperatures(int[] temperatures)
    {
        int n = temperatures.Length;
        int[] result = new int[n];
        var stack = new Stack<int>(); // Store indices

        for (int i = 0; i < n; i++)
        {
            // Process all days that are colder than today
            while (stack.Count > 0 && temperatures[i] > temperatures[stack.Peek()])
            {
                int prevIndex = stack.Pop();
                result[prevIndex] = i - prevIndex;
            }

            // Add current day to stack
            stack.Push(i);
        }

        // Remaining indices in stack have no warmer day (result already 0)
        return result;
    }
}
```

**Time Complexity:** O(n) - Each index pushed and popped at most once  
**Space Complexity:** O(n) - Stack can hold all indices

**Explanation:**

- Use monotonic decreasing stack (temperatures are decreasing)
- Stack stores indices, not temperatures
- For each day, pop all colder days and update their results
- Current day becomes the "next warmer day" for popped days
- Days remaining in stack have no warmer day ahead
- This is a classic monotonic stack pattern

**Step-by-step example:**

```
temperatures = [73, 74, 75, 71]
Stack stores indices

i=0, temp=73:
  Stack empty, push 0
  Stack: [0]

i=1, temp=74:
  74 > 73 (stack[0]), pop 0, result[0] = 1-0 = 1
  Push 1
  Stack: [1]

i=2, temp=75:
  75 > 74 (stack[1]), pop 1, result[1] = 2-1 = 1
  Push 2
  Stack: [2]

i=3, temp=71:
  71 < 75, just push 3
  Stack: [2, 3]

Result: [1, 1, 0, 0] (indices 2,3 remain in stack → no warmer day)
```

---

## Problem 3: Sliding Window Maximum (Hard)

**Difficulty:** ⭐⭐⭐ Hard

### Problem Statement

Given an array `nums` and a sliding window of size `k`, return the maximum element in each window as the window slides from left to right.

**Example:**

```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]

Window positions:
[1  3  -1] -3  5  3  6  7  -> max = 3
 1 [3  -1  -3] 5  3  6  7  -> max = 3
 1  3 [-1  -3  5] 3  6  7  -> max = 5
 ...
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int[] MaxSlidingWindow(int[] nums, int k)
    {
        if (nums.Length == 0 || k == 0) return new int[0];

        int n = nums.Length;
        int[] result = new int[n - k + 1];

        for (int i = 0; i <= n - k; i++)
        {
            // Find max in window [i, i+k-1]
            int max = nums[i];
            for (int j = i; j < i + k; j++)
            {
                max = Math.Max(max, nums[j]);
            }
            result[i] = max;
        }

        return result;
    }
}
```

**Time Complexity:** O(n × k) - For each window, find max  
**Space Complexity:** O(1) - Not counting output

**Explanation:**

- For each window position, scan k elements to find max
- Simple but very inefficient
- Recalculates max even when most elements don't change

### Solution 2: Deque (Monotonic Queue) (Optimal)

```csharp
public class Solution
{
    public int[] MaxSlidingWindow(int[] nums, int k)
    {
        if (nums.Length == 0 || k == 0) return new int[0];

        int n = nums.Length;
        int[] result = new int[n - k + 1];
        var deque = new LinkedList<int>(); // Store indices

        for (int i = 0; i < n; i++)
        {
            // Remove indices outside current window
            while (deque.Count > 0 && deque.First.Value < i - k + 1)
            {
                deque.RemoveFirst();
            }

            // Remove indices with smaller values from back
            // (they can never be maximum)
            while (deque.Count > 0 && nums[deque.Last.Value] < nums[i])
            {
                deque.RemoveLast();
            }

            // Add current index to deque
            deque.AddLast(i);

            // First element is the maximum for current window
            if (i >= k - 1)
            {
                result[i - k + 1] = nums[deque.First.Value];
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(n) - Each element added and removed at most once  
**Space Complexity:** O(k) - Deque holds at most k elements

**Explanation:**

- Use deque (double-ended queue) to maintain potential maximums
- Deque stores indices in decreasing order of values
- Front of deque always has index of current maximum
- Remove indices outside current window from front
- Remove smaller values from back (they can't be future maximums)
- This maintains a monotonic decreasing deque
- One of the hardest queue problems!

**Detailed walkthrough:**

```
nums = [1,3,-1,-3,5], k = 3

i=0, num=1:
  Add 0
  Deque: [0] (values: [1])

i=1, num=3:
  3 > 1, remove 0 from back
  Add 1
  Deque: [1] (values: [3])

i=2, num=-1:
  -1 < 3, just add 2
  Window complete! result[0] = nums[1] = 3
  Deque: [1, 2] (values: [3, -1])

i=3, num=-3:
  Index 1 in window [1,3], keep it
  -3 < -1, just add 3
  result[1] = nums[1] = 3
  Deque: [1, 2, 3] (values: [3, -1, -3])

i=4, num=5:
  Index 1 outside window [2,4], remove from front
  5 > all remaining, clear deque
  Add 4
  result[2] = nums[4] = 5
  Deque: [4] (values: [5])
```

### Solution 3: Using C# Queue (Less Optimal but Simpler)

```csharp
public class Solution
{
    public int[] MaxSlidingWindow(int[] nums, int k)
    {
        if (nums.Length == 0 || k == 0) return new int[0];

        var pq = new PriorityQueue<int, int>(); // value, -value (for max heap)
        int n = nums.Length;
        int[] result = new int[n - k + 1];

        // Add first k elements
        for (int i = 0; i < k; i++)
        {
            pq.Enqueue(i, -nums[i]); // Negative for max heap behavior
        }

        result[0] = nums[pq.Peek()];

        for (int i = k; i < n; i++)
        {
            pq.Enqueue(i, -nums[i]);

            // Remove elements outside window
            while (pq.Peek() <= i - k)
            {
                pq.Dequeue();
            }

            result[i - k + 1] = nums[pq.Peek()];
        }

        return result;
    }
}
```

**Time Complexity:** O(n log k) - Priority queue operations  
**Space Complexity:** O(k) - Priority queue size

**Explanation:**

- Use max heap (priority queue) to track maximum
- Easier to understand than deque solution
- Slightly less efficient (O(n log k) vs O(n))
- Still acceptable for interviews

---

## Key Takeaways for Day 6

### Stack Patterns

#### 1. **Matching/Balancing Pattern**

```csharp
var stack = new Stack<char>();
foreach (char c in input)
{
    if (isOpening(c))
        stack.Push(c);
    else if (stack.Count == 0 || !matches(stack.Pop(), c))
        return false;
}
return stack.Count == 0;
```

**Use for:** Parentheses, HTML tags, balanced expressions

#### 2. **Monotonic Stack Pattern**

```csharp
var stack = new Stack<int>(); // Store indices
for (int i = 0; i < arr.Length; i++)
{
    while (stack.Count > 0 && arr[i] > arr[stack.Peek()])
    {
        int prev = stack.Pop();
        // Process prev with i as next greater element
    }
    stack.Push(i);
}
```

**Use for:** Next greater/smaller element, stock span, histogram problems

#### 3. **Expression Evaluation**

```csharp
// Separate stacks for operands and operators
var values = new Stack<int>();
var operators = new Stack<char>();
```

**Use for:** Calculator problems, postfix evaluation

### Queue Patterns

#### 1. **Sliding Window with Deque**

```csharp
var deque = new LinkedList<int>();
// Maintain elements in useful order
// Remove from both ends as needed
```

**Use for:** Sliding window maximum/minimum

#### 2. **BFS Pattern (Coming in Day 9)**

```csharp
var queue = new Queue<T>();
queue.Enqueue(start);
while (queue.Count > 0)
{
    var current = queue.Dequeue();
    // Process and enqueue neighbors
}
```

**Use for:** Level-order traversal, shortest path

### Stack vs Queue

| Feature           | Stack                           | Queue                           |
| ----------------- | ------------------------------- | ------------------------------- |
| Order             | LIFO (Last In First Out)        | FIFO (First In First Out)       |
| Operations        | Push, Pop, Peek                 | Enqueue, Dequeue, Peek          |
| Use Cases         | Undo/Redo, Expression eval, DFS | BFS, Task scheduling, Buffering |
| C# Implementation | `Stack<T>`                      | `Queue<T>`                      |

### C# Collections for Stack/Queue Problems

```csharp
// Stack
var stack = new Stack<int>();
stack.Push(1);
int top = stack.Peek();  // Look without removing
int item = stack.Pop();  // Remove and return
bool empty = stack.Count == 0;

// Queue
var queue = new Queue<int>();
queue.Enqueue(1);
int front = queue.Peek();
int item = queue.Dequeue();
bool empty = queue.Count == 0;

// Deque (use LinkedList)
var deque = new LinkedList<int>();
deque.AddFirst(1);     // Add to front
deque.AddLast(2);      // Add to back
deque.RemoveFirst();   // Remove from front
deque.RemoveLast();    // Remove from back
int first = deque.First.Value;
int last = deque.Last.Value;

// Priority Queue (.NET 6+)
var pq = new PriorityQueue<T, int>();
pq.Enqueue(item, priority);
T item = pq.Dequeue(); // Gets item with lowest priority
```

### Interview Tips

1. **Recognize stack problems:**

   - "Nearest greater/smaller element"
   - "Valid/balanced"
   - "Nested structures"
   - "Expression evaluation"
   - Can you process items in reverse order?

2. **Recognize queue problems:**

   - "Process in order"
   - "First come first serve"
   - "Level by level"
   - "Sliding window" (with deque)

3. **Common patterns:**

   - Monotonic stack → store indices, not values
   - Always check empty before Pop/Peek
   - Use dummy nodes or initialize carefully
   - Consider using deque when need both ends

4. **Edge cases:**
   - Empty input
   - Single element
   - All same elements
   - Strictly increasing/decreasing

---

## Additional Practice Problems

1. **Min Stack** (Easy) - Design stack with O(1) min operation
2. **Evaluate Reverse Polish Notation** (Medium) - Stack for postfix
3. **Largest Rectangle in Histogram** (Hard) - Monotonic stack
4. **Basic Calculator II** (Medium) - Stack for expression evaluation
5. **Implement Queue using Stacks** (Easy) - Two stacks = one queue

**Tomorrow:** Day 7 - Binary Trees (Tree Fundamentals & Traversals)
