# File: python/42-concurrency-part-2-the-global-interpreter-lock.md

# Advanced Python Runtime & Concurrency
# Concurrency Part 2: The Global Interpreter Lock (GIL)

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 42
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 6–7 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| Global Interpreter Lock (CPython) | Python 1.0 |
| `sys.getswitchinterval()` | Python 3.2 |
| `sys.setswitchinterval()` | Python 3.2 |

> **Important:** The GIL is an implementation detail of **CPython**, not of the Python language itself. Other Python implementations may use different concurrency models.

---

# Learning Objectives

By the end of this lesson, you will understand:

- What the GIL is
- Why the GIL exists
- CPython internals
- Reference counting and thread safety
- How the GIL works
- Thread scheduling
- When the GIL is released
- CPU-bound vs I/O-bound threading
- Common misconceptions
- Production implications

---

# Recap

In the previous lesson, we learned:

- Processes
- Threads
- Concurrency
- Parallelism
- CPU-bound workloads
- I/O-bound workloads

A natural question follows:

> If threads are lightweight, why doesn't every Python application simply create hundreds of threads?

The answer lies in one of CPython's most important design decisions:

**The Global Interpreter Lock (GIL).**

---

# What is the GIL?

The Global Interpreter Lock is a **process-wide mutex** inside CPython.

It ensures that:

> **Only one thread executes Python bytecode at a time within a single Python process.**

Notice the wording carefully.

It does **not** say:

- One thread in the entire operating system
- One thread on the entire machine

It only applies to:

```
One CPython Process
```

---

# Why Does the GIL Exist?

To answer this, we must revisit something you learned much earlier.

Remember:

```
Objects

↓

Reference Counts

↓

Garbage Collection
```

Every Python object stores a reference count.

Example

```
Object

Reference Count = 3
```

Whenever a reference changes:

```
Reference Count++

or

Reference Count--
```

These operations happen constantly.

---

# Imagine Two Threads

Suppose two threads both execute

```python
user = None
```

at nearly the same time.

Internally, CPython needs to do something like:

```
Read reference count

↓

Subtract 1

↓

Write reference count
```

Now imagine two CPUs modifying that value simultaneously.

Without protection:

```
Thread A

Reference Count = 5

↓

Thread B

Reference Count = 5

↓

Both write 4
```

Correct value:

```
3
```

Instead:

```
4
```

Memory corruption.

Eventually:

- Memory leaks
- Crashes
- Objects freed too early

---

# The Original Design Decision

When Python was created in the early 1990s:

The goals were:

- Simplicity
- Stability
- Portability

Adding a single global lock made:

- Memory management simpler
- Extension development easier
- The interpreter much safer

The trade-off:

Reduced CPU parallelism.

---

# What Does the GIL Actually Lock?

Many developers imagine this:

```
Entire Python Program

↓

Locked
```

That's incorrect.

The GIL protects:

```
Python Bytecode Execution
```

Only one thread may execute Python bytecode at any instant.

---

# Visualisation

```
Python Process

│

├── Thread A

├── Thread B

├── Thread C

↓

Global Interpreter Lock

↓

Python Interpreter
```

Only one thread passes through the lock at a time.

---

# Example

Imagine:

```python
while True:
    total += 1
```

Two threads execute this simultaneously.

Reality:

```
Thread A

Running

↓

Paused

↓

Thread B

Running

↓

Paused

↓

Thread A
```

Not

```
Thread A + Thread B

Running Together
```

---

# Does the GIL Affect Processes?

No.

Each process owns its own interpreter.

```
Process A

↓

Own GIL


Process B

↓

Own GIL
```

Multiple processes can execute simultaneously on different CPU cores.

This is why multiprocessing achieves real parallelism.

---

# CPU-Bound Example

Consider:

```python
def calculate():
    total = 0

    for i in range(100_000_000):
        total += i
```

Now launch:

- Thread A
- Thread B

Expectation:

```
2x Faster
```

Reality:

Almost no improvement.

Sometimes it is even slower because of context switching.

---

# Why?

Both threads repeatedly compete for:

```
GIL

↓

Execute Bytecode

↓

Release

↓

Acquire Again
```

Only one thread is making progress at a time.

---

# I/O-Bound Example

Suppose a thread performs:

```python
response = requests.get(url)
```

What happens?

```
Send HTTP Request

↓

Wait...

↓

Receive Response
```

While waiting:

The thread isn't executing Python instructions.

CPython can safely release the GIL.

Another thread begins running.

---

# When Does Python Release the GIL?

The GIL is commonly released during blocking operations such as:

- Socket communication
- File I/O
- Database queries
- Sleeping (`time.sleep()`)
- Many C extensions performing long-running native work

This allows another thread to execute while the current thread waits.

---

# Example

```python
import threading
import time

def worker(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")

t1 = threading.Thread(target=worker, args=("A",))
t2 = threading.Thread(target=worker, args=("B",))

t1.start()
t2.start()

t1.join()
t2.join()
```

Although both threads call `sleep()`, the program finishes in approximately two seconds rather than four because `time.sleep()` releases the GIL while waiting.

---

# Thread Switching

CPython periodically allows another thread to run.

You can inspect the switching interval.

```python
import sys

print(sys.getswitchinterval())
```

Typical output:

```text
0.005
```

Approximately:

```
5 milliseconds
```

This is not a guarantee that threads switch every 5 ms.

It is the interpreter's scheduling interval.

---

# Does Every Python Operation Hold the GIL?

No.

Many C extensions deliberately release it.

Examples include:

- NumPy
- OpenSSL operations
- Compression libraries
- Image processing libraries

These libraries perform heavy computation in native code, allowing true CPU parallelism internally.

---

# Example

```
Python

↓

NumPy

↓

Native C Loop

↓

GIL Released

↓

Multiple CPU Cores
```

This is one reason scientific Python performs so well.

---

# Common Misconception #1

> "Python threads are useless."

False.

They are extremely useful for:

- Web servers
- Downloading files
- Database queries
- Message queues
- API clients
- Network services

These are mostly I/O-bound.

---

# Common Misconception #2

> "The GIL makes Python slow."

Not exactly.

Most backend applications spend much of their time waiting:

- PostgreSQL
- Redis
- Kafka
- External APIs
- Files

During these waits, other threads can run.

The GIL is rarely the primary bottleneck in typical web applications.

---

# Common Misconception #3

> "Removing the GIL would automatically make Python faster."

Not necessarily.

Removing the GIL introduces:

- More locking
- Increased complexity
- Additional memory overhead
- Compatibility challenges

The design trade-offs are significant.

---

# Production Example

Consider a FastAPI application.

One request:

```
Receive Request

↓

Validate JSON

↓

Query PostgreSQL

↓

Query Redis

↓

Call Payment API

↓

Return Response
```

Where is most of the time spent?

Usually:

```
Waiting
```

Not computing.

Therefore, threads remain effective despite the GIL.

---

# When Should You Use Threads?

Ideal for:

- HTTP requests
- Database access
- File operations
- SMTP
- S3 uploads
- Redis
- Kafka consumers
- Web scraping

---

# When Should You Use Processes?

Ideal for:

- Video encoding
- Encryption
- Scientific computing
- Machine learning inference
- Image processing
- Large numerical calculations

---

# Threads vs Processes

| Workload | Best Choice |
|-----------|-------------|
| Database queries | Threads |
| API requests | Threads |
| File I/O | Threads |
| Image processing | Processes |
| Video transcoding | Processes |
| Scientific calculations | Processes |

---

# CPython Internals

A simplified execution cycle:

```
Thread Requests GIL

↓

GIL Granted

↓

Execute Python Bytecode

↓

Blocking Operation?

↓

Yes

↓

Release GIL

↓

Another Thread Runs
```

This cycle repeats continuously throughout program execution.

---

# Common Mistakes

## Mistake 1

Expecting CPU-bound threads to scale across multiple CPU cores.

Use processes instead.

---

## Mistake 2

Assuming every library behaves identically.

Many C extensions release the GIL internally.

---

## Mistake 3

Creating hundreds of threads for CPU-intensive work.

This often increases overhead without improving throughput.

---

## Mistake 4

Blaming every performance issue on the GIL.

Always profile your application before drawing conclusions.

---

# Best Practices

✅ Use threads for I/O-bound workloads.

✅ Use processes for CPU-bound workloads.

✅ Understand that the GIL is specific to CPython.

✅ Profile before optimising.

✅ Prefer high-level concurrency libraries when possible.

❌ Don't assume more threads equal more performance.

❌ Don't optimise for the GIL without measuring real bottlenecks.

---

# Production Insight

Most production Python web services are limited by:

- Database latency
- Network latency
- Disk I/O
- External services

—not by the GIL.

This is why frameworks such as FastAPI, Django, and Flask continue to perform well despite the GIL.

Understanding where your application spends its time is far more valuable than simply knowing that the GIL exists.

---

# Questions

### Question

> What is the Global Interpreter Lock?

### Answer

The GIL is a mutex in CPython that allows only one thread at a time to execute Python bytecode within a single process.

---

### Question

> Why was the GIL introduced?

### Answer

It simplifies memory management, particularly reference counting, making the interpreter easier to implement and thread-safe.

---

### Question

> Why don't CPU-bound Python threads scale well?

### Answer

Because only one thread can execute Python bytecode at a time within a process due to the GIL.

---

### Question

> Why are Python threads still useful?

### Answer

Because they perform well for I/O-bound workloads where threads spend much of their time waiting for external resources, allowing other threads to execute.

---

### Question

> Does multiprocessing avoid the GIL?

### Answer

Yes. Each process has its own Python interpreter and its own GIL, enabling true parallel execution across CPU cores.

---

# Practical Lesson

Create:

```text
gil_demo.py
```

```python
import threading
import time


def cpu_task():
    total = 0
    for i in range(50_000_000):
        total += i


def io_task():
    time.sleep(2)


# CPU-bound demonstration
start = time.perf_counter()

t1 = threading.Thread(target=cpu_task)
t2 = threading.Thread(target=cpu_task)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"CPU-bound: {time.perf_counter() - start:.2f} seconds")

# I/O-bound demonstration
start = time.perf_counter()

t1 = threading.Thread(target=io_task)
t2 = threading.Thread(target=io_task)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"I/O-bound: {time.perf_counter() - start:.2f} seconds")
```

Observe that:

- The CPU-bound section gains little benefit from threading.
- The I/O-bound section completes in roughly the same time as a single `sleep(2)` because both threads wait concurrently.

---

# Questions

## Question 1

Why does the GIL exist?

### Answer

To simplify CPython's memory management and make reference counting thread-safe.

---

## Question 2

Does the GIL prevent multiprocessing?

### Answer

No. Each process has its own interpreter and its own GIL.

---

## Question 3

When is the GIL typically released?

### Answer

During blocking operations such as network I/O, file I/O, database operations, `time.sleep()`, and many native C extension calls.

---

## Question 4

Why are threads suitable for web servers?

### Answer

Because web servers spend much of their time waiting for external resources, allowing other threads to execute while one thread is blocked.

---

## Question 5

What is the biggest misconception about the GIL?

### Answer

That it makes Python threads useless. In reality, threads are highly effective for I/O-bound applications.

---

# Assignment

## Exercise 1

Run the CPU-bound and I/O-bound examples on your machine.

Record:

- Execution time
- CPU utilisation
- Your observations

Explain why the results differ.

---

## Exercise 2

Research three popular Python libraries that release the GIL internally.

For each library, explain:

- What it does
- Why releasing the GIL improves performance

---

## Exercise 3

Take one of your existing FastAPI endpoints and identify:

- CPU-bound sections
- I/O-bound sections

Suggest whether threads or processes would be more appropriate for each.

---

## Exercise 4

Draw a diagram illustrating:

- Multiple threads
- A single GIL
- Python bytecode execution
- Blocking I/O
- GIL release and reacquisition

---

# Summary

In this lesson, you learned:

- ✅ What the Global Interpreter Lock is.
- ✅ Why CPython introduced the GIL.
- ✅ How the GIL protects reference counting.
- ✅ Why CPU-bound threads rarely scale.
- ✅ Why I/O-bound threads perform well.
- ✅ When the GIL is released.
- ✅ Common misconceptions about Python threading.
- ✅ Production implications of the GIL.
- ✅ Senior backend interview topics.

---

# Next Lesson

**File:**
[43-Concurrency-part-3-Threading-Module](43-concurrency-part-3-threading-module.md)

In the next lesson, we'll move from theory to implementation. You'll learn how to create and manage threads using Python's `threading` module, including thread lifecycle, daemon threads, thread naming, `join()`, communication patterns, and production-ready threading practices.
