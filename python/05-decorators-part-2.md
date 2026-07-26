# File: python/python-advanced-05-decorators-part-2.md

# Python Advanced - Lesson 05 (Part 2)
# Advanced Decorators

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Advanced
>
> **Lesson:** 05 (Part 2)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 75 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Decorators with arguments
- Stacking multiple decorators
- Why `functools.wraps` is important
- How to build timing decorators
- How to build authentication decorators
- How to build caching decorators
- How decorators are used in FastAPI and Flask

---

# Theory

In the previous lesson, we built a simple decorator.

```python
@logger
def greet():
    print("Hello")
```

Now let's make decorators much more powerful.

---

# Decorators with Arguments

Suppose you want a logger that prints different messages.

Instead of:

```python
@logger
def create_user():
    ...
```

You want:

```python
@logger("USER SERVICE")
def create_user():
    ...
```

To achieve this, we need **one extra level of nesting**.

---

# Example 1

```python
def logger(service_name):
    """
    Receives the decorator argument.
    """

    def decorator(function):
        """
        Receives the original function.
        """

        def wrapper(*args, **kwargs):

            print(f"[{service_name}] Starting")

            result = function(*args, **kwargs)

            print(f"[{service_name}] Finished")

            return result

        return wrapper

    return decorator
```

Usage

```python
@logger("USER SERVICE")
def create_user():

    print("Creating user...")
```

Run

```python
create_user()
```

Output

```
[USER SERVICE] Starting

Creating user...

[USER SERVICE] Finished
```

---

# Understanding the Flow

When Python sees

```python
@logger("USER SERVICE")
def create_user():
    ...
```

It performs these steps:

```
logger("USER SERVICE")

↓

returns decorator

↓

decorator(create_user)

↓

returns wrapper

↓

create_user = wrapper
```

There are now **three functions** involved:

- `logger`
- `decorator`
- `wrapper`

---

# Stacking Decorators

A function can have multiple decorators.

Example

```python
@logger
@timer
def process():
    print("Processing...")
```

Python executes them from bottom to top.

Equivalent code:

```python
process = logger(timer(process))
```

Visualization

```
process()

↓

timer()

↓

logger()

↓

Actual Function
```

The decorator closest to the function executes first.

---

# Example 2

```python
def first(function):

    def wrapper():

        print("First")

        function()

    return wrapper


def second(function):

    def wrapper():

        print("Second")

        function()

    return wrapper


@first
@second
def greet():

    print("Hello")


greet()
```

Output

```
First

Second

Hello
```

---

# The Problem with Simple Decorators

Let's inspect a decorated function.

```python
def logger(function):

    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@logger
def greet():
    """Greets the user."""
    print("Hello")


print(greet.__name__)

print(greet.__doc__)
```

Output

```
wrapper

None
```

Oops!

We lost the original function's metadata.

---

# functools.wraps

Python provides a solution.

```python
from functools import wraps
```

---

# Example 3

```python
from functools import wraps


def logger(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        return function(*args, **kwargs)

    return wrapper


@logger
def greet():
    """Greets the user."""
    print("Hello")


print(greet.__name__)

print(greet.__doc__)
```

Output

```
greet

Greets the user.
```

Always use `@wraps` in production decorators.

---

# Timing Decorator

A common production use case is measuring execution time.

```python
import time
from functools import wraps


def timer(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = function(*args, **kwargs)

        end = time.perf_counter()

        print(f"Execution Time: {end - start:.6f} seconds")

        return result

    return wrapper
```

Usage

```python
@timer
def calculate():

    total = 0

    for i in range(1_000_000):
        total += i

    return total


calculate()
```

---

# Authentication Decorator

Imagine every API requires authentication.

Instead of writing

```python
if not authenticated:
    ...
```

inside every endpoint,

use a decorator.

```python
from functools import wraps

logged_in = True


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not logged_in:
            raise PermissionError("Login Required")

        return function(*args, **kwargs)

    return wrapper
```

Usage

```python
@login_required
def dashboard():

    print("Dashboard Loaded")


dashboard()
```

Output

```
Dashboard Loaded
```

---

# Caching Decorator

Suppose a function performs an expensive calculation.

```python
from functools import wraps


def cache(function):

    saved_results = {}

    @wraps(function)
    def wrapper(number):

        if number in saved_results:

            print("Using Cache")

            return saved_results[number]

        result = function(number)

        saved_results[number] = result

        return result

    return wrapper
```

Usage

```python
@cache
def square(number):

    print("Calculating...")

    return number * number


print(square(5))

print(square(5))
```

Output

```
Calculating...

25

Using Cache

25
```

Notice that the second call never recalculates the value.

---

# Production Insight

Decorators are everywhere in backend development.

FastAPI

```python
@app.get("/users")
```

Registers an API endpoint.

Flask

```python
@app.route("/users")
```

Registers a route.

Pytest

```python
@pytest.fixture
```

Registers a fixture.

Even Python's standard library uses decorators:

```python
@property

@classmethod

@staticmethod
```

Understanding decorators means understanding how many Python frameworks work internally.

---

# Interview Deep Dive

### Interviewer

> Why should you use `functools.wraps`?

### Answer

`functools.wraps` preserves the original function's metadata, such as its name, documentation string and annotations. Without it, the decorated function appears to be the wrapper function, which makes debugging, introspection and documentation generation more difficult.

---

### Interviewer

> In what order are multiple decorators applied?

### Answer

Decorators are applied from the bottom up. For:

```python
@A
@B
def func():
    ...
```

Python evaluates it as:

```python
func = A(B(func))
```

The decorator closest to the function is applied first.

---

### Interviewer

> Why are decorators widely used in web frameworks?

### Answer

Decorators separate cross-cutting concerns such as routing, authentication, validation, caching and logging from business logic. This keeps endpoint functions clean, reusable and easier to maintain.

---

# Practical Lesson

Create a file:

```
timer_decorator.py
```

```python
import time
from functools import wraps


def timer(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = function(*args, **kwargs)

        end = time.perf_counter()

        print(f"Execution Time: {end - start:.6f} seconds")

        return result

    return wrapper


@timer
def slow_task():

    """
    Simulate a slow operation.
    """

    time.sleep(2)

    print("Task Finished")


slow_task()
```

Expected Output

```
Task Finished

Execution Time: 2.00xxxx seconds
```

---

# Interview Questions

## Question 1

Why do decorator factories require three nested functions?

### Answer

The outer function receives the decorator's arguments, the middle function receives the original function, and the innermost wrapper executes the function while adding extra behaviour.

---

## Question 2

Why should decorators use `@wraps`?

### Answer

To preserve the original function's metadata, making debugging, documentation and framework integration work correctly.

---

## Question 3

How are multiple decorators executed?

### Answer

They are applied from the bottom up. The decorator closest to the function wraps it first.

---

## Question 4

Name three real-world uses of decorators.

### Answer

- Authentication
- Logging
- Performance monitoring

Other common uses include caching, routing, transactions and validation.

---

## Question 5

What problem do decorators solve?

### Answer

They eliminate duplicated code by separating reusable behaviour from business logic, making applications cleaner and easier to maintain.

---

# Assignment

## Exercise 1

Create a decorator that measures how long a function takes to execute.

---

## Exercise 2

Create a decorator that prints the function name before executing it.

Example:

```
Running function: calculate_salary
```

(Hint: Use `function.__name__`.)

---

## Exercise 3

Create a decorator factory:

```python
@repeat(3)
```

that executes a function three times.

Example:

```python
@repeat(3)
def hello():
    print("Hello")
```

Output

```
Hello
Hello
Hello
```

---

# Summary

In this lesson, you learned:

- ✅ How decorator factories work.
- ✅ How to pass arguments to decorators.
- ✅ How multiple decorators are stacked.
- ✅ Why `functools.wraps` is essential.
- ✅ How timing, authentication and caching decorators are implemented.
- ✅ Why decorators are fundamental to modern Python web frameworks.

---

# What's Next

**File:**

`python/python-advanced-06-iterators-and-iterables-part-1.md`

Topics:

- Iterable vs Iterator
- Iterator Protocol
- `iter()`
- `next()`
- Why `for` loops work
- Building a Custom Iterator
- Production Examples
- Interview Questions
