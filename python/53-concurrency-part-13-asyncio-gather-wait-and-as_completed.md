# File: python/53-concurrency-part-13-asyncio-gather-wait-and-as_completed.md

# Advanced Python Runtime & Concurrency

# Concurrency Part 13: Coordinating Multiple Tasks with `asyncio.gather()`, `wait()` & `as_completed()`

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced Python Runtime & Concurrency
>
> **Lesson:** 53
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 10 Hours

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `asyncio.gather()` | Python 3.4 |
| `asyncio.wait()` | Python 3.4 |
| `asyncio.as_completed()` | Python 3.4 |

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why coordinating multiple tasks is important
- `asyncio.gather()`
- `asyncio.wait()`
- `asyncio.as_completed()`
- Result ordering
- Exception handling
- Partial completion
- Timeouts
- Cancellation behaviour
- Production backend patterns
- Best practices
- questions

______________________________________________________________________

# Recap

In the previous lesson we learned:

- Event Loop
- Tasks
- `create_task()`
- Task lifecycle
- Task cancellation

Creating tasks is only half the story.

Suppose your API creates

```
50 Tasks
```

How do you wait for them?

Should you write

```python
await task1
await task2
await task3
...
```

There are much better solutions.

______________________________________________________________________

# The Problem

Suppose an endpoint needs

```
User Profile

Orders

Notifications

Permissions

Recommendations
```

Each request is independent.

Waiting for them one by one wastes time.

Instead,

they should execute concurrently.

______________________________________________________________________

# Sequential Approach

```python
profile = await fetch_profile()

orders = await fetch_orders()

notifications = await fetch_notifications()
```

Execution

```
Profile

↓

Orders

↓

Notifications
```

______________________________________________________________________

# Concurrent Approach

```
Profile

Orders

Notifications

↓

Run Together
```

The total response time becomes approximately

```
Longest Task
```

instead of

```
Sum Of All Tasks
```

______________________________________________________________________

# Introducing `asyncio.gather()`

`gather()` is the most commonly used function for running multiple coroutines concurrently.

```python
results = await asyncio.gather(
    coroutine1(),
    coroutine2(),
    coroutine3()
)
```

______________________________________________________________________

# First Example

```python
import asyncio


async def fetch(name):

    print(f"Starting {name}")

    await asyncio.sleep(2)

    print(f"Finished {name}")

    return name


async def main():

    results = await asyncio.gather(

        fetch("Users"),

        fetch("Orders"),

        fetch("Products")

    )

    print(results)


asyncio.run(main())
```

Output

```text
Starting Users
Starting Orders
Starting Products

Finished Users
Finished Orders
Finished Products

['Users', 'Orders', 'Products']
```

______________________________________________________________________

# What Happens?

```
Coroutine 1

↓

Task

↓

Coroutine 2

↓

Task

↓

Coroutine 3

↓

Task

↓

Event Loop

↓

Concurrent Execution
```

Notice

You never called

```python
create_task()
```

Internally,

`gather()` automatically schedules the coroutines as tasks.

______________________________________________________________________

# Result Ordering

Suppose

```
Task A

2 seconds

Task B

1 second

Task C

3 seconds
```

Completion order

```
B

A

C
```

Result from `gather()`

```python
[
    result_A,
    result_B,
    result_C
]
```

Important:

Results always follow the **input order**,

not completion order.

______________________________________________________________________

# Exception Behaviour

Suppose

```python
async def divide():

    return 10 / 0
```

Example

```python
await asyncio.gather(

    fetch_users(),

    divide(),

    fetch_orders()
)
```

Default behaviour

```
One Task Fails

↓

gather Raises Exception

↓

Caller Receives Error
```

______________________________________________________________________

# `return_exceptions=True`

Sometimes

you want all tasks to finish,

even if some fail.

```python
results = await asyncio.gather(

    task1(),

    task2(),

    return_exceptions=True

)
```

Now

exceptions become part of the result list.

Example

```python
[
    "Users",

    ZeroDivisionError(),

    "Orders"
]
```

______________________________________________________________________

# Production Example

Suppose an API loads:

- User
- Orders
- Wishlist
- Notifications

If one service fails,

you may still return partial data.

`return_exceptions=True`

allows graceful degradation.

______________________________________________________________________

# Introducing `asyncio.wait()`

Unlike `gather()`,

`wait()` provides finer control.

```python
done,

pending = await asyncio.wait(
    tasks
)
```

It returns two sets.

```
Completed Tasks

Pending Tasks
```

______________________________________________________________________

# Example

```python
tasks = [

    asyncio.create_task(fetch(i))

    for i in range(5)

]

done, pending = await asyncio.wait(
    tasks
)
```

______________________________________________________________________

# Return Conditions

`wait()` supports multiple stopping conditions.

______________________________________________________________________

## Wait For Everything

```python
asyncio.ALL_COMPLETED
```

Default behaviour.

______________________________________________________________________

## Wait For First Task

```python
asyncio.FIRST_COMPLETED
```

Example

```
Five Tasks

↓

First Finishes

↓

Return Immediately
```

______________________________________________________________________

## Wait For First Exception

```python
asyncio.FIRST_EXCEPTION
```

Returns immediately

if any task fails.

______________________________________________________________________

# Timeouts

Suppose

you wait only

```
3 Seconds
```

```python
done, pending = await asyncio.wait(

    tasks,

    timeout=3
)
```

Tasks still running after three seconds remain inside

```
pending
```

______________________________________________________________________

# Cancelling Pending Tasks

```python
for task in pending:

    task.cancel()
```

Very common in production systems.

______________________________________________________________________

# Introducing `asyncio.as_completed()`

Sometimes

you don't care about input order.

You want results

as soon as they finish.

That's exactly what

```python
asyncio.as_completed()
```

provides.

______________________________________________________________________

# Example

```python
tasks = [

    asyncio.create_task(fetch(i))

    for i in range(5)

]

for completed in asyncio.as_completed(tasks):

    result = await completed

    print(result)
```

______________________________________________________________________

# Execution

Suppose

```
Task A

3 sec

Task B

1 sec

Task C

2 sec
```

Completion

```
B

↓

C

↓

A
```

Results arrive immediately.

No waiting for slower tasks.

______________________________________________________________________

# Comparison

## `gather()`

```
Start Everything

↓

Wait Everything

↓

Return List
```

______________________________________________________________________

## `wait()`

```
Start Everything

↓

Return

↓

Done

+

Pending
```

______________________________________________________________________

## `as_completed()`

```
Start Everything

↓

Return Results

↓

One By One

↓

Completion Order
```

______________________________________________________________________

# Choosing the Right Tool

| Requirement | Best Choice |
|-------------|-------------|
| Need all results | `gather()` |
| Need partial completion | `wait()` |
| Need results immediately | `as_completed()` |
| Need timeout handling | `wait()` |
| Need ordered results | `gather()` |

______________________________________________________________________

# Backend Example

Suppose

an API gateway calls

```
Inventory Service

Pricing Service

User Service

Recommendation Service
```

Using

```python
asyncio.gather()
```

all four requests execute concurrently.

Instead of

```
800 ms
+
600 ms
+
500 ms
+
700 ms

↓

2600 ms
```

the response becomes approximately

```
800 ms
```

assuming all requests are independent.

______________________________________________________________________

# Processing Large Downloads

Imagine downloading

```
100 Files
```

Using

```python
as_completed()
```

you can process

the first completed download immediately,

without waiting for the remaining ninety-nine.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating tasks

and awaiting them immediately.

```python
task = asyncio.create_task(fetch())

await task
```

This often removes concurrency.

______________________________________________________________________

## Mistake 2

Using `gather()`

when partial results are acceptable.

Sometimes

`as_completed()`

provides a better user experience.

______________________________________________________________________

## Mistake 3

Ignoring pending tasks after a timeout.

Always decide whether they should:

- Continue
- Be cancelled
- Be retried

______________________________________________________________________

## Mistake 4

Assuming `gather()`

returns results

in completion order.

It doesn't.

______________________________________________________________________

# Best Practices

✅ Use `gather()` for independent operations.

✅ Use `as_completed()` for streaming results.

✅ Use `wait()` when timeouts or partial completion matter.

✅ Handle exceptions explicitly.

✅ Cancel unnecessary tasks.

❌ Don't leave pending tasks running unintentionally.

❌ Don't ignore failed tasks.

______________________________________________________________________

# Production Insight

Many backend endpoints perform several independent operations simultaneously.

Example

```
Client

↓

FastAPI Endpoint

↓

Task

↓

Database

↓

Task

↓

Redis

↓

Task

↓

External API

↓

Task

↓

Permission Service

↓

gather()

↓

Single Response
```

This pattern dramatically reduces response time while keeping the code readable.

______________________________________________________________________

# Questions

### Question

> What does `asyncio.gather()` do?

### Answer

It schedules multiple coroutines concurrently and returns their results in the same order they were provided.

______________________________________________________________________

### Question

> When should `asyncio.wait()` be used?

### Answer

When you need finer control over task completion, timeouts, or partial results.

______________________________________________________________________

### Question

> Why use `asyncio.as_completed()`?

### Answer

It allows processing task results immediately as each task finishes instead of waiting for all tasks.

______________________________________________________________________

### Question

> Does `gather()` preserve completion order?

### Answer

No. It preserves the order of the input coroutines.

______________________________________________________________________

### Question

> What happens when one coroutine fails inside `gather()`?

### Answer

By default, the exception is propagated to the caller. Using `return_exceptions=True` allows all tasks to complete and
returns exceptions as results.

______________________________________________________________________

# Practical Lesson

Create

```text
gather_demo.py
```

```python
import asyncio
import random


async def fetch(service):

    delay = random.randint(1, 4)

    print(f"{service} started")

    await asyncio.sleep(delay)

    print(f"{service} finished")

    return service


async def main():

    results = await asyncio.gather(

        fetch("Users"),

        fetch("Orders"),

        fetch("Products"),

        fetch("Notifications")

    )

    print(results)


asyncio.run(main())
```

Modify the program to use

- `wait()`
- `as_completed()`

Compare:

- Result ordering
- Execution flow
- Readability

______________________________________________________________________

# Questions

## Question 1

What is the difference between `gather()` and `wait()`?

### Answer

`gather()` returns the results of all coroutines in input order, while `wait()` returns two sets containing completed
and pending tasks, providing greater control over execution.

______________________________________________________________________

## Question 2

When should `as_completed()` be preferred?

### Answer

When results should be processed immediately as tasks finish rather than waiting for all tasks to complete.

______________________________________________________________________

## Question 3

How does `return_exceptions=True` change the behaviour of `gather()`?

### Answer

Instead of immediately propagating exceptions, it includes them in the returned result list, allowing all tasks to
finish.

______________________________________________________________________

## Question 4

Why is `wait()` useful for implementing timeouts?

### Answer

Because it separates completed and pending tasks, allowing applications to cancel, retry, or continue processing
outstanding work after a timeout.

______________________________________________________________________

## Question 5

Why do many FastAPI endpoints use `asyncio.gather()`?

### Answer

Because they often need to perform several independent I/O operations concurrently, reducing overall response time
without increasing thread usage.

______________________________________________________________________

# Assignment

## Exercise 1

Create five simulated API calls using `asyncio.sleep()`.

Execute them:

- Sequentially
- With `gather()`

Measure and compare execution time.

______________________________________________________________________

## Exercise 2

Replace `gather()` with `as_completed()`.

Print each result immediately as it becomes available.

Observe the difference in output ordering.

______________________________________________________________________

## Exercise 3

Use `wait()` with a timeout of two seconds.

Cancel any pending tasks.

Print:

- Completed tasks
- Cancelled tasks

______________________________________________________________________

## Exercise 4

Imagine a FastAPI endpoint that requires data from:

- PostgreSQL
- Redis
- User Service
- Recommendation Service

Design an implementation using `asyncio.gather()`.

Explain:

- Which operations can run concurrently
- How exceptions should be handled
- Whether partial responses should be returned if one dependency fails

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ How `asyncio.gather()` coordinates multiple coroutines.
- ✅ Result ordering.
- ✅ Exception handling with `return_exceptions=True`.
- ✅ How `asyncio.wait()` provides timeout and completion control.
- ✅ How `asyncio.as_completed()` streams results as tasks finish.
- ✅ Production coordination patterns used in modern async backend services.

______________________________________________________________________

# Next Lesson

**File:**
[54-concurrency-part-14-asyncio-synchronization-primitives](54-concurrency-part-14-asyncio-synchronization-primitives.md)

In the next lesson, you'll learn how asyncio handles synchronization using `asyncio.Lock`, `Event`, `Condition`,
`Semaphore`, `BoundedSemaphore`, and `Queue`. We'll explore race conditions in asynchronous code, resource limiting,
producer-consumer patterns, and the synchronization techniques used in production FastAPI and asynchronous backend
applications.
