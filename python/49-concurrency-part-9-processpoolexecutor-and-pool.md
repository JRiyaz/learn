# File: python/49-concurrency-part-9-processpoolexecutor-and-pool.md

# Advanced Python Runtime & Concurrency
# Concurrency Part 9: Process Pools - `multiprocessing.Pool` & `ProcessPoolExecutor`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 49
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 8–9 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `multiprocessing.Pool` | Python 2.6 |
| `concurrent.futures.ProcessPoolExecutor` | Python 3.2 |

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why process pools exist
- Problems with manually creating processes
- How `multiprocessing.Pool` works
- How `ProcessPoolExecutor` works
- `map()`
- `apply()`
- `apply_async()`
- `submit()`
- Futures
- Exception handling
- Choosing the right API
- Production best practices
- questions

---

# Recap

Previously we learned:

- Multiprocessing
- Parent and child processes
- Inter-Process Communication (IPC)
- Queues
- Pipes
- Managers
- Shared Memory

Suppose you need to process:

```
10,000 images
```

Should you create:

```
10,000 Processes?
```

Absolutely not.

Just as threads have thread pools,

processes have process pools.

---

# Why Process Pools?

Creating a process is expensive.

For every new process the operating system must allocate:

- Memory
- Address space
- Interpreter
- Scheduling information
- System resources

Repeatedly creating and destroying processes wastes time.

Instead:

```
Create Workers Once

↓

Reuse Them

↓

Submit Tasks
```

---

# Real-World Analogy

Imagine a warehouse.

Poor approach

```
Every Package

↓

Hire New Worker

↓

Fire Worker
```

Efficient approach

```
20 Permanent Workers

↓

New Packages Arrive

↓

Workers Reuse Existing Equipment
```

A process pool works the same way.

---

# What is a Process Pool?

A process pool is:

> A fixed number of worker processes that continuously execute submitted tasks.

```
Tasks

↓

Queue

↓

Worker Processes

↓

Results
```

---

# `multiprocessing.Pool`

The original multiprocessing API.

```python
from multiprocessing import Pool
```

---

# Creating a Pool

```python
from multiprocessing import Pool

with Pool(processes=4) as pool:

    ...
```

The context manager automatically:

- Starts workers
- Cleans up workers
- Releases resources

---

# First Example

```python
from multiprocessing import Pool


def square(number):

    return number * number


with Pool(processes=4) as pool:

    results = pool.map(
        square,
        [1, 2, 3, 4]
    )

print(results)
```

Output

```text
[1, 4, 9, 16]
```

---

# How `map()` Works

```
Input

↓

1

2

3

4

↓

Task Queue

↓

Worker Processes

↓

Results

↓

[1, 4, 9, 16]
```

The order of results always matches the input order.

---

# `apply()`

Runs one function.

```python
result = pool.apply(
    square,
    args=(10,)
)

print(result)
```

Output

```text
100
```

Unlike `map()`,

this blocks until completion.

---

# `apply_async()`

Suppose you don't want to wait immediately.

Use:

```python
result = pool.apply_async(
    square,
    args=(10,)
)
```

Later

```python
print(
    result.get()
)
```

This behaves similarly to a Future.

---

# `imap()`

Suppose your input contains:

```
1 Million Items
```

Should Python compute every result before returning?

No.

Instead,

```python
pool.imap(...)
```

returns an iterator.

Results are produced lazily.

---

# Example

```python
from multiprocessing import Pool


def square(number):

    return number * number


with Pool() as pool:

    for result in pool.imap(
        square,
        range(5)
    ):

        print(result)
```

Output

```text
0
1
4
9
16
```

Useful for very large datasets.

---

# `ProcessPoolExecutor`

Modern Python introduced

```python
from concurrent.futures import ProcessPoolExecutor
```

The API intentionally resembles:

```
ThreadPoolExecutor
```

making it easier to learn.

---

# Creating a Process Pool

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(
    max_workers=4
) as executor:

    ...
```

---

# Using `submit()`

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

This should feel familiar from the previous lesson.

---

# Multiple Tasks

```python
from concurrent.futures import ProcessPoolExecutor


def cube(number):

    return number ** 3


with ProcessPoolExecutor() as executor:

    futures = [

        executor.submit(cube, i)

        for i in range(5)
    ]

    for future in futures:

        print(future.result())
```

---

# `map()`

Like the thread pool,

the process pool also supports:

```python
executor.map()
```

Example

```python
results = executor.map(
    cube,
    range(5)
)

print(list(results))
```

Output

```text
[0, 1, 8, 27, 64]
```

---

# Handling Exceptions

Suppose

```python
def divide(number):

    return 10 / number
```

One task receives

```python
0
```

Submission succeeds.

The exception is stored.

```python
future.result()
```

Raises

```text
ZeroDivisionError
```

---

# Pool Lifecycle

```
Create Pool

↓

Create Worker Processes

↓

Submit Tasks

↓

Execute

↓

Return Results

↓

Shutdown
```

---

# Choosing Worker Count

Suppose your machine has:

```
8 CPU Cores
```

Starting

```
100 Worker Processes
```

usually hurts performance.

General guideline:

```
Workers ≈ CPU Cores
```

However,

always benchmark.

Factors include:

- Workload
- Memory
- Cache locality
- Serialization overhead

---

# Pool vs Executor

| Feature | `Pool` | `ProcessPoolExecutor` |
|----------|---------|----------------------|
| Older API | ✅ | ❌ |
| Future support | ❌ | ✅ |
| `submit()` | ❌ | ✅ |
| `map()` | ✅ | ✅ |
| Exception handling | Basic | Modern |
| Similar to ThreadPoolExecutor | ❌ | ✅ |

---

# Which Should You Use?

For new applications,

prefer

```
ProcessPoolExecutor
```

Reasons:

- Cleaner API
- Futures
- Better consistency
- Easier migration between thread and process pools

`multiprocessing.Pool` is still common in older codebases and remains fully supported.

---

# Performance Considerations

Remember,

every submitted task requires:

```
Serialize Input

↓

Send To Worker

↓

Execute

↓

Serialize Result

↓

Return Result
```

Very small tasks may spend more time communicating than computing.

---

# Task Granularity

Poor

```
1 Million Tiny Tasks
```

Better

```
100 Large Tasks
```

Reducing IPC overhead often improves performance.

---

# Production Example

Suppose an image platform stores:

```
50,000 Photos
```

Each photo requires:

- Resize
- Watermark
- Compression
- Thumbnail generation

A process pool distributes work:

```
Task Queue

↓

Process 1

↓

Process 2

↓

Process 3

↓

Process 4
```

Each worker continuously processes images until the queue is empty.

---

# Common Mistakes

## Mistake 1

Creating a new process pool inside a loop.

Pools should generally be created once and reused.

---

## Mistake 2

Submitting extremely small tasks.

IPC overhead can exceed computation time.

---

## Mistake 3

Using a process pool for database queries.

Database operations are primarily I/O-bound.

Threads or asynchronous programming are usually better.

---

## Mistake 4

Ignoring exceptions from futures.

Always retrieve results.

---

# Best Practices

✅ Use process pools for CPU-intensive work.

✅ Prefer `ProcessPoolExecutor` for new projects.

✅ Keep tasks reasonably large.

✅ Benchmark worker counts.

✅ Use context managers.

❌ Don't create excessive workers.

❌ Don't use multiprocessing without measuring performance.

---

# Production Insight

Many production systems execute CPU-heavy jobs using worker pools.

Examples include:

- Video transcoding
- Report generation
- Machine learning inference
- Password hashing
- Scientific simulations

Frameworks like Celery often combine:

- Multiple worker processes
- Internal task queues
- Optional thread pools

The same principles learned here apply at much larger scales.

---

# Questions

### Question

> Why use a process pool instead of creating individual processes?

### Answer

A process pool reuses worker processes, reducing process creation overhead and improving throughput.

---

### Question

> When should `ProcessPoolExecutor` be preferred?

### Answer

For modern Python applications that require a clean API, futures, and consistency with `ThreadPoolExecutor`.

---

### Question

> Why can process pools perform poorly with tiny tasks?

### Answer

Because serialization and inter-process communication may take longer than the computation itself.

---

### Question

> Why is `executor.map()` useful?

### Answer

It efficiently applies the same function to multiple inputs while preserving result order.

---

### Question

> Should the number of workers always equal the CPU core count?

### Answer

Not always. It is a good starting point, but the optimal value depends on workload characteristics and should be determined through benchmarking.

---

# Practical Lesson

Create:

```text
process_pool_demo.py
```

```python
from concurrent.futures import ProcessPoolExecutor
import math


def calculate(number):
    """
    Simulate CPU-intensive work.
    """
    total = 0

    for i in range(5_000_000):
        total += math.sqrt(i)

    return number


numbers = range(4)

with ProcessPoolExecutor(max_workers=4) as executor:

    results = executor.map(
        calculate,
        numbers
    )

    print(list(results))
```

Run the same workload:

- Sequentially
- Using threads
- Using a process pool

Compare:

- Execution time
- CPU utilisation
- Memory usage

---

# Questions

## Question 1

What is a process pool?

### Answer

A collection of reusable worker processes that execute submitted CPU-bound tasks.

---

## Question 2

Why is `ProcessPoolExecutor` generally preferred over `multiprocessing.Pool`?

### Answer

Because it provides a modern Future-based API that is consistent with other executor implementations.

---

## Question 3

What is the disadvantage of submitting very small tasks?

### Answer

Serialization and IPC overhead may outweigh the cost of computation.

---

## Question 4

What kind of workloads benefit most from process pools?

### Answer

CPU-intensive workloads such as image processing, encryption, numerical computation, and scientific simulations.

---

## Question 5

Why shouldn't process pools be used for most database operations?

### Answer

Because database access is typically I/O-bound, making threads or asynchronous programming more efficient and less resource-intensive.

---

# Assignment

## Exercise 1

Compare the execution time of:

- Sequential execution
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

using a CPU-intensive workload.

Record:

- Total execution time
- CPU utilisation
- Memory usage

Explain the results.

---

## Exercise 2

Modify the process pool example so one task raises an exception.

Handle the exception gracefully without stopping the remaining tasks.

---

## Exercise 3

Experiment with:

- 2 workers
- 4 workers
- 8 workers
- 16 workers

Measure execution time and determine the optimal worker count for your machine.

---

## Exercise 4

Choose a CPU-intensive operation from one of your backend projects.

Design how you would integrate a process pool into the application.

Explain:

- Why multiprocessing is appropriate
- Expected performance gains
- Potential drawbacks
- How results would be collected

---

# Summary

In this lesson, you learned:

- ✅ Why process pools exist.
- ✅ How `multiprocessing.Pool` works.
- ✅ How `ProcessPoolExecutor` works.
- ✅ `map()`, `apply()`, and `apply_async()`.
- ✅ Futures and result handling.
- ✅ Exception propagation.
- ✅ Performance considerations.
- ✅ Production process pool patterns.

---

# Next Lesson

**File:**
[50-concurrency-part-10-process-start-methods](50-concurrency-part-10-process-start-methods.md)

In the next lesson, you'll learn one of the most important and frequently misunderstood multiprocessing topics: **process start methods**. We'll cover `fork`, `spawn`, and `forkserver`, platform differences (Linux, macOS, Windows), memory implications, copy-on-write, process initialization, and why choosing the correct start method is critical for building reliable production applications.
