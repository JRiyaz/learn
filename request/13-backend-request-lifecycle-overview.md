# Complete HTTP Request Lifecycle Deep Dive

## 13. Backend Request Lifecycle Overview

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand **exactly** what happens after the infrastructure (CDN, WAF, Load Balancer, Reverse Proxy, API Gateway) forwards a request to your backend server. We will trace the request from the Linux kernel to your FastAPI application.

______________________________________________________________________

# Introduction

Until now,

everything happened

outside

your application.

The request has successfully passed

- Browser
- DNS
- TCP
- TLS
- CDN
- WAF
- Load Balancer
- Reverse Proxy
- API Gateway

Now

the request

finally reaches

your server.

This is where

most backend engineers

stop explaining.

We won't.

We'll follow

every step.

______________________________________________________________________

# Complete Backend Flow

```
Internet

↓

Network Interface Card (NIC)

↓

Linux Kernel

↓

TCP Receive Buffer

↓

Socket

↓

epoll()

↓

Uvicorn

↓

HTTP Parser

↓

ASGI Scope

↓

FastAPI Application

↓

Middleware

↓

Dependency Injection

↓

Request Validation

↓

Authentication

↓

Authorization

↓

Business Logic

↓

Cache

↓

Database

↓

Business Logic

↓

Response

↓

ASGI

↓

Uvicorn

↓

Linux Kernel

↓

NIC

↓

Internet
```

This chapter

provides

the complete roadmap.

Each block

will become

its own chapter

later.

______________________________________________________________________

# Production Architecture

```
                        Internet

                            │

                            ▼

                     Network Card (NIC)

                            │

                            ▼

                     Linux Network Stack

                            │

                            ▼

                       TCP Socket

                            │

                            ▼

                          epoll()

                            │

                            ▼

                         Uvicorn

                            │

                            ▼

                    httptools Parser

                            │

                            ▼

                      ASGI Application

                            │

                            ▼

                         FastAPI

                            │

            ┌───────────────┼────────────────┐

            ▼               ▼                ▼

      Middleware      Dependencies      Exception Handler

                            │

                            ▼

                     Request Validation

                            │

                            ▼

                     Authentication

                            │

                            ▼

                     Authorization

                            │

                            ▼

                      Business Logic

                            │

             ┌──────────────┼───────────────┐

             ▼              ▼               ▼

          Redis        PostgreSQL       Kafka

             │              │               │

             └──────────────┼───────────────┘

                            ▼

                      Response Object

                            │

                            ▼

                         Uvicorn

                            │

                            ▼

                        Linux Kernel

                            │

                            ▼

                           Client
```

______________________________________________________________________

# Stage 1

# Network Interface Card (NIC)

Interview favorite.

The HTTP request

arrives

as

electrical

or

radio signals.

```
Internet

↓

Ethernet Cable

↓

NIC
```

The NIC

converts

signals

into

binary data.

It then

raises

a hardware interrupt

to notify

the operating system.

______________________________________________________________________

# What Happens Internally?

```
Ethernet Frame

↓

NIC Memory

↓

DMA

↓

Kernel Memory
```

Notice

the CPU

doesn't initially

copy the data.

The NIC

uses

DMA

(Direct Memory Access)

to write

directly

into RAM.

This reduces

CPU usage.

______________________________________________________________________

# Stage 2

# Linux Kernel

The Linux Kernel

owns

the network stack.

It receives

the packet

from

the NIC.

```
NIC

↓

Kernel

↓

Network Stack
```

Responsibilities

- Verify checksum
- Remove Ethernet header
- Read IP header
- Read TCP header
- Find destination socket

______________________________________________________________________

# What Happens Internally?

```
Ethernet Frame

↓

Remove Ethernet Header

↓

IP Packet

↓

Remove IP Header

↓

TCP Segment

↓

TCP Socket
```

This process

is called

```
Decapsulation
```

______________________________________________________________________

# Stage 3

# TCP Receive Buffer

Every TCP connection

has

a receive buffer.

```
Network

↓

Kernel

↓

Receive Buffer
```

Incoming bytes

are stored here

until

the application

reads them.

______________________________________________________________________

# Why A Buffer?

Suppose

the network

is faster

than

your application.

Without

a buffer,

packets

would be lost.

The receive buffer

absorbs

temporary bursts.

______________________________________________________________________

# Stage 4

# Socket

Interview favorite.

The kernel

identifies

which socket

owns

the packet.

A socket

is identified by

```
Source IP

↓

Source Port

↓

Destination IP

↓

Destination Port
```

Example

```
192.168.1.10:52345

↓

10.0.0.15:443
```

______________________________________________________________________

# Stage 5

# epoll()

Interview favorite.

Suppose

10,000 clients

are connected.

Should

Uvicorn

continuously check

every socket?

No.

Instead

Linux provides

```
epoll()
```

```
Socket Ready?

↓

Notify Application
```

No CPU

is wasted

checking

idle sockets.

______________________________________________________________________

# Why epoll()?

Without epoll

```
Loop

↓

Socket1?

↓

Socket2?

↓

Socket3?

↓

...

↓

Socket100000?
```

Huge waste

of CPU.

With epoll

```
Kernel

↓

Ready Socket

↓

Notify Uvicorn
```

Much faster.

______________________________________________________________________

# Stage 6

# Uvicorn

Interview favorite.

Uvicorn

is

an

ASGI Server.

Responsibilities

```
Read Socket

↓

Parse HTTP

↓

Create ASGI Scope

↓

Call FastAPI
```

Notice

Uvicorn

is NOT

FastAPI.

FastAPI

is simply

an ASGI application.

______________________________________________________________________

# What Actually Happens?

Uvicorn

calls

```
socket.recv()
```

The kernel

copies

available bytes

from

the receive buffer

into

Uvicorn's memory.

```
Kernel Buffer

↓

recv()

↓

Python Memory
```

______________________________________________________________________

# Stage 7

# HTTP Parser

Interview favorite.

The bytes

received

are meaningless.

Example

```
47 45 54 ...

```

The HTTP parser

converts

raw bytes

into

HTTP structures.

Example

```
Method

GET
```

```
Path

/users
```

```
Headers

Host

Authorization

Content-Type
```

Popular parser

used by Uvicorn

```
httptools
```

______________________________________________________________________

# Stage 8

# ASGI Scope

Interview favorite.

Uvicorn

creates

an

ASGI Scope.

Example

```python
{
    "type": "http",
    "method": "GET",
    "path": "/users",
    "headers": [...],
    "client": (...),
    "server": (...)
}
```

This

is

FastAPI's

request metadata.

______________________________________________________________________

# What Is ASGI?

ASGI

means

```
Asynchronous

Server

Gateway

Interface
```

Think of it as

the contract

between

```
Uvicorn

↓

FastAPI
```

FastAPI

doesn't know

whether

Uvicorn,

Hypercorn,

or Daphne

is running.

They all speak

ASGI.

______________________________________________________________________

# Stage 9

# FastAPI Application

Now

Uvicorn

calls

the FastAPI application.

Internally

something similar

to this happens.

```python
await app(scope, receive, send)
```

FastAPI

now takes control.

______________________________________________________________________

# Stage 10

# Middleware Chain

Before

your endpoint executes,

every middleware

runs.

Example

```
Logging

↓

CORS

↓

GZip

↓

Authentication

↓

Custom Middleware
```

Every request

passes

through

the middleware chain.

______________________________________________________________________

# Stage 11

# Dependency Injection

Interview favorite.

FastAPI

builds

all dependencies

before

calling

your endpoint.

Example

```python
def get_db():
    ...
```

```python
def get_current_user():
    ...
```

These execute

before

your route handler.

______________________________________________________________________

# Stage 12

# Request Validation

Suppose

the request body

contains

```
{
    "email":"abc@gmail.com",
    "password":"secret"
}
```

FastAPI

doesn't give

raw JSON

to

your function.

Instead

```
Raw Bytes

↓

JSON Parser

↓

Python Dictionary

↓

Pydantic Model

↓

Validated Object
```

Invalid data

never reaches

your business logic.

______________________________________________________________________

# Stage 13

# Authentication

Now

FastAPI

asks

```
Who is

this user?
```

Examples

- JWT
- OAuth
- API Key
- Session Cookie

This

will become

an entire chapter.

______________________________________________________________________

# Stage 14

# Authorization

Now

FastAPI asks

```
Can

this user

perform

this action?
```

Example

```
DELETE

/users

↓

Admin?
```

______________________________________________________________________

# Stage 15

# Business Logic

Finally

your code

runs.

Example

```python
@app.get("/users/{id}")
```

Everything

before this

was

framework

or

infrastructure.

______________________________________________________________________

# Stage 16

# Cache

Business logic

may check

Redis first.

```
Redis

↓

Hit?

↓

Return

↓

Miss?

↓

Database
```

______________________________________________________________________

# Stage 17

# Database

If necessary

the application

queries

PostgreSQL.

Later

we'll study

how PostgreSQL

internally executes

queries.

______________________________________________________________________

# Stage 18

# Build Response

FastAPI

creates

a Response object.

Example

```json
{
    "id":1,
    "name":"Riyaz"
}
```

______________________________________________________________________

# Stage 19

# Response Serialization

Python objects

become

JSON bytes.

```
Python Object

↓

JSON

↓

UTF-8 Bytes
```

______________________________________________________________________

# Stage 20

# Send Response

FastAPI

returns

the response

to

Uvicorn.

Uvicorn

writes

the bytes

back

to

the socket.

```
FastAPI

↓

Uvicorn

↓

Kernel

↓

NIC

↓

Internet

↓

Browser
```

______________________________________________________________________

# Complete Internal Flow

```
NIC

↓

Kernel

↓

TCP Buffer

↓

Socket

↓

epoll()

↓

Uvicorn

↓

recv()

↓

httptools

↓

ASGI Scope

↓

FastAPI

↓

Middleware

↓

Dependencies

↓

Validation

↓

Authentication

↓

Authorization

↓

Business Logic

↓

Redis

↓

PostgreSQL

↓

Response

↓

Uvicorn

↓

Kernel

↓

NIC
```

______________________________________________________________________

# What Will We Learn Next?

Every box

above

becomes

its own

deep dive.

We won't simply say

```
Authentication

↓

Authorization
```

We'll explain

everything.

Example

Authentication

```
Request Body

↓

JSON Parsing

↓

Pydantic

↓

Extract Username

↓

Normalize Email

↓

SQL Query

↓

Read Password Hash

↓

Argon2 Hash

↓

Constant Time Compare

↓

Generate JWT

↓

Store Refresh Token

↓

Return Response
```

We'll also explain

- Memory allocation
- Python objects
- Security attacks
- Timing attacks
- SQL injection
- Hashing algorithms
- Constant-time comparison
- JWT internals

______________________________________________________________________

# Common Interview Questions

## What is the first userspace program that receives an HTTP request?

Normally the ASGI server (such as Uvicorn), after the Linux kernel has accepted the TCP connection and signaled that
socket data is available.

______________________________________________________________________

## Does FastAPI read data directly from the network?

No.

The Linux kernel receives packets first. Uvicorn reads bytes from the socket, parses HTTP, creates an ASGI scope, and
then calls the FastAPI application.

______________________________________________________________________

## What is ASGI?

ASGI (Asynchronous Server Gateway Interface) is the interface between an ASGI server (Uvicorn, Hypercorn) and
asynchronous Python web frameworks like FastAPI.

______________________________________________________________________

## Why doesn't FastAPI parse raw TCP packets?

Because networking responsibilities belong to the operating system and the ASGI server. FastAPI operates at the HTTP
application layer.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens after a request reaches your Linux server.

### Answer

The NIC receives the Ethernet frame and transfers it into memory using DMA. The Linux kernel processes the Ethernet, IP,
and TCP headers, places the payload into the socket's receive buffer, and notifies Uvicorn through `epoll()`. Uvicorn
reads the bytes using `recv()`, parses the HTTP request with `httptools`, creates an ASGI scope, and invokes the FastAPI
application. FastAPI then executes middleware, dependency injection, validation, authentication, authorization, business
logic, and eventually builds the response, which flows back through Uvicorn, the kernel, and the NIC to the client.

______________________________________________________________________

# Summary

This chapter marks the transition from infrastructure into application internals.

From the next chapter onward, we stop talking about servers and start exploring **exactly how Python, Uvicorn, FastAPI,
and the Linux kernel cooperate to process every request**.

______________________________________________________________________

# Next

[14. Web Server and ASGI Internals](14-web-server-and-asgi-internals.md)
