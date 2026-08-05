# 27-valid-parentheses.md

# Valid Parentheses

> **🎯 This is your first Stack problem.**
>
> If Sliding Window taught you how to manage a moving range,
> **Stacks teach you how to remember unfinished work.**
>
> This is one of the most important data structures in interviews and real-world backend systems.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem isn't really about parentheses.

Interviewers want to know if you understand:

- Stack data structure
- Last-In-First-Out (LIFO)
- Matching pairs
- Nested structures
- Parsing algorithms

Understanding this problem prepares you for:

- HTML/XML parsing
- JSON validation
- Compiler design
- Expression evaluation
- DFS (Graph)
- Function call stack
- Undo/Redo systems

______________________________________________________________________

# Problem Statement

Given a string containing only

```text
()

{}

[]
```

determine whether it is valid.

A string is valid if:

1. Every opening bracket has a matching closing bracket.
1. The brackets close in the correct order.
1. Every closing bracket matches the most recent unmatched opening bracket.

Return:

```text
True
```

or

```text
False
```

______________________________________________________________________

## Example 1

```text
Input

"()"
```

Output

```text
True
```

______________________________________________________________________

## Example 2

```text
Input

"()[]{}"
```

Output

```text
True
```

______________________________________________________________________

## Example 3

```text
Input

"(]"
```

Output

```text
False
```

______________________________________________________________________

## Example 4

```text
Input

"([)]"
```

Output

```text
False
```

______________________________________________________________________

## Example 5

```text
Input

"{[]}"
```

Output

```text
True
```

______________________________________________________________________

# Before Learning the Algorithm

## Why Doesn't Counting Work?

Many beginners think:

```
Count (

Count )
```

If both are equal,

it's valid.

Wrong.

Example

```
)(
```

Count

```
(

=

1
```

Count

```
)

=

1
```

Equal.

But

```
)(
```

is invalid.

Order matters.

______________________________________________________________________

# Simple English

Imagine a pile of plates.

```
Plate A

↓

Plate B

↓

Plate C
```

To remove plates,

you must first remove

```
Plate C
```

The last plate placed on the stack comes off first.

That's exactly how brackets behave.

______________________________________________________________________

# Backend Engineering Analogy

Imagine parsing a JSON document.

```json
{
    "user": {
        "name": "John"
    }
}
```

When the parser reads

```text
{
```

it remembers:

```
One object started.
```

When another

```text
{
```

appears,

it remembers another.

When

```text
}
```

appears,

it must close the **most recent** object.

This is exactly a Stack.

The same idea appears in:

- XML parsing
- HTML parsing
- Function calls
- Recursive algorithms
- Browser navigation
- Undo/Redo

______________________________________________________________________

# Pattern Recognition

## Pattern

**Stack (LIFO)**

______________________________________________________________________

## Recognition Clues

Whenever the question contains:

- Matching
- Nested
- Balanced
- Expression
- Parsing
- Undo
- Backtracking

Think

```
Stack
```

______________________________________________________________________

# Why Brute Force Fails

Suppose

```
({[]})
```

Can we repeatedly remove

```
()
```

```
[]
```

```
{}
```

until nothing remains?

Yes.

But repeatedly searching and replacing substrings becomes inefficient.

______________________________________________________________________

# Brute Force Solution

## Intuition

Repeatedly remove

```
()
```

```
[]
```

```
{}
```

until no more pairs exist.

______________________________________________________________________

## Algorithm

Input

```
{[]}
```

↓

Remove

```
[]
```

```
{}
```

↓

Remove

```
{}
```

↓

Empty String

↓

Valid.

______________________________________________________________________

## Dry Run

Input

```
([)]
```

Nothing removable.

Still remains.

Invalid.

______________________________________________________________________

## Complexity

Repeated scanning.

Worst case

```
O(n²)
```

Space

```
O(n)
```

______________________________________________________________________

## Limitations

Repeated searching is expensive.

Can we process the string in one pass?

Yes.

______________________________________________________________________

# Optimized Solution (Stack)

## Key Insight

Whenever we see:

```
(

{

[
```

Push it onto the stack.

Whenever we see:

```
)

}

]
```

Check whether it matches the **top** of the stack.

If yes,

Pop.

Otherwise,

Invalid.

______________________________________________________________________

# Understanding the Stack

Initially

```
Stack

[]
```

Read

```
(
```

Push

```
[
(
]
```

Read

```
[
```

Push

```
[
(

[
]
```

Read

```
]
```

Matches

```
[
```

Pop.

Stack

```
[
(
]
```

Read

```
)
```

Matches

```
(
```

Pop.

Stack

```
[]
```

Finished.

Empty stack.

Valid.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
{[]}
```

______________________________________________________________________

Read

```
{
```

Push

```
{
```

______________________________________________________________________

Read

```
[
```

Push

```
{

[
```

______________________________________________________________________

Read

```
]
```

Matches

```
[
```

Pop.

Stack

```
{
```

______________________________________________________________________

Read

```
}
```

Matches

```
{
```

Pop.

Stack

```
Empty
```

Return

```
True
```

______________________________________________________________________

# Another Dry Run

Input

```
([)]
```

Read

```
(
```

Push.

______________________________________________________________________

Read

```
[
```

Push.

______________________________________________________________________

Read

```
)
```

Top

```
[
```

Expected

```
]
```

Mismatch.

Return

```
False
```

Immediately.

______________________________________________________________________

# Visual Explanation

Input

```
{ [ ] }
```

```
Stack

[]
```

↓

```
[
{
]
```

↓

```
[
{

[
]
```

↓

Pop

```
[
{
]
```

↓

Pop

```
[]
```

Done.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before processing each character, the stack contains every unmatched opening bracket in the correct order.

Whenever:

Opening bracket

↓

Push.

Whenever:

Closing bracket

↓

It must match the **latest unmatched opening bracket**.

That's exactly what the stack provides.

At the end,

the stack must be empty.

Otherwise,

some brackets were never closed.

______________________________________________________________________

# Why LIFO?

Suppose

```
( [ ] )
```

Latest opening bracket

```
[
```

must close first.

Not

```
(
```

This is

```
Last In

↓

First Out
```

Exactly Stack behavior.

______________________________________________________________________

# Edge Cases

### Empty String

```
""
```

Valid.

______________________________________________________________________

### Only Opening Brackets

```
(((
```

Invalid.

Stack isn't empty.

______________________________________________________________________

### Only Closing Brackets

```
)))
```

Invalid immediately.

______________________________________________________________________

### Nested Brackets

```
({[]})
```

Valid.

______________________________________________________________________

### Wrong Order

```
([)]
```

Invalid.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n²)
```

Space

```
O(n)
```

______________________________________________________________________

## Stack Solution

Time

```
O(n)
```

Each character is pushed and popped at most once.

Space

```
O(n)
```

Worst case

```
(((((((((
```

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_valid(text: str) -> bool:
    previous = None

    while previous != text:
        previous = text
        text = (
            text.replace("()", "")
            .replace("[]", "")
            .replace("{}", "")
        )

    return text == ""
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def is_valid(text: str) -> bool:
    stack: List[str] = []

    matching = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    for character in text:
        if character in "([{":
            stack.append(character)
        else:
            if not stack:
                return False

            top = stack.pop()

            if top != matching[character]:
                return False

    return len(stack) == 0


if __name__ == "__main__":
    print(is_valid("{[]}"))
```

______________________________________________________________________

# Even Cleaner Solution

Instead of storing opening brackets,

store the **expected closing bracket**.

Example

Read

```
(
```

Push

```
)
```

Read

```
[
```

Push

```
]
```

Now,

whenever a closing bracket appears,

simply compare it with the top.

```python
mapping = {
    "(": ")",
    "[": "]",
    "{": "}",
}
```

Many senior engineers prefer this version because it reduces one dictionary lookup.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Only counting brackets.

Counts don't preserve order.

______________________________________________________________________

## Mistake 2

Forgetting to check whether the stack is empty before popping.

Causes runtime errors.

______________________________________________________________________

## Mistake 3

Not checking whether the stack is empty at the end.

Remaining opening brackets make the string invalid.

______________________________________________________________________

## Mistake 4

Using a Queue instead of a Stack.

Queues are FIFO.

Brackets require LIFO.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A brute-force solution repeatedly removes matching bracket pairs, but that requires repeated scans. Since every closing bracket must match the most recent unmatched opening bracket, a Stack is the ideal data structure. I push opening brackets, pop when I encounter closing brackets, and ensure the pairs match. If the stack is empty at the end, the string is valid."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a Stack?**

Because brackets follow **Last-In-First-Out** ordering.

______________________________________________________________________

**Q. Why check `if not stack` before popping?**

To handle cases like:

```
")"
```

where there's no opening bracket to match.

______________________________________________________________________

**Q. Why check whether the stack is empty at the end?**

Unmatched opening brackets remain.

Example

```
"((("
```

______________________________________________________________________

**Q. Where is this used in backend engineering?**

- JSON parsing
- HTML parsing
- XML parsing
- Compiler syntax checking
- Function call management

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Stack (LIFO) |
| Recognition | Matching / Nested Structures |
| Brute Force | Repeated Replacement |
| Optimized | Stack |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Matching brackets naturally require a Stack.
- Push opening brackets.
- Pop when encountering closing brackets.
- Compare the popped bracket with the expected opening bracket.
- Check for an empty stack before popping.
- Ensure the stack is empty at the end.
- Time complexity is O(n).
- This is the foundation for many parsing problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Baseball Game
1. Backspace String Compare
1. Remove Outermost Parentheses

______________________________________________________________________

## Medium

4. Decode String
1. Evaluate Reverse Polish Notation
1. Daily Temperatures
1. Simplify Path

______________________________________________________________________

## Hard (Optional)

8. Largest Rectangle in Histogram
1. Basic Calculator
1. Remove Invalid Parentheses

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is understanding **when to use a Stack**. Whenever a problem involves **nested
structures, matching pairs, or "the most recent unfinished work"**, think **LIFO**. A Stack remembers exactly what still
needs to be completed, making it the perfect data structure for parsers, compilers, interpreters, and many interview
problems.

______________________________________________________________________

# Next

[28-min-stack.md](28-min-stack.md)
