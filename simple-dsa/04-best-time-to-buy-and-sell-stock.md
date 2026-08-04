# 04-best-time-to-buy-and-sell-stock.md

# Best Time to Buy and Sell Stock — Learning Running Minimum

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

You are given an array `prices` where `prices[i]` is the stock price on day `i`.

You want to maximize your profit by choosing:

- one day to buy
- one later day to sell

Return the maximum profit.

If no profit is possible, return `0`.

Example:

```text
prices = [7,1,5,3,6,4]

Output = 5
```

Buy at **1**

Sell at **6**

Profit = **5**

______________________________________________________________________

# What Is Actually Being Asked?

You are **not** asked to find:

- highest price
- lowest price

You are asked:

> Find the maximum difference where the smaller number appears **before** the larger number.

This constraint changes everything.

Example:

```text
[7,6,5,4,3]
```

Lowest = 3

Highest = 7

Profit is NOT

```
7-3 = 4
```

Because you cannot sell before buying.

Correct answer:

```
0
```

______________________________________________________________________

# Real-World Analogy

Suppose you're building a stock analytics backend.

Every minute, a new stock price arrives.

```text
100
102
98
105
101
```

You don't want to compare every price with every previous one.

Instead, while processing the stream, you keep track of:

- cheapest price so far
- best profit so far

This allows real-time processing.

______________________________________________________________________

# Pattern Recognition

This problem teaches the **Running Minimum Pattern**.

Whenever you see:

- maximize difference
- buy before sell
- best profit
- lowest value before highest value
- one pass optimization

Think:

> Keep the smallest value seen so far.

______________________________________________________________________

# Brute Force Solution

## Intuition

Try every possible buying day.

For each buying day:

Try every selling day after it.

Compute profit.

Keep the maximum.

______________________________________________________________________

## Visual

```text
Buy

↓

Compare all future days

↓

Find best profit

↓

Repeat
```

Example

```text
7 1 5 3 6 4
```

```
Buy 7

Compare

1

5

3

6

4

Then

Buy 1

Compare

5

3

6

4
```

______________________________________________________________________

## Complexity

Time

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

## Python

```python
from typing import List


def max_profit_brute(prices: List[int]) -> int:
    max_profit = 0

    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):
            profit = prices[sell] - prices[buy]
            max_profit = max(max_profit, profit)

    return max_profit
```

______________________________________________________________________

# Optimal Solution

## Key Insight

When processing today's price:

You only need to know:

> What was the cheapest price before today?

Nothing else matters.

Maintain two variables:

```text
minimum_price

maximum_profit
```

Every new price:

1. Compute profit.
1. Update answer.
1. Update minimum price.

______________________________________________________________________

# Visual Explanation

Example

```text
7 1 5 3 6 4
```

Start

```
Minimum = 7

Profit = 0
```

______________________________________________________________________

Price = 1

```
Minimum = 1

Profit = 0
```

______________________________________________________________________

Price = 5

```
Profit = 5-1 = 4

Maximum = 4
```

______________________________________________________________________

Price = 3

```
Profit = 2

Maximum = 4
```

______________________________________________________________________

Price = 6

```
Profit = 5

Maximum = 5
```

______________________________________________________________________

Price = 4

```
Profit = 3

Maximum = 5
```

Answer

```
5
```

______________________________________________________________________

# Step-by-Step Algorithm

Initialize:

```text
minimum_price = first element

maximum_profit = 0
```

For every remaining price:

```
profit = current - minimum_price

Update answer

Update minimum_price
```

Return maximum profit.

______________________________________________________________________

# Why This Works

For every selling day, the best buying day is simply:

> The lowest price seen before that day.

We don't need to remember every previous price.

The running minimum already represents the best buying opportunity.

Thus:

- one pass
- no repeated work

______________________________________________________________________

# Edge Cases

## Empty Array

Return

```
0
```

______________________________________________________________________

## One Price

Cannot sell.

```
0
```

______________________________________________________________________

## Strictly Decreasing

```text
9 8 7 6 5
```

Never profitable.

Return

```
0
```

______________________________________________________________________

## Strictly Increasing

```text
1 2 3 4 5
```

Buy first.

Sell last.

______________________________________________________________________

## Duplicate Prices

```text
3 3 3 3
```

Profit

```
0
```

______________________________________________________________________

# Complexity Analysis

## Time

Single traversal.

```
O(n)
```

______________________________________________________________________

## Space

Only two variables.

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def max_profit(prices: List[int]) -> int:
    """
    Returns the maximum profit from one buy and one sell.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    if not prices:
        return 0

    minimum_price = prices[0]
    maximum_profit = 0

    for current_price in prices[1:]:
        profit = current_price - minimum_price
        maximum_profit = max(maximum_profit, profit)
        minimum_price = min(minimum_price, current_price)

    return maximum_profit
```

______________________________________________________________________

# Common Mistakes

### 1. Choosing Global Minimum and Maximum

Wrong.

Minimum must occur **before** maximum.

______________________________________________________________________

### 2. Buying and Selling Same Day

No profit.

Maximum should remain 0.

______________________________________________________________________

### 3. Nested Loops

Correct.

Too slow.

______________________________________________________________________

### 4. Updating Minimum Too Late

Always update the minimum price after processing the current price so future days can use it.

______________________________________________________________________

### 5. Forgetting Empty Input

Always check.

```python
if not prices:
    return 0
```

______________________________________________________________________

# Variations

## Easy

- Maximum Difference Between Increasing Elements

______________________________________________________________________

## Medium

- Best Time to Buy and Sell Stock II
- Best Time to Buy and Sell Stock with Cooldown
- Best Time to Buy and Sell Stock with Transaction Fee
- Maximum Subarray (similar running computation idea)

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

A strong candidate usually says:

1. Brute force compares every buy/sell pair.
1. Complexity is O(n²).
1. Observe that each selling day only needs the cheapest earlier price.
1. Maintain a running minimum.
1. Achieve O(n).

______________________________________________________________________

### Common Follow-ups

**Q:** Why not sort?

Sorting changes the order of days.

Buying must happen before selling.

______________________________________________________________________

**Q:** Can this be solved in one pass?

Yes.

______________________________________________________________________

**Q:** Extra memory?

Only two variables.

______________________________________________________________________

**Q:** What if multiple transactions are allowed?

That's a different problem (Stock II).

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Running Minimum |
| Recognition | Max difference, buy before sell |
| Brute Force | Compare every pair |
| Optimal | Track minimum so far |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Maximum Difference Between Increasing Elements
1. Find Pivot Index

## Medium

1. Best Time to Buy and Sell Stock II
1. Maximum Subarray
1. Maximum Product Subarray
1. Container With Most Water

## Hard (Optional)

1. Best Time to Buy and Sell Stock III
1. Best Time to Buy and Sell Stock IV

______________________________________________________________________

# Quick Revision

- Keep the **minimum price seen so far**.
- At each day:
  - Calculate current profit.
  - Update maximum profit.
  - Update minimum price.
- Never compare every pair.
- Sorting is invalid because order matters.
- Time: **O(n)**
- Space: **O(1)**
- This teaches the **Running Minimum Pattern**, useful in many streaming and analytics problems.

______________________________________________________________________

# Navigation

**Previous**

[03-two-sum.md](03-two-sum.md)

**Next**

[05-contains-duplicate.md](05-contains-duplicate.md)
