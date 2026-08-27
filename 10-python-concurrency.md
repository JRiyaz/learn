# 10. Python Concurrency & AsyncIO

**Previous:** [09. Advanced Python OOP](./09-python-advanced-oop.md)

**Next:** [11. Typing & Testing](./11-python-exceptions-typing-testing.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain concurrency and parallelism.
- Distinguish CPU-bound and I/O-bound workloads.
- Explain processes vs threads.
- Explain the GIL and its practical impact on Python backend applications.
- Understand thread creation and synchronization.
- Identify race conditions.
- Use locks appropriately.
- Explain deadlocks and common prevention strategies.
- Understand `ThreadPoolExecutor`.
- Understand multiprocessing and `ProcessPoolExecutor`.
- Explain AsyncIO at a practical backend level.
- Understand the event loop.
- Explain coroutines, tasks and `await`.
- Use `asyncio.gather()` for independent asynchronous work.
- Understand cancellation and timeouts.
- Identify blocking code inside async applications.
- Choose an appropriate concurrency model for a backend workload.
- Recognize common concurrency mistakes in production systems.

______________________________________________________________________

# 1. Concurrency vs Parallelism

These terms are related but not identical.

### Concurrency

Concurrency means multiple units of work can make progress during overlapping periods.

The work does not necessarily execute simultaneously.

### Parallelism

Parallelism means multiple units of work execute at the same time, usually on different CPU cores.

A system can therefore be concurrent without being parallel.

______________________________________________________________________

# 2. CPU-Bound vs I/O-Bound Work

This distinction is important when choosing a concurrency model.

## CPU-bound

The program spends most of its time performing computation.

Examples:

- Image processing
- Compression
- Large calculations
- CPU-heavy parsing
- Data transformation

## I/O-bound

The program spends significant time waiting for external resources.

Examples:

- HTTP requests
- Database queries
- File operations
- Network communication
- External APIs

Python backend applications are frequently I/O-bound.

______________________________________________________________________

# 3. Why This Distinction Matters

Suppose an endpoint performs:

```text
Request
  ↓
HTTP call
  ↓
Database call
  ↓
Another HTTP call
```

Most of the time may be spent waiting for external systems.

Concurrency can allow other work to proceed while one operation is waiting.

Compare that with:

```text
Request
  ↓
CPU-heavy calculation
  ↓
CPU-heavy calculation
```

Adding more I/O concurrency does not solve a CPU bottleneck.

The workload should determine the execution model.

______________________________________________________________________

# 4. Processes vs Threads

A thread is an execution unit within a process.

Threads within the same process normally share the process's memory.

Processes have separate memory spaces.

| Feature | Threads | Processes |
|---|---|---|
| Memory | Shared within process | Separate |
| Communication | Relatively easy through shared state | Requires IPC/serialization mechanisms |
| Creation overhead | Generally lower | Generally higher |
| CPU parallelism for traditional CPython Python bytecode | Limited by GIL | Can use multiple CPU cores |
| Typical use | I/O-bound work | CPU-bound work |

This is a practical guideline, not an absolute rule.

______________________________________________________________________

# 5. The GIL

The **Global Interpreter Lock (GIL)** is a CPython implementation mechanism that, in traditional CPython execution,
allows only one thread at a time to execute Python bytecode within a given interpreter.

This means Python threads do not generally provide CPU-bound parallel execution of Python bytecode in traditional
CPython.

However, threads remain useful for I/O-bound work because the interpreter can release the GIL while waiting for I/O, and
some native extensions can release it during expensive operations.

For interviews, avoid saying:

> Python cannot do multithreading.

That statement is incorrect.

A better statement is:

> CPython's GIL limits simultaneous execution of Python bytecode by threads, but threads are still useful for concurrency, especially for I/O-bound workloads.

______________________________________________________________________

# 6. Threading

Python provides the `threading` module.

Basic example:

```python
import threading


def worker():
    print("worker running")


thread = threading.Thread(target=worker)
thread.start()

thread.join()
```

`start()` begins the thread.

`join()` waits for it to finish.

______________________________________________________________________

# 7. Why Use `join()`?

Without waiting for a thread, the main program may continue before the worker finishes.

Example:

```python
thread.start()
thread.join()
```

means:

> Start the worker and wait for its completion.

In larger applications, however, you generally want a thread-pool abstraction rather than manually creating large
numbers of threads.

______________________________________________________________________

# 8. Shared Mutable State

Threads in the same process can access shared state.

Example:

```python
counter = 0
```

Multiple threads modifying the same state can introduce correctness problems.

The safest strategy is often:

> Minimize shared mutable state.

If shared state is required, use an appropriate synchronization mechanism.

______________________________________________________________________

# 9. Race Conditions

A race condition occurs when the result depends on the timing or interleaving of concurrent operations.

Consider:

```python
counter += 1
```

Conceptually, it involves:

```text
read
modify
write
```

Two threads can interleave these operations in a way that produces an unexpected result.

Do not rely on individual Python statements being magically safe just because they appear short.

______________________________________________________________________

# 10. Locks

Python provides locks through `threading`.

```python
import threading

lock = threading.Lock()
```

Use:

```python
with lock:
    counter += 1
```

The lock provides mutual exclusion for the protected critical section.

______________________________________________________________________

# 11. Critical Sections

A critical section is code that accesses shared state and therefore needs synchronization.

Example:

```python
with lock:
    balance -= amount
```

Keep critical sections as small as practical.

A lock held around slow network or database operations can unnecessarily reduce concurrency.

______________________________________________________________________

# 12. `Lock` vs `RLock`

`threading.Lock` is a standard mutual-exclusion lock.

`threading.RLock` is a reentrant lock.

With an `RLock`, the same thread can acquire the lock multiple times and then release it the corresponding number of
times.

Use `RLock` only when reentrancy is actually required.

______________________________________________________________________

# 13. Deadlocks

A deadlock occurs when concurrent operations wait indefinitely for resources held by one another.

Classic example:

```text
Thread A:
    Lock 1
    ↓
    waits for Lock 2

Thread B:
    Lock 2
    ↓
    waits for Lock 1
```

Neither thread can continue.

______________________________________________________________________

# 14. Preventing Deadlocks

Common strategies:

### 1. Consistent lock ordering

Always acquire multiple locks in the same order.

### 2. Minimize lock scope

Hold locks only when required.

### 3. Avoid unnecessary nested locking

Multiple locks increase complexity.

### 4. Use timeouts where appropriate

Timeouts can prevent indefinite waiting and provide an opportunity for recovery.

______________________________________________________________________

# 15. ThreadPoolExecutor

For many concurrent operations, use:

```python
from concurrent.futures import ThreadPoolExecutor
```

Example:

```python
def fetch_user(user_id):
    ...


with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_user, user_ids)
```

The executor manages a pool of worker threads.

This is usually preferable to manually creating one thread per task.

______________________________________________________________________

# 16. `submit()` and Futures

You can submit individual tasks:

```python
future = executor.submit(fetch_user, user_id)
```

A `Future` represents work that may complete in the future.

You can retrieve the result:

```python
result = future.result()
```

If the worker raised an exception, retrieving the result can surface that exception.

______________________________________________________________________

# 17. Thread Pool Sizing

More threads do not always mean more performance.

Too many threads can cause:

- Scheduling overhead
- Memory usage
- Connection pressure
- Downstream overload
- Increased contention

For I/O workloads, the appropriate pool size depends on:

- Operation latency
- Number of concurrent requests
- External service limits
- Connection pools
- CPU resources

Treat pool size as a capacity decision rather than a magic constant.

______________________________________________________________________

# 18. Multiprocessing

The `multiprocessing` module creates separate processes.

Each process has its own memory space.

This makes multiprocessing useful when actual CPU parallelism is required.

Example:

```python
from multiprocessing import Process


def worker():
    print("working")


process = Process(target=worker)
process.start()
process.join()
```

______________________________________________________________________

# 19. ProcessPoolExecutor

Python also provides:

```python
from concurrent.futures import ProcessPoolExecutor
```

Example:

```python
with ProcessPoolExecutor() as executor:
    results = executor.map(expensive_calculation, values)
```

This provides a higher-level process-pool abstraction.

It is useful for CPU-heavy independent tasks.

______________________________________________________________________

# 20. Process Communication

Processes do not normally share the same memory space.

Communication therefore requires mechanisms such as:

- Queues
- Pipes
- Shared memory
- IPC
- Serialization

Moving data between processes has overhead.

Large objects may therefore make multiprocessing less attractive if they need to be transferred frequently.

______________________________________________________________________

# 21. Threads vs Processes — Practical Decision

A useful decision table:

| Workload | Usually consider |
|---|---|
| Blocking HTTP calls | Threads |
| Blocking database client | Threads |
| High-volume non-blocking I/O | AsyncIO |
| CPU-heavy Python computation | Processes |
| CPU-heavy native extension that releases the GIL | Depends on workload |
| Simple synchronous work | Keep it synchronous |

Always validate the actual bottleneck before introducing concurrency.

______________________________________________________________________

# 22. AsyncIO

AsyncIO is Python's asynchronous I/O framework.

It uses an event loop to coordinate asynchronous tasks.

Instead of waiting synchronously for an I/O operation to finish, a coroutine can suspend and allow another task to run.

This makes AsyncIO particularly useful for high-concurrency I/O-bound applications.

______________________________________________________________________

# 23. The Event Loop

The event loop is responsible for coordinating asynchronous work.

Conceptually:

```text
Task A → waiting for network
                ↓
          event loop runs
                ↓
Task B → waiting for database
                ↓
          event loop runs
                ↓
Task A → ready to continue
```

The important idea is:

> While one task is waiting on non-blocking I/O, the event loop can run other ready tasks.

______________________________________________________________________

# 24. Coroutines

A coroutine function is defined using:

```python
async def
```

Example:

```python
async def fetch_user():
    ...
```

Calling:

```python
fetch_user()
```

produces a coroutine object.

It does not necessarily execute the body immediately in the same way as a normal function call.

The coroutine needs to be awaited or scheduled.

______________________________________________________________________

# 25. `await`

Example:

```python
async def fetch_user():
    user = await client.get("/users/1")
    return user
```

`await` allows the current coroutine to suspend while the awaited operation is incomplete.

The event loop can then run other ready work.

______________________________________________________________________

# 26. Tasks

A coroutine can be scheduled as an asyncio task:

```python
task = asyncio.create_task(fetch_user())
```

A task represents scheduled asynchronous execution.

This differs from merely creating a coroutine object.

______________________________________________________________________

# 27. Coroutine vs Task

### Coroutine

```python
coro = fetch_user()
```

This creates a coroutine object.

### Task

```python
task = asyncio.create_task(fetch_user())
```

This schedules the coroutine as a task on the event loop.

This distinction is commonly asked in interviews.

______________________________________________________________________

# 28. Sequential Async Operations

Consider:

```python
user = await fetch_user()
orders = await fetch_orders()
```

The second operation begins only after the first operation completes.

If the operations are independent, this may unnecessarily increase latency.

______________________________________________________________________

# 29. Concurrent Async Operations

You can schedule independent operations concurrently:

```python
user_task = asyncio.create_task(fetch_user())
orders_task = asyncio.create_task(fetch_orders())

user = await user_task
orders = await orders_task
```

Or use `asyncio.gather()`.

______________________________________________________________________

# 30. `asyncio.gather()`

Example:

```python
results = await asyncio.gather(
    fetch_user(),
    fetch_orders(),
    fetch_preferences(),
)
```

This is useful when operations are independent.

The total waiting time can approach the slowest operation rather than the sum of all operations, assuming the
dependencies and resources can actually support concurrent execution.

______________________________________________________________________

# 31. When Not to Parallelize

Do not blindly use:

```python
asyncio.gather(...)
```

Consider:

- Dependency relationships
- Database connection limits
- External API rate limits
- Remote service capacity
- Memory usage
- Ordering requirements
- Business semantics

Concurrency improves throughput/latency only when the system can support it.

______________________________________________________________________

# 32. Blocking Code in Async Applications

This is one of the most important backend interview topics.

Bad:

```python
async def endpoint():
    time.sleep(5)
```

`time.sleep()` blocks the event-loop thread.

Use:

```python
await asyncio.sleep(5)
```

for asynchronous sleeping.

______________________________________________________________________

# 33. Blocking Libraries

Declaring a function `async` does not automatically make everything inside it non-blocking.

For example:

```python
async def endpoint():
    response = requests.get(url)
    return response.json()
```

`requests.get()` is synchronous and blocking.

It can block the event loop.

Use an async-compatible client or move blocking work to an appropriate thread/executor.

______________________________________________________________________

# 34. CPU Work Inside AsyncIO

AsyncIO is not a replacement for CPU parallelism.

This is dangerous:

```python
async def endpoint():
    result = expensive_cpu_calculation()
    return result
```

If the calculation takes significant time, it blocks the event loop.

Move CPU-heavy work to:

- A process pool
- A background worker
- A separate service
- Another suitable execution model

______________________________________________________________________

# 35. Cancellation

Async tasks can be cancelled.

Example:

```python
task.cancel()
```

Cancellation is cooperative.

Code should generally allow cancellation to propagate unless it has a specific reason to handle it.

Cleanup should still happen correctly.

Example:

```python
async def worker():
    try:
        await do_work()
    finally:
        await cleanup()
```

______________________________________________________________________

# 36. Timeouts

External operations should not wait indefinitely.

Async code can use timeout mechanisms.

Example:

```python
await asyncio.wait_for(
    operation(),
    timeout=5,
)
```

Modern Python also provides timeout context-manager APIs.

The backend principle is:

> Bound the time spent waiting on external dependencies.

______________________________________________________________________

# 37. Async Context Managers

Asynchronous resources can support:

```python
async with resource:
    ...
```

using the asynchronous context-manager protocol:

```python
__aenter__
__aexit__
```

This is useful for:

- Async clients
- Connections
- Transactions
- Streaming resources

______________________________________________________________________

# 38. Async Iteration

Async iterators can be consumed with:

```python
async for item in source:
    ...
```

This is useful when data arrives incrementally from an asynchronous source.

______________________________________________________________________

# 39. Async Generators

An async generator can produce values incrementally:

```python
async def stream():
    for item in items:
        yield item
```

Consumers can use:

```python
async for item in stream():
    ...
```

This is useful for streaming and memory-efficient processing.

______________________________________________________________________

# 40. AsyncIO and FastAPI

FastAPI supports asynchronous endpoints:

```python
@app.get("/users")
async def get_users():
    users = await repository.get_users()
    return users
```

This works best when the underlying operations are also asynchronous/non-blocking.

An `async def` endpoint containing blocking synchronous operations can still block the event loop.

______________________________________________________________________

# 41. Connection Pools and Concurrency

Suppose an application does:

```python
await asyncio.gather(
    *[fetch_from_db(i) for i in range(1000)]
)
```

This does not mean the database will execute 1,000 queries simultaneously.

A database connection pool may allow only a limited number of connections.

Therefore:

```text
Application concurrency
        ↓
Connection pool
        ↓
Database capacity
```

must be considered together.

______________________________________________________________________

# 42. Bounded Concurrency

A semaphore can limit concurrent operations.

```python
semaphore = asyncio.Semaphore(10)


async def fetch(item):
    async with semaphore:
        return await remote_call(item)
```

At most 10 tasks can enter the protected section concurrently.

This is useful for:

- External APIs
- Database access
- Resource protection
- Rate limiting
- Backpressure

______________________________________________________________________

# 43. Backpressure

Backpressure prevents producers from overwhelming consumers.

Example:

```text
Producer
   ↓
100,000 operations
   ↓
10 database connections
```

Unbounded concurrency can cause:

- Memory pressure
- Connection exhaustion
- Increased latency
- Downstream failures

Use:

- Bounded queues
- Semaphores
- Worker pools
- Rate limits
- Connection limits

______________________________________________________________________

# 44. Concurrency, Retries and Idempotency

Concurrency and retries can produce duplicate side effects.

Example:

```text
Request
   ↓
Payment operation
   ↓
Timeout
   ↓
Retry
   ↓
Original operation actually succeeded
```

The retry could perform the operation twice.

For operations such as:

- Payments
- Order creation
- Message processing
- External side effects

consider idempotency and deduplication.

______________________________________________________________________

# 45. Concurrency and Database Transactions

Application concurrency does not replace database concurrency control.

When multiple requests update the same data, use appropriate database mechanisms such as:

- Transactions
- Row-level locks
- Optimistic locking
- Unique constraints

The correct mechanism depends on the business operation.

______________________________________________________________________

# 46. Exception Handling in Concurrent Work

When several tasks execute concurrently, failures require careful handling.

Consider:

```python
await asyncio.gather(
    operation_a(),
    operation_b(),
    operation_c(),
)
```

One operation may fail while others have progressed.

Production code should consider:

- Failure propagation
- Cancellation
- Cleanup
- Partial results
- Retry behavior
- Idempotency

______________________________________________________________________

# 47. Common Concurrency Mistakes

## Mistake 1 — Thinking Python threads are useless

They are useful for I/O-bound workloads and blocking integrations.

______________________________________________________________________

## Mistake 2 — Thinking `async def` makes code asynchronous

Blocking operations inside `async def` can still block the event loop.

______________________________________________________________________

## Mistake 3 — Creating unlimited tasks

This can exhaust memory and overwhelm dependencies.

______________________________________________________________________

## Mistake 4 — Holding locks during slow I/O

This can dramatically reduce concurrency.

______________________________________________________________________

## Mistake 5 — Adding concurrency without considering downstream capacity

Database pools and external service limits can become the real bottleneck.

______________________________________________________________________

## Mistake 6 — Ignoring cancellation

Long-running async work should respond correctly to cancellation.

______________________________________________________________________

## Mistake 7 — Retrying non-idempotent operations blindly

Retries can create duplicate side effects.

______________________________________________________________________

## Mistake 8 — Using processes for tiny tasks

Process creation and serialization overhead can outweigh the benefit.

______________________________________________________________________

# 48. Backend Decision Framework

When asked:

> "How would you make this backend operation concurrent?"

Walk through these questions:

### Step 1 — Is it CPU-bound or I/O-bound?

This determines the initial direction.

### Step 2 — Is the operation synchronous or asynchronous?

If blocking libraries are involved, threads may be appropriate.

### Step 3 — Can operations run independently?

If yes, concurrent execution may reduce latency.

### Step 4 — What are the downstream limits?

Check:

- Database pool
- HTTP connection pool
- API rate limits
- CPU
- Memory

### Step 5 — Do we need bounded concurrency?

If the number of operations can become large, usually yes.

### Step 6 — What happens on failure?

Define:

- Timeout
- Retry
- Cancellation
- Partial failure
- Idempotency

This is a strong senior-level approach because it considers the entire system rather than only Python syntax.

______________________________________________________________________

# 49. Interview Questions & Answers

## Q1. What is concurrency?

**Answer:**

Concurrency means multiple tasks can make progress during overlapping periods.

They do not necessarily execute simultaneously.

______________________________________________________________________

## Q2. What is parallelism?

**Answer:**

Parallelism means multiple tasks execute simultaneously, generally using multiple CPU cores or execution units.

______________________________________________________________________

## Q3. CPU-bound vs I/O-bound?

**Answer:**

CPU-bound work primarily consumes CPU for computation.

I/O-bound work primarily waits for external resources such as databases or networks.

______________________________________________________________________

## Q4. Threads vs processes?

**Answer:**

Threads share memory within a process and are useful for concurrent I/O.

Processes have separate memory and can provide CPU parallelism, at the cost of higher process/communication overhead.

______________________________________________________________________

## Q5. What is the GIL?

**Answer:**

The GIL is a CPython implementation mechanism that traditionally permits only one thread at a time to execute Python
bytecode within a given interpreter.

It limits CPU-bound Python-bytecode parallelism with threads, but does not make threading useless.

______________________________________________________________________

## Q6. Why are threads useful despite the GIL?

**Answer:**

Threads can overlap I/O waits, and the GIL can be released during I/O or by native extensions.

They are therefore useful for many I/O-bound workloads and blocking libraries.

______________________________________________________________________

## Q7. What is a race condition?

**Answer:**

A race condition occurs when the result depends on the timing or interleaving of concurrent operations.

Shared mutable state is a common source.

______________________________________________________________________

## Q8. How do you protect shared state between threads?

**Answer:**

Use appropriate synchronization such as a `Lock`, or preferably redesign the system to minimize shared mutable state.

______________________________________________________________________

## Q9. What is a critical section?

**Answer:**

A critical section is a portion of code that accesses shared state and needs synchronization to maintain correctness.

______________________________________________________________________

## Q10. What is a deadlock?

**Answer:**

A deadlock occurs when concurrent operations wait indefinitely for resources held by one another.

______________________________________________________________________

## Q11. How do you prevent deadlocks?

**Answer:**

Use consistent lock ordering, minimize lock scope, avoid unnecessary nested locks, and use timeouts where appropriate.

______________________________________________________________________

## Q12. What is `ThreadPoolExecutor`?

**Answer:**

It manages a pool of worker threads and provides a convenient API for executing multiple callable tasks concurrently.

It is especially useful for blocking I/O workloads.

______________________________________________________________________

## Q13. What is a Future?

**Answer:**

A Future represents the eventual result or failure of asynchronous/concurrent work submitted to an executor.

______________________________________________________________________

## Q14. When would you use multiprocessing?

**Answer:**

For CPU-bound workloads where process-based parallelism can use multiple CPU cores.

______________________________________________________________________

## Q15. Why does multiprocessing have overhead?

**Answer:**

Processes have separate memory spaces and communication often requires serialization or IPC.

Creating processes and moving data between them can therefore be expensive.

______________________________________________________________________

## Q16. What is AsyncIO?

**Answer:**

AsyncIO is Python's asynchronous I/O framework based around an event loop, coroutines and tasks.

It is particularly useful for high-concurrency I/O-bound applications.

______________________________________________________________________

## Q17. What is an event loop?

**Answer:**

The event loop coordinates asynchronous tasks and resumes them when awaited non-blocking operations become ready.

______________________________________________________________________

## Q18. What is a coroutine?

**Answer:**

A coroutine is the execution object produced when an `async def` function is called.

It can suspend at `await` points and later resume.

______________________________________________________________________

## Q19. What does `await` do?

**Answer:**

It suspends the current coroutine while the awaited operation is incomplete, allowing the event loop to run other ready
tasks.

______________________________________________________________________

## Q20. Coroutine vs Task?

**Answer:**

A coroutine is an awaitable execution object.

A Task schedules a coroutine to run on the event loop and represents its eventual completion.

______________________________________________________________________

## Q21. What does `asyncio.gather()` do?

**Answer:**

It waits for multiple awaitables and is commonly used to execute independent asynchronous operations concurrently.

______________________________________________________________________

## Q22. Why can `gather()` with thousands of operations be dangerous?

**Answer:**

Unbounded concurrency can consume large amounts of memory and overwhelm databases, APIs, connection pools or other
dependencies.

Use bounded concurrency when appropriate.

______________________________________________________________________

## Q23. Why is `time.sleep()` bad inside async code?

**Answer:**

It blocks the event-loop thread.

Other tasks using that event loop may be unable to make progress.

Use `await asyncio.sleep()` for asynchronous sleeping.

______________________________________________________________________

## Q24. Does `async def` automatically make code non-blocking?

**Answer:**

No.

A blocking synchronous operation inside an async function can still block the event loop.

______________________________________________________________________

## Q25. How do you use a blocking library inside an async application?

**Answer:**

Prefer an async-compatible library when possible.

If the blocking library must be used, move the blocking operation to an appropriate thread/executor rather than blocking
the event loop.

______________________________________________________________________

## Q26. Is AsyncIO useful for CPU-bound work?

**Answer:**

Not by itself.

CPU-heavy code can block the event loop.

Use processes, worker systems or another appropriate execution model for significant CPU-bound work.

______________________________________________________________________

## Q27. What is cancellation?

**Answer:**

Cancellation is a request for an asynchronous task to stop.

It is cooperative, so code should allow cancellation to propagate and perform required cleanup.

______________________________________________________________________

## Q28. Why are timeouts important?

**Answer:**

They prevent external operations from waiting indefinitely and consuming resources.

Timeouts are essential for resilient backend systems.

______________________________________________________________________

## Q29. How do you limit concurrent async operations?

**Answer:**

Use mechanisms such as:

```python
asyncio.Semaphore
```

bounded queues, worker pools or rate limiters.

______________________________________________________________________

## Q30. What is backpressure?

**Answer:**

Backpressure prevents producers from overwhelming consumers or downstream dependencies.

______________________________________________________________________

## Q31. How does a connection pool affect AsyncIO concurrency?

**Answer:**

The application may schedule many tasks, but the connection pool limits how many database operations can actually
execute concurrently.

Therefore, application concurrency must be designed around downstream capacity.

______________________________________________________________________

## Q32. Why can more concurrency make a service slower?

**Answer:**

Too much concurrency can cause contention, connection exhaustion, CPU scheduling overhead, memory pressure and
downstream overload.

Concurrency needs to be bounded and aligned with system capacity.

______________________________________________________________________

## Q33. How do retries interact with concurrency?

**Answer:**

Concurrent retries can duplicate side effects.

Operations that may be retried should be designed for idempotency or deduplication.

______________________________________________________________________

## Q34. How does concurrency affect database correctness?

**Answer:**

Concurrent requests can update the same records simultaneously.

Database transactions, locks, optimistic concurrency controls and constraints may be required to preserve correctness.

______________________________________________________________________

## Q35. How would you choose between synchronous code, threads, AsyncIO and processes?

**Answer:**

Start with the workload.

- Simple synchronous operation → synchronous code.
- Blocking I/O → threads may help.
- High-volume non-blocking I/O → AsyncIO is often appropriate.
- CPU-bound work → processes or a dedicated worker system.

Then consider downstream capacity, failure handling, resource limits and operational complexity.

______________________________________________________________________

# 50. Scenario-Based Questions

## Scenario 1 — Three Independent HTTP Calls

An endpoint performs:

```python
a = await call_a()
b = await call_b()
c = await call_c()
```

Each takes approximately 200 ms.

**Question:** How could you reduce latency?

**Answer:**

If they are independent, run them concurrently:

```python
a, b, c = await asyncio.gather(
    call_a(),
    call_b(),
    call_c(),
)
```

The total waiting time can approach the slowest call rather than the sum, assuming the remote systems and connection
pools can support the concurrency.

______________________________________________________________________

## Scenario 2 — `requests` Inside FastAPI

You find:

```python
async def endpoint():
    response = requests.get(url)
    return response.json()
```

**Question:** What is the problem?

**Answer:**

`requests.get()` is blocking.

It can block the event-loop thread.

Use an async HTTP client or move the blocking call to an appropriate thread/executor.

______________________________________________________________________

## Scenario 3 — Database Connection Exhaustion

A developer changes an endpoint to:

```python
await asyncio.gather(
    *[query_database(i) for i in range(1000)]
)
```

Production starts reporting connection pool exhaustion.

**Question:** Why?

**Answer:**

The application created more concurrent work than the database connection pool and database could handle.

Use bounded concurrency, batching or a better query strategy.

______________________________________________________________________

## Scenario 4 — CPU Work Blocks Requests

An async API endpoint performs a CPU-heavy calculation.

Other requests become slow.

**Question:** Why?

**Answer:**

The CPU-heavy work is executing on the event-loop thread and prevents other tasks from progressing.

Move the work to a process pool, worker or separate service.

______________________________________________________________________

## Scenario 5 — Shared Counter

Multiple threads update:

```python
counter += 1
```

The final result is unexpectedly low.

**Question:** What is the likely issue?

**Answer:**

Concurrent access to shared mutable state creates a race condition.

Protect the critical section with synchronization or redesign the state ownership.

______________________________________________________________________

## Scenario 6 — Deadlock

Thread A acquires:

```text
lock_a → lock_b
```

Thread B acquires:

```text
lock_b → lock_a
```

The service hangs.

**Question:** Diagnose and fix it.

**Answer:**

The threads can deadlock through circular waiting.

Establish a consistent lock acquisition order and minimize nested locking.

______________________________________________________________________

## Scenario 7 — Millions of Tasks

A service processes millions of records with:

```python
await asyncio.gather(
    *[process(record) for record in records]
)
```

**Question:** What is dangerous about this?

**Answer:**

It can create an enormous amount of in-memory concurrency and overwhelm dependencies.

Use bounded concurrency, batching or a worker queue.

______________________________________________________________________

## Scenario 8 — Timeout and Retry

A payment API call times out after five seconds. The application retries immediately, but the original request actually
succeeded.

**Question:** What problem can occur?

**Answer:**

The retry can create a duplicate payment.

The operation should use an idempotency mechanism or another deduplication strategy.

______________________________________________________________________

## Scenario 9 — Choosing the Concurrency Model

A service needs to:

1. Make 100 independent HTTP calls.
1. Process a large CPU-heavy transformation.
1. Call an existing blocking SDK.

**Question:** What would you choose?

**Answer:**

Potentially:

1. AsyncIO for the independent non-blocking HTTP calls.
1. Processes/worker system for the CPU-heavy transformation.
1. A thread/executor for the blocking SDK if it must remain synchronous.

The final design should also consider rate limits, connection pools and workload size.

______________________________________________________________________

# 51. Practice Exercises

## Exercise 1 — Threading

Create a program that executes several independent blocking operations.

Compare:

```text
Sequential execution
vs
multiple threads
```

Measure elapsed time.

______________________________________________________________________

## Exercise 2 — Race Condition

Create a shared counter and update it from multiple threads.

Observe the result.

Then protect the critical section with a lock.

Explain why the lock fixes the correctness problem.

______________________________________________________________________

## Exercise 3 — Deadlock

Create a small program with two locks and intentionally reproduce a deadlock.

Then fix it using consistent lock ordering.

Terminate the test program safely if it becomes deadlocked.

______________________________________________________________________

## Exercise 4 — ThreadPoolExecutor

Use:

```python
ThreadPoolExecutor
```

to execute multiple blocking I/O operations.

Experiment with different pool sizes and record the effect on elapsed time.

Explain why increasing the pool size indefinitely does not necessarily improve performance.

______________________________________________________________________

## Exercise 5 — ProcessPoolExecutor

Create a CPU-heavy function.

Compare:

```text
Sequential
vs
ProcessPoolExecutor
```

Measure the difference.

______________________________________________________________________

## Exercise 6 — AsyncIO Basics

Create three async functions that each wait for one second.

Run them:

1. Sequentially.
1. Concurrently with `asyncio.gather()`.

Compare elapsed time.

______________________________________________________________________

## Exercise 7 — Blocking Async Code

Compare:

```python
async def bad():
    time.sleep(2)
```

with:

```python
async def good():
    await asyncio.sleep(2)
```

Run both alongside another async task and observe the difference.

______________________________________________________________________

## Exercise 8 — Bounded Async Concurrency

Process 1,000 asynchronous operations but allow only 10 concurrent operations using:

```python
asyncio.Semaphore(10)
```

Explain how this protects downstream resources.

______________________________________________________________________

## Exercise 9 — FastAPI Concurrency Review

Take one endpoint from a backend application.

Identify:

- CPU-bound operations
- Blocking operations
- Async/non-blocking operations
- External dependencies
- Connection-pool limits
- Places where concurrency could improve latency
- Places where concurrency could cause overload

______________________________________________________________________

## Exercise 10 — Failure Design

Design an asynchronous operation that has:

- A timeout
- Cancellation handling
- Retry behavior
- Idempotency protection
- Bounded concurrency

Explain the failure behavior for each step.

______________________________________________________________________

# 52. Quick Revision

| Concept | Key Point |
|---|---|
| Concurrency | Multiple tasks make overlapping progress |
| Parallelism | Multiple tasks execute simultaneously |
| CPU-bound | Mostly computation |
| I/O-bound | Mostly waiting |
| Thread | Execution unit sharing process memory |
| Process | Separate memory/execution unit |
| GIL | CPython mechanism limiting simultaneous Python-bytecode execution by traditional threads |
| Race condition | Result depends on timing/interleaving |
| Lock | Mutual exclusion |
| RLock | Reentrant lock |
| Deadlock | Indefinite circular/resource waiting |
| ThreadPoolExecutor | Thread pool abstraction |
| Future | Represents eventual concurrent result |
| Multiprocessing | Separate-process execution |
| ProcessPoolExecutor | Process pool abstraction |
| AsyncIO | Asynchronous I/O framework |
| Event loop | Coordinates async tasks |
| Coroutine | Awaitable execution object from `async def` |
| Task | Scheduled coroutine |
| `await` | Suspends coroutine while awaited work progresses |
| `gather` | Waits for multiple awaitables |
| Cancellation | Cooperative request to stop async work |
| Timeout | Bounds waiting time |
| Semaphore | Limits concurrent operations |
| Backpressure | Prevents downstream overload |
| Blocking async code | Synchronous work that blocks event loop |
| Idempotency | Makes repeated logical operations safe |

______________________________________________________________________

# 53. Completion Checklist

Before moving to File 11, make sure you can explain:

- [ ] Concurrency
- [ ] Parallelism
- [ ] CPU-bound vs I/O-bound
- [ ] Threads
- [ ] Processes
- [ ] GIL
- [ ] Thread creation
- [ ] Shared mutable state
- [ ] Race conditions
- [ ] Locks
- [ ] Critical sections
- [ ] `Lock` vs `RLock`
- [ ] Deadlocks
- [ ] Deadlock prevention
- [ ] `ThreadPoolExecutor`
- [ ] Futures
- [ ] Thread-pool sizing
- [ ] Multiprocessing
- [ ] `ProcessPoolExecutor`
- [ ] Process communication
- [ ] Choosing threads vs processes
- [ ] AsyncIO
- [ ] Event loop
- [ ] Coroutines
- [ ] `await`
- [ ] Tasks
- [ ] Coroutine vs Task
- [ ] `asyncio.gather()`
- [ ] Sequential vs concurrent async execution
- [ ] Cancellation
- [ ] Timeouts
- [ ] Async context managers
- [ ] Async iteration
- [ ] Async generators
- [ ] Blocking calls inside async code
- [ ] Blocking third-party libraries
- [ ] CPU-heavy work inside AsyncIO
- [ ] FastAPI and AsyncIO
- [ ] Connection pools
- [ ] Bounded concurrency
- [ ] Semaphores
- [ ] Backpressure
- [ ] Retries and idempotency
- [ ] Database concurrency
- [ ] Concurrent exception handling
- [ ] Choosing the right concurrency model

______________________________________________________________________

# 54. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is concurrency?
1. What is parallelism?
1. CPU-bound vs I/O-bound?
1. Threads vs processes?
1. Explain the GIL.
1. Why are threads still useful in Python?
1. What is a race condition?
1. How do you protect shared state?
1. What is a critical section?
1. What is a deadlock?
1. How do you prevent deadlocks?
1. What is `ThreadPoolExecutor`?
1. What is a Future?
1. When would you use multiprocessing?
1. What is `ProcessPoolExecutor`?
1. Why does multiprocessing have overhead?
1. What is AsyncIO?
1. Explain the event loop.
1. What is a coroutine?
1. What does `await` do?
1. What is an asyncio Task?
1. Coroutine vs Task?
1. What does `asyncio.gather()` do?
1. When should independent operations be executed concurrently?
1. Why can unbounded `gather()` be dangerous?
1. Why is `time.sleep()` dangerous in async code?
1. Does `async def` automatically make blocking code non-blocking?
1. How would you use a blocking SDK inside an async application?
1. Is AsyncIO suitable for CPU-heavy work?
1. What is cancellation?
1. Why are timeouts important?
1. How do you limit async concurrency?
1. What is backpressure?
1. How do connection pools affect concurrency?
1. Why can more concurrency make a system slower?
1. How do retries interact with idempotency?
1. How does concurrency affect database correctness?
1. How would you choose between sync, threads, AsyncIO and processes?
1. A FastAPI endpoint is slow because it performs three independent network calls sequentially. What would you change?
1. A production service starts exhausting database connections after introducing `asyncio.gather()`. How would you diagnose and fix it?
1. An async endpoint blocks every other request while performing a CPU-heavy calculation. What would you do?
1. A service hangs intermittently after introducing two locks. How would you investigate a possible deadlock?
1. A payment operation times out and retries. How would you prevent duplicate charges?

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [09. Advanced Python OOP](./09-python-advanced-oop.md)

**Next:** [11. Typing & Testing](./11-python-exceptions-typing-testing.md)
