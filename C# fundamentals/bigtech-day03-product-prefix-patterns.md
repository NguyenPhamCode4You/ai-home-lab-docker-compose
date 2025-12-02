# Day 3: Product & Prefix Patterns 🎯

## Overview

**Prefix/suffix patterns** appear in approximately **20-25% of big tech interviews**. These problems test:

- Understanding of cumulative operations
- Optimization from O(n²) to O(n)
- Space-time tradeoffs
- Creative use of pre-computation

**Key Insight:** When you need to compute aggregate information for subarrays, think prefix sums or products. The pattern is: `result[i] = prefix[i] × suffix[i]`.

---

## Problem 1: Product of Array Except Self ⭐⭐⭐ (Medium)

### Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

**Constraint:** You must write an algorithm that runs in **O(n)** time and **without using division**.

### Example

```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Explanation:
answer[0] = 2×3×4 = 24
answer[1] = 1×3×4 = 12
answer[2] = 1×2×4 = 8
answer[3] = 1×2×3 = 6

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

---

### Solution 1: Brute Force (Not Optimal)

```csharp
public class Solution
{
    public int[] ProductExceptSelf(int[] nums)
    {
        int n = nums.Length;
        int[] answer = new int[n];

        for (int i = 0; i < n; i++)
        {
            int product = 1;
            for (int j = 0; j < n; j++)
            {
                if (i != j)
                {
                    product *= nums[j];
                }
            }
            answer[i] = product;
        }

        return answer;
    }
}
```

**Time Complexity:** O(n²) - Nested loops  
**Space Complexity:** O(1) - Not counting output

**Explanation:**

- For each position, multiply all other elements
- Too slow for large inputs
- Helps understand the problem

---

### Solution 2: Left and Right Arrays (Better)

```csharp
public class Solution
{
    public int[] ProductExceptSelf(int[] nums)
    {
        int n = nums.Length;

        // left[i] = product of all elements to the left of i
        int[] left = new int[n];
        // right[i] = product of all elements to the right of i
        int[] right = new int[n];
        int[] answer = new int[n];

        // Build left array
        left[0] = 1;
        for (int i = 1; i < n; i++)
        {
            left[i] = left[i - 1] * nums[i - 1];
        }

        // Build right array
        right[n - 1] = 1;
        for (int i = n - 2; i >= 0; i--)
        {
            right[i] = right[i + 1] * nums[i + 1];
        }

        // Combine: answer[i] = left[i] * right[i]
        for (int i = 0; i < n; i++)
        {
            answer[i] = left[i] * right[i];
        }

        return answer;
    }
}
```

**Time Complexity:** O(n) - Three passes  
**Space Complexity:** O(n) - Two extra arrays

**Explanation:**

- `left[i]` = product of `nums[0..i-1]`
- `right[i]` = product of `nums[i+1..n-1]`
- Result = left × right

**Visual Example for [1,2,3,4]:**

```
nums:   [1, 2, 3, 4]
left:   [1, 1, 2, 6]   (1, 1, 1×2, 1×2×3)
right:  [24,12,4, 1]   (2×3×4, 3×4, 4, 1)
answer: [24,12,8, 6]   (left × right)
```

---

### Solution 3: Single Array Optimization (Optimal)

```csharp
public class Solution
{
    public int[] ProductExceptSelf(int[] nums)
    {
        int n = nums.Length;
        int[] answer = new int[n];

        // Build left products directly in answer array
        answer[0] = 1;
        for (int i = 1; i < n; i++)
        {
            answer[i] = answer[i - 1] * nums[i - 1];
        }

        // Build right products and multiply with existing left products
        int rightProduct = 1;
        for (int i = n - 1; i >= 0; i--)
        {
            answer[i] *= rightProduct;
            rightProduct *= nums[i];
        }

        return answer;
    }
}
```

**Time Complexity:** O(n) - Two passes  
**Space Complexity:** O(1) - Not counting output array

**Explanation:**

1. **First pass (left to right):** Store left products in answer
2. **Second pass (right to left):** Multiply by right products on-the-fly
3. Use running variable `rightProduct` instead of array
4. Most efficient solution

---

## Problem 2: Subarray Sum Equals K ⭐⭐⭐ (Medium)

### Problem Statement

Given an array of integers `nums` and an integer `k`, return the total number of **continuous subarrays** whose sum equals `k`.

### Example

```
Input: nums = [1,1,1], k = 2
Output: 2
Explanation: [1,1] and [1,1]

Input: nums = [1,2,3], k = 3
Output: 2
Explanation: [1,2] and [3]
```

---

### Solution 1: Brute Force (Not Optimal)

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        int count = 0;

        // Check all subarrays
        for (int start = 0; start < nums.Length; start++)
        {
            int sum = 0;
            for (int end = start; end < nums.Length; end++)
            {
                sum += nums[end];
                if (sum == k)
                {
                    count++;
                }
            }
        }

        return count;
    }
}
```

**Time Complexity:** O(n²) - Nested loops  
**Space Complexity:** O(1)

**Explanation:**

- Check every possible subarray
- Too slow for large inputs

---

### Solution 2: Prefix Sum with HashMap (Optimal)

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        var prefixSumCount = new Dictionary<int, int>();
        prefixSumCount[0] = 1;  // Important: empty prefix has sum 0

        int count = 0;
        int currentSum = 0;

        foreach (int num in nums)
        {
            currentSum += num;

            // Check if (currentSum - k) exists in map
            // This means there's a subarray with sum = k
            if (prefixSumCount.ContainsKey(currentSum - k))
            {
                count += prefixSumCount[currentSum - k];
            }

            // Add current prefix sum to map
            if (prefixSumCount.ContainsKey(currentSum))
            {
                prefixSumCount[currentSum]++;
            }
            else
            {
                prefixSumCount[currentSum] = 1;
            }
        }

        return count;
    }
}
```

**Time Complexity:** O(n) - Single pass  
**Space Complexity:** O(n) - HashMap storage

**Explanation:**

1. **Key insight:** If `prefixSum[j] - prefixSum[i] = k`, then subarray `[i+1..j]` sums to k
2. Rearranging: `prefixSum[i] = prefixSum[j] - k`
3. Store prefix sums in HashMap with their frequencies
4. For each position, check if `(currentSum - k)` exists
5. Initialize with `map[0] = 1` to handle subarrays starting at index 0

**Visual Example for nums=[1,1,1], k=2:**

```
Index:  0   1   2
nums:   1   1   1
prefix: 1   2   3

At index 0: currentSum=1, check for (1-2)=-1 → not found
At index 1: currentSum=2, check for (2-2)=0 → found! count=1
At index 2: currentSum=3, check for (3-2)=1 → found! count=2
```

---

### Solution 3: Cleaner Version with GetValueOrDefault

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        var map = new Dictionary<int, int> { [0] = 1 };
        int sum = 0, count = 0;

        foreach (int num in nums)
        {
            sum += num;
            count += map.GetValueOrDefault(sum - k, 0);
            map[sum] = map.GetValueOrDefault(sum, 0) + 1;
        }

        return count;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

- More concise using C# dictionary methods
- `GetValueOrDefault` eliminates ContainsKey checks

---

## Problem 3: Range Sum Query - Immutable ⭐ (Easy)

### Problem Statement

Given an integer array `nums`, handle multiple queries of the following type:

Calculate the **sum of the elements** of `nums` between indices `left` and `right` (inclusive).

Implement the `NumArray` class with:

- `NumArray(int[] nums)` - Initialize with the array
- `int SumRange(int left, int right)` - Return sum of elements between indices

### Example

```
Input:
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]

Output:
[null, 1, -1, -3]

Explanation:
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // -2 + 0 + 3 = 1
numArray.sumRange(2, 5); // 3 + (-5) + 2 + (-1) = -1
numArray.sumRange(0, 5); // -2 + 0 + 3 + (-5) + 2 + (-1) = -3
```

---

### Solution 1: Naive Approach (Not Optimal)

```csharp
public class NumArray
{
    private int[] nums;

    public NumArray(int[] nums)
    {
        this.nums = nums;
    }

    public int SumRange(int left, int right)
    {
        int sum = 0;
        for (int i = left; i <= right; i++)
        {
            sum += nums[i];
        }
        return sum;
    }
}
```

**Time Complexity:** O(n) per query  
**Space Complexity:** O(1)

**Explanation:**

- Recalculate sum for each query
- Inefficient if many queries

---

### Solution 2: Prefix Sum Array (Optimal)

```csharp
public class NumArray
{
    private int[] prefixSum;

    public NumArray(int[] nums)
    {
        int n = nums.Length;
        prefixSum = new int[n + 1];  // Extra space for easier calculation

        // Build prefix sum array
        // prefixSum[i] = sum of nums[0..i-1]
        for (int i = 0; i < n; i++)
        {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }
    }

    public int SumRange(int left, int right)
    {
        // Sum of nums[left..right] = prefixSum[right+1] - prefixSum[left]
        return prefixSum[right + 1] - prefixSum[left];
    }
}
```

**Time Complexity:**

- Constructor: O(n)
- Query: O(1)

**Space Complexity:** O(n) - Prefix sum array

**Explanation:**

1. **Build prefix sum:** `prefixSum[i]` = sum of first `i` elements
2. **Query formula:** `sum[left..right] = prefixSum[right+1] - prefixSum[left]`
3. Extra element at index 0 simplifies edge cases

**Visual Example for nums=[-2,0,3,-5,2,-1]:**

```
Index:      0   1   2   3   4   5   6
nums:          -2   0   3  -5   2  -1
prefixSum: [0, -2, -2,  1, -4, -2, -3]

sumRange(0,2) = prefixSum[3] - prefixSum[0] = 1 - 0 = 1
sumRange(2,5) = prefixSum[6] - prefixSum[2] = -3 - (-2) = -1
```

---

### Solution 3: Alternative Without Extra Space

```csharp
public class NumArray
{
    private int[] nums;

    public NumArray(int[] nums)
    {
        // Convert to prefix sum in-place
        for (int i = 1; i < nums.Length; i++)
        {
            nums[i] += nums[i - 1];
        }
        this.nums = nums;
    }

    public int SumRange(int left, int right)
    {
        if (left == 0)
            return nums[right];

        return nums[right] - nums[left - 1];
    }
}
```

**Time Complexity:** Same as Solution 2  
**Space Complexity:** O(1) - Modifies input array

**Explanation:**

- Saves space by modifying input array
- Must handle `left == 0` separately

---

## Key Takeaways

### 1. Prefix/Suffix Patterns

| Problem Type            | Pattern                  | Formula                               |
| ----------------------- | ------------------------ | ------------------------------------- |
| **Product except self** | Prefix × Suffix          | `result[i] = left[i] × right[i]`      |
| **Subarray sum = k**    | Prefix sum + HashMap     | Check if `(currentSum - k)` exists    |
| **Range sum queries**   | Prefix sum array         | `sum[l..r] = prefix[r+1] - prefix[l]` |
| **Max subarray**        | Running sum + min prefix | Kadane's or prefix min                |

### 2. Common Techniques

```csharp
// Prefix sum array (1-indexed for easier math)
int[] prefix = new int[n + 1];
for (int i = 0; i < n; i++)
    prefix[i + 1] = prefix[i] + nums[i];

// Range sum [left, right]
int sum = prefix[right + 1] - prefix[left];

// Prefix sum with HashMap (for subarray problems)
var map = new Dictionary<int, int> { [0] = 1 };
int sum = 0;
foreach (int num in nums)
{
    sum += num;
    if (map.ContainsKey(sum - k))
        count += map[sum - k];
    map[sum] = map.GetValueOrDefault(sum, 0) + 1;
}
```

### 3. Space Optimization Tricks

✅ **Use output array for prefix** (Product Except Self)  
✅ **Running variable instead of array** (Suffix products)  
✅ **HashMap for cumulative sums** (Subarray sum problems)  
✅ **Modify input array** (if allowed and space-constrained)

### 4. Interview Tips

✅ **Recognize the pattern:** "All elements except" → prefix/suffix  
✅ **Ask about constraints:** Can we modify input? Is extra space ok?  
✅ **Start with O(n) space:** Then optimize to O(1) if possible  
✅ **HashMap for sum problems:** Store cumulative sums for O(n) solution  
✅ **Don't forget edge cases:** Empty arrays, single element, all zeros

---

## Practice Problems

### Easy

1. **Range Sum Query - Immutable** ✓ (Covered above)
2. **Running Sum of 1D Array** - Basic prefix sum

### Medium

3. **Product of Array Except Self** ✓ (Covered above)
4. **Subarray Sum Equals K** ✓ (Covered above)
5. **Continuous Subarray Sum** - Multiple of k
6. **Subarray Sums Divisible by K** - Modulo arithmetic
7. **Maximum Subarray** (Kadane's) - DP with prefix pattern

### Hard

8. **Maximum Sum of 3 Non-Overlapping Subarrays** - Advanced prefix DP
9. **Shortest Subarray with Sum at Least K** - Deque optimization

---

## Common Mistakes to Avoid

❌ **Forgetting division constraint** - Product problems often ban division  
❌ **Not initializing map[0] = 1** - Needed for subarrays starting at index 0  
❌ **Off-by-one in prefix arrays** - Use n+1 size for cleaner indexing  
❌ **Modifying array during iteration** - Build prefix first, query later  
❌ **Not handling negative numbers** - Prefix patterns work with negatives too

---

## Time Complexity Summary

| Problem             | Brute Force    | Optimal        | Space  |
| ------------------- | -------------- | -------------- | ------ |
| Product Except Self | O(n²)          | O(n)           | O(1)\* |
| Subarray Sum = K    | O(n²)          | O(n)           | O(n)   |
| Range Sum Query     | O(n) per query | O(1) per query | O(n)   |

\*O(1) extra space not counting output array

---

## Next Steps

- ✅ Master prefix/suffix patterns
- 📚 Practice subarray sum variants
- 🎯 Learn Kadane's algorithm (max subarray)
- 💡 Recognize when HashMap can optimize to O(n)

**Remember:** Prefix patterns turn O(n²) problems into O(n) by trading space for time. The key insight is storing cumulative information!
