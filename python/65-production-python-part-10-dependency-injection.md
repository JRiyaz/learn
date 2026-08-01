# File: python/64-production-python-part-10-dependency-injection.md

# Production Python

# Part 9: Dependency Injection – Building Loosely Coupled and Testable Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 64
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What Dependency Injection (DI) is
- Why Dependency Injection exists
- Dependency vs Dependency Injection
- Tight coupling vs loose coupling
- Constructor Injection
- Method Injection
- Interface-based design
- Manual Dependency Injection
- Dependency Injection Containers
- Dependency Injection in FastAPI
- Common anti-patterns
- Production best practices

______________________________________________________________________

# Recap

As applications grow, classes begin to depend on other classes.

For example:

```
Order API

↓

Order Service

↓

Payment Service

↓

Email Service

↓

Database
```

The question is:

**Who should create these objects?**

Many beginners write code like this:

```python
class UserService:

    def __init__(self):

        self.repository = UserRepository()
```

Although this works, it creates a hidden problem:

**`UserService` is now responsible for creating its own dependencies.**

______________________________________________________________________

# What is a Dependency?

A dependency is simply **another object that a class needs to perform its work.**

Example:

```python
class UserService:

    def __init__(self):

        self.repository = UserRepository()
```

Here:

```
UserService

↓

UserRepository
```

`UserRepository` is a dependency.

______________________________________________________________________

# What is Dependency Injection?

Dependency Injection means:

> **Instead of creating dependencies inside a class, provide them from the outside.**

Instead of this:

```python
class UserService:

    def __init__(self):

        self.repository = UserRepository()
```

Do this:

```python
class UserService:

    def __init__(

        self,

        repository

    ):

        self.repository = repository
```

Now the service no longer decides **which repository** to use.

Someone else supplies it.

______________________________________________________________________

# Why is This Better?

Without Dependency Injection:

```
UserService

↓

Creates

↓

UserRepository
```

With Dependency Injection:

```
Application Startup

↓

Create Repository

↓

Inject Repository

↓

UserService
```

Responsibilities are separated.

______________________________________________________________________

# Tight Coupling

Suppose we have:

```python
class EmailService:

    ...
```

```python
class UserService:

    def __init__(self):

        self.email = EmailService()
```

Problems:

- Cannot replace `EmailService`.
- Difficult to test.
- Hard to reuse.
- Hidden dependencies.

This is called **tight coupling**.

______________________________________________________________________

# Loose Coupling

Instead:

```python
class UserService:

    def __init__(

        self,

        email_service

    ):

        self.email = email_service
```

Now we can provide:

- Real email service
- Fake email service
- Test email service
- Mock email service

without changing `UserService`.

______________________________________________________________________

# Constructor Injection

The most common form of Dependency Injection.

```python
class UserService:

    def __init__(

        self,

        repository,

        email_service

    ):

        self.repository = repository

        self.email_service = email_service
```

Dependencies are required before the object can be used.

This is the preferred approach in most backend applications.

______________________________________________________________________

# Method Injection

Sometimes a dependency is only needed temporarily.

```python
class ReportService:

    def generate(

        self,

        exporter

    ):

        exporter.export()
```

The dependency is supplied only for that method call.

______________________________________________________________________

# Interface-Based Design

Imagine two repositories.

```python
PostgresRepository
```

```python
MongoRepository
```

Both expose:

```python
save()

find()

delete()
```

`UserService` should depend on **behaviour**, not a specific implementation.

Conceptually:

```
UserService

↓

Repository Interface

↓

PostgresRepository

or

MongoRepository
```

In Python, this is commonly achieved using:

- Abstract Base Classes
- Protocols (covered in the previous lesson)

______________________________________________________________________

# Manual Dependency Injection

Most small applications perform Dependency Injection manually.

```python
repository = UserRepository()

email = EmailService()

service = UserService(

    repository,

    email
)
```

This is perfectly acceptable for many projects.

Not every application requires a Dependency Injection framework.

______________________________________________________________________

# Dependency Injection Container

As applications grow:

```
Repository

↓

Service

↓

API

↓

Authentication

↓

Cache

↓

Logger

↓

Configuration
```

Managing object creation manually becomes repetitive.

A Dependency Injection container can:

- Create objects.
- Resolve dependencies.
- Manage object lifetimes.

Many languages have mature DI frameworks.

Python often relies on manual DI or lightweight libraries.

______________________________________________________________________

# Dependency Injection in FastAPI

FastAPI provides built-in Dependency Injection.

Example:

```python
from fastapi import Depends


def get_repository():

    return UserRepository()


@app.get("/users")

def get_users(

    repository = Depends(

        get_repository

    )

):

    ...
```

FastAPI creates and injects the dependency automatically.

We will explore this in detail during the FastAPI module.

______________________________________________________________________

# Testing with Dependency Injection

Without DI:

```python
UserService

↓

Real Database
```

Unit testing becomes difficult.

With DI:

```
UserService

↓

Fake Repository
```

Example:

```python
class FakeRepository:

    def get_user(

        self,

        user_id

    ):

        return {

            "id": user_id,

            "name": "Test"

        }
```

```python
service = UserService(

    FakeRepository()
)
```

The service can now be tested without a real database.

______________________________________________________________________

# Lifetime Management

Not every dependency should be recreated repeatedly.

Some objects should exist only once.

Examples:

- Configuration
- Logger
- Database connection pool

Others may be created per request.

Examples:

- Request context
- Database session
- Transaction

Managing these lifetimes is one responsibility of Dependency Injection frameworks.

______________________________________________________________________

# Backend Example

```
HTTP Request

↓

Router

↓

OrderService

↓

OrderRepository

↓

PostgreSQL
```

Application startup:

```python
repository = OrderRepository()

service = OrderService(

    repository
)
```

Each incoming request reuses the already-created service.

Object creation is centralised.

______________________________________________________________________

# Service Locator (Anti-Pattern)

Avoid code like:

```python
repository = Container.get(

    "repository"
)
```

inside business logic.

The class now secretly depends on a global container.

Its dependencies are hidden.

Constructor Injection makes dependencies explicit.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating dependencies inside constructors.

______________________________________________________________________

## Mistake 2

Using global singleton objects everywhere.

______________________________________________________________________

## Mistake 3

Injecting too many dependencies.

If a class requires:

```
12 dependencies
```

it may have too many responsibilities.

______________________________________________________________________

## Mistake 4

Using a Dependency Injection framework for a very small application.

Manual Dependency Injection is often simpler.

______________________________________________________________________

## Mistake 5

Confusing Dependency Injection with Inversion of Control.

Dependency Injection is one technique for achieving Inversion of Control.

______________________________________________________________________

# Best Practices

✅ Prefer Constructor Injection.

✅ Keep dependencies explicit.

✅ Depend on abstractions rather than implementations.

✅ Use Dependency Injection to improve testing.

✅ Centralise object creation.

❌ Don't create dependencies inside business logic.

❌ Don't overuse Dependency Injection frameworks.

______________________________________________________________________

# Production Insight

Most modern backend frameworks use Dependency Injection.

Examples include:

- FastAPI
- ASP.NET Core
- Spring Boot
- NestJS

Dependency Injection enables:

- Easier testing
- Better modularity
- Clearer architecture
- Flexible implementations
- Reduced coupling

In Python, many production applications successfully use **manual Dependency Injection** combined with thoughtful object
composition rather than large DI frameworks.

______________________________________________________________________

# Questions

### Question

> What is Dependency Injection?

### Answer

It is the practice of providing dependencies to an object from the outside instead of allowing the object to create them
itself.

______________________________________________________________________

### Question

> Why is Constructor Injection preferred?

### Answer

It makes dependencies explicit and ensures an object cannot be created without everything it requires.

______________________________________________________________________

### Question

> Why does Dependency Injection improve testing?

### Answer

Because dependencies can easily be replaced with fake or mock implementations without modifying the class being tested.

______________________________________________________________________

### Question

> Does every Python application need a Dependency Injection framework?

### Answer

No. Manual Dependency Injection is sufficient for many applications and is often simpler.

______________________________________________________________________

### Question

> What is tight coupling?

### Answer

It occurs when a class directly creates or depends on specific implementations, making replacement, testing, and
maintenance more difficult.

______________________________________________________________________

# Practical Lesson

Create the following structure:

```text
app/

├── repository.py

├── service.py

├── api.py

└── main.py
```

Implement:

- `BookRepository`
- `BookService`

First:

```python
BookService()

↓

Creates BookRepository()
```

Then refactor it to:

```python
repository = BookRepository()

service = BookService(

    repository
)
```

Finally, create a `FakeBookRepository` and verify that `BookService` works without any code changes.

______________________________________________________________________

# Knowledge Check

## Question 1

Why is Dependency Injection considered a design principle rather than a framework feature?

### Answer

Because it is a way of organising object creation and dependencies. Frameworks may support it, but it can be implemented
manually.

______________________________________________________________________

## Question 2

What problem does Dependency Injection solve?

### Answer

It reduces coupling by separating object creation from object behaviour, making systems easier to maintain and test.

______________________________________________________________________

## Question 3

When is manual Dependency Injection preferable?

### Answer

For small to medium-sized applications where explicit object creation remains simple and easy to understand.

______________________________________________________________________

## Question 4

Why should business logic depend on abstractions?

### Answer

Depending on abstractions allows implementations to change without affecting the business logic.

______________________________________________________________________

## Question 5

What is the Service Locator anti-pattern?

### Answer

It hides dependencies by allowing classes to fetch them from a global container, making the code harder to understand,
test, and maintain.

______________________________________________________________________

# Assignment

## Exercise 1

Refactor one of your existing Flask or FastAPI projects to use Constructor Injection instead of creating dependencies
inside services.

______________________________________________________________________

## Exercise 2

Replace one repository with a fake implementation and verify that the service behaves identically.

______________________________________________________________________

## Exercise 3

Draw the dependency graph of one of your backend projects.

Identify which objects should be created once and which should be created per request.

______________________________________________________________________

## Exercise 4

Review your service classes.

If any service has more than five constructor dependencies, evaluate whether it is taking on too many responsibilities
and suggest a refactoring.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What Dependency Injection is.
- ✅ Dependencies vs Dependency Injection.
- ✅ Tight coupling vs loose coupling.
- ✅ Constructor and Method Injection.
- ✅ Interface-based design.
- ✅ Manual Dependency Injection.
- ✅ Dependency Injection containers.
- ✅ Dependency Injection in FastAPI.
- ✅ Production best practices.

______________________________________________________________________

# Next Lesson

**File:** [66-production-python-part-11-profiling.md](66-production-python-part-11-profiling.md)
