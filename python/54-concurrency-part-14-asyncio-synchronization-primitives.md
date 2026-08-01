# File: python/54-concurrency-part-14-asyncio-synchronization-primitives.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 14: Asyncio Synchronization Primitives (`Lock`, `Event`, `Condition`, `Semaphore`, `Queue`)

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 54
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `asyncio.Lock` | Python 3.4 |
| `asyncio.Event` | Python 3.4 |
| `asyncio.Condition` | Python 3.4 |
| `asyncio.Semaphore` | Python 3.4 |
| `asyncio.Queue` | Python 3.4 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why race conditions still exist in async programs
- Why asyncio needs synchronization primitives
- `asyncio.Lock`
- `asyncio.Event`
- `asyncio.Condition`
- `asyncio.Semaphore`
- `asyncio.BoundedSemaphore`
- `asyncio.Queue`
- Producer-consumer patterns
- Resource limiting
- Production backend examples
- Best practices
- questions

______________________________________________________________________

# Recap

One of the biggest misconceptions about asyncio is:

> "Because everything runs on one thread, race conditions cannot happen."

This is **false**.

Although only one coroutine executes Python bytecode at a time, execution switches whenever a coroutine reaches an
`await`.

That switch can occur inside what you thought was a single logical operation.

______________________________________________________________________

# A Race Condition in Async Code

Consider:

```python
counter = 0


async def increment():

    global counter

    value = counter

    await asyncio.sleep(0)

    counter = value + 1
```

Suppose two coroutines execute `increment()` concurrently.

Timeline

```
Coroutine A

Read counter = 0

↓

await


Coroutine B

Read counter = 0

↓

await


Coroutine A

counter = 1


Coroutine B

counter = 1
```

Expected:

```
2
```

Actual:

```
1
```

Exactly the same logical race condition we saw with threads.

The difference is **when** context switching occurs.

______________________________________________________________________

# Why Does This Happen?

With threads:

```
Operating System

↓

May Interrupt Anytime
```

With asyncio:

```
Coroutine

↓

await

↓

Event Loop Switches Tasks
```

The switch is cooperative,

but it still happens.

______________________________________________________________________

# Asyncio Lock

The solution is:

```python
asyncio.Lock()
```

Unlike `threading.Lock`,

this lock is designed specifically for coroutines.

______________________________________________________________________

# Creating a Lock

```python
import asyncio

lock = asyncio.Lock()
```

______________________________________________________________________

# Acquiring a Lock

```python
async with lock:

    ...
```

This is equivalent to:

```python
await lock.acquire()

try:

    ...

finally:

    lock.release()
```

The context manager is preferred.

______________________________________________________________________

# Example

```python
import asyncio

counter = 0

lock = asyncio.Lock()


async def increment():

    global counter

    async with lock:

        value = counter

        await asyncio.sleep(0)

        counter = value + 1


async def main():

    await asyncio.gather(

        increment(),

        increment()

    )

    print(counter)


asyncio.run(main())
```

Output

```text
2
```

______________________________________________________________________

# Asyncio Event

Sometimes,

coroutines don't need exclusive access.

They simply need to wait for something.

Example

```
Application Starts

↓

Load Configuration

↓

Allow Workers To Continue
```

This is what `Event` is for.

______________________________________________________________________

# Creating an Event

```python
event = asyncio.Event()
```

______________________________________________________________________

# Waiting

```python
await event.wait()
```

______________________________________________________________________

# Signalling

```python
event.set()
```

Every waiting coroutine resumes.

______________________________________________________________________

# Example

```python
import asyncio


event = asyncio.Event()


async def worker():

    print("Waiting...")

    await event.wait()

    print("Started!")


async def main():

    asyncio.create_task(worker())

    await asyncio.sleep(2)

    event.set()

    await asyncio.sleep(1)


asyncio.run(main())
```

______________________________________________________________________

# Asyncio Condition

Suppose workers should continue only when:

```
Queue Size ≥ 10
```

A lock alone cannot express this.

A condition combines:

- Lock
- Waiting
- Notification

Example

```python
condition = asyncio.Condition()
```

Waiting

```python
async with condition:

    await condition.wait()
```

Notification

```python
async with condition:

    condition.notify_all()
```

______________________________________________________________________

# Asyncio Semaphore

Suppose your application communicates with:

```
Payment API
```

The provider allows:

```
Maximum

10 Concurrent Requests
```

Should your application send

```
500 Requests
```

at once?

No.

Use:

```python
asyncio.Semaphore(10)
```

______________________________________________________________________

# Example

```python
semaphore = asyncio.Semaphore(10)


async def call_api():

    async with semaphore:

        await make_request()
```

Only ten coroutines may execute the protected section simultaneously.

______________________________________________________________________

# BoundedSemaphore

```python
asyncio.BoundedSemaphore()
```

Works like a normal semaphore,

but raises an exception if released more times than acquired.

Useful for detecting programming errors.

______________________________________________________________________

# Asyncio Queue

`asyncio.Queue`

implements the producer-consumer pattern.

Unlike

```python
queue.Queue
```

it is designed for coroutines,

not threads.

______________________________________________________________________

# Creating a Queue

```python
queue = asyncio.Queue()
```

______________________________________________________________________

# Producer

```python
await queue.put(item)
```

______________________________________________________________________

# Consumer

```python
item = await queue.get()

queue.task_done()
```

______________________________________________________________________

# Example

```python
import asyncio


async def producer(queue):

    for i in range(5):

        print(f"Produced {i}")

        await queue.put(i)


async def consumer(queue):

    while True:

        item = await queue.get()

        print(f"Consumed {item}")

        queue.task_done()


async def main():

    queue = asyncio.Queue()

    asyncio.create_task(consumer(queue))

    await producer(queue)

    await queue.join()


asyncio.run(main())
```

______________________________________________________________________

# Producer-Consumer Workflow

```
Producer

↓

Queue

↓

Consumer
```

This pattern is common in asynchronous applications.

______________________________________________________________________

# Synchronization Comparison

| Need | Primitive |
|------|-----------|
| Mutual exclusion | `Lock` |
| Broadcast signal | `Event` |
| Wait for state | `Condition` |
| Limit concurrency | `Semaphore` |
| Producer-consumer | `Queue` |

______________________________________________________________________

# Production Example

Imagine a FastAPI service processing uploaded images.

```
Incoming Requests

↓

Queue

↓

Workers

↓

Virus Scan

↓

Image Resize

↓

Cloud Upload
```

To avoid overwhelming cloud storage,

uploads are protected by

```
Semaphore(20)
```

ensuring that no more than twenty uploads happen simultaneously.

______________________________________________________________________

# Async Locks vs Thread Locks

| `threading.Lock` | `asyncio.Lock` |
|------------------|----------------|
| Blocks threads | Suspends coroutines |
| Used in multithreading | Used in asyncio |
| `with lock:` | `async with lock:` |

Never use a `threading.Lock` to synchronize coroutines running on the event loop.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using

```python
threading.Lock
```

inside async code.

______________________________________________________________________

## Mistake 2

Forgetting

```python
queue.task_done()
```

when using `asyncio.Queue`.

______________________________________________________________________

## Mistake 3

Holding a lock longer than necessary.

Keep critical sections as short as possible.

______________________________________________________________________

## Mistake 4

Using a semaphore as a mutex.

If only one coroutine should enter,

use a `Lock`.

______________________________________________________________________

# Best Practices

✅ Use `asyncio.Lock` to protect shared mutable state.

✅ Prefer `async with` over manual acquire/release.

✅ Use semaphores to limit external API usage.

✅ Use queues for producer-consumer workflows.

✅ Minimise time spent inside critical sections.

❌ Don't block the event loop while holding a lock.

______________________________________________________________________

# Production Insight

Most high-performance async services combine these primitives.

Example:

```
FastAPI

↓

Incoming Request

↓

Semaphore

↓

Database Pool

↓

Queue

↓

Background Processing

↓

Lock

↓

Shared Cache Update
```

Although the application uses only a few operating system threads,

proper synchronization remains essential for correctness.

______________________________________________________________________

# Questions

### Question

> Can asyncio programs have race conditions?

### Answer

Yes. Coroutines may interleave execution whenever they reach an `await`, leading to inconsistent updates if shared state
is not synchronized.

______________________________________________________________________

### Question

> Why use `asyncio.Lock` instead of `threading.Lock`?

### Answer

`asyncio.Lock` suspends coroutines without blocking the event loop, whereas `threading.Lock` is designed for operating
system threads.

______________________________________________________________________

### Question

> When should a semaphore be used?

### Answer

When limiting concurrent access to a finite resource such as a database connection pool or an external API.

______________________________________________________________________

### Question

> What is the purpose of `asyncio.Queue`?

### Answer

It provides asynchronous producer-consumer communication between coroutines.

______________________________________________________________________

### Question

> Why should locks protect only small sections of code?

### Answer

Long critical sections reduce concurrency and increase waiting time for other coroutines.

______________________________________________________________________

# Practical Lesson

Create:

```text
async_lock_demo.py
```

```python
import asyncio

counter = 0
lock = asyncio.Lock()


async def increment():

    global counter

    async with lock:

        current = counter

        await asyncio.sleep(0)

        counter = current + 1


async def main():

    await asyncio.gather(

        *(increment() for _ in range(100))
    )

    print(counter)


asyncio.run(main())
```

Run the example with and without the lock.

Observe how synchronization affects the final value.

______________________________________________________________________

# Questions

## Question 1

Can race conditions occur in asyncio?

### Answer

Yes. They occur when multiple coroutines access shared mutable state and yield execution at `await` points before
completing a logical operation.

______________________________________________________________________

## Question 2

Why is `asyncio.Lock` non-blocking?

### Answer

Because waiting coroutines are suspended by the event loop instead of blocking the operating system thread.

______________________________________________________________________

## Question 3

When should `asyncio.Queue` be preferred?

### Answer

For asynchronous producer-consumer workflows where coroutines exchange work items safely.

______________________________________________________________________

## Question 4

What is the difference between `Semaphore` and `Lock`?

### Answer

A lock allows only one coroutine into a critical section, whereas a semaphore allows a configurable number of concurrent
entrants.

______________________________________________________________________

## Question 5

How is `asyncio.Semaphore` commonly used in backend applications?

### Answer

To limit concurrent access to rate-limited services, connection pools, or expensive shared resources.

______________________________________________________________________

# Assignment

## Exercise 1

Create 100 coroutines that increment a shared counter.

Run the program:

- Without a lock
- With `asyncio.Lock`

Compare the results.

______________________________________________________________________

## Exercise 2

Build a producer-consumer application using `asyncio.Queue`.

Use:

- Three producers
- Five consumers

Measure throughput.

______________________________________________________________________

## Exercise 3

Simulate an external API that allows only five concurrent requests.

Use `asyncio.Semaphore` to enforce the limit.

______________________________________________________________________

## Exercise 4

Take one of your FastAPI projects.

Identify where you would use:

- `Lock`
- `Semaphore`
- `Queue`

Explain why each primitive is appropriate.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why race conditions still exist in asyncio.
- ✅ How `asyncio.Lock` protects shared state.
- ✅ How `Event` coordinates coroutines.
- ✅ How `Condition` waits for state changes.
- ✅ How `Semaphore` limits concurrency.
- ✅ How `Queue` implements asynchronous producer-consumer workflows.
- ✅ Production synchronization patterns used in modern async services.

______________________________________________________________________

# Next Lesson

**File:**
[55-concurrency-part-15-asyncio-timeouts-cancellation-and-shielding](55-concurrency-part-15-asyncio-timeouts-cancellation-and-shielding.md)

In the next lesson, we'll cover one of the most important topics for production async systems: **timeouts, cancellation,
and shielding**. You'll learn how `asyncio.wait_for()`, `asyncio.timeout()`, `asyncio.shield()`, and cooperative
cancellation work, why client disconnects cancel tasks, and how to write cancellation-safe code in FastAPI and other
asyncio-based services.
