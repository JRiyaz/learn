# File: python/59-production-python-part-04-typing-module.md

# Production Python

# Part 4: The `typing` Module – Writing Self-Documenting and Maintainable Code

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 59
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why the `typing` module exists
- Type annotations vs runtime behaviour
- Static vs dynamic typing
- Core types in `typing`
- Generic types
- `Optional`
- `Union`
- `Literal`
- `TypedDict`
- `Protocol`
- `Callable`
- `TypeVar`
- `Generic`
- Modern Python typing syntax
- Production best practices
- Common mistakes
- questions

> **Note**
>
> This lesson intentionally focuses on the **`typing` module**. A deeper lesson on **Type Hinting** and static type checkers (such as `mypy` and `pyright`) has been deferred and will be covered later alongside FastAPI.

______________________________________________________________________

# Recap

Python is a dynamically typed language.

This is perfectly valid:

```python
value = 10

value = "Hello"

value = [1, 2, 3]
```

The variable changes type during execution.

The `typing` module does **not** change this behaviour.

Instead, it provides a common language for describing expected types.

______________________________________________________________________

# Why Does `typing` Exist?

Imagine a function:

```python
def calculate(a, b):

    return a + b
```

Questions immediately arise:

- Should `a` be an integer?
- Can it be a float?
- Can it be a string?
- Can it be a list?

The function signature does not communicate intent.

Using `typing` makes expectations explicit.

______________________________________________________________________

# Type Annotations Are Metadata

Example:

```python
def calculate(

    a: int,

    b: int

) -> int:

    return a + b
```

Python still executes:

```python
calculate("Hello", "World")
```

Result:

```text
HelloWorld
```

No exception is raised simply because of the annotations.

Annotations are metadata.

Python does not enforce them at runtime.

______________________________________________________________________

# Where Are Annotations Stored?

Every function stores annotations in:

```python
__annotations__
```

Example:

```python
def greet(name: str) -> str:

    return f"Hello {name}"
```

```python
print(greet.__annotations__)
```

Output:

```python
{
    "name": str,
    "return": str
}
```

Frameworks such as FastAPI, Pydantic and dependency injection systems inspect this metadata.

______________________________________________________________________

# Built-in Generic Types

Modern Python (3.9+) allows generic built-in collections.

Instead of:

```python
from typing import List

numbers: List[int]
```

Prefer:

```python
numbers: list[int]
```

Similarly:

```python
dict[str, int]

tuple[int, str]

set[str]
```

The older forms remain supported but are gradually being replaced.

______________________________________________________________________

# Optional

Sometimes a value may be absent.

```python
from typing import Optional
```

```python
def find_user(

    user_id: int

) -> Optional[str]:

    ...
```

Equivalent modern syntax:

```python
str | None
```

Meaning:

The function returns either:

- `str`
- `None`

______________________________________________________________________

# Union

A value may have multiple possible types.

```python
from typing import Union
```

```python
def parse(

    value: Union[int, float]

):

    ...
```

Modern syntax:

```python
int | float
```

______________________________________________________________________

# Literal

Sometimes only specific values are allowed.

```python
from typing import Literal
```

Example:

```python
def set_log_level(

    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR"
    ]

):

    ...
```

This communicates the allowed values clearly.

______________________________________________________________________

# Callable

Functions are objects.

They can be passed as arguments.

```python
from typing import Callable
```

Example:

```python
def execute(

    callback: Callable[[int], str]

):

    return callback(10)
```

Meaning:

The callback accepts:

```python
int
```

and returns:

```python
str
```

______________________________________________________________________

# TypedDict

Suppose an API returns:

```python
{
    "id": 1,
    "name": "Alice"
}
```

Instead of documenting this informally,

define its shape.

```python
from typing import TypedDict
```

```python
class UserDict(

    TypedDict

):

    id: int

    name: str
```

Now:

```python
def load_user() -> UserDict:

    ...
```

The expected dictionary structure becomes explicit.

______________________________________________________________________

# Protocol

Sometimes behaviour matters more than inheritance.

Example:

```python
from typing import Protocol
```

```python
class Serializer(

    Protocol

):

    def serialize(

        self,

        value: object

    ) -> str:

        ...
```

Any object implementing:

```python
serialize()
```

matches this protocol,

even if it inherits from nothing.

This is known as **structural typing**.

______________________________________________________________________

# TypeVar

Suppose we write:

```python
def first(items):

    return items[0]
```

We want the return type to match the element type.

```python
from typing import TypeVar

T = TypeVar("T")
```

```python
def first(

    items: list[T]

) -> T:

    return items[0]
```

If given:

```python
list[int]
```

the return type is inferred as:

```python
int
```

______________________________________________________________________

# Generic Classes

Generics work for classes too.

```python
from typing import Generic
from typing import TypeVar

T = TypeVar("T")
```

```python
class Repository(

    Generic[T]

):

    def save(

        self,

        item: T

    ):

        ...
```

Now you can create:

```python
Repository[User]

Repository[Order]

Repository[Product]
```

without rewriting the class.

______________________________________________________________________

# Type Aliases

Complex types can become difficult to read.

Instead of:

```python
dict[str, list[int]]
```

define:

```python
UserScores = dict[str, list[int]]
```

Now:

```python
def calculate(

    scores: UserScores

):

    ...
```

The code becomes more expressive.

______________________________________________________________________

# Runtime Inspection

Annotations remain available.

```python
from typing import get_type_hints
```

```python
hints = get_type_hints(

    calculate

)
```

Many frameworks use this function to inspect application code.

______________________________________________________________________

# Production Example

Suppose a repository returns:

```python
class User(

    TypedDict

):

    id: int

    username: str

    email: str
```

Service layer:

```python
def load_user(

    user_id: int

) -> User:

    ...
```

API layer immediately knows:

- Required keys
- Expected value types

without additional documentation.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Assuming annotations are enforced at runtime.

______________________________________________________________________

## Mistake 2

Using deprecated collection types unnecessarily.

Instead of:

```python
List[int]
```

prefer:

```python
list[int]
```

when targeting Python 3.9+.

______________________________________________________________________

## Mistake 3

Creating extremely complex nested types.

Example:

```python
dict[
    str,
    list[
        tuple[
            int,
            dict[str, float]
        ]
    ]
]
```

Consider using type aliases.

______________________________________________________________________

## Mistake 4

Using `Any` everywhere.

Doing so removes most of the value of typing.

______________________________________________________________________

## Mistake 5

Ignoring protocols in favour of unnecessary inheritance.

Sometimes behaviour is more important than class hierarchy.

______________________________________________________________________

# Best Practices

✅ Prefer modern built-in generic types.

✅ Use `TypedDict` for structured dictionaries.

✅ Use `Literal` for restricted values.

✅ Use `Protocol` for behaviour-based interfaces.

✅ Use `TypeVar` and `Generic` for reusable abstractions.

❌ Don't expect annotations to enforce runtime validation.

❌ Don't overcomplicate type definitions.

______________________________________________________________________

# Production Insight

Modern Python frameworks make extensive use of the `typing` module.

Examples include:

- FastAPI
- SQLAlchemy 2.x
- Dependency injection frameworks
- Data validation libraries
- API documentation generators

Even when runtime validation is handled elsewhere, rich type metadata improves tooling, documentation, IDE support, and
framework integration.

______________________________________________________________________

# Questions

### Question

> Does the `typing` module enforce type safety at runtime?

### Answer

No. It provides metadata that tools and frameworks can use, but Python itself does not enforce type annotations during
normal execution.

______________________________________________________________________

### Question

> Why use `TypedDict`?

### Answer

To describe the expected structure of dictionaries, making APIs and function contracts clearer.

______________________________________________________________________

### Question

> What is a `Protocol`?

### Answer

A protocol defines required behaviour rather than inheritance. Any object implementing the required methods satisfies
the protocol.

______________________________________________________________________

### Question

> What problem does `TypeVar` solve?

### Answer

It allows generic functions and classes to preserve relationships between input and output types.

______________________________________________________________________

### Question

> Why are type aliases useful?

### Answer

They improve readability by giving meaningful names to complex type expressions.

______________________________________________________________________

# Practical Lesson

Create a small project containing:

```text
app/
├── models.py
├── repository.py
├── service.py
└── api.py
```

Implement:

- A `TypedDict` representing a user.
- A generic `Repository[T]`.
- A `Protocol` for serialization.
- A function using `Literal` to configure log levels.
- A reusable type alias for application settings.

Inspect function annotations using:

```python
get_type_hints()
```

Observe how metadata can be accessed at runtime.

______________________________________________________________________

# Questions

## Question 1

Why does the `typing` module exist if Python is dynamically typed?

### Answer

It provides a standard way to describe expected types, improving readability, tooling, documentation, and framework
integration without changing Python's runtime behaviour.

______________________________________________________________________

## Question 2

When should `TypedDict` be preferred over a normal dictionary?

### Answer

When the dictionary has a well-defined structure that should be documented and consistently used across an application.

______________________________________________________________________

## Question 3

What is the advantage of `Protocol` over inheritance?

### Answer

Protocols support structural typing, allowing unrelated classes to satisfy an interface simply by implementing the
required behaviour.

______________________________________________________________________

## Question 4

What is the difference between `TypeVar` and `Generic`?

### Answer

`TypeVar` defines a type parameter, while `Generic` uses those parameters to build reusable generic classes.

______________________________________________________________________

## Question 5

Why is `Any` generally discouraged?

### Answer

Because it disables meaningful type information, reducing the benefits of documentation, tooling, and static analysis.

______________________________________________________________________

# Assignment

## Exercise 1

Replace informal dictionary return values with `TypedDict` definitions.

______________________________________________________________________

## Exercise 2

Implement a generic repository using `TypeVar` and `Generic`.

______________________________________________________________________

## Exercise 3

Define a `Protocol` for a notification service.

Create two classes that satisfy it without inheriting from a common base class.

______________________________________________________________________

## Exercise 4

Review one of your backend projects.

Identify places where:

- `Literal`
- `TypedDict`
- Type aliases
- Generic classes

could improve readability and maintainability.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why the `typing` module exists.
- ✅ Runtime behaviour of annotations.
- ✅ `Optional`, `Union`, `Literal`, and `Callable`.
- ✅ `TypedDict`.
- ✅ `Protocol`.
- ✅ `TypeVar` and `Generic`.
- ✅ Type aliases.
- ✅ Production use cases and best practices.

______________________________________________________________________

# Next Lesson

**File:**
[60-production-python-part-05-configuration-management](60-production-python-part-05-configuration-management.md)

```
```
