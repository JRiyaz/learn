# Advanced Distributed Systems – Designing Stripe

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand how a platform like Stripe processes billions of payment requests, maintains financial correctness, provides APIs to developers, ensures idempotency, supports webhooks, and scales globally.

______________________________________________________________________

# Introduction

Stripe

is not

just

a Payment Gateway.

It is

a complete

financial platform.

It provides

- Payment Processing
- Payment APIs
- Subscription Billing
- Invoicing
- Refunds
- Payouts
- Fraud Detection
- Webhooks
- Connect Platform
- Developer SDKs

The biggest challenge

is

```
Financial Correctness

at

Global Scale
```

______________________________________________________________________

# Functional Requirements

Assume

our platform

supports

- Card Payments
- UPI
- Wallets
- Bank Transfers
- Refunds
- Payouts
- Subscriptions
- Webhooks
- Payment Links
- Developer APIs

______________________________________________________________________

# Non-Functional Requirements

Need

- Strong Consistency
- High Availability
- Idempotency
- PCI Compliance
- Low Latency
- Fault Tolerance
- Global Scalability

______________________________________________________________________

# High-Level Architecture

```
                  Merchant

                     │

                     ▼

              Stripe REST API

                     │

      ┌──────────────┼───────────────┐

      ▼              ▼               ▼

 Payment Service Billing Service Connect Service

      │              │               │

      ▼              ▼               ▼

 Fraud Engine    Ledger Service   Webhook Service

      │

      ▼

 Bank / Card Network / PSP
```

______________________________________________________________________

# Core Services

Stripe

is composed

of

many independent

services.

- API Gateway
- Authentication
- Payment Service
- Billing Service
- Subscription Service
- Ledger Service
- Fraud Detection
- Webhook Service
- Settlement Service
- Connect Service

______________________________________________________________________

# Payment Flow

```
Merchant

↓

Create Payment

↓

Stripe

↓

Bank

↓

Authorization

↓

Capture

↓

Response
```

______________________________________________________________________

# API First Design

Interview favorite.

Everything

is exposed

through APIs.

Examples

```
POST /payment_intents
```

```
POST /customers
```

```
POST /refunds
```

```
POST /subscriptions
```

Developers

integrate

using

APIs

instead of

building

payment infrastructure.

______________________________________________________________________

# Payment Intent

Interview favorite.

Stripe

doesn't

immediately

charge

the card.

Instead

it creates

```
Payment Intent
```

Lifecycle

```
Created

↓

Requires Payment Method

↓

Processing

↓

Succeeded

or

Failed
```

______________________________________________________________________

# Why Payment Intent?

Supports

- Authentication
- Retries
- Multiple payment methods
- Asynchronous payments
- Better tracking

______________________________________________________________________

# Idempotency

Interview favorite.

Every

payment request

may include

```
Idempotency-Key
```

Example

```
abc-123
```

If

the client

retries

Stripe

returns

the original result.

Never

creates

another payment.

______________________________________________________________________

# Customer Objects

Stripe

stores

customers.

Example

```
Customer

↓

Cards

↓

Subscriptions

↓

Invoices
```

Developers

reference

customer IDs

instead

of

raw card data.

______________________________________________________________________

# Tokenization

Interview favorite.

Instead of

storing

card numbers

Stripe stores

```
Payment Method Token
```

Example

```
pm_xxxxx
```

Sensitive

payment data

remains protected.

______________________________________________________________________

# Ledger

Interview favorite.

Every

financial operation

creates

ledger entries.

Example

```
Customer

Debit

↓

Platform

Credit
```

Balances

are derived

from

ledger entries,

not

mutable totals.

______________________________________________________________________

# Double Entry Accounting

Every transaction

contains

both

```
Debit

↓

Credit
```

Money

cannot

appear

or disappear.

______________________________________________________________________

# Refund Flow

```
Refund Request

↓

Validation

↓

Ledger Entry

↓

Bank

↓

Refund Complete
```

Refunds

are also

tracked

inside

the ledger.

______________________________________________________________________

# Subscriptions

Stripe

supports

recurring payments.

```
Subscription

↓

Scheduler

↓

Invoice

↓

Payment

↓

Renewal
```

Recurring billing

is handled

automatically.

______________________________________________________________________

# Billing Engine

Responsible for

- Invoice generation
- Taxes
- Coupons
- Discounts
- Proration
- Renewals

______________________________________________________________________

# Connect

Interview favorite.

Stripe Connect

supports

marketplaces.

Example

```
Customer

↓

Platform

↓

Seller
```

Money

must be

distributed

correctly

between

multiple parties.

______________________________________________________________________

# Payouts

Merchants

don't receive

money

immediately.

```
Payments

↓

Settlement

↓

Payout

↓

Merchant Bank
```

______________________________________________________________________

# Fraud Detection

Stripe Radar

uses

risk analysis.

Examples

- Device fingerprint
- IP reputation
- Velocity
- Country
- Previous fraud
- Machine learning signals

High-risk

payments

may be

blocked

or require

additional verification.

______________________________________________________________________

# Webhooks

Interview favorite.

Merchants

receive

events.

Examples

```
payment.succeeded
```

```
invoice.created
```

```
refund.completed
```

```
subscription.updated
```

______________________________________________________________________

# Webhook Delivery

```
Stripe

↓

Webhook Queue

↓

Merchant

↓

200 OK
```

If

merchant

doesn't respond

retry

using

exponential backoff.

______________________________________________________________________

# Webhook Verification

Never trust

incoming

webhooks.

Verify

cryptographic

signatures

before

processing.

______________________________________________________________________

# Event Driven Architecture

Stripe

uses

events.

```
Payment Success

↓

Event

↓

Billing

↓

Notification

↓

Analytics
```

Services

remain

loosely coupled.

______________________________________________________________________

# Saga Pattern

Interview favorite.

Payment

affects

multiple services.

```
Payment

↓

Ledger

↓

Invoice

↓

Email

↓

Analytics
```

Use

Saga

instead of

distributed transactions.

______________________________________________________________________

# Global Architecture

Stripe

operates

worldwide.

```
Region A

Region B

Region C
```

Requests

are routed

to

the nearest

healthy region.

______________________________________________________________________

# Database Design

Payments

| id | status | amount |

Customers

| id | email |

Payment Methods

| id | customer |

Ledger

| entry | debit | credit |

Invoices

| id | status |

Subscriptions

| id | plan |

______________________________________________________________________

# Caching

Cache

only

safe,

non-financial

data.

Examples

- Customer profile
- Products
- Pricing
- Configuration

Do

not

treat cache

as

the source

of truth

for balances.

______________________________________________________________________

# Monitoring

Monitor

- Payment success rate
- Authorization latency
- Capture latency
- Webhook failures
- Fraud rate
- API latency
- Retry count
- Settlement delay

______________________________________________________________________

# Failure Scenarios

## Bank Timeout

Retry

using

idempotency.

______________________________________________________________________

## Merchant Retries

Return

existing result

using

Idempotency-Key.

______________________________________________________________________

## Webhook Failure

Retry

delivery

with

backoff.

______________________________________________________________________

## Fraud Service Down

Continue

with

fallback rules

or

queue

manual review,

depending on

risk policy.

______________________________________________________________________

## Region Failure

Route

traffic

to

another

healthy region,

subject to

business continuity

requirements.

______________________________________________________________________

# Typical Architecture

```
                 Merchant

                     │

                     ▼

               API Gateway

                     │

     ┌───────────────┼────────────────┐

     ▼               ▼                ▼

 Payment Service Billing Service Connect Service

     │               │                │

     ▼               ▼                ▼

 Ledger Service Fraud Engine Webhook Queue

     │

     ▼

 Bank / Card Network
```

______________________________________________________________________

# Common Interview Questions

## Why does Stripe use Payment Intents?

Payment Intents model the entire payment lifecycle, allowing authentication, retries, asynchronous payment methods, and
better state management.

______________________________________________________________________

## Why is the Ledger immutable?

Financial history must never be rewritten. Immutable ledger entries provide accurate auditing, reconciliation, and
balance calculation.

______________________________________________________________________

## Why use webhooks?

Payment processing is often asynchronous. Webhooks notify merchants when important events occur without requiring
continuous polling.

______________________________________________________________________

## Why is idempotency mandatory?

Network failures and retries are inevitable. Idempotency guarantees that retrying the same payment request does not
create duplicate charges.

______________________________________________________________________

## Why doesn't Stripe store raw card numbers?

Tokenization reduces exposure to sensitive data and helps satisfy strict security and compliance requirements such as
PCI DSS.

______________________________________________________________________

# Common Mistakes

## Mutable Balances

Always

derive balances

from

ledger entries.

______________________________________________________________________

## No Idempotency

Retries

can cause

duplicate charges.

______________________________________________________________________

## Trusting Webhooks

Always

verify

webhook signatures.

______________________________________________________________________

## Caching Financial State

Never

treat cache

as

the source

of truth

for financial correctness.

______________________________________________________________________

## Tight Service Coupling

Prefer

events

and

asynchronous communication

where appropriate.

______________________________________________________________________

# Best Practices

✅ Use Payment Intents.

✅ Implement idempotency.

✅ Maintain an immutable ledger.

✅ Verify webhook signatures.

✅ Tokenize payment methods.

✅ Use event-driven communication.

✅ Monitor financial operations continuously.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is Stripe considered API-first?

### Answer

Stripe exposes nearly all payment functionality through well-designed APIs and SDKs, enabling developers to integrate
complex payment workflows without building payment infrastructure themselves.

______________________________________________________________________

## Question

Why is an immutable ledger important?

### Answer

An immutable ledger records every debit and credit without modifying historical entries. This guarantees accurate
auditing, reconciliation, and financial reporting.

______________________________________________________________________

## Question

How does Stripe prevent duplicate charges?

### Answer

Clients send an Idempotency-Key with payment requests. If the request is retried due to a timeout or network issue,
Stripe returns the original response instead of creating another payment.

______________________________________________________________________

# Practice Exercise

Design

a platform

like

Stripe.

Explain

1. Payment Intents
1. Idempotency
1. Ledger
1. Double-entry accounting
1. Fraud detection
1. Billing
1. Connect
1. Webhooks
1. Monitoring
1. Failure recovery
1. Global architecture
1. Trade-offs

Present

your solution

within

60 minutes,

similar to

a Senior Backend Engineer

System Design interview.

______________________________________________________________________

# Summary

Stripe is one of the best advanced System Design interview topics because it combines API design, distributed systems,
financial correctness, security, scalability, and developer experience.

A strong solution should demonstrate

- API-first architecture
- Payment Intents
- Idempotency
- Immutable ledger
- Double-entry accounting
- Fraud detection
- Billing and subscriptions
- Webhooks
- Event-driven architecture
- Monitoring
- Trade-off analysis

Mastering Stripe prepares you for interviews at fintech companies, payment providers, banks, and other large-scale
financial platforms.

______________________________________________________________________

# Next

[42. Designing Slack](42-design-slack.md)
