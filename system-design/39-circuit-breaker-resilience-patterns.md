# Advanced Distributed Systems – Circuit Breaker & Resilience Patterns

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand Circuit Breakers, resilience patterns, retries, timeouts, bulkheads, fallback strategies, and how modern distributed systems remain available during failures.

______________________________________________________________________

# Introduction

Imagine

your application

calls

```
Payment Service
```

Normally

everything

works.

But suddenly

Payment Service

becomes

very slow.

Your application

continues

sending requests.

Eventually

```
Threads Exhausted

↓

Timeouts

↓

Database Connections Blocked

↓

Entire System Down
```

This is called

```
Cascading Failure
```

Modern systems

prevent this

using

```
Circuit Breakers
```

______________________________________________________________________

# What Is A Circuit Breaker?

A Circuit Breaker

protects

your application

from repeatedly

calling

an unhealthy service.

Instead of

```
Service A

↓

Payment Service

↓

Timeout
```

every time,

the Circuit Breaker

quickly rejects

requests

until

the downstream service

recovers.

______________________________________________________________________

# Real-World Analogy

Think of

an electrical

circuit breaker.

```
Too Much Current

↓

Breaker Trips

↓

Power Stops
```

The breaker

protects

the system.

Software

uses

the same idea.

______________________________________________________________________

# Why Do We Need It?

Without

a Circuit Breaker

```
1000 Requests

↓

1000 Timeouts
```

Application threads

remain blocked.

Eventually

the entire system

fails.

______________________________________________________________________

# Basic Architecture

```
Users

↓

API

↓

Circuit Breaker

↓

Payment Service
```

Every request

passes through

the breaker.

______________________________________________________________________

# Circuit States

Interview favorite.

A Circuit Breaker

has

three states.

```
Closed

↓

Open

↓

Half-Open
```

______________________________________________________________________

# Closed State

Normal operation.

```
Request

↓

Payment Service

↓

Response
```

Failures

are counted.

______________________________________________________________________

# Open State

Too many failures.

```
Request

↓

Circuit Breaker

↓

Rejected Immediately
```

No request

reaches

the downstream service.

______________________________________________________________________

# Half-Open State

After

a cooldown period

allow

a few

test requests.

```
Request

↓

Payment Service

↓

Success?
```

If successful

```
Closed
```

Otherwise

```
Open Again
```

______________________________________________________________________

# State Transition

```
Closed

↓

Failure Threshold Reached

↓

Open

↓

Wait

↓

Half-Open

↓

Success

↓

Closed
```

______________________________________________________________________

# Failure Threshold

Example

```
50%

Failures

Within

20 Requests
```

Circuit

opens.

Thresholds

depend

on

business requirements.

______________________________________________________________________

# Timeout

Interview favorite.

Never wait

forever.

Example

```
Payment API

↓

Timeout

2 Seconds
```

After timeout

treat

the request

as failed.

______________________________________________________________________

# Why Timeouts Matter

Without

timeouts

threads

remain blocked.

Eventually

```
Thread Pool

↓

Exhausted
```

No requests

can be processed.

______________________________________________________________________

# Retry Pattern

Temporary failures

can often

be retried.

```
Request

↓

Failure

↓

Retry

↓

Success
```

______________________________________________________________________

# When Should You Retry?

Good candidates

- Network timeout
- Temporary service outage
- HTTP 503
- Connection reset

______________________________________________________________________

# When NOT To Retry?

Don't retry

for

- Invalid request
- Authentication failure
- Validation errors
- Permission denied

Retrying

won't help.

______________________________________________________________________

# Exponential Backoff

Interview favorite.

Instead of

retrying immediately

```
1 sec

↓

2 sec

↓

4 sec

↓

8 sec
```

Reduces

pressure

on

the failing service.

______________________________________________________________________

# Jitter

Suppose

1000 clients

retry

at

exactly

2 seconds.

Problem

```
Retry Storm
```

Solution

```
Random Delay

(Jitter)
```

Example

```
2.3 sec

1.8 sec

2.6 sec
```

Requests

are spread out.

______________________________________________________________________

# Retry + Circuit Breaker

Common pattern.

```
Request

↓

Retry

↓

Still Failing

↓

Circuit Opens
```

Retries

should happen

before

opening

the circuit.

______________________________________________________________________

# Fallback

Interview favorite.

Suppose

Recommendation Service

fails.

Instead of

returning

an error

show

```
Popular Products
```

instead.

______________________________________________________________________

# Example

```
Recommendations

↓

Failure

↓

Trending Products
```

User

still receives

a usable response.

______________________________________________________________________

# Bulkhead Pattern

Interview favorite.

Imagine

one ship.

If

one compartment

fills with water,

the entire ship

doesn't sink.

Software

uses

the same idea.

______________________________________________________________________

# Bulkhead Example

Separate

thread pools.

```
Payments

↓

Thread Pool A
```

```
Notifications

↓

Thread Pool B
```

Payment failures

won't consume

notification threads.

______________________________________________________________________

# Why Bulkheads?

Without isolation

one failing service

can consume

all resources.

______________________________________________________________________

# Rate Limiting

Prevent

overloading

downstream services.

Example

```
100 Requests/sec
```

Extra requests

are delayed

or rejected.

______________________________________________________________________

# Queue

Suppose

Email Service

becomes slow.

Instead of

blocking

users

```
Queue

↓

Worker

↓

Email
```

Absorb

traffic spikes.

______________________________________________________________________

# Hedged Requests

Interview bonus.

Send

the same request

to

multiple replicas

when latency

is unusually high.

Use

the first

successful response.

Useful

for

latency-sensitive systems,

but

increases load.

______________________________________________________________________

# Graceful Degradation

Interview favorite.

Suppose

Search Suggestions

fail.

Continue

serving

basic search.

Disable

only

the failing feature.

______________________________________________________________________

# Health Checks

Circuit Breakers

should monitor

service health.

Metrics

include

- Latency
- Error rate
- Timeout rate

______________________________________________________________________

# Monitoring

Monitor

- Circuit state
- Failure count
- Retry count
- Timeout rate
- Latency
- Open duration
- Fallback usage

______________________________________________________________________

# Failure Scenarios

## Payment Service Down

Circuit

opens.

Fallback

returns

appropriate error

or queues

the request,

depending on

business requirements.

______________________________________________________________________

## Recommendation Service Down

Show

cached

or

popular items.

______________________________________________________________________

## Notification Service Down

Store

notifications

inside

a queue

for later delivery.

______________________________________________________________________

## Database Slow

Increase

timeouts carefully,

optimize queries,

or fail fast

if necessary.

Avoid

indefinitely waiting.

______________________________________________________________________

# Typical Architecture

```
                  Users
                     │
                     ▼
               API Gateway
                     │
                     ▼
             Circuit Breaker
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 Payment Service Search Service User Service
        │            │            │
        ▼            ▼            ▼
     Database     Redis      Database
```

______________________________________________________________________

# Common Resilience Patterns

| Pattern | Purpose |
|----------|---------|
| Timeout | Stop waiting forever |
| Retry | Handle transient failures |
| Exponential Backoff | Reduce retry pressure |
| Jitter | Prevent retry storms |
| Circuit Breaker | Stop repeated failures |
| Bulkhead | Isolate failures |
| Queue | Absorb traffic spikes |
| Fallback | Provide degraded service |
| Rate Limiter | Protect downstream services |

______________________________________________________________________

# Common Interview Questions

## Why do we need a Circuit Breaker?

A Circuit Breaker prevents repeated requests to an unhealthy dependency, reducing resource exhaustion and avoiding
cascading failures.

______________________________________________________________________

## What is the difference between Timeout and Circuit Breaker?

A timeout limits how long an individual request waits. A Circuit Breaker observes repeated failures over time and
temporarily stops sending requests to the failing service.

______________________________________________________________________

## Why use Exponential Backoff?

Immediate retries can overload an already unhealthy service. Exponential backoff spaces retries over increasing
intervals, giving the service time to recover.

______________________________________________________________________

## Why add Jitter?

If every client retries simultaneously, the downstream service can experience another traffic spike. Jitter randomizes
retry timing to spread the load.

______________________________________________________________________

## What is the Bulkhead Pattern?

Bulkheads isolate resources so failures in one component do not exhaust the resources needed by other components.

______________________________________________________________________

# Common Mistakes

## Infinite Retries

Always

limit

retry attempts.

______________________________________________________________________

## Retrying Validation Errors

Only retry

transient failures.

______________________________________________________________________

## No Timeouts

Every network call

should have

a timeout.

______________________________________________________________________

## Shared Thread Pools

Isolate

critical services

using

bulkheads.

______________________________________________________________________

## No Monitoring

Track

circuit states,

timeouts,

and fallback usage.

______________________________________________________________________

# Best Practices

✅ Configure reasonable timeouts.

✅ Retry only transient failures.

✅ Use exponential backoff with jitter.

✅ Protect dependencies using Circuit Breakers.

✅ Isolate workloads with Bulkheads.

✅ Implement graceful degradation.

✅ Monitor resilience metrics continuously.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the biggest problem a Circuit Breaker solves?

### Answer

It prevents cascading failures by quickly rejecting requests to unhealthy downstream services instead of allowing every
request to wait for timeouts and consume valuable resources.

______________________________________________________________________

## Question

Why shouldn't retries be unlimited?

### Answer

Unlimited retries can overload an already failing service, increase latency, waste resources, and amplify outages. Retry
limits with exponential backoff are much safer.

______________________________________________________________________

## Question

When should you use a fallback?

### Answer

Fallbacks are appropriate when partial functionality is acceptable, such as serving cached data, popular
recommendations, or temporarily disabling non-critical features while keeping the application usable.

______________________________________________________________________

# Practice Exercise

Design

a resilient

Payment Service.

Explain

1. Timeouts
1. Retry policy
1. Exponential backoff
1. Jitter
1. Circuit Breaker
1. Bulkhead
1. Queue usage
1. Fallback strategy
1. Monitoring
1. Failure recovery

Then explain

how your design

handles

- Payment gateway outage
- Slow database
- Network latency
- Notification failure
- Traffic spikes

______________________________________________________________________

# Summary

Circuit Breakers and resilience patterns are essential for modern distributed systems because failures are inevitable.

A strong solution should demonstrate

- Timeouts
- Retries
- Exponential backoff
- Jitter
- Circuit Breakers
- Bulkheads
- Queues
- Fallbacks
- Graceful degradation
- Monitoring
- Trade-off analysis

Mastering these patterns prepares you for senior backend interviews involving microservices, cloud-native systems,
fintech platforms, and high-availability distributed architectures.

______________________________________________________________________

# Next

[40. Designing a Payment Gateway](40-design-payment-gateway.md)
