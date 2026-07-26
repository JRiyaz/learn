# File: python/52-concurrency-part-12-event-loop-and-tasks.md

# Advanced Python Runtime & Concurrency
# Concurrency Part 12: Event Loop, Tasks & Scheduling

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 52
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 9–10 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `asyncio.create_task()` | Python 3.7 |
| `asyncio.current_task()` | Python 3.7 |
| `asyncio.all_tasks()` | Python 3.7 |
| `Task.cancel()` | Python 3.4 |

---

# Learning Objectives

By the end of this lesson, you will understand:

- What the event loop really does
- How coroutines become tasks
- What an asyncio Task is
- `asyncio.create_task()`
- Task lifecycle
- Running multiple tasks concurrently
- Task cancellation
- Task inspection
- Production scheduling patterns
- Best practices
- questions

---

# Recap

In the previous lesson, we learned:

- Async programming
- Coroutines
- Event loop
- `async`
- `await`

We learned that:

```python
async def fetch():
    ...
```

creates a coroutine.

But here's an important question.

Who actually executes that coroutine?

The answer is:

```
The Event Loop
```

Today we'll understand exactly how.

---

# The Event Loop

The event loop is the scheduler of an asyncio application.

Think of it as an operating system,

but only for coroutines.

Its responsibilities include:

- Scheduling coroutines
- Managing tasks
- Monitoring sockets
- Handling timers
- Waking paused coroutines
- Executing ready coroutines

Everything in asyncio revolves around the event loop.

---

# A Simple View

```
Coroutine A

↓

Coroutine B

↓

Coroutine C

↓

Event Loop

↓

Run Ready Coroutine
```

The event loop repeatedly asks:

```
Which coroutine is ready to run?
```

---

# Infinite Loop

Internally,

the event loop behaves something like:

```text
while application_running:

    find_ready_tasks()

    execute_ready_tasks()

    wait_for_io_events()

    wake_completed_tasks()
```

This repeats thousands of times every second.

---

# Coroutines Are Passive

Consider

```python
async def hello():

    print("Hello")
```

Calling it

```python
hello()
```

does not execute it.

Instead,

Python creates

```
Coroutine Object
```

The coroutine simply waits.

---

# How Coroutines Execute

```
Call Coroutine

↓

Coroutine Object

↓

Task

↓

Event Loop

↓

Execution
```

Notice the missing piece.

```
Task
```

---

# What is a Task?

A Task is a wrapper around a coroutine.

It tells the event loop:

> Schedule this coroutine for execution.

Without a task,

the event loop has nothing to schedule.

---

# Creating a Task

```python
import asyncio


async def hello():

    print("Hello")


async def main():

    task = asyncio.create_task(
        hello()
    )

    await task


asyncio.run(main())
```

Output

```text
Hello
```

---

# Why Use `create_task()`?

Suppose we simply write

```python
await fetch_user()

await fetch_orders()

await fetch_products()
```

Execution

```
User

↓

Orders

↓

Products
```

Sequential.

---

Using tasks

```python
user = asyncio.create_task(fetch_user())

orders = asyncio.create_task(fetch_orders())

products = asyncio.create_task(fetch_products())
```

Execution

```
User

Orders

Products

↓

Concurrent Execution
```

Much more efficient.

---

# Task Lifecycle

Every task moves through several states.

```
Created

↓

Scheduled

↓

Running

↓

Waiting

↓

Running

↓

Completed
```

Or

```
Cancelled
```

Or

```
Failed
```

---

# Example

```python
import asyncio


async def worker():

    print("Started")

    await asyncio.sleep(2)

    print("Finished")


async def main():

    task = asyncio.create_task(
        worker()
    )

    await task


asyncio.run(main())
```

---

# Multiple Tasks

```python
import asyncio


async def worker(number):

    print(f"Start {number}")

    await asyncio.sleep(2)

    print(f"End {number}")


async def main():

    tasks = []

    for i in range(5):

        task = asyncio.create_task(
            worker(i)
        )

        tasks.append(task)

    for task in tasks:

        await task


asyncio.run(main())
```

Output

```text
Start 0
Start 1
Start 2
Start 3
Start 4

...

End 0
End 1
...
```

Notice

all tasks started immediately.

---

# Visualising Scheduling

```
Task 1

↓

Waiting

↓

Ready


Task 2

↓

Running


Task 3

↓

Waiting


↓

Event Loop

↓

Choose Ready Task
```

The event loop continuously switches between tasks whenever they reach an `await`.

---

# Awaiting a Task

When you write

```python
await task
```

you are saying:

> Suspend this coroutine until the task completes.

Importantly,

other tasks continue running.

---

# Fire-and-Forget

Sometimes you don't need to wait immediately.

```python
asyncio.create_task(
    background_cleanup()
)
```

The background task begins running while your current coroutine continues.

Be careful:

The task should eventually be awaited or otherwise managed to avoid unnoticed exceptions.

---

# `asyncio.current_task()`

Returns

the currently executing task.

```python
import asyncio


async def worker():

    print(
        asyncio.current_task()
    )


asyncio.run(worker())
```

Useful for:

- Debugging
- Logging
- Diagnostics

---

# `asyncio.all_tasks()`

Returns

all active tasks in the current event loop.

Example

```python
tasks = asyncio.all_tasks()
```

Useful when debugging hanging applications.

---

# Task Completion

```python
task.done()
```

Returns

```python
True
```

or

```python
False
```

---

# Retrieving Results

Tasks return values.

```python
async def square(number):

    return number * number


async def main():

    task = asyncio.create_task(
        square(5)
    )

    result = await task

    print(result)


asyncio.run(main())
```

Output

```text
25
```

---

# Handling Exceptions

Suppose

```python
async def divide():

    return 10 / 0
```

```python
task = asyncio.create_task(
    divide()
)

await task
```

Raises

```text
ZeroDivisionError
```

The exception is stored inside the task until awaited.

---

# Cancelling Tasks

Tasks can be cancelled.

```python
task.cancel()
```

Cancellation is cooperative.

The coroutine receives

```python
asyncio.CancelledError
```

at its next suspension point.

---

# Example

```python
import asyncio


async def worker():

    try:

        while True:

            print("Working...")

            await asyncio.sleep(1)

    except asyncio.CancelledError:

        print("Cleaning up...")

        raise


async def main():

    task = asyncio.create_task(
        worker()
    )

    await asyncio.sleep(3)

    task.cancel()

    try:

        await task

    except asyncio.CancelledError:

        print("Task cancelled.")


asyncio.run(main())
```

Output

```text
Working...
Working...
Working...
Cleaning up...
Task cancelled.
```

---

# Why Cancellation Matters

Imagine:

```
HTTP Request

↓

Client Disconnects
```

Should the server continue downloading a 2 GB file?

No.

The task should be cancelled,

freeing resources for other requests.

---

# Tasks vs Threads

| Task | Thread |
|------|--------|
| Lightweight | Heavyweight |
| Managed by event loop | Managed by OS |
| Cooperative | Preemptive |
| Low memory usage | Higher memory usage |
| Ideal for I/O | General concurrency |

---

# Event Loop Timeline

Suppose three requests arrive.

```
Task A

↓

Database

↓

Waiting


Task B

↓

HTTP Call

↓

Waiting


Task C

↓

Read File

↓

Waiting
```

The event loop continually executes whichever task becomes ready first.

No thread switching occurs.

---

# Production Example

A FastAPI endpoint may perform:

- Read user profile
- Read permissions
- Read feature flags
- Read notifications

Instead of:

```
Profile

↓

Permissions

↓

Notifications
```

the endpoint creates multiple tasks.

All I/O operations proceed concurrently,

reducing response time.

---

# Common Mistakes

## Mistake 1

Calling

```python
await task
```

immediately after

```python
create_task()
```

inside a loop.

This often eliminates concurrency.

---

Example

```python
for user in users:

    task = asyncio.create_task(
        fetch(user)
    )

    await task
```

This runs sequentially.

---

Better

```python
tasks = [

    asyncio.create_task(fetch(user))

    for user in users
]

for task in tasks:

    await task
```

---

## Mistake 2

Ignoring background tasks.

Unobserved exceptions may go unnoticed.

---

## Mistake 3

Using blocking functions.

Never do:

```python
time.sleep(5)
```

inside async code.

---

## Mistake 4

Creating tasks unnecessarily.

If work must complete before continuing,

a simple

```python
await function()
```

may be clearer.

---

# Best Practices

✅ Use `create_task()` for independent concurrent work.

✅ Keep references to created tasks.

✅ Handle task cancellation.

✅ Await task results.

✅ Use logging when debugging task behaviour.

❌ Don't ignore exceptions.

❌ Don't block the event loop.

---

# Production Insight

Most production ASGI servers operate like this:

```
Worker Process

↓

Event Loop

↓

Incoming HTTP Requests

↓

One Task Per Request

↓

Database

↓

Cache

↓

HTTP APIs

↓

Response
```

A busy FastAPI application may have thousands of active tasks while using only a handful of operating system threads.

Understanding tasks is essential before learning advanced async patterns such as `asyncio.gather()`, timeouts, queues, and structured concurrency.

---

# Questions

### Question

> What is an asyncio Task?

### Answer

A Task is a wrapper around a coroutine that schedules it for execution by the event loop.

---

### Question

> Why use `asyncio.create_task()`?

### Answer

To schedule multiple coroutines so they can execute concurrently instead of sequentially.

---

### Question

> What happens when a task reaches `await`?

### Answer

The task voluntarily suspends execution, allowing the event loop to run another ready task.

---

### Question

> How are task exceptions handled?

### Answer

Exceptions are stored within the task and raised when the task is awaited.

---

### Question

> Why is task cancellation important?

### Answer

It allows applications to stop unnecessary work, release resources, and respond to changing conditions such as client disconnections.

---

# Practical Lesson

Create:

```text
task_demo.py
```

```python
import asyncio


async def fetch(name):

    print(f"Starting {name}")

    await asyncio.sleep(2)

    print(f"Finished {name}")

    return name


async def main():

    tasks = [

        asyncio.create_task(fetch("Users")),

        asyncio.create_task(fetch("Orders")),

        asyncio.create_task(fetch("Products"))

    ]

    for task in tasks:

        result = await task

        print(f"Result: {result}")


asyncio.run(main())
```

Observe:

- All three tasks start immediately.
- The event loop switches between them while they wait.
- Results are retrieved when each task completes.

---

# Questions

## Question 1

What is the difference between a coroutine and a task?

### Answer

A coroutine defines asynchronous work, while a task wraps a coroutine and schedules it for execution by the event loop.

---

## Question 2

Why is `create_task()` necessary?

### Answer

Because simply calling a coroutine creates a coroutine object. `create_task()` schedules that coroutine to run concurrently.

---

## Question 3

What happens when a task is cancelled?

### Answer

The event loop injects an `asyncio.CancelledError` into the coroutine at its next suspension point, giving it an opportunity to perform cleanup.

---

## Question 4

Can thousands of asyncio tasks run simultaneously?

### Answer

Thousands of tasks can be active concurrently, but only one task executes Python code at a time within a single event loop thread.

---

## Question 5

Why shouldn't blocking functions be used inside async code?

### Answer

Blocking functions prevent the event loop from scheduling other tasks, reducing concurrency and degrading application performance.

---

# Assignment

## Exercise 1

Create five coroutines that simulate downloading different files.

Schedule them using `create_task()`.

Compare the execution time with sequential execution.

---

## Exercise 2

Modify one task to raise an exception.

Observe how the exception propagates when the task is awaited.

---

## Exercise 3

Create a long-running task.

Cancel it after three seconds.

Handle `asyncio.CancelledError` and perform cleanup before exiting.

---

## Exercise 4

Research how FastAPI creates and schedules one asyncio task per incoming request.

Draw a diagram illustrating:

- Client
- Uvicorn
- Event Loop
- Task
- Endpoint Function
- Response

---

# Summary

In this lesson, you learned:

- ✅ The responsibilities of the event loop.
- ✅ The difference between coroutines and tasks.
- ✅ How `asyncio.create_task()` works.
- ✅ Task lifecycle.
- ✅ Concurrent task scheduling.
- ✅ Task cancellation.
- ✅ Task inspection.
- ✅ Production scheduling patterns used by modern ASGI applications.

---

# Next Lesson

**File:**
[53-concurrency-part-13-asyncio-gather-wait-and-as_completed](53-concurrency-part-13-asyncio-gather-wait-and-as_completed.md)

In the next lesson, you'll learn how to coordinate multiple asynchronous operations using `asyncio.gather()`, `asyncio.wait()`, and `asyncio.as_completed()`. We'll explore result aggregation, exception propagation, timeouts, partial completion, and the concurrency patterns used in high-performance backend services.
