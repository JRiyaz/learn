# 20-longest-common-prefix.md

# Longest Common Prefix

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐☆ High |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem looks like a simple string comparison problem.

It isn't.

Interviewers use it to test:

- String traversal
- Comparing multiple strings
- Early termination
- Choosing the shortest candidate
- Thinking about optimization

More importantly, this problem introduces the idea of **Vertical Scanning**, which is used in:

- Trie (Prefix Tree)
- Search Engines
- Auto-complete Systems
- DNS Lookup
- URL Routing

______________________________________________________________________

# Problem Statement

Given an array of strings,

find the **longest common prefix** shared by all strings.

If no common prefix exists,

return an empty string.

______________________________________________________________________

## Example 1

```text
Input

["flower","flow","flight"]
```

Output

```text
"fl"
```

______________________________________________________________________

## Example 2

```text
Input

["dog","racecar","car"]
```

Output

```text
""
```

No common prefix.

______________________________________________________________________

## Example 3

```text
Input

["interview","internet","internal"]
```

Output

```text
"inter"
```

______________________________________________________________________

# Simple English

Imagine several roads.

```
Road 1

flower
```

```
Road 2

flow
```

```
Road 3

flight
```

Initially,

all roads are identical.

```
f

↓

l
```

Then,

they split.

The shared path before the split is the answer.

______________________________________________________________________

# Backend Engineering Analogy

Suppose multiple API endpoints exist.

```
/api/v1/users

/api/v1/orders

/api/v1/products
```

The common prefix is

```
/api/v1/
```

This helps in:

- API Gateway routing
- URL grouping
- Reverse proxies
- Load balancers

Similarly,

search engines use common prefixes to build **Trie** structures.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Vertical Scanning**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Common prefix
- Common beginning
- Compare multiple strings
- Shared path

Think

```
Character by Character

↓

Across All Strings
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Compare every string with every other string.

Reduce the common prefix step by step.

______________________________________________________________________

## Algorithm

Start

```
flower
```

Compare with

```
flow
```

Common

```
flow
```

Now compare

```
flow

flight
```

Common

```
fl
```

Done.

______________________________________________________________________

## Dry Run

Input

```
flower

flow

flight
```

Current prefix

```
flower
```

↓

Compare

```
flow
```

↓

```
flow
```

↓

Compare

```
flight
```

↓

```
fl
```

Answer

```
fl
```

______________________________________________________________________

## Complexity

Worst case

```
O(n × m)
```

where

```
n

=

number of strings
```

```
m

=

average string length
```

______________________________________________________________________

## Limitations

Repeated substring creation can make this less efficient.

Can we compare characters directly?

Yes.

______________________________________________________________________

# Optimized Solution (Vertical Scanning)

## Key Insight

Instead of comparing whole strings,

compare one character at a time.

Example

```
flower

flow

flight
```

Compare first character

```
f

=

f

=

f

✔
```

Second

```
l

=

l

=

l

✔
```

Third

```
o

o

i

✖
```

Stop immediately.

Answer

```
fl
```

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
flower

flow

flight
```

Index

```
0
```

All strings contain

```
f
```

Continue.

______________________________________________________________________

Index

```
1
```

All contain

```
l
```

Continue.

______________________________________________________________________

Index

```
2
```

```
o

o

i
```

Mismatch.

Stop.

Return

```
fl
```

______________________________________________________________________

# Visual Explanation

```
flower

flow

flight
```

Compare vertically

```
f

↓

f

↓

f

✔
```

```
l

↓

l

↓

l

✔
```

```
o

↓

o

↓

i

✖
```

Stop.

______________________________________________________________________

# Another Example

```
interview

internet

internal
```

```
i ✔

n ✔

t ✔

e ✔

r ✔

v ✖
```

Answer

```
inter
```

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration, all previously checked characters form a valid common prefix.

As soon as one string differs,

no longer prefix can exist.

Why?

Because prefixes must match from the beginning.

Once they diverge,

the answer is complete.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
""
```

______________________________________________________________________

### One String

```
["hello"]
```

Return

```
hello
```

______________________________________________________________________

### Empty String Exists

```
["","abc"]
```

Answer

```
""
```

______________________________________________________________________

### No Common Prefix

```
cat

dog

apple
```

Return

```
""
```

______________________________________________________________________

### All Strings Same

```
python

python

python
```

Return

```
python
```

______________________________________________________________________

# Complexity Analysis

Let

```
n

=

number of strings
```

```
m

=

length of the shortest string
```

Every character is checked at most once across all strings.

Time

```
O(n × m)
```

Space

```
O(1)
```

No additional data structures are required.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def longest_common_prefix(strings: List[str]) -> str:
    if not strings:
        return ""

    prefix = strings[0]

    for current in strings[1:]:
        while not current.startswith(prefix):
            prefix = prefix[:-1]

            if not prefix:
                return ""

    return prefix
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def longest_common_prefix(strings: List[str]) -> str:
    if not strings:
        return ""

    shortest = min(strings, key=len)

    for index, character in enumerate(shortest):
        for current in strings:
            if current[index] != character:
                return shortest[:index]

    return shortest


if __name__ == "__main__":
    values = [
        "flower",
        "flow",
        "flight",
    ]

    print(longest_common_prefix(values))
```

______________________________________________________________________

# Alternative Approach (Sorting)

Sort the strings.

```
flower

flow

flight
```

↓

Sorted

```
flight

flow

flower
```

Now,

only compare

```
First

and

Last
```

Why?

Because they are the most different.

Their common prefix is also the common prefix of the entire list.

Complexity

```
O(n log n)
```

Useful,

but not optimal.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Comparing entire strings repeatedly.

Character-by-character comparison stops earlier.

______________________________________________________________________

## Mistake 2

Not checking for an empty list.

______________________________________________________________________

## Mistake 3

Accessing beyond the shortest string.

Always use the shortest string as the reference.

______________________________________________________________________

## Mistake 4

Continuing after the first mismatch.

No longer prefix is possible.

Stop immediately.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution repeatedly shrinks the prefix until it matches every string. A more intuitive solution is vertical scanning. I compare characters column by column across all strings. The first mismatch tells me exactly where the common prefix ends. By using the shortest string as the reference, I avoid index errors."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use the shortest string?**

Because the common prefix cannot be longer than the shortest string.

______________________________________________________________________

**Q. Why stop at the first mismatch?**

A prefix must match from the beginning.

Once characters differ,

the common prefix ends.

______________________________________________________________________

**Q. Is there a faster solution?**

Not asymptotically.

Every matching character must be inspected at least once.

______________________________________________________________________

**Q. Where is this used in backend systems?**

- Trie construction
- Auto-complete
- API routing
- URL grouping
- Search indexing

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Vertical Scanning |
| Recognition | Common Prefix |
| Brute Force | Shrinking Prefix |
| Optimized | Character-by-Character Scan |
| Time | O(n × m) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Compare prefixes, not suffixes.
- Use the shortest string as the reference.
- Compare characters vertically.
- Stop at the first mismatch.
- Return the matched portion.
- Time complexity is O(n × m).
- Space complexity is O(1).
- This concept leads naturally to **Trie (Prefix Tree)** problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Implement Trie (Introduction)
1. Find Common Characters
1. Prefix Count

______________________________________________________________________

## Medium

4. Replace Words
1. Search Suggestions System
1. Implement Trie (Prefix Tree)
1. Word Dictionary

______________________________________________________________________

## Hard (Optional)

8. Word Search II
1. Design Add and Search Words Data Structure
1. Concatenated Words

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning **Vertical Scanning**—comparing multiple strings one character at a
time. This approach avoids unnecessary comparisons, stops early on mismatches, and introduces the foundational idea
behind **Trie (Prefix Tree)**, a data structure widely used in search engines, autocomplete systems, routing, and text
indexing.

______________________________________________________________________

# Next

[21-two-sum.md](21-two-sum.md)
