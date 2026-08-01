# File: python/39-collections-module-part-2.md

# Python Standard Library

# Collections Module - Part 2: `namedtuple`, `OrderedDict`, `ChainMap`, `UserDict`, `UserList` & `UserString`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Standard Library
>
> **Lesson:** 39
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 5 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `namedtuple` | Python 2.6 |
| `OrderedDict` | Python 2.7 |
| `ChainMap` | Python 3.3 |
| `UserDict` | Python 1.5 |
| `UserList` | Python 1.5 |
| `UserString` | Python 1.5 |

### Important Python Version Changes

- Python 3.7 guarantees insertion order for normal dictionaries.
- Because of this, `OrderedDict` is needed much less frequently today.
- `namedtuple` remains useful, although many projects now prefer `dataclass` for mutable domain models.
- `ChainMap` and the `User*` classes remain valuable in specialised scenarios.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- `namedtuple`
- `OrderedDict`
- `ChainMap`
- `UserDict`
- `UserList`
- `UserString`
- When to use each collection
- Performance trade-offs
- Production use cases
- Modern alternatives

______________________________________________________________________

# Recap

In Part 1 we covered:

- `deque`
- `Counter`
- `defaultdict`

These solve common data processing problems.

Today we'll finish the `collections` module by looking at several specialised data structures.

______________________________________________________________________

# Choosing the Right Collection

Python provides many collection types because different problems require different tools.

| Problem | Best Choice |
|----------|-------------|
| Queue | `deque` |
| Frequency counting | `Counter` |
| Grouping | `defaultdict` |
| Immutable record | `namedtuple` |
| Layered configuration | `ChainMap` |
| Custom dictionary behaviour | `UserDict` |

Choosing the correct data structure often simplifies both code and maintenance.

______________________________________________________________________

# `namedtuple`

Suppose we represent a user like this.

```python
user = ("Alice", 30, "Engineer")
```

Accessing values

```python
print(user[0])
```

Output

```text
Alice
```

What does index `0` represent?

Nothing in the code tells us.

______________________________________________________________________

# Introducing `namedtuple`

```python
from collections import namedtuple

User = namedtuple(
    "User",
    ["name", "age", "role"]
)

user = User(
    "Alice",
    30,
    "Engineer"
)

print(user.name)
```

Output

```text
Alice
```

The code is immediately more readable.

______________________________________________________________________

# Tuple Behaviour

A `namedtuple` is still a tuple.

```python
print(isinstance(user, tuple))
```

Output

```text
True
```

It remains:

- Immutable
- Memory efficient
- Hashable (when fields are hashable)

______________________________________________________________________

# Index Access Still Works

```python
print(user[1])
```

Output

```text
30
```

Field names simply provide a clearer interface.

______________________________________________________________________

# Useful Methods

Convert to a dictionary.

```python
print(user._asdict())
```

Output

```python
{
    "name": "Alice",
    "age": 30,
    "role": "Engineer"
}
```

Replace fields.

```python
updated = user._replace(age=31)

print(updated)
```

Output

```text
User(name='Alice', age=31, role='Engineer')
```

Notice that `_replace()` returns a **new** object because `namedtuple` is immutable.

______________________________________________________________________

# When Should You Use `namedtuple`?

Good use cases:

- Lightweight immutable records
- Returning multiple related values
- CSV rows
- Database query results
- Geographic coordinates

______________________________________________________________________

# When Should You Prefer `dataclass`?

If the object:

- Changes frequently
- Contains business logic
- Has validation
- Needs methods

a `dataclass` is usually a better choice.

______________________________________________________________________

# Production Example

Database query

```python
User = namedtuple(
    "User",
    ["id", "email", "role"]
)

user = User(
    101,
    "alice@example.com",
    "admin"
)

print(user.email)
```

______________________________________________________________________

# `OrderedDict`

Before Python 3.7,

normal dictionaries did **not** guarantee insertion order.

Developers used

```python
from collections import OrderedDict
```

______________________________________________________________________

# Example

```python
from collections import OrderedDict

data = OrderedDict()

data["A"] = 1
data["B"] = 2

print(data)
```

Today,

a normal dictionary produces similar ordering behaviour.

______________________________________________________________________

# Does `OrderedDict` Still Matter?

Yes, but for specialised behaviour.

It provides methods such as:

```python
move_to_end()
```

Example

```python
from collections import OrderedDict

cache = OrderedDict()

cache["A"] = 1
cache["B"] = 2
cache["C"] = 3

cache.move_to_end("A")

print(cache)
```

Output

```text
OrderedDict([
    ('B', 2),
    ('C', 3),
    ('A', 1)
])
```

______________________________________________________________________

# LRU Cache Concept

Least Recently Used caches frequently use ordering.

```
Oldest

↓

Newest
```

Whenever an item is accessed,

move it to the end.

When the cache becomes full,

remove the oldest item.

`OrderedDict` makes this simple.

______________________________________________________________________

# `ChainMap`

Imagine configuration values.

```
Application Defaults

↓

Environment Variables

↓

User Configuration
```

Which value should be used?

Normally,

we merge dictionaries.

Instead,

`ChainMap` lets us search several mappings without copying them.

______________________________________________________________________

# Creating a ChainMap

```python
from collections import ChainMap

defaults = {
    "host": "localhost",
    "port": 5432
}

environment = {
    "port": 5433
}

config = ChainMap(
    environment,
    defaults
)

print(config["port"])
```

Output

```text
5433
```

The first mapping wins.

______________________________________________________________________

# Search Order

```
ChainMap

↓

Environment

↓

Defaults

↓

Key Found
```

No dictionary merging occurs.

______________________________________________________________________

# Updating Values

```python
config["debug"] = True

print(environment)
```

Output

```text
{
    "port": 5433,
    "debug": True
}
```

Assignments always affect the first mapping.

______________________________________________________________________

# Production Example

Configuration loading

```python
config = ChainMap(
    user_config,
    environment,
    defaults
)
```

Priority becomes

```
User

↓

Environment

↓

Defaults
```

Exactly what many backend applications require.

______________________________________________________________________

# `UserDict`

Sometimes you want a dictionary,

but with custom behaviour.

You could subclass `dict`.

However,

CPython's built-in types sometimes bypass overridden methods internally.

The recommended approach is usually to inherit from `UserDict`.

______________________________________________________________________

# Example

```python
from collections import UserDict

class LowerCaseDict(UserDict):

    def __setitem__(self, key, value):
        self.data[key.lower()] = value

headers = LowerCaseDict()

headers["Content-Type"] = "application/json"

print(headers)
```

Output

```text
{'content-type': 'application/json'}
```

______________________________________________________________________

# Why `UserDict`?

Internally,

`UserDict` stores values inside

```python
self.data
```

rather than implementing everything in C like the built-in `dict`.

This makes subclass behaviour more predictable.

______________________________________________________________________

# Production Example

HTTP headers are case-insensitive.

```text
Content-Type

content-type

CONTENT-TYPE
```

A custom dictionary can normalise keys automatically.

______________________________________________________________________

# `UserList`

The same idea applies to lists.

```python
from collections import UserList
```

Example

```python
from collections import UserList

class PositiveNumbers(UserList):

    def append(self, value):

        if value < 0:
            raise ValueError(
                "Negative values are not allowed."
            )

        super().append(value)

numbers = PositiveNumbers()

numbers.append(10)

numbers.append(20)
```

______________________________________________________________________

# `UserString`

Likewise,

strings.

```python
from collections import UserString

class SafeString(UserString):

    def lower(self):
        return "Custom"

text = SafeString("HELLO")

print(text.lower())
```

Although possible,

subclassing strings is relatively uncommon.

______________________________________________________________________

# Comparison

| Type | Modern Usage |
|------|--------------|
| `deque` | ⭐⭐⭐⭐⭐ |
| `Counter` | ⭐⭐⭐⭐⭐ |
| `defaultdict` | ⭐⭐⭐⭐⭐ |
| `namedtuple` | ⭐⭐⭐⭐☆ |
| `ChainMap` | ⭐⭐⭐☆☆ |
| `OrderedDict` | ⭐⭐☆☆☆ |
| `UserDict` | ⭐⭐⭐☆☆ |
| `UserList` | ⭐⭐☆☆☆ |
| `UserString` | ⭐☆☆☆☆ |

______________________________________________________________________

# Time Complexity

| Structure | Lookup | Insert | Delete |
|------------|---------|---------|---------|
| `namedtuple` | O(1) | Immutable | Immutable |
| `OrderedDict` | O(1) | O(1) | O(1) |
| `ChainMap` | O(number of mappings) | O(1) (first map) | O(1) (first map) |
| `UserDict` | O(1) | O(1) | O(1) |

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `OrderedDict` only to preserve insertion order.

Modern dictionaries already preserve insertion order.

______________________________________________________________________

## Mistake 2

Using `namedtuple` for complex domain objects.

Use `dataclass` when mutability or methods are needed.

______________________________________________________________________

## Mistake 3

Merging multiple dictionaries unnecessarily.

If you only need layered lookups,

consider `ChainMap`.

______________________________________________________________________

## Mistake 4

Subclassing `dict` directly when extensive customisation is required.

`UserDict` is often easier and more predictable.

______________________________________________________________________

# Best Practices

✅ Use `namedtuple` for lightweight immutable records.

✅ Use `ChainMap` for layered configuration.

✅ Use `UserDict` when implementing custom dictionary behaviour.

✅ Use `OrderedDict` only when its specialised ordering operations are required.

❌ Don't replace every `dict` with `OrderedDict`.

❌ Don't use `namedtuple` when objects need validation or mutable state.

______________________________________________________________________

# Production Insight

These structures appear in specialised backend scenarios.

**`namedtuple`**

- Database result rows
- Geographic coordinates
- Lightweight immutable records

**`OrderedDict`**

- LRU cache implementations
- Ordered processing pipelines

**`ChainMap`**

- Configuration systems
- Template variable resolution
- Context stacks

**`UserDict`**

- Case-insensitive dictionaries
- Validating dictionaries
- Automatically transforming keys

Senior engineers know these tools exist—even if they use them less frequently than `deque`, `Counter`, or `defaultdict`.

______________________________________________________________________

# Questions

### Question

> When would you choose `namedtuple` over a normal tuple?

### Answer

When the data has named fields and represents a fixed immutable record. Named fields improve readability while
preserving tuple performance.

______________________________________________________________________

### Question

> Is `OrderedDict` obsolete?

### Answer

Not entirely. Normal dictionaries preserve insertion order, but `OrderedDict` still provides specialised ordering
operations such as `move_to_end()` that are useful for algorithms like LRU caches.

______________________________________________________________________

### Question

> What is the purpose of `ChainMap`?

### Answer

It provides a single view across multiple mappings, searching each in order without copying or merging dictionaries.

______________________________________________________________________

### Question

> Why use `UserDict` instead of subclassing `dict`?

### Answer

`UserDict` is implemented in Python and stores data in an internal dictionary, making custom behaviour easier and more
predictable than subclassing the built-in `dict`.

______________________________________________________________________

### Question

> When should you use a `dataclass` instead of a `namedtuple`?

### Answer

Use a `dataclass` when objects need mutability, validation, methods, inheritance, or more complex business logic.

______________________________________________________________________

# Practical Lesson

Create:

```text
advanced_collections.py
```

```python
from collections import ChainMap
from collections import UserDict
from collections import namedtuple

# -----------------------------
# namedtuple
# -----------------------------
User = namedtuple(
    "User",
    ["id", "email"]
)

user = User(1, "alice@example.com")

print(user.email)

# -----------------------------
# ChainMap
# -----------------------------
defaults = {
    "host": "localhost",
    "port": 5432,
}

environment = {
    "port": 5433,
}

config = ChainMap(
    environment,
    defaults,
)

print(config["port"])

# -----------------------------
# UserDict
# -----------------------------
class LowerCaseHeaders(UserDict):

    def __setitem__(self, key, value):
        self.data[key.lower()] = value

headers = LowerCaseHeaders()

headers["Content-Type"] = "application/json"

print(headers)
```

Expected Output

```text
alice@example.com

5433

{'content-type': 'application/json'}
```

______________________________________________________________________

# Questions

## Question 1

When should you use a `namedtuple`?

### Answer

For lightweight immutable records with named fields, especially when readability is more important than raw tuples.

______________________________________________________________________

## Question 2

Why is `OrderedDict` less common today?

### Answer

Because Python 3.7+ guarantees insertion order for normal dictionaries, eliminating its primary historical purpose.

______________________________________________________________________

## Question 3

What problem does `ChainMap` solve?

### Answer

It allows multiple mappings to be searched as a single logical mapping without creating merged copies.

______________________________________________________________________

## Question 4

Why use `UserDict`?

### Answer

To implement custom dictionary behaviour more predictably than subclassing the built-in `dict`.

______________________________________________________________________

## Question 5

When should you use a `dataclass` instead of a `namedtuple`?

### Answer

When the object requires mutable fields, methods, validation, inheritance, or business logic.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a case-insensitive HTTP header dictionary using `UserDict`.

Support:

- Case-insensitive lookup
- Case-insensitive insertion
- Normal dictionary interface

______________________________________________________________________

## Exercise 2

Create an application configuration loader using `ChainMap` with:

- Default configuration
- Environment configuration
- User configuration

Demonstrate how precedence works.

______________________________________________________________________

## Exercise 3

Replace tuple-based database query results with `namedtuple` objects and compare the readability of the resulting code.

______________________________________________________________________

## Exercise 4

Implement a simple LRU cache using `OrderedDict`.

Support:

- `get(key)`
- `put(key, value)`
- Maximum cache size
- Automatic eviction of the least recently used item

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ How `namedtuple` improves tuple readability.
- ✅ Why `OrderedDict` is less important in modern Python.
- ✅ How `ChainMap` enables layered configuration.
- ✅ Why `UserDict`, `UserList`, and `UserString` exist.
- ✅ Modern alternatives such as `dataclass`.
- ✅ Production use cases.
- ✅ Performance trade-offs.
- ✅ Senior backend interview topics.

______________________________________________________________________

# Module Summary – Built-in Types & Collections

Over Lessons **29–39**, you've developed a deep understanding of Python's core data structures:

- Strings and Unicode
- Lists and dynamic arrays
- Tuples and immutability
- Dictionaries and hash tables
- Sets and hash-based membership
- Numeric types and precision
- The `collections` module

This knowledge forms the foundation for writing efficient, production-grade Python code. Understanding the internal
behaviour of these data structures will help you make informed design decisions, optimise performance, and write cleaner
backend applications.

______________________________________________________________________

# What's Next

**File:** [40-Algorithms-With-Python-Collections](40-algorithms-with-python-collections.md)

Topics:

- Choosing the right data structure
- Solving real backend problems efficiently
- Frequency counting
- Grouping data
- Sliding window algorithms
- Top-K problems
- BFS with `deque`
- Deduplication with `set`
- Caching with `dict`
- Complexity analysis
- Production case studies
- Senior backend interview problems

> **Note:** This lesson bridges Python's collection types with algorithmic thinking. Rather than introducing new syntax, you'll learn how experienced backend engineers combine these data structures to solve real-world problems efficiently.
