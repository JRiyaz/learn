# File: python/python-advanced-22-new-and-metaclasses.md

# Python Advanced - Lesson 22
# `__new__` and Metaclasses - How Python Creates Classes and Objects

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 22
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 140 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- The complete object creation lifecycle
- Why `__new__` exists
- The difference between `__new__` and `__init__`
- When to override `__new__`
- Creating immutable objects
- Implementing the Singleton pattern
- What metaclasses are
- Why `type` is a metaclass
- How custom metaclasses work
- Production use cases
- Interview questions

---

# Congratulations

This is the final lesson in the **Advanced OOP** module.

You've learned about:

- Inheritance
- Multiple Inheritance
- MRO
- Composition
- Abstract Base Classes
- Mixins
- Method Types
- Properties
- Descriptors
- `__slots__`

Today's lesson ties everything together by exploring what happens **before an object even exists**.

---

# The Object Creation Process

Consider

```python
user = User("Alice")
```

Most developers imagine

```
User()

↓

Object Created
```

That's only part of the story.

Internally Python performs:

```
User()

↓

__new__()

↓

Creates Object

↓

__init__()

↓

Initialises Object

↓

Returns Object
```

Understanding this lifecycle is essential for advanced Python.

---

# What is `__new__`?

`__new__` is responsible for **creating** an object.

It runs **before** `__init__`.

Its job is to return a new instance.

---

# What is `__init__`?

`__init__` does **not** create an object.

Instead,

it configures an object that already exists.

This distinction is one of the most common interview questions.

---

# A Simple Example

```python
class User:

    def __new__(cls):

        print("Creating object")

        return super().__new__(cls)

    def __init__(self):

        print("Initialising object")
```

Usage

```python
user = User()
```

Output

```
Creating object

Initialising object
```

Notice the order.

---

# Visualising the Lifecycle

```
Call Constructor

↓

__new__()

↓

Memory Allocated

↓

Object Returned

↓

__init__()

↓

Ready to Use
```

---

# Why Does `__new__` Return an Object?

Because Python needs something for `__init__` to initialise.

If `__new__` returns something else,

`__init__` is skipped.

Example

```python
class User:

    def __new__(cls):

        print("Returning integer")

        return 42

    def __init__(self):

        print("Never called")
```

Usage

```python
user = User()

print(user)
```

Output

```
Returning integer

42
```

`__init__` never runs.

---

# Why Override `__new__`?

Most classes never need to.

Typical reasons include:

- Immutable objects
- Singleton pattern
- Object caching
- Custom object creation
- Advanced libraries

---

# Immutable Objects

Immutable types include:

- `str`
- `tuple`
- `frozenset`
- `int`

Once created,

they cannot be modified.

Therefore,

their value must be determined **during object creation**.

That means `__new__`.

---

# Example

```python
class PositiveInt(int):

    def __new__(cls, value):

        if value < 0:

            value = 0

        return super().__new__(
            cls,
            value
        )
```

Usage

```python
number = PositiveInt(-10)

print(number)
```

Output

```
0
```

Because `int` is immutable,

changing it inside `__init__` would be too late.

---

# Object Caching

Python itself caches some objects.

Example

```python
a = 10

b = 10
```

Often

```python
a is b
```

returns

```
True
```

Small integers are cached.

Although implementation details vary by Python version,

this demonstrates that Python may reuse objects instead of creating new ones.

---

# Singleton Pattern

A Singleton ensures only one instance exists.

Example

```python
class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance
```

Usage

```python
db1 = Database()

db2 = Database()

print(db1 is db2)
```

Output

```
True
```

Both variables reference the same object.

---

# A Common Problem

Notice

```python
db1 = Database()

db2 = Database()
```

`__init__` still executes every time.

Example

```python
class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        print("Connecting...")
```

Output

```
Connecting...

Connecting...
```

The object wasn't recreated,

but it was reinitialised.

---

# Preventing Reinitialisation

```python
class Database:

    _instance = None

    _initialised = False

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self._initialised:

            return

        print("Connecting...")

        self._initialised = True
```

Now initialisation happens only once.

---

# Should You Use the Singleton Pattern?

Modern Python applications often prefer:

- Dependency Injection
- Module-level objects
- Framework-managed lifecycles

Singletons can introduce hidden global state and make testing more difficult.

Use them only when there is a clear requirement.

---

# Introducing Metaclasses

Now we move one level higher.

Question:

If objects are created from classes...

what creates classes?

Answer:

**Metaclasses.**

---

# Everything is an Object

Python treats classes as objects.

```python
class User:

    pass
```

Check its type.

```python
print(type(User))
```

Output

```
<class 'type'>
```

The class `User` is itself an object.

It was created by `type`.

---

# `type`

You already know

```python
type(10)
```

returns

```
<class 'int'>
```

Less obviously,

```python
type(User)
```

returns

```
<class 'type'>
```

So `type` has two jobs.

1. Determine an object's type.

2. Create classes.

---

# Creating a Class Without class

The following two definitions are equivalent.

Traditional syntax

```python
class User:

    def hello(self):

        print("Hello")
```

Using `type`

```python
def hello(self):

    print("Hello")


User = type(

    "User",

    (),

    {

        "hello": hello

    }

)
```

Usage

```python
user = User()

user.hello()
```

Output

```
Hello
```

This demonstrates that classes are created programmatically.

---

# What is a Metaclass?

A metaclass is simply **the class of a class**.

Visual hierarchy

```
Object

↓

Class

↓

Metaclass
```

Example

```
Alice

↓

User

↓

type
```

---

# Why Use Metaclasses?

Suppose every model in a project must define

```python
table_name
```

Instead of checking manually,

a metaclass can enforce the rule.

---

# Simple Metaclass

```python
class ModelMeta(type):

    def __new__(

        cls,

        name,

        bases,

        namespace

    ):

        print(f"Creating {name}")

        return super().__new__(

            cls,

            name,

            bases,

            namespace

        )
```

Usage

```python
class User(

    metaclass=ModelMeta

):

    pass
```

Output

```
Creating User
```

The metaclass executes **when the class is created**, not when instances are created.

---

# Understanding the Parameters

```python
def __new__(

    cls,

    name,

    bases,

    namespace

):
```

| Parameter | Meaning |
|------------|---------|
| `cls` | The metaclass |
| `name` | Class name |
| `bases` | Parent classes |
| `namespace` | Class attributes and methods |

---

# Enforcing Rules

```python
class ModelMeta(type):

    def __new__(

        cls,

        name,

        bases,

        namespace

    ):

        if "table_name" not in namespace:

            raise TypeError(

                "table_name required"

            )

        return super().__new__(

            cls,

            name,

            bases,

            namespace

        )
```

Works

```python
class User(

    metaclass=ModelMeta

):

    table_name = "users"
```

Fails

```python
class Product(

    metaclass=ModelMeta

):

    pass
```

Output

```
TypeError:
table_name required
```

The error occurs when the class is defined.

---

# Where Are Metaclasses Used?

You rarely write them,

but many frameworks do.

Examples include:

- Django ORM
- SQLAlchemy ORM
- Pydantic
- Django Forms
- Enum
- Abstract Base Classes (`ABCMeta`)

Whenever a framework automatically registers classes, validates definitions or builds metadata, a metaclass is often involved.

---

# Metaclasses vs Class Decorators

Suppose you only want to modify a class after it's created.

A class decorator may be simpler.

Metaclasses are appropriate when you need to control **how classes themselves are created**.

Rule of thumb:

- Modify existing class → Class decorator
- Control class creation → Metaclass

---

# Common Mistakes

## Mistake 1

Using `__new__` instead of `__init__`.

Most initialisation belongs in `__init__`.

Override `__new__` only when object creation itself must change.

---

## Mistake 2

Using metaclasses for ordinary problems.

Most applications never require a custom metaclass.

---

## Mistake 3

Returning the wrong object from `__new__`.

If `__new__` doesn't return an instance of the class (or a compatible object), `__init__` may never execute.

---

# Best Practices

✅ Override `__new__` primarily for immutable types or specialised object creation.

✅ Prefer dependency injection over Singleton patterns.

✅ Use metaclasses sparingly.

✅ Document metaclasses clearly because they affect class creation.

❌ Don't introduce metaclasses to reduce a few lines of code.

❌ Don't use `__new__` when `__init__` is sufficient.

---

# Production Insight

Although custom metaclasses are uncommon in everyday backend development, you'll frequently **use** classes that rely on them.

For example:

- Django models automatically become database-aware classes.
- Pydantic models automatically validate fields.
- Enums automatically register their members.
- Abstract Base Classes enforce interface contracts through `ABCMeta`.

Most backend engineers don't write metaclasses regularly, but understanding them helps explain how these frameworks provide powerful, declarative APIs.

---

# Interview Deep Dive

### Interviewer

> What is the difference between `__new__` and `__init__`?

### Answer

`__new__` creates and returns a new object. `__init__` initialises an object that has already been created.

---

### Interviewer

> When should you override `__new__`?

### Answer

Typically when subclassing immutable types, implementing specialised object creation or controlling instance creation, such as caching or Singleton patterns.

---

### Interviewer

> What is a metaclass?

### Answer

A metaclass is the class responsible for creating classes. In Python, the default metaclass is `type`.

---

### Interviewer

> Name some libraries that use metaclasses.

### Answer

Examples include Django's ORM, SQLAlchemy, Pydantic, Python's `Enum` implementation and Abstract Base Classes through `ABCMeta`.

---

# Practical Lesson

Create a file:

```
new_and_metaclasses_examples.py
```

```python
class PositiveInt(int):

    def __new__(cls, value):

        if value < 0:

            value = 0

        return super().__new__(

            cls,

            value

        )


print(PositiveInt(-25))


class RegistryMeta(type):

    registry = []

    def __new__(

        cls,

        name,

        bases,

        namespace

    ):

        new_class = super().__new__(

            cls,

            name,

            bases,

            namespace

        )

        cls.registry.append(name)

        return new_class


class User(

    metaclass=RegistryMeta

):

    pass


class Product(

    metaclass=RegistryMeta

):

    pass


print(RegistryMeta.registry)
```

Expected Output

```
0

['User', 'Product']
```

Observe that the registry is populated **when the classes are defined**, before any objects are created.

---

# Interview Questions

## Question 1

What is the purpose of `__new__`?

### Answer

`__new__` is responsible for creating and returning a new object before `__init__` is called.

---

## Question 2

Why is `__new__` important when subclassing immutable types?

### Answer

Immutable objects cannot be modified after creation, so any changes to their value must occur during object creation inside `__new__`.

---

## Question 3

What is the default metaclass in Python?

### Answer

The default metaclass is `type`, which is responsible for creating classes.

---

## Question 4

When are metaclass methods executed?

### Answer

Metaclass methods execute when a class is created, not when instances of that class are created.

---

## Question 5

Should most backend developers write custom metaclasses?

### Answer

No. Most developers interact with frameworks that use metaclasses internally but rarely need to create their own.

---

# Assignment

## Exercise 1

Create a subclass of `str` that automatically trims leading and trailing whitespace by overriding `__new__`.

Example

```python
name = TrimmedString("  Alice  ")

print(name)
```

Expected Output

```
Alice
```

---

## Exercise 2

Implement a thread-safe Singleton class and explain why thread safety matters in multi-threaded applications.

---

## Exercise 3

Create a metaclass that automatically adds a class attribute:

```python
version = "1.0"
```

to every class that uses it.

---

## Exercise 4

Create a metaclass that registers every subclass into a dictionary keyed by the class name.

Explain how this pattern could be useful for plugin systems or command registries.

---

# Summary

In this lesson, you learned:

- ✅ The complete Python object creation lifecycle.
- ✅ The difference between `__new__` and `__init__`.
- ✅ When overriding `__new__` is appropriate.
- ✅ How immutable objects rely on `__new__`.
- ✅ How the Singleton pattern works.
- ✅ That classes are themselves objects created by `type`.
- ✅ What metaclasses are and when they're used.
- ✅ Why frameworks like Django and Pydantic rely on metaclasses.

---

# 🎉 Module Complete - Advanced OOP

You have now completed the **Advanced OOP** module.

Topics mastered:

- ✅ Inheritance
- ✅ Multiple Inheritance
- ✅ Method Resolution Order (MRO)
- ✅ Composition
- ✅ Abstract Base Classes
- ✅ Mixins
- ✅ Instance, Class & Static Methods
- ✅ Properties
- ✅ Descriptors
- ✅ `__slots__`
- ✅ `__new__`
- ✅ Metaclasses

These concepts form the foundation of Python's object model and explain many of the "magic" behaviours used by modern frameworks.

---

# What's Next

**Module 3 – Functional Python**

**File:**

`python/python-functional-23-map-filter-reduce.md`

Topics:

- Functional Programming Concepts
- Pure Functions
- Immutability
- `map()`
- `filter()`
- `reduce()`
- `functools.reduce`
- Lambda with Functional Tools
- Performance Considerations
- Production Examples
- Interview Questions

> **Why this next?**
>
> Functional programming features are used extensively in Python's standard library, data processing, asynchronous code and backend applications. Understanding them will prepare you for powerful modules like `functools`, `itertools` and `collections`, which we'll explore in the upcoming lessons.
