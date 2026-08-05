# 44-maximum-depth-of-binary-tree.md

# Maximum Depth of Binary Tree

> **🎯 This is the most important recursion problem for Trees.**
>
> Almost every tree interview eventually asks a variation of:
>
> - Height of Tree
> - Maximum Depth
> - Minimum Depth
> - Diameter
> - Balanced Tree
>
> Understanding this lesson will make many advanced tree problems much easier.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers want to test whether you understand:

- Tree recursion
- Divide and Conquer
- Recursive return values
- Bottom-up computation
- Base cases

This pattern is reused in:

- Balanced Binary Tree
- Diameter of Binary Tree
- Lowest Common Ancestor
- Path Sum
- Tree Dynamic Programming

______________________________________________________________________

# Problem Statement

Given the root of a binary tree,

return its **maximum depth**.

The maximum depth is the number of nodes along the **longest path** from the root to any leaf.

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

```text
3
```

Because the longest path is

```text
3 → 20 → 15
```

or

```text
3 → 20 → 7
```

Both contain

```
3
```

nodes.

______________________________________________________________________

# Before Learning the Algorithm

Suppose someone asks:

> "How tall is this tree?"

Would you count every node?

No.

Instead,

compare the height of the left subtree

and

the height of the right subtree.

Take the larger one.

Add one for the current node.

That's the entire algorithm.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a company's reporting hierarchy.

```text
CEO
│
├── VP
│   ├── Manager
│   │   └── Engineer
│   └── Manager
└── VP
```

Question:

What's the deepest reporting chain?

Exactly the same problem.

Other examples:

- Nested folders
- JSON depth
- Expression trees
- Dependency chains

______________________________________________________________________

# Pattern Recognition

## Pattern

**Tree Recursion (Postorder Thinking)**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Height
- Maximum depth
- Longest path from root
- Tree height

Think

```text
Answer(node)

=

1 + max(
    Answer(left),
    Answer(right)
)
```

______________________________________________________________________

# Brute Force Solution

A beginner might think:

1. Store every root-to-leaf path.
1. Measure every path.
1. Return the largest.

Example

```text
1 → 2 → 4
```

Length

```
3
```

Another path

```text
1 → 3
```

Length

```
2
```

Take maximum.

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

Potentially

```
O(n)
```

or more,

because entire paths are stored.

Works,

but unnecessary.

______________________________________________________________________

# Better Observation

We don't need every path.

We only need the

```
Longest
```

one.

Each subtree can answer:

> "What is your height?"

The parent simply takes

```
Maximum
```

______________________________________________________________________

# Key Insight

Suppose the tree is

```text
          1
        /   \
       2     3
      /
     4
```

Node

```
4
```

has height

```
1
```

Node

```
2
```

asks

```
Left = 1

Right = 0
```

Returns

```
2
```

Root asks

```
Left = 2

Right = 1
```

Returns

```
3
```

Done.

______________________________________________________________________

# Why Bottom-Up?

Notice

The root cannot compute its height

until both children finish.

Therefore,

the computation flows

```
Leaves

↓

Parents

↓

Root
```

This is

**Postorder Thinking**

even though we don't explicitly perform a Postorder traversal.

______________________________________________________________________

# Visual Explanation

```text
          1
        /   \
       2     3
      /
     4
```

Leaf

```
4

↓

Height = 1
```

↓

Node

```
2

↓

1 + max(1,0)

=

2
```

↓

Root

```
1 + max(2,1)

=

3
```

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

Visit

```
9
```

Height

```
1
```

______________________________________________________________________

Visit

```
15
```

Height

```
1
```

______________________________________________________________________

Visit

```
7
```

Height

```
1
```

______________________________________________________________________

Node

```
20
```

Left

```
1
```

Right

```
1
```

Return

```
2
```

______________________________________________________________________

Root

```
3
```

Left

```
1
```

Right

```
2
```

Return

```
3
```

Answer.

______________________________________________________________________

# Why This Works

Loop Invariant (Recursive Invariant)

> When a recursive call returns,
> it returns the correct maximum depth of that subtree.

At every node,

we combine the already-correct answers from the left and right subtrees.

Since every subtree is solved correctly,

the root's answer is also correct.

______________________________________________________________________

# Recursive Formula

For every node

```text
Depth(node)

=

1 + max(
    Depth(left),
    Depth(right)
)
```

Base Case

```text
Depth(None)

=

0
```

This formula alone solves the entire problem.

______________________________________________________________________

# Can We Solve It Using BFS?

Yes.

Count levels.

Every level processed

↓

Depth +1

Example

```text
Level 1

3
```

↓

```text
Level 2

9

20
```

↓

```text
Level 3

15

7
```

Answer

```
3
```

Works,

but recursion is simpler.

______________________________________________________________________

# Edge Cases

### Empty Tree

```text
None
```

Depth

```
0
```

______________________________________________________________________

### One Node

```text
1
```

Depth

```
1
```

______________________________________________________________________

### Left-Skewed Tree

```text
1
|
2
|
3
|
4
```

Depth

```
4
```

______________________________________________________________________

### Right-Skewed Tree

Same idea.

______________________________________________________________________

### Balanced Tree

Works correctly.

______________________________________________________________________

# Complexity Analysis

Every node is visited exactly once.

Time

```
O(n)
```

______________________________________________________________________

Space

Recursive call stack.

Balanced tree

```
O(log n)
```

Worst case

(skewed tree)

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

## Recursive Solution (Recommended)

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)

    return 1 + max(left_depth, right_depth)
```

______________________________________________________________________

## BFS Solution

```python
from collections import deque
from typing import Optional


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    queue = deque([root])
    depth = 0

    while queue:
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        depth += 1

    return depth
```

______________________________________________________________________

# Recursive Call Stack Visualization

Tree

```text
      1
     /
    2
   /
  3
```

Calls

```text
Depth(1)

↓

Depth(2)

↓

Depth(3)

↓

Depth(None)
```

Returns

```text
0

↓

1

↓

2

↓

3
```

Notice

Information flows upward.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Returning

```python
max(left, right)
```

instead of

```python
1 + max(left, right)
```

Don't forget the current node.

______________________________________________________________________

## Mistake 2

Returning

```
1
```

for

```
None
```

Empty trees have depth

```
0
```

______________________________________________________________________

## Mistake 3

Thinking recursion visits parents first.

The useful computation happens

after children return.

______________________________________________________________________

## Mistake 4

Confusing

Depth

with

Number of Edges.

LeetCode defines depth as

```
Number of Nodes
```

Always verify the problem statement.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The maximum depth of a tree depends on the maximum depth of its left and right subtrees. I'll recursively compute both depths, take the larger one, and add one for the current node. The base case is an empty node, whose depth is zero."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is recursion natural here?**

Each subtree is itself a binary tree.

The same function solves smaller versions of the problem.

______________________________________________________________________

**Q. Why add one?**

To count the current node.

______________________________________________________________________

**Q. Can BFS solve this?**

Yes.

Count the number of levels processed.

______________________________________________________________________

**Q. Where is this used in backend systems?**

- Folder hierarchies
- JSON nesting
- Dependency graphs
- Organization trees
- AST depth analysis

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Tree Recursion |
| Formula | 1 + max(left, right) |
| Base Case | None → 0 |
| Alternative | BFS (Count Levels) |
| Time | O(n) |
| Space | O(h) |

______________________________________________________________________

# Quick Revision

- Maximum depth means the longest root-to-leaf path.
- Every subtree solves the same problem.
- Base case: `None → 0`.
- Return `1 + max(left, right)`.
- Uses postorder-style recursion.
- Every node is visited once.
- Time complexity is O(n).
- Space complexity is O(h).

______________________________________________________________________

# Practice Questions

## Easy

1. Minimum Depth of Binary Tree
1. Balanced Binary Tree
1. Same Tree

______________________________________________________________________

## Medium

4. Diameter of Binary Tree
1. Path Sum II
1. Binary Tree Maximum Path Sum
1. Longest Univalue Path

______________________________________________________________________

## Hard (Optional)

8. Binary Tree Cameras
1. Maximum Width of Binary Tree
1. Tree Dynamic Programming Problems

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **tree problems are often solved from the bottom up**. Rather than trying
to compute the answer at the root immediately, let each subtree compute its own answer first. Once you understand the
recursive formula:

```text
Answer(node) =
1 + max(
    Answer(left),
    Answer(right)
)
```

you'll recognize the same pattern in many advanced tree interview problems.

______________________________________________________________________

# Next

[45-same-tree-and-invert-binary-tree.md](45-same-tree-and-invert-binary-tree.md)
