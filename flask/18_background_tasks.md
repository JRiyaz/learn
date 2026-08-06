# Background Tasks with Celery

> **Course:** Flask for Backend Engineers
>
> **Module:** 8
>
> **File:** `18_background_tasks.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Background Tasks are
- Why Background Tasks are Needed
- Synchronous vs Asynchronous Processing
- Celery
- Message Brokers
- Redis vs RabbitMQ
- Task Lifecycle
- Periodic Tasks
- Retries
- Task Monitoring
- Production Best Practices

______________________________________________________________________

# Why Background Tasks?

Imagine a user places an order.

Your application needs to:

- Save Order
- Send Email
- Generate Invoice
- Notify Warehouse
- Resize Images

If everything runs during the request,

```
User

↓

Waits

↓

8 Seconds
```

Poor user experience.

______________________________________________________________________

# Better Approach

```
User

↓

Create Order

↓

Response

200 ms

↓

Background Worker

↓

Email

↓

Invoice

↓

Notifications
```

The user gets a fast response.

______________________________________________________________________

# Synchronous Processing

```
Request

↓

Task 1

↓

Task 2

↓

Task 3

↓

Response
```

The client waits for every task to finish.

______________________________________________________________________

# Asynchronous Processing

```
Request

↓

Save Data

↓

Queue Task

↓

Response

↓

Worker

↓

Execute Tasks
```

The long-running work happens later.

______________________________________________________________________

# What Should Run in Background?

Examples

- Sending emails
- PDF generation
- Video processing
- Image resizing
- Report generation
- Payment notifications
- Data synchronization
- Scheduled jobs

______________________________________________________________________

# What is Celery?

Celery is a distributed task queue for Python.

Responsibilities

- Execute background jobs
- Retry failed jobs
- Schedule periodic tasks
- Distribute work across workers

______________________________________________________________________

# Celery Architecture

```
Flask

↓

Message Broker

↓

Celery Worker

↓

Task
```

Flask publishes tasks.

Workers execute them.

______________________________________________________________________

# Components

```
Application

↓

Celery

↓

Broker

↓

Worker

↓

Result Backend (Optional)
```

______________________________________________________________________

# Message Broker

Celery requires a broker.

Common choices

- Redis
- RabbitMQ

The broker stores tasks until workers process them.

______________________________________________________________________

# Redis vs RabbitMQ

| Redis | RabbitMQ |
|--------|----------|
| Simple setup | Rich messaging features |
| Very fast | Advanced routing |
| Great for many applications | Better for complex messaging patterns |
| Can also be used as a cache | Dedicated message broker |

Both are widely used with Celery.

______________________________________________________________________

# Install Celery

```bash
pip install celery
```

Redis support

```bash
pip install redis
```

______________________________________________________________________

# Basic Celery App

```python
from celery import Celery

celery = Celery(

    "tasks",

    broker="redis://localhost:6379/0"
)
```

______________________________________________________________________

# Create a Task

```python
@celery.task

def send_email(

    user_id

):

    print(

        f"Email sent to {user_id}"

    )
```

______________________________________________________________________

# Execute Task

```python
send_email.delay(

    user.id
)
```

`.delay()` sends the task to the broker.

The request returns immediately.

______________________________________________________________________

# Task Flow

```
Flask

↓

delay()

↓

Redis

↓

Worker

↓

Execute Task
```

______________________________________________________________________

# Running a Worker

Example

```bash
celery -A app.celery worker --loglevel=info
```

The worker continuously listens for new tasks.

______________________________________________________________________

# Task States

```
PENDING

↓

STARTED

↓

SUCCESS
```

or

```
PENDING

↓

FAILURE
```

______________________________________________________________________

# Retries

Sometimes external systems fail.

Example

```
Email Service

↓

Timeout
```

Retry.

```python
@celery.task(

    autoretry_for=(Exception,),

    retry_backoff=True,

    max_retries=5
)
```

Automatic retries improve resilience.

______________________________________________________________________

# Scheduled Tasks

Examples

- Daily Reports
- Cleanup Jobs
- Email Digests

Celery Beat schedules recurring tasks.

______________________________________________________________________

# Celery Beat

Architecture

```
Celery Beat

↓

Broker

↓

Worker

↓

Task
```

Beat publishes tasks on a schedule.

Workers execute them.

______________________________________________________________________

# Example Schedule

```
Every Day

↓

08:00 AM

↓

Generate Report
```

______________________________________________________________________

# Passing Arguments

```python
send_email.delay(

    user_id=10
)
```

Arguments are serialized and sent through the broker.

______________________________________________________________________

# Returning Results

```python
@celery.task

def add(a, b):

    return a + b
```

Execute

```python
result = add.delay(2, 3)
```

Read later

```python
result.get()
```

In many production systems, tasks are designed for side effects (emails, notifications, etc.), so retrieving results is
often unnecessary.

______________________________________________________________________

# Idempotent Tasks

Tasks may be retried.

Bad

```
Charge Credit Card

↓

Retry

↓

Charge Again
```

Good

```
Check

Already Charged?

↓

If No

↓

Charge
```

Design tasks to be idempotent whenever possible.

______________________________________________________________________

# Task Time Limits

Prevent tasks from running forever.

Example

```python
@celery.task(

    soft_time_limit=30
)
```

______________________________________________________________________

# Monitoring

Common tools

- Flower
- Prometheus
- Grafana

Flower provides a web UI for Celery.

______________________________________________________________________

# Logging

Every task should log

- Start
- Success
- Failure
- Retry

This simplifies troubleshooting.

______________________________________________________________________

# Error Handling

```python
try:

    ...

except Exception:

    logger.exception(

        "Task Failed"

    )

    raise
```

Allow Celery to detect failures and apply retry policies when appropriate.

______________________________________________________________________

# Architecture

```
Client

↓

Flask API

↓

Database

↓

Queue Task

↓

Redis

↓

Celery Worker

↓

Email Service
```

The request finishes before the email is sent.

______________________________________________________________________

# Production Deployment

Typical setup

```
Nginx

↓

Gunicorn

↓

Flask

↓

Redis

↓

Celery Workers

↓

Celery Beat
```

Each component scales independently.

______________________________________________________________________

# Common Mistakes

❌ Running long tasks inside request handlers

❌ Using background tasks for very small operations

❌ Forgetting retries

❌ Not monitoring workers

❌ Designing non-idempotent tasks

❌ Blocking on `result.get()` inside request handlers

______________________________________________________________________

# Production Best Practices

- Move long-running work to Celery.
- Keep tasks idempotent.
- Configure retries for transient failures.
- Monitor workers.
- Log task execution.
- Use Redis or RabbitMQ as a broker.
- Use Celery Beat for scheduled jobs.
- Set reasonable task time limits.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should long-running operations be moved to Celery instead of executing inside Flask request handlers?**

### Answer

Executing long-running operations inside request handlers increases response times and ties up web server resources.

Using Celery allows Flask to:

1. Return responses quickly.
1. Improve user experience.
1. Scale web servers independently from workers.
1. Retry failed operations.
1. Execute scheduled jobs.
1. Process work asynchronously.

This architecture improves both scalability and reliability.

______________________________________________________________________

# Summary

In this chapter you learned:

- Background Tasks
- Celery
- Message Brokers
- Redis
- RabbitMQ
- Workers
- Retries
- Celery Beat
- Monitoring
- Production Architecture

Background task processing is an essential capability for production systems because it keeps APIs responsive while
handling long-running operations asynchronously.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What are background tasks?
1. Why shouldn't long-running work execute inside Flask request handlers?
1. What is Celery?

______________________________________________________________________

## Architecture

4. What is the role of a message broker?
1. What is the difference between Redis and RabbitMQ?
1. What does a Celery worker do?
1. What is Celery Beat?

______________________________________________________________________

## Tasks

8. What does `.delay()` do?
1. Why should background tasks be idempotent?
1. Why are retries important?

______________________________________________________________________

## Production

11. Why should workers be monitored?
01. Why should tasks have time limits?
01. Why is logging important for background jobs?

______________________________________________________________________

## Scenario-Based

14. Your `/checkout` endpoint takes 12 seconds because it generates invoices and sends emails before returning a response. How would you redesign it?
01. A Celery task charges a customer's credit card and is automatically retried after a timeout. What design changes would prevent duplicate charges?
01. Your Celery workers stop processing tasks because Redis becomes unavailable. What happens to newly submitted tasks, and what operational considerations should you have?
01. A developer calls `result.get()` immediately after `task.delay()` inside a Flask route. Why does this reduce the benefit of asynchronous processing?
01. Your application needs to generate a daily sales report every morning at 8:00 AM. Which Celery component would you use and why?

______________________________________________________________________

# Next

[Deploying Flask with Gunicorn & Nginx](19_deployment_gunicorn_nginx.md)
