# File: python/06-iterators-and-iterables-part-2.md

# Python Advanced - Lesson 06 (Part 2)

# The Iterator Protocol & Building Custom Iterators

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 06 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What the Iterator Protocol is
- Why Python uses `__iter__()` and `__next__()`
- How to build your own iterator
- How infinite iterators work
- The difference between custom iterators and generators
- Where custom iterators are used in backend applications

______________________________________________________________________

# Theory

In the previous lesson, we learned that every `for` loop does something similar to this:

```python
iterator = iter(iterable)

while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

But here's the question:

> **How does `iter()` know what to do?**

The answer is:

**The Iterator Protocol.**

______________________________________________________________________

# What is the Iterator Protocol?

The Iterator Protocol is simply a set of rules.

To become an iterator, an object must implement two methods:

```python
__iter__()

__next__()
```

These methods tell Python:

- How to start iteration
- How to get the next value

______________________________________________________________________

# __iter__()

The `__iter__()` method returns an iterator.

Example:

```python
numbers = [1, 2, 3]

iterator = numbers.__iter__()

print(iterator)
```

Output

```
<list_iterator object at ...>
```

Normally we write:

```python
iter(numbers)
```

Python internally calls:

```python
numbers.__iter__()
```

These are equivalent.

______________________________________________________________________

# __next__()

The `__next__()` method returns the next value.

Example:

```python
numbers = [1, 2, 3]

iterator = iter(numbers)

print(iterator.__next__())

print(iterator.__next__())
```

Output

```
1

2
```

Normally we write:

```python
next(iterator)
```

Python internally calls:

```python
iterator.__next__()
```

______________________________________________________________________

# Building Your First Iterator

Let's create our own iterator.

The goal:

```
1

2

3

4

5
```

______________________________________________________________________

# Example 1

```python
class Counter:
    """
    A simple iterator that counts
    from 1 up to a given limit.
    """

    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        """
        This object is its own iterator.
        """
        return self

    def __next__(self):
        """
        Return the next value.
        """

        if self.current > self.limit:
            raise StopIteration

        value = self.current

        self.current += 1

        return value


counter = Counter(5)

for number in counter:
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

______________________________________________________________________

# Understanding the Flow

Let's see what happens during:

```python
for number in counter:
    print(number)
```

Python performs these steps:

```
counter

↓

counter.__iter__()

↓

counter.__next__()

↓

1

↓

counter.__next__()

↓

2

↓

...

↓

StopIteration

↓

Loop Ends
```

Nothing magical happens.

The `for` loop simply follows the Iterator Protocol.

______________________________________________________________________

# Why Does __iter__ Return self?

Our `Counter` class is both:

- An iterable
- An iterator

So it returns itself.

```python
def __iter__(self):
    return self
```

Some objects return a **different iterator object**, but returning `self` is common when the object already implements
`__next__()`.

______________________________________________________________________

# Example 2 - Even Numbers Iterator

```python
class EvenNumbers:

    def __init__(self, limit):
        self.current = 2
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):

        if self.current > self.limit:
            raise StopIteration

        value = self.current

        self.current += 2

        return value


for number in EvenNumbers(10):
    print(number)
```

Output

```
2

4

6

8

10
```

Notice how we completely control what values are produced.

______________________________________________________________________

# Infinite Iterators

Not all iterators stop.

Example:

```python
class InfiniteCounter:

    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):

        value = self.number

        self.number += 1

        return value
```

This iterator never raises:

```python
StopIteration
```

Using:

```python
for number in InfiniteCounter():
    print(number)
```

would run forever.

______________________________________________________________________

# Limiting an Infinite Iterator

Instead of using a `for` loop,

call `next()` manually.

```python
counter = InfiniteCounter()

for _ in range(5):
    print(next(counter))
```

Output

```
1

2

3

4

5
```

______________________________________________________________________

# Iterator vs Generator

We haven't learned generators yet,

but here's a preview.

Custom Iterator

```python
class Counter:

    def __iter__(self):
        return self

    def __next__(self):
        ...
```

Generator

```python
def counter():

    yield 1

    yield 2

    yield 3
```

Both produce values one at a time.

The difference is:

| Custom Iterator | Generator |
|-----------------|-----------|
| Uses a class | Uses a function |
| Requires `__iter__()` and `__next__()` | Uses `yield` |
| More code | Less code |
| More control | Easier to write |

We'll study generators in the next lesson.

______________________________________________________________________

# Production Insight

Suppose you're processing millions of records from a database.

Instead of loading everything into memory:

```python
users = database.fetch_all()
```

you can stream one record at a time.

```python
for user in database:
    process(user)
```

The database object may internally implement the Iterator Protocol.

Other real-world examples include:

- Reading large CSV files
- Processing log files
- Kafka message consumers
- Streaming API responses
- Database cursors

Using iterators allows applications to process huge datasets efficiently without exhausting memory.

______________________________________________________________________

# Questions

### Question

> What methods must a custom iterator implement?

### Answer

A custom iterator must implement `__iter__()` and `__next__()`. The `__iter__()` method returns the iterator object,
while `__next__()` returns the next value and raises `StopIteration` when there are no more values.

______________________________________________________________________

### Question

> Why is `StopIteration` important?

### Answer

`StopIteration` signals that the iterator has been exhausted. Python's `for` loop catches this exception internally and
ends the iteration gracefully.

______________________________________________________________________

### Question

> What is the difference between an iterable and an iterator?

### Answer

An iterable can produce an iterator using `iter()`. An iterator maintains iteration state and produces one value at a
time using `next()`.

______________________________________________________________________

# Practical Lesson

Create a file:

```
custom_iterator.py
```

```python
class Countdown:
    """
    Count backwards from a given number.
    """

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):

        if self.current == 0:
            raise StopIteration

        value = self.current

        self.current -= 1

        return value


for number in Countdown(5):
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

Now modify the iterator so that it counts down by **2** instead of **1**.

______________________________________________________________________

# Questions

## Question 1

What is the Iterator Protocol?

### Answer

The Iterator Protocol is a set of rules that allows Python to iterate over objects. An iterator must implement
`__iter__()` and `__next__()`.

______________________________________________________________________

## Question 2

What should `__iter__()` return?

### Answer

It should return an iterator object. If the object itself is an iterator, it usually returns `self`.

______________________________________________________________________

## Question 3

When should `__next__()` raise `StopIteration`?

### Answer

It should raise `StopIteration` when there are no more values to produce.

______________________________________________________________________

## Question 4

Can an iterator be infinite?

### Answer

Yes. An iterator can continue producing values indefinitely if it never raises `StopIteration`.

______________________________________________________________________

## Question 5

Why are generators often preferred over custom iterators?

### Answer

Generators are easier to write and automatically implement the Iterator Protocol. They provide the same lazy evaluation
with much less code.

______________________________________________________________________

# Assignment

## Exercise 1

Create a custom iterator that returns:

```
10

20

30

40

50
```

______________________________________________________________________

## Exercise 2

Create an iterator that returns the characters of your name one at a time.

______________________________________________________________________

## Exercise 3

Create an infinite iterator that generates even numbers.

Use `next()` to print only the first ten values.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What the Iterator Protocol is.
- ✅ How `__iter__()` works.
- ✅ How `__next__()` works.
- ✅ How to build a custom iterator.
- ✅ How infinite iterators work.
- ✅ The difference between iterators and generators.

______________________________________________________________________

# What's Next

**File:** [07-Generators-part-1](07-generators-part-1.md)

Topics:

- Why Generators Exist
- The `yield` Keyword
- Generator Functions
- Generator Objects
- Memory Efficiency
- `yield` vs `return`
- Real-world Backend Examples
