# Celery Masterclass for Backend Engineers

## File 16 – Sending Tasks, `delay()`, `apply_async()` & Advanced Task Options

> **Course Level:** Intermediate → Advanced
>
> By now you've learned how to create and execute Celery tasks.
>
> But in production, developers rarely use only:
>
> ```python
> task.delay(...)
> ```
>
> Instead, they use:
>
> - `apply_async()`
> - Countdown
> - ETA
> - Expiration
> - Retries
> - Routing
> - Priorities
> - Custom Queues
>
> This chapter covers all of them.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Understand `delay()`
- Understand `apply_async()`
- Know when to use each
- Schedule future tasks
- Delay task execution
- Route tasks to specific queues
- Assign task priorities
- Configure task expiration
- Design production-ready task submissions

______________________________________________________________________

# Table of Contents

1. delay()
1. apply_async()
1. delay vs apply_async
1. Countdown
1. ETA
1. Expiration
1. Routing
1. Priorities
1. Serialization
1. Production Examples
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Why Isn't `delay()` Enough?

Most beginners write

```python
send_email.delay(user.email)
```

Works perfectly.

But what if you want

- Execute after 5 minutes
- Execute tomorrow morning
- Execute only before midnight
- Execute on the high-priority queue
- Execute on GPU workers
- Execute with retries

`delay()` cannot do these.

______________________________________________________________________

# delay()

`delay()` is simply

a shortcut.

```python
send_email.delay(user.email)
```

Internally,

Celery converts it into

```python
send_email.apply_async(args=[user.email])
```

That's all.

No magic.

______________________________________________________________________

# What Does delay() Support?

Only

- Positional arguments
- Keyword arguments

Example

```python
resize_image.delay(
    "photo.jpg",
    width=500
)
```

Nothing more.

______________________________________________________________________

# apply_async()

`apply_async()` is the real API.

Everything in Celery

eventually becomes

```python
apply_async()
```

Example

```python
send_email.apply_async(
    args=["alice@gmail.com"]
)
```

Equivalent to

```python
send_email.delay(
    "alice@gmail.com"
)
```

______________________________________________________________________

# Why Use apply_async()?

Because it supports

- Countdown
- ETA
- Expiration
- Queue selection
- Priority
- Retry options
- Serialization options
- Routing options

Almost every advanced feature.

______________________________________________________________________

# delay vs apply_async

| delay() | apply_async() |
|----------|---------------|
| Simple | Advanced |
| Shortcut | Full API |
| No scheduling | Supports scheduling |
| No routing | Supports routing |
| No priority | Supports priority |
| Easier | More powerful |

______________________________________________________________________

# Countdown

Suppose

User signs up.

Instead of sending

Welcome Email

immediately,

wait

```
10 Minutes
```

Example

```python
send_email.apply_async(
    args=[email],
    countdown=600
)
```

RabbitMQ stores the task.

Worker executes it

10 minutes later.

______________________________________________________________________

Timeline

```
12:00

↓

Task Submitted

↓

12:10

↓

Worker Executes
```

______________________________________________________________________

# Real Production Example

Food delivery.

```
Order Delivered
```

Wait

```
30 Minutes
```

Then ask

```
Rate Your Delivery
```

Countdown is perfect.

______________________________________________________________________

# ETA (Exact Time)

Countdown

means

```
Run After X Seconds
```

ETA

means

```
Run At This Exact Time
```

Example

```python
from datetime import datetime

send_email.apply_async(
    eta=datetime(
        2026,
        12,
        25,
        9,
        0
    )
)
```

Runs

```
Christmas

9:00 AM
```

______________________________________________________________________

# Countdown vs ETA

Countdown

```
10 Minutes Later
```

ETA

```
Tomorrow

10:00 AM
```

______________________________________________________________________

Comparison

| Countdown | ETA |
|------------|-----|
| Relative | Absolute |
| Seconds later | Specific date/time |
| Simpler | Calendar based |

______________________________________________________________________

# Expiration

Suppose

```
OTP
```

valid only for

```
5 Minutes
```

If the task hasn't started,

don't execute it.

Example

```python
send_otp.apply_async(
    args=[phone],
    expires=300
)
```

After

```
5 Minutes
```

Celery discards it.

______________________________________________________________________

Real Example

```
Flash Sale Notification
```

Useful only today.

Tomorrow

it's meaningless.

______________________________________________________________________

# Queue Routing

Imagine

```
Email Task
```

Should not go to

```
Video Workers
```

Instead

```python
send_email.apply_async(
    queue="email"
)
```

RabbitMQ routes it

to the Email Queue.

______________________________________________________________________

Architecture

```
Email Queue

↓

Email Workers

--------------------

Video Queue

↓

Video Workers
```

______________________________________________________________________

# Why Route Tasks?

Suppose

Video Encoding

takes

```
5 Minutes
```

Email

takes

```
50 ms
```

If both share

the same Queue,

Emails become slow.

Separate Queues solve this.

______________________________________________________________________

# Task Priorities

Suppose

Queue contains

```
Newsletter

Newsletter

Newsletter

Password Reset
```

Password Reset

should execute first.

Celery supports priorities.

Example

```python
reset_password.apply_async(
    priority=9
)
```

Newsletter

```python
send_newsletter.apply_async(
    priority=1
)
```

Higher priority

gets processed sooner,

provided the broker supports priorities and the queue is configured for them.

______________________________________________________________________

# Production Example

Priority

```
10

↓

Payment

```

Priority

```
8

↓

Password Reset
```

Priority

```
5

↓

Invoice
```

Priority

```
1

↓

Analytics
```

______________________________________________________________________

# Serialization

Before RabbitMQ receives a task,

Celery serializes it.

Common serializers

```
JSON

Pickle

YAML

MessagePack
```

Default

```
JSON
```

______________________________________________________________________

# Why JSON?

Advantages

- Language independent
- Safe
- Fast
- Human readable

______________________________________________________________________

# Why Not Pickle?

Pickle can serialize almost anything,

including Python objects.

But

- Python-specific
- Security risks if data is untrusted

Production systems

usually prefer

```
JSON
```

______________________________________________________________________

# Task IDs

Every task receives

```
UUID
```

Example

```python
result = task.delay()
```

```python
print(result.id)
```

Output

```
8d67...

```

Useful for

- Logging
- Monitoring
- Debugging
- API responses

______________________________________________________________________

# Complete Flow

```
FastAPI

↓

apply_async()

↓

Celery

↓

Serialize

↓

RabbitMQ

↓

Queue

↓

Worker

↓

Execute

↓

Result Backend
```

______________________________________________________________________

# Production Example

Customer places an order.

API

↓

Save Order

↓

Return Response

↓

Generate Invoice

```
Queue = invoice
```

↓

Send Email

```
Queue = email
```

↓

Notify Warehouse

```
Countdown = 5 Seconds
```

↓

Analytics

```
Priority = Low
```

Every task

uses different options.

______________________________________________________________________

# Best Practices

✔ Use `delay()` for simple tasks.

✔ Use `apply_async()` for production.

✔ Separate workloads by Queue.

✔ Use priorities carefully.

✔ Use Countdown for reminders.

✔ Use ETA for scheduled events.

✔ Expire obsolete tasks.

✔ Prefer JSON serialization.

______________________________________________________________________

# Summary

`delay()` is a convenient shortcut for submitting Celery tasks.

`apply_async()` is the full-featured API that enables scheduling, routing, priorities, expiration, and other advanced
task options.

Most production systems use `apply_async()` because it provides complete control over task execution.

______________________________________________________________________

# Key Takeaways

- `delay()` internally calls `apply_async()`.
- `apply_async()` supports advanced task options.
- Countdown schedules tasks after a delay.
- ETA schedules tasks at an exact time.
- Expiration prevents stale tasks from executing.
- Queue routing separates workloads.
- Priorities help order task execution.
- JSON is the preferred serializer.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### What is the difference between `delay()` and `apply_async()`?

#### Answer

`delay()` is a convenience wrapper around `apply_async()` that only supports passing task arguments. `apply_async()`
provides advanced options such as countdowns, ETAs, routing, priorities, expiration, and retry configuration.

______________________________________________________________________

## Question 2

### When should you use `apply_async()`?

#### Answer

Use `apply_async()` whenever you need advanced scheduling or routing features, such as delayed execution, queue
selection, task priorities, expiration, or custom execution options.

______________________________________________________________________

## Question 3

### What is the difference between Countdown and ETA?

#### Answer

Countdown schedules a task relative to the current time (for example, 10 minutes later), while ETA schedules a task at a
specific absolute date and time.

______________________________________________________________________

## Question 4

### Why would you configure task expiration?

#### Answer

Expiration prevents outdated tasks, such as OTP delivery or flash sale notifications, from executing after they are no
longer useful.

______________________________________________________________________

## Question 5

### Why should tasks be routed to different queues?

#### Answer

Separating workloads prevents long-running tasks from blocking lightweight tasks and allows each workload to scale
independently with dedicated worker pools.

______________________________________________________________________

## Question 6

### Why is JSON the preferred serializer?

#### Answer

JSON is language-independent, widely supported, human-readable, and safer than Python-specific serializers like Pickle
when exchanging messages between systems.

______________________________________________________________________

## Question 7

### Does RabbitMQ automatically respect task priorities?

#### Answer

No. Queue priorities depend on broker support and queue configuration. Simply assigning a priority in Celery is not
sufficient unless the underlying queue is configured to use priorities.

______________________________________________________________________

# Practice Questions

1. Explain how `delay()` works internally.
1. Compare `delay()` and `apply_async()`.
1. What is Countdown?
1. What is ETA?
1. When should Expiration be used?
1. Why separate tasks into multiple queues?
1. Explain task priorities.
1. Why is JSON preferred over Pickle?
1. Design a routing strategy for an e-commerce application.
1. Explain the complete flow of `apply_async()`.

______________________________________________________________________

# Mini Assignment

Design the task submission strategy for a banking application.

Tasks include:

- Send OTP
- Generate monthly statement
- Fraud detection
- Notify customer
- Backup transactions
- Generate analytics

For each task, specify:

- `delay()` or `apply_async()`
- Queue name
- Priority
- Countdown or ETA (if applicable)
- Expiration
- Serializer

Explain why you chose each option.

______________________________________________________________________

# Common Mistakes

❌ Using `delay()` when scheduling is required.

❌ Sending every task to the default queue.

❌ Using task priorities without configuring broker support.

❌ Using Pickle for untrusted environments.

❌ Forgetting to expire time-sensitive tasks.

❌ Mixing CPU-intensive and lightweight tasks in the same queue.

______________________________________________________________________

# What's Next?

Now that you know how to submit tasks with advanced options, we'll explore **task reliability**.

The next chapter covers:

- Automatic retries
- Retry policies
- Exponential backoff
- Retry limits
- Idempotency
- Time limits
- Soft vs Hard timeouts
- Failure handling

➡ **Next File:** [File 17 – Retries, Time Limits & Reliable Task Execution](17-retries-timeouts.md)
