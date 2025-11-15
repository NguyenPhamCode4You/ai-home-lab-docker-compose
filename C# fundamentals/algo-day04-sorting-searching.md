# Day 4: Sorting & Searching - Binary Search & Sort Algorithms

## Problem 1: Binary Search (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given a sorted array of integers `nums` and a target value, return the index of the target if found. If not found, return -1. You must write an algorithm with O(log n) runtime complexity.

**Example:**

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums at index 4
```

### Solution 1: Linear Search (Simple)

```csharp
public class Solution
{
    public int Search(int[] nums, int target)
    {
        for (int i = 0; i < nums.Length; i++)
        {
            if (nums[i] == target)
            {
                return i;
            }
        }
        return -1;
    }
}
```

**Time Complexity:** O(n) - Check every element  
**Space Complexity:** O(1) - No extra space

**Explanation:**

- Simple linear scan through array
- Doesn't use the fact that array is sorted
- Doesn't meet O(log n) requirement

### Solution 2: Binary Search Iterative (Optimal)

```csharp
public class Solution
{
    public int Search(int[] nums, int target)
    {
        int left = 0;
        int right = nums.Length - 1;

        while (left <= right)
        {
            // Avoid overflow: use left + (right - left) / 2
            int mid = left + (right - left) / 2;

            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                // Target is in right half
                left = mid + 1;
            }
            else
            {
                // Target is in left half
                right = mid - 1;
            }
        }

        return -1; // Not found
    }
}
```

**Time Complexity:** O(log n) - Halve search space each iteration  
**Space Complexity:** O(1) - Only using pointers

**Explanation:**

- Divide and conquer approach
- Each iteration eliminates half the remaining elements
- Key: mid calculation to avoid integer overflow
- Use `left + (right - left) / 2` instead of `(left + right) / 2`
- This is the standard binary search implementation

### Solution 3: Binary Search Recursive

```csharp
public class Solution
{
    public int Search(int[] nums, int target)
    {
        return BinarySearchHelper(nums, target, 0, nums.Length - 1);
    }

    private int BinarySearchHelper(int[] nums, int target, int left, int right)
    {
        if (left > right)
        {
            return -1; // Base case: not found
        }

        int mid = left + (right - left) / 2;

        if (nums[mid] == target)
        {
            return mid;
        }
        else if (nums[mid] < target)
        {
            return BinarySearchHelper(nums, target, mid + 1, right);
        }
        else
        {
            return BinarySearchHelper(nums, target, left, mid - 1);
        }
    }
}
```

**Time Complexity:** O(log n) - Same as iterative  
**Space Complexity:** O(log n) - Recursion call stack

**Explanation:**

- Same logic as iterative but using recursion
- Each recursive call processes half the array
- Recursion depth is log n
- Iterative version preferred in interviews (no stack overhead)

---

## Problem 2: Find First and Last Position (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given a sorted array of integers, find the starting and ending position of a given target value. If target is not found, return `[-1, -1]`. Algorithm must run in O(log n) time.

**Example:**

```
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
```

### Solution 1: Linear Scan (Simple)

```csharp
public class Solution
{
    public int[] SearchRange(int[] nums, int target)
    {
        int first = -1, last = -1;

        for (int i = 0; i < nums.Length; i++)
        {
            if (nums[i] == target)
            {
                if (first == -1)
                {
                    first = i;
                }
                last = i;
            }
        }

        return new int[] { first, last };
    }
}
```

**Time Complexity:** O(n) - May scan entire array  
**Space Complexity:** O(1)

**Explanation:**

- Find first occurrence, then keep updating last
- Simple but doesn't meet O(log n) requirement
- Inefficient when target appears many times

### Solution 2: Two Binary Searches (Optimal)

```csharp
public class Solution
{
    public int[] SearchRange(int[] nums, int target)
    {
        int first = FindBound(nums, target, true);

        // If target not found, no need to search for last
        if (first == -1)
        {
            return new int[] { -1, -1 };
        }

        int last = FindBound(nums, target, false);
        return new int[] { first, last };
    }

    private int FindBound(int[] nums, int target, bool findFirst)
    {
        int left = 0;
        int right = nums.Length - 1;
        int result = -1;

        while (left <= right)
        {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target)
            {
                result = mid; // Found target, but keep searching

                if (findFirst)
                {
                    // For first occurrence, search left half
                    right = mid - 1;
                }
                else
                {
                    // For last occurrence, search right half
                    left = mid + 1;
                }
            }
            else if (nums[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        return result;
    }
}
```

**Time Complexity:** O(log n) - Two binary searches  
**Space Complexity:** O(1)

**Explanation:**

- Run binary search twice: once for first position, once for last
- Key difference: when target found, don't return immediately
- For first: continue searching left to find earlier occurrence
- For last: continue searching right to find later occurrence
- This is the optimal solution for this problem

---

## Problem 3: Search in Rotated Sorted Array (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

A sorted array has been rotated at an unknown pivot. Given this array and a target, return the index of target, or -1 if not found. Algorithm must run in O(log n) time.

**Example:**

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
Explanation: Array was [0,1,2,4,5,6,7] rotated at pivot
```

### Solution 1: Find Pivot Then Binary Search (Simple)

```csharp
public class Solution
{
    public int Search(int[] nums, int target)
    {
        // Find the pivot (minimum element)
        int pivot = FindPivot(nums);

        // Determine which half to search
        if (pivot == 0 || target < nums[0])
        {
            // Search right half
            return BinarySearch(nums, pivot, nums.Length - 1, target);
        }
        else
        {
            // Search left half
            return BinarySearch(nums, 0, pivot - 1, target);
        }
    }

    private int FindPivot(int[] nums)
    {
        int left = 0, right = nums.Length - 1;

        while (left < right)
        {
            int mid = left + (right - left) / 2;

            if (nums[mid] > nums[right])
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

    private int BinarySearch(int[] nums, int left, int right, int target)
    {
        while (left <= right)
        {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target)
            {
                return mid;
            }
            else if (nums[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        return -1;
    }
}
```

**Time Complexity:** O(log n) - Two binary searches  
**Space Complexity:** O(1)

**Explanation:**

- First find the pivot point (where array was rotated)
- Then do normal binary search in appropriate half
- Clear and easy to understand approach
- Two separate binary searches

### Solution 2: Modified Binary Search (Optimal)

```csharp
public class Solution
{
    public int Search(int[] nums, int target)
    {
        int left = 0;
        int right = nums.Length - 1;

        while (left <= right)
        {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target)
            {
                return mid;
            }

            // Determine which half is sorted
            if (nums[left] <= nums[mid])
            {
                // Left half is sorted
                if (nums[left] <= target && target < nums[mid])
                {
                    // Target is in sorted left half
                    right = mid - 1;
                }
                else
                {
                    // Target is in right half
                    left = mid + 1;
                }
            }
            else
            {
                // Right half is sorted
                if (nums[mid] < target && target <= nums[right])
                {
                    // Target is in sorted right half
                    left = mid + 1;
                }
                else
                {
                    // Target is in left half
                    right = mid - 1;
                }
            }
        }

        return -1;
    }
}
```

**Time Complexity:** O(log n) - Single binary search  
**Space Complexity:** O(1)

**Explanation:**

- Key insight: at least one half is always sorted
- Determine which half is sorted by comparing endpoints
- If left half sorted: check if target in range [left, mid]
- If right half sorted: check if target in range [mid, right]
- Search appropriate half based on where target should be
- This is more elegant with single pass

### Detailed Walkthrough

```
nums = [4,5,6,7,0,1,2], target = 0

Iteration 1:
  left=0, right=6, mid=3
  nums[mid]=7, nums[left]=4, nums[right]=2
  Left half [4,5,6,7] is sorted
  Target 0 not in [4,7], search right
  left = 4

Iteration 2:
  left=4, right=6, mid=5
  nums[mid]=1, nums[left]=0, nums[right]=2
  Left half [0,1] is sorted
  Target 0 in [0,1], search left
  right = 4

Iteration 3:
  left=4, right=4, mid=4
  nums[mid]=0 = target
  Found at index 4!
```

---

## Key Takeaways for Day 4

### Binary Search Template

```csharp
int left = 0, right = nums.Length - 1;
while (left <= right)
{
    int mid = left + (right - left) / 2;

    if (nums[mid] == target)
        return mid;
    else if (nums[mid] < target)
        left = mid + 1;  // Search right
    else
        right = mid - 1; // Search left
}
return -1; // Not found
```

### Binary Search Variations

#### 1. **Standard Binary Search**

- Find exact target in sorted array
- Return index or -1

#### 2. **Find Boundary (First/Last Occurrence)**

- Continue searching after finding target
- Track result and narrow search space

#### 3. **Search Space Reduction**

- Not always on sorted array
- Any monotonic function works
- Examples: find minimum in rotated array

#### 4. **Binary Search on Answer**

- Search space is range of possible answers
- Used in optimization problems
- Example: "minimum capacity to ship packages"

### Common Binary Search Pitfalls

1. **Infinite Loop**

   ```csharp
   // WRONG: might cause infinite loop
   while (left < right)
   {
       int mid = (left + right) / 2;
       left = mid; // Should be mid + 1
   }
   ```

2. **Integer Overflow**

   ```csharp
   // WRONG: can overflow for large values
   int mid = (left + right) / 2;

   // CORRECT:
   int mid = left + (right - left) / 2;
   ```

3. **Off-by-One Errors**
   - Use `left <= right` for finding exact match
   - Use `left < right` for finding boundaries
   - Carefully choose `mid + 1` vs `mid` and `mid - 1` vs `mid`

### Sorting Algorithms Comparison

| Algorithm      | Time (Best) | Time (Average) | Time (Worst) | Space    | Stable |
| -------------- | ----------- | -------------- | ------------ | -------- | ------ |
| Quick Sort     | O(n log n)  | O(n log n)     | O(n²)        | O(log n) | No     |
| Merge Sort     | O(n log n)  | O(n log n)     | O(n log n)   | O(n)     | Yes    |
| Heap Sort      | O(n log n)  | O(n log n)     | O(n log n)   | O(1)     | No     |
| Bubble Sort    | O(n)        | O(n²)          | O(n²)        | O(1)     | Yes    |
| Insertion Sort | O(n)        | O(n²)          | O(n²)        | O(1)     | Yes    |

**C# Array.Sort():**

- Uses IntroSort (hybrid: QuickSort + HeapSort + InsertionSort)
- O(n log n) average and worst case
- Not stable for primitive types, stable for reference types

### When to Use Binary Search

**Prerequisites:**

- Array/list is sorted (or search space is monotonic)
- Random access available (not linked list)

**Indicators in problem:**

- "Sorted array"
- "Find in O(log n)"
- "Find first/last occurrence"
- "Minimum/maximum that satisfies condition"
- "Search in rotated array"

### Interview Tips

1. **Always clarify:**

   - Is array sorted?
   - Are there duplicates?
   - What to return if not found?

2. **Start with template:**

   - Write standard binary search first
   - Modify based on requirements
   - Test with simple examples

3. **Edge cases:**

   - Empty array
   - Single element
   - Target at boundaries
   - All elements same
   - Target not in array

4. **Explain your logic:**
   - Why you're narrowing to left/right
   - How you handle equal elements
   - Why your termination condition works

---

## Additional Practice Problems

1. **Find Minimum in Rotated Sorted Array** (Medium)
2. **Search a 2D Matrix** (Medium) - Binary search on matrix
3. **Find Peak Element** (Medium) - Binary search on unsorted
4. **Median of Two Sorted Arrays** (Hard) - Advanced binary search
5. **Split Array Largest Sum** (Hard) - Binary search on answer

**Tomorrow:** Day 5 - Linked Lists (Pointers & List Manipulation)
