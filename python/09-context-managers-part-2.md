# File: python/09-context-managers-part-2.md

# Python Advanced - Lesson 09 (Part 2)
# Advanced Context Managers - Exception Handling & `contextlib`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 09 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 90 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- How exceptions are handled inside context managers
- How `__exit__()` can suppress exceptions
- How to create context managers using `contextlib.contextmanager`
- How nested and multiple context managers work
- Real-world database transaction patterns
- Best practices for writing production-ready context managers

---

# Recap

In the previous lesson, we learned that a context manager implements:

```python
__enter__()

__exit__()
```

Python executes them like this:

```
__enter__()

↓

Your Code

↓

__exit__()
```

Even if an exception occurs,

`__exit__()` is always executed.

Now let's see how exceptions are handled.

---

# Understanding __exit__()

The full method signature is:

```python
def __exit__(self, exc_type, exc_value, traceback):
```

Suppose this code runs:

```python
with Resource():

    raise ValueError("Invalid Input")
```

Python automatically calls:

```python
resource.__exit__(
    ValueError,
    ValueError("Invalid Input"),
    traceback
)
```

The exception information is passed into `__exit__()`.

---

# Example 1 - Inspecting Exceptions

```python
class Resource:

    def __enter__(self):

        print("Opening Resource")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Closing Resource")

        print(exc_type)

        print(exc_value)
```

Usage

```python
with Resource():

    raise ValueError("Invalid Age")
```

Output

```
Opening Resource

Closing Resource

<class 'ValueError'>

Invalid Age

Traceback...
```

The exception still propagates after `__exit__()` finishes.

---

# Suppressing Exceptions

Normally,

exceptions continue after `__exit__()`.

But there's a special feature.

If `__exit__()` returns:

```python
True
```

Python treats the exception as handled.

Example

```python
class Resource:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        print("Handled Exception")

        return True
```

Usage

```python
with Resource():

    raise ValueError("Something went wrong")

print("Program Continues")
```

Output

```
Handled Exception

Program Continues
```

No exception reaches the caller.

---

# When Should You Suppress Exceptions?

Only suppress an exception if you have genuinely handled it.

Good examples:

- Logging and ignoring optional cleanup failures
- Retrying temporary operations
- Gracefully shutting down resources

Avoid suppressing exceptions simply to prevent a program from crashing.

Hidden errors are difficult to debug.

---

# Multiple Context Managers

Instead of writing:

```python
with open("users.txt") as users:

    with open("orders.txt") as orders:

        print(users.read())

        print(orders.read())
```

You can write:

```python
with open("users.txt") as users, \
     open("orders.txt") as orders:

    print(users.read())

    print(orders.read())
```

Python opens them from left to right.

Cleanup happens in reverse order.

Visualization

```
Open File A

↓

Open File B

↓

Work

↓

Close File B

↓

Close File A
```

This is similar to the order in which function calls are unwound from the call stack.

---

# Nested Context Managers

You can also nest them.

```python
with Database():

    with Transaction():

        print("Updating User")
```

Execution order

```
Database.__enter__()

↓

Transaction.__enter__()

↓

Business Logic

↓

Transaction.__exit__()

↓

Database.__exit__()
```

Each context manager is responsible only for its own resource.

---

# Creating Context Managers with contextlib

Writing a class for every context manager can be unnecessary.

Python provides:

```python
from contextlib import contextmanager
```

This decorator converts a generator into a context manager.

---

# Example 2

```python
from contextlib import contextmanager


@contextmanager
def database():

    print("Connecting")

    yield

    print("Disconnecting")
```

Usage

```python
with database():

    print("Running Query")
```

Output

```
Connecting

Running Query

Disconnecting
```

Only a few lines of code are needed.

---

# How Does It Work?

The generator pauses at:

```python
yield
```

Everything before `yield` behaves like:

```python
__enter__()
```

Everything after `yield` behaves like:

```python
__exit__()
```

Visualization

```
Before yield

↓

Enter Context

↓

yield

↓

Your Code

↓

Resume After yield

↓

Exit Context
```

---

# Handling Exceptions with contextmanager

```python
from contextlib import contextmanager


@contextmanager
def database():

    print("Connecting")

    try:

        yield

    finally:

        print("Disconnecting")
```

Now cleanup happens even if an exception occurs.

```python
with database():

    raise RuntimeError("Database Error")
```

Output

```
Connecting

Disconnecting

RuntimeError...
```

This pattern is very common in production code.

---

# Real-World Example - Database Transaction

Imagine a banking system.

Transfer money.

```
Withdraw Money

↓

Deposit Money

↓

Commit Transaction
```

If depositing fails,

the withdrawal should also be undone.

A simplified context manager might look like this:

```python
class Transaction:

    def __enter__(self):

        print("Transaction Started")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type:

            print("Rollback Transaction")

        else:

            print("Commit Transaction")
```

Usage

```python
with Transaction():

    print("Transfer Money")
```

Successful Output

```
Transaction Started

Transfer Money

Commit Transaction
```

If an exception occurs

```
Transaction Started

Transfer Money

Rollback Transaction
```

This is conceptually how many ORM libraries such as SQLAlchemy manage transactions.

---

# Production Insight

Context managers are widely used throughout backend systems.

Examples include:

Database sessions

```python
with Session() as session:
    ...
```

Database transactions

```python
with session.begin():
    ...
```

File uploads

```python
with open(file_path, "wb") as file:
    ...
```

Locks

```python
with lock:
    ...
```

HTTP sessions

```python
with requests.Session() as session:
    ...
```

The biggest benefit is reliability.

Developers don't need to remember to release resources manually.

Python guarantees cleanup.

---

# Questions

### Question

> What happens if `__exit__()` returns `True`?

### Answer

Returning `True` tells Python that the exception has been handled. The exception is suppressed and does not propagate outside the `with` block.

---

### Question

> What is the purpose of `contextlib.contextmanager`?

### Answer

It allows a generator function to be used as a context manager. Code before `yield` acts like `__enter__()`, while code after `yield` acts like `__exit__()`.

---

### Question

> Why are context managers commonly used for database transactions?

### Answer

They guarantee that transactions are either committed when operations succeed or rolled back if an exception occurs, ensuring data consistency.

---

# Practical Lesson

Create a file:

```
transaction.py
```

```python
class Transaction:

    def __enter__(self):

        print("Transaction Started")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type:

            print("Rollback")

        else:

            print("Commit")
```

Test a successful transaction.

```python
with Transaction():

    print("Updating User")
```

Now test a failed transaction.

```python
with Transaction():

    print("Updating User")

    raise ValueError("Invalid Data")
```

Observe the difference between **Commit** and **Rollback**.

---

# Questions

## Question 1

What information is passed to `__exit__()` when an exception occurs?

### Answer

Python passes the exception type, exception instance and traceback object. These allow the context manager to inspect or handle the exception.

---

## Question 2

What happens when `__exit__()` returns `True`?

### Answer

Python suppresses the exception, treating it as handled, and execution continues after the `with` block.

---

## Question 3

Why is `contextlib.contextmanager` useful?

### Answer

It simplifies creating context managers by allowing a generator function with a single `yield` to replace a full class implementing `__enter__()` and `__exit__()`.

---

## Question 4

In what order are multiple context managers cleaned up?

### Answer

They are cleaned up in reverse order of acquisition. The last resource acquired is the first one released.

---

## Question 5

Why are context managers important in production applications?

### Answer

They ensure reliable resource management, prevent leaks, simplify cleanup logic and make code easier to read and maintain.

---

# Assignment

## Exercise 1

Create a context manager that logs:

```
Starting Task
```

before a block executes and:

```
Task Finished
```

after it completes.

Implement it using `contextlib.contextmanager`.

---

## Exercise 2

Create a class-based context manager that simulates a database transaction.

Print:

- `Commit` if the block succeeds.
- `Rollback` if an exception occurs.

---

## Exercise 3

Open two files using a single `with` statement.

Read data from both and explain why Python closes them in reverse order.

---

# Summary

In this lesson, you learned:

- ✅ How `__exit__()` receives exception information.
- ✅ How exceptions can be suppressed by returning `True`.
- ✅ How to create generator-based context managers using `contextlib.contextmanager`.
- ✅ How nested and multiple context managers work.
- ✅ How context managers are used for database transactions.
- ✅ Why context managers are essential for writing reliable backend applications.

---

# What's Next

**File:**
[10-Magic-Methods-part-1](10-magic-methods-part-1.md)
