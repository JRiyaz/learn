# 45-same-tree-and-invert-binary-tree.md

# Same Tree & Invert Binary Tree

> **🎯 These are two of the most common "recursion on trees" interview problems.**
>
> They look different, but both teach the same core skill:
>
> **Thinking recursively about tree structure instead of individual nodes.**
>
> After this lesson, you'll be able to solve many recursive tree comparison and tree transformation problems.

______________________________________________________________________

# Interview Confidence

| Item | Same Tree | Invert Binary Tree |
|------|-----------|--------------------|
| Difficulty | Easy | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Importance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 20 min | 20 min |
| Revision Time | 15 min | 15 min |

______________________________________________________________________

# Why Interviewers Ask These Problems

These questions test whether you understand:

- Recursive thinking
- Tree structure
- Base cases
- Tree traversal
- Returning information from recursion
- Modifying trees safely

These ideas are reused in:

- Symmetric Tree
- Subtree of Another Tree
- Lowest Common Ancestor
- Serialize / Deserialize
- Clone Tree
- Tree Dynamic Programming

______________________________________________________________________

# Part 1 — Same Tree

______________________________________________________________________

# Problem Statement

Given the roots of two binary trees,

determine whether they are **identical**.

Two trees are identical if:

- Their structure is the same.
- Every corresponding node has the same value.

______________________________________________________________________

## Example 1

```text
Tree A

      1
     / \
    2   3
```

```text
Tree B

      1
     / \
    2   3
```

Output

```text
True
```

______________________________________________________________________

## Example 2

```text
Tree A

      1
     /
    2
```

```text
Tree B

      1
       \
        2
```

Output

```text
False
```

Different structure.

______________________________________________________________________

## Example 3

```text
Tree A

      1
     / \
    2   3
```

```text
Tree B

      1
     / \
    2   4
```

Output

```text
False
```

Different value.

______________________________________________________________________

# Simple English

Imagine comparing two folders.

Both must have:

- Same folder structure
- Same file names

If anything differs,

they aren't identical.

Exactly the same idea.

______________________________________________________________________

# Backend Engineering Analogy

Suppose two servers return JSON.

Server A

```json
{
  "user": {
    "name": "Alice"
  }
}
```

Server B

```json
{
  "user": {
    "name": "Alice"
  }
}
```

Need to compare

- Structure
- Values

Exactly Same Tree.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Recursive Tree Comparison**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Compare trees
- Identical
- Equal structure
- Same hierarchy

Think

```
Compare

↓

Left

↓

Right
```

______________________________________________________________________

# Brute Force Solution

Convert both trees into arrays using preorder traversal.

Compare arrays.

Works.

But unnecessary.

Also fails unless null children are encoded.

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Better Observation

Trees are recursive.

If

```
Root
```

matches,

simply compare

```
Left

and

Right
```

______________________________________________________________________

# Recursive Formula

Two trees are equal if:

```text
Root Values Equal

AND

Left Trees Equal

AND

Right Trees Equal
```

______________________________________________________________________

# Base Cases

Both None

↓

```text
True
```

______________________________________________________________________

One None

↓

```text
False
```

______________________________________________________________________

Values Different

↓

```text
False
```

______________________________________________________________________

# Visual Explanation

```text
      1              1
     / \            / \
    2   3          2   3
```

Compare

```
1 == 1

↓

True
```

↓

Compare Left

```
2 == 2
```

↓

Compare Right

```
3 == 3
```

↓

True

______________________________________________________________________

# Dry Run

Tree

```text
      1
     / \
    2   3
```

vs

```text
      1
     / \
    2   3
```

Root

```
Equal
```

↓

Left

```
Equal
```

↓

Right

```
Equal
```

↓

Answer

```
True
```

______________________________________________________________________

# Production-Quality Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def is_same_tree(
    first: Optional[TreeNode],
    second: Optional[TreeNode],
) -> bool:
    if first is None and second is None:
        return True

    if first is None or second is None:
        return False

    if first.value != second.value:
        return False

    return (
        is_same_tree(first.left, second.left)
        and is_same_tree(first.right, second.right)
    )
```

______________________________________________________________________

# Why This Works

Loop (Recursive) Invariant

> When the recursive call returns,
> it correctly determines whether the corresponding subtrees are identical.

If every subtree matches,

the entire tree matches.

______________________________________________________________________

# Complexity

Time

```
O(n)
```

Space

```
O(h)
```

Recursive stack.

______________________________________________________________________

# Common Mistakes

- Comparing only values.
- Ignoring structure.
- Forgetting the `None` base cases.
- Returning `OR` instead of `AND`.

______________________________________________________________________

# Part 2 — Invert Binary Tree

______________________________________________________________________

# Problem Statement

Given a binary tree,

invert it.

Swap every node's

```
Left

↓

Right
```

______________________________________________________________________

## Example

Input

```text
        4
      /   \
     2     7
    / \   / \
   1  3  6   9
```

Output

```text
        4
      /   \
     7     2
    / \   / \
   9  6  3   1
```

______________________________________________________________________

# Simple English

Imagine looking at a tree in a mirror.

Everything on the left moves to the right.

Everything on the right moves to the left.

______________________________________________________________________

# Backend Engineering Analogy

Suppose a UI layout stores widgets as a tree.

Switching from

Left-to-Right

to

Right-to-Left

requires recursively swapping child components.

Exactly this algorithm.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Recursive Tree Transformation**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Mirror
- Reverse Tree
- Flip Tree
- Swap Children

Think

```
Swap

↓

Left

↓

Right
```

______________________________________________________________________

# Brute Force Solution

Create an entirely new mirrored tree.

Works,

but wastes memory.

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Better Observation

Simply swap child pointers.

No new tree required.

______________________________________________________________________

# Key Insight

At every node

Swap

```text
Left

↓

Right
```

Then recursively invert both children.

______________________________________________________________________

# Visual Explanation

Before

```text
      4
     / \
    2   7
```

Swap

```text
      4
     / \
    7   2
```

Continue recursively.

______________________________________________________________________

# Step-by-Step Dry Run

Initial

```text
        4
      /   \
     2     7
```

Swap

↓

```text
        4
      /   \
     7     2
```

Invert

```
7
```

↓

Invert

```
2
```

Done.

______________________________________________________________________

# Recursive Formula

```text
Invert(node)

↓

Swap children

↓

Invert(left)

↓

Invert(right)
```

______________________________________________________________________

# Why This Works

Recursive Invariant

> After `invert(node)` returns,
> the subtree rooted at `node` is completely mirrored.

Every node performs one swap.

Eventually,

every subtree becomes mirrored.

Therefore,

the whole tree becomes mirrored.

______________________________________________________________________

# Production-Quality Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def invert_tree(
    root: Optional[TreeNode],
) -> Optional[TreeNode]:
    if root is None:
        return None

    root.left, root.right = root.right, root.left

    invert_tree(root.left)
    invert_tree(root.right)

    return root
```

______________________________________________________________________

# Can BFS Also Solve It?

Yes.

Instead of recursion,

use a queue.

For every node

```
Dequeue

↓

Swap children

↓

Enqueue children
```

Also

```
O(n)
```

______________________________________________________________________

# BFS Solution

```python
from collections import deque
from typing import Optional


def invert_tree(
    root: Optional[TreeNode],
) -> Optional[TreeNode]:
    if root is None:
        return None

    queue = deque([root])

    while queue:
        node = queue.popleft()

        node.left, node.right = node.right, node.left

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return root
```

______________________________________________________________________

# Edge Cases

### Empty Tree

Return

```
None
```

______________________________________________________________________

### One Node

No changes.

______________________________________________________________________

### Left-Skewed Tree

Becomes

Right-Skewed.

______________________________________________________________________

### Right-Skewed Tree

Becomes

Left-Skewed.

______________________________________________________________________

# Complexity Analysis

## Same Tree

Time

```
O(n)
```

Space

```
O(h)
```

______________________________________________________________________

## Invert Tree

Time

```
O(n)
```

Space

Recursive

```
O(h)
```

BFS

```
O(n)
```

______________________________________________________________________

# Common Mistakes

## Same Tree

- Ignoring `None`.
- Comparing only values.
- Forgetting to compare both subtrees.

______________________________________________________________________

## Invert Tree

- Forgetting to recurse after swapping.
- Creating unnecessary nodes.
- Returning nothing.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process (Same Tree)

> "Two trees are identical only if their current nodes match, their left subtrees match, and their right subtrees match. Since every subtree is itself a tree, recursion naturally fits the problem."

______________________________________________________________________

### Expected Thought Process (Invert Tree)

> "To mirror a tree, every node simply swaps its left and right children. After swapping the current node, I recursively invert both subtrees. Every node performs exactly one swap."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is recursion natural here?**

Because every subtree is itself a binary tree.

______________________________________________________________________

**Q. Can both problems be solved iteratively?**

Yes.

Using BFS with a queue or DFS with a stack.

______________________________________________________________________

**Q. Why doesn't Invert Tree require extra memory?**

We modify the existing pointers instead of creating new nodes.

______________________________________________________________________

# Pattern Summary

| Problem | Pattern | Time | Space |
|----------|---------|------|--------|
| Same Tree | Recursive Comparison | O(n) | O(h) |
| Invert Tree | Recursive Transformation | O(n) | O(h) |

______________________________________________________________________

# Quick Revision

- Same Tree compares structure and values.
- Base cases are critical.
- Invert Tree swaps left and right children.
- Both use recursion naturally.
- Every node is visited exactly once.
- Both have O(n) time complexity.
- Recursive stack uses O(h) space.

______________________________________________________________________

# Practice Questions

## Easy

1. Symmetric Tree
1. Subtree of Another Tree
1. Merge Two Binary Trees

______________________________________________________________________

## Medium

4. Lowest Common Ancestor of a Binary Tree
1. Binary Tree Pruning
1. Delete Leaves With a Given Value
1. Construct Binary Tree from Traversals

______________________________________________________________________

## Hard (Optional)

8. Serialize and Deserialize Binary Tree
1. Recover Binary Search Tree
1. Binary Tree Maximum Path Sum

______________________________________________________________________

# Key Takeaway

The biggest lesson from these problems is that **trees are recursive structures**. Instead of trying to solve the entire
tree at once, solve the same problem for the left subtree and the right subtree, then combine the results. Whether
you're **comparing trees (Same Tree)** or **transforming trees (Invert Tree)**, this recursive mindset is one of the
most valuable skills for tree interviews.

______________________________________________________________________

# Next

[46-top-k-frequent-elements.md](46-top-k-frequent-elements.md)
