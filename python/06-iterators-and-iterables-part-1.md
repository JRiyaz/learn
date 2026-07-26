# File: python/python-advanced-06-iterators-and-iterables-part-1.md

# Python Advanced - Lesson 06 (Part 1)
# Iterables, Iterators & The Iterator Protocol

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 06 (Part 1)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What an iterable is
- What an iterator is
- The difference between iterables and iterators
- The Iterator Protocol
- How `iter()` works
- How `next()` works
- What actually happens inside a `for` loop

---

# Why Should You Learn This?

Generators, file handling, database cursors, streaming APIs and even `for` loops all rely on the **Iterator Protocol**.

If you understand iterators, you'll understand:

- Generators
- File reading
- Database result streaming
- Large data processing
- Memory-efficient programming

---

# Theory

Suppose you have a list.

```python
numbers = [10, 20, 30]
```

You can write:

```python
for number in numbers:
    print(number)
```

Question:

How does Python know how to move from:

```
10

↓

20

↓

30
```

The answer is:

**Iterators.**

---

# What is an Iterable?

An iterable is any object that can produce its values one at a time.

Examples:

```python
list

tuple

string

dictionary

set

range

file
```

Example

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

The list itself is an iterable.

It knows **how to create an iterator**.

---

# What is an Iterator?

An iterator is an object that remembers:

- Where it currently is
- What the next value is

Think of an iterator as a bookmark inside a book.

```
Book

↓

Page 1

↓

Page 2

↓

Page 3

↓

Bookmark
```

Every time you call `next()`,

the bookmark moves forward.

---

# Iterable vs Iterator

This is one of the most common interview questions.

| Iterable | Iterator |
|----------|----------|
| Can produce an iterator | Produces values one at a time |
| Can be iterated multiple times | Usually consumed only once |
| Uses `iter()` | Uses `next()` |

Remember:

```
Iterable

↓

iter()

↓

Iterator

↓

next()

↓

Values
```

---

# Example 1 - Creating an Iterator

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(iterator)
```

Output

```
<list_iterator object at ...>
```

Notice that:

```python
numbers
```

is **not** the iterator.

Calling

```python
iter(numbers)
```

creates a new iterator.

---

# Example 2 - Using next()

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))

print(next(iterator))

print(next(iterator))
```

Output

```
10

20

30
```

Every call to `next()` returns the next value.

---

# What Happens After the Last Item?

Let's call `next()` again.

```python
print(next(iterator))
```

Output

```
StopIteration
```

This exception tells Python:

> "There are no more values."

---

# Visualization

```
numbers

↓

[10, 20, 30]

↓

iter()

↓

Iterator

↓

next()

↓

10

↓

next()

↓

20

↓

next()

↓

30

↓

next()

↓

StopIteration
```

---

# Why Doesn't a for Loop Raise StopIteration?

Consider this code.

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Output

```
10

20

30
```

Why don't we see:

```
StopIteration
```

Because Python catches it internally.

A `for` loop works roughly like this:

```python
iterator = iter(numbers)

while True:

    try:
        value = next(iterator)

        print(value)

    except StopIteration:
        break
```

This is essentially what Python does behind the scenes.

---

# Example 3 - Strings are Iterables

```python
name = "Riyaz"

iterator = iter(name)

print(next(iterator))

print(next(iterator))

print(next(iterator))
```

Output

```
R

i

y
```

Strings are iterables too.

---

# Example 4 - Dictionaries

```python
user = {

    "name": "Alice",

    "age": 25
}

iterator = iter(user)

print(next(iterator))

print(next(iterator))
```

Output

```
name

age
```

By default,

iterating over a dictionary returns its **keys**.

---

# Iterator Exhaustion

An iterator can usually be used only once.

Example

```python
numbers = [1, 2, 3]

iterator = iter(numbers)

for value in iterator:
    print(value)

print("Second Loop")

for value in iterator:
    print(value)
```

Output

```
1

2

3

Second Loop
```

Nothing prints the second time.

Why?

Because the iterator has already reached the end.

To iterate again,

create a new iterator.

```python
iterator = iter(numbers)
```

---

# Production Insight

Suppose you're reading a huge log file.

Instead of loading the entire file into memory,

Python reads one line at a time.

```python
with open("server.log") as file:

    for line in file:

        print(line)
```

The file object is an iterable.

Internally,

Python creates an iterator that reads one line at a time.

This allows Python to process files that are several gigabytes in size without consuming excessive memory.

The same concept is used in:

- Database cursors
- CSV readers
- Kafka consumers
- API response streaming

---

# Interview Deep Dive

### Interviewer

> What is the difference between an iterable and an iterator?

### Answer

An iterable is an object capable of producing an iterator. An iterator is an object that keeps track of its current position and returns one value at a time using `next()`. Every iterator is iterable, but not every iterable is an iterator.

---

### Interviewer

> What happens when a `for` loop starts?

### Answer

Python calls `iter()` on the iterable to create an iterator. It repeatedly calls `next()` until a `StopIteration` exception is raised, which signals that iteration has finished.

---

### Interviewer

> Why can an iterator usually be used only once?

### Answer

Because it maintains internal state. Each call to `next()` advances the iterator. Once it reaches the end, it is exhausted and must be recreated using `iter()` if you want to iterate again.

---

# Practical Lesson

Create a file:

```
iterator_demo.py
```

```python
numbers = [100, 200, 300]

# Create an iterator.
iterator = iter(numbers)

print(next(iterator))

print(next(iterator))

print(next(iterator))

try:

    print(next(iterator))

except StopIteration:

    print("No more values!")
```

Expected Output

```
100

200

300

No more values!
```

Now replace the list with:

```python
"Python"
```

Observe how strings also behave as iterables.

---

# Interview Questions

## Question 1

What is an iterable?

### Answer

An iterable is any object that can return an iterator using the `iter()` function.

Examples include lists, tuples, strings, dictionaries, sets, files and ranges.

---

## Question 2

What is an iterator?

### Answer

An iterator is an object that returns one value at a time using the `next()` function while keeping track of its current position.

---

## Question 3

What exception signals the end of iteration?

### Answer

`StopIteration`

Python raises this exception when there are no more values to return.

---

## Question 4

What does `iter()` do?

### Answer

It creates and returns an iterator from an iterable object.

---

## Question 5

Why doesn't a `for` loop raise `StopIteration`?

### Answer

Because Python catches the `StopIteration` exception internally and uses it to terminate the loop gracefully.

---

# Assignment

## Exercise 1

Create an iterator from a tuple.

Retrieve every value manually using `next()`.

---

## Exercise 2

Create an iterator from a string.

Print each character using `next()` until `StopIteration` occurs.

Handle the exception gracefully.

---

## Exercise 3

Write a program that demonstrates iterator exhaustion.

Iterate over the same iterator twice and explain why the second loop produces no output.

---

# Summary

In this lesson, you learned:

- ✅ What an iterable is.
- ✅ What an iterator is.
- ✅ The difference between iterables and iterators.
- ✅ How `iter()` creates an iterator.
- ✅ How `next()` retrieves values.
- ✅ Why `StopIteration` exists.
- ✅ What a `for` loop does internally.

---

# What's Next

**File:**

`python/python-advanced-06-iterators-and-iterables-part-2.md`

Topics:

- The Iterator Protocol (`__iter__()` and `__next__()`)
- Building a Custom Iterator
- Infinite Iterators
- Iterators vs Generators
- Real-world Backend Examples
- Interview Questions
