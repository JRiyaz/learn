# Advanced Distributed Systems – Designing a Payment Gateway

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand how payment gateways like Stripe, Razorpay, Adyen, or PayPal process payments securely, reliably, and at scale while preventing duplicate payments and ensuring consistency.

______________________________________________________________________

# Introduction

Every e-commerce platform

needs

payments.

Examples

- Amazon
- Flipkart
- Uber
- Swiggy
- Netflix

Behind

every payment

is

a Payment Gateway.

The biggest challenge

is not

processing money.

It is

```
Never

Charge

Twice
```

Even

during

network failures,

timeouts,

or retries.

______________________________________________________________________

# What Is A Payment Gateway?

A Payment Gateway

acts as

a secure bridge

between

the merchant,

customer,

banks,

and

payment networks.

```
Customer

↓

Merchant

↓

Payment Gateway

↓

Bank

↓

Card Network

↓

Bank
```

______________________________________________________________________

# Functional Requirements

Assume

the system

supports

- Card payments
- UPI
- Net Banking
- Wallets
- Refunds
- Payment Status
- Payment Retry
- Webhooks

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Strong Consistency
- Security
- PCI Compliance
- Low Latency
- Idempotency
- Auditability

______________________________________________________________________

# High-Level Architecture

```
                Customer
                    │
                    ▼
              Merchant App
                    │
                    ▼
             Payment Gateway API
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Payment Service Fraud Service Webhook Service
     │              │              │
     ▼              ▼              ▼
 Payment DB     Risk Engine     Queue
     │
     ▼
 Bank / PSP / Card Network
```

______________________________________________________________________

# Core Services

Separate

responsibilities.

- Payment API
- Payment Processor
- Fraud Detection
- Refund Service
- Webhook Service
- Notification Service
- Settlement Service
- Audit Service

______________________________________________________________________

# Payment Flow

```
Customer

↓

Checkout

↓

Payment Gateway

↓

Bank Authorization

↓

Response

↓

Merchant
```

______________________________________________________________________

# Payment Lifecycle

Interview favorite.

```
Created

↓

Authorized

↓

Captured

↓

Settled

↓

Completed
```

Other possible states

```
Failed

Cancelled

Expired

Refunded
```

______________________________________________________________________

# Authorization vs Capture

Interview favorite.

Authorization

```
Reserve Money
```

Capture

```
Actually Transfer Money
```

Hotels

and airlines

commonly

authorize first

and capture later.

______________________________________________________________________

# API Design

Create Payment

```
POST /payments
```

Get Status

```
GET /payments/{id}
```

Capture Payment

```
POST /payments/{id}/capture
```

Refund

```
POST /refunds
```

______________________________________________________________________

# Database Design

Payments

| payment_id | amount | status |

Refunds

| refund_id | payment_id |

Transactions

| txn_id | provider | status |

Audit Logs

| id | event | timestamp |

______________________________________________________________________

# Idempotency

Interview favorite.

Suppose

customer clicks

```
Pay
```

twice.

Or

network

times out.

Client retries.

Without

protection

```
Two Charges
```

______________________________________________________________________

# Idempotency Key

Client sends

```
Idempotency-Key

↓

abc123
```

Server

stores

the first result.

Future retries

with

the same key

return

the existing result

instead of

creating

a new payment.

______________________________________________________________________

# Request Flow

```
Request

↓

Idempotency Check

↓

Existing?

↓

Yes

↓

Return Previous Result
```

Otherwise

continue

payment processing.

______________________________________________________________________

# Why Idempotency Matters

Prevents

- Double charging
- Duplicate orders
- Duplicate refunds
- Duplicate payouts

______________________________________________________________________

# Payment Processing

```
Payment Request

↓

Validation

↓

Fraud Check

↓

Bank

↓

Response

↓

Store Result
```

______________________________________________________________________

# Fraud Detection

Before

processing

payments

check

- Velocity
- Device
- Location
- Blacklist
- Risk Score

High-risk

payments

may require

additional verification

or

be rejected.

______________________________________________________________________

# 3-D Secure

Interview bonus.

Some payments

require

additional authentication.

```
Customer

↓

OTP

↓

Bank

↓

Payment
```

Improves

security.

______________________________________________________________________

# Asynchronous Processing

Banks

may respond

later.

Use

queues.

```
Payment

↓

Queue

↓

Worker

↓

Bank
```

Merchant

can poll

or

receive

a webhook.

______________________________________________________________________

# Webhooks

Interview favorite.

Bank

or PSP

sends

payment updates.

```
Payment Success

↓

Webhook

↓

Merchant
```

Webhooks

must be

idempotent.

______________________________________________________________________

# Webhook Retry

Suppose

merchant server

is unavailable.

Retry

delivery

using

exponential backoff.

______________________________________________________________________

# Refund Flow

```
Refund Request

↓

Validation

↓

Bank

↓

Refund Complete
```

Refunds

should also

be idempotent.

______________________________________________________________________

# Settlement

Interview favorite.

Customer pays

today.

Merchant

receives

money later.

```
Payments

↓

Settlement Batch

↓

Merchant Bank
```

______________________________________________________________________

# Ledger

Never

calculate balances

from

current state.

Instead

record

every transaction.

```
Debit

Credit

Debit

Credit
```

This creates

an immutable

audit trail.

______________________________________________________________________

# Audit Logs

Record

every event.

Examples

- Payment Created
- Authorized
- Captured
- Failed
- Refunded

Never

modify

audit history.

______________________________________________________________________

# Distributed Transactions

Interview favorite.

Payment

updates

multiple services.

Example

```
Payment

↓

Order

↓

Inventory

↓

Notification
```

Use

```
Saga Pattern
```

instead of

distributed ACID

transactions.

______________________________________________________________________

# Retry Policy

Retry

only

temporary failures.

Examples

- Timeout
- HTTP 503
- Network errors

Don't retry

card declined

or

invalid requests.

______________________________________________________________________

# Circuit Breaker

Protect

downstream

bank APIs.

If

bank

is unavailable

```
Circuit Opens
```

Prevent

resource exhaustion.

______________________________________________________________________

# Security

Interview favorite.

Protect

payment data.

Use

- HTTPS
- Encryption
- Tokenization
- PCI DSS compliance
- Secrets management

Never

store

raw card numbers

unless

your system

is explicitly

designed

and certified

to do so.

______________________________________________________________________

# Tokenization

Instead of

storing

card number

```
4111...

```

Store

```
tok_xxxxx
```

Actual

card data

remains

with

the payment provider

or

secure vault.

______________________________________________________________________

# Monitoring

Monitor

- Success rate
- Failure rate
- Authorization latency
- Capture latency
- Refund rate
- Retry count
- Fraud rate
- Webhook failures

______________________________________________________________________

# Failure Scenarios

## Bank Timeout

Retry

with

idempotency.

______________________________________________________________________

## Merchant Retries

Return

previous payment

using

idempotency key.

______________________________________________________________________

## Webhook Failure

Retry

delivery

using

backoff.

______________________________________________________________________

## Database Failure

Promote

replica

and

recover

using

transaction logs.

______________________________________________________________________

## Payment Processor Down

Use

Circuit Breaker.

If available,

route

to

an alternate

processor.

______________________________________________________________________

# Typical Architecture

```
                 Customer
                     │
                     ▼
               Merchant App
                     │
                     ▼
            Payment Gateway API
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Payment Service Fraud Engine Webhook Service
      │              │              │
      ▼              ▼              ▼
   Payment DB     Redis Cache     Kafka
      │
      ▼
 Bank / Card Network / PSP
```

______________________________________________________________________

# Common Interview Questions

## Why is idempotency critical?

Network failures and retries are common during payments. Idempotency ensures the same payment request is processed only
once, preventing duplicate charges.

______________________________________________________________________

## Why separate authorization and capture?

Authorization reserves funds, while capture transfers them. Separating these steps allows businesses such as hotels and
airlines to confirm availability before collecting payment.

______________________________________________________________________

## Why use webhooks?

Payment providers may complete processing asynchronously. Webhooks notify merchants about payment status changes without
requiring continuous polling.

______________________________________________________________________

## Why keep an immutable ledger?

A ledger preserves every financial event, making audits, reconciliation, and dispute resolution reliable without losing
historical information.

______________________________________________________________________

## Why use Saga instead of distributed transactions?

Payments often involve multiple services. Saga coordinates local transactions with compensating actions, avoiding the
complexity of distributed ACID transactions.

______________________________________________________________________

# Common Mistakes

## No Idempotency

Can result

in

double charging.

______________________________________________________________________

## Storing Card Numbers

Prefer

tokenization

and

PCI-compliant providers.

______________________________________________________________________

## No Audit Trail

Financial systems

must preserve

transaction history.

______________________________________________________________________

## Infinite Retries

Retry

only

transient failures.

______________________________________________________________________

## Synchronous Webhooks

Process

webhooks

asynchronously

when appropriate.

______________________________________________________________________

# Best Practices

✅ Use idempotency keys.

✅ Tokenize sensitive payment data.

✅ Maintain an immutable ledger.

✅ Implement retries with backoff.

✅ Protect dependencies using Circuit Breakers.

✅ Verify webhook authenticity.

✅ Monitor payment health continuously.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the biggest challenge in payment systems?

### Answer

Maintaining correctness despite failures. The system must ensure customers are never charged twice while handling
retries, network failures, asynchronous processing, and downstream outages.

______________________________________________________________________

## Question

Why shouldn't card numbers be stored directly?

### Answer

Storing raw card data significantly increases security and compliance requirements. Tokenization minimizes exposure by
replacing sensitive card information with secure tokens.

______________________________________________________________________

## Question

How do you prevent duplicate payments?

### Answer

Require an idempotency key for payment creation. If the same request is retried, return the previously stored result
instead of creating a new transaction.

______________________________________________________________________

# Practice Exercise

Design

a Payment Gateway

for

Amazon.

Explain

1. Payment lifecycle
1. Authorization vs Capture
1. Idempotency
1. Fraud detection
1. Webhooks
1. Refunds
1. Settlement
1. Ledger
1. Security
1. Monitoring
1. Failure recovery
1. Trade-offs

Present

your solution

within

45–60 minutes,

similar to

a Senior Backend Engineer

System Design interview.

______________________________________________________________________

# Summary

Payment Gateways are among the most important distributed systems because they combine financial correctness, security,
reliability, and scalability.

A strong solution should demonstrate

- Payment lifecycle
- Authorization and capture
- Idempotency
- Fraud detection
- Webhooks
- Immutable ledger
- Tokenization
- Circuit Breakers
- Monitoring
- Trade-off analysis

Understanding Payment Gateway design prepares you for interviews at fintech companies, payment providers, banks, and
large e-commerce platforms.

______________________________________________________________________

# Next

[41. Designing Stripe](41-design-stripe.md)
