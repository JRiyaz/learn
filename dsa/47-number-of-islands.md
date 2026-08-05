# 47-number-of-islands.md

# Number of Islands

> **🎯 This is the most important Graph problem for coding interviews.**
>
> Surprisingly, you don't need to know advanced graph theory.
>
> The problem is simply:
>
> **Find connected components in a grid.**
>
> Once you master this lesson, you'll understand:
>
> - Graph Traversal
> - DFS
> - BFS
> - Flood Fill
> - Connected Components
> - Matrix Traversal
>
> Many grid-based interview problems are just variations of this one.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–40 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem tests multiple concepts together:

- Graph traversal
- DFS / BFS
- Matrix traversal
- Visited tracking
- Connected components
- Recursive thinking

This pattern appears in:

- Flood Fill
- Rotten Oranges
- Pacific Atlantic Water Flow
- Word Search
- Surrounded Regions
- Image Processing
- GIS Systems (Maps)

______________________________________________________________________

# Problem Statement

You are given a 2D grid.

Each cell contains either:

- `"1"` → Land
- `"0"` → Water

An **island** is a group of horizontally or vertically connected land cells.

Return the total number of islands.

______________________________________________________________________

## Example

Input

```text
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

Output

```text
3
```

Because the grid contains:

```text
Island 1

1 1
1 1
```

```text
Island 2

1
```

```text
Island 3

1 1
```

______________________________________________________________________

# Before Learning the Algorithm

Imagine a satellite image.

```text
🌊 🌊 🏝 🏝 🌊
🌊 🏝 🏝 🌊 🌊
🌊 🌊 🌊 🏝 🌊
```

Question:

How many islands exist?

You don't count every land cell.

You count

```
Connected Groups
```

______________________________________________________________________

# Backend Engineering Analogy

Imagine a network.

Each server is connected to nearby servers.

Question:

How many disconnected clusters exist?

Exactly the same problem.

Other examples:

- Social networks
- Computer networks
- Map regions
- Image segmentation
- Friend groups

______________________________________________________________________

# Step 1 — Convert the Grid into a Graph

This is the biggest realization.

Example

```text
1 1
1 0
```

Can be viewed as

```text
A ---- B
|
|
C
```

Every land cell

↓

Node

Neighboring cells

↓

Edges

Therefore,

this is simply

```
Graph Traversal
```

______________________________________________________________________

# Pattern Recognition

## Pattern

**DFS / BFS on Grid**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Matrix
- Grid
- Connected
- Region
- Cluster
- Island
- Flood Fill

Think

```
DFS

or

BFS
```

______________________________________________________________________

# Brute Force Idea

Suppose we visit every land cell.

Question:

How do we avoid counting the same island again?

Need

```
Visited
```

information.

______________________________________________________________________

# Better Observation

Whenever we discover new land,

we should explore

the entire island immediately.

Only then,

increase island count.

______________________________________________________________________

# Key Insight

Algorithm

```
Scan Grid

↓

Find Land?

↓

Island Count++

↓

DFS/BFS

↓

Mark Entire Island Visited
```

Continue scanning.

______________________________________________________________________

# Visual Explanation

Grid

```text
1 1 0

1 0 1

0 0 1
```

Start

```text
*
1 0

1 0 1

0 0 1
```

DFS

Visits

```text
* * 0

* 0 1

0 0 1
```

Island finished.

Count

```
1
```

Continue scanning.

Find another

```
1
```

Repeat.

Answer

```
2
```

______________________________________________________________________

# Why DFS Works

Suppose

```text
1 1 1
```

DFS

```
Visit

↓

Visit Neighbor

↓

Visit Neighbor
```

Eventually,

every connected land cell is visited.

The next unvisited land must belong to

another island.

______________________________________________________________________

# Step-by-Step Dry Run

Grid

```text
1 1 0

1 0 0

0 1 1
```

Start

```
(0,0)
```

DFS

Visits

```text
X X 0

X 0 0

0 1 1
```

Island

```
1
```

Continue.

Find

```
(2,1)
```

DFS

Visits

```text
X X 0

X 0 0

0 X X
```

Island

```
2
```

Done.

______________________________________________________________________

# DFS Traversal

At every cell,

visit

```text
Up

↓

Down

↓

Left

↓

Right
```

Ignore

- Water
- Outside grid
- Already visited

______________________________________________________________________

# Recursive Formula

```text
DFS(row, col)

↓

Mark Visited

↓

DFS(Up)

↓

DFS(Down)

↓

DFS(Left)

↓

DFS(Right)
```

______________________________________________________________________

# Why This Works

Loop (Recursive) Invariant

> After `dfs(row, col)` returns,
> every land cell connected to `(row, col)` has been visited.

Therefore,

that island will never be counted again.

Each new DFS starts from a completely new island.

______________________________________________________________________

# DFS vs BFS

Both work.

______________________________________________________________________

## DFS

Uses

```
Recursion

or

Stack
```

Simple.

______________________________________________________________________

## BFS

Uses

```
Queue
```

Processes layer by layer.

Same complexity.

Interviewers usually expect DFS first.

______________________________________________________________________

# Edge Cases

### Empty Grid

Return

```
0
```

______________________________________________________________________

### All Water

```text
0 0
0 0
```

Answer

```
0
```

______________________________________________________________________

### One Large Island

Answer

```
1
```

______________________________________________________________________

### Every Cell Separate

```text
1 0 1

0 1 0
```

Each land cell

↓

Separate island.

______________________________________________________________________

# Complexity Analysis

Suppose

Grid

```
m × n
```

Every cell visited once.

Time

```
O(m × n)
```

______________________________________________________________________

Space

DFS recursion

Worst

```
O(m × n)
```

(skewed island)

______________________________________________________________________

# Production-Quality Python

## DFS Solution

```python
from typing import List


def num_islands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    rows = len(grid)
    columns = len(grid[0])

    def dfs(row: int, column: int) -> None:
        if (
            row < 0
            or row >= rows
            or column < 0
            or column >= columns
            or grid[row][column] == "0"
        ):
            return

        grid[row][column] = "0"

        dfs(row - 1, column)
        dfs(row + 1, column)
        dfs(row, column - 1)
        dfs(row, column + 1)

    islands = 0

    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == "1":
                islands += 1
                dfs(row, column)

    return islands
```

______________________________________________________________________

## BFS Solution

```python
from collections import deque
from typing import List


def num_islands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    rows = len(grid)
    columns = len(grid[0])
    islands = 0

    for row in range(rows):
        for column in range(columns):
            if grid[row][column] != "1":
                continue

            islands += 1
            grid[row][column] = "0"

            queue = deque([(row, column)])

            while queue:
                current_row, current_column = queue.popleft()

                for row_offset, column_offset in [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                ]:
                    next_row = current_row + row_offset
                    next_column = current_column + column_offset

                    if (
                        0 <= next_row < rows
                        and 0 <= next_column < columns
                        and grid[next_row][next_column] == "1"
                    ):
                        grid[next_row][next_column] = "0"
                        queue.append((next_row, next_column))

    return islands
```

______________________________________________________________________

# Should We Modify the Grid?

Interviewers may ask.

Two choices.

______________________________________________________________________

### Option 1

Modify Grid

```text
1

↓

0
```

Memory

```
O(1)
```

(extra)

Most common interview solution.

______________________________________________________________________

### Option 2

Maintain

```python
visited = set()
```

Useful when the original grid cannot be modified.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting to mark visited.

Causes infinite recursion.

______________________________________________________________________

## Mistake 2

Checking diagonal neighbors.

Problem only allows

```
Up

Down

Left

Right
```

______________________________________________________________________

## Mistake 3

Counting every land cell.

Need to count

```
Connected Components
```

______________________________________________________________________

## Mistake 4

Missing boundary checks.

Always verify row and column limits.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Every land cell can be viewed as a graph node connected to its neighboring land cells. The problem is asking for the number of connected components. I'll scan the grid, and whenever I find an unvisited land cell, I'll increment the island count and run DFS to mark every connected land cell as visited. This ensures each island is counted exactly once."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use DFS?**

It naturally explores one connected component completely before moving to the next.

______________________________________________________________________

**Q. Can BFS solve it?**

Yes.

Both have identical time complexity.

______________________________________________________________________

**Q. Why modify the grid?**

It avoids maintaining a separate visited structure.

______________________________________________________________________

**Q. Where is this pattern used?**

- Image processing
- Maps
- Computer networks
- Social graphs
- Flood fill
- Region detection

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | DFS/BFS on Grid |
| Recognition | Connected Components |
| Traversal | Up, Down, Left, Right |
| Brute Force | Scan + Visited |
| Optimized | DFS/BFS Flood Fill |
| Time | O(m × n) |
| Space | O(m × n) worst case |

______________________________________________________________________

# Quick Revision

- Treat the grid as a graph.
- Land cells are graph nodes.
- Connected land forms one island.
- Scan the grid.
- On finding new land, start DFS/BFS.
- Mark the entire island as visited.
- Increment island count once per DFS/BFS.
- Every cell is visited once.

______________________________________________________________________

# Practice Questions

## Easy

1. Flood Fill
1. Max Area of Island
1. Find if Path Exists in Graph

______________________________________________________________________

## Medium

4. Surrounded Regions
1. Rotting Oranges
1. Pacific Atlantic Water Flow
1. Number of Closed Islands

______________________________________________________________________

## Hard (Optional)

8. Shortest Path in Binary Matrix
1. Making a Large Island
1. Alien Dictionary

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning to **see a grid as a graph**. Once you recognize that each land cell is
a node and adjacent land cells are connected, the problem becomes a classic **connected components** problem. The **scan
→ discover → DFS/BFS → mark visited** pattern is one of the most reusable graph techniques in coding interviews.

______________________________________________________________________

# Next

[48-climbing-stairs.md](48-climbing-stairs.md)
