# 14-best-time-to-buy-sell-stock.md

# Best Time to Buy and Sell Stock

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the **most asked interview questions** for backend and product companies.

At first glance, it looks like a finance problem.

It isn't.

Interviewers are testing whether you can:

- Traverse an array efficiently
- Maintain running minimums
- Maintain running maximums
- Optimize from O(n²) to O(n)
- Think in terms of **state**

This problem introduces one of the most important interview patterns:

> **Maintain the best answer seen so far while scanning the array.**

You'll reuse this idea in:

- Maximum Subarray
- Maximum Product Subarray
- Sliding Window problems
- Dynamic Programming
- Greedy Algorithms

______________________________________________________________________

# Problem Statement

You are given an array where:

```
prices[i]
```

is the stock price on day `i`.

You may:

- Buy **once**
- Sell **once**

You **must buy before selling**.

Return the maximum possible profit.

If no profit is possible,

return

```
0
```

______________________________________________________________________

## Example 1

```text
Input

[7,1,5,3,6,4]
```

Output

```text
5
```

Explanation

```
Buy

1

Sell

6

Profit

5
```

______________________________________________________________________

## Example 2

```text
Input

[7,6,4,3,1]
```

Output

```text
0
```

Prices always decrease.

No profitable transaction exists.

______________________________________________________________________

# Simple English

Imagine a fruit market.

Every morning,

fruit prices change.

You want to:

- Buy once
- Sell once

Your goal is to maximize profit.

The challenge is:

> You **cannot travel back in time**.

You must buy before you sell.

______________________________________________________________________

# Common Misunderstandings

Many beginners think:

> "Find the smallest number and the largest number."

Wrong.

Example

```
[8,2,6,1,10]
```

Smallest

```
1
```

Largest

```
10
```

Looks like

```
Profit = 9
```

Correct here.

But consider

```
[10,1,9]
```

Still works.

Now

```
[9,8,7,10,1]
```

Smallest

```
1
```

Largest

```
10
```

But

```
1

comes AFTER

10
```

You cannot buy after selling.

Order matters.

______________________________________________________________________

# Backend Engineering Analogy

Imagine you're monitoring CPU usage.

```
Day

CPU
```

You want to know:

> What's the maximum increase from any earlier reading?

You continuously remember:

```
Lowest CPU seen so far

↓

Current CPU

↓

Maximum Increase
```

This pattern appears in:

- Monitoring systems
- Analytics
- Performance tracking
- Metrics dashboards
- Time-series databases

______________________________________________________________________

# Pattern Recognition

## Pattern

**Running Minimum + Running Maximum Profit**

______________________________________________________________________

## Recognition Clues

Whenever the problem contains:

- Maximum profit
- Buy before sell
- Earlier vs later
- Best difference
- Time-series data

Think

```
Running Minimum

+

Running Answer
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Try every possible buying day.

For each buying day,

try every possible selling day.

Keep the maximum profit.

______________________________________________________________________

## Algorithm

```
Buy Day

↓

Every Future Sell Day

↓

Compute Profit

↓

Update Maximum
```

______________________________________________________________________

## Dry Run

```
Prices

7 1 5 3 6 4
```

Buy

```
7
```

Profits

```
-6

-2

-4

-1

-3
```

Best

```
0
```

______________________________________________________________________

Buy

```
1
```

Profits

```
4

2

5

3
```

Best

```
5
```

Continue.

Maximum remains

```
5
```

______________________________________________________________________

## Complexity

Outer loop

```
n
```

Inner loop

```
n
```

Time

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

## Limitations

Suppose

```
100,000
```

prices exist.

```
O(n²)
```

becomes far too slow.

Can we avoid checking every pair?

Yes.

______________________________________________________________________

# Optimized Solution

## Key Insight

When selling today,

you only care about one thing:

> **What is the cheapest price I've seen before today?**

That's it.

You don't need to compare against every previous day.

Only the cheapest one.

______________________________________________________________________

Maintain two variables:

```
minimum_price

maximum_profit
```

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
[7,1,5,3,6,4]
```

Initially

```
Minimum Price

7
```

```
Maximum Profit

0
```

______________________________________________________________________

Read

```
1
```

Cheaper.

Update

```
Minimum Price

1
```

______________________________________________________________________

Read

```
5
```

Profit

```
5 - 1

=

4
```

Maximum

```
4
```

______________________________________________________________________

Read

```
3
```

Profit

```
3 - 1

=

2
```

Ignore.

______________________________________________________________________

Read

```
6
```

Profit

```
6 - 1

=

5
```

Update.

Maximum

```
5
```

______________________________________________________________________

Read

```
4
```

Profit

```
4 - 1

=

3
```

Ignore.

Finished.

______________________________________________________________________

# Dry Run

| Price | Minimum Price | Current Profit | Maximum Profit |
|--------|---------------|----------------|----------------|
|7|7|0|0|
|1|1|0|0|
|5|1|4|4|
|3|1|2|4|
|6|1|5|5|
|4|1|3|5|

Answer

```
5
```

______________________________________________________________________

# Visual Explanation

```
Prices

7

1

5

3

6

4
```

```
Minimum

7

↓

1

↓

1

↓

1

↓

1

↓

1
```

```
Profit

0

↓

0

↓

4

↓

2

↓

5

↓

3
```

```
Best

5
```

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before processing each price, `minimum_price` stores the lowest price seen so far, and `maximum_profit` stores the highest profit achievable using only the prices processed so far.

At every new price,

only two possibilities exist:

### Case 1

Current price is lower.

```
Update minimum.
```

______________________________________________________________________

### Case 2

Current price is higher.

Compute

```
Current Price

-

Minimum Price
```

Update maximum profit if larger.

Since every selling day is considered exactly once,

the algorithm never misses the optimal transaction.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
0
```

______________________________________________________________________

### One Price

```
[5]
```

Cannot sell.

Return

```
0
```

______________________________________________________________________

### Decreasing Prices

```
7 6 5 4
```

Return

```
0
```

______________________________________________________________________

### Increasing Prices

```
1 2 3 4 5
```

Buy first.

Sell last.

______________________________________________________________________

### Duplicate Prices

Works correctly.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Space

```
O(1)
```

Only one traversal.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def max_profit(prices: List[int]) -> int:
    maximum_profit = 0

    for buy_day in range(len(prices)):
        for sell_day in range(buy_day + 1, len(prices)):
            profit = prices[sell_day] - prices[buy_day]
            maximum_profit = max(maximum_profit, profit)

    return maximum_profit
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def max_profit(prices: List[int]) -> int:
    if not prices:
        return 0

    minimum_price = prices[0]
    maximum_profit = 0

    for current_price in prices[1:]:
        minimum_price = min(minimum_price, current_price)

        current_profit = current_price - minimum_price

        maximum_profit = max(maximum_profit, current_profit)

    return maximum_profit


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]

    print(max_profit(prices))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Choosing the smallest and largest values without considering their order.

Remember:

```
Buy

↓

Sell
```

Never the reverse.

______________________________________________________________________

## Mistake 2

Updating profit before updating the minimum price.

Always update the minimum first.

______________________________________________________________________

## Mistake 3

Returning negative profit.

If no profit exists,

return

```
0
```

______________________________________________________________________

## Mistake 4

Using nested loops.

This gives

```
O(n²)
```

instead of

```
O(n)
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A brute-force solution checks every buy-sell pair, resulting in O(n²) time. However, while scanning the array once, I only need to remember the cheapest price seen so far. For every new price, I calculate the profit if I sold today and update the maximum profit accordingly. This reduces the complexity to O(n) while using constant extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why store only the minimum price?**

Because for today's selling price,

only the cheapest earlier buying price can produce the highest profit.

______________________________________________________________________

**Q. Why not store every previous price?**

They aren't needed.

The smallest price dominates all other buying choices.

______________________________________________________________________

**Q. What if multiple transactions are allowed?**

That's a different problem:

**Best Time to Buy and Sell Stock II.**

The greedy solution changes completely.

______________________________________________________________________

**Q. Is this Dynamic Programming?**

Not exactly.

It's closer to a **Greedy** algorithm with a running state.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Running Minimum |
| Recognition | Maximum Difference Over Time |
| Brute Force | Check Every Pair |
| Optimized | Track Minimum Price |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Order matters: buy before sell.
- Brute force compares every pair.
- Maintain the minimum price seen so far.
- Compute today's profit using that minimum.
- Update the maximum profit.
- One traversal is enough.
- Time complexity is O(n).
- Space complexity is O(1).
- This "running minimum" pattern appears in many interview problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Maximum Difference Between Increasing Elements
1. Maximum Product Difference Between Two Pairs
1. Best Time to Buy and Sell Stock (Review)

______________________________________________________________________

## Medium

4. Best Time to Buy and Sell Stock II
1. Best Time to Buy and Sell Stock with Transaction Fee
1. Best Time to Buy and Sell Stock with Cooldown
1. Maximum Subarray

______________________________________________________________________

## Hard (Optional)

8. Best Time to Buy and Sell Stock III
1. Best Time to Buy and Sell Stock IV
1. Maximum Profit in Job Scheduling

______________________________________________________________________

# Key Takeaway

The biggest lesson is learning to maintain a **running minimum** while traversing the array. Instead of comparing every
possible buy-sell pair, you continuously remember the best buying opportunity seen so far. This transforms an O(n²)
solution into an elegant O(n) algorithm—a pattern that appears repeatedly in array, greedy, and dynamic programming
interview problems.

______________________________________________________________________

# Next

[15-product-of-array-except-self.md](15-product-of-array-except-self.md)
