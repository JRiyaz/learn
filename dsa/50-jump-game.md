# 50-jump-game.md

# Jump Game

> **🎯 Congratulations! This is the final lesson of your interview-focused DSA course.**
>
> Jump Game introduces one of the most powerful interview strategies:
>
> **Greedy Algorithms**
>
> Unlike Dynamic Programming, where we often remember many previous states, a Greedy algorithm makes the **best decision available at the current moment**.
>
> Surprisingly, this problem looks like DP, but the optimal solution is Greedy.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 25–35 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use this problem to evaluate:

- Greedy thinking
- Reachability
- Array traversal
- Optimization
- Choosing the simplest correct solution

This pattern appears in:

- Jump Game II
- Gas Station
- Partition Labels
- Task Scheduling
- Video Streaming Buffers
- Network Routing

______________________________________________________________________

# Problem Statement

You are given an array where each element represents the **maximum jump length** from that position.

Return `True` if you can reach the last index.

Otherwise,

return `False`.

______________________________________________________________________

## Example 1

Input

```text
[2,3,1,1,4]
```

Output

```text
True
```

Path

```text
0

↓

1

↓

4
```

Reached the end.

______________________________________________________________________

## Example 2

Input

```text
[3,2,1,0,4]
```

Output

```text
False
```

At index

```
3
```

Maximum jump

```
0
```

Cannot move further.

______________________________________________________________________

# Before Learning the Algorithm

Suppose

```text
2 3 1 1 4
```

Question

Should we try

every possible jump?

No.

Too many combinations.

Instead,

ask

> **What is the farthest position I can currently reach?**

That single question solves the problem.

______________________________________________________________________

# Backend Engineering Analogy

Imagine forwarding a request through multiple proxy servers.

Each proxy can forward the request only a certain distance.

Question

Can the request eventually reach the destination?

Instead of trying every path,

track

```
Farthest Reachable Server
```

Exactly the Jump Game idea.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Greedy**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Can reach?
- Minimum decisions
- Maximum reach
- Best local choice
- Feasibility

Think

```
Greedy
```

______________________________________________________________________

# Brute Force Solution

Try every jump.

Example

```text
2 3 1 1 4
```

Jump

```
1
```

or

```
2
```

Every branch creates more branches.

Recursive Tree

```text
0
├──1
│   ├──2
│   └──3
└──2
```

Very expensive.

______________________________________________________________________

## Complexity

Time

```
O(2ⁿ)
```

______________________________________________________________________

# Better Observation

At every position,

only one thing matters.

```
How far can I reach?
```

Not

```
Which path did I take?
```

______________________________________________________________________

# Key Insight

Maintain

```text
farthest_reachable
```

Initially

```text
0
```

For every index

If

```text
index > farthest_reachable
```

We cannot even reach this position.

Answer

```
False
```

Otherwise,

update

```text
farthest_reachable

=

max(

farthest_reachable,

index + nums[index]

)
```

If

```
farthest_reachable
```

reaches the last index,

we're done.

______________________________________________________________________

# Visual Explanation

Input

```text
2 3 1 1 4
```

Initially

```text
Reach = 0
```

Index

```
0
```

Jump

```
2
```

Reach

```
2
```

↓

Index

```
1
```

Reach

```
max(2,1+3)

=

4
```

Reached end.

Answer

```
True
```

______________________________________________________________________

# Step-by-Step Dry Run

Input

```text
3 2 1 0 4
```

______________________________________________________________________

Index

```
0
```

Reach

```
3
```

______________________________________________________________________

Index

```
1
```

Reach

```
3
```

______________________________________________________________________

Index

```
2
```

Reach

```
3
```

______________________________________________________________________

Index

```
3
```

Jump

```
0
```

Reach

```
3
```

______________________________________________________________________

Next

Index

```
4
```

Need

Reach

```
4
```

But

Current Reach

```
3
```

Cannot reach.

Answer

```
False
```

______________________________________________________________________

# Why This Works

Loop Invariant

> Before processing index `i`,
> `farthest_reachable` stores the farthest index that can be reached using any valid jumps from the positions already processed.

If

```
i > farthest_reachable
```

then no previous jump can reach `i`.

Therefore,

the end is impossible to reach.

______________________________________________________________________

# Why Isn't DP Needed?

A common first thought:

```
DP[i]

=

Can Reach i?
```

Works.

But unnecessary.

We don't need to know

every reachable position.

Only the

```
Farthest Reach
```

matters.

Greedy wins.

______________________________________________________________________

# Edge Cases

### Empty Array

Usually treated as already reachable.

Return

```
True
```

(if allowed by problem definition).

______________________________________________________________________

### One Element

Already at destination.

Return

```
True
```

______________________________________________________________________

### Starts with Zero

```text
0 2 3
```

Cannot move.

Return

```
False
```

unless the array has only one element.

______________________________________________________________________

### Large Jump

```text
10 0 0 0
```

Immediately reaches the end.

______________________________________________________________________

# Complexity Analysis

Every element is processed once.

Time

```
O(n)
```

Space

```
O(1)
```

Optimal.

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def can_jump(numbers: List[int]) -> bool:
    farthest_reachable = 0

    for index, jump_length in enumerate(numbers):
        if index > farthest_reachable:
            return False

        farthest_reachable = max(
            farthest_reachable,
            index + jump_length,
        )

        if farthest_reachable >= len(numbers) - 1:
            return True

    return True
```

______________________________________________________________________

# DP Solution (For Learning)

```python
from typing import List


def can_jump(numbers: List[int]) -> bool:
    reachable = [False] * len(numbers)
    reachable[0] = True

    for index in range(len(numbers)):
        if not reachable[index]:
            continue

        for jump in range(1, numbers[index] + 1):
            if index + jump < len(numbers):
                reachable[index + jump] = True

    return reachable[-1]
```

______________________________________________________________________

# Why Greedy Is Better

DP

```text
Tracks

Every Reachable Position
```

Greedy

```text
Tracks

Only

Farthest Reach
```

Less memory.

Less work.

Cleaner solution.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Trying every possible jump.

This leads to exponential complexity.

______________________________________________________________________

## Mistake 2

Stopping when a zero appears.

A zero isn't necessarily bad.

A previous jump may skip over it.

Example

```text
3 0 0 0
```

Still reachable.

______________________________________________________________________

## Mistake 3

Updating the reach incorrectly.

Always use

```python
max(current_reach, index + jump)
```

______________________________________________________________________

## Mistake 4

Thinking Dynamic Programming is always required.

Sometimes Greedy is both simpler and optimal.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Instead of exploring every jump, I'll keep track of the farthest index that can be reached so far. As I iterate through the array, if I encounter an index beyond my current reach, I know it's impossible to continue. Otherwise, I'll update the farthest reachable position. This greedy strategy processes the array once and guarantees the correct answer."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is Greedy correct?**

Because only the farthest reachable index affects future possibilities.

______________________________________________________________________

**Q. Why not use DP?**

DP stores more information than necessary.

The farthest reachable position completely summarizes the required state.

______________________________________________________________________

**Q. What changes in Jump Game II?**

Instead of asking

"Can we reach?"

we ask

"What's the minimum number of jumps?"

That requires a different greedy strategy.

______________________________________________________________________

**Q. Where is this pattern used?**

- Routing
- Streaming
- Resource allocation
- Interval coverage
- Scheduling

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Greedy |
| Recognition | Maximum Reach |
| State | Farthest Reachable Index |
| Brute Force | Recursion |
| Better | DP |
| Best | Greedy |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Track the farthest reachable index.
- If the current index is beyond that reach, return `False`.
- Update reach using `max(reach, index + jump)`.
- Stop early if the last index becomes reachable.
- Greedy is optimal.
- DP also works but is unnecessary.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Jump Game II (Read the problem only)
1. Can Place Flowers
1. Lemonade Change

______________________________________________________________________

## Medium

4. Gas Station
1. Partition Labels
1. Minimum Number of Arrows to Burst Balloons
1. Non-overlapping Intervals

______________________________________________________________________

## Hard (Optional)

8. Candy
1. Minimum Refueling Stops
1. Course Schedule III

______________________________________________________________________

# Key Takeaway

The biggest lesson from Jump Game is learning **when not to use Dynamic Programming**. Although the problem appears to
involve many choices, all the information we need can be summarized by a single value: **the farthest reachable index**.
Recognizing when a simple greedy invariant is sufficient is a valuable interview skill and often leads to cleaner, more
efficient solutions.

______________________________________________________________________

# 🎉 Congratulations!

You have completed the **50-lesson DSA Interview Course** designed specifically for:

- Backend Software Engineers
- Startup interviews
- Mid-sized product companies
- Python developers
- Engineers targeting strong Easy and Medium problem-solving skills

You now have exposure to the core interview patterns:

| Category | Core Pattern |
|----------|--------------|
| Math | Number Manipulation |
| Arrays | Traversal & Simulation |
| Strings | Two Pointers |
| Hash Maps | Counting & Lookup |
| Two Pointers | Bidirectional Traversal |
| Sliding Window | Dynamic Range |
| Stack | LIFO Processing |
| Queue | FIFO Processing |
| Linked List | Pointer Manipulation |
| Binary Search | Search Space Reduction |
| Sorting | Divide & Conquer |
| Trees | DFS / BFS / Recursion |
| Heap | Priority Queue |
| Graph | Connected Components |
| Dynamic Programming | State Transition |
| Greedy | Local Optimal Choice |

______________________________________________________________________

# What's Next? (Highly Recommended)

To make this course even more valuable, I recommend creating these companion Markdown files:

1. **51-dsa-pattern-cheatsheet.md** – One-page summary of every DSA pattern.
1. **52-time-and-space-complexity-cheatsheet.md** – Big-O reference for data structures and algorithms.
1. **53-problem-pattern-recognition-guide.md** – "If you see X in a problem, think Y."
1. **54-common-dsa-mistakes.md** – Off-by-one errors, recursion mistakes, binary search bugs, pointer pitfalls, etc.
1. **55-curated-practice-roadmap.md** – A structured list of 75–100 practice problems grouped by pattern and difficulty.

These five files will make revision much faster before interviews and help connect all the concepts you've learned.
