# System Design - Part 87

# Nginx System Design (How Nginx Works Internally)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Nginx was created
- Nginx Architecture
- Master & Worker Processes
- Event-Driven Architecture
- epoll / kqueue
- Reverse Proxy
- Load Balancing
- SSL Termination
- Static File Serving
- Caching
- Compression
- Rate Limiting
- WebSockets
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Nginx.**

Almost every modern production system places **Nginx** in front of application servers.

Examples:

```text id="ngx8701"
Client

↓

Nginx

↓

Spring Boot

Node.js

Django

FastAPI

Go
```

Nginx is much more than

a web server.

It is also:

- Reverse Proxy
- Load Balancer
- SSL Terminator
- Cache
- API Gateway (basic)
- Static File Server

______________________________________________________________________

# Why Nginx?

Before Nginx,

Apache HTTP Server

used

a process/thread

per connection.

Suppose

100,000 users

connect simultaneously.

Apache

would require

thousands

of threads

or processes.

Memory usage

becomes huge.

This became known as

the

**C10K Problem**

(handling 10,000+ concurrent connections).

Nginx

solved

this problem

using

an event-driven architecture.

______________________________________________________________________

# High-Level Architecture

```text id="ngx8702"
Clients

↓

Master Process

↓

Worker Processes

↓

Application Servers
```

______________________________________________________________________

# Master Process

Interview favorite.

The Master Process

does not

serve requests.

Responsibilities:

- Read configuration
- Start workers
- Reload configuration
- Graceful restart
- Monitor workers

If

a worker crashes,

the master

creates

a new one.

______________________________________________________________________

# Worker Processes

Workers

handle

client requests.

```text id="ngx8703"
Master

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

Each worker

is independent.

Workers

share

listening sockets

but

process

different requests.

______________________________________________________________________

# Event-Driven Architecture

Interview favorite.

Unlike

thread-per-request,

Nginx

uses

an event loop.

```text id="ngx8704"
Socket Ready

↓

Event Loop

↓

Process Request
```

One worker

can manage

thousands

of connections.

______________________________________________________________________

# epoll / kqueue

Interview favorite.

How does

Nginx know

which sockets

are ready?

Linux

provides

```text id="ngx8705"
epoll
```

BSD/macOS

provides

```text id="ngx8706"
kqueue
```

These OS mechanisms

notify

Nginx

only

when

a socket

is ready,

avoiding

continuous polling.

______________________________________________________________________

# Request Flow

```text id="ngx8707"
Browser

↓

TCP Connection

↓

Worker Process

↓

Reverse Proxy

↓

Application
```

______________________________________________________________________

# Reverse Proxy

Interview favorite.

Clients

never communicate

directly

with

application servers.

Instead

they talk

to Nginx.

```text id="ngx8708"
Client

↓

Nginx

↓

Backend
```

Benefits:

- Hide backend servers
- Centralized SSL
- Better security
- Easier scaling

______________________________________________________________________

# Load Balancing

Interview favorite.

Suppose

three backend servers

exist.

```text id="ngx8709"
Nginx

↓

App 1

App 2

App 3
```

Nginx

distributes

incoming requests.

______________________________________________________________________

# Load Balancing Algorithms

### Round Robin

Default.

```text id="ngx8710"
Request 1

↓

Server 1

Request 2

↓

Server 2

Request 3

↓

Server 3
```

______________________________________________________________________

### Least Connections

Choose

the server

with

the fewest

active connections.

Useful

for

long-running requests.

______________________________________________________________________

### IP Hash

Hash

the client's IP.

Requests

from

the same client

usually reach

the same backend.

Useful

for

session affinity.

______________________________________________________________________

### Weighted Round Robin

Suppose

one server

is more powerful.

```text id="ngx8711"
Server A

Weight = 3

Server B

Weight = 1
```

Server A

receives

more traffic.

______________________________________________________________________

# SSL Termination

Interview favorite.

Without Nginx

every backend

must handle

TLS.

Instead,

Nginx decrypts

HTTPS traffic.

```text id="ngx8712"
HTTPS

↓

Nginx

↓

HTTP

↓

Backend
```

Benefits:

- Less CPU usage
- Simpler applications
- Central certificate management

______________________________________________________________________

# Static File Serving

Nginx

is excellent

at serving:

- HTML
- CSS
- JavaScript
- Images
- Videos

These files

do not require

backend processing.

```text id="ngx8713"
Browser

↓

Nginx

↓

Static File
```

______________________________________________________________________

# Proxy Cache

Interview favorite.

Frequently requested

responses

can be cached.

```text id="ngx8714"
Request

↓

Cache Hit

↓

Response
```

Benefits:

- Lower backend load
- Faster responses

______________________________________________________________________

# Gzip Compression

Large responses

consume

bandwidth.

Nginx

can compress

responses.

```text id="ngx8715"
100 KB

↓

20 KB
```

Benefits:

- Faster downloads
- Lower bandwidth costs

______________________________________________________________________

# Rate Limiting

Interview favorite.

Suppose

one client

sends

10,000 requests/sec.

Prevent abuse.

Example

```text id="ngx8716"
100 Requests/minute
```

Excess requests

may receive

```http id="ngx8717"
HTTP 429

Too Many Requests
```

Useful

against

bots

and

DoS attacks.

______________________________________________________________________

# WebSocket Support

Interview favorite.

Normal HTTP

closes

after

every response.

WebSockets

stay open.

Nginx

can proxy

WebSocket connections.

```text id="ngx8718"
Client

↔

Nginx

↔

WebSocket Server
```

Useful

for:

- Chat
- Gaming
- Live dashboards

______________________________________________________________________

# Health Checks

Nginx

periodically checks

backend health.

Suppose

App Server 2

fails.

```text id="ngx8719"
App 2

↓

Unhealthy
```

Traffic

is routed

only

to

healthy servers.

______________________________________________________________________

# Zero-Downtime Reload

Interview favorite.

Suppose

the configuration

changes.

The Master Process

starts

new workers,

then

gracefully stops

old workers.

Existing connections

continue

until complete.

No downtime.

______________________________________________________________________

# Scaling

Scale

by adding

more backend servers.

```text id="ngx8720"
Nginx

↓

App 1

App 2

App 3

App 4
```

Nginx

itself

can also

be deployed

behind

DNS

or

another load balancer

for redundancy.

______________________________________________________________________

# Failure Scenario

Suppose

one backend

crashes.

Nginx

removes it

from

the load-balancing pool.

Requests

continue

to

healthy servers.

______________________________________________________________________

# Another Failure

Suppose

one Nginx instance

fails.

Use:

- Multiple Nginx instances
- DNS failover
- External Load Balancer

to eliminate

single points

of failure.

______________________________________________________________________

# End-to-End Architecture

```text id="ngx8721"
Users

↓

DNS

↓

Load Balancer

↓

Nginx

↓

Application Servers

↓

Redis

↓

PostgreSQL
```

______________________________________________________________________

# Trade-offs

Thread-per-Request

vs

Event-Driven

| Thread-per-Request | Event-Driven |
| ------------------ | ------------------ |
| More memory | Low memory |
| Context switching | Event loop |
| Simpler model | Better scalability |

______________________________________________________________________

Reverse Proxy

vs

Direct Backend Access

| Reverse Proxy | Direct Access |
| ------------------- | ------------------- |
| Better security | Simpler |
| SSL termination | Backend manages SSL |
| Centralized control | No central routing |

______________________________________________________________________

Caching

vs

No Cache

| Cache | No Cache |
| ------------------- | ------------------- |
| Faster | Always fresh |
| Lower backend load | Higher backend load |
| Possible stale data | No stale data |

______________________________________________________________________

# Best Practices

✅ Use Nginx as a reverse proxy.

✅ Enable SSL termination.

✅ Serve static assets directly.

✅ Enable gzip or Brotli compression.

✅ Configure health checks.

✅ Apply rate limiting.

✅ Cache appropriate responses.

______________________________________________________________________

# Common Mistakes

### Serving Static Files Through the Application

Application servers

should focus

on business logic.

Let Nginx

serve

static assets.

______________________________________________________________________

### No Rate Limiting

Without limits,

bots

or attackers

can overwhelm

your backend.

______________________________________________________________________

### Running a Single Nginx Instance

One Nginx server

creates

a single point

of failure.

Deploy

multiple instances.

______________________________________________________________________

### Ignoring Connection Timeouts

Long-lived

idle connections

consume

resources.

Configure

appropriate

timeouts.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Nginx?

Design Nginx as an event-driven reverse proxy with a master process responsible for configuration management and worker
processes responsible for handling client connections. Each worker uses operating system event notification mechanisms
such as epoll (Linux) or kqueue (BSD/macOS) to efficiently manage thousands of concurrent connections without creating a
thread per request. Support reverse proxying, load balancing, SSL termination, static file serving, caching,
compression, WebSocket proxying, and rate limiting. Perform health checks to route traffic only to healthy backend
servers and allow zero-downtime configuration reloads by replacing worker processes gracefully. Deploy multiple Nginx
instances behind DNS or an external load balancer for high availability.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Master & Worker architecture
- Event-driven programming
- epoll / kqueue
- Reverse proxy
- Load balancing
- SSL termination
- Static file serving
- Proxy caching
- Compression
- Rate limiting
- WebSocket proxying
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ Kafka Internals
- ✅ Redis Internals
- ✅ Nginx Internals

You now understand the three infrastructure components that appear in the majority of production backend architectures
and senior system design interviews.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll explore **Elasticsearch Internals**, including:

- Lucene architecture
- Inverted indexes
- Documents & mappings
- Shards & replicas
- Query execution
- Aggregations
- Cluster coordination
- Scaling and fault tolerance

______________________________________________________________________

# What's Next

[Elasticsearch System Design](88-elasticsearch-system-design.md)
