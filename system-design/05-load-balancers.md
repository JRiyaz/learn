# Load Balancers

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand what Load Balancers are, why they are needed, how they work, and how to discuss them confidently in System Design interviews.

______________________________________________________________________

# Introduction

Imagine your application

has

one server.

```
Users

↓

Server
```

Everything works well

until

10 million users

arrive.

Now

every request

hits

the same machine.

Eventually

```
CPU

↑

Memory

↑

Network

↑

Response Time

↑

Crash
```

How do we solve this?

We don't buy

one gigantic server forever.

Instead,

we add

more servers.

But now

another question appears.

```
How do users know

which server

to connect to?
```

The answer is

```
Load Balancer
```

______________________________________________________________________

# What Is A Load Balancer?

A Load Balancer

is a component

that distributes

incoming requests

across multiple servers.

Instead of

```
Users

↓

Server
```

we get

```
           ┌──────────┐
Users ───► │ Load     │
           │ Balancer │
           └────┬─────┘
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
  Server A   Server B   Server C
```

Every request

first reaches

the Load Balancer.

The Load Balancer

decides

which server

should handle it.

______________________________________________________________________

# Why Do We Need A Load Balancer?

Without it

```
Users

↓

One Server

↓

Overloaded
```

With it

```
Users

↓

Load Balancer

↓

Multiple Servers

↓

Better Performance
```

Benefits

- Better scalability
- Better availability
- Higher throughput
- Fault tolerance
- Easier maintenance

______________________________________________________________________

# Real World Example

Imagine

three supermarket cashiers.

Without coordination,

everyone chooses

the first cashier.

One queue

becomes huge.

The other two

sit idle.

A manager

directs customers

to the shortest queue.

That manager

is the

Load Balancer.

______________________________________________________________________

# High-Level Architecture

```
                    Internet
                        │
                        ▼
                 ┌────────────┐
                 │    DNS     │
                 └─────┬──────┘
                       │
                       ▼
               ┌────────────────┐
               │ Load Balancer  │
               └─────┬──────────┘
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     App Server   App Server   App Server
          │          │          │
          └──────┬───┴──────────┘
                 ▼
             Database
```

______________________________________________________________________

# Load Balancer Responsibilities

A Load Balancer

does much more than

forward requests.

It also

- Distributes traffic
- Detects unhealthy servers
- Removes failed servers
- Supports SSL termination
- Supports sticky sessions
- Performs health checks
- Enables zero-downtime deployments

______________________________________________________________________

# Health Checks

Suppose

Server B

crashes.

```
           Load Balancer
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Server A   Server B   Server C
                ❌
```

The Load Balancer

detects

that Server B

is unhealthy.

New requests

are automatically

sent only to

A

and

C.

Users

may never notice

the failure.

______________________________________________________________________

# Health Check Example

Every

5 seconds

the Load Balancer

calls

```
GET /health
```

Healthy server

returns

```
200 OK
```

Failed server

returns

```
500

or

No Response
```

The server

is removed

from rotation.

______________________________________________________________________

# Load Balancing Algorithms

There isn't

one algorithm.

Different situations

require

different strategies.

______________________________________________________________________

# 1. Round Robin

Most common.

Requests

are distributed

one by one.

```
Request 1 → Server A

Request 2 → Server B

Request 3 → Server C

Request 4 → Server A

Request 5 → Server B
```

Advantages

- Very simple
- Fair distribution

Disadvantages

- Doesn't consider server load

______________________________________________________________________

# 2. Weighted Round Robin

Some servers

are more powerful.

Example

```
Server A

Weight = 4

Server B

Weight = 2

Server C

Weight = 1
```

Traffic

approximately becomes

```
A

A

A

A

B

B

C
```

Useful

when servers

have different capacities.

______________________________________________________________________

# 3. Least Connections

Instead of

counting requests,

count

active connections.

Example

```
Server A

250 Connections

Server B

20 Connections

Server C

60 Connections
```

Next request

goes to

Server B.

Useful

for long-lived connections.

______________________________________________________________________

# 4. Least Response Time

The Load Balancer

tracks

which server

responds fastest.

Future requests

prefer

that server.

Useful

when response times

vary significantly.

______________________________________________________________________

# 5. IP Hash

Client IP

determines

the server.

Example

```
192.168.1.10

↓

Server B
```

Same client

usually reaches

the same server.

Useful

for session affinity.

______________________________________________________________________

# Sticky Sessions (Session Affinity)

Suppose

users log in.

Session data

is stored

inside

Server A.

If the next request

goes to

Server B,

the session

is missing.

Problem.

Solution

Sticky Sessions.

```
User

↓

Always Server A
```

______________________________________________________________________

# Why Sticky Sessions Are Not Ideal

If Server A

fails,

the user's session

is lost.

Modern applications

prefer

storing sessions

in Redis

or

Databases.

Then

any server

can handle

the request.

Stateless applications

scale better.

______________________________________________________________________

# Stateless Architecture

Instead of

storing sessions

inside application servers,

store them

externally.

```
Users

↓

Load Balancer

↓

App Servers

↓

Redis

↓

Database
```

Now

every server

is identical.

______________________________________________________________________

# Layer 4 Load Balancer

Operates at

the Transport Layer.

Uses

- TCP
- UDP

Fast

because

it doesn't inspect

HTTP requests.

Examples

- AWS Network Load Balancer
- HAProxy (TCP mode)

______________________________________________________________________

# Layer 7 Load Balancer

Operates at

the Application Layer.

Understands

HTTP

HTTPS

Headers

Cookies

Paths

Example

```
/api/*

↓

Backend Cluster

```

```
/images/*

↓

Image Service
```

Much more intelligent.

Examples

- NGINX
- AWS Application Load Balancer
- Traefik

______________________________________________________________________

# SSL Termination

Normally

every application server

decrypts HTTPS.

Expensive.

Instead

```
HTTPS

↓

Load Balancer

↓

HTTP

↓

Application Servers
```

Benefits

- Less CPU usage
- Simpler server configuration
- Easier certificate management

______________________________________________________________________

# Reverse Proxy vs Load Balancer

Many people

confuse them.

Reverse Proxy

```
Client

↓

Reverse Proxy

↓

One

or

Many Servers
```

Primary goal

Hide backend servers.

Load Balancer

Primary goal

Distribute traffic.

NGINX

can do

both.

______________________________________________________________________

# Active-Active

```
Users

↓

Load Balancer

↓

Server A

+

Server B

+

Server C
```

All servers

serve traffic.

Most common.

______________________________________________________________________

# Active-Passive

```
Primary Server

↓

Handles Traffic
```

```
Backup Server

↓

Waits
```

If Primary fails,

Backup

takes over.

Common

in disaster recovery.

______________________________________________________________________

# Load Balancer Failure

What if

the Load Balancer

fails?

```
Users

↓

❌ Load Balancer
```

Entire application

becomes unavailable.

This is

a

Single Point Of Failure.

Solution

Use

multiple

Load Balancers.

```
          DNS
           │
   ┌───────┴────────┐
   ▼                ▼
Load Balancer   Load Balancer
      │                │
      └────────┬───────┘
               ▼
         Application Servers
```

______________________________________________________________________

# Cloud Load Balancers

Most companies

don't build

their own.

Common services

- AWS Application Load Balancer (ALB)
- AWS Network Load Balancer (NLB)
- Google Cloud Load Balancer
- Azure Load Balancer

Interviewers

care more

about concepts

than vendor-specific details.

______________________________________________________________________

# Load Balancer In Kubernetes

```
Internet

↓

LoadBalancer Service

↓

Ingress Controller

↓

Pods
```

We'll study

Kubernetes networking

later.

______________________________________________________________________

# Common Interview Questions

## Why can't DNS replace a Load Balancer?

DNS

doesn't know

server health,

active connections,

or response times.

Load Balancers

do.

______________________________________________________________________

## Can a Load Balancer improve availability?

Yes.

Failed servers

are removed automatically.

Traffic

continues

to healthy servers.

______________________________________________________________________

## Does a Load Balancer improve performance?

Yes.

By distributing traffic,

it prevents

individual servers

from becoming overloaded.

______________________________________________________________________

## What happens if one server crashes?

Health checks

detect failure.

The server

is removed

from rotation.

Users

are redirected

to healthy servers.

______________________________________________________________________

# Common Mistakes

## Believing Load Balancers Store Data

They don't.

They route traffic.

______________________________________________________________________

## Confusing Load Balancer With CDN

Load Balancer

distributes requests.

CDN

caches content.

Different responsibilities.

______________________________________________________________________

## Ignoring Health Checks

Health checks

are one of

the most important features.

______________________________________________________________________

## Using Sticky Sessions Everywhere

Modern cloud applications

prefer

stateless services

with shared session storage.

______________________________________________________________________

# Best Practices

✅ Keep application servers stateless.

✅ Enable health checks.

✅ Use Layer 7 for web applications.

✅ Use multiple Load Balancers for high availability.

✅ Store sessions in Redis instead of application memory.

______________________________________________________________________

# Interview Deep Dive

## Question

When would you choose Least Connections instead of Round Robin?

### Answer

Least Connections is better for workloads where requests take varying amounts of time, such as WebSocket connections or
long-running uploads. Round Robin assumes each request has a similar cost.

______________________________________________________________________

## Question

Why are stateless services preferred?

### Answer

Stateless services allow any application server to handle any request. This simplifies scaling, improves fault
tolerance, and avoids reliance on sticky sessions.

______________________________________________________________________

## Question

Is a Load Balancer always required?

### Answer

No. Small applications with a single server don't need one. As traffic grows and multiple servers are introduced, a Load
Balancer becomes essential for scalability and high availability.

______________________________________________________________________

# Practice Exercise

For each application,

explain

1. Why a Load Balancer is needed.
1. Which load-balancing algorithm you would choose.
1. Whether sticky sessions are appropriate.
1. How health checks should work.
1. Whether Layer 4 or Layer 7 is a better fit.

Applications

- WhatsApp
- Netflix
- Instagram
- Online Banking
- URL Shortener
- Food Delivery Platform

______________________________________________________________________

# Summary

Load Balancers are one of the most important components in distributed systems.

They

- Distribute traffic
- Improve scalability
- Increase availability
- Detect failed servers
- Enable zero-downtime deployments
- Remove single points of failure

Understanding how they work—and more importantly, **when** and **why** to use them—is fundamental to succeeding in
System Design interviews.

______________________________________________________________________

# Next

[DNS (Domain Name System)](06-dns.md)
