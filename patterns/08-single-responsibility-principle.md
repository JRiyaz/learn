# Software Design & Design Patterns - Part 08

# Single Responsibility Principle (SRP)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Single Responsibility Principle (SRP) is
- The problem SRP solves
- What "one reason to change" actually means
- How to identify SRP violations
- How to refactor code using SRP
- Real-world backend examples
- FastAPI examples
- When NOT to apply SRP excessively

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

The business wants the following workflow:

1. Add a book
1. Save it to the database
1. Log the action
1. Send an email to the librarian
1. Clear the cache
1. Publish an event to Kafka

A junior developer writes this.

```python
class LibraryService:

    def add_book(self, book):

        # Validate

        # Save to database

        # Write logs

        # Send email

        # Clear cache

        # Publish Kafka event

        print("Book Added")
```

Everything works.

The application is deployed.

______________________________________________________________________

# Three Months Later...

The business changes.

Email notifications are replaced by Slack.

So you modify

```python
add_book()
```

A week later,

the logging format changes.

Again,

you modify

```python
add_book()
```

Next month,

Kafka is replaced by RabbitMQ.

Again,

you modify

```python
add_book()
```

Then,

cache invalidation changes.

Again,

you modify

```python
add_book()
```

______________________________________________________________________

# What's the Problem?

Ask yourself.

Why is

```python
LibraryService
```

changing?

Because of:

- Database changes
- Logging changes
- Notification changes
- Cache changes
- Messaging changes

One class.

Five different reasons to change.

That is exactly

what SRP tries to prevent.

______________________________________________________________________

# What is SRP?

The **Single Responsibility Principle** states:

> **A class should have only one reason to change.**

Notice something.

It **doesn't** say

> A class should do only one thing.

It says

> A class should have one **reason** to change.

This is one of the most misunderstood principles in software engineering.

______________________________________________________________________

# What Does "One Reason to Change" Mean?

Let's look at our example.

Why would

`LibraryService`

change?

| Reason | Should LibraryService Change? |
| ---------------------------- | ----------------------------- |
| New database | ❌ No |
| New logger | ❌ No |
| New notification service | ❌ No |
| New cache implementation | ❌ No |
| New Kafka topic | ❌ No |
| Book creation business rules | ✅ Yes |

Only the business rules

for creating books

should affect

`LibraryService`.

Everything else

belongs elsewhere.

______________________________________________________________________

# Refactoring

Instead of one class,

split responsibilities.

```python
class BookRepository:

    def save(self, book):
        ...
```

```python
class NotificationService:

    def send(self, message):
        ...
```

```python
class Logger:

    def log(self, message):
        ...
```

```python
class CacheService:

    def clear_books(self):
        ...
```

```python
class EventPublisher:

    def publish(self, event):
        ...
```

Now,

our service becomes

much simpler.

```python
class LibraryService:

    def __init__(
        self,
        repository,
        notification,
        logger,
        cache,
        publisher,
    ):

        self.repository = repository
        self.notification = notification
        self.logger = logger
        self.cache = cache
        self.publisher = publisher

    def add_book(
        self,
        book,
    ):

        self.repository.save(book)

        self.logger.log(
            "Book Added"
        )

        self.notification.send(
            "New Book Added"
        )

        self.cache.clear_books()

        self.publisher.publish(
            "BOOK_CREATED"
        )
```

______________________________________________________________________

# Why Is This Better?

Suppose

Slack replaces Email.

Which class changes?

Only

```python
NotificationService
```

Suppose

Redis is replaced

with Memcached.

Which class changes?

Only

```python
CacheService
```

Suppose

Kafka becomes RabbitMQ.

Only

```python
EventPublisher
```

The business logic

never changes.

______________________________________________________________________

# Another Real Backend Example

Imagine an

Order Service.

Bad

```python
class OrderService:

    def place_order(self):

        # Validate

        # Save Order

        # Charge Payment

        # Send Email

        # Update Inventory

        # Write Logs
```

Every team

touches

the same class.

Conflicts become common.

______________________________________________________________________

# Better Design

```text
OrderService

↓

PaymentService

↓

InventoryService

↓

NotificationService

↓

OrderRepository

↓

Logger
```

Each service

has

one responsibility.

______________________________________________________________________

# FastAPI Example

Bad

```python
@app.post("/books")
def create_book():

    # SQL

    # Logging

    # Email

    # Cache

    # Kafka
```

Everything

inside one endpoint.

______________________________________________________________________

Better

```python
@app.post("/books")
def create_book(

    service=Depends(
        get_library_service
    ),
):

    service.add_book(...)
```

The endpoint

doesn't know

how notifications,

logging,

or caching work.

It simply delegates

to the service.

______________________________________________________________________

# Does SRP Mean One Method Per Class?

No.

This is a common myth.

Bad understanding

```python
BookValidator
```

```python
BookNameValidator
```

```python
BookAuthorValidator
```

```python
BookPriceValidator
```

You end up creating

hundreds of tiny classes.

That's not SRP.

SRP is about

**responsibility**,

not

the number of methods.

______________________________________________________________________

# Benefits of SRP

Applying SRP gives you:

✅ Easier maintenance

✅ Easier testing

✅ Better readability

✅ Better code reuse

✅ Smaller classes

✅ Lower coupling

______________________________________________________________________

# When NOT to Use SRP Excessively

Suppose

your application

contains

50 lines of code.

Splitting it

into

20 classes

would make it

harder to understand.

SRP should

simplify code,

not complicate it.

______________________________________________________________________

# Real Company Example

Suppose Netflix

changes

its notification provider.

Should

the recommendation engine

also change?

No.

Different teams

own different responsibilities.

SRP allows

each team

to work independently.

______________________________________________________________________

# Best Practices

✅ One responsibility per class.

✅ Group related behavior together.

✅ Separate business logic from infrastructure.

✅ Keep classes focused.

✅ Prefer collaboration over giant classes.

______________________________________________________________________

# Common Mistakes

### Confusing "One Method" with "One Responsibility"

A class may have

many methods

as long as

they serve

the same responsibility.

______________________________________________________________________

### Creating God Classes

Large services

that do everything

are difficult

to maintain.

______________________________________________________________________

### Splitting Too Early

Don't create

dozens of services

for a tiny application.

Grow naturally.

______________________________________________________________________

### Mixing Infrastructure with Business Logic

Business rules

shouldn't know

how emails,

Kafka,

or Redis work.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Single Responsibility Principle?

The Single Responsibility Principle states that a class should have only one reason to change. In other words, a class
should focus on a single responsibility or concern. If a class changes because of multiple unrelated reasons, such as
database updates, logging changes, or notification changes, it is likely violating SRP. Applying SRP leads to smaller,
more maintainable, testable, and reusable components.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What SRP is
- What "one reason to change" means
- How to identify SRP violations
- How to refactor using SRP
- FastAPI example
- Backend example
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Open/Closed Principle (OCP)](09-open-closed-principle.md)
