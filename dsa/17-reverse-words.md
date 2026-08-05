# 17-reverse-words.md

# Reverse Words in a String

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐☆ High |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem looks similar to **Reverse String**.

It is not.

Interviewers are testing whether you understand:

- String parsing
- Splitting and joining
- Two Pointer thinking
- Handling multiple spaces
- Input normalization

Many candidates immediately reverse all the characters.

That produces the wrong answer.

The question asks to reverse the **order of words**, **not** the characters inside each word.

______________________________________________________________________

# Problem Statement

Given a string `text`, reverse the order of the words.

Requirements:

- Remove leading spaces.
- Remove trailing spaces.
- Replace multiple spaces between words with a single space.

______________________________________________________________________

## Example 1

```text
Input

"the sky is blue"
```

Output

```text
"blue is sky the"
```

______________________________________________________________________

## Example 2

```text
Input

"  hello world  "
```

Output

```text
"world hello"
```

______________________________________________________________________

## Example 3

```text
Input

"a good   example"
```

Output

```text
"example good a"
```

Notice

Multiple spaces become one.

______________________________________________________________________

# Simple English

Imagine sticky notes on a wall.

```
the

sky

is

blue
```

Don't reverse the letters.

Just reverse the order of the notes.

```
blue

is

sky

the
```

______________________________________________________________________

# Common Misunderstandings

Many beginners reverse the entire string.

Example

```
Input

the sky
```

Wrong

```
yks eht
```

Correct

```
sky the
```

______________________________________________________________________

# Backend Engineering Analogy

Suppose a logging system stores tags.

```
ERROR API DATABASE
```

For display,

the newest tag should appear first.

```
DATABASE API ERROR
```

The tags themselves don't change.

Only their order changes.

Similar operations occur in:

- Search engines
- Log processing
- Query parsing
- Command interpreters

______________________________________________________________________

# Pattern Recognition

## Pattern

**Split → Process → Join**

or

**Two Pointers (Advanced In-place Version)**

______________________________________________________________________

## Recognition Clues

Whenever the question contains:

- Reverse words
- Sentence
- Spaces
- Tokens
- Parsing

Think

```
Split

↓

Process

↓

Join
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Split the sentence into words.

Reverse the list.

Join the words back together.

______________________________________________________________________

## Algorithm

Input

```
the sky is blue
```

Split

```
["the","sky","is","blue"]
```

Reverse

```
["blue","is","sky","the"]
```

Join

```
blue is sky the
```

Done.

______________________________________________________________________

## Dry Run

Input

```
hello world
```

Split

```
["hello","world"]
```

Reverse

```
["world","hello"]
```

Join

```
world hello
```

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Why Does `split()` Handle Multiple Spaces?

Python's

```python
split()
```

(without arguments)

automatically:

- removes leading spaces
- removes trailing spaces
- ignores multiple spaces

Example

```python
"   hello   world   ".split()
```

Result

```python
["hello", "world"]
```

This is one reason the brute-force solution is both simple and practical in Python.

______________________________________________________________________

# Better Solution (Manual Parsing)

## Why Learn This?

Some interviewers may ask:

> "Suppose you cannot use `split()`."

Then,

you manually build words.

______________________________________________________________________

## Algorithm

Read characters one by one.

```
Current Word

↓

Completed Word

↓

Store
```

Skip extra spaces.

Example

```
the   sky
```

Build

```
the
```

Store.

Skip spaces.

Build

```
sky
```

Store.

Reverse.

Join.

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Optimized Solution (In-place Character Array)

> **Interview Note:** This solution is rarely expected in startup interviews, but it is sometimes asked in senior interviews or when the interviewer explicitly asks for **O(1)** extra space.

______________________________________________________________________

## Key Insight

Instead of reversing words,

reverse the **entire string first**.

Example

```
the sky is blue
```

Reverse characters

```
eulb si yks eht
```

Now,

reverse every word individually.

```
blue is sky the
```

Done.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
the sky
```

Reverse everything

```
yks eht
```

Reverse first word

```
sky eht
```

Reverse second word

```
sky the
```

Finished.

______________________________________________________________________

# Visual Explanation

Original

```
the sky is blue
```

↓

Reverse All

```
eulb si yks eht
```

↓

Reverse Each Word

```
blue is sky the
```

______________________________________________________________________

# Why This Works

Think of the sentence as:

```
Word1 Space Word2 Space Word3
```

Reversing everything changes:

- Word order ✔
- Character order ✖

Reversing each individual word fixes the characters.

The overall word order remains reversed.

______________________________________________________________________

# Edge Cases

### Empty String

```
""
```

Output

```
""
```

______________________________________________________________________

### Only Spaces

```
"      "
```

Output

```
""
```

______________________________________________________________________

### One Word

```
Python
```

No change.

______________________________________________________________________

### Multiple Spaces

```
a    b     c
```

Output

```
c b a
```

______________________________________________________________________

### Leading & Trailing Spaces

```
 hello world
```

↓

```
world hello
```

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

## Manual Parsing

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## In-place Character Array

Time

```
O(n)
```

Space

```
O(1)
```

(If mutable character array is provided.)

______________________________________________________________________

# Production-Quality Python

## Brute Force (Recommended for Python)

```python
def reverse_words(text: str) -> str:
    words = text.split()

    words.reverse()

    return " ".join(words)


if __name__ == "__main__":
    sentence = "  the   sky is   blue "

    print(reverse_words(sentence))
```

______________________________________________________________________

## Manual Parsing (Without `split()`)

```python
def reverse_words(text: str) -> str:
    words = []
    current_word = []

    for character in text:
        if character != " ":
            current_word.append(character)
        elif current_word:
            words.append("".join(current_word))
            current_word = []

    if current_word:
        words.append("".join(current_word))

    words.reverse()

    return " ".join(words)
```

______________________________________________________________________

# Optimized (Character Array Concept)

```python
# Concept only

1. Reverse entire character array.
2. Reverse every individual word.
3. Remove extra spaces (if required).
```

In Python,

strings are immutable,

so the brute-force solution using `split()` and `join()` is generally preferred in production.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Reversing characters instead of words.

______________________________________________________________________

## Mistake 2

Using

```python
split(" ")
```

instead of

```python
split()
```

Difference:

```python
"  hello   world  ".split(" ")
```

Produces

```python
['', '', 'hello', '', '', 'world', '', '']
```

Whereas

```python
split()
```

Produces

```python
['hello', 'world']
```

______________________________________________________________________

## Mistake 3

Forgetting to remove extra spaces.

______________________________________________________________________

## Mistake 4

Trying to modify a Python string in-place.

Strings are immutable.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The easiest solution is to split the sentence into words, reverse the list, and join it back together. Python's `split()` conveniently removes extra spaces. If the interviewer restricts the use of `split()`, I can manually parse the string. If they further require O(1) extra space, I can reverse the entire character array and then reverse each word individually."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use `split()` instead of `split(" ")`?**

Because `split()` automatically handles multiple spaces and trims leading/trailing spaces.

______________________________________________________________________

**Q. Can this be done in-place?**

Yes,

if the input is a mutable character array.

______________________________________________________________________

**Q. Why reverse twice?**

The first reversal changes the word order.

The second reversal restores the characters inside each word.

______________________________________________________________________

**Q. What interview pattern does this teach?**

Tokenization and the **Reverse-All, Reverse-Parts** pattern.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Split → Reverse → Join |
| Recognition | Reverse Words |
| Brute Force | Split + Reverse |
| Better | Manual Parsing |
| Optimized | Reverse All + Reverse Each Word |
| Time | O(n) |
| Space | O(n) (Python) |

______________________________________________________________________

# Quick Revision

- Reverse words, not characters.
- `split()` removes unnecessary spaces automatically.
- Reverse the list of words.
- Join using a single space.
- Manual parsing is useful when `split()` isn't allowed.
- In-place solutions reverse the whole string first, then each word.
- Python strings are immutable.
- Time complexity is O(n).

______________________________________________________________________

# Practice Questions

## Easy

1. Reverse String
1. Length of Last Word
1. Reverse Prefix of Word

______________________________________________________________________

## Medium

4. Reverse Words in a String II
1. Reverse Words in a String III
1. Text Justification
1. Goat Latin

______________________________________________________________________

## Hard (Optional)

8. Minimum Remove to Make Valid Parentheses
1. Basic Calculator
1. Simplify Path

______________________________________________________________________

# Key Takeaway

The biggest lesson is distinguishing between **reversing characters** and **reversing logical units (words)**. This
problem introduces the idea of **tokenizing**, processing tokens, and reconstructing the result—an approach commonly
used in compilers, log processors, search engines, and backend text-processing systems.

______________________________________________________________________

# Next

[18-valid-palindrome.md](18-valid-palindrome.md)
