# Day 14: Advanced Data Structures

## Problem 1: LRU Cache (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Design a Least Recently Used (LRU) cache with `get` and `put` operations, both in O(1) time.

**Example:**

```
LRUCache cache = new LRUCache(2); // capacity = 2
cache.Put(1, 1);
cache.Put(2, 2);
cache.Get(1);       // returns 1
cache.Put(3, 3);    // evicts key 2
cache.Get(2);       // returns -1 (not found)
```

### Solution: HashMap + Doubly Linked List

```csharp
public class LRUCache
{
    private class Node
    {
        public int Key;
        public int Value;
        public Node Prev;
        public Node Next;

        public Node(int key, int value)
        {
            Key = key;
            Value = value;
        }
    }

    private Dictionary<int, Node> cache;
    private int capacity;
    private Node head; // Most recent
    private Node tail; // Least recent

    public LRUCache(int capacity)
    {
        this.capacity = capacity;
        cache = new Dictionary<int, Node>();

        // Dummy head and tail
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.Next = tail;
        tail.Prev = head;
    }

    public int Get(int key)
    {
        if (!cache.ContainsKey(key))
        {
            return -1;
        }

        Node node = cache[key];
        MoveToHead(node);
        return node.Value;
    }

    public void Put(int key, int value)
    {
        if (cache.ContainsKey(key))
        {
            Node node = cache[key];
            node.Value = value;
            MoveToHead(node);
        }
        else
        {
            Node newNode = new Node(key, value);
            cache[key] = newNode;
            AddToHead(newNode);

            if (cache.Count > capacity)
            {
                Node lru = RemoveTail();
                cache.Remove(lru.Key);
            }
        }
    }

    private void AddToHead(Node node)
    {
        node.Next = head.Next;
        node.Prev = head;
        head.Next.Prev = node;
        head.Next = node;
    }

    private void RemoveNode(Node node)
    {
        node.Prev.Next = node.Next;
        node.Next.Prev = node.Prev;
    }

    private void MoveToHead(Node node)
    {
        RemoveNode(node);
        AddToHead(node);
    }

    private Node RemoveTail()
    {
        Node lru = tail.Prev;
        RemoveNode(lru);
        return lru;
    }
}
```

**Time Complexity:** O(1) for both get and put  
**Space Complexity:** O(capacity)

**Explanation:**

- HashMap for O(1) access to nodes
- Doubly linked list to track access order
- Most recent at head, least recent at tail
- Move accessed nodes to head
- Evict from tail when capacity exceeded

---

## Problem 2: Implement Trie (Prefix Tree) (Medium)

**Difficulty:** ⭐⭐ Medium

### Problem Statement

Implement a trie with `insert`, `search`, and `startsWith` methods.

**Example:**

```
Trie trie = new Trie();
trie.Insert("apple");
trie.Search("apple");   // returns true
trie.Search("app");     // returns false
trie.StartsWith("app"); // returns true
```

### Solution: Trie Implementation

```csharp
public class Trie
{
    private class TrieNode
    {
        public Dictionary<char, TrieNode> Children;
        public bool IsEndOfWord;

        public TrieNode()
        {
            Children = new Dictionary<char, TrieNode>();
            IsEndOfWord = false;
        }
    }

    private TrieNode root;

    public Trie()
    {
        root = new TrieNode();
    }

    public void Insert(string word)
    {
        TrieNode current = root;

        foreach (char c in word)
        {
            if (!current.Children.ContainsKey(c))
            {
                current.Children[c] = new TrieNode();
            }
            current = current.Children[c];
        }

        current.IsEndOfWord = true;
    }

    public bool Search(string word)
    {
        TrieNode node = SearchNode(word);
        return node != null && node.IsEndOfWord;
    }

    public bool StartsWith(string prefix)
    {
        return SearchNode(prefix) != null;
    }

    private TrieNode SearchNode(string str)
    {
        TrieNode current = root;

        foreach (char c in str)
        {
            if (!current.Children.ContainsKey(c))
            {
                return null;
            }
            current = current.Children[c];
        }

        return current;
    }
}
```

**Time Complexity:** O(m) where m = word length  
**Space Complexity:** O(n × m) - n words of average length m

**Explanation:**

- Tree where each node represents a character
- Path from root to node forms a word/prefix
- Efficient for autocomplete, spell check
- Better than hash table for prefix queries

---

## Problem 3: Top K Frequent Elements (Medium-Hard)

**Difficulty:** ⭐⭐⭐ Medium-Hard

### Problem Statement

Given an integer array and an integer k, return the k most frequent elements.

**Example:**

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

### Solution 1: Heap (Priority Queue)

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

        // Min heap of size k
        var minHeap = new PriorityQueue<int, int>();

        foreach (var kvp in freqMap)
        {
            minHeap.Enqueue(kvp.Key, kvp.Value);

            if (minHeap.Count > k)
            {
                minHeap.Dequeue();
            }
        }

        // Extract elements from heap
        int[] result = new int[k];
        for (int i = 0; i < k; i++)
        {
            result[i] = minHeap.Dequeue();
        }

        return result;
    }
}
```

**Time Complexity:** O(n log k)  
**Space Complexity:** O(n)

### Solution 2: Bucket Sort (Optimal for this problem)

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

        // Bucket sort: index = frequency
        var buckets = new List<int>[nums.Length + 1];

        foreach (var kvp in freqMap)
        {
            int freq = kvp.Value;
            if (buckets[freq] == null)
            {
                buckets[freq] = new List<int>();
            }
            buckets[freq].Add(kvp.Key);
        }

        // Collect top k elements
        var result = new List<int>();
        for (int i = buckets.Length - 1; i >= 0 && result.Count < k; i--)
        {
            if (buckets[i] != null)
            {
                result.AddRange(buckets[i]);
            }
        }

        return result.Take(k).ToArray();
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

**Explanation:**

- Bucket sort by frequency
- Index i contains elements with frequency i
- Scan from high to low frequencies
- Collect first k elements
- Optimal O(n) solution!

---

## Key Takeaways for Day 14

### Advanced Data Structures Comparison

| Structure    | Use Case                     | Time (avg)   | Space  |
| ------------ | ---------------------------- | ------------ | ------ |
| LRU Cache    | Recent access tracking       | O(1) get/put | O(n)   |
| Trie         | Prefix queries, autocomplete | O(m) search  | O(n×m) |
| Heap         | Priority queue, top K        | O(log n) ops | O(n)   |
| Union-Find   | Disjoint sets, connectivity  | O(α(n))      | O(n)   |
| Segment Tree | Range queries                | O(log n)     | O(n)   |

### When to Use What

**LRU Cache:**

- Need O(1) access with eviction policy
- Cache implementation
- Browser history

**Trie:**

- Autocomplete
- Spell checker
- IP routing
- String prefix problems

**Heap:**

- Top K elements
- Priority scheduling
- Median finding (two heaps)
- Merge K sorted lists

**Segment Tree:**

- Range sum/min/max queries
- Interval updates
- Better than array for many queries

**Tomorrow:** Day 15 - Interview Preparation & System Design
