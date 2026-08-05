# 19-valid-anagram.md

# Valid Anagram

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem looks like a simple string question.

It isn't.

Interviewers are testing whether you understand:

- Hash Maps (Dictionaries)
- Frequency Counting
- Character matching
- Choosing the right data structure
- Optimizing from sorting to linear time

This is usually the **first Hash Map problem** candidates encounter.

Understanding this problem makes many future questions easier:

- Group Anagrams
- Top K Frequent Elements
- Frequency Sort
- First Unique Character
- Majority Element

______________________________________________________________________

# Problem Statement

Given two strings `first` and `second`,

return `True` if they are **anagrams**.

Otherwise,

return `False`.

______________________________________________________________________

## What is an Anagram?

Two strings are anagrams if:

- They contain exactly the same characters.
- Every character appears the same number of times.
- The order of characters does **not** matter.

______________________________________________________________________

## Example 1

```text
Input

first = "anagram"

second = "nagaram"
```

Output

```text
True
```

______________________________________________________________________

## Example 2

```text
Input

first = "rat"

second = "car"
```

Output

```text
False
```

______________________________________________________________________

## Example 3

```text
Input

first = "listen"

second = "silent"
```

Output

```text
True
```

______________________________________________________________________

# Simple English

Imagine two bags of Scrabble letters.

Bag 1

```
c a t
```

Bag 2

```
t a c
```

Different order.

Same letters.

Same counts.

They are anagrams.

______________________________________________________________________

Now

```
cat
```

and

```
car
```

Letter

```
t
```

is missing.

Not an anagram.

______________________________________________________________________

# Backend Engineering Analogy

Imagine two API requests.

They contain the same query parameters,

but the order differs.

Request 1

```
user=10

sort=name

page=2
```

Request 2

```
page=2

user=10

sort=name
```

They represent the same request.

The order isn't important.

Only the content and frequency matter.

This idea appears in:

- Cache key normalization
- Request deduplication
- Data comparison
- Search indexing

______________________________________________________________________

# Pattern Recognition

## Pattern

**Frequency Counting (Hash Map)**

______________________________________________________________________

## Recognition Clues

Whenever the question contains:

- Same characters
- Frequency
- Count occurrences
- Rearrangement
- Duplicate counting

Think

```
Hash Map

Character

↓

Frequency
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Sort both strings.

If they become identical,

they are anagrams.

______________________________________________________________________

## Algorithm

Input

```
listen

silent
```

Sort

```
eilnst

eilnst
```

Equal.

Return

```
True
```

______________________________________________________________________

## Dry Run

Input

```
rat

car
```

Sort

```
art
```

```
acr
```

Different.

Return

```
False
```

______________________________________________________________________

## Complexity

Sorting

```
O(n log n)
```

Space

Depends on implementation.

Usually

```
O(n)
```

______________________________________________________________________

## Limitations

Sorting performs more work than necessary.

We don't care about order.

We only care about counts.

Can we count instead?

Yes.

______________________________________________________________________

# Optimized Solution (Hash Map)

## Key Insight

Instead of sorting,

count how many times each character appears.

If both strings have identical frequency maps,

they are anagrams.

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
anagram

nagaram
```

Count first string.

```
a

↓

3
```

```
n

↓

1
```

```
g

↓

1
```

```
r

↓

1
```

```
m

↓

1
```

Frequency Map

```
{
a:3,
n:1,
g:1,
r:1,
m:1
}
```

______________________________________________________________________

Now process

```
nagaram
```

Subtract counts.

Eventually

```
a

↓

0
```

```
n

↓

0
```

Everything becomes

```
0
```

Return

```
True
```

______________________________________________________________________

# Alternative Approach

Instead of:

```
Increase

↓

Decrease
```

You can build two frequency maps.

Compare them.

```
Map 1

==

Map 2
```

Also works.

______________________________________________________________________

# Dry Run

Input

```
cat

tac
```

Build map

```
c

1
```

```
a

1
```

```
t

1
```

Second string

```
t

↓

0
```

```
a

↓

0
```

```
c

↓

0
```

Every count

```
0
```

Anagram.

______________________________________________________________________

# Visual Explanation

```
listen
```

↓

```
l :1

i :1

s :1

t :1

e :1

n :1
```

Second string

```
silent
```

↓

Subtract

```
l

0
```

```
i

0
```

...

Everything

```
0
```

Valid.

______________________________________________________________________

# Why This Works

Loop Invariant:

> After processing characters from both strings, the frequency map always represents the difference between the character counts seen so far.

If,

after processing every character,

every frequency becomes zero,

both strings contain:

- identical characters
- identical counts

Therefore,

they are anagrams.

______________________________________________________________________

# Edge Cases

### Different Lengths

```
cat

cats
```

Immediately return

```
False
```

______________________________________________________________________

### Empty Strings

```
""

""
```

Return

```
True
```

______________________________________________________________________

### Different Characters

```
abc

abd
```

Return

```
False
```

______________________________________________________________________

### Repeated Characters

```
aabb

abab
```

Still an anagram.

______________________________________________________________________

### Unicode Characters

Python dictionaries work correctly with Unicode characters as well.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n log n)
```

Space

```
O(n)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Space

```
O(k)
```

where

```
k
```

is the number of unique characters.

For lowercase English letters,

this is effectively constant.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_anagram(first: str, second: str) -> bool:
    return sorted(first) == sorted(second)
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import Dict


def is_anagram(first: str, second: str) -> bool:
    if len(first) != len(second):
        return False

    frequency: Dict[str, int] = {}

    for character in first:
        frequency[character] = (
            frequency.get(character, 0) + 1
        )

    for character in second:
        if character not in frequency:
            return False

        frequency[character] -= 1

        if frequency[character] < 0:
            return False

    return True


if __name__ == "__main__":
    print(is_anagram("listen", "silent"))
```

______________________________________________________________________

# Even Better Python Solution

Python provides a built-in class for frequency counting.

```python
from collections import Counter


def is_anagram(first: str, second: str) -> bool:
    return Counter(first) == Counter(second)
```

> **Interview Tip:** Use the manual dictionary implementation during interviews unless the interviewer specifically allows library shortcuts. It demonstrates that you understand the underlying algorithm.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Not checking string lengths first.

Different lengths can never be anagrams.

______________________________________________________________________

## Mistake 2

Comparing sets.

Wrong

```python
set(first) == set(second)
```

Example

```
aab

ab
```

Sets are equal,

but frequencies differ.

______________________________________________________________________

## Mistake 3

Forgetting repeated characters.

Counts matter,

not just presence.

______________________________________________________________________

## Mistake 4

Sorting immediately.

Hash Maps give a better solution.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution sorts both strings and compares them, which takes O(n log n) time. Since order doesn't matter, only frequency does. I can use a hash map to count characters in the first string and subtract counts while processing the second string. If every count returns to zero, the strings are anagrams. This reduces the time complexity to O(n)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why check lengths first?**

Different lengths cannot have identical character frequencies.

______________________________________________________________________

**Q. Why not compare sets?**

Sets ignore duplicate counts.

```
aab

ab
```

would incorrectly appear equal.

______________________________________________________________________

**Q. Why use a Hash Map?**

It provides O(1) average-time insertions and lookups,

making the overall solution O(n).

______________________________________________________________________

**Q. What if only lowercase English letters are allowed?**

You could use a fixed-size array of length 26 instead of a dictionary.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Frequency Counting |
| Recognition | Same Characters / Counts |
| Brute Force | Sort |
| Optimized | Hash Map |
| Time | O(n) |
| Space | O(k) |

______________________________________________________________________

# Quick Revision

- Order doesn't matter.
- Frequency does matter.
- Check lengths first.
- Sorting gives O(n log n).
- Hash Map gives O(n).
- Don't compare sets.
- Dictionaries are ideal for frequency counting.
- This is the foundation for many Hash Map interview questions.

______________________________________________________________________

# Practice Questions

## Easy

1. Ransom Note
1. First Unique Character in a String
1. Find the Difference

______________________________________________________________________

## Medium

4. Group Anagrams
1. Determine if Two Strings Are Close
1. Find All Anagrams in a String
1. Sort Characters by Frequency

______________________________________________________________________

## Hard (Optional)

8. Minimum Window Substring
1. Substring with Concatenation of All Words
1. Word Pattern II

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is recognizing when **frequency is more important than order**. Whenever a question
asks whether two collections contain the same elements with the same counts, think **Hash Map + Frequency Counting**
instead of sorting. This pattern is one of the most common in backend engineering and coding interviews.

______________________________________________________________________

# Next

[20-longest-common-prefix.md](20-longest-common-prefix.md)
