# Software Architecture - Part 37

# Domain Events

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Domain Events are
- Why Domain Events exist
- Domain Events vs Integration Events
- Event publication
- Event handlers
- FastAPI implementation
- Microservices examples
- CQRS integration
- Event Sourcing integration
- When NOT to use Domain Events

______________________________________________________________________

# Before We Start

You've already learned:

- Observer Pattern
- CQRS
- Event Sourcing
- DDD Aggregates

Now we're going to connect

all of them.

This is one of

the most important

enterprise backend concepts.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

A member

borrows a book.

A developer writes

```python id="de3701"
def borrow_book():

    repository.save()

    email.send()

    analytics.update()

    recommendation.update()

    kafka.publish()

    audit.log()
```

Everything works.

______________________________________________________________________

# Another Requirement

Tomorrow,

the business adds

- Loyalty Points
- SMS Notifications
- ML Recommendations
- Fraud Detection

Every new feature

requires changing

`borrow_book()`.

Soon,

the method

contains

hundreds

of lines.

______________________________________________________________________

# What's the Problem?

The business action

is simple.

> Borrow a Book

But the method

knows

about

- Email
- Analytics
- Kafka
- Audit
- Recommendations

Problems:

❌ Tight coupling

❌ Difficult testing

❌ Difficult maintenance

❌ Violates SRP

______________________________________________________________________

# The Idea

Instead of

telling

every service

what to do,

announce

that

something happened.

Interested components

can react

independently.

______________________________________________________________________

# What is a Domain Event?

A **Domain Event**

represents

something important

that

already happened

inside

the business domain.

Examples:

- BookBorrowed
- BookReturned
- MemberRegistered
- FinePaid
- LoanExpired

Notice

the naming.

Events

are always

written

in

the **past tense**.

______________________________________________________________________

# Event vs Command

This interview question

appears frequently.

Command

↓

Requests

an action.

```text id="de3702"
Borrow Book
```

Event

↓

Records

what happened.

```text id="de3703"
Book Borrowed
```

Commands

look

toward

the future.

Events

describe

the past.

______________________________________________________________________

# Domain Event Example

```python id="de3704"
from dataclasses import (
    dataclass,
)

@dataclass
class BookBorrowed:

    book_id: int

    member_id: int
```

Notice

there is

no business logic.

Only

facts.

______________________________________________________________________

# Aggregate Creates Events

Suppose

our

Loan Aggregate

borrows

a book.

```python id="de3705"
class Loan:

    def borrow_book(

        self,

        book,

    ):

        ...

        self.events.append(

            BookBorrowed(

                book.id,

                self.member_id,

            )

        )
```

The Aggregate

records

what happened.

It doesn't

send emails.

______________________________________________________________________

# Event Publisher

After

the transaction

succeeds,

publish

the events.

```text id="de3706"
Aggregate

↓

Event Publisher

↓

Handlers
```

______________________________________________________________________

# Event Handler

Example

```python id="de3707"
class EmailHandler:

    def handle(

        self,

        event,

    ):

        print(

            "Email Sent"

        )
```

Another handler.

```python id="de3708"
class AnalyticsHandler:

    def handle(

        self,

        event,

    ):

        print(

            "Analytics Updated"

        )
```

Each handler

has

one responsibility.

______________________________________________________________________

# Execution Flow

```text id="de3709"
Borrow Book

↓

BookBorrowed Event

↓

Email

↓

Analytics

↓

Recommendation

↓

Audit
```

The Aggregate

knows nothing

about

these handlers.

______________________________________________________________________

# FastAPI Example

Endpoint

↓

```python id="de3710"
use_case.execute()
```

↓

Loan Aggregate

↓

BookBorrowed Event

↓

Publisher

↓

Handlers

The endpoint

remains

very small.

______________________________________________________________________

# CQRS Example

Commands

modify

the write model.

After success,

publish

Domain Events.

Example

```text id="de3711"
BorrowBookCommand

↓

BookBorrowed Event

↓

Update Read Model
```

The event

keeps

the read side

synchronized.

______________________________________________________________________

# Event Sourcing Example

In Event Sourcing,

events

are

the source

of truth.

Example

```text id="de3712"
BookBorrowed

↓

BookReturned

↓

FinePaid
```

Domain Events

are stored

inside

the Event Store.

The current state

is reconstructed

by replaying them.

______________________________________________________________________

# Domain Event vs Integration Event

One of

the most important

interview questions.

## Domain Event

Lives

inside

one application.

Example

```text id="de3713"
BookBorrowed
```

Used

to notify

internal handlers.

______________________________________________________________________

## Integration Event

Leaves

the application.

Example

```text id="de3714"
BookBorrowed

↓

Kafka

↓

Inventory Service

↓

Analytics Service

↓

Recommendation Service
```

Integration Events

are consumed

by

other systems.

______________________________________________________________________

# Important Rule

Not every

Domain Event

should become

an Integration Event.

Some events

are

purely internal.

Example

```text id="de3715"
FineCalculated
```

Other services

may not

care.

______________________________________________________________________

# Real Backend Example

Suppose

an order

is placed.

Domain Event

```text id="de3716"
OrderPlaced
```

Internal handlers

- Reserve Inventory
- Update Dashboard
- Audit Log

Integration Event

↓

Kafka

↓

Shipping Service

↓

Billing Service

↓

Email Service

______________________________________________________________________

# AI/ML Example

Suppose

a model

finishes training.

Domain Event

```text id="de3717"
ModelTrainingCompleted
```

Handlers

- Register Model
- Generate Metrics
- Notify Team

Integration Event

↓

Deploy Service

↓

Monitoring Platform

↓

Inference Cluster

______________________________________________________________________

# Domain Events + Outbox Pattern

Publishing

directly

to Kafka

can fail.

Better approach

```text id="de3718"
Database Transaction

↓

Save Aggregate

↓

Save Domain Events

↓

Outbox Table

↓

Outbox Worker

↓

Kafka
```

We'll study

the Outbox Pattern

later.

______________________________________________________________________

# Domain Events vs Observer

Another interview favorite.

| Observer | Domain Event |
| -------------------------- | ---------------------------- |
| Design Pattern | DDD Concept |
| Object-level notifications | Business-level notifications |
| Generic | Domain-specific |

Example

Observer

↓

Button Clicked

Domain Event

↓

OrderPlaced

BookBorrowed

PaymentCaptured

______________________________________________________________________

# Benefits

Domain Events give you:

✅ Loose coupling

✅ Easy extension

✅ Better SRP

✅ Better scalability

✅ Cleaner business logic

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Event ordering

❌ Debugging complexity

❌ Asynchronous behavior

❌ Eventual consistency

______________________________________________________________________

# Real Company Example

Suppose

Amazon

receives

an order.

The Order Aggregate

creates

```text id="de3719"
OrderPlaced
```

Handlers

perform:

- Payment
- Inventory
- Shipping
- Recommendations
- Analytics

The Order Aggregate

doesn't know

about

any of them.

______________________________________________________________________

# When NOT to Use Domain Events

Don't create

events

for

every method.

Example

```text id="de3720"
UserNameUpdated
```

may not

need

a Domain Event.

Reserve

Domain Events

for

important

business occurrences.

______________________________________________________________________

# Best Practices

✅ Name events in the past tense.

✅ Keep events immutable.

✅ Put only business facts in events.

✅ Keep handlers independent.

______________________________________________________________________

# Common Mistakes

### Business Logic Inside Events

Events

describe

what happened.

They don't

execute

business rules.

______________________________________________________________________

### Publishing Before Commit

Never publish

events

before

the database transaction

has succeeded.

Otherwise,

other systems

may observe

changes

that were

rolled back.

______________________________________________________________________

### Too Many Events

Only publish

meaningful

business events.

______________________________________________________________________

### Confusing Domain Events with Integration Events

Remember

Domain Events

are

internal.

Integration Events

cross

application boundaries.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are Domain Events, and how do they differ from Integration Events?

Domain Events are immutable objects that represent important business events that have already occurred within a domain,
such as `OrderPlaced` or `BookBorrowed`. They are used internally to decouple components and trigger additional business
processes without tightly coupling the aggregate to other services. Integration Events, on the other hand, are events
published outside the application—typically through a message broker such as Kafka or RabbitMQ—to notify other services.
While a Domain Event may lead to an Integration Event, the two serve different purposes and should not be treated as
interchangeable.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Domain Events are
- Domain Events vs Commands
- Domain Events vs Integration Events
- Event publication
- Event handlers
- CQRS integration
- Event Sourcing integration
- Outbox integration
- Best practices

______________________________________________________________________

# 🧠 DDD Progress

You have now completed the core concepts of Tactical DDD:

- ✅ Entities
- ✅ Value Objects
- ✅ Aggregates
- ✅ Aggregate Roots
- ✅ Domain Events

From here, we'll shift from domain modeling to **distributed architecture**, starting with **Microservices
Architecture**, where these DDD concepts become essential for defining service boundaries.

______________________________________________________________________

# What's Next

[Microservices Architecture](38-microservices-architecture.md)
