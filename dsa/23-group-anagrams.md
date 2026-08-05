# 23-group-anagrams.md

# Group Anagrams

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 25–30 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem is a natural extension of **Valid Anagram**.

Previously, we answered:

> "Are these two strings anagrams?"

Now the question becomes:

> "Can you automatically group **all** anagrams together?"

Interviewers are testing whether you understand:

- Hash Maps
- Grouping data
- Choosing the correct key
- Frequency vs Sorting
- Mapping multiple values to one key

This pattern appears frequently in backend engineering:

- Grouping users
- Grouping logs
- Aggregation
- MapReduce
- SQL GROUP BY
- Analytics pipelines

______________________________________________________________________

# Problem Statement

Given an array of strings,

group the anagrams together.

Return the groups in any order.

______________________________________________________________________

## Example 1

```text
Input

["eat","tea","tan","ate","nat","bat"]
```

Output

```text
[
    ["eat","tea","ate"],
    ["tan","nat"],
    ["bat"]
]
```

______________________________________________________________________

## Example 2

```text
Input

[""]
```

Output

```text
[
    [""]
]
```

______________________________________________________________________

## Example 3

```text
Input

["a"]
```

Output

```text
[
    ["a"]
]
```

______________________________________________________________________

# Simple English

Imagine several bags of letters.

```
eat

↓

e a t
```

```
tea

↓

t e a
```

```
ate

↓

a t e
```

All contain exactly the same letters.

They belong in one group.

______________________________________________________________________

# Backend Engineering Analogy

Suppose millions of log files arrive.

```
ERROR

ERROR

INFO

WARNING

INFO
```

You don't want individual logs.

You want groups.

```
ERROR

↓

[log1, log5]
```

```
INFO

↓

[log2, log6]
```

The Hash Map key becomes:

```
Log Level
```

Similarly,

for this problem,

the key is:

```
Canonical Representation
```

of the word.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Hash Map for Grouping**

______________________________________________________________________

## Recognition Clues

Whenever the question contains:

- Group
- Categorize
- Aggregate
- Same property
- Buckets

Think

```
Hash Map

Key

↓

List of Values
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Take every word.

Compare it with every remaining word.

If they are anagrams,

put them in the same group.

______________________________________________________________________

## Algorithm

Input

```
eat

tea

tan

ate
```

Compare

```
eat

↓

tea

✔
```

Compare

```
eat

↓

tan

✖
```

Compare

```
eat

↓

ate

✔
```

Continue.

______________________________________________________________________

## Complexity

Suppose

```
n

words
```

Every pair is compared.

Each comparison costs

```
O(k)
```

where

```
k

=

word length
```

Overall

```
O(n² × k)
```

Too slow.

______________________________________________________________________

# Better Solution (Sorting Key)

## Key Insight

If two words are anagrams,

their sorted versions are identical.

Example

```
eat

↓

aet
```

```
tea

↓

aet
```

```
ate

↓

aet
```

Perfect.

Use

```
Sorted Word
```

as the Hash Map key.

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
eat
```

Sort

```
aet
```

Hash Map

```
aet

↓

[eat]
```

______________________________________________________________________

Read

```
tea
```

Sort

```
aet
```

Append

```
aet

↓

[eat,tea]
```

______________________________________________________________________

Read

```
ate
```

Append

```
[eat,tea,ate]
```

Done.

______________________________________________________________________

# Dry Run

Input

```
["eat","tea","tan","ate","nat","bat"]
```

| Word | Sorted Key | Hash Map |
|------|------------|----------|
|eat|aet|aet → [eat]|
|tea|aet|aet → [eat, tea]|
|tan|ant|ant → [tan]|
|ate|aet|aet → [eat, tea, ate]|
|nat|ant|ant → [tan, nat]|
|bat|abt|abt → [bat]|

Return

```
[
[eat,tea,ate],

[tan,nat],

[bat]
]
```

______________________________________________________________________

# Optimized Solution (Character Frequency Key)

## Why Another Solution?

Sorting each word costs

```
O(k log k)
```

Can we avoid sorting?

Yes.

Count character frequencies.

______________________________________________________________________

Example

```
eat
```

Frequency

```
a

1
```

```
e

1
```

```
t

1
```

Everything else

```
0
```

Represent as

```
(1,0,0,0,1,...)
```

This tuple uniquely identifies the anagram group.

______________________________________________________________________

# Step-by-Step Algorithm

Word

```
eat
```

Frequency Array

```
a

1
```

```
b

0
```

...

```
e

1
```

...

```
t

1
```

Convert

```
List

↓

Tuple
```

Use tuple as Hash Map key.

______________________________________________________________________

# Visual Explanation

Input

```
eat

tea

ate
```

↓

Sorted

```
aet

aet

aet
```

↓

Hash Map

```
aet

↓

eat

tea

ate
```

Final Group

```
[eat,tea,ate]
```

______________________________________________________________________

# Why This Works

Loop Invariant:

> After processing each word, the hash map contains correctly grouped anagrams for all processed words.

Every anagram has the same canonical representation.

That representation can be:

- Sorted word
- Frequency tuple

Therefore,

every matching word lands in the same bucket.

______________________________________________________________________

# Choosing the Right Key

## Option 1

Sorted String

```
eat

↓

aet
```

Pros

- Easy
- Readable

Cons

- Sorting costs

```
O(k log k)
```

______________________________________________________________________

## Option 2

Frequency Tuple

```
(1,0,0,...)
```

Pros

- Linear time

```
O(k)
```

Cons

- More code
- Usually assumes lowercase English letters

______________________________________________________________________

# Edge Cases

### Empty List

```
[]
```

Return

```
[]
```

______________________________________________________________________

### Empty String

```
[""]
```

Return

```
[[""]]
```

______________________________________________________________________

### One Word

```
["python"]
```

Return

```
[["python"]]
```

______________________________________________________________________

### Duplicate Words

```
["eat","eat"]
```

Both belong in the same group.

______________________________________________________________________

### Unicode Characters

Sorting solution works naturally.

Frequency-array solution would need modification.

______________________________________________________________________

# Complexity Analysis

Assume

```
n

=

number of words
```

```
k

=

average word length
```

______________________________________________________________________

## Brute Force

Time

```
O(n² × k)
```

Space

```
O(n)
```

______________________________________________________________________

## Sorting Key

Time

```
O(n × k log k)
```

Space

```
O(n × k)
```

______________________________________________________________________

## Frequency Key

Time

```
O(n × k)
```

Space

```
O(n × k)
```

Best asymptotic solution.

______________________________________________________________________

# Production-Quality Python

## Sorting Key (Recommended)

```python
from collections import defaultdict
from typing import DefaultDict, List


def group_anagrams(words: List[str]) -> List[List[str]]:
    groups: DefaultDict[str, List[str]] = defaultdict(list)

    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)

    return list(groups.values())


if __name__ == "__main__":
    values = ["eat", "tea", "tan", "ate", "nat", "bat"]

    print(group_anagrams(values))
```

______________________________________________________________________

## Optimized (Frequency Key)

```python
from collections import defaultdict
from typing import DefaultDict, List, Tuple


def group_anagrams(words: List[str]) -> List[List[str]]:
    groups: DefaultDict[Tuple[int, ...], List[str]] = defaultdict(list)

    for word in words:
        frequency = [0] * 26

        for character in word:
            frequency[ord(character) - ord("a")] += 1

        groups[tuple(frequency)].append(word)

    return list(groups.values())
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using the original word as the Hash Map key.

```
eat

≠

tea
```

Need a canonical representation.

______________________________________________________________________

## Mistake 2

Sorting the entire list.

We sort **each word**,

not the list of words.

______________________________________________________________________

## Mistake 3

Using a list as a dictionary key.

Lists are mutable.

Use

```
Tuple
```

instead.

______________________________________________________________________

## Mistake 4

Not recognizing this as a grouping problem.

Whenever you hear

```
Group

↓

Hash Map
```

should come to mind.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The brute-force solution compares every pair of words, which is too slow. Instead, I need a way to identify anagrams using a common key. Sorting each word produces the same result for all anagrams, so I can use the sorted word as the key in a hash map whose value is a list of matching words. If I want to optimize further, I can replace sorting with a character frequency tuple."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does sorting work?**

Because anagrams contain the same letters,

and sorting places them in the same order.

______________________________________________________________________

**Q. Why use `defaultdict(list)`?**

It automatically creates an empty list for new keys,

avoiding manual initialization.

______________________________________________________________________

**Q. Why use a tuple for the frequency array?**

Dictionary keys must be immutable.

Lists are mutable.

Tuples are immutable.

______________________________________________________________________

**Q. Which solution would you choose in production?**

For readability,

the sorting solution is usually preferred.

If performance is critical and the character set is fixed,

the frequency solution is faster.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Hash Map Grouping |
| Recognition | Group by Shared Property |
| Brute Force | Compare Every Pair |
| Better | Sorted String Key |
| Optimized | Frequency Tuple Key |
| Time | O(n × k log k) / O(n × k) |
| Space | O(n × k) |

______________________________________________________________________

# Quick Revision

- Grouping problems usually use a Hash Map.
- Every group needs a canonical key.
- Sorted strings make excellent keys.
- Frequency tuples avoid sorting.
- `defaultdict(list)` simplifies grouping.
- Tuples can be dictionary keys; lists cannot.
- Sorting solution is easier to explain.
- Frequency solution is asymptotically faster.

______________________________________________________________________

# Practice Questions

## Easy

1. Valid Anagram
1. Find Common Characters
1. Ransom Note

______________________________________________________________________

## Medium

4. Top K Frequent Words
1. Sort Characters by Frequency
1. Find All Anagrams in a String
1. Partition Labels

______________________________________________________________________

## Hard (Optional)

8. Word Ladder
1. Word Search II
1. Alien Dictionary

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning the **Hash Map Grouping** pattern. Instead of comparing every pair of
objects, compute a **canonical representation** (such as a sorted string or a frequency tuple) and use it as the key.
This approach is widely used in backend systems for grouping logs, aggregating analytics, deduplicating records, and
implementing SQL-like `GROUP BY` operations.

______________________________________________________________________

# Next

[24-merge-sorted-array.md](24-merge-sorted-array.md)
