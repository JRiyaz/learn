# File: python/10-magic-methods-part-1.md

# Python Advanced - Lesson 10 (Part 1)

# Magic Methods - Understanding Python's Object Model

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Object Model
>
> **Lesson:** 10 (Part 1)
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What magic (dunder) methods are
- Why Python uses magic methods
- The object lifecycle
- The purpose of `__new__()`
- The purpose of `__init__()`
- The purpose of `__del__()`
- The order in which these methods are executed
- Real-world backend use cases

______________________________________________________________________

# Why Learn Magic Methods?

Throughout this course, you've already used several magic methods.

For example:

Context Managers

```python
__enter__()

__exit__()
```

Iterators

```python
__iter__()

__next__()
```

But we never discussed what these methods actually are.

Magic methods are one of Python's core language features.

They allow your own objects to behave like Python's built-in objects.

______________________________________________________________________

# What Are Magic Methods?

Magic methods are special methods whose names begin and end with double underscores.

Example

```python
__init__

__len__

__str__

__iter__

__next__

__enter__

__exit__
```

They are also called:

- Dunder methods (Double UNDERscore)
- Special methods

Python automatically calls them at the appropriate time.

You almost never call them directly.

______________________________________________________________________

# Why Do They Exist?

Suppose you create a class.

```python
class User:

    pass


user = User()
```

When you create:

```python
user = User()
```

Python performs much more work than it appears.

Internally, Python does something similar to:

```
Allocate Memory

↓

Create Object

↓

Initialize Object

↓

Return Object
```

Magic methods allow us to customise each step.

______________________________________________________________________

# The Object Lifecycle

Whenever you create an object,

Python follows this sequence.

```
User()

↓

__new__()

↓

Object Created

↓

__init__()

↓

Ready to Use

↓

...

↓

__del__()

↓

Object Destroyed
```

Let's understand each step.

______________________________________________________________________

# __new__()

`__new__()` is responsible for creating a new object.

It executes **before** `__init__()`.

Example

```python
class User:

    def __new__(cls):

        print("Creating Object")

        return super().__new__(cls)

    def __init__(self):

        print("Initializing Object")


user = User()
```

Output

```
Creating Object

Initializing Object
```

Notice the order.

```
__new__()

↓

__init__()
```

______________________________________________________________________

# What Does cls Mean?

Inside `__new__()`,

the first parameter is:

```python
cls
```

Unlike `self`,

`cls` refers to the class itself.

```
User

↓

cls

↓

Create Object
```

Python hasn't created the object yet.

So `self` doesn't exist.

______________________________________________________________________

# Why Must __new__ Return an Object?

Look at this example.

```python
class User:

    def __new__(cls):

        print("Creating")

        return super().__new__(cls)
```

The return statement creates the actual object.

Without it,

there is no object for Python to initialise.

______________________________________________________________________

# What Happens If __new__ Doesn't Return an Object?

```python
class User:

    def __new__(cls):

        print("Creating")

        return None

    def __init__(self):

        print("Initializing")


user = User()
```

Output

```
Creating
```

`__init__()` never runs.

Why?

Because no object was created.

This demonstrates an important rule:

> `__init__()` only runs if `__new__()` successfully returns an instance.

______________________________________________________________________

# __init__()

Once the object exists,

Python calls:

```python
__init__()
```

Its job is to initialise the object's attributes.

Example

```python
class User:

    def __init__(self, name):

        self.name = name


user = User("Alice")

print(user.name)
```

Output

```
Alice
```

Think of it like moving into a new house.

```
House Built

↓

Move Furniture

↓

Ready to Live
```

`__new__()` builds the house.

`__init__()` arranges the furniture.

______________________________________________________________________

# __new__ vs __init__

This is a common interview question.

| `__new__()` | `__init__()` |
|-------------|--------------|
| Creates the object | Initialises the object |
| Runs first | Runs second |
| Receives `cls` | Receives `self` |
| Must return an object | Returns `None` |
| Rarely overridden | Frequently overridden |

Remember:

```
__new__()

↓

Object Exists

↓

__init__()
```

______________________________________________________________________

# __del__()

When an object is about to be destroyed,

Python may call:

```python
__del__()
```

Example

```python
class User:

    def __del__(self):

        print("Object Destroyed")


user = User()

del user
```

Possible Output

```
Object Destroyed
```

Notice the word **possible**.

______________________________________________________________________

# Why "Possible"?

Unlike `__init__()`,

`__del__()` is **not guaranteed** to run immediately.

Python decides when an object is actually destroyed.

This depends on:

- Reference counting
- Garbage collection
- Circular references

We studied these earlier in the course.

______________________________________________________________________

# Should You Use __del__?

Generally,

**No.**

Avoid relying on `__del__()` for important cleanup.

Instead,

use:

```python
with ...
```

and context managers.

Context managers provide deterministic cleanup.

`__del__()` does not.

______________________________________________________________________

# Example - Object Lifecycle

```python
class User:

    def __new__(cls):

        print("1. __new__")

        return super().__new__(cls)

    def __init__(self):

        print("2. __init__")

    def __del__(self):

        print("3. __del__")


user = User()

del user
```

Possible Output

```
1. __new__

2. __init__

3. __del__
```

This demonstrates the complete lifecycle of a Python object.

______________________________________________________________________

# Production Insight

Most backend developers override:

```python
__init__()
```

every day.

Examples include:

```python
class UserService:

    def __init__(self, database):

        self.database = database
```

This is constructor-based dependency injection.

______________________________________________________________________

`__new__()` is far less common.

It is mainly used for advanced scenarios such as:

- Immutable types
- Singleton implementations
- Object caching
- Metaclasses

______________________________________________________________________

`__del__()` is rarely used in production.

Resource cleanup is almost always handled using:

```python
with ...
```

or explicit `close()` methods.

______________________________________________________________________

# Questions

### Question

> What is the difference between `__new__()` and `__init__()`?

### Answer

`__new__()` creates and returns a new object. It executes before `__init__()`. Once the object has been created,
`__init__()` initialises its attributes. If `__new__()` does not return an instance of the class, `__init__()` is never
called.

______________________________________________________________________

### Question

> Why is `__new__()` rarely overridden?

### Answer

Most classes only need custom initialisation, which is handled by `__init__()`. Overriding `__new__()` is typically
reserved for advanced cases such as immutable objects, object caching, singletons or metaclasses.

______________________________________________________________________

### Question

> Why is relying on `__del__()` discouraged?

### Answer

`__del__()` is not guaranteed to execute at a predictable time because object destruction depends on Python's memory
management and garbage collector. Context managers provide a safer and more reliable mechanism for resource cleanup.

______________________________________________________________________

# Practical Lesson

Create a file:

```
object_lifecycle.py
```

```python
class Employee:

    def __new__(cls):

        print("Creating Employee")

        return super().__new__(cls)

    def __init__(self, name):

        print("Initializing Employee")

        self.name = name

    def __del__(self):

        print("Destroying Employee")


employee = Employee("Alice")

print(employee.name)

del employee
```

Expected Output

```
Creating Employee

Initializing Employee

Alice

Destroying Employee
```

Depending on the Python implementation, the final message may appear immediately or later.

______________________________________________________________________

# Questions

## Question 1

What are magic methods?

### Answer

Magic methods are special methods with names surrounded by double underscores. Python calls them automatically to
customise the behaviour of objects.

______________________________________________________________________

## Question 2

Which method creates an object?

### Answer

`__new__()` creates and returns a new object before `__init__()` is called.

______________________________________________________________________

## Question 3

What is the purpose of `__init__()`?

### Answer

`__init__()` initialises a newly created object by assigning values to its attributes and preparing it for use.

______________________________________________________________________

## Question 4

Can `__init__()` return an object?

### Answer

No. `__init__()` must return `None`. Object creation is the responsibility of `__new__()`.

______________________________________________________________________

## Question 5

Why should `__del__()` generally be avoided for resource cleanup?

### Answer

Because its execution is not deterministic. Python decides when objects are destroyed, so important cleanup should be
performed using context managers or explicit cleanup methods.

______________________________________________________________________

# Assignment

## Exercise 1

Create a class that prints a message from both `__new__()` and `__init__()`.

Observe the order in which they execute.

______________________________________________________________________

## Exercise 2

Modify `__new__()` to return `None`.

Observe whether `__init__()` is called and explain why.

______________________________________________________________________

## Exercise 3

Create a class that defines `__del__()`.

Create and delete several objects, and observe when `__del__()` is executed.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What magic methods are.
- ✅ Why Python uses magic methods.
- ✅ The object lifecycle.
- ✅ The responsibilities of `__new__()`, `__init__()` and `__del__()`.
- ✅ Why `__new__()` executes before `__init__()`.
- ✅ Why `__del__()` should not be relied upon for resource management.
- ✅ Where these methods are used in production code.

______________________________________________________________________

# What's Next

**File:** [10-Magic-Methods-part-2](10-magic-methods-part-2.md)

Topics:

- `__str__()` vs `__repr__()`
- `__len__()`
- `__bool__()`
- `__eq__()`
- Comparison Magic Methods
- `__hash__()`
- Operator Overloading (`__add__()`, `__sub__()`)
- Production Examples
