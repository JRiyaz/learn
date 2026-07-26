# File: python/41-concurrency-part-1-processes-vs-threads.md

# Advanced Python Runtime & Concurrency
# Concurrency Part 1: Processes vs Threads

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 41
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 6 Hours

---

# Python Version Introduced

Concurrency itself is not tied to a specific Python version, but the major modules discussed in this lesson have been available for many years.

| Feature | Python Version |
|----------|----------------|
| `threading` | Python 1.5.2 |
| `multiprocessing` | Python 2.6 |
| `concurrent.futures` | Python 3.2 |

---

# Learning Objectives

By the end of this lesson, you will understand:

- What concurrency is
- What parallelism is
- Why backend systems need concurrency
- Processes
- Threads
- Operating system scheduling
- Context switching
- CPU-bound workloads
- I/O-bound workloads
- Choosing the right execution model
- Backend production examples

---

# Recap

In the previous module, we explored Python's built-in data structures and algorithmic patterns.

Those lessons focused on **how data is organised**.

This module focuses on **how work is executed**.

Understanding concurrency is one of the biggest differences between a mid-level and senior backend engineer.

---

# Why Does Concurrency Matter?

Imagine a FastAPI application.

Users send requests like:

```
User A

↓

GET /products

User B

↓

POST /orders

User C

↓

GET /users
```

Should the server finish one request before starting the next?

Obviously not.

Modern backend systems handle many requests simultaneously.

That requires concurrency.

---

# What Is Concurrency?

Concurrency means making progress on **multiple tasks during the same period of time**.

Notice something important.

Concurrency does **not** necessarily mean multiple CPUs are executing simultaneously.

Instead, execution may switch rapidly between tasks.

Example:

```
Task A

↓

Task B

↓

Task A

↓

Task C

↓

Task B

↓

Task A
```

All tasks make progress.

---

# What Is Parallelism?

Parallelism means multiple tasks execute **at exactly the same time**.

Example:

```
CPU Core 1

↓

Task A


CPU Core 2

↓

Task B


CPU Core 3

↓

Task C
```

Tasks are literally running simultaneously.

---

# Concurrency vs Parallelism

```
Concurrency

Task A

↓

Task B

↓

Task A

↓

Task C

↓

Task B


Parallelism

Core 1 → Task A

Core 2 → Task B

Core 3 → Task C
```

Think of it this way:

- Concurrency is about **structure**
- Parallelism is about **execution**

---

# Real-World Analogy

Imagine a chef.

## Concurrency

One chef:

- Starts boiling pasta
- Chops vegetables
- Stirs sauce
- Returns to pasta

One person.

Many tasks.

---

## Parallelism

Three chefs.

Each cooks one dish.

Everything happens simultaneously.

---

# Why Backend Applications Need Concurrency

Suppose one request needs to:

- Query PostgreSQL
- Call Redis
- Fetch data from another API
- Read a file
- Send an email

During database or network operations, the CPU is mostly waiting.

Waiting wastes resources.

Concurrency allows the application to perform other work while waiting.

---

# CPU-Bound vs I/O-Bound Workloads

This distinction is one of the most common interview topics.

---

# CPU-Bound

CPU-bound programs spend most of their time performing calculations.

Examples:

- Image processing
- Video encoding
- Encryption
- Compression
- Machine learning inference
- Scientific computing

The CPU is the bottleneck.

---

# I/O-Bound

I/O means Input/Output.

Examples:

- Database queries
- API calls
- Reading files
- Writing files
- Network communication
- Waiting for Redis
- Waiting for Kafka
- Waiting for S3

Most backend applications are primarily I/O-bound.

---

# Visual Comparison

CPU-bound

```
Compute

↓

Compute

↓

Compute

↓

Compute
```

Little waiting.

---

I/O-bound

```
Send Query

↓

Wait...

↓

Receive Data

↓

Process

↓

Wait...

↓

Process
```

Most time is spent waiting.

---

# Processes

A process is an independent running program.

Each process has:

- Its own memory
- Its own Python interpreter
- Its own resources
- Its own operating system state

Example:

```
Chrome

VS

VS Code

Spotify

Python
```

Each is a separate process.

---

# Process Isolation

Imagine two Python programs.

```
Process A

users = []



Process B

users = []
```

These are completely different lists.

Changing one does not affect the other.

---

# Process Memory

```
+------------------------+
| Process A              |
|                        |
| Heap                   |
| Stack                  |
| Variables              |
+------------------------+

+------------------------+
| Process B              |
|                        |
| Heap                   |
| Stack                  |
| Variables              |
+------------------------+
```

Memory is isolated.

---

# Advantages of Processes

- Strong isolation
- Better fault tolerance
- True parallel execution
- Suitable for CPU-heavy workloads

---

# Disadvantages of Processes

- More memory usage
- Slower startup
- More expensive communication
- Data sharing requires special mechanisms

---

# Threads

A thread is a unit of execution **inside a process**.

A single process can have many threads.

```
Python Process

│

├── Thread 1

├── Thread 2

├── Thread 3
```

---

# Shared Memory

Unlike processes,

threads share:

- Heap
- Variables
- Objects
- File descriptors

Only their call stacks are separate.

---

# Thread Example

```
Python Process

↓

Shared Memory

↓

Thread A

Thread B

Thread C
```

Every thread can access the same objects.

---

# Advantages of Threads

- Lightweight
- Fast creation
- Shared memory
- Efficient for I/O-bound work

---

# Disadvantages of Threads

- Shared state
- Race conditions
- Synchronisation required
- Harder debugging

We'll study these problems later in the module.

---

# Context Switching

Suppose a CPU executes:

```
Task A
```

Suddenly,

the operating system pauses it.

```
↓

Task B
```

Later,

execution returns.

```
↓

Task A
```

This is called **context switching**.

---

# What Gets Saved?

The operating system saves:

- Program counter
- CPU registers
- Stack pointer
- Scheduling information

Later, it restores them.

The paused task continues as if nothing happened.

---

# Is Context Switching Free?

No.

Every switch requires work.

Too many context switches can reduce performance.

This is one reason why creating thousands of threads unnecessarily is a bad idea.

---

# How the Operating System Schedules Work

Modern operating systems maintain a scheduler.

Conceptually:

```
Ready Queue

↓

Task A

↓

Task B

↓

Task C

↓

CPU
```

The scheduler decides which task runs next.

Python does **not** directly schedule threads or processes.

The operating system does.

---

# Backend Example

Imagine an e-commerce service.

One request:

```
GET /products
```

Needs:

- PostgreSQL query
- Redis lookup
- Inventory service
- Recommendation service

While PostgreSQL is processing,

another thread can handle:

```
POST /login
```

This improves throughput.

---

# Choosing Between Processes and Threads

| Characteristic | Process | Thread |
|----------------|----------|---------|
| Memory | Separate | Shared |
| Startup Cost | Higher | Lower |
| Communication | Expensive | Cheap |
| Isolation | Strong | Weak |
| Crash Impact | Limited | Shared process affected |
| Best For | CPU-bound | I/O-bound |

---

# Production Examples

## Processes

- Image resizing
- Video transcoding
- PDF generation
- Data science workloads

---

## Threads

- Web servers
- Database access
- REST API clients
- File downloads
- Log processing
- Email sending

---

# Common Mistakes

## Mistake 1

Assuming concurrency always means faster execution.

If work is CPU-bound, adding threads may not improve performance.

---

## Mistake 2

Using processes for every problem.

Processes consume more memory and have higher startup costs.

---

## Mistake 3

Ignoring workload type.

The best solution depends on whether the application is CPU-bound or I/O-bound.

---

## Mistake 4

Assuming threads automatically run simultaneously.

Whether they truly execute in parallel depends on the runtime, operating system, hardware, and (in Python) the Global Interpreter Lock, which we'll study next.

---

# Best Practices

✅ Identify whether the workload is CPU-bound or I/O-bound before choosing a concurrency model.

✅ Prefer threads for waiting on external resources.

✅ Prefer processes for CPU-intensive calculations.

✅ Measure performance rather than relying on assumptions.

❌ Don't create unnecessary threads.

❌ Don't assume more threads always increase throughput.

---

# Production Insight

If you inspect a production FastAPI or Django deployment, you'll often find multiple worker **processes**, each handling many concurrent requests.

For example:

```
Machine

│

├── Worker Process 1

│      ├── Thread A

│      ├── Thread B

│

├── Worker Process 2

│      ├── Thread A

│      ├── Thread B
```

This hybrid approach combines:

- Process isolation
- Better CPU utilisation
- Efficient handling of I/O-bound requests

Understanding why this architecture is used will become clearer as we explore the Global Interpreter Lock and asynchronous programming.

---

# Questions

### Question

> What is the difference between concurrency and parallelism?

### Answer

Concurrency is the ability to make progress on multiple tasks during the same period, while parallelism means multiple tasks execute simultaneously on different CPU cores.

---

### Question

> When would you choose processes instead of threads?

### Answer

Processes are preferred for CPU-bound workloads because they provide separate memory spaces and can execute truly in parallel on multiple CPU cores.

---

### Question

> Why are threads useful for web applications?

### Answer

Web applications spend much of their time waiting for databases, files, or network responses. Threads allow other requests to be processed while one thread is waiting.

---

### Question

> What is context switching?

### Answer

Context switching is the operating system's process of saving the state of one task and restoring another so multiple tasks can share CPU time.

---

### Question

> Why do processes consume more memory than threads?

### Answer

Each process has its own address space and interpreter, whereas threads share most resources within the same process.

---

# Practical Lesson

Create:

```text
concurrency_concepts.py
```

```python
"""
This example demonstrates the conceptual difference between
CPU-bound and I/O-bound work.
"""

import time

# ----------------------------
# CPU-bound example
# ----------------------------
def cpu_task():
    total = 0
    for number in range(5_000_000):
        total += number
    return total

# ----------------------------
# I/O-bound example
# ----------------------------
def io_task():
    print("Waiting for external resource...")
    time.sleep(2)
    print("Finished waiting")

print("Starting CPU task...")
cpu_task()
print("CPU task complete")

print("\nStarting I/O task...")
io_task()
```

Expected Output

```text
Starting CPU task...
CPU task complete

Starting I/O task...
Waiting for external resource...
Finished waiting
```

Although both tasks take time, the CPU task spends nearly all of its time computing, while the I/O task spends most of its time waiting.

---

# Questions

## Question 1

What is the difference between a process and a thread?

### Answer

A process has its own memory and resources, while threads execute within a process and share its memory.

---

## Question 2

What is a CPU-bound workload?

### Answer

A workload where computation is the primary bottleneck, such as encryption or image processing.

---

## Question 3

What is an I/O-bound workload?

### Answer

A workload that spends most of its time waiting for external operations like databases, files, or network communication.

---

## Question 4

Why is context switching necessary?

### Answer

It allows multiple tasks to share CPU time by pausing one task and resuming another.

---

## Question 5

Why are backend APIs usually considered I/O-bound?

### Answer

Because they spend much of their execution time waiting for databases, caches, external APIs, file systems, or message brokers.

---

# Assignment

## Exercise 1

Classify the following as **CPU-bound** or **I/O-bound** and explain why:

- Password hashing
- PostgreSQL query
- Reading a CSV file
- Image resizing
- REST API call
- Video encoding
- Redis lookup
- Sending an email

---

## Exercise 2

Draw a diagram showing the relationship between:

- Operating system
- Processes
- Threads
- CPU cores

Explain how they interact.

---

## Exercise 3

Research how your operating system schedules processes and threads.

Write a one-page summary describing:

- Time slicing
- Context switching
- Priority scheduling

---

## Exercise 4

Take a typical FastAPI endpoint from one of your projects and identify every operation that is CPU-bound and every operation that is I/O-bound.

Suggest which concurrency model would best suit each operation.

---

# Summary

In this lesson, you learned:

- ✅ The difference between concurrency and parallelism.
- ✅ Why backend systems rely on concurrency.
- ✅ What processes are.
- ✅ What threads are.
- ✅ Process isolation and shared memory.
- ✅ CPU-bound vs I/O-bound workloads.
- ✅ Context switching.
- ✅ Operating system scheduling.
- ✅ When to choose processes versus threads.

---

# Next Lesson

**File:**
[42-Concurrency-part-2-The-Global-Interpreter-Lock](42-concurrency-part-2-the-global-interpreter-lock.md)

In the next lesson, we'll explore one of the most misunderstood aspects of Python: the **Global Interpreter Lock (GIL)**. You'll learn why CPU-bound threads often fail to scale, how the GIL works internally in CPython, when it is released, common misconceptions, and how it influences the design of production Python applications.
