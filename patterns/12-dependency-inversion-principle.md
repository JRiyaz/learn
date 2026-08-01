# Software Design & Design Patterns - Part 12

# Dependency Inversion Principle (DIP)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Dependency Inversion Principle (DIP) is
- Why DIP exists
- The problem DIP solves
- High-level vs low-level modules
- What "depend on abstractions" actually means
- Real-world backend examples
- FastAPI examples
- How DIP differs from Dependency Injection (DI)
- When NOT to apply DIP

______________________________________________________________________

# Before We Start

This is probably the **most important SOLID principle** for modern backend development.

FastAPI,

Spring Boot,

ASP.NET,

NestJS,

Django,

Angular,

and many other frameworks

are heavily influenced by this principle.

If you understand DIP,

the next lesson on **Dependency Injection (DI)** will become very easy.

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

When a member borrows a book,

we send an email.

A junior developer writes:

```python
class EmailService:

    def send(
        self,
        message,
    ):
        print(
            "Email Sent"
        )
```

Then

```python
class LibraryService:

    def __init__(self):
        self.email_service = EmailService()

    def borrow_book(
        self,
        book,
    ):

        print("Book Borrowed")

        self.email_service.send(
            "Book Borrowed"
        )
```

Everything works.

______________________________________________________________________

# New Requirement

The business says

> "We no longer use Email."

Now

notifications

must be sent through

Slack.

What happens?

You modify

```python
self.email_service = EmailService()
```

to

```python
self.slack_service = SlackService()
```

______________________________________________________________________

# Another Requirement

Now

customers want

SMS.

Again,

modify

LibraryService.

______________________________________________________________________

# Another Requirement

Now

enterprise customers

want

Microsoft Teams.

Again,

modify

LibraryService.

______________________________________________________________________

# What's the Problem?

The business logic

inside

```python
LibraryService
```

keeps changing

because

notification providers

keep changing.

But...

Should borrowing books

care

whether

notifications use:

- Email?
- Slack?
- SMS?
- Teams?

No.

Those are

implementation details.

______________________________________________________________________

# Understanding High-Level and Low-Level Modules

This terminology

confuses many developers.

Let's simplify it.

## High-Level Module

Contains

business logic.

Example

```text
LibraryService
```

Its responsibility is

borrowing books.

______________________________________________________________________

## Low-Level Module

Handles

technical details.

Examples

- Email
- SMS
- Database
- Redis
- Kafka
- S3

These support

the business logic.

______________________________________________________________________

# Current Design

```text
LibraryService

↓

EmailService
```

The business logic

directly depends on

a specific implementation.

This creates

tight coupling.

______________________________________________________________________

# What Does DIP Say?

The **Dependency Inversion Principle** states:

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Again,

let's simplify it.

Instead of depending on

```text
EmailService
```

depend on

```text
NotificationService
```

The business logic

doesn't care

which notification service

is used.

______________________________________________________________________

# Step 1

Create an abstraction.

```python
from abc import (
    ABC,
    abstractmethod,
)

class NotificationService(
    ABC
):

    @abstractmethod
    def send(
        self,
        message,
    ):
        ...
```

______________________________________________________________________

# Step 2

Implement Email.

```python
class EmailService(
    NotificationService
):

    def send(
        self,
        message,
    ):
        print(
            "Email Sent"
        )
```

______________________________________________________________________

# Step 3

Implement Slack.

```python
class SlackService(
    NotificationService
):

    def send(
        self,
        message,
    ):
        print(
            "Slack Message Sent"
        )
```

______________________________________________________________________

# Step 4

Update LibraryService

```python
class LibraryService:

    def __init__(
        self,
        notification,
    ):
        self.notification = notification

    def borrow_book(
        self,
        book,
    ):

        print("Book Borrowed")

        self.notification.send(
            "Book Borrowed"
        )
```

Notice something.

LibraryService

no longer knows

whether

notifications are sent via:

- Email
- Slack
- SMS
- Teams

It simply calls

```python
notification.send(...)
```

______________________________________________________________________

# Why Is This Better?

Tomorrow,

the company introduces

WhatsApp.

Create

```python
class WhatsAppService(
    NotificationService
):
    ...
```

Does

LibraryService

change?

No.

The business logic

remains untouched.

______________________________________________________________________

# Real Backend Example

Suppose

our application

stores files.

Bad

```python
class FileService:

    def __init__(self):

        self.storage = S3Storage()
```

Now

the company migrates

to Azure.

You must modify

FileService.

______________________________________________________________________

# Better

```python
class FileService:

    def __init__(
        self,
        storage,
    ):
        self.storage = storage
```

Now

it works with:

- AWS S3
- Azure Blob
- Google Cloud Storage
- MinIO

without changing

the business logic.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

creates books.

```python
@app.post("/books")
def create_book(

    service=Depends(
        get_library_service
    ),
):
    ...
```

Where does

`service`

come from?

FastAPI

creates it

and injects

its dependencies.

The endpoint

doesn't know

which database,

logger,

or cache

is being used.

That's DIP in action.

We'll see exactly

how FastAPI does this

in the next lesson.

______________________________________________________________________

# DIP vs Dependency Injection

This is one of the

most common interview questions.

Many developers

think they're the same.

They are not.

## Dependency Inversion Principle

A **design principle**.

It says

depend on abstractions.

______________________________________________________________________

## Dependency Injection

A **technique**

used to implement DIP.

It provides

the required dependency

from outside.

Think of it like this.

```text
DIP

↓

Idea

↓

DI

↓

Implementation
```

DIP is the rule.

DI is one way

to follow the rule.

______________________________________________________________________

# Real Company Example

Suppose Netflix

changes

its recommendation engine.

The recommendation service

shouldn't know

whether

the algorithm is:

- Collaborative Filtering
- Deep Learning
- Matrix Factorization

It depends only

on an abstraction.

New algorithms

are plugged in

without changing

the business logic.

______________________________________________________________________

# Benefits of DIP

Following DIP gives you:

✅ Loose coupling

✅ Easier testing

✅ Better flexibility

✅ Easier maintenance

✅ Easier replacement of dependencies

______________________________________________________________________

# When NOT to Apply DIP

Suppose

you're writing

a small script

to send

one email.

Creating

interfaces,

factories,

and dependency injection

would be unnecessary.

Use DIP

when dependencies

are likely

to change

or need

multiple implementations.

______________________________________________________________________

# Best Practices

✅ Depend on abstractions.

✅ Keep business logic independent of infrastructure.

✅ Pass dependencies from outside.

✅ Avoid creating dependencies inside business classes.

______________________________________________________________________

# Common Mistakes

### Creating Dependencies with `new`

Bad

```python
self.db = Database()
```

Now

your class

is tightly coupled

to one implementation.

______________________________________________________________________

### Depending on Concrete Classes

Business logic

shouldn't care

whether

the implementation is

MySQL,

PostgreSQL,

or MongoDB.

______________________________________________________________________

### Confusing DIP with DI

Remember:

DIP

is the principle.

DI

is the technique.

______________________________________________________________________

### Using DIP Everywhere

Small scripts

don't need

enterprise architecture.

Apply DIP

where flexibility

provides value.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Dependency Inversion Principle, and how is it different from Dependency Injection?

The Dependency Inversion Principle states that high-level modules should not depend on low-level modules. Instead, both
should depend on abstractions. This allows business logic to remain independent of implementation details such as
databases, notification providers, or storage systems. Dependency Injection is a technique used to implement this
principle by providing dependencies from outside the class rather than creating them internally. In short, DIP is the
design principle, while DI is one implementation technique.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What DIP is
- High-level vs low-level modules
- Why abstractions matter
- Real backend examples
- FastAPI example
- DIP vs DI
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Dependency Injection (DI)](13-dependency-injection.md)
