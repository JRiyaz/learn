# File: python/56-production-python-part-01-logging.md

# Production Python

# Part 1: Logging – Building Observable Python Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 56
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why logging is essential in production systems
- Why `print()` should not be used for debugging production applications
- The architecture of Python's `logging` module
- Loggers
- Handlers
- Formatters
- Log levels
- Log propagation
- Logger hierarchy
- Logging configuration
- Structured logging concepts
- Logging best practices
- Production patterns
- questions

______________________________________________________________________

# Recap

As developers, one of the first debugging tools we learn is:

```python
print("Reached here")
```

This is useful during learning, but it becomes a serious limitation in production.

Imagine a backend service handling:

- 10,000 requests per minute
- 20 worker processes
- Multiple threads or asyncio tasks

How would you answer questions like:

- Why did a request fail?
- Which user was affected?
- How long did the database query take?
- Which server processed the request?

`print()` cannot answer these questions.

Production systems require **logging**.

______________________________________________________________________

# Why Logging Exists

Logs provide a historical record of what an application did.

Typical information includes:

- Application startup
- Incoming requests
- Database operations
- Authentication events
- Business events
- Errors
- Performance metrics
- Shutdown events

Without logs, diagnosing production problems becomes extremely difficult.

______________________________________________________________________

# `print()` vs Logging

Consider:

```python
print("User created")
```

Problems:

- No timestamp
- No severity level
- No module information
- Cannot filter messages
- Difficult to redirect
- Difficult to search

Now compare:

```python
import logging

logging.info("User created")
```

A logging system can include:

- Timestamp
- Log level
- Logger name
- Process ID
- Thread name
- Module
- Message

______________________________________________________________________

# Logging Architecture

Python's logging framework consists of several components.

```
Application

↓

Logger

↓

Log Record

↓

Handler

↓

Formatter

↓

Destination
```

A destination might be:

- Console
- File
- Syslog
- Cloud logging service
- Elasticsearch
- Splunk

______________________________________________________________________

# Creating a Logger

```python
import logging

logger = logging.getLogger(__name__)
```

Why `__name__`?

It creates a hierarchical logger based on the module name.

Example:

```text
app.api.users
```

or

```text
app.services.orders
```

This hierarchy makes large applications much easier to manage.

______________________________________________________________________

# Log Levels

Python defines standard severity levels.

| Level | Purpose |
|--------|---------|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | Normal application events |
| `WARNING` | Unexpected but recoverable situations |
| `ERROR` | An operation failed |
| `CRITICAL` | Serious failure threatening application stability |

______________________________________________________________________

# Example

```python
logger.debug("SQL query started.")

logger.info("User logged in.")

logger.warning("Cache miss.")

logger.error("Database unavailable.")

logger.critical("Payment system unavailable.")
```

Choosing the correct level is important because operations teams often filter logs by severity.

______________________________________________________________________

# Basic Configuration

```python
import logging

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(name)s %(message)s"

)

logger = logging.getLogger(__name__)
```

Example output:

```text
2026-07-26 10:15:42 INFO app.users User created successfully
```

______________________________________________________________________

# Handlers

A logger emits records.

Handlers decide where they go.

Example:

```
Logger

↓

ConsoleHandler

↓

Terminal
```

or

```
Logger

↓

FileHandler

↓

application.log
```

A single logger can have multiple handlers.

______________________________________________________________________

# Formatters

Formatters control how a log message appears.

Example format string:

```python
"%(asctime)s %(levelname)s %(name)s %(message)s"
```

Common fields include:

- `asctime`
- `levelname`
- `name`
- `filename`
- `lineno`
- `process`
- `threadName`
- `message`

______________________________________________________________________

# Logger Hierarchy

Suppose your project contains:

```text
app
├── api
├── services
└── repositories
```

Each module can create its own logger:

```python
logging.getLogger(__name__)
```

Resulting hierarchy:

```
app

├── app.api

├── app.services

└── app.repositories
```

Configuration can be applied at the root and inherited by child loggers.

______________________________________________________________________

# Propagation

By default, log records propagate up the logger hierarchy.

```
app.services.user

↓

app.services

↓

app

↓

Root Logger
```

This usually means you configure logging once at application startup rather than in every module.

______________________________________________________________________

# Logging Exceptions

Instead of:

```python
logger.error("Database failed.")
```

use:

```python
try:
    ...
except Exception:

    logger.exception("Database operation failed.")
```

`logger.exception()` automatically includes the traceback, making debugging much easier.

______________________________________________________________________

# Structured Logging

Instead of writing human-only messages:

```text
User created.
```

prefer structured information:

```text
user_id=123 action=create_user
```

This makes logs easier to search and analyse.

Modern logging systems index structured fields for querying and dashboards.

______________________________________________________________________

# What Should Be Logged?

Good candidates:

- Application startup
- Shutdown
- Incoming requests
- Authentication
- External API calls
- Database failures
- Business events
- Retry attempts
- Unexpected exceptions

Avoid logging:

- Passwords
- API secrets
- Authentication tokens
- Credit card numbers
- Personally identifiable information unless strictly necessary

______________________________________________________________________

# Production Example

A request reaches a FastAPI service.

```
Request Received

↓

Authenticate User

↓

Query PostgreSQL

↓

Call Redis

↓

Call Payment API

↓

Return Response
```

Each stage emits logs with:

- Request ID
- User ID (if appropriate)
- Duration
- Outcome

This allows engineers to reconstruct the lifecycle of a request.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using `print()` instead of logging.

______________________________________________________________________

## Mistake 2

Logging the same exception multiple times.

______________________________________________________________________

## Mistake 3

Logging sensitive information.

______________________________________________________________________

## Mistake 4

Using the wrong log level.

______________________________________________________________________

## Mistake 5

Creating a new logger inside every function.

Create one logger per module instead.

______________________________________________________________________

# Best Practices

✅ Create loggers using `logging.getLogger(__name__)`.

✅ Configure logging once during application startup.

✅ Use meaningful log levels.

✅ Log exceptions with `logger.exception()`.

✅ Include contextual information such as request IDs.

❌ Don't log secrets.

❌ Don't use logging as a replacement for exception handling.

______________________________________________________________________

# Production Insight

In mature backend systems, logs are one pillar of **observability**, alongside:

- Metrics
- Traces
- Health checks

Logging tells you **what happened**, metrics tell you **how often**, and traces show **where time was spent**. Together,
they make production systems diagnosable and operable at scale.

______________________________________________________________________

# Questions

### Question

> Why shouldn't production applications use `print()` for logging?

### Answer

Because `print()` lacks severity levels, timestamps, structured formatting, filtering, and configurable destinations.

______________________________________________________________________

### Question

> Why use `logging.getLogger(__name__)`?

### Answer

It creates a hierarchical logger tied to the current module, allowing central configuration and fine-grained control.

______________________________________________________________________

### Question

> When should `logger.exception()` be used?

### Answer

Inside an `except` block when you want to log both the error message and the full traceback.

______________________________________________________________________

### Question

> What information should never be logged?

### Answer

Secrets, passwords, authentication tokens, and other sensitive information that could create security or privacy risks.

______________________________________________________________________

### Question

> What is log propagation?

### Answer

It is the process by which log records are passed up the logger hierarchy so that parent loggers or the root logger can
handle them.

______________________________________________________________________

# Practical Lesson

Build a small application with three modules:

- `api.py`
- `service.py`
- `repository.py`

Each module should:

- Create its own logger using `logging.getLogger(__name__)`.
- Log at different severity levels.
- Simulate an exception and record it using `logger.exception()`.

Configure logging only once in the application's entry point.

______________________________________________________________________

# Questions

## Question 1

Why is logging considered essential in production systems?

### Answer

Because it provides a persistent record of application behaviour, enabling debugging, auditing, monitoring, and incident
investigation.

______________________________________________________________________

## Question 2

What is the difference between a logger and a handler?

### Answer

A logger creates log records, while handlers determine where those records are sent, such as the console, files, or
external logging systems.

______________________________________________________________________

## Question 3

Why is the logger hierarchy useful?

### Answer

It allows consistent configuration across an application while still enabling module-specific logging behaviour.

______________________________________________________________________

## Question 4

When should `DEBUG` logs be used?

### Answer

For detailed diagnostic information that is useful during development or troubleshooting but is usually disabled in
production.

______________________________________________________________________

## Question 5

Why is structured logging preferred in distributed systems?

### Answer

Because structured fields make logs easier to search, aggregate, correlate, and analyse across multiple services.

______________________________________________________________________

# Assignment

## Exercise 1

Replace every `print()` statement in one of your projects with the appropriate logging call.

______________________________________________________________________

## Exercise 2

Configure separate console and file handlers.

Verify that both receive log messages.

______________________________________________________________________

## Exercise 3

Trigger an exception intentionally and compare the output of:

- `logger.error()`
- `logger.exception()`

______________________________________________________________________

## Exercise 4

Design a logging strategy for one of your backend services.

Document:

- Log levels
- What events to log
- What sensitive data must never be logged
- How request IDs would be included

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why logging is essential in production.
- ✅ The architecture of Python's logging module.
- ✅ Loggers, handlers, formatters, and propagation.
- ✅ Log levels.
- ✅ Exception logging.
- ✅ Structured logging concepts.
- ✅ Production logging best practices.

______________________________________________________________________

# Next Lesson

**File:** [57-production-python-part-02-exception-handling.md](57-production-python-part-02-exception-handling.md)
