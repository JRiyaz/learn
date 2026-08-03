# System Design - Part 57

# WebSockets & Long Polling

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why real-time communication is needed
- What Polling is
- What Long Polling is
- What WebSockets are
- HTTP vs WebSockets
- WebSocket Lifecycle
- Scaling WebSockets
- FastAPI implementation
- AI/ML examples
- WebSockets vs SSE vs Long Polling
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

shows

notifications.

A member

borrows a book.

Immediately,

the librarian

should see

the update.

Question.

Should

the browser

refresh

every second?

Probably not.

We need

real-time communication.

______________________________________________________________________

# The Problem

Suppose

the browser

asks

every second

for updates.

```text id="ws5701"
Browser

↓

GET /notifications

↓

Server

↓

"No Updates"
```

One second later,

the browser

asks again.

```text id="ws5702"
Browser

↓

GET /notifications
```

Most requests

return

nothing.

The server

still processes

every request.

______________________________________________________________________

# Polling

This approach

is called

**Polling.**

The client

periodically

asks

the server

for updates.

```text id="ws5703"
Browser

↓

Request

↓

Response

↓

Wait

↓

Request
```

Simple.

But inefficient.

______________________________________________________________________

# Problems with Polling

Suppose

10 million users

poll

every second.

Even

if

nothing changes,

the server

must answer

every request.

Problems:

❌ Wasted bandwidth

❌ High CPU usage

❌ Higher latency

______________________________________________________________________

# The Idea

Instead of

asking

repeatedly,

let

the server

notify

the client

when

something changes.

______________________________________________________________________

# Long Polling

Instead of

responding

immediately,

the server

keeps

the request

open.

```text id="ws5704"
Browser

↓

Request

↓

Wait

↓

New Data

↓

Response
```

After

receiving

the response,

the browser

opens

another request.

______________________________________________________________________

# Long Polling Flow

```text id="ws5705"
Client

↓

Request

↓

Server Waits

↓

Event Happens

↓

Response

↓

New Request
```

This reduces

unnecessary requests

compared

to

regular polling.

______________________________________________________________________

# Problems with Long Polling

Although

better than

Polling,

Long Polling

still requires

new HTTP requests

after

every response.

At

very large scale,

this becomes

expensive.

______________________________________________________________________

# WebSockets

Instead of

opening

many HTTP requests,

create

one connection.

Keep it open.

Both

client

and server

can send data

at any time.

______________________________________________________________________

# What is a WebSocket?

A **WebSocket**

is a protocol

that provides

full-duplex,

persistent,

bidirectional communication

between

a client

and

a server.

______________________________________________________________________

# HTTP vs WebSocket

HTTP

```text id="ws5706"
Request

↓

Response

↓

Connection Closed
```

WebSocket

```text id="ws5707"
Connection Open

↓

Client ↔ Server

↓

Messages

↓

Connection Closed
```

The connection

remains open.

______________________________________________________________________

# WebSocket Handshake

A WebSocket

starts

as

an HTTP request.

```text id="ws5708"
HTTP Upgrade

↓

WebSocket Connection
```

After

the handshake,

communication

uses

the WebSocket protocol.

______________________________________________________________________

# Full Duplex

With WebSockets,

both sides

can send messages

independently.

```text id="ws5709"
Client

↔

Server
```

No request

is required

before

the server

sends data.

______________________________________________________________________

# Example

Suppose

a librarian

receives

a new notification.

```text id="ws5710"
Server

↓

Notification

↓

Browser
```

The browser

updates

immediately.

No polling.

______________________________________________________________________

# WebSocket Lifecycle

```text id="ws5711"
Connect

↓

Open

↓

Send/Receive

↓

Close
```

Connections

may remain open

for hours.

______________________________________________________________________

# FastAPI Example

FastAPI

provides

WebSocket support.

Example endpoint

```python id="ws5712"
@app.websocket("/ws")
```

Clients

connect once

and

exchange messages

continuously.

______________________________________________________________________

# Chat Example

Suppose

two users

chat.

```text id="ws5713"
User A

↓

Server

↓

User B
```

Messages

appear

instantly.

______________________________________________________________________

# AI/ML Example

Suppose

a user

uploads

a video

for AI processing.

The processing

takes

two minutes.

Instead of

refreshing

the page,

the server

uses

a WebSocket

to send:

```text id="ws5714"
0%

↓

25%

↓

50%

↓

100%
```

The UI

updates

in real time.

______________________________________________________________________

# Stock Market Example

Stock prices

change

every second.

Using

Polling

would create

millions

of unnecessary requests.

WebSockets

allow

the server

to push

price updates

immediately.

______________________________________________________________________

# Multiplayer Games

Games

require

very low latency.

Players'

positions

change

many times

per second.

WebSockets

are commonly used

to synchronize

game state.

______________________________________________________________________

# Scaling Problem

Suppose

one server

supports

100,000

WebSocket connections.

Now,

one million users

connect.

We need

multiple servers.

```text id="ws5715"
Load Balancer

↓

Server 1

Server 2

Server 3
```

______________________________________________________________________

# Sticky Sessions

WebSockets

typically remain

connected

to

one server.

Load Balancers

often use

Sticky Sessions

or

consistent routing

to keep

the connection

on

the same backend.

______________________________________________________________________

# Shared Messaging

Suppose

User A

connects

to

Server 1,

while

User B

connects

to

Server 2.

How does

Server 2

receive

messages

from

Server 1?

Usually

through

Redis Pub/Sub,

Kafka,

or another

message broker.

```text id="ws5716"
Server 1

↓

Redis

↓

Server 2
```

______________________________________________________________________

# Server-Sent Events (SSE)

Another option

for

real-time updates

is

**Server-Sent Events (SSE).**

Unlike

WebSockets,

SSE

supports

only

one-way communication.

```text id="ws5717"
Server

↓

Browser
```

The browser

cannot

send messages

over

the same connection.

______________________________________________________________________

# Polling vs Long Polling vs SSE vs WebSockets

| Feature | Polling | Long Polling | SSE | WebSockets |
| --------------------- | ------- | ------------- | ------- | ---------- |
| Client → Server | ✅ | ✅ | Limited | ✅ |
| Server → Client | ❌ | Response only | ✅ | ✅ |
| Persistent Connection | ❌ | Temporary | ✅ | ✅ |
| Bidirectional | ❌ | ❌ | ❌ | ✅ |
| Real-Time | Poor | Good | Better | Excellent |

______________________________________________________________________

# Real Backend Example

Suppose

a ride-sharing app.

The driver's

location

updates

every second.

WebSockets

allow

the driver's app

to continuously

send coordinates

while

the rider's app

receives

live updates.

______________________________________________________________________

# Benefits

WebSockets provide:

✅ Real-time communication

✅ Low latency

✅ Persistent connection

✅ Reduced network overhead

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Connection management

❌ Scaling complexity

❌ Stateful servers

❌ More memory usage

______________________________________________________________________

# When NOT to Use WebSockets

Avoid WebSockets

when:

- Simple CRUD APIs
- Traditional REST applications
- Infrequent updates

Regular HTTP

is often

simpler.

______________________________________________________________________

# Best Practices

✅ Authenticate connections.

✅ Handle reconnects.

✅ Send heartbeat messages.

✅ Monitor connection count.

______________________________________________________________________

# Common Mistakes

### Opening Too Many Connections

Each connection

consumes

memory

and

server resources.

______________________________________________________________________

### Forgetting Heartbeats

Long-lived connections

may silently

disconnect.

Heartbeat messages

detect

dead connections.

______________________________________________________________________

### Using WebSockets for Everything

Many APIs

work perfectly

with

HTTP.

Use WebSockets

only

when

real-time communication

is required.

______________________________________________________________________

### Ignoring Horizontal Scaling

Multiple servers

must coordinate

messages

using

Redis,

Kafka,

or another broker.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** When should you use WebSockets instead of HTTP?

WebSockets should be used when applications require real-time, bidirectional communication between clients and servers.
Unlike HTTP, which follows a request-response model, WebSockets establish a persistent connection that allows either
side to send messages at any time. They are commonly used for chat applications, multiplayer games, stock market
updates, collaborative editing, live dashboards, and AI inference progress updates. For standard CRUD operations or
infrequent updates, traditional HTTP remains simpler and more efficient.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Polling
- Long Polling
- WebSockets
- WebSocket lifecycle
- SSE
- Scaling WebSockets
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand the major communication models:

- ✅ REST APIs
- ✅ Message Queues
- ✅ Event-Driven Architecture
- ✅ Publish/Subscribe
- ✅ WebSockets

Each communication model solves a different problem, and choosing the right one is a common system design interview
topic.

______________________________________________________________________

# What's Next

[Webhooks](58-webhooks.md)
