# File: python/07-generators-part-1.md

# Python Advanced - Lesson 07 (Part 1)

# Generators - Why They Exist & How `yield` Works

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 07 (Part 1)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why generators exist
- What problem generators solve
- What the `yield` keyword does
- The difference between `yield` and `return`
- How generator functions work internally
- Why generators are memory efficient
- Where generators are used in backend development

______________________________________________________________________

# Prerequisites

Before starting this lesson, you should understand:

- ✅ Iterables
- ✅ Iterators
- ✅ The Iterator Protocol (`__iter__()` and `__next__()`)

Generators are Python's way of making custom iterators much easier to write.

______________________________________________________________________

# Why Do Generators Exist?

In the previous lesson, we built a custom iterator.

```python
class Counter:

    def __init__(self, limit):
        self.current = 1
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):

        if self.current > self.limit:
            raise StopIteration

        value = self.current
        self.current += 1

        return value
```

Although it works, notice how much code is required.

To count from **1 to 5**, we had to write:

- A class
- `__init__()`
- `__iter__()`
- `__next__()`
- Manual state management
- `StopIteration`

That's a lot of code for a simple task.

Generators solve this problem.

______________________________________________________________________

# Your First Generator

Let's count from 1 to 5 again.

```python
def counter():

    yield 1
    yield 2
    yield 3
    yield 4
    yield 5
```

Use it like this:

```python
for number in counter():
    print(number)
```

Output

```
1

2

3

4

5
```

The result is identical to our custom iterator.

However, we wrote only a few lines of code.

______________________________________________________________________

# Is a Generator a Function?

At first glance, it looks like one.

```python
def counter():

    yield 1
```

But watch what happens.

```python
result = counter()

print(result)
```

Output

```
<generator object counter at 0x...>
```

The function **does not execute immediately**.

Instead, Python creates a **generator object**.

______________________________________________________________________

# Generator Function vs Generator Object

These two terms are often confused.

## Generator Function

A function containing at least one `yield`.

```python
def counter():

    yield 1
```

______________________________________________________________________

## Generator Object

Created when the function is called.

```python
generator = counter()
```

```
counter
        │
        ▼
Generator Function

counter()
        │
        ▼
Generator Object
```

The generator object is an iterator.

This means:

```python
next(generator)
```

works.

______________________________________________________________________

# Using next()

```python
generator = counter()

print(next(generator))
print(next(generator))
print(next(generator))
```

Output

```
1

2

3
```

Just like any other iterator.

______________________________________________________________________

# What Does `yield` Actually Do?

This is the most important concept in this lesson.

Suppose we have:

```python
def greet():

    print("Hello")

    yield "Python"

    print("World")
```

Create the generator.

```python
generator = greet()
```

Nothing happens.

No output.

Now call:

```python
print(next(generator))
```

Output

```
Hello

Python
```

Notice that:

- `"Hello"` was printed.
- `"Python"` was returned.
- `"World"` did **not** print.

Why?

Because execution paused at `yield`.

______________________________________________________________________

# Execution Resumes

Call `next()` again.

```python
next(generator)
```

Output

```
World

StopIteration
```

Execution resumed **exactly where it stopped**.

This is the key difference between generators and normal functions.

______________________________________________________________________

# Visualising `yield`

```
Start Function

↓

print("Hello")

↓

yield "Python"

↓

⏸ Execution Pauses

↓

next()

↓

Resume Here

↓

print("World")

↓

Function Ends

↓

StopIteration
```

A generator remembers:

- Local variables
- Current line of execution
- Internal state

without requiring you to manage them manually.

______________________________________________________________________

# `yield` vs `return`

This is another common interview topic.

Consider this function.

```python
def add():

    return 10
```

```python
print(add())
```

Output

```
10
```

Once `return` executes,

the function finishes permanently.

______________________________________________________________________

Now compare it with:

```python
def numbers():

    yield 10

    yield 20

    yield 30
```

```python
generator = numbers()

print(next(generator))

print(next(generator))

print(next(generator))
```

Output

```
10

20

30
```

Instead of ending,

the function pauses after each `yield`.

______________________________________________________________________

# Multiple `yield` Statements

A generator may contain many `yield` statements.

```python
def weekdays():

    yield "Monday"

    yield "Tuesday"

    yield "Wednesday"
```

Using a loop:

```python
for day in weekdays():
    print(day)
```

Output

```
Monday

Tuesday

Wednesday
```

Each iteration continues from the previous `yield`.

______________________________________________________________________

# Memory Efficiency

Suppose you need numbers from:

```
1

↓

10,000,000
```

One approach is:

```python
numbers = list(range(10_000_000))
```

This creates **every number** immediately.

Memory usage grows with the size of the list.

______________________________________________________________________

A generator does something different.

```python
def numbers():

    for number in range(10_000_000):

        yield number
```

Only **one value** exists at a time.

```
Generate

↓

Use

↓

Discard

↓

Generate Next

↓

Use

↓

Discard
```

Memory stays almost constant regardless of how many values are produced.

______________________________________________________________________

# Production Insight

Imagine your backend exports one million users as a CSV.

A poor implementation might do this:

```python
users = database.fetch_all_users()

for user in users:
    write_to_csv(user)
```

Every user is loaded into memory first.

Instead, many database libraries stream records.

```python
for user in database.stream_users():
    write_to_csv(user)
```

Internally, `stream_users()` often returns a generator.

This allows your application to process millions of records while using only a small amount of memory.

You'll encounter generators in:

- Database query results
- File processing
- API response streaming
- Kafka consumers
- ETL pipelines
- Background job processing

______________________________________________________________________

# Questions

### Question

> Why were generators introduced in Python?

### Answer

Generators provide a simpler way to create iterators. Instead of implementing `__iter__()` and `__next__()` manually, a
generator function uses `yield`, and Python automatically creates an iterator that maintains its execution state.

______________________________________________________________________

### Question

> What is the difference between `yield` and `return`?

### Answer

`return` immediately terminates a function and optionally returns a value. `yield` pauses execution, returns a value to
the caller, and allows the function to resume from the same point when the next value is requested.

______________________________________________________________________

### Questions

> Why are generators memory efficient?

### Answer

Generators produce values lazily, creating each value only when it is needed instead of storing the entire sequence in
memory. This makes them ideal for processing large datasets or streams.

______________________________________________________________________

# Practical Lesson

Create a file:

```
generator_demo.py
```

```python
def countdown(start):
    """
    Generate numbers from start down to 1.
    """

    while start > 0:

        yield start

        start -= 1


generator = countdown(5)

for number in generator:
    print(number)
```

Expected Output

```
5

4

3

2

1
```

Now replace the `for` loop with repeated calls to `next()` and observe where `StopIteration` occurs.

______________________________________________________________________

# Questions

## Question 1

What is a generator function?

### Answer

A generator function is a function that contains one or more `yield` statements. Calling it returns a generator object
instead of executing the function immediately.

______________________________________________________________________

## Question 2

What is a generator object?

### Answer

A generator object is an iterator created by calling a generator function. It produces values one at a time and
remembers its execution state between calls.

______________________________________________________________________

## Question 3

Does calling a generator function execute its body?

### Answer

No. Calling a generator function creates a generator object. The function body starts executing only when iteration
begins, such as through `next()` or a `for` loop.

______________________________________________________________________

## Question 4

Why does a generator pause at `yield`?

### Answer

The `yield` keyword saves the function's current state and returns a value. Execution resumes from the same point when
the next value is requested.

______________________________________________________________________

## Question 5

When would you choose a generator instead of a list?

### Answer

Use a generator when processing large datasets, files or streams where holding every value in memory is unnecessary.
Generators produce values lazily and use significantly less memory.

______________________________________________________________________

# Assignment

## Exercise 1

Create a generator that yields the first ten even numbers.

______________________________________________________________________

## Exercise 2

Create a generator that yields each character of a string one at a time.

Example:

```
Input

"Python"

Output

P
y
t
h
o
n
```

______________________________________________________________________

## Exercise 3

Create a generator that yields the square of numbers from **1** to **20**.

Print the values using a `for` loop.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why generators exist.
- ✅ What a generator function is.
- ✅ What a generator object is.
- ✅ How `yield` works.
- ✅ The difference between `yield` and `return`.
- ✅ Why generators are memory efficient.
- ✅ Where generators are used in production backend systems.

______________________________________________________________________

# What's Next

**File:** [07-Generators-part-2](07-generators-part-2.md)

Topics:

- Generator Expressions
- `yield from`
- Sending Values into Generators (`send()`)
- Closing Generators
- Real-world Streaming Pipelines
- Generators vs Iterators vs Lists
- Production Examples
