# File: python/55-concurrency-part-15-asyncio-timeouts-cancellation-and-shielding.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 15: Timeouts, Cancellation & Shielding in `asyncio`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 55
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `asyncio.wait_for()` | Python 3.4 |
| `asyncio.shield()` | Python 3.4 |
| `asyncio.timeout()` | Python 3.11 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why timeouts are essential
- Cooperative cancellation
- `asyncio.wait_for()`
- `asyncio.timeout()`
- `asyncio.shield()`
- Cancellation propagation
- Writing cancellation-safe coroutines
- Cleanup with `try`/`finally`
- Production timeout strategies
- FastAPI cancellation behaviour
- Best practices
- questions

______________________________________________________________________

# Recap

Async applications spend much of their time waiting.

But waiting forever is rarely acceptable.

Imagine:

```
Client

↓

HTTP Request

↓

External Payment API

↓

Never Responds
```

Without a timeout:

- Memory remains allocated.
- Database connections stay open.
- The client may wait indefinitely.
- The event loop wastes resources.

Production systems must assume that every network call can fail or stall.

______________________________________________________________________

# Why Timeouts Matter

Consider an endpoint that performs:

1. Read from PostgreSQL
1. Call a payment provider
1. Store audit logs
1. Return a response

If the payment provider never replies, should the request remain active forever?

No.

Every external dependency should have an appropriate timeout.

______________________________________________________________________

# Cooperative Cancellation

Unlike threads, asyncio does not forcibly terminate a coroutine.

Instead, cancellation is **cooperative**.

When you call:

```python
task.cancel()
```

the event loop schedules a cancellation.

At the next suspension point (typically an `await`), the coroutine receives:

```python
asyncio.CancelledError
```

The coroutine can then:

- Perform cleanup
- Release resources
- Re-raise the exception

______________________________________________________________________

# Example

```python
import asyncio


async def worker():

    try:

        while True:

            print("Working...")

            await asyncio.sleep(1)

    except asyncio.CancelledError:

        print("Cleaning up resources...")

        raise


async def main():

    task = asyncio.create_task(worker())

    await asyncio.sleep(3)

    task.cancel()

    try:

        await task

    except asyncio.CancelledError:

        print("Task cancelled.")


asyncio.run(main())
```

______________________________________________________________________

# `asyncio.wait_for()`

`wait_for()` applies a timeout to an awaitable.

```python
await asyncio.wait_for(

    fetch_data(),

    timeout=5
)
```

If five seconds pass,

`asyncio.TimeoutError` is raised.

Internally,

`wait_for()` also cancels the underlying task.

______________________________________________________________________

# Timeline

```
Task Starts

↓

5 Seconds

↓

Timeout

↓

Cancel Task

↓

Raise TimeoutError
```

______________________________________________________________________

# Example

```python
import asyncio


async def slow():

    await asyncio.sleep(10)


async def main():

    try:

        await asyncio.wait_for(

            slow(),

            timeout=2

        )

    except asyncio.TimeoutError:

        print("Operation timed out.")


asyncio.run(main())
```

______________________________________________________________________

# `asyncio.timeout()` (Python 3.11+)

Python 3.11 introduced a cleaner timeout API.

```python
async with asyncio.timeout(2):

    await fetch_user()

    await fetch_orders()
```

Every await inside the block shares the timeout budget.

This is often more readable than nesting multiple `wait_for()` calls.

______________________________________________________________________

# `asyncio.shield()`

Sometimes a task must continue even if the caller is cancelled.

Example:

- Writing an audit log
- Finalising a financial transaction
- Committing a database transaction

`shield()` prevents the wrapped awaitable from being cancelled by the surrounding cancellation.

```python
await asyncio.shield(commit_transaction())
```

If the outer coroutine is cancelled, the commit can still complete.

______________________________________________________________________

# Cancellation Propagation

Consider:

```
Task A

↓

await Task B
```

If Task A is cancelled,

Task B is usually cancelled as well.

Cancellation propagates through await chains unless shielding or other control mechanisms are used.

______________________________________________________________________

# Writing Cancellation-Safe Code

Always assume your coroutine may be cancelled at any `await`.

Use:

```python
try:

    ...

finally:

    release_resources()
```

or

```python
except asyncio.CancelledError:

    cleanup()

    raise
```

Never swallow `CancelledError` unless you intentionally want to suppress cancellation.

______________________________________________________________________

# Production Example

A FastAPI endpoint uploads a file to cloud storage.

```
Client

↓

Upload

↓

Client Disconnects
```

The request task is cancelled.

Your coroutine should:

- Close the file handle.
- Release the database session.
- Remove temporary files.
- Stop background processing if appropriate.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Ignoring timeouts for external APIs.

______________________________________________________________________

## Mistake 2

Suppressing `CancelledError` without re-raising it.

______________________________________________________________________

## Mistake 3

Using very large timeout values "just to be safe."

______________________________________________________________________

## Mistake 4

Forgetting cleanup when cancellation occurs.

______________________________________________________________________

# Best Practices

✅ Apply timeouts to every external dependency.

✅ Use `asyncio.timeout()` for grouped operations on Python 3.11+.

✅ Use `try`/`finally` for resource cleanup.

✅ Shield only operations that truly must complete.

❌ Don't ignore cancellation requests.

❌ Don't block the event loop during cleanup.

______________________________________________________________________

# Production Insight

In production systems, cancellations happen frequently:

- Browser closes the connection.
- Load balancer times out.
- Reverse proxy disconnects.
- Kubernetes terminates a pod.
- Autoscaling shuts down a worker.

Robust async services treat cancellation as a normal control flow rather than an exceptional event.

______________________________________________________________________

# Questions

### Question

> Why is cancellation called cooperative?

### Answer

Because the coroutine decides when it can be interrupted—typically at the next `await`—allowing it to clean up safely.

______________________________________________________________________

### Question

> What does `asyncio.wait_for()` do?

### Answer

It waits for an awaitable to finish within a specified timeout and cancels it if the timeout expires.

______________________________________________________________________

### Question

> When should `asyncio.shield()` be used?

### Answer

When an operation, such as committing a transaction or writing an audit log, must complete even if the caller is
cancelled.

______________________________________________________________________

### Question

> Why should every external API call have a timeout?

### Answer

Without a timeout, stalled services can consume resources indefinitely and reduce system reliability.

______________________________________________________________________

### Question

> What is the safest way to release resources?

### Answer

Use `try`/`finally` or handle `asyncio.CancelledError` explicitly, ensuring cleanup always occurs before re-raising the
exception.

______________________________________________________________________

# Practical Lesson

Create:

```text
timeout_demo.py
```

Implement:

- A coroutine that sleeps for 10 seconds.
- Wrap it with `asyncio.wait_for(..., timeout=2)`.
- Catch `TimeoutError`.
- Add cleanup using `finally`.
- Repeat using `asyncio.timeout()` if running Python 3.11+.

Observe how cancellation and cleanup interact.

______________________________________________________________________

# Questions

## Question 1

What happens internally when `asyncio.wait_for()` times out?

### Answer

It cancels the awaited task and raises `asyncio.TimeoutError` to the caller.

______________________________________________________________________

## Question 2

Why should `CancelledError` usually be re-raised?

### Answer

Because it signals normal cancellation to the event loop and higher-level code. Suppressing it can leave tasks in an
inconsistent state.

______________________________________________________________________

## Question 3

What is the difference between `wait_for()` and `timeout()`?

### Answer

`wait_for()` wraps a single awaitable, while `asyncio.timeout()` provides a context manager that applies a shared
timeout to all await operations within its block.

______________________________________________________________________

## Question 4

When is `asyncio.shield()` appropriate?

### Answer

When a critical operation must not be cancelled by its caller, such as finalising a transaction or persisting an audit
record.

______________________________________________________________________

## Question 5

Why are timeouts considered mandatory in production systems?

### Answer

Because networks and external services are unreliable. Timeouts prevent resource exhaustion and allow systems to fail
fast and recover gracefully.

______________________________________________________________________

# Assignment

## Exercise 1

Wrap multiple simulated API calls with `asyncio.timeout()`.

Observe how the shared timeout behaves.

______________________________________________________________________

## Exercise 2

Create a long-running task.

Cancel it after three seconds.

Ensure all resources are cleaned up correctly.

______________________________________________________________________

## Exercise 3

Protect a simulated "commit transaction" coroutine using `asyncio.shield()`.

Cancel the outer task and verify that the commit still completes.

______________________________________________________________________

## Exercise 4

Review one of your FastAPI projects.

Identify every external dependency (database, Redis, HTTP APIs, cloud storage).

Document:

- Recommended timeout values.
- Which operations should be shielded.
- Which operations should be cancelled immediately on client disconnect.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why production systems require timeouts.
- ✅ How cooperative cancellation works.
- ✅ `asyncio.wait_for()`.
- ✅ `asyncio.timeout()`.
- ✅ `asyncio.shield()`.
- ✅ Cancellation propagation.
- ✅ Cleanup patterns.
- ✅ Production timeout strategies.

______________________________________________________________________

# Next Lesson

**File:** [56-production-python-part-01-logging](56-production-python-part-01-logging.md)
