# 24-evaluate-reverse-polish-notation.md

# Evaluate Reverse Polish Notation — Expression Evaluation Using a Stack

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐☆

**Importance:** ⭐⭐⭐⭐☆

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

You are given an array of strings representing an arithmetic expression in **Reverse Polish Notation (RPN)**.

Evaluate the expression and return the result.

Supported operators:

```text
+
-
*
/
```

Division truncates toward zero.

______________________________________________________________________

### Example 1

```text
Input

["2", "1", "+", "3", "*"]
```

Expression

```text
(2 + 1) * 3
```

Output

```text
9
```

______________________________________________________________________

### Example 2

```text
Input

["4", "13", "5", "/", "+"]
```

Expression

```text
4 + (13 / 5)
```

Output

```text
6
```

______________________________________________________________________

### Example 3

```text
Input

["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
```

Output

```text
22
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Evaluate an expression where operators come **after** their operands.

Unlike normal arithmetic:

```text
2 + 3
```

RPN writes:

```text
2 3 +
```

No parentheses are needed because the order of evaluation is implicit.

______________________________________________________________________

# Real-World Analogy

Many calculators, compilers, and interpreters internally convert expressions into postfix (RPN) before evaluation.

Examples:

- Expression parsers
- SQL execution engines
- Compiler syntax trees
- Virtual machines
- Calculator applications

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Expression evaluation
- Postfix notation
- Reverse Polish Notation
- Operators after operands

Think immediately:

```text
Stack
```

______________________________________________________________________

# Why a Stack?

Consider

```text
2 3 +
```

Read

```text
2
```

Store it.

Read

```text
3
```

Store it.

Read

```text
+
```

Use the **last two numbers**.

Exactly LIFO.

______________________________________________________________________

# Visual Explanation

Expression

```text
2 1 + 3 *
```

Read

```text
2
```

Stack

```
2
```

______________________________________________________________________

Read

```text
1
```

Stack

```
1
2
```

______________________________________________________________________

Read

```text
+
```

Pop

```
1

2
```

Compute

```text
2 + 1 = 3
```

Push

```
3
```

______________________________________________________________________

Read

```text
3
```

Stack

```
3
3
```

______________________________________________________________________

Read

```text
*
```

Pop

```
3

3
```

Compute

```text
3 × 3 = 9
```

Push

```
9
```

Finished.

Answer

```text
9
```

______________________________________________________________________

# Step-by-Step Algorithm

For every token:

If it is a number:

Push it.

Otherwise:

Pop two operands.

Perform operation.

Push result.

Final stack element is the answer.

______________________________________________________________________

# Operand Order Matters

Suppose

```text
4 2 -
```

Pop

```text
2

4
```

Correct calculation

```text
4 - 2
```

Not

```text
2 - 4
```

Remember:

```python
right = stack.pop()

left = stack.pop()
```

Then

```python
left operator right
```

______________________________________________________________________

# Dry Run

Input

```text
["4","13","5","/","+"]
```

Stack

```
4
```

______________________________________________________________________

Push

```
13
```

______________________________________________________________________

Push

```
5
```

______________________________________________________________________

Read

```text
/
```

Pop

```text
5

13
```

Result

```text
2
```

Push

```
2

4
```

______________________________________________________________________

Read

```text
+
```

Result

```text
6
```

Done.

______________________________________________________________________

# Why This Works

Whenever an operator appears,

its operands have already been processed.

The stack naturally stores intermediate results.

This guarantees correct evaluation order.

______________________________________________________________________

# Edge Cases

## Single Number

```text
["7"]
```

Answer

```text
7
```

______________________________________________________________________

## Negative Numbers

```text
["4","-2","/"]
```

Valid.

______________________________________________________________________

## Large Expressions

Still

```text
O(n)
```

______________________________________________________________________

# Complexity Analysis

## Time

Each token:

- pushed once
- popped once

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Worst case

All operands before operators.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluates a Reverse Polish Notation expression.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    stack: List[int] = []

    for token in tokens:
        if token not in {"+", "-", "*", "/"}:
            stack.append(int(token))
            continue

        right = stack.pop()
        left = stack.pop()

        if token == "+":
            stack.append(left + right)

        elif token == "-":
            stack.append(left - right)

        elif token == "*":
            stack.append(left * right)

        else:
            stack.append(int(left / right))

    return stack[-1]
```

______________________________________________________________________

# Why Use `int(left / right)`?

Python's floor division (`//`) rounds toward negative infinity.

Example

```python
-3 // 2
```

Result

```text
-2
```

But the problem requires truncation toward zero.

```python
int(-3 / 2)
```

Result

```text
-1
```

This matches the interview requirement.

______________________________________________________________________

# Common Mistakes

## 1. Reversing Operand Order

Wrong

```python
a = stack.pop()
b = stack.pop()

a - b
```

Correct

```python
right = stack.pop()
left = stack.pop()

left - right
```

______________________________________________________________________

## 2. Using `//` for Division

Use

```python
int(left / right)
```

______________________________________________________________________

## 3. Forgetting Negative Numbers

Tokens can be:

```text
-11
```

Treat them as operands, not operators.

______________________________________________________________________

## 4. Popping Too Early

Always ensure two operands exist before applying an operator.

______________________________________________________________________

# Variations

## Medium

- Basic Calculator II
- Decode String
- Simplify Path

______________________________________________________________________

## Hard

- Basic Calculator
- Parse Lisp Expression

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize postfix notation.
1. Think Stack.
1. Push operands.
1. Pop two operands for operators.
1. Preserve operand order.
1. Return the final stack element.

______________________________________________________________________

### Common Follow-ups

### Q: Why Stack?

The most recent operands are always used first.

LIFO fits naturally.

______________________________________________________________________

### Q: Why not recursion?

Stack is simpler, iterative, and directly models postfix evaluation.

______________________________________________________________________

### Q: Why is the algorithm O(n)?

Every token is processed exactly once.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Expression Evaluation Stack |
| Recognition | Reverse Polish Notation, postfix |
| Store | Operands and intermediate results |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Baseball Game
1. Valid Parentheses

## Medium

1. Basic Calculator II
1. Decode String
1. Simplify Path
1. Remove All Adjacent Duplicates in String II

## Hard

1. Basic Calculator
1. Parse Lisp Expression

______________________________________________________________________

# Quick Revision

- Push operands.
- Pop two operands for every operator.
- Preserve operand order.
- Push intermediate results back.
- Final stack element is the answer.
- Use `int(left / right)` for truncation toward zero.
- Time: **O(n)**
- Space: **O(n)**

______________________________________________________________________

# Key Takeaway

This problem demonstrates another important Stack use case:

> **Stacks are excellent for evaluating expressions because they naturally preserve intermediate results.**

Unlike the previous Stack problems:

- **Valid Parentheses** stored **unfinished brackets**.
- **Daily Temperatures** stored **unfinished indices**.
- **Reverse Polish Notation** stores **unfinished calculations**.

The underlying idea is the same:

> **The stack always contains work that hasn't been fully resolved yet.**

______________________________________________________________________

# Navigation

**Previous**

[23-daily-temperatures.md](23-daily-temperatures.md)

**Next**

[25-largest-rectangle-in-histogram.md](25-largest-rectangle-in-histogram.md)
