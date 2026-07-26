# File: python/python-advanced-05-decorators-part-1.md

# Python Advanced - Lesson 05 (Part 1)
# Decorators - Why They Exist & How They Work

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 05 (Part 1)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why decorators exist
- What problem decorators solve
- How function wrapping works
- How to write your first decorator
- Why `*args` and `**kwargs` are required
- How decorators preserve function behaviour
- Why frameworks like FastAPI and Flask use decorators everywhere

---

# Prerequisites

Before learning decorators, you should already understand:

- ✅ First-class functions
- ✅ Higher-order functions
- ✅ Closures
- ✅ `*args` and `**kwargs` (basic understanding)

Decorators combine all of these concepts into one powerful feature.

---

# Theory

Imagine you have three API functions.

```python
def create_user():
    print("Creating User...")


def update_user():
    print("Updating User...")


def delete_user():
    print("Deleting User...")
```

Now your manager says:

> "Before every function runs, print `Starting...`"

You modify every function.

```python
def create_user():
    print("Starting...")
    print("Creating User...")


def update_user():
    print("Starting...")
    print("Updating User...")


def delete_user():
    print("Starting...")
    print("Deleting User...")
```

A week later...

Your manager says:

> "Also print `Finished.` after every function."

Now every function becomes:

```python
def create_user():
    print("Starting...")
    print("Creating User...")
    print("Finished.")


def update_user():
    print("Starting...")
    print("Updating User...")
    print("Finished.")


def delete_user():
    print("Starting...")
    print("Deleting User...")
    print("Finished.")
```

Notice the problem.

The business logic is becoming mixed with:

- Logging
- Authentication
- Timing
- Error handling
- Metrics

This violates the **Single Responsibility Principle (SRP)**.

Decorators solve this problem.

---

# What is a Decorator?

A decorator is simply:

> **A function that takes another function, adds extra behaviour, and returns a new function.**

Visualization

```
Original Function

        │
        ▼

Decorator

        │
        ▼

New Function

(with additional behaviour)
```

The original function remains focused on its job.

The decorator adds extra behaviour around it.

---

# Function Wrapping

Let's build a decorator manually.

```python
def greet():

    print("Hello!")
```

Now create a wrapper.

```python
def wrapper():

    print("Starting...")

    greet()

    print("Finished.")
```

Run it.

```python
wrapper()
```

Output

```
Starting...

Hello!

Finished.
```

It works.

But there's a problem.

The wrapper only works for `greet()`.

It isn't reusable.

---

# Writing Your First Decorator

Let's make the wrapper generic.

```python
def logger(function):

    def wrapper():

        print("Starting...")

        function()

        print("Finished.")

    return wrapper
```

Now create a function.

```python
def greet():

    print("Hello!")
```

Wrap it.

```python
decorated_function = logger(greet)

decorated_function()
```

Output

```
Starting...

Hello!

Finished.
```

Visualization

```
greet

        │
        ▼

logger()

        │
        ▼

wrapper()

        │
        ▼

Starting...

Hello!

Finished.
```

This is the core idea behind every decorator in Python.

---

# The @ Syntax

The previous example works, but writing:

```python
decorated_function = logger(greet)
```

every time is inconvenient.

Python provides a shortcut.

Instead of:

```python
def greet():
    print("Hello!")

greet = logger(greet)
```

You can write:

```python
@logger
def greet():
    print("Hello!")
```

These two approaches are **exactly the same**.

Python automatically converts:

```python
@logger
def greet():
    ...
```

into:

```python
def greet():
    ...

greet = logger(greet)
```

This is one of the most common Python interview questions.

---

# Why Do We Need *args and **kwargs?

Let's modify our function.

```python
def greet(name):

    print(f"Hello {name}")
```

Now use our decorator.

```python
@logger
def greet(name):

    print(f"Hello {name}")

greet("Alice")
```

Output

```
TypeError
```

Why?

Because our wrapper accepts **no parameters**.

```python
def wrapper():
```

But `greet()` expects one.

---

# The Solution

Use `*args` and `**kwargs`.

```python
def logger(function):

    def wrapper(*args, **kwargs):

        print("Starting...")

        function(*args, **kwargs)

        print("Finished.")

    return wrapper
```

Now:

```python
@logger
def greet(name):

    print(f"Hello {name}")

greet("Alice")
```

Output

```
Starting...

Hello Alice

Finished.
```

Now the decorator works for **any function signature**.

---

# Multiple Arguments

```python
@logger
def add(a, b):

    print(a + b)


add(10, 20)
```

Output

```
Starting...

30

Finished.
```

No changes to the decorator were needed.

`*args` collects positional arguments.

`**kwargs` collects keyword arguments.

---

# Returning Values

Consider this function.

```python
def add(a, b):

    return a + b
```

Decorate it.

```python
@logger
def add(a, b):

    return a + b
```

Now:

```python
result = add(10, 20)

print(result)
```

Output

```
Starting...

Finished.

None
```

Where did `30` go?

---

# Why?

Our wrapper never returned it.

```python
function(*args, **kwargs)
```

The return value was ignored.

---

# Correct Decorator

```python
def logger(function):

    def wrapper(*args, **kwargs):

        print("Starting...")

        result = function(*args, **kwargs)

        print("Finished.")

        return result

    return wrapper
```

Now:

```python
@logger
def add(a, b):

    return a + b

print(add(10, 20))
```

Output

```
Starting...

Finished.

30
```

Always return the wrapped function's result unless you intentionally want to change it.

---

# Production Insight

Suppose every API request should be logged.

Without decorators:

```python
def get_users():

    print("Request Started")

    print("Fetching Users")

    print("Request Finished")


def get_orders():

    print("Request Started")

    print("Fetching Orders")

    print("Request Finished")
```

The logging code is duplicated.

Instead:

```python
@logger
def get_users():

    print("Fetching Users")


@logger
def get_orders():

    print("Fetching Orders")
```

Now logging is written once and reused everywhere.

This is exactly how frameworks implement:

- Authentication
- Logging
- Performance monitoring
- Permission checks
- Exception handling
- Transaction management

---

# FastAPI Example

When you write:

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

`@app.get("/users")` is a decorator.

Conceptually, it does something similar to:

```python
app.get("/users")(get_users)
```

The decorator registers the function with the framework.

Later, when a request arrives for `/users`, FastAPI knows which function to execute.

The same pattern is used in Flask:

```python
@app.route("/users")
def get_users():
    ...
```

---

# Interview Deep Dive

### Interviewer

> What is a decorator?

### Weak Answer

> A decorator adds functionality to a function.

This is correct but incomplete.

---

### Strong Answer

> A decorator is a higher-order function that accepts another function, wraps it with additional behaviour, and returns a new function. It allows cross-cutting concerns such as logging, authentication, caching and timing to be added without modifying the original business logic.

---

### Interviewer

> What does the `@` symbol do?

### Weak Answer

> It calls the decorator.

---

### Strong Answer

> The `@decorator` syntax is syntactic sugar. Python automatically rewrites:

```python
@decorator
def func():
    ...
```

as:

```python
def func():
    ...

func = decorator(func)
```

---

### Interviewer

> Why do decorators usually use `*args` and `**kwargs`?

### Weak Answer

> To accept arguments.

---

### Strong Answer

> Decorators should work with functions that have different parameter lists. Using `*args` and `**kwargs` allows the wrapper to forward any positional and keyword arguments to the original function without knowing its signature in advance.

---

# Practical Lesson

Create a file:

```
logger_decorator.py
```

Write the following program.

```python
def logger(function):
    """
    A reusable decorator that logs
    before and after a function executes.
    """

    def wrapper(*args, **kwargs):

        print("=== Starting ===")

        result = function(*args, **kwargs)

        print("=== Finished ===")

        return result

    return wrapper


@logger
def multiply(a, b):
    return a * b


@logger
def welcome(name):
    print(f"Welcome {name}!")


print(multiply(5, 4))

welcome("Alice")
```

Expected Output

```
=== Starting ===

=== Finished ===

20

=== Starting ===

Welcome Alice!

=== Finished ===
```

---

# Interview Questions

## Question 1

What is a decorator?

### Answer

A decorator is a function that accepts another function, adds extra behaviour before or after it executes, and returns a new wrapped function.

---

## Question 2

Why are decorators useful?

### Answer

They allow common functionality such as logging, authentication, caching and validation to be written once and reused across many functions without modifying the business logic.

---

## Question 3

What does `@logger` mean?

### Answer

It is shorthand for:

```python
function = logger(function)
```

Python automatically performs this assignment when the function is defined.

---

## Question 4

Why do decorators usually use `*args` and `**kwargs`?

### Answer

To make the decorator reusable for functions with different parameter lists.

---

## Question 5

Why should a decorator return the wrapped function's result?

### Answer

If the wrapper doesn't return the result, the decorated function returns `None` by default, causing the original return value to be lost.

---

# Assignment

## Exercise 1

Create a decorator that prints:

```
Function Started
```

before execution and:

```
Function Ended
```

after execution.

---

## Exercise 2

Decorate three different functions:

- Addition
- Multiplication
- Greeting

Verify that the same decorator works for all of them.

---

## Exercise 3

Write a decorator that counts how many times a function has been called.

Example:

```
Hello

Called 1 time(s)

Hello

Called 2 time(s)

Hello

Called 3 time(s)
```

(Hint: You'll use a **closure** and `nonlocal`.)

---

# Summary

In this lesson, you learned:

- ✅ Why decorators exist.
- ✅ How decorators solve code duplication.
- ✅ How function wrapping works.
- ✅ How to write your first decorator.
- ✅ Why `*args` and `**kwargs` are essential.
- ✅ Why returning the original result matters.
- ✅ How frameworks like FastAPI and Flask use decorators.

---

# What's Next

**File:**

`python/python-advanced-05-decorators-part-2.md`

Topics:

- Decorators with Arguments
- Stacking Multiple Decorators
- `functools.wraps`
- Timing Decorator
- Authentication Decorator
- Caching Decorator
- Real FastAPI/Flask Examples
- Interview Questions
