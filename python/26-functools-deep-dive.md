# File: python/26-functools-deep-dive.md

# Python Functional Programming - Part 4
# Deep Dive into the `functools` Module

> **Course:** Backend Engineering Roadmap
>
> **Module:** Functional Python
>
> **Lesson:** 4
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 160 Minutes

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `functools` module | Python 2.5 |
| `functools.partial()` | Python 2.5 |
| `functools.wraps()` | Python 2.5 |
| `functools.lru_cache()` | Python 3.2 |
| `typed` parameter for `lru_cache()` | Python 3.3 |
| `user_function` parameter for `lru_cache()` | Python 3.8 |
| `functools.cached_property` | Python 3.8 |
| `functools.singledispatch()` | Python 3.4 |
| `functools.total_ordering()` | Python 2.7 |

### Important Python Version Notes

- `cached_property` is only available from **Python 3.8**.
- `lru_cache()` is widely used in modern backend applications for memoisation.
- `singledispatch()` enables a form of function overloading based on argument types.
- Most production projects running Python 3.10+ use these utilities extensively.

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why `functools` exists
- Function metadata
- `functools.wraps()`
- `functools.partial()`
- Memoisation
- `functools.lru_cache()`
- `functools.cached_property`
- `functools.singledispatch`
- `functools.total_ordering`
- Production use cases
- Performance considerations

---

# Recap

So far we've learned

- Functional Programming
- Pure Functions
- map()
- filter()
- reduce()
- Comprehensions
- zip()
- enumerate()
- any()
- all()

Today we'll study one of Python's most important standard library modules.

```
functools
```

Many popular frameworks rely on it internally.

---

# Why Does functools Exist?

As Python grew,

developers repeatedly solved the same problems:

- Function caching
- Function wrapping
- Partial application
- Generic functions
- Comparison methods

The standard library collected these utilities into one module.

```
functools
```

---

# Overview

The most commonly used tools are

```
functools

│

├── wraps()

├── partial()

├── lru_cache()

├── cached_property

├── singledispatch()

└── total_ordering()
```

We'll study each one.

---

# Part 1 — functools.wraps()

---

# The Problem

Earlier we created decorators.

```python
def logger(func):

    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper
```

Looks fine.

Let's inspect the function.

```python
@logger
def calculate():

    pass

print(calculate.__name__)
```

Output

```
wrapper
```

Problem.

The original function name has disappeared.

---

# Why Does This Matter?

Many frameworks inspect functions.

Examples

- FastAPI
- Flask
- Django
- Click
- pytest

If metadata disappears,

frameworks may behave incorrectly.

---

# Enter wraps()

```python
from functools import wraps


def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper
```

Now

```python
print(calculate.__name__)
```

Output

```
calculate
```

---

# What Does wraps() Copy?

It preserves

- `__name__`
- `__doc__`
- `__module__`
- annotations
- other metadata

Always use it when writing decorators.

---

# Production Example

FastAPI uses function metadata to generate API documentation.

Without `@wraps`

```python
GET /users
```

may appear with incorrect metadata.

---

# Part 2 — functools.partial()

---

# The Problem

Suppose we repeatedly call

```python
def power(base, exponent):

    return base ** exponent
```

We often calculate squares.

```python
power(5, 2)

power(7, 2)

power(9, 2)
```

The exponent never changes.

---

# partial()

```python
from functools import partial


square = partial(

    power,

    exponent=2

)

print(square(5))
```

Output

```
25
```

Internally

```
square(5)

↓

power(5, 2)
```

---

# Another Example

```python
cube = partial(

    power,

    exponent=3

)

print(cube(4))
```

Output

```
64
```

---

# Visualising partial()

```
Original

power(base, exponent)

↓

Fix exponent = 2

↓

New Function

square(base)
```

---

# Production Example

Suppose every API request uses the same timeout.

```python
import requests

api_get = partial(

    requests.get,

    timeout=5

)
```

Now

```python
api_get(url)
```

always uses

```
timeout=5
```

> **Note:** We'll cover the `requests` library later in the course. This example illustrates the concept of partially applying keyword arguments.

---

# Part 3 — Memoisation

Before learning

```
lru_cache()
```

we need memoisation.

Memoisation means

```
Remember previous results.
```

Instead of

```
Compute

↓

Forget
```

we do

```
Compute

↓

Store

↓

Reuse
```

---

# Expensive Function

```python
def fibonacci(n):

    if n < 2:

        return n

    return (

        fibonacci(n - 1)

        +

        fibonacci(n - 2)

    )
```

For

```python
fibonacci(40)
```

Python performs millions of repeated calculations.

---

# lru_cache()

```python
from functools import lru_cache


@lru_cache
def fibonacci(n):

    if n < 2:

        return n

    return (

        fibonacci(n - 1)

        +

        fibonacci(n - 2)

    )
```

The code barely changes,

but performance improves dramatically.

---

# Why?

Without cache

```
fib(5)

↓

fib(4)

↓

fib(3)

↓

fib(2)

↓

fib(1)
```

Many branches repeat.

With cache

```
fib(3)

↓

Store

↓

Reuse later
```

Every input is calculated only once.

---

# Cache Statistics

```python
print(

    fibonacci.cache_info()

)
```

Example Output

```
CacheInfo(

    hits=38,

    misses=41,

    maxsize=128,

    currsize=41

)
```

Useful for debugging.

---

# Clearing the Cache

```python
fibonacci.cache_clear()
```

Removes all cached values.

---

# maxsize

Default

```
128
```

Custom

```python
@lru_cache(

    maxsize=512

)
```

Unlimited

```python
@lru_cache(

    maxsize=None

)
```

Use unlimited caching carefully,

as memory usage can grow without bound.

---

# Important Restriction

Arguments must be hashable.

Works

```python
calculate(10)
```

Fails

```python
calculate([])

calculate({})
```

Lists and dictionaries cannot be used as cache keys.

---

# Production Example

Caching

- Currency exchange rates
- Configuration files
- Feature flags
- Expensive calculations
- Regular expression compilation
- Parsed schemas

Never cache rapidly changing database queries unless stale data is acceptable.

---

# Part 4 — cached_property

---

# The Problem

Suppose

```python
class User:

    @property
    def permissions(self):

        ...
```

Every access recalculates permissions.

If calculation is expensive,

this wastes CPU time.

---

# cached_property

```python
from functools import cached_property


class User:

    @cached_property
    def permissions(self):

        print("Loading...")

        return [

            "admin",

            "editor"

        ]
```

Usage

```python
user = User()

print(user.permissions)

print(user.permissions)
```

Output

```
Loading...

['admin', 'editor']

['admin', 'editor']
```

Notice

The calculation runs only once.

---

# How Does It Work?

First access

```
Call Function

↓

Store Result

↓

Return
```

Later accesses

```
Return Stored Value
```

No recalculation.

---

# Production Example

Cache

- Parsed JWT claims
- User permissions
- Expensive database metadata
- Configuration parsing

---

# cached_property vs property

| `property` | `cached_property` |
|------------|------------------|
| Executes every access | Executes once |
| No caching | Stores result |
| Lower memory | Higher memory |

---

# Part 5 — singledispatch()

---

# The Problem

Python doesn't support traditional function overloading.

This doesn't work.

```python
def print_value(value):

    ...


def print_value(

    value,

    extra

):

    ...
```

The second definition replaces the first.

---

# singledispatch()

```python
from functools import singledispatch


@singledispatch
def describe(value):

    print("Unknown")
```

Register another implementation.

```python
@describe.register(int)
def _(value):

    print("Integer")
```

Another.

```python
@describe.register(str)
def _(value):

    print("String")
```

Usage

```python
describe(10)

describe("Hello")
```

Output

```
Integer

String
```

---

# Why Is This Useful?

Instead of

```python
if isinstance(...)

elif isinstance(...)

elif ...
```

dispatch happens automatically.

---

# Production Example

Serialising different object types.

```python
serialize(user)

serialize(order)

serialize(product)
```

Each type gets its own implementation.

---

# Part 6 — total_ordering()

---

# The Problem

Suppose

```python
class Product:
```

needs

```
<

<=

>

>=

==
```

Implementing every comparison becomes repetitive.

---

# total_ordering()

```python
from functools import total_ordering


@total_ordering
class Product:

    def __init__(

        self,

        price

    ):

        self.price = price

    def __eq__(

        self,

        other

    ):

        return self.price == other.price

    def __lt__(

        self,

        other

    ):

        return self.price < other.price
```

Python automatically creates

```
<=

>

>=
```

Only

```
__eq__

__lt__
```

were required.

---

# How Does It Work?

You provide

```
==

+

<
```

Python derives

```
>

<=

>=

!=
```

This reduces boilerplate.

---

# Performance Consideration

`@total_ordering` trades a tiny amount of runtime performance for cleaner code.

In most applications,

the difference is negligible.

For extremely performance-critical classes,

implement every comparison method manually.

---

# Common Mistakes

## Mistake 1

Forgetting `@wraps` inside decorators.

Frameworks may lose important metadata.

---

## Mistake 2

Using unlimited caches

```python
maxsize=None
```

without considering memory usage.

---

## Mistake 3

Caching mutable or frequently changing data.

Old values may become stale.

---

## Mistake 4

Using `cached_property` for values that should change over the lifetime of an object.

---

## Mistake 5

Using `singledispatch` when simple polymorphism or class methods would be clearer.

---

# Best Practices

✅ Always use `@wraps` in decorators.

✅ Profile before introducing caching.

✅ Cache only deterministic (pure) functions.

✅ Choose a sensible `maxsize` for `lru_cache()`.

✅ Use `cached_property` only for expensive computations that rarely change.

❌ Don't cache database queries without an invalidation strategy.

❌ Don't use `partial()` when a small wrapper function would be clearer.

---

# Production Insight

The most commonly used `functools` features in backend engineering are:

1. **`@wraps`** — Essential whenever writing decorators. You'll see it in authentication, logging, tracing and retry decorators.

2. **`@lru_cache`** — Frequently used to cache expensive computations or configuration loading.

3. **`cached_property`** — Common in ORMs and API clients for lazily computing expensive object attributes.

`partial()`, `singledispatch()` and `total_ordering()` are valuable tools, but they appear less frequently in everyday backend code than the three features above.

---

# Questions

### Question

> Why should you always use `functools.wraps()`?

### Answer

It preserves the original function's metadata, including its name, documentation and annotations, which many frameworks rely on.

---

### Question

> What problem does `lru_cache()` solve?

### Answer

It avoids repeated computation by caching function results for previously seen arguments.

---

### Question

> What is memoisation?

### Answer

Memoisation is the technique of storing the results of expensive function calls so they can be reused for identical inputs.

---

### Question

> When should you use `cached_property`?

### Answer

When an object's property is expensive to compute but unlikely to change during the object's lifetime.

---

### Question

> What is `singledispatch()`?

### Answer

It allows different implementations of a function to be selected automatically based on the type of the first argument.

---

# Practical Lesson

Create a file:

```
functools_examples.py
```

```python
from functools import (
    wraps,
    partial,
    lru_cache,
    cached_property,
)


# wraps
def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print("Calling function...")

        return func(*args, **kwargs)

    return wrapper


@logger
def greet(name):

    return f"Hello, {name}"


print(greet.__name__)


# partial
def multiply(a, b):

    return a * b


double = partial(multiply, b=2)

print(double(10))


# lru_cache
@lru_cache(maxsize=64)
def factorial(n):

    if n <= 1:

        return 1

    return n * factorial(n - 1)


print(factorial(10))
print(factorial.cache_info())


# cached_property
class Configuration:

    @cached_property
    def settings(self):

        print("Loading configuration...")

        return {"debug": False}


config = Configuration()

print(config.settings)
print(config.settings)
```

Expected Output

```
greet

20

3628800

CacheInfo(...)

Loading configuration...

{'debug': False}

{'debug': False}
```

Notice that **"Loading configuration..."** is printed only once.

---

# Questions

## Question 1

Why is `@wraps` important?

### Answer

It preserves the original function's metadata after decoration.

---

## Question 2

When is `lru_cache()` most effective?

### Answer

For deterministic functions that are expensive to compute and are called repeatedly with the same arguments.

---

## Question 3

Why can't `lru_cache()` cache functions that receive lists?

### Answer

Because lists are mutable and unhashable, so they cannot be used as dictionary keys for the cache.

---

## Question 4

What is the advantage of `cached_property` over `property`?

### Answer

It computes the value only once and reuses the cached result for subsequent accesses.

---

## Question 5

What problem does `partial()` solve?

### Answer

It creates a new callable with some arguments already fixed, reducing repeated code.

---

# Assignment

## Exercise 1

Create a decorator that logs a function's execution time using `time.perf_counter()`. Ensure you preserve the original function's metadata with `@wraps`.

---

## Exercise 2

Write a recursive function to calculate Fibonacci numbers.

- Measure its execution time.
- Add `@lru_cache`.
- Measure the execution time again.
- Compare the results.

---

## Exercise 3

Create a `DatabaseConfig` class with a `cached_property` that simulates loading configuration from a file. Verify that the configuration is loaded only once.

---

## Exercise 4

Create a `@singledispatch` function called `to_json()` that behaves differently for:

- `dict`
- `list`
- `str`
- `int`

Explain why this approach is preferable to a long chain of `isinstance()` checks.

---

# Summary

In this lesson, you learned:

- ✅ Why the `functools` module exists.
- ✅ How `@wraps` preserves function metadata.
- ✅ How `partial()` creates specialised functions.
- ✅ How `lru_cache()` implements memoisation.
- ✅ When to use `cached_property`.
- ✅ How `singledispatch()` provides type-based dispatch.
- ✅ How `total_ordering()` reduces boilerplate.
- ✅ Which `functools` features are most valuable in production backend applications.

---

# What's Next

**File:**
[27-Itertools-part-1](27-itertools-part-1.md)

Topics:

- Introduction to `itertools`
- Why Iterators Matter
- Infinite Iterators (`count`, `cycle`, `repeat`)
- Finite Iterators (`chain`, `islice`)
- Lazy Evaluation
- Memory Optimisation
- Production Examples
- Performance Benchmarks

> **Why next?**
>
> The `itertools` module is one of Python's most powerful standard library modules. It provides highly optimised, lazy iterator building blocks that are extensively used in data pipelines, ETL jobs, streaming systems and high-performance backend applications.
