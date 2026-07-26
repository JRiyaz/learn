# File: python/07-generators-part-2.md

# Python Advanced - Lesson 07 (Part 2)
# Advanced Generators - Generator Expressions, `yield from` & Generator Control

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 07 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 90 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Generator expressions
- How `yield from` works
- How to send values into generators using `send()`
- How to close generators
- The difference between generators, iterators and lists
- How generators are used to build data processing pipelines

---

# Recap

In the previous lesson, we learned that generators:

- Are iterators
- Produce values lazily
- Use `yield`
- Pause execution after each `yield`
- Resume from the same location

Now we'll explore the more advanced features that make generators extremely powerful.

---

# Generator Expressions

A generator expression is similar to a list comprehension.

List comprehension:

```python
numbers = [number * 2 for number in range(5)]

print(numbers)
```

Output

```
[0, 2, 4, 6, 8]
```

Generator expression:

```python
numbers = (number * 2 for number in range(5))

print(numbers)
```

Output

```
<generator object ...>
```

Notice that no values have been created yet.

---

# Consuming a Generator Expression

```python
numbers = (number * 2 for number in range(5))

for value in numbers:
    print(value)
```

Output

```
0

2

4

6

8
```

The values are generated one at a time.

---

# List vs Generator Expression

```python
numbers = [number for number in range(1_000_000)]
```

Python creates:

```
1

2

3

...

1,000,000
```

immediately.

---

Generator expression:

```python
numbers = (number for number in range(1_000_000))
```

Python creates:

```
Generator Object

↓

1

↓

2

↓

3

↓

...
```

Only one value exists at a time.

---

# When Should You Use Generator Expressions?

Use them when:

- Processing large datasets
- Reading files
- Streaming API responses
- Chaining multiple operations
- Memory efficiency matters

Avoid them when:

- You need random indexing
- You need the data multiple times
- The dataset is small and readability is more important

---

# yield from

Suppose you have two generators.

```python
def numbers():

    yield 1
    yield 2
```

```python
def letters():

    yield "A"
    yield "B"
```

Now combine them.

Without `yield from`:

```python
def combined():

    for value in numbers():
        yield value

    for value in letters():
        yield value
```

Output

```
1

2

A

B
```

This works, but it's repetitive.

---

# Using yield from

```python
def combined():

    yield from numbers()

    yield from letters()
```

Exactly the same output.

```
1

2

A

B
```

`yield from` delegates iteration to another iterable.

---

# Understanding yield from

Without it:

```
combined()

↓

numbers()

↓

yield

↓

combined()

↓

yield
```

With it:

```
combined()

↓

yield from numbers()

↓

Python handles iteration automatically
```

It removes boilerplate code.

---

# Example - Reading Multiple Files

Imagine three log files.

```
server1.log

server2.log

server3.log
```

Without `yield from`:

```python
def all_logs():

    for line in server1():
        yield line

    for line in server2():
        yield line

    for line in server3():
        yield line
```

With `yield from`:

```python
def all_logs():

    yield from server1()

    yield from server2()

    yield from server3()
```

Cleaner and easier to maintain.

---

# Sending Values into Generators

Most people think generators only produce values.

They can also receive values.

Example:

```python
def calculator():

    number = yield

    print(number)
```

Create the generator.

```python
generator = calculator()
```

Start it.

```python
next(generator)
```

The generator pauses at:

```python
number = yield
```

Now send a value.

```python
generator.send(100)
```

Output

```
100
```

The value `100` becomes the result of the `yield` expression.

---

# Why Must next() Be Called First?

This is a common source of confusion.

Consider:

```python
generator = calculator()

generator.send(100)
```

Output

```
TypeError
```

Why?

The generator hasn't reached its first `yield`.

Calling:

```python
next(generator)
```

starts the generator and pauses it at the first `yield`, making it ready to receive values.

---

# A More Practical Example

```python
def running_total():

    total = 0

    while True:

        number = yield total

        total += number
```

Usage:

```python
generator = running_total()

print(next(generator))

print(generator.send(5))

print(generator.send(10))

print(generator.send(20))
```

Output

```
0

5

15

35
```

Notice that the generator remembers the value of `total`.

---

# Closing a Generator

Generators don't always run until completion.

Sometimes you want to stop them early.

```python
def counter():

    while True:

        yield 1
```

Create it.

```python
generator = counter()
```

Close it.

```python
generator.close()
```

Now:

```python
next(generator)
```

raises:

```
StopIteration
```

The generator is permanently closed.

---

# Generators vs Iterators vs Lists

| Feature | List | Iterator | Generator |
|----------|------|----------|-----------|
| Stores all values | ✅ | ❌ | ❌ |
| Lazy evaluation | ❌ | ✅ | ✅ |
| Random indexing | ✅ | ❌ | ❌ |
| Can usually iterate multiple times | ✅ | ❌ | ❌ |
| Memory efficient | ❌ | ✅ | ✅ |
| Easy to implement | ✅ | ❌ | ✅ |

---

# Generator Pipelines

One of the biggest strengths of generators is chaining them together.

Example:

```python
def numbers():

    for number in range(10):
        yield number
```

Filter even numbers.

```python
def even(values):

    for value in values:

        if value % 2 == 0:
            yield value
```

Square them.

```python
def square(values):

    for value in values:
        yield value * value
```

Pipeline:

```python
pipeline = square(even(numbers()))

for value in pipeline:
    print(value)
```

Output

```
0

4

16

36

64
```

Each stage processes one value at a time.

No intermediate lists are created.

---

# Production Insight

Suppose your backend processes uploaded log files.

A poor implementation might:

```
Read Entire File

↓

Filter Errors

↓

Transform Data

↓

Save Results
```

Every step creates another large list.

A generator pipeline works differently.

```
Read One Line

↓

Filter

↓

Transform

↓

Save

↓

Next Line
```

Only one line is in memory at any moment.

Frameworks and libraries that use similar ideas include:

- FastAPI response streaming
- Pandas chunk processing
- Database cursors
- Kafka consumers
- ETL pipelines
- Log processors

This design scales much better for large datasets.

---

# Question

### Question

> What is the difference between a list comprehension and a generator expression?

### Answer

A list comprehension creates and stores all values immediately, while a generator expression produces values lazily as they are requested. Generator expressions are more memory efficient for large datasets.

---

### Question

> What does `yield from` do?

### Answer

`yield from` delegates iteration to another iterable or generator. It automatically yields every value from the delegated iterable without requiring an explicit loop.

---

### Question

> Why would you use `send()`?

### Answer

The `send()` method allows values to be passed back into a paused generator. This enables two-way communication and can be useful for stateful processing, coroutines and event-driven workflows.

---

# Practical Lesson

Create a file:

```
generator_pipeline.py
```

```python
def numbers():

    for number in range(20):
        yield number


def even(values):

    for value in values:

        if value % 2 == 0:
            yield value


def square(values):

    for value in values:
        yield value * value


pipeline = square(even(numbers()))

for value in pipeline:
    print(value)
```

Expected Output

```
0

4

16

36

64

100

144

196

256

324
```

Try replacing the generators with lists and compare the code. Notice how generators avoid creating unnecessary intermediate collections.

---

# Questions

## Question 1

What is a generator expression?

### Answer

A generator expression is a concise way to create a generator. It uses parentheses instead of square brackets and produces values lazily.

---

## Question 2

What does `yield from` simplify?

### Answer

It simplifies yielding values from another iterable or generator by automatically forwarding each value without writing an explicit loop.

---

## Question 3

Why must `next()` usually be called before `send()`?

### Answer

The generator must first execute until it reaches its initial `yield`. Only then is it paused and ready to receive a value through `send()`.

---

## Question 4

What does `generator.close()` do?

### Answer

It terminates the generator by raising `GeneratorExit` internally. After being closed, the generator cannot produce any more values.

---

## Question 5

Why are generator pipelines efficient?

### Answer

Each stage processes one value at a time instead of creating multiple intermediate collections, reducing memory usage and improving scalability.

---

# Assignment

## Exercise 1

Create a generator expression that produces the squares of numbers from **1** to **100**.

Print only the first ten values.

---

## Exercise 2

Create two generators:

- One that yields numbers from **1** to **5**
- Another that yields numbers from **6** to **10**

Combine them using `yield from`.

---

## Exercise 3

Build a three-stage generator pipeline:

1. Generate numbers from **1** to **50**
2. Keep only numbers divisible by **5**
3. Multiply each number by **10**

Print the final output.

---

# Summary

In this lesson, you learned:

- ✅ How generator expressions work.
- ✅ The difference between generator expressions and list comprehensions.
- ✅ How `yield from` delegates iteration.
- ✅ How `send()` enables two-way communication with generators.
- ✅ How to close generators.
- ✅ How generator pipelines process data efficiently.
- ✅ Why generators are widely used in production data processing systems.

---

# What's Next

**File:**
[08-Lambda-Functions](08-lambda-functions.md)
