# File: python/21-slots.md

# Python Advanced - Lesson 21
# `__slots__` - Optimising Memory and Controlling Object Attributes

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 21
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 100 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why `__slots__` exists
- How normal Python objects store attributes
- What `__dict__` is
- How `__slots__` changes object memory
- Memory and performance implications
- Inheritance with `__slots__`
- Dataclasses with slots
- Production use cases

---

# Recap

In the previous lesson, we learned about descriptors.

Descriptors intercept attribute access.

Today we'll learn another feature that changes how Python stores object attributes.

This feature is

```python
__slots__
```

Unlike descriptors, `__slots__` is primarily about:

- Memory optimisation
- Preventing accidental attributes
- Controlling object layout

---

# The Problem

Consider a simple class.

```python
class User:

    def __init__(self, name, age):

        self.name = name

        self.age = age
```

Usage

```python
user = User("Alice", 30)
```

Everything looks normal.

But internally, Python stores attributes in a dictionary.

---

# Every Object Has a __dict__

Let's inspect it.

```python
print(user.__dict__)
```

Output

```python
{
    "name": "Alice",
    "age": 30
}
```

Every instance owns its own dictionary.

Visual representation

```
User Object

+----------------------+
| __dict__             |
|----------------------|
| name -> Alice        |
| age  -> 30           |
+----------------------+
```

---

# Why Use a Dictionary?

Dictionaries are flexible.

You can add attributes dynamically.

```python
user.country = "India"
```

Now

```python
print(user.__dict__)
```

Output

```python
{
    "name": "Alice",
    "age": 30,
    "country": "India"
}
```

Python allows this because attributes are stored in a dictionary.

---

# The Cost of Flexibility

Dictionaries are powerful.

But they consume memory.

Imagine

```
10 objects
```

No problem.

Now imagine

```
10 million objects
```

Each object owns a dictionary.

That's a huge amount of memory.

Large applications like:

- Web servers
- Data pipelines
- Machine learning
- ORMs

may create millions of objects.

Saving even a small amount of memory per object becomes significant.

---

# Enter __slots__

Instead of using a dictionary,

we explicitly tell Python which attributes are allowed.

```python
class User:

    __slots__ = ("name", "age")

    def __init__(self, name, age):

        self.name = name

        self.age = age
```

Usage

```python
user = User("Alice", 30)
```

Looks identical.

Internally,

it's very different.

---

# What Changed?

Instead of storing

```
name

↓

Dictionary
```

Python creates fixed storage.

Visual representation

Without `__slots__`

```
User

↓

__dict__

↓

name

age
```

With `__slots__`

```
User

↓

Fixed Memory

↓

name

age
```

No instance dictionary is created.

---

# Checking __dict__

```python
print(user.__dict__)
```

Output

```
AttributeError:
'User' object has no attribute '__dict__'
```

The dictionary no longer exists.

---

# Dynamic Attributes Are Gone

Previously

```python
user.country = "India"
```

worked.

Now

```python
user.country = "India"
```

Output

```
AttributeError:
'User' object has no attribute 'country'
```

Only declared attributes are allowed.

---

# Why Does This Save Memory?

Normal object

```
Object

↓

Dictionary

↓

Hash Table

↓

Attribute
```

Slots

```
Object

↓

Direct Memory Location

↓

Attribute
```

Python avoids creating and managing a dictionary for every object.

---

# Memory Comparison

Suppose one million objects.

Without slots

```
Object

+

Dictionary

+

Dictionary Overhead
```

With slots

```
Object

+

Fixed Attribute Storage
```

Memory savings can be substantial, although the exact amount depends on the Python version and the number of attributes.

---

# Does __slots__ Improve Speed?

This is a common interview question.

The answer is:

**Sometimes—but memory is the primary benefit.**

Attribute lookup may be slightly faster because Python doesn't need to search an instance dictionary.

However,

the improvement is usually small.

You should choose `__slots__` because of memory efficiency and attribute control,

not because you expect major performance gains.

---

# Using Multiple Slots

```python
class Employee:

    __slots__ = (

        "name",

        "age",

        "salary"

    )
```

These are now the only permitted instance attributes.

---

# Inheritance Without Slots

Consider

```python
class Person:

    __slots__ = ("name",)


class Employee(Person):

    pass
```

Now

```python
employee = Employee()

employee.salary = 50000
```

This works.

Why?

Because the child class does **not** define `__slots__`.

Python automatically gives it a `__dict__`.

The optimisation is lost.

---

# Inheritance With Slots

To preserve slot behaviour,

the child must also define slots.

```python
class Person:

    __slots__ = ("name",)


class Employee(Person):

    __slots__ = ("salary",)
```

Now

```python
employee = Employee()

employee.name = "Alice"

employee.salary = 50000
```

Works correctly.

Attempting

```python
employee.department = "Engineering"
```

raises

```
AttributeError
```

---

# Empty Slots

Sometimes you'll see

```python
class Child(Parent):

    __slots__ = ()
```

Why?

The child introduces no new attributes,

but still wants to prevent Python from creating a `__dict__`.

This preserves the parent's slot optimisation.

---

# Weak References

Normally

```python
import weakref

ref = weakref.ref(user)
```

works.

With slots

```python
class User:

    __slots__ = ("name",)
```

this raises an error.

To support weak references,

include

```python
class User:

    __slots__ = (

        "name",

        "__weakref__"

    )
```

Most applications never need this,

but libraries often do.

---

# Slots and Dataclasses

Dataclasses support slots directly.

```python
from dataclasses import dataclass


@dataclass(slots=True)
class User:

    name: str

    age: int
```

Python automatically creates the appropriate slots.

This is the recommended approach when using dataclasses in memory-sensitive applications.

---

# Slots and Descriptors

From the previous lesson,

you learned that properties are descriptors.

They continue to work with slots.

Example

```python
class Product:

    __slots__ = ("_price",)

    @property
    def price(self):

        return self._price

    @price.setter
    def price(self, value):

        if value < 0:

            raise ValueError

        self._price = value
```

Descriptors and slots work together perfectly.

---

# When Should You Use __slots__?

Good candidates

- Millions of objects
- Data processing
- Geometry libraries
- Scientific computing
- Large caches
- ORMs
- High-performance backend services

Poor candidates

- Small applications
- Classes requiring dynamic attributes
- Rapid prototyping
- Code that heavily relies on `__dict__`

---

# Production Example - Game Engine

Suppose a game creates

```
5 million bullets
```

Each bullet contains

- x
- y
- velocity

Using slots significantly reduces memory consumption.

```python
class Bullet:

    __slots__ = (

        "x",

        "y",

        "velocity"
    )
```

---

# Production Example - Market Data

A financial trading system may process millions of price updates.

```python
class Tick:

    __slots__ = (

        "symbol",

        "price",

        "timestamp"
    )
```

Reducing per-object memory allows more market data to remain in memory simultaneously.

---

# Production Example - Backend APIs

Imagine parsing millions of JSON records.

```python
class UserRecord:

    __slots__ = (

        "id",

        "name",

        "email"
    )
```

Memory savings can reduce garbage collection pressure and improve overall throughput.

---

# Common Mistakes

## Mistake 1

Using slots everywhere.

Most applications won't benefit.

---

## Mistake 2

Expecting dramatic speed improvements.

Memory savings are the primary advantage.

---

## Mistake 3

Forgetting slots in subclasses.

```python
class Child(Parent):

    pass
```

This silently reintroduces `__dict__`.

---

## Mistake 4

Forgetting `__weakref__`

Library code that relies on weak references may stop working.

---

# Best Practices

✅ Use slots for lightweight objects created in very large numbers.

✅ Measure memory usage before and after optimisation.

✅ Define slots in subclasses if you want to preserve slot behaviour.

✅ Use `@dataclass(slots=True)` when appropriate.

❌ Don't optimise prematurely.

❌ Don't use slots if dynamic attributes are required.

---

# Production Insight

Many developers hear about `__slots__` in interviews and assume it should be used everywhere.

In reality,

most production web applications create relatively few long-lived business objects.

The memory savings are often negligible.

Where `__slots__` shines is in systems that create **millions** of lightweight objects, such as:

- Data science workloads
- Streaming systems
- Game engines
- Financial trading platforms
- Parsers
- Compilers

Always profile your application before introducing memory optimisations.

---

# Questions

### Question

> What problem does `__slots__` solve?

### Answer

`__slots__` reduces per-instance memory usage by preventing Python from creating an instance `__dict__` and by storing attributes in fixed locations.

---

### Question

> Can you add new attributes to a slotted object?

### Answer

No. Only attributes listed in `__slots__` may be assigned unless the class also defines a `__dict__`.

---

### Question

> Does `__slots__` improve performance?

### Answer

It may provide a small improvement in attribute access, but its primary benefit is reduced memory usage and preventing accidental attribute creation.

---

### Question

> What happens if a subclass doesn't define `__slots__`?

### Answer

Python creates an instance `__dict__` for the subclass, which removes most of the memory optimisation provided by the parent class.

---

# Practical Lesson

Create a file:

```
slots_examples.py
```

```python
from dataclasses import dataclass


class User:

    __slots__ = ("name", "age")

    def __init__(self, name, age):

        self.name = name
        self.age = age


user = User("Alice", 30)

print(user.name)

try:

    user.country = "India"

except AttributeError as error:

    print(error)


@dataclass(slots=True)
class Product:

    name: str
    price: float


product = Product("Keyboard", 49.99)

print(product)
```

Expected Output

```
Alice

'User' object has no attribute 'country'

Product(name='Keyboard', price=49.99)
```

Now remove `__slots__` from `User` and observe how adding `country` succeeds.

---

# Questions

## Question 1

What is `__slots__`?

### Answer

`__slots__` is a class attribute that defines a fixed set of allowed instance attributes, reducing memory usage by eliminating the instance `__dict__`.

---

## Question 2

Why does `__slots__` reduce memory usage?

### Answer

Because Python stores attribute values in fixed locations instead of allocating a separate dictionary for every object.

---

## Question 3

Does every class benefit from `__slots__`?

### Answer

No. It is most useful for classes with many instances where memory consumption is significant.

---

## Question 4

Why might a subclass lose the benefits of `__slots__`?

### Answer

If the subclass doesn't define its own `__slots__`, Python creates an instance `__dict__`, reintroducing the memory overhead.

---

## Question 5

Can `@property` be used with `__slots__`?

### Answer

Yes. Properties are descriptors and work normally with slotted classes as long as the underlying storage attribute is included in `__slots__`.

---

# Assignment

## Exercise 1

Create a `Point` class with:

- `x`
- `y`

Use `__slots__`.

Verify that adding a `colour` attribute raises an exception.

---

## Exercise 2

Create:

- `Vehicle`
- `Car`

Both should use `__slots__`.

Ensure `Car` adds only one new attribute without reintroducing `__dict__`.

---

## Exercise 3

Rewrite one of your previous dataclass examples using:

```python
@dataclass(slots=True)
```

Explain what changed.

---

## Exercise 4

Research a Python library you use (such as SQLAlchemy, NumPy or Pydantic) and investigate whether it uses `__slots__` internally. Summarise why it does—or why it doesn't.

---

# Summary

In this lesson, you learned:

- ✅ Why Python objects normally have a `__dict__`.
- ✅ How `__slots__` changes object memory layout.
- ✅ The memory and performance trade-offs.
- ✅ How inheritance interacts with `__slots__`.
- ✅ Why `__weakref__` may be required.
- ✅ How `@dataclass(slots=True)` simplifies usage.
- ✅ When `__slots__` is beneficial in production systems.

---

# What's Next

**File:**
[22-New-and-Metaclasses](22-new-and-metaclasses.md)

Topics:

- Revisiting `__new__`
- `__new__` vs `__init__`
- Object Creation Lifecycle
- Immutable Types and `__new__`
- Singleton Pattern
- Introduction to Metaclasses
- `type` as a Metaclass
- Creating Custom Metaclasses (Level)
- Production Examples

> **Note:** This will be the final lesson in the **Advanced OOP** module. After completing it, we'll move into **Functional Python**, starting with higher-order built-ins like `map()`, `filter()`, `reduce()`, and the powerful `functools` and `itertools` modules.
