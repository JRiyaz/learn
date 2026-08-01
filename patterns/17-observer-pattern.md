# Software Design & Design Patterns - Part 17

# Observer Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Observer Pattern is
- Why the Observer Pattern exists
- The problems it solves
- Publishers and Subscribers
- Real-world backend examples
- FastAPI examples
- How Kafka, RabbitMQ, and Event-Driven Systems use this pattern
- When NOT to use the Observer Pattern

______________________________________________________________________

# Before We Start

Imagine this situation.

A member borrows a book.

What happens next?

The application should:

- Send an email
- Send an SMS
- Update analytics
- Update recommendations
- Write an audit log
- Notify the librarian
- Publish an event

Should the `LibraryService` know about all these?

Probably not.

Let's see why.

______________________________________________________________________

# The Problem

Our library service currently looks like this.

```python
class LibraryService:

    def borrow_book(
        self,
        book,
    ):

        print("Book Borrowed")

        email_service.send()

        sms_service.send()

        analytics.update()

        audit.log()

        recommendation.update()
```

Everything works.

______________________________________________________________________

# New Requirement

The business grows.

Now,

every time

a book is borrowed,

we also need to:

- Send a Slack notification
- Update Redis
- Notify Inventory
- Publish Kafka event
- Trigger ML pipeline

The method becomes

```python
borrow_book()

↓

Email

↓

SMS

↓

Analytics

↓

Audit

↓

Recommendations

↓

Slack

↓

Redis

↓

Inventory

↓

Kafka

↓

ML Pipeline
```

______________________________________________________________________

# What's the Problem?

The business logic

inside

`borrow_book()`

knows

too much.

Every new feature

requires modifying

the same method.

Problems:

❌ Tight coupling

❌ Difficult testing

❌ Violates OCP

❌ Difficult maintenance

______________________________________________________________________

# The Idea

Instead of

the library service

calling

every component,

let it simply announce

that

something happened.

Example

```text
Book Borrowed
```

Anyone interested

can respond.

The library service

doesn't care

who is listening.

______________________________________________________________________

# Real-World Example

Imagine

YouTube.

You upload

a new video.

Does YouTube

personally message

every subscriber?

No.

It simply says

```text
New Video Published
```

Subscribers

who are interested

receive the notification.

This is

the Observer Pattern.

______________________________________________________________________

# What is the Observer Pattern?

The **Observer Pattern** says:

> **When one object changes state, all interested objects are automatically notified.**

The object

being observed

is called

the **Subject**

or

**Publisher**.

The objects

receiving updates

are called

**Observers**

or

**Subscribers**.

______________________________________________________________________

# The Components

```text
LibraryService

↓

Publishes Event

↓

Email

SMS

Analytics

Audit

Inventory

Recommendations
```

The publisher

doesn't know

who receives

the event.

______________________________________________________________________

# Step 1

Create

an observer.

```python
from abc import (
    ABC,
    abstractmethod,
)

class Observer(
    ABC
):

    @abstractmethod
    def update(
        self,
        event,
    ):
        ...
```

______________________________________________________________________

# Step 2

Create

an Email Observer.

```python
class EmailObserver(
    Observer
):

    def update(
        self,
        event,
    ):

        print(
            "Email Sent"
        )
```

______________________________________________________________________

# Step 3

Analytics Observer.

```python
class AnalyticsObserver(
    Observer
):

    def update(
        self,
        event,
    ):

        print(
            "Analytics Updated"
        )
```

______________________________________________________________________

# Step 4

Publisher

```python
class EventPublisher:

    def __init__(self):

        self.observers = []

    def subscribe(
        self,
        observer,
    ):

        self.observers.append(
            observer
        )

    def publish(
        self,
        event,
    ):

        for observer in self.observers:

            observer.update(
                event
            )
```

______________________________________________________________________

# Step 5

Using It

```python
publisher = EventPublisher()

publisher.subscribe(
    EmailObserver()
)

publisher.subscribe(
    AnalyticsObserver()
)

publisher.publish(
    "BOOK_BORROWED"
)
```

Output

```text
Email Sent

Analytics Updated
```

The publisher

doesn't know

what each observer does.

______________________________________________________________________

# Adding a New Feature

Tomorrow,

the business wants

Slack notifications.

Create

```python
class SlackObserver(
    Observer
):

    def update(
        self,
        event,
    ):
        print(
            "Slack Notification"
        )
```

Subscribe it.

```python
publisher.subscribe(
    SlackObserver()
)
```

Done.

No changes

to

`LibraryService`.

No changes

to

`EventPublisher`.

______________________________________________________________________

# Real Backend Example

Suppose

an order

is placed.

Many systems

become interested.

```text
Order Created

↓

Inventory

↓

Payment

↓

Email

↓

Analytics

↓

Shipping

↓

Audit Logs
```

Instead of

calling

each one manually,

publish

an event.

______________________________________________________________________

# Kafka

Kafka

works similarly.

A producer

publishes

an event.

```text
BOOK_BORROWED
```

Consumers

subscribe.

```text
Email Service
```

```text
Recommendation Service
```

```text
Analytics Service
```

Each service

works independently.

______________________________________________________________________

# RabbitMQ

RabbitMQ

also follows

the same concept.

Producer

↓

Queue

↓

Consumers

The producer

doesn't know

who receives

the message.

______________________________________________________________________

# FastAPI Example

Suppose

your endpoint

creates a user.

Bad

```python
create_user()

↓

Send Email

↓

Update Cache

↓

Publish Event

↓

Write Audit
```

Better

```python
create_user()

↓

Publish

USER_CREATED
```

Other services

react

to the event.

The endpoint

stays simple.

______________________________________________________________________

# Event-Driven Architecture

The Observer Pattern

is the foundation

of

Event-Driven Architecture.

Examples:

- Kafka
- RabbitMQ
- AWS SNS
- AWS EventBridge
- Google Pub/Sub
- Redis Pub/Sub

Once you understand

Observer,

these technologies

become much easier.

______________________________________________________________________

# Benefits

Observer gives you:

✅ Loose coupling

✅ Easy extensibility

✅ Independent services

✅ Better scalability

✅ Easier maintenance

______________________________________________________________________

# Drawbacks

Observer also introduces

new challenges.

❌ Harder debugging

❌ Event ordering issues

❌ Duplicate events

❌ Event failures

Distributed systems

must handle

these carefully.

______________________________________________________________________

# When NOT to Use Observer

Suppose

your application

contains

one service

and

one database.

Creating

an event system

would be

overengineering.

Use Observer

when

multiple components

need to react

to the same event.

______________________________________________________________________

# Best Practices

✅ Publish business events.

✅ Keep observers independent.

✅ Make observers idempotent when possible.

✅ Don't let publishers know about implementation details.

______________________________________________________________________

# Common Mistakes

### Publishing Too Many Events

Not every function call

needs an event.

Publish

meaningful

business events.

______________________________________________________________________

### Putting Business Logic in the Publisher

The publisher

should only announce

what happened.

Observers

should perform

their own work.

______________________________________________________________________

### Tight Coupling Between Publisher and Observers

Publishers

should never depend

on specific observers.

______________________________________________________________________

### Ignoring Failures

If one observer fails,

decide whether

other observers

should continue.

This becomes

especially important

in distributed systems.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Observer Pattern, and where is it used?

The Observer Pattern is a behavioral design pattern in which one object (the publisher) notifies multiple interested
objects (observers) whenever an event occurs. This decouples the publisher from the subscribers, making the system
easier to extend and maintain. The pattern is widely used in event-driven architectures, messaging systems such as Kafka
and RabbitMQ, notification systems, audit logging, analytics pipelines, and microservices.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Observer Pattern is
- Publisher and Subscriber
- Backend examples
- FastAPI example
- Kafka and RabbitMQ
- Event-Driven Architecture
- Benefits
- Common mistakes

______________________________________________________________________

# What's Next

[Adapter Pattern](18-adapter-pattern.md)
