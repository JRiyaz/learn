# 43-binary-tree-level-order-traversal.md

# Binary Tree Level Order Traversal

> **🎯 This lesson teaches one of the most frequently asked Tree interview problems.**
>
> While the previous lesson introduced **BFS (Breadth First Search)**, this lesson focuses on using BFS to process a tree **level by level**.
>
> This pattern appears in dozens of interview questions.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–30 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use this problem to test whether you understand:

- Queue operations
- Breadth First Search (BFS)
- Tree traversal
- Level-based processing
- Queue size technique

Mastering this pattern helps solve:

- Zigzag Level Order Traversal
- Right Side View
- Average of Levels
- Minimum Depth
- Maximum Width
- Cousins in Binary Tree

______________________________________________________________________

# Problem Statement

Given the root of a binary tree,

return the nodes **level by level**.

Nodes on the same level should be grouped together.

______________________________________________________________________

## Example

Input

```text
          3
        /   \
       9     20
            /  \
          15    7
```

Output

```python
[
    [3],
    [9, 20],
    [15, 7],
]
```

______________________________________________________________________

# Before Learning the Algorithm

In the previous lesson,

we learned BFS.

But BFS returned

```text
3

9

20

15

7
```

Question:

How do we know

```
9

20
```

belong to the same level?

Need a way to process

**one level at a time.**

______________________________________________________________________

# Backend Engineering Analogy

Imagine a company hierarchy.

```text
CEO

↓

Managers

↓

Engineers

↓

Interns
```

Suppose HR wants to email

every level separately.

Process:

```
CEO

↓

Managers

↓

Engineers
```

Exactly Level Order Traversal.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Breadth First Search (Level-by-Level)**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Level
- Depth
- Floor
- Distance
- Layer
- Breadth

Think

```
Queue

+

BFS
```

______________________________________________________________________

# Brute Force Solution

A beginner might try:

```
Find height.

↓

Visit each level separately.
```

For every level,

run another DFS.

______________________________________________________________________

Example

Height

```
3
```

Visit

```
Level 1
```

↓

```
Level 2
```

↓

```
Level 3
```

Works,

but inefficient.

______________________________________________________________________

## Complexity

Height

```
h
```

Each DFS

```
O(n)
```

Overall

```
O(n²)
```

Worst case.

______________________________________________________________________

# Better Observation

BFS already visits nodes level by level.

We simply need to know:

> **Where does one level end?**

______________________________________________________________________

# Key Insight

Before processing a level,

record

```python
level_size = len(queue)
```

This tells us

exactly how many nodes belong to the current level.

Process exactly those nodes.

Children automatically belong to the next level.

______________________________________________________________________

# Visual Explanation

Tree

```text
          3
        /   \
       9     20
            /  \
          15    7
```

Queue

```text
[3]
```

Level Size

```
1
```

Process

```
3
```

Add children

```text
9

20
```

Queue

```text
[9,20]
```

______________________________________________________________________

Next

Level Size

```
2
```

Process

```
9

20
```

Add

```
15

7
```

Queue

```text
[15,7]
```

______________________________________________________________________

Next

Level Size

```
2
```

Process

```
15

7
```

Done.

______________________________________________________________________

# Step-by-Step Dry Run

Tree

```text
          3
        /   \
       9     20
            /  \
          15    7
```

______________________________________________________________________

### Level 1

Queue

```
3
```

Result

```python
[
    [3]
]
```

______________________________________________________________________

### Level 2

Queue

```
9

20
```

Result

```python
[
    [3],
    [9,20],
]
```

______________________________________________________________________

### Level 3

Queue

```
15

7
```

Result

```python
[
    [3],
    [9,20],
    [15,7],
]
```

Done.

______________________________________________________________________

# Why Queue Size Works

Suppose queue contains

```text
9

20
```

Current size

```
2
```

These are exactly the nodes belonging to this level.

While processing them,

their children get added.

Those children belong to

the next level,

not the current one.

______________________________________________________________________

# Why This Works

Loop Invariant

> Before each outer loop iteration,
>
> the queue contains **all nodes of exactly one level**, and no nodes from earlier levels.

During the iteration:

- Process exactly `level_size` nodes.
- Add their children.

When finished,

the queue contains exactly the next level.

______________________________________________________________________

# Edge Cases

### Empty Tree

```text
None
```

Return

```python
[]
```

______________________________________________________________________

### One Node

```text
1
```

Return

```python
[[1]]
```

______________________________________________________________________

### Left-Skewed Tree

```text
1
|
2
|
3
```

Output

```python
[[1],[2],[3]]
```

______________________________________________________________________

### Right-Skewed Tree

Works correctly.

______________________________________________________________________

### Complete Tree

Works correctly.

______________________________________________________________________

# Complexity Analysis

Every node

- Enqueued once
- Dequeued once

Time

```
O(n)
```

Space

Queue stores one level.

Worst case

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if root is None:
        return []

    result: List[List[int]] = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level: List[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.value)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result
```

______________________________________________________________________

# Dry Run of the Code

Initial

```text
Queue

[3]
```

Loop

```
Size = 1
```

Process

```
3
```

Queue

```text
[9,20]
```

Append

```python
[3]
```

______________________________________________________________________

Loop

```
Size = 2
```

Process

```
9

20
```

Queue

```text
[15,7]
```

Append

```python
[9,20]
```

Continue.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using DFS.

DFS doesn't naturally process nodes level by level.

______________________________________________________________________

## Mistake 2

Using

```python
while queue:
    node = queue.popleft()
```

without recording `level_size`.

You'll lose level boundaries.

______________________________________________________________________

## Mistake 3

Computing `len(queue)` inside the inner loop.

The queue size changes as children are added.

Always save it before the loop starts.

______________________________________________________________________

## Mistake 4

Appending children before removing the current node.

Always process the current node first.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Since the problem asks for nodes level by level, I'll use Breadth First Search with a queue. Before processing each level, I'll record the current queue size. That tells me exactly how many nodes belong to this level. While processing those nodes, I'll enqueue their children. After processing `level_size` nodes, I append the collected values as one level in the result."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why not DFS?**

DFS explores depth first.

The problem requires breadth-first traversal.

______________________________________________________________________

**Q. Why store `level_size` first?**

Because the queue grows while processing the current level.

______________________________________________________________________

**Q. Why use a queue instead of a stack?**

Queues preserve FIFO order,

which is required for BFS.

______________________________________________________________________

**Q. Where is this used in backend systems?**

- Organization charts
- Network routing
- Graph traversal
- Job dependency levels
- File system exploration

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Breadth First Search |
| Data Structure | Queue |
| Recognition | Level / Layer / Depth |
| Brute Force | DFS Per Level |
| Optimized | BFS with Queue Size |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Use BFS.
- Maintain a queue.
- Save the queue size before each level.
- Process exactly that many nodes.
- Add children to the queue.
- Append the current level to the result.
- Each node is visited once.
- Time complexity is O(n).

______________________________________________________________________

# Practice Questions

## Easy

1. Average of Levels in Binary Tree
1. Binary Tree Right Side View
1. Minimum Depth of Binary Tree

______________________________________________________________________

## Medium

4. Binary Tree Zigzag Level Order Traversal
1. Populating Next Right Pointers
1. Binary Tree Vertical Order Traversal
1. Maximum Width of Binary Tree

______________________________________________________________________

## Hard (Optional)

8. Serialize and Deserialize Binary Tree
1. Vertical Traversal of a Binary Tree
1. N-ary Tree Level Order Traversal

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **BFS naturally processes data level by level**. The simple trick of
storing the **queue size before processing a level** is one of the most reusable interview techniques for tree problems.
Once you master this pattern, many BFS tree questions become almost identical.

______________________________________________________________________

# Next

[44-maximum-depth-of-binary-tree.md](44-maximum-depth-of-binary-tree.md)
