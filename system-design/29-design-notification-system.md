# System Design – Notification System

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how to design a scalable notification system capable of sending Email, SMS, Push Notifications, In-App Notifications, and Webhooks while handling billions of notifications reliably.

______________________________________________________________________

# Introduction

Every modern application

needs

notifications.

Examples

```
Amazon

↓

Order Confirmed
```

```
Uber

↓

Driver Arriving
```

```
WhatsApp

↓

New Message
```

```
Instagram

↓

New Follower
```

```
Netflix

↓

New Season Released
```

Sending

millions

or

billions

of notifications

is

a challenging

distributed systems problem.

______________________________________________________________________

# What Is A Notification System?

A Notification System

delivers

messages

to users

through

multiple channels.

Examples

- Email
- SMS
- Push Notifications
- In-App Notifications
- Webhooks

______________________________________________________________________

# Functional Requirements

Assume

our system

supports

- Email
- SMS
- Push Notifications
- In-App Notifications
- Scheduled Notifications
- Bulk Notifications
- Delivery Tracking
- Retry Mechanism

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Low Latency
- Reliability
- Scalability
- Fault Tolerance
- Retry Support

______________________________________________________________________

# Step 1

# High-Level Architecture

```
                   Applications
                         │
                         ▼
                 Notification API
                         │
                         ▼
                  Notification Queue
                         │
      ┌──────────────────┼───────────────────┐
      ▼                  ▼                   ▼
 Email Worker      SMS Worker       Push Worker
      │                  │                   │
      ▼                  ▼                   ▼
 Email Provider    SMS Provider     Push Provider
```

______________________________________________________________________

# Core Services

Separate

responsibilities.

- Notification API
- Template Service
- Queue
- Email Worker
- SMS Worker
- Push Worker
- Retry Service
- Preference Service
- Analytics Service

______________________________________________________________________

# APIs

Send Notification

```
POST /notifications
```

Get Status

```
GET /notifications/{id}
```

Cancel Scheduled Notification

```
DELETE /notifications/{id}
```

______________________________________________________________________

# Notification Request

Example

```json
{
  "userId": 100,
  "channel": "email",
  "template": "order_confirmation"
}
```

______________________________________________________________________

# Why Use A Queue?

Interview favorite.

Without

a queue

```
Application

↓

Email Provider
```

User

must wait

for

the email

to be sent.

Bad experience.

______________________________________________________________________

# Better Solution

```
Application

↓

Queue

↓

Response

↓

Worker

↓

Provider
```

Fast API.

Reliable processing.

______________________________________________________________________

# Why Separate Workers?

Email

SMS

and

Push

have

different providers,

different retry logic,

and

different throughput.

Separate workers

allow

independent scaling.

______________________________________________________________________

# Email Flow

```
Application

↓

Queue

↓

Email Worker

↓

SMTP / Email Provider

↓

User
```

______________________________________________________________________

# SMS Flow

```
Application

↓

Queue

↓

SMS Worker

↓

SMS Provider

↓

Phone
```

______________________________________________________________________

# Push Notification Flow

```
Application

↓

Queue

↓

Push Worker

↓

FCM / APNs

↓

Mobile Device
```

______________________________________________________________________

# In-App Notifications

Unlike

Email

or SMS,

In-App Notifications

are stored

inside

the application.

Example

```
Instagram

↓

Someone Liked

Your Photo
```

Store

inside

the database

and

retrieve

when

the user

opens

the app.

______________________________________________________________________

# Notification Templates

Avoid

hardcoding

messages.

Example

```
Order #{id}

has been shipped.
```

Replace

placeholders

during

processing.

______________________________________________________________________

# Template Service

```
Template ID

↓

Load Template

↓

Replace Variables

↓

Send
```

Reusable

and

maintainable.

______________________________________________________________________

# User Preferences

Interview favorite.

Users

may disable

certain notifications.

Example

```
Marketing Email

↓

Disabled
```

```
Order Updates

↓

Enabled
```

Always

check

preferences

before

sending.

______________________________________________________________________

# Notification Priority

Different

notifications

have

different importance.

High

- OTP
- Payment Success
- Security Alerts

Medium

- Order Updates

Low

- Promotions
- Marketing Campaigns

Priority

can determine

queue selection

or processing order.

______________________________________________________________________

# Scheduled Notifications

Example

```
Meeting Reminder

Tomorrow

9 AM
```

Store

future notifications

until

their scheduled time.

______________________________________________________________________

# Scheduler

```
Database

↓

Scheduler

↓

Queue

↓

Worker
```

______________________________________________________________________

# Retry Mechanism

Interview favorite.

Suppose

Email Provider

is unavailable.

```
Send

↓

Failure

↓

Retry
```

Don't

retry

immediately.

______________________________________________________________________

# Exponential Backoff

Example

Retry after

```
1 Minute

↓

5 Minutes

↓

15 Minutes

↓

30 Minutes
```

Reduces

pressure

on

the provider.

______________________________________________________________________

# Dead Letter Queue (DLQ)

Suppose

notification

fails

after

multiple retries.

Move

it

to

```
Dead Letter Queue
```

Later

investigate

or replay.

______________________________________________________________________

# Idempotency

Suppose

worker crashes

after

sending

the email.

Retry

must not

send

duplicate emails.

Use

```
Notification ID
```

to detect

duplicates.

______________________________________________________________________

# Delivery Status

Track

notification lifecycle.

```
Queued

↓

Processing

↓

Sent

↓

Delivered

↓

Failed
```

______________________________________________________________________

# Webhooks

Some customers

want

real-time updates.

Example

```
Payment Completed

↓

Webhook

↓

Customer Server
```

Treat

webhook delivery

like any other

notification channel

with retries

and idempotency.

______________________________________________________________________

# Database Design

Notifications

| id | user | channel | status |

Templates

| id | name | content |

Preferences

| user | email | sms | push |

______________________________________________________________________

# Queue Design

Separate queues

can improve

throughput.

Example

```
Email Queue
```

```
SMS Queue
```

```
Push Queue
```

Critical notifications

may also

use

high-priority queues.

______________________________________________________________________

# Scaling Workers

Suppose

Email traffic

increases.

Scale

only

Email Workers.

```
2 Workers

↓

20 Workers
```

Other workers

remain unchanged.

______________________________________________________________________

# Monitoring

Monitor

- Queue length
- Delivery rate
- Failure rate
- Retry count
- Provider latency
- Processing time

______________________________________________________________________

# Failure Scenarios

## Email Provider Down

Retry

using

backoff.

If supported,

switch

to

a secondary provider.

______________________________________________________________________

## Queue Failure

Persist

messages

until

the queue

recovers.

Highly available

message brokers

reduce

this risk.

______________________________________________________________________

## Worker Failure

Another worker

consumes

the pending

message.

______________________________________________________________________

## Duplicate Processing

Use

idempotency

to prevent

duplicate notifications.

______________________________________________________________________

# Multiple Providers

Interview bonus.

Example

```
Primary Provider

↓

Failure

↓

Secondary Provider
```

Improves

availability.

______________________________________________________________________

# Rate Limiting

Providers

often enforce

sending limits.

Example

```
100 Emails/sec
```

Workers

must

respect

provider limits.

______________________________________________________________________

# Typical Architecture

```
                  Applications
                        │
                        ▼
                Notification API
                        │
                        ▼
                 RabbitMQ / Kafka
                        │
      ┌─────────────────┼──────────────────┐
      ▼                 ▼                  ▼
 Email Worker      SMS Worker       Push Worker
      │                 │                  │
      ▼                 ▼                  ▼
 Email Provider   SMS Provider     FCM / APNs
      │
      ▼
Analytics & Status Service
```

______________________________________________________________________

# Common Interview Questions

## Why use a queue?

Queues decouple applications from notification delivery, improve response times, absorb traffic spikes, and enable
retries when downstream providers fail.

______________________________________________________________________

## Why separate Email, SMS, and Push workers?

Each channel has different providers, throughput, rate limits, retry strategies, and failure modes. Independent workers
allow separate scaling and management.

______________________________________________________________________

## Why use exponential backoff?

Repeated immediate retries can overload providers during outages. Exponential backoff spaces retries over increasing
intervals, improving system stability.

______________________________________________________________________

## What is a Dead Letter Queue?

A Dead Letter Queue stores messages that repeatedly fail processing, allowing operators to inspect, fix, or replay them
later.

______________________________________________________________________

## Why is idempotency important?

Workers may retry after crashes or timeouts. Idempotency ensures the same notification is not delivered multiple times.

______________________________________________________________________

# Common Mistakes

## Sending Notifications Synchronously

Never

block

user requests

while

sending emails

or SMS.

______________________________________________________________________

## Hardcoding Message Content

Use

templates

instead.

______________________________________________________________________

## Ignoring User Preferences

Respect

notification settings

before

sending.

______________________________________________________________________

## Infinite Retries

Always

set

retry limits

and

use

Dead Letter Queues.

______________________________________________________________________

## Single Provider Dependency

Support

provider failover

for

critical notifications.

______________________________________________________________________

# Best Practices

✅ Process notifications asynchronously.

✅ Use separate workers for each channel.

✅ Implement retries with exponential backoff.

✅ Use Dead Letter Queues.

✅ Track delivery status.

✅ Respect user preferences.

✅ Make notification processing idempotent.

______________________________________________________________________

# Interview Deep Dive

## Question

Why shouldn't applications send emails directly?

### Answer

Sending emails directly increases API latency and tightly couples business logic with external providers. A queue allows
asynchronous processing, retries, and better scalability.

______________________________________________________________________

## Question

How do you prevent duplicate notifications?

### Answer

Assign a unique notification ID and ensure workers process each notification idempotently. If the same notification is
retried, it is recognized and ignored if already completed.

______________________________________________________________________

## Question

How would you handle a provider outage?

### Answer

Retry failed notifications using exponential backoff. For critical notifications, fail over to a secondary provider if
available. Persist failed notifications in a Dead Letter Queue after retry limits are exceeded.

______________________________________________________________________

# Practice Exercise

Design

a Notification System

for

500 Million Users.

Explain

1. API design
1. Queue architecture
1. Worker design
1. Retry mechanism
1. Dead Letter Queue
1. User preferences
1. Scheduling
1. Multi-provider support
1. Monitoring
1. Failure recovery
1. Scaling strategy
1. Trade-offs

Present

your complete design

within

45 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

A Notification System is a foundational distributed system used across nearly every modern application.

A strong design should demonstrate

- Asynchronous processing
- Queue-based architecture
- Channel-specific workers
- Retry strategies
- Dead Letter Queues
- Idempotency
- User preferences
- Multi-provider failover
- Monitoring
- High availability

Mastering this topic prepares you for interviews involving messaging platforms, e-commerce systems, fintech
applications, and cloud-native architectures.

______________________________________________________________________

# Next

[System Design – Search Autocomplete](30-design-search-autocomplete.md)
