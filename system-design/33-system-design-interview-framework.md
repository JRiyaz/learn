# System Design Interview Framework

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn a repeatable framework to solve **any** System Design interview confidently, even if you've never designed that exact system before.

______________________________________________________________________

# Why Do You Need A Framework?

Many candidates

know

Redis,

Kafka,

Load Balancer,

Microservices,

and Databases.

Yet,

they fail

System Design interviews.

Why?

Because

they jump

directly

into architecture.

Interviewers

are not testing

whether

you know

technologies.

They are testing

how

you think.

______________________________________________________________________

# The Biggest Mistake

Candidate

starts with

```
We'll use

Microservices,

Kafka,

Redis,

Kubernetes,

ElasticSearch...
```

within

the first

two minutes.

No requirements.

No estimates.

No trade-offs.

This

is

a major red flag.

______________________________________________________________________

# The Framework

Every System Design interview

can be solved

using

the following framework.

```
1. Clarify Requirements

↓

2. Estimate Scale

↓

3. APIs

↓

4. Data Model

↓

5. High-Level Architecture

↓

6. Deep Dive

↓

7. Bottlenecks

↓

8. Scaling

↓

9. Monitoring

↓

10. Trade-offs
```

Memorize

this flow.

It works

for

almost every interview.

______________________________________________________________________

# Step 1

# Clarify Requirements

Interviewers

expect

questions.

Never assume.

Ask

about

functional requirements.

Examples

```
Do users

need authentication?
```

```
Should data

be searchable?
```

```
Should users

receive notifications?
```

```
Should uploads

be supported?
```

______________________________________________________________________

# Functional Requirements

Examples

- Create
- Read
- Update
- Delete
- Search
- Upload
- Download
- Notifications
- Analytics

______________________________________________________________________

# Non-Functional Requirements

Examples

- Scalability
- Availability
- Latency
- Consistency
- Durability
- Fault Tolerance
- Security

______________________________________________________________________

# Step 2

# Capacity Estimation

Interview favorite.

Estimate

instead of

guessing.

Example

```
100 Million Users
```

Suppose

```
10%

Daily Active
```

Estimate

- Daily Requests
- Requests/sec
- Storage
- Bandwidth
- Growth

Interviewers

care more

about

your reasoning

than

the exact numbers.

______________________________________________________________________

# Example

Suppose

```
20 Million

Requests/day
```

Average

```
≈231 Requests/sec
```

Peak

```
700 Requests/sec
```

Now

you know

whether

one server

is enough.

______________________________________________________________________

# Step 3

# API Design

Design

simple

REST APIs.

Example

```
POST /orders
```

```
GET /orders/{id}
```

```
DELETE /orders/{id}
```

Don't spend

too much time

here.

______________________________________________________________________

# Step 4

# Data Model

Interviewers

expect

basic schema.

Example

Orders

| id | user | status |

Users

| id | name |

Products

| id | price |

Focus

on

important entities.

Don't design

every column.

______________________________________________________________________

# Step 5

# High-Level Architecture

Now

draw

the system.

Example

```
Users

↓

Load Balancer

↓

API Servers

↓

Cache

↓

Database
```

Keep

the first diagram

simple.

______________________________________________________________________

# Architecture First

Do not

draw

every component

immediately.

Start

simple.

Then

add

complexity.

______________________________________________________________________

# Step 6

# Deep Dive

Interviewer

usually asks

```
How would you

handle...
```

This is where

you discuss

- Cache
- Queue
- Search
- Replication
- Sharding
- CDN
- Object Storage
- WebSockets
- Rate Limiting

Only introduce

components

when needed.

______________________________________________________________________

# Example

Instagram

requires

```
Object Storage

↓

CDN
```

BookMyShow

requires

```
Distributed Lock
```

Uber

requires

```
Geospatial Search
```

Different systems

require

different solutions.

______________________________________________________________________

# Step 7

# Identify Bottlenecks

Always ask

yourself

```
What breaks first?
```

Possible bottlenecks

- Database
- Cache
- API Server
- Queue
- Network
- Storage

Then

explain

how

you solve them.

______________________________________________________________________

# Example

Database

becomes slow.

Solution

```
Replication

↓

Read Replicas
```

Later

```
Sharding
```

______________________________________________________________________

# Step 8

# Scaling

Interviewers

love this question.

Explain

horizontal scaling.

```
More Users

↓

More Servers
```

Avoid

vertical scaling

as

the primary answer.

______________________________________________________________________

# Scale Components Independently

Example

```
More Searches

↓

Scale Search Service
```

```
More Uploads

↓

Scale Upload Service
```

Don't scale

everything

together.

______________________________________________________________________

# Step 9

# Monitoring

Many candidates

forget

this section.

Monitor

- API latency
- Error rate
- CPU
- Memory
- Queue length
- Cache hit ratio
- Database latency

Mention

alerts

and dashboards.

______________________________________________________________________

# Step 10

# Trade-offs

Interview favorite.

Every design

has

trade-offs.

Example

Cache

↓

Faster Reads

↓

Possible Stale Data

Example

Replication

↓

Higher Availability

↓

Replication Lag

Interviewers

want

to hear

these discussions.

______________________________________________________________________

# CAP Thinking

Don't force

CAP theorem

into

every answer.

Mention it

only

when relevant.

Example

Banking

↓

Consistency

Instagram Feed

↓

Availability

______________________________________________________________________

# Ask For Feedback

Halfway

through

the interview,

it is okay

to ask

```
Would you like me

to go deeper

into

the database,

caching,

or scaling?
```

This shows

structured thinking.

______________________________________________________________________

# Whiteboard Strategy

If

using

a whiteboard

or virtual board

follow

this order.

```
Requirements

↓

Numbers

↓

Architecture

↓

Deep Dive

↓

Scaling
```

Never

start

with

the final architecture.

______________________________________________________________________

# Time Management

Typical

45-minute interview.

| Section | Time |
|----------|------|
| Requirements | 5 min |
| Estimation | 5 min |
| Architecture | 10 min |
| Deep Dive | 15 min |
| Scaling & Trade-offs | 10 min |

Don't spend

30 minutes

drawing boxes.

______________________________________________________________________

# Common Follow-Up Questions

Interviewers

often ask

```
What if

traffic

grows 100x?
```

```
What if

Redis fails?
```

```
How do you

prevent duplicates?
```

```
How do you

monitor this?
```

```
How do you

recover

from failures?
```

Always

expect

follow-ups.

______________________________________________________________________

# Architecture Checklist

Before

finishing,

verify

whether

you discussed

- Load Balancer
- API Servers
- Database
- Cache
- Queue
- Storage
- Scaling
- Monitoring
- Security
- Failure Recovery

Not every system

needs

every component,

but

you should

consider them.

______________________________________________________________________

# Decision Framework

When introducing

a technology,

always answer

three questions.

```
Why?

↓

What Problem

Does It Solve?

↓

Trade-offs?
```

Example

Redis

Why?

↓

Reduce

Database Load

Trade-off?

↓

Stale Cache

______________________________________________________________________

# Communication Tips

Think aloud.

Explain

every decision.

Instead of

```
Use Redis.
```

say

```
The system

is read-heavy,

so I'll introduce

Redis

to reduce

database latency.
```

Reasoning

is more important

than

buzzwords.

______________________________________________________________________

# Common Mistakes

## Starting With Kafka

Always

start

with

requirements.

______________________________________________________________________

## Overengineering

Don't use

Kafka,

Redis,

ElasticSearch,

CDN,

and

Microservices

unless

they solve

a real problem.

______________________________________________________________________

## Ignoring Scale

Capacity estimation

guides

architecture.

______________________________________________________________________

## No Trade-offs

Every decision

has

advantages

and disadvantages.

Discuss both.

______________________________________________________________________

## No Failure Handling

Always explain

what happens

when

components fail.

______________________________________________________________________

# Best Practices

✅ Clarify requirements first.

✅ Estimate traffic.

✅ Keep the first architecture simple.

✅ Scale only where needed.

✅ Explain trade-offs.

✅ Mention monitoring.

✅ Handle failures gracefully.

______________________________________________________________________

# Universal System Design Checklist

Before ending

your interview,

confirm

you covered

```
✔ Requirements

✔ Capacity

✔ APIs

✔ Data Model

✔ Architecture

✔ Cache

✔ Database

✔ Queue

✔ Scaling

✔ Monitoring

✔ Failure Recovery

✔ Trade-offs
```

______________________________________________________________________

# Interview Deep Dive

## Question

What is the most important part of a System Design interview?

### Answer

Structured problem solving. Interviewers evaluate how you gather requirements, estimate scale, justify architectural
decisions, identify trade-offs, and communicate your reasoning—not just whether you know specific technologies.

______________________________________________________________________

## Question

Should I always use Redis, Kafka, and Microservices?

### Answer

No. Introduce technologies only when they solve a specific problem. Overengineering is a common interview mistake and
can weaken your design.

______________________________________________________________________

## Question

What if I don't know the perfect architecture?

### Answer

Start with a simple design, explain your assumptions, identify likely bottlenecks, and evolve the architecture
incrementally as requirements and scale increase. Interviewers value this thought process.

______________________________________________________________________

# Practice Exercise

Choose

any one

of the following.

- Amazon
- Uber
- Netflix
- WhatsApp
- BookMyShow
- Instagram

Now

design it

using

only

this framework.

Explain

1. Requirements
1. Capacity estimation
1. APIs
1. Data model
1. High-level architecture
1. Deep dive
1. Bottlenecks
1. Scaling
1. Monitoring
1. Trade-offs

Do this

without

looking

at your notes.

______________________________________________________________________

# Summary

A good System Design interview is not about remembering architectures—it's about following a consistent problem-solving
process.

If you always follow this framework,

- Clarify requirements
- Estimate scale
- Design APIs
- Model the data
- Build a simple architecture
- Dive deeper where needed
- Discuss scaling
- Handle failures
- Explain trade-offs

you'll be able to approach almost any System Design interview with confidence.

______________________________________________________________________

# Next

[System Design Cheat Sheet](34-system-design-cheat-sheet.md)
