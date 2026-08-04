# 22-valid-parentheses.md

# Valid Parentheses — The Matching Pair Stack Pattern

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given a string containing only:

```text
(
)

{

}

[

]
```

Determine whether the string is valid.

A string is valid if:

- Every opening bracket has a matching closing bracket.
- Brackets close in the correct order.
- Every closing bracket matches the most recent unmatched opening bracket.

______________________________________________________________________

### Example 1

```text
Input

()

Output

True
```

______________________________________________________________________

### Example 2

```text
Input

()[]{}

Output

True
```

______________________________________________________________________

### Example 3

```text
Input

(]

Output

False
```

______________________________________________________________________

### Example 4

```text
Input

([)]

Output

False
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Can every opening bracket find its correct closing bracket?

Not only that—

It must match in the **correct order**.

______________________________________________________________________

# Real-World Analogy

Think about nested function calls.

```text
main()

↓

login()

↓

database()
```

The last function entered

must finish first.

Similarly,

```text
(
[
{
```

must close as

```text
}
]
)
```

This is exactly **LIFO** behavior.

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Parentheses
- Nested
- Balanced
- Matching symbols
- Correct order

Think:

```text
Stack
```

Immediately.

______________________________________________________________________

# Brute Force Solution

Try repeatedly removing:

```text
()

[]

{}
```

until nothing remains.

Example

```text
([])

↓

()

↓

Empty
```

Works,

but repeatedly scanning the string is inefficient.

______________________________________________________________________

## Complexity

Worst case

```text
O(n²)
```

______________________________________________________________________

# Optimal Solution

## Key Insight

Whenever you see an opening bracket,

remember it.

Whenever you see a closing bracket,

it must match the **most recent opening bracket**.

That's exactly what a Stack does.

______________________________________________________________________

# Visual Explanation

Input

```text
({[]})
```

Read

```text
(
```

Stack

```text
(
```

______________________________________________________________________

Read

```text
{
```

Stack

```text
{

(
```

______________________________________________________________________

Read

```text
[
```

Stack

```text
[

{

(
```

______________________________________________________________________

Read

```text
]
```

Pop

```text
[
```

Matches.

______________________________________________________________________

Read

```text
}
```

Pop

```text
{
```

Matches.

______________________________________________________________________

Read

```text
)
```

Pop

```text
(
```

Matches.

Stack becomes empty.

Valid.

______________________________________________________________________

# Invalid Example

```text
([)]
```

Process

```text
(

↓

[
```

Stack

```text
[

(
```

Next

```text
)
```

Top

```text
[
```

Mismatch.

Return

```text
False
```

______________________________________________________________________

# Step-by-Step Algorithm

Create empty stack.

For every character:

If opening bracket

Push.

Else

If stack is empty

Return False.

Pop.

Check if it matches.

At the end,

Stack must be empty.

______________________________________________________________________

# Why This Works

The stack always stores

the unmatched opening brackets.

The top of the stack represents

the only bracket that can legally close next.

If another closing bracket appears,

the string is invalid.

______________________________________________________________________

# Dry Run

Input

```text
()[]{}
```

Read

```text
(
```

Push.

______________________________________________________________________

Read

```text
)
```

Pop.

______________________________________________________________________

Read

```text
[
```

Push.

______________________________________________________________________

Read

```text
]
```

Pop.

______________________________________________________________________

Read

```text
{
```

Push.

______________________________________________________________________

Read

```text
}
```

Pop.

Stack empty.

Return

```text
True
```

______________________________________________________________________

# Edge Cases

## Empty String

```text
""
```

Valid.

______________________________________________________________________

## Only Opening Brackets

```text
(((
```

Invalid.

Stack not empty.

______________________________________________________________________

## Only Closing Brackets

```text
)))
```

Invalid.

Stack empty before pop.

______________________________________________________________________

## Wrong Order

```text
([)]
```

Invalid.

______________________________________________________________________

# Complexity Analysis

## Time

Each character is:

- pushed once
- popped once

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Worst case

```text
(((((((
```

Stack stores every character.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def is_valid(s: str) -> bool:
    """
    Returns True if parentheses are balanced.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    stack: List[str] = []

    matching = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    for char in s:
        if char in "([{":
            stack.append(char)

        else:
            if not stack:
                return False

            top = stack.pop()

            if top != matching[char]:
                return False

    return len(stack) == 0
```

______________________________________________________________________

# Alternative Implementation

Instead of storing opening brackets,

store the expected closing bracket.

```python
def is_valid(s: str) -> bool:
    stack = []

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    for char in s:
        if char in pairs:
            stack.append(pairs[char])

        else:
            if not stack or stack.pop() != char:
                return False

    return not stack
```

Many experienced engineers prefer this version because the comparison becomes simpler.

______________________________________________________________________

# Common Mistakes

## 1. Forgetting Empty Stack Check

Wrong

```python
stack.pop()
```

Always verify the stack is not empty first.

______________________________________________________________________

## 2. Ignoring Order

Example

```text
([)]
```

Counts are correct.

Order isn't.

Still invalid.

______________________________________________________________________

## 3. Checking Only Counts

```text
(()))
```

Equal counts do not guarantee validity.

Order matters.

______________________________________________________________________

## 4. Forgetting Remaining Opening Brackets

At the end,

the stack must be empty.

______________________________________________________________________

# Variations

## Easy

- Baseball Game

______________________________________________________________________

## Medium

- Decode String
- Remove All Adjacent Duplicates
- Simplify Path
- Asteroid Collision

______________________________________________________________________

## Hard

- Basic Calculator
- Parse Lisp Expression

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize nested matching.
1. Think LIFO.
1. Use a Stack.
1. Push opening brackets.
1. Match closing brackets.
1. Verify stack is empty.

______________________________________________________________________

### Common Follow-ups

### Q: Why Stack?

The most recent opening bracket must close first.

That's exactly LIFO.

______________________________________________________________________

### Q: Why not count brackets?

Counts ignore ordering.

Example

```text
([)]
```

Counts match.

Structure doesn't.

______________________________________________________________________

### Q: Can recursion solve this?

Yes.

But it uses the call stack and is less practical here.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Matching Pair Stack |
| Recognition | Parentheses, nested, balanced |
| Push | Opening brackets |
| Pop | Closing brackets |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Baseball Game
1. Remove All Adjacent Duplicates in String

## Medium

1. Decode String
1. Simplify Path
1. Asteroid Collision
1. Evaluate Reverse Polish Notation

## Hard

1. Basic Calculator
1. Parse Lisp Expression

______________________________________________________________________

# Quick Revision

- Stack stores unmatched opening brackets.
- Push opening brackets.
- Pop on closing brackets.
- Top must match the closing bracket.
- Empty stack at the end means success.
- Time: **O(n)**
- Space: **O(n)**

______________________________________________________________________

# Key Takeaway

This is the **foundation of Stack interview questions**.

The invariant is:

> **The stack always contains unmatched opening brackets in the exact order they must be closed.**

Whenever you see nested or balanced structures, ask yourself:

> **"Does the most recent opening item have to close first?"**

If the answer is **yes**, a Stack is usually the right tool.

______________________________________________________________________

# Navigation

**Previous**

[21-stack.md](21-stack.md)

**Next**

[23-daily-temperatures.md](23-daily-temperatures.md)
