# Software Design & Design Patterns - Part 25

# Chain of Responsibility Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Chain of Responsibility Pattern is
- Why the Chain of Responsibility Pattern exists
- The problem it solves
- Request pipelines
- Middleware concepts
- Real-world backend examples
- FastAPI examples
- Web framework examples
- When NOT to use the Chain of Responsibility Pattern

______________________________________________________________________

# Before We Start

Every HTTP request

to a backend application

usually passes through

multiple stages.

```text id="cor2501"
HTTP Request

↓

Authentication

↓

Authorization

↓

Rate Limiting

↓

Logging

↓

Validation

↓

Business Logic

↓

HTTP Response
```

Have you ever wondered

how frameworks

like FastAPI,

Django,

Spring Boot,

or ASP.NET

execute these

one after another?

The answer is

the

**Chain of Responsibility Pattern.**

______________________________________________________________________

# The Problem

Let's continue with our

**Library Management System**.

Our endpoint

borrows a book.

```python id="cor2502"
@app.post("/borrow")
def borrow_book():

    authenticate()

    authorize()

    validate_request()

    check_rate_limit()

    logger.info(...)

    borrow()

    return response
```

Everything works.

______________________________________________________________________

# Another Requirement

Tomorrow,

every request

must also:

- Check API key
- Record metrics
- Add tracing
- Verify CSRF
- Detect fraud

The endpoint

continues growing.

______________________________________________________________________

# What's the Problem?

The endpoint

knows

every processing step.

Problems:

❌ Difficult maintenance

❌ Difficult reuse

❌ Difficult testing

❌ Tight coupling

Every endpoint

duplicates

the same logic.

______________________________________________________________________

# The Idea

Instead of

one method

doing everything,

create

a chain

of handlers.

Each handler

decides

whether to:

- Process the request
- Stop the request
- Pass it to the next handler

______________________________________________________________________

# What is the Chain of Responsibility Pattern?

The **Chain of Responsibility Pattern** says:

> **Pass a request through a chain of handlers until it reaches the appropriate handler or the end of the chain.**

Each handler

has one responsibility.

No handler

needs to know

the entire pipeline.

______________________________________________________________________

# Without Chain

```text id="cor2503"
Endpoint

↓

Authentication

↓

Authorization

↓

Validation

↓

Logging

↓

Business Logic
```

Everything

inside one function.

______________________________________________________________________

# With Chain

```text id="cor2504"
Request

↓

Authentication Handler

↓

Authorization Handler

↓

Validation Handler

↓

Logging Handler

↓

Business Handler
```

Each handler

does

one job.

______________________________________________________________________

# Step 1

Create

the handler.

```python id="cor2505"
from abc import (
    ABC,
    abstractmethod,
)

class Handler(
    ABC
):

    def __init__(self):

        self.next = None

    def set_next(
        self,
        handler,
    ):

        self.next = handler

        return handler

    @abstractmethod
    def handle(
        self,
        request,
    ):
        ...
```

______________________________________________________________________

# Step 2

Authentication Handler.

```python id="cor2506"
class AuthHandler(
    Handler
):

    def handle(
        self,
        request,
    ):

        print(
            "Authentication"
        )

        if self.next:

            return self.next.handle(
                request
            )
```

______________________________________________________________________

# Step 3

Validation Handler.

```python id="cor2507"
class ValidationHandler(
    Handler
):

    def handle(
        self,
        request,
    ):

        print(
            "Validation"
        )

        if self.next:

            return self.next.handle(
                request
            )
```

______________________________________________________________________

# Step 4

Business Handler.

```python id="cor2508"
class BorrowHandler(
    Handler
):

    def handle(
        self,
        request,
    ):

        print(
            "Borrow Book"
        )
```

______________________________________________________________________

# Building the Chain

```python id="cor2509"
auth = AuthHandler()

validation = ValidationHandler()

borrow = BorrowHandler()

auth.set_next(
    validation
).set_next(
    borrow
)
```

______________________________________________________________________

# Executing the Chain

```python id="cor2510"
auth.handle(request)
```

Output

```text id="cor2511"
Authentication

Validation

Borrow Book
```

Each handler

passes

the request

to the next.

______________________________________________________________________

# Stopping the Chain

Suppose

authentication fails.

```python id="cor2512"
if not authenticated:

    return "401"
```

The next handlers

never execute.

This makes

security pipelines

very easy

to build.

______________________________________________________________________

# Real Backend Example

Every request

may pass through

these handlers.

```text id="cor2513"
Authentication

↓

Authorization

↓

Rate Limiting

↓

Validation

↓

Business Logic

↓

Audit Logging
```

Each handler

remains

independent.

______________________________________________________________________

# FastAPI Example

FastAPI

supports

Middleware.

```python id="cor2514"
@app.middleware("http")
```

Each middleware

receives

the request,

performs work,

and decides

whether

to continue.

This is

the Chain of Responsibility

in action.

______________________________________________________________________

# Django Example

Django

also uses

middleware.

```text id="cor2515"
Security Middleware

↓

Session Middleware

↓

Authentication Middleware

↓

CSRF Middleware

↓

View
```

Every request

flows

through

the chain.

______________________________________________________________________

# AI/ML Example

Suppose

your AI application

receives

a prompt.

Pipeline

```text id="cor2516"
Input Validation

↓

Prompt Moderation

↓

Prompt Template

↓

LLM

↓

Output Moderation

↓

Logging
```

Each stage

handles

one concern.

______________________________________________________________________

# API Gateway Example

API Gateways

often use

this pattern.

Incoming request

↓

Authentication

↓

Authorization

↓

Quota Check

↓

Routing

↓

Service

Each stage

can reject

the request

before it reaches

the application.

______________________________________________________________________

# Chain vs Decorator

A common interview question.

| Chain | Decorator |
| -------------------- | -------------------- |
| Multiple handlers | Multiple wrappers |
| Pass request forward | Wrap object behavior |
| Request pipeline | Object enhancement |

Decorator

adds behavior

to an object.

Chain

processes

a request

through

multiple handlers.

______________________________________________________________________

# Chain vs Middleware

Another common question.

Middleware

is one of

the most common

implementations

of the

Chain of Responsibility Pattern.

If you understand

this pattern,

you'll understand

how most web frameworks

process requests.

______________________________________________________________________

# Benefits

Chain gives you:

✅ Loose coupling

✅ Reusable handlers

✅ Easy pipeline creation

✅ Easy insertion/removal

✅ Cleaner request processing

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More objects

❌ Harder debugging

❌ Pipeline ordering matters

A wrongly ordered chain

can introduce

subtle bugs.

______________________________________________________________________

# Real Company Example

Suppose

Stripe

receives

an API request.

Before processing,

the request

may pass through:

- Authentication
- Fraud Detection
- Risk Analysis
- Rate Limiting
- Logging
- Metrics

Each concern

is isolated

inside

its own handler.

______________________________________________________________________

# When NOT to Use Chain

Suppose

your application

contains

only

one processing step.

Creating

five handlers

would add

unnecessary complexity.

The pattern

becomes valuable

when

requests

naturally flow

through

multiple stages.

______________________________________________________________________

# Best Practices

✅ One handler,

one responsibility.

✅ Keep handlers independent.

✅ Make handlers reusable.

✅ Allow handlers to stop the chain when appropriate.

______________________________________________________________________

# Common Mistakes

### One Giant Handler

If one handler

performs

authentication,

logging,

validation,

and business logic,

the pattern

loses its value.

______________________________________________________________________

### Tight Coupling

Handlers

should know

only

about

the next handler,

not

the entire chain.

______________________________________________________________________

### Wrong Ordering

Authentication

should usually happen

before

business logic.

Ordering

is critical.

______________________________________________________________________

### Ignoring Short-Circuiting

Handlers

should be able

to stop

the chain

when necessary,

such as

authentication failures.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Chain of Responsibility Pattern, and where is it used?

The Chain of Responsibility Pattern is a behavioral design pattern in which a request passes through a sequence of
independent handlers. Each handler performs its own responsibility and then either forwards the request to the next
handler or stops the processing. This pattern is widely used in HTTP middleware, authentication pipelines, API gateways,
request validation, logging, rate limiting, and AI inference pipelines. Modern web frameworks such as FastAPI and Django
use this pattern extensively for request processing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Chain of Responsibility Pattern is
- Why it exists
- Handler pipelines
- FastAPI middleware
- Django middleware
- AI pipelines
- API Gateway examples
- Best practices
- Common mistakes

______________________________________________________________________

# 🎯 Design Patterns Progress

You have now covered the patterns that appear most frequently in production backend systems:

- Factory
- Singleton
- Strategy
- Observer
- Adapter
- Decorator
- Repository
- Builder
- Facade
- Command
- Template Method
- Chain of Responsibility

From here, we'll move into a few additional patterns that are valuable in enterprise applications and interviews before
transitioning into architecture topics such as Clean Architecture, Hexagonal Architecture, CQRS, and Event Sourcing.

______________________________________________________________________

# What's Next

[Proxy Pattern](26-proxy-pattern.md)
