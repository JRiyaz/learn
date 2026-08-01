# File: python/51-concurrency-part-11-asyncio-fundamentals.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 11: Async Programming Fundamentals - `asyncio`, Coroutines & the Event Loop

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 51
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 9–10 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `asyncio` | Python 3.4 |
| `async` / `await` syntax | Python 3.5 |
| `asyncio.run()` | Python 3.7 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why asynchronous programming exists
- The evolution from synchronous programming to async programming
- What `asyncio` is
- What a coroutine is
- The event loop
- Cooperative multitasking
- How async differs from threading and multiprocessing
- Why FastAPI is built on asyncio
- Production use cases
- Best practices
- questions

______________________________________________________________________

# Recap

So far we've explored three concurrency models.

```
Threading

↓

Concurrent execution

↓

One GIL
```

```
Multiprocessing

↓

True Parallelism

↓

Multiple Processes
```

Now we'll study the third model.

```
Async Programming
```

Unlike threading,

async programming usually uses

```
One Thread

↓

One Process

↓

Thousands of Tasks
```

______________________________________________________________________

# The Problem

Imagine a backend API.

A request arrives.

The server performs:

```
Receive Request

↓

Read Database

↓

Call Payment API

↓

Upload File

↓

Return Response
```

Notice something.

Most of the time,

the CPU is **not** working.

It is waiting.

Waiting for:

- Database
- Network
- File system
- External services

The CPU remains idle.

______________________________________________________________________

# Waiting is Expensive

Suppose a database query takes

```
100 ms
```

CPU work

```
2 ms
```

Waiting

```
98 ms
```

During those 98 milliseconds,

the CPU could have served another request.

______________________________________________________________________

# Synchronous Programming

Traditional code executes like this.

```python
data = read_database()

send_email(data)

upload_file()

print("Done")
```

Execution order

```
Database

↓

Wait

↓

Email

↓

Wait

↓

Upload

↓

Wait

↓

Finish
```

Everything waits.

______________________________________________________________________

# Real-World Analogy

Imagine a restaurant.

One waiter serves one table.

```
Take Order

↓

Stand Still

↓

Wait For Kitchen

↓

Deliver Food
```

While waiting,

the waiter ignores every other customer.

Very inefficient.

______________________________________________________________________

# Async Analogy

Now imagine a different waiter.

```
Take Order

↓

Kitchen Starts Cooking

↓

Serve Another Table

↓

Return When Food Ready
```

The waiter never stands idle.

This is the core idea behind async programming.

______________________________________________________________________

# What is Asynchronous Programming?

Asynchronous programming means:

> When one task must wait, another task is allowed to run.

Notice something important.

Tasks are **not**

running simultaneously.

Instead,

they voluntarily give up execution while waiting.

______________________________________________________________________

# Concurrency vs Parallelism

Async provides

```
Concurrency
```

not

```
Parallelism
```

Usually,

everything runs on

```
One Thread
```

There is still only one CPU executing Python code.

______________________________________________________________________

# What is `asyncio`?

`asyncio` is Python's standard asynchronous programming framework.

It provides:

- Event loop
- Coroutines
- Tasks
- Scheduling
- Networking primitives
- Synchronisation primitives

Most modern async Python frameworks build on top of `asyncio`.

Examples include:

- FastAPI
- Starlette
- Uvicorn
- aiohttp

______________________________________________________________________

# Coroutines

A coroutine is a special function that can:

- Pause
- Resume
- Cooperatively yield execution

Normal function

```python
def work():
    ...
```

Coroutine

```python
async def work():
    ...
```

Notice

```
async def
```

instead of

```
def
```

______________________________________________________________________

# First Coroutine

```python
async def hello():

    print("Hello")
```

Did it execute?

No.

It only created

a coroutine object.

______________________________________________________________________

# Coroutine Objects

```python
async def hello():

    return "Hello"


result = hello()

print(result)
```

Output

```text
<coroutine object hello at ...>
```

The function has **not** run.

______________________________________________________________________

# Why?

Calling a coroutine does **not**

execute it.

Instead,

Python creates an object representing future execution.

```
Call Coroutine

↓

Create Coroutine Object

↓

Event Loop Executes It
```

______________________________________________________________________

# Enter the Event Loop

The event loop is the heart of asyncio.

Think of it as a scheduler.

```
Task A

↓

Task B

↓

Task C

↓

Run Ready Tasks

↓

Pause Waiting Tasks

↓

Resume Later
```

The event loop continuously decides:

```
Who Runs Next?
```

______________________________________________________________________

# Running a Coroutine

```python
import asyncio


async def hello():

    print("Hello")


asyncio.run(
    hello()
)
```

Output

```text
Hello
```

`asyncio.run()` creates an event loop,

runs the coroutine,

then closes the loop.

______________________________________________________________________

# What Happens Internally?

```
asyncio.run()

↓

Create Event Loop

↓

Schedule Coroutine

↓

Execute

↓

Coroutine Finishes

↓

Close Loop
```

______________________________________________________________________

# Introducing `await`

Consider:

```python
async def work():

    await something()
```

`await` means:

> Pause this coroutine until the awaited operation completes.

Importantly,

the thread does **not** block.

Instead,

the coroutine voluntarily yields control back to the event loop.

______________________________________________________________________

# Example

```python
import asyncio


async def work():

    print("Start")

    await asyncio.sleep(2)

    print("End")


asyncio.run(work())
```

Output

```text
Start

(wait 2 seconds)

End
```

______________________________________________________________________

# Is `asyncio.sleep()` Blocking?

No.

Unlike

```python
time.sleep()
```

which blocks the thread,

```python
await asyncio.sleep()
```

allows the event loop to execute other coroutines.

______________________________________________________________________

# Visual Comparison

## Blocking Sleep

```
Thread

↓

Sleep

↓

Nothing Happens
```

______________________________________________________________________

## Async Sleep

```
Coroutine A

↓

Sleep

↓

Coroutine B Runs

↓

Coroutine C Runs

↓

Coroutine A Resumes
```

This is the key advantage of async programming.

______________________________________________________________________

# Cooperative Multitasking

Threads rely on the operating system.

```
OS Scheduler

↓

Interrupt Threads
```

Async uses a different model.

```
Coroutine

↓

await

↓

Voluntarily Pause

↓

Another Coroutine Runs
```

No forced interruption.

The coroutine decides when to yield.

______________________________________________________________________

# Why "Cooperative"?

Because every coroutine must cooperate.

If one coroutine never reaches:

```python
await
```

it blocks the event loop.

Example

```python
async def bad():

    while True:
        pass
```

Nothing else can execute.

______________________________________________________________________

# Event Loop Example

Imagine three API requests.

```
Request 1

↓

Database

↓

Waiting
```

While Request 1 waits,

```
Request 2

↓

HTTP Call
```

While Request 2 waits,

```
Request 3

↓

Read File
```

The event loop continuously switches between ready coroutines.

______________________________________________________________________

# Threading vs Async

| Threading | Async |
|------------|-------|
| OS schedules execution | Event loop schedules execution |
| Multiple threads | Usually one thread |
| Context switching | Coroutine switching |
| Preemptive | Cooperative |
| Locking required | Usually unnecessary |

______________________________________________________________________

# Multiprocessing vs Async

| Multiprocessing | Async |
|-----------------|-------|
| Multiple processes | Usually one process |
| Multiple CPU cores | One CPU core |
| True parallelism | Concurrency |
| CPU-bound | I/O-bound |

______________________________________________________________________

# When Should You Use Async?

Excellent for:

- HTTP APIs
- WebSockets
- Database queries
- Network applications
- Chat systems
- Streaming
- Proxy servers
- Reverse proxies

Poor choice for:

- Video encoding
- Image processing
- Machine learning
- Password hashing
- Heavy numerical computation

Those workloads are CPU-bound.

______________________________________________________________________

# Why FastAPI Uses Async

A FastAPI application may handle:

```
5,000 Clients
```

Most clients spend nearly all their time waiting for:

- Database queries
- External APIs
- Network responses

Instead of creating:

```
5,000 Threads
```

FastAPI creates thousands of lightweight coroutines managed by one event loop.

______________________________________________________________________

# Common Misconceptions

## Misconception 1

"Async is faster."

Not necessarily.

Async reduces waiting.

It does not make CPU calculations faster.

______________________________________________________________________

## Misconception 2

"Async uses multiple CPU cores."

Usually,

it does not.

______________________________________________________________________

## Misconception 3

"Async replaces multiprocessing."

It solves a different problem.

______________________________________________________________________

## Misconception 4

"Every function should become async."

Only functions that perform asynchronous operations should generally be coroutines.

______________________________________________________________________

# Best Practices

✅ Use async for I/O-bound workloads.

✅ Use `await` instead of blocking functions.

✅ Keep CPU-intensive work outside the event loop.

✅ Understand that async is cooperative.

❌ Don't call blocking functions inside async code.

❌ Don't assume async automatically improves every application.

______________________________________________________________________

# Production Insight

Many modern backend services combine all three concurrency models.

```
Gunicorn

↓

Multiple Worker Processes

↓

Each Worker

↓

One Event Loop

↓

Thousands of Coroutines
```

If CPU-heavy work is required,

the event loop delegates it to:

- Process pools
- Worker queues
- Celery
- Background services

Understanding when to combine these models is a hallmark of experienced backend engineers.

______________________________________________________________________

# Questions

### Question

> Why was asyncio introduced?

### Answer

To efficiently handle large numbers of I/O-bound operations without creating a thread for every task.

______________________________________________________________________

### Question

> What is a coroutine?

### Answer

A coroutine is a special function declared with `async def` that can pause and resume execution using `await`.

______________________________________________________________________

### Question

> What is the event loop?

### Answer

The event loop is the scheduler that executes coroutines, pauses them while they wait for I/O, and resumes them when
they are ready.

______________________________________________________________________

### Question

> Does async provide parallelism?

### Answer

No. Async provides concurrency, typically using a single thread and a single CPU core.

______________________________________________________________________

### Question

> Why does `await asyncio.sleep()` not block the thread?

### Answer

Because it suspends only the current coroutine and returns control to the event loop, allowing other coroutines to run.

______________________________________________________________________

# Practical Lesson

Create:

```text
asyncio_fundamentals.py
```

```python
import asyncio


async def fetch_user():

    print("Fetching user...")

    await asyncio.sleep(2)

    print("User fetched.")


async def main():

    print("Application started.")

    await fetch_user()

    print("Application finished.")


asyncio.run(main())
```

Observe:

- `fetch_user()` does not execute until it is awaited.
- `asyncio.run()` creates and manages the event loop.
- `asyncio.sleep()` suspends the coroutine without blocking the thread.

______________________________________________________________________

# Questions

## Question 1

What problem does asyncio solve?

### Answer

It improves the efficiency of I/O-bound applications by allowing other coroutines to execute while one coroutine waits
for an asynchronous operation.

______________________________________________________________________

## Question 2

What is the difference between a function and a coroutine?

### Answer

A normal function executes immediately when called, whereas calling a coroutine creates a coroutine object that must be
executed by an event loop.

______________________________________________________________________

## Question 3

What is the purpose of `await`?

### Answer

It suspends the current coroutine until the awaited asynchronous operation completes, allowing the event loop to execute
other coroutines.

______________________________________________________________________

## Question 4

How is asyncio different from threading?

### Answer

Threading relies on the operating system to schedule multiple threads, while asyncio uses an event loop to cooperatively
schedule coroutines, usually within a single thread.

______________________________________________________________________

## Question 5

Why is asyncio well suited for FastAPI?

### Answer

Because FastAPI primarily handles I/O-bound operations such as HTTP requests and database communication, allowing
thousands of concurrent requests to be managed efficiently with coroutines.

______________________________________________________________________

# Assignment

## Exercise 1

Create three coroutines:

- Download user profile
- Download user orders
- Download notifications

For now, execute them sequentially using `await`.

______________________________________________________________________

## Exercise 2

Replace `time.sleep()` with `await asyncio.sleep()`.

Observe the behavioural difference.

______________________________________________________________________

## Exercise 3

Draw a diagram illustrating how an event loop schedules three coroutines while each waits for different I/O operations.

______________________________________________________________________

## Exercise 4

Research how FastAPI, Uvicorn, and Starlette use asyncio.

Write a one-page explanation describing how an incoming HTTP request is processed from the moment it reaches the server
until a response is returned.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why asynchronous programming exists.
- ✅ What asyncio is.
- ✅ What coroutines are.
- ✅ How the event loop works.
- ✅ The purpose of `await`.
- ✅ Cooperative multitasking.
- ✅ Differences between threading, multiprocessing, and asyncio.
- ✅ Why modern Python web frameworks rely on asyncio.

______________________________________________________________________

# Next Lesson

**File:** [52-concurrency-part-12-event-loop-and-tasks](52-concurrency-part-12-event-loop-and-tasks.md)

In the next lesson, we'll dive deeper into the heart of asyncio: the **Event Loop** and **Tasks**. You'll learn how
coroutines become tasks, how the event loop schedules them, `asyncio.create_task()`, task lifecycle, cancellation, task
states, and how thousands of concurrent operations are managed efficiently in production systems.
