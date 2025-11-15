# Day 5: Selection Algorithms & Kth Element 🎯

## Overview

**Selection algorithms** (finding the Kth largest/smallest element) appear in approximately **15-20%** of big tech interviews. These problems test:

- Heap data structures (PriorityQueue)
- Quickselect algorithm understanding
- Trade-offs between sorting and selection
- Time complexity optimization

**Key Insight:** Finding the Kth element doesn't require full sorting. Quickselect gives O(n) average time, while heaps give O(n log k).

---

## Problem 1: Kth Largest Element in an Array ⭐⭐ (Medium)

### Problem Statement

Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.

Note that it is the `k`th largest element in the **sorted order**, not the `k`th distinct element.

Can you solve it **without sorting**?

### Example

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Explanation: Sorted array is [6,5,4,3,2,1], 2nd largest is 5

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

---

### Solution 1: Sorting (Simple but Not Optimal)

```csharp
public class Solution
{
    public int FindKthLargest(int[] nums, int k)
    {
        Array.Sort(nums);
        return nums[nums.Length - k];
    }
}
```

**Time Complexity:** O(n log n) - Sorting  
**Space Complexity:** O(1) - In-place sort (depends on sort implementation)

**Explanation:**

- Sort array in ascending order
- Kth largest is at index `n - k`
- Simple but overkill (we don't need full sort)

---

### Solution 2: Min Heap of Size K (Better)

```csharp
public class Solution
{
    public int FindKthLargest(int[] nums, int k)
    {
        // Min heap: smallest element at top
        var minHeap = new PriorityQueue<int, int>();

        foreach (int num in nums)
        {
            minHeap.Enqueue(num, num);

            // Keep only k largest elements
            if (minHeap.Count > k)
            {
                minHeap.Dequeue();  // Remove smallest
            }
        }

        // Top of min heap is kth largest
        return minHeap.Peek();
    }
}
```

**Time Complexity:** O(n log k) - n insertions, each O(log k)  
**Space Complexity:** O(k) - Heap size

**Explanation:**

1. Maintain min heap of k largest elements seen so far
2. Heap top is always the smallest of these k elements
3. When heap size exceeds k, remove the smallest
4. Final heap top is the kth largest overall

**Why min heap?** We want to quickly remove the smallest element when we have more than k elements.

---

### Solution 3: Quickselect (Optimal Average Case)

```csharp
public class Solution
{
    private Random rand = new Random();

    public int FindKthLargest(int[] nums, int k)
    {
        // Kth largest = (n - k)th smallest in 0-indexed
        return Quickselect(nums, 0, nums.Length - 1, nums.Length - k);
    }

    private int Quickselect(int[] nums, int left, int right, int kSmallest)
    {
        if (left == right)
            return nums[left];

        // Partition around random pivot
        int pivotIndex = Partition(nums, left, right);

        if (kSmallest == pivotIndex)
        {
            return nums[kSmallest];
        }
        else if (kSmallest < pivotIndex)
        {
            // Search left half
            return Quickselect(nums, left, pivotIndex - 1, kSmallest);
        }
        else
        {
            // Search right half
            return Quickselect(nums, pivotIndex + 1, right, kSmallest);
        }
    }

    private int Partition(int[] nums, int left, int right)
    {
        // Random pivot for better average performance
        int randomIndex = rand.Next(left, right + 1);
        Swap(nums, randomIndex, right);

        int pivot = nums[right];
        int i = left;

        // Move elements smaller than pivot to left
        for (int j = left; j < right; j++)
        {
            if (nums[j] < pivot)
            {
                Swap(nums, i, j);
                i++;
            }
        }

        // Place pivot in correct position
        Swap(nums, i, right);
        return i;
    }

    private void Swap(int[] nums, int i, int j)
    {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

**Time Complexity:**

- Average: O(n) - Each partition eliminates half on average
- Worst: O(n²) - If always pick bad pivot (rare with random)

**Space Complexity:** O(1) - In-place

**Explanation:**

1. Based on QuickSort partitioning
2. After partition, pivot is in correct sorted position
3. If pivot index = k, we found the answer
4. Otherwise, recurse on appropriate half only
5. Random pivot helps avoid worst case

**Why O(n) average?**

- First partition: O(n)
- Second partition: O(n/2)
- Third partition: O(n/4)
- Sum: n + n/2 + n/4 + ... ≈ 2n = O(n)

---

### Solution 4: Max Heap (Alternative Approach)

```csharp
public class Solution
{
    public int FindKthLargest(int[] nums, int k)
    {
        // C# PriorityQueue is min heap by default
        // Negate values to simulate max heap
        var maxHeap = new PriorityQueue<int, int>();

        foreach (int num in nums)
        {
            maxHeap.Enqueue(num, -num);  // Negate for max heap behavior
        }

        // Pop k-1 times to get kth largest
        for (int i = 0; i < k - 1; i++)
        {
            maxHeap.Dequeue();
        }

        return maxHeap.Peek();
    }
}
```

**Time Complexity:** O(n log n + k log n) = O(n log n)  
**Space Complexity:** O(n) - Full heap

**Explanation:**

- Build max heap with all elements
- Pop k-1 times, next element is kth largest
- Less efficient than min heap of size k

---

## Problem 2: Top K Frequent Elements ⭐⭐ (Medium)

### Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in **any order**.

### Example

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Input: nums = [1], k = 1
Output: [1]
```

---

### Solution 1: Heap (Straightforward)

```csharp
public class Solution
{
    public int[] TopKFrequent(int[] nums, int k)
    {
        // Count frequencies
        var freqMap = new Dictionary<int, int>();
        foreach (int num in nums)
        {
            freqMap[num] = freqMap.GetValueOrDefault(num, 0) + 1;
        }

        // Min heap of size k (by frequency)
        var minHeap = new PriorityQueue<int, int>();

        foreach (var (num, freq) in freqMap)
        {
            minHeap.Enqueue(num, freq);

            if (minHeap.Count > k)
            {
                minHeap.Dequeue();
            }
        }

        // Extract results
        var result = new int[k];
        for (int i = 0; i < k; i++)
        {
            result[i] = minHeap.Dequeue();
        }

        return result;
    }
}
```

**Time Complexity:** O(n + m log k) where m is unique elements  
**Space Complexity:** O(m) - Frequency map + heap

**Explanation:**

1. Count frequencies in O(n)
2. Maintain min heap of k most frequent
3. Heap ordered by frequency
4. Same pattern as Kth largest

---

### Solution 2: Bucket Sort (Optimal)

```csharp
public class Solution
{
    public int[] TopKFrequent(int[] nums, int k)
    {
        // Count frequencies
        var freqMap = new Dictionary<int, int>();
        foreach (int num in nums)
        {
            freqMap[num] = freqMap.GetValueOrDefault(num, 0) + 1;
        }

        // Bucket sort: bucket[i] contains numbers with frequency i
        var buckets = new List<int>[nums.Length + 1];

        foreach (var (num, freq) in freqMap)
        {
            if (buckets[freq] == null)
                buckets[freq] = new List<int>();

            buckets[freq].Add(num);
        }

        // Collect top k from highest frequency buckets
        var result = new List<int>();
        for (int freq = buckets.Length - 1; freq >= 0 && result.Count < k; freq--)
        {
            if (buckets[freq] != null)
            {
                result.AddRange(buckets[freq]);
            }
        }

        return result.Take(k).ToArray();
    }
}
```

**Time Complexity:** O(n) - Linear time  
**Space Complexity:** O(n) - Buckets array

**Explanation:**

1. Frequency can't exceed n (array length)
2. Create n+1 buckets, bucket[i] holds numbers with frequency i
3. Iterate from highest frequency downward
4. Collect k elements
5. **Key insight:** Frequency values are bounded by n

---

## Problem 3: Kth Smallest Element in a Sorted Matrix ⭐⭐⭐ (Medium-Hard)

### Problem Statement

Given an `n x n` matrix where each row and column is sorted in ascending order, return the `k`th smallest element in the matrix.

Note: It is the kth smallest element **in the sorted order**, not the kth distinct element.

### Example

```
Input: matrix =
[[1,  5,  9],
 [10, 11, 13],
 [12, 13, 15]],
k = 8

Output: 13
Explanation: The 8th smallest element is 13
```

---

### Solution 1: Min Heap (Intuitive)

```csharp
public class Solution
{
    public int KthSmallest(int[][] matrix, int k)
    {
        int n = matrix.Length;

        // Min heap: (value, row, col)
        var minHeap = new PriorityQueue<(int val, int row, int col), int>();

        // Add first element from each row
        for (int r = 0; r < Math.Min(n, k); r++)
        {
            minHeap.Enqueue((matrix[r][0], r, 0), matrix[r][0]);
        }

        // Pop k-1 times
        for (int i = 0; i < k - 1; i++)
        {
            var (val, row, col) = minHeap.Dequeue();

            // Add next element from same row
            if (col + 1 < n)
            {
                minHeap.Enqueue((matrix[row][col + 1], row, col + 1),
                               matrix[row][col + 1]);
            }
        }

        return minHeap.Peek().val;
    }
}
```

**Time Complexity:** O(k log n) - k pops, each O(log n)  
**Space Complexity:** O(n) - Heap size

**Explanation:**

1. Start with first element of each row in heap
2. Pop smallest k times
3. When pop element at (r, c), add (r, c+1) to heap
4. Similar to merging k sorted lists

---

### Solution 2: Binary Search (Optimal)

```csharp
public class Solution
{
    public int KthSmallest(int[][] matrix, int k)
    {
        int n = matrix.Length;
        int left = matrix[0][0];
        int right = matrix[n - 1][n - 1];

        while (left < right)
        {
            int mid = left + (right - left) / 2;

            // Count elements <= mid
            int count = CountLessOrEqual(matrix, mid);

            if (count < k)
            {
                left = mid + 1;
            }
            else
            {
                right = mid;
            }
        }

        return left;
    }

    private int CountLessOrEqual(int[][] matrix, int target)
    {
        int n = matrix.Length;
        int count = 0;
        int row = n - 1, col = 0;

        // Start from bottom-left corner
        while (row >= 0 && col < n)
        {
            if (matrix[row][col] <= target)
            {
                count += row + 1;  // All elements in this column up to row
                col++;
            }
            else
            {
                row--;
            }
        }

        return count;
    }
}
```

**Time Complexity:** O(n log(max - min)) - Binary search on value range  
**Space Complexity:** O(1)

**Explanation:**

1. **Binary search on answer** (not on indices!)
2. For each mid value, count how many elements ≤ mid
3. If count < k, answer is larger
4. CountLessOrEqual uses sorted property: O(n) per call
5. Clever technique: search on value range, not position

---

## Key Takeaways

### 1. Selection Algorithm Patterns

| Problem Type             | Best Approach          | Time Complexity |
| ------------------------ | ---------------------- | --------------- |
| **Kth largest in array** | Quickselect            | O(n) average    |
| **Kth largest (stable)** | Min heap of size k     | O(n log k)      |
| **Top K frequent**       | Bucket sort            | O(n)            |
| **Kth in sorted matrix** | Binary search on value | O(n log range)  |

### 2. Heap Strategies

```csharp
// Min heap for K largest elements
var minHeap = new PriorityQueue<int, int>();
foreach (int num in nums)
{
    minHeap.Enqueue(num, num);
    if (minHeap.Count > k)
        minHeap.Dequeue();
}
return minHeap.Peek();  // Kth largest

// Max heap simulation (negate priority)
var maxHeap = new PriorityQueue<int, int>();
maxHeap.Enqueue(num, -num);

// Custom priority (e.g., by frequency)
minHeap.Enqueue(element, frequency);
```

### 3. When to Use Each Approach

✅ **Quickselect:** Need exact kth, can modify array, average O(n) is acceptable  
✅ **Min heap of size k:** Can't modify array, need stable solution, streaming data  
✅ **Bucket sort:** Bounded value range (like frequencies)  
✅ **Binary search on answer:** Sorted matrix/structure, can count efficiently

### 4. Interview Tips

✅ **Clarify k:** Is it 1-indexed or 0-indexed? Kth largest or smallest?  
✅ **Ask about duplicates:** Kth distinct or allowing duplicates?  
✅ **Discuss trade-offs:** Quickselect vs heap (time vs space, average vs worst)  
✅ **Mention streaming:** If data stream, heap is better (can't do quickselect)  
✅ **Binary search creativity:** When sorted structure, think binary search on answer

---

## Practice Problems

### Easy

1. **Find K Pairs with Smallest Sums** - Merge k sorted lists pattern

### Medium

2. **Kth Largest Element** ✓ (Covered above)
3. **Top K Frequent Elements** ✓ (Covered above)
4. **Kth Smallest in Sorted Matrix** ✓ (Covered above)
5. **K Closest Points to Origin** - Same pattern with distance
6. **Reorganize String** - Frequency + heap

### Hard

7. **Find Median from Data Stream** - Two heaps
8. **Sliding Window Median** - Two heaps + removal
9. **Swim in Rising Water** - Binary search + BFS

---

## Common Mistakes to Avoid

❌ **Using max heap for kth largest** - Use min heap of size k instead  
❌ **Forgetting index conversion** - Kth largest = (n-k)th smallest  
❌ **Not randomizing quickselect pivot** - Can hit O(n²) worst case  
❌ **Full sort for selection** - Overkill, use quickselect or heap  
❌ **Wrong heap type** - Largest → min heap, Smallest → max heap

---

## Time Complexity Comparison

| Approach              | Average        | Worst          | Space | When to Use               |
| --------------------- | -------------- | -------------- | ----- | ------------------------- |
| **Sorting**           | O(n log n)     | O(n log n)     | O(1)  | Simple, k close to n      |
| **Quickselect**       | O(n)           | O(n²)          | O(1)  | Can modify, need O(n) avg |
| **Min Heap (size k)** | O(n log k)     | O(n log k)     | O(k)  | Streaming, can't modify   |
| **Max Heap (size n)** | O(n + k log n) | O(n + k log n) | O(n)  | Need all elements anyway  |
| **Bucket Sort**       | O(n)           | O(n)           | O(n)  | Bounded frequency range   |

---

## Next Steps

- ✅ Master heap operations in C#
- 📚 Practice "binary search on answer" technique
- 🎯 Study median problems (two-heap pattern)
- 💡 Learn partial sorting (nth_element in C++)

**Remember:** Selection doesn't require full sorting! Quickselect gives O(n) average, heaps give O(n log k). Choose based on constraints and whether you can modify the array.
