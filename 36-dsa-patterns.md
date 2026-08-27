# 36. DSA Interview Patterns

**Previous:** [35. DSA Fundamentals](./35-dsa-foundations.md)

**Next:** [37. DSA Coding Practice](./37-dsa-practice.md)

______________________________________________________________________

## Objective

By the end of this topic, you should be able to:

- Recognize common patterns behind interview problems.
- Choose an appropriate pattern from the problem constraints.
- Apply two pointers to arrays and strings.
- Apply sliding-window techniques.
- Use hash maps and sets to reduce repeated work.
- Use stack-based patterns.
- Apply binary search beyond simple sorted-array lookup.
- Understand BFS and DFS.
- Solve basic Top-K problems.
- Use prefix/suffix techniques.
- Recognize simple dynamic-programming problems.
- Explain the time and space complexity of your solution.

> **Scope:** This topic focuses on reusable interview patterns rather than advanced algorithms. The goal is to recognize the structure of a problem quickly and apply a reliable technique.

______________________________________________________________________

# 1. Why Patterns Matter

Interview questions often look different on the surface but use the same underlying technique.

For example:

```text
Find a pair
Find a target sum
Find two values satisfying a condition
```

may repeatedly lead to:

```text
Hash map
Two pointers
```

Similarly:

```text
Longest substring
Maximum sum of a fixed-size range
Smallest window satisfying a condition
```

often suggests:

```text
Sliding window
```

The goal is to recognize the pattern before writing the implementation.

______________________________________________________________________

# 2. Pattern Recognition

When reading a problem, ask:

```text
What is the input?
Is it sorted?
Do I need a contiguous range?
Do I need fast lookup?
Do I need the best K items?
Do I need to explore a graph/tree?
Do I need repeated comparisons?
Can I reuse previous results?
```

These questions often reveal the appropriate pattern.

______________________________________________________________________

# 3. Pattern Selection Guide

| Problem Signal | Likely Pattern |
|---|---|
| Sorted array + pair condition | Two pointers |
| Contiguous subarray/substring | Sliding window |
| Need fast lookup/counting | Hash map/set |
| Matching nested structure | Stack |
| Sorted search space | Binary search |
| Shortest unweighted path | BFS |
| Explore all paths/branches | DFS |
| K largest/smallest | Heap / Top-K |
| Range sums | Prefix sum |
| Need information from both directions | Prefix/suffix |
| Repeated overlapping subproblems | Dynamic programming |

These are heuristics, not absolute rules.

______________________________________________________________________

# 4. Two Pointers

Two pointers use two indexes or references to process a sequence efficiently.

Typical forms:

```text
left → ← right
```

or:

```text
slow →
fast →
```

The first form is especially common with sorted arrays and strings.

______________________________________________________________________

# 5. Two Pointers on a Sorted Array

Example:

```text
[1, 2, 4, 7, 11]
target = 9
```

Start:

```text
left = 1
right = 11
```

Since:

```text
1 + 11 > 9
```

move the right pointer.

Then:

```text
1 + 7 < 9
```

move the left pointer.

Eventually:

```text
2 + 7 = 9
```

______________________________________________________________________

# 6. Two-Pointer Algorithm

```python
def two_sum_sorted(values, target):
    left = 0
    right = len(values) - 1

    while left < right:
        total = values[left] + values[right]

        if total == target:
            return left, right
        elif total < target:
            left += 1
        else:
            right -= 1

    return None
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

assuming the input is already sorted.

______________________________________________________________________

# 7. Why Two Pointers Work

The sorted order provides information.

If:

```text
values[left] + values[right] < target
```

then keeping the same `left` while decreasing `right` cannot increase the sum.

Therefore moving `left` is justified.

The pattern relies on a monotonic relationship.

______________________________________________________________________

# 8. Two Pointers for Palindromes

Example:

```text
racecar
```

Compare:

```text
r ↔ r
a ↔ a
c ↔ c
```

Move inward until the pointers meet.

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False

        left += 1
        right -= 1

    return True
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

______________________________________________________________________

# 9. Two Pointers for In-Place Modification

Two pointers can separate elements while scanning once.

Example use cases:

- Remove duplicates
- Move zeroes
- Partition values
- Remove a target value

A common structure is:

```text
read pointer
write pointer
```

The read pointer scans input while the write pointer tracks where the next valid value should go.

______________________________________________________________________

# 10. Sliding Window

Sliding window is useful when the problem concerns a contiguous:

```text
subarray
substring
range
```

Instead of recomputing every range, maintain information about the current window.

Conceptually:

```text
[ left ........ right ]
```

Expand or shrink the window according to the condition.

______________________________________________________________________

# 11. Fixed-Size Sliding Window

Problem:

> Find the maximum sum of any subarray of size `k`.

Naive approach:

```text
Calculate every window independently.
```

This can be O(nk).

Sliding window:

```text
Add new element
Remove old element
```

gives:

```text
O(n)
```

______________________________________________________________________

# 12. Fixed Window Example

```python
def max_sum(values, k):
    if k <= 0 or k > len(values):
        return None

    window_sum = sum(values[:k])
    best = window_sum

    for right in range(k, len(values)):
        window_sum += values[right]
        window_sum -= values[right - k]
        best = max(best, window_sum)

    return best
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

______________________________________________________________________

# 13. Variable-Size Sliding Window

A variable window expands until a condition is violated and then shrinks.

Conceptually:

```text
right →
[ left ........ right ]
   ← shrink
```

This is common for:

```text
Longest valid substring
Smallest valid subarray
At most K distinct values
```

______________________________________________________________________

# 14. Longest Substring Without Repeating Characters

Example:

```text
abcabcbb
```

Maintain a window containing unique characters.

When a duplicate appears:

```text
move left
```

until the window becomes valid again.

A set or dictionary is commonly used to track characters.

______________________________________________________________________

# 15. Sliding Window Example

```python
def longest_unique_substring(s):
    seen = set()
    left = 0
    best = 0

    for right, char in enumerate(s):
        while char in seen:
            seen.remove(s[left])
            left += 1

        seen.add(char)
        best = max(best, right - left + 1)

    return best
```

Complexity:

```text
Time: O(n)
Space: O(k)
```

where `k` is the number of distinct characters that can appear in the window.

______________________________________________________________________

# 16. Sliding Window Recognition

Think:

> "Can I maintain a valid contiguous range while moving the boundaries?"

If yes, sliding window may apply.

Common clues:

```text
longest
shortest
maximum
minimum
substring
subarray
contiguous
at most K
at least K
```

______________________________________________________________________

# 17. Hash-Map Patterns

Hash maps are useful when you need to remember information about previously seen values.

Common uses:

```text
Frequency counting
Index lookup
Grouping
Deduplication
Complement lookup
Prefix-state tracking
```

______________________________________________________________________

# 18. Frequency Counting

Example:

```text
"banana"
```

Frequency:

```text
b → 1
a → 3
n → 2
```

Python:

```python
from collections import Counter

counts = Counter("banana")
```

This is often the first step in:

```text
Anagram problems
Frequency problems
Duplicate detection
Top-K frequency
```

______________________________________________________________________

# 19. Two Sum with a Hash Map

For an unsorted array:

```text
[2, 7, 11, 15]
target = 9
```

For each value:

```text
needed = target - value
```

Check whether `needed` was already seen.

```python
def two_sum(values, target):
    seen = {}

    for index, value in enumerate(values):
        needed = target - value

        if needed in seen:
            return seen[needed], index

        seen[value] = index

    return None
```

Complexity:

```text
Time: O(n) average
Space: O(n)
```

______________________________________________________________________

# 20. Hash Map vs Two Pointers

For Two Sum:

### Unsorted input

Hash map:

```text
O(n) average
```

### Sorted input

Two pointers:

```text
O(n)
O(1) extra space
```

This is an important interview trade-off.

______________________________________________________________________

# 21. Grouping with Hash Maps

Suppose you need to group anagrams.

Example:

```text
eat
tea
ate
tan
nat
```

A normalized representation can become the key:

```text
aet → [eat, tea, ate]
ant → [tan, nat]
```

This demonstrates a common pattern:

```text
derived key
→ group of values
```

______________________________________________________________________

# 22. Stack Patterns

Stacks are useful when the current item depends on the most recent unresolved item.

Common clues:

```text
Matching brackets
Nested structures
Undo
Previous greater/smaller element
Next greater/smaller element
Monotonic relationships
```

______________________________________________________________________

# 23. Valid Parentheses

Use a stack.

```python
def is_valid(s):
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    stack = []

    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)

    return not stack
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

______________________________________________________________________

# 24. Monotonic Stack

A monotonic stack maintains elements in increasing or decreasing order.

It is useful for:

```text
Next greater element
Next smaller element
Previous greater element
Previous smaller element
```

Example:

```text
[2, 1, 2, 4, 3]
```

You can use a monotonic stack to efficiently find the next greater element.

The key insight is:

> Keep unresolved candidates on the stack until a future value resolves them.

______________________________________________________________________

# 25. Why Monotonic Stack Is Efficient

A naive approach may compare each element with many later elements:

```text
O(n²)
```

A monotonic stack can process each element a limited number of times:

```text
O(n)
```

This is a classic interview optimization.

______________________________________________________________________

# 26. Binary Search

Binary search works when the search space has a monotonic ordering/property.

Classic example:

```text
Sorted array
```

Instead of checking every element:

```text
O(n)
```

repeatedly divide the search space:

```text
O(log n)
```

______________________________________________________________________

# 27. Basic Binary Search

```python
def binary_search(values, target):
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if values[mid] == target:
            return mid
        elif values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

Complexity:

```text
Time: O(log n)
Space: O(1)
```

______________________________________________________________________

# 28. Binary Search Invariants

A reliable binary-search implementation maintains a clear invariant.

For example:

```text
All possible answers are within [left, right].
```

At every iteration, the search space becomes smaller.

Many binary-search bugs come from unclear boundary conditions.

______________________________________________________________________

# 29. Lower Bound

A common binary-search variant finds the first position where:

```text
values[index] >= target
```

This is useful for:

- Insertion position
- First occurrence
- Range queries
- Counting values in a range

Python's `bisect` module provides useful primitives for these operations.

______________________________________________________________________

# 30. Binary Search on the Answer

Binary search does not always have to search an array.

Sometimes the possible answer itself forms a monotonic search space.

Example:

> Find the minimum capacity that allows all jobs to finish within `D` days.

You can ask:

```text
Can capacity X satisfy the requirement?
```

If:

```text
X works
```

then larger values may also work.

That monotonic property enables binary search over the answer.

______________________________________________________________________

# 31. Binary Search Recognition

Ask:

> Is there a yes/no feasibility condition that changes monotonically as the candidate value changes?

If:

```text
false false false true true true
```

or:

```text
true true true false false false
```

appears conceptually, binary search may be applicable.

______________________________________________________________________

# 32. BFS

Breadth-First Search explores a graph/tree level by level.

Typical structure:

```text
Start
 ↓
neighbors
 ↓
neighbors of neighbors
```

Use a queue.

______________________________________________________________________

# 33. BFS Example

```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

Complexity for a graph:

```text
Time: O(V + E)
Space: O(V)
```

where:

```text
V = vertices
E = edges
```

______________________________________________________________________

# 34. BFS and Shortest Path

For an unweighted graph, BFS can find the shortest path in terms of number of edges.

Why?

Because BFS explores:

```text
distance 0
distance 1
distance 2
distance 3
...
```

The first time a node is reached, it is reached using the minimum number of edges.

______________________________________________________________________

# 35. BFS on a Grid

Grid problems frequently use BFS.

Example:

```text
0 0 0
1 1 0
0 0 0
```

Typical operations:

```text
up
down
left
right
```

BFS is useful for:

- Minimum number of moves
- Shortest path
- Level-by-level expansion
- Multi-source spreading problems

______________________________________________________________________

# 36. Multi-Source BFS

Sometimes multiple starting nodes exist.

Example:

```text
Sources:
A . . B . .
```

Initialize the queue with all sources.

Then BFS expands simultaneously from them.

This is useful for problems involving:

```text
Nearest source
Spreading
Rotting/contamination
Distance from multiple starting points
```

______________________________________________________________________

# 37. DFS

Depth-First Search explores one branch deeply before backtracking.

Typical structure:

```text
node
 ↓
child
 ↓
child
 ↓
backtrack
```

It can be implemented recursively or with an explicit stack.

______________________________________________________________________

# 38. DFS Example

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    if node in visited:
        return

    visited.add(node)

    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)
```

Complexity:

```text
Time: O(V + E)
Space: O(V)
```

______________________________________________________________________

# 39. BFS vs DFS

| Property | BFS | DFS |
|---|---|---|
| Main structure | Queue | Stack/recursion |
| Exploration | Level by level | Depth first |
| Shortest unweighted path | Yes | Not generally |
| Useful for | Distance/levels | Exploration/backtracking |
| Auxiliary space | O(V) | O(V) worst case |

______________________________________________________________________

# 40. Connected Components

DFS/BFS can find connected components.

Conceptually:

```text
For every unvisited node:
    start traversal
    mark all reachable nodes
    increment component count
```

This is a common graph interview pattern.

______________________________________________________________________

# 41. Cycle Detection

Traversal can also detect cycles.

For undirected graphs, track parent information.

For directed graphs, a common DFS approach tracks:

```text
currently visiting
fully processed
```

The exact technique depends on graph type.

______________________________________________________________________

# 42. Top-K Pattern

Top-K problems ask for:

```text
K largest
K smallest
K most frequent
K closest
```

A heap is often useful.

Python provides:

```python
import heapq
```

______________________________________________________________________

# 43. Why Use a Heap for Top-K?

Suppose:

```text
n = 1,000,000
k = 10
```

Sorting everything costs approximately:

```text
O(n log n)
```

A size-k heap can often achieve:

```text
O(n log k)
```

which is much smaller when `k << n`.

______________________________________________________________________

# 44. Top-K Largest

Conceptually maintain a min-heap of size `k`.

For each value:

```text
push value
if heap size > k:
    remove smallest
```

At the end, the heap contains the K largest values.

Complexity:

```text
Time: O(n log k)
Space: O(k)
```

______________________________________________________________________

# 45. Top-K Frequent

Typical approach:

```text
1. Count frequencies.
2. Keep the K highest-frequency items.
```

Possible tools:

```text
Counter
heap
sorting
```

The best approach depends on constraints.

______________________________________________________________________

# 46. Prefix Sum

Prefix sums allow repeated range-sum queries to be answered efficiently.

Given:

```text
[2, 4, 1, 5]
```

Prefix sums:

```text
[0, 2, 6, 7, 12]
```

Then a range sum can be calculated using subtraction.

______________________________________________________________________

# 47. Prefix Sum Example

```python
def build_prefix(values):
    prefix = [0]

    for value in values:
        prefix.append(prefix[-1] + value)

    return prefix
```

Range:

```text
values[left:right+1]
```

can be computed using:

```text
prefix[right + 1] - prefix[left]
```

______________________________________________________________________

# 48. Prefix Sum Complexity

Building:

```text
O(n)
```

Each range query:

```text
O(1)
```

Additional space:

```text
O(n)
```

This is useful when there are many range queries.

______________________________________________________________________

# 49. Prefix Sum + Hash Map

A powerful pattern combines prefix sums with a hash map.

Example problem:

> Find whether a subarray sums to a target.

If:

```text
prefix[j] - prefix[i] = target
```

then:

```text
prefix[i] = prefix[j] - target
```

A hash map can store previous prefix sums.

This can produce an O(n) average solution.

______________________________________________________________________

# 50. Prefix vs Sliding Window

Sliding window is often effective when the window validity changes monotonically as boundaries move.

Prefix sums are useful when:

```text
Range sums
Subarray sum relationships
Repeated range queries
```

The presence of negative numbers is one reason a simple positive-number sliding window may not work, while
prefix-sum/hash-map methods can still work.

______________________________________________________________________

# 51. Prefix/Suffix Pattern

Sometimes the answer for each element depends on information:

```text
to its left
+
to its right
```

A prefix/suffix approach precomputes these values.

Classic example:

> Product of array except self.

Conceptually:

```text
prefix product
+
suffix product
```

______________________________________________________________________

# 52. Prefix/Suffix Example

For:

```text
[1, 2, 3, 4]
```

For index `2`, the answer is:

```text
1 × 2 × 4
```

Precompute information from both directions rather than repeatedly scanning the entire array.

Typical complexity:

```text
Time: O(n)
Space: O(n)
```

or O(1) extra space beyond the output in optimized variants.

______________________________________________________________________

# 53. Dynamic Programming

Dynamic programming is useful when a problem has:

```text
Overlapping subproblems
+
Optimal substructure
```

Instead of recomputing the same states repeatedly, store previous results.

______________________________________________________________________

# 54. Memoization

Memoization is top-down DP.

Example:

```python
def fib(n, memo=None):
    if memo is None:
        memo = {}

    if n <= 1:
        return n

    if n in memo:
        return memo[n]

    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

The dictionary stores previously computed results.

______________________________________________________________________

# 55. Tabulation

Tabulation is bottom-up DP.

Example:

```python
def fib(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]
```

______________________________________________________________________

# 56. DP State

The hardest part of many DP problems is defining the state.

Ask:

> What information uniquely describes the subproblem?

For Fibonacci:

```text
dp[i] = Fibonacci number at i
```

For other problems it might be:

```text
dp[i] = best answer using first i items
```

or:

```text
dp[i][j] = best answer using positions i and j
```

______________________________________________________________________

# 57. DP Transition

Once the state is defined, determine how the current state depends on previous states.

Example:

```text
dp[i] = dp[i - 1] + dp[i - 2]
```

This relationship is the transition.

A reliable DP solution usually requires:

```text
State
+
Base case
+
Transition
+
Iteration/order
```

______________________________________________________________________

# 58. Basic 1D DP Example

Problem:

> You can climb either one or two steps. How many ways can you reach step n?

Relationship:

```text
ways[n] = ways[n - 1] + ways[n - 2]
```

This has the same structure as Fibonacci.

Complexity:

```text
Time: O(n)
Space: O(n)
```

It can be optimized to O(1) extra space.

______________________________________________________________________

# 59. When Not to Use DP

Do not use dynamic programming simply because:

```text
The problem is difficult.
```

Look for:

```text
Repeated subproblems
+
A state that captures the necessary information
```

If every state is unique, memoization may not provide useful savings.

______________________________________________________________________

# 60. Pattern Comparison

| Pattern | Main Signal | Typical Complexity |
|---|---|---:|
| Two pointers | Ordered/paired movement | O(n) |
| Sliding window | Contiguous range | O(n) |
| Hash map | Fast lookup/counting | O(n) avg |
| Stack | Nested/unresolved relationships | O(n) |
| Binary search | Monotonic search space | O(log n) |
| BFS | Levels/shortest unweighted path | O(V+E) |
| DFS | Deep exploration/components | O(V+E) |
| Top-K | Need K best items | O(n log k) |
| Prefix sum | Range/subarray sums | O(n) preprocessing |
| Prefix/suffix | Both-side information | O(n) |
| DP | Overlapping subproblems | Problem-dependent |

______________________________________________________________________

# 61. Pattern Combinations

Real interview problems may combine patterns.

Examples:

```text
Hash map + prefix sum
Sliding window + hash map
BFS + visited set
DFS + memoization
Heap + hash map
Binary search + greedy feasibility check
```

Do not assume every problem uses exactly one technique.

______________________________________________________________________

# 62. Example Combination — Sliding Window + Hash Map

Problem:

> Find the longest substring containing at most K distinct characters.

Use:

```text
Sliding window
+
Frequency dictionary
```

The dictionary tells you how many occurrences remain in the current window.

When distinct count exceeds K:

```text
move left
decrease frequency
remove key when frequency reaches zero
```

______________________________________________________________________

# 63. Example Combination — BFS + Visited

Without tracking visited nodes, a graph with cycles can cause repeated traversal.

Use:

```python
visited = {start}
```

and add nodes when they are discovered.

This ensures each node is processed appropriately once.

______________________________________________________________________

# 64. Example Combination — DFS + Memoization

Suppose different recursive paths reach the same state.

Without memoization:

```text
recompute state
recompute state
recompute state
```

With memoization:

```text
first calculation
 ↓
store result
 ↓
reuse result
```

This is a common bridge from recursion to DP.

______________________________________________________________________

# 65. How to Approach a Pattern Problem

Use this interview process:

### Step 1 — Understand

Restate the problem.

### Step 2 — Clarify

Ask about:

```text
Constraints
Duplicates
Ordering
Empty input
Negative values
```

### Step 3 — Brute force

Explain the obvious solution.

### Step 4 — Find the bottleneck

Ask:

> What work is being repeated?

### Step 5 — Identify pattern

Choose:

```text
Hash map
Two pointers
Sliding window
Stack
Binary search
BFS
DFS
Heap
Prefix/suffix
DP
```

### Step 6 — Implement

Write clean Python.

### Step 7 — Validate

Test:

```text
Empty
Single element
Duplicates
Boundary cases
Large input
```

### Step 8 — Complexity

State:

```text
Time: O(...)
Space: O(...)
```

______________________________________________________________________

# 66. Common Pattern Mistakes

## Mistake 1 — Using two pointers without ordering

Two-pointer movement often relies on sorted/monotonic properties.

## Mistake 2 — Using sliding window for every subarray problem

Not every contiguous-range problem has the monotonic property required.

## Mistake 3 — Forgetting visited in graph traversal

Can cause repeated work or infinite traversal on cyclic graphs.

## Mistake 4 — Incorrect binary-search boundaries

Be explicit about whether the range is:

```text
[left, right]
```

or:

```text
[left, right)
```

## Mistake 5 — Using a heap without considering K

Top-K problems often benefit from maintaining a heap of size K.

## Mistake 6 — Jumping to DP too early

First identify the state and overlapping subproblems.

______________________________________________________________________

# 67. Interview Questions & Answers

## Q1. How do you recognize a two-pointer problem?

**Answer:**

Look for arrays or strings where two positions can move through the data without needing to revisit most elements.
Sorted arrays, palindrome checks and in-place partitioning are common examples.

______________________________________________________________________

## Q2. Why does two-pointer Two Sum require a sorted array?

**Answer:**

The pointer movement relies on ordering. If the sum is too small, moving the left pointer increases the sum; if it is
too large, moving the right pointer decreases it.

______________________________________________________________________

## Q3. When would you use a hash map instead of two pointers?

**Answer:**

For unsorted input where fast lookup is required. A hash map can usually provide O(n) average time at the cost of O(n)
extra space.

______________________________________________________________________

## Q4. What is sliding window?

**Answer:**

It maintains a contiguous range and updates its state incrementally as the left and right boundaries move, avoiding
repeated computation of overlapping ranges.

______________________________________________________________________

## Q5. When does sliding window work well?

**Answer:**

When the problem involves a contiguous subarray/substring and the validity or objective can be maintained efficiently as
the window expands and shrinks.

______________________________________________________________________

## Q6. What is the difference between fixed and variable sliding windows?

**Answer:**

A fixed window has a predetermined size K. A variable window changes size according to a condition, often expanding with
the right pointer and shrinking from the left.

______________________________________________________________________

## Q7. Why can a simple sliding-window solution fail when negative numbers exist?

**Answer:**

Some sliding-window approaches rely on monotonic behavior, such as increasing a sum when expanding and decreasing it
when shrinking. Negative values can break that property. Prefix sums or other techniques may be more appropriate.

______________________________________________________________________

## Q8. What are common uses of hash maps in DSA?

**Answer:**

Frequency counting, complement lookup, indexing previously seen values, grouping and storing prefix-state information.

______________________________________________________________________

## Q9. What is a monotonic stack?

**Answer:**

A stack maintained in increasing or decreasing order. It efficiently solves next/previous greater or smaller element
problems by keeping unresolved candidates.

______________________________________________________________________

## Q10. Why can a monotonic stack be O(n)?

**Answer:**

Although there are nested-looking operations, each element is typically pushed and popped at most once, giving O(n)
total stack operations.

______________________________________________________________________

## Q11. What conditions are required for binary search?

**Answer:**

You need an ordered or monotonic search space where you can determine which half can be discarded after evaluating the
midpoint.

______________________________________________________________________

## Q12. Can binary search work without an explicitly sorted array?

**Answer:**

Yes. It can operate on any search space with a monotonic feasibility/property, such as binary search on a numeric
answer.

______________________________________________________________________

## Q13. What is binary search on the answer?

**Answer:**

Instead of searching for an element, search possible answer values and use a monotonic yes/no feasibility test to
determine which half of the answer space can be discarded.

______________________________________________________________________

## Q14. When should you use BFS?

**Answer:**

When you need level-order exploration or the shortest path in an unweighted graph/grid.

______________________________________________________________________

## Q15. When should you use DFS?

**Answer:**

When deep exploration, connectivity, components, cycle detection or backtracking-style traversal is appropriate.

______________________________________________________________________

## Q16. BFS vs DFS for shortest path?

**Answer:**

For an unweighted graph, BFS guarantees the shortest path by number of edges. DFS does not generally provide that
guarantee.

______________________________________________________________________

## Q17. Why do graph algorithms need a visited set?

**Answer:**

Graphs can contain cycles and multiple paths to the same node. A visited set prevents repeated processing and infinite
traversal.

______________________________________________________________________

## Q18. What is a Top-K problem?

**Answer:**

A problem asking for K largest, K smallest, K most frequent, K closest or similar "best K" elements.

______________________________________________________________________

## Q19. Why use a heap for Top-K?

**Answer:**

A heap can maintain only K candidates rather than sorting all N elements, often giving O(n log k) time and O(k)
additional space.

______________________________________________________________________

## Q20. What is a prefix sum?

**Answer:**

A cumulative sum array that allows range sums to be calculated through subtraction after O(n) preprocessing.

______________________________________________________________________

## Q21. Why combine prefix sums with a hash map?

**Answer:**

To find subarrays satisfying sum relationships efficiently. For target sum K, if the current prefix is P, we look for an
earlier prefix P-K.

______________________________________________________________________

## Q22. What is a prefix/suffix technique?

**Answer:**

It precomputes information from the left and/or right so each position can be answered without repeatedly scanning the
entire input.

______________________________________________________________________

## Q23. What makes a problem suitable for dynamic programming?

**Answer:**

It typically has overlapping subproblems and a reusable state representation with an optimal/subproblem structure.

______________________________________________________________________

## Q24. Memoization vs tabulation?

**Answer:**

Memoization is top-down recursion with cached results. Tabulation is bottom-up computation of states, usually
iteratively.

______________________________________________________________________

## Q25. What are the components of a DP solution?

**Answer:**

State definition, base cases, transition relation and the order in which states are computed.

______________________________________________________________________

## Q26. How do you know whether a sliding-window solution is valid?

**Answer:**

Verify that the window condition can be updated incrementally and that moving the left/right boundaries does not require
reconsidering an unbounded number of earlier states.

______________________________________________________________________

## Q27. Can interview problems combine patterns?

**Answer:**

Yes. Common combinations include sliding window plus hash map, BFS plus visited set, DFS plus memoization, heap plus
hash map and prefix sum plus hash map.

______________________________________________________________________

## Q28. How would you optimize a nested-loop solution?

**Answer:**

First identify what information the inner loop repeatedly calculates. Then determine whether a hash map, set, sorting,
two pointers, prefix data structure or another pattern can reuse that information.

______________________________________________________________________

## Q29. How do you choose between sorting and hashing?

**Answer:**

Hashing usually provides O(n) average lookup but uses additional memory and does not inherently provide ordering.
Sorting costs O(n log n) but can enable two pointers, binary search and ordered processing.

______________________________________________________________________

## Q30. What is the senior-level approach to DSA interviews?

**Answer:**

"I focus on constraints and the operation that dominates the brute-force solution. I identify whether the problem has
ordering, contiguity, repeated lookup, monotonicity, graph traversal, Top-K requirements or overlapping subproblems.
Then I select the corresponding pattern, explain why it works, implement it clearly in Python, test edge cases and state
the time/space trade-off."

______________________________________________________________________

# 68. Pattern Recognition Drills

For each problem, identify the likely pattern before coding.

## Problem 1

> Find whether a sorted array contains two values whose sum equals a target.

**Pattern:**

```text
Two pointers
```

______________________________________________________________________

## Problem 2

> Find the longest substring without repeating characters.

**Pattern:**

```text
Sliding window + set/hash map
```

______________________________________________________________________

## Problem 3

> Find the first non-repeating character.

**Pattern:**

```text
Hash map/frequency counting
```

______________________________________________________________________

## Problem 4

> Determine whether brackets are correctly nested.

**Pattern:**

```text
Stack
```

______________________________________________________________________

## Problem 5

> Find the first position where a sorted value is greater than or equal to target.

**Pattern:**

```text
Binary search / lower bound
```

______________________________________________________________________

## Problem 6

> Find the shortest path through an unweighted grid.

**Pattern:**

```text
BFS
```

______________________________________________________________________

## Problem 7

> Count connected islands in a grid.

**Pattern:**

```text
DFS or BFS
```

______________________________________________________________________

## Problem 8

> Find the 10 largest values in a stream.

**Pattern:**

```text
Top-K + heap
```

______________________________________________________________________

## Problem 9

> Answer thousands of range-sum queries.

**Pattern:**

```text
Prefix sum
```

______________________________________________________________________

## Problem 10

> Find the number of ways to reach the nth step when you can move one or two steps.

**Pattern:**

```text
Dynamic programming
```

______________________________________________________________________

# 69. Practical Exercises

Before moving to File 37, implement these problems yourself.

### Two Pointers

1. Two Sum on a sorted array.
1. Valid palindrome.
1. Remove duplicates from a sorted array.
1. Move zeroes to the end.

### Sliding Window

5. Maximum sum subarray of size K.
1. Longest substring without repeating characters.
1. Longest substring with at most K distinct characters.
1. Minimum-size subarray with a required sum.

### Hash Map

9. Two Sum on an unsorted array.
1. First unique character.
1. Group anagrams.
1. Frequency-based comparison.

### Stack

13. Valid parentheses.
01. Next greater element.
01. Evaluate a simple postfix expression.

### Binary Search

16. Standard binary search.
01. First occurrence.
01. Search insertion position.
01. Binary search on a monotonic answer space.

### BFS/DFS

20. Tree level-order traversal.
01. Number of islands.
01. Connected components.
01. Shortest path in an unweighted grid.

### Top-K

24. K largest elements.
01. K most frequent elements.

### Prefix/Suffix

26. Range sum queries.
01. Product of array except self.
01. Subarray sum equals K.

### Basic DP

29. Climbing stairs.
01. House robber-style one-dimensional DP.

For each problem, write down:

```text
Pattern
Approach
Time complexity
Space complexity
Edge cases
```

before writing code.

______________________________________________________________________

# 70. Final Interview Readiness Checklist

Before moving to File 37, make sure you can:

- [ ] Recognize common DSA patterns.
- [ ] Explain when two pointers apply.
- [ ] Implement two-pointer solutions.
- [ ] Explain sorted-array two pointers.
- [ ] Explain palindrome two pointers.
- [ ] Explain read/write pointers.
- [ ] Recognize fixed sliding windows.
- [ ] Recognize variable sliding windows.
- [ ] Implement a sliding-window solution.
- [ ] Explain when sliding window does not apply.
- [ ] Use hash maps for lookup.
- [ ] Use hash maps for frequency counting.
- [ ] Combine hash maps with other patterns.
- [ ] Recognize stack problems.
- [ ] Implement a monotonic stack.
- [ ] Explain why monotonic stacks can be O(n).
- [ ] Implement binary search.
- [ ] Explain lower bound.
- [ ] Explain binary search on the answer.
- [ ] Identify monotonic search spaces.
- [ ] Implement BFS.
- [ ] Implement DFS.
- [ ] Explain BFS vs DFS.
- [ ] Explain BFS shortest-path behavior.
- [ ] Track visited nodes correctly.
- [ ] Find connected components.
- [ ] Recognize Top-K problems.
- [ ] Use `heapq` for Top-K.
- [ ] Explain O(n log k).
- [ ] Build prefix sums.
- [ ] Combine prefix sums with a hash map.
- [ ] Use prefix/suffix preprocessing.
- [ ] Recognize basic DP.
- [ ] Define a DP state.
- [ ] Define a DP transition.
- [ ] Explain memoization.
- [ ] Explain tabulation.
- [ ] Combine patterns.
- [ ] Analyze time complexity.
- [ ] Analyze space complexity.
- [ ] Explain trade-offs.
- [ ] Communicate the solution clearly.

______________________________________________________________________

# 71. Final Takeaways

The goal of DSA interview preparation is not to memorize solutions.

It is to recognize structures:

```text
Sorted + pair relationship
→ Two pointers

Contiguous + changing window
→ Sliding window

Repeated lookup/counting
→ Hash map/set

Nested/unresolved relationships
→ Stack

Monotonic search space
→ Binary search

Levels / shortest unweighted path
→ BFS

Deep exploration / connectivity
→ DFS

Best K elements
→ Heap / Top-K

Range information
→ Prefix/suffix

Repeated subproblems
→ Dynamic programming
```

When you get stuck, return to the basic question:

> **What work is being repeated, and what information could I keep so I don't have to do it again?**

That question leads naturally to many of the most important interview patterns.

______________________________________________________________________

**Previous:** [35. DSA Fundamentals](./35-dsa-foundations.md)

**Next:** [37. DSA Coding Practice](./37-dsa-practice.md)
