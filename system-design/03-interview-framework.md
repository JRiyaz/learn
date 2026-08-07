# System Design Interview Framework

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn a repeatable framework that can be used to solve **almost every System Design interview question**, regardless of the application being designed.

______________________________________________________________________

# Introduction

One of the biggest reasons candidates fail System Design interviews is

they immediately start drawing architecture.

Experienced interviewers notice this immediately.

The best candidates

don't start with solutions.

They start with

questions.

______________________________________________________________________

# The Universal Framework

Every System Design interview should follow

this exact flow.

```
Requirements

↓

Scale Estimation

↓

High-Level Design

↓

API Design

↓

Data Model

↓

Database Selection

↓

Detailed Component Design

↓

Scaling

↓

Reliability

↓

Security

↓

Monitoring

↓

Trade-offs
```

Memorize it.

We'll use this framework

for every design question.

______________________________________________________________________

# Step 1

# Clarify Requirements

Never assume.

Always ask questions.

______________________________________________________________________

## Functional Requirements

Ask

- What should the system do?
- What are the core features?
- Who are the users?
- Is authentication required?
- Is real-time communication needed?

Example

Design WhatsApp

Questions

- One-to-one chat?
- Group chat?
- Media sharing?
- Read receipts?
- Online status?
- Voice calls?

______________________________________________________________________

## Non-Functional Requirements

Ask

- Expected latency?
- Availability target?
- Scalability?
- Security?
- Consistency requirements?
- Disaster recovery?

Example

```
Latency

<200ms

↓

Availability

99.99%

↓

Millions of users
```

______________________________________________________________________

# Never Skip Requirements

Interviewers expect

discussion.

Not assumptions.

______________________________________________________________________

# Step 2

# Estimate Scale

Now estimate

traffic.

You don't need

perfect numbers.

Reasonable assumptions

are enough.

Example

```
100 Million Users

↓

10 Million Daily Active Users

↓

1 Million Concurrent Users

↓

100K Requests/sec
```

______________________________________________________________________

## Why Estimate?

Scale affects

everything.

Example

```
100 Users

↓

One Database
```

vs

```
100 Million Users

↓

Sharding

↓

Caching

↓

Replication

↓

CDN
```

______________________________________________________________________

# Step 3

# High-Level Design

Now draw

major components.

Example

```
Users

↓

DNS

↓

Load Balancer

↓

API Servers

↓

Redis

↓

Database

↓

Object Storage

↓

Message Queue
```

Keep it

simple.

Don't explain

every component yet.

______________________________________________________________________

# Step 4

# Define APIs

Most candidates

forget APIs.

Don't.

Example

For URL Shortener

```
POST /shorten

↓

Create URL
```

```
GET /abc123

↓

Redirect
```

Example

For Chat

```
POST /messages

↓

Send Message
```

```
GET /messages

↓

Receive Messages
```

API discussion

shows

structured thinking.

______________________________________________________________________

# Step 5

# Data Model

Now define

entities.

Example

Instagram

```
User

↓

Post

↓

Comment

↓

Like

↓

Follower
```

Example

WhatsApp

```
User

↓

Conversation

↓

Message

↓

Attachment
```

Keep

relationships

simple.

______________________________________________________________________

# Step 6

# Database Selection

Don't say

```
Use MongoDB.
```

Explain

why.

Example

```
SQL

↓

Transactions

↓

Consistency
```

vs

```
NoSQL

↓

Scalability

↓

Flexible Schema
```

Always discuss

trade-offs.

______________________________________________________________________

# Step 7

# Deep Dive Components

Now explain

each component.

Example

API Server

- Authentication
- Validation
- Business Logic

Database

- Indexes
- Replication
- Sharding

Cache

- Frequently accessed data
- TTL
- Cache invalidation

Message Queue

- Async processing
- Retry
- Dead Letter Queue

______________________________________________________________________

# Step 8

# Scaling

Now discuss

growth.

Topics

```
Horizontal Scaling

↓

Replication

↓

Sharding

↓

Caching

↓

CDN

↓

Auto Scaling
```

Interviewers expect

this discussion.

______________________________________________________________________

# Step 9

# Reliability

Ask yourself

```
What happens

if

something fails?
```

Discuss

- Replication
- Health checks
- Retry
- Circuit Breaker
- Failover
- Backup

______________________________________________________________________

# Step 10

# Security

Many candidates

forget security.

Mention

- Authentication
- Authorization
- HTTPS
- Encryption
- Rate Limiting
- Secrets Management
- Input Validation

You don't need

deep security knowledge,

but don't ignore it.

______________________________________________________________________

# Step 11

# Monitoring

Good systems

must be

observable.

Discuss

```
Logging

↓

Metrics

↓

Tracing

↓

Alerts

↓

Dashboards
```

Example

Monitor

- API latency
- Error rate
- CPU
- Memory
- Queue length
- Database latency

______________________________________________________________________

# Step 12

# Trade-offs

This is where

Senior Engineers

stand out.

Every decision

has advantages

and disadvantages.

Example

Redis

Advantages

- Fast
- Low latency

Disadvantages

- Memory cost
- Cache invalidation complexity

______________________________________________________________________

# Complete Flow

Here's the full interview process.

```
Understand Requirements

↓

Estimate Scale

↓

Draw High-Level Design

↓

Define APIs

↓

Design Database

↓

Discuss Components

↓

Scale

↓

Reliability

↓

Security

↓

Monitoring

↓

Trade-offs

↓

Summary
```

______________________________________________________________________

# Time Allocation

For a

45-minute interview

consider

| Time | Activity |
|------|----------|
| 5 min | Clarify requirements |
| 5 min | Scale estimation |
| 10 min | High-level design |
| 10 min | Deep dive |
| 10 min | Scaling & reliability |
| 5 min | Trade-offs & summary |

Don't spend

20 minutes

drawing boxes.

______________________________________________________________________

# Interview Communication

Always explain

what you're thinking.

Bad

*Silent drawing.*

Good

> Since this application is expected to support millions of users, I'd like to introduce a cache in front of the database to reduce read load.

Interviewers

evaluate

your reasoning.

______________________________________________________________________

# Common Follow-Up Questions

Expect

- Why SQL?
- Why Redis?
- Why Kafka?
- Why microservices?
- What happens if Redis fails?
- How do you scale?
- What is the bottleneck?
- What would you improve next?

Be prepared.

______________________________________________________________________

# Whiteboard Tips

Use simple diagrams.

Example

```
Users

↓

Load Balancer

↓

Application Servers

↓

Redis

↓

Database
```

Don't draw

every internal class.

Focus

on architecture.

______________________________________________________________________

# Common Mistakes

## Starting With Database

Always start

with

requirements.

______________________________________________________________________

## Ignoring Scale

Architecture depends

on traffic.

______________________________________________________________________

## Choosing Technologies Without Reason

Don't say

```
Kafka

because everyone uses it.
```

Explain

why.

______________________________________________________________________

## Ignoring Failures

Every component

can fail.

Discuss

recovery.

______________________________________________________________________

## Forgetting Trade-offs

Interviewers

want reasoning,

not memorization.

______________________________________________________________________

# Best Practices

✅ Ask clarifying questions.

✅ Estimate scale.

✅ Start simple.

✅ Scale gradually.

✅ Explain trade-offs.

✅ Discuss failures.

✅ Mention monitoring.

✅ Finish with improvements.

______________________________________________________________________

# Universal Interview Template

Whenever you're asked

```
Design X
```

follow this checklist.

```
□ Requirements

□ Scale

□ High-Level Design

□ APIs

□ Database

□ Components

□ Cache

□ Load Balancer

□ Messaging

□ Scaling

□ Reliability

□ Security

□ Monitoring

□ Trade-offs

□ Summary
```

This template works for

almost every

System Design interview.

______________________________________________________________________

# Interview Deep Dive

## Question

Why do interviewers ask clarifying questions first?

### Answer

They want to see whether you understand the problem before designing a solution. Strong candidates avoid assumptions and
gather enough information to make appropriate architectural decisions.

______________________________________________________________________

## Question

Should I design the perfect system immediately?

### Answer

No. Start with a simple working design, then evolve it by introducing caching, replication, load balancing, messaging,
and other components as scale increases.

______________________________________________________________________

## Question

How important are trade-offs?

### Answer

Trade-offs are one of the most important parts of a System Design interview. Interviewers expect you to explain not only
what you're choosing, but why you're choosing it and what disadvantages come with that decision.

______________________________________________________________________

# Practice Exercise

Using the framework above,

outline a design for each of the following.

1. URL Shortener
1. WhatsApp
1. Instagram
1. Netflix
1. Uber
1. Online Food Delivery
1. Payment Gateway
1. Notification Service

For each,

write down

- Requirements
- Estimated scale
- High-level architecture
- APIs
- Database choice
- Caching strategy
- Scaling approach
- Reliability measures
- Security considerations
- Trade-offs

______________________________________________________________________

# Summary

A successful System Design interview is **structured**, not rushed.

Strong candidates

- Clarify requirements
- Estimate scale
- Build incrementally
- Explain trade-offs
- Discuss reliability
- Think about operations

By following the same framework every time, you'll be able to confidently approach almost any System Design problem.

______________________________________________________________________

# Next

[Capacity Estimation](04-capacity-estimation.md)
