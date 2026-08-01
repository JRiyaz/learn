# Software Architecture - Part 38

# Microservices Architecture

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Microservices are
- Why Microservices exist
- Monolith vs Microservices
- Service boundaries
- Database per Service
- Communication patterns
- Synchronous vs Asynchronous communication
- DDD and Microservices
- FastAPI implementation
- When NOT to use Microservices

______________________________________________________________________

# Before We Start

This is probably

the most requested

architecture topic

in backend engineering.

However,

many developers

make one mistake.

They think

> "Microservices make applications scalable."

Not exactly.

Microservices

solve

organizational

and

architectural problems.

They also introduce

many new challenges.

Let's understand

when

they help

and

when

they hurt.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

Initially,

everything

lives

inside

one application.

```text id="ms3801"
Books

↓

Members

↓

Payments

↓

Notifications

↓

Recommendations

↓

Analytics
```

One project.

One deployment.

One database.

Everything works.

______________________________________________________________________

# Six Months Later

The company grows.

Now,

different teams

work on:

- Books
- Payments
- Recommendations
- Analytics

Every deployment

requires

the entire application

to be rebuilt.

One bug

can affect

everyone.

______________________________________________________________________

# Another Problem

Traffic changes.

Books API

receives

100,000 requests/minute.

Payments

receive

only

500 requests/minute.

Can we scale

only

the Books module?

Not easily.

Everything

runs together.

______________________________________________________________________

# What is a Monolith?

A **Monolith**

is

an application

where

all business capabilities

are packaged

and deployed

as

one unit.

Example

```text id="ms3802"
FastAPI

↓

Books

↓

Payments

↓

Members

↓

Analytics

↓

One Database
```

______________________________________________________________________

# Advantages of a Monolith

Monoliths provide:

✅ Easy development

✅ Simple deployment

✅ Simple debugging

✅ Easy transactions

✅ Lower operational cost

For small

and medium projects,

a monolith

is often

the best choice.

______________________________________________________________________

# Problems with Large Monoliths

As applications grow,

monoliths may develop:

❌ Long deployment times

❌ Large codebases

❌ Team conflicts

❌ Scaling limitations

❌ Technology lock-in

______________________________________________________________________

# The Idea

Instead of

one large application,

split

the system

into

small,

independent services.

Each service

owns

one business capability.

______________________________________________________________________

# What are Microservices?

A **Microservice**

is

an independently deployable

application

that owns

a specific

business capability.

Examples:

- Book Service
- Member Service
- Payment Service
- Recommendation Service

Each service

has

its own lifecycle.

______________________________________________________________________

# Architecture

```text id="ms3803"
Client

↓

API Gateway

↓

Book Service

Member Service

Payment Service

Recommendation Service
```

Each service

runs independently.

______________________________________________________________________

# Database per Service

One of

the most important

microservice principles.

Every service

owns

its own database.

```text id="ms3804"
Book Service

↓

Books DB
```

```text id="ms3805"
Payment Service

↓

Payments DB
```

Never

allow

multiple services

to share

the same database.

______________________________________________________________________

# Why?

Suppose

Book Service

changes

its schema.

Should

Payment Service

break?

No.

Independent databases

allow

independent evolution.

______________________________________________________________________

# Service Ownership

Each service

owns

one

business capability.

Good

```text id="ms3806"
Books

Payments

Members

Recommendations
```

Bad

```text id="ms3807"
User Table Service

Book Table Service

Loan Table Service
```

Services

should represent

business domains,

not

database tables.

______________________________________________________________________

# DDD Connection

Remember

Bounded Contexts?

Each

Bounded Context

often becomes

one microservice.

Example

```text id="ms3808"
Books Context

↓

Book Service
```

```text id="ms3809"
Payments Context

↓

Payment Service
```

DDD

helps

identify

microservice boundaries.

______________________________________________________________________

# Communication

Services

must communicate.

There are

two main approaches.

______________________________________________________________________

# Synchronous Communication

One service

waits

for another.

Examples:

- HTTP REST
- gRPC

```text id="ms3810"
Order Service

↓

Payment Service

↓

Response
```

Simple,

but

creates coupling.

______________________________________________________________________

# Asynchronous Communication

Services

communicate

through events.

Examples:

- Kafka
- RabbitMQ
- Amazon SQS

```text id="ms3811"
OrderPlaced

↓

Kafka

↓

Inventory

↓

Shipping

↓

Analytics
```

The sender

doesn't wait

for consumers.

______________________________________________________________________

# FastAPI Example

Book Service

```python id="ms3812"
@app.post("/books")
```

Payment Service

```python id="ms3813"
@app.post("/payments")
```

Each service

runs

as

its own

FastAPI application.

______________________________________________________________________

# Service Discovery

Suppose

multiple instances

of

Book Service

exist.

How does

Payment Service

find them?

Using

Service Discovery.

We'll study

this later.

______________________________________________________________________

# API Gateway

Clients

shouldn't

call

20 services

directly.

Instead,

they call

an

API Gateway.

```text id="ms3814"
Client

↓

API Gateway

↓

Microservices
```

The gateway

handles

routing,

authentication,

and

aggregation.

______________________________________________________________________

# Distributed Transactions

Suppose

placing an order

requires:

- Payment
- Inventory
- Shipping

What happens

if

Payment succeeds

but

Inventory fails?

Traditional database

transactions

don't work

across services.

Microservices

require

new patterns,

such as:

- Saga
- Outbox

We'll learn

those next.

______________________________________________________________________

# Real Backend Example

Suppose

Netflix.

Services include:

- User Service
- Billing Service
- Recommendation Service
- Streaming Service
- Content Metadata Service

Each team

deploys

its service

independently.

______________________________________________________________________

# AI/ML Example

Suppose

an AI platform.

Services:

```text id="ms3815"
Model Registry

↓

Training

↓

Inference

↓

Monitoring

↓

Billing
```

Each service

can scale

independently.

Inference

may require

100 instances.

Billing

may require

only 2.

______________________________________________________________________

# Monolith vs Microservices

| Monolith | Microservices |
| ------------------ | --------------------------- |
| One deployment | Multiple deployments |
| One database | Database per service |
| Easier development | Easier independent scaling |
| Simpler operations | More operational complexity |

______________________________________________________________________

# Benefits

Microservices provide:

✅ Independent deployments

✅ Independent scaling

✅ Smaller codebases

✅ Better team autonomy

✅ Technology flexibility

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Distributed systems complexity

❌ Network failures

❌ Eventual consistency

❌ Service discovery

❌ Monitoring complexity

❌ Distributed tracing

❌ More infrastructure

______________________________________________________________________

# Common Misconception

Many people

think

Microservices

make applications

faster.

Not necessarily.

Network calls

are

much slower

than

function calls.

Microservices

improve

organizational scalability,

not

individual request speed.

______________________________________________________________________

# Real Company Example

Amazon's famous

"Two Pizza Team"

approach

encouraged

small,

independent teams

to own

their services.

This organizational model

works well

with

microservice architectures,

where teams

can build,

deploy,

and operate

their services

independently.

______________________________________________________________________

# When NOT to Use Microservices

Don't use

Microservices

for:

- Small startups
- CRUD applications
- Internal tools
- Small teams
- Early-stage products

Start

with

a modular monolith.

Split

into microservices

only

when

clear business

or organizational needs

emerge.

______________________________________________________________________

# Best Practices

✅ Design services around business capabilities.

✅ Give each service its own database.

✅ Prefer asynchronous communication when appropriate.

✅ Keep services independently deployable.

______________________________________________________________________

# Common Mistakes

### Splitting Too Early

Many teams

adopt

microservices

before

they understand

their domain.

Start simple.

______________________________________________________________________

### Shared Database

Sharing

one database

between services

creates

tight coupling

and defeats

service independence.

______________________________________________________________________

### Wrong Service Boundaries

Don't split

by database tables.

Split

by

business capabilities

and

bounded contexts.

______________________________________________________________________

### Synchronous Calls Everywhere

If every service

must wait

for five others,

the system

becomes fragile.

Use events

where appropriate.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are Microservices, and when should they be used?

Microservices are independently deployable services, each responsible for a specific business capability. Every service
owns its business logic, data, and lifecycle, allowing teams to develop, deploy, and scale them independently. They are
well suited for large systems with multiple teams, complex business domains, and varying scalability requirements.
However, microservices introduce distributed systems challenges such as network failures, eventual consistency, service
discovery, and distributed transactions, making them unsuitable for many small applications.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Microservices are
- Monolith vs Microservices
- Database per Service
- Synchronous vs Asynchronous communication
- DDD connection
- FastAPI example
- AI/ML example
- Benefits
- Common mistakes

______________________________________________________________________

# 🚀 What's Coming Next

From this point onward, we'll study the patterns that make microservices reliable in production.

These include:

- API Gateway
- Saga Pattern
- Outbox Pattern
- Circuit Breaker
- Bulkhead
- Service Discovery
- Distributed Transactions

Together, these patterns solve the biggest challenges of distributed systems.

______________________________________________________________________

# What's Next

[API Gateway Pattern](39-api-gateway-pattern.md)
