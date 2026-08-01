# Software Design & Design Patterns - Part 06

# Composition vs Inheritance

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- The difference between Composition and Inheritance
- Why modern backend applications prefer Composition
- The problems caused by excessive Inheritance
- Real-world backend examples
- How FastAPI uses Composition
- When to use Composition
- When to use Inheritance
- Why this topic is frequently asked in interviews

______________________________________________________________________

# The Problem

Let's continue building our **Library Management System**.

Initially, we create an `OrderService`.

A junior developer writes:

```python id="comp0601"
class OrderService:

    def create_order(self):
        print("Order Created")
```

Everything works.

______________________________________________________________________

# New Requirement

The business now wants:

- Logging
- Database access
- Email notifications
- Payment processing
- Cache
- Audit logging

The developer thinks,

> "I'll use inheritance everywhere."

______________________________________________________________________

# First Attempt - Inheritance

```python id="comp0602"
class Logger:

    def log(self):
        print("Logging...")
```

```python id="comp0603"
class OrderService(Logger):

    def create_order(self):
        self.log()
```

Later,

database support arrives.

```python id="comp0604"
class Database(Logger):

    def save(self):
        print("Saving...")
```

Then,

```python id="comp0605"
class OrderService(Database):

    def create_order(self):
        self.save()
        self.log()
```

Then comes email support.

Then payment support.

Eventually,

the developer starts wondering,

> "Should OrderService inherit from EmailService too?"

______________________________________________________________________

# What's the Problem?

Ask yourself.

Is an Order Service

a Database?

No.

Is an Order Service

a Logger?

No.

Is an Order Service

an Email Service?

No.

Inheritance expresses

an **IS-A** relationship.

But here,

the relationship is

completely different.

______________________________________________________________________

# The Correct Relationship

An Order Service

doesn't **IS-A**

Logger.

It **HAS-A**

Logger.

It **HAS-A**

Database.

It **HAS-A**

Payment Service.

It **HAS-A**

Email Service.

This is called

**Composition**.

______________________________________________________________________

# Composition

Composition means:

> **One object is built using other objects.**

Instead of inheriting behavior,

we **combine** objects.

______________________________________________________________________

# Refactored Design

Logger

```python id="comp0606"
class Logger:

    def log(self, message):
        print(message)
```

Database

```python id="comp0607"
class Database:

    def save(self):
        print("Saved")
```

Email

```python id="comp0608"
class EmailService:

    def send(self):
        print("Email Sent")
```

Now,

the Order Service.

```python id="comp0609"
class OrderService:

    def __init__(
        self,
        database,
        logger,
        email_service,
    ):
        self.database = database
        self.logger = logger
        self.email_service = email_service

    def create_order(self):

        self.database.save()

        self.logger.log(
            "Order Created"
        )

        self.email_service.send()
```

______________________________________________________________________

# Why Is This Better?

Suppose tomorrow,

the company replaces

its logger.

Old

```text id="comp0610"
Console Logger
```

New

```text id="comp0611"
Cloud Logger
```

Nothing changes

inside

OrderService.

You simply provide

another logger.

______________________________________________________________________

# Another Example

Suppose

Stripe

is replaced

with Razorpay.

Old

```python id="comp0612"
stripe.pay()
```

New

```python id="comp0613"
razorpay.pay()
```

Only one dependency changes.

The checkout service

remains the same.

______________________________________________________________________

# Real Backend Example

Suppose you're building

a User Service.

It needs:

- Database
- Cache
- Logger
- Email Service

Good design

looks like this.

```python id="comp0614"
class UserService:

    def __init__(

        self,

        database,

        cache,

        logger,

        email_service,

    ):
        ...
```

Each dependency

has

its own responsibility.

______________________________________________________________________

# FastAPI Uses Composition

Look at

a typical endpoint.

```python id="comp0615"
@app.post("/books")
def create_book(

    db=Depends(get_db),

    logger=Depends(get_logger),

):
    ...
```

Does the endpoint

inherit

from Database?

No.

It **receives**

the Database.

That is Composition.

______________________________________________________________________

# SQLAlchemy Example

Repositories

usually receive

a Session.

```python id="comp0616"
class BookRepository:

    def __init__(
        self,
        session,
    ):
        self.session = session
```

The repository

doesn't inherit

from Session.

It simply

uses it.

______________________________________________________________________

# Testing Becomes Easier

Suppose

you want

to test

OrderService.

Instead of

a real email service,

use

```python id="comp0617"
class FakeEmail:

    def send(self):
        pass
```

Now

```python id="comp0618"
service = OrderService(

    database,

    logger,

    FakeEmail(),
)
```

Testing becomes

simple.

______________________________________________________________________

# Composition vs Inheritance

| Inheritance | Composition |
| ------------------------------ | ---------------------------- |
| IS-A relationship | HAS-A relationship |
| Tight coupling | Loose coupling |
| Harder to replace dependencies | Easy to replace dependencies |
| Deep hierarchies possible | Small reusable objects |
| Less flexible | More flexible |

______________________________________________________________________

# When Should You Use Inheritance?

Use inheritance

when the relationship

is naturally

an

**IS-A**

relationship.

Examples:

- `EBook` **is a** `Book`
- `AdminUser` **is a** `User`
- `ValidationError` **is an** `Exception`

These are

natural hierarchies.

______________________________________________________________________

# When Should You Use Composition?

Use composition

when objects

work together.

Examples:

- Services
- Repositories
- Loggers
- Payment Providers
- Cache
- Storage Providers
- Email Services
- AI Models

Most backend applications

use composition

far more often

than inheritance.

______________________________________________________________________

# One of the Most Famous Design Principles

You'll often hear

experienced developers say:

> **Favor Composition Over Inheritance.**

This doesn't mean

inheritance is bad.

It means

composition

usually provides

greater flexibility.

______________________________________________________________________

# When NOT to Use Composition

Don't split

every tiny task

into separate classes.

If you're writing

a small script,

simple functions

may be

the better choice.

______________________________________________________________________

# Best Practices

✅ Use inheritance for genuine hierarchies.

✅ Use composition for collaboration.

✅ Keep dependencies independent.

✅ Prefer loosely coupled objects.

✅ Inject dependencies instead of creating them.

______________________________________________________________________

# Common Mistakes

### Inheriting Just to Reuse Code

Code reuse alone

is not a good reason

to use inheritance.

______________________________________________________________________

### Deep Inheritance Trees

Deep hierarchies

become difficult

to understand

and maintain.

______________________________________________________________________

### Creating Dependencies Inside Classes

Bad

```python id="comp0619"
self.logger = Logger()
```

Better

Receive

the logger

from outside.

______________________________________________________________________

### Forgetting the Relationship

Always ask:

Is this

an

**IS-A**

relationship

or

a

**HAS-A**

relationship?

That question alone

helps choose

the right design.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is composition generally preferred over inheritance in modern backend development?

Composition is preferred because it creates loosely coupled components that can be replaced, tested, and extended
independently. Instead of inheriting behavior, objects receive the dependencies they need, making the system more
flexible. Modern frameworks like FastAPI rely heavily on composition through dependency injection, while inheritance is
reserved for true "IS-A" relationships such as exceptions, base models, and shared domain hierarchies.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Composition
- Composition vs Inheritance
- IS-A vs HAS-A
- Backend examples
- FastAPI examples
- Testing benefits
- When to use each approach
- Best practices

______________________________________________________________________

# What's Next

[SOLID Principles Overview](07-solid-overview.md)
