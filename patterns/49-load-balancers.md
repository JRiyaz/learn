# System Design - Part 49

# Load Balancers

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Load Balancer is
- Why Load Balancers exist
- Types of Load Balancers
- Layer 4 vs Layer 7 Load Balancing
- Load Balancing Algorithms
- Health Checks
- Sticky Sessions
- Reverse Proxy vs Load Balancer
- FastAPI examples
- Kubernetes examples
- Common interview questions

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

becomes popular.

Instead of

100 users,

it now has

10 million users.

Originally,

the architecture

looked like this.

```text id="lb4901"
Users

↓

Application Server
```

Everything

worked.

Until

traffic increased.

______________________________________________________________________

# The Problem

Suppose

50,000 users

send requests

at the same time.

```text id="lb4902"
Users

↓

Server
```

One server

has

limited:

- CPU
- Memory
- Network
- Threads

Eventually,

the server

becomes overloaded.

Requests

become slower.

Some requests

start failing.

______________________________________________________________________

# Scaling Vertically

One solution

is

to upgrade

the server.

```text id="lb4903"
4 CPU

↓

16 CPU
```

```text id="lb4904"
16 GB RAM

↓

64 GB RAM
```

This is called

**Vertical Scaling**.

It helps,

but

only

up to a limit.

Eventually,

you cannot buy

a larger machine.

______________________________________________________________________

# Scaling Horizontally

Instead of

one large server,

use

multiple servers.

```text id="lb4905"
Server 1

Server 2

Server 3

Server 4
```

Now,

a new question arises.

How do users

know

which server

to send requests to?

______________________________________________________________________

# The Idea

Place

one component

in front

of

all servers.

That component

distributes

incoming traffic.

This is

the

**Load Balancer**.

______________________________________________________________________

# What is a Load Balancer?

A **Load Balancer**

is a component

that distributes

incoming requests

across

multiple backend servers,

improving:

- Availability
- Scalability
- Reliability

______________________________________________________________________

# Architecture

```text id="lb4906"
Users

↓

Load Balancer

↓

Server 1

Server 2

Server 3
```

Clients

see

only

one endpoint.

The Load Balancer

chooses

the backend server.

______________________________________________________________________

# Why Use a Load Balancer?

Without

a Load Balancer,

one server

may receive

all traffic.

Other servers

remain idle.

With

a Load Balancer,

traffic

is distributed

more evenly.

______________________________________________________________________

# Layer 4 Load Balancer

Operates

at

the

**Transport Layer**

(TCP/UDP).

It routes

connections

without

understanding

HTTP requests.

Example:

- TCP Load Balancing
- Database connections

Popular examples:

- AWS Network Load Balancer
- HAProxy (TCP mode)

______________________________________________________________________

# Layer 7 Load Balancer

Operates

at

the

**Application Layer**

(HTTP/HTTPS).

It understands:

- URLs
- Headers
- Cookies
- HTTP Methods

Example

```text id="lb4907"
/books

↓

Book Service
```

```text id="lb4908"
/payments

↓

Payment Service
```

Popular examples:

- NGINX
- Envoy
- Traefik
- AWS Application Load Balancer

______________________________________________________________________

# Layer 4 vs Layer 7

| Layer 4 | Layer 7 |
| ------------------------ | ------------------------ |
| TCP/UDP | HTTP/HTTPS |
| Faster | More intelligent routing |
| Doesn't inspect requests | Can inspect requests |

Choose

based on

application needs.

______________________________________________________________________

# Load Balancing Algorithms

The Load Balancer

must decide

where

to send

each request.

Several algorithms

exist.

______________________________________________________________________

# Round Robin

Requests

are distributed

one by one.

```text id="lb4909"
Request 1

↓

Server 1
```

```text id="lb4910"
Request 2

↓

Server 2
```

```text id="lb4911"
Request 3

↓

Server 3
```

Simple.

Fair.

Very common.

______________________________________________________________________

# Least Connections

The Load Balancer

chooses

the server

with

the fewest

active connections.

Useful

when

requests

have

different durations.

______________________________________________________________________

# Weighted Round Robin

Suppose

one server

is twice

as powerful.

Assign

weights.

```text id="lb4912"
Server 1

Weight = 2
```

```text id="lb4913"
Server 2

Weight = 1
```

Server 1

receives

twice

as much traffic.

______________________________________________________________________

# IP Hash

The client's

IP address

determines

the server.

The same client

usually reaches

the same backend.

Useful

for

session affinity.

______________________________________________________________________

# Health Checks

Suppose

Server 2

crashes.

Without

health checks,

the Load Balancer

continues

sending traffic.

Users

receive errors.

Instead,

the Load Balancer

periodically checks

server health.

```text id="lb4914"
Server

↓

Health Check

↓

Healthy
```

or

```text id="lb4915"
Unhealthy

↓

Remove
```

Only

healthy servers

receive traffic.

______________________________________________________________________

# Sticky Sessions

Some applications

store

session data

in memory.

Example

```text id="lb4916"
Login

↓

Server 1
```

Later,

the same user

should return

to

Server 1.

This is called

**Sticky Sessions**

or

**Session Affinity**.

______________________________________________________________________

# Why Sticky Sessions Can Be Problematic

Suppose

Server 1

fails.

All sessions

stored

in memory

are lost.

Modern systems

prefer

shared storage

or

distributed caches

such as Redis

instead of

Sticky Sessions.

______________________________________________________________________

# Reverse Proxy vs Load Balancer

Interview favorite.

| Reverse Proxy | Load Balancer |
| ---------------------------------- | ------------------------------------------ |
| Usually fronts one or more servers | Distributes traffic |
| Can cache, compress, terminate TLS | Focuses on traffic distribution |
| NGINX can do both | Often combined with reverse proxy features |

Many products,

such as NGINX,

perform

both roles.

______________________________________________________________________

# FastAPI Example

Suppose

you run

four

FastAPI instances.

```text id="lb4917"
FastAPI #1

FastAPI #2

FastAPI #3

FastAPI #4
```

The Load Balancer

distributes

incoming requests

among them.

The application

doesn't need

to know

which instance

handled

the request.

______________________________________________________________________

# Kubernetes Example

Suppose

your deployment

has

five Pods.

```text id="lb4918"
Pod 1

Pod 2

Pod 3

Pod 4

Pod 5
```

A Kubernetes Service

acts

as

an internal

Load Balancer,

routing traffic

only

to

healthy Pods.

______________________________________________________________________

# Cloud Example

Cloud providers

offer

managed

Load Balancers.

Examples:

- AWS Application Load Balancer (ALB)
- AWS Network Load Balancer (NLB)
- Azure Load Balancer
- Google Cloud Load Balancer

These services

automatically

scale

and

perform

health checks.

______________________________________________________________________

# AI/ML Example

Suppose

your application

has

10 LLM inference servers.

Some servers

have GPUs.

Others

have CPUs.

A Load Balancer

can route

GPU-intensive requests

to GPU nodes

and

lighter requests

to CPU nodes,

depending

on routing rules.

______________________________________________________________________

# Benefits

Load Balancers provide:

✅ Horizontal scaling

✅ High availability

✅ Fault tolerance

✅ Better resource utilization

✅ Zero-downtime deployments

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Additional infrastructure

❌ Network hop

❌ Configuration complexity

❌ Potential bottleneck

if

not deployed

redundantly.

______________________________________________________________________

# Real Company Example

A video streaming platform

may run

thousands

of backend servers.

Users

connect

to

a Load Balancer,

which routes

requests

to

healthy,

least-loaded servers,

ensuring

continuous availability

even

when

individual servers fail.

______________________________________________________________________

# When NOT to Use Load Balancers

Don't introduce

a Load Balancer

for:

- Single-server applications
- Local development
- Very small internal tools

As traffic grows,

they become

an essential component.

______________________________________________________________________

# Best Practices

✅ Enable health checks.

✅ Use multiple Load Balancers for redundancy.

✅ Prefer stateless applications.

✅ Monitor latency and backend utilization.

______________________________________________________________________

# Common Mistakes

### Single Load Balancer

One Load Balancer

can become

a single point

of failure.

Deploy

multiple instances

or

use

managed cloud services.

______________________________________________________________________

### Sticky Sessions Everywhere

Prefer

stateless services

and

shared session storage.

______________________________________________________________________

### Ignoring Health Checks

A server

that has crashed

should stop

receiving traffic

immediately.

______________________________________________________________________

### Wrong Algorithm

Choose

the balancing algorithm

based on

traffic characteristics,

not

personal preference.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Load Balancer, and how does it improve scalability?

A Load Balancer is a component that distributes incoming client requests across multiple backend servers. It improves
scalability by enabling horizontal scaling, where additional servers can be added to handle increased traffic. It also
improves availability by routing requests only to healthy servers and preventing any single server from becoming
overloaded. Modern Load Balancers support health checks, intelligent routing algorithms, TLS termination, and
integration with cloud platforms and Kubernetes.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a Load Balancer is
- Vertical vs Horizontal Scaling
- Layer 4 vs Layer 7
- Load Balancing Algorithms
- Health Checks
- Sticky Sessions
- Kubernetes example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand the first major building block of scalable systems:

- ✅ Load Balancers

Next, we'll learn another critical component that almost every high-scale system uses:

> **Caching**, which dramatically reduces latency and database load.

______________________________________________________________________

# What's Next

[Caching](50-caching.md)
