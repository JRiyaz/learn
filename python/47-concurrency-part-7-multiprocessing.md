# File: python/47-concurrency-part-7-multiprocessing.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 7: Multiprocessing - True Parallelism in Python

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 47
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 8 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `multiprocessing` | Python 2.6 |
| `Process` | Python 2.6 |
| `Pool` | Python 2.6 |
| `multiprocessing.Manager` | Python 2.6 |
| `multiprocessing.shared_memory` | Python 3.8 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why multiprocessing exists
- Processes vs threads
- True parallelism
- The `multiprocessing` module
- Creating processes
- Process lifecycle
- Parent and child processes
- Process IDs (PID)
- Process communication overview
- Production use cases
- Best practices
- questions

______________________________________________________________________

# Recap

In the previous lesson, we learned about thread pools.

Thread pools solve many I/O-bound problems efficiently.

However, one major limitation remains.

```
Threads

↓

Global Interpreter Lock

↓

Only One Thread Executes Python Bytecode
```

So how do we fully utilise all CPU cores?

The answer is:

```
Multiprocessing
```

______________________________________________________________________

# Why Multiprocessing?

Imagine a machine with:

```
8 CPU Cores
```

Your Python program performs:

- Image processing
- Password hashing
- Video encoding
- Data compression

These are CPU-bound workloads.

Threads cannot execute Python bytecode on all eight cores simultaneously because of the GIL.

Processes can.

______________________________________________________________________

# What is Multiprocessing?

Multiprocessing means:

> Running multiple independent Python processes simultaneously.

Each process has:

- Its own Python interpreter
- Its own memory
- Its own Global Interpreter Lock
- Its own execution state

Because each process owns its own interpreter, multiple CPU cores can execute Python code at the same time.

______________________________________________________________________

# Visualisation

```
CPU Core 1

↓

Python Process A

↓

Own GIL


CPU Core 2

↓

Python Process B

↓

Own GIL


CPU Core 3

↓

Python Process C

↓

Own GIL
```

Unlike threads,

these processes execute truly in parallel.

______________________________________________________________________

# Threads vs Processes

```
One Process

↓

Multiple Threads

↓

One Shared GIL
```

versus

```
Multiple Processes

↓

Multiple GILs

↓

True Parallelism
```

______________________________________________________________________

# Introducing `multiprocessing`

```python
import multiprocessing
```

This module provides an API similar to the `threading` module.

If you've learned threads,

many concepts will already feel familiar.

______________________________________________________________________

# Your First Process

```python
from multiprocessing import Process


def worker():

    print("Worker process")


process = Process(target=worker)

process.start()

process.join()
```

Output

```text
Worker process
```

______________________________________________________________________

# Understanding `Process`

```python
process = Process(
    target=worker
)
```

Just like `Thread`,

nothing executes immediately.

The process is only created.

Execution begins when:

```python
process.start()
```

is called.

______________________________________________________________________

# Process Lifecycle

Every process moves through several stages.

```
Created

↓

Started

↓

Running

↓

Finished

↓

Terminated
```

A process can only be started once.

______________________________________________________________________

# Parent and Child Processes

Consider:

```python
main.py
```

This program creates another process.

```
Parent Process

↓

Child Process
```

The child inherits part of the parent's execution context depending on the operating system's process creation method,
which we'll study later.

______________________________________________________________________

# Process IDs (PID)

Every operating system process has a unique identifier.

```python
import os

print(os.getpid())
```

Example

```text
18452
```

______________________________________________________________________

# Parent Process ID

```python
import os

print(os.getppid())
```

Example

```text
18397
```

This identifies the process that created the current one.

______________________________________________________________________

# Example

```python
from multiprocessing import Process
import os


def worker():

    print(
        f"Child PID: {os.getpid()}"
    )

    print(
        f"Parent PID: {os.getppid()}"
    )


print(f"Main PID: {os.getpid()}")

process = Process(target=worker)

process.start()

process.join()
```

Sample Output

```text
Main PID: 10401

Child PID: 10415

Parent PID: 10401
```

______________________________________________________________________

# Multiple Processes

```python
from multiprocessing import Process
import time


def worker(number):

    print(f"Worker {number}")

    time.sleep(2)


processes = []

for i in range(4):

    process = Process(
        target=worker,
        args=(i,)
    )

    process.start()

    processes.append(process)

for process in processes:

    process.join()
```

If your machine has multiple CPU cores,

these processes may execute simultaneously.

______________________________________________________________________

# Process Isolation

Suppose

```python
counter = 0
```

Process A

```python
counter += 1
```

Process B

```python
counter += 1
```

Will they modify the same variable?

No.

Each process has its own memory.

______________________________________________________________________

# Demonstration

```python
from multiprocessing import Process

counter = 0


def worker():

    global counter

    counter += 1

    print(counter)


process = Process(target=worker)

process.start()

process.join()

print(counter)
```

Output

```text
1

0
```

The parent process remains unchanged.

______________________________________________________________________

# Why?

Memory is isolated.

```
Parent Process

↓

counter = 0


Child Process

↓

counter = 1
```

They are different variables in different memory spaces.

______________________________________________________________________

# Sharing Data

Threads

```
Shared Memory

↓

Easy Communication
```

Processes

```
Separate Memory

↓

Explicit Communication Required
```

We'll study:

- Queues
- Pipes
- Shared Memory
- Managers

in upcoming lessons.

______________________________________________________________________

# Process Startup Cost

Creating a process is significantly more expensive than creating a thread.

Why?

Because the operating system must allocate:

- New address space
- New interpreter
- New memory
- Process metadata
- Scheduling structures

Threads reuse existing process resources.

______________________________________________________________________

# Memory Usage

Every process has:

- Independent heap
- Independent stack
- Independent interpreter state

Consequently,

multiprocessing consumes more memory than multithreading.

This is one of the trade-offs for achieving true parallelism.

______________________________________________________________________

# Process Termination

Normally,

a process exits after completing its target function.

You can also terminate it explicitly.

```python
process.terminate()
```

Use this carefully.

Forcefully terminating a process may leave files, sockets, or other resources in an inconsistent state.

______________________________________________________________________

# Checking Process Status

```python
process.is_alive()
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

# Daemon Processes

Processes can also be daemon processes.

```python
process.daemon = True
```

Like daemon threads,

daemon processes terminate automatically when their parent process exits.

Daemon processes are generally used only for background helper tasks.

______________________________________________________________________

# Multiprocessing vs Threading

| Feature | Threading | Multiprocessing |
|----------|------------|-----------------|
| Memory | Shared | Separate |
| GIL | Shared | One per process |
| CPU-bound | Poor | Excellent |
| I/O-bound | Excellent | Usually unnecessary |
| Startup Cost | Low | Higher |
| Memory Usage | Low | Higher |
| Communication | Easy | More complex |

______________________________________________________________________

# When Should You Use Multiprocessing?

Ideal workloads include:

- Video transcoding
- Image processing
- Password hashing
- Data analytics
- Machine learning
- Scientific simulations
- Numerical computation
- Large-scale data transformation

______________________________________________________________________

# Production Example

Imagine a media platform.

Users upload videos.

Processing pipeline

```
Upload

↓

Video Process 1

↓

Video Process 2

↓

Thumbnail Generator

↓

Compression

↓

Store
```

Each stage performs heavy CPU computation.

Running these tasks in separate processes allows multiple CPU cores to work simultaneously.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using multiprocessing for database queries.

Database operations are I/O-bound.

Threads or asynchronous programming are usually more appropriate.

______________________________________________________________________

## Mistake 2

Assuming processes share variables.

They do not.

Explicit communication is required.

______________________________________________________________________

## Mistake 3

Creating too many processes.

More processes than CPU cores often increase scheduling overhead without improving performance.

______________________________________________________________________

## Mistake 4

Ignoring process startup cost.

Short-lived tasks may spend more time creating processes than performing useful work.

______________________________________________________________________

# Best Practices

✅ Use multiprocessing for CPU-intensive workloads.

✅ Keep the number of worker processes close to the available CPU cores unless measurements suggest otherwise.

✅ Use `join()` to wait for child processes.

✅ Design clear communication mechanisms between processes.

❌ Don't use multiprocessing for every workload.

❌ Don't assume memory is shared.

______________________________________________________________________

# Production Insight

Many backend systems use multiprocessing behind the scenes.

Examples include:

- Gunicorn worker processes
- Celery worker processes
- Data processing pipelines
- Scientific computing frameworks

Each worker process provides:

- Fault isolation
- Independent memory
- Better CPU utilisation

This architecture is one reason Python performs well in production despite the GIL.

______________________________________________________________________

# Questions

### Question

> Why does multiprocessing avoid the GIL?

### Answer

Each process has its own Python interpreter and its own Global Interpreter Lock, allowing multiple CPU cores to execute
Python bytecode simultaneously.

______________________________________________________________________

### Question

> Why don't processes share variables?

### Answer

Each process has an independent memory space created by the operating system.

______________________________________________________________________

### Question

> When should multiprocessing be preferred?

### Answer

For CPU-bound workloads such as image processing, encryption, numerical computation, and machine learning.

______________________________________________________________________

### Question

> Why is multiprocessing more expensive than threading?

### Answer

Because every process requires its own memory, interpreter, operating system resources, and scheduling information.

______________________________________________________________________

### Question

> What is a parent process?

### Answer

A parent process is the process that creates another process, known as the child process.

______________________________________________________________________

# Practical Lesson

Create:

```text
multiprocessing_demo.py
```

```python
from multiprocessing import Process
import os
import time


def worker(number):

    print(
        f"Worker {number} "
        f"running in PID {os.getpid()}"
    )

    time.sleep(2)

    print(
        f"Worker {number} finished."
    )


processes = []

for i in range(4):

    process = Process(
        target=worker,
        args=(i,)
    )

    process.start()

    processes.append(process)

for process in processes:
    process.join()

print("All processes completed.")
```

Run the program and observe:

- Different process IDs
- Concurrent execution
- Independent worker processes

______________________________________________________________________

# Questions

## Question 1

What is multiprocessing?

### Answer

Multiprocessing is the execution of multiple independent processes simultaneously, allowing true parallelism across CPU
cores.

______________________________________________________________________

## Question 2

Why is multiprocessing better for CPU-bound tasks?

### Answer

Because each process has its own interpreter and GIL, allowing multiple CPU cores to execute Python code in parallel.

______________________________________________________________________

## Question 3

Do processes share memory by default?

### Answer

No. Each process has its own independent address space.

______________________________________________________________________

## Question 4

What is the purpose of `join()`?

### Answer

It blocks until the child process completes execution.

______________________________________________________________________

## Question 5

Why is multiprocessing more memory-intensive than threading?

### Answer

Because every process maintains its own interpreter, memory space, stacks, heaps, and operating system resources.

______________________________________________________________________

# Assignment

## Exercise 1

Create four processes that each calculate the sum of one million integers.

Measure the total execution time.

Compare it with a sequential implementation.

______________________________________________________________________

## Exercise 2

Modify the example so that every child process prints:

- PID
- Parent PID
- Start time
- Finish time

Explain how this demonstrates parallel execution.

______________________________________________________________________

## Exercise 3

Create one parent process and three child processes.

Attempt to modify a shared global variable.

Document why the parent's variable remains unchanged.

______________________________________________________________________

## Exercise 4

Take one CPU-intensive task from one of your own projects.

Explain whether multiprocessing would improve its performance.

Justify your answer based on CPU usage, memory requirements, and communication overhead.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why multiprocessing exists.
- ✅ How multiprocessing achieves true parallelism.
- ✅ How to create processes.
- ✅ Process lifecycle.
- ✅ Parent and child processes.
- ✅ Process IDs.
- ✅ Process isolation.
- ✅ Memory separation.
- ✅ Production multiprocessing patterns.

______________________________________________________________________

# Next Lesson

**File:** [48-concurrency-part-8-process-communication](48-concurrency-part-8-process-communication.md)

In the next lesson, you'll learn how separate processes communicate safely using Pipes, Queues, Managers, shared memory,
and other Inter-Process Communication (IPC) mechanisms. We'll also discuss serialization, pickling, performance
considerations, and production design patterns for multi-process applications.
