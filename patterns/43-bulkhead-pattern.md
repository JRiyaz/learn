# Software Architecture - Part 43

# Bulkhead Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Bulkhead Pattern is
- Why the Bulkhead Pattern exists
- Resource isolation
- Thread pool isolation
- Connection pool isolation
- FastAPI examples
- Kubernetes examples
- AI/ML examples
- Bulkhead vs Circuit Breaker
- When NOT to use the Bulkhead Pattern

______________________________________________________________________

# Before We Start

Imagine

a large ship.

Ships

are divided

into

multiple

watertight compartments.

```text id="bulk4301"
████ | ████ | ████ | ████
```

If

one compartment

fills

with water,

the others

remain safe.

The ship

doesn't sink.

This design

is called

a

**Bulkhead**.

Software

borrows

the same idea.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

Book Service

handles

three operations.

- Search Books
- Borrow Books
- Recommendations

All requests

share

the same

thread pool.

```text id="bulk4302"
Search

↓

Borrow

↓

Recommendation

↓

Shared Threads
```

Everything

works

until...

______________________________________________________________________

# Failure Scenario

Suppose

Recommendation Service

becomes slow.

Every request

waits

20 seconds.

Soon,

all threads

become busy.

Now,

even

Borrow Book

requests

cannot execute.

One feature

has affected

the entire application.

______________________________________________________________________

# Resource Contention

Different workloads

share

the same resources.

Examples:

- Threads
- CPU
- Database Connections
- Memory
- Network

One workload

consumes everything.

Others

starve.

______________________________________________________________________

# The Idea

Instead of

sharing

one pool

of resources,

divide them.

Each feature

gets

its own

resource pool.

______________________________________________________________________

# What is the Bulkhead Pattern?

The **Bulkhead Pattern**

isolates

resources

between

different workloads

so that

a failure

in one part

doesn't affect

the rest

of the application.

______________________________________________________________________

# Architecture

Without Bulkheads

```text id="bulk4303"
Search

Borrow

Recommendation

↓

Shared Resources
```

______________________________________________________________________

With Bulkheads

```text id="bulk4304"
Search

↓

Pool A

Borrow

↓

Pool B

Recommendation

↓

Pool C
```

Each workload

has

its own resources.

______________________________________________________________________

# Thread Pool Isolation

Suppose

your service

has

100 worker threads.

Instead of

one pool,

split them.

```text id="bulk4305"
Search

40 Threads
```

```text id="bulk4306"
Borrow

40 Threads
```

```text id="bulk4307"
Recommendations

20 Threads
```

Now,

if

Recommendations

hang,

Borrow

still works.

______________________________________________________________________

# Database Connection Pools

Suppose

all endpoints

share

one database pool.

```text id="bulk4308"
100 Connections
```

Analytics

runs

a huge query.

All connections

are occupied.

Borrow requests

cannot reach

the database.

Instead,

allocate

separate pools.

```text id="bulk4309"
Borrow

40 Connections
```

```text id="bulk4310"
Analytics

20 Connections
```

```text id="bulk4311"
Search

40 Connections
```

______________________________________________________________________

# FastAPI Example

Suppose

your application

contains

two endpoints.

```python id="bulk4312"
POST /borrow
```

```python id="bulk4313"
GET /recommendations
```

Recommendations

call

an external

ML service.

Borrow

uses

only

the database.

Run

recommendations

in

a separate

worker pool.

Even if

the ML service

slows down,

borrowing

continues.

______________________________________________________________________

# Kubernetes Example

Suppose

Recommendation Service

consumes

too much CPU.

Instead of

running

everything

inside

one Pod,

deploy

separate deployments.

```text id="bulk4314"
Book Pods

3 Replicas
```

```text id="bulk4315"
Recommendation Pods

10 Replicas
```

Each deployment

has

independent

CPU,

memory,

and scaling.

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

supports:

- Chat
- Embeddings
- Image Generation

Image generation

requires

GPUs.

Chat

requires

low latency.

Don't let

image generation

consume

all GPU resources.

Allocate

dedicated resources.

```text id="bulk4316"
Chat GPU Pool
```

```text id="bulk4317"
Image GPU Pool
```

______________________________________________________________________

# Queue Isolation

Suppose

background jobs

share

one queue.

Large

video-processing jobs

occupy

all workers.

Small

email jobs

wait

for hours.

Instead,

create

separate queues.

```text id="bulk4318"
Email Queue
```

```text id="bulk4319"
Video Queue
```

Each queue

has

its own workers.

______________________________________________________________________

# Bulkhead vs Circuit Breaker

Very common

interview question.

| Bulkhead | Circuit Breaker |
| ---------------------------- | --------------------------------- |
| Isolates resources | Stops failing requests |
| Prevents resource starvation | Prevents repeated failures |
| Works before failure spreads | Works after failures are detected |

Often,

they're used

together.

______________________________________________________________________

# Bulkhead + Circuit Breaker

Workflow

```text id="bulk4320"
Recommendation Pool

↓

Circuit Breaker

↓

ML Service
```

If

the ML service

fails,

only

the Recommendation Pool

is affected.

Borrow requests

continue

normally.

______________________________________________________________________

# Bulkhead + Retry

Retries

should stay

inside

their own

resource pool.

Otherwise,

retry storms

can consume

resources

needed

by

other workloads.

______________________________________________________________________

# Real Backend Example

Suppose

a banking application.

Services:

- Balance Inquiry
- Money Transfer
- Statement Generation

Statement generation

may involve

large reports.

If

it shares

resources

with

Money Transfer,

customers

may be unable

to transfer funds.

Bulkheads

prevent

this problem.

______________________________________________________________________

# Cloud Example

Cloud providers

offer

resource isolation

through:

- Kubernetes Namespaces
- Resource Quotas
- CPU Limits
- Memory Limits
- Autoscaling Groups

These mechanisms

implement

Bulkhead principles

at

the infrastructure level.

______________________________________________________________________

# Benefits

Bulkhead Pattern provides:

✅ Fault isolation

✅ Better reliability

✅ Resource protection

✅ Improved resilience

✅ Predictable performance

______________________________________________________________________

# Drawbacks

It also introduces:

❌ More resource planning

❌ Potential underutilization

❌ More operational complexity

______________________________________________________________________

# Capacity Planning

Suppose

Borrow

receives

more traffic

than expected.

If

its pool

is too small,

requests

will still fail.

Bulkheads

must be

sized

according

to

real workloads.

______________________________________________________________________

# Real Company Example

A streaming platform

may separate:

- Video Streaming
- Recommendations
- Search
- Billing

Heavy

recommendation workloads

should never

impact

video playback.

Resource isolation

helps

maintain

core functionality

even

under heavy load.

______________________________________________________________________

# When NOT to Use the Bulkhead Pattern

Don't use

Bulkheads

for:

- Small monoliths
- Simple CRUD APIs
- Applications

with

minimal traffic

and

shared resource usage.

The additional

resource management

may not

provide

enough value.

______________________________________________________________________

# Best Practices

✅ Isolate critical workloads.

✅ Separate CPU-intensive tasks.

✅ Separate database pools where needed.

✅ Monitor pool utilization.

______________________________________________________________________

# Common Mistakes

### One Pool for Everything

Sharing

all resources

defeats

the purpose

of Bulkheads.

______________________________________________________________________

### Tiny Resource Pools

Pools

that are

too small

create

artificial bottlenecks.

______________________________________________________________________

### Ignoring Monitoring

Track:

- Queue length
- Thread usage
- Connection pool usage
- CPU utilization

These metrics

help

identify

resource contention.

______________________________________________________________________

### Isolating Everything

Not every

component

requires

its own pool.

Create

boundaries

where

failures

are likely

to spread.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Bulkhead Pattern, and how does it differ from the Circuit Breaker Pattern?

The Bulkhead Pattern is a resilience pattern that isolates system resources such as threads, connection pools, queues,
CPU, or memory so that failures in one workload do not affect others. It prevents resource starvation by allocating
separate resource pools to different parts of an application. In contrast, the Circuit Breaker Pattern monitors failures
when calling remote services and temporarily stops requests to unhealthy dependencies. Bulkheads focus on resource
isolation, while Circuit Breakers focus on failure isolation. Together, they improve the resilience of distributed
systems.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Bulkhead Pattern is
- Resource isolation
- Thread pool isolation
- Connection pool isolation
- Queue isolation
- Kubernetes example
- AI/ML example
- Bulkhead vs Circuit Breaker
- Best practices

______________________________________________________________________

# 🧠 Reliability Patterns Progress

You now understand the core resilience patterns used in production microservices:

- ✅ API Gateway
- ✅ Saga Pattern
- ✅ Outbox Pattern
- ✅ Circuit Breaker
- ✅ Bulkhead Pattern

These patterns work together to keep large distributed systems available even when individual services fail.

______________________________________________________________________

# What's Next

[Service Discovery](44-service-discovery.md)
