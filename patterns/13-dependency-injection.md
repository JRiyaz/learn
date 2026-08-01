# Software Design & Design Patterns - Part 13

# Dependency Injection (DI)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Dependency Injection (DI) is
- Why Dependency Injection exists
- The problems it solves
- The different types of Dependency Injection
- Real-world backend examples
- FastAPI examples
- How DI works internally
- Why almost every modern framework uses DI

______________________________________________________________________

# Before We Start

In the previous lesson,

we learned the **Dependency Inversion Principle (DIP)**.

DIP told us:

> Depend on abstractions instead of concrete implementations.

But one question remained.

> **Who creates those implementations?**

For example,

if `LibraryService` depends on a `NotificationService`,

who creates the `EmailService` object?

Who passes it to `LibraryService`?

That is exactly what **Dependency Injection** solves.

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

We have a repository.

```python
class BookRepository:

    def save(
        self,
        book,
    ):
        print("Book Saved")
```

Our service uses it.

```python
class LibraryService:

    def __init__(self):

        self.repository = BookRepository()

    def add_book(
        self,
        book,
    ):

        self.repository.save(book)
```

Everything works.

______________________________________________________________________

# New Requirement

The company decides

to migrate from

PostgreSQL

to

MongoDB.

Where do we change the code?

Inside

```python
LibraryService
```

Again.

______________________________________________________________________

# Another Requirement

Now,

for testing,

we don't want

a real database.

We want

a fake repository.

Again,

we modify

`LibraryService`.

______________________________________________________________________

# What's the Problem?

The business logic

keeps creating

its own dependencies.

```python
self.repository = BookRepository()
```

This causes

tight coupling.

The service

decides

what database

to use.

But...

Should it?

No.

Its job is

to manage books,

not create databases.

______________________________________________________________________

# What Is a Dependency?

Anything

your class

needs

to perform its work

is called

a **dependency**.

For example,

our

`LibraryService`

depends on:

- Repository
- Logger
- Cache
- Notification Service
- Event Publisher

Without them,

it cannot perform

its work.

______________________________________________________________________

# What Is Dependency Injection?

Dependency Injection means:

> **Instead of creating dependencies inside a class, provide them from outside.**

The class

receives

what it needs.

It doesn't create it.

______________________________________________________________________

# Without Dependency Injection

```python
class LibraryService:

    def __init__(self):

        self.repository = BookRepository()
```

The service

creates

its own dependency.

______________________________________________________________________

# With Dependency Injection

```python
class LibraryService:

    def __init__(
        self,
        repository,
    ):
        self.repository = repository
```

Now,

someone else

creates

the repository

and passes it in.

This is

Dependency Injection.

______________________________________________________________________

# Who Performs the Injection?

Usually,

another part

of the application.

Example

```python
repository = BookRepository()

service = LibraryService(
    repository
)
```

Notice something.

The service

never creates

the repository.

It simply

uses it.

______________________________________________________________________

# Why Is This Better?

Tomorrow,

replace

```text
BookRepository
```

with

```text
MongoRepository
```

Only this line changes.

```python
service = LibraryService(
    MongoRepository()
)
```

The service

remains unchanged.

______________________________________________________________________

# Another Example

Suppose

we have

notifications.

```python
class NotificationService:

    def send(self):
        ...
```

Inject

the implementation.

```python
service = LibraryService(

    repository,

    EmailService(),
)
```

Tomorrow

```python
SlackService()
```

No changes

inside

LibraryService.

______________________________________________________________________

# Dependency Injection in FastAPI

FastAPI

uses DI

every day.

Example

```python
@app.get("/books")
def get_books(

    db=Depends(get_db),

):
    ...
```

Where did

`db`

come from?

You didn't create it.

FastAPI did.

It injected

the dependency.

______________________________________________________________________

# Another FastAPI Example

Suppose

your service

needs

three dependencies.

```python
class LibraryService:

    def __init__(

        self,

        repository,

        logger,

        cache,

    ):
        ...
```

FastAPI

can automatically

construct

this object

by resolving

each dependency.

This is one reason

FastAPI applications

remain clean

as they grow.

______________________________________________________________________

# Types of Dependency Injection

There are

three common types.

______________________________________________________________________

## 1. Constructor Injection

Dependencies

are passed

through

the constructor.

```python
class Service:

    def __init__(
        self,
        repository,
    ):
        self.repository = repository
```

This is

the most common

and recommended approach.

______________________________________________________________________

## 2. Method Injection

Dependencies

are passed

to a method.

```python
class Service:

    def export(

        self,

        exporter,

    ):

        exporter.export()
```

Useful

when a dependency

is needed

only for

one operation.

______________________________________________________________________

## 3. Property Injection

Dependencies

are assigned

after

the object

is created.

```python
service.logger = Logger()
```

Python allows it,

but it's

less common

because the object

may exist

in an incomplete state.

______________________________________________________________________

# Real Backend Example

Suppose

our application

uploads files.

Instead of

creating

an S3 client

inside

the service,

inject it.

```python
class FileService:

    def __init__(
        self,
        storage,
    ):
        self.storage = storage
```

Tomorrow,

switch to

Azure Blob Storage.

No changes

inside

FileService.

______________________________________________________________________

# Why DI Makes Testing Easy

Without DI

you need

a real database.

With DI

you can inject

a fake repository.

```python
class FakeRepository:

    def save(
        self,
        book,
    ):
        print(
            "Fake Save"
        )
```

Test

```python
service = LibraryService(
    FakeRepository()
)
```

No database.

No network.

Fast tests.

This is one of

the biggest reasons

companies

love Dependency Injection.

______________________________________________________________________

# How FastAPI Works Internally

When a request arrives,

FastAPI roughly performs

these steps.

```text
HTTP Request

↓

Find Endpoint

↓

Resolve Dependencies

↓

Create Objects

↓

Call Endpoint

↓

Return Response
```

This entire process

happens automatically.

______________________________________________________________________

# DI and SOLID

Dependency Injection

helps implement

multiple SOLID principles.

| Principle | Benefit |
| --------- | ----------------------------------- |
| SRP | Classes focus on business logic |
| OCP | Swap implementations easily |
| DIP | Dependencies come from abstractions |

DI

works hand-in-hand

with SOLID.

______________________________________________________________________

# Does Python Need a DI Framework?

Usually,

no.

Unlike Java,

Python's simplicity

means

manual constructor injection

is often enough.

FastAPI

already provides

excellent DI support.

Large applications

may use

specialized DI containers,

but many production systems

don't need them.

______________________________________________________________________

# When NOT to Use Dependency Injection

Suppose

you're writing

a 50-line script.

Creating

dependency containers,

factories,

and interfaces

would be unnecessary.

DI provides value

when applications

grow

and dependencies

become numerous.

______________________________________________________________________

# Best Practices

✅ Prefer constructor injection.

✅ Keep object creation outside business classes.

✅ Inject abstractions when possible.

✅ Keep dependencies explicit.

______________________________________________________________________

# Common Mistakes

### Creating Dependencies Inside Classes

Bad

```python
self.repository = BookRepository()
```

Always ask,

"Can this dependency

be provided

from outside?"

______________________________________________________________________

### Too Many Hidden Dependencies

If a class

requires

15 dependencies,

it may be

doing too much.

That's often

an SRP issue.

______________________________________________________________________

### Confusing DI with Frameworks

Dependency Injection

is a design technique,

not a FastAPI feature.

FastAPI simply

automates it.

______________________________________________________________________

### Using Global Objects Everywhere

Global dependencies

make testing

and maintenance

more difficult.

Prefer injection.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Dependency Injection, and why is it useful?

Dependency Injection is a design technique where a class receives its dependencies from an external source instead of
creating them internally. This reduces coupling, improves testability, and makes it easy to replace implementations such
as databases, storage providers, or notification services. Modern frameworks like FastAPI automate dependency injection
using mechanisms such as `Depends()`, allowing developers to focus on business logic rather than object creation.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Dependency Injection is
- Why it exists
- Constructor, Method, and Property Injection
- FastAPI examples
- Testing with DI
- How FastAPI resolves dependencies
- Best practices
- Common mistakes

______________________________________________________________________

# 🚀 Congratulations!

You have now completed the **OOP + SOLID Foundation**.

Everything that follows—Factory, Strategy, Repository, Decorator, Observer, Clean Architecture—will build on the
concepts you've already learned.

You'll start recognizing that most design patterns are simply different ways of applying the principles you've mastered
so far.

______________________________________________________________________

# What's Next

[Factory Pattern](14-factory-pattern.md)
