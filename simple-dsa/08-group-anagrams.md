# 08-group-anagrams.md

# Group Anagrams — The Group By Pattern

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an array of strings `strs`, group the anagrams together.

You may return the answer in any order.

### Example

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

# What Is Actually Being Asked?

The interviewer is asking:

> "How can we identify words that belong to the same group?"

Notice that we don't compare every word with every other word.

Instead, we need to generate a **signature** (or fingerprint) for each word.

Words with the same signature belong to the same group.

______________________________________________________________________

# Real-World Analogy

Imagine a backend service that groups uploaded files by content.

Instead of comparing every file byte-by-byte:

```text
File A ↔ File B
File A ↔ File C
File B ↔ File C
...
```

We compute a checksum (MD5/SHA).

```text
File

↓

Checksum

↓

Group by checksum
```

Likewise, for words:

```text
Word

↓

Signature

↓

Group together
```

Other real-world examples:

- Group users by city
- Orders by customer
- Logs by request ID
- Products by category

______________________________________________________________________

# Pattern Recognition

This problem teaches the **Group By Pattern** using a **Hash Map**.

Interview clues:

- Group similar items
- Cluster
- Categorize
- Same pattern
- Same frequency
- Same composition

Think:

> **Generate a key → Store in Hash Map**

______________________________________________________________________

# Brute Force Solution

## Intuition

Compare every word with every other word.

If two words are anagrams,

put them into the same group.

Example

```text
eat

↓

Compare with tea

↓

Compare with tan

↓

Compare with ate
```

Repeat for every word.

______________________________________________________________________

## Complexity

If there are `n` words of average length `k`:

```text
O(n² × k log k)
```

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

Instead of comparing words,

generate a unique key.

Two common choices:

### Option 1 (Most Common)

Sort characters.

```text
eat

↓

aet
```

```text
tea

↓

aet
```

Same key.

Same group.

______________________________________________________________________

### Option 2 (More Optimal)

Count character frequencies.

```text
a -> 1
e -> 1
t -> 1
```

Represent this as a tuple.

This avoids sorting and runs in O(k).

______________________________________________________________________

# Visual Explanation

Input

```text
eat
tea
tan
ate
nat
bat
```

Generate Keys

```text
eat → aet

tea → aet

tan → ant

ate → aet

nat → ant

bat → abt
```

Hash Map

```text
aet

↓

[eat, tea, ate]
```

```text
ant

↓

[tan, nat]
```

```text
abt

↓

[bat]
```

Result

```text
[
  [eat, tea, ate],
  [tan, nat],
  [bat]
]
```

______________________________________________________________________

# Step-by-Step Algorithm

Create empty dictionary.

For each word:

1. Generate key.
1. If key doesn't exist:
   - create empty list.
1. Append word.

Return all dictionary values.

______________________________________________________________________

# Why This Works

Every anagram produces the same signature.

Different words produce different signatures.

Therefore,

all words with identical keys naturally fall into the same dictionary entry.

______________________________________________________________________

# Edge Cases

## Empty Input

```text
[]
```

Return

```text
[]
```

______________________________________________________________________

## One Word

```text
["abc"]
```

Return

```text
[
  ["abc"]
]
```

______________________________________________________________________

## Duplicate Words

```text
["abc","abc"]
```

Both belong to the same group.

______________________________________________________________________

## Empty Strings

```text
["","",""]
```

All have the same signature.

One group.

______________________________________________________________________

# Complexity Analysis

## Sorting Approach

Let

```text
n = number of words

k = average word length
```

Sorting each word

```text
O(k log k)
```

Overall

```text
O(n × k log k)
```

Space

```text
O(n × k)
```

______________________________________________________________________

## Frequency Count Approach

Generating frequency array

```text
O(k)
```

Overall

```text
O(n × k)
```

Slightly faster, especially for long strings.

______________________________________________________________________

# Production-Quality Python

## Approach 1 (Recommended for Interviews)

```python
from collections import defaultdict
from typing import List


def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups anagrams together.

    Time Complexity: O(n × k log k)
    Space Complexity: O(n × k)
    """

    groups = defaultdict(list)

    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)

    return list(groups.values())
```

______________________________________________________________________

## Approach 2 (Frequency Count)

```python
from collections import defaultdict
from typing import List, Tuple


def group_anagrams(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)

    for word in strs:
        frequency = [0] * 26

        for char in word:
            frequency[ord(char) - ord("a")] += 1

        groups[tuple(frequency)].append(word)

    return list(groups.values())
```

______________________________________________________________________

# Common Mistakes

## 1. Comparing Every Pair

Results in

```text
O(n²)
```

Avoid pairwise comparisons.

______________________________________________________________________

## 2. Using List as Dictionary Key

Wrong

```python
frequency = [1,0,2]

dictionary[frequency]
```

Lists are mutable.

Use

```python
tuple(frequency)
```

instead.

______________________________________________________________________

## 3. Forgetting Empty Groups

Create the list before appending.

`defaultdict(list)` simplifies this.

______________________________________________________________________

## 4. Using `set(word)` as Key

Wrong.

Example

```text
abb

bab
```

Both work.

But

```text
abb

ab
```

Would incorrectly appear similar because sets ignore frequency.

______________________________________________________________________

# Variations

## Easy

- Valid Anagram

______________________________________________________________________

## Medium

- Group Shifted Strings
- Find All Anagrams in a String
- Top K Frequent Words
- Partition Labels

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Brute force compares every word.
1. That's expensive.
1. Generate a unique signature.
1. Use a Hash Map.
1. Return grouped values.

______________________________________________________________________

### Common Follow-ups

### Q: Why does sorting work?

Because all anagrams produce the same sorted string.

Example

```text
eat

↓

aet
```

```text
tea

↓

aet
```

______________________________________________________________________

### Q: Which approach is faster?

Frequency counting:

```text
O(n × k)
```

Sorting:

```text
O(n × k log k)
```

______________________________________________________________________

### Q: Which should you use in interviews?

Sorting is simpler, easier to explain, and usually preferred unless the interviewer specifically asks for further
optimization.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Group By |
| Recognition | Group similar items |
| Brute Force | Compare every pair |
| Optimal | Hash Map + Signature |
| Signature | Sorted string or frequency tuple |
| Time | O(n × k log k) |

______________________________________________________________________

# Practice Problems

## Easy

1. Valid Anagram
1. Find the Difference

## Medium

1. Find All Anagrams in a String
1. Group Shifted Strings
1. Top K Frequent Words
1. Encode and Decode Strings

## Hard

1. Word Squares
1. Word Ladder II

______________________________________________________________________

# Quick Revision

- Don't compare every word with every other word.
- Generate a unique **signature** for each word.
- Store groups in a Hash Map.
- Two common signatures:
  - Sorted string
  - Frequency tuple
- `defaultdict(list)` simplifies grouping.
- Sorting approach: **O(n × k log k)**
- Frequency approach: **O(n × k)**

______________________________________________________________________

# Key Takeaway

This problem introduces one of the most reusable interview ideas:

> **If similar items share a common property, convert that property into a key and use a Hash Map to group them.**

You'll reuse this pattern in problems involving:

- Grouping records
- Categorization
- Bucketing
- Aggregation
- Database-style `GROUP BY`
- Log and analytics processing

______________________________________________________________________

# Navigation

**Previous**

[07-valid-anagram.md](07-valid-anagram.md)

**Next**

[09-top-k-frequent-elements.md](09-top-k-frequent-elements.md)
