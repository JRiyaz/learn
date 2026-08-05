# 16-reverse-string.md

# Reverse String

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This looks like one of the easiest interview questions.

It isn't.

Interviewers use this problem to evaluate whether you understand:

- Two Pointer technique
- In-place modification
- Swapping
- String vs Array differences
- Time and space optimization

Most interview versions (like LeetCode 344) specifically say:

> **Modify the character array in-place using O(1) extra space.**

The problem is not about reversing text.

It's about recognizing the **Two Pointer Pattern**.

______________________________________________________________________

# Problem Statement

Given an array of characters,

reverse the array **in-place**.

You must not create another array.

______________________________________________________________________

## Example 1

```text
Input

["h","e","l","l","o"]
```

Output

```text
["o","l","l","e","h"]
```

______________________________________________________________________

## Example 2

```text
Input

["H","a","n","n","a","h"]
```

Output

```text
["h","a","n","n","a","H"]
```

______________________________________________________________________

# Simple English

Imagine five people standing in a line.

```
A B C D E
```

The first and last person swap places.

```
E B C D A
```

Then,

the second and second-last swap.

```
E D C B A
```

The middle person never moves.

That's exactly how the algorithm works.

______________________________________________________________________

# Common Misunderstandings

Many beginners think:

```python
reversed_string = string[::-1]
```

or

```python
string.reverse()
```

These solve the problem in Python,

but they **don't demonstrate the algorithm**.

Interviewers want to see:

- Pointer movement
- Swapping
- In-place modification

______________________________________________________________________

# Backend Engineering Analogy

Suppose a networking system stores packet bytes.

```
A B C D E
```

To decode a protocol,

the byte order must be reversed.

Instead of allocating another buffer,

the system swaps bytes directly inside memory.

This saves memory and improves performance.

The same technique appears in:

- Memory buffers
- Network protocols
- Image processing
- Binary file manipulation

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers (Opposite Direction)**

______________________________________________________________________

## Recognition Clues

Whenever the question contains:

- Reverse
- Swap ends
- Palindrome
- Mirror
- In-place
- Character array

Think

```
Left Pointer

+

Right Pointer
```

Move toward the center.

______________________________________________________________________

# Brute Force Solution

## Intuition

Create another array.

Traverse from the end toward the beginning.

Copy elements into the new array.

______________________________________________________________________

## Algorithm

Input

```
h e l l o
```

New array

```
[]
```

Copy

```
o

↓

o l

↓

o l l

↓

o l l e

↓

o l l e h
```

______________________________________________________________________

## Dry Run

Input

```
a b c d
```

Result

```
d c b a
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

## Limitations

Creates another array.

Interview asks for

```
O(1)
```

extra space.

______________________________________________________________________

# Optimized Solution (Two Pointers)

## Key Insight

Instead of copying,

swap.

Use:

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

Swap,

then move inward.

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
h e l l o
```

Initially

```
L         R

h e l l o
```

Swap

```
o e l l h
```

Move both.

______________________________________________________________________

Now

```
  L     R

o e l l h
```

Swap

```
o l l e h
```

Move both.

______________________________________________________________________

Now

```
    L R

o l l e h
```

Pointers meet.

Done.

______________________________________________________________________

# Dry Run

```
Input

A B C D E
```

Step 1

```
Swap

A

E
```

```
E B C D A
```

______________________________________________________________________

Step 2

Swap

```
B

D
```

```
E D C B A
```

Done.

______________________________________________________________________

# Visual Explanation

Original

```
A B C D E

L       R
```

↓

Swap

```
E B C D A

  L   R
```

↓

Swap

```
E D C B A

    LR
```

Finished.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration, all characters outside the range `[left, right]` are already in their correct reversed positions.

Each swap correctly places:

- One character at the beginning
- One character at the end

After every iteration,

the unsolved portion becomes smaller.

Eventually,

the pointers meet.

Every character reaches its correct position.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

No changes.

______________________________________________________________________

### One Character

```
A
```

Already reversed.

______________________________________________________________________

### Two Characters

```
A B
```

↓

```
B A
```

______________________________________________________________________

### Even Length

```
A B C D
```

Two swaps.

______________________________________________________________________

### Odd Length

```
A B C D E
```

Middle character remains unchanged.

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

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def reverse_string(characters: List[str]) -> None:
    reversed_characters = []

    for index in range(len(characters) - 1, -1, -1):
        reversed_characters.append(characters[index])

    characters[:] = reversed_characters
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def reverse_string(characters: List[str]) -> None:
    left = 0
    right = len(characters) - 1

    while left < right:
        characters[left], characters[right] = (
            characters[right],
            characters[left],
        )

        left += 1
        right -= 1


if __name__ == "__main__":
    values = ["h", "e", "l", "l", "o"]

    reverse_string(values)

    print(values)
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating another array.

The interviewer specifically asks for in-place modification.

______________________________________________________________________

## Mistake 2

Forgetting to move both pointers.

After every swap,

move

```python
left += 1
right -= 1
```

______________________________________________________________________

## Mistake 3

Using

```python
while left <= right
```

The middle character doesn't need to swap with itself.

Preferred:

```python
while left < right
```

______________________________________________________________________

## Mistake 4

Trying to modify Python strings.

Remember:

```python
text = "hello"
```

Strings are **immutable**.

Interview versions usually provide

```python
List[str]
```

instead.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution creates another array and copies characters in reverse order, but that uses O(n) extra space. Since the problem requires in-place modification, I'll use two pointers. One starts at the beginning and the other at the end. I swap their values and move both pointers toward the center until they meet."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use two pointers?**

Because each swap correctly places two characters.

______________________________________________________________________

**Q. Why stop when pointers meet?**

At that point,

every character has reached its final position.

______________________________________________________________________

**Q. Why not use slicing?**

Because interviewers want the algorithm,

not the built-in shortcut.

______________________________________________________________________

**Q. Does this work for Unicode characters?**

Yes,

as long as the input is a list of characters.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers |
| Recognition | Reverse / Mirror |
| Brute Force | Extra Array |
| Optimized | Swap Ends |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Reverse using swaps.
- Use left and right pointers.
- Swap both ends.
- Move inward.
- Stop when pointers meet.
- Don't create another array.
- Strings in Python are immutable.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Reverse Vowels of a String
1. Valid Palindrome
1. Reverse Prefix of Word

______________________________________________________________________

## Medium

4. Reverse Words in a String
1. Reverse String II
1. Rotate String
1. Backspace String Compare

______________________________________________________________________

## Hard (Optional)

8. Reverse Nodes in k-Group (Linked List)
1. Shortest Palindrome
1. Minimum Insertions to Form a Palindrome

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is mastering the **Two Pointer (Opposite Direction)** pattern. Whenever you need to
compare, reverse, or process elements from both ends of a sequence, think of placing one pointer at the beginning and
one at the end, then moving them toward each other. This pattern appears repeatedly in string, array, and linked list
interview questions.

______________________________________________________________________

# Next

[17-reverse-words.md](17-reverse-words.md)
