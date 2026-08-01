# File: python/48-concurrency-part-8-process-communication.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 8: Inter-Process Communication (IPC) - Pipes, Queues, Managers & Shared Memory

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 48
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 8–9 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `multiprocessing.Queue` | Python 2.6 |
| `multiprocessing.Pipe` | Python 2.6 |
| `multiprocessing.Manager` | Python 2.6 |
| `multiprocessing.Value` | Python 2.6 |
| `multiprocessing.Array` | Python 2.6 |
| `multiprocessing.shared_memory` | Python 3.8 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why processes need IPC
- What IPC is
- Process communication methods
- Pipes
- Queues
- Managers
- Shared Memory
- Serialization (Pickling)
- IPC performance considerations
- Production backend examples
- Best practices
- questions

______________________________________________________________________

# Recap

In the previous lesson, we learned:

- Processes
- Parent and child processes
- Process isolation
- True parallelism

One important property of processes is:

```
Memory is NOT shared.
```

This creates a new challenge.

If processes cannot directly access each other's variables,

how do they communicate?

The answer is:

```
Inter-Process Communication (IPC)
```

______________________________________________________________________

# What is IPC?

IPC stands for:

```
Inter-Process Communication
```

It refers to techniques that allow separate processes to exchange:

- Data
- Messages
- Signals
- Shared state

without directly sharing their memory.

______________________________________________________________________

# Why is IPC Needed?

Imagine two processes.

```
Process A

↓

Downloads Image
```

```
Process B

↓

Resizes Image
```

How does Process B receive the downloaded image?

It cannot access:

```python
image_data
```

inside Process A.

The data must be communicated explicitly.

______________________________________________________________________

# IPC Overview

Python provides several IPC mechanisms.

| Mechanism | Best For |
|------------|----------|
| Queue | Producer-Consumer |
| Pipe | Two-way communication |
| Manager | Shared Python objects |
| Shared Memory | Large data |
| Value / Array | Small shared primitives |

Each has different trade-offs.

______________________________________________________________________

# Serialization

Before discussing IPC,

we must understand one important concept.

Suppose a process sends:

```python
user = {
    "id": 1,
    "name": "Alice"
}
```

The receiving process cannot access the object directly.

Instead,

Python converts it into bytes.

This process is called:

```
Serialization
```

In Python,

serialization is usually performed using:

```
Pickle
```

______________________________________________________________________

# Pickling

```
Python Object

↓

Pickle

↓

Bytes

↓

Transfer

↓

Unpickle

↓

Python Object
```

This happens automatically for most multiprocessing communication.

______________________________________________________________________

# Why Serialization Matters

Serialization is not free.

Complex objects require:

- CPU time
- Memory allocation
- Data copying

Large objects may become expensive to transfer.

______________________________________________________________________

# Introducing `multiprocessing.Queue`

This is the most commonly used IPC mechanism.

```python
from multiprocessing import Queue

queue = Queue()
```

Unlike `queue.Queue`,

this queue communicates across

different processes.

______________________________________________________________________

# Example

```python
from multiprocessing import Process, Queue


def producer(queue):

    queue.put("Hello")


def consumer(queue):

    print(queue.get())


queue = Queue()

p1 = Process(
    target=producer,
    args=(queue,)
)

p2 = Process(
    target=consumer,
    args=(queue,)
)

p1.start()
p2.start()

p1.join()
p2.join()
```

Output

```text
Hello
```

______________________________________________________________________

# Queue Workflow

```
Producer Process

↓

put()

↓

Queue

↓

get()

↓

Consumer Process
```

Python handles:

- Synchronization
- Serialization
- Process safety

______________________________________________________________________

# Queue Advantages

- Easy to use
- Thread-safe
- Process-safe
- Multiple producers
- Multiple consumers

______________________________________________________________________

# Queue Disadvantages

Every object is:

```
Serialized

↓

Copied

↓

Deserialized
```

Large objects increase overhead.

______________________________________________________________________

# Introducing `Pipe`

A Pipe connects exactly two processes.

```
Process A

↔

Process B
```

______________________________________________________________________

# Creating a Pipe

```python
from multiprocessing import Pipe

parent_conn, child_conn = Pipe()
```

Both ends can:

- Send
- Receive

______________________________________________________________________

# Example

```python
from multiprocessing import Process
from multiprocessing import Pipe


def worker(connection):

    connection.send("Hello")

    connection.close()


parent, child = Pipe()

process = Process(
    target=worker,
    args=(child,)
)

process.start()

print(parent.recv())

process.join()
```

Output

```text
Hello
```

______________________________________________________________________

# Pipe Workflow

```
Parent

↓

send()

↓

Pipe

↓

recv()

↓

Child
```

Unlike a Queue,

a Pipe is designed primarily for communication between two endpoints.

______________________________________________________________________

# Queue vs Pipe

| Feature | Queue | Pipe |
|----------|--------|------|
| Multiple Producers | ✅ | ❌ |
| Multiple Consumers | ✅ | ❌ |
| Simplicity | High | Medium |
| Typical Use | Work queues | Direct communication |

______________________________________________________________________

# Introducing `Manager`

Suppose multiple processes need access to:

```python
shared_users
```

A normal list won't work.

Instead,

Python provides a Manager.

______________________________________________________________________

# Creating a Manager List

```python
from multiprocessing import Manager

manager = Manager()

users = manager.list()
```

Now,

multiple processes may safely modify

the same logical list.

______________________________________________________________________

# Example

```python
from multiprocessing import Process
from multiprocessing import Manager


def worker(users):

    users.append("Alice")


manager = Manager()

users = manager.list()

process = Process(
    target=worker,
    args=(users,)
)

process.start()
process.join()

print(users)
```

Output

```text
['Alice']
```

______________________________________________________________________

# How Manager Works

Internally,

a Manager creates

a dedicated server process.

```
Worker A

↓

Manager Server

↑

Worker B
```

All operations go through this server.

______________________________________________________________________

# Manager Advantages

- Familiar Python objects
- Shared dictionaries
- Shared lists
- Shared sets
- Easy API

______________________________________________________________________

# Manager Disadvantages

Every operation:

- Crosses process boundaries
- Requires serialization
- Communicates with the manager process

Managers are convenient,

but not the fastest solution.

______________________________________________________________________

# Shared Memory

Suppose you process

a 500 MB NumPy array.

Serializing that array repeatedly would be expensive.

Instead,

processes can share memory directly.

Python 3.8 introduced:

```python
multiprocessing.shared_memory
```

______________________________________________________________________

# Concept

```
Shared Memory Region

↓

Process A

↓

Process B

↓

Process C
```

One copy of the data.

No repeated serialization.

______________________________________________________________________

# Value

For simple shared variables,

Python provides:

```python
from multiprocessing import Value
```

Example

```python
counter = Value("i", 0)
```

Here

```
i

↓

Signed Integer
```

______________________________________________________________________

# Example

```python
from multiprocessing import Process
from multiprocessing import Value


def worker(counter):

    with counter.get_lock():

        counter.value += 1


counter = Value("i", 0)

process = Process(
    target=worker,
    args=(counter,)
)

process.start()
process.join()

print(counter.value)
```

Output

```text
1
```

Notice

`Value` includes an associated lock by default.

______________________________________________________________________

# Array

Need shared arrays?

Use

```python
from multiprocessing import Array
```

Example

```python
numbers = Array(
    "i",
    [1, 2, 3]
)
```

All processes can access the same memory.

______________________________________________________________________

# Choosing an IPC Mechanism

| Situation | Recommended |
|------------|-------------|
| Work distribution | Queue |
| Two-process communication | Pipe |
| Shared list/dict | Manager |
| Shared integer | Value |
| Shared array | Array |
| Large binary data | Shared Memory |

______________________________________________________________________

# Production Example

Imagine an image processing service.

```
API

↓

Queue

↓

Worker Process

↓

Resize

↓

Compress

↓

Store
```

The queue distributes work.

Large image buffers may be stored in shared memory to avoid repeated copying.

______________________________________________________________________

# Serialization Cost

Consider sending:

```
10 KB JSON
```

Fast.

Now imagine:

```
2 GB Video
```

Serialization becomes expensive.

Choosing the right IPC mechanism can significantly improve performance.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Assuming global variables are shared.

Each process has its own memory.

______________________________________________________________________

## Mistake 2

Using `Manager` for high-performance workloads.

Managers are convenient but slower than shared memory.

______________________________________________________________________

## Mistake 3

Passing extremely large objects through queues repeatedly.

Serialization overhead can dominate execution time.

______________________________________________________________________

## Mistake 4

Ignoring synchronization when using shared memory.

Shared memory still requires coordination if multiple processes modify the same data concurrently.

______________________________________________________________________

# Best Practices

✅ Use queues for producer-consumer systems.

✅ Use pipes for simple two-process communication.

✅ Use managers for convenience.

✅ Use shared memory for large datasets.

✅ Minimise serialization of large objects.

❌ Don't assume IPC is free.

❌ Don't choose the most complex mechanism unless necessary.

______________________________________________________________________

# Production Insight

Modern distributed systems extend these same IPC concepts across machines.

Examples include:

- RabbitMQ
- Apache Kafka
- Redis Streams
- Amazon SQS
- Google Pub/Sub

Conceptually,

these systems behave like distributed queues.

Understanding local IPC makes distributed messaging systems much easier to learn.

______________________________________________________________________

# Questions

### Question

> Why can't processes directly access each other's variables?

### Answer

Because each process has its own isolated memory space managed by the operating system.

______________________________________________________________________

### Question

> What is serialization?

### Answer

Serialization converts Python objects into a transferable byte representation so they can be sent between processes or
stored.

______________________________________________________________________

### Question

> Why is `multiprocessing.Queue` commonly used?

### Answer

It provides safe, process-aware communication between multiple producers and consumers while handling synchronization
and serialization automatically.

______________________________________________________________________

### Question

> When should shared memory be preferred?

### Answer

When processes need efficient access to large datasets without repeatedly serializing and copying them.

______________________________________________________________________

### Question

> Why is a Manager slower than shared memory?

### Answer

Because every operation is routed through a manager server process and involves inter-process communication and
serialization.

______________________________________________________________________

# Practical Lesson

Create:

```text
process_queue_demo.py
```

```python
from multiprocessing import Process, Queue


def producer(queue):

    for number in range(5):

        print(f"Produced: {number}")

        queue.put(number)

    queue.put(None)


def consumer(queue):

    while True:

        item = queue.get()

        if item is None:
            break

        print(f"Consumed: {item}")


queue = Queue()

producer_process = Process(
    target=producer,
    args=(queue,)
)

consumer_process = Process(
    target=consumer,
    args=(queue,)
)

producer_process.start()
consumer_process.start()

producer_process.join()
consumer_process.join()
```

Expected Output (order may vary)

```text
Produced: 0
Produced: 1
...

Consumed: 0
Consumed: 1
...
```

______________________________________________________________________

# Questions

## Question 1

What is IPC?

### Answer

IPC (Inter-Process Communication) is a collection of mechanisms that allow separate processes to exchange data and
coordinate execution.

______________________________________________________________________

## Question 2

Why is serialization necessary in multiprocessing?

### Answer

Because processes do not share memory, objects must be converted into bytes before being transmitted between them.

______________________________________________________________________

## Question 3

When should you use a Pipe instead of a Queue?

### Answer

When communication is primarily between two processes and a simple direct channel is sufficient.

______________________________________________________________________

## Question 4

What is the advantage of shared memory?

### Answer

It allows multiple processes to access the same memory without repeatedly serializing and copying large objects.

______________________________________________________________________

## Question 5

When should a Manager be used?

### Answer

When multiple processes need to share familiar Python objects such as lists or dictionaries and convenience is more
important than maximum performance.

______________________________________________________________________

# Assignment

## Exercise 1

Implement a producer-consumer system using `multiprocessing.Queue` with:

- Two producer processes
- Three consumer processes

Measure throughput.

______________________________________________________________________

## Exercise 2

Build a simple chat application between two processes using `Pipe`.

Each process should send and receive multiple messages.

______________________________________________________________________

## Exercise 3

Create a shared counter using `Value`.

Spawn four processes that increment the counter safely.

Verify the final value.

______________________________________________________________________

## Exercise 4

Research the `multiprocessing.shared_memory` module.

Explain:

- How it differs from `Manager`
- Why it is faster for large datasets
- When it should be avoided

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why IPC is necessary.
- ✅ How serialization works.
- ✅ How `multiprocessing.Queue` works.
- ✅ How `Pipe` works.
- ✅ How `Manager` shares Python objects.
- ✅ How `Value`, `Array`, and shared memory enable efficient data sharing.
- ✅ Performance trade-offs between IPC mechanisms.
- ✅ Production IPC patterns.

______________________________________________________________________

# Next Lesson

**File:** [49-concurrency-part-9-processpoolexecutor-and-pool](49-concurrency-part-9-processpoolexecutor-and-pool.md)

In the next lesson, you'll learn how to efficiently manage multiple worker processes using `multiprocessing.Pool` and
`concurrent.futures.ProcessPoolExecutor`. We'll compare both APIs, explore task scheduling, futures, result handling,
exception propagation, performance tuning, and learn why process pools are the standard solution for CPU-bound workloads
in production.
