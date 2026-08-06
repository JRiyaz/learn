# Celery Masterclass for Backend Engineers

## File 14 – Celery Architecture & Core Components

> **Course Level:** Intermediate → Advanced
>
> In the previous chapter, we learned **what Celery is** and **why it exists**.
>
> In this chapter, we'll go much deeper.
>
> We'll understand exactly **what happens internally** when you write:
>
> ```python
> send_email.delay(user_id)
> ```
>
> This is one of the most important chapters because it explains the complete lifecycle of a Celery task.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Understand every Celery component.
- Explain the lifecycle of a task.
- Understand how Celery communicates with RabbitMQ.
- Explain Workers in detail.
- Understand Result Backends.
- Explain Celery internals in interviews.
- Debug Celery task execution.

______________________________________________________________________

# Table of Contents

1. Celery Architecture
1. Components Overview
1. Celery Application
1. Tasks
1. Broker
1. Worker
1. Result Backend
1. Task Lifecycle
1. Task States
1. Complete Message Flow
1. Production Architecture
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Celery Architecture

Let's look at the entire architecture.

```
                 Client

                    │

                    ▼

                FastAPI

                    │

        send_email.delay()

                    │

                    ▼

            Celery Application

                    │

                    ▼

              RabbitMQ Broker

                    │

                    ▼

             Celery Worker

                    │

                    ▼

             Python Function

                    │

                    ▼

            Result Backend
```

Every task follows this path.

______________________________________________________________________

# Components Overview

Celery consists of five major components.

```
Application

↓

Task

↓

Broker

↓

Worker

↓

Result Backend
```

Each has a different responsibility.

______________________________________________________________________

# Celery Application

The Celery Application is the central configuration object.

Think of it as

```
Brain

of

Celery
```

It knows

- Broker
- Result Backend
- Registered Tasks
- Configuration
- Serializers
- Retry Policies

Everything begins here.

______________________________________________________________________

## Example

```python
from celery import Celery

app = Celery(
    "my_app",
    broker="amqp://",
    backend="redis://"
)
```

This creates a Celery application.

______________________________________________________________________

# What Does the Application Store?

```
Celery App

├── Broker URL

├── Result Backend

├── Task Registry

├── Worker Settings

├── Serializer

├── Retry Settings

└── Queue Configuration
```

______________________________________________________________________

# Tasks

A Task is simply

a Python function

registered with Celery.

Example

```python
@app.task
def send_email(user_id):
    ...
```

Without

```python
@app.task
```

Celery doesn't know about it.

______________________________________________________________________

# Task Registration

When the application starts,

Celery scans your project.

Every

```python
@app.task
```

is registered.

```
Task Registry

↓

send_email

↓

resize_image

↓

generate_invoice

↓

send_sms
```

Workers use this registry.

______________________________________________________________________

# Broker

The Broker transports tasks.

Common Brokers

```
RabbitMQ

Redis
```

Remember

The Broker

never executes code.

It only stores and delivers messages.

______________________________________________________________________

# What Does Celery Send?

Suppose

```python
send_email.delay(101)
```

Celery doesn't send Python code.

It sends a message.

Conceptually,

```
Task Name

↓

send_email

----------------

Arguments

↓

101

----------------

Task ID

↓

UUID

----------------

Metadata
```

RabbitMQ stores this message.

______________________________________________________________________

# Worker

The Worker continuously listens.

```
RabbitMQ

↓

Worker

↓

Task Received

↓

Execute Python Function
```

Workers never stop listening.

______________________________________________________________________

# Worker Lifecycle

```
Worker Starts

↓

Connects to Broker

↓

Waits

↓

Receives Task

↓

Executes Task

↓

ACK

↓

Waits Again
```

Workers repeat this forever.

______________________________________________________________________

# Worker Processes

One Worker

can execute

multiple tasks simultaneously.

Example

```
Worker

├── Process 1

├── Process 2

├── Process 3

└── Process 4
```

Each process executes one task.

This allows parallel execution.

______________________________________________________________________

# Result Backend

Some tasks return values.

Example

```python
@app.task
def add(a, b):
    return a + b
```

Question

Where should

```
15
```

be stored?

Answer

```
Result Backend
```

______________________________________________________________________

Common Result Backends

```
Redis

Database

RPC

Memcached
```

______________________________________________________________________

# Task Lifecycle

Let's follow one task.

```
send_email.delay()
```

Step 1

```
Task Created
```

↓

Step 2

```
Serialized
```

↓

Step 3

```
Sent to RabbitMQ
```

↓

Step 4

```
Worker Receives Task
```

↓

Step 5

```
Execute Function
```

↓

Step 6

```
Store Result
```

↓

Step 7

```
ACK Broker
```

↓

Done.

______________________________________________________________________

# Serialization

RabbitMQ

cannot store Python functions.

Celery converts

```
Python Objects

↓

JSON

or

Pickle

or

YAML
```

This process is called

```
Serialization
```

Workers deserialize

before executing.

______________________________________________________________________

# Complete Flow

Suppose

```python
resize_image.delay("photo.jpg")
```

Flow

```
FastAPI

↓

Celery

↓

JSON Message

↓

RabbitMQ

↓

Worker

↓

Deserialize

↓

resize_image()

↓

Result Backend

↓

ACK
```

______________________________________________________________________

# Task States

Celery tracks task progress.

Common states include

```
PENDING

↓

RECEIVED

↓

STARTED

↓

SUCCESS
```

or

```
PENDING

↓

RECEIVED

↓

STARTED

↓

FAILURE
```

______________________________________________________________________

# PENDING

Task exists,

but hasn't been executed.

```
RabbitMQ

↓

Waiting
```

______________________________________________________________________

# RECEIVED

Worker accepted the task.

```
RabbitMQ

↓

Worker
```

Task hasn't started yet.

______________________________________________________________________

# STARTED

Worker is executing

the function.

______________________________________________________________________

# SUCCESS

Task completed successfully.

Result stored

(if a Result Backend exists).

______________________________________________________________________

# FAILURE

Task crashed.

Celery stores

- Exception
- Stack Trace
- Error Details

Useful for debugging.

______________________________________________________________________

# RETRY

Suppose

```
SMTP Server

↓

Offline
```

Worker says

```
Retry Later
```

Task enters

```
RETRY
```

state.

______________________________________________________________________

# REVOKED

Sometimes

we cancel tasks.

```
Pending Task

↓

Cancelled
```

Celery marks

```
REVOKED
```

______________________________________________________________________

# Task Flow Diagram

```
PENDING

↓

RECEIVED

↓

STARTED

↓

SUCCESS
```

or

```
PENDING

↓

RECEIVED

↓

STARTED

↓

RETRY

↓

SUCCESS
```

or

```
PENDING

↓

RECEIVED

↓

STARTED

↓

FAILURE
```

______________________________________________________________________

# Production Architecture

Imagine

```
FastAPI

↓

RabbitMQ

↓

Worker 1

Worker 2

Worker 3

Worker 4

↓

Redis Result Backend
```

Every worker

shares

- Broker
- Result Backend

Tasks are distributed automatically.

______________________________________________________________________

# Why Separate Workers?

Suppose

```
Video Encoding

30 Seconds
```

Email Sending

```
100 ms
```

Don't use

the same worker pool.

Instead

```
Email Queue

↓

Email Workers

------------------

Video Queue

↓

Video Workers
```

Better scalability.

______________________________________________________________________

# Summary

A Celery application consists of

- Application
- Tasks
- Broker
- Workers
- Result Backend

Tasks are serialized,

transported through RabbitMQ,

executed by Workers,

and optionally stored in a Result Backend.

Understanding this lifecycle is essential for debugging and designing production systems.

______________________________________________________________________

# Key Takeaways

- The Celery Application manages configuration.
- Tasks are registered Python functions.
- RabbitMQ transports serialized task messages.
- Workers execute tasks.
- Result Backends store task states and return values.
- Tasks move through several execution states.
- Workers deserialize tasks before execution.
- Multiple Worker processes enable parallelism.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### What are the core components of Celery?

#### Answer

Celery consists of the Application, Tasks, Broker, Workers, and an optional Result Backend. Together they enable
asynchronous task execution.

______________________________________________________________________

## Question 2

### What happens internally when `task.delay()` is called?

#### Answer

Celery serializes the task name, arguments, and metadata into a message, publishes it to the configured Broker, and
returns immediately. A Worker later consumes the message, deserializes it, executes the task, optionally stores the
result, and acknowledges the message.

______________________________________________________________________

## Question 3

### Why is serialization required?

#### Answer

RabbitMQ cannot store Python functions directly. Celery serializes task information into formats such as JSON before
sending it to the Broker. Workers deserialize the message before execution.

______________________________________________________________________

## Question 4

### What is the purpose of the Result Backend?

#### Answer

The Result Backend stores task states and optional return values, allowing applications to query whether tasks are
pending, running, successful, failed, or retried.

______________________________________________________________________

## Question 5

### What are the common Celery task states?

#### Answer

Common task states include PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, and REVOKED.

______________________________________________________________________

## Question 6

### Why should long-running and short-running tasks use different Workers?

#### Answer

Separate Worker pools prevent long-running tasks from blocking short tasks, improve resource utilization, and allow
independent scaling of different workloads.

______________________________________________________________________

## Question 7

### Does RabbitMQ execute Celery tasks?

#### Answer

No. RabbitMQ only transports task messages. Celery Workers execute the actual Python functions.

______________________________________________________________________

# Practice Questions

1. Explain the Celery architecture.
1. What is the Celery Application?
1. What happens during task registration?
1. Why is serialization required?
1. Explain the role of the Broker.
1. Explain the Worker lifecycle.
1. What is a Result Backend?
1. List the common task states.
1. Explain the complete task lifecycle.
1. Why should different workloads use different Worker pools?

______________________________________________________________________

# Mini Assignment

Design the Celery architecture for a video-sharing platform.

Tasks include:

- Generate thumbnails
- Encode videos
- Scan for malware
- Notify subscribers
- Update recommendations
- Generate AI captions

For each task, determine:

- Queue
- Worker Pool
- Broker
- Result Backend requirement
- Expected task state transitions

Draw the complete architecture using ASCII diagrams.

______________________________________________________________________

# Common Mistakes

❌ Thinking RabbitMQ executes tasks.

❌ Forgetting to register tasks with `@app.task`.

❌ Using one Worker pool for every type of workload.

❌ Assuming Result Backends are mandatory.

❌ Returning large objects from tasks unnecessarily.

❌ Ignoring task state monitoring.

______________________________________________________________________

# What's Next?

Now that you understand Celery's internal architecture, we'll start writing real Celery code.

In the next chapter, we'll cover:

- Creating Celery applications
- Defining tasks
- Starting Workers
- Sending tasks
- Task execution
- Logging
- Folder structure
- First production-ready Celery project

➡ **Next File:** [File 15 – Creating Your First Celery Application](15-first-celery-app.md)
