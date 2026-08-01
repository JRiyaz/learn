# Software Architecture - Part 44

# Service Discovery

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Service Discovery is
- Why Service Discovery exists
- Static vs Dynamic Service Discovery
- Client-Side Discovery
- Server-Side Discovery
- Service Registry
- Health Checks
- FastAPI examples
- Kubernetes examples
- Service Discovery vs Load Balancer
- When NOT to use Service Discovery

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

contains

multiple instances

of

Book Service.

```text id="sd4401"
Book Service #1

Book Service #2

Book Service #3
```

Question.

How does

Payment Service

know

which instance

to call?

Hardcoding

IP addresses

doesn't work.

Containers

start,

stop,

and restart

all the time.

We need

a better solution.

______________________________________________________________________

# The Problem

Suppose

Book Service

runs on

```text id="sd4402"
10.0.0.12
```

Tomorrow,

the container

restarts.

Now,

it runs on

```text id="sd4403"
10.0.0.28
```

Every client

still tries

to call

the old address.

Requests fail.

______________________________________________________________________

# Another Problem

Suppose

Book Service

has

20 instances.

```text id="sd4404"
Book #1

Book #2

Book #3

...

Book #20
```

How do clients

know

which instance

is healthy?

Which one

has capacity?

Which one

should receive

the next request?

______________________________________________________________________

# The Idea

Instead of

hardcoding

service addresses,

maintain

a central registry

of

available services.

Services

register themselves.

Clients

discover them.

______________________________________________________________________

# What is Service Discovery?

**Service Discovery**

is a mechanism

that enables

services

to locate

and communicate

with

other services

dynamically,

without

hardcoded addresses.

______________________________________________________________________

# Architecture

```text id="sd4405"
Book Service

↓

Service Registry

↑

Payment Service
```

Book Service

registers itself.

Payment Service

asks

the registry

where

Book Service

is running.

______________________________________________________________________

# Service Registry

A **Service Registry**

stores

information

about

running services.

Example

| Service | Address |
| ------------ | --------- |
| Book | 10.0.0.12 |
| Payment | 10.0.0.18 |
| Notification | 10.0.0.25 |

Services

join

and leave

the registry

automatically.

______________________________________________________________________

# Registration Flow

When

Book Service

starts,

it performs

```text id="sd4406"
Book Service

↓

Register

↓

Service Registry
```

Now,

other services

can discover it.

______________________________________________________________________

# Health Checks

Suppose

Book Service

crashes.

The registry

must know.

Health checks

periodically verify

that

services

are alive.

```text id="sd4407"
Health Check

↓

Healthy

↓

Keep Registered
```

or

```text id="sd4408"
Health Check

↓

Failed

↓

Remove Service
```

Unhealthy instances

stop receiving traffic.

______________________________________________________________________

# Static Discovery

Old systems

often use

configuration files.

Example

```text id="sd4409"
book-service:

10.0.0.12
```

Problems:

❌ Manual updates

❌ Doesn't scale

❌ Doesn't handle failures

______________________________________________________________________

# Dynamic Discovery

Modern systems

use

automatic registration.

Services

start.

Register.

Become discoverable.

When

they stop,

they disappear

from

the registry.

______________________________________________________________________

# Client-Side Discovery

In this model,

the client

queries

the registry.

```text id="sd4410"
Payment Service

↓

Service Registry

↓

Book Instance

↓

Book Service
```

The client

chooses

which instance

to call.

Popular examples:

- Netflix Eureka
- Consul

______________________________________________________________________

# Server-Side Discovery

Here,

the client

calls

a Load Balancer.

```text id="sd4411"
Payment Service

↓

Load Balancer

↓

Service Registry

↓

Book Service
```

The client

doesn't know

about

individual instances.

Kubernetes

uses

this model.

______________________________________________________________________

# Kubernetes Example

Suppose

Book Service

has

five Pods.

```text id="sd4412"
Pod 1

Pod 2

Pod 3

Pod 4

Pod 5
```

Clients

call

only

the Kubernetes Service.

Kubernetes

automatically

routes

traffic

to

healthy Pods.

Developers

rarely need

to know

individual Pod IPs.

______________________________________________________________________

# FastAPI Example

Suppose

Book Service

runs

as

multiple

FastAPI containers.

Instead of

calling

```text id="sd4413"
http://10.0.0.12
```

another service

calls

```text id="sd4414"
http://book-service
```

The platform

resolves

the actual destination.

______________________________________________________________________

# Cloud Example

Cloud providers

offer

managed discovery.

Examples:

- AWS Cloud Map
- Azure Service Discovery
- Google Cloud Service Directory

Applications

discover services

using names,

not

IP addresses.

______________________________________________________________________

# DNS-Based Discovery

Sometimes,

DNS

acts

as

the Service Registry.

Example

```text id="sd4415"
book-service.internal
```

DNS

returns

healthy instances.

Many cloud platforms

support

this approach.

______________________________________________________________________

# Service Discovery vs Load Balancer

Interview favorite.

| Service Discovery | Load Balancer |
| ------------------------- | --------------------------- |
| Finds services | Distributes traffic |
| Knows available instances | Chooses request destination |
| Registry | Traffic manager |

Often,

they work

together.

______________________________________________________________________

# Service Discovery vs API Gateway

| Service Discovery | API Gateway |
| ------------------------------ | --------------------------- |
| Internal service communication | External client entry point |
| Used by services | Used by clients |

Microservices

typically use

both.

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

contains

multiple

Inference Services.

```text id="sd4416"
Inference Pod 1

Inference Pod 2

Inference Pod 3
```

The API Gateway

asks

Service Discovery

for

healthy inference instances,

then

routes

the request.

As new GPUs

come online,

they register

automatically.

______________________________________________________________________

# Real Backend Example

Suppose

Recommendation Service

scales

from

2 instances

to

20 instances.

Without

Service Discovery,

every caller

must update

its configuration.

With

Service Discovery,

new instances

register automatically,

and

traffic

starts flowing

immediately.

______________________________________________________________________

# Popular Technologies

Common

Service Discovery solutions:

- Kubernetes Services
- Consul
- Netflix Eureka
- Apache ZooKeeper
- etcd

Kubernetes

is

the most common

choice today

for cloud-native systems.

______________________________________________________________________

# Benefits

Service Discovery provides:

✅ Dynamic scaling

✅ Automatic failover

✅ No hardcoded IP addresses

✅ Easier deployments

✅ Better resilience

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Additional infrastructure

❌ Registry management

❌ Network complexity

❌ Health check configuration

______________________________________________________________________

# Real Company Example

Ride-sharing platforms

continuously

add

and remove

service instances

based on demand.

Service Discovery

ensures

that

new instances

start receiving traffic

immediately,

while

failed instances

are removed

without manual intervention.

______________________________________________________________________

# When NOT to Use Service Discovery

Don't use

Service Discovery

for:

- Single-server applications
- Small monoliths
- Applications

with

fixed infrastructure

and

no dynamic scaling.

Simple

DNS

or configuration

may be enough.

______________________________________________________________________

# Best Practices

✅ Use health checks.

✅ Register services automatically.

✅ Avoid hardcoded IP addresses.

✅ Prefer service names over network addresses.

______________________________________________________________________

# Common Mistakes

### Hardcoding Addresses

Containers

and Pods

change

their IPs

frequently.

Always

discover services

dynamically.

______________________________________________________________________

### Ignoring Health Checks

A service

that is

registered

but unhealthy

should not

receive traffic.

______________________________________________________________________

### Treating the Registry as a Database

The registry

stores

service locations,

not

business data.

______________________________________________________________________

### No Retry Logic

Discovery

finds services.

Transient

network failures

may still occur.

Combine

Service Discovery

with

timeouts,

retries,

and

Circuit Breakers.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Service Discovery, and why is it important in microservices?

Service Discovery is a mechanism that allows services to locate one another dynamically without relying on hardcoded
network addresses. Services register themselves with a Service Registry when they start, and clients or load balancers
query the registry to discover healthy service instances. This enables automatic scaling, failover, and infrastructure
changes without requiring application reconfiguration. Modern platforms such as Kubernetes provide built-in Service
Discovery, making it a fundamental component of cloud-native microservice architectures.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Service Discovery is
- Service Registry
- Health Checks
- Static vs Dynamic Discovery
- Client-Side vs Server-Side Discovery
- Kubernetes example
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 Distributed Systems Progress

You now understand six major production patterns:

- ✅ API Gateway
- ✅ Saga Pattern
- ✅ Outbox Pattern
- ✅ Circuit Breaker
- ✅ Bulkhead Pattern
- ✅ Service Discovery

These patterns are commonly used together in modern Kubernetes-based microservice platforms.

______________________________________________________________________

# What's Next

[Distributed Transactions](45-distributed-transactions.md)
