# Day 3: Hash Tables & Sets - Advanced Hashing Techniques

## Problem 1: Group Anagrams (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given an array of strings `strs`, group the anagrams together. An anagram is a word formed by rearranging the letters of another word.

**Example:**

```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

### Solution 1: Sorting as Key (Simple)

```csharp
public class Solution
{
    public IList<IList<string>> GroupAnagrams(string[] strs)
    {
        // Dictionary: sorted string -> list of anagrams
        var groups = new Dictionary<string, List<string>>();

        foreach (string str in strs)
        {
            // Sort characters to create key
            char[] chars = str.ToCharArray();
            Array.Sort(chars);
            string key = new string(chars);

            // Add to appropriate group
            if (!groups.ContainsKey(key))
            {
                groups[key] = new List<string>();
            }
            groups[key].Add(str);
        }

        // Convert to required return type
        return groups.Values.ToList<IList<string>>();
    }
}
```

**Time Complexity:** O(n × k log k) - n strings, each of length k sorted  
**Space Complexity:** O(n × k) - Store all strings in dictionary

**Explanation:**

- Anagrams have same characters, so sorting produces same string
- Use sorted string as dictionary key
- Group all strings with same key together
- Simple and intuitive approach

### Solution 2: Character Count as Key (Optimal)

```csharp
public class Solution
{
    public IList<IList<string>> GroupAnagrams(string[] strs)
    {
        var groups = new Dictionary<string, List<string>>();

        foreach (string str in strs)
        {
            // Create key from character counts
            int[] count = new int[26]; // a-z
            foreach (char c in str)
            {
                count[c - 'a']++;
            }

            // Convert count array to string key
            // Format: "1#0#2#..." where numbers are counts
            var keyBuilder = new StringBuilder();
            for (int i = 0; i < 26; i++)
            {
                keyBuilder.Append(count[i]);
                keyBuilder.Append('#');
            }
            string key = keyBuilder.ToString();

            if (!groups.ContainsKey(key))
            {
                groups[key] = new List<string>();
            }
            groups[key].Add(str);
        }

        return groups.Values.ToList<IList<string>>();
    }
}
```

**Time Complexity:** O(n × k) - n strings, each of length k counted  
**Space Complexity:** O(n × k) - Store all strings in dictionary

**Explanation:**

- Instead of sorting, count character frequencies
- Create unique key from character counts
- Faster than sorting for longer strings
- O(k) to count vs O(k log k) to sort
- This is optimal for this problem

---

## Problem 2: Longest Consecutive Sequence (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.

**Example:**

```
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: Longest sequence is [1,2,3,4]
```

### Solution 1: Sorting (Simple)

```csharp
public class Solution
{
    public int LongestConsecutive(int[] nums)
    {
        if (nums.Length == 0) return 0;

        Array.Sort(nums);

        int maxLength = 1;
        int currentLength = 1;

        for (int i = 1; i < nums.Length; i++)
        {
            // Skip duplicates
            if (nums[i] == nums[i - 1])
            {
                continue;
            }

            // Check if consecutive
            if (nums[i] == nums[i - 1] + 1)
            {
                currentLength++;
            }
            else
            {
                maxLength = Math.Max(maxLength, currentLength);
                currentLength = 1;
            }
        }

        return Math.Max(maxLength, currentLength);
    }
}
```

**Time Complexity:** O(n log n) - Dominated by sorting  
**Space Complexity:** O(1) - In-place sorting (or O(n) if sorting creates new array)

**Explanation:**

- Sort array first
- Scan for consecutive numbers
- Track current and maximum sequence length
- Simple but doesn't meet O(n) requirement

### Solution 2: HashSet (Optimal)

```csharp
public class Solution
{
    public int LongestConsecutive(int[] nums)
    {
        if (nums.Length == 0) return 0;

        // Put all numbers in HashSet for O(1) lookup
        var numSet = new HashSet<int>(nums);
        int maxLength = 0;

        foreach (int num in numSet)
        {
            // Only start sequence from the beginning
            // If num-1 exists, this isn't the start
            if (!numSet.Contains(num - 1))
            {
                int currentNum = num;
                int currentLength = 1;

                // Count consecutive numbers
                while (numSet.Contains(currentNum + 1))
                {
                    currentNum++;
                    currentLength++;
                }

                maxLength = Math.Max(maxLength, currentLength);
            }
        }

        return maxLength;
    }
}
```

**Time Complexity:** O(n) - Each number visited at most twice  
**Space Complexity:** O(n) - HashSet stores all numbers

**Explanation:**

- Store all numbers in HashSet for O(1) lookups
- Key insight: only start counting from sequence starts
- A number is a sequence start if (number - 1) doesn't exist
- From each start, count consecutive numbers
- Each number enters HashSet once, checked as potential start once, and counted once in a sequence
- Achieves O(n) time requirement using smart HashSet usage

---

## Problem 3: Subarray Sum Equals K (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`.

**Example:**

```
Input: nums = [1,1,1], k = 2
Output: 2
Explanation: [1,1] appears twice
```

### Solution 1: Brute Force (Simple)

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        int count = 0;

        // Try every subarray
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

**Time Complexity:** O(n²) - Check all subarrays  
**Space Complexity:** O(1) - Only counters

**Explanation:**

- Try every possible subarray
- Calculate sum for each subarray
- Count those equal to k
- Straightforward but slow for large arrays

### Solution 2: Cumulative Sum with HashMap (Optimal)

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        // Dictionary: cumulative sum -> frequency
        var sumCount = new Dictionary<int, int>();
        sumCount[0] = 1; // Empty subarray has sum 0

        int cumulativeSum = 0;
        int count = 0;

        foreach (int num in nums)
        {
            cumulativeSum += num;

            // Check if there's a previous sum such that
            // cumulativeSum - previousSum = k
            // Which means: previousSum = cumulativeSum - k
            int target = cumulativeSum - k;

            if (sumCount.ContainsKey(target))
            {
                count += sumCount[target];
            }

            // Add current cumulative sum to map
            sumCount[cumulativeSum] = sumCount.GetValueOrDefault(cumulativeSum, 0) + 1;
        }

        return count;
    }
}
```

**Time Complexity:** O(n) - Single pass through array  
**Space Complexity:** O(n) - Dictionary can store up to n sums

**Explanation:**

- Key insight: if sum[0...j] - sum[0...i] = k, then sum[i+1...j] = k
- Use cumulative sum: sum from start to current position
- Store frequency of each cumulative sum in dictionary
- For current sum, check if (currentSum - k) exists
- If yes, those are valid subarrays ending at current position
- This technique is called "prefix sum with hash map"

### Detailed Example Walkthrough

```
nums = [1, 2, 3], k = 3
Initialize: sumCount = {0: 1}, cumulativeSum = 0, count = 0

i=0, num=1:
  cumulativeSum = 1
  target = 1 - 3 = -2 (not in map)
  sumCount = {0: 1, 1: 1}

i=1, num=2:
  cumulativeSum = 3
  target = 3 - 3 = 0 (found! count += 1)
  sumCount = {0: 1, 1: 1, 3: 1}
  (subarray [1,2] has sum 3)

i=2, num=3:
  cumulativeSum = 6
  target = 6 - 3 = 3 (found! count += 1)
  sumCount = {0: 1, 1: 1, 3: 1, 6: 1}
  (subarray [3] has sum 3)

Result: count = 2
```

### Solution 3: With Detailed Comments (Learning Version)

```csharp
public class Solution
{
    public int SubarraySum(int[] nums, int k)
    {
        // This map stores: sum -> how many times we've seen this sum
        // Key concept: if we've seen sum S before, and now we see sum S+k,
        // it means there's a subarray with sum k between those positions
        var prefixSumCount = new Dictionary<int, int>();

        // Base case: sum 0 appears once (before any elements)
        // This handles subarrays starting from index 0
        prefixSumCount[0] = 1;

        int runningSum = 0; // Cumulative sum from start to current position
        int result = 0;     // Count of subarrays with sum k

        for (int i = 0; i < nums.Length; i++)
        {
            // Add current element to running sum
            runningSum += nums[i];

            // Mathematical insight:
            // If runningSum - previousSum = k
            // Then previousSum = runningSum - k
            //
            // If we've seen (runningSum - k) before, it means there are
            // subarrays ending at current position with sum k
            int complement = runningSum - k;

            if (prefixSumCount.ContainsKey(complement))
            {
                // Add count of times we've seen the complement
                // Each occurrence represents one valid subarray
                result += prefixSumCount[complement];
            }

            // Record current running sum for future use
            prefixSumCount[runningSum] =
                prefixSumCount.GetValueOrDefault(runningSum, 0) + 1;
        }

        return result;
    }
}
```

**Time Complexity:** O(n) - Single pass with O(1) dictionary operations  
**Space Complexity:** O(n) - Dictionary size proportional to array size

---

## Key Takeaways for Day 3

### Hash Table Design Patterns

#### 1. **Frequency Counter Pattern**

```csharp
var frequency = new Dictionary<T, int>();
foreach (var item in collection)
{
    frequency[item] = frequency.GetValueOrDefault(item, 0) + 1;
}
```

**Use for:** Counting occurrences, finding duplicates, anagrams

#### 2. **Lookup/Existence Pattern**

```csharp
var seen = new HashSet<T>(collection);
if (seen.Contains(target)) { /* ... */ }
```

**Use for:** Fast membership testing, finding complements

#### 3. **Grouping Pattern**

```csharp
var groups = new Dictionary<TKey, List<TValue>>();
foreach (var item in collection)
{
    var key = GetKey(item);
    if (!groups.ContainsKey(key))
        groups[key] = new List<TValue>();
    groups[key].Add(item);
}
```

**Use for:** Grouping by criteria, categorizing data

#### 4. **Prefix Sum Pattern**

```csharp
var prefixSums = new Dictionary<int, int>();
prefixSums[0] = 1;
int sum = 0;
foreach (var num in nums)
{
    sum += num;
    // Use (sum - target) to find subarrays
}
```

**Use for:** Subarray sum problems, range queries

### Dictionary vs HashSet in C#

| Feature  | Dictionary<TKey, TValue> | HashSet<T>                 |
| -------- | ------------------------ | -------------------------- |
| Stores   | Key-value pairs          | Unique values only         |
| Lookup   | O(1) by key              | O(1) membership test       |
| Use when | Need associated data     | Only need presence/absence |
| Memory   | More (stores values)     | Less (just keys)           |

### Common Hash Table Tricks

1. **Using Sorted String as Key**

   - For anagrams: sort characters
   - Time: O(k log k) per string

2. **Character Count as Key**

   - For anagrams: count array/string
   - Time: O(k) per string, faster than sorting

3. **Cumulative Sum + HashMap**

   - For subarray problems
   - Track sum -> frequency or sum -> index

4. **Two-Pass vs One-Pass**
   - Two-pass: Build hash table first, then query
   - One-pass: Build and query simultaneously
   - One-pass usually possible and optimal

### Big-O with Hash Tables

- **Average Case:** O(1) insert, lookup, delete
- **Worst Case:** O(n) if many collisions (rare with good hash function)
- **Space:** Always O(n) to store n items
- **When to use:** Need fast lookups/insertions, can afford O(n) space

### Interview Tips

1. **Recognize hash table opportunities:**

   - "Find pair/group that..."
   - "Count frequency of..."
   - "Check if exists..."
   - Subarray/substring sum problems

2. **Choose right data structure:**

   - Need counts? → Dictionary<T, int>
   - Just existence? → HashSet<T>
   - Need order? → Consider SortedDictionary (O(log n))

3. **Common mistakes to avoid:**

   - Forgetting to initialize dictionary entries
   - Not handling duplicate keys
   - Inefficient key generation (e.g., string concatenation in loop)

4. **Optimization techniques:**
   - Use StringBuilder for building string keys
   - Use arrays instead of dictionaries when key space is small (e.g., 26 letters)
   - Consider hash table vs sorting trade-off

---

## Additional Practice Problems

1. **Top K Frequent Elements** (Medium) - Heap + Hash table
2. **4Sum II** (Medium) - Multiple hash tables
3. **Valid Sudoku** (Medium) - Hash set for validation
4. **Ransom Note** (Easy) - Character frequency
5. **Isomorphic Strings** (Easy) - Bidirectional mapping

**Tomorrow:** Day 4 - Sorting & Searching (Binary Search & Sort Algorithms)
