# File: python/50-concurrency-part-10-process-start-methods.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 10: Process Start Methods (`fork`, `spawn`, and `forkserver`)

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 50
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `multiprocessing.set_start_method()` | Python 3.4 |
| `multiprocessing.get_start_method()` | Python 3.4 |
| `forkserver` | Python 3.4 (Unix) |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why process start methods exist
- The difference between `fork`, `spawn`, and `forkserver`
- How operating systems create processes
- Copy-on-Write (CoW)
- Platform differences
- Why Windows behaves differently
- Why `if __name__ == "__main__":` is mandatory
- Choosing the correct start method
- Production best practices
- questions

______________________________________________________________________

# Recap

So far we've learned:

- Multiprocessing
- Process communication
- Process pools

Creating a process looked simple:

```python
process.start()
```

But what actually happens?

How does the operating system create a new Python process?

The answer depends on the **start method**.

______________________________________________________________________

# Why Start Methods Exist

When Python creates a child process, it must answer several questions:

- Should memory be copied?
- Should the interpreter restart?
- Should existing threads be copied?
- Should open files be inherited?
- Should sockets be inherited?

Different operating systems answer these questions differently.

______________________________________________________________________

# Three Start Methods

Python supports three process start methods.

```
fork

spawn

forkserver
```

Not every operating system supports all three.

______________________________________________________________________

# Operating System Support

| Platform | Default Method |
|-----------|----------------|
| Linux | `fork` |
| macOS | `spawn` (Python 3.8+) |
| Windows | `spawn` |

Notice that Windows does **not** support `fork`.

______________________________________________________________________

# Checking the Current Start Method

```python
import multiprocessing

print(
    multiprocessing.get_start_method()
)
```

Possible output

```text
fork
```

or

```text
spawn
```

depending on your platform.

______________________________________________________________________

# Setting the Start Method

```python
import multiprocessing

multiprocessing.set_start_method(
    "spawn"
)
```

This must be called before creating any child processes.

Only one start method may be selected for a program.

______________________________________________________________________

# Understanding `fork`

`fork` is the traditional Unix process creation mechanism.

```
Parent Process

↓

fork()

↓

Child Process
```

Initially,

the child appears to be an exact copy of the parent.

______________________________________________________________________

# What Gets Copied?

Imagine the parent process contains:

```
Variables

Functions

Objects

Modules

Open Files

Memory
```

After `fork`:

```
Parent

↓

Memory

↓

Copied (Logically)

↓

Child
```

The child starts with almost the same state.

______________________________________________________________________

# Is Memory Really Copied?

Not immediately.

Modern operating systems use:

```
Copy-on-Write (CoW)
```

______________________________________________________________________

# Copy-on-Write

Initially,

both processes share the same physical memory pages.

```
Parent

↓

Shared Memory Pages

↑

Child
```

No actual copying occurs.

______________________________________________________________________

# What Happens on Modification?

Suppose the child modifies:

```python
counter += 1
```

Now the operating system creates a private copy of only the modified memory page.

```
Shared Page

↓

Write Operation

↓

Duplicate Page

↓

Independent Copies
```

This optimisation is called:

```
Copy-on-Write
```

______________________________________________________________________

# Advantages of `fork`

- Extremely fast
- Efficient memory usage
- Minimal startup overhead
- Excellent for CPU-bound workloads

______________________________________________________________________

# Disadvantages of `fork`

Copying an already-running process also copies:

- Existing locks
- Internal interpreter state
- Partially completed operations
- Thread state

This can introduce subtle bugs.

______________________________________________________________________

# Threads and `fork`

Suppose the parent has:

```
Thread A

Thread B

Thread C
```

After `fork`:

Only the thread that called `fork()` exists in the child.

The other threads disappear.

However,

their locks and shared resources may remain in inconsistent states.

This is why combining threads and `fork` requires great care.

______________________________________________________________________

# Understanding `spawn`

Unlike `fork`,

`spawn` starts a completely new Python interpreter.

```
Parent

↓

Start New Interpreter

↓

Import Main Module

↓

Run Target Function
```

Nothing is copied from the running interpreter.

______________________________________________________________________

# What Happens During `spawn`?

The operating system:

- Starts a new Python interpreter
- Imports your program
- Recreates required objects
- Executes the requested function

The child begins almost as if you launched:

```bash
python app.py
```

again.

______________________________________________________________________

# Advantages of `spawn`

- Clean interpreter state
- Safe with threads
- Predictable behaviour
- Platform independent

______________________________________________________________________

# Disadvantages of `spawn`

Every child must:

- Start a new interpreter
- Import modules
- Construct objects

This makes it slower than `fork`.

______________________________________________________________________

# Why `spawn` Requires Pickling

Since the child starts from scratch,

Python cannot simply share existing objects.

Instead,

functions and arguments must be serialized.

```
Parent

↓

Pickle

↓

Child

↓

Unpickle

↓

Execute
```

Therefore,

only picklable objects can be passed.

______________________________________________________________________

# Understanding `forkserver`

`forkserver` combines ideas from both approaches.

```
Main Process

↓

Fork Server

↓

Worker Processes
```

Instead of every process calling `fork()`,

a dedicated server creates child processes.

______________________________________________________________________

# Why Use `forkserver`?

The fork server starts before extra threads or complex application state exist.

Later,

all new worker processes are created from this clean server.

This reduces many of the problems associated with calling `fork()` in a multithreaded program.

______________________________________________________________________

# Choosing a Start Method

| Requirement | Recommended Method |
|--------------|--------------------|
| Maximum performance on Linux | `fork` |
| Cross-platform compatibility | `spawn` |
| Thread-heavy Unix application | `forkserver` |
| Windows | `spawn` |

______________________________________________________________________

# The `__main__` Guard

This is one of the most important multiprocessing rules.

Always write:

```python
if __name__ == "__main__":
    ...
```

______________________________________________________________________

# Why Is It Necessary?

Suppose your file contains:

```python
process.start()
```

With `spawn`:

```
Start Child

↓

Import Module

↓

Execute Top-Level Code

↓

Create Another Child

↓

Import Module

↓

Create Another Child

↓

...
```

Without protection,

the program repeatedly creates new processes.

______________________________________________________________________

# Correct Example

```python
from multiprocessing import Process


def worker():

    print("Working...")


if __name__ == "__main__":

    process = Process(target=worker)

    process.start()

    process.join()
```

This prevents recursive process creation.

______________________________________________________________________

# Incorrect Example

```python
from multiprocessing import Process


def worker():

    print("Working...")


process = Process(target=worker)

process.start()
```

This may work with `fork`,

but usually fails on Windows and with `spawn`.

______________________________________________________________________

# Process Creation Comparison

## `fork`

```
Parent

↓

Copy Process

↓

Run Child
```

______________________________________________________________________

## `spawn`

```
Parent

↓

New Interpreter

↓

Import Module

↓

Execute Child
```

______________________________________________________________________

## `forkserver`

```
Parent

↓

Fork Server

↓

Create Worker

↓

Execute
```

______________________________________________________________________

# Production Example

Suppose you deploy a FastAPI application.

```
Gunicorn

↓

4 Worker Processes

↓

Each Worker

↓

Multiple Threads
```

Choosing the wrong process creation method may cause:

- Deadlocks
- Frozen locks
- Unexpected behaviour
- Increased startup time

Understanding process creation is essential for diagnosing production issues.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting:

```python
if __name__ == "__main__":
```

This is one of the most common multiprocessing errors.

______________________________________________________________________

## Mistake 2

Assuming `fork` works everywhere.

Windows only supports `spawn`.

______________________________________________________________________

## Mistake 3

Passing non-picklable objects.

Examples include:

- Open sockets
- Thread locks
- Database connections
- File handles

These cannot usually be transferred to spawned processes.

______________________________________________________________________

## Mistake 4

Using `fork` in applications with many threads without understanding the risks.

______________________________________________________________________

# Best Practices

✅ Always use the `__main__` guard.

✅ Design multiprocessing code to work with `spawn`.

✅ Keep process arguments simple and picklable.

✅ Test on every supported operating system.

✅ Understand your deployment platform.

❌ Don't rely on Linux-only behaviour if your application must run on Windows or macOS.

______________________________________________________________________

# Production Insight

Many production bugs appear only after deployment because development often occurs on one operating system while
production runs on another.

Example:

- Developer laptop: macOS (`spawn`)
- CI pipeline: Linux (`fork`)
- Customer environment: Windows (`spawn`)

Writing multiprocessing code that works correctly with `spawn` generally leads to more portable and reliable
applications.

______________________________________________________________________

# Questions

### Question

> Why is `fork` faster than `spawn`?

### Answer

Because `fork` initially shares the parent's memory using Copy-on-Write instead of starting a completely new
interpreter.

______________________________________________________________________

### Question

> Why is `spawn` safer?

### Answer

Because every child starts with a fresh interpreter, avoiding inherited locks, threads, and inconsistent runtime state.

______________________________________________________________________

### Question

> What is Copy-on-Write?

### Answer

A memory optimisation where parent and child initially share memory pages until one process modifies them, at which
point only the modified pages are copied.

______________________________________________________________________

### Question

> Why is `if __name__ == "__main__":` required?

### Answer

It prevents recursive process creation when using the `spawn` start method.

______________________________________________________________________

### Question

> Which start method should be preferred for cross-platform applications?

### Answer

`spawn`, because it is supported on all major platforms and provides consistent behaviour.

______________________________________________________________________

# Practical Lesson

Create:

```text
start_method_demo.py
```

```python
import multiprocessing
import os


def worker():

    print(
        f"Worker PID: {os.getpid()}"
    )


if __name__ == "__main__":

    print(
        "Start Method:",
        multiprocessing.get_start_method()
    )

    process = multiprocessing.Process(
        target=worker
    )

    process.start()

    process.join()
```

Experiment by changing the start method:

```python
multiprocessing.set_start_method("spawn")
```

and

```python
multiprocessing.set_start_method("fork")
```

(if your operating system supports it).

Observe:

- Startup behaviour
- Platform differences
- Performance differences

______________________________________________________________________

# Questions

## Question 1

Why does Python support multiple process start methods?

### Answer

Different operating systems provide different process creation mechanisms, each with unique trade-offs in performance,
safety, and compatibility.

______________________________________________________________________

## Question 2

What is the main difference between `fork` and `spawn`?

### Answer

`fork` duplicates the current process using Copy-on-Write, while `spawn` starts a completely new Python interpreter.

______________________________________________________________________

## Question 3

Why is `spawn` slower?

### Answer

Because every child process must start a new interpreter, import modules, and reconstruct the execution environment.

______________________________________________________________________

## Question 4

Why is the `__main__` guard essential?

### Answer

It prevents child processes created with `spawn` from repeatedly executing top-level code and recursively creating more
child processes.

______________________________________________________________________

## Question 5

What is the purpose of `forkserver`?

### Answer

It uses a dedicated server process to safely create new child processes, reducing issues associated with calling
`fork()` from multithreaded applications.

______________________________________________________________________

# Assignment

## Exercise 1

Print the current multiprocessing start method on your operating system.

Research why it is the default.

______________________________________________________________________

## Exercise 2

Run the same multiprocessing program on:

- Linux (or WSL)
- macOS (if available)
- Windows (if available)

Compare the observed behaviour.

______________________________________________________________________

## Exercise 3

Remove the `if __name__ == "__main__":` guard.

Observe what happens using the `spawn` method.

Restore the guard afterwards.

______________________________________________________________________

## Exercise 4

Research Copy-on-Write.

Explain:

- Why it improves performance
- When memory is actually copied
- Why it benefits `fork`

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why process start methods exist.
- ✅ How `fork`, `spawn`, and `forkserver` work.
- ✅ Copy-on-Write memory optimisation.
- ✅ Platform differences.
- ✅ Why the `__main__` guard is mandatory.
- ✅ Production implications of each start method.
- ✅ Best practices for writing portable multiprocessing applications.

______________________________________________________________________

# Next Lesson

**File:** [51-concurrency-part-11-asyncio-fundamentals](51-concurrency-part-11-asyncio-fundamentals.md)

In the next lesson, we'll begin one of the most important modules for modern backend development: **Async Programming
with `asyncio`**. You'll learn what asynchronous programming is, why it exists, the event loop, coroutines, cooperative
multitasking, and how `asyncio` differs fundamentally from threading and multiprocessing. This marks the transition into
the concurrency model used by modern frameworks such as FastAPI, Starlette, Uvicorn, and many high-performance Python
services.
