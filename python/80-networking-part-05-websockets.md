# File:

python/python-80-networking-part-05-websockets.md

# Computer Networking

# Part 5: WebSockets – Real-Time Communication for Modern Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Computer Networking & Sockets
>
> **Lesson:** 80
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 16–20 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why HTTP is insufficient for real-time communication
- What WebSockets are
- How the WebSocket handshake works
- The WebSocket lifecycle
- Full-duplex communication
- WebSocket frames
- Building WebSocket servers with FastAPI
- Handling multiple WebSocket clients
- Broadcasting messages
- Connection management
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how to build a high-performance server using non-blocking sockets and selectors.

Modern web frameworks hide much of this complexity.

For example:

```
Browser

↓

HTTP

↓

FastAPI

↓

Business Logic
```

But what if the server needs to push information to the browser **without waiting for another HTTP request**?

Examples include:

- Chat applications
- Live stock prices
- Multiplayer games
- Live sports scores
- Notifications
- Collaborative editors

HTTP alone is not enough.

______________________________________________________________________

# The Problem with HTTP

HTTP follows a request-response model.

```
Browser

↓

Request

↓

Server

↓

Response
```

After the response is sent:

```
Connection Ends
```

If new information becomes available:

```
Server

↓

???

↓

Browser
```

The server cannot send it.

The browser must ask again.

______________________________________________________________________

# Polling

One solution is polling.

```
Browser

↓

GET /messages

↓

Server

↓

No Updates
```

Wait five seconds.

```
Browser

↓

GET /messages

↓

Server

↓

No Updates
```

Repeat.

Problems:

- Wasted requests
- Increased latency
- Higher server load

______________________________________________________________________

# Long Polling

A better approach is long polling.

```
Browser

↓

Request

↓

Server Waits

↓

New Message

↓

Response
```

After receiving the response:

```
Browser

↓

New Request
```

Better than polling.

Still based on repeated HTTP requests.

______________________________________________________________________

# WebSockets

WebSockets establish **one persistent connection**.

```
Browser

══════════════════════

Server
```

After the connection is established:

```
Browser

⇄

Server
```

Both sides can send messages at any time.

______________________________________________________________________

# Full-Duplex Communication

HTTP:

```
Client

↓

Server

↓

Client
```

WebSocket:

```
Client

⇄

Server
```

Both sides communicate independently.

This is called **full-duplex communication**.

______________________________________________________________________

# WebSocket Lifecycle

```
HTTP Request

↓

Upgrade Request

↓

WebSocket Connection

↓

Messages

↓

Connection Closed
```

Unlike HTTP, the connection stays open.

______________________________________________________________________

# The Handshake

A WebSocket connection begins as an ordinary HTTP request.

```
GET /chat HTTP/1.1
```

The client includes headers requesting an upgrade.

```
Upgrade: websocket

Connection: Upgrade
```

If accepted:

```
HTTP/1.1 101 Switching Protocols
```

After that:

```
HTTP Ends

↓

WebSocket Begins
```

______________________________________________________________________

# Visualising the Upgrade

```
Browser

↓

HTTP Request

↓

Upgrade Request

↓

Server

↓

101 Switching Protocols

══════════════════════

Persistent WebSocket Connection
```

______________________________________________________________________

# Messages Instead of Requests

HTTP:

```
Request

↓

Response

↓

Finished
```

WebSocket:

```
Message

↓

Message

↓

Message

↓

Message

↓

Close
```

______________________________________________________________________

# WebSocket Frames

Messages are transmitted as **frames**.

A large message may be divided into multiple frames.

```
Frame 1

↓

Frame 2

↓

Frame 3
```

The receiving endpoint reconstructs the original message.

Applications usually work with complete messages rather than individual frames.

______________________________________________________________________

# FastAPI WebSocket Endpoint

FastAPI provides a dedicated WebSocket type.

```python
from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(

    websocket: WebSocket

):
    ...
```

Notice:

There is no `GET` or `POST`.

______________________________________________________________________

# Accepting a Connection

Before sending or receiving messages:

```python
await websocket.accept()
```

The handshake completes.

The connection becomes active.

______________________________________________________________________

# Receiving Messages

```python
message = await websocket.receive_text()

print(message)
```

Unlike HTTP:

The same connection remains open.

______________________________________________________________________

# Sending Messages

```python
await websocket.send_text(

    "Hello Client"

)
```

The server may send messages whenever appropriate.

______________________________________________________________________

# Echo Server

```python
from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def echo(

    websocket: WebSocket

):

    await websocket.accept()

    while True:

        message = await websocket.receive_text()

        await websocket.send_text(

            f"Echo: {message}"

        )
```

The connection remains active until one side disconnects.

______________________________________________________________________

# Multiple Clients

Suppose three users connect.

```
Alice

↓

WebSocket

↓

Server
```

```
Bob

↓

WebSocket

↓

Server
```

```
Charlie

↓

WebSocket

↓

Server
```

Each client has its own WebSocket connection.

______________________________________________________________________

# Connection Manager

A common pattern is a connection manager.

```python
class ConnectionManager:

    def __init__(self):

        self.connections = []
```

Responsibilities include:

- Accepting connections.
- Tracking active clients.
- Removing disconnected clients.
- Broadcasting messages.

______________________________________________________________________

# Connecting Clients

```python
async def connect(

    self,

    websocket

):

    await websocket.accept()

    self.connections.append(

        websocket

    )
```

______________________________________________________________________

# Disconnecting Clients

```python
def disconnect(

    self,

    websocket

):

    self.connections.remove(

        websocket

    )
```

Always remove disconnected clients to avoid stale references.

______________________________________________________________________

# Broadcasting Messages

```python
async def broadcast(

    self,

    message

):

    for connection in self.connections:

        await connection.send_text(

            message

        )
```

Every connected client receives the same message.

______________________________________________________________________

# Handling Disconnects

Eventually:

```
Browser Closed

↓

Connection Lost

↓

Exception Raised
```

FastAPI raises:

```python
WebSocketDisconnect
```

Typical handling:

```python
try:
    ...
except WebSocketDisconnect:
    manager.disconnect(websocket)
```

______________________________________________________________________

# Authentication

Many applications authenticate before accepting a WebSocket.

Common approaches:

- JWT in headers.
- JWT in query parameters.
- Session cookies.

Example:

```
Client

↓

JWT

↓

Server

↓

Validate Token

↓

Accept Connection
```

Never trust client identity without verification.

______________________________________________________________________

# Heartbeats

Connections may disappear unexpectedly.

Servers often send:

```
Ping

↓

Pong
```

If no response arrives:

```
Close Connection
```

Heartbeats help detect dead connections.

______________________________________________________________________

# Common Use Cases

WebSockets are ideal for:

- Chat systems
- Live dashboards
- Collaborative editing
- Multiplayer games
- Live notifications
- IoT monitoring
- Market data feeds

They are usually unnecessary for standard CRUD APIs.

______________________________________________________________________

# Backend Architecture Example

```
Browser

↓

WebSocket

↓

FastAPI

↓

Redis Pub/Sub

↓

Worker

↓

Database
```

A worker publishes events.

FastAPI receives them.

Connected clients receive updates instantly.

______________________________________________________________________

# WebSockets vs HTTP

| HTTP | WebSocket |
|------|-----------|
| Request-response | Persistent connection |
| Client initiates | Either side initiates |
| Short-lived | Long-lived |
| Stateless | Stateful connection |
| CRUD APIs | Real-time communication |
| One response per request | Unlimited messages |

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using WebSockets for ordinary CRUD operations.

______________________________________________________________________

## Mistake 2

Forgetting to handle client disconnects.

______________________________________________________________________

## Mistake 3

Never removing inactive connections.

______________________________________________________________________

## Mistake 4

Performing blocking operations inside WebSocket handlers.

______________________________________________________________________

## Mistake 5

Ignoring authentication.

______________________________________________________________________

# Best Practices

✅ Keep messages small.

✅ Authenticate before accepting connections.

✅ Handle disconnects gracefully.

✅ Remove inactive clients.

✅ Use heartbeats for long-lived connections.

✅ Keep WebSocket handlers lightweight.

❌ Don't store large amounts of per-client state in memory.

❌ Don't block the event loop.

______________________________________________________________________

# Production Insight

Large-scale systems rarely send messages directly from business logic.

Instead:

```
Application

↓

Redis Pub/Sub

↓

WebSocket Server

↓

Connected Clients
```

Or:

```
Kafka

↓

Consumers

↓

WebSocket Gateway

↓

Users
```

Separating message production from message delivery improves scalability and allows multiple WebSocket servers to serve
the same application.

______________________________________________________________________

# Questions

### Question

> Why can't HTTP efficiently support real-time communication?

### Answer

Because HTTP is request-response based. Once the server sends a response, it cannot continue sending updates without the
client making another request.

______________________________________________________________________

### Question

> What is full-duplex communication?

### Answer

A communication model where both the client and server can send messages independently over the same connection.

______________________________________________________________________

### Question

> Why does a WebSocket begin with an HTTP request?

### Answer

The HTTP request performs the protocol upgrade, allowing existing web infrastructure to establish a WebSocket connection
using the standard HTTP port.

______________________________________________________________________

### Question

> Why is a connection manager useful?

### Answer

It centralises connection tracking, broadcasting, and cleanup logic, making the application easier to maintain.

______________________________________________________________________

### Question

> Why are heartbeats important?

### Answer

They help detect broken or inactive connections so server resources can be released promptly.

______________________________________________________________________

# Practical Lesson

Create:

```text
realtime_chat/

├── app.py

├── manager.py

└── client.html
```

Implement:

- A FastAPI WebSocket endpoint.
- A connection manager.
- User connection tracking.
- Message broadcasting.
- Graceful disconnect handling.

Then open the HTML page in multiple browser windows and verify that:

- Messages appear instantly.
- New users can join.
- Disconnected users are removed correctly.

______________________________________________________________________

# Knowledge Check

## Question 1

Why is WebSocket considered stateful while HTTP is generally stateless?

### Answer

A WebSocket connection remains open and maintains state about the connected client, whereas HTTP typically treats each
request independently.

______________________________________________________________________

## Question 2

What is the purpose of the HTTP 101 response?

### Answer

It confirms that the server has agreed to switch from the HTTP protocol to the WebSocket protocol.

______________________________________________________________________

## Question 3

Why should blocking database operations be avoided inside a WebSocket handler?

### Answer

Blocking operations prevent the event loop from processing messages for other connected clients, reducing
responsiveness.

______________________________________________________________________

## Question 4

Why is broadcasting easier with a connection manager?

### Answer

Because all active WebSocket connections are tracked in one place, allowing messages to be sent to every connected
client efficiently.

______________________________________________________________________

## Question 5

When should you choose WebSockets instead of HTTP?

### Answer

When the application requires low-latency, bidirectional, real-time communication between clients and the server.

______________________________________________________________________

# Assignment

## Exercise 1

Build a real-time chat application using FastAPI WebSockets.

______________________________________________________________________

## Exercise 2

Add usernames so each broadcast includes the sender's name.

______________________________________________________________________

## Exercise 3

Implement authentication using a JWT before accepting a WebSocket connection.

______________________________________________________________________

## Exercise 4

Integrate Redis Pub/Sub so that messages published by one application instance are broadcast to clients connected to
every WebSocket server instance.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why HTTP is limited for real-time communication.
- ✅ How WebSockets establish persistent connections.
- ✅ The WebSocket handshake.
- ✅ Full-duplex communication.
- ✅ Building WebSocket endpoints in FastAPI.
- ✅ Managing multiple connections.
- ✅ Broadcasting messages.
- ✅ Handling disconnects and authentication.
- ✅ Production architectures using Redis Pub/Sub.

______________________________________________________________________

# Next Lesson

**File:** [Questions-Part-1](81.questions-part-1.md)
