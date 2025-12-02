# C# Algorithm Interview Preparation - 15-Day Series

## 🎯 Overview

A comprehensive 15-day algorithm preparation guide designed specifically for C# developers interviewing at big tech companies. Each day contains 3 carefully selected problems progressing from simple to advanced, with multiple solutions, Big-O analysis, and interview tips.

**Total:** 45 problems covering all major algorithm patterns and data structures.

---

## 📚 Course Structure

### Week 1: Fundamentals

Build a strong foundation with basic data structures and patterns that appear in 60% of interviews.

#### [Day 1: Arrays & Strings - Fundamentals](./algo-day01-arrays-strings.md)

**Focus:** Hash tables, two pointers basics  
**Problems:**

1. ⭐ Two Sum (Hash table optimization)
2. ⭐⭐ Valid Palindrome (Two pointers)
3. ⭐⭐⭐ Longest Substring Without Repeating Characters (Sliding window)

**Key Patterns:** Hash table for O(1) lookups, two pointers for space optimization

---

#### [Day 2: Two Pointers & Sliding Window - Advanced](./algo-day02-two-pointers-sliding-window.md)

**Focus:** Advanced pointer techniques, window optimization  
**Problems:**

1. ⭐ Remove Duplicates from Sorted Array (In-place modification)
2. ⭐⭐ Container With Most Water (Greedy two pointers)
3. ⭐⭐⭐ Minimum Window Substring (Advanced sliding window)

**Key Patterns:** Opposite direction pointers, expandable windows, monotonic sequences

---

#### [Day 3: Hash Tables & Sets - Advanced Hashing](./algo-day03-hash-tables-sets.md)

**Focus:** Frequency counting, grouping, prefix sums  
**Problems:**

1. ⭐⭐ Group Anagrams (Hashing with custom keys)
2. ⭐⭐ Longest Consecutive Sequence (HashSet intelligence)
3. ⭐⭐⭐ Subarray Sum Equals K (Prefix sum technique)

**Key Patterns:** Using sorted strings as keys, prefix sum + hash map

---

#### [Day 4: Sorting & Searching](./algo-day04-sorting-searching.md)

**Focus:** Binary search variations, search space reduction  
**Problems:**

1. ⭐ Binary Search (Classic implementation)
2. ⭐⭐ Find First and Last Position (Modified binary search)
3. ⭐⭐⭐ Search in Rotated Sorted Array (Advanced binary search)

**Key Patterns:** Binary search template, finding boundaries, rotated array handling

---

#### [Day 5: Linked Lists](./algo-day05-linked-lists.md)

**Focus:** Pointer manipulation, cycle detection  
**Problems:**

1. ⭐ Reverse Linked List (Essential pointer technique)
2. ⭐⭐ Linked List Cycle (Floyd's algorithm)
3. ⭐⭐⭐ Merge K Sorted Lists (Divide and conquer)

**Key Patterns:** Dummy nodes, fast/slow pointers, in-place reversal

---

#### [Day 6: Stacks & Queues - LIFO & FIFO](./algo-day06-stacks-queues.md)

**Focus:** Monotonic structures, matching patterns  
**Problems:**

1. ⭐ Valid Parentheses (Classic stack)
2. ⭐⭐ Daily Temperatures (Monotonic stack)
3. ⭐⭐⭐ Sliding Window Maximum (Deque optimization)

**Key Patterns:** Monotonic stack for next greater/smaller, deque for sliding windows

---

#### [Day 7: Binary Trees - Fundamentals](./algo-day07-binary-trees.md)

**Focus:** Tree traversals, recursion patterns  
**Problems:**

1. ⭐ Maximum Depth (Basic recursion)
2. ⭐⭐ Validate BST (Range validation)
3. ⭐⭐⭐ Lowest Common Ancestor (Post-order logic)

**Key Patterns:** DFS recursion, BFS level-order, divide and conquer

---

### Week 2: Intermediate Topics

Master trees, graphs, and dynamic programming - core topics for all tech interviews.

#### [Day 8: BST & Advanced Trees](./algo-day08-bst-advanced-trees.md)

**Focus:** BST properties, tree construction  
**Problems:**

1. ⭐⭐ Kth Smallest in BST (Inorder optimization)
2. ⭐⭐ Binary Tree Right Side View (BFS/DFS views)
3. ⭐⭐⭐ Construct Tree from Traversals (Reconstruction logic)

**Key Patterns:** BST inorder = sorted, tree reconstruction, view problems

---

#### [Day 9: Graphs - BFS & DFS](./algo-day09-graphs-bfs-dfs.md)

**Focus:** Graph traversals, cycle detection  
**Problems:**

1. ⭐⭐ Number of Islands (DFS/BFS on grid)
2. ⭐⭐ Clone Graph (Graph copying with HashMap)
3. ⭐⭐⭐ Course Schedule (Cycle detection, topological sort)

**Key Patterns:** DFS for connectivity, BFS for shortest path, topological sort

---

#### [Day 10: Dynamic Programming - Basics](./algo-day10-dynamic-programming-basics.md)

**Focus:** DP fundamentals, memoization, tabulation  
**Problems:**

1. ⭐ Climbing Stairs (Introduction to DP)
2. ⭐⭐ House Robber (Choice-based DP)
3. ⭐⭐⭐ Longest Increasing Subsequence (Subsequence DP)

**Key Patterns:** Top-down vs bottom-up, space optimization, state definition

---

#### [Day 11: Dynamic Programming - Advanced](./algo-day11-dynamic-programming-advanced.md)

**Focus:** 2D DP, multiple sequences  
**Problems:**

1. ⭐⭐ Coin Change (Unbounded knapsack)
2. ⭐⭐ Longest Common Subsequence (2D DP)
3. ⭐⭐⭐ Word Break (String segmentation)

**Key Patterns:** 2D DP template, string problems, choice trees

---

#### [Day 12: Backtracking & Recursion](./algo-day12-backtracking-recursion.md)

**Focus:** Exhaustive search, constraint satisfaction  
**Problems:**

1. ⭐⭐ Subsets (Power set generation)
2. ⭐⭐ Permutations (All orderings)
3. ⭐⭐⭐ N-Queens (Constraint satisfaction)

**Key Patterns:** Choose/explore/unchoose, pruning, state space search

---

#### [Day 13: Greedy Algorithms](./algo-day13-greedy-algorithms.md)

**Focus:** Local optimal choices, interval problems  
**Problems:**

1. ⭐⭐ Best Time to Buy/Sell Stock II (Greedy gains)
2. ⭐⭐ Jump Game (Reachability)
3. ⭐⭐⭐ Meeting Rooms II (Interval scheduling)

**Key Patterns:** Sorting for greedy, interval problems, exchange arguments

---

#### [Day 14: Advanced Data Structures](./algo-day14-advanced-data-structures.md)

**Focus:** LRU, Trie, Heap applications  
**Problems:**

1. ⭐⭐ LRU Cache (Design problem)
2. ⭐⭐ Implement Trie (Prefix tree)
3. ⭐⭐⭐ Top K Frequent Elements (Heap/bucket sort)

**Key Patterns:** Design patterns, custom data structures, optimization techniques

---

#### [Day 15: Interview Prep & System Design](./algo-day15-interview-prep-system-design.md)

**Focus:** Complete interview strategy, system design basics  
**Problems:**

1. ⭐⭐⭐ Design Twitter (Multi-structure design)
2. ⭐⭐⭐ Autocomplete System (Trie + heap)
3. ⭐⭐⭐ Rate Limiter (System design)

**Includes:** Interview checklist, complexity reference, company-specific tips

---

## 🎓 Learning Path Recommendations

### For Complete Beginners

**Start here:** Days 1-4 (Arrays, Strings, Sorting)  
**Then:** Days 5-7 (Linked Lists, Stacks, Trees)  
**Finally:** Days 10-15 (DP, Advanced topics)

### For Intermediate Developers

**Review:** Days 1-3 (Fundamentals)  
**Focus on:** Days 7-12 (Trees, Graphs, DP, Backtracking)  
**Master:** Days 13-15 (Advanced patterns)

### Last-Minute Interview Prep (1 Week)

- **Days 1-2:** Arrays, two pointers, sliding window
- **Day 3:** Hash tables (most common in real interviews)
- **Day 4:** Binary search (test your logic skills)
- **Days 7-9:** Trees and graphs (tech company favorites)
- **Day 10:** DP basics (at least understand fundamentals)
- **Day 15:** Interview strategy and system design

---

## 📊 Problem Difficulty Distribution

| Difficulty           | Count  | Percentage |
| -------------------- | ------ | ---------- |
| Easy (⭐)            | 8      | 18%        |
| Easy-Medium (⭐⭐)   | 17     | 38%        |
| Medium-Hard (⭐⭐⭐) | 20     | 44%        |
| **Total**            | **45** | **100%**   |

---

## 🛠️ Technical Stack

**Language:** C# (Latest features)  
**Frameworks:** .NET 6+  
**Data Structures:** Native C# collections (List, Dictionary, HashSet, Queue, Stack, PriorityQueue)  
**Style:** Clean code, SOLID principles, modern C# idioms

---

## 📈 Progress Tracking

Use this checklist to track your progress:

- [ ] Day 1: Arrays & Strings ✓
- [ ] Day 2: Two Pointers & Sliding Window ✓
- [ ] Day 3: Hash Tables & Sets ✓
- [ ] Day 4: Sorting & Searching ✓
- [ ] Day 5: Linked Lists ✓
- [ ] Day 6: Stacks & Queues ✓
- [ ] Day 7: Binary Trees ✓
- [ ] Day 8: BST & Advanced Trees ✓
- [ ] Day 9: Graphs ✓
- [ ] Day 10: Dynamic Programming Basics ✓
- [ ] Day 11: Dynamic Programming Advanced ✓
- [ ] Day 12: Backtracking & Recursion ✓
- [ ] Day 13: Greedy Algorithms ✓
- [ ] Day 14: Advanced Data Structures ✓
- [ ] Day 15: Interview Preparation ✓

---

## 💡 Study Tips

### Daily Routine (2-3 hours)

1. **Read** the day's material (30 min)
2. **Code** the solutions yourself (60 min)
3. **Analyze** Big-O complexities (15 min)
4. **Review** key patterns (15 min)
5. **Practice** additional problems on LeetCode (30 min)

### Best Practices

- **Don't memorize solutions** - understand the patterns
- **Code without looking** - test your understanding
- **Explain out loud** - practice for interviews
- **Time yourself** - simulate real interview pressure
- **Review daily** - spaced repetition works

### Common Pitfalls to Avoid

- ❌ Skipping "easy" problems (they teach fundamentals)
- ❌ Only reading without coding
- ❌ Not testing edge cases
- ❌ Ignoring space complexity
- ❌ Giving up too quickly on hard problems

---

## 🏆 Success Metrics

After completing this course, you should be able to:

✅ Recognize 15+ algorithm patterns instantly  
✅ Analyze time/space complexity accurately  
✅ Solve medium LeetCode problems in 20-30 minutes  
✅ Explain your solution clearly during interviews  
✅ Optimize brute force solutions systematically  
✅ Handle edge cases confidently  
✅ Write clean, readable C# code  
✅ Perform well in technical interviews at FAANG companies

---

## 🔗 Additional Resources

### Practice Platforms

- **LeetCode:** Problems by pattern
- **HackerRank:** C# specific challenges
- **Pramp:** Free mock interviews
- **InterviewBit:** Structured learning paths

### Books

- "Cracking the Coding Interview" by Gayle McDowell
- "Elements of Programming Interviews" (C# edition)
- "Introduction to Algorithms" (CLRS)

### Videos

- NeetCode (LeetCode solutions)
- Tushar Roy (Algorithm explanations)
- CS Dojo (Beginner-friendly)

### C# Specific

- C# 11 features and modern patterns
- LINQ optimization techniques
- .NET performance tips

---

## 🎯 Interview Company Mapping

### Google

**Focus:** Days 4, 7-10 (Algorithms, DP, Graphs)  
**Extra:** System design, scalability

### Microsoft

**Focus:** Days 1-7, 14 (Fundamentals, Design patterns)  
**Extra:** OOP design, Windows/Azure knowledge

### Amazon

**Focus:** Days 1-6, 10-11 (Arrays, strings, DP)  
**Extra:** Leadership principles, scalability

### Meta (Facebook)

**Focus:** Days 3, 7-9, 14 (Hash tables, Trees, Graphs)  
**Extra:** Product sense, optimization

### Apple

**Focus:** Days 4-7, 14 (Binary search, Trees, Design)  
**Extra:** Memory management, low-level optimization

---

## 🚀 Getting Started

**Ready to begin?** Start with [Day 1: Arrays & Strings](./algo-day01-arrays-strings.md)

**Questions or feedback?** This is your personal interview preparation journey. Take it at your own pace, and remember: consistency beats intensity!

**Good luck with your interviews!** 🎉

---

_Created for C# developers preparing for technical interviews at top tech companies. Last updated: November 2025_
