# Background Tasks

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 6 - Background Processing
>
> **File:** `25_background_tasks.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Background Tasks are
- Why Background Tasks are Needed
- How `BackgroundTasks` Works
- Adding Background Tasks
- Passing Arguments
- Multiple Background Tasks
- Limitations
- Background Tasks vs Celery
- Production Best Practices

______________________________________________________________________

# What are Background Tasks?

Sometimes an API should return a response immediately,

while performing additional work **after** the response is sent.

Example

```
Create User

↓

Return 201

↓

Send Welcome Email
```

The client doesn't need to wait for the email.

______________________________________________________________________

# Why Use Background Tasks?

Without background tasks

```
Request

↓

Create User

↓

Send Email

↓

Generate Report

↓

Response
```

Slow response.

With background tasks

```
Request

↓

Create User

↓

Response

↓

Email

↓

Logging

↓

Notifications
```

Much faster for the client.

______________________________________________________________________

# Common Use Cases

Background tasks are useful for

- Sending Emails
- Writing Audit Logs
- Updating Analytics
- Cache Refresh
- Notifications
- Webhooks
- Temporary File Cleanup
- Image Thumbnail Generation (small workloads)

______________________________________________________________________

# How BackgroundTasks Works

FastAPI provides

```python
BackgroundTasks
```

Import

```python
from fastapi import BackgroundTasks
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI

from fastapi import BackgroundTasks

app = FastAPI()

def send_email(

    email: str

):

    print(

        f"Email sent to {email}"

    )

@app.post("/users")

def create_user(

    background_tasks:

    BackgroundTasks

):

    background_tasks.add_task(

        send_email,

        "user@example.com"

    )

    return {

        "message":

        "User created"

    }
```

______________________________________________________________________

# Execution Flow

```
Request

↓

Route

↓

add_task()

↓

Response Sent

↓

Background Task Runs
```

The client receives the response before the task executes.

______________________________________________________________________

# Internal Flow

```
HTTP Request

↓

Route

↓

Register Task

↓

Response

↓

Execute Task
```

The task runs in the same application process after the response is returned.

______________________________________________________________________

# Passing Arguments

Example

```python
background_tasks.add_task(

    send_email,

    email,

    username
)
```

Equivalent to

```python
send_email(

    email,

    username
)
```

executed later.

______________________________________________________________________

# Multiple Tasks

```python
background_tasks.add_task(

    send_email,

    email
)

background_tasks.add_task(

    write_log,

    username
)

background_tasks.add_task(

    update_metrics
)
```

Tasks execute after the response has been sent.

______________________________________________________________________

# Example Flow

```
Response

↓

Email

↓

Log Entry

↓

Metrics Update
```

______________________________________________________________________

# Using File Operations

Example

```python
def cleanup(

    filename: str

):

    os.remove(

        filename
    )
```

After generating a downloadable file,

schedule cleanup as a background task.

______________________________________________________________________

# Logging Example

```python
def audit(

    username: str

):

    print(

        "Audit:",

        username
    )
```

```python
background_tasks.add_task(

    audit,

    username
)
```

Useful for audit trails.

______________________________________________________________________

# Notification Example

```
Order Created

↓

Response

↓

Send SMS

↓

Send Email

↓

Push Notification
```

The user doesn't wait for notifications.

______________________________________________________________________

# Background Task Lifecycle

```
Client

↓

Request

↓

Route

↓

Response

↓

Background Tasks

↓

Finished
```

______________________________________________________________________

# Error Handling

If a background task raises an exception,

the client has **already received** the response.

Therefore,

background tasks should

- Handle errors
- Log failures
- Retry when appropriate (if implemented externally)

______________________________________________________________________

# Async Tasks

Both synchronous and asynchronous callables can be used.

Example

```python
async def notify(

    email: str

):

    ...
```

or

```python
def notify(

    email: str

):

    ...
```

FastAPI handles both appropriately.

______________________________________________________________________

# Limitations

Background tasks

- Run inside the FastAPI process.
- Are not distributed.
- Do not survive process crashes or restarts.
- Are not designed for long-running jobs.

______________________________________________________________________

# BackgroundTasks vs Celery

| BackgroundTasks | Celery |
|-----------------|--------|
| Built into FastAPI | External system |
| Same Process | Separate Workers |
| Simple Setup | Requires Broker |
| Lightweight Tasks | Long-running Jobs |
| No Retry System | Retry Support |
| No Task Queue | Distributed Queue |

______________________________________________________________________

# When to Use BackgroundTasks

Good choices

- Email notifications
- Logging
- Cache updates
- Short cleanup tasks

Avoid for

- Video processing
- Machine Learning inference
- Large report generation
- Batch processing
- Long-running workflows

______________________________________________________________________

# When to Use Celery

Use Celery (or a similar task queue) when you need

- Multiple workers
- Task retries
- Scheduling
- Long-running jobs
- Distributed execution
- Fault tolerance

______________________________________________________________________

# Production Architecture

```
Client

↓

FastAPI

↓

Response

↓

Background Task
```

Larger systems

```
Client

↓

FastAPI

↓

Message Broker

↓

Celery Worker

↓

Task
```

______________________________________________________________________

# Common Mistakes

❌ Running CPU-intensive work in `BackgroundTasks`

❌ Assuming background tasks survive application crashes

❌ Performing very long-running operations

❌ Ignoring task failures

❌ Using background tasks as a replacement for a real task queue

______________________________________________________________________

# Production Best Practices

- Keep background tasks short.
- Log task failures.
- Use them only for lightweight work.
- Move heavy processing to Celery or another worker system.
- Avoid blocking operations when possible.
- Make tasks idempotent if they may be retried externally.

______________________________________________________________________

# Interview Deep Dive

### Question

**When should you use FastAPI `BackgroundTasks` instead of Celery?**

### Answer

Use **`BackgroundTasks`** for lightweight operations that should execute after the response is returned, such as:

- Sending emails
- Writing logs
- Updating metrics
- Cleaning temporary files

Use **Celery** when tasks require:

- Distributed execution
- Retries
- Scheduling
- Long-running processing
- Fault tolerance
- Worker scalability

`BackgroundTasks` improves response time but is not a replacement for a full task queue.

______________________________________________________________________

# Summary

In this chapter you learned:

- Background Tasks
- `BackgroundTasks`
- Adding Tasks
- Passing Arguments
- Multiple Tasks
- Error Handling
- Limitations
- BackgroundTasks vs Celery
- Production Best Practices

Background tasks allow FastAPI applications to perform lightweight work after sending the response, improving
responsiveness without introducing a full distributed task queue.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What are background tasks?
1. Why are background tasks useful?
1. When are background tasks executed?

______________________________________________________________________

## FastAPI

4. How do you create a background task?
1. How do you pass arguments to a background task?
1. Can multiple background tasks be scheduled in one request?

______________________________________________________________________

## Architecture

7. Why do background tasks improve API response time?
1. Why do background tasks run after the response is sent?
1. What happens if a background task fails?

______________________________________________________________________

## Comparison

10. What are the differences between `BackgroundTasks` and Celery?
01. Why isn't `BackgroundTasks` suitable for long-running jobs?
01. When should Celery be preferred?

______________________________________________________________________

## Production

13. Why should background tasks remain lightweight?
01. Why should background task failures be logged?
01. Why don't background tasks provide fault tolerance?

______________________________________________________________________

## Scenario-Based

16. Your registration endpoint sends a welcome email before returning a response, causing a noticeable delay. How could `BackgroundTasks` improve the user experience?
01. Your application generates 500-page PDF reports that take several minutes to complete. Would `BackgroundTasks` or Celery be more appropriate? Why?
01. A background task crashes while sending an email, but the client has already received HTTP 201. How should the application handle this situation?
01. Your application needs automatic retries when a third-party email service is temporarily unavailable. Why is Celery a better fit than `BackgroundTasks`?
01. Your team starts using `BackgroundTasks` for CPU-intensive video transcoding jobs. What scalability and reliability problems are likely to appear?

______________________________________________________________________

# Next

[Dependency Injection](26_dependency_injection.md)
