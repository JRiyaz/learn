# Celery Masterclass for Backend Engineers

## File 15 – Creating Your First Celery Application

> **Course Level:** Intermediate → Advanced
>
> So far we've learned the theory behind Celery.
>
> Now it's time to build a real application.
>
> In this chapter, you'll learn how to:
>
> - Install Celery
> - Configure RabbitMQ
> - Create tasks
> - Run workers
> - Submit background jobs
> - Understand what happens internally
>
> This is the first chapter where we'll write production-style code.

______________________________________________________________________

# Learning Objectives

By the end of this chapter, you will be able to:

- Install Celery.
- Configure RabbitMQ as the broker.
- Create a Celery application.
- Write Celery tasks.
- Start Workers.
- Submit asynchronous tasks.
- Understand project structure.
- Debug common startup issues.

______________________________________________________________________

# Table of Contents

1. Project Architecture
1. Installing RabbitMQ
1. Installing Celery
1. Project Structure
1. Creating the Celery Application
1. Creating Tasks
1. Starting RabbitMQ
1. Starting Workers
1. Sending Tasks
1. Complete Task Flow
1. Common Errors
1. Best Practices
1. Summary
1. Key Takeaways
1. Interview Deep Dive
1. Practice Questions
1. Mini Assignment
1. Common Mistakes
1. What's Next?

______________________________________________________________________

# Project Architecture

We'll build the following system.

```
                FastAPI

                    │

      send_email.delay()

                    │

                    ▼

             RabbitMQ Broker

                    │

                    ▼

              Celery Worker

                    │

                    ▼

             send_email()
```

The API creates tasks.

RabbitMQ transports them.

Workers execute them.

______________________________________________________________________

# Step 1 — Install RabbitMQ

If RabbitMQ is already running,

you can skip this section.

Using Docker

```bash
docker run -d \
  --hostname rabbitmq \
  --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:management
```

Management UI

```
http://localhost:15672
```

Broker Port

```
5672
```

______________________________________________________________________

# Step 2 — Install Celery

```bash
pip install celery
```

Verify

```bash
celery --version
```

Example

```
5.x.x
```

______________________________________________________________________

# Step 3 — Project Structure

A clean project layout.

```
project/

│

├── app/

│   ├── __init__.py

│   ├── celery_app.py

│   ├── tasks.py

│   └── main.py

│

├── requirements.txt

│

└── README.md
```

As applications grow,

split tasks into multiple modules.

______________________________________________________________________

# Step 4 — Create the Celery Application

Create

```
app/celery_app.py
```

```python
from celery import Celery

celery = Celery(
    "my_app",
    broker="amqp://guest:guest@localhost:5672//"
)
```

This tells Celery

where RabbitMQ is running.

______________________________________________________________________

# Broker URL Format

RabbitMQ

```
amqp://

↓

username

↓

password

↓

host

↓

port

↓

virtual host
```

Example

```
amqp://guest:guest@localhost:5672//
```

Production usually uses

non-default credentials.

______________________________________________________________________

# Step 5 — Create Tasks

Create

```
app/tasks.py
```

```python
from app.celery_app import celery

@celery.task
def send_email(email):
    print(f"Sending email to {email}")
```

The decorator

```python
@celery.task
```

registers the function.

Without it,

Workers won't recognize the task.

______________________________________________________________________

# Step 6 — Another Task

```python
from app.celery_app import celery

@celery.task
def add(a, b):
    return a + b
```

Any Python function

can become a Celery task,

provided its arguments are serializable.

______________________________________________________________________

# Step 7 — Start RabbitMQ

If using Docker

```bash
docker start rabbitmq
```

Verify

```bash
docker ps
```

RabbitMQ should appear.

______________________________________________________________________

# Step 8 — Start a Worker

Run

```bash
celery -A app.celery_app worker --loglevel=info
```

Explanation

```
-A

Application
```

```
worker

Start Worker
```

```
--loglevel

Logging verbosity
```

Worker output

```
Connected to amqp://...

Ready.
```

Now the Worker is listening.

______________________________________________________________________

# Step 9 — Send a Task

Open Python shell

```python
from app.tasks import send_email

send_email.delay("alice@example.com")
```

Immediately,

the function returns.

The email isn't executed here.

Instead,

RabbitMQ receives

```
Task

↓

send_email

↓

alice@example.com
```

______________________________________________________________________

# What Happens Internally?

Let's trace the request.

```
send_email.delay()

↓

Celery

↓

Serialize Task

↓

RabbitMQ

↓

Worker

↓

Deserialize

↓

send_email()

↓

ACK
```

Everything happens asynchronously.

______________________________________________________________________

# Another Example

```python
from app.tasks import add

result = add.delay(10, 20)
```

Immediately

```
result

↓

AsyncResult
```

Not

```
30
```

The task is still executing.

______________________________________________________________________

# Task IDs

Every task receives

a unique identifier.

Example

```
Task ID

↓

5d7f09c2...

```

Useful for

- logging
- monitoring
- debugging
- querying task status

______________________________________________________________________

# AsyncResult

Suppose

```python
result = add.delay(5, 7)
```

Celery returns

```python
AsyncResult
```

Example

```python
print(result.id)
```

Output

```
7c3e...

```

Task IDs uniquely identify each task.

______________________________________________________________________

# Checking Task State

Example

```python
print(result.status)
```

Possible output

```
PENDING
```

Later

```
SUCCESS
```

Or

```
FAILURE
```

Without a Result Backend,

state tracking is limited.

______________________________________________________________________

# Returning Values

Task

```python
@celery.task
def multiply(a, b):
    return a * b
```

Later,

if a Result Backend is configured,

```
multiply.delay(5, 4)

↓

20
```

can be retrieved.

______________________________________________________________________

# Running Multiple Tasks

```python
send_email.delay(...)

send_sms.delay(...)

resize_image.delay(...)

generate_invoice.delay(...)
```

All tasks are independent.

Workers execute them concurrently.

______________________________________________________________________

# Folder Organization (Production)

Instead of

```
tasks.py
```

use

```
tasks/

├── email.py

├── payment.py

├── reports.py

├── analytics.py

└── notifications.py
```

Much easier to maintain.

______________________________________________________________________

# Logging

Avoid

```python
print()
```

Instead

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Email sent")
```

Structured logging is essential for production debugging.

______________________________________________________________________

# Common Startup Errors

## RabbitMQ Not Running

Worker logs

```
Connection Refused
```

Solution

Start RabbitMQ.

______________________________________________________________________

## Wrong Broker URL

Worker logs

```
Authentication Failed
```

Solution

Check username,

password,

host,

and port.

______________________________________________________________________

## Task Not Registered

Worker logs

```
Received unregistered task
```

Solution

Ensure the task module is imported and decorated with `@celery.task`.

______________________________________________________________________

## Wrong Application Path

Command

```bash
celery -A wrong.path worker
```

Result

```
Module Not Found
```

Verify the `-A` argument points to the correct Celery application.

______________________________________________________________________

# Best Practices

✔ Use one Celery application.

✔ Keep tasks small.

✔ Make tasks idempotent.

✔ Organize tasks into modules.

✔ Use logging instead of print statements.

✔ Run multiple Workers in production.

✔ Secure RabbitMQ credentials.

______________________________________________________________________

# Summary

A Celery application consists of

- A Celery application object
- Registered tasks
- RabbitMQ as the broker
- Workers that execute tasks

Calling `.delay()` creates a task message,

RabbitMQ stores it,

and a Worker executes it asynchronously.

This pattern allows APIs to remain fast while heavy work happens in the background.

______________________________________________________________________

# Key Takeaways

- Install Celery separately from RabbitMQ.
- Define one Celery application.
- Register tasks using `@celery.task`.
- Start Workers with the Celery CLI.
- `.delay()` sends a task asynchronously.
- Workers execute tasks independently.
- Use structured logging.
- Organize tasks by domain.

______________________________________________________________________

# Interview Deep Dive

## Question 1

### How do you create a Celery application?

#### Answer

Create a `Celery` object with a name and a Broker configuration. This application manages task registration,
configuration, and communication with the message broker.

______________________________________________________________________

## Question 2

### What does `.delay()` do?

#### Answer

`.delay()` serializes the task name and arguments, sends them to the configured Broker, and immediately returns an
`AsyncResult` object without executing the task synchronously.

______________________________________________________________________

## Question 3

### Why doesn't `.delay()` return the task result immediately?

#### Answer

Because task execution happens asynchronously in a separate Worker process. `.delay()` only schedules the task and
returns immediately.

______________________________________________________________________

## Question 4

### What is `AsyncResult`?

#### Answer

`AsyncResult` is a handle to a submitted task. It contains the task ID and can be used to check task status or retrieve
results when a Result Backend is configured.

______________________________________________________________________

## Question 5

### Why is `@celery.task` required?

#### Answer

The decorator registers the function with the Celery application so Workers can discover and execute it when task
messages arrive.

______________________________________________________________________

## Question 6

### What causes a "Received unregistered task" error?

#### Answer

This occurs when the Worker has not imported the module containing the task or when the function is missing the
`@celery.task` decorator.

______________________________________________________________________

## Question 7

### How do Workers discover tasks?

#### Answer

Workers load the Celery application, import registered task modules, build a task registry, and match incoming task
names from the Broker to registered Python functions.

______________________________________________________________________

# Practice Questions

1. Explain the project structure of a Celery application.
1. What is the purpose of the Celery application object?
1. What happens internally when `.delay()` is called?
1. Explain the Broker URL.
1. Why is the `@celery.task` decorator required?
1. What is an `AsyncResult`?
1. How are task IDs used?
1. Why should logging be used instead of `print()`?
1. Explain how Workers execute tasks.
1. What are common startup errors?

______________________________________________________________________

# Mini Assignment

Build a simple Celery application with the following tasks:

- Send welcome email
- Resize image
- Generate invoice
- Export CSV report
- Send SMS notification

For each task, explain:

- Input parameters
- Expected output
- Whether a Result Backend is required
- Retry requirements
- Whether the task is CPU-bound or I/O-bound

Also design a clean folder structure for the project.

______________________________________________________________________

# Common Mistakes

❌ Forgetting to start RabbitMQ before Workers.

❌ Running Workers with the wrong `-A` path.

❌ Missing the `@celery.task` decorator.

❌ Using `print()` instead of logging.

❌ Returning huge objects from tasks.

❌ Placing every task in one giant `tasks.py` file.

______________________________________________________________________

# What's Next?

Now that you've built your first Celery application, it's time to learn the APIs you'll use every day.

The next chapter covers:

- `.delay()`
- `.apply_async()`
- Task options
- ETA
- Countdown
- Expiration
- Routing
- Serialization
- Task priorities

➡ **Next File:** [File 16 – Sending Tasks, apply_async() & Task Options](16-task-options.md)
