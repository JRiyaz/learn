# Software Architecture - Part 35

# Domain-Driven Design (DDD) Fundamentals

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Domain-Driven Design (DDD) is
- Why DDD exists
- The problems it solves
- Domain vs Technical Design
- Ubiquitous Language
- Bounded Context
- Strategic vs Tactical DDD
- Real-world backend examples
- FastAPI examples
- When NOT to use DDD

______________________________________________________________________

# Before We Start

This is one of

the most misunderstood

topics

in software engineering.

Many developers think

DDD means

- Entities
- Value Objects
- Aggregates

Actually,

those are only

a small part

of DDD.

DDD is primarily

about

understanding

the business,

not

writing code.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

The business team says

> A member may reserve up to 5 books.

A developer writes

```python
if reservations < 5:
    ...
```

Another developer

calls it

```python
Booking
```

Another developer

calls it

```python
Hold
```

Another says

```python
Reserve
```

Everyone

means

the same thing,

but

uses different words.

______________________________________________________________________

# Another Problem

Suppose

the company grows.

Different teams

work on

- Payments
- Membership
- Books
- Recommendations

The term

"Member"

means

different things

to each team.

The Payment team

cares about

billing.

The Library team

cares about

borrowing.

The Recommendation team

cares about

reading habits.

Should

they all

share

the same model?

Probably not.

______________________________________________________________________

# The Real Problem

Many software projects

are designed

around

the database.

```text
Books Table

↓

Members Table

↓

Loans Table
```

Instead,

they should be designed

around

the business.

______________________________________________________________________

# What is Domain?

A **Domain**

is

the business area

your software

solves.

Examples:

- Banking
- Healthcare
- E-commerce
- Library Management
- Insurance
- Airline Booking

The domain

is

not

the technology.

It is

the business.

______________________________________________________________________

# What is Domain-Driven Design?

Domain-Driven Design,

popularized by

Eric Evans,

is

an approach

to software design

where

the software model

is built

around

the business domain.

Instead of asking

> "How should I design my database?"

DDD asks

> "How does the business actually work?"

______________________________________________________________________

# The Core Idea

Traditional Development

↓

Technology First

```text
Database

↓

API

↓

Business
```

DDD

↓

Business First

```text
Business

↓

Model

↓

Code

↓

Database
```

Business drives

the software.

______________________________________________________________________

# Ubiquitous Language

One of

the most important

DDD concepts.

Everyone

uses

the same words.

Developers.

Product Managers.

Business Analysts.

QA Engineers.

Everyone.

______________________________________________________________________

# Example

Bad

Business says

```text
Reserve Book
```

Developers write

```text
Book Hold
```

QA writes

```text
Booking
```

Documentation says

```text
Reservation
```

Confusion begins.

______________________________________________________________________

# Good

Everyone

uses

one term.

```text
Reservation
```

Everywhere.

Database.

API.

Documentation.

Meetings.

Code.

This shared vocabulary

is called

**Ubiquitous Language**.

______________________________________________________________________

# Bounded Context

Perhaps

the most important

DDD concept.

Suppose

Amazon

has

multiple teams.

```text
Orders

Payments

Inventory

Shipping
```

Each team

defines

"Order"

differently.

That's okay.

Each team

owns

its own

model.

This boundary

is called

a

**Bounded Context**.

______________________________________________________________________

# Library Example

Our application

may contain

these contexts.

```text
Books

Members

Payments

Recommendations
```

Each context

has

its own rules,

models,

and terminology.

______________________________________________________________________

# Why Bounded Context?

Suppose

the Payment team

adds

```text
credit_score
```

Should

the Recommendation team

care?

No.

Their models

should remain

independent.

______________________________________________________________________

# Strategic vs Tactical DDD

DDD

has

two major parts.

______________________________________________________________________

## Strategic DDD

Focuses on

the big picture.

Examples:

- Bounded Contexts
- Context Mapping
- Team boundaries
- Service boundaries

Question answered:

> How should the business be divided?

______________________________________________________________________

## Tactical DDD

Focuses on

the implementation.

Examples:

- Entities
- Value Objects
- Aggregates
- Domain Events
- Repositories

Question answered:

> How should the code be written?

We'll study

these

in the next lessons.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Contexts

might be

```text
Catalog

Orders

Payments

Shipping

Customer Support
```

Each team

owns

its own

business rules.

______________________________________________________________________

# FastAPI Example

Instead of

one huge project,

organize

by domain.

```text
app/

books/

members/

payments/

recommendations/
```

Not

by technology.

Avoid

```text
controllers/

services/

repositories/
```

for very large systems,

because business features

become scattered.

______________________________________________________________________

# AI/ML Example

Suppose

an AI platform.

Contexts

might include

```text
Prompt Management

Model Serving

Training

Billing

Monitoring
```

Each context

has

its own

business model.

The Training team

shouldn't

directly depend

on

Billing models.

______________________________________________________________________

# Context Map

Large organizations

connect

Bounded Contexts

using

Context Maps.

Example

```text
Orders

↓

Payments

↓

Shipping

↓

Notifications
```

Each context

communicates

through

well-defined contracts,

not

shared databases.

______________________________________________________________________

# DDD and Microservices

One of

the biggest

DDD influences.

Many organizations

create

microservices

around

Bounded Contexts.

Example

```text
Payment Service

Inventory Service

Order Service

Notification Service
```

Notice

the service boundary

matches

the business boundary.

______________________________________________________________________

# DDD vs CRUD

| CRUD | DDD |
| ------------------- | -------------------- |
| Database-first | Business-first |
| Tables drive design | Domain drives design |
| Technical focus | Business focus |

______________________________________________________________________

# Benefits

DDD gives you:

✅ Better business understanding

✅ Shared language

✅ Clear service boundaries

✅ Easier long-term maintenance

✅ Better collaboration

between business

and engineering teams.

______________________________________________________________________

# Drawbacks

DDD also introduces:

❌ Learning curve

❌ More modeling work

❌ More abstractions

❌ Requires close business collaboration

______________________________________________________________________

# Real Company Example

Netflix

doesn't have

one giant model

for

everything.

Streaming,

Billing,

Recommendations,

Profiles,

and

Content Management

are all

different business domains,

each with

its own language

and rules.

______________________________________________________________________

# When NOT to Use DDD

Don't use

full DDD

for:

- Small CRUD APIs
- Internal admin tools
- Personal projects
- Applications with simple business rules

DDD provides

the most value

when

business complexity

is higher

than

technical complexity.

______________________________________________________________________

# Best Practices

✅ Learn the business first.

✅ Use a ubiquitous language.

✅ Identify bounded contexts early.

✅ Model business concepts,

not database tables.

______________________________________________________________________

# Common Mistakes

### Database-Driven Design

Don't start

with

tables.

Start

with

business concepts.

______________________________________________________________________

### One Model for Everything

Different domains

often require

different models.

______________________________________________________________________

### Ignoring Business Experts

DDD

requires

collaboration

with

domain experts.

______________________________________________________________________

### Confusing DDD with Design Patterns

DDD

is

a software design philosophy,

not

a collection

of coding patterns.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Domain-Driven Design (DDD), and why is it useful?

Domain-Driven Design (DDD) is a software design approach that models applications around the business domain rather than
technical concerns. It emphasizes collaboration between developers and domain experts to create a shared ubiquitous
language and divide the system into bounded contexts, each representing a distinct business area. DDD is especially
valuable for complex domains because it aligns software with real business processes, improves maintainability, and
provides a strong foundation for architectures such as microservices.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What DDD is
- Domain vs Technology
- Ubiquitous Language
- Bounded Context
- Strategic vs Tactical DDD
- FastAPI example
- AI/ML example
- DDD vs CRUD
- Best practices

______________________________________________________________________

# 🚀 Important Note

This lesson covered the **philosophy** of DDD.

Starting in the next lesson, we'll move into the **building blocks** of Tactical DDD that you'll use in code:

- Entities
- Value Objects
- Aggregates
- Aggregate Roots
- Domain Services
- Domain Events
- Repositories
- Factories

These concepts are frequently discussed in senior backend and system design interviews.

______________________________________________________________________

# What's Next

[DDD: Entities, Value Objects & Aggregates](36-ddd-entities-value-objects-aggregates.md)
