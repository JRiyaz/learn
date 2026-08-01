# Software Design & Design Patterns - Part 28

# Mediator Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Mediator Pattern is
- Why the Mediator Pattern exists
- The problem it solves
- Centralized communication
- Real-world backend examples
- FastAPI examples
- Microservices examples
- Mediator vs Observer
- When NOT to use the Mediator Pattern

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

contains these services.

```text id="med2801"
Book Service

↓

Member Service

↓

Payment Service

↓

Notification Service

↓

Inventory Service

↓

Recommendation Service
```

Now imagine

every service

communicates

with

every other service.

Very quickly,

the application

becomes difficult

to understand.

______________________________________________________________________

# The Problem

Suppose

a member

borrows a book.

The Book Service

directly calls

```text id="med2802"
Payment Service

↓

Notification Service

↓

Inventory Service

↓

Recommendation Service
```

Later,

Notification Service

calls

Analytics Service.

Inventory Service

calls

Audit Service.

Recommendation Service

calls

ML Service.

Soon,

the communication

looks like this.

```text id="med2803"
A ↔ B

A ↔ C

A ↔ D

B ↔ D

C ↔ E

D ↔ F

E ↔ G
```

Every service

knows

about

many other services.

______________________________________________________________________

# What's the Problem?

Problems:

❌ Tight coupling

❌ Difficult testing

❌ Hard to add new services

❌ Hard to trace communication

Every new feature

requires

updating

multiple classes.

______________________________________________________________________

# The Idea

Instead of

services

talking

to each other,

they all

talk

to

one object.

That object

coordinates

communication.

______________________________________________________________________

# What is the Mediator Pattern?

The **Mediator Pattern** says:

> **Define an object that encapsulates how a set of objects interact.**

Instead of

objects

communicating directly,

they communicate

through

a mediator.

______________________________________________________________________

# Without Mediator

```text id="med2804"
Book

↓

Payment

↓

Inventory

↓

Notification

↓

Recommendation
```

Many

connections.

______________________________________________________________________

# With Mediator

```text id="med2805"
Book

↓

Mediator

↑

Payment

Inventory

Notification

Recommendation
```

Every service

knows

only

the mediator.

______________________________________________________________________

# Step 1

Create

the mediator.

```python id="med2806"
from abc import (
    ABC,
    abstractmethod,
)

class Mediator(
    ABC
):

    @abstractmethod
    def notify(
        self,
        sender,
        event,
    ):
        ...
```

______________________________________________________________________

# Step 2

Create

the services.

```python id="med2807"
class BookService:

    def __init__(
        self,
        mediator,
    ):

        self.mediator = mediator
```

Borrowing

a book

becomes

```python id="med2808"
def borrow(self):

    print(
        "Book Borrowed"
    )

    self.mediator.notify(

        self,

        "BOOK_BORROWED",

    )
```

Notice

the service

doesn't know

who reacts.

______________________________________________________________________

# Step 3

Implement

the mediator.

```python id="med2809"
class LibraryMediator(
    Mediator
):

    def notify(

        self,

        sender,

        event,

    ):

        if event == "BOOK_BORROWED":

            inventory.update()

            notification.send()

            recommendation.update()
```

The mediator

coordinates

everything.

______________________________________________________________________

# Using It

```python id="med2810"
mediator = LibraryMediator()

books = BookService(
    mediator
)

books.borrow()
```

Book Service

doesn't know

Inventory Service,

Notification Service,

or Recommendation Service.

______________________________________________________________________

# Real Backend Example

Suppose

an order

is placed.

Without Mediator

```text id="med2811"
Order Service

↓

Inventory

↓

Payment

↓

Shipping

↓

Email

↓

Analytics
```

With Mediator

```text id="med2812"
Order Service

↓

Order Mediator

↓

Inventory

Payment

Shipping

Email

Analytics
```

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

creates

a user.

Instead of

calling

five services,

call

```python id="med2813"
UserRegistrationMediator
```

The mediator

coordinates:

- User creation
- Email
- Audit
- Metrics
- Welcome notification

The endpoint

remains clean.

______________________________________________________________________

# Microservices Example

Suppose

many services

must coordinate

a checkout process.

Instead of

every service

calling

every other service,

an

**Orchestrator**

coordinates

the workflow.

This orchestration

is conceptually

very similar

to the Mediator Pattern.

______________________________________________________________________

# AI/ML Example

Suppose

an AI request

requires:

- Prompt validation
- Retrieval
- LLM
- Guardrails
- Logging
- Metrics

Instead of

each component

calling

the next,

an

AI Pipeline Manager

coordinates

the entire flow.

This manager

acts

as

a mediator.

______________________________________________________________________

# Mediator vs Observer

A very common

interview question.

| Mediator | Observer |
| ------------------------- | ---------------------------------- |
| Coordinates communication | Broadcasts events |
| Central controller | Independent subscribers |
| Objects know mediator | Publisher doesn't know subscribers |

Observer

↓

Event

↓

Many listeners

Mediator

↓

Request

↓

Central coordinator

______________________________________________________________________

# Mediator vs Facade

Another

common confusion.

| Mediator | Facade |
| ---------------------- | ---------------------- |
| Coordinates colleagues | Simplifies a subsystem |
| Controls interactions | Hides complexity |

Facade

makes

a system

easier to use.

Mediator

controls

how objects

communicate.

______________________________________________________________________

# Event Bus vs Mediator

In modern systems,

you'll hear

about

Event Buses.

Example:

```text id="med2814"
Kafka

RabbitMQ

Redis Pub/Sub
```

These are

not exactly

the Mediator Pattern,

but they often

serve

a similar purpose

of reducing

direct coupling

between components.

______________________________________________________________________

# Benefits

Mediator gives you:

✅ Loose coupling

✅ Centralized communication

✅ Easier maintenance

✅ Easier testing

✅ Cleaner services

______________________________________________________________________

# Drawbacks

It also introduces:

❌ One extra layer

❌ Mediator can become large

❌ Poor design can create

a God Object.

______________________________________________________________________

# Real Company Example

Suppose

an airline

books a ticket.

Many systems

must coordinate.

- Seat Reservation
- Payment
- Loyalty Points
- Email
- SMS
- Fraud Detection

Instead of

each service

communicating

directly,

a booking coordinator

manages

the workflow.

That's

a mediator.

______________________________________________________________________

# When NOT to Use Mediator

Don't introduce

a mediator

if

only

two simple classes

communicate.

Direct interaction

is usually

simpler.

Use Mediator

when

many objects

communicate

with each other.

______________________________________________________________________

# Best Practices

✅ Keep colleagues independent.

✅ Put communication logic inside the mediator.

✅ Avoid business logic in colleagues.

✅ Keep mediators focused on one workflow.

______________________________________________________________________

# Common Mistakes

### Giant Mediator

If one mediator

controls

the entire application,

it becomes

another God Class.

Split

mediators

by workflow.

______________________________________________________________________

### Business Logic Everywhere

The mediator

should coordinate,

not replace

domain services.

______________________________________________________________________

### Tight Coupling to Colleagues

Colleagues

should know

only

the mediator.

______________________________________________________________________

### Confusing Mediator with Observer

Observer

broadcasts events.

Mediator

coordinates

interactions.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Mediator Pattern, and where is it commonly used?

The Mediator Pattern is a behavioral design pattern that centralizes communication between multiple objects through a
mediator instead of allowing them to communicate directly. This reduces coupling, simplifies maintenance, and makes
interactions easier to manage. It is commonly used in workflow orchestration, UI frameworks, backend service
coordination, checkout processes, and AI pipelines where many components must collaborate to complete a task.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Mediator Pattern is
- Why it exists
- Backend examples
- FastAPI example
- Microservices example
- AI pipeline example
- Mediator vs Observer
- Mediator vs Facade
- Best practices

______________________________________________________________________

# 🎯 Course Progress

At this point, you've covered nearly all of the design patterns that appear regularly in production Python backend
systems.

The remaining lessons will focus on enterprise architectural patterns and modern software architecture that build on
everything you've learned so far.

______________________________________________________________________

# What's Next

[CQRS (Command Query Responsibility Segregation)](29-cqrs.md)
