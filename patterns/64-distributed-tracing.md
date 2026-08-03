# System Design - Part 64

# Distributed Tracing

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Distributed Tracing is
- Why Distributed Tracing exists
- Trace
- Span
- Parent-Child Relationships
- Trace Context Propagation
- OpenTelemetry
- Jaeger & Zipkin
- FastAPI examples
- Kubernetes examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

uses

multiple microservices.

A member

borrows

a book.

The request

passes through

multiple services.

```text id="trace6401"
API Gateway

↓

Loan Service

↓

Inventory Service

↓

Notification Service

↓

Payment Service
```

The user

reports

that

the request

takes

10 seconds.

Question.

Which service

is slow?

______________________________________________________________________

# The Problem

Logs

exist.

Metrics

exist.

But

each service

has

its own

logs.

```text id="trace6402"
Gateway Logs

Loan Logs

Inventory Logs

Notification Logs
```

Finding

one request

across

all services

is difficult.

______________________________________________________________________

# Another Problem

Suppose

Payment Service

calls

Fraud Service.

Fraud Service

calls

Redis.

Redis

becomes slow.

How do

you discover

that

Redis

is

the real bottleneck?

______________________________________________________________________

# The Idea

Instead of

viewing

services

individually,

follow

one request

through

the entire system.

______________________________________________________________________

# What is Distributed Tracing?

**Distributed Tracing**

is the process

of tracking

a single request

as it travels

through

multiple services,

allowing engineers

to understand

the complete

execution path

and identify

performance bottlenecks.

______________________________________________________________________

# Trace

A **Trace**

represents

the complete journey

of

one request.

Example

```text id="trace6403"
Borrow Book Request
```

Everything

related

to

that request

belongs

to

one Trace.

______________________________________________________________________

# Span

A **Span**

represents

one operation

inside

a Trace.

Example

```text id="trace6404"
Gateway

↓

Loan Service

↓

Inventory

↓

Payment
```

Each operation

creates

its own

Span.

______________________________________________________________________

# Parent-Child Relationship

Spans

form

a tree.

Example

```text id="trace6405"
Gateway

↓

Loan Service

↓

Inventory Service

↓

Database
```

Gateway

is

the parent.

Loan Service

is

its child.

Database

is

Inventory Service's child.

______________________________________________________________________

# Trace ID

Interview favorite.

Every request

receives

a unique

**Trace ID.**

Example

```text id="trace6406"
Trace ID

abc-123
```

Every service

includes

the same

Trace ID

in

its spans.

______________________________________________________________________

# Span ID

Each Span

also has

its own

unique identifier.

Example

```text id="trace6407"
Trace ID

abc123
```

```text id="trace6408"
Span ID

xyz789
```

One Trace

contains

many Spans.

______________________________________________________________________

# Trace Context Propagation

Suppose

Gateway

calls

Loan Service.

The Trace ID

must travel

with

the request.

```text id="trace6409"
Gateway

↓

Trace ID

↓

Loan Service
```

Otherwise,

the request

appears

as

multiple

independent traces.

______________________________________________________________________

# Example Flow

```text id="trace6410"
Client

↓

Gateway

↓

Loan

↓

Inventory

↓

PostgreSQL
```

Each step

records:

- Start Time
- End Time
- Duration
- Status
- Trace ID

______________________________________________________________________

# Latency Breakdown

Suppose

the request

takes

1000 ms.

Tracing shows

```text id="trace6411"
Gateway

20 ms
```

```text id="trace6412"
Loan Service

80 ms
```

```text id="trace6413"
Inventory Service

850 ms
```

```text id="trace6414"
Database

50 ms
```

Immediately,

developers

know

Inventory Service

is

the bottleneck.

______________________________________________________________________

# Error Tracking

Suppose

Payment Service

returns

HTTP 500.

Tracing

shows

exactly

where

the failure

occurred.

No need

to manually

search

dozens

of log files.

______________________________________________________________________

# OpenTelemetry

Interview favorite.

**OpenTelemetry**

is

the industry standard

for collecting

Telemetry Data.

It supports:

- Traces
- Metrics
- Logs

Most modern

frameworks

support

OpenTelemetry.

______________________________________________________________________

# Jaeger

Jaeger

collects,

stores,

and visualizes

distributed traces.

Example

```text id="trace6415"
Trace Timeline

↓

Gateway

↓

Loan

↓

Inventory
```

Developers

see

the entire

request flow.

______________________________________________________________________

# Zipkin

Zipkin

is another

popular

Distributed Tracing

system.

Like Jaeger,

it helps

visualize

request paths

and latency

across services.

______________________________________________________________________

# FastAPI Example

Suppose

a request

arrives.

```python id="trace6416"
GET /borrow
```

OpenTelemetry

automatically

creates

a Trace

and

Spans

for

database calls,

HTTP requests,

and

external services.

______________________________________________________________________

# Kubernetes Example

Suppose

your application

runs

across

20 Pods.

Tracing

follows

the request

across Pods,

not

just

inside

one container.

This is

essential

for debugging

microservices.

______________________________________________________________________

# AI/ML Example

Suppose

an AI request

passes through

multiple components.

```text id="trace6417"
API

↓

Authentication

↓

Embedding Model

↓

Vector Database

↓

LLM

↓

Response
```

Tracing

shows

which stage

consumes

the most time.

Example

LLM inference

may take

2 seconds,

while

Vector Search

takes

40 ms.

______________________________________________________________________

# External Services

Tracing

can also include

calls

to:

- Payment Providers
- Object Storage
- Redis
- Kafka
- Search Engines

This provides

complete visibility

into

external dependencies.

______________________________________________________________________

# Sampling

Large systems

process

millions

of requests.

Tracing

every request

is expensive.

Instead,

trace

only

a percentage.

Example

```text id="trace6418"
Sample

5%
```

This reduces

storage

and

processing costs.

______________________________________________________________________

# Distributed Tracing vs Logging

Interview favorite.

| Logging | Tracing |
| ------------------ | ---------------------------- |
| Records events | Tracks request flow |
| Individual service | Entire distributed system |
| Good for debugging | Good for bottleneck analysis |

______________________________________________________________________

# Distributed Tracing vs Monitoring

| Monitoring | Tracing |
| ------------------ | --------------------- |
| Aggregated metrics | Individual request |
| Detects issues | Explains request path |

Monitoring

may tell you

latency increased.

Tracing

shows

where.

______________________________________________________________________

# Real Backend Example

Suppose

an order

takes

12 seconds.

Tracing

reveals

that

Inventory Service

waited

10 seconds

for

a slow database query.

Without tracing,

finding

the bottleneck

could take

hours.

______________________________________________________________________

# Benefits

Distributed Tracing provides:

✅ End-to-end visibility

✅ Bottleneck detection

✅ Faster debugging

✅ Cross-service monitoring

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Storage cost

❌ Performance overhead

❌ Instrumentation effort

❌ Trace sampling decisions

______________________________________________________________________

# When NOT to Use Distributed Tracing

Small applications

with

one service

often don't

need

Distributed Tracing.

Logging

and

Monitoring

are usually

sufficient.

Tracing

becomes valuable

once

multiple services

communicate.

______________________________________________________________________

# Best Practices

✅ Propagate Trace IDs.

✅ Instrument

every service.

✅ Sample intelligently.

✅ Correlate

traces,

logs,

and metrics.

______________________________________________________________________

# Common Mistakes

### Losing Trace Context

If

one service

doesn't forward

the Trace ID,

the request

appears

broken

into

multiple traces.

______________________________________________________________________

### Tracing Every Request

Tracing

100%

of traffic

may become

too expensive.

Use

sampling.

______________________________________________________________________

### Ignoring External Calls

Database,

Redis,

Kafka,

and

HTTP calls

should also

be traced.

______________________________________________________________________

### Treating Traces Like Logs

Tracing

shows

the request journey.

Logs

provide

the detailed

information

inside

each step.

Use both.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Distributed Tracing, and why is it important in microservices?

Distributed Tracing tracks the complete lifecycle of a single request as it passes through multiple services in a
distributed system. Every request receives a Trace ID, and each operation creates a Span. This allows engineers to
visualize the complete request path, identify slow services, locate failures, and understand dependencies across APIs,
databases, caches, and external systems. Tools such as OpenTelemetry, Jaeger, and Zipkin make distributed tracing a
fundamental part of modern observability for microservices.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Distributed Tracing is
- Trace
- Span
- Trace Context Propagation
- OpenTelemetry
- Jaeger
- Zipkin
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 Observability Progress

You have now completed the **Observability** module:

- ✅ Logging
- ✅ Monitoring & Metrics
- ✅ Distributed Tracing

Together, these three pillars provide complete visibility into production systems:

- **Logging** → What happened?
- **Monitoring** → Is the system healthy?
- **Tracing** → Where did the request spend time?

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll begin the **Security** module, covering topics that every production backend system must implement:

- Authentication
- Authorization
- Rate Limiting
- API Versioning

We'll start with one of the most important concepts in backend engineering:

> **Authentication & Authorization in System Design**

______________________________________________________________________

# What's Next

[Authentication & Authorization](65-authentication-and-authorization.md)
