# 42-binary-tree-traversals.md

# Binary Tree Traversals (DFS & BFS Foundations)

> **🎯 This is your first Tree lesson.**
>
> Trees are one of the most important data structures in backend interviews.
>
> **Everything starts here.**
>
> If you understand traversals, you'll understand:
>
> - Binary Search Trees (BST)
> - Heap
> - Trie
> - Segment Tree
> - Expression Trees
> - File Systems
> - DOM Trees
> - Organization Charts
> - AST (Abstract Syntax Trees)
>
> Nearly every tree problem is built on the traversal techniques you'll learn in this lesson.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 35–45 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers aren't checking whether you can memorize:

```
Preorder

Inorder

Postorder
```

They want to know if you understand:

- Tree structure
- Recursion
- DFS (Depth First Search)
- BFS (Breadth First Search)
- Stack vs Queue
- Recursive thinking

Understanding traversals makes most tree interview problems much easier.

______________________________________________________________________

# Before Learning Trees

## Arrays

Arrays look like this:

```text
10 20 30 40
```

One dimension.

______________________________________________________________________

## Linked Lists

```text
10 → 20 → 30 → 40
```

Each node has

```
One Next Pointer
```

______________________________________________________________________

## Trees

Each node can have

```
Left Child

Right Child
```

Example

```text
        10
       /  \
      5   15
```

A tree branches.

______________________________________________________________________

# What Is a Binary Tree?

A Binary Tree is a collection of nodes.

Every node has:

- Value
- Left Child
- Right Child

Maximum

```
Two Children
```

______________________________________________________________________

# Tree Terminology

Example

```text
          1
        /   \
       2     3
      / \   / \
     4  5  6  7
```

Root

```
1
```

Leaves

```
4

5

6

7
```

Parent

```
2
```

Children

```
4

5
```

Height

```
3 Levels
```

______________________________________________________________________

# Backend Engineering Analogy

Trees appear everywhere.

File System

```text
Root
│
├── home
│   ├── user
│   └── admin
│
└── var
```

HTML DOM

```text
html
│
├── head
└── body
```

Database Execution Plan

```text
JOIN
│
├── Table A
└── Table B
```

JSON

```json
{
  "user": {
    "address": {
      "city": "Bangalore"
    }
  }
}
```

Nested objects naturally form trees.

______________________________________________________________________

# Tree Node

```python
class TreeNode:
    value
    left
    right
```

Visualization

```text
      +------+
      |  10  |
      +------+
      /      \
   left      right
```

______________________________________________________________________

# Why Traversal?

Suppose we have

```text
        1
       / \
      2   3
     / \
    4   5
```

Question

How do we visit every node?

Unlike arrays,

there is no index.

Need traversal.

______________________________________________________________________

# Two Families of Traversal

There are only two major traversal families.

```
DFS

Depth First Search
```

and

```
BFS

Breadth First Search
```

Everything else belongs to one of these.

______________________________________________________________________

# DFS (Depth First Search)

Idea

Go as deep as possible.

Only then,

come back.

Implemented using:

- Recursion
- Stack

______________________________________________________________________

There are

three DFS traversals.

______________________________________________________________________

# 1. Preorder

Rule

```
Root

↓

Left

↓

Right
```

Remember

```
R L R
```

Root

Left

Right

______________________________________________________________________

Example

```text
        1
       / \
      2   3
     / \
    4   5
```

Traversal

```
1

2

4

5

3
```

______________________________________________________________________

# Visual

```text
        1
       / \
      2   3
     / \
    4   5
```

Visit

```
①

↓

②

↓

④

↑

⑤

↑

③
```

______________________________________________________________________

# Where Is Preorder Used?

- Copying trees
- Serialization
- Directory export
- Expression parsing

______________________________________________________________________

# 2. Inorder

Rule

```
Left

↓

Root

↓

Right
```

Remember

```
L R R
```

Left

Root

Right

______________________________________________________________________

Traversal

```text
4

2

5

1

3
```

______________________________________________________________________

# Why Is Inorder Important?

For a

Binary Search Tree

Inorder traversal always produces

```
Sorted Order
```

Very important interview fact.

______________________________________________________________________

# 3. Postorder

Rule

```
Left

↓

Right

↓

Root
```

Traversal

```text
4

5

2

3

1
```

______________________________________________________________________

# Where Is Postorder Used?

- Delete trees
- Free memory
- Evaluate expressions
- Bottom-up calculations

______________________________________________________________________

# Comparing DFS Traversals

| Traversal | Order |
|-----------|-------|
| Preorder | Root → Left → Right |
| Inorder | Left → Root → Right |
| Postorder | Left → Right → Root |

______________________________________________________________________

# Why Recursion Works

Suppose

```text
        1
       / \
      2   3
```

Tree is recursive.

Node

↓

Left Subtree

↓

Right Subtree

Each subtree is itself a tree.

Therefore,

recursion fits naturally.

______________________________________________________________________

# BFS (Breadth First Search)

Instead of going deep,

visit

```
Level by Level
```

Uses

```
Queue
```

______________________________________________________________________

Example

```text
        1
       / \
      2   3
     / \
    4   5
```

Traversal

```text
1

2

3

4

5
```

______________________________________________________________________

# Visual

```text
Queue

[1]
```

↓

Visit

```
1
```

Add

```
2

3
```

Queue

```text
2 3
```

↓

Visit

```
2
```

Add

```
4

5
```

Queue

```text
3 4 5
```

Continue.

______________________________________________________________________

# DFS vs BFS

| DFS | BFS |
|------|------|
| Stack / Recursion | Queue |
| Goes Deep | Goes Wide |
| Less Memory (Usually) | More Memory |
| Used in Recursive Problems | Used in Level Problems |

______________________________________________________________________

# Brute Force Solution

There isn't a brute-force alternative.

Traversal itself is the solution.

The challenge is choosing the correct traversal strategy.

______________________________________________________________________

# Why This Works

Loop Invariant (DFS):

> Before processing a node,
> its ancestors have already been visited according to the traversal order.

Loop Invariant (BFS):

> Before processing a node,
> all nodes from previous levels have already been processed.

These invariants guarantee complete traversal without missing any nodes.

______________________________________________________________________

# Complexity Analysis

Suppose

```
n
```

nodes.

Every traversal visits every node exactly once.

Time

```
O(n)
```

______________________________________________________________________

Space

DFS

```
O(h)
```

where

```
h
```

is tree height.

Worst case

```
O(n)
```

______________________________________________________________________

BFS

Queue may contain one entire level.

Worst

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

## Tree Node

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
```

______________________________________________________________________

## Preorder

```python
def preorder(
    node: Optional[TreeNode],
    result: List[int],
) -> None:
    if node is None:
        return

    result.append(node.value)

    preorder(node.left, result)
    preorder(node.right, result)
```

______________________________________________________________________

## Inorder

```python
def inorder(
    node: Optional[TreeNode],
    result: List[int],
) -> None:
    if node is None:
        return

    inorder(node.left, result)

    result.append(node.value)

    inorder(node.right, result)
```

______________________________________________________________________

## Postorder

```python
def postorder(
    node: Optional[TreeNode],
    result: List[int],
) -> None:
    if node is None:
        return

    postorder(node.left, result)
    postorder(node.right, result)

    result.append(node.value)
```

______________________________________________________________________

## Level Order (BFS)

```python
def level_order(
    root: Optional[TreeNode],
) -> List[int]:
    if root is None:
        return []

    result: List[int] = []
    queue = deque([root])

    while queue:
        node = queue.popleft()

        result.append(node.value)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return result
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Confusing DFS with BFS.

DFS uses recursion/stack.

BFS uses a queue.

______________________________________________________________________

## Mistake 2

Forgetting the base case.

Always stop when

```python
node is None
```

______________________________________________________________________

## Mistake 3

Thinking Inorder is always sorted.

It is sorted **only for Binary Search Trees**, not every binary tree.

______________________________________________________________________

## Mistake 4

Using BFS when the problem asks for recursive processing.

Choose the traversal based on the problem, not preference.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Tree traversal is the process of visiting every node exactly once. DFS explores one branch completely before backtracking and can be implemented using recursion or a stack. Depending on when I process the current node, I get Preorder, Inorder, or Postorder traversal. BFS visits nodes level by level using a queue."

______________________________________________________________________

### Common Follow-up Questions

**Q. Which traversal returns sorted values?**

Only **Inorder traversal of a Binary Search Tree**.

______________________________________________________________________

**Q. Why is recursion natural for trees?**

Because every subtree is itself a tree.

______________________________________________________________________

**Q. Why does BFS use a queue?**

Nodes must be processed in the same order they are discovered.

______________________________________________________________________

**Q. Where are tree traversals used in backend systems?**

- File systems
- JSON processing
- HTML DOM traversal
- Query execution plans
- Expression evaluation
- Organization hierarchies

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | DFS / BFS |
| DFS Structure | Stack / Recursion |
| BFS Structure | Queue |
| Preorder | Root → Left → Right |
| Inorder | Left → Root → Right |
| Postorder | Left → Right → Root |
| Level Order | BFS |
| Time | O(n) |
| Space | O(h) DFS, O(n) BFS |

______________________________________________________________________

# Quick Revision

- Trees branch instead of storing elements linearly.
- DFS explores depth first.
- BFS explores level by level.
- Preorder: Root → Left → Right.
- Inorder: Left → Root → Right.
- Postorder: Left → Right → Root.
- BFS uses a queue.
- DFS usually uses recursion.
- Every traversal visits each node exactly once.

______________________________________________________________________

# Practice Questions

## Easy

1. Binary Tree Preorder Traversal
1. Binary Tree Inorder Traversal
1. Binary Tree Postorder Traversal

______________________________________________________________________

## Medium

4. Binary Tree Right Side View
1. Zigzag Level Order Traversal
1. Binary Tree Paths
1. Average of Levels in Binary Tree

______________________________________________________________________

## Hard (Optional)

8. Serialize and Deserialize Binary Tree
1. Vertical Order Traversal
1. Boundary Traversal of Binary Tree

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is that **every tree problem begins with traversal**. Before worrying about complex
tree algorithms, first decide **how you want to visit the nodes**. Once you recognize whether a problem needs **DFS
(depth-first)** or **BFS (level-first)**, many tree problems become straightforward.

______________________________________________________________________

# Next

[43-binary-tree-level-order-traversal.md](43-binary-tree-level-order-traversal.md)
