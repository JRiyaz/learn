# Complete HTTP Request Lifecycle Deep Dive

## 09. Forward Proxy vs Reverse Proxy

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand the difference between Forward Proxy and Reverse Proxy, how Reverse Proxies work internally, why almost every production backend uses Nginx or Envoy, how requests are processed before reaching the application, and what happens inside the operating system.

______________________________________________________________________

# Introduction

In the previous chapter,

the Load Balancer

selected

one backend server.

Now

the request

arrives

at

that server.

Many engineers think

it goes directly

to

FastAPI

or

Spring Boot.

In production,

that's almost

never true.

Instead,

the request

usually reaches

a

Reverse Proxy.

______________________________________________________________________

# High-Level Flow

```
Browser

↓

CDN

↓

WAF

↓

Load Balancer

↓

Reverse Proxy

↓

FastAPI

↓

Business Logic
```

______________________________________________________________________

# Why Do We Need A Reverse Proxy?

Imagine

your FastAPI

application

is exposed

directly

to

the Internet.

```
Internet

↓

FastAPI
```

Problems

- No SSL management
- No compression
- No static files
- No caching
- No request buffering
- No rate limiting
- Difficult deployments

Instead

we use

```
Internet

↓

Nginx

↓

FastAPI
```

______________________________________________________________________

# What Is A Proxy?

A proxy

is simply

a server

that forwards

requests

between

two parties.

Instead of

```
Client

↓

Server
```

we get

```
Client

↓

Proxy

↓

Server
```

______________________________________________________________________

# Types Of Proxy

Interview favorite.

There are

two major types.

```
Forward Proxy
```

```
Reverse Proxy
```

They solve

completely different

problems.

______________________________________________________________________

# Forward Proxy

A Forward Proxy

represents

the

client.

```
Client

↓

Forward Proxy

↓

Internet

↓

Server
```

The server

doesn't know

who the

real client is.

______________________________________________________________________

# Example

Suppose

a company

blocks

Facebook.

Employees

use

a Forward Proxy.

```
Laptop

↓

Corporate Proxy

↓

facebook.com
```

Facebook

only sees

the proxy.

______________________________________________________________________

# Common Uses

Forward Proxy

- Anonymous browsing
- Internet filtering
- Corporate networks
- VPNs
- Web scraping
- Caching

______________________________________________________________________

# Reverse Proxy

Interview favorite.

A Reverse Proxy

represents

the

server.

```
Client

↓

Reverse Proxy

↓

Backend Servers
```

The client

doesn't know

how many

backend servers

exist.

______________________________________________________________________

# Real Production Flow

```
Internet

↓

Cloudflare

↓

AWS ALB

↓

Nginx

↓

FastAPI
```

Browser thinks

it's talking

to

```
api.company.com
```

Actually

Nginx

handles

the request first.

______________________________________________________________________

# Popular Reverse Proxies

```
Nginx

Envoy

HAProxy

Traefik

Apache
```

______________________________________________________________________

# What Happens Internally?

Suppose

the request

reaches

Nginx.

```
TCP Connection

↓

TLS

↓

HTTP Parser

↓

Configuration Lookup

↓

Middleware

↓

Routing

↓

Forward To FastAPI
```

Notice

FastAPI

still hasn't

received

the request.

______________________________________________________________________

# Step 1

# Accept TCP Connection

Nginx

accepts

the TCP connection.

Internally

```
NIC

↓

Kernel

↓

Socket

↓

epoll()

↓

Nginx Worker
```

Unlike

many applications,

Nginx

uses

an event-driven

architecture.

______________________________________________________________________

# Why Is Nginx Fast?

Interview favorite.

Nginx

doesn't create

one thread

per request.

Instead

it uses

```
One Worker

↓

Thousands

of Connections
```

using

```
epoll()

Linux
```

or

```
kqueue()

macOS
```

This makes

Nginx

extremely scalable.

______________________________________________________________________

# Step 2

# TLS Termination

Suppose

TLS

wasn't terminated

at

the Load Balancer.

Nginx

decrypts

HTTPS.

```
HTTPS

↓

Nginx

↓

HTTP

↓

FastAPI
```

______________________________________________________________________

# Step 3

# HTTP Parsing

Nginx parses

```
Method

↓

Path

↓

Headers

↓

Cookies

↓

Body
```

It builds

an internal

HTTP request

representation.

______________________________________________________________________

# Step 4

# Configuration Lookup

Interview favorite.

Nginx

reads

its configuration.

Example

```nginx
location /api {
    proxy_pass http://fastapi;
}
```

Now

it knows

where

to send

the request.

______________________________________________________________________

# Step 5

# Route Matching

Suppose

the request

is

```
/images/logo.png
```

Nginx

may return

the file

directly.

```
Browser

↓

Nginx

↓

logo.png
```

FastAPI

is never called.

______________________________________________________________________

Another example

```
/api/users
```

↓

Forward

to

FastAPI.

______________________________________________________________________

# Static File Serving

Interview favorite.

Nginx

is much faster

than

FastAPI

for serving

```
Images

CSS

JavaScript

Videos
```

Reason

Nginx

uses

efficient

kernel APIs.

______________________________________________________________________

# sendfile()

Linux provides

```
sendfile()
```

Instead of

```
Disk

↓

Kernel

↓

User Space

↓

Kernel

↓

Socket
```

the kernel

copies data

directly.

```
Disk

↓

Kernel

↓

Socket
```

Much faster.

______________________________________________________________________

# Step 6

# Request Buffering

Suppose

client uploads

```
2 GB
```

Without buffering

FastAPI

must wait

while

the upload

arrives.

Instead

Nginx

buffers

the request.

```
Client

↓

Nginx Buffer

↓

FastAPI
```

Benefits

- Better performance
- Protection
- Backpressure

______________________________________________________________________

# Step 7

# Compression

Interview favorite.

Suppose

FastAPI

returns

```
2 MB JSON
```

Nginx

compresses

the response.

```
JSON

↓

Gzip

↓

Browser
```

Bandwidth

is reduced.

______________________________________________________________________

# Step 8

# Caching

Nginx

can cache

responses.

```
Client

↓

Nginx Cache

↓

Hit?

↓

Return

↓

Miss?

↓

FastAPI
```

Backend load

reduces.

______________________________________________________________________

# Step 9

# Rate Limiting

Example

```
100 Requests

per minute

per IP
```

Exceeded?

↓

```
429

Too Many Requests
```

FastAPI

never sees

the request.

______________________________________________________________________

# Step 10

# Security Headers

Interview favorite.

Nginx

can add

```
Strict-Transport-Security

Content-Security-Policy

X-Frame-Options

X-Content-Type-Options
```

before

returning

the response.

______________________________________________________________________

# Step 11

# Proxy Headers

Nginx

adds

important headers.

```
X-Forwarded-For

X-Forwarded-Proto

X-Real-IP

Forwarded
```

These tell

FastAPI

the original

client IP

and protocol.

______________________________________________________________________

# Example

Without

```
X-Forwarded-For
```

FastAPI sees

```
127.0.0.1
```

because

Nginx

is the client.

With

```
X-Forwarded-For

203.45.xx.xx
```

FastAPI knows

the real client.

______________________________________________________________________

# Step 12

# Forward To Backend

Finally

Nginx

opens

(or reuses)

a backend connection.

```
Nginx

↓

FastAPI

↓

ASGI

↓

Application
```

Only now

does

FastAPI

receive

the request.

______________________________________________________________________

# Connection Reuse

Interview favorite.

Instead of

opening

a new TCP connection

for every request,

Nginx

keeps

backend connections

alive.

Benefits

- Lower latency
- Less CPU
- Higher throughput

______________________________________________________________________

# Reverse Proxy Features

```
SSL Termination

↓

Compression

↓

Caching

↓

Routing

↓

Rate Limiting

↓

Static Files

↓

Security Headers

↓

Connection Pooling

↓

Load Balancing
```

______________________________________________________________________

# Reverse Proxy vs Load Balancer

Interview favorite.

Many people

confuse them.

## Reverse Proxy

Primary job

```
Request Processing
```

Examples

- SSL
- Compression
- Caching
- Routing

______________________________________________________________________

## Load Balancer

Primary job

```
Traffic Distribution
```

Chooses

which server

receives

the request.

______________________________________________________________________

# Can Nginx Do Both?

Yes.

Nginx

can act as

```
Reverse Proxy

+

Load Balancer
```

Many companies

use it

for both.

______________________________________________________________________

# What Happens Inside The OS?

```
NIC

↓

Kernel

↓

Socket

↓

epoll()

↓

Nginx Worker

↓

Configuration

↓

Backend Socket

↓

FastAPI
```

Nginx

doesn't poll

every socket.

The kernel

notifies

Nginx

only when

data arrives.

This is why

Nginx scales

to

hundreds of thousands

of connections.

______________________________________________________________________

# Common Failures

## Backend Down

Nginx

returns

```
502 Bad Gateway
```

or

tries

another backend.

______________________________________________________________________

## Backend Timeout

Nginx

returns

```
504 Gateway Timeout
```

______________________________________________________________________

## Client Disconnects

Nginx

closes

the backend connection

if appropriate.

______________________________________________________________________

# Common Attacks

## Slowloris

Attacker

sends

headers

very slowly.

Mitigation

Request timeout.

______________________________________________________________________

## Large Upload Attack

Huge uploads

consume resources.

Mitigation

```
client_max_body_size
```

______________________________________________________________________

## Header Injection

Malformed headers.

Mitigation

Strict parsing.

______________________________________________________________________

## Request Smuggling

Different proxies

interpret

HTTP requests

differently.

Modern Nginx

includes

protections,

but

correct configuration

is important.

______________________________________________________________________

# Popular Technologies

```
Nginx

Envoy

Traefik

HAProxy

Apache HTTP Server
```

______________________________________________________________________

# Technologies Used

| Feature | Technologies |
|----------|--------------|
| Reverse Proxy | Nginx, Envoy, Traefik |
| Event Loop | epoll, kqueue |
| Compression | Gzip, Brotli |
| Static Files | sendfile() |
| TLS | OpenSSL, BoringSSL |
| Proxy Protocol | HTTP/1.1, HTTP/2, gRPC |

______________________________________________________________________

# Common Interview Questions

## What is the difference between a Forward Proxy and a Reverse Proxy?

A Forward Proxy represents the client and forwards client requests to the Internet. A Reverse Proxy represents the
server and forwards incoming client requests to backend servers.

______________________________________________________________________

## Why do we put Nginx in front of FastAPI?

Nginx handles TLS termination, static file serving, compression, buffering, caching, security headers, rate limiting,
and connection management, allowing FastAPI to focus on application logic.

______________________________________________________________________

## Why is Nginx faster at serving static files?

Nginx uses an event-driven architecture and efficient kernel system calls such as `sendfile()`, avoiding unnecessary
memory copies and reducing CPU usage.

______________________________________________________________________

## What is `X-Forwarded-For`?

It is an HTTP header added by proxies that contains the original client's IP address, allowing backend applications to
identify the real client instead of the proxy.

______________________________________________________________________

## What is the difference between a 502 and a 504 error?

- **502 Bad Gateway** usually means the proxy received an invalid response from the backend.
- **504 Gateway Timeout** means the backend did not respond within the configured timeout.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when a request reaches Nginx.

### Answer

Nginx accepts the TCP connection, optionally terminates TLS, parses the HTTP request, matches the request against its
configuration, applies features such as compression, caching, rate limiting, and security headers, serves static files
directly when appropriate, or forwards the request to the backend application over a reused connection. It then receives
the backend response, optionally modifies it, and sends it back to the client.

______________________________________________________________________

# Summary

Reverse Proxies are one of the most important components in modern web infrastructure.

Key concepts include

- Forward Proxy vs Reverse Proxy
- TLS Termination
- HTTP Parsing
- Request Buffering
- Static File Serving
- `sendfile()`
- Compression
- Caching
- Security Headers
- `X-Forwarded-*` Headers
- Connection Reuse
- Event-Driven Architecture

At this point,

the request has safely entered your infrastructure and reached the server hosting your application.

The next intelligent routing layer is the **API Gateway**, which decides **which microservice** should handle the
request and applies cross-cutting concerns such as authentication, authorization, and rate limiting.

______________________________________________________________________

# Next

[10. API Gateway Deep Dive](10-api-gateway-deep-dive.md)
