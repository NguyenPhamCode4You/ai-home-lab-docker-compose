# Day 2: Two Pointers & Sliding Window - Advanced Patterns

## Problem 1: Remove Duplicates from Sorted Array (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given an integer array `nums` sorted in non-decreasing order, remove duplicates in-place such that each unique element appears only once. Return the number of unique elements. The relative order must be maintained.

**Example:**

```
Input: nums = [1,1,2,2,3]
Output: 3, nums = [1,2,3,_,_]
Explanation: First 3 elements are unique
```

### Solution 1: Using Extra Array (Simple)

```csharp
public class Solution
{
    public int RemoveDuplicates(int[] nums)
    {
        if (nums.Length == 0) return 0;

        var unique = new List<int>();
        unique.Add(nums[0]);

        for (int i = 1; i < nums.Length; i++)
        {
            if (nums[i] != nums[i - 1])
            {
                unique.Add(nums[i]);
            }
        }

        // Copy back to original array
        for (int i = 0; i < unique.Count; i++)
        {
            nums[i] = unique[i];
        }

        return unique.Count;
    }
}
```

**Time Complexity:** O(n) - Single pass through array  
**Space Complexity:** O(n) - Extra list to store unique elements

**Explanation:**

- Create a list to store unique elements
- Compare each element with previous one
- If different, add to unique list
- Copy unique elements back to original array
- Simple but violates "in-place" requirement with extra space

### Solution 2: Two Pointers (Optimal)

```csharp
public class Solution
{
    public int RemoveDuplicates(int[] nums)
    {
        if (nums.Length == 0) return 0;

        // Slow pointer tracks position for next unique element
        int slow = 0;

        // Fast pointer scans through array
        for (int fast = 1; fast < nums.Length; fast++)
        {
            // Found a new unique element
            if (nums[fast] != nums[slow])
            {
                slow++;
                nums[slow] = nums[fast];
            }
        }

        return slow + 1; // Length of unique elements
    }
}
```

**Time Complexity:** O(n) - Single pass through array  
**Space Complexity:** O(1) - Only using two pointers

**Explanation:**

- Use two pointers: slow (write position) and fast (read position)
- Slow pointer marks where next unique element should go
- Fast pointer scans for unique elements
- When fast finds a unique element, copy it to slow+1 position
- This is true in-place modification with optimal space

---

## Problem 2: Container With Most Water (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

You are given an array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container that holds the most water.

**Example:**

```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: Lines at index 1 and 8 form container with area = 7 * 7 = 49
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int MaxArea(int[] height)
    {
        int maxArea = 0;

        // Try every pair of lines
        for (int i = 0; i < height.Length; i++)
        {
            for (int j = i + 1; j < height.Length; j++)
            {
                // Width between lines
                int width = j - i;

                // Height is limited by shorter line
                int h = Math.Min(height[i], height[j]);

                // Calculate area
                int area = width * h;
                maxArea = Math.Max(maxArea, area);
            }
        }

        return maxArea;
    }
}
```

**Time Complexity:** O(n²) - Check all pairs  
**Space Complexity:** O(1) - Only storing variables

**Explanation:**

- Try every possible pair of lines
- Area = width × height (height is minimum of two lines)
- Keep track of maximum area found
- Inefficient for large arrays

### Solution 2: Two Pointers (Optimal)

```csharp
public class Solution
{
    public int MaxArea(int[] height)
    {
        int left = 0;
        int right = height.Length - 1;
        int maxArea = 0;

        while (left < right)
        {
            // Calculate current area
            int width = right - left;
            int h = Math.Min(height[left], height[right]);
            int area = width * h;

            maxArea = Math.Max(maxArea, area);

            // Move pointer with shorter height
            // (moving the taller one can't possibly increase area)
            if (height[left] < height[right])
            {
                left++;
            }
            else
            {
                right--;
            }
        }

        return maxArea;
    }
}
```

**Time Complexity:** O(n) - Single pass with two pointers  
**Space Complexity:** O(1) - Only using two pointers

**Explanation:**

- Start with widest possible container (left=0, right=end)
- Calculate area with current pair
- Key insight: move the pointer with shorter height inward
  - Moving taller line can only decrease area (width decreases, height can't increase)
  - Moving shorter line might find a taller line, potentially increasing area
- Continue until pointers meet
- This greedy approach is optimal

---

## Problem 3: Minimum Window Substring (Hard)

**Difficulty:** ⭐⭐⭐ Hard

### Problem Statement

Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return an empty string.

**Example:**

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: "BANC" is the minimum window that contains all characters from t
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public string MinWindow(string s, string t)
    {
        if (s.Length < t.Length) return "";

        string result = "";
        int minLength = int.MaxValue;

        // Try every substring of s
        for (int i = 0; i < s.Length; i++)
        {
            for (int j = i; j < s.Length; j++)
            {
                string substring = s.Substring(i, j - i + 1);

                if (ContainsAll(substring, t) && substring.Length < minLength)
                {
                    minLength = substring.Length;
                    result = substring;
                }
            }
        }

        return result;
    }

    private bool ContainsAll(string s, string t)
    {
        var tCount = new Dictionary<char, int>();
        foreach (char c in t)
        {
            tCount[c] = tCount.GetValueOrDefault(c, 0) + 1;
        }

        var sCount = new Dictionary<char, int>();
        foreach (char c in s)
        {
            sCount[c] = sCount.GetValueOrDefault(c, 0) + 1;
        }

        foreach (var kvp in tCount)
        {
            if (!sCount.ContainsKey(kvp.Key) || sCount[kvp.Key] < kvp.Value)
            {
                return false;
            }
        }

        return true;
    }
}
```

**Time Complexity:** O(n³) - O(n²) substrings × O(n) validation  
**Space Complexity:** O(n) - Dictionaries for character counts

**Explanation:**

- Generate all possible substrings
- Check each substring if it contains all characters from t
- Track minimum valid substring
- Very inefficient, will timeout on large inputs

### Solution 2: Sliding Window with HashMap (Optimal)

```csharp
public class Solution
{
    public string MinWindow(string s, string t)
    {
        if (s.Length < t.Length) return "";

        // Count characters needed from t
        var tCount = new Dictionary<char, int>();
        foreach (char c in t)
        {
            tCount[c] = tCount.GetValueOrDefault(c, 0) + 1;
        }

        int required = tCount.Count; // Unique characters needed
        int formed = 0; // Unique characters in current window with desired frequency

        var windowCounts = new Dictionary<char, int>();
        int left = 0;
        int minLength = int.MaxValue;
        int minLeft = 0;

        for (int right = 0; right < s.Length; right++)
        {
            // Add character from right
            char c = s[right];
            windowCounts[c] = windowCounts.GetValueOrDefault(c, 0) + 1;

            // Check if this character's frequency matches requirement
            if (tCount.ContainsKey(c) && windowCounts[c] == tCount[c])
            {
                formed++;
            }

            // Try to contract window from left while valid
            while (left <= right && formed == required)
            {
                // Update result if this window is smaller
                if (right - left + 1 < minLength)
                {
                    minLength = right - left + 1;
                    minLeft = left;
                }

                // Remove character from left
                char leftChar = s[left];
                windowCounts[leftChar]--;

                if (tCount.ContainsKey(leftChar) &&
                    windowCounts[leftChar] < tCount[leftChar])
                {
                    formed--;
                }

                left++;
            }
        }

        return minLength == int.MaxValue ? "" : s.Substring(minLeft, minLength);
    }
}
```

**Time Complexity:** O(n + m) - where n = s.Length, m = t.Length  
**Space Complexity:** O(n + m) - Dictionaries for character counts

**Explanation:**

- Use sliding window technique with two pointers
- Expand window by moving right pointer until all characters from t are included
- Contract window from left while still valid, tracking minimum
- Use two dictionaries:
  - `tCount`: what we need
  - `windowCounts`: what we have in current window
- Track `formed`: how many unique characters have desired frequency
- When `formed == required`, we have a valid window
- This is optimal for this problem type

### Solution 3: Optimized with Array (Even Better for ASCII)

```csharp
public class Solution
{
    public string MinWindow(string s, string t)
    {
        if (s.Length < t.Length) return "";

        // Use arrays instead of dictionaries for better performance
        int[] tCount = new int[128]; // ASCII characters
        int[] windowCount = new int[128];

        int required = 0;
        foreach (char c in t)
        {
            if (tCount[c] == 0) required++;
            tCount[c]++;
        }

        int formed = 0;
        int left = 0;
        int minLength = int.MaxValue;
        int minLeft = 0;

        for (int right = 0; right < s.Length; right++)
        {
            char c = s[right];
            windowCount[c]++;

            if (tCount[c] > 0 && windowCount[c] == tCount[c])
            {
                formed++;
            }

            while (left <= right && formed == required)
            {
                if (right - left + 1 < minLength)
                {
                    minLength = right - left + 1;
                    minLeft = left;
                }

                char leftChar = s[left];
                windowCount[leftChar]--;

                if (tCount[leftChar] > 0 && windowCount[leftChar] < tCount[leftChar])
                {
                    formed--;
                }

                left++;
            }
        }

        return minLength == int.MaxValue ? "" : s.Substring(minLeft, minLength);
    }
}
```

**Time Complexity:** O(n + m) - Same as above  
**Space Complexity:** O(1) - Fixed size arrays (128 for ASCII)

**Explanation:**

- Same algorithm but using fixed-size arrays instead of dictionaries
- Arrays provide O(1) access without hashing overhead
- Works for ASCII characters (can extend to 256 for extended ASCII)
- Slightly faster in practice due to better cache locality
- Space is technically O(1) since array size doesn't grow with input

---

## Key Takeaways for Day 2

### Two Pointers Pattern

**When to use:**

- Array/string is sorted or can be sorted
- Need to find pairs that satisfy a condition
- Need to process from both ends

**Common variations:**

- **Opposite Directions:** Start from both ends, move toward center
- **Same Direction:** Both move forward, one faster (slow/fast)
- **Collision:** Move pointers until they meet

### Sliding Window Pattern

**When to use:**

- Find subarray/substring with certain properties
- Contiguous sequence of elements
- Optimization problems (min/max length)

**Types:**

- **Fixed Size:** Window size is constant
- **Variable Size:** Window expands and contracts based on conditions

**Template:**

```csharp
int left = 0;
for (int right = 0; right < array.Length; right++)
{
    // Expand window by including right element
    // Add array[right] to window state

    while (window_condition_violated)
    {
        // Contract window from left
        // Remove array[left] from window state
        left++;
    }

    // Update result based on current window [left, right]
}
```

### Big-O Analysis Tips

- **Two Pointers (opposite):** Usually O(n) - each element visited once
- **Sliding Window:** Usually O(n) - each element enters and leaves window once
- **Nested Loops:** Usually O(n²) - avoid if possible with two pointers

### Interview Strategy

1. **Recognize the pattern:**

   - Sorted array → Two pointers
   - Subarray/substring → Sliding window
   - Find pairs → Two pointers

2. **Start with brute force:**

   - Helps understand the problem
   - Shows logical thinking

3. **Optimize with pattern:**

   - Explain why two pointers/sliding window works
   - Draw diagrams to illustrate

4. **Edge cases to test:**
   - Empty array/string
   - Single element
   - All elements same
   - Already optimal/worst case

---

## Practice Patterns Summary

| Pattern        | Time  | Space | Use Case                |
| -------------- | ----- | ----- | ----------------------- |
| Brute Force    | O(n²) | O(1)  | Try all pairs/subarrays |
| Two Pointers   | O(n)  | O(1)  | Sorted data, find pairs |
| Sliding Window | O(n)  | O(k)  | Contiguous subarrays    |
| Hash Table     | O(n)  | O(n)  | Fast lookups needed     |

---

## Additional Practice Problems

1. **3Sum** (Medium) - Extension of two pointers
2. **Longest Repeating Character Replacement** (Medium) - Sliding window
3. **Trapping Rain Water** (Hard) - Two pointers
4. **Substring with Concatenation of All Words** (Hard) - Advanced sliding window

**Tomorrow:** Day 3 - Hash Tables & Sets (Advanced Hashing Techniques)
