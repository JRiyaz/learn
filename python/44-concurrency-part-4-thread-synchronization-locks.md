# File: python/44-concurrency-part-4-thread-synchronization-locks.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 4: Thread Synchronization - Locks, Race Conditions & Deadlocks

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 44
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 7 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `threading.Lock` | Python 1.5.2 |
| `threading.RLock` | Python 2.4 |
| Context Manager Support (`with`) | Python 2.5 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why synchronization is necessary
- Race conditions
- Critical sections
- Mutual exclusion
- `threading.Lock`
- `threading.RLock`
- Deadlocks
- Lock ordering
- Thread-safe programming
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how to:

- Create threads
- Start threads
- Wait using `join()`
- Create daemon threads
- Name threads

However, we ignored one major problem.

Suppose two threads modify the **same object**.

What happens?

The answer introduces one of the most important topics in concurrent programming.

______________________________________________________________________

# Shared Memory

Remember,

threads share memory.

```
Python Process

│

├── Thread A

├── Thread B

│

↓

Shared Objects
```

Both threads can access the same variable.

That sounds convenient.

It is also dangerous.

______________________________________________________________________

# Example

Suppose

```python
balance = 100
```

Thread A

```
Withdraw £20
```

Thread B

```
Withdraw £50
```

Expected result

```
£30
```

Can we guarantee that?

No.

______________________________________________________________________

# The Problem

Withdrawal is not a single operation.

Conceptually it is:

```
Read balance

↓

Subtract amount

↓

Write new balance
```

Three separate steps.

If another thread runs between them,

the result may become incorrect.

______________________________________________________________________

# Race Condition

A **race condition** occurs when:

> The correctness of a program depends on the unpredictable timing of multiple threads.

Example

Initial value

```
balance = 100
```

Thread A

```
Read 100

↓

Subtract 20

↓

Waiting...
```

Thread B

```
Read 100

↓

Subtract 50

↓

Write 50
```

Thread A resumes

```
Write 80
```

Final balance

```
80
```

Correct answer

```
30
```

One update was lost.

______________________________________________________________________

# Another Example

Counter

```python
counter = 0
```

Two threads execute

```python
counter += 1
```

100,000 times each.

Expected

```
200000
```

Actual

Maybe

```
187413

194220

198999
```

It varies.

______________________________________________________________________

# Why?

Many beginners think

```python
counter += 1
```

is one operation.

Internally it is approximately:

```
Read counter

↓

Add 1

↓

Write counter
```

Multiple steps.

Another thread can interrupt.

______________________________________________________________________

# Critical Section

A **critical section** is:

> A piece of code that accesses shared mutable data.

Example

```python
balance -= amount
```

Only one thread should execute this at a time.

______________________________________________________________________

# Mutual Exclusion

The solution is called:

```
Mutual Exclusion

↓

Mutex
```

Meaning

```
Only

One Thread

At A Time
```

______________________________________________________________________

# Introducing `Lock`

Python provides

```python
threading.Lock()
```

A lock protects critical sections.

______________________________________________________________________

# Creating a Lock

```python
import threading

lock = threading.Lock()
```

Initially

```
Unlocked
```

______________________________________________________________________

# Acquiring a Lock

```python
lock.acquire()

try:
    # Critical section

finally:
    lock.release()
```

Timeline

```
Thread A

Acquire

↓

Execute

↓

Release

↓

Thread B

Acquire

↓

Execute
```

Only one thread enters.

______________________________________________________________________

# Using `with`

The preferred approach is

```python
with lock:
    balance -= amount
```

Equivalent to

```python
lock.acquire()

try:
    ...

finally:
    lock.release()
```

Using `with` prevents accidentally forgetting to release the lock.

______________________________________________________________________

# Thread-Safe Counter

```python
import threading

counter = 0

lock = threading.Lock()

def increment():

    global counter

    for _ in range(100_000):

        with lock:

            counter += 1
```

Now,

every update is protected.

______________________________________________________________________

# Multiple Threads

```python
threads = []

for _ in range(2):

    thread = threading.Thread(
        target=increment
    )

    thread.start()

    threads.append(thread)

for thread in threads:

    thread.join()

print(counter)
```

Output

```text
200000
```

Every time.

______________________________________________________________________

# Lock Behaviour

Imagine

```
Thread A

↓

Acquire Lock

↓

Working...


Thread B

↓

Acquire Lock

↓

Wait...
```

Thread B blocks until Thread A releases the lock.

______________________________________________________________________

# Is Locking Free?

No.

Locks introduce overhead.

Every acquisition requires coordination.

Too much locking can reduce performance.

Always keep critical sections as small as possible.

______________________________________________________________________

# Good Locking

```python
with lock:

    counter += 1
```

Very small.

______________________________________________________________________

# Poor Locking

```python
with lock:

    download_large_file()

    process_image()

    save_database()

    send_email()
```

Every other thread waits unnecessarily.

______________________________________________________________________

# Lock Granularity

Fine-grained locking

```
Small Critical Sections

↓

More Concurrency
```

Coarse-grained locking

```
Large Critical Sections

↓

Less Concurrency
```

Finding the right balance is an important design skill.

______________________________________________________________________

# Lock Isn't Magic

A lock only protects the code that actually uses it.

Suppose

```python
balance -= amount
```

uses a lock,

but another function modifies

```python
balance
```

without the lock.

The race condition still exists.

Every access to shared mutable state must follow the same synchronization strategy.

______________________________________________________________________

# Reentrant Lock (`RLock`)

Suppose

```python
lock.acquire()

...

lock.acquire()
```

The same thread tries to acquire the same lock again.

With a normal `Lock`

```
Deadlock
```

______________________________________________________________________

# Example

```python
import threading

lock = threading.Lock()

def outer():

    with lock:

        inner()

def inner():

    with lock:

        print("Hello")
```

The thread waits forever.

It already owns the lock.

______________________________________________________________________

# Introducing `RLock`

```python
lock = threading.RLock()
```

An `RLock` allows:

```
Same Thread

↓

Acquire Again

↓

Acquire Again

↓

Release

↓

Release
```

Internally it keeps:

- Owner thread
- Acquisition count

The lock is released only when the acquisition count reaches zero.

______________________________________________________________________

# When Should You Use `RLock`?

Typical scenarios

- Recursive functions
- Nested function calls
- Object-oriented code where one locked method calls another locked method

Otherwise,

prefer a normal `Lock`.

It is simpler and slightly faster.

______________________________________________________________________

# Deadlock

A deadlock occurs when:

Two or more threads wait forever.

No thread can continue.

______________________________________________________________________

# Example

Thread A

```
Lock 1

↓

Waiting

↓

Lock 2
```

Thread B

```
Lock 2

↓

Waiting

↓

Lock 1
```

Result

```
Forever Waiting
```

______________________________________________________________________

# Visualisation

```
Thread A

↓

Lock A

↓

Waiting for Lock B


Thread B

↓

Lock B

↓

Waiting for Lock A
```

Neither thread can continue.

______________________________________________________________________

# Preventing Deadlocks

Rule 1

Acquire locks in a consistent order.

Example

Always

```
Lock A

↓

Lock B
```

Never

```
Lock B

↓

Lock A
```

______________________________________________________________________

Rule 2

Keep locks for the shortest possible time.

______________________________________________________________________

Rule 3

Avoid nested locks when possible.

______________________________________________________________________

Rule 4

Prefer higher-level synchronization primitives if they better express the problem.

______________________________________________________________________

# Lock Timeout

Instead of waiting forever,

```python
lock.acquire(timeout=2)
```

Returns

```python
True
```

or

```python
False
```

Useful when deadlocks must be detected or avoided.

______________________________________________________________________

# Production Example

Imagine inventory management.

Two customers purchase the last item simultaneously.

Without synchronization

```
Stock = 1

↓

Customer A buys

↓

Customer B buys

↓

Stock = -1
```

With a lock

```
Customer A

↓

Acquire Lock

↓

Update Stock

↓

Release

↓

Customer B
```

The second purchase correctly observes the updated stock.

> **Note:** In distributed systems, this problem is often solved using database transactions or distributed locks rather than Python thread locks. However, understanding thread synchronization is the foundation for those more advanced concepts.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Assuming the GIL prevents race conditions.

It does not.

The GIL only ensures one thread executes Python bytecode at a time.

Multiple bytecode operations can still interleave.

______________________________________________________________________

## Mistake 2

Forgetting to release a lock.

Always prefer

```python
with lock:
```

instead of manually calling `acquire()` and `release()`.

______________________________________________________________________

## Mistake 3

Holding locks during slow operations.

Examples:

- Network requests
- Database queries
- File downloads

This blocks every other waiting thread.

______________________________________________________________________

## Mistake 4

Using many nested locks without a consistent acquisition order.

This is one of the most common causes of deadlocks.

______________________________________________________________________

# Best Practices

✅ Keep critical sections as short as possible.

✅ Use `with lock:` whenever possible.

✅ Use `Lock` by default.

✅ Use `RLock` only when reentrancy is required.

✅ Document lock ownership rules.

❌ Don't assume the GIL replaces synchronization.

❌ Don't hold locks during blocking I/O.

❌ Don't ignore deadlock risks.

______________________________________________________________________

# Production Insight

Thread synchronization appears throughout backend systems.

Examples include:

- In-memory caches
- Connection pools
- Metrics collectors
- Shared configuration
- Rate limiters
- Background schedulers

However, large distributed systems often move synchronization into external systems:

- PostgreSQL transactions
- Redis distributed locks
- ZooKeeper
- etcd

The same principles still apply:

Only one actor should modify shared state at a time.

______________________________________________________________________

# Questions

### Question

> What is a race condition?

### Answer

A race condition occurs when multiple threads access shared mutable data and the program's correctness depends on the
unpredictable order of execution.

______________________________________________________________________

### Question

> What is a critical section?

### Answer

A critical section is a portion of code that accesses shared mutable state and must not be executed concurrently by
multiple threads.

______________________________________________________________________

### Question

> Why should `with lock:` be preferred?

### Answer

Because it guarantees that the lock is released even if an exception occurs, reducing the risk of deadlocks caused by
forgotten `release()` calls.

______________________________________________________________________

### Question

> What is the difference between `Lock` and `RLock`?

### Answer

`Lock` can only be acquired once by a thread before being released. `RLock` allows the owning thread to acquire the same
lock multiple times, tracking the acquisition count internally.

______________________________________________________________________

### Question

> Does the GIL eliminate race conditions?

### Answer

No. Multiple bytecode operations can still interleave, so shared mutable data must still be synchronized using locks or
other mechanisms.

______________________________________________________________________

# Practical Lesson

Create:

```text
thread_lock_demo.py
```

```python
import threading

counter = 0
lock = threading.Lock()


def increment():
    global counter

    for _ in range(100_000):
        with lock:
            counter += 1


threads = [
    threading.Thread(target=increment),
    threading.Thread(target=increment),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter: {counter}")
```

Expected Output

```text
Final counter: 200000
```

Now remove:

```python
with lock:
```

Run the program several times.

Observe how the final value changes unpredictably.

______________________________________________________________________

# Questions

## Question 1

What problem does a lock solve?

### Answer

It prevents multiple threads from entering a critical section simultaneously, avoiding race conditions.

______________________________________________________________________

## Question 2

Why doesn't the GIL eliminate the need for locks?

### Answer

Because many operations consist of multiple bytecode instructions that can still interleave between threads.

______________________________________________________________________

## Question 3

When should you use an `RLock`?

### Answer

When the same thread may need to acquire the same lock multiple times, such as during recursive or nested function
calls.

______________________________________________________________________

## Question 4

What is a deadlock?

### Answer

A situation where two or more threads wait indefinitely for resources held by each other, preventing all progress.

______________________________________________________________________

## Question 5

How can deadlocks be reduced?

### Answer

Acquire locks in a consistent order, keep critical sections short, avoid unnecessary nested locks, and use timeouts or
higher-level synchronization primitives where appropriate.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a thread-safe bank account.

Support:

- Deposit
- Withdraw
- Balance inquiry

Use `threading.Lock`.

Verify that concurrent transactions always produce the correct balance.

______________________________________________________________________

## Exercise 2

Create two versions of a shared counter:

- Without synchronization
- Using `threading.Lock`

Measure the results over multiple runs and explain the differences.

______________________________________________________________________

## Exercise 3

Create a program that intentionally deadlocks using two locks.

Then fix it by acquiring the locks in a consistent order.

Document what changed.

______________________________________________________________________

## Exercise 4

Implement a recursive object that requires nested locking.

Demonstrate why `Lock` fails and `RLock` succeeds.

Explain the internal acquisition count maintained by `RLock`.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why race conditions occur.
- ✅ What critical sections are.
- ✅ How mutual exclusion works.
- ✅ How to use `threading.Lock`.
- ✅ Why `with lock:` is preferred.
- ✅ How `threading.RLock` differs from `Lock`.
- ✅ How deadlocks occur.
- ✅ Strategies for preventing deadlocks.
- ✅ Production synchronization practices.

______________________________________________________________________

# Next Lesson

**File:** [ß45-concurrency-part-5-thread-communication](45-concurrency-part-5-thread-communication.md)

In the next lesson, you'll learn how threads communicate safely without relying on shared global variables. We'll cover
`Queue`, `Event`, `Condition`, `Semaphore`, producer-consumer patterns, coordination techniques, and production-ready
thread communication patterns.
