# File: python/23-map-filter-reduce.md

# Python Functional Programming - Part 1

# Functional Programming Fundamentals, `map()`, `filter()` and `reduce()`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Functional Python
>
> **Lesson:** 1
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 120 Minutes

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| Functional programming concepts | Python 1.0 |
| `map()` | Python 1.0 |
| `filter()` | Python 1.0 |
| `lambda` | Python 1.0 |
| `reduce()` (built-in) | Python 1.0 |
| `functools.reduce()` | Python 2.6 |
| `reduce()` removed from built-ins | Python 3.0 |

### Important Python 3 Change

In Python 2:

```python
map()
```

and

```python
filter()
```

returned **lists**.

In Python 3, they return **iterators (lazy objects)**.

This change significantly reduced memory usage when processing large datasets.

Since almost all production systems today use Python 3, this course focuses exclusively on Python 3 behaviour.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What functional programming is
- Why Python supports functional programming
- Pure functions
- Side effects
- Immutability
- `map()`
- `filter()`
- `reduce()`
- `lambda` with functional tools
- Lazy evaluation
- Performance considerations
- Production use cases

______________________________________________________________________

# Recap

So far we've learned Object-Oriented Programming.

```
Objects

↓

Methods

↓

State

↓

Inheritance
```

Python is **multi-paradigm**.

Besides OOP, it also supports:

- Functional Programming
- Procedural Programming
- Imperative Programming

A good Python developer knows when each style is appropriate.

______________________________________________________________________

# What is Functional Programming?

Functional Programming (FP) is a programming style where computation is performed by applying functions to data.

Instead of focusing on **objects**,

FP focuses on **transforming data**.

Example

Instead of

```python
employee.salary += 500
```

we prefer

```python
new_salary = increase_salary(employee.salary)
```

The original value is left unchanged.

______________________________________________________________________

# Core Ideas of Functional Programming

Functional programming encourages:

- Pure functions
- Immutability
- No hidden state
- Function composition
- Higher-order functions

Python doesn't enforce these rules,

but encourages them.

______________________________________________________________________

# What is a Pure Function?

A pure function has two properties.

1. Same input → same output.

1. No side effects.

Example

```python
def square(number):

    return number * number
```

Usage

```python
print(square(5))
```

Output

```
25
```

Every call with `5` always returns `25`.

______________________________________________________________________

# Impure Function

```python
counter = 0


def increment():

    global counter

    counter += 1

    return counter
```

Output

```
1

2

3
```

The same function call produces different results because it depends on external state.

______________________________________________________________________

# Why Pure Functions Matter

Pure functions are:

- Easy to test
- Easy to understand
- Thread-safe
- Predictable
- Easier to cache
- Easier to parallelise

Large backend systems often favour pure business logic whenever possible.

______________________________________________________________________

# Side Effects

A side effect is anything that changes the outside world.

Examples

- Writing to a database
- Printing
- Sending an email
- Writing a log file
- Making an API request
- Updating a global variable

Example

```python
def save_user(user):

    database.save(user)
```

This function has side effects.

______________________________________________________________________

# Immutability

Functional programming prefers immutable data.

Mutable

```python
numbers = [1, 2, 3]

numbers.append(4)
```

The original object changes.

Immutable

```python
numbers = (1, 2, 3)

new_numbers = numbers + (4,)
```

The original tuple remains unchanged.

______________________________________________________________________

# Why Immutability?

Immutable objects:

- Are safer in concurrent programs
- Prevent accidental modification
- Simplify debugging
- Reduce shared-state bugs

Python provides several immutable types:

- `tuple`
- `str`
- `frozenset`
- `int`
- `float`
- `bool`

______________________________________________________________________

# Higher-Order Functions

We covered higher-order functions earlier in the course.

Reminder:

A higher-order function either:

- Accepts another function
- Returns another function

Examples include:

- `map()`
- `filter()`
- `sorted()`
- `reduce()`

______________________________________________________________________

# Introducing map()

`map()` applies a function to every item in an iterable.

Syntax

```python
map(function, iterable)
```

Example

```python
numbers = [1, 2, 3, 4]

result = map(
    lambda x: x * 2,
    numbers
)

print(result)
```

Output

```
<map object ...>
```

Notice

No list is returned.

______________________________________________________________________

# Why?

Python 3 returns an iterator.

Convert it if necessary.

```python
print(list(result))
```

Output

```
[2, 4, 6, 8]
```

______________________________________________________________________

# Visualising map()

```
Input

1

2

3

4

↓

Function

x * 2

↓

Output

2

4

6

8
```

______________________________________________________________________

# Using a Normal Function

```python
def square(number):

    return number ** 2


numbers = [1, 2, 3]

result = map(
    square,
    numbers
)

print(list(result))
```

Output

```
[1, 4, 9]
```

______________________________________________________________________

# map() with Multiple Iterables

```python
numbers1 = [1, 2, 3]

numbers2 = [10, 20, 30]


result = map(

    lambda x, y: x + y,

    numbers1,

    numbers2

)

print(list(result))
```

Output

```
[11, 22, 33]
```

Python stops when the shortest iterable ends.

______________________________________________________________________

# Introducing filter()

`filter()` selects items that satisfy a condition.

Syntax

```python
filter(function, iterable)
```

Example

```python
numbers = [1, 2, 3, 4, 5, 6]

result = filter(

    lambda x: x % 2 == 0,

    numbers

)

print(list(result))
```

Output

```
[2, 4, 6]
```

______________________________________________________________________

# Visualising filter()

```
Input

1

2

3

4

5

6

↓

Condition

Even?

↓

Output

2

4

6
```

______________________________________________________________________

# filter(None, iterable)

This is an interview favourite.

```python
values = [

    0,

    "",

    None,

    False,

    10,

    "Hello"

]

print(list(filter(None, values)))
```

Output

```
[10, 'Hello']
```

`None` tells `filter()` to remove values that evaluate to `False`.

______________________________________________________________________

# Introducing reduce()

Unlike `map()` and `filter()`,

`reduce()` produces a **single value**.

Import

```python
from functools import reduce
```

Syntax

```python
reduce(function, iterable)
```

______________________________________________________________________

# Example

```python
from functools import reduce

numbers = [1, 2, 3, 4]


result = reduce(

    lambda x, y: x + y,

    numbers

)

print(result)
```

Output

```
10
```

______________________________________________________________________

# How reduce() Works

```
1 + 2 = 3

↓

3 + 3 = 6

↓

6 + 4 = 10
```

The accumulated value is passed into the next call.

______________________________________________________________________

# reduce() with an Initial Value

```python
from functools import reduce

numbers = [1, 2, 3]


result = reduce(

    lambda x, y: x + y,

    numbers,

    100

)

print(result)
```

Output

```
106
```

Steps

```
100 + 1 = 101

↓

101 + 2 = 103

↓

103 + 3 = 106
```

______________________________________________________________________

# map() vs filter() vs reduce()

| Function | Purpose | Output |
|-----------|---------|--------|
| `map()` | Transform every item | Iterator |
| `filter()` | Select matching items | Iterator |
| `reduce()` | Combine everything | Single value |

______________________________________________________________________

# Chaining Functional Operations

Suppose we need to:

- Double numbers
- Keep numbers greater than 5
- Sum everything

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]


doubled = map(

    lambda x: x * 2,

    numbers

)

filtered = filter(

    lambda x: x > 5,

    doubled

)

result = reduce(

    lambda x, y: x + y,

    filtered

)

print(result)
```

Output

```
24
```

Pipeline

```
Input

↓

map()

↓

filter()

↓

reduce()

↓

Result
```

______________________________________________________________________

# Lazy Evaluation

One of the biggest advantages of `map()` and `filter()` is laziness.

Nothing happens until values are requested.

```python
def square(number):

    print(number)

    return number ** 2


numbers = [1, 2, 3]

result = map(

    square,

    numbers

)

print("Created")
```

Output

```
Created
```

No numbers are processed yet.

Only when

```python
list(result)
```

is executed does processing begin.

This makes these functions memory-efficient for large datasets.

______________________________________________________________________

# Functional Programming vs Loops

Traditional

```python
result = []

for number in numbers:

    result.append(number * 2)
```

Functional

```python
result = map(

    lambda x: x * 2,

    numbers
)
```

Both are valid.

Python values readability over strict functional style.

______________________________________________________________________

# Should You Always Use map()?

Not necessarily.

Many Python developers prefer list comprehensions.

Example

Instead of

```python
list(

    map(

        lambda x: x * 2,

        numbers

    )

)
```

they write

```python
[x * 2 for x in numbers]
```

The comprehension is often considered easier to read.

We'll compare these approaches in the next lesson.

______________________________________________________________________

# Production Example - API Data Transformation

Imagine an API returns

```python
users = [

    {

        "name": "Alice"

    },

    {

        "name": "Bob"

    }

]
```

Extract names.

```python
names = map(

    lambda user: user["name"],

    users

)
```

______________________________________________________________________

# Production Example - Validation

Filter active users.

```python
active_users = filter(

    lambda user: user.active,

    users

)
```

______________________________________________________________________

# Production Example - Calculating Totals

Suppose we have shopping basket values.

```python
prices = [

    10,

    20,

    15

]
```

Calculate the total.

```python
from functools import reduce

total = reduce(

    lambda x, y: x + y,

    prices
)
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting that `map()` returns an iterator.

```python
print(map(...))
```

prints

```
<map object ...>
```

______________________________________________________________________

## Mistake 2

Using `reduce()` for simple sums.

Instead of

```python
reduce(...)
```

prefer

```python
sum(numbers)
```

It is simpler and faster.

______________________________________________________________________

## Mistake 3

Overusing `lambda`.

Sometimes

```python
def square():

    ...
```

is much easier to understand.

______________________________________________________________________

# Best Practices

✅ Prefer pure functions.

✅ Keep transformations simple.

✅ Use `sum()`, `max()`, `min()` when appropriate instead of `reduce()`.

✅ Use meaningful function names.

✅ Take advantage of lazy evaluation for large datasets.

❌ Don't sacrifice readability for clever functional code.

❌ Don't chain many nested lambdas.

______________________________________________________________________

# Production Insight

Modern Python codebases use functional programming selectively.

You'll commonly see:

- `map()` for straightforward transformations.
- `filter()` for pipelines.
- `reduce()` less frequently, often replaced by built-in functions such as `sum()`.
- Generator expressions and comprehensions even more frequently because they are concise and highly readable.

Libraries such as Pandas, FastAPI, Airflow and ETL frameworks often build data-processing pipelines using functional
concepts, even if they don't explicitly use `map()` or `reduce()`.

______________________________________________________________________

# Questions

### Question

> What is a pure function?

### Answer

A pure function always produces the same output for the same input and has no observable side effects.

______________________________________________________________________

### Question

> Why does `map()` return an iterator in Python 3?

### Answer

Returning an iterator enables lazy evaluation, reducing memory usage by processing items only when needed.

______________________________________________________________________

### Question

> What is the difference between `map()`, `filter()` and `reduce()`?

### Answer

`map()` transforms each element, `filter()` selects elements that satisfy a condition, and `reduce()` combines all
elements into a single value.

______________________________________________________________________

### Question

> Why is `reduce()` less common in modern Python?

### Answer

Many common reductions are better expressed using specialised built-in functions like `sum()`, `max()`, `min()` or
`any()`, which are clearer and often more efficient.

______________________________________________________________________

# Practical Lesson

Create a file:

```
functional_programming_part_1.py
```

```python
from functools import reduce


numbers = [1, 2, 3, 4, 5]


# Double each number.
doubled = map(

    lambda x: x * 2,

    numbers

)

print(list(doubled))


# Keep even numbers.
evens = filter(

    lambda x: x % 2 == 0,

    numbers

)

print(list(evens))


# Calculate the total.
total = reduce(

    lambda x, y: x + y,

    numbers

)

print(total)
```

Expected Output

```
[2, 4, 6, 8, 10]

[2, 4]

15
```

______________________________________________________________________

# Questions

## Question 1

What is a pure function?

### Answer

A pure function always returns the same output for the same input and does not produce side effects.

______________________________________________________________________

## Question 2

Why does `map()` return an iterator in Python 3?

### Answer

To enable lazy evaluation, reducing memory usage and allowing efficient processing of large datasets.

______________________________________________________________________

## Question 3

What does `filter()` do?

### Answer

It returns an iterator containing only the elements for which the filtering function evaluates to `True`.

______________________________________________________________________

## Question 4

Why is `reduce()` located in `functools`?

### Answer

It was moved from the built-in namespace to `functools` in Python 3 because it is a specialised function used less
frequently than other built-ins.

______________________________________________________________________

## Question 5

When would you avoid using `reduce()`?

### Answer

When a dedicated built-in function such as `sum()`, `max()` or `any()` provides a simpler and more readable solution.

______________________________________________________________________

# Assignment

## Exercise 1

Given:

```python
numbers = [5, 10, 15, 20, 25]
```

- Use `map()` to multiply every number by 3.
- Use `filter()` to keep only values greater than 30.
- Use `reduce()` to calculate the total.

______________________________________________________________________

## Exercise 2

Given:

```python
users = [
    {"name": "Alice", "active": True},
    {"name": "Bob", "active": False},
    {"name": "Charlie", "active": True}
]
```

- Use `filter()` to keep only active users.
- Use `map()` to extract their names.

______________________________________________________________________

## Exercise 3

Rewrite all the examples in this lesson using traditional `for` loops.

Compare readability and performance.

______________________________________________________________________

## Exercise 4

Research why Guido van Rossum has stated that list comprehensions are often preferred over `map()` and `filter()` for
simple transformations. Summarise the reasons in your own words.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ The principles of functional programming.
- ✅ What pure functions and side effects are.
- ✅ Why immutability improves reliability.
- ✅ How `map()` transforms data.
- ✅ How `filter()` selects data.
- ✅ How `reduce()` combines data.
- ✅ Why lazy evaluation matters.
- ✅ When functional programming is appropriate in production Python.

______________________________________________________________________

# What's Next

**File:** [24-Comprehensions-vs-Map-Filter](24-comprehensions-vs-map-filter.md)

Topics:

- List Comprehensions
- Dictionary Comprehensions
- Set Comprehensions
- Generator Expressions
- Comprehensions vs `map()`
- Comprehensions vs `filter()`
- Nested Comprehensions
- Performance Benchmarks
- Readability Guidelines
- Production Best Practices

> **Why next?**
>
> While `map()` and `filter()` are foundational functional tools, **list comprehensions and generator expressions are far more common in modern Python codebases**. Understanding when to use each approach is essential for writing clean, idiomatic, production-quality Python.
