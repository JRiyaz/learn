# File: python/78-networking-part-03-multi-client-tcp-server.md

# Computer Networking
# Part 3: Building a Multi-Client TCP Server – Handling Multiple Connections

> **Course:** Backend Engineering Roadmap
>
> **Module:** Computer Networking & Sockets
>
> **Lesson:** 78
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 14–16 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why single-client servers are insufficient
- How operating systems handle multiple connections
- Sequential vs concurrent servers
- Thread-per-client architecture
- Client handler functions
- Thread lifecycle
- Daemon threads
- Thread pools for socket servers
- Graceful server shutdown
- Common concurrency issues
- Production best practices

---

# Recap

In the previous lessons, we built TCP and UDP servers.

Our TCP server looked like this:

```python
server.accept()

↓

Handle Client

↓

Client Disconnects

↓

server.accept()
```

It worked perfectly.

But only for **one client at a time**.

---

# The Problem

Imagine two users connecting.

```
Client A

↓

Talking To Server
```

While:

```
Client B

↓

Waiting...
```

The server cannot serve Client B until Client A disconnects.

For a real backend application, this is unacceptable.

---

# Real Backend Servers

Consider:

- FastAPI
- Flask
- PostgreSQL
- Redis
- Nginx

Thousands of clients may connect simultaneously.

```
Client 1

Client 2

Client 3

...

Client 10,000

↓

Server
```

The server must handle many connections concurrently.

---

# Sequential Server

A simple TCP server follows this pattern.

```
accept()

↓

Handle Client

↓

Close Client

↓

Repeat
```

Only one client is processed at any given time.

---

# Concurrent Server

Instead:

```
accept()

↓

Create Thread

↓

accept()

↓

Create Thread

↓

accept()

↓

Create Thread
```

Each client receives its own execution context.

---

# Thread-per-Client Model

This is one of the oldest and easiest concurrency models.

```
Main Thread

↓

accept()

↓

Thread A

↓

Client A
```

```
Main Thread

↓

accept()

↓

Thread B

↓

Client B
```

Each client communicates independently.

---

# Server Architecture

```
               Main Thread

                    │

         accept() new connection

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

 Client Thread   Client Thread   Client Thread

      │             │             │

  recv/send     recv/send     recv/send
```

The main thread accepts connections.

Worker threads perform communication.

---

# Client Handler Function

Instead of placing communication logic inside the main loop, move it into a separate function.

```python
def handle_client(

    client,

    address

):

    print(

        f"Connected: {address}"

    )

    while True:

        data = client.recv(1024)

        if not data:

            break

        client.send(data)

    client.close()
```

Each thread executes this function independently.

---

# Starting a Thread

```python
import threading

thread = threading.Thread(

    target=handle_client,

    args=(client, address)

)

thread.start()
```

The server immediately returns to:

```python
accept()
```

allowing additional clients to connect.

---

# Complete Multi-Client Server

```python
import socket
import threading


def handle_client(

    client,

    address

):

    print(

        f"{address} connected"

    )

    while True:

        data = client.recv(1024)

        if not data:
            break

        client.send(data)

    client.close()


server = socket.socket(

    socket.AF_INET,

    socket.SOCK_STREAM

)

server.bind(("127.0.0.1", 8000))

server.listen()

print("Server started")

while True:

    client, address = server.accept()

    thread = threading.Thread(

        target=handle_client,

        args=(client, address)

    )

    thread.start()
```

Now multiple clients can communicate simultaneously.

---

# What Happens Internally?

Suppose three clients connect.

```
Main Thread

↓

accept()

↓

Thread 1

↓

Client A
```

```
Main Thread

↓

accept()

↓

Thread 2

↓

Client B
```

```
Main Thread

↓

accept()

↓

Thread 3

↓

Client C
```

Each thread blocks independently while waiting for network data.

---

# Why Threads Work Well Here

Remember the GIL lesson.

Threads are not ideal for CPU-intensive work.

However:

```
recv()

↓

Waiting

↓

Operating System
```

During blocking I/O operations, Python releases the GIL.

This allows other threads to continue executing.

This is why thread-per-client servers can scale surprisingly well for moderate workloads.

---

# Daemon Threads

Threads can be marked as daemon threads.

```python
thread = threading.Thread(

    target=handle_client,

    daemon=True

)
```

Daemon threads terminate automatically when the main program exits.

Useful for experiments.

Less common for production servers where graceful shutdown is preferred.

---

# Problems with Thread-per-Client

Imagine:

```
10 Clients

↓

10 Threads
```

Fine.

Now imagine:

```
50,000 Clients

↓

50,000 Threads
```

Problems:

- High memory usage.
- Context switching overhead.
- Scheduler pressure.
- Longer startup time.
- Reduced scalability.

Eventually the operating system becomes the bottleneck.

---

# Thread Pools

Instead of unlimited threads:

```
100 Worker Threads

↓

Queue

↓

Thousands Of Clients
```

Worker threads are reused.

Python provides:

```python
ThreadPoolExecutor
```

Although simple socket servers often create threads manually, thread pools are useful when tasks are short-lived.

---

# Graceful Shutdown

Avoid terminating the server abruptly.

Instead:

```
Stop Accepting Clients

↓

Finish Existing Requests

↓

Close Client Sockets

↓

Close Listening Socket

↓

Exit
```

Graceful shutdown prevents lost data and corrupted connections.

---

# Socket Timeouts

A client may stop responding.

Instead of blocking forever:

```python
client.settimeout(30)
```

If no data arrives within 30 seconds:

```python
socket.timeout
```

is raised.

This prevents idle clients from occupying server resources indefinitely.

---

# Broadcasting Messages

Suppose we're writing a chat server.

```
Alice

↓

Server

↓

Bob
```

```
Alice

↓

Server

↓

Charlie
```

The server must maintain a collection of connected clients.

Example:

```python
clients = []
```

Each client socket is added when connected and removed when disconnected.

---

# Shared State

Once multiple threads exist:

```python
clients.append(

    client

)
```

becomes shared state.

Multiple threads may modify the list simultaneously.

Potential issues:

- Race conditions.
- Lost updates.
- Inconsistent state.

Locks may be required.

---

# Backend Example

Imagine a notification server.

```
Users

↓

Socket Server

↓

Worker Threads

↓

Redis

↓

Database
```

Each thread handles one user's connection.

The backend services remain shared.

---

# Architecture Limitations

Thread-per-client is excellent for:

- Learning.
- Internal tools.
- Small servers.
- Moderate traffic.

Modern high-performance servers often use:

- Event loops.
- Non-blocking sockets.
- `selectors`
- `epoll`
- `kqueue`
- `IOCP`
- `asyncio`

These allow tens of thousands of concurrent connections with relatively few threads.

We'll study those in the next lesson.

---

# Common Mistakes

## Mistake 1

Creating unlimited threads.

---

## Mistake 2

Ignoring socket timeouts.

---

## Mistake 3

Not closing client sockets.

---

## Mistake 4

Sharing mutable state without synchronization.

---

## Mistake 5

Performing long CPU-intensive work inside client threads.

---

# Best Practices

✅ Separate client handling into its own function.

✅ Close sockets in `finally` blocks where appropriate.

✅ Configure timeouts.

✅ Log client connections and disconnections.

✅ Protect shared state with synchronization primitives when necessary.

❌ Don't create unbounded numbers of threads.

❌ Don't ignore exceptions inside worker threads.

---

# Production Insight

Historically, many web servers used a thread-per-client model.

Examples include:

- Early Java servlet containers.
- Older Python socket servers.
- Many internal enterprise applications.

Modern servers have largely moved toward event-driven architectures.

Examples:

```
Nginx

↓

epoll

↓

Thousands Of Connections
```

```
Uvicorn

↓

asyncio

↓

Thousands Of Connections
```

Nevertheless, understanding the thread-per-client model is valuable because it clearly illustrates how concurrent servers evolved and why event loops became necessary.

---

# Questions

### Question

> Why can't a sequential server handle many clients efficiently?

### Answer

Because it blocks while communicating with one client, preventing other clients from being served until the current interaction completes.

---

### Question

> Why does creating one thread per client improve responsiveness?

### Answer

Each client can block independently while waiting for network I/O, allowing the server to continue accepting and servicing other connections.

---

### Question

> Why are socket servers often I/O-bound rather than CPU-bound?

### Answer

Most of their time is spent waiting for data to arrive over the network rather than performing intensive computations.

---

### Question

> What problem appears when thousands of threads are created?

### Answer

Memory consumption, context switching, and operating system scheduling overhead increase significantly, reducing scalability.

---

### Question

> Why do modern servers often avoid the thread-per-client model?

### Answer

Because event-driven architectures can handle far more concurrent connections with fewer threads and lower resource usage.

---

# Practical Lesson

Create:

```text
chat_server/

├── server.py

└── client.py
```

Implement:

- A TCP server.
- Thread-per-client architecture.
- A client handler function.
- Logging of client connections.
- Socket timeouts.
- Graceful client disconnection.

Then extend the server to:

- Maintain a list of connected clients.
- Broadcast messages received from one client to every other connected client.
- Protect the shared client list with a lock.

Finally, connect three terminal windows simultaneously and verify that messages are broadcast correctly.

---

# Knowledge Check

## Question 1

Why is a dedicated client handler function preferable to putting all logic in the main loop?

### Answer

It separates connection acceptance from client communication, making the server easier to maintain and allowing each client to execute independently.

---

## Question 2

Why do threads perform reasonably well for socket servers despite the GIL?

### Answer

Because blocking socket operations release the GIL, allowing other threads to continue processing network I/O.

---

## Question 3

Why can broadcasting messages introduce race conditions?

### Answer

Multiple client threads may modify or iterate over the shared collection of connected clients simultaneously.

---

## Question 4

When should a thread pool be considered?

### Answer

When many short-lived tasks need to be processed while limiting the number of active threads.

---

## Question 5

Why is graceful shutdown important?

### Answer

It allows active connections to complete cleanly, releases resources properly, and prevents abrupt termination of client communications.

---

# Assignment

## Exercise 1

Convert your single-client TCP server into a thread-per-client server.

---

## Exercise 2

Implement a simple multi-client chat server with broadcasting.

---

## Exercise 3

Add logging that records:

- Client IP address.
- Connection time.
- Disconnection time.
- Number of bytes received.

---

## Exercise 4

Stress-test the server by connecting multiple clients simultaneously.

Observe CPU usage, memory consumption, and thread count.

Explain why this architecture eventually becomes inefficient as the number of concurrent clients grows.

---

# Summary

In this lesson, you learned:

- ✅ Why sequential servers are limited.
- ✅ How the thread-per-client model works.
- ✅ Creating worker threads for socket communication.
- ✅ Thread lifecycle.
- ✅ Socket timeouts.
- ✅ Shared state challenges.
- ✅ Thread pools.
- ✅ Why modern servers prefer event-driven architectures.

---

# Next Lesson

**File:**
[79-networking-part-04-non-blocking-sockets-and-selectors](79-networking-part-04-non-blocking-sockets-and-selectors.md)
