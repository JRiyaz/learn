# Complete HTTP Request Lifecycle Deep Dive

## 12. Request Routing and Traffic Management

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how production systems intelligently route requests between services and deployments, including traffic splitting, blue-green deployments, canary releases, retries, circuit breakers, failover, and request routing strategies.

______________________________________________________________________

# Introduction

In the previous chapter,

the API Gateway

found

the correct service.

Now

another question arises.

Suppose

there are

10 instances

of

User Service.

```
User Service

↓

10 Pods
```

Which one

should receive

the request?

What if

one version

is newer?

What if

one region

goes down?

This is where

Traffic Management

comes in.

______________________________________________________________________

# High Level Flow

```
Incoming Request

↓

Gateway

↓

Traffic Rules

↓

Healthy Instance

↓

FastAPI
```

Traffic

is no longer

random.

It is

controlled.

______________________________________________________________________

# Why Traffic Management?

Suppose

your application

has

```
Version 1

↓

Stable
```

and

```
Version 2

↓

New Release
```

Should

100%

of users

immediately

use

Version 2?

No.

Instead

```
95%

↓

Version 1
```

```
5%

↓

Version 2
```

______________________________________________________________________

# Request Routing

Routing

can happen

based on

```
URL

↓

Headers

↓

Cookies

↓

Region

↓

User ID

↓

Device

↓

Version
```

______________________________________________________________________

# Path Based Routing

Example

```
/users

↓

User Service
```

```
/orders

↓

Order Service
```

______________________________________________________________________

# Host Based Routing

```
api.company.com

↓

API Cluster
```

```
admin.company.com

↓

Admin Cluster
```

______________________________________________________________________

# Header Based Routing

Suppose

developers

send

```
X-Version: beta
```

Gateway

routes

only

those requests

to

```
Version 2
```

Everyone else

continues

using

Version 1.

______________________________________________________________________

# Cookie Based Routing

Useful

for

A/B Testing.

```
Cookie

experiment=A

↓

Cluster A
```

```
Cookie

experiment=B

↓

Cluster B
```

______________________________________________________________________

# Geographic Routing

Interview favorite.

Users

from

India

↓

Mumbai

Cluster

Users

from Europe

↓

Frankfurt

Cluster

Reduces

latency.

______________________________________________________________________

# Weighted Routing

Suppose

Version 2

is new.

```
95%

↓

Version 1
```

```
5%

↓

Version 2
```

Gradually increase

```
80 / 20

↓

50 / 50

↓

0 / 100
```

______________________________________________________________________

# Blue-Green Deployment

Interview favorite.

Two

identical

environments.

```
Blue

↓

Current Production
```

```
Green

↓

New Version
```

Traffic

switches

instantly.

```
Blue

↓

Green
```

Rollback

takes

seconds.

______________________________________________________________________

# Canary Deployment

Interview favorite.

Instead of

switching

everyone,

release

to

a few users.

```
1%

↓

5%

↓

20%

↓

50%

↓

100%
```

If

errors increase

rollback.

______________________________________________________________________

# Shadow Traffic

Advanced.

Real user requests

go to

Production.

Copies

of the same request

are also sent

to

the new version.

```
User

↓

Production

↓

Copy

↓

New Version
```

The user

never sees

the new version.

Useful

for testing.

______________________________________________________________________

# A/B Testing

Different users

see

different versions.

Example

```
Group A

↓

Old UI
```

```
Group B

↓

New UI
```

Business

compares

results.

______________________________________________________________________

# Retry Policy

Suppose

the request

fails.

Gateway

may retry.

```
Request

↓

Timeout

↓

Retry

↓

Success
```

Retries

should only

be used

for

safe operations.

______________________________________________________________________

# Idempotency

Interview favorite.

Retries

can create

duplicates.

Example

```
POST

Create Payment
```

Retrying

may charge

the customer

twice.

Solution

```
Idempotency Key
```

______________________________________________________________________

# Timeout

Never

wait forever.

Example

```
Timeout

3 Seconds
```

If exceeded

```
504

Gateway Timeout
```

______________________________________________________________________

# Circuit Breaker

Interview favorite.

Suppose

Payment Service

is failing.

Without

Circuit Breaker

```
Every Request

↓

30 Second Wait
```

With

Circuit Breaker

```
Failure Threshold

↓

Open Circuit

↓

Fail Immediately
```

Protects

the system.

______________________________________________________________________

# Circuit States

```
Closed

↓

Open

↓

Half Open

↓

Closed
```

______________________________________________________________________

# Bulkhead Pattern

Prevent

one service

from consuming

all resources.

Example

```
Payment

↓

Dedicated Thread Pool
```

```
Orders

↓

Dedicated Thread Pool
```

Failure

doesn't spread.

______________________________________________________________________

# Failover

Suppose

Mumbai

goes down.

Traffic

automatically moves

to

Singapore.

```
Mumbai

↓

Unavailable

↓

Singapore
```

______________________________________________________________________

# Multi Region Routing

```
India

↓

Mumbai
```

```
Germany

↓

Frankfurt
```

```
USA

↓

Virginia
```

Improves

availability

and

latency.

______________________________________________________________________

# Session Affinity

Sometimes

requests

must reach

the same server.

```
User

↓

Server A

↓

Server A

↓

Server A
```

Usually

avoided

using

JWT

or

Redis.

______________________________________________________________________

# Request Mirroring

Production request

is copied

to

another environment.

```
Production

↓

Mirror

↓

Testing
```

Useful

for

performance testing.

______________________________________________________________________

# Adaptive Routing

Modern systems

can route

based on

```
Latency

↓

CPU

↓

Memory

↓

Errors
```

Fastest service

receives

the request.

______________________________________________________________________

# Service Degradation

Suppose

Recommendation Service

fails.

Instead of

failing

the whole request,

return

```
Products

↓

Without Recommendations
```

Graceful degradation.

______________________________________________________________________

# What Happens Internally?

```
Gateway

↓

Routing Rules

↓

Traffic Policies

↓

Health Check

↓

Load Balancing

↓

Retry Policy

↓

Circuit Breaker

↓

Backend
```

Everything

happens

before

FastAPI

receives

the request.

______________________________________________________________________

# Popular Technologies

Traffic Management

```
Istio

↓

Envoy

↓

Linkerd

↓

NGINX

↓

AWS ALB

↓

Traefik
```

______________________________________________________________________

# Common Interview Questions

## What is the difference between Blue-Green and Canary deployments?

Blue-Green switches all traffic from one environment to another instantly. Canary gradually shifts traffic to the new
version while monitoring its health.

______________________________________________________________________

## What is Shadow Traffic?

Production requests are copied to a new service without affecting users. Responses from the shadow service are ignored
and used only for testing.

______________________________________________________________________

## Why shouldn't POST requests always be retried?

POST requests may create duplicate resources or repeat side effects. Safe retries require idempotency mechanisms.

______________________________________________________________________

## What is a Circuit Breaker?

A Circuit Breaker temporarily stops sending requests to an unhealthy service after repeated failures, allowing the
system to fail fast and recover gracefully.

______________________________________________________________________

## What is Bulkhead Isolation?

Bulkhead Isolation separates resources between services so that failures in one service cannot exhaust resources
required by another.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain how modern production systems route traffic safely during deployments.

### Answer

Modern systems use traffic management policies implemented by API Gateways, Service Meshes, or Load Balancers. Requests
can be routed based on paths, headers, cookies, regions, or versions. Deployments commonly use blue-green or canary
strategies, while retries, circuit breakers, health checks, and failover mechanisms improve reliability. Traffic can
also be mirrored to new versions for testing without affecting users.

______________________________________________________________________

# Summary

Traffic management enables safe, scalable, and resilient deployments.

Key concepts include

- Path-based routing
- Header-based routing
- Geographic routing
- Weighted routing
- Blue-Green deployments
- Canary releases
- Shadow traffic
- Circuit breakers
- Retries
- Idempotency
- Failover
- Bulkhead isolation

At this point,

the request has reached the correct application instance and is ready to enter the **application server**.

From the next chapter onward, we move inside the backend itself and begin tracing **every internal step from the Linux
kernel to Uvicorn, ASGI, FastAPI, middleware, dependency injection, and finally your business logic**.

______________________________________________________________________

# Next

[13. Backend Request Lifecycle Overview](13-backend-request-lifecycle-overview.md)
