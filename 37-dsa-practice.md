# 37. DSA Coding Practice

**Previous:** [36. DSA Interview Patterns](./36-dsa-patterns.md)

**Next:** [38. System Design Fundamentals](./38-system-design-fundamentals.md)

______________________________________________________________________

## Objective

This file is the practical DSA coding set for interview preparation.

The goal is not to solve hundreds of problems. It is to become comfortable with the most reusable patterns covered in
Files 35 and 36.

By the end of this topic, you should be able to:

- Recognize the pattern behind a coding problem.
- Explain a brute-force solution.
- Improve it to an optimal or near-optimal solution.
- Write clean Python under interview conditions.
- Analyze time and space complexity.
- Discuss edge cases.
- Handle common follow-up questions.
- Explain your reasoning while coding.

______________________________________________________________________

# How to Use This File

For each problem:

1. Read only the **Problem** section.
1. Try solving it yourself.
1. Explain the brute-force approach.
1. Identify the bottleneck.
1. Identify the pattern.
1. Implement the optimal solution.
1. Test edge cases.
1. Compare your solution with the provided answer.
1. Practice explaining the follow-up questions aloud.

For a 5+ year backend interview, prioritize **reasoning and communication** over memorizing code.

______________________________________________________________________

# Problem 1 — Two Sum

## Problem

Given an array of integers `nums` and an integer `target`, return the indices of two numbers whose values add up to
`target`.

Assume exactly one valid answer exists.

Example:

```text
Input:
nums = [2, 7, 11, 15]
target = 9

Output:
[0, 1]
```

## Pattern

```text
Hash map
```

## Brute Force

Check every pair.

```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

    return []
```

Complexity:

```text
Time: O(n²)
Space: O(1)
```

## Optimal Solution

Store previously seen values in a dictionary.

```python
def two_sum(nums, target):
    seen = {}

    for i, value in enumerate(nums):
        needed = target - value

        if needed in seen:
            return [seen[needed], i]

        seen[value] = i

    return []
```

Complexity:

```text
Time: O(n) average
Space: O(n)
```

## Edge Cases

- Empty array
- One element
- Negative numbers
- Duplicate values
- Target equal to twice a duplicated value

## Follow-Up Questions

### Q: What if the array is already sorted?

**Answer:** Use two pointers and achieve O(n) time with O(1) extra space.

### Q: Why not use two pointers on the original unsorted array?

**Answer:** Two-pointer movement depends on ordering. Sorting would also lose the original indices unless they are
preserved.

### Q: What if there are multiple valid pairs?

**Answer:** Clarify whether the requirement is any pair, all pairs, unique pairs, or the pair with a particular
property.

______________________________________________________________________

# Problem 2 — Contains Duplicate

## Problem

Given an integer array, determine whether any value appears at least twice.

Example:

```text
[1, 2, 3, 1] → True
[1, 2, 3, 4] → False
```

## Pattern

```text
Hash set
```

## Brute Force

Compare every pair.

```python
def contains_duplicate_brute(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True

    return False
```

Complexity:

```text
Time: O(n²)
Space: O(1)
```

## Optimal Solution

```python
def contains_duplicate(nums):
    seen = set()

    for value in nums:
        if value in seen:
            return True

        seen.add(value)

    return False
```

Complexity:

```text
Time: O(n) average
Space: O(n)
```

## Edge Cases

- Empty input
- One element
- All values equal
- All values unique

## Follow-Up Questions

### Q: Can this use O(1) extra space?

**Answer:** If modifying the input is allowed, sorting can be used and adjacent values compared, but that changes the
input and costs O(n log n) time.

### Q: Why is set membership fast?

**Answer:** Python sets are hash-table-based, providing O(1) average membership checks.

______________________________________________________________________

# Problem 3 — Group Anagrams

## Problem

Given a list of strings, group the strings that are anagrams.

Example:

```text
["eat", "tea", "tan", "ate", "nat", "bat"]
```

Possible output:

```text
[
    ["eat", "tea", "ate"],
    ["tan", "nat"],
    ["bat"]
]
```

## Pattern

```text
Hash map + derived key
```

## Brute Force

Compare strings against existing groups and determine whether they are anagrams.

This can become expensive because each string may need repeated comparisons and character processing.

## Optimal Solution

Use a normalized representation as the key.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)

    for value in strs:
        key = tuple(sorted(value))
        groups[key].append(value)

    return list(groups.values())
```

Complexity:

Let `n` be the number of strings and `k` their average length.

```text
Time: approximately O(n * k log k)
Space: O(nk)
```

## Edge Cases

- Empty list
- Empty strings
- Duplicate strings
- Strings with different lengths
- Case sensitivity

## Follow-Up Questions

### Q: Can you avoid sorting each string?

**Answer:** Yes. For a constrained character set, use a frequency tuple as the key, reducing per-string key construction
to O(k).

### Q: Why use a dictionary?

**Answer:** The normalized key lets us group equivalent strings in average O(1) hash-map lookup/insertion.

______________________________________________________________________

# Problem 4 — Top K Frequent Elements

## Problem

Given an integer array and integer `k`, return the `k` most frequent elements.

Example:

```text
nums = [1, 1, 1, 2, 2, 3]
k = 2

Output:
[1, 2]
```

## Pattern

```text
Frequency map + Top-K
```

## Brute Force

Count frequencies and sort all distinct values by frequency.

```python
from collections import Counter

def top_k_frequent_sort(nums, k):
    counts = Counter(nums)

    return [
        value
        for value, _ in counts.most_common(k)
    ]
```

A general sort-based implementation costs approximately:

```text
O(n + m log m)
```

where `m` is the number of distinct values.

## Optimal Solution

Use a min-heap of size `k`.

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    counts = Counter(nums)

    heap = []

    for value, frequency in counts.items():
        heapq.heappush(heap, (frequency, value))

        if len(heap) > k:
            heapq.heappop(heap)

    return [value for _, value in heap]
```

Complexity:

```text
Time: O(n + m log k)
Space: O(m + k)
```

## Edge Cases

- `k = 1`
- `k` equals number of unique values
- Duplicate-heavy input
- Negative values

## Follow-Up Questions

### Q: Why use a heap of size k?

**Answer:** It avoids sorting every unique value and keeps only the candidates needed for the final result.

### Q: What if k is close to the number of unique values?

**Answer:** Sorting may be simpler and can be competitive. The constraints should guide the choice.

______________________________________________________________________

# Problem 5 — Longest Consecutive Sequence

## Problem

Given an unsorted array, return the length of the longest consecutive sequence.

Example:

```text
[100, 4, 200, 1, 3, 2]

Output:
4
```

Because:

```text
1, 2, 3, 4
```

## Pattern

```text
Hash set
```

## Brute Force

For every value, repeatedly search for the next value in the array.

This can result in O(n²).

## Optimal Solution

Put all values in a set.

Only start counting when the value has no predecessor.

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0

    for value in values:
        if value - 1 not in values:
            length = 1

            while value + length in values:
                length += 1

            best = max(best, length)

    return best
```

Complexity:

```text
Time: O(n) average
Space: O(n)
```

The total number of successful sequence-expansion checks remains linear across the set.

## Edge Cases

- Empty input
- Duplicate values
- Negative numbers
- Already sorted input
- One value

## Follow-Up Questions

### Q: Why don't we start a sequence from every number?

**Answer:** We only start at sequence beginnings. If `value - 1` exists, that value belongs to an earlier sequence
position.

### Q: What if sorting is allowed?

**Answer:** Sort and scan adjacent values. That costs O(n log n) time and can use less auxiliary data depending on the
implementation.

______________________________________________________________________

# Problem 6 — Valid Palindrome

## Problem

Determine whether a string is a palindrome after ignoring non-alphanumeric characters and case.

Example:

```text
"A man, a plan, a canal: Panama"

→ True
```

## Pattern

```text
Two pointers
```

## Brute Force

Normalize the string and compare it with its reverse.

```python
def is_palindrome_brute(s):
    normalized = "".join(
        char.lower()
        for char in s
        if char.isalnum()
    )

    return normalized == normalized[::-1]
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

## Optimal Solution

Use two pointers directly.

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1

        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
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

## Edge Cases

- Empty string
- Only punctuation
- One character
- Mixed case
- Spaces

## Follow-Up Questions

### Q: Why are two pointers useful?

**Answer:** They compare characters from both ends without constructing a normalized copy.

______________________________________________________________________

# Problem 7 — Container With Most Water

## Problem

Given heights representing vertical lines, find the maximum amount of water that can be contained between two lines.

Example:

```text
[1, 8, 6, 2, 5, 4, 8, 3, 7]

Output:
49
```

## Pattern

```text
Two pointers
```

## Brute Force

Try every pair.

```text
Time: O(n²)
```

## Optimal Solution

Start from both ends.

```python
def max_area(height):
    left = 0
    right = len(height) - 1
    best = 0

    while left < right:
        width = right - left
        area = min(height[left], height[right]) * width
        best = max(best, area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Key Insight

The shorter line limits the water height.

Moving the taller line while keeping the shorter line cannot improve the area because the width decreases and the
limiting height does not improve.

## Edge Cases

- Two elements
- Equal heights
- Increasing heights
- Decreasing heights

## Follow-Up Questions

### Q: Why move the shorter pointer?

**Answer:** The shorter side is the limiting factor. Moving the taller side cannot increase the minimum height, while
the width decreases.

______________________________________________________________________

# Problem 8 — Longest Substring Without Repeating Characters

## Problem

Find the length of the longest substring without repeating characters.

Example:

```text
"abcabcbb"

Output:
3
```

## Pattern

```text
Sliding window + set
```

## Brute Force

Generate substrings and check each one for duplicates.

This can be O(n²) or worse depending on implementation.

## Optimal Solution

```python
def length_of_longest_substring(s):
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

where `k` is the number of distinct characters.

## Edge Cases

- Empty string
- One character
- All unique
- All identical
- Unicode characters

## Follow-Up Questions

### Q: Can you optimize the left-pointer movement?

**Answer:** Yes. A dictionary can store the latest index of each character and move `left` directly past the previous
occurrence.

______________________________________________________________________

# Problem 9 — Valid Parentheses

## Problem

Given a string containing:

```text
()
[]
{}
```

determine whether the brackets are correctly balanced.

Example:

```text
"{[()]}"

→ True
```

## Pattern

```text
Stack
```

## Brute Force

Repeatedly remove matching adjacent pairs.

This is less efficient and less clean.

## Optimal Solution

```python
def is_valid_parentheses(s):
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

## Edge Cases

- Empty string
- Only opening brackets
- Only closing brackets
- Incorrect nesting
- Odd length

## Follow-Up Questions

### Q: Why is a stack appropriate?

**Answer:** The most recent unmatched opening bracket must be matched first, which is LIFO behavior.

______________________________________________________________________

# Problem 10 — Daily Temperatures

## Problem

Given daily temperatures, return how many days you must wait until a warmer temperature.

Example:

```text
[73, 74, 75, 71, 69, 72, 76, 73]

Output:
[1, 1, 4, 2, 1, 1, 0, 0]
```

## Pattern

```text
Monotonic stack
```

## Brute Force

For each day, scan forward until finding a warmer day.

```text
Time: O(n²)
```

## Optimal Solution

Keep indices whose warmer day has not yet been found.

```python
def daily_temperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i, temperature in enumerate(temperatures):
        while stack and temperature > temperatures[stack[-1]]:
            previous = stack.pop()
            result[previous] = i - previous

        stack.append(i)

    return result
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

Each index is pushed and popped at most once.

## Edge Cases

- Empty input
- One day
- Strictly increasing
- Strictly decreasing
- Equal temperatures

## Follow-Up Questions

### Q: Why is this O(n) despite the while loop?

**Answer:** Each index enters the stack once and leaves the stack once, so the total number of stack operations is
linear.

______________________________________________________________________

# Problem 11 — Reverse Linked List

## Problem

Reverse a singly linked list.

Example:

```text
1 → 2 → 3 → None

becomes

3 → 2 → 1 → None
```

## Pattern

```text
Pointer manipulation
```

## Brute Force

Copy values into another structure and create a reversed list.

This uses O(n) additional memory.

## Optimal Solution

```python
class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next


def reverse_list(head):
    previous = None
    current = head

    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node

    return previous
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Edge Cases

- Empty list
- One node
- Two nodes
- Long list

## Follow-Up Questions

### Q: Can you implement it recursively?

**Answer:** Yes, but recursion consumes O(n) call-stack space and is generally less attractive for very long Python
lists.

______________________________________________________________________

# Problem 12 — Linked List Cycle

## Problem

Determine whether a linked list contains a cycle.

## Pattern

```text
Fast/slow pointers
```

## Brute Force

Store visited node identities in a set.

```text
Time: O(n)
Space: O(n)
```

## Optimal Solution

```python
def has_cycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Edge Cases

- Empty list
- One node without cycle
- One node pointing to itself
- Cycle at head
- Cycle near the tail

## Follow-Up Questions

### Q: Why do the pointers eventually meet?

**Answer:** Once both pointers enter a cycle, the faster pointer gains one position relative to the slower pointer on
every iteration and eventually catches it.

______________________________________________________________________

# Problem 13 — Merge Two Sorted Lists

## Problem

Merge two sorted linked lists into one sorted linked list.

Example:

```text
1 → 3 → 5
2 → 4 → 6

→

1 → 2 → 3 → 4 → 5 → 6
```

## Pattern

```text
Two pointers
```

## Brute Force

Copy all values into a list, sort them and construct a linked list.

```text
Time: O((n+m) log(n+m))
Space: O(n+m)
```

## Optimal Solution

```python
def merge_two_lists(list1, list2):
    dummy = ListNode()
    current = dummy

    while list1 and list2:
        if list1.value <= list2.value:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    current.next = list1 or list2

    return dummy.next
```

Complexity:

```text
Time: O(n + m)
Space: O(1)
```

## Edge Cases

- Both lists empty
- One list empty
- Duplicate values
- Different lengths

## Follow-Up Questions

### Q: Why use a dummy node?

**Answer:** It avoids special handling for the first node and simplifies pointer management.

______________________________________________________________________

# Problem 14 — Binary Search

## Problem

Given a sorted array, return the index of a target value or `-1`.

Example:

```text
nums = [1, 3, 5, 7, 9]
target = 7

Output:
3
```

## Pattern

```text
Binary search
```

## Brute Force

Linear scan:

```text
Time: O(n)
```

## Optimal Solution

```python
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if nums[middle] == target:
            return middle

        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1
```

Complexity:

```text
Time: O(log n)
Space: O(1)
```

## Edge Cases

- Empty array
- One element
- Target at beginning
- Target at end
- Target absent
- Duplicate values

## Follow-Up Questions

### Q: How do you find the first occurrence?

**Answer:** Continue searching left after finding the target while recording the current answer.

### Q: What is the most common binary-search bug?

**Answer:** Incorrect boundary updates or mixing inclusive and exclusive interval conventions.

______________________________________________________________________

# Problem 15 — Number of Islands

## Problem

Given a grid containing land (`"1"`) and water (`"0"`), count the number of islands.

Adjacent land cells connected horizontally or vertically belong to the same island.

Example:

```text
1 1 0
1 0 0
0 0 1

→ 2 islands
```

## Pattern

```text
DFS/BFS + visited state
```

## Brute Force

Repeatedly inspect connected cells without marking them can revisit the same cells many times.

## Optimal Solution — DFS

```python
def num_islands(grid):
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    islands = 0

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or grid[row][col] != "1"
        ):
            return

        grid[row][col] = "0"

        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "1":
                islands += 1
                dfs(row, col)

    return islands
```

Complexity:

```text
Time: O(rows × cols)
Space: O(rows × cols) worst-case recursion/visited state
```

If modifying the input is not allowed, use a separate `visited` set.

## Edge Cases

- Empty grid
- All water
- All land
- One cell
- Irregular input should be clarified if constraints do not guarantee rectangular shape

## Follow-Up Questions

### Q: BFS instead of DFS?

**Answer:** Yes. Use a queue and process neighboring cells iteratively.

### Q: What if the grid is too large for recursion?

**Answer:** Use iterative DFS/BFS to avoid Python recursion-depth limitations.

______________________________________________________________________

# Problem 16 — Climbing Stairs

## Problem

You can climb either one or two steps at a time. Return the number of distinct ways to reach step `n`.

Example:

```text
n = 3

Ways:
1 + 1 + 1
1 + 2
2 + 1

Output:
3
```

## Pattern

```text
Dynamic programming
```

## Brute Force

Recursive enumeration branches into many repeated subproblems.

Without memoization it becomes exponential.

## Optimal Solution

```python
def climb_stairs(n):
    if n <= 2:
        return n

    previous_two = 1
    previous_one = 2

    for _ in range(3, n + 1):
        current = previous_one + previous_two
        previous_two = previous_one
        previous_one = current

    return previous_one
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Edge Cases

- `n = 1`
- `n = 2`
- Large `n`

## Follow-Up Questions

### Q: How does this relate to Fibonacci?

**Answer:** The recurrence has the same structure as Fibonacci because the ways to reach step `n` come from steps `n-1`
and `n-2`.

______________________________________________________________________

# Problem 17 — House Robber

## Problem

You are given the amount of money in each house. You cannot rob two adjacent houses. Find the maximum amount you can
rob.

Example:

```text
[2, 7, 9, 3, 1]

Output:
12
```

because:

```text
2 + 9 + 1 = 12
```

## Pattern

```text
1D dynamic programming
```

## Brute Force

At each house, choose:

```text
rob
or
skip
```

This creates repeated subproblems and can become exponential.

## Optimal Solution

At each position:

```text
rob current + best before previous
OR
skip current
```

```python
def rob(nums):
    previous_two = 0
    previous_one = 0

    for value in nums:
        current = max(
            previous_one,
            previous_two + value,
        )

        previous_two = previous_one
        previous_one = current

    return previous_one
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Edge Cases

- Empty list
- One house
- Two houses
- All zeroes
- Large values

## Follow-Up Questions

### Q: What is the DP state?

**Answer:** The running value represents the maximum amount that can be robbed from the houses processed so far.

### Q: What changes if houses are arranged in a circle?

**Answer:** You cannot rob both the first and last house. Solve two linear cases: exclude the first or exclude the last,
then take the maximum.

______________________________________________________________________

# Problem 18 — Jump Game

## Problem

Given an array where each value represents the maximum jump length from that position, determine whether the last index
is reachable.

Example:

```text
[2, 3, 1, 1, 4]

→ True
```

Example:

```text
[3, 2, 1, 0, 4]

→ False
```

## Pattern

```text
Greedy
```

This problem is included because recognizing that a problem does **not** need full DP is an important interview skill.

## Brute Force

Try every possible jump.

This can become exponential.

## Optimal Solution

Track the farthest reachable position.

```python
def can_jump(nums):
    farthest = 0

    for i, jump in enumerate(nums):
        if i > farthest:
            return False

        farthest = max(farthest, i + jump)

        if farthest >= len(nums) - 1:
            return True

    return True
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Edge Cases

- Empty input
- One element
- First element is zero
- Zero in the middle
- Last index already reachable

## Follow-Up Questions

### Q: Why is greedy sufficient?

**Answer:** At each position, only the farthest reachable index matters. Keeping a less-far reachable position cannot
improve the future reach beyond what the maximum reach already provides.

### Q: Is every jump problem greedy?

**Answer:** No. The constraints and objective determine whether greedy, DP, BFS or another approach is appropriate.

______________________________________________________________________

# Problem 19 — Minimum Size Subarray Sum

## Problem

Given an array of positive integers and a target, find the minimum-length contiguous subarray whose sum is at least the
target.

Example:

```text
target = 7
nums = [2, 3, 1, 2, 4, 3]

Output:
2
```

because:

```text
4 + 3 = 7
```

## Pattern

```text
Variable sliding window
```

## Brute Force

Check every possible subarray.

```text
Time: O(n²)
```

## Optimal Solution

```python
def min_subarray_len(target, nums):
    left = 0
    window_sum = 0
    best = float("inf")

    for right, value in enumerate(nums):
        window_sum += value

        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return 0 if best == float("inf") else best
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

## Important Constraint

The values must be positive for this simple sliding-window reasoning to work.

## Follow-Up Questions

### Q: What if negative numbers are allowed?

**Answer:** This sliding-window approach no longer has the required monotonic behavior. Prefix sums plus another
technique may be necessary.

______________________________________________________________________

# Problem 20 — Subarray Sum Equals K

## Problem

Given an integer array and target `k`, count the number of contiguous subarrays whose sum equals `k`.

Example:

```text
nums = [1, 1, 1]
k = 2

Output:
2
```

## Pattern

```text
Prefix sum + hash map
```

## Brute Force

Calculate every subarray sum.

```text
Time: O(n²)
```

## Optimal Solution

If current prefix sum is:

```text
current_sum
```

we need an earlier prefix sum:

```text
current_sum - k
```

```python
from collections import defaultdict

def subarray_sum(nums, k):
    counts = defaultdict(int)
    counts[0] = 1

    current_sum = 0
    result = 0

    for value in nums:
        current_sum += value

        result += counts[current_sum - k]
        counts[current_sum] += 1

    return result
```

Complexity:

```text
Time: O(n) average
Space: O(n)
```

## Edge Cases

- Negative values
- Zero values
- Empty input
- `k = 0`
- Repeated prefix sums

## Follow-Up Questions

### Q: Why does a normal sliding window not work?

**Answer:** Negative values can make the sum increase or decrease unpredictably when the window changes. Prefix sums
avoid relying on that monotonic property.

______________________________________________________________________

# 21. Mixed Pattern Practice

The following problems are useful after completing the core set.

Try identifying the pattern before looking at the answer.

| Problem | Primary Pattern |
|---|---|
| Product of Array Except Self | Prefix/Suffix |
| Best Time to Buy and Sell Stock | Sliding Window / Running Minimum |
| Merge Intervals | Sorting + Greedy |
| Search in Rotated Sorted Array | Binary Search |
| Kth Largest Element | Heap / Quickselect concept |
| Number of Connected Components | DFS/BFS |
| Lowest Common Ancestor | Tree DFS |
| Binary Tree Level Order Traversal | BFS |
| Coin Change | Dynamic Programming |
| Maximum Subarray | Dynamic Programming / Kadane |
| Longest Increasing Subsequence | Dynamic Programming concept |

These are deliberately kept as additional practice rather than full solutions in this file.

______________________________________________________________________

# 22. How to Practice These Problems

Use three passes.

## Pass 1 — Pattern Recognition

Read only the problem.

Write:

```text
Input:
Output:
Constraints:
Pattern:
```

Do not code immediately.

______________________________________________________________________

## Pass 2 — Implementation

Implement the solution without looking at the answer.

Then test:

```text
Normal case
Empty input
Smallest valid input
Boundary values
Duplicates
Negative values where applicable
```

______________________________________________________________________

## Pass 3 — Interview Explanation

Explain aloud:

```text
1. Brute force
2. Bottleneck
3. Pattern
4. Optimal approach
5. Correctness intuition
6. Complexity
7. Edge cases
```

You should be able to do this without reading the notes.

______________________________________________________________________

# 23. Interview Communication Template

For almost every coding problem, use this structure:

> "The straightforward solution is \_\_\_\_, which takes O(__) time. The bottleneck is \_\_\_\_. Because the input has \_\_ property, I can use \_\_ pattern. I will maintain __. Each element is processed \_\_ times, so the time complexity is O(__), with O(__) additional space."

Then code.

After coding:

> "Let me verify the empty case, the smallest input, duplicates/boundaries, and a normal example."

This makes your reasoning visible to the interviewer.

______________________________________________________________________

# 24. Complexity Summary

| Problem | Pattern | Time | Extra Space |
|---|---|---:|---:|
| Two Sum | Hash map | O(n) avg | O(n) |
| Contains Duplicate | Set | O(n) avg | O(n) |
| Group Anagrams | Hash map | O(nk log k) | O(nk) |
| Top K Frequent | Heap | O(n + m log k) | O(m + k) |
| Longest Consecutive | Set | O(n) avg | O(n) |
| Valid Palindrome | Two pointers | O(n) | O(1) |
| Container With Most Water | Two pointers | O(n) | O(1) |
| Longest Unique Substring | Sliding window | O(n) | O(k) |
| Valid Parentheses | Stack | O(n) | O(n) |
| Daily Temperatures | Monotonic stack | O(n) | O(n) |
| Reverse Linked List | Pointers | O(n) | O(1) |
| Linked List Cycle | Fast/slow | O(n) | O(1) |
| Merge Sorted Lists | Two pointers | O(n+m) | O(1) |
| Binary Search | Binary search | O(log n) | O(1) |
| Number of Islands | DFS/BFS | O(RC) | O(RC) worst case |
| Climbing Stairs | DP | O(n) | O(1) |
| House Robber | DP | O(n) | O(1) |
| Jump Game | Greedy | O(n) | O(1) |
| Minimum Size Subarray | Sliding window | O(n) | O(1) |
| Subarray Sum K | Prefix + hash map | O(n) avg | O(n) |

______________________________________________________________________

# 25. Follow-Up Topics to Revisit

Before an interview, make sure you can also explain:

- Why hashing is average O(1).
- When sorting enables two pointers.
- Why sliding window requires appropriate monotonic behavior.
- Why each element is pushed/popped once in a monotonic stack.
- Why BFS gives shortest paths in unweighted graphs.
- Why DFS does not generally guarantee shortest paths.
- Why binary search requires a monotonic property.
- Why Top-K can use O(n log k).
- Why prefix sums help with range/subarray problems.
- How memoization changes exponential recursion into a more efficient DP solution.
- Why some apparently DP problems have simpler greedy solutions.

______________________________________________________________________

# 26. Interview Questions & Answers

## Q1. Which DSA patterns are most important for backend interviews?

**Answer:**

The highest-value patterns for this preparation are hash maps/sets, two pointers, sliding windows, stacks, binary
search, BFS/DFS, Top-K with heaps, prefix/suffix techniques and basic dynamic programming.

______________________________________________________________________

## Q2. How do you decide between brute force and an optimized solution?

**Answer:**

First establish a correct brute-force approach, then identify repeated work or the dominant bottleneck. Use the input
constraints to determine whether optimization is necessary and which data structure or pattern removes the bottleneck.

______________________________________________________________________

## Q3. Why is Two Sum O(n) with a hash map?

**Answer:**

Each element is processed once and the required complement is checked using average O(1) hash-map lookup, giving O(n)
average total time.

______________________________________________________________________

## Q4. Why does sorting sometimes help?

**Answer:**

Sorting provides ordering that can enable two pointers, binary search, merging and other monotonic techniques. The
trade-off is typically O(n log n) sorting time.

______________________________________________________________________

## Q5. Why is the sliding-window approach for Longest Unique Substring O(n)?

**Answer:**

The right pointer moves forward at most n times and the left pointer also moves forward at most n times. Each character
is inserted and removed from the window a bounded number of times.

______________________________________________________________________

## Q6. Why is Daily Temperatures O(n) even though it has a nested while loop?

**Answer:**

Each index is pushed onto the monotonic stack once and popped at most once. Therefore the total stack operations are
O(n).

______________________________________________________________________

## Q7. Why does BFS find the shortest path in an unweighted graph?

**Answer:**

BFS explores nodes in increasing order of distance from the source. Therefore the first time a node is reached, it is
reached using the minimum number of edges.

______________________________________________________________________

## Q8. When would DFS be preferable to BFS?

**Answer:**

DFS is often convenient for connectivity, component discovery, recursive tree processing and exploration where shortest
distance is not the primary requirement.

______________________________________________________________________

## Q9. Why can binary search be O(log n)?

**Answer:**

Each iteration discards approximately half of the remaining search space.

______________________________________________________________________

## Q10. What is a monotonic condition?

**Answer:**

A condition where once it changes from false to true, it remains true, or vice versa. This structure enables binary
search over the answer space.

______________________________________________________________________

## Q11. Why is Top-K often O(n log k) instead of O(n log n)?

**Answer:**

A heap can retain only K candidates. Each of N elements requires at most O(log k) heap work rather than sorting all N
elements.

______________________________________________________________________

## Q12. Why does prefix sum help with subarray-sum problems?

**Answer:**

The sum of a range can be expressed as the difference between two prefix sums. A hash map can store previous prefix sums
so matching ranges can be found without repeatedly summing the same elements.

______________________________________________________________________

## Q13. Why does Subarray Sum Equals K work with negative numbers?

**Answer:**

The prefix-sum relationship does not depend on values being positive. We look for a previous prefix sum equal to
`current_sum - k`, so negative values are naturally supported.

______________________________________________________________________

## Q14. What is the difference between memoization and tabulation?

**Answer:**

Memoization is top-down recursion with cached states. Tabulation computes states bottom-up, usually with iteration.

______________________________________________________________________

## Q15. How do you recognize a DP problem?

**Answer:**

Look for repeated subproblems and a compact state that captures everything needed to determine the answer for a
subproblem.

______________________________________________________________________

## Q16. Why is Jump Game greedy instead of DP?

**Answer:**

For the standard version, only the farthest reachable position matters. Maintaining the maximum reach gives an O(n)
solution without storing a DP table.

______________________________________________________________________

## Q17. How would you handle a coding problem where you don't immediately know the pattern?

**Answer:**

I would clarify constraints, construct a brute-force solution, analyze what makes it expensive and look for repeated
work, ordering, contiguity, lookup, monotonicity, graph structure or overlapping subproblems. Those clues usually point
toward the appropriate pattern.

______________________________________________________________________

## Q18. What should you do if your optimal approach becomes complicated during an interview?

**Answer:**

Explain the trade-off, validate the simpler solution first and then improve it incrementally. A correct, well-explained
solution is better than an unverified optimization.

______________________________________________________________________

## Q19. How do you test DSA code during an interview?

**Answer:**

Start with a normal example, then test empty input, one element, minimum/maximum boundaries, duplicates, negative values
where relevant and cases where the answer does not exist.

______________________________________________________________________

## Q20. What does a strong senior-level coding explanation sound like?

**Answer:**

"I'll first establish the straightforward solution and its complexity. The expensive part is repeated lookup/scanning.
Because the input has this property, I can maintain this additional state using this data structure. That reduces the
repeated work from X to Y. I'll implement that, then verify edge cases and confirm the complexity."

______________________________________________________________________

# 27. Final Interview Readiness Checklist

Before moving to System Design Fundamentals, make sure you can solve or explain:

- [ ] Two Sum
- [ ] Contains Duplicate
- [ ] Group Anagrams
- [ ] Top K Frequent Elements
- [ ] Longest Consecutive Sequence
- [ ] Valid Palindrome
- [ ] Container With Most Water
- [ ] Longest Substring Without Repeating Characters
- [ ] Valid Parentheses
- [ ] Daily Temperatures
- [ ] Reverse Linked List
- [ ] Linked List Cycle
- [ ] Merge Two Sorted Lists
- [ ] Binary Search
- [ ] Number of Islands
- [ ] Climbing Stairs
- [ ] House Robber
- [ ] Jump Game
- [ ] Minimum Size Subarray Sum
- [ ] Subarray Sum Equals K
- [ ] Identify two-pointer problems.
- [ ] Identify sliding-window problems.
- [ ] Identify hash-map problems.
- [ ] Identify stack problems.
- [ ] Identify binary-search problems.
- [ ] Identify BFS/DFS problems.
- [ ] Identify Top-K problems.
- [ ] Identify prefix/suffix problems.
- [ ] Identify basic DP problems.
- [ ] Explain brute force.
- [ ] Explain the bottleneck.
- [ ] Explain the optimal approach.
- [ ] State time complexity.
- [ ] State space complexity.
- [ ] Discuss edge cases.
- [ ] Answer follow-up questions.

______________________________________________________________________

# 28. Final Takeaways

For this course, the target is not:

```text
"How many LeetCode problems did you solve?"
```

The target is:

```text
"Can you recognize the pattern and reason about the solution?"
```

If you can confidently move through:

```text
Problem
→ Constraints
→ Brute force
→ Bottleneck
→ Pattern
→ Data structure
→ Optimal solution
→ Complexity
→ Edge cases
→ Follow-up
```

you have the DSA foundation expected for this interview-preparation track.

The next topic moves from coding problems to **System Design Fundamentals**, where the focus shifts from individual
algorithms to designing reliable backend systems.

______________________________________________________________________

**Previous:** [36. DSA Interview Patterns](./36-dsa-patterns.md)

**Next:** [38. System Design Fundamentals](./38-system-design-fundamentals.md)
