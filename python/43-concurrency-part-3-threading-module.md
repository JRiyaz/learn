# File: python/43-concurrency-part-3-threading-module.md

# Advanced Python Runtime & Concurrency
# Concurrency Part 3: The `threading` Module

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 43
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 6–7 Hours

---

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `threading` module | Python 1.5.2 |
| `Thread` class | Python 1.5.2 |
| `current_thread()` | Python 2.3 |
| `main_thread()` | Python 3.4 |

---

# Learning Objectives

By the end of this lesson, you will understand:

- The `threading` module
- Creating threads
- Thread lifecycle
- Main thread
- Daemon vs non-daemon threads
- Thread naming
- `join()`
- Thread communication basics
- Thread-safe design principles
- Production use cases

---

# Recap

In the previous lesson, we learned about the **Global Interpreter Lock (GIL)**.

We discovered:

- Only one thread executes Python bytecode at a time.
- Threads are still excellent for I/O-bound workloads.
- Processes are better suited for CPU-bound workloads.

Now it's time to start writing multithreaded programs.

---

# What is the `threading` Module?

The `threading` module provides a high-level interface for creating and managing threads.

Instead of dealing directly with operating system APIs, Python gives us a clean abstraction.

```python
import threading
```

---

# Your First Thread

```python
import threading

def worker():
    print("Worker thread running")

thread = threading.Thread(target=worker)

thread.start()

thread.join()
```

Output

```text
Worker thread running
```

This is the smallest useful multithreaded Python program.

---

# Understanding `Thread`

```python
thread = threading.Thread(
    target=worker
)
```

Here:

- `Thread` creates a new thread object.
- `target` specifies the function that will execute.
- Nothing starts yet.

Think of this as creating a process description.

---

# `start()` vs Calling the Function

Consider:

```python
worker()
```

This executes immediately in the current thread.

Now compare:

```python
thread.start()
```

This tells the operating system:

> Create a new thread and execute `worker()` inside it.

This distinction is extremely important.

---

# Common Beginner Mistake

Wrong

```python
thread = threading.Thread(
    target=worker()
)
```

What happens?

Python executes:

```python
worker()
```

first.

Then its return value becomes the target.

Correct

```python
thread = threading.Thread(
    target=worker
)
```

Notice:

No parentheses.

---

# Thread Lifecycle

Every thread moves through several states.

```
Created

↓

Runnable

↓

Running

↓

Waiting (optional)

↓

Finished
```

Once a thread finishes, it cannot be restarted.

---

# Demonstration

```python
import threading
import time

def worker():
    print("Starting")
    time.sleep(2)
    print("Finished")

thread = threading.Thread(target=worker)

thread.start()
```

Timeline

```
Main Thread

↓

Create Thread

↓

Start Thread

↓

Worker Executes

↓

Worker Ends
```

---

# The Main Thread

Every Python program begins with one thread.

```
Python Process

↓

Main Thread
```

Even programs that never use `threading` are running inside the main thread.

---

# Identifying the Current Thread

```python
import threading

print(threading.current_thread())
```

Example output

```text
<_MainThread(MainThread, started ...)>
```

---

# Naming Threads

By default

```text
Thread-1

Thread-2

Thread-3
```

You can assign meaningful names.

```python
thread = threading.Thread(
    target=worker,
    name="EmailSender"
)
```

Later

```python
print(
    threading.current_thread().name
)
```

Output

```text
EmailSender
```

Useful for:

- Logging
- Debugging
- Monitoring

---

# Passing Arguments

Use

```python
args=
```

Example

```python
import threading

def greet(name):

    print(f"Hello {name}")

thread = threading.Thread(
    target=greet,
    args=("Alice",)
)

thread.start()
thread.join()
```

Notice

A single-element tuple requires a trailing comma.

---

# Multiple Arguments

```python
def add(a, b):

    print(a + b)

thread = threading.Thread(
    target=add,
    args=(10, 20)
)
```

---

# Keyword Arguments

```python
def welcome(name, city):

    print(name, city)

thread = threading.Thread(
    target=welcome,
    kwargs={
        "name": "Alice",
        "city": "London"
    }
)
```

---

# Waiting for a Thread

Suppose

```python
thread.start()
```

Does the main program wait?

No.

It continues immediately.

---

# `join()`

```python
thread.start()

thread.join()

print("Finished")
```

Timeline

```
Main

↓

Start Thread

↓

Wait

↓

Thread Ends

↓

Continue
```

Without `join()`

```
Main

↓

Start Thread

↓

Continue Immediately
```

---

# Multiple Threads

```python
import threading
import time

def worker(number):

    print(f"Worker {number} starting")

    time.sleep(2)

    print(f"Worker {number} finished")

threads = []

for i in range(3):

    thread = threading.Thread(
        target=worker,
        args=(i,)
    )

    thread.start()

    threads.append(thread)

for thread in threads:

    thread.join()

print("All workers completed")
```

---

# Parallel Waiting

Suppose every worker sleeps:

```
2 seconds
```

Three sequential calls:

```
2 + 2 + 2

=

6 seconds
```

Three threads:

```
2 seconds

approximately
```

Because sleeping releases the GIL.

---

# Daemon Threads

Some threads should not prevent program exit.

Example:

- Metrics collector
- Background logger
- Cache cleaner

These are called daemon threads.

---

# Creating a Daemon Thread

```python
thread = threading.Thread(
    target=worker,
    daemon=True
)
```

If the main program exits,

daemon threads terminate automatically.

---

# Non-Daemon Threads

Default behaviour:

```python
daemon=False
```

Python waits for them before exiting.

Example:

```
Main Thread Ends

↓

Worker Still Running

↓

Python Waits

↓

Program Exits
```

---

# Daemon vs Non-Daemon

| Feature | Daemon | Non-Daemon |
|----------|---------|------------|
| Keeps program alive | ❌ | ✅ |
| Suitable for background work | ✅ | Sometimes |
| Automatically terminated | ✅ | ❌ |

---

# Checking if a Thread is Alive

```python
print(thread.is_alive())
```

Example

```python
thread.start()

print(thread.is_alive())

thread.join()

print(thread.is_alive())
```

Output

```text
True

False
```

Useful for monitoring.

---

# Thread Identity

Each thread has a unique identifier.

```python
print(threading.get_ident())
```

Or

```python
print(
    threading.current_thread().ident
)
```

Useful in:

- Logging
- Debugging
- Profiling

---

# Enumerating Threads

See all active threads.

```python
import threading

print(
    threading.enumerate()
)
```

Useful when diagnosing applications.

---

# Thread Communication (Preview)

Suppose

Thread A downloads a file.

Thread B processes it.

How do they communicate?

Not like this:

```python
global data
```

Shared globals quickly become difficult to manage.

We'll later study:

- Locks
- Queues
- Events
- Conditions

These are the preferred mechanisms.

---

# Production Example

Imagine an API endpoint.

```
Receive Request

↓

Store in Database

↓

Send Confirmation Email
```

The email may take several seconds.

Instead:

```
Main Request

↓

Respond Immediately


Background Thread

↓

Send Email
```

The user receives a faster response.

> **Note:** In large production systems, background jobs are usually handled by task queues such as Celery or message brokers rather than raw threads, but understanding threads is still essential.

---

# Common Mistakes

## Mistake 1

Calling the function instead of passing it.

Wrong

```python
target=worker()
```

Correct

```python
target=worker
```

---

## Mistake 2

Forgetting `join()` when the result of the thread is required before continuing.

---

## Mistake 3

Trying to restart a finished thread.

A `Thread` object can only be started once.

---

## Mistake 4

Using daemon threads for important work.

Daemon threads may terminate abruptly when the interpreter exits.

---

# Best Practices

✅ Give threads meaningful names.

✅ Use `join()` when synchronization is required.

✅ Keep thread functions small and focused.

✅ Prefer high-level concurrency abstractions when appropriate.

✅ Understand whether work is CPU-bound or I/O-bound.

❌ Don't share mutable global state unnecessarily.

❌ Don't create hundreds of threads without measuring performance.

---

# Production Insight

Many production frameworks use threads internally.

Examples include:

- Database connection pools
- Background log writers
- HTTP client libraries
- Monitoring agents
- File upload handlers

Even if you don't explicitly create threads, your application is likely using them through libraries.

Understanding the thread lifecycle helps when debugging deadlocks, hanging applications, or shutdown issues.

---

# Questions

### Question

> What is the difference between `start()` and directly calling the target function?

### Answer

Calling the function executes it immediately in the current thread. Calling `start()` creates a new operating system thread and executes the target function inside it.

---

### Question

> What does `join()` do?

### Answer

It blocks the calling thread until the target thread completes execution.

---

### Question

> What is a daemon thread?

### Answer

A daemon thread runs in the background and does not prevent the Python process from exiting. It is automatically terminated when all non-daemon threads finish.

---

### Question

> Can a thread be started twice?

### Answer

No. A `Thread` instance can only be started once. Attempting to call `start()` again raises a `RuntimeError`.

---

### Question

> Why should thread names be meaningful?

### Answer

Meaningful names improve logging, debugging, monitoring, and troubleshooting in production systems.

---

# Practical Lesson

Create:

```text
threading_basics.py
```

```python
import threading
import time


def download_file(filename):
    print(
        f"[{threading.current_thread().name}] "
        f"Downloading {filename}"
    )

    time.sleep(2)

    print(
        f"[{threading.current_thread().name}] "
        f"Finished {filename}"
    )


files = [
    "users.csv",
    "orders.csv",
    "products.csv",
]

threads = []

for file in files:

    thread = threading.Thread(
        target=download_file,
        args=(file,),
        name=f"Downloader-{file}"
    )

    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()

print("All downloads completed.")
```

Expected Output (order may vary)

```text
[Downloader-users.csv] Downloading users.csv
[Downloader-orders.csv] Downloading orders.csv
[Downloader-products.csv] Downloading products.csv
[Downloader-orders.csv] Finished orders.csv
[Downloader-users.csv] Finished users.csv
[Downloader-products.csv] Finished products.csv
All downloads completed.
```

---

# Questions

## Question 1

How do you create a thread in Python?

### Answer

Create a `threading.Thread` object with a target function and call `start()`.

---

## Question 2

What is the purpose of `join()`?

### Answer

To wait until another thread finishes execution.

---

## Question 3

What is the difference between daemon and non-daemon threads?

### Answer

Daemon threads terminate automatically when the interpreter exits, whereas non-daemon threads keep the process alive until they complete.

---

## Question 4

Can two threads share memory?

### Answer

Yes. Threads within the same process share the heap and can access the same Python objects.

---

## Question 5

Why is thread execution order unpredictable?

### Answer

Because thread scheduling is controlled by the operating system and the Python interpreter, not by the order in which `start()` is called.

---

# Assignment

## Exercise 1

Create five threads that simulate downloading five different files.

- Give each thread a meaningful name.
- Wait for all threads using `join()`.
- Print the total execution time.

---

## Exercise 2

Create one daemon thread and one non-daemon thread.

Observe what happens when the main program exits before both complete.

Explain the difference.

---

## Exercise 3

Write a program that periodically prints:

- Current thread name
- Thread ID
- Whether the thread is alive

Use `threading.current_thread()` and `is_alive()`.

---

## Exercise 4

Modify one of your previous FastAPI or Flask projects.

Identify one I/O-bound task that could safely run in a background thread.

Explain why it is appropriate and what potential limitations exist.

---

# Summary

In this lesson, you learned:

- ✅ How to create threads.
- ✅ The lifecycle of a thread.
- ✅ The difference between `start()` and calling a function directly.
- ✅ How `join()` works.
- ✅ Daemon vs non-daemon threads.
- ✅ Thread naming.
- ✅ Thread inspection utilities.
- ✅ Production threading practices.
- ✅ Common interview questions.

---

# Next Lesson

**File:**
[44-concurrency-part-4-thread-synchronization-locks](44-concurrency-part-4-thread-synchronization-locks.md)

In the next lesson, we'll study one of the most critical topics in concurrent programming: **thread synchronization**. You'll learn about race conditions, critical sections, `Lock`, `RLock`, deadlocks, lock ordering, and how to write thread-safe production code.
