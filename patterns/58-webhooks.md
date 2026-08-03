# System Design - Part 58

# Webhooks

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Webhooks are
- Why Webhooks exist
- Polling vs Webhooks
- Webhook Flow
- Webhook Registration
- Webhook Delivery
- Retry Mechanisms
- Security (Signatures & Verification)
- Idempotency
- FastAPI implementation
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

uses

an external

Payment Gateway.

A member

pays

a fine.

Question.

How does

our application

know

whether

the payment

succeeded?

Should

our application

ask

the payment provider

every few seconds?

That works,

but

it's inefficient.

There is

a better solution.

______________________________________________________________________

# The Problem

Suppose

a payment

takes

30 seconds

to complete.

Without

Webhooks,

our application

keeps asking

the payment provider.

```text id="wh5801"
Our System

↓

"Payment Complete?"

↓

No

↓

Wait

↓

"Payment Complete?"
```

Most requests

return

"No."

Bandwidth

and

API calls

are wasted.

______________________________________________________________________

# The Idea

Instead of

asking repeatedly,

let

the payment provider

notify

our application

when

something happens.

______________________________________________________________________

# What is a Webhook?

A **Webhook**

is an HTTP callback

where

one application

automatically sends

an HTTP request

to another application

when

a specific event

occurs.

Instead of

polling,

the receiver

gets notified

immediately.

______________________________________________________________________

# Architecture

```text id="wh5802"
Payment Provider

↓

Webhook

↓

Our API
```

The sender

pushes

the event.

The receiver

doesn't poll.

______________________________________________________________________

# Webhook Flow

Step 1

Register

a callback URL.

```text id="wh5803"
https://example.com/webhooks/payment
```

Step 2

An event occurs.

Step 3

The provider

sends

an HTTP POST

to

the registered URL.

______________________________________________________________________

# Example

Suppose

payment succeeds.

The provider

sends

```text id="wh5804"
POST

/webhooks/payment
```

Payload

```json id="wh5805"
{
  "event": "payment.completed",
  "payment_id": "pay_123",
  "amount": 500
}
```

Our application

processes

the event.

______________________________________________________________________

# Polling vs Webhooks

Interview favorite.

| Polling | Webhooks |
| ------------------------- | ---------------------- |
| Client asks repeatedly | Server pushes updates |
| Many unnecessary requests | Only sends when needed |
| Higher latency | Near real-time |
| More API usage | More efficient |

______________________________________________________________________

# Registration

Most providers

require

applications

to register

their Webhook URL.

Example

```text id="wh5806"
Stripe

↓

Webhook URL
```

Whenever

an event

occurs,

Stripe

calls

that URL.

______________________________________________________________________

# Webhook Response

After

receiving

the event,

our server

should respond

quickly.

Example

```http id="wh5807"
HTTP 200 OK
```

This tells

the sender

that

the event

was received.

______________________________________________________________________

# Don't Process Immediately

Suppose

processing

takes

30 seconds.

Should

the Webhook

wait?

No.

Instead,

enqueue

the work.

```text id="wh5808"
Webhook

↓

Message Queue

↓

Worker
```

Return

HTTP 200

immediately.

Process

the event

in

the background.

______________________________________________________________________

# Retry Mechanism

Suppose

our server

is down.

The sender

tries again.

```text id="wh5809"
Attempt 1

↓

Failed

↓

Attempt 2

↓

Failed

↓

Attempt 3

↓

Success
```

Most providers

retry

failed deliveries.

______________________________________________________________________

# Duplicate Delivery

Suppose

the sender

never receives

our

HTTP 200.

It retries.

Now

our application

receives

the same event

twice.

This is expected.

______________________________________________________________________

# Idempotency

Webhook handlers

must be

**idempotent**.

Example

```text id="wh5810"
payment.completed
```

Processing

the same event

twice

must not

credit

the customer's account

twice.

______________________________________________________________________

# Security Problem

Anyone

could send

an HTTP POST

to

our endpoint.

How do we know

it came

from

the payment provider?

______________________________________________________________________

# Signature Verification

Most providers

sign

their requests.

Workflow

```text id="wh5811"
Payload

↓

Signature

↓

Verify Secret

↓

Accept
```

If

verification fails,

reject

the request.

______________________________________________________________________

# HTTPS

Webhook endpoints

should always use

HTTPS.

```text id="wh5812"
https://...
```

This protects

the payload

during transmission.

______________________________________________________________________

# FastAPI Example

Create

a webhook endpoint.

```python id="wh5813"
@app.post(
    "/webhooks/payment"
)
```

Inside

the endpoint:

- Verify signature
- Validate payload
- Publish to Queue
- Return 200

______________________________________________________________________

# AI/ML Example

Suppose

an AI platform

uses

an external

OCR provider.

The user

uploads

a document.

Processing

takes

2 minutes.

Instead of

polling,

the OCR service

calls

our webhook.

```text id="wh5814"
OCR Complete

↓

Webhook

↓

Our API
```

The application

continues

processing.

______________________________________________________________________

# GitHub Example

Suppose

someone

pushes

code

to GitHub.

GitHub

can call

a webhook.

```text id="wh5815"
Push Event

↓

Webhook

↓

CI/CD Pipeline
```

Builds

start

automatically.

______________________________________________________________________

# Stripe Example

Suppose

a customer

pays

an invoice.

Stripe

sends

```text id="wh5816"
invoice.paid
```

Our application

updates

the customer's

subscription

after

receiving

the webhook.

______________________________________________________________________

# Webhooks vs APIs

Interview favorite.

| API | Webhook |
| -------------------- | -------------------- |
| Client requests data | Server pushes events |
| Pull Model | Push Model |
| Synchronous | Event-driven |

Often,

systems

use

both.

______________________________________________________________________

# Webhooks vs Message Queues

Another

interview question.

| Webhook | Message Queue |
| ---------------------- | ---------------------------------- |
| HTTP callback | Internal messaging |
| Between applications | Usually inside distributed systems |
| Internet communication | Backend communication |

Sometimes,

a webhook

immediately

publishes

its event

to

a message queue.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

External services

send webhooks

for:

- Payment completed
- Shipment delivered
- Refund processed

The application

updates

its database

after

receiving

the webhook.

______________________________________________________________________

# Benefits

Webhooks provide:

✅ Near real-time updates

✅ Lower API usage

✅ Lower latency

✅ Efficient event delivery

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Retry handling

❌ Duplicate deliveries

❌ Security verification

❌ Public endpoint requirements

______________________________________________________________________

# Monitoring

Track:

- Successful deliveries
- Failed deliveries
- Retry count
- Processing latency
- Signature failures

These metrics

help detect

integration problems.

______________________________________________________________________

# When NOT to Use Webhooks

Avoid Webhooks

when:

- Immediate response

is required

inside

the same application

- The sender

cannot

reach

your server

- Simple synchronous

API calls

are sufficient

______________________________________________________________________

# Best Practices

✅ Verify request signatures.

✅ Respond quickly.

✅ Process asynchronously.

✅ Make handlers idempotent.

______________________________________________________________________

# Common Mistakes

### Doing Heavy Work in the Webhook

Don't spend

30 seconds

processing

inside

the webhook.

Publish

the event

to

a queue.

______________________________________________________________________

### Ignoring Retries

Webhook providers

retry

failed deliveries.

Your handler

must safely

handle duplicates.

______________________________________________________________________

### No Signature Verification

Never trust

incoming requests

without

verifying

their signature.

______________________________________________________________________

### Returning Non-200 Responses

If

processing succeeds,

return

HTTP 200

quickly,

or

the provider

may retry

the request.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Webhook, and how is it different from Polling?

A Webhook is an HTTP callback mechanism where one application automatically sends an HTTP request to another application
when a specific event occurs. Unlike polling, where a client repeatedly asks a server for updates, webhooks follow a
push model in which updates are delivered only when necessary. This reduces unnecessary network traffic, lowers latency,
and enables near real-time integrations. Because webhook deliveries may be retried, webhook handlers should verify
request signatures, respond quickly, and be idempotent.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Webhooks are
- Polling vs Webhooks
- Webhook Flow
- Registration
- Retry Mechanisms
- Signature Verification
- Idempotency
- FastAPI example
- Best practices

______________________________________________________________________

# 🧠 Communication Patterns Progress

You now understand the complete communication stack:

- ✅ REST APIs
- ✅ Message Queues
- ✅ Event-Driven Architecture
- ✅ Publish/Subscribe
- ✅ WebSockets
- ✅ Webhooks

These are the primary communication mechanisms used in modern distributed systems.

______________________________________________________________________

# 🚀 What's Coming Next

We've now completed the **Communication** section.

Next, we'll begin **Storage Systems**, starting with one of the most widely used components in cloud architecture:

- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- MinIO

These all implement the concept of **Object Storage**.

______________________________________________________________________

# What's Next

[Object Storage](59-object-storage.md)
