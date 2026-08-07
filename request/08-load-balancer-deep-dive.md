# Complete HTTP Request Lifecycle Deep Dive

## 08. Load Balancer Deep Dive

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand why Load Balancers are needed, how they distribute traffic, how health checks work, different load balancing algorithms, Layer 4 vs Layer 7 Load Balancers, sticky sessions, SSL termination, and what actually happens internally.

______________________________________________________________________

# Introduction

The request

has successfully

passed

the

- Browser
- DNS
- TCP
- TLS
- CDN
- WAF

Now

it reaches

your infrastructure.

Suppose

your application

runs

on

one server.

```
                Client

                   │

                   ▼

            FastAPI Server
```

Works fine.

Until

10,000 users

arrive.

______________________________________________________________________

# The Problem

One server

has limited

- CPU
- Memory
- Network
- Disk

Eventually

it becomes

overloaded.

```
CPU

100%
```

```
Memory

95%
```

```
Requests

Timeout
```

Users

start seeing

```
503 Service Unavailable
```

______________________________________________________________________

# The Solution

Instead of

one server,

run

multiple servers.

```
FastAPI-1

FastAPI-2

FastAPI-3

FastAPI-4
```

But now

another problem.

```
Who decides

which server

handles

the request?
```

Answer

```
Load Balancer
```

______________________________________________________________________

# What Is A Load Balancer?

A Load Balancer

distributes

incoming traffic

across

multiple servers.

Instead of

```
Client

↓

Server 1
```

we get

```
             Client

                │

                ▼

         Load Balancer

      ┌───────┼────────┐

      ▼       ▼        ▼

 Server1   Server2   Server3
```

______________________________________________________________________

# Why Do We Need It?

Benefits

- High Availability
- Scalability
- Fault Tolerance
- Better Resource Usage
- Zero Downtime Deployments

______________________________________________________________________

# Real Production Architecture

```
Internet

↓

CDN

↓

WAF

↓

Load Balancer

↓

Nginx

↓

FastAPI

↓

Redis

↓

PostgreSQL
```

______________________________________________________________________

# What Happens Internally?

```
Incoming Request

↓

Accept TCP Connection

↓

Health Check

↓

Choose Server

↓

Forward Request

↓

Receive Response

↓

Return To Client
```

Notice

the Load Balancer

usually

doesn't execute

your business logic.

It simply

routes traffic.

______________________________________________________________________

# Step 1

# Receive Request

The client

connects to

```
api.company.com
```

DNS

returns

the IP

of

the Load Balancer,

not

your backend.

Example

```
api.company.com

↓

18.215.xxx.xxx

(ALB)
```

The browser

doesn't know

your backend servers

exist.

______________________________________________________________________

# Step 2

# Accept Connection

The Load Balancer

accepts

the TCP connection.

If

HTTPS

is enabled,

it may also

terminate

TLS.

```
Browser

↓

HTTPS

↓

Load Balancer

↓

HTTP

↓

Backend
```

This is called

```
SSL/TLS Termination
```

______________________________________________________________________

# Why TLS Termination?

Interview favorite.

Without

TLS termination,

every backend

must

decrypt

HTTPS.

Example

```
FastAPI-1

↓

TLS

↓

CPU
```

```
FastAPI-2

↓

TLS

↓

CPU
```

```
FastAPI-3

↓

TLS

↓

CPU
```

Instead,

only

the Load Balancer

performs

TLS decryption.

Benefits

- Lower CPU usage
- Easier certificate management
- Centralized security

______________________________________________________________________

# Step 3

# Health Check

Before

sending

the request,

the Load Balancer

checks

which servers

are healthy.

Example

```
GET /health
```

Response

```
200 OK
```

Healthy.

______________________________________________________________________

Suppose

```
Server 2

↓

500 Error
```

or

```
Timeout
```

The Load Balancer

marks it

as

Unhealthy.

Future requests

are not sent

to

Server 2.

______________________________________________________________________

# Health Check Flow

```
Load Balancer

↓

FastAPI-1

↓

200 OK

Healthy
```

```
Load Balancer

↓

FastAPI-2

↓

Timeout

Unhealthy
```

______________________________________________________________________

# Step 4

# Select Backend

Now

the Load Balancer

chooses

one server.

Example

```
Server1

↓

Server2

↓

Server3
```

Selection depends

on

the balancing algorithm.

______________________________________________________________________

# Round Robin

Interview favorite.

Simplest algorithm.

```
Request1

↓

Server1
```

```
Request2

↓

Server2
```

```
Request3

↓

Server3
```

```
Request4

↓

Server1
```

Even distribution.

______________________________________________________________________

# Weighted Round Robin

Suppose

Server3

has

twice

the CPU.

```
Server1

Weight 1
```

```
Server2

Weight 1
```

```
Server3

Weight 2
```

Traffic

```
1

↓

2

↓

3

↓

3
```

______________________________________________________________________

# Least Connections

Interview favorite.

Instead of

counting requests,

count

active connections.

Example

```
Server1

10 Connections
```

```
Server2

2 Connections
```

New request

↓

Server2

______________________________________________________________________

Useful

when

request duration

varies.

______________________________________________________________________

# Least Response Time

Some Load Balancers

choose

the fastest server.

Example

```
Server1

20 ms
```

```
Server2

80 ms
```

↓

Server1

______________________________________________________________________

# IP Hash

The same client IP

always goes

to

the same server.

Useful

for

session-based applications.

______________________________________________________________________

# Sticky Sessions

Interview favorite.

Suppose

the user logs in.

Session

is stored

inside

FastAPI-2.

Next request

must also

reach

FastAPI-2.

```
User

↓

Server2

↓

Server2

↓

Server2
```

This is called

```
Sticky Session
```

______________________________________________________________________

# Problems With Sticky Sessions

Suppose

Server2

fails.

User

loses

their session.

Modern systems

prefer

shared storage.

Examples

- Redis
- Database
- JWT

Instead of

server memory.

______________________________________________________________________

# Stateless Applications

Modern microservices

are usually

stateless.

```
Request1

↓

Server1
```

```
Request2

↓

Server3
```

No problem.

Session

is stored

in

JWT

or

Redis.

______________________________________________________________________

# Connection Pooling

The Load Balancer

may reuse

existing

backend connections.

Instead of

opening

new TCP connections

for

every request.

Benefits

- Lower latency
- Better throughput

______________________________________________________________________

# Layer 4 Load Balancer

Interview favorite.

Operates

at

TCP level.

Knows

```
IP

↓

Port
```

Does NOT

understand

HTTP.

Examples

AWS NLB.

______________________________________________________________________

# Layer 7 Load Balancer

Interview favorite.

Operates

at

HTTP level.

Understands

```
URL

Headers

Cookies

Host

Path
```

Can route

based on

HTTP information.

Examples

AWS ALB,

Nginx,

Envoy.

______________________________________________________________________

# Example

Suppose

```
/users
```

goes to

User Service.

```
/payments
```

goes to

Payment Service.

```
Incoming

↓

/users

↓

User Cluster
```

```
Incoming

↓

/payments

↓

Payment Cluster
```

Impossible

with

Layer 4.

______________________________________________________________________

# Path Based Routing

Example

```
api.company.com/users

↓

User Service
```

```
api.company.com/orders

↓

Order Service
```

______________________________________________________________________

# Host Based Routing

Example

```
admin.company.com

↓

Admin Cluster
```

```
api.company.com

↓

API Cluster
```

______________________________________________________________________

# SSL Offloading

Interview favorite.

Load Balancer

decrypts

HTTPS

then forwards

plain HTTP

inside

the trusted network.

Sometimes

backend communication

also uses

HTTPS.

Depends

on

security requirements.

______________________________________________________________________

# Cross-Zone Load Balancing

Suppose

servers exist

in

```
Zone A

Zone B

Zone C
```

Traffic

can be

distributed

across

all zones.

Provides

high availability.

______________________________________________________________________

# Autoscaling

Suppose

traffic increases.

```
100 Users

↓

2 Servers
```

```
10,000 Users

↓

20 Servers
```

The Load Balancer

automatically

starts using

new servers.

______________________________________________________________________

# Draining Connections

Interview favorite.

Suppose

Server2

needs

maintenance.

Don't immediately

disconnect users.

Instead

```
Stop New Requests

↓

Finish Existing Requests

↓

Remove Server
```

Called

```
Connection Draining
```

______________________________________________________________________

# Blue-Green Deployment

Load Balancer

makes this easy.

```
Blue

↓

Current
```

```
Green

↓

New Version
```

Switch traffic

instantly.

Rollback

is simple.

______________________________________________________________________

# Canary Deployment

Traffic

gradually moves.

```
5%

↓

20%

↓

50%

↓

100%
```

The Load Balancer

controls

traffic distribution.

______________________________________________________________________

# What Happens Inside The Kernel?

When

the Load Balancer

receives

a TCP packet

```
NIC

↓

Kernel

↓

Socket

↓

Load Balancer Process

↓

Routing Decision

↓

Backend Socket

↓

Backend Server
```

Notice

the kernel

handles

the low-level

networking.

______________________________________________________________________

# Common Failures

## Backend Crash

Health check fails.

Traffic

is removed.

______________________________________________________________________

## Slow Backend

Least Response Time

may stop

sending traffic

there.

______________________________________________________________________

## Entire Zone Down

Traffic

moves

to

another zone.

______________________________________________________________________

## Load Balancer Failure

Production systems

deploy

multiple

Load Balancers.

______________________________________________________________________

# Common Attacks

## SYN Flood

Millions

of TCP connections.

Mitigation

- SYN Cookies
- Rate Limiting

______________________________________________________________________

## Slowloris

Attacker

opens

connections

very slowly,

keeping them alive.

Mitigation

Connection timeout.

______________________________________________________________________

## HTTP Flood

Millions

of HTTP requests.

Mitigation

Rate limiting,

WAF,

CDN.

______________________________________________________________________

# Popular Technologies

Cloud

```
AWS ALB

AWS NLB

Azure Load Balancer

Google Cloud Load Balancer
```

Self Hosted

```
NGINX

HAProxy

Envoy

Traefik
```

Hardware

```
F5 BIG-IP

Citrix ADC
```

______________________________________________________________________

# Technologies Used

| Purpose | Technologies |
|----------|--------------|
| Layer 4 | AWS NLB, HAProxy |
| Layer 7 | AWS ALB, NGINX, Envoy, Traefik |
| Health Checks | HTTP, TCP, gRPC |
| SSL Termination | OpenSSL, BoringSSL |
| Service Discovery | Kubernetes, Consul |

______________________________________________________________________

# Common Interview Questions

## Why use a Load Balancer?

A Load Balancer distributes incoming traffic across multiple backend servers, improving availability, scalability, fault
tolerance, and resource utilization.

______________________________________________________________________

## What is the difference between Layer 4 and Layer 7 Load Balancers?

A Layer 4 Load Balancer routes traffic using IP addresses and ports. A Layer 7 Load Balancer understands HTTP and can
route based on URLs, headers, cookies, hostnames, and request paths.

______________________________________________________________________

## What are Sticky Sessions?

Sticky Sessions ensure requests from the same client are routed to the same backend server. They are useful for stateful
applications but are generally avoided in modern stateless architectures.

______________________________________________________________________

## Why terminate TLS at the Load Balancer?

Centralizing TLS termination reduces CPU usage on backend servers, simplifies certificate management, and allows backend
services to focus on application logic.

______________________________________________________________________

## Why are health checks important?

Health checks prevent traffic from being routed to unhealthy servers, improving application reliability and user
experience.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when a request reaches a Load Balancer.

### Answer

The Load Balancer accepts the incoming TCP connection, optionally terminates TLS, performs health checks to identify
healthy backend servers, selects a target server using a routing algorithm such as Round Robin or Least Connections,
forwards the request to that server, receives the response, and returns it to the client. Throughout this process, it
monitors backend health and can automatically stop sending traffic to unhealthy instances.

______________________________________________________________________

# Summary

A Load Balancer is one of the most important infrastructure components in modern distributed systems.

Key concepts include

- Layer 4 vs Layer 7
- Health Checks
- Round Robin
- Least Connections
- Sticky Sessions
- TLS Termination
- Connection Draining
- Blue-Green Deployments
- Canary Releases
- Autoscaling
- High Availability

The Load Balancer decides **which server** should receive the request.

Once the backend server is selected, the request is typically forwarded to a **Reverse Proxy**, which performs another
layer of intelligent request processing before your application receives it.

______________________________________________________________________

# Next

[09. Forward Proxy vs Reverse Proxy](09-forward-proxy-vs-reverse-proxy.md)
