# 18-valid-palindrome.md

# Valid Palindrome

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

This is one of the most frequently asked **Two Pointer** interview questions.

It looks simple:

> "Check whether a string is a palindrome."

But interviewers are actually testing:

- Two Pointer technique
- String traversal
- Character validation
- Case normalization
- Ignoring irrelevant characters
- Writing clean conditional logic

Many candidates immediately reverse the string.

Interviewers often ask:

> "Can you do it without creating another string?"

This leads to the optimal Two Pointer solution.

______________________________________________________________________

# Problem Statement

Given a string `text`,

determine whether it is a palindrome.

Rules:

- Ignore uppercase/lowercase differences.
- Ignore spaces.
- Ignore punctuation.
- Consider only alphanumeric characters.

Return:

- `True`
- `False`

______________________________________________________________________

## Example 1

```text
Input

"A man, a plan, a canal: Panama"
```

Output

```text
True
```

Because after removing non-alphanumeric characters:

```
amanaplanacanalpanama
```

which reads the same from both directions.

______________________________________________________________________

## Example 2

```text
Input

"race a car"
```

Output

```text
False
```

______________________________________________________________________

## Example 3

```text
Input

" "
```

Output

```text
True
```

An empty string is considered a palindrome.

______________________________________________________________________

# Simple English

Imagine writing a word on paper.

Now,

read it:

```
Left → Right
```

and

```
Right → Left
```

If both readings are identical,

it's a palindrome.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a system validating a product code.

```
AB-123-BA
```

Hyphens don't matter.

Uppercase/lowercase doesn't matter.

Only the meaningful characters matter.

Similarly,

our algorithm ignores:

- Spaces
- Symbols
- Punctuation

and compares only valid characters.

______________________________________________________________________

# Common Misunderstandings

Many beginners think

```
"A man, a plan, a canal: Panama"
```

is **not** a palindrome because of spaces and punctuation.

Interview questions explicitly tell us to ignore them.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers (Opposite Direction)**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Palindrome
- Compare both ends
- Ignore characters
- Mirror
- Symmetry

Think

```
Left Pointer

↓

Beginning
```

```
Right Pointer

↓

End
```

Move inward.

______________________________________________________________________

# Brute Force Solution

## Intuition

Normalize the string first.

Steps:

1. Remove non-alphanumeric characters.
1. Convert to lowercase.
1. Reverse the cleaned string.
1. Compare.

______________________________________________________________________

## Algorithm

Input

```
RaceCar
```

Lowercase

```
racecar
```

Reverse

```
racecar
```

Compare

```
Equal

↓

Palindrome
```

______________________________________________________________________

## Dry Run

Input

```
A man
```

Clean

```
aman
```

Reverse

```
nama
```

Different.

Return

```
False
```

______________________________________________________________________

## Complexity

Cleaning

```
O(n)
```

Reverse

```
O(n)
```

Comparison

```
O(n)
```

Overall

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Limitations

Creates another string.

Can we avoid that?

Yes.

______________________________________________________________________

# Optimized Solution (Two Pointers)

## Key Insight

We don't need to create another string.

We compare characters directly from both ends.

If a character isn't alphanumeric,

skip it.

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
A man, a plan, a canal: Panama
```

Initially

```
L                               R
```

Compare

```
A

a
```

Equal.

Move both.

______________________________________________________________________

Left points to

```
(space)
```

Ignore.

______________________________________________________________________

Right points to

```
:
```

Ignore.

______________________________________________________________________

Compare

```
m

m
```

Equal.

Continue.

Eventually,

all comparisons succeed.

Return

```
True
```

______________________________________________________________________

# Dry Run

Input

```
race a car
```

Pointers

```
L           R
```

Compare

```
r

r
```

OK.

______________________________________________________________________

Compare

```
a

a
```

OK.

______________________________________________________________________

Compare

```
c

c
```

OK.

______________________________________________________________________

Compare

```
e

a
```

Different.

Return

```
False
```

Stop immediately.

______________________________________________________________________

# Visual Explanation

Input

```
A man, a plan, a canal: Panama
```

```
L                             R
```

↓

Skip

```
Spaces

,

:
```

↓

Compare

```
A == a

✔
```

↓

Move inward

↓

Repeat

↓

Pointers cross

↓

Palindrome

______________________________________________________________________

Example

```
race a car
```

```
L          R
```

↓

Eventually

```
e

≠

a
```

↓

Not a palindrome.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration, all previously compared valid characters from the outside are equal.

Each iteration:

1. Skips invalid characters.
1. Compares valid characters.
1. Moves inward.

If a mismatch occurs,

the string cannot be a palindrome.

If pointers cross,

every mirrored pair matched.

Therefore,

the string is a palindrome.

______________________________________________________________________

# Edge Cases

### Empty String

```
""
```

Palindrome.

______________________________________________________________________

### Only Spaces

```
"     "
```

Palindrome.

______________________________________________________________________

### Only Symbols

```
"!@#$"
```

Palindrome after cleaning.

______________________________________________________________________

### One Character

```
a
```

Palindrome.

______________________________________________________________________

### Mixed Case

```
RaceCar
```

Palindrome.

______________________________________________________________________

### Numbers

```
12321
```

Palindrome.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
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
O(1)
```

No extra string is created.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_palindrome(text: str) -> bool:
    cleaned = []

    for character in text:
        if character.isalnum():
            cleaned.append(character.lower())

    cleaned_text = "".join(cleaned)

    return cleaned_text == cleaned_text[::-1]
```

______________________________________________________________________

## Optimized (Recommended)

```python
def is_palindrome(text: str) -> bool:
    left = 0
    right = len(text) - 1

    while left < right:
        while left < right and not text[left].isalnum():
            left += 1

        while left < right and not text[right].isalnum():
            right -= 1

        if text[left].lower() != text[right].lower():
            return False

        left += 1
        right -= 1

    return True


if __name__ == "__main__":
    sentence = "A man, a plan, a canal: Panama"

    print(is_palindrome(sentence))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Comparing spaces and punctuation.

Always ignore non-alphanumeric characters.

______________________________________________________________________

## Mistake 2

Forgetting to convert to lowercase.

```
A

≠

a
```

unless normalized.

______________________________________________________________________

## Mistake 3

Using

```python
isalpha()
```

instead of

```python
isalnum()
```

Digits are also valid characters.

______________________________________________________________________

## Mistake 4

Not skipping invalid characters before comparison.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution is to clean the string, reverse it, and compare the results. However, that requires extra space. Since we're only comparing mirrored characters, I can use two pointers, skip non-alphanumeric characters, compare lowercase versions, and move inward until the pointers meet."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use two pointers?**

Because palindrome comparison naturally happens from both ends.

______________________________________________________________________

**Q. Why use `isalnum()`?**

Because both letters and digits are considered valid.

______________________________________________________________________

**Q. Why convert to lowercase?**

To make comparisons case-insensitive.

______________________________________________________________________

**Q. What if the string contains only punctuation?**

After ignoring invalid characters,

it becomes an empty string,

which is considered a palindrome.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers |
| Recognition | Palindrome / Symmetry |
| Brute Force | Clean + Reverse |
| Optimized | Two Pointers with Skipping |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Compare from both ends.
- Ignore spaces and punctuation.
- Convert to lowercase.
- Use `isalnum()` to identify valid characters.
- Skip invalid characters before comparison.
- Stop immediately on mismatch.
- If pointers cross, it's a palindrome.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Palindrome Number
1. Reverse String
1. Valid Palindrome II

______________________________________________________________________

## Medium

4. Longest Palindromic Substring
1. Palindromic Substrings
1. Break a Palindrome
1. Shortest Palindrome

______________________________________________________________________

## Hard (Optional)

8. Minimum Insertions to Form a Palindrome
1. Palindrome Partitioning II
1. Shortest Palindrome (KMP)

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is mastering the **Two Pointer (Opposite Direction)** pattern with **conditional
skipping**. Instead of preprocessing the entire string, you process only the characters that matter, achieving the same
result with constant extra space. This technique is widely used in string processing, parsers, compilers, and many
interview problems involving symmetry or comparison.

______________________________________________________________________

# Next

[19-valid-anagram.md](19-valid-anagram.md)
