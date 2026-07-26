# File: python/python-advanced-13-enums.md

# Python Advanced - Lesson 13
# Enums - Creating Meaningful Constants in Python

> **Course:** Backend Engineering Roadmap
>
> **Module:** Python Object Model & Memory
>
> **Lesson:** 13
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 80 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why Enums exist
- Problems with magic values
- Creating Enums
- Enum members
- Enum values
- Enum names
- `auto()`
- `IntEnum`
- `StrEnum`
- `Flag` and `IntFlag`
- Enum vs constants
- Production use cases
- Interview questions

---

# Why Do Enums Exist?

Imagine you're building an Order Management System.

Without enums, you might write:

```python
status = "PENDING"

if status == "PENDING":
    print("Waiting for payment")
```

Later someone writes:

```python
status = "pending"
```

or

```python
status = "Pending"
```

or

```python
status = "PENDNG"
```

Notice the typo.

Python won't stop you.

Your program may now behave incorrectly.

---

# Another Common Example

Some developers use integers.

```python
status = 1
```

Later,

```python
if status == 3:
    ...
```

What does `3` mean?

- Pending?
- Delivered?
- Cancelled?

Nobody knows without documentation.

These are called **magic values**.

---

# What Are Magic Values?

Magic values are numbers or strings whose meaning isn't immediately obvious.

Examples

```python
status == 4

priority == 2

role == "A"
```

Good code should be self-explanatory.

Enums solve this problem.

---

# Introducing Enum

Python provides the `enum` module.

```python
from enum import Enum
```

Create an enum.

```python
from enum import Enum


class OrderStatus(Enum):

    PENDING = "PENDING"

    PAID = "PAID"

    SHIPPED = "SHIPPED"

    DELIVERED = "DELIVERED"
```

Usage

```python
status = OrderStatus.PENDING

print(status)
```

Output

```
OrderStatus.PENDING
```

---

# Accessing Values

Each enum member has two important attributes.

```python
print(status.name)

print(status.value)
```

Output

```
PENDING

PENDING
```

If values were integers,

```python
class Status(Enum):

    PENDING = 1

    PAID = 2
```

Then

```python
print(Status.PAID.name)

print(Status.PAID.value)
```

Output

```
PAID

2
```

---

# Comparing Enums

Always compare enum members.

```python
if status == OrderStatus.PENDING:

    print("Waiting")
```

Avoid

```python
if status.value == "PENDING":
```

Using enum members is safer and more readable.

---

# Iterating Over Enums

Enums are iterable.

```python
for status in OrderStatus:

    print(status)
```

Output

```
OrderStatus.PENDING

OrderStatus.PAID

OrderStatus.SHIPPED

OrderStatus.DELIVERED
```

---

# auto()

Sometimes the actual value doesn't matter.

Python can assign values automatically.

```python
from enum import Enum, auto


class Priority(Enum):

    LOW = auto()

    MEDIUM = auto()

    HIGH = auto()
```

Output

```python
print(Priority.LOW.value)

print(Priority.HIGH.value)
```

```
1

3
```

---

# Why Use auto()?

Suppose you insert another priority.

Without `auto()`:

```python
LOW = 1

MEDIUM = 2

HIGH = 3

CRITICAL = 4
```

Every value must be updated manually.

With `auto()`:

```python
LOW = auto()

MEDIUM = auto()

HIGH = auto()

CRITICAL = auto()
```

Python handles numbering automatically.

---

# IntEnum

Sometimes an enum must behave like an integer.

Python provides:

```python
from enum import IntEnum
```

Example

```python
from enum import IntEnum


class HTTPStatus(IntEnum):

    OK = 200

    NOT_FOUND = 404
```

Usage

```python
print(HTTPStatus.OK == 200)
```

Output

```
True
```

Unlike `Enum`,

`IntEnum` behaves as an integer.

---

# Enum vs IntEnum

Normal Enum

```python
Status.SUCCESS == 1
```

Output

```
False
```

IntEnum

```python
Status.SUCCESS == 1
```

Output

```
True
```

Use `IntEnum` only when integer compatibility is required.

---

# StrEnum

Python 3.11 introduced `StrEnum`.

```python
from enum import StrEnum
```

Example

```python
from enum import StrEnum


class Environment(StrEnum):

    DEVELOPMENT = "development"

    STAGING = "staging"

    PRODUCTION = "production"
```

Usage

```python
print(Environment.PRODUCTION)
```

Output

```
production
```

It behaves like both a string and an enum.

---

# Flag

Sometimes multiple values should be combined.

Example:

A user may have multiple permissions.

- Read
- Write
- Execute

Python provides `Flag`.

```python
from enum import Flag, auto


class Permission(Flag):

    READ = auto()

    WRITE = auto()

    EXECUTE = auto()
```

Combine permissions.

```python
permission = (
    Permission.READ |
    Permission.WRITE
)
```

Check permissions.

```python
if Permission.READ in permission:

    print("Can Read")
```

Output

```
Can Read
```

---

# IntFlag

`IntFlag` behaves similarly to `Flag`

but also behaves like an integer.

Useful when working with:

- Operating systems
- Bitmasks
- Low-level APIs

---

# Enum vs Constants

Many beginners write:

```python
PENDING = "PENDING"

PAID = "PAID"

SHIPPED = "SHIPPED"
```

This works.

But there is no grouping.

There is no validation.

Typos are still possible.

Enums provide:

- Better organisation
- Type safety
- Autocompletion
- Easier maintenance

---

# Production Example - Payment Status

```python
from enum import Enum


class PaymentStatus(Enum):

    PENDING = "PENDING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    REFUNDED = "REFUNDED"
```

Usage

```python
def process_payment(status):

    if status == PaymentStatus.SUCCESS:

        print("Deliver Product")
```

This is much safer than comparing raw strings.

---

# Production Example - FastAPI

Enums work naturally with FastAPI.

```python
class UserRole(StrEnum):

    ADMIN = "admin"

    CUSTOMER = "customer"

    SELLER = "seller"
```

A request model might contain:

```python
role: UserRole
```

Only valid roles are accepted.

Invalid values produce validation errors automatically.

---

# Production Example - SQLAlchemy

Database models often store enum values.

```python
class OrderStatus(Enum):

    PENDING = "PENDING"

    SHIPPED = "SHIPPED"

    DELIVERED = "DELIVERED"
```

Business logic becomes much easier to read.

```python
if order.status == OrderStatus.SHIPPED:

    notify_customer()
```

---

# Best Practices

✅ Use enums for fixed sets of values.

✅ Prefer `StrEnum` for APIs and JSON.

✅ Use `auto()` when the numeric value is unimportant.

✅ Group related constants into enums.

❌ Don't compare against raw strings.

❌ Don't use enums for values that change dynamically.

---

# Interview Deep Dive

### Interviewer

> Why should enums be used instead of string constants?

### Answer

Enums provide meaningful names, improve readability, reduce typographical errors, enable IDE autocompletion and group related constants into a single type.

---

### Interviewer

> What is the difference between `Enum` and `IntEnum`?

### Answer

`Enum` members are compared only with other members of the same enum, while `IntEnum` members also behave like integers and can be compared directly with integer values.

---

### Interviewer

> When should you use `auto()`?

### Answer

Use `auto()` when the actual numeric value is not important. It allows Python to assign values automatically, making enums easier to maintain.

---

# Practical Lesson

Create a file:

```
enum_examples.py
```

```python
from enum import Enum


class TicketStatus(Enum):

    OPEN = "OPEN"

    IN_PROGRESS = "IN_PROGRESS"

    CLOSED = "CLOSED"


ticket = TicketStatus.OPEN

print(ticket)

print(ticket.name)

print(ticket.value)
```

Expected Output

```
TicketStatus.OPEN

OPEN

OPEN
```

Now iterate through all statuses.

```python
for status in TicketStatus:

    print(status.name)
```

---

# Interview Questions

## Question 1

Why were enums introduced?

### Answer

Enums provide meaningful, type-safe names for fixed sets of constants, making code easier to read and maintain.

---

## Question 2

What is the difference between `.name` and `.value`?

### Answer

`.name` returns the enum member's identifier, while `.value` returns the associated value assigned to that member.

---

## Question 3

When should you use `StrEnum`?

### Answer

Use `StrEnum` when enum values need to behave like strings, such as in APIs, JSON payloads or configuration values.

---

## Question 4

What is `Flag` used for?

### Answer

`Flag` allows multiple enum members to be combined using bitwise operators, making it useful for permissions and feature flags.

---

## Question 5

Why is `auto()` useful?

### Answer

It automatically assigns values to enum members, reducing manual work and preventing numbering mistakes.

---

# Assignment

## Exercise 1

Create an enum called `TrafficLight` with:

- RED
- YELLOW
- GREEN

Print the name and value of each member.

---

## Exercise 2

Create an `IntEnum` representing HTTP status codes.

Compare an enum member with its corresponding integer.

---

## Exercise 3

Create a `Permission` enum using `Flag`.

Combine multiple permissions and check whether a specific permission is present.

---

## Exercise 4

Replace the following string constants with an enum.

```python
ROLE_ADMIN = "admin"

ROLE_USER = "user"

ROLE_MANAGER = "manager"
```

Rewrite the application logic to use enum members instead of raw strings.

---

# Summary

In this lesson, you learned:

- ✅ Why enums exist.
- ✅ How enums eliminate magic values.
- ✅ How to create and use enums.
- ✅ The difference between `.name` and `.value`.
- ✅ How `auto()` simplifies enum definitions.
- ✅ The differences between `Enum`, `IntEnum`, `StrEnum`, `Flag` and `IntFlag`.
- ✅ Production use cases in backend systems.
- ✅ Best practices for writing maintainable code.

---

# Module Complete 🎉

You have now completed **Module 1 – Python Object Model & Memory**.

You have covered:

- ✅ Memory Management & Object Model
- ✅ Reference Counting
- ✅ Garbage Collection
- ✅ Shallow vs Deep Copy
- ✅ Mutable Default Arguments
- ✅ Small Integer Caching
- ✅ Interning
- ✅ LEGB Scope
- ✅ Closures
- ✅ Decorators
- ✅ First-Class Functions
- ✅ Higher-Order Functions
- ✅ Lambda Functions
- ✅ Iterators
- ✅ Iterator Protocol
- ✅ Generators
- ✅ Generator Expressions
- ✅ Context Managers
- ✅ Magic Methods
- ✅ Dataclasses
- ✅ NamedTuple
- ✅ Enums

---

# What's Next

**File:**

`python/python-advanced-14-inheritance.md`

Topics:

- Why Inheritance Exists
- Parent vs Child Classes
- Method Overriding
- `super()`
- The `is-a` Relationship
- When to Use (and Avoid) Inheritance
- Production Examples
- Interview Questions
