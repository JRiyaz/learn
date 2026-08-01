# Software Design & Design Patterns - Part 23

# Command Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Command Pattern is
- Why the Command Pattern exists
- The problem it solves
- Commands, Receivers, and Invokers
- Undo and Queue support
- Real-world backend examples
- FastAPI examples
- Message Queue examples
- When NOT to use the Command Pattern

______________________________________________________________________

# Before We Start

Imagine

you click

**Borrow Book**

in a web application.

Should

the button

know

how to:

- Validate inventory
- Update the database
- Calculate fines
- Send emails
- Publish Kafka events

No.

The button

should simply say

> "Execute the borrow operation."

This idea

is the foundation

of the Command Pattern.

______________________________________________________________________

# The Problem

Let's continue

our

**Library Management System**.

A developer writes

```python id="cmd2301"
@app.post("/borrow")
def borrow_book():

    inventory.check()

    repository.save()

    email.send()

    kafka.publish()
```

Everything works.

______________________________________________________________________

# Another Requirement

Now,

we need

to support

scheduled borrowing.

Tomorrow,

the business wants

retry.

Next,

background execution.

Then,

audit history.

Eventually,

undo.

The endpoint

keeps changing.

______________________________________________________________________

# What's the Problem?

The endpoint

directly executes

the operation.

There's no way

to:

- Queue it
- Retry it
- Log it
- Undo it
- Execute later

The operation

is tightly coupled

to the caller.

______________________________________________________________________

# The Idea

Instead of

executing

the work directly,

wrap it

inside

an object.

That object

represents

a command.

The caller

simply says

```text id="cmd2302"
Execute Command
```

without knowing

what happens internally.

______________________________________________________________________

# What is the Command Pattern?

The **Command Pattern** says:

> **Encapsulate a request as an object.**

Instead of

calling methods,

create

objects

that represent

operations.

______________________________________________________________________

# The Components

The pattern

has four main parts.

```text id="cmd2303"
Client

↓

Command

↓

Receiver

↓

Invoker
```

Let's understand

each one.

______________________________________________________________________

# Client

Creates

the command.

Example

```python id="cmd2304"
BorrowBookCommand()
```

______________________________________________________________________

# Receiver

The receiver

knows

how to perform

the actual work.

```python id="cmd2305"
class LibraryService:

    def borrow_book(self):

        print(
            "Book Borrowed"
        )
```

______________________________________________________________________

# Command

Wraps

the receiver.

```python id="cmd2306"
from abc import (
    ABC,
    abstractmethod,
)

class Command(
    ABC
):

    @abstractmethod
    def execute(self):
        ...
```

______________________________________________________________________

# Borrow Command

```python id="cmd2307"
class BorrowBookCommand(
    Command
):

    def __init__(
        self,
        service,
    ):

        self.service = service

    def execute(self):

        self.service.borrow_book()
```

Notice

the command

contains

the request,

not

the implementation.

______________________________________________________________________

# Invoker

The invoker

doesn't know

what the command does.

```python id="cmd2308"
class Button:

    def click(
        self,
        command,
    ):

        command.execute()
```

______________________________________________________________________

# Using It

```python id="cmd2309"
service = LibraryService()

command = BorrowBookCommand(
    service
)

button = Button()

button.click(command)
```

The button

doesn't know

anything

about

borrowing books.

______________________________________________________________________

# Another Command

Tomorrow,

add

```python id="cmd2310"
ReturnBookCommand
```

The button

doesn't change.

It still executes

```python id="cmd2311"
command.execute()
```

______________________________________________________________________

# Undo Support

One reason

the Command Pattern

became famous

is

Undo.

Example

```text id="cmd2312"
Execute

↓

Undo

↓

Redo
```

Each command

knows

how to reverse

its own action.

Example

```python id="cmd2313"
execute()

undo()
```

Text editors,

Photoshop,

and IDEs

use this idea.

______________________________________________________________________

# Queue Support

Commands

can be stored

inside a queue.

```text id="cmd2314"
Queue

↓

Borrow Command

↓

Return Command

↓

Fine Command
```

Workers

execute them

later.

This makes

background processing

easy.

______________________________________________________________________

# Real Backend Example

Suppose

a customer

places an order.

Instead of

processing it

immediately,

create

```text id="cmd2315"
CreateOrderCommand
```

Push it

to RabbitMQ.

Workers

consume

the command

later.

This improves

scalability.

______________________________________________________________________

# Celery Example

Celery tasks

closely resemble

the Command Pattern.

Instead of

calling

```python id="cmd2316"
send_email()
```

directly,

you enqueue

a task.

```python id="cmd2317"
send_email.delay()
```

The task

represents

the work

to be executed later.

______________________________________________________________________

# FastAPI Example

Instead of

processing

a report

inside

the request,

create

```python id="cmd2318"
GenerateReportCommand
```

Push it

to

Celery,

RQ,

or

Dramatiq.

Return

HTTP 202 Accepted.

The user

doesn't wait

for completion.

______________________________________________________________________

# Kafka Example

Suppose

our API

publishes

```text id="cmd2319"
GenerateInvoice
```

A consumer

receives

the command

and executes it.

Again,

the sender

doesn't know

who processes

the request.

______________________________________________________________________

# Command vs Observer

Another interview favorite.

| Command | Observer |
| -------------------- | -------------------- |
| One action | One event |
| Execute a request | Notify subscribers |
| Usually one receiver | Often many receivers |

Example

```text
Borrow Book
```

↓

Command

↓

Library Service

Example

```text
Book Borrowed
```

↓

Observer

↓

Email

↓

Analytics

↓

Audit

The first

asks

something

to happen.

The second

announces

that

something

already happened.

______________________________________________________________________

# Command vs Strategy

| Strategy | Command |
| -------------------- | ------------------ |
| Different algorithms | Different requests |
| Focuses on behavior | Focuses on actions |

______________________________________________________________________

# Benefits

Command gives you:

✅ Queue support

✅ Retry support

✅ Undo support

✅ Audit history

✅ Delayed execution

✅ Loose coupling

______________________________________________________________________

# Drawbacks

Command also introduces:

❌ More classes

❌ More objects

❌ More abstraction

For very small applications,

this may be unnecessary.

______________________________________________________________________

# Real Company Example

Suppose

Amazon

receives

10 million orders

during Prime Day.

Instead of

processing everything

inside

the HTTP request,

commands

are placed

into queues.

Background workers

process them

independently.

This allows

the platform

to scale.

______________________________________________________________________

# When NOT to Use Command

Don't create

a command

for

every

simple method call.

Example

```python id="cmd2320"
user.get_name()
```

doesn't need

a command object.

Commands

are useful

when operations

need

queuing,

retry,

history,

or delayed execution.

______________________________________________________________________

# Best Practices

✅ Commands should represent one business action.

✅ Keep commands immutable when possible.

✅ Put business logic in receivers.

✅ Let commands delegate work.

______________________________________________________________________

# Common Mistakes

### Putting Business Logic Inside Commands

Commands

should coordinate,

not become

the business service.

______________________________________________________________________

### One Command Doing Everything

A command

should represent

one action.

______________________________________________________________________

### Confusing Commands with Events

Remember

Commands

tell

the system

what to do.

Events

tell

the system

what already happened.

______________________________________________________________________

### Ignoring Idempotency

Queued commands

may execute

more than once.

Design them

to handle retries safely.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Command Pattern, and where is it commonly used?

The Command Pattern is a behavioral design pattern that encapsulates a request as an object. This allows requests to be
queued, logged, retried, scheduled, or undone independently of the code that initiates them. It is widely used in
background job systems, task queues such as Celery, GUI applications, message-driven architectures, and distributed
systems where actions need to be executed asynchronously or reliably.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Command Pattern is
- Commands, Receivers, and Invokers
- Queue support
- Undo support
- FastAPI example
- Celery example
- Kafka example
- Command vs Observer
- Best practices

______________________________________________________________________

# What's Next

[Template Method Pattern](24-template-method-pattern.md)
