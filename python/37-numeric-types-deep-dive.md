# File: python/37-numeric-types-deep-dive.md

# Python Built-in Types

# Numeric Types Deep Dive (`int`, `float`, `bool`, `Decimal`, `Fraction`, `complex`)

> **Course:** Backend Engineering Roadmap
>
> **Module:** Built-in Types
>
> **Lesson:** 37
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 5 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `int` | Python 1.0 |
| `float` | Python 1.0 |
| `bool` | Python 2.3 |
| `complex` | Python 1.0 |
| `decimal` module | Python 2.4 |
| `fractions` module | Python 2.6 |

### Important Python Version Changes

- Python 2 had separate `int` and `long` types.
- Python 3 unified them into a single arbitrary-precision `int`.
- Floating-point numbers still follow the IEEE 754 double-precision standard.
- `Decimal` and `Fraction` remain specialised numeric types for high-precision calculations.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Python's numeric hierarchy
- Integer internals
- Arbitrary-precision integers
- Floating-point representation
- IEEE 754
- Floating-point precision errors
- `Decimal`
- `Fraction`
- `complex`
- `bool`
- Numeric performance
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we covered:

- Sets
- FrozenSets
- Hash tables
- Membership testing
- Set operations

Now we'll explore Python's numeric types and understand why choosing the correct numeric type matters in production
systems.

______________________________________________________________________

# Why Should Backend Engineers Care?

Numbers are everywhere.

Examples:

- Payment processing
- Tax calculations
- Currency conversion
- Analytics
- Database IDs
- JWT expiration timestamps
- Pagination
- Inventory systems
- Scientific calculations
- Monitoring metrics

Choosing the wrong numeric type can introduce subtle production bugs.

______________________________________________________________________

# Python's Numeric Hierarchy

```
                 Number

                    │

      ┌─────────────┴─────────────┐

     Complex

        │

      Float

        │

      Integer

        │

       Bool
```

Interestingly,

`bool` is actually a subclass of `int`.

We'll see why shortly.

______________________________________________________________________

# Integer (`int`)

Integers represent whole numbers.

```python
count = 42

temperature = -10

population = 8000000
```

Unlike many languages,

Python integers have **no fixed size**.

______________________________________________________________________

# Python 2 vs Python 3

Python 2

```
int

↓

32-bit / 64-bit

long

↓

Unlimited size
```

Python 3

```
int

↓

Unlimited size
```

This simplifies programming considerably.

______________________________________________________________________

# Arbitrary Precision Integers

Consider

```python
number = 10 ** 100

print(number)
```

Output

```text
10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```

Python handles this automatically.

Many languages would overflow.

______________________________________________________________________

# How Does Python Store Large Integers?

Internally,

small integers fit into a small amount of memory.

Large integers require additional memory.

Conceptually:

```
123

↓

One memory block
```

Large value

```
123456789012345678901234567890...

↓

Multiple internal blocks
```

As numbers grow,

memory usage and computation time also grow.

______________________________________________________________________

# Integer Operations

```python
a = 20

b = 6

print(a + b)

print(a - b)

print(a * b)

print(a // b)

print(a % b)

print(a ** b)
```

Output

```text
26
14
120
3
2
64000000
```

______________________________________________________________________

# Integer Division

Python has two division operators.

True division

```python
print(5 / 2)
```

Output

```text
2.5
```

Floor division

```python
print(5 // 2)
```

Output

```text
2
```

______________________________________________________________________

# Negative Floor Division

Many beginners expect

```python
-5 // 2
```

to produce

```text
-2
```

Actually,

```python
print(-5 // 2)
```

Output

```text
-3
```

Why?

Floor division rounds **towards negative infinity**.

```
-2.5

↓

Floor

↓

-3
```

______________________________________________________________________

# Float (`float`)

Floating-point numbers represent real numbers.

```python
price = 19.99

pi = 3.14159
```

Python uses the IEEE 754 double-precision standard.

______________________________________________________________________

# IEEE 754

A floating-point number is stored using three components.

```
+----------+-----------+----------------------+

| Sign | Exponent | Fraction (Mantissa) |

+----------+-----------+----------------------+
```

You don't need to memorise the bit layout,

but you should understand that floating-point numbers are approximations.

______________________________________________________________________

# The Famous Example

```python
print(0.1 + 0.2)
```

Output

```text
0.30000000000000004
```

Many new Python developers think this is a bug.

It isn't.

______________________________________________________________________

# Why Does This Happen?

Most decimal fractions cannot be represented exactly in binary.

Just like

```
1 / 3

↓

0.333333333...
```

cannot be represented exactly in decimal,

numbers like `0.1` cannot be represented exactly in binary.

Python stores the nearest representable value.

______________________________________________________________________

# Visualising

```
0.1

↓

Binary Approximation

↓

Stored Float

↓

Small Rounding Error
```

The error is tiny,

but repeated calculations can accumulate it.

______________________________________________________________________

# Never Compare Floats Directly

Wrong

```python
if 0.1 + 0.2 == 0.3:
    print("Equal")
```

Correct

```python
import math

print(math.isclose(0.1 + 0.2, 0.3))
```

Output

```text
True
```

______________________________________________________________________

# Why is `math.isclose()` Better?

Floating-point calculations often differ by extremely small amounts.

`math.isclose()` compares numbers within a configurable tolerance rather than requiring exact equality.

______________________________________________________________________

# Decimal

Financial software should rarely use `float`.

Suppose

```python
price = 0.10

tax = 0.20
```

Small floating-point errors may accumulate over thousands of transactions.

Instead,

use `Decimal`.

______________________________________________________________________

# Using Decimal

```python
from decimal import Decimal

price = Decimal("0.10")

tax = Decimal("0.20")

print(price + tax)
```

Output

```text
0.30
```

Notice

The values are created from **strings**.

______________________________________________________________________

# Why Strings?

Wrong

```python
Decimal(0.1)
```

This converts the already inaccurate float into a Decimal.

Correct

```python
Decimal("0.1")
```

This preserves the exact decimal value.

______________________________________________________________________

# Production Example

```python
from decimal import Decimal

subtotal = Decimal("99.95")

tax = Decimal("17.99")

total = subtotal + tax

print(total)
```

Output

```text
117.94
```

Financial systems should prefer `Decimal`.

______________________________________________________________________

# Fraction

Sometimes exact fractions matter.

```python
from fractions import Fraction

value = Fraction(1, 3)

print(value)
```

Output

```text
1/3
```

Arithmetic remains exact.

```python
from fractions import Fraction

print(Fraction(1, 3) + Fraction(1, 6))
```

Output

```text
1/2
```

______________________________________________________________________

# Complex Numbers

Python also supports complex numbers.

```python
z = 3 + 4j

print(z.real)

print(z.imag)
```

Output

```text
3.0

4.0
```

Complex numbers are mainly used in:

- Scientific computing
- Signal processing
- Engineering
- Mathematics

Rarely used in backend applications.

______________________________________________________________________

# Bool

One surprising fact:

```python
print(isinstance(True, int))
```

Output

```text
True
```

Why?

Because

```
False = 0

True = 1
```

Example

```python
print(True + True)
```

Output

```text
2
```

This behaviour exists largely for historical compatibility and makes boolean arithmetic possible.

______________________________________________________________________

# Numeric Conversions

```python
print(int("42"))

print(float("3.14"))

print(bool(1))

print(bool(0))
```

Output

```text
42

3.14

True

False
```

______________________________________________________________________

# Truthiness

Python determines truthiness automatically.

Falsy values include:

```python
0

0.0

False

None

""

[]

{}

set()
```

Everything else is truthy unless the object defines otherwise.

______________________________________________________________________

# Numeric Performance

Approximate performance (fastest to slowest):

```
bool

↓

int

↓

float

↓

Decimal

↓

Fraction
```

`Decimal` and `Fraction` trade performance for correctness.

Choose them only when precision matters.

______________________________________________________________________

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Integer Addition | O(1)\* |
| Integer Multiplication | O(1)\* |
| Float Addition | O(1) |
| Decimal Addition | O(n) |
| Fraction Addition | O(n) |

\*For typical machine-sized integers. Very large integers require more work as the number of digits increases.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `float` for money.

```python
balance = 19.99
```

Prefer

```python
from decimal import Decimal

balance = Decimal("19.99")
```

______________________________________________________________________

## Mistake 2

Comparing floats directly.

Wrong

```python
a == b
```

Better

```python
math.isclose(a, b)
```

______________________________________________________________________

## Mistake 3

Creating `Decimal` objects from floats.

Wrong

```python
Decimal(0.1)
```

Correct

```python
Decimal("0.1")
```

______________________________________________________________________

## Mistake 4

Assuming Python integers overflow.

Python integers automatically grow to accommodate larger values, limited only by available memory.

______________________________________________________________________

# Best Practices

✅ Use `int` for counters, IDs and indexes.

✅ Use `float` for scientific or approximate calculations.

✅ Use `Decimal` for financial applications.

✅ Use `Fraction` when exact rational arithmetic is required.

✅ Use `math.isclose()` for float comparisons.

❌ Don't use `float` for currency calculations.

❌ Don't create `Decimal` objects from floats.

❌ Don't assume all numeric types have identical performance.

______________________________________________________________________

# Production Insight

Backend systems use different numeric types for different jobs.

Database IDs

```python
user_id = 1250
```

Currency

```python
from decimal import Decimal

price = Decimal("149.99")
```

JWT expiration

```python
expires_at = 1735603200
```

Analytics

```python
average_response_time = 12.43
```

Scientific API

```python
measurement = 0.00000452
```

Senior engineers choose the numeric type based on correctness first and performance second.

______________________________________________________________________

# Questions

### Question

> Why shouldn't `float` be used for financial calculations?

### Answer

Floats use binary floating-point representation, which cannot exactly represent many decimal values. Small rounding
errors accumulate over time, making `Decimal` a safer choice for financial data.

______________________________________________________________________

### Question

> Why does `0.1 + 0.2` not equal `0.3` exactly?

### Answer

Because `0.1` and `0.2` cannot be represented exactly in binary. Python stores the closest representable values, leading
to tiny rounding errors.

______________________________________________________________________

### Question

> Why can Python integers become arbitrarily large?

### Answer

Python 3 integers use arbitrary-precision arithmetic, allocating additional memory as needed instead of overflowing
fixed-size integer types.

______________________________________________________________________

### Question

> Why is `bool` a subclass of `int`?

### Answer

Python represents `False` as `0` and `True` as `1`, allowing booleans to participate naturally in arithmetic while
maintaining backwards compatibility.

______________________________________________________________________

### Question

> When would you use `Fraction` instead of `Decimal`?

### Answer

Use `Fraction` when exact rational arithmetic is required, such as symbolic mathematics or algorithms that depend on
exact fractional values rather than decimal approximations.

______________________________________________________________________

# Practical Lesson

Create:

```text
numeric_examples.py
```

```python
from decimal import Decimal
from fractions import Fraction
import math

# Integer
print(10 ** 20)

# Float precision
print(0.1 + 0.2)

print(math.isclose(0.1 + 0.2, 0.3))

# Decimal
price = Decimal("99.95")
tax = Decimal("18.00")

print(price + tax)

# Fraction
print(Fraction(1, 3) + Fraction(1, 6))

# Boolean arithmetic
print(True + True)
```

Expected Output

```text
100000000000000000000

0.30000000000000004

True

117.95

1/2

2
```

______________________________________________________________________

# Questions

## Question 1

Why should financial software use `Decimal` instead of `float`?

### Answer

`Decimal` represents decimal values exactly, avoiding the binary floating-point rounding errors that occur with `float`.

______________________________________________________________________

## Question 2

Why are Python integers called arbitrary-precision integers?

### Answer

Because they automatically expand to accommodate larger values instead of overflowing fixed-size integer storage.

______________________________________________________________________

## Question 3

Why should floats rarely be compared using `==`?

### Answer

Floating-point values often differ by tiny rounding errors. `math.isclose()` is usually a safer comparison.

______________________________________________________________________

## Question 4

What is the relationship between `bool` and `int`?

### Answer

`bool` is a subclass of `int`, where `False` behaves as `0` and `True` behaves as `1`.

______________________________________________________________________

## Question 5

When should you use `Fraction`?

### Answer

When calculations require exact rational values rather than approximate decimal representations.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a shopping cart that calculates:

- Subtotal
- Tax
- Discount
- Grand Total

using `Decimal`.

Compare the result with an implementation using `float`.

______________________________________________________________________

## Exercise 2

Write a function that compares two floating-point values safely using `math.isclose()`.

Allow callers to customise the relative and absolute tolerance.

______________________________________________________________________

## Exercise 3

Create a statistics module that computes:

- Mean
- Median
- Percentage
- Growth rate

using appropriate numeric types.

Explain why you chose each type.

______________________________________________________________________

## Exercise 4

Research IEEE 754 and explain:

- Why floating-point numbers cannot exactly represent many decimal fractions.
- What the mantissa and exponent represent.
- Why floating-point arithmetic is still the standard choice for scientific computing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Python's numeric type hierarchy.
- ✅ Arbitrary-precision integers.
- ✅ IEEE 754 floating-point representation.
- ✅ Why floating-point errors occur.
- ✅ When to use `Decimal`.
- ✅ When to use `Fraction`.
- ✅ Boolean arithmetic.
- ✅ Numeric performance trade-offs.
- ✅ Production best practices.
- ✅ Senior backend interview topics.

______________________________________________________________________

# What's Next

**File:** [38-Collections-Module-part-1](38-collections-module-part-1.md)

Topics:

- Why the `collections` module exists
- `deque`
- `Counter`
- `defaultdict`
- Internal implementations
- Performance comparisons
- Production use cases
- Best practices

> **Note:** The `collections` module is broad and foundational. We'll cover it in **two parts**, starting with the three data structures that every backend engineer should know: `deque`, `Counter`, and `defaultdict`.
