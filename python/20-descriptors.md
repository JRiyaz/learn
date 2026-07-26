# File: python/python-advanced-20-descriptors.md

# Python Advanced - Lesson 20
# Descriptors - The Hidden Engine Behind Python Attributes

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 20
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 120 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What descriptors are
- Why descriptors exist
- The descriptor protocol
- `__get__()`
- `__set__()`
- `__delete__()`
- Data vs Non-Data Descriptors
- Attribute lookup order
- How `@property` works internally
- Production use cases
- Interview questions

---

# Recap

In the previous lesson, we learned about

- `@property`
- Property setters
- Property deleters

Example

```python
class Product:

    @property
    def price(self):

        return self._price
```

This looked like magic.

Today you'll discover that **it isn't magic at all**.

`property` is implemented using **Descriptors**.

Descriptors are one of the most powerful features in Python and are used throughout the language and many major frameworks.

---

# What is a Descriptor?

A descriptor is an object that controls how another object's attributes are accessed.

Instead of Python reading or writing an attribute directly,

it asks the descriptor what should happen.

Think of it as a gatekeeper.

```
Object

↓

Attribute Access

↓

Descriptor

↓

Actual Value
```

---

# Why Were Descriptors Introduced?

Imagine every class needs validation.

Without descriptors

```python
class User:

    @property
    def age(self):

        return self._age

    @age.setter
    def age(self, value):

        if value < 0:

            raise ValueError

        self._age = value
```

Now another class.

```python
class Employee:

    @property
    def age(self):

        ...
```

Then

```python
class Student:

    @property
    def age(self):

        ...
```

The validation is duplicated everywhere.

Descriptors let us write the validation once and reuse it across many classes.

---

# The Descriptor Protocol

Python recognises a descriptor if it implements one or more of these methods.

```python
__get__()

__set__()

__delete__()
```

These methods form the **descriptor protocol**.

---

# The Simplest Descriptor

```python
class Descriptor:

    def __get__(
        self,
        instance,
        owner
    ):

        print("Getting value")
```

Usage

```python
class User:

    name = Descriptor()


user = User()

user.name
```

Output

```
Getting value
```

Python automatically calls `__get__()`.

---

# Understanding __get__()

The method signature is

```python
def __get__(
    self,
    instance,
    owner
):
```

Parameters

| Parameter | Meaning |
|-----------|---------|
| `self` | Descriptor object |
| `instance` | Instance being accessed |
| `owner` | Class that owns the descriptor |

---

# Example

```python
class Descriptor:

    def __get__(
        self,
        instance,
        owner
    ):

        print(instance)

        print(owner)

        return "Alice"
```

```python
class User:

    name = Descriptor()


user = User()

print(user.name)
```

Output

```
<__main__.User object ...>

<class '__main__.User'>

Alice
```

---

# __set__()

Descriptors can intercept assignments.

```python
class Descriptor:

    def __set__(
        self,
        instance,
        value
    ):

        print(
            f"Setting {value}"
        )
```

Usage

```python
class User:

    name = Descriptor()


user = User()

user.name = "Alice"
```

Output

```
Setting Alice
```

---

# __delete__()

Descriptors can intercept deletion.

```python
class Descriptor:

    def __delete__(
        self,
        instance
    ):

        print("Deleting")
```

Usage

```python
del user.name
```

Output

```
Deleting
```

---

# Building a Real Descriptor

Suppose every age must be positive.

Instead of writing properties repeatedly,

create a reusable descriptor.

```python
class PositiveNumber:

    def __set_name__(
        self,
        owner,
        name
    ):

        self.storage_name = "_" + name

    def __get__(
        self,
        instance,
        owner
    ):

        return getattr(
            instance,
            self.storage_name
        )

    def __set__(
        self,
        instance,
        value
    ):

        if value <= 0:

            raise ValueError(
                "Must be positive."
            )

        setattr(
            instance,
            self.storage_name,
            value
        )
```

Usage

```python
class Product:

    price = PositiveNumber()


product = Product()

product.price = 50

print(product.price)
```

Output

```
50
```

---

# Understanding __set_name__()

Python automatically calls

```python
__set_name__()
```

when the class is created.

It tells the descriptor which attribute name it has been assigned to.

Example

```python
class Product:

    price = PositiveNumber()
```

Python effectively executes

```python
descriptor.__set_name__(
    Product,
    "price"
)
```

This allows the descriptor to know it manages the `price` attribute.

---

# Why Use getattr() and setattr()?

Notice

```python
setattr(
    instance,
    self.storage_name,
    value
)
```

instead of

```python
instance.price = value
```

Why?

Writing

```python
instance.price = value
```

would call the descriptor again,

creating infinite recursion.

Using a different internal attribute avoids this problem.

---

# Data vs Non-Data Descriptors

This is a favourite interview topic.

---

# Non-Data Descriptor

Implements

```python
__get__()
```

only.

Example

```python
class Example:

    def __get__(...):

        ...
```

---

# Data Descriptor

Implements

```python
__set__()
```

or

```python
__delete__()
```

in addition to `__get__()`.

Example

```python
class Example:

    def __get__(...):

        ...

    def __set__(...):

        ...
```

---

# Why Does This Matter?

Because Python gives them different priorities during attribute lookup.

Data descriptors have higher priority than instance attributes.

Non-data descriptors do not.

---

# Attribute Lookup Order

When Python evaluates

```python
user.name
```

it follows this order.

```
1. Data Descriptor

↓

2. Instance Dictionary

↓

3. Non-Data Descriptor

↓

4. Class Dictionary

↓

5. Parent Classes
```

Understanding this explains many "strange" attribute behaviours.

---

# Example

```python
class Descriptor:

    def __get__(
        self,
        instance,
        owner
    ):

        return "Descriptor"
```

```python
class User:

    name = Descriptor()
```

```python
user = User()

user.__dict__["name"] = "Instance"

print(user.name)
```

Output

```
Instance
```

Because this descriptor is **non-data**, the instance attribute wins.

---

Now implement `__set__()`.

```python
class Descriptor:

    def __get__(...):

        ...

    def __set__(...):

        ...
```

Now

```python
print(user.name)
```

returns the descriptor's value.

The data descriptor now takes priority.

---

# How @property Works

When you write

```python
class Product:

    @property
    def price(self):

        return self._price
```

Python approximately creates

```python
price = property(price)
```

The `property` object itself implements

- `__get__()`
- `__set__()`
- `__delete__()`

which makes it a **data descriptor**.

This is why

```python
product.price
```

automatically calls the property's getter.

---

# Built-in Descriptors

Many Python features are descriptors.

Examples

```python
@property
```

```python
classmethod
```

```python
staticmethod
```

Functions inside classes

```python
def hello():

    ...
```

ORM fields

```
Column()

Field()

ForeignKey()
```

Validation frameworks

```
Pydantic

attrs

SQLAlchemy
```

Descriptors are everywhere.

---

# Production Example - Validation

Imagine an application where many models contain email addresses.

```python
class Email:

    ...
```

Instead of repeating validation,

a descriptor validates every assignment automatically.

```python
user.email = ...

employee.email = ...

customer.email = ...
```

One implementation serves every class.

---

# Production Example - ORM

ORMs like SQLAlchemy don't store fields directly.

Instead,

they expose descriptors.

When you write

```python
user.name
```

Python doesn't simply return an attribute.

The ORM descriptor may:

- Track changes
- Perform lazy loading
- Validate values
- Mark objects as dirty

This is one reason ORMs feel "magical."

---

# Production Example - Lazy Loading

Suppose loading a profile requires a database query.

A descriptor can delay that work.

```python
user.profile
```

The first access

- queries the database
- caches the result

Later accesses return the cached value.

The caller never knows a descriptor is involved.

---

# Common Mistakes

## Mistake 1

Storing values inside the descriptor object.

```python
self.value = value
```

One descriptor instance is shared across all objects.

Store values on the instance instead.

---

## Mistake 2

Writing

```python
instance.attribute = value
```

inside `__set__()`.

This causes infinite recursion.

Use `setattr()` with a different internal attribute name.

---

## Mistake 3

Using descriptors when a simple property is sufficient.

Descriptors are powerful,

but they also add complexity.

---

# Best Practices

✅ Use descriptors when behaviour is reused across many classes.

✅ Keep descriptors focused on one responsibility.

✅ Use `__set_name__()` to avoid hardcoding attribute names.

✅ Store values on the instance, not the descriptor.

❌ Don't use descriptors for one-off validation.

❌ Don't over-engineer simple classes.

---

# Production Insight

Descriptors form the foundation of many advanced Python libraries.

Examples include:

- SQLAlchemy ORM columns
- Django model fields
- Pydantic model fields
- Properties
- Bound methods
- Cached attributes

Understanding descriptors explains why these frameworks can intercept attribute access without changing Python syntax.

Many senior Python developers use descriptors rarely,

but they benefit from understanding them because so many libraries depend on them.

---

# Interview Deep Dive

### Interviewer

> What is a descriptor?

### Answer

A descriptor is an object that defines one or more of `__get__()`, `__set__()` or `__delete__()` to customise how another object's attributes are accessed, assigned or deleted.

---

### Interviewer

> What is the descriptor protocol?

### Answer

The descriptor protocol consists of the methods `__get__()`, `__set__()` and `__delete__()`. Implementing these methods allows an object to participate in Python's attribute access mechanism.

---

### Interviewer

> What is the difference between a data descriptor and a non-data descriptor?

### Answer

A data descriptor implements `__set__()` or `__delete__()` in addition to `__get__()`. It takes precedence over instance attributes during attribute lookup. A non-data descriptor implements only `__get__()` and has lower priority than instance attributes.

---

### Interviewer

> How does `@property` use descriptors?

### Answer

The `property` class is itself a descriptor. It implements the descriptor protocol so that reading, writing or deleting an attribute invokes the corresponding property methods.

---

# Practical Lesson

Create a file:

```
descriptors_examples.py
```

```python
class PositiveInteger:

    def __set_name__(self, owner, name):

        self.storage_name = "_" + name

    def __get__(self, instance, owner):

        if instance is None:
            return self

        return getattr(
            instance,
            self.storage_name
        )

    def __set__(self, instance, value):

        if value <= 0:

            raise ValueError(
                "Value must be positive."
            )

        setattr(
            instance,
            self.storage_name,
            value
        )


class Product:

    stock = PositiveInteger()

    def __init__(self, stock):

        self.stock = stock


product = Product(25)

print(product.stock)

product.stock = 40

print(product.stock)
```

Expected Output

```
25

40
```

Now try

```python
product.stock = -5
```

Observe the validation error generated by the descriptor.

---

# Interview Questions

## Question 1

What is a descriptor?

### Answer

A descriptor is an object that customises attribute access by implementing one or more methods from the descriptor protocol.

---

## Question 2

What methods make up the descriptor protocol?

### Answer

`__get__()`, `__set__()` and `__delete__()`.

---

## Question 3

What is the purpose of `__set_name__()`?

### Answer

It allows a descriptor to discover the attribute name it is assigned to when the owning class is created.

---

## Question 4

What is the difference between a data descriptor and a non-data descriptor?

### Answer

A data descriptor implements `__set__()` or `__delete__()` and takes priority over instance attributes. A non-data descriptor implements only `__get__()` and has lower lookup priority.

---

## Question 5

Why don't most Python developers write descriptors every day?

### Answer

Because higher-level features such as `@property`, dataclasses and ORMs already use descriptors internally. Developers benefit more from understanding descriptors than from writing them frequently.

---

# Assignment

## Exercise 1

Create a `PositiveFloat` descriptor.

Use it to validate:

- Product price
- Employee salary
- Account balance

---

## Exercise 2

Create a descriptor that automatically converts assigned strings to uppercase.

Example

```python
user.country = "india"
```

Should store

```
INDIA
```

---

## Exercise 3

Create an `EmailDescriptor` that validates an email address contains exactly one `@` before storing it.

---

## Exercise 4

Explain the attribute lookup order for the following expression:

```python
user.name
```

Describe each step Python performs before returning the value.

---

# Summary

In this lesson, you learned:

- ✅ What descriptors are and why they exist.
- ✅ The descriptor protocol (`__get__()`, `__set__()`, `__delete__()`).
- ✅ The role of `__set_name__()`.
- ✅ The difference between data and non-data descriptors.
- ✅ Python's attribute lookup order.
- ✅ How `@property` is implemented internally.
- ✅ Why descriptors power frameworks like SQLAlchemy and Pydantic.
- ✅ Best practices for designing reusable attribute behaviour.

---

# What's Next

**File:**

`python/python-advanced-21-slots.md`

Topics:

- Why `__slots__` Exists
- Object Memory Layout
- `__dict__` vs `__slots__`
- Memory Optimisation
- Performance Considerations
- Inheritance with `__slots__`
- Weak References
- Dataclasses with Slots
- Production Examples
- Interview Questions

> **Note:** `__slots__` is the final major Advanced OOP topic before we move into Python's standard-library power tools (`functools`, `itertools`, `collections`, etc.). By now, you have all the background—attribute lookup, descriptors and object internals—to fully understand why `__slots__` works.
