# Software Architecture - Part 42

# Circuit Breaker Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What the Circuit Breaker Pattern is
- Why Circuit Breakers exist
- Cascading failures
- Circuit states
- Closed, Open, and Half-Open states
- FastAPI examples
- Microservices examples
- AI/ML examples
- Circuit Breaker vs Retry
- When NOT to use Circuit Breakers

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

contains

these services.

```text id="cb4201"
Book Service

↓

Payment Service

↓

Notification Service
```

Everything

works perfectly.

Until

one day,

Payment Service

starts failing.

What happens

to

Book Service?

Let's find out.

______________________________________________________________________

# The Problem

Book Service

needs

Payment Service.

```text id="cb4202"
Book Service

↓

Payment Service
```

Every request

waits

for

Payment Service.

Suppose

Payment Service

becomes slow.

Each request

waits

30 seconds.

Soon,

Book Service

runs out

of worker threads.

Now,

Book Service

also becomes unavailable.

______________________________________________________________________

# Cascading Failure

One service

fails.

Another service

waits.

Soon,

another service

fails.

Eventually,

the whole system

is affected.

```text id="cb4203"
Payment

❌

↓

Book

❌

↓

Gateway

❌

↓

Client
```

This is called

a

**Cascading Failure**.

______________________________________________________________________

# Another Problem

Developers

often write

this.

```python id="cb4204"
while True:

    try:

        payment()

        break

    except:

        pass
```

The service

keeps retrying.

When

Payment Service

is already overloaded,

these retries

make

the problem

even worse.

______________________________________________________________________

# The Idea

Suppose

an electrical circuit

detects

a fault.

It opens

the circuit

to prevent damage.

The same idea

can be applied

to software.

If

a dependency

is failing,

stop calling it

for a while.

______________________________________________________________________

# What is the Circuit Breaker Pattern?

The **Circuit Breaker Pattern**

prevents

an application

from repeatedly

calling

a failing service.

Instead,

it temporarily

stops

requests,

allowing

the failing service

time

to recover.

______________________________________________________________________

# The Three States

A Circuit Breaker

has

three states.

```text id="cb4205"
Closed

↓

Open

↓

Half-Open

↓

Closed
```

Let's study

each one.

______________________________________________________________________

# State 1

## Closed

Everything

is healthy.

Requests

flow normally.

```text id="cb4206"
Book Service

↓

Payment Service
```

Failures

are counted.

______________________________________________________________________

# State 2

## Open

Suppose

five consecutive

requests fail.

The breaker

opens.

```text id="cb4207"
Book Service

↓

❌

↓

Payment Service
```

Requests

are rejected

immediately.

No network call

is made.

This protects

both services.

______________________________________________________________________

# State 3

## Half-Open

After

a timeout,

the breaker

allows

a small number

of test requests.

```text id="cb4208"
One Request

↓

Payment Service
```

If

the request

succeeds,

the breaker

closes.

If

it fails,

the breaker

opens again.

______________________________________________________________________

# State Diagram

```text id="cb4209"
Closed

↓

Failures

↓

Open

↓

Timeout

↓

Half-Open

↓

Success

↓

Closed
```

______________________________________________________________________

# Example

Suppose

Payment Service

fails

10 times.

```text id="cb4210"
Failure

↓

Failure

↓

Failure

↓

Open Circuit
```

The next

1,000 requests

fail instantly,

without

contacting

Payment Service.

______________________________________________________________________

# FastAPI Example

Suppose

Book Service

calls

Payment Service.

Instead of

```python id="cb4211"
payment_client.pay()
```

the call

goes through

a Circuit Breaker.

```python id="cb4212"
breaker.call(

    payment_client.pay

)
```

The breaker

tracks

failures

automatically.

______________________________________________________________________

# Retry vs Circuit Breaker

Very common

interview question.

Retry

↓

Try again.

Circuit Breaker

↓

Stop trying.

Retries

assume

the failure

is temporary.

Circuit Breakers

assume

the service

is unhealthy.

______________________________________________________________________

# Retry + Circuit Breaker

In practice,

both

are used together.

Workflow

```text id="cb4213"
Request

↓

Retry (3 Times)

↓

Still Failing

↓

Open Circuit
```

Limited retries

handle

temporary issues.

The breaker

prevents

continuous failures.

______________________________________________________________________

# Fallback

Instead of

returning

an error,

the breaker

may provide

a fallback.

Example

```text id="cb4214"
Payment Failed

↓

Cached Response

↓

Default Value
```

Users

receive

a degraded,

but usable,

experience.

______________________________________________________________________

# AI/ML Example

Suppose

your application

calls

an LLM API.

```text id="cb4215"
App

↓

LLM Provider
```

If

the provider

is unavailable,

the Circuit Breaker

can:

- Return cached answers
- Use a local model
- Return a friendly error

instead of

waiting

30 seconds

for every request.

______________________________________________________________________

# Real Backend Example

Suppose

Recommendation Service

depends

on

an ML model.

If

the model service

fails,

recommendations

can be skipped,

while

checkout

continues.

The business

remains available,

although

with reduced functionality.

______________________________________________________________________

# Popular Libraries

Java

↓

Resilience4j

.NET

↓

Polly

Python

↓

PyBreaker

Cloud platforms

often provide

Circuit Breakers

through

service meshes

such as

Istio

or

Envoy.

______________________________________________________________________

# Benefits

Circuit Breakers provide:

✅ Prevent cascading failures

✅ Faster failure detection

✅ Better resource utilization

✅ Improved resilience

✅ Graceful degradation

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Additional complexity

❌ State management

❌ Configuration tuning

❌ False positives

if thresholds

are too aggressive.

______________________________________________________________________

# Choosing Thresholds

Suppose

the breaker

opens

after

one failure.

Too sensitive.

Suppose

it opens

after

10,000 failures.

Too slow.

Thresholds

must match

the reliability

requirements

of the system.

______________________________________________________________________

# Real Company Example

Suppose

a food delivery platform.

Checkout

depends

on

a mapping service

for

delivery estimates.

If

the mapping service

fails,

orders

can still

be placed,

using

estimated delivery times

or

a fallback calculation.

The checkout system

stays online.

______________________________________________________________________

# Circuit Breaker vs Timeout

Another interview question.

| Timeout | Circuit Breaker |
| ---------------------- | -------------------- |
| Limits waiting time | Stops future calls |
| Per request | Across many requests |
| Doesn't track failures | Tracks failures |

Most production systems

use both.

______________________________________________________________________

# Circuit Breaker vs Load Balancer

| Load Balancer | Circuit Breaker |
| -------------------- | ------------------------- |
| Distributes requests | Prevents failing requests |
| Chooses destination | Decides whether to call |

These patterns

solve

different problems.

______________________________________________________________________

# When NOT to Use Circuit Breakers

Don't use

Circuit Breakers

for:

- Local function calls
- Single-process applications
- Internal helper methods

They are most valuable

when

communicating

with

external systems

or

remote services.

______________________________________________________________________

# Best Practices

✅ Combine with timeouts.

✅ Use limited retries.

✅ Provide fallbacks where appropriate.

✅ Monitor breaker metrics.

______________________________________________________________________

# Common Mistakes

### Infinite Retries

Never retry

forever.

Retries

must have

limits.

______________________________________________________________________

### No Timeout

A Circuit Breaker

without

timeouts

may wait

too long

before recording failures.

______________________________________________________________________

### No Monitoring

Track:

- Failure count
- Open duration
- Half-open attempts

These metrics

help diagnose

service health.

______________________________________________________________________

### Aggressive Thresholds

Poor thresholds

can cause

healthy services

to appear

unavailable.

Tune them

using

real production data.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the Circuit Breaker Pattern, and why is it useful?

The Circuit Breaker Pattern is a resilience pattern that prevents applications from repeatedly calling a failing remote
service. It monitors failures and transitions through three states: Closed (normal operation), Open (requests fail
immediately), and Half-Open (a limited number of test requests determine whether the service has recovered). This
prevents cascading failures, conserves system resources, and improves overall reliability. Circuit Breakers are commonly
used with retries, timeouts, and fallback mechanisms in distributed systems.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What the Circuit Breaker Pattern is
- Cascading failures
- Closed, Open, and Half-Open states
- Retry vs Circuit Breaker
- Fallbacks
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand:

- ✅ API Gateway
- ✅ Saga Pattern
- ✅ Outbox Pattern
- ✅ Circuit Breaker Pattern

These patterns are fundamental to building reliable, fault-tolerant microservice architectures.

______________________________________________________________________

# What's Next

[Bulkhead Pattern](43-bulkhead-pattern.md)
