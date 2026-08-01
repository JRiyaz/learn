# File: python/79-networking-part-04-non-blocking-sockets-and-selectors.md

# Computer Networking

# Part 4: Non-Blocking Sockets & Selectors – Building High-Concurrency Servers

> **Course:** Backend Engineering Roadmap
>
> **Module:** Computer Networking & Sockets
>
> **Lesson:** 79
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 16–20 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why thread-per-client servers do not scale indefinitely
- Blocking vs non-blocking sockets
- What I/O multiplexing is
- The `selectors` module
- Event-driven programming
- Read and write events
- Building a multi-client event loop
- How `selectors` relates to `asyncio`
- Operating system polling mechanisms
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we built a multi-client server using threads.

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

This architecture works well for hundreds of clients.

But what happens when:

```
100,000 Clients
```

Creating:

```
100,000 Threads
```

is impractical.

Instead of creating more threads, modern servers use **event-driven I/O**.

______________________________________________________________________

# The Problem with Blocking Sockets

Remember:

```python
data = client.recv(1024)
```

If no data exists:

```
Thread

↓

Wait

↓

Wait

↓

Wait

↓

Data Arrives
```

The thread does nothing while waiting.

Imagine thousands of idle clients.

Thousands of threads are sleeping.

Most server resources are wasted.

______________________________________________________________________

# Blocking I/O

```
Client

↓

recv()

↓

Thread Stops

↓

Data Arrives

↓

Continue
```

Every blocking call consumes a thread.

______________________________________________________________________

# Non-Blocking I/O

Instead:

```
recv()

↓

No Data

↓

Immediately Return

↓

Continue Doing Other Work
```

The application never waits unnecessarily.

______________________________________________________________________

# Creating a Non-Blocking Socket

```python
server.setblocking(False)
```

Now:

```python
accept()
```

or

```python
recv()
```

will no longer wait.

If no data exists:

```
BlockingIOError
```

is raised immediately.

______________________________________________________________________

# Why Non-Blocking Alone Isn't Enough

Imagine:

```python
while True:

    try:

        data = client.recv(1024)

    except BlockingIOError:

        pass
```

This becomes:

```
CPU

↓

Check

↓

Check

↓

Check

↓

Check
```

called **busy waiting**.

CPU usage becomes extremely high.

We need a better solution.

______________________________________________________________________

# Enter Selectors

Instead of repeatedly checking every socket:

```
Socket 1?

Socket 2?

Socket 3?

Socket 4?
```

Ask the operating system:

> "Tell me when any socket is ready."

This is exactly what **selectors** does.

______________________________________________________________________

# What is a Selector?

A selector waits until one or more sockets become ready for I/O.

```
Sockets

↓

Selector

↓

Ready Socket

↓

Application
```

No CPU is wasted checking idle sockets.

______________________________________________________________________

# The selectors Module

Python provides:

```python
import selectors
```

Create:

```python
selector = selectors.DefaultSelector()
```

`DefaultSelector` automatically chooses the best implementation for your operating system.

______________________________________________________________________

# Registering a Socket

```python
selector.register(

    server,

    selectors.EVENT_READ
)
```

This tells the selector:

> Notify me when this socket becomes readable.

______________________________________________________________________

# Waiting for Events

```python
events = selector.select()
```

Unlike busy waiting:

```
Application

↓

Sleep

↓

Operating System

↓

Socket Ready

↓

Wake Up
```

The application sleeps efficiently until work exists.

______________________________________________________________________

# Event Types

Most socket servers use:

```python
EVENT_READ
```

Data can be read.

and

```python
EVENT_WRITE
```

Data can be written.

______________________________________________________________________

# Accepting New Clients

Suppose:

```
Listening Socket

↓

Readable
```

For a listening socket:

```
Readable

↓

New Connection Waiting
```

We call:

```python
accept()
```

______________________________________________________________________

# Registering Client Sockets

After accepting:

```python
client.setblocking(False)
```

Register:

```python
selector.register(

    client,

    selectors.EVENT_READ
)
```

Now the selector watches both:

- Server socket
- Client sockets

______________________________________________________________________

# Event Loop

The server continuously waits for events.

```
select()

↓

Socket Ready?

↓

Handle Event

↓

Repeat
```

Only sockets with work pending are processed.

______________________________________________________________________

# Minimal Event Loop

```python
while True:

    events = selector.select()

    for key, mask in events:

        callback = key.data

        callback(key.fileobj)
```

Each socket has an associated callback function.

______________________________________________________________________

# Complete Server Architecture

```
                 Selector

                     │

      ┌──────────────┼──────────────┐

      ▼              ▼              ▼

 Server Socket   Client A      Client B

                     │              │

                 recv()         recv()

                     │              │

                 send()         send()
```

One thread.

Many connections.

______________________________________________________________________

# Why This Scales

Thread-per-client:

```
10,000 Clients

↓

10,000 Threads
```

Selector model:

```
10,000 Clients

↓

1 Thread

↓

Selector
```

Memory usage drops dramatically.

Context switching almost disappears.

______________________________________________________________________

# Behind the Scenes

`DefaultSelector` chooses different OS APIs.

Linux:

```
epoll
```

macOS:

```
kqueue
```

Windows:

```
select()
```

Python hides these differences behind one interface.

______________________________________________________________________

# Callback Example

```python
def accept(

    server

):

    client, address = server.accept()

    client.setblocking(False)

    selector.register(

        client,

        selectors.EVENT_READ,

        read
    )
```

Every client receives:

```python
read()
```

when data arrives.

______________________________________________________________________

# Reading Client Data

```python
def read(

    client

):

    data = client.recv(1024)

    if data:

        client.send(data)

    else:

        selector.unregister(client)

        client.close()
```

Notice:

No thread creation.

No blocking.

______________________________________________________________________

# Event-Driven Programming

Traditional:

```
Call Function

↓

Wait

↓

Continue
```

Event-driven:

```
Wait For Event

↓

Execute Callback

↓

Return To Event Loop
```

The flow is inverted.

This programming model is the foundation of many modern frameworks.

______________________________________________________________________

# selectors and asyncio

The event loop inside:

```python
asyncio
```

uses the same fundamental idea.

```
asyncio

↓

Selector

↓

epoll / kqueue / IOCP

↓

Operating System
```

Understanding selectors makes `asyncio` much easier to understand.

______________________________________________________________________

# Backend Example

Consider Uvicorn.

```
Socket

↓

Selector

↓

Event Loop

↓

HTTP Request

↓

FastAPI

↓

HTTP Response
```

Thousands of connections are handled by a small number of threads.

______________________________________________________________________

# Threads vs Selectors

| Thread-per-Client | Selectors |
|-------------------|-----------|
| Many threads | Few threads |
| Blocking I/O | Non-blocking I/O |
| High memory usage | Low memory usage |
| Context switching | Minimal switching |
| Easier to understand | More complex |
| Moderate scalability | Very high scalability |

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using non-blocking sockets without a selector.

______________________________________________________________________

## Mistake 2

Busy waiting in a loop.

______________________________________________________________________

## Mistake 3

Forgetting to unregister closed sockets.

______________________________________________________________________

## Mistake 4

Blocking inside callback functions.

______________________________________________________________________

## Mistake 5

Assuming selectors eliminate all scalability limits.

CPU-intensive work still requires worker threads or processes.

______________________________________________________________________

# Best Practices

✅ Use `DefaultSelector`.

✅ Keep callbacks short.

✅ Remove disconnected clients promptly.

✅ Avoid blocking operations inside the event loop.

✅ Offload CPU-intensive work to executors or worker processes.

❌ Don't mix blocking socket calls into an event-driven server.

❌ Don't perform long database queries synchronously inside callbacks.

______________________________________________________________________

# Production Insight

Modern network servers are almost universally event-driven.

Examples include:

```
Nginx

↓

epoll
```

```
HAProxy

↓

epoll
```

```
Redis

↓

epoll
```

```
Node.js

↓

libuv

↓

epoll / kqueue / IOCP
```

```
Uvicorn

↓

asyncio

↓

selectors

↓

epoll / kqueue
```

Although the implementations differ, the underlying idea is the same:

> Wait efficiently until the operating system reports that work is available.

______________________________________________________________________

# Questions

### Question

> Why do blocking sockets limit scalability?

### Answer

Because each blocked socket typically occupies a thread that cannot perform other work while waiting for network
activity.

______________________________________________________________________

### Question

> What problem does a selector solve?

### Answer

A selector allows one thread to efficiently monitor many sockets and wake up only when one or more become ready for I/O.

______________________________________________________________________

### Question

> Why is busy waiting inefficient?

### Answer

Because it repeatedly checks sockets even when no work exists, wasting CPU time.

______________________________________________________________________

### Question

> Why should callbacks remain short?

### Answer

While one callback is executing, the event loop cannot process other ready events. Long-running callbacks reduce
responsiveness.

______________________________________________________________________

### Question

> How does `selectors.DefaultSelector()` improve portability?

### Answer

It automatically chooses the most appropriate I/O multiplexing mechanism for the current operating system.

______________________________________________________________________

# Practical Lesson

Create:

```text
event_server/

├── server.py

└── client.py
```

Implement:

- A non-blocking TCP server.
- A selector-based event loop.
- Client registration.
- Echo functionality.
- Client disconnection handling.
- Proper socket cleanup.

Then connect multiple terminal clients simultaneously and verify that:

- One server thread handles every connection.
- No additional threads are created for each client.
- Idle clients consume minimal CPU resources.

______________________________________________________________________

# Knowledge Check

## Question 1

Why do event-driven servers generally scale better than thread-per-client servers?

### Answer

Because they can manage many concurrent connections using a small number of threads, avoiding excessive memory usage and
context switching.

______________________________________________________________________

## Question 2

What role does the operating system play in a selector-based server?

### Answer

The operating system monitors sockets and notifies the application only when I/O operations can proceed without
blocking.

______________________________________________________________________

## Question 3

Why is `selectors` considered an abstraction layer?

### Answer

Because it presents a consistent Python interface while using different platform-specific mechanisms such as `epoll`,
`kqueue`, or `select()` underneath.

______________________________________________________________________

## Question 4

Why should blocking operations be avoided inside the event loop?

### Answer

A blocking operation prevents the event loop from processing other ready sockets, reducing throughput and increasing
latency.

______________________________________________________________________

## Question 5

How does this lesson prepare you for learning `asyncio`?

### Answer

`asyncio` builds on the same event-driven model, using selectors internally to schedule and manage asynchronous I/O
operations efficiently.

______________________________________________________________________

# Assignment

## Exercise 1

Convert your thread-per-client echo server into a selector-based server.

______________________________________________________________________

## Exercise 2

Add logging that records when sockets are:

- Registered.
- Ready for reading.
- Closed.
- Unregistered.

______________________________________________________________________

## Exercise 3

Modify the server to broadcast messages to all connected clients using a single event loop.

______________________________________________________________________

## Exercise 4

Compare the resource usage of:

- Thread-per-client server.
- Selector-based server.

Measure:

- Thread count.
- Memory usage.
- CPU utilisation.

Explain why the selector-based implementation scales more effectively.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why blocking sockets limit scalability.
- ✅ How non-blocking sockets work.
- ✅ What I/O multiplexing is.
- ✅ Using Python's `selectors` module.
- ✅ Building an event-driven server.
- ✅ The relationship between selectors and `asyncio`.
- ✅ Why modern web servers use event loops.
- ✅ Production best practices for high-concurrency network applications.

______________________________________________________________________

# Next Lesson

**File:** [80-networking-part-05-websockets](80-networking-part-05-websockets.md)
