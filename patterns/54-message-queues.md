# System Design - Part 54

# Message Queues

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Message Queue is
- Why Message Queues exist
- Synchronous vs Asynchronous Communication
- Queue Producers and Consumers
- Message Broker
- Point-to-Point Messaging
- Queue Acknowledgements
- Dead Letter Queue (DLQ)
- Kafka vs RabbitMQ vs Amazon SQS
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

allows

members

to borrow books.

When

a book

is borrowed,

the system must:

- Save the loan
- Send an email
- Send an SMS
- Update analytics
- Update recommendations
- Generate an audit log

Initially,

the application

does

everything

inside

one request.

______________________________________________________________________

# The Problem

```text id="mq5401"
Client

↓

Borrow API

↓

Save Loan

↓

Send Email

↓

Send SMS

↓

Update Analytics

↓

Update Recommendations

↓

Return Response
```

Question.

When does

the client

receive

the response?

Only after

every task

finishes.

______________________________________________________________________

# Problems

Suppose

Email Service

takes

5 seconds.

The user

waits

5 seconds.

Suppose

Analytics

fails.

Should

borrowing

the book

also fail?

Probably not.

The application

has become

tightly coupled.

______________________________________________________________________

# The Idea

Separate

important work

from

background work.

Return

the response

immediately.

Process

the remaining work

later.

______________________________________________________________________

# What is a Message Queue?

A **Message Queue**

is a communication mechanism

that allows

one application

to send messages

to another application

asynchronously.

Instead of

communicating directly,

applications

exchange

messages

through

a queue.

______________________________________________________________________

# Architecture

```text id="mq5402"
Producer

↓

Message Queue

↓

Consumer
```

The Producer

creates messages.

The Queue

stores messages.

The Consumer

processes messages.

______________________________________________________________________

# Producer

A **Producer**

creates

and sends

messages.

Example

```text id="mq5403"
Borrow Service

↓

BookBorrowed Event
```

The Producer

doesn't wait

for

the Consumer

to finish.

______________________________________________________________________

# Consumer

A **Consumer**

reads

messages

from

the queue

and processes them.

Example

```text id="mq5404"
Email Worker

↓

Send Email
```

Multiple consumers

can process

messages

in parallel.

______________________________________________________________________

# Message Broker

The software

that manages

the queue

is called

a

**Message Broker**.

Examples:

- RabbitMQ
- Apache Kafka
- Amazon SQS
- Azure Service Bus
- Google Pub/Sub

______________________________________________________________________

# Synchronous Communication

Without

Message Queues

```text id="mq5405"
Borrow Service

↓

Email Service

↓

Wait
```

The caller

must wait

for

the response.

______________________________________________________________________

# Asynchronous Communication

With

Message Queues

```text id="mq5406"
Borrow Service

↓

Queue

↓

Return Response

↓

Email Worker
```

The user

gets

an immediate response.

Background work

continues later.

______________________________________________________________________

# Queue Example

Suppose

100 emails

must be sent.

Instead of

sending them

inside

the request,

enqueue them.

```text id="mq5407"
Email 1

Email 2

Email 3

...

Email 100
```

Workers

process

them

one by one.

______________________________________________________________________

# FIFO Queue

FIFO means

\*\*First In,

First Out.\*\*

Example

```text id="mq5408"
Message A

↓

Message B

↓

Message C
```

Processing order

remains

A → B → C.

Useful

when

ordering matters.

______________________________________________________________________

# Multiple Consumers

Suppose

one worker

cannot

process messages

fast enough.

Add

more workers.

```text id="mq5409"
Queue

↓

Worker 1

Worker 2

Worker 3
```

Each worker

processes

different messages.

Throughput

increases.

______________________________________________________________________

# Message Acknowledgement

Suppose

a Consumer

successfully processes

a message.

It sends

an

**Acknowledgement (ACK).**

```text id="mq5410"
Message

↓

Processed

↓

ACK
```

The broker

removes

the message

only after

receiving

the ACK.

______________________________________________________________________

# What Happens if a Worker Crashes?

Suppose

a Consumer

crashes

before

sending

an ACK.

```text id="mq5411"
Worker

❌
```

The broker

still has

the message.

Another worker

can process it.

This improves

reliability.

______________________________________________________________________

# Message Retry

Sometimes,

processing fails.

Example

Email Server

is temporarily down.

The broker

can retry

processing.

```text id="mq5412"
Attempt 1

↓

Failed

↓

Attempt 2

↓

Success
```

______________________________________________________________________

# Dead Letter Queue (DLQ)

Suppose

a message

fails

10 times.

Should

the broker

retry forever?

No.

Move it

to

a

**Dead Letter Queue (DLQ).**

```text id="mq5413"
Queue

↓

Failed

↓

DLQ
```

Developers

can inspect

these messages

later.

______________________________________________________________________

# Queue Length

A useful metric

is

queue length.

Suppose

10 messages

arrive

every second,

but

workers process

only

5.

The queue

keeps growing.

This indicates

the system

needs

more consumers

or

faster processing.

______________________________________________________________________

# FastAPI Example

Suppose

a member

borrows

a book.

Instead of

sending

an email

directly,

the API

publishes

a message.

```python id="mq5414"
POST /borrow

↓

save_loan()

↓

queue.publish(
    "SendEmail"
)
```

The API

returns

immediately.

______________________________________________________________________

# AI/ML Example

Suppose

users upload

images.

Image processing

takes

30 seconds.

Instead of

making

the user wait,

enqueue

the task.

```text id="mq5415"
Upload

↓

Queue

↓

ML Worker

↓

Inference
```

The user

receives

an upload confirmation

immediately.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

After

an order

is placed,

background jobs

include:

- Email confirmation
- Inventory update
- Recommendation update
- Analytics
- Fraud detection

Each task

can be

processed

independently

through

message queues.

______________________________________________________________________

# RabbitMQ vs Kafka vs Amazon SQS

Interview favorite.

| RabbitMQ | Kafka | Amazon SQS |
| --------------------------------- | --------------------------- | ---------------------------- |
| Traditional Message Queue | Distributed Event Streaming | Managed Cloud Queue |
| Removes message after consumption | Retains messages | Fully managed |
| Complex routing | Very high throughput | No infrastructure management |
| Task processing | Event streaming | Cloud applications |

______________________________________________________________________

# Queue vs Pub/Sub

Another

interview question.

| Queue | Pub/Sub |
| ---------------------------------------- | ------------------------------------------- |
| One consumer usually processes a message | Multiple consumers receive the same message |
| Task distribution | Event broadcasting |

We'll study

Pub/Sub

in

the next lesson.

______________________________________________________________________

# Message Queue vs API Call

| API Call | Message Queue |
| ------------------ | --------------------- |
| Immediate response | Background processing |
| Tight coupling | Loose coupling |
| Client waits | Client doesn't wait |

______________________________________________________________________

# Benefits

Message Queues provide:

✅ Asynchronous processing

✅ Loose coupling

✅ Better scalability

✅ Retry capability

✅ Improved reliability

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Eventual consistency

❌ Message ordering challenges

❌ Operational complexity

❌ Duplicate message handling

______________________________________________________________________

# Idempotency

Suppose

the same message

is delivered

twice.

Example

```text id="mq5416"
Send Welcome Email
```

The consumer

should ensure

the email

isn't sent

twice.

Consumers

should be

**idempotent.**

______________________________________________________________________

# Monitoring

Monitor

these metrics:

- Queue length
- Processing rate
- Retry count
- DLQ size
- Processing latency

These help

identify

backlogs

before

they become

production issues.

______________________________________________________________________

# Real Company Example

Ride-sharing platforms

use

message queues

to process:

- Trip completion
- Receipt generation
- Driver incentives
- Notifications
- Analytics

The rider

doesn't wait

for

all these tasks

before

seeing

"Trip Completed."

______________________________________________________________________

# When NOT to Use Message Queues

Don't use

Message Queues

when:

- Immediate response

is required

- Strong consistency

is mandatory

- The operation

must complete

before

returning

to the client

Examples:

- Login authentication
- Payment authorization
- OTP verification

______________________________________________________________________

# Best Practices

✅ Keep messages small.

✅ Make consumers idempotent.

✅ Use DLQs for failed messages.

✅ Monitor queue health.

______________________________________________________________________

# Common Mistakes

### Sending Huge Messages

Large messages

reduce

throughput.

Store

large payloads

externally

and

send

references.

______________________________________________________________________

### Infinite Retries

Retrying forever

can overload

the system.

Use

retry limits

and

DLQs.

______________________________________________________________________

### Ignoring Message Ordering

Some workflows

require

strict ordering.

Choose

the appropriate

queue configuration.

______________________________________________________________________

### Treating the Queue as a Database

Queues

are designed

for

message delivery,

not

long-term storage.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Message Queue, and why is it used?

A Message Queue is an asynchronous communication mechanism that allows producers to send messages to consumers through a
broker without requiring both systems to communicate directly. It decouples services, improves scalability, enables
background processing, and provides features such as retries, acknowledgements, and Dead Letter Queues. Message Queues
are commonly used for tasks like sending emails, processing images, generating reports, and handling background jobs
without increasing API response times.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a Message Queue is
- Producer and Consumer
- Message Broker
- FIFO
- ACKs
- Retries
- Dead Letter Queue (DLQ)
- RabbitMQ vs Kafka vs SQS
- FastAPI example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand another essential building block of scalable systems:

- ✅ Message Queues

This is the foundation for **event-driven architectures**, where services communicate through events instead of direct
API calls.

______________________________________________________________________

# What's Next

[Event-Driven Architecture](55-event-driven-architecture.md)
