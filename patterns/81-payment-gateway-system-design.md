# System Design - Part 81

# Payment Gateway System Design (Stripe / Razorpay)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- Payment lifecycle
- Payment Gateway Architecture
- Payment States
- Idempotency
- Webhooks
- Double Spending Prevention
- Ledger
- Reconciliation
- Refunds
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a Payment Gateway like Stripe or Razorpay.**

Unlike

Amazon,

where payments

are just

one component,

here

payments

are

the entire system.

The biggest challenges

are:

- Money safety
- Exactly-once processing
- High reliability
- Fraud prevention
- Financial reconciliation

Unlike

social media,

a duplicated payment

is unacceptable.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Create payment
- Process payment
- Payment status
- Refunds
- Webhooks
- Payment history
- Merchant dashboard

Optional

- UPI
- Cards
- Net Banking
- Wallets
- EMI
- International payments

______________________________________________________________________

# Non-Functional Requirements

- Strong consistency
- High availability
- Security
- Low latency
- No duplicate payments
- Auditability

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the gateway

processes

```text id="pg8101"
100 Million

Payments/day
```

Peak traffic

```text id="pg8102"
25,000 TPS
```

Every payment

produces

multiple events:

- Authorization
- Capture
- Settlement
- Notification
- Ledger entry

______________________________________________________________________

# Step 3

# API Design

Create Payment

```http id="pg8103"
POST /payments
```

______________________________________________________________________

Get Payment

```http id="pg8104"
GET /payments/{id}
```

______________________________________________________________________

Refund

```http id="pg8105"
POST /refunds
```

______________________________________________________________________

Webhook

```http id="pg8106"
POST /webhooks
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="pg8107"
Merchant

↓

API Gateway

↓

Payment Service

↓

Bank / Card Network

↓

Ledger Service

↓

Notification Service
```

Supporting services:

- Fraud Service
- Reconciliation Service
- Webhook Service
- Audit Service

______________________________________________________________________

# Payment Lifecycle

Interview favorite.

A payment

moves

through

multiple states.

```text id="pg8108"
Created

↓

Authorized

↓

Captured

↓

Settled
```

If

something fails,

additional states

may include:

```text id="pg8109"
Failed

Cancelled

Refunded
```

______________________________________________________________________

# Authorization vs Capture

Interview favorite.

Authorization

means

the bank

reserves

the money.

Capture

means

the money

is actually

transferred.

Example

Hotel booking.

Money

is authorized

during booking,

but

captured

after checkout.

______________________________________________________________________

# Payment Flow

```text id="pg8110"
Customer

↓

Merchant

↓

Payment Gateway

↓

Bank

↓

Response

↓

Merchant
```

The gateway

coordinates

the process,

it does not

hold

customer money.

______________________________________________________________________

# Idempotency

Interview favorite.

Suppose

the client

times out

after

sending

a payment request.

It retries.

Question.

Should

the payment

be charged

twice?

No.

______________________________________________________________________

# Idempotency Key

Clients

send

a unique key.

Example

```http id="pg8111"
Idempotency-Key:

abc123
```

If

the same key

is received again,

return

the previous result

instead of

processing

another payment.

______________________________________________________________________

# Why Idempotency Matters

Without it

```text id="pg8112"
Retry

↓

Charge Again
```

With it

```text id="pg8113"
Retry

↓

Same Response
```

Money

is charged

exactly once.

______________________________________________________________________

# Double Spending Prevention

Interview favorite.

Suppose

two requests

attempt

to spend

the same balance

simultaneously.

Solutions:

- Database transactions
- Row-level locking
- Optimistic locking
- Distributed locking

Consistency

is critical.

______________________________________________________________________

# Ledger

Interview favorite.

A ledger

is

the financial

source of truth.

Never

update balances

directly.

Instead,

record

transactions.

Example

```text id="pg8114"
Debit

Customer

100
```

```text id="pg8115"
Credit

Merchant

100
```

Balances

are derived

from

ledger entries.

______________________________________________________________________

# Double-Entry Accounting

Every transaction

has

two entries.

```text id="pg8116"
Debit

↓

Credit
```

Money

never

appears

or disappears.

This is

how

banks

maintain

financial accuracy.

______________________________________________________________________

# Webhooks

Interview favorite.

After

payment success,

notify

the merchant.

Workflow

```text id="pg8117"
Payment

↓

Webhook

↓

Merchant Server
```

Merchants

should not

continuously poll

for payment status.

______________________________________________________________________

# Webhook Retry

Suppose

the merchant's

server

is unavailable.

Retry.

```text id="pg8118"
Webhook

↓

Retry

↓

Retry

↓

Success
```

Retries

should use

exponential backoff.

______________________________________________________________________

# Refunds

Workflow

```text id="pg8119"
Refund Request

↓

Payment Service

↓

Bank

↓

Ledger

↓

Merchant
```

Refunds

are

new transactions,

not

modifications

of old ones.

______________________________________________________________________

# Reconciliation

Interview favorite.

Question.

What if

your database

shows

payment success,

but

the bank

shows failure?

Reconciliation

compares

internal records

with

bank records.

```text id="pg8120"
Gateway

↓

Bank

↓

Compare

↓

Fix
```

Usually

performed

periodically.

______________________________________________________________________

# Fraud Detection

Fraud Service

evaluates:

- Unusual spending
- Device fingerprint
- Location
- Velocity checks
- Previous fraud history

High-risk payments

may require

additional verification.

______________________________________________________________________

# Notifications

Payment events

are asynchronous.

```text id="pg8121"
Payment Success

↓

Kafka

↓

Notification Service

↓

Email / SMS
```

The customer

doesn't wait

for notifications.

______________________________________________________________________

# Database Schema

Payments

```text id="pg8122"
payment_id

merchant_id

customer_id

amount

currency

status

created_at
```

Ledger

```text id="pg8123"
entry_id

payment_id

account

debit

credit

timestamp
```

______________________________________________________________________

# Caching

Redis stores:

- Merchant configuration
- API rate limits
- Session tokens

Never

store

financial balances

only

inside Redis.

The database

and ledger

remain

the source of truth.

______________________________________________________________________

# Scaling

Scale independently:

- Payment Service
- Ledger Service
- Fraud Service
- Webhook Service
- Reconciliation Service

Payment processing

must remain

stateless.

______________________________________________________________________

# AI/ML Example

Machine Learning

helps detect:

- Card fraud
- Fake merchants
- Money laundering
- Account takeover
- Suspicious transactions

Models

assign

a risk score

before

approving

payments.

______________________________________________________________________

# Failure Scenario

Suppose

the merchant

doesn't receive

the payment response.

The client

retries

using

the same

Idempotency Key.

The gateway

returns

the existing result.

No duplicate charge

occurs.

______________________________________________________________________

# Another Failure

Suppose

the webhook

fails.

Payment

remains successful.

The Webhook Service

continues

retrying

until

delivery succeeds

or

the retry policy

expires.

______________________________________________________________________

# End-to-End Architecture

```text id="pg8124"
Customer

↓

Merchant

↓

API Gateway

↓

Payment Service

↓

Bank / Card Network

↓

Ledger Service

↓

PostgreSQL

↓

Kafka

↓

Webhook Service

↓

Notification Service

↓

Fraud Service

↓

Reconciliation Service
```

______________________________________________________________________

# Trade-offs

Ledger

vs

Balance Table

| Ledger | Balance Table |
| ------------------ | ---------------- |
| Auditable | Simple |
| Immutable | Updates in-place |
| Financial accuracy | Easier queries |

______________________________________________________________________

Polling

vs

Webhooks

| Polling | Webhooks |
| ------------------- | -------------- |
| Continuous requests | Event-driven |
| Higher load | Lower load |
| Delayed updates | Near real-time |

______________________________________________________________________

Synchronous

vs

Asynchronous Notifications

| Sync | Async |
| -------------- | --------------------- |
| Slower payment | Faster payment |
| User waits | Background processing |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a Payment Gateway?

Start by separating payment processing from supporting services such as fraud detection, ledgers, reconciliation,
notifications, and webhooks. Every payment follows a lifecycle from creation to authorization, capture, settlement, and
possible refund. Use idempotency keys to guarantee exactly-once payment processing when clients retry requests. Record
all financial operations using an immutable double-entry ledger instead of directly updating balances. Integrate with
banks and payment networks through dedicated connectors, notify merchants using webhooks with retry mechanisms, and
periodically reconcile internal records with bank settlement reports. Scale services independently while ensuring strong
consistency for financial data and high availability for payment processing.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Payment lifecycle
- Authorization vs Capture
- Idempotency
- Double spending prevention
- Double-entry ledger
- Webhooks
- Refunds
- Reconciliation
- Fraud detection
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram
- ✅ Twitter/X
- ✅ YouTube
- ✅ Netflix
- ✅ Spotify
- ✅ Google Drive
- ✅ Uber
- ✅ Amazon
- ✅ Payment Gateway

You now understand one of the most critical financial distributed systems, where correctness, consistency, and
auditability are more important than raw throughput.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design a system that almost every modern application depends on:

- Multi-channel delivery
- Email
- SMS
- Push Notifications
- Scheduling
- Retry mechanisms
- Dead Letter Queues (DLQ)
- User preferences
- Rate limiting

We'll design a **Notification Service**.

______________________________________________________________________

# What's Next

[Notification Service System Design](82-notification-service-system-design.md)
