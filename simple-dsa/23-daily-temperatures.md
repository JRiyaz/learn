# 23-daily-temperatures.md

# Daily Temperatures — The Monotonic Stack Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 7 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an array of daily temperatures, return an array where:

```text
answer[i]
```

represents the number of days you have to wait until a warmer temperature.

If no warmer day exists,

return

```text
0
```

for that position.

______________________________________________________________________

### Example

```text
Input

[73,74,75,71,69,72,76,73]
```

Output

```text
[1,1,4,2,1,1,0,0]
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> For every day,

find the **next greater temperature**.

Notice:

You are **not**

looking for

```text
Largest temperature
```

You are looking for

```text
First warmer temperature
```

______________________________________________________________________

# Real-World Analogy

Suppose you're monitoring stock prices.

```text
100

105

101

120
```

For every day,

find when the next higher price occurs.

Other examples:

- Price alerts
- CPU utilization spikes
- Sensor readings
- Traffic peaks

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Next greater
- Next warmer
- First larger value
- Nearest larger element

Think immediately:

```text
Monotonic Stack
```

______________________________________________________________________

# Brute Force Solution

For every temperature,

scan all future temperatures.

Example

```text
73

↓

74

Found
```

Next

```text
74

↓

75

Found
```

Next

```text
75

↓

71

↓

69

↓

72

↓

76

Found
```

______________________________________________________________________

## Complexity

Time

```text
O(n²)
```

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

Instead of repeatedly searching,

keep temperatures waiting for a warmer day.

As soon as a warmer temperature appears,

resolve all waiting days.

______________________________________________________________________

# Why Store Indices Instead of Temperatures?

Suppose

```text
73
```

becomes warmer at

```text
74
```

Need answer

```text
1 day
```

Need

```text
Current Index

-

Previous Index
```

Therefore,

store indices.

Not values.

______________________________________________________________________

# Monotonic Stack

The stack stores indices whose temperatures are in **decreasing order**.

Example

```
Temperatures

73 75 71 69

Stack

69

71

75
```

Top always has the **smallest unresolved temperature**.

______________________________________________________________________

# Visual Explanation

Input

```text
73 74 75 71 69 72 76 73
```

Start

```text
73
```

Stack

```text
73
```

______________________________________________________________________

Read

```text
74
```

Warmer than

```text
73
```

Resolve

```text
73 → wait 1 day
```

Push

```text
74
```

______________________________________________________________________

Read

```text
75
```

Warmer.

Resolve

```text
74 → wait 1 day
```

Push.

Continue.

______________________________________________________________________

Eventually

```text
76
```

Warmer than

```text
72

75
```

Resolve both.

______________________________________________________________________

# Step-by-Step Algorithm

Create:

- answer array
- empty stack

For every index:

While

```text
Current temperature

>

Temperature at stack top
```

Resolve top.

Store answer.

Push current index.

______________________________________________________________________

# Dry Run

Input

```text
73 74 75
```

Stack

```text
73
```

Read

```text
74
```

Warmer.

Answer

```text
73

↓

1
```

Push

```text
74
```

Read

```text
75
```

Resolve

```text
74

↓

1
```

Done.

Last element

```text
0
```

______________________________________________________________________

# Why This Works

Each temperature enters the stack once.

Leaves once.

Never re-enters.

The stack always contains unresolved temperatures in decreasing order.

Whenever a warmer day appears,

multiple temperatures may be resolved.

______________________________________________________________________

# Edge Cases

## Strictly Increasing

```text
70 71 72
```

Output

```text
1 1 0
```

______________________________________________________________________

## Strictly Decreasing

```text
75 74 73
```

Output

```text
0 0 0
```

______________________________________________________________________

## Equal Temperatures

```text
70 70 70
```

Need

strictly warmer.

Output

```text
0 0 0
```

______________________________________________________________________

## One Element

```text
50
```

Output

```text
0
```

______________________________________________________________________

# Complexity Analysis

## Time

Each index:

- pushed once
- popped once

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Worst case

Strictly decreasing temperatures.

Stack stores every index.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Returns the number of days until
    a warmer temperature.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    answer = [0] * len(temperatures)
    stack: List[int] = []

    for current_index, current_temperature in enumerate(temperatures):
        while (
            stack
            and current_temperature > temperatures[stack[-1]]
        ):
            previous_index = stack.pop()
            answer[previous_index] = (
                current_index - previous_index
            )

        stack.append(current_index)

    return answer
```

______________________________________________________________________

# Common Mistakes

## 1. Storing Temperatures Instead of Indices

Need distance.

Store indices.

______________________________________________________________________

## 2. Using >= Instead of >

Problem says

```text
Warmer
```

Equal isn't warmer.

______________________________________________________________________

## 3. Forgetting Multiple Pops

One warmer day can resolve several earlier days.

Always use

```python
while
```

not

```python
if
```

______________________________________________________________________

## 4. Forgetting Unresolved Days

Default answer is

```text
0
```

No need for extra processing.

______________________________________________________________________

# Variations

## Medium

- Next Greater Element I
- Next Greater Element II
- Online Stock Span
- Asteroid Collision

______________________________________________________________________

## Hard

- Largest Rectangle in Histogram
- Trapping Rain Water (Stack Solution)

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize "next greater element."
1. Mention brute force.
1. Explain repeated scanning.
1. Introduce Monotonic Stack.
1. Store indices.
1. Resolve previous temperatures.
1. Analyze O(n).

______________________________________________________________________

### Common Follow-ups

### Q: Why store indices?

Need to calculate:

```text
Current Index

-

Previous Index
```

______________________________________________________________________

### Q: Why a decreasing stack?

Only colder temperatures are waiting for a warmer day.

Keeping them in decreasing order lets us resolve them efficiently.

______________________________________________________________________

### Q: Why is this O(n)?

Each index is pushed once and popped once.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Monotonic Decreasing Stack |
| Recognition | Next greater element |
| Store | Indices |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Next Greater Element I
1. Baseball Game

## Medium

1. Next Greater Element II
1. Online Stock Span
1. Asteroid Collision
1. Car Fleet *(different reasoning, same stack intuition)*

## Hard

1. Largest Rectangle in Histogram
1. Trapping Rain Water (Stack)

______________________________________________________________________

# Quick Revision

- Looking for the next greater value.
- Use a **Monotonic Decreasing Stack**.
- Store indices, not values.
- While current value is greater, pop and resolve.
- One element may resolve many previous elements.
- Time: **O(n)**
- Space: **O(n)**

______________________________________________________________________

# Key Takeaway

This problem introduces one of the most reusable interview patterns:

> **Monotonic Stack**

The invariant is:

```text
The stack contains unresolved elements in decreasing order.
```

Whenever a larger value appears:

- Pop smaller values.
- Resolve them.
- Push the current value.

You'll reuse this exact idea in many interview problems.

______________________________________________________________________

# Navigation

**Previous**

[22-valid-parentheses.md](22-valid-parentheses.md)

**Next**

[24-evaluate-reverse-polish-notation.md](24-evaluate-reverse-polish-notation.md)
