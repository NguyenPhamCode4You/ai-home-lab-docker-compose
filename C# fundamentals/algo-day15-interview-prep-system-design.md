# Day 15: Interview Preparation & System Design

## Problem 1: Design Twitter (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Design a simplified Twitter with `postTweet`, `getNewsFeed`, `follow`, and `unfollow` methods.

**Requirements:**

- `postTweet(userId, tweetId)`: Create a tweet
- `getNewsFeed(userId)`: Return 10 most recent tweets from user's followed users (including self)
- `follow(followerId, followeeId)`: Follower follows followee
- `unfollow(followerId, followeeId)`: Follower unfollows followee

### Solution: Hash Tables + Merge K Sorted Lists

```csharp
public class Twitter
{
    private class Tweet
    {
        public int Id;
        public int Timestamp;
        public Tweet Next;

        public Tweet(int id, int timestamp)
        {
            Id = id;
            Timestamp = timestamp;
        }
    }

    private Dictionary<int, HashSet<int>> following; // userId -> followees
    private Dictionary<int, Tweet> tweets; // userId -> linked list of tweets
    private int timestamp;

    public Twitter()
    {
        following = new Dictionary<int, HashSet<int>>();
        tweets = new Dictionary<int, Tweet>();
        timestamp = 0;
    }

    public void PostTweet(int userId, int tweetId)
    {
        var tweet = new Tweet(tweetId, timestamp++);

        if (!tweets.ContainsKey(userId))
        {
            tweets[userId] = tweet;
        }
        else
        {
            tweet.Next = tweets[userId];
            tweets[userId] = tweet;
        }
    }

    public IList<int> GetNewsFeed(int userId)
    {
        // Max heap by timestamp
        var heap = new PriorityQueue<Tweet, int>();

        // Add user's own tweets
        if (tweets.ContainsKey(userId))
        {
            heap.Enqueue(tweets[userId], -tweets[userId].Timestamp);
        }

        // Add followed users' tweets
        if (following.ContainsKey(userId))
        {
            foreach (int followeeId in following[userId])
            {
                if (tweets.ContainsKey(followeeId))
                {
                    heap.Enqueue(tweets[followeeId], -tweets[followeeId].Timestamp);
                }
            }
        }

        // Extract top 10
        var result = new List<int>();
        while (result.Count < 10 && heap.Count > 0)
        {
            var tweet = heap.Dequeue();
            result.Add(tweet.Id);

            if (tweet.Next != null)
            {
                heap.Enqueue(tweet.Next, -tweet.Next.Timestamp);
            }
        }

        return result;
    }

    public void Follow(int followerId, int followeeId)
    {
        if (followerId == followeeId) return;

        if (!following.ContainsKey(followerId))
        {
            following[followerId] = new HashSet<int>();
        }
        following[followerId].Add(followeeId);
    }

    public void Unfollow(int followerId, int followeeId)
    {
        if (following.ContainsKey(followerId))
        {
            following[followerId].Remove(followeeId);
        }
    }
}
```

**Time Complexity:**

- `postTweet`: O(1)
- `getNewsFeed`: O(n log k) - n = followed users, k = 10
- `follow/unfollow`: O(1)

**Space Complexity:** O(users + tweets)

**Explanation:**

- Store tweets as linked lists (most recent first)
- Use hash set for follower relationships
- Merge K sorted lists (tweets from followed users) using heap
- Demonstrates multiple data structures working together

---

## Problem 2: Design Search Autocomplete System (Hard)

**Difficulty:** ⭐⭐⭐ Hard

### Problem Statement

Design a search autocomplete system that returns top 3 historical hot sentences based on input prefix.

### Solution: Trie + Priority Queue

```csharp
public class AutocompleteSystem
{
    private class TrieNode
    {
        public Dictionary<char, TrieNode> Children = new Dictionary<char, TrieNode>();
        public Dictionary<string, int> Sentences = new Dictionary<string, int>();
    }

    private TrieNode root;
    private TrieNode currentNode;
    private StringBuilder currentInput;

    public AutocompleteSystem(string[] sentences, int[] times)
    {
        root = new TrieNode();
        currentNode = root;
        currentInput = new StringBuilder();

        // Build initial trie
        for (int i = 0; i < sentences.Length; i++)
        {
            AddSentence(sentences[i], times[i]);
        }
    }

    public IList<string> Input(char c)
    {
        if (c == '#')
        {
            // Save current sentence
            string sentence = currentInput.ToString();
            AddSentence(sentence, 1);

            // Reset
            currentInput.Clear();
            currentNode = root;
            return new List<string>();
        }

        currentInput.Append(c);

        // Move to next node
        if (!currentNode.Children.ContainsKey(c))
        {
            currentNode.Children[c] = new TrieNode();
        }
        currentNode = currentNode.Children[c];

        // Get top 3 sentences
        var pq = new PriorityQueue<string, (int, string)>();

        foreach (var kvp in currentNode.Sentences)
        {
            // Sort by frequency (desc), then lexicographically (asc)
            pq.Enqueue(kvp.Key, (-kvp.Value, kvp.Key));
        }

        var result = new List<string>();
        while (result.Count < 3 && pq.Count > 0)
        {
            result.Add(pq.Dequeue());
        }

        return result;
    }

    private void AddSentence(string sentence, int count)
    {
        TrieNode node = root;

        foreach (char c in sentence)
        {
            if (!node.Children.ContainsKey(c))
            {
                node.Children[c] = new TrieNode();
            }
            node = node.Children[c];

            // Update sentence count at each node
            node.Sentences[sentence] = node.Sentences.GetValueOrDefault(sentence, 0) + count;
        }
    }
}
```

**Explanation:**

- Trie stores all prefixes
- Each node stores complete sentences passing through
- Priority queue sorts by frequency then lexicographically
- Real-world application of tries

---

## Problem 3: Rate Limiter Design (System Design)

**Difficulty:** ⭐⭐⭐ System Design

### Problem Statement

Design a rate limiter that allows at most N requests per time window.

### Solution: Sliding Window with Queue

```csharp
public class RateLimiter
{
    private Queue<long> requestTimes;
    private int maxRequests;
    private long windowMs;

    public RateLimiter(int maxRequests, long windowMs)
    {
        this.requestTimes = new Queue<long>();
        this.maxRequests = maxRequests;
        this.windowMs = windowMs;
    }

    public bool AllowRequest()
    {
        long now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

        // Remove old requests outside window
        while (requestTimes.Count > 0 && now - requestTimes.Peek() >= windowMs)
        {
            requestTimes.Dequeue();
        }

        // Check if we can accept request
        if (requestTimes.Count < maxRequests)
        {
            requestTimes.Enqueue(now);
            return true;
        }

        return false;
    }
}
```

**Time Complexity:** O(n) worst case, O(1) amortized  
**Space Complexity:** O(n)

**Alternative: Token Bucket Algorithm**

```csharp
public class TokenBucketRateLimiter
{
    private int tokens;
    private int capacity;
    private int refillRate; // tokens per second
    private long lastRefill;

    public TokenBucketRateLimiter(int capacity, int refillRate)
    {
        this.tokens = capacity;
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.lastRefill = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
    }

    public bool AllowRequest()
    {
        Refill();

        if (tokens > 0)
        {
            tokens--;
            return true;
        }

        return false;
    }

    private void Refill()
    {
        long now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        long elapsed = now - lastRefill;

        int tokensToAdd = (int)(elapsed * refillRate);
        tokens = Math.Min(capacity, tokens + tokensToAdd);

        if (tokensToAdd > 0)
        {
            lastRefill = now;
        }
    }
}
```

---

## Complete Interview Strategy Guide

### Before the Interview

**1. Clarify Requirements (2-3 minutes)**

- Ask about input constraints (size, range, type)
- Clarify edge cases
- Understand expected output format
- Ask about time/space requirements

**Example questions:**

- "Can the array be empty?"
- "Are there duplicate elements?"
- "What's the maximum array size?"
- "Should I optimize for time or space?"

**2. Think Out Loud (1-2 minutes)**

- Explain your initial thoughts
- Discuss potential approaches
- Mention trade-offs

**3. Start with Brute Force (2-3 minutes)**

- Explain simplest solution
- Analyze complexity
- Shows you can solve it, even if not optimal

**4. Optimize (3-5 minutes)**

- Identify bottlenecks
- Apply patterns (hash table, two pointers, etc.)
- Explain why optimization works

**5. Code (10-15 minutes)**

- Write clean, readable code
- Use meaningful variable names
- Add comments for complex parts

**6. Test (3-5 minutes)**

- Walk through with example
- Test edge cases
- Fix bugs calmly

**7. Discuss Further Optimization (2-3 minutes)**

- Space vs time trade-offs
- Handle even larger inputs
- Distributed systems (for system design)

### The STAR Method for Behavioral Questions

**Situation:** Describe context  
**Task:** Explain challenge  
**Action:** What you did  
**Result:** Outcome and learnings

### Common Interview Pitfalls

❌ **Don't:**

- Jump into coding immediately
- Stay silent while thinking
- Give up when stuck
- Argue with interviewer
- Ignore edge cases

✅ **Do:**

- Ask clarifying questions
- Think out loud
- Start with working solution
- Test your code
- Stay calm and positive

---

## Algorithm Complexity Reference

### Time Complexity Ranking (Best to Worst)

1. O(1) - Constant
2. O(log n) - Logarithmic
3. O(n) - Linear
4. O(n log n) - Linearithmic
5. O(n²) - Quadratic
6. O(n³) - Cubic
7. O(2ⁿ) - Exponential
8. O(n!) - Factorial

### For n = 1,000,000:

- O(1): 1 operation
- O(log n): ~20 operations
- O(n): 1,000,000 operations
- O(n log n): ~20,000,000 operations
- O(n²): 1,000,000,000,000 operations (too slow!)

---

## Final Checklist for Big Tech Interviews

### Data Structures Mastery

- ✅ Arrays & Strings
- ✅ Hash Tables & Sets
- ✅ Linked Lists
- ✅ Stacks & Queues
- ✅ Trees (Binary, BST)
- ✅ Graphs
- ✅ Heaps
- ✅ Tries
- ✅ Union-Find (optional)

### Algorithm Patterns

- ✅ Two Pointers
- ✅ Sliding Window
- ✅ Binary Search
- ✅ DFS & BFS
- ✅ Dynamic Programming
- ✅ Backtracking
- ✅ Greedy
- ✅ Divide & Conquer

### Problem-Solving Skills

- ✅ Time/Space complexity analysis
- ✅ Optimization techniques
- ✅ Edge case handling
- ✅ Code clarity and style
- ✅ Testing and debugging
- ✅ Communication skills

### Company-Specific Preparation

- **Google:** Focus on algorithms, system design
- **Microsoft:** Balanced approach, OOP design
- **Amazon:** Leadership principles, scalability
- **Meta:** Product thinking, optimization
- **Apple:** Low-level programming, design patterns

### Resources for Continued Practice

- **LeetCode:** 200+ problems (Easy: 40, Medium: 120, Hard: 40)
- **Mock Interviews:** Practice with peers or Pramp
- **System Design:** "Designing Data-Intensive Applications"
- **Behavioral:** Prepare STAR stories

---

## Congratulations! 🎉

You've completed a comprehensive 15-day algorithm interview preparation course in C#. You've learned:

- **45 problems** from easy to hard
- **Core patterns** used in 80% of interview questions
- **Multiple solutions** for each problem (brute force to optimal)
- **Big-O analysis** for every solution
- **Interview strategies** and communication tips

### Next Steps

1. **Review** problems you found difficult
2. **Practice** 2-3 problems daily on LeetCode
3. **Mock interviews** to build confidence
4. **System design** if interviewing for senior roles
5. **Stay consistent** - algorithms are a skill, not talent

### Remember

- **Interviews are learnable skills**
- **Communication > Perfect Code**
- **Process matters more than final answer**
- **Every interview is practice**
- **You've got this!** 💪

Good luck with your interviews! 🚀
