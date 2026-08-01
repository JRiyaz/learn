# File: python/27-itertools-part-1.md

# Python Functional Programming - Part 5

# `itertools` Part 1 - Infinite Iterators and Iterator Building Blocks

> **Course:** Backend Engineering Roadmap
>
> **Module:** Functional Python
>
> **Lesson:** 5
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 170 Minutes

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `itertools` module | Python 2.3 |
| `count()` | Python 2.3 |
| `cycle()` | Python 2.3 |
| `repeat()` | Python 2.3 |
| `chain()` | Python 2.3 |
| `islice()` | Python 2.3 |

### Important Notes

- All `itertools` functions return **iterators**, not lists.
- They are implemented in highly optimised **C code**, making them faster than equivalent pure Python implementations in many scenarios.
- The biggest advantage of `itertools` is **lazy evaluation**, allowing you to process datasets much larger than available memory.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why `itertools` exists
- Lazy iterator pipelines
- Infinite iterators
- `count()`
- `cycle()`
- `repeat()`
- `chain()`
- `islice()`
- Memory optimisation
- Production use cases
- Performance considerations

______________________________________________________________________

# Recap

So far you've learned

- Functional Programming
- `map()`
- `filter()`
- `reduce()`
- Comprehensions
- Generator Expressions
- `zip()`
- `enumerate()`
- `any()`
- `all()`
- `functools`

Today we'll begin studying one of the most powerful modules in Python's standard library.

```
itertools
```

Many experienced Python developers consider it one of the most valuable modules to master.

______________________________________________________________________

# Why Does itertools Exist?

Suppose you need to process

```
10 GB CSV

↓

Transform rows

↓

Filter rows

↓

Aggregate results
```

Loading everything into memory first is inefficient.

Instead, we process

```
One Row

↓

Transform

↓

Filter

↓

Output

↓

Next Row
```

This streaming approach is exactly what `itertools` enables.

______________________________________________________________________

# Philosophy of itertools

The module provides

> "Fast, memory-efficient tools for working with iterators."

Instead of repeatedly writing loops,

Python provides reusable iterator building blocks.

Think of them as LEGO bricks.

```
Iterator

↓

chain()

↓

filter()

↓

map()

↓

islice()

↓

Output
```

______________________________________________________________________

# Categories of itertools

The module can roughly be divided into three groups.

```
itertools

│

├── Infinite Iterators

├── Finite Iterators

└── Combinatoric Iterators
```

Today we'll study the first two groups.

Combinatoric iterators deserve an entire lesson of their own.

______________________________________________________________________

# Lazy Evaluation Refresher

Remember

```python
map()

filter()

zip()

generator expressions
```

All of them are lazy.

`itertools` continues the same philosophy.

Nothing happens until values are requested.

______________________________________________________________________

# Part 1 — count()

______________________________________________________________________

# What is count()?

`count()` creates an infinite sequence of numbers.

Import

```python
from itertools import count
```

Example

```python
from itertools import count

counter = count()

print(next(counter))

print(next(counter))

print(next(counter))
```

Output

```
0

1

2
```

Notice

The iterator never ends.

______________________________________________________________________

# Starting Value

Default

```python
count()
```

starts at

```
0
```

Specify another starting value.

```python
counter = count(100)

print(next(counter))

print(next(counter))
```

Output

```
100

101
```

______________________________________________________________________

# Step Size

```python
counter = count(

    start=10,

    step=5

)

print(next(counter))

print(next(counter))

print(next(counter))
```

Output

```
10

15

20
```

______________________________________________________________________

# Visualising count()

```
count()

↓

0

↓

1

↓

2

↓

3

↓

4

↓

∞
```

______________________________________________________________________

# Why Is It Infinite?

There is no stopping condition.

Internally,

Python simply keeps adding the step value.

______________________________________________________________________

# Danger

Never write

```python
list(count())
```

It never finishes.

Your program will eventually exhaust available memory.

______________________________________________________________________

# Production Example

Generating IDs

```python
from itertools import count

request_ids = count(1000)

print(next(request_ids))
```

Output

```
1000
```

Each request receives a unique sequential identifier.

______________________________________________________________________

# Part 2 — cycle()

______________________________________________________________________

# What is cycle()?

Suppose we have

```python
colors = [

    "Red",

    "Green",

    "Blue"

]
```

Normally

```
Red

Green

Blue

Stop
```

With

```python
cycle()
```

```
Red

Green

Blue

Red

Green

Blue

...
```

Forever.

______________________________________________________________________

# Example

```python
from itertools import cycle

colors = [

    "Red",

    "Green",

    "Blue"

]

iterator = cycle(colors)

print(next(iterator))

print(next(iterator))

print(next(iterator))

print(next(iterator))
```

Output

```
Red

Green

Blue

Red
```

______________________________________________________________________

# Visualising cycle()

```
Red

↓

Green

↓

Blue

↓

Back to Red

↓

Repeat Forever
```

______________________________________________________________________

# Production Example

Round-robin load balancing.

Servers

```
Server A

Server B

Server C
```

Requests

```
A

B

C

A

B

C
```

Using

```python
cycle(servers)
```

makes this trivial.

______________________________________________________________________

# Important Note

`cycle()` stores a copy of the iterable internally.

For huge iterables,

this may consume significant memory.

______________________________________________________________________

# Part 3 — repeat()

______________________________________________________________________

# What is repeat()?

Sometimes we need the same value repeatedly.

Instead of

```python
for _ in range(5):

    print("Hello")
```

we can use

```python
repeat()
```

______________________________________________________________________

# Example

```python
from itertools import repeat

iterator = repeat(

    "Hello",

    3

)

print(list(iterator))
```

Output

```
[

'Hello',

'Hello',

'Hello'

]
```

______________________________________________________________________

# Infinite repeat()

Without a limit

```python
repeat("A")
```

produces

```
A

A

A

A

...
```

forever.

______________________________________________________________________

# Production Example

Suppose every API request uses the same timeout.

```python
timeouts = repeat(30)
```

Combined with `zip()`.

```python
for url, timeout in zip(

    urls,

    repeat(30)

):

    ...
```

Every URL receives the same timeout value without constructing a second list.

______________________________________________________________________

# Part 4 — chain()

______________________________________________________________________

# The Problem

Suppose

```python
numbers1 = [

    1,

    2

]

numbers2 = [

    3,

    4
]
```

We want

```
1

2

3

4
```

Traditional

```python
numbers1 + numbers2
```

Works,

but creates a new list.

______________________________________________________________________

# chain()

```python
from itertools import chain

iterator = chain(

    numbers1,

    numbers2

)

print(

    list(iterator)

)
```

Output

```
[

1,

2,

3,

4

]
```

______________________________________________________________________

# Visualising chain()

```
Iterator A

↓

Iterator B

↓

Iterator C

↓

Single Stream
```

______________________________________________________________________

# Why Is chain Better?

List concatenation

```
Create New List

↓

Copy Items
```

`chain()`

```
Iterator A

↓

Iterator B

↓

No Copy
```

It simply visits one iterable after another.

______________________________________________________________________

# chain.from_iterable()

Suppose

```python
lists = [

    [1, 2],

    [3, 4],

    [5, 6]

]
```

Instead of

```python
chain(

    *lists

)
```

write

```python
chain.from_iterable(

    lists

)
```

Output

```
1

2

3

4

5

6
```

This is especially useful when the number of iterables is unknown.

______________________________________________________________________

# Production Example

Suppose a service fetches users from multiple sources.

```python
internal_users

external_users

guest_users
```

Process them as one stream.

```python
for user in chain(

    internal_users,

    external_users,

    guest_users

):

    process(user)
```

______________________________________________________________________

# Part 5 — islice()

______________________________________________________________________

# The Problem

Consider

```python
count()
```

It's infinite.

How do we stop after ten values?

Using

```python
list(count())
```

is impossible.

______________________________________________________________________

# islice()

```python
from itertools import count

from itertools import islice

numbers = count()

print(

    list(

        islice(

            numbers,

            5

        )

    )

)
```

Output

```
[

0,

1,

2,

3,

4

]
```

______________________________________________________________________

# Visualising islice()

```
Iterator

↓

Take First 5

↓

Stop
```

______________________________________________________________________

# Start and Stop

```python
numbers = count()

print(

    list(

        islice(

            numbers,

            10,

            15

        )

    )

)
```

Output

```
[

10,

11,

12,

13,

14

]
```

Similar to

```python
range(

    10,

    15
)
```

but works with any iterator.

______________________________________________________________________

# Step

```python
numbers = count()

print(

    list(

        islice(

            numbers,

            0,

            10,

            2

        )

    )

)
```

Output

```
[

0,

2,

4,

6,

8

]
```

______________________________________________________________________

# Iterator Pipeline

One of the biggest strengths of `itertools`.

Example

```python
from itertools import (
    count,
    islice
)

numbers = count(1)

squares = (

    value ** 2

    for value in numbers

)

result = islice(

    squares,

    10

)

print(

    list(result)

)
```

Processing

```
Generate Number

↓

Square

↓

Take 10

↓

Stop
```

No unnecessary work is performed.

______________________________________________________________________

# Why Not Use range()?

favourite Questions.

`range()` already has

```
start

stop

step
```

Why use

```
count()

+

islice()
```

Answer:

Because `range()` only works with integer sequences.

`islice()` works with **any iterator**.

Examples

- Database cursors
- File objects
- Network streams
- Generator functions
- `zip()`
- `map()`
- `filter()`

______________________________________________________________________

# Performance Considerations

All these tools

- Are lazy.
- Avoid unnecessary memory allocation.
- Are implemented in C.
- Compose well with generators.

They are particularly valuable when processing large datasets.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Calling

```python
list(count())
```

on an infinite iterator.

______________________________________________________________________

## Mistake 2

Assuming `cycle()` does not use additional memory.

It stores previously seen values.

______________________________________________________________________

## Mistake 3

Using `chain()` after converting everything into lists first.

You lose its memory benefits.

______________________________________________________________________

## Mistake 4

Using `islice()` on an iterator and expecting skipped values to remain available.

Iterators are consumed as they are advanced.

Example

```python
numbers = iter([1, 2, 3, 4, 5])

print(list(islice(numbers, 2)))  # [1, 2]
print(list(numbers))             # [3, 4, 5]
```

______________________________________________________________________

# Best Practices

✅ Prefer `chain()` over list concatenation for large iterables.

✅ Use `islice()` when working with iterators instead of converting them into lists.

✅ Use `repeat()` to avoid creating unnecessary constant-value collections.

✅ Use `count()` for sequential IDs in non-persistent contexts.

❌ Don't use infinite iterators without a stopping condition.

❌ Don't assume every `itertools` function is memory-free—understand each one's behaviour.

______________________________________________________________________

# Production Insight

`itertools` is used heavily in systems that process **streams of data** rather than fixed collections.

Common examples include:

- Reading millions of database rows.
- Processing large log files.
- Streaming API responses.
- ETL (Extract, Transform, Load) pipelines.
- Message queue consumers.
- Event processing systems.

The ability to process one item at a time keeps memory usage low and allows applications to scale to datasets that would
never fit into RAM.

______________________________________________________________________

# Questions

### Question

> Why is `itertools` considered memory efficient?

### Answer

Most `itertools` functions return lazy iterators that generate values only when requested instead of creating entire
collections in memory.

______________________________________________________________________

### Question

> What is the difference between `chain()` and using the `+` operator on lists?

### Answer

`+` creates a new list by copying elements, whereas `chain()` lazily iterates through each iterable without copying.

______________________________________________________________________

### Question

> Why can't you call `list(count())`?

### Answer

Because `count()` produces an infinite sequence, so iteration never terminates and memory usage will continue growing.

______________________________________________________________________

### Question

> When would you use `islice()` instead of list slicing?

### Answer

When working with iterators or generators that don't support normal slicing, allowing lazy extraction of a subset of
values.

______________________________________________________________________

# Practical Lesson

Create a file:

```
itertools_part_1.py
```

```python
from itertools import (
    count,
    cycle,
    repeat,
    chain,
    islice,
)


# count()
counter = count(start=10, step=2)

print(next(counter))
print(next(counter))
print(next(counter))


# cycle()
colours = cycle(["Red", "Green"])

print(next(colours))
print(next(colours))
print(next(colours))


# repeat()
print(list(repeat("Python", 3)))


# chain()
numbers = chain([1, 2], [3, 4])

print(list(numbers))


# islice()
values = islice(count(), 5)

print(list(values))
```

Expected Output

```
10
12
14

Red
Green
Red

['Python', 'Python', 'Python']

[1, 2, 3, 4]

[0, 1, 2, 3, 4]
```

______________________________________________________________________

# Questions

## Question 1

Why is `itertools` faster than many equivalent Python implementations?

### Answer

Many `itertools` functions are implemented in C and avoid creating unnecessary intermediate collections.

______________________________________________________________________

## Question 2

What is the purpose of `count()`?

### Answer

It creates an infinite iterator that generates sequential values starting from a specified number and incrementing by a
configurable step.

______________________________________________________________________

## Question 3

What is the difference between `chain()` and `chain.from_iterable()`?

### Answer

`chain()` accepts multiple iterables as separate arguments, while `chain.from_iterable()` accepts a single iterable
whose elements are themselves iterables.

______________________________________________________________________

## Question 4

Why is `cycle()` potentially memory intensive?

### Answer

It stores the values it has already seen so that it can repeat them indefinitely.

______________________________________________________________________

## Question 5

What makes `islice()` different from normal slicing?

### Answer

`islice()` works lazily with any iterator, while normal slicing requires a sequence type that supports indexing.

______________________________________________________________________

# Assignment

## Exercise 1

Use `count()` and `islice()` to generate the first 20 multiples of 7.

______________________________________________________________________

## Exercise 2

Create a round-robin task scheduler using `cycle()` for three worker names.

Stop after assigning 15 tasks.

______________________________________________________________________

## Exercise 3

Merge the following iterables using both `chain()` and `chain.from_iterable()`:

```python
api_users = ["Alice", "Bob"]
db_users = ["Charlie"]
cache_users = ["David", "Emma"]
```

Explain when `chain.from_iterable()` is preferable.

______________________________________________________________________

## Exercise 4

Build a processing pipeline that:

1. Generates numbers using `count(1)`.
1. Squares each number using a generator expression.
1. Uses `islice()` to return the first 25 squared values.
1. Prints the result without creating unnecessary intermediate lists.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why the `itertools` module exists.
- ✅ How lazy iterators improve memory efficiency.
- ✅ How to use `count()`, `cycle()` and `repeat()`.
- ✅ How `chain()` combines iterables without copying.
- ✅ How `islice()` slices any iterator lazily.
- ✅ Common production use cases for iterator pipelines.
- ✅ Performance characteristics and common pitfalls.

______________________________________________________________________

# What's Next

**File:** [28-Itertools-part-2](28-itertools-part-2.md)

Topics:

- Combinatoric Iterators
- `product()`
- `permutations()`
- `combinations()`
- `combinations_with_replacement()`
- `accumulate()`
- `groupby()`
- `tee()`
- `pairwise()` (Python 3.10+)
- Real-world Production Examples
- Performance Considerations

> **Why next?**
>
> The remaining `itertools` functions solve many advanced problems involving combinations, grouping, cumulative calculations and iterator duplication. They are frequently used in analytics, scheduling, optimisation algorithms, recommendation systems and technical interviews.
