# System Design Common Mistakes

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn the most common mistakes candidates make during System Design interviews and how to avoid them.

______________________________________________________________________

# Introduction

Many candidates

know

Redis,

Kafka,

Load Balancers,

CDNs,

Microservices,

and Databases.

Yet,

they still

fail

System Design interviews.

Why?

Because

System Design

is not

a technology quiz.

It is

a problem-solving interview.

This chapter

covers

the most common

mistakes

and

how to avoid them.

______________________________________________________________________

# Mistake 1

# Jumping Directly To Architecture

Candidate

starts with

```
We'll use

Microservices,

Redis,

Kafka,

Kubernetes...
```

Problem

No requirements

were discussed.

______________________________________________________________________

# Correct Approach

Always begin with

```
Requirements

↓

Capacity

↓

Architecture
```

Interviewers

expect

a structured process.

______________________________________________________________________

# Mistake 2

# Never Asking Questions

Some candidates

assume

requirements.

Example

User says

```
Design Instagram
```

Candidate assumes

- Stories
- Reels
- Live Video
- Messaging

without asking.

______________________________________________________________________

# Correct Approach

Clarify.

Ask

```
Should we

support videos?
```

```
Do we need

notifications?
```

```
Should search

be included?
```

Never assume

major features.

______________________________________________________________________

# Mistake 3

# Ignoring Scale

Candidates

draw

a perfect architecture

without asking

```
How many users?
```

Scale determines

everything.

______________________________________________________________________

# Example

```
100 Users
```

Needs

different architecture

than

```
100 Million Users
```

______________________________________________________________________

# Correct Approach

Estimate

- Users
- DAU
- RPS
- Storage
- Growth

Then

design accordingly.

______________________________________________________________________

# Mistake 4

# Overengineering

Interview favorite.

Candidate uses

- Kafka
- Redis
- CDN
- Elasticsearch
- Kubernetes
- Graph Database

for

a tiny application.

______________________________________________________________________

# Correct Approach

Only introduce

components

when

they solve

a real problem.

______________________________________________________________________

# Mistake 5

# No Trade-Off Discussion

Candidate says

```
Use Redis.
```

Stops there.

______________________________________________________________________

# Correct Approach

Explain

```
Why Redis?

↓

Lower latency

↓

Trade-off

Possible stale cache
```

Every decision

should include

benefits

and

limitations.

______________________________________________________________________

# Mistake 6

# Forgetting Failure Scenarios

Many candidates

never ask

```
What if

Redis fails?
```

```
What if

Database fails?
```

```
What if

Queue fails?
```

______________________________________________________________________

# Correct Approach

Discuss

- Failover
- Retry
- Replication
- Backups
- Circuit Breakers

______________________________________________________________________

# Mistake 7

# Ignoring Monitoring

Candidates

finish

the design

without

mentioning

operations.

______________________________________________________________________

# Correct Approach

Monitor

- API latency
- Error rate
- Queue length
- Cache hit ratio
- CPU
- Memory
- Database latency

Mention

alerts

and dashboards.

______________________________________________________________________

# Mistake 8

# Choosing SQL Or NoSQL Without Reason

Wrong answer

```
Use MongoDB.
```

Why?

```
Because

it's scalable.
```

______________________________________________________________________

# Correct Approach

Explain

why.

Example

SQL

↓

Transactions

Relationships

Strong consistency

______________________________________________________________________

NoSQL

↓

Flexible schema

Massive scale

High write throughput

______________________________________________________________________

# Mistake 9

# Using Cache Incorrectly

Candidate

stores

everything

inside

Redis.

______________________________________________________________________

# Problems

- Memory waste
- Expensive
- Stale data

______________________________________________________________________

# Correct Approach

Cache

only

data

that benefits

from caching.

Examples

- Product details
- Sessions
- Trending posts
- User profiles

______________________________________________________________________

# Mistake 10

# Forgetting Cache Consistency

Database

changes.

Cache

still

contains

old data.

______________________________________________________________________

# Correct Approach

Choose

a strategy.

Examples

- Cache Aside
- Write Through
- Cache Invalidation

Explain

why.

______________________________________________________________________

# Mistake 11

# Ignoring Concurrency

Interview favorite.

Example

BookMyShow

Two users

book

Seat A10

simultaneously.

Without

proper handling

↓

Double Booking.

______________________________________________________________________

# Correct Approach

Use

- Atomic operations
- Optimistic locking
- Pessimistic locking
- Distributed locks

______________________________________________________________________

# Mistake 12

# Synchronous Everything

Candidate

sends

Emails,

SMS,

Analytics,

Image Processing,

Notifications

inside

the request path.

______________________________________________________________________

# Problems

Higher latency

Poor scalability

______________________________________________________________________

# Correct Approach

Use

queues.

```
Request

↓

Queue

↓

Worker

↓

Background Processing
```

______________________________________________________________________

# Mistake 13

# Ignoring Idempotency

Suppose

payment

times out.

Client retries.

Without

idempotency

payment

may be charged

twice.

______________________________________________________________________

# Correct Approach

Use

unique

request IDs

or

idempotency keys.

______________________________________________________________________

# Mistake 14

# No Capacity Estimation

Candidate

starts

designing

without

estimating

traffic.

______________________________________________________________________

# Correct Approach

Estimate

- Requests/sec
- Storage
- Bandwidth
- Peak traffic

Architecture

depends

on

these numbers.

______________________________________________________________________

# Mistake 15

# Ignoring Bottlenecks

Candidates

design

the system

but never ask

```
What breaks first?
```

______________________________________________________________________

# Correct Approach

Identify

likely bottlenecks.

Examples

- Database
- Cache
- Queue
- Network
- Storage

Then

explain

how

you scale them.

______________________________________________________________________

# Mistake 16

# Scaling Everything

Wrong approach

```
Traffic increased

↓

Scale

every service
```

______________________________________________________________________

# Correct Approach

Scale

only

the bottleneck.

Examples

More searches

↓

Scale

Search Service

More uploads

↓

Scale

Upload Service

______________________________________________________________________

# Mistake 17

# Using Microservices Everywhere

Small project

↓

50 microservices.

______________________________________________________________________

# Problems

- Operational complexity
- More network calls
- Harder debugging

______________________________________________________________________

# Correct Approach

Start

with

a modular monolith

or

a small number

of services,

then split

as the system

grows,

if appropriate.

______________________________________________________________________

# Mistake 18

# Ignoring Security

Many candidates

forget

security.

______________________________________________________________________

# Mention

- Authentication
- Authorization
- HTTPS
- Encryption
- Secrets Management
- Input Validation
- Rate Limiting

______________________________________________________________________

# Mistake 19

# Confusing Replication And Sharding

Replication

↓

Copies

same data.

Purpose

↓

Availability

Read scaling.

______________________________________________________________________

Sharding

↓

Splits

data.

Purpose

↓

Write scaling

Storage scaling.

______________________________________________________________________

# Mistake 20

# No Summary

Candidates

finish

without

recapping

their design.

______________________________________________________________________

# Correct Approach

Summarize

- Requirements
- Architecture
- Scaling
- Trade-offs
- Failure handling

This reinforces

your reasoning.

______________________________________________________________________

# Red Flags Interviewers Notice

🚩 Using technologies without justification.

🚩 No clarification questions.

🚩 Ignoring scale.

🚩 Ignoring failures.

🚩 Ignoring trade-offs.

🚩 Overengineering.

🚩 No monitoring.

🚩 Poor communication.

______________________________________________________________________

# Strong Candidate Behavior

A strong candidate

typically

does the following.

✔ Clarifies requirements.

✔ Estimates traffic.

✔ Starts with a simple design.

✔ Adds complexity only when needed.

✔ Explains every technology choice.

✔ Discusses trade-offs.

✔ Plans for failures.

✔ Monitors the system.

✔ Communicates clearly.

______________________________________________________________________

# Interview Checklist

Before ending

ask yourself

```
Did I cover

Requirements?

Capacity?

Architecture?

Database?

Cache?

Queue?

Scaling?

Monitoring?

Security?

Failures?

Trade-offs?
```

If

the answer

is

Yes,

your design

is usually

well-rounded.

______________________________________________________________________

# Quick Recovery Tips

Suppose

you realize

you forgot

something.

Simply say

```
I'd also like

to discuss

failure handling

for this design.
```

or

```
Let me explain

how I'd

scale this

if traffic

grew 100×.
```

Interviewers

generally appreciate

structured additions.

______________________________________________________________________

# Common Follow-Up Questions

Be ready for

```
Why Redis?
```

```
Why Kafka?
```

```
Why SQL?
```

```
Why not NoSQL?
```

```
How do you

prevent duplicates?
```

```
How do you

handle failures?
```

```
How do you

monitor this?
```

```
How would you

scale to

10× traffic?
```

Practice

answering

these confidently.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the biggest mistake candidates make?

### Answer

Jumping directly into technologies without first understanding requirements, estimating scale, and explaining why each
architectural decision is needed.

______________________________________________________________________

## Question

Is overengineering a problem in interviews?

### Answer

Yes. Adding technologies that do not solve a demonstrated problem often signals poor judgment. Simpler architectures
that evolve based on requirements are generally preferred.

______________________________________________________________________

## Question

How do I recover if I forget an important topic?

### Answer

State it explicitly and incorporate it into the discussion. For example, add failure handling, monitoring, or scaling
considerations before concluding your design.

______________________________________________________________________

# Practice Exercise

Review

your previous

System Design solutions

for

Amazon,

Uber,

Instagram,

WhatsApp,

Netflix,

and

BookMyShow.

For each,

identify

- One unnecessary component
- One missing trade-off
- One possible bottleneck
- One failure scenario
- One monitoring metric
- One security improvement

This exercise

helps build

the review skills

expected

from senior engineers.

______________________________________________________________________

# Summary

Most System Design interview failures are caused by process mistakes rather than technology gaps.

A successful interview usually follows this pattern:

- Clarify requirements
- Estimate scale
- Build a simple architecture
- Add components only when justified
- Explain trade-offs
- Handle failures
- Discuss monitoring
- Communicate clearly

Following this disciplined approach will consistently produce stronger interview performance than memorizing
architectures alone.

______________________________________________________________________

# Next

[System Design Interview Questions](36-system-design-interview-questions.md)
