# File: python/45-concurrency-part-5-thread-communication.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 5: Thread Communication - Queue, Event, Condition & Semaphore

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 45
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 7–8 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `queue.Queue` | Python 2.2 |
| `threading.Event` | Python 2.3 |
| `threading.Condition` | Python 2.3 |
| `threading.Semaphore` | Python 2.3 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why threads need communication mechanisms
- Problems with shared global variables
- Producer-consumer architecture
- `queue.Queue`
- `threading.Event`
- `threading.Condition`
- `threading.Semaphore`
- Choosing the right synchronization primitive
- Production backend examples
- Best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned how to protect shared data using locks.

Locks answer one question:

> **How do we prevent multiple threads from modifying shared data simultaneously?**

Now we need to answer another question:

> **How do threads communicate with each other safely?**

______________________________________________________________________

# Why Communication Matters

Imagine an e-commerce application.

```
Download Orders

↓

Validate Orders

↓

Generate Invoice

↓

Send Email
```

Should every thread continuously check whether work is available?

No.

That wastes CPU time.

Instead, threads should communicate efficiently.

______________________________________________________________________

# Problems with Shared Variables

A beginner might write:

```python
tasks = []
```

Producer thread:

```python
tasks.append(job)
```

Consumer thread:

```python
while True:
    if tasks:
        process(tasks.pop(0))
```

Problems:

- Busy waiting
- Race conditions
- Manual synchronization
- Poor scalability

Python provides better tools.

______________________________________________________________________

# Producer-Consumer Pattern

This is one of the most common concurrent programming patterns.

```
Producer

↓

Queue

↓

Consumer
```

The producer creates work.

The consumer processes work.

Neither thread needs to know how fast the other runs.

______________________________________________________________________

# Introducing `queue.Queue`

`Queue` is a thread-safe FIFO data structure.

```
First In

↓

First Out
```

It handles synchronization internally.

No manual locking required.

______________________________________________________________________

# Creating a Queue

```python
from queue import Queue

queue = Queue()
```

Initially:

```
Empty
```

______________________________________________________________________

# Putting Data

```python
queue.put("Order #101")
queue.put("Order #102")
```

Queue

```
Front

↓

101

↓

102

↓

Back
```

______________________________________________________________________

# Getting Data

```python
job = queue.get()
```

Returns:

```
Order #101
```

The first inserted item.

______________________________________________________________________

# Blocking Behaviour

Suppose the queue is empty.

```python
queue.get()
```

What happens?

It waits.

No busy loop.

No CPU waste.

As soon as another thread calls:

```python
queue.put(...)
```

The waiting thread wakes automatically.

______________________________________________________________________

# Example

```python
from queue import Queue
import threading
import time

queue = Queue()

def producer():

    for i in range(5):

        queue.put(i)

        print(f"Produced {i}")

        time.sleep(1)

def consumer():

    while True:

        item = queue.get()

        print(f"Consumed {item}")

        queue.task_done()

producer_thread = threading.Thread(target=producer)

consumer_thread = threading.Thread(
    target=consumer,
    daemon=True
)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
queue.join()
```

______________________________________________________________________

# Why `task_done()`?

Every

```python
queue.get()
```

must eventually call

```python
queue.task_done()
```

This informs the queue that processing has completed.

Without it,

```python
queue.join()
```

waits forever.

______________________________________________________________________

# Queue Lifecycle

```
Producer

↓

put()

↓

Queue

↓

get()

↓

Consumer

↓

task_done()
```

______________________________________________________________________

# `threading.Event`

Sometimes threads don't exchange data.

Instead,

they wait for a signal.

Example:

```
Database Ready

↓

Start Workers
```

This is exactly what `Event` is for.

______________________________________________________________________

# Creating an Event

```python
event = threading.Event()
```

Initially

```
Not Set
```

______________________________________________________________________

# Waiting

```python
event.wait()
```

Thread pauses until another thread signals it.

______________________________________________________________________

# Sending the Signal

```python
event.set()
```

Every waiting thread continues.

______________________________________________________________________

# Example

```python
import threading
import time

event = threading.Event()

def worker():

    print("Waiting...")

    event.wait()

    print("Started!")

thread = threading.Thread(target=worker)

thread.start()

time.sleep(2)

event.set()
```

Output

```
Waiting...

Started!
```

______________________________________________________________________

# Event Lifecycle

```
Not Set

↓

Threads Wait

↓

set()

↓

All Waiting Threads Continue
```

______________________________________________________________________

# `Condition`

Suppose workers should continue

only when

```
Queue Size >= 10
```

A simple lock cannot express this.

A condition variable can.

______________________________________________________________________

# Creating a Condition

```python
condition = threading.Condition()
```

A condition combines:

- Lock
- Waiting queue
- Notification mechanism

______________________________________________________________________

# Waiting

```python
with condition:

    condition.wait()
```

______________________________________________________________________

# Notification

```python
with condition:

    condition.notify()
```

or

```python
condition.notify_all()
```

______________________________________________________________________

# Example Use Cases

- Database connection pools
- Job schedulers
- Cache refresh
- Resource availability

______________________________________________________________________

# `Semaphore`

Imagine:

Database pool

```
Maximum Connections = 10
```

Should thread number eleven connect?

No.

It should wait.

______________________________________________________________________

# Creating a Semaphore

```python
semaphore = threading.Semaphore(3)
```

Only

```
3 Threads
```

may enter simultaneously.

______________________________________________________________________

# Example

```python
with semaphore:

    query_database()
```

When three threads are already inside,

the fourth waits.

______________________________________________________________________

# Lock vs Semaphore

| Feature | Lock | Semaphore |
|----------|------|-----------|
| Maximum holders | 1 | Many |
| Use case | Critical section | Limited resources |

______________________________________________________________________

# Which Primitive Should You Use?

| Situation | Primitive |
|------------|-----------|
| Shared data | Lock |
| Work queue | Queue |
| Startup signal | Event |
| Resource pool | Semaphore |
| Wait for state | Condition |

______________________________________________________________________

# Production Example

Suppose your API receives uploaded images.

```
API

↓

Queue

↓

Worker Threads

↓

Resize Image

↓

Upload S3
```

The API responds immediately.

Workers continue processing in the background.

This pattern appears in:

- Celery workers
- RabbitMQ consumers
- Kafka consumers
- Background processing systems

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using lists instead of `Queue`.

`Queue` is already thread-safe.

______________________________________________________________________

## Mistake 2

Busy waiting.

Wrong

```python
while not ready:
    pass
```

Use `Event` or `Condition`.

______________________________________________________________________

## Mistake 3

Forgetting `task_done()`.

This causes `queue.join()` to block forever.

______________________________________________________________________

## Mistake 4

Using a semaphore where a lock is sufficient.

Choose the simplest synchronization primitive that solves the problem.

______________________________________________________________________

# Best Practices

✅ Prefer `Queue` for producer-consumer workflows.

✅ Use `Event` for signalling.

✅ Use `Semaphore` to limit concurrent access to finite resources.

✅ Use `Condition` when waiting for specific state changes.

❌ Avoid busy waiting.

❌ Avoid manually implementing thread-safe queues.

______________________________________________________________________

# Production Insight

Many backend systems use these primitives indirectly.

Examples:

- Web servers dispatch requests through internal queues.
- Database connection pools often use semaphores.
- Background workers consume jobs from queues.
- Service startup routines coordinate using events.

Even if you later adopt Celery, Kafka, or asyncio, these underlying concepts remain the same.

______________________________________________________________________

# Questions

### Question

> Why is `Queue` preferred over a shared list?

### Answer

Because `Queue` is thread-safe, blocks efficiently when empty, and eliminates the need for manual synchronization.

______________________________________________________________________

### Question

> When should `Event` be used?

### Answer

When one or more threads need to wait until another thread signals that a condition has occurred.

______________________________________________________________________

### Question

> What problem does a semaphore solve?

### Answer

It limits the number of threads that can access a finite resource simultaneously.

______________________________________________________________________

### Question

> Why use a `Condition` instead of a lock?

### Answer

A condition allows threads to wait until a particular state becomes true, whereas a lock only provides mutual exclusion.

______________________________________________________________________

### Question

> What is the producer-consumer pattern?

### Answer

A design pattern where producer threads generate work and consumer threads process it asynchronously using a shared
queue.

______________________________________________________________________

# Practical Lesson

Create:

```text
producer_consumer.py
```

```python
from queue import Queue
import threading
import time

queue = Queue()


def producer():

    for i in range(10):

        print(f"Produced {i}")

        queue.put(i)

        time.sleep(0.5)


def consumer():

    while True:

        item = queue.get()

        print(f"Consumed {item}")

        time.sleep(1)

        queue.task_done()


consumer_thread = threading.Thread(
    target=consumer,
    daemon=True
)

consumer_thread.start()

producer()

queue.join()

print("All jobs processed.")
```

Observe how the producer and consumer run independently while the queue coordinates communication.

______________________________________________________________________

# Questions

## Question 1

Why should `Queue` be preferred over a list for thread communication?

### Answer

Because `Queue` provides built-in thread safety and blocking operations.

______________________________________________________________________

## Question 2

What is the purpose of `task_done()`?

### Answer

It informs the queue that a retrieved task has finished processing.

______________________________________________________________________

## Question 3

When should `Event` be used?

### Answer

When one thread needs to signal one or more waiting threads.

______________________________________________________________________

## Question 4

When is a semaphore useful?

### Answer

When limiting concurrent access to a finite number of resources such as database connections.

______________________________________________________________________

## Question 5

What is the difference between `Condition` and `Event`?

### Answer

An `Event` represents a simple on/off signal, whereas a `Condition` allows threads to wait for and be notified about
specific state changes while coordinating with a lock.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a producer-consumer system with:

- Two producer threads
- Three consumer threads
- One shared queue

Record how work is distributed.

______________________________________________________________________

## Exercise 2

Simulate a database connection pool using a semaphore with a maximum of three concurrent connections.

______________________________________________________________________

## Exercise 3

Create an `Event` that delays worker threads until application configuration has finished loading.

______________________________________________________________________

## Exercise 4

Implement a bounded queue where producers wait when the queue is full and consumers notify producers when space becomes
available.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why threads need communication mechanisms.
- ✅ The producer-consumer pattern.
- ✅ How `Queue` works.
- ✅ How to use `Event`.
- ✅ How to use `Condition`.
- ✅ How to use `Semaphore`.
- ✅ Production communication patterns.
- ✅ Common interview topics.

______________________________________________________________________

# Next Lesson

**File:** [46-concurrency-part-6-threadpoolexecutor](46-concurrency-part-6-threadpoolexecutor.md)

In the next lesson, you'll learn about thread pools and the `concurrent.futures.ThreadPoolExecutor`. We'll cover task
submission, futures, result handling, exception propagation, cancellation, performance considerations, and why thread
pools are preferred over manually creating large numbers of threads in production systems.
