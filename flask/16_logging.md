# Logging

> **Course:** Flask for Backend Engineers
>
> **Module:** 7
>
> **File:** `16_logging.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Logging is
- Why Logging is Important
- Logging Levels
- Python Logging Module
- Flask Logging
- Log Formatters
- Log Handlers
- File Logging
- Rotating Logs
- Structured Logging
- Correlation IDs
- Centralized Logging
- Production Best Practices

______________________________________________________________________

# What is Logging?

Logging is the process of recording important events that occur while an application is running.

Examples

- User Login
- API Request
- Database Error
- Payment Success
- Authentication Failure
- Application Startup

Logs help developers understand what happened inside an application.

______________________________________________________________________

# Why Logging Matters

Imagine a production issue.

A customer reports:

```
"The application is not working."
```

Without logs

```
No Information
```

With logs

```
10:32 AM

POST /orders

Database Timeout

Order ID 1023
```

Logs are often the first place engineers investigate.

______________________________________________________________________

# Logging vs print()

Many beginners use

```python
print("User Logged In")
```

Problems

- No log level
- Difficult to search
- No timestamps
- No file output
- Not configurable

Instead use

```python
logging.info(
    "User Logged In"
)
```

______________________________________________________________________

# Logging Flow

```
Application

↓

Logger

↓

Handler

↓

Formatter

↓

Console

or

↓

Log File

or

↓

Cloud Logging System
```

______________________________________________________________________

# Logging Levels

| Level | Purpose |
|---------|----------|
| DEBUG | Detailed debugging information |
| INFO | Normal application events |
| WARNING | Unexpected but recoverable situations |
| ERROR | Operation failed |
| CRITICAL | Serious failure requiring immediate attention |

______________________________________________________________________

# DEBUG

Example

```python
logging.debug(

    "SQL Query Executed"

)
```

Useful during development.

Usually disabled in production.

______________________________________________________________________

# INFO

```python
logging.info(

    "User logged in"

)
```

Normal business events.

______________________________________________________________________

# WARNING

```python
logging.warning(

    "Disk space low"

)
```

Application continues,

but something should be investigated.

______________________________________________________________________

# ERROR

```python
logging.error(

    "Database connection failed"

)
```

An operation failed.

______________________________________________________________________

# CRITICAL

```python
logging.critical(

    "Application cannot start"

)
```

Requires immediate action.

______________________________________________________________________

# Basic Logging

```python
import logging

logging.basicConfig(

    level=logging.INFO
)
```

______________________________________________________________________

# Logger

Instead of using the root logger,

create one.

```python
logger = logging.getLogger(

    __name__

)
```

______________________________________________________________________

# Using the Logger

```python
logger.info(

    "Application Started"

)
```

______________________________________________________________________

# Logging Exceptions

```python
try:

    1 / 0

except Exception:

    logger.exception(

        "Unexpected Error"

    )
```

`logger.exception()` logs the message and the full stack trace.

______________________________________________________________________

# Log Format

Example

```
Time

Level

Module

Message
```

______________________________________________________________________

# Custom Formatter

```python
formatter = logging.Formatter(

    "%(asctime)s "

    "%(levelname)s "

    "%(name)s "

    "%(message)s"
)
```

Example output

```
2026-08-07 10:00:00

INFO

app.users

User Created
```

______________________________________________________________________

# Console Handler

```python
handler = logging.StreamHandler()
```

Outputs logs to the console.

Useful for containers and development.

______________________________________________________________________

# File Handler

```python
handler = logging.FileHandler(

    "app.log"
)
```

Logs are written to a file.

______________________________________________________________________

# Rotating File Handler

Without rotation

```
app.log

↓

10 GB
```

Use

```python
from logging.handlers import RotatingFileHandler
```

Example

```python
handler = RotatingFileHandler(

    "app.log",

    maxBytes=5_000_000,

    backupCount=5
)
```

Old log files are rotated automatically.

______________________________________________________________________

# Timed Rotation

```python
from logging.handlers import TimedRotatingFileHandler
```

Rotate

- Daily
- Hourly
- Weekly

depending on configuration.

______________________________________________________________________

# Flask Logger

Flask provides

```python
app.logger.info(

    "Started"
)
```

For larger applications,

many teams configure their own loggers for greater flexibility.

______________________________________________________________________

# Request Logging

Useful information

```
Method

URL

Status Code

Response Time

IP Address

User ID
```

Example

```
GET /users

200

42 ms
```

______________________________________________________________________

# Structured Logging

Instead of

```
User Logged In
```

Use

```json
{
    "event": "login",
    "user_id": 10,
    "ip": "10.0.0.1"
}
```

Structured logs are easier for log aggregation systems to search and analyze.

______________________________________________________________________

# Correlation IDs

Imagine one request travels through:

```
API

↓

Service

↓

Database

↓

Payment

↓

Notification
```

Attach

```
Request ID

↓

abc123
```

Every log entry includes the same ID.

Example

```
[abc123]

Payment Started
```

```
[abc123]

Payment Completed
```

This makes tracing distributed requests much easier.

______________________________________________________________________

# Sensitive Information

Never log

- Passwords
- Access Tokens
- Credit Card Numbers
- Secrets
- API Keys

Logs may be widely accessible.

______________________________________________________________________

# Log Aggregation

Instead of checking every server,

send logs to a central system.

Example

```
Application

↓

CloudWatch

↓

Search

↓

Dashboard
```

Other common platforms include:

- ELK Stack
- OpenSearch
- Splunk
- Datadog

______________________________________________________________________

# Logging Architecture

```
Flask

↓

Logger

↓

Handler

↓

Formatter

↓

Console

↓

Cloud Logging
```

______________________________________________________________________

# Development vs Production

Development

```
DEBUG
```

Production

```
INFO

WARNING

ERROR
```

Production usually avoids verbose debug logging.

______________________________________________________________________

# Common Mistakes

❌ Using `print()` instead of logging

❌ Logging passwords

❌ Logging entire request bodies without filtering

❌ Using DEBUG level in production

❌ Never rotating log files

❌ Ignoring exceptions

______________________________________________________________________

# Production Best Practices

- Use the `logging` module.
- Configure log levels appropriately.
- Rotate log files.
- Use structured logging when possible.
- Include correlation IDs.
- Centralize logs.
- Never log sensitive data.
- Monitor logs continuously.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is structured logging preferred over plain text logging in modern backend systems?**

### Answer

Structured logging stores log data as key-value pairs instead of free-form text.

Example

```json
{
    "user_id": 10,
    "request_id": "abc123",
    "endpoint": "/orders",
    "status": 201
}
```

Benefits include:

1. Easier searching and filtering.
1. Better integration with log aggregation platforms.
1. Improved analytics and dashboards.
1. Faster troubleshooting.
1. Better support for distributed systems.

Structured logging becomes increasingly valuable as applications grow.

______________________________________________________________________

# Summary

In this chapter you learned:

- Logging
- Logging Levels
- Loggers
- Handlers
- Formatters
- File Logging
- Rotating Logs
- Structured Logging
- Correlation IDs
- Centralized Logging
- Production Best Practices

Logging is one of the most important operational capabilities of a production application because it enables
troubleshooting, monitoring, auditing, and incident investigation.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is logging?
1. Why is logging better than `print()`?
1. What information should logs contain?

______________________________________________________________________

## Logging Levels

4. What is the purpose of the DEBUG level?
1. When should WARNING be used?
1. What is the difference between ERROR and CRITICAL?

______________________________________________________________________

## Python Logging

7. Why should you create named loggers?
1. What does `logger.exception()` do?
1. What is the purpose of a Formatter?
1. What is the purpose of a Handler?

______________________________________________________________________

## Production

11. Why should log files be rotated?
01. Why should logs be centralized?
01. What is structured logging?
01. What is a correlation ID?

______________________________________________________________________

## Security

15. Why should passwords never be logged?
01. Why should access tokens be excluded from logs?

______________________________________________________________________

## Scenario-Based

17. Your production application stores all logs in a single file that has grown to 40 GB. How would you redesign the logging system?
01. A customer reports an intermittent payment failure that spans multiple services. How would correlation IDs help during investigation?
01. A developer enables DEBUG logging in production and logs complete request bodies, including passwords. What risks does this introduce?
01. Your application runs across multiple containers. Why is centralized logging important, and what kinds of platforms can be used to collect logs?

______________________________________________________________________

# Next

[Testing Flask Applications](17_testing.md)
