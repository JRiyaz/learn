# File: python/09-context-managers-part-1.md

# Python Advanced - Lesson 09 (Part 1)
# Context Managers - Managing Resources Safely with `with`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 09 (Part 1)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why context managers exist
- What problem the `with` statement solves
- The Context Manager Protocol
- The purpose of `__enter__()` and `__exit__()`
- How files use context managers
- How to build your first custom context manager
- Real-world backend use cases

---

# Prerequisites

Before starting this lesson, you should understand:

- Classes and objects (basic)
- Exceptions (`try` / `except`)
- Functions

Don't worry if you haven't studied OOP deeply yet. We'll only use simple classes in this lesson.

---

# Why Do Context Managers Exist?

Imagine you need to read a file.

A beginner might write:

```python
file = open("users.txt")

content = file.read()

print(content)

file.close()
```

This works.

But what happens if an exception occurs before `file.close()`?

```python
file = open("users.txt")

content = file.read()

raise Exception("Something went wrong!")

file.close()
```

Output

```
Exception: Something went wrong!
```

Notice that:

```
file.close()
```

never executes.

The file remains open until Python eventually cleans it up.

This is called a **resource leak**.

---

# What is a Resource?

A resource is anything that must be acquired and later released.

Examples include:

- Files
- Database connections
- Network sockets
- Locks
- Threads
- Temporary files

If resources are not released properly, your application can:

- Waste memory
- Keep files locked
- Exhaust database connections
- Slow down or crash

---

# The Traditional Solution

Before context managers became common, developers used:

```python
file = open("users.txt")

try:

    content = file.read()

    print(content)

finally:

    file.close()
```

Why `finally`?

Because it always executes.

Even if an exception occurs.

This works well, but it's repetitive.

---

# The with Statement

Python introduced the `with` statement to automate this pattern.

Instead of writing:

```python
file = open("users.txt")

try:

    content = file.read()

finally:

    file.close()
```

you simply write:

```python
with open("users.txt") as file:

    content = file.read()

    print(content)
```

When the block finishes,

Python automatically closes the file.

Even if an exception occurs.

---

# Visualising the with Statement

```
Open Resource

↓

Run Code

↓

Exception?

↓

Yes / No

↓

Always Clean Up

↓

Continue
```

This automatic cleanup is the main purpose of a context manager.

---

# What is a Context Manager?

A context manager is an object that manages a resource.

It has two responsibilities:

1. Acquire the resource.
2. Release the resource.

Python performs these steps automatically.

---

# The Context Manager Protocol

A context manager implements two special methods.

```python
__enter__()

__exit__()
```

These methods form the **Context Manager Protocol**.

---

# __enter__()

`__enter__()` runs when entering the `with` block.

Example flow:

```
with Resource():

↓

__enter__()

↓

Your Code
```

Its job is usually to:

- Open a file
- Connect to a database
- Acquire a lock
- Allocate a resource

---

# __exit__()

`__exit__()` runs when leaving the `with` block.

Even if an exception occurs.

```
Your Code

↓

Exception?

↓

Yes / No

↓

__exit__()
```

Its job is to clean up resources.

---

# Building Your First Context Manager

Let's build one from scratch.

```python
class Resource:

    def __enter__(self):

        print("Opening Resource")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Closing Resource")
```

Use it.

```python
with Resource():

    print("Working...")
```

Output

```
Opening Resource

Working...

Closing Resource
```

Notice that:

`__exit__()` runs automatically.

---

# Returning a Value from __enter__()

Usually,

`__enter__()` returns the resource you'll use.

Example:

```python
class Database:

    def __enter__(self):

        print("Connected")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Disconnected")
```

Usage:

```python
with Database() as database:

    print(database)
```

Output

```
Connected

<Database object ...>

Disconnected
```

The value returned by `__enter__()` becomes the variable after `as`.

---

# What Happens if an Exception Occurs?

```python
class Resource:

    def __enter__(self):

        print("Opening")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Closing")
```

Now:

```python
with Resource():

    print("Working")

    raise ValueError("Unexpected Error")
```

Output

```
Opening

Working

Closing

ValueError: Unexpected Error
```

Even though an exception occurred,

`__exit__()` still executed.

This is the guarantee provided by context managers.

---

# Understanding the Parameters of __exit__()

The signature is:

```python
def __exit__(self, exc_type, exc_value, traceback):
```

These parameters describe any exception that occurred.

| Parameter | Description |
|-----------|-------------|
| `exc_type` | Exception class (e.g. `ValueError`) |
| `exc_value` | Exception instance |
| `traceback` | Traceback object |

If no exception occurs,

all three parameters are `None`.

---

# What Happens Internally?

This code:

```python
with Resource() as resource:

    print("Working")
```

is conceptually similar to:

```python
resource_manager = Resource()

resource = resource_manager.__enter__()

try:

    print("Working")

finally:

    resource_manager.__exit__(None, None, None)
```

The real implementation is more sophisticated because it also handles exceptions, but this is the basic idea.

---

# Production Insight

Context managers are everywhere in backend applications.

Examples include:

Opening files:

```python
with open("users.csv") as file:
```

Database transactions:

```python
with database.transaction():
    ...
```

Thread locks:

```python
with lock:
    ...
```

Temporary directories:

```python
with TemporaryDirectory() as directory:
    ...
```

HTTP client sessions:

```python
with requests.Session() as session:
    ...
```

In all of these cases, the context manager ensures that resources are cleaned up properly, even if errors occur.

---

# Questions

### Question

> Why should you use the `with` statement instead of manually calling `close()`?

### Answer

The `with` statement guarantees that resources are released correctly, even if an exception occurs. It reduces boilerplate code and prevents resource leaks.

---

### Question

> What methods must a context manager implement?

### Answer

A context manager implements `__enter__()` and `__exit__()`. `__enter__()` prepares the resource and returns the object used inside the `with` block. `__exit__()` performs cleanup when the block finishes.

---

### Question

> What is passed to `__exit__()`?

### Answer

Python passes the exception type, exception instance and traceback if an exception occurs. If the block exits normally, all three arguments are `None`.

---

# Practical Lesson

Create a file:

```
resource_manager.py
```

```python
class Resource:

    def __enter__(self):

        print("Resource Opened")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Resource Closed")


with Resource():

    print("Using Resource")
```

Expected Output

```
Resource Opened

Using Resource

Resource Closed
```

Now modify the `with` block to raise an exception.

Observe that `__exit__()` still executes.

---

# Questions

## Question 1

What problem do context managers solve?

### Answer

They ensure that resources such as files, database connections and locks are always released correctly, even when exceptions occur.

---

## Question 2

When is `__enter__()` executed?

### Answer

It is executed immediately before entering the `with` block and usually acquires or prepares the resource.

---

## Question 3

When is `__exit__()` executed?

### Answer

It is executed whenever the `with` block finishes, whether normally or because of an exception.

---

## Question 4

What does `__enter__()` usually return?

### Answer

It typically returns the resource or object that will be assigned to the variable following the `as` keyword.

---

## Question 5

Why is the `with` statement safer than manually calling `close()`?

### Answer

Because cleanup is guaranteed to happen even if an exception interrupts the normal flow of execution.

---

# Assignment

## Exercise 1

Create a context manager that prints:

```
Entering

Leaving
```

around a block of code.

---

## Exercise 2

Modify your context manager to return a string from `__enter__()`.

Print the returned value inside the `with` block.

---

## Exercise 3

Raise an exception inside the `with` block and verify that `__exit__()` is still executed.

---

# Summary

In this lesson, you learned:

- ✅ Why context managers exist.
- ✅ What the `with` statement does.
- ✅ The Context Manager Protocol.
- ✅ How `__enter__()` works.
- ✅ How `__exit__()` works.
- ✅ How Python guarantees resource cleanup.
- ✅ Why context managers are essential in backend applications.

---

# What's Next

**File:**
[09-Context-Managers-part-2](09-context-managers-part-2.md)

Topics:

- Exception Handling in `__exit__()`
- Suppressing Exceptions
- `contextlib.contextmanager`
- Nested Context Managers
- Multiple Context Managers
- Real-world Database Transactions
- Production Examples
