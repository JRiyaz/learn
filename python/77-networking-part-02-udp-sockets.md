# File: python/77-networking-part-02-udp-sockets.md

# Computer Networking
# Part 2: UDP Sockets – Fast, Connectionless Communication

> **Course:** Backend Engineering Roadmap
>
> **Module:** Computer Networking & Sockets
>
> **Lesson:** 77
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- What UDP is
- UDP vs TCP
- Datagram communication
- Connectionless networking
- UDP sockets in Python
- Sending and receiving datagrams
- Packet loss
- Packet ordering
- Broadcast communication
- When to use UDP
- Production best practices

---

# Recap

In the previous lesson, we built a TCP server and client.

TCP provides:

- Reliable delivery
- Ordered packets
- Retransmission
- Flow control
- Connection establishment

However, reliability comes with overhead.

Many applications prefer **speed over reliability**.

Examples include:

- Live video streaming
- Online gaming
- DNS
- Voice calls
- Service discovery

These commonly use **UDP**.

---

# What is UDP?

UDP (User Datagram Protocol) is a connectionless transport protocol.

Unlike TCP:

- No connection is established.
- No retransmission occurs.
- No delivery guarantee exists.
- Packet order is not guaranteed.

Instead, data is sent as independent **datagrams**.

```
Application

↓

UDP Socket

↓

Network

↓

UDP Socket

↓

Application
```

---

# TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Yes | No |
| Reliable delivery | Yes | No |
| Packet ordering | Yes | No |
| Retransmission | Yes | No |
| Speed | Moderate | High |
| Streaming | Byte stream | Datagram |
| Typical use | HTTP, PostgreSQL | DNS, VoIP, Gaming |

---

# Why Use UDP?

Suppose you're watching a live football match.

If one video packet is lost:

```
Frame 103 ❌

↓

Continue Playing
```

It's better to skip a frame than pause the video while waiting for retransmission.

TCP would retransmit.

UDP simply continues.

---

# UDP Socket Lifecycle

A UDP server follows a much simpler lifecycle:

```
socket()

↓

bind()

↓

recvfrom()

↓

sendto()

↓

close()
```

Notice what's missing:

- `listen()`
- `accept()`
- `connect()` (optional for UDP)

There is no persistent connection.

---

# Creating a UDP Socket

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)
```

The only difference from TCP is:

```python
SOCK_DGRAM
```

which creates a UDP socket.

---

# Binding

A UDP server still binds to an address and port.

```python
server.bind(("127.0.0.1", 9000))
```

The operating system delivers UDP datagrams sent to that port.

---

# Receiving Data

```python
data, address = server.recvfrom(1024)
```

Unlike TCP:

- The sender's address is returned with each datagram.
- There is no dedicated client socket.

---

# Sending Data

```python
server.sendto(
    b"Hello",
    address,
)
```

The destination address must be supplied for every datagram.

---

# UDP Server Example

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)

server.bind(("127.0.0.1", 9000))

print("Waiting for datagrams...")

while True:
    data, address = server.recvfrom(1024)

    print(
        f"{address}: {data.decode()}"
    )

    server.sendto(
        b"Received",
        address,
    )
```

---

# UDP Client Example

```python
import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)

client.sendto(
    b"Hello Server",
    ("127.0.0.1", 9000),
)

data, _ = client.recvfrom(1024)

print(data.decode())

client.close()
```

---

# Datagram Behaviour

Each call to:

```python
sendto()
```

creates one datagram.

```
Datagram 1

Datagram 2

Datagram 3
```

The receiver may receive:

```
1

3

2
```

or

```
1

2
```

if one packet is lost.

Applications using UDP must tolerate this.

---

# Packet Loss

Unlike TCP:

```
Sender

↓

Packet Lost

↓

Receiver Never Gets It
```

No automatic retry occurs.

If reliability is required, the application must implement it.

---

# Broadcast Communication

UDP supports broadcasting.

One sender can transmit to multiple receivers on the local network.

Example use cases:

- Device discovery
- Multiplayer game discovery
- Network services

---

# Backend Examples

Although most REST APIs use TCP, backend engineers encounter UDP frequently.

Examples:

- DNS lookups
- Service discovery protocols
- Metrics collection
- Telemetry
- Monitoring agents

Understanding UDP helps explain why these systems prioritise low latency over guaranteed delivery.

---

# Common Mistakes

## Mistake 1

Assuming packets always arrive.

---

## Mistake 2

Assuming packets arrive in order.

---

## Mistake 3

Sending messages larger than the network can efficiently handle.

---

## Mistake 4

Using UDP when reliable delivery is required.

---

## Mistake 5

Treating UDP like TCP.

---

# Best Practices

✅ Use UDP only when occasional packet loss is acceptable.

✅ Keep datagrams reasonably small.

✅ Validate received data.

✅ Design application protocols to tolerate missing packets.

❌ Don't assume delivery.

❌ Don't assume ordering.

---

# Production Insight

Many distributed systems use both protocols.

```
Browser

↓

HTTP (TCP)

↓

Application

↓

DNS Query (UDP)

↓

DNS Server

↓

Database (TCP)
```

A single request may involve both TCP and UDP, each chosen for its strengths.

---

# Questions

### Question

> Why doesn't UDP require `listen()` or `accept()`?

### Answer

Because UDP is connectionless. The server receives independent datagrams rather than maintaining dedicated client connections.

---

### Question

> Why does `recvfrom()` return the sender's address?

### Answer

Since there is no established connection, the server must know where to send the reply.

---

### Question

> Why is UDP faster than TCP?

### Answer

It avoids connection establishment, acknowledgements, retransmissions, and ordering guarantees, reducing protocol overhead.

---

### Question

> When should UDP be avoided?

### Answer

When reliable, ordered delivery is essential, such as file transfers, HTTP requests, or database communication.

---

### Question

> Can UDP packets arrive out of order?

### Answer

Yes. The network may deliver packets in a different order or drop them entirely.

---

# Practical Lesson

Build:

```text
udp_chat/

├── server.py

└── client.py
```

Implement:

- A UDP echo server.
- A UDP client.
- Message logging.
- Handling of multiple clients.
- Graceful shutdown.

Then intentionally stop the server while the client is running and observe how UDP behaves compared with TCP.

---

# Knowledge Check

## Question 1

What is the primary advantage of UDP?

### Answer

Low latency and minimal protocol overhead, making it suitable for time-sensitive communication.

---

## Question 2

Why can't applications rely on UDP packet ordering?

### Answer

The protocol provides no ordering guarantees; packets may arrive out of sequence or not at all.

---

## Question 3

What is a datagram?

### Answer

A self-contained packet of data sent independently over the network using UDP.

---

## Question 4

Why is DNS commonly implemented over UDP?

### Answer

DNS queries and responses are typically small, and avoiding TCP's connection overhead reduces latency for frequent lookups.

---

## Question 5

How should applications handle important data when using UDP?

### Answer

If reliable delivery is required, the application must implement acknowledgements, retries, sequencing, or choose TCP instead.

---

# Assignment

## Exercise 1

Build a UDP echo server and client.

---

## Exercise 2

Extend the server to log the IP address and port of every sender.

---

## Exercise 3

Modify the client to send 100 datagrams and observe how the server processes them.

---

## Exercise 4

Research one real-world protocol that uses UDP (for example, DNS or DHCP) and explain why UDP is more suitable than TCP for that protocol.

---

# Summary

In this lesson, you learned:

- ✅ What UDP is.
- ✅ How it differs from TCP.
- ✅ Creating UDP sockets.
- ✅ Sending and receiving datagrams.
- ✅ Packet loss and ordering.
- ✅ Broadcast communication.
- ✅ Production use cases for UDP.

---

# Next Lesson

**File:**
[78-networking-part-03-multi-client-tcp-server](78-networking-part-03-multi-client-tcp-server.md)
