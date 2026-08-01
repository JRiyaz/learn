# File: python/12-namedtuple.md

# Python Advanced - Lesson 12

# NamedTuple - Lightweight Immutable Data Structures

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Object Model & Memory
>
> **Lesson:** 12
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 75 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why `namedtuple` was introduced
- Problems with regular tuples
- Creating named tuples
- Accessing fields
- Immutability
- Useful helper methods
- `collections.namedtuple` vs `typing.NamedTuple`
- NamedTuple vs Dataclass
- Production use cases

______________________________________________________________________

# Why Does NamedTuple Exist?

Before Python had dataclasses, developers often used tuples to return multiple values.

Example

```python
employee = (101, "Alice", "Engineering")
```

Accessing values works.

```python
print(employee[0])

print(employee[1])

print(employee[2])
```

Output

```
101

Alice

Engineering
```

But there's a problem.

______________________________________________________________________

# The Problem with Regular Tuples

Suppose someone writes:

```python
employee[2]
```

What does index `2` represent?

- Employee ID?
- Department?
- Salary?
- Manager?

Without documentation, nobody knows.

Even worse,

```python
employee[0]
```

isn't nearly as readable as

```python
employee.id
```

This is exactly the problem `namedtuple` solves.

______________________________________________________________________

# Introducing namedtuple

Python provides `namedtuple` in the `collections` module.

```python
from collections import namedtuple
```

We define a new tuple type.

```python
Employee = namedtuple(
    "Employee",
    ["id", "name", "department"]
)
```

Now create an object.

```python
employee = Employee(
    101,
    "Alice",
    "Engineering"
)
```

______________________________________________________________________

# Accessing Fields

Instead of indexes,

we use attribute names.

```python
print(employee.id)

print(employee.name)

print(employee.department)
```

Output

```
101

Alice

Engineering
```

Much easier to understand.

______________________________________________________________________

# NamedTuple is Still a Tuple

Although it behaves like an object,

it is still a tuple.

```python
print(type(employee))
```

Output

```
<class '__main__.Employee'>
```

It also behaves like a tuple.

```python
print(employee[0])

print(employee[1])
```

Output

```
101

Alice
```

You get the best of both worlds.

______________________________________________________________________

# Immutability

Named tuples cannot be modified.

```python
employee.name = "Bob"
```

Output

```
AttributeError:
can't set attribute
```

This is intentional.

Like normal tuples,

named tuples are immutable.

______________________________________________________________________

# Why is Immutability Useful?

Immutable objects:

- Cannot change accidentally.
- Are thread-safe.
- Are easier to reason about.
- Can often be hashed.
- Work well as dictionary keys.

In backend systems,

immutable data structures reduce unexpected side effects.

______________________________________________________________________

# \_fields

Every named tuple exposes its field names.

```python
print(Employee._fields)
```

Output

```
('id', 'name', 'department')
```

Useful for:

- Dynamic programming
- Serialisation
- Debugging

______________________________________________________________________

# \_asdict()

Convert a named tuple into a dictionary.

```python
employee = Employee(
    101,
    "Alice",
    "Engineering"
)

print(employee._asdict())
```

Output

```python
{
    'id': 101,
    'name': 'Alice',
    'department': 'Engineering'
}
```

This is useful when converting data into JSON-friendly formats.

______________________________________________________________________

# \_replace()

Since named tuples are immutable,

they cannot be modified directly.

Instead,

Python creates a new object.

```python
updated = employee._replace(
    department="Platform"
)

print(updated)
```

Output

```
Employee(id=101,
         name='Alice',
         department='Platform')
```

The original object remains unchanged.

______________________________________________________________________

# Unpacking

Named tuples support tuple unpacking.

```python
employee = Employee(
    101,
    "Alice",
    "Engineering"
)

employee_id, name, department = employee

print(employee_id)
```

Output

```
101
```

______________________________________________________________________

# typing.NamedTuple

Python also provides

```python
from typing import NamedTuple
```

Example

```python
from typing import NamedTuple


class Employee(NamedTuple):

    id: int
    name: str
    department: str
```

Usage

```python
employee = Employee(
    101,
    "Alice",
    "Engineering"
)

print(employee.name)
```

Advantages include:

- Better type hints
- IDE support
- Static analysis
- Cleaner syntax

Modern Python projects generally prefer this version.

______________________________________________________________________

# collections.namedtuple vs typing.NamedTuple

| collections.namedtuple | typing.NamedTuple |
|-------------------------|------------------|
| Function-based | Class-based |
| Older syntax | Modern syntax |
| Limited typing | Full type hints |
| Still widely used | Preferred in new code |

______________________________________________________________________

# NamedTuple vs Dataclass

This is a very common interview question.

| NamedTuple | Dataclass |
|------------|-----------|
| Immutable | Mutable by default |
| Lightweight | More features |
| Behaves like a tuple | Behaves like a normal class |
| Very memory efficient | Slightly larger memory footprint |
| Best for fixed data | Best for business objects |

______________________________________________________________________

# When Should You Use NamedTuple?

Use a named tuple when:

- Data never changes.
- Objects are lightweight.
- You need tuple behaviour.
- Memory usage matters.
- Objects are primarily containers for values.

Use a dataclass when:

- Objects contain business logic.
- Values need to change.
- Validation is required.
- Methods are needed.

______________________________________________________________________

# Production Insight

Named tuples appear in many production systems.

Examples include:

Configuration values

```python
Server = NamedTuple(
    "Server",
    [
        ("host", str),
        ("port", int)
    ]
)
```

Database query results

```python
UserRow(
    id=1,
    name="Alice"
)
```

Geographical coordinates

```python
Point(
    latitude,
    longitude
)
```

Log entries

```python
LogEntry(
    timestamp,
    level,
    message
)
```

Although dataclasses have become more popular,

named tuples are still common in libraries that return immutable records.

______________________________________________________________________

# Best Practices

✅ Use meaningful field names.

✅ Prefer `typing.NamedTuple` in new projects.

✅ Use named tuples for immutable records.

❌ Don't add business logic to named tuples.

❌ Don't use named tuples when frequent updates are required.

______________________________________________________________________

# Questions

### Question

> Why should you use a named tuple instead of a regular tuple?

### Answer

A named tuple provides meaningful attribute names while retaining the efficiency and immutability of a tuple. This makes
code more readable and less error-prone.

______________________________________________________________________

### Question

> What is the difference between a named tuple and a dataclass?

### Answer

A named tuple is immutable, lightweight and behaves like a tuple. A dataclass is more flexible, mutable by default and
designed for objects that may contain behaviour as well as data.

______________________________________________________________________

### Question

> Why is `typing.NamedTuple` generally preferred over `collections.namedtuple`?

### Answer

`typing.NamedTuple` supports type annotations, integrates better with static type checkers and IDEs, and provides a
cleaner class-based syntax.

______________________________________________________________________

# Practical Lesson

Create a file:

```
namedtuple_examples.py
```

```python
from typing import NamedTuple


class Employee(NamedTuple):

    id: int
    name: str
    department: str


employee = Employee(
    101,
    "Alice",
    "Engineering"
)

print(employee.name)

print(employee._fields)

print(employee._asdict())
```

Expected Output

```
Alice

('id', 'name', 'department')

{
    'id': 101,
    'name': 'Alice',
    'department': 'Engineering'
}
```

Now create an updated employee.

```python
updated = employee._replace(
    department="Platform"
)

print(updated)
```

Observe that the original object remains unchanged.

______________________________________________________________________

# Questions

## Question 1

What problem does `namedtuple` solve?

### Answer

It provides meaningful field names for tuple elements, making code more readable while preserving tuple behaviour and
immutability.

______________________________________________________________________

## Question 2

Can a named tuple be modified?

### Answer

No. Named tuples are immutable. Any change requires creating a new instance, often using `_replace()`.

______________________________________________________________________

## Question 3

What does `_asdict()` do?

### Answer

It returns a dictionary containing the named tuple's field names and values.

______________________________________________________________________

## Question 4

What does `_fields` return?

### Answer

It returns a tuple containing the names of all fields defined in the named tuple.

______________________________________________________________________

## Question 5

When should you use a named tuple instead of a dataclass?

### Answer

Use a named tuple when you need a lightweight, immutable data structure with tuple behaviour. Use a dataclass when you
need mutable objects, richer behaviour or additional features.

______________________________________________________________________

# Assignment

## Exercise 1

Create a `Book` named tuple with:

- title
- author
- price

Print each field using attribute access.

______________________________________________________________________

## Exercise 2

Use `_replace()` to create a new book with an updated price.

Verify that the original object has not changed.

______________________________________________________________________

## Exercise 3

Convert a named tuple into a dictionary using `_asdict()` and print the result.

______________________________________________________________________

## Exercise 4

Implement the same `Book` model using both a `NamedTuple` and a `@dataclass`.

Compare:

- Mutability
- Memory usage
- Readability
- Ease of modification

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why `namedtuple` was introduced.
- ✅ How named tuples improve readability over regular tuples.
- ✅ Why they are immutable.
- ✅ How to use `_fields`, `_asdict()` and `_replace()`.
- ✅ The difference between `collections.namedtuple` and `typing.NamedTuple`.
- ✅ When to choose a named tuple over a dataclass.
- ✅ Production use cases and best practices.

______________________________________________________________________

# What's Next

**File:** [13-Enums](13-enums.md)

Topics:

- Why Enums Exist
- Creating Enums
- Enum Members
- `auto()`
- `IntEnum`
- `StrEnum`
- Flag & IntFlag
- Iterating Enums
- Enum vs Constants
- Production Examples

```
```
