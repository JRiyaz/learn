# Software Design & Design Patterns - Part 19

# Decorator Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Decorator Pattern is
- Why the Decorator Pattern exists
- The problem it solves
- Dynamic behavior vs inheritance
- Real-world backend examples
- FastAPI examples
- Python decorators vs the Decorator Pattern
- When NOT to use the Decorator Pattern

______________________________________________________________________

# Before We Start

If you've worked with Python,

you've already seen decorators.

```python
@login_required

@cache

@retry

@app.get("/books")
```

But here's something interesting.

**Python decorators** and the **Decorator Design Pattern** are related,

but they are **not exactly the same thing**.

We'll understand both in this lesson.

______________________________________________________________________

# The Problem

Let's continue with our **Library Management System**.

We have a service

that borrows books.

```python
class LibraryService:

    def borrow_book(
        self,
        book_id,
    ):

        print(
            "Book Borrowed"
        )
```

Everything works.

______________________________________________________________________

# New Requirement

Every request

must also:

- Log requests
- Check authentication
- Measure execution time
- Cache responses
- Retry on failure

A junior developer writes

```python
class LibraryService:

    def borrow_book(
        self,
        book_id,
    ):

        authenticate()

        logger.info(
            "Borrow Started"
        )

        start_timer()

        print(
            "Book Borrowed"
        )

        stop_timer()

        cache_result()

        retry_if_needed()
```

______________________________________________________________________

# Another Requirement

Now,

the business says

some endpoints

need caching,

others don't.

Some endpoints

need retry,

others don't.

Some endpoints

need metrics,

others don't.

The service

becomes difficult

to maintain.

______________________________________________________________________

# What's the Problem?

Business logic

is mixed with

cross-cutting concerns.

What is

the real job

of

`borrow_book()`?

Borrowing books.

Not

- Logging
- Authentication
- Metrics
- Retry
- Caching

These are

additional behaviors.

______________________________________________________________________

# The Idea

Instead of

changing

the original object,

let's

**wrap**

it

with new functionality.

Think of it like

gift wrapping.

The gift

doesn't change.

You simply

add

another layer.

______________________________________________________________________

# What is the Decorator Pattern?

The **Decorator Pattern** says:

> **Attach additional responsibilities to an object dynamically without modifying its original code.**

Instead of

changing

the object,

wrap it

inside

another object.

______________________________________________________________________

# Without Decorator

```text
LibraryService

↓

Borrow Book
```

______________________________________________________________________

# With Decorator

```text
Logging

↓

Authentication

↓

Caching

↓

LibraryService

↓

Borrow Book
```

Each layer

adds behavior.

______________________________________________________________________

# Step 1

Create

an abstraction.

```python
from abc import (
    ABC,
    abstractmethod,
)

class LibraryOperation(
    ABC
):

    @abstractmethod
    def execute(self):
        ...
```

______________________________________________________________________

# Step 2

Implement

the original object.

```python
class BorrowBook(
    LibraryOperation
):

    def execute(self):

        print(
            "Book Borrowed"
        )
```

______________________________________________________________________

# Step 3

Create

a Logging Decorator.

```python
class LoggingDecorator(
    LibraryOperation
):

    def __init__(
        self,
        operation,
    ):

        self.operation = operation

    def execute(self):

        print(
            "Logging..."
        )

        self.operation.execute()
```

Notice something.

The decorator

doesn't replace

the original object.

It wraps it.

______________________________________________________________________

# Step 4

Authentication Decorator.

```python
class AuthDecorator(
    LibraryOperation
):

    def __init__(
        self,
        operation,
    ):

        self.operation = operation

    def execute(self):

        print(
            "Authenticating..."
        )

        self.operation.execute()
```

______________________________________________________________________

# Using Decorators

```python
service = BorrowBook()

service = LoggingDecorator(
    service
)

service = AuthDecorator(
    service
)

service.execute()
```

Output

```text
Authenticating...

Logging...

Book Borrowed
```

The original object

never changed.

______________________________________________________________________

# Real Backend Example

Suppose

our payment service

needs:

- Logging
- Retry
- Metrics

Instead of writing

```python
pay()

↓

Logging

↓

Retry

↓

Metrics
```

inside

every payment provider,

wrap

the payment service

with decorators.

Each decorator

adds

one responsibility.

______________________________________________________________________

# FastAPI Example

FastAPI endpoints

often use

Python decorators.

```python
@app.get("/books")
```

Libraries

may add

```python
@cache

@rate_limit

@authorize
```

Each decorator

adds functionality

without modifying

the endpoint itself.

This is

the same idea

as the Decorator Pattern.

______________________________________________________________________

# Python Function Decorators

Python provides

language support

for decorators.

Example

```python
def logger(func):

    def wrapper():

        print("Started")

        result = func()

        print("Finished")

        return result

    return wrapper
```

Use it.

```python
@logger
def borrow_book():

    print(
        "Borrowing..."
    )
```

Output

```text
Started

Borrowing...

Finished
```

This is

a function-level implementation

of the Decorator concept.

______________________________________________________________________

# Real Backend Example

Suppose

our API

needs

rate limiting.

Instead of

modifying

every endpoint,

apply

```python
@rate_limit
```

Need caching?

```python
@cache
```

Need metrics?

```python
@track_metrics
```

Each feature

remains

independent.

______________________________________________________________________

# AI/ML Example

Suppose

you have

an AI model.

```python
model.predict(data)
```

Now,

add

- Logging
- Performance Metrics
- Caching
- Input Validation

Instead of

changing

the model,

decorate it.

______________________________________________________________________

# Decorator vs Inheritance

A common interview question.

Suppose

you need:

- Logging
- Retry
- Metrics
- Caching

Inheritance

might require

many combinations.

```text
LoggedService

CachedService

LoggedCachedService

LoggedCachedRetryService
```

This quickly

becomes impossible

to maintain.

Decorators

allow

combining behaviors

at runtime.

______________________________________________________________________

# Benefits

Decorator gives you:

✅ Dynamic behavior

✅ No class explosion

✅ Better separation of concerns

✅ Reusable features

✅ Cleaner business logic

______________________________________________________________________

# Drawbacks

Decorators also introduce:

❌ More objects

❌ More layers

❌ Harder debugging

❌ Call stack becomes deeper

______________________________________________________________________

# When NOT to Use Decorator

Don't use decorators

for core business logic.

Business rules

should remain

inside

the business object.

Decorators

should add

cross-cutting concerns,

such as:

- Logging
- Metrics
- Retry
- Security
- Caching

______________________________________________________________________

# Best Practices

✅ Keep decorators focused.

✅ One decorator,

one responsibility.

✅ Wrap behavior,

don't rewrite it.

✅ Keep business logic separate.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic in Decorators

Decorators

should enhance behavior,

not replace

business logic.

______________________________________________________________________

### Creating Huge Decorators

Each decorator

should perform

one task.

______________________________________________________________________

### Confusing Python Decorators with the Pattern

Python decorators

are syntax.

The Decorator Pattern

is a design concept.

Python simply

makes implementing it

very convenient.

______________________________________________________________________

### Using Inheritance Instead

If behaviors

need to be combined

dynamically,

decorators

are usually

a better choice.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Decorator Pattern, and how is it related to Python decorators?

The Decorator Pattern is a structural design pattern that dynamically adds new behavior to an object without modifying
its original implementation. It achieves this by wrapping the object inside one or more decorator objects, each
responsible for a specific feature such as logging, caching, authentication, or metrics. Python's `@decorator` syntax is
a language feature that provides a convenient way to implement the same underlying idea for functions and methods.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Decorator Pattern is
- Why it exists
- Backend examples
- FastAPI examples
- Python decorators
- Decorator vs Inheritance
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Repository Pattern](20-repository-pattern.md)
