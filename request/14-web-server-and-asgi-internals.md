# Complete HTTP Request Lifecycle Deep Dive

## 14. Web Server and ASGI Internals

> **Target Audience:** Backend Engineers (Intermediate → Senior)
>
> **Goal:** Understand exactly what happens from the moment the Linux kernel notifies Uvicorn that data is available until FastAPI receives a Python request object.

______________________________________________________________________

# Introduction

In the previous chapter,

we stopped here.

```
Internet

↓

NIC

↓

Linux Kernel

↓

TCP Buffer

↓

Socket

↓

epoll()

↓

Uvicorn
```

Now

we'll go inside

Uvicorn.

This chapter explains

what happens

inside

the web server.

______________________________________________________________________

# Where We Are

```
Browser

↓

Internet

↓

Linux Kernel

↓

Socket

↓

epoll()

↓

Uvicorn

❗ You are here

↓

FastAPI
```

______________________________________________________________________

# What Is A Web Server?

Interview favorite.

A web server

is responsible for

```
Accept TCP Connections

↓

Read Socket

↓

Parse HTTP

↓

Create Request

↓

Call Application

↓

Send Response
```

Notice

it does **NOT**

contain

your business logic.

______________________________________________________________________

# Popular Python Web Servers

| Server | Supports |
|---------|----------|
| Uvicorn | ASGI |
| Hypercorn | ASGI |
| Daphne | ASGI |
| Gunicorn | WSGI + ASGI Workers |
| Waitress | WSGI |

______________________________________________________________________

# Uvicorn Architecture

```
             Linux Kernel

                    │

                    ▼

                epoll()

                    │

                    ▼

             Uvicorn Event Loop

                    │

        ┌───────────┼────────────┐

        ▼           ▼            ▼

    Socket      HTTP Parser    ASGI App

                                   │

                                   ▼

                               FastAPI
```

______________________________________________________________________

# Why Doesn't FastAPI Listen On Port 8000?

Interview favorite.

Many developers think

```
FastAPI

↓

Port 8000
```

Actually

```
FastAPI

↓

ASGI Application
```

Uvicorn

owns

the socket.

Example

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Uvicorn

opens

the socket.

FastAPI

never does.

______________________________________________________________________

# What Happens First?

Suppose

a packet arrives.

Linux

already notified

Uvicorn

using

```
epoll()
```

Now

Uvicorn calls

```python
socket.recv()
```

______________________________________________________________________

# socket.recv()

Interview favorite.

```
Kernel Receive Buffer

↓

socket.recv()

↓

Python Bytes
```

Suppose

the client sent

```
GET /users HTTP/1.1
Host: api.company.com
```

Initially

these are

just bytes.

```
47 45 54 20 ...
```

Not strings.

Not JSON.

Not HTTP objects.

Just bytes.

______________________________________________________________________

# Why Bytes?

Networks

don't send

Python objects.

They send

binary data.

```
01001010

01100101

01110100
```

Uvicorn

must decode

them.

______________________________________________________________________

# HTTP Parser

Interview favorite.

Uvicorn

uses

```
httptools
```

which is based on

Node.js'

HTTP parser.

Responsibilities

```
Read Bytes

↓

Recognize Method

↓

Recognize Headers

↓

Recognize Body

↓

Recognize HTTP Version
```

______________________________________________________________________

# Example

Incoming bytes

```
GET /users HTTP/1.1

Host: api.company.com

Accept: application/json
```

After parsing

```
Method

GET
```

```
Path

/users
```

```
Version

HTTP/1.1
```

```
Headers

Dictionary
```

______________________________________________________________________

# Parsing Request Body

Suppose

client sends

```
POST /login
```

Body

```
{
    "email":"riyaz@gmail.com",
    "password":"secret"
}
```

Parser

does NOT

understand JSON.

It simply says

```
These bytes

belong

to

the body.
```

JSON parsing

happens later

inside FastAPI.

______________________________________________________________________

# HTTP Parser State Machine

Interview favorite.

The parser

moves through

states.

```
Request Line

↓

Headers

↓

Blank Line

↓

Body

↓

Complete
```

Each state

generates

callbacks.

______________________________________________________________________

# Why Use A State Machine?

Because

HTTP data

may arrive

in pieces.

Example

Packet 1

```
GET /use
```

Packet 2

```
rs HTTP/1.1
```

Parser

waits

until

enough bytes

arrive.

______________________________________________________________________

# Partial Reads

Interview favorite.

Suppose

client uploads

100 MB.

Uvicorn

does NOT

receive

100 MB

at once.

Instead

```
Chunk 1

↓

Chunk 2

↓

Chunk 3

↓

...
```

Parser

processes

the stream

incrementally.

______________________________________________________________________

# Creating The ASGI Scope

After parsing,

Uvicorn creates

the ASGI Scope.

Example

```python
scope = {
    "type": "http",
    "method": "GET",
    "path": "/users",
    "scheme": "https",
    "headers": [...],
    "client": ("192.168.1.5", 54321),
    "server": ("10.0.0.5", 443),
}
```

This contains

metadata only.

No request body yet.

______________________________________________________________________

# What Is Receive?

Interview favorite.

ASGI

passes

three arguments.

```python
await app(scope, receive, send)
```

```
scope

↓

Metadata
```

```
receive()

↓

Incoming Messages
```

```
send()

↓

Outgoing Messages
```

______________________________________________________________________

# Why Isn't The Body Inside scope?

Imagine

uploading

```
5 GB
```

Putting

5 GB

inside

memory

immediately

would be terrible.

Instead

FastAPI

reads

the body

when needed

using

```
receive()
```

______________________________________________________________________

# receive()

Internally

FastAPI asks

```
Do you have

more data?
```

Uvicorn replies

```
Chunk

↓

Chunk

↓

Chunk

↓

Finished
```

Streaming.

______________________________________________________________________

# send()

Later

FastAPI uses

```
send()
```

to return

```
Headers

↓

Body

↓

Complete
```

to Uvicorn.

______________________________________________________________________

# Event Loop

Interview favorite.

Uvicorn

doesn't create

one thread

per request.

Instead

```
One Event Loop

↓

Many Coroutines
```

Example

```
Request A

↓

Waiting DB
```

CPU

switches

to

```
Request B
```

No thread

is blocked.

______________________________________________________________________

# asyncio

Uvicorn

uses

Python's

```
asyncio
```

Example

```python
await socket.recv()
```

While waiting,

the event loop

runs

other requests.

______________________________________________________________________

# Blocking Code

Suppose

inside FastAPI

you write

```python
time.sleep(10)
```

Problem

```
Entire Worker

Stops
```

Because

the event loop

is blocked.

Correct

```python
await asyncio.sleep(10)
```

______________________________________________________________________

# Request Lifecycle Inside Uvicorn

```
Socket Ready

↓

recv()

↓

HTTP Parser

↓

ASGI Scope

↓

FastAPI

↓

Response

↓

Socket Send
```

______________________________________________________________________

# Keep-Alive

Interview favorite.

HTTP/1.1

keeps

connections open.

Instead of

```
Request

↓

Close

↓

Reconnect
```

We get

```
Connect

↓

Request

↓

Request

↓

Request

↓

Close
```

Faster.

______________________________________________________________________

# Connection Pool

Browser

may reuse

existing

TCP connections.

Less latency.

Less CPU.

______________________________________________________________________

# Worker Process

Example

```
Gunicorn

↓

Worker1

↓

Uvicorn
```

```
Worker2

↓

Uvicorn
```

Each worker

has

its own

event loop.

______________________________________________________________________

# Why Multiple Workers?

One Python process

uses

one CPU core.

Multiple workers

utilize

multiple CPU cores.

Example

```
8 CPU

↓

8 Workers
```

______________________________________________________________________

# Memory Allocation

Interview bonus.

When

recv()

returns

```
bytes
```

Python allocates

a bytes object.

Later

headers

become

Python dictionaries.

Eventually

FastAPI

creates

Request objects.

Understanding

these allocations

helps explain

memory usage

under heavy load.

______________________________________________________________________

# What Happens If Client Disconnects?

Suppose

client closes

the browser.

Uvicorn receives

```
Connection Closed
```

FastAPI

can cancel

the coroutine.

Resources

are released.

______________________________________________________________________

# Common Attacks

## Slowloris

Attacker

sends

headers

very slowly.

Worker

stays busy.

Mitigation

Request timeout.

______________________________________________________________________

## Huge Headers

Attacker sends

100 MB headers.

Mitigation

Header size limits.

______________________________________________________________________

## Huge Body

Attacker uploads

100 GB.

Mitigation

Maximum body size.

______________________________________________________________________

# Technologies Used

| Component | Technology |
|-----------|------------|
| Event Loop | asyncio |
| Socket API | socket.recv(), socket.send() |
| HTTP Parser | httptools |
| ASGI Server | Uvicorn |
| Multiprocessing | Gunicorn |
| Kernel Notification | epoll |

______________________________________________________________________

# Common Interview Questions

## Does FastAPI read sockets?

No.

Uvicorn owns the sockets.

FastAPI only receives ASGI messages.

______________________________________________________________________

## Why is Uvicorn asynchronous?

It uses Python's asyncio event loop so one worker can efficiently handle thousands of concurrent idle or waiting
connections without blocking on I/O.

______________________________________________________________________

## What is the difference between `scope`, `receive`, and `send`?

- `scope` contains request metadata.
- `receive()` streams incoming request events (such as the body).
- `send()` streams outgoing response events.

______________________________________________________________________

## Why doesn't Uvicorn parse JSON?

JSON belongs to the application layer. Uvicorn parses HTTP, while FastAPI (through Starlette and Pydantic) parses JSON.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens inside Uvicorn after `epoll()` signals that data is available.

### Answer

Uvicorn calls `socket.recv()` to copy bytes from the kernel's receive buffer into user space. It feeds those bytes to
the HTTP parser (`httptools`), which incrementally parses the request line, headers, and body. Uvicorn constructs an
ASGI scope containing request metadata and invokes the FastAPI application using `await app(scope, receive, send)`. The
request body is streamed through `receive()`, and the response is later streamed back through `send()`.

______________________________________________________________________

# Summary

At this point,

the raw network packets have become

an ASGI request.

Key concepts include

- socket.recv()
- HTTP parsing
- State machines
- Partial reads
- ASGI Scope
- receive()
- send()
- Event Loop
- asyncio
- Keep-Alive
- Worker Processes

The request is now inside **FastAPI**.

The next chapter begins tracing **the middleware pipeline**, where every request is intercepted before it reaches your
endpoint.

______________________________________________________________________

# Next

[15. Middleware Request Pipeline](15-middleware-request-pipeline.md)
