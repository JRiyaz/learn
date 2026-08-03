# System Design - Part 82

# Notification Service System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Multi-Channel Notifications
- Email
- SMS
- Push Notifications
- Scheduling
- Retry Mechanism
- Dead Letter Queue (DLQ)
- User Preferences
- Rate Limiting
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a Notification Service.**

Almost

every application

needs notifications.

Examples:

- Amazon → Order updates
- Uber → Driver arrived
- WhatsApp → New message
- Instagram → New follower
- Google Drive → Shared file

Instead of

every service

sending notifications

directly,

build

one centralized

Notification Service.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Send Email
- Send SMS
- Send Push Notifications
- Schedule notifications
- Retry failed deliveries
- User notification preferences
- Delivery status

Optional

- WhatsApp notifications
- Slack notifications
- Webhooks
- Voice calls

______________________________________________________________________

# Non-Functional Requirements

- High availability
- High throughput
- Reliable delivery
- Scalable
- Low latency

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the platform

serves

100 applications.

Daily Notifications

```text id="ns8201"
2 Billion
```

Peak Traffic

```text id="ns8202"
100,000 Notifications/sec
```

Observation.

The workload

is

write-heavy

and

asynchronous.

______________________________________________________________________

# Step 3

# API Design

Send Notification

```http id="ns8203"
POST /notifications
```

Request

```json id="ns8204"
{
  "user_id": 101,
  "channel": "email",
  "template": "order_confirmation"
}
```

______________________________________________________________________

Notification Status

```http id="ns8205"
GET /notifications/{id}
```

______________________________________________________________________

Schedule Notification

```http id="ns8206"
POST /notifications/schedule
```

______________________________________________________________________

Update Preferences

```http id="ns8207"
PUT /users/preferences
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="ns8208"
Application

↓

API Gateway

↓

Notification Service

↓

Kafka

↓

Workers

↓

Providers
```

Providers

include:

- Email Provider
- SMS Provider
- Push Provider

Supporting services:

- Template Service
- Preference Service
- Scheduler
- Retry Service

______________________________________________________________________

# Why Asynchronous?

Interview favorite.

Suppose

Amazon

creates

an order.

Should

the customer

wait

until

the email

is delivered?

No.

Instead,

publish

an event.

```text id="ns8209"
Order Created

↓

Kafka

↓

Notification Worker
```

The API

returns

immediately.

______________________________________________________________________

# Multi-Channel Delivery

One notification

may be sent

through

different channels.

```text id="ns8210"
Notification

↓

Email

↓

SMS

↓

Push
```

Each channel

uses

its own

provider.

______________________________________________________________________

# Email Delivery

Workflow

```text id="ns8211"
Worker

↓

SMTP / Email API

↓

Customer
```

Common providers:

- Amazon SES
- SendGrid
- Mailgun

______________________________________________________________________

# SMS Delivery

Workflow

```text id="ns8212"
Worker

↓

SMS Provider

↓

Phone
```

Examples:

- Twilio
- Vonage
- Local telecom gateways

______________________________________________________________________

# Push Notifications

Workflow

```text id="ns8213"
Worker

↓

FCM / APNs

↓

Mobile Device
```

Android

typically uses

Firebase Cloud Messaging (FCM).

iOS

uses

Apple Push Notification Service (APNs).

______________________________________________________________________

# Templates

Interview favorite.

Applications

shouldn't send

raw messages.

Instead

send

template IDs.

Example

```text id="ns8214"
Order Confirmation
```

Variables

```text id="ns8215"
Name

Order ID

Amount
```

The Template Service

renders

the final message.

______________________________________________________________________

# User Preferences

Users

may disable

certain notifications.

Example

```text id="ns8216"
Email

OFF
```

```text id="ns8217"
Push

ON
```

Before sending,

the service

checks

user preferences.

______________________________________________________________________

# Scheduling

Interview favorite.

Suppose

a reminder

should be sent

tomorrow

at

9 AM.

Workflow

```text id="ns8218"
Notification

↓

Scheduler

↓

Kafka

↓

Worker
```

The Scheduler

publishes

the event

at

the correct time.

______________________________________________________________________

# Retry Mechanism

Providers

sometimes fail.

Workflow

```text id="ns8219"
Send

↓

Failure

↓

Retry
```

Retries

use

Exponential Backoff.

Example

```text id="ns8220"
1 min

↓

5 min

↓

15 min

↓

1 hour
```

______________________________________________________________________

# Dead Letter Queue (DLQ)

Interview favorite.

Suppose

all retries

fail.

Don't

lose

the notification.

Instead,

move it

to

a

Dead Letter Queue.

```text id="ns8221"
Retry Failed

↓

DLQ
```

Operations teams

can investigate

later.

______________________________________________________________________

# Idempotency

Suppose

the worker

crashes

after

sending

the email

but

before

updating

the database.

On retry,

avoid

sending

duplicate emails.

Use

an

Idempotency Key

or

Notification ID.

______________________________________________________________________

# Rate Limiting

Interview favorite.

Suppose

a bug

causes

1 Million emails

to one user.

Apply

rate limits.

Examples:

- 5 SMS/hour
- 20 Emails/day
- 100 Push/day

Limits

may differ

per channel.

______________________________________________________________________

# Database Schema

Notifications

```text id="ns8222"
notification_id

user_id

channel

status

template

created_at
```

Preferences

```text id="ns8223"
user_id

email_enabled

sms_enabled

push_enabled
```

______________________________________________________________________

# Delivery Status

A notification

moves

through

multiple states.

```text id="ns8224"
Created

↓

Queued

↓

Sent

↓

Delivered
```

Possible failures

include:

```text id="ns8225"
Failed

Expired

Cancelled
```

______________________________________________________________________

# Caching

Redis stores:

- User preferences
- Templates
- Provider configuration
- Rate limit counters

Delivery history

remains

inside

the database.

______________________________________________________________________

# Scaling

Scale independently:

- Notification API
- Email Workers
- SMS Workers
- Push Workers
- Scheduler

Kafka partitions

allow

millions

of notifications

to be processed

in parallel.

______________________________________________________________________

# Failure Scenario

Suppose

the Email Provider

is unavailable.

Workflow

```text id="ns8226"
Retry

↓

Retry

↓

DLQ
```

The notification

is not lost.

______________________________________________________________________

# Another Failure

Suppose

Kafka

becomes unavailable.

Applications

may temporarily

store requests

or

retry publishing

until

Kafka

recovers.

______________________________________________________________________

# End-to-End Architecture

```text id="ns8227"
Application

↓

API Gateway

↓

Notification Service

↓

Redis

↓

Kafka

↓

Email Workers

↓

SMS Workers

↓

Push Workers

↓

Scheduler

↓

Retry Service

↓

DLQ

↓

Email/SMS/Push Providers

↓

PostgreSQL
```

______________________________________________________________________

# Trade-offs

Synchronous

vs

Asynchronous

| Sync | Async |
| ---------- | --------------------- |
| Slower API | Faster API |
| User waits | Background processing |

______________________________________________________________________

Single Queue

vs

Multiple Queues

| Single Queue | Multiple Queues |
| ----------------------- | ------------------- |
| Simpler | Better isolation |
| One backlog affects all | Independent scaling |

______________________________________________________________________

Email

vs

Push

| Email | Push |
| -------------- | -------------- |
| Reliable | Instant |
| Longer content | Short messages |
| Higher latency | Low latency |

______________________________________________________________________

# Best Practices

✅ Use templates.

✅ Respect user preferences.

✅ Retry with exponential backoff.

✅ Store failed messages in a DLQ.

✅ Use idempotency to prevent duplicate notifications.

______________________________________________________________________

# Common Mistakes

### Sending Notifications Synchronously

Applications

should never

wait

for

email or SMS delivery.

Use

queues

and

background workers.

______________________________________________________________________

### Ignoring User Preferences

Users

expect

control

over

which notifications

they receive.

Always

check preferences

before sending.

______________________________________________________________________

### Infinite Retries

Retries

without limits

can overload

providers.

Always

define:

- Maximum retry count
- Exponential backoff
- DLQ policy

______________________________________________________________________

### No Delivery Tracking

Without

status tracking,

support teams

cannot determine

whether

a notification

was actually delivered.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a Notification Service?

Start by building a centralized Notification Service that accepts notification requests from multiple applications.
Publish requests to Kafka so delivery is asynchronous and does not block the calling application. Create separate worker
pools for Email, SMS, and Push notifications, each integrating with external providers. Use a Template Service to render
messages, a Preference Service to honor user notification settings, Redis for caching preferences and rate-limit
counters, and PostgreSQL for storing delivery history. Implement retries with exponential backoff, move permanently
failed messages to a Dead Letter Queue, and use idempotency keys to prevent duplicate deliveries during worker retries.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Multi-channel notifications
- Email, SMS & Push
- Templates
- User preferences
- Scheduling
- Retry mechanisms
- Dead Letter Queue (DLQ)
- Rate limiting
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
- ✅ Notification Service

You now understand the architecture of one of the most reusable infrastructure services in modern distributed systems.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll begin the **AI Systems** category with one of the most requested modern interview topics:

- LLM serving
- Prompt processing
- Token streaming
- Context management
- Conversation history
- GPU workers
- Model routing
- Safety filters

We'll design **ChatGPT / LLM System Architecture**.

______________________________________________________________________

# What's Next

[ChatGPT / LLM System Design](83-chatgpt-llm-system-design.md)
