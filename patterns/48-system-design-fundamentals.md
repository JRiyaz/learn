# System Design - Part 48

# System Design Fundamentals

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What System Design is
- Why System Design matters
- Functional vs Non-Functional Requirements
- Capacity Estimation
- Bottlenecks
- High-Level Design (HLD)
- Low-Level Design (LLD)
- System Design Interview Process
- Common mistakes
- Real-world examples

______________________________________________________________________

# Before We Start

Congratulations!

You've completed

the Software Architecture module.

Now,

we begin

the next major topic:

**System Design.**

Everything

you've learned so far

will now

come together.

You'll use:

- SOLID
- Design Patterns
- DDD
- Microservices
- Distributed Systems

to design

real-world applications.

______________________________________________________________________

# What is System Design?

System Design

is the process

of designing

a software system

that satisfies

business requirements,

performance goals,

and scalability needs.

It answers questions like:

- How should the system be structured?
- How will components communicate?
- How will data be stored?
- How will the system scale?
- How will failures be handled?

______________________________________________________________________

# What Does a System Designer Do?

A system designer

doesn't write

individual functions.

Instead,

they answer

questions like:

- Should we use Redis?
- Do we need Kafka?
- One database or many?
- Monolith or Microservices?
- SQL or NoSQL?
- CDN or not?

______________________________________________________________________

# A Simple Example

Suppose

someone asks:

> Design a URL Shortener.

Immediately,

you should think about:

```text id="sd4801"
Users

↓

API

↓

Database

↓

Cache

↓

Analytics
```

Not

the code.

The architecture.

______________________________________________________________________

# System Design vs Coding

| Coding | System Design |
| -------------------- | ------------------- |
| Individual functions | Entire systems |
| Algorithms | Architecture |
| Correctness | Scalability |
| Local optimization | Global optimization |

Both

are important,

but

they solve

different problems.

______________________________________________________________________

# Functional Requirements

Functional Requirements

describe

**what**

the system

must do.

Examples:

Library System

- Borrow books
- Return books
- Search books
- Pay fines

URL Shortener

- Shorten URLs
- Redirect URLs
- Track clicks

______________________________________________________________________

# Non-Functional Requirements

Non-Functional Requirements

describe

**how well**

the system

should perform.

Examples:

- High availability
- Low latency
- Scalability
- Security
- Reliability
- Durability

These

often determine

the architecture.

______________________________________________________________________

# Example

Suppose

you need

to build

a chat application.

Functional Requirements

```text id="sd4802"
Send Message

Receive Message

Create Group
```

Non-Functional Requirements

```text id="sd4803"
100 Million Users

<100ms Latency

99.99% Availability
```

Notice

the requirements

change

the design.

______________________________________________________________________

# High-Level Design (HLD)

High-Level Design

focuses on

major components.

Example

```text id="sd4804"
Client

↓

Load Balancer

↓

API

↓

Cache

↓

Database
```

At this stage,

we don't care

about

class diagrams

or

individual methods.

______________________________________________________________________

# Low-Level Design (LLD)

Low-Level Design

focuses on

implementation.

Examples:

- Classes
- Interfaces
- Design Patterns
- Database schema
- APIs

LLD answers

questions like

"How should this service be implemented?"

______________________________________________________________________

# Capacity Estimation

Every system

starts

with

basic estimates.

Questions include:

- How many users?
- Requests per second?
- Storage required?
- Network bandwidth?
- Peak traffic?

Without estimates,

it's difficult

to choose

the right architecture.

______________________________________________________________________

# Example

Suppose

10 million users

visit

your application.

If

1 million

are active daily,

how many requests

arrive

every second?

These numbers

influence:

- Server count
- Database size
- Cache size
- Load balancers

We'll learn

how to calculate

these values

in later lessons.

______________________________________________________________________

# Identifying Bottlenecks

Every system

has bottlenecks.

Examples:

- CPU
- Database
- Network
- Disk
- External APIs

A good design

identifies

likely bottlenecks

before

they become

production problems.

______________________________________________________________________

# Real Backend Example

Suppose

your API

calls

a third-party

payment provider.

```text id="sd4805"
Client

↓

Your API

↓

Payment Provider
```

Question.

What happens

if

the provider

becomes slow?

You'll recognize

this immediately.

Solution:

- Timeout
- Retry
- Circuit Breaker

Architecture knowledge

helps

solve

real problems.

______________________________________________________________________

# AI/ML Example

Suppose

you build

an AI chatbot.

High-Level Design

might look like:

```text id="sd4806"
Client

↓

API Gateway

↓

Authentication

↓

Prompt Service

↓

LLM

↓

Vector Database

↓

PostgreSQL
```

Each component

has

a specific responsibility.

______________________________________________________________________

# Common Components

Most modern

backend systems

contain

some combination

of:

- Load Balancer
- API Gateway
- Application Servers
- Cache
- Database
- Message Queue
- Search Engine
- CDN
- Monitoring

The challenge

is deciding

which ones

are actually needed.

______________________________________________________________________

# The System Design Process

During interviews,

follow

a structured approach.

Step 1

↓

Clarify requirements.

Step 2

↓

Estimate scale.

Step 3

↓

Design the High-Level Architecture.

Step 4

↓

Identify bottlenecks.

Step 5

↓

Improve the design.

Following

the same process

helps

avoid missing

important considerations.

______________________________________________________________________

# Common Mistakes

### Jumping into Architecture

Don't start

drawing databases

before

understanding

the requirements.

______________________________________________________________________

### Ignoring Scale

Designing

for

100 users

is different

from

100 million users.

Always ask

about scale.

______________________________________________________________________

### Using Every Technology

Don't add:

- Kafka
- Redis
- Elasticsearch
- Kubernetes

unless

they solve

a real problem.

Complexity

is a cost.

______________________________________________________________________

### Forgetting Non-Functional Requirements

Availability,

latency,

security,

and scalability

often matter

more than

the functional features.

______________________________________________________________________

# Best Practices

✅ Clarify requirements first.

✅ Estimate traffic.

✅ Design incrementally.

✅ Identify bottlenecks.

✅ Justify every technology choice.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is System Design?

System Design is the process of designing scalable, reliable, maintainable, and efficient software systems that satisfy
both functional and non-functional requirements. It involves selecting appropriate architectures, databases,
communication patterns, caching strategies, and infrastructure while considering scalability, availability, reliability,
and cost. A good system design balances technical trade-offs rather than simply choosing the most advanced technologies.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What System Design is
- Functional vs Non-Functional Requirements
- High-Level vs Low-Level Design
- Capacity Estimation
- Bottlenecks
- The System Design process
- Common mistakes
- Best practices

______________________________________________________________________

# 🚀 What's Coming Next

Before designing systems like:

- WhatsApp
- YouTube
- Uber
- Instagram
- Netflix
- Google Drive

you must first learn

the fundamental building blocks

used in almost every distributed system.

We'll begin with

the most important one:

**Load Balancers**.

______________________________________________________________________

# What's Next

[Load Balancers](49-load-balancers.md)
