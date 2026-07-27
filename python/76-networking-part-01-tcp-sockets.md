# File: python/76-networking-part-01-tcp-sockets.md

# Computer Networking
# Part 2: TCP Sockets – How Applications Communicate Over the Network

> **Course:** Backend Engineering Roadmap
>
> **Module:** Computer Networking & Sockets
>
> **Lesson:** 77
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 14–16 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- What a socket is
- Why sockets exist
- TCP sockets
- Client-server communication
- Socket lifecycle
- Binding
- Listening
- Accepting connections
- Sending and receiving data
- Closing connections
- Common socket errors
- Production best practices

---

# Recap

Every backend application communicates over a network.

For example:

```
Browser

↓

FastAPI

↓

PostgreSQL
```

Or:

```
Mobile App

↓

API

↓

Redis
```

Or:

```
Microservice A

↓

Microservice B
```

How does one program actually send data to another?

The answer is:

**Sockets.**

---

# What is a Socket?

A socket is an endpoint for network communication between two processes.

Think of it as a communication channel.

```
Application

↓

Socket

↓

Network

↓

Socket

↓

Application
```

Applications do not communicate directly with each other.

They communicate through sockets managed by the operating system.

---

# A Real-World Analogy

Imagine two people talking on telephones.

```
Alice

↓

Telephone

══════════

Telephone

↓

Bob
```

The people exchange information.

The telephones provide the communication channel.

A socket plays the role of the telephone.

---

# Why Do We Need Sockets?

Without sockets:

```
Program A

❌

Program B
```

There is no standard way to exchange data.

With sockets:

```
Program A

↓

Socket

↓

Network

↓

Socket

↓

Program B
```

The operating system handles routing, buffering, retransmission, and connection management.

---

# Socket Types

The two most common transport protocols are:

```
TCP
```

Reliable, connection-oriented communication.

```
UDP
```

Fast, connectionless communication.

This lesson focuses on **TCP**.

---

# TCP Characteristics

TCP provides:

- Reliable delivery
- Ordered packets
- Error detection
- Retransmission
- Flow control

```
Sender

↓

Packet 1

↓

Packet 2

↓

Packet 3

↓

Receiver
```

The receiver gets the data in the correct order.

---

# Client–Server Model

```
Client

↓

Request

↓

Server

↓

Response
```

Examples:

- Browser → Web Server
- FastAPI → PostgreSQL
- Redis Client → Redis Server

---

# Socket Lifecycle

A TCP server follows this sequence:

```
socket()

↓

bind()

↓

listen()

↓

accept()

↓

recv()

↓

send()

↓

close()
```

Understanding this lifecycle is fundamental to network programming.

---

# Creating a Socket

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
```

Explanation:

- `AF_INET` specifies IPv4.
- `SOCK_STREAM` specifies TCP.

---

# Binding

A server must bind to an IP address and port.

```python
server.bind(("127.0.0.1", 8000))
```

This tells the operating system:

> "Deliver connections for port 8000 to this socket."

---

# Listening

```python
server.listen()
```

The socket is now ready to accept incoming connections.

```
Client

↓

Waiting Queue

↓

Server
```

The operating system maintains a backlog of pending connections.

---

# Accepting Connections

```python
client_socket, address = server.accept()
```

This call blocks until a client connects.

It returns:

- A new socket dedicated to the client.
- The client's address.

The original listening socket continues accepting future connections.

---

# Receiving Data

```python
data = client_socket.recv(1024)
```

The argument specifies the maximum number of bytes to read.

The result is a `bytes` object.

```python
print(data)
```

Output:

```text
b"Hello"
```

---

# Sending Data

```python
client_socket.send(
    b"Hello Client"
)
```

Sockets transmit bytes, not Python strings.

Encode text before sending:

```python
message = "Hello"

client_socket.send(
    message.encode("utf-8")
)
```

---

# Closing Connections

Always release socket resources.

```python
client_socket.close()

server.close()
```

Closing sockets frees operating system resources and notifies the peer that communication has ended.

---

# Complete Echo Server

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

server.bind(("127.0.0.1", 8000))
server.listen()

print("Waiting for client...")

client, address = server.accept()

print(f"Connected: {address}")

while True:

    data = client.recv(1024)

    if not data:
        break

    client.send(data)

client.close()
server.close()
```

This server echoes every message it receives.

---

# Client Example

```python
import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(("127.0.0.1", 8000))

client.send(b"Hello")

response = client.recv(1024)

print(response.decode())

client.close()
```

---

# What Actually Happens?

```
Client

↓

connect()

═══════════════

Server

↓

accept()

↓

recv()

↓

send()

═══════════════

Client

↓

recv()
```

Although the code appears simple, the operating system performs:

- Connection establishment
- Packet routing
- Error detection
- Buffer management
- Packet retransmission
- Connection teardown

---

# Common Socket Errors

## Port Already in Use

```text
OSError:

Address already in use
```

Another process is already bound to the port.

---

## Connection Refused

```text
ConnectionRefusedError
```

No server is listening on the destination port.

---

## Timeout

The peer does not respond within the configured time.

---

## Broken Pipe

The remote peer closed the connection while data was being sent.

---

# Best Practices

✅ Always close sockets.

✅ Handle exceptions.

✅ Set timeouts where appropriate.

✅ Validate received data.

✅ Encode and decode consistently.

❌ Don't assume `recv()` returns the complete message.

❌ Don't ignore partial sends or receives in production code.

---

# Production Insight

Every major backend system ultimately relies on sockets:

```
Browser

↓

Socket

↓

Nginx

↓

Socket

↓

Gunicorn

↓

Socket

↓

FastAPI

↓

Socket

↓

PostgreSQL
```

Frameworks such as Flask and FastAPI hide socket management, but underneath they still use the same operating system socket APIs.

Understanding sockets helps explain how web servers, databases, proxies, message brokers, and distributed systems communicate.

---

# Questions

### Question

> What is a socket?

### Answer

A socket is an operating system abstraction that provides an endpoint for network communication between processes.

---

### Question

> Why does a server call `bind()`?

### Answer

To associate a socket with a specific IP address and port so the operating system knows where to deliver incoming connections.

---

### Question

> Why does `accept()` return a new socket?

### Answer

The listening socket continues accepting new clients, while each connected client receives its own dedicated communication socket.

---

### Question

> Why does `recv()` return bytes?

### Answer

Networks transmit raw bytes. Applications are responsible for encoding and decoding text or other data formats.

---

### Question

> Why is TCP suitable for web applications?

### Answer

Because it provides reliable, ordered, and error-checked delivery, ensuring requests and responses arrive correctly.

---

# Practical Lesson

Build a simple chat application.

Project structure:

```text
chat/

├── server.py

└── client.py
```

Implement:

- A TCP server.
- A TCP client.
- Message echoing.
- UTF-8 encoding and decoding.
- Graceful connection shutdown.

Then extend the server to support multiple sequential client connections (one client at a time).

---

# Knowledge Check

## Question 1

Why is TCP described as connection-oriented?

### Answer

Because a connection is established between the client and server before application data is exchanged.

---

## Question 2

Why should developers not assume one `recv()` call contains an entire message?

### Answer

TCP is a byte stream, not a message protocol. Large messages may arrive in multiple reads, and multiple small messages may be combined into one read.

---

## Question 3

What is the difference between the listening socket and the socket returned by `accept()`?

### Answer

The listening socket waits for new connections, while the socket returned by `accept()` is dedicated to communicating with a single connected client.

---

## Question 4

Why must applications encode strings before sending them over a socket?

### Answer

Sockets transmit bytes. Strings must be converted to bytes using an encoding such as UTF-8 before transmission.

---

## Question 5

How do sockets relate to web frameworks like FastAPI?

### Answer

FastAPI does not communicate directly with the network. It runs on servers such as Uvicorn, which use operating system sockets to receive HTTP requests and send responses.

---

# Assignment

## Exercise 1

Implement a TCP echo server and client.

Verify that messages sent by the client are echoed back correctly.

---

## Exercise 2

Modify the server to log each client's IP address and port.

---

## Exercise 3

Add socket timeouts and handle connection failures gracefully.

---

## Exercise 4

Experiment with sending messages larger than 1 KB.

Observe how many `recv()` calls are required and explain why this happens.

---

# Summary

In this lesson, you learned:

- ✅ What sockets are.
- ✅ The client-server communication model.
- ✅ The TCP socket lifecycle.
- ✅ Creating, binding, listening, accepting, sending, and receiving.
- ✅ Common socket errors.
- ✅ Why sockets are the foundation of networked applications.

---

# Next Lesson

**File:**
[77-networking-part-02-udp-sockets](77-networking-part-02-udp-sockets.md)
