# Day 1: Arrays & Strings - Fundamentals

## Problem 1: Two Sum (Easy)

**Difficulty:** ⭐ Easy

### Problem Statement

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example:**

```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int[] TwoSum(int[] nums, int target)
    {
        // Try every pair of numbers
        for (int i = 0; i < nums.Length; i++)
        {
            for (int j = i + 1; j < nums.Length; j++)
            {
                if (nums[i] + nums[j] == target)
                {
                    return new int[] { i, j };
                }
            }
        }

        throw new ArgumentException("No solution found");
    }
}
```

**Time Complexity:** O(n²) - We have nested loops iterating through the array  
**Space Complexity:** O(1) - Only using constant extra space

**Explanation:**

- We check every possible pair using two nested loops
- The outer loop fixes one number, inner loop checks all remaining numbers
- This is inefficient for large arrays but easy to understand

### Solution 2: Hash Table (Optimal)

```csharp
public class Solution
{
    public int[] TwoSum(int[] nums, int target)
    {
        // Dictionary to store: value -> index
        var map = new Dictionary<int, int>();

        for (int i = 0; i < nums.Length; i++)
        {
            int complement = target - nums[i];

            // Check if complement exists in our map
            if (map.ContainsKey(complement))
            {
                return new int[] { map[complement], i };
            }

            // Store current number and its index
            map[nums[i]] = i;
        }

        throw new ArgumentException("No solution found");
    }
}
```

**Time Complexity:** O(n) - Single pass through the array  
**Space Complexity:** O(n) - Dictionary can store up to n elements

**Explanation:**

- We trade space for time using a hash table
- For each number, we calculate what number we need (complement)
- If complement exists in our map, we found the answer
- Otherwise, we store current number for future lookups
- This is the optimal solution used in real interviews

---

## Problem 2: Valid Palindrome (Easy-Medium)

**Difficulty:** ⭐⭐ Easy-Medium

### Problem Statement

A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

**Example:**

```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome
```

### Solution 1: Clean and Compare (Simple)

```csharp
public class Solution
{
    public bool IsPalindrome(string s)
    {
        // Clean the string: keep only alphanumeric, convert to lowercase
        var cleaned = new StringBuilder();
        foreach (char c in s)
        {
            if (char.IsLetterOrDigit(c))
            {
                cleaned.Append(char.ToLower(c));
            }
        }

        string cleanedStr = cleaned.ToString();

        // Compare with its reverse
        string reversed = new string(cleanedStr.Reverse().ToArray());
        return cleanedStr == reversed;
    }
}
```

**Time Complexity:** O(n) - Process string once, reverse once, compare once  
**Space Complexity:** O(n) - Store cleaned string and reversed string

**Explanation:**

- First pass: clean the string (remove non-alphanumeric, lowercase)
- Create reversed version
- Compare the two strings
- Simple but uses extra space for reversed string

### Solution 2: Two Pointers (Optimal)

```csharp
public class Solution
{
    public bool IsPalindrome(string s)
    {
        int left = 0;
        int right = s.Length - 1;

        while (left < right)
        {
            // Skip non-alphanumeric characters from left
            while (left < right && !char.IsLetterOrDigit(s[left]))
            {
                left++;
            }

            // Skip non-alphanumeric characters from right
            while (left < right && !char.IsLetterOrDigit(s[right]))
            {
                right--;
            }

            // Compare characters (case-insensitive)
            if (char.ToLower(s[left]) != char.ToLower(s[right]))
            {
                return false;
            }

            left++;
            right--;
        }

        return true;
    }
}
```

**Time Complexity:** O(n) - Single pass through the string  
**Space Complexity:** O(1) - Only using two pointers, no extra space

**Explanation:**

- Use two pointers: one from start, one from end
- Skip invalid characters on both sides
- Compare valid characters directly without creating new strings
- Move pointers inward until they meet
- This is more efficient as it doesn't create extra strings

---

## Problem 3: Longest Substring Without Repeating Characters (Medium)

**Difficulty:** ⭐⭐⭐ Medium

### Problem Statement

Given a string `s`, find the length of the longest substring without repeating characters.

**Example:**

```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with length 3
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int LengthOfLongestSubstring(string s)
    {
        int maxLength = 0;

        // Try every possible substring
        for (int i = 0; i < s.Length; i++)
        {
            var seen = new HashSet<char>();

            for (int j = i; j < s.Length; j++)
            {
                // If character already seen, break
                if (seen.Contains(s[j]))
                {
                    break;
                }

                seen.Add(s[j]);
                maxLength = Math.Max(maxLength, seen.Count);
            }
        }

        return maxLength;
    }
}
```

**Time Complexity:** O(n²) - For each position, check substring from that position  
**Space Complexity:** O(min(n, m)) - HashSet size limited by string length or charset size

**Explanation:**

- For each starting position, try to extend the substring
- Use HashSet to track characters in current substring
- Stop when we encounter a duplicate
- Update maximum length found
- This checks many overlapping substrings unnecessarily

### Solution 2: Sliding Window with Hash Set (Better)

```csharp
public class Solution
{
    public int LengthOfLongestSubstring(string s)
    {
        var charSet = new HashSet<char>();
        int left = 0;
        int maxLength = 0;

        for (int right = 0; right < s.Length; right++)
        {
            // Remove characters from left until no duplicate
            while (charSet.Contains(s[right]))
            {
                charSet.Remove(s[left]);
                left++;
            }

            // Add current character
            charSet.Add(s[right]);

            // Update maximum length
            maxLength = Math.Max(maxLength, right - left + 1);
        }

        return maxLength;
    }
}
```

**Time Complexity:** O(n) - Each character visited at most twice (once by right, once by left)  
**Space Complexity:** O(min(n, m)) - HashSet size limited by string length or charset size

**Explanation:**

- Use sliding window technique with two pointers
- Expand window by moving right pointer
- When duplicate found, shrink from left until duplicate removed
- Track maximum window size seen
- Each character added/removed at most once

### Solution 3: Sliding Window with Dictionary (Optimal)

```csharp
public class Solution
{
    public int LengthOfLongestSubstring(string s)
    {
        // Dictionary stores: character -> last seen index
        var charIndex = new Dictionary<char, int>();
        int left = 0;
        int maxLength = 0;

        for (int right = 0; right < s.Length; right++)
        {
            char currentChar = s[right];

            // If character seen and within current window
            if (charIndex.ContainsKey(currentChar) && charIndex[currentChar] >= left)
            {
                // Move left pointer past the duplicate
                left = charIndex[currentChar] + 1;
            }

            // Update character's last seen index
            charIndex[currentChar] = right;

            // Update maximum length
            maxLength = Math.Max(maxLength, right - left + 1);
        }

        return maxLength;
    }
}
```

**Time Complexity:** O(n) - Single pass through the string  
**Space Complexity:** O(min(n, m)) - Dictionary size limited by string length or charset size

**Explanation:**

- Improved sliding window using dictionary to store last index
- When duplicate found, jump left pointer directly past previous occurrence
- No need to remove characters one by one
- This is the most efficient solution with single pass
- Uses dictionary to track positions for O(1) lookup and jump

---

## Key Takeaways for Day 1

### Big-O Notation Basics

- **O(1)** - Constant: Operation takes same time regardless of input size
- **O(n)** - Linear: Time grows proportionally with input size
- **O(n²)** - Quadratic: Time grows with square of input size (nested loops)
- **O(log n)** - Logarithmic: Time grows slowly (binary search, trees)

### Interview Tips

1. **Always start with brute force** - Show you understand the problem
2. **Discuss trade-offs** - Time vs Space complexity
3. **Optimize incrementally** - Don't jump to optimal solution immediately
4. **Test edge cases** - Empty arrays, single elements, duplicates
5. **Communication is key** - Explain your thinking process

### Common Patterns Learned

- **Hash Table/Dictionary** - Trade space for time, O(1) lookups
- **Two Pointers** - Process from both ends or track window, save space
- **Sliding Window** - Expand and contract to find optimal subarray/substring

### Practice Tips

- Implement all three solutions for each problem
- Time yourself (45 minutes per problem maximum in interview)
- Practice explaining solutions out loud
- Write test cases before coding
- Consider edge cases: null, empty, single element, all same elements

---

## Additional Practice Problems

Try these similar problems to reinforce today's concepts:

1. **Contains Duplicate** (Easy) - Use HashSet
2. **Valid Anagram** (Easy) - Use Dictionary/array counting
3. **Group Anagrams** (Medium) - Combine hashing with sorting
4. **Minimum Window Substring** (Hard) - Advanced sliding window

**Tomorrow:** Day 2 - Two Pointers & Sliding Window (Advanced Patterns)
