# File: python/python-advanced-18-mixins.md

# Python Advanced - Lesson 18
# Mixins - Reusing Small, Focused Behaviours

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 18
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What mixins are
- Why mixins exist
- Characteristics of a good mixin
- Mixins vs inheritance
- Mixins vs composition
- Cooperative multiple inheritance
- Real-world framework examples
- Common mistakes
- Production best practices
- Interview questions

---

# Recap

In previous lessons, we learned:

- Single inheritance
- Multiple inheritance
- Method Resolution Order (MRO)
- Composition
- Abstract Base Classes (ABC)

One major use case for multiple inheritance is **Mixins**.

Many Python frameworks use mixins extensively.

---

# What is a Mixin?

A mixin is a small class that provides one specific piece of reusable behaviour.

Unlike a normal parent class, a mixin is **not intended to represent an object**.

Instead, it represents a capability.

Think of it as adding a feature.

---

# Example

Imagine a web application.

Many models need timestamps.

```
User

↓

created_at

updated_at
```

```
Order

↓

created_at

updated_at
```

```
Invoice

↓

created_at

updated_at
```

Instead of rewriting the same code,

we create a mixin.

---

# First Mixin

```python
from datetime import datetime


class TimestampMixin:

    def set_timestamp(self):

        self.created_at = datetime.now()

        self.updated_at = datetime.now()
```

Now any class can inherit this behaviour.

```python
class User(TimestampMixin):

    pass
```

Usage

```python
user = User()

user.set_timestamp()

print(user.created_at)
```

The `User` class gained timestamp functionality without duplicating code.

---

# Why Not Use a Parent Class?

Suppose we write

```python
class Timestamp:

    ...
```

Should we say

```python
class User(Timestamp):
```

No.

A `User` **is not a** `Timestamp`.

The relationship is wrong.

Instead,

`TimestampMixin` simply contributes behaviour.

---

# A Good Mixin Has One Responsibility

A mixin should focus on **one feature**.

Good examples

```
LoggingMixin

TimestampMixin

SoftDeleteMixin

PermissionMixin

ValidationMixin

AuditMixin
```

Bad example

```
EverythingMixin
```

If a mixin performs many unrelated tasks,

it is no longer a mixin.

---

# Multiple Mixins

A class can inherit several mixins.

```python
class LoggingMixin:

    def log(self):

        print("Logging")
```

```python
class ValidationMixin:

    def validate(self):

        print("Valid")
```

```python
class UserService(

    LoggingMixin,

    ValidationMixin

):

    pass
```

Usage

```python
service = UserService()

service.log()

service.validate()
```

Output

```
Logging

Valid
```

---

# Mixins and MRO

Mixins rely on multiple inheritance.

```python
class A:

    def process(self):

        print("A")
```

```python
class LoggingMixin:

    def process(self):

        print("Logging")

        super().process()
```

```python
class Service(

    LoggingMixin,

    A

):

    pass
```

Output

```
Logging

A
```

The mixin participates in the Method Resolution Order.

---

# Cooperative Mixins

Good mixins cooperate using `super()`.

Example

```python
class AuditMixin:

    def save(self):

        print("Audit")

        super().save()
```

Another mixin

```python
class LoggingMixin:

    def save(self):

        print("Logging")

        super().save()
```

Base class

```python
class Repository:

    def save(self):

        print("Saving")
```

Final class

```python
class UserRepository(

    AuditMixin,

    LoggingMixin,

    Repository

):

    pass
```

Usage

```python
repository = UserRepository()

repository.save()
```

Output

```
Audit

Logging

Saving
```

Each class contributes one part of the operation.

---

# What Happens Without super()?

Suppose `AuditMixin` becomes

```python
class AuditMixin:

    def save(self):

        print("Audit")
```

Now

```python
repository.save()
```

Output

```
Audit
```

The chain stops.

Neither `LoggingMixin` nor `Repository` executes.

This is why cooperative inheritance is important.

---

# Mixins vs Normal Inheritance

Normal inheritance models an **is-a** relationship.

```
Vehicle

↓

Car
```

A car **is a** vehicle.

Mixins add capabilities.

```
User

↓

LoggingMixin

↓

TimestampMixin
```

A user is **not** a logging system.

The mixins simply add behaviour.

---

# Mixins vs Composition

Suppose a service needs logging.

Composition

```python
class UserService:

    def __init__(self, logger):

        self.logger = logger
```

Mixin

```python
class LoggingMixin:

    def log(self):

        ...
```

Both are valid.

Composition injects another object.

Mixins reuse methods through inheritance.

---

# When Should You Choose a Mixin?

Use a mixin when:

- Behaviour is reusable.
- Behaviour is small.
- Behaviour is stateless or minimally stateful.
- Many unrelated classes need the same feature.

Examples

- Logging
- Validation
- Timestamping
- Permissions
- Serialisation

---

# When Should You Avoid Mixins?

Avoid mixins when:

- They require many constructor arguments.
- They contain business logic.
- They represent real domain objects.
- They maintain complex internal state.

Those situations are often better handled using composition.

---

# Production Example - Django

Django uses mixins extensively.

```
LoginRequiredMixin

PermissionRequiredMixin

UserPassesTestMixin
```

Example

```python
class DashboardView(

    LoginRequiredMixin,

    PermissionRequiredMixin,

    View

):

    ...
```

Each mixin contributes one capability.

---

# Production Example - SQLAlchemy

Common mixins include

```python
class TimestampMixin:

    created_at

    updated_at
```

```python
class SoftDeleteMixin:

    deleted_at
```

Models inherit these reusable features instead of repeating them.

---

# Production Example - FastAPI

Suppose several services need request logging.

```python
class LoggingMixin:

    def log_request(self):

        ...
```

```python
class UserService(

    LoggingMixin

):

    ...
```

Although FastAPI itself relies more heavily on dependency injection than mixins, you'll still encounter mixins in supporting libraries and larger applications.

---

# Common Mistakes

## Mistake 1

Creating huge mixins.

```
Logging

Validation

Authentication

Caching

Database

↓

One Mixin
```

This violates the Single Responsibility Principle.

---

## Mistake 2

Treating mixins like business objects.

```
CustomerMixin
```

A customer is not reusable behaviour.

This should be a normal class.

---

## Mistake 3

Not using `super()`.

Breaking the MRO prevents other mixins from participating.

---

# Best Practices

✅ Keep mixins small.

✅ Give each mixin one responsibility.

✅ Use `super()` for cooperative inheritance.

✅ Name mixins with the `Mixin` suffix.

✅ Document assumptions made by the mixin.

❌ Don't store large amounts of state.

❌ Don't create deep chains of dependent mixins.

❌ Don't replace composition with mixins everywhere.

---

# Production Insight

Large backend systems often combine several mixins.

Example

```
UserModel

↓

TimestampMixin

↓

SoftDeleteMixin

↓

AuditMixin

↓

BaseModel
```

Each mixin contributes a single feature.

Benefits include:

- Less duplicated code
- Consistent behaviour
- Easier maintenance
- Smaller classes
- Better separation of concerns

This is why Django, SQLAlchemy and many internal enterprise frameworks rely heavily on mixins.

---

# Interview Deep Dive

### Interviewer

> What is a mixin?

### Answer

A mixin is a small class designed to provide a single reusable behaviour that can be inherited by multiple unrelated classes. It is intended to add capabilities rather than model an "is-a" relationship.

---

### Interviewer

> How is a mixin different from a normal parent class?

### Answer

A normal parent class represents a domain relationship, such as `Car` inheriting from `Vehicle`. A mixin exists solely to provide reusable behaviour and is not intended to represent a standalone domain object.

---

### Interviewer

> Why do mixins typically use `super()`?

### Answer

Mixins participate in cooperative multiple inheritance. Calling `super()` ensures every class in the Method Resolution Order has an opportunity to contribute its behaviour.

---

### Interviewer

> When should you choose composition instead of a mixin?

### Answer

Choose composition when functionality depends on another object or maintains significant state. Composition creates looser coupling and is often more flexible than inheritance.

---

# Practical Lesson

Create a file:

```
mixins_examples.py
```

```python
class LoggingMixin:

    def save(self):

        print("Logging save")

        super().save()


class ValidationMixin:

    def save(self):

        print("Validation passed")

        super().save()


class Repository:

    def save(self):

        print("Saving to database")


class UserRepository(

    LoggingMixin,

    ValidationMixin,

    Repository

):

    pass


repository = UserRepository()

repository.save()
```

Expected Output

```
Logging save

Validation passed

Saving to database
```

Now change the inheritance order.

```python
class UserRepository(

    ValidationMixin,

    LoggingMixin,

    Repository

):
    pass
```

Observe how the output changes.

Finally, print the MRO.

```python
print(UserRepository.mro())
```

Notice how the inheritance order directly affects execution.

---

# Interview Questions

## Question 1

What is a mixin?

### Answer

A mixin is a small reusable class that provides one specific behaviour to multiple classes through inheritance.

---

## Question 2

Why are mixins commonly used with multiple inheritance?

### Answer

Multiple inheritance allows a class to combine several independent behaviours, each provided by a different mixin.

---

## Question 3

Why should mixins usually call `super()`?

### Answer

Calling `super()` allows cooperative multiple inheritance, ensuring every class in the MRO has an opportunity to execute.

---

## Question 4

Should a mixin represent a business entity?

### Answer

No. A mixin should represent reusable behaviour, not a domain model or business object.

---

## Question 5

When should composition be preferred over mixins?

### Answer

Composition should be preferred when behaviour depends on another object, requires significant state, or when loose coupling is more important than code reuse through inheritance.

---

# Assignment

## Exercise 1

Create:

- `LoggingMixin`
- `ValidationMixin`
- `CachingMixin`

Combine all three in a `ProductService`.

Verify the execution order using `super()`.

---

## Exercise 2

Print the MRO for your `ProductService`.

Explain why the methods execute in that order.

---

## Exercise 3

Remove one `super()` call.

Observe which methods no longer execute.

Explain why the chain breaks.

---

## Exercise 4

Build a reusable `TimestampMixin` that automatically sets:

- `created_at`
- `updated_at`

Use it in two unrelated classes:

- `User`
- `Order`

---

# Summary

In this lesson, you learned:

- ✅ What mixins are and why they exist.
- ✅ How mixins differ from traditional inheritance.
- ✅ How mixins rely on multiple inheritance and the MRO.
- ✅ Why cooperative inheritance with `super()` is essential.
- ✅ The differences between mixins and composition.
- ✅ Real-world usage in frameworks like Django and SQLAlchemy.
- ✅ Best practices for designing reusable behaviours.

---

# What's Next

**File:**

`python/python-advanced-19-class-methods-static-methods-properties.md`

Topics:

- Instance Methods
- Class Methods
- Static Methods
- `@property`
- Property Setters and Deleters
- Read-only Properties
- Choosing the Right Method Type
- Production Examples
- Interview Questions

> **Note:** These concepts are closely related and frequently used together in production code, so we'll cover them in a single comprehensive lesson before moving on to descriptors and `__slots__`.
