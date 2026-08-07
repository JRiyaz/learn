# Multithreading & Concurrency

Concurrency is one of the most important topics for backend engineers.

Modern backend systems handle:

- Thousands of concurrent users
- Multiple API requests
- Database operations
- File processing
- Background jobs
- Message queues
- Scheduled tasks

Without concurrency, a server would process one request at a time.

This chapter covers the concepts every backend engineer should know for interviews and production systems.

______________________________________________________________________

# Process vs Thread

One of the most frequently asked interview questions.

## Process

A process is an independent running program.

Examples

- Chrome
- IntelliJ IDEA
- VS Code
- Spotify

Each process has:

- Its own memory
- Own heap
- Own resources

Processes are isolated.

______________________________________________________________________

## Thread

A thread is a lightweight unit of execution inside a process.

A single process can have multiple threads.

Example

```
Chrome Process

├── UI Thread
├── Network Thread
├── Rendering Thread
├── Audio Thread
└── JavaScript Thread
```

Threads share the same memory.

______________________________________________________________________

# Why Multithreading?

Suppose a backend server receives

```
1000 HTTP Requests
```

Without threads

```
Request 1

↓

Request 2

↓

Request 3

↓

...
```

Very slow.

With threads

```
Thread 1 → Request 1

Thread 2 → Request 2

Thread 3 → Request 3
```

Multiple requests execute simultaneously.

______________________________________________________________________

# Creating a Thread

There are two traditional approaches.

## Extending Thread

```java
class MyThread extends Thread {

    @Override
    public void run() {

        System.out.println("Running...");

    }

}
```

Usage

```java
MyThread thread = new MyThread();

thread.start();
```

______________________________________________________________________

## Implementing Runnable ⭐ Preferred

```java
class MyTask implements Runnable {

    @Override
    public void run() {

        System.out.println("Running...");

    }

}
```

Usage

```java
Thread thread = new Thread(new MyTask());

thread.start();
```

______________________________________________________________________

# Why Runnable is Preferred?

Because Java supports only single inheritance.

If you extend Thread,

you cannot extend another class.

Using Runnable keeps your class hierarchy flexible.

______________________________________________________________________

# start() vs run()

Very common interview question.

Wrong

```java
thread.run();
```

Correct

```java
thread.start();
```

Difference

`run()`

Runs like a normal method.

Single thread.

`start()`

Creates a new thread.

Calls `run()` internally.

______________________________________________________________________

# Thread Lifecycle

```
New

↓

Runnable

↓

Running

↓

Blocked / Waiting

↓

Terminated
```

Understanding these states helps when debugging concurrency issues.

______________________________________________________________________

# Thread Methods

Start

```java
thread.start();
```

Sleep

```java
Thread.sleep(1000);
```

Join

```java
thread.join();
```

Interrupt

```java
thread.interrupt();
```

Current Thread

```java
Thread.currentThread();
```

______________________________________________________________________

# Sleeping

```java
Thread.sleep(2000);
```

Pauses the current thread for approximately two seconds.

Throws

```
InterruptedException
```

______________________________________________________________________

# join()

Wait for another thread to finish.

```java
Thread thread =
    new Thread(task);

thread.start();

thread.join();
```

The main thread waits until `thread` completes.

______________________________________________________________________

# Race Condition

One of the most important interview topics.

Suppose

```java
count++;
```

looks simple.

Actually

```
Read

↓

Increment

↓

Write
```

If two threads execute simultaneously,

results become unpredictable.

Example

Expected

```
2000
```

Actual

```
1738
```

This is a **Race Condition**.

______________________________________________________________________

# Synchronization

Java provides

```java
synchronized
```

to allow only one thread into a critical section.

Example

```java
class Counter {

    private int count = 0;

    public synchronized void increment() {

        count++;

    }

}
```

Now only one thread can execute `increment()` at a time.

______________________________________________________________________

# Synchronized Block

Instead of synchronizing the entire method,

you can synchronize only the critical section.

```java
public void increment() {

    synchronized(this){

        count++;

    }

}
```

Usually more efficient.

______________________________________________________________________

# Object Lock

Every Java object has an intrinsic monitor (lock).

When entering a synchronized block,

a thread acquires that object's lock.

Other threads wait until the lock is released.

______________________________________________________________________

# Static Synchronization

```java
public static synchronized void print(){

}
```

Locks the

```
Class

```

instead of an object.

______________________________________________________________________

# volatile

Another popular interview topic.

```java
private volatile boolean running = true;
```

`volatile` ensures changes made by one thread become immediately visible to other threads.

It **does not** make operations atomic.

Example

Safe

```java
volatile boolean running;
```

Unsafe

```java
volatile int count;

count++;
```

`count++` is still not atomic.

______________________________________________________________________

# Atomic Classes

Instead of

```java
int count;
```

Use

```java
AtomicInteger count =
    new AtomicInteger();
```

Increment

```java
count.incrementAndGet();
```

Thread-safe without synchronization.

Common atomic classes

- AtomicInteger
- AtomicLong
- AtomicBoolean
- AtomicReference

______________________________________________________________________

# Lock Interface

Sometimes `synchronized` isn't flexible enough.

Java provides

```java
ReentrantLock
```

Example

```java
Lock lock = new ReentrantLock();

lock.lock();

try {

    // critical section

} finally {

    lock.unlock();

}
```

Always unlock inside `finally`.

______________________________________________________________________

# synchronized vs ReentrantLock

| synchronized | ReentrantLock |
|--------------|---------------|
| Simpler | More flexible |
| Automatic release | Manual unlock |
| Less control | Try lock, timeout, fairness |

Use `synchronized` unless advanced features are required.

______________________________________________________________________

# Deadlock

A deadlock occurs when two or more threads wait forever for each other.

Example

Thread 1

```
Lock A

↓

Waiting for Lock B
```

Thread 2

```
Lock B

↓

Waiting for Lock A
```

Neither thread proceeds.

Application hangs.

______________________________________________________________________

# Avoiding Deadlocks

- Acquire locks in a consistent order.
- Minimize lock scope.
- Avoid nested locks.
- Use `tryLock()` when appropriate.

______________________________________________________________________

# ExecutorService ⭐⭐⭐⭐⭐

One of the most important modern concurrency APIs.

Instead of creating threads manually,

use a thread pool.

```java
ExecutorService executor =
    Executors.newFixedThreadPool(4);
```

Submit work

```java
executor.submit(() ->
    System.out.println("Running"));
```

Shutdown

```java
executor.shutdown();
```

Thread pools improve performance by reusing threads instead of creating new ones for every task.

______________________________________________________________________

# Types of Thread Pools

Fixed

```java
Executors.newFixedThreadPool(5)
```

Cached

```java
Executors.newCachedThreadPool()
```

Single Thread

```java
Executors.newSingleThreadExecutor()
```

Scheduled

```java
Executors.newScheduledThreadPool(2)
```

______________________________________________________________________

# Callable

Unlike Runnable,

Callable returns a result.

Runnable

```java
void run()
```

Callable

```java
V call()
```

Example

```java
Callable<Integer> task =
    () -> 100;
```

______________________________________________________________________

# Future

Represents the result of an asynchronous computation.

```java
ExecutorService executor =
    Executors.newSingleThreadExecutor();

Future<Integer> future =
    executor.submit(() -> 100);

System.out.println(future.get());
```

Output

```
100
```

`get()` blocks until the result is available.

______________________________________________________________________

# CompletableFuture ⭐⭐⭐⭐⭐

One of the most important modern Java APIs.

Traditional

```
Future

↓

Wait
```

CompletableFuture

```
Future

↓

Chain

↓

Combine

↓

Transform

↓

Async
```

Example

```java
CompletableFuture<String> future =
    CompletableFuture.supplyAsync(
        () -> "Hello"
    );

System.out.println(future.join());
```

Output

```
Hello
```

______________________________________________________________________

# Chaining

```java
CompletableFuture.supplyAsync(
    () -> "Java"
)
.thenApply(String::toUpperCase)
.thenAccept(System.out::println);
```

Output

```
JAVA
```

______________________________________________________________________

# Combining Futures

```java
CompletableFuture<String> first =
    CompletableFuture.supplyAsync(() -> "Hello");

CompletableFuture<String> second =
    CompletableFuture.supplyAsync(() -> "World");

first.thenCombine(
    second,
    (a, b) -> a + " " + b
).thenAccept(System.out::println);
```

Output

```
Hello World
```

______________________________________________________________________

# Thread-Safe Collections

Instead of

```java
HashMap
```

Use

```java
ConcurrentHashMap
```

Instead of

```java
ArrayList
```

Consider

```java
CopyOnWriteArrayList
```

These collections are designed for concurrent access.

______________________________________________________________________

# Common Concurrency Problems

- Race Condition
- Deadlock
- Starvation
- Livelock
- Thread Leakage

Interviewers often ask you to explain these conceptually.

______________________________________________________________________

# Common Mistakes

## Creating Too Many Threads

Wrong

```java
for(int i = 0; i < 10000; i++){

    new Thread(task).start();

}
```

Use a thread pool.

______________________________________________________________________

## Forgetting shutdown()

Always shut down an `ExecutorService`.

```java
executor.shutdown();
```

______________________________________________________________________

## Synchronizing Everything

Too much synchronization reduces performance.

Synchronize only critical sections.

______________________________________________________________________

## Ignoring InterruptedException

Never swallow it.

Handle it appropriately or restore the interrupt status.

______________________________________________________________________

# Best Practices

✅ Prefer `Runnable` over extending `Thread`.

✅ Use `ExecutorService` instead of manually creating threads.

✅ Prefer `CompletableFuture` for asynchronous workflows.

✅ Use `AtomicInteger` instead of synchronized counters when appropriate.

✅ Minimize synchronized blocks.

✅ Always release locks in `finally`.

✅ Use concurrent collections when sharing data.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between a Process and a Thread?

### Answer

A process is an independent program with its own memory and resources. Threads are lightweight units of execution within
a process. Threads share the same heap and resources, making communication faster but requiring synchronization to avoid
race conditions.

______________________________________________________________________

## Question

What is the difference between `start()` and `run()`?

### Answer

Calling `run()` executes the method like a normal function on the current thread.

Calling `start()` creates a new thread, after which the JVM invokes the `run()` method on that new thread.

______________________________________________________________________

## Question

What is a Race Condition?

### Answer

A race condition occurs when multiple threads access and modify shared data concurrently without proper synchronization,
causing unpredictable or incorrect results.

______________________________________________________________________

## Question

What is the difference between `synchronized` and `volatile`?

### Answer

`synchronized` provides mutual exclusion, ensuring that only one thread can execute a critical section at a time while
also providing memory visibility.

`volatile` guarantees visibility of changes across threads but does not provide atomicity or mutual exclusion. It is
suitable for simple state flags but not compound operations like `count++`.

______________________________________________________________________

## Question

Why is `ExecutorService` preferred over manually creating threads?

### Answer

`ExecutorService` manages a pool of reusable threads, reducing the overhead of thread creation and destruction. It
provides better scalability, resource management, and task scheduling compared to creating new threads for every task.

______________________________________________________________________

## Question

What are the advantages of `CompletableFuture`?

### Answer

`CompletableFuture` supports asynchronous programming with non-blocking task composition. It allows developers to chain,
combine, transform, and handle asynchronous computations in a readable and efficient manner without manually managing
threads.

______________________________________________________________________

# Practice Questions

1. What is the difference between a process and a thread?
1. Why is implementing `Runnable` preferred over extending `Thread`?
1. What is the difference between `start()` and `run()`?
1. What is a race condition?
1. What is synchronization?
1. What is the purpose of the `volatile` keyword?
1. What are atomic classes?
1. What is a deadlock, and how can it be avoided?
1. Why should `ExecutorService` be preferred over manual thread creation?
1. What is `CompletableFuture`, and when would you use it?

______________________________________________________________________

# Summary

Concurrency enables Java applications to efficiently handle multiple tasks at the same time, making it a cornerstone of
modern backend development.

In this chapter, you learned:

- Processes vs Threads
- Thread lifecycle
- Creating threads
- `Runnable` vs `Thread`
- Synchronization
- Race conditions
- `volatile`
- Atomic classes
- Locks
- Deadlocks
- `ExecutorService`
- `Callable`
- `Future`
- `CompletableFuture`
- Thread-safe collections
- Concurrency best practices

Understanding these concepts is essential for building scalable backend services and for succeeding in Java backend
interviews.

______________________________________________________________________

# Next

[JVM Memory & Garbage Collection](13-jvm-memory-garbage-collection.md)
