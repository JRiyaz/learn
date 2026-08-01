# File: python/46-concurrency-part-6-threadpoolexecutor.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 6: ThreadPoolExecutor & Futures

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 46
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 7–8 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `concurrent.futures` | Python 3.2 |
| `ThreadPoolExecutor` | Python 3.2 |
| `Future` | Python 3.2 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why thread pools exist
- Problems with manually managing threads
- What `ThreadPoolExecutor` is
- How thread pools work internally
- `submit()`
- `map()`
- `Future`
- Retrieving results
- Handling exceptions
- Cancelling tasks
- Production best practices

______________________________________________________________________

# Recap

So far we've learned:

- Threads
- Locks
- Queues
- Events
- Conditions
- Semaphores

We've manually created threads using:

```python
threading.Thread(...)
```

But imagine processing 10,000 API requests.

Should we create 10,000 threads?

Absolutely not.

______________________________________________________________________

# The Problem with Manual Threads

Suppose you have 500 tasks.

A naïve implementation might do this:

```python
for task in tasks:

    thread = threading.Thread(
        target=process,
        args=(task,)
    )

    thread.start()
```

Problems:

- Hundreds of operating system threads
- Large memory usage
- Context-switching overhead
- Difficult lifecycle management
- Poor scalability

______________________________________________________________________

# Real-World Analogy

Imagine a restaurant.

Option 1:

Hire one chef for every customer.

```
100 Customers

↓

100 Chefs
```

Ridiculous.

______________________________________________________________________

Option 2:

Hire a fixed number of chefs.

```
100 Customers

↓

10 Chefs

↓

Work Queue
```

The chefs continuously take new orders.

That's a thread pool.

______________________________________________________________________

# What is a Thread Pool?

A thread pool is:

> A fixed collection of reusable worker threads.

Instead of creating new threads repeatedly,

existing workers execute new tasks.

```
Tasks

↓

Queue

↓

Worker Threads

↓

Results
```

______________________________________________________________________

# Introducing `ThreadPoolExecutor`

Python provides:

```python
from concurrent.futures import ThreadPoolExecutor
```

It manages:

- Thread creation
- Thread reuse
- Scheduling
- Shutdown
- Error propagation

______________________________________________________________________

# Creating a Thread Pool

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(
    max_workers=4
) as executor:

    ...
```

The context manager ensures:

- Threads are started
- Threads are cleaned up
- Resources are released

______________________________________________________________________

# First Example

```python
from concurrent.futures import ThreadPoolExecutor
import time


def worker(number):

    print(f"Starting {number}")

    time.sleep(2)

    print(f"Finished {number}")


with ThreadPoolExecutor(
    max_workers=3
) as executor:

    for i in range(6):

        executor.submit(worker, i)
```

Output (order varies)

```text
Starting 0
Starting 1
Starting 2

Finished 1

Starting 3

Finished 0

Starting 4

...
```

Notice:

Only three workers execute simultaneously.

______________________________________________________________________

# How It Works

```
Tasks

0

1

2

3

4

5

↓

Queue

↓

Worker 1

Worker 2

Worker 3
```

When Worker 1 finishes,

it automatically receives another task.

______________________________________________________________________

# `submit()`

The most common method is:

```python
future = executor.submit(
    function,
    *args
)
```

It immediately returns a:

```
Future
```

______________________________________________________________________

# What is a Future?

A `Future` represents:

> A result that may not exist yet.

Think of it as a promise.

```
Task Submitted

↓

Running

↓

Finished

↓

Result Available
```

______________________________________________________________________

# Retrieving Results

```python
future = executor.submit(
    square,
    10
)

print(
    future.result()
)
```

Output

```text
100
```

If the task hasn't finished,

`result()` waits.

______________________________________________________________________

# Example

```python
from concurrent.futures import ThreadPoolExecutor
import time


def square(number):

    time.sleep(2)

    return number * number


with ThreadPoolExecutor() as executor:

    future = executor.submit(square, 8)

    print(future.result())
```

Output

```text
64
```

______________________________________________________________________

# Multiple Futures

```python
futures = []

with ThreadPoolExecutor() as executor:

    for i in range(5):

        futures.append(
            executor.submit(square, i)
        )

for future in futures:

    print(future.result())
```

______________________________________________________________________

# Processing Results as They Finish

Suppose tasks finish in different orders.

Instead of waiting sequentially,

use:

```python
from concurrent.futures import as_completed
```

______________________________________________________________________

# Example

```python
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

import random
import time


def work(number):

    time.sleep(random.randint(1, 3))

    return number


with ThreadPoolExecutor() as executor:

    futures = [
        executor.submit(work, i)
        for i in range(5)
    ]

    for future in as_completed(futures):

        print(future.result())
```

Results appear

as each task completes,

not submission order.

______________________________________________________________________

# `map()`

Suppose every task performs the same function.

Instead of

```python
submit()

submit()

submit()
```

Use

```python
executor.map()
```

______________________________________________________________________

# Example

```python
from concurrent.futures import ThreadPoolExecutor


def square(number):

    return number * number


with ThreadPoolExecutor() as executor:

    results = executor.map(
        square,
        [1, 2, 3, 4]
    )

print(list(results))
```

Output

```text
[1, 4, 9, 16]
```

Unlike `as_completed()`,

`map()` preserves input order.

______________________________________________________________________

# `submit()` vs `map()`

| Feature | `submit()` | `map()` |
|----------|------------|----------|
| Individual tasks | ✅ | ❌ |
| Different arguments | ✅ | Limited |
| Future objects | ✅ | ❌ |
| Preserves order | No | Yes |
| Best for | Flexible workflows | Bulk processing |

______________________________________________________________________

# Handling Exceptions

Suppose

```python
def divide(x):

    return 10 / x
```

One task receives:

```python
0
```

The exception is stored inside the `Future`.

______________________________________________________________________

# Example

```python
future = executor.submit(
    divide,
    0
)

future.result()
```

Raises

```text
ZeroDivisionError
```

Notice

The exception isn't raised during `submit()`.

It appears when retrieving the result.

______________________________________________________________________

# Checking Completion

```python
future.done()
```

Returns

```python
True
```

or

```python
False
```

______________________________________________________________________

# Cancelling Tasks

```python
future.cancel()
```

Cancellation succeeds only if

the task has not started.

Check using

```python
future.cancelled()
```

______________________________________________________________________

# Thread Pool Lifecycle

```
Create Pool

↓

Create Workers

↓

Submit Tasks

↓

Workers Execute

↓

Results Returned

↓

Shutdown
```

______________________________________________________________________

# Choosing `max_workers`

Too few workers

```
Poor utilisation
```

Too many

```
High memory

↓

Context Switching

↓

Reduced Performance
```

There is no universal number.

The optimal value depends on:

- Workload type
- CPU cores
- I/O wait time
- Memory
- External services

______________________________________________________________________

# Production Example

Imagine a backend service.

One request requires:

- Download avatar
- Download profile
- Download permissions
- Download recommendations

Instead of

```
Sequential

↓

4 seconds
```

Thread pool

```
4 Workers

↓

1 second (approximately)
```

assuming each task is I/O-bound.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating a new thread pool for every small function call.

Pools are designed to be reused.

______________________________________________________________________

## Mistake 2

Using a thread pool for CPU-bound work.

For CPU-intensive tasks,

prefer `ProcessPoolExecutor`.

______________________________________________________________________

## Mistake 3

Ignoring exceptions inside futures.

Always call:

```python
future.result()
```

or inspect the future.

______________________________________________________________________

## Mistake 4

Using an excessively large number of workers.

More threads do not necessarily improve performance.

______________________________________________________________________

# Best Practices

✅ Prefer `ThreadPoolExecutor` over manually creating many threads.

✅ Use context managers.

✅ Retrieve every future result.

✅ Choose an appropriate worker count.

✅ Use `as_completed()` when completion order matters.

❌ Don't ignore failed futures.

❌ Don't create thousands of workers.

______________________________________________________________________

# Production Insight

Many Python libraries internally use thread pools.

Examples include:

- HTTP clients
- Cloud SDKs
- Background job systems
- File processing frameworks

In production APIs,

thread pools are commonly used for:

- Parallel API requests
- Reading multiple files
- Uploading objects to cloud storage
- Background notifications

However, long-running background jobs are generally delegated to dedicated worker systems such as Celery or distributed
task queues.

______________________________________________________________________

# Questions

### Question

> Why use a thread pool instead of creating a thread for every task?

### Answer

A thread pool reuses a fixed number of worker threads, reducing memory usage, thread creation overhead, and context
switching.

______________________________________________________________________

### Question

> What is a `Future`?

### Answer

A `Future` is an object representing the eventual result or exception of an asynchronous task.

______________________________________________________________________

### Question

> When is `submit()` preferred over `map()`?

### Answer

When tasks require different arguments, individual tracking, cancellation, or flexible scheduling.

______________________________________________________________________

### Question

> Why can `future.result()` block?

### Answer

Because the associated task may still be running when the result is requested.

______________________________________________________________________

### Question

> Why shouldn't thread pools be used for CPU-bound workloads?

### Answer

Because CPU-bound threads still compete for the GIL. `ProcessPoolExecutor` is generally a better choice for
CPU-intensive work.

______________________________________________________________________

# Practical Lesson

Create:

```text
thread_pool_demo.py
```

```python
from concurrent.futures import ThreadPoolExecutor
import time


def fetch_user(user_id):
    print(f"Fetching user {user_id}")

    time.sleep(2)

    return {
        "id": user_id,
        "name": f"User {user_id}"
    }


user_ids = [1, 2, 3, 4, 5]

with ThreadPoolExecutor(max_workers=3) as executor:

    futures = [
        executor.submit(fetch_user, user_id)
        for user_id in user_ids
    ]

    for future in futures:
        print(future.result())
```

Expected Output (order of "Fetching..." messages may vary)

```text
Fetching user 1
Fetching user 2
Fetching user 3
...

{'id': 1, 'name': 'User 1'}
...
```

______________________________________________________________________

# Questions

## Question 1

What is a thread pool?

### Answer

A collection of reusable worker threads that execute submitted tasks.

______________________________________________________________________

## Question 2

What is the purpose of a `Future`?

### Answer

It represents the eventual result or exception of an asynchronous operation.

______________________________________________________________________

## Question 3

What is the difference between `submit()` and `map()`?

### Answer

`submit()` returns individual `Future` objects and offers greater flexibility, while `map()` applies the same function
to an iterable and preserves input order.

______________________________________________________________________

## Question 4

When does `future.result()` raise an exception?

### Answer

When the task executed by the future raised an exception.

______________________________________________________________________

## Question 5

When should `ThreadPoolExecutor` be preferred?

### Answer

For managing many independent I/O-bound tasks efficiently without manually creating and managing threads.

______________________________________________________________________

# Assignment

## Exercise 1

Use `ThreadPoolExecutor` to download data from ten simulated APIs.

Limit the pool to four workers.

Measure the execution time.

______________________________________________________________________

## Exercise 2

Modify one task so it raises an exception.

Handle the exception gracefully without stopping the remaining tasks.

______________________________________________________________________

## Exercise 3

Compare:

- Sequential execution
- Manual threads
- `ThreadPoolExecutor`

Measure execution time and memory usage for an I/O-bound workload.

______________________________________________________________________

## Exercise 4

Take a FastAPI project.

Identify three independent I/O operations that could execute concurrently using a thread pool.

Explain the expected performance improvement and any limitations.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why thread pools exist.
- ✅ How `ThreadPoolExecutor` works.
- ✅ How to submit tasks.
- ✅ What `Future` objects represent.
- ✅ How to retrieve results.
- ✅ How to process tasks as they complete.
- ✅ The difference between `submit()` and `map()`.
- ✅ Exception handling and task cancellation.
- ✅ Production thread pool patterns.

______________________________________________________________________

# Next Lesson

**File:** [47-concurrency-part-7-multiprocessing](47-concurrency-part-7-multiprocessing.md)

In the next lesson, you'll learn how Python achieves true parallelism using the `multiprocessing` module. We'll cover
process creation, process lifecycle, process communication, shared memory, IPC mechanisms, start methods (`fork`,
`spawn`, `forkserver`), and when multiprocessing is the right choice over threading.
