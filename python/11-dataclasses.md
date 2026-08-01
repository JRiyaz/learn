# File: python/11-dataclasses.md

# Python Advanced - Lesson 11

# Dataclasses - Writing Cleaner and More Maintainable Classes

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Object Model & Memory
>
> **Lesson:** 11
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why dataclasses were introduced
- How the `@dataclass` decorator works
- Automatically generated magic methods
- Default values
- `field()`
- `default_factory`
- Frozen dataclasses
- Ordered dataclasses
- Dataclass inheritance
- Production use cases
- Best practices and interview questions

______________________________________________________________________

# Why Were Dataclasses Introduced?

Before Python 3.7, many classes existed only to hold data.

Consider a simple `User` class.

```python
class User:

    def __init__(self, id, name, email):

        self.id = id
        self.name = name
        self.email = email
```

Creating an object works as expected.

```python
user = User(1, "Alice", "alice@example.com")
```

Now imagine another class.

```python
class Product:

    def __init__(self, id, name, price):

        self.id = id
        self.name = name
        self.price = price
```

And another.

```python
class Employee:

    def __init__(self, id, department, salary):

        self.id = id
        self.department = department
        self.salary = salary
```

Notice the repetition.

Every class needs nearly identical boilerplate.

______________________________________________________________________

# The Problem

A simple data class usually needs:

- `__init__()`
- `__repr__()`
- `__eq__()`

Sometimes it also needs:

- Ordering methods
- Hashing
- Immutability

Writing these repeatedly becomes tedious and error-prone.

______________________________________________________________________

# Introducing Dataclasses

Python 3.7 introduced the `dataclasses` module.

Instead of writing:

```python
class User:

    def __init__(self, id, name):

        self.id = id
        self.name = name
```

we write:

```python
from dataclasses import dataclass


@dataclass
class User:

    id: int
    name: str
```

That's all.

Python generates the constructor automatically.

______________________________________________________________________

# What Does @dataclass Generate?

By default, Python generates:

- `__init__()`
- `__repr__()`
- `__eq__()`

Let's verify.

```python
from dataclasses import dataclass


@dataclass
class User:

    id: int
    name: str


user = User(1, "Alice")

print(user)
```

Output

```
User(id=1, name='Alice')
```

We never implemented `__repr__()` ourselves.

______________________________________________________________________

# Automatic Equality

```python
from dataclasses import dataclass


@dataclass
class User:

    id: int
    name: str


user1 = User(1, "Alice")
user2 = User(1, "Alice")

print(user1 == user2)
```

Output

```
True
```

A normal class compares object identity unless `__eq__()` is implemented.

A dataclass compares field values by default.

______________________________________________________________________

# Type Annotations

Notice the syntax.

```python
id: int
name: str
```

These are type annotations.

They describe the expected type of each field.

Dataclasses use these annotations to identify which attributes belong to the class.

______________________________________________________________________

# Default Values

Fields can have defaults.

```python
from dataclasses import dataclass


@dataclass
class User:

    name: str
    active: bool = True
```

Usage

```python
user = User("Alice")

print(user)
```

Output

```
User(name='Alice', active=True)
```

______________________________________________________________________

# The Mutable Default Problem Returns

Consider this dataclass.

```python
from dataclasses import dataclass


@dataclass
class Team:

    members: list = []
```

Python raises an error.

Why?

Because mutable defaults are dangerous.

We studied this earlier in the course.

Every instance would otherwise share the same list.

______________________________________________________________________

# default_factory

The correct solution is:

```python
from dataclasses import dataclass, field


@dataclass
class Team:

    members: list = field(default_factory=list)
```

Now every object gets its own list.

```python
team1 = Team()
team2 = Team()

team1.members.append("Alice")

print(team1.members)

print(team2.members)
```

Output

```
['Alice']

[]
```

Each instance has an independent list.

______________________________________________________________________

# field()

The `field()` function allows additional configuration.

Common options include:

```python
field(default=0)

field(default_factory=list)

field(repr=False)

field(compare=False)
```

Example

```python
from dataclasses import dataclass, field


@dataclass
class User:

    username: str

    password: str = field(repr=False)
```

```python
user = User("alice", "secret")

print(user)
```

Output

```
User(username='alice')
```

The password is hidden from the object's string representation.

______________________________________________________________________

# Frozen Dataclasses

Sometimes objects should never change.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Currency:

    code: str
```

```python
currency = Currency("GBP")

currency.code = "USD"
```

Output

```
FrozenInstanceError
```

Frozen dataclasses are immutable after creation.

______________________________________________________________________

# Ordered Dataclasses

Python can also generate comparison methods.

```python
from dataclasses import dataclass


@dataclass(order=True)
class Product:

    price: int
```

```python
print(Product(10) < Product(20))
```

Output

```
True
```

Python automatically creates:

- `__lt__()`
- `__le__()`
- `__gt__()`
- `__ge__()`

______________________________________________________________________

# Dataclass Inheritance

Dataclasses support inheritance.

```python
from dataclasses import dataclass


@dataclass
class Person:

    name: str


@dataclass
class Employee(Person):

    salary: int
```

```python
employee = Employee("Alice", 50000)

print(employee)
```

Output

```
Employee(name='Alice', salary=50000)
```

______________________________________________________________________

# Dataclass vs Normal Class

| Normal Class | Dataclass |
|--------------|-----------|
| Manual `__init__()` | Generated automatically |
| Manual `__repr__()` | Generated automatically |
| Manual `__eq__()` | Generated automatically |
| More boilerplate | Less boilerplate |
| Better for complex behaviour | Better for data containers |

______________________________________________________________________

# Production Insight

Dataclasses are widely used in backend systems for:

- Configuration objects
- DTOs (Data Transfer Objects)
- API request/response models (when Pydantic isn't required)
- Domain models
- Internal service messages
- Immutable configuration

They are **not** typically used as ORM models in frameworks such as SQLAlchemy because those frameworks manage object
behaviour differently.

______________________________________________________________________

# Questions

### Question

> Why were dataclasses introduced?

### Answer

Dataclasses reduce boilerplate for classes whose primary purpose is storing data. They automatically generate methods
such as `__init__()`, `__repr__()` and `__eq__()`.

______________________________________________________________________

### Question

> Why should mutable defaults use `default_factory`?

### Answer

Using a mutable object as a default value would cause every instance to share the same object. `default_factory` creates
a new object for each instance.

______________________________________________________________________

### Question

> What does `frozen=True` do?

### Answer

It makes instances immutable after creation. Attempting to modify a field raises a `FrozenInstanceError`.

______________________________________________________________________

# Practical Lesson

Create a file:

```
dataclass_examples.py
```

```python
from dataclasses import dataclass, field


@dataclass
class Employee:

    id: int
    name: str
    skills: list = field(default_factory=list)


employee = Employee(1, "Alice")

employee.skills.append("Python")

print(employee)
```

Modify the program to:

- Add another employee.
- Verify that each employee has an independent `skills` list.
- Mark the dataclass as frozen and observe the behaviour when trying to modify a field.

______________________________________________________________________

# Questions

## Question 1

What problem do dataclasses solve?

### Answer

They reduce boilerplate by automatically generating common methods for classes that primarily store data.

______________________________________________________________________

## Question 2

Which methods are generated by default?

### Answer

`__init__()`, `__repr__()` and `__eq__()`.

______________________________________________________________________

## Question 3

Why is `default_factory` preferred over mutable default values?

### Answer

It creates a new object for every instance, preventing unintended sharing of mutable objects.

______________________________________________________________________

## Question 4

What does `frozen=True` do?

### Answer

It makes the dataclass immutable after construction.

______________________________________________________________________

## Question 5

When should you choose a dataclass?

### Answer

When the class primarily represents structured data with little or no custom behaviour.

______________________________________________________________________

# Assignment

## Exercise 1

Create a `Book` dataclass with:

- title
- author
- price

Instantiate three books and print them.

______________________________________________________________________

## Exercise 2

Create a `Library` dataclass containing a list of books using `default_factory`.

Verify that two `Library` instances maintain separate book collections.

______________________________________________________________________

## Exercise 3

Create a frozen `Configuration` dataclass and confirm that attempting to modify a field raises an exception.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why dataclasses were introduced.
- ✅ How `@dataclass` removes boilerplate.
- ✅ Automatically generated magic methods.
- ✅ Default values and `field()`.
- ✅ `default_factory` for mutable fields.
- ✅ Frozen and ordered dataclasses.
- ✅ Dataclass inheritance.
- ✅ Production use cases and best practices.

______________________________________________________________________

# What's Next

**File:** [12-NamedTuple](12-namedtuple.md)

Topics:

- Why `namedtuple` Exists
- Creating Named Tuples
- Immutability
- `_fields`
- `_replace()`
- `_asdict()`
- `typing.NamedTuple`
- Dataclass vs NamedTuple
- Production Examples
