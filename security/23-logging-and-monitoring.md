# Security - Part 23

# Logging & Monitoring

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why logging and monitoring are important
- What should be logged
- What should **never** be logged
- Log levels
- Structured logging
- Correlation IDs
- Monitoring and alerting
- FastAPI logging best practices

______________________________________________________________________

# Why Do We Need Logging?

Imagine your production API suddenly starts returning

```text id="log2301"
500 Internal Server Error
```

Without logs,

you have no idea:

- Which endpoint failed?
- Which user was affected?
- What exception occurred?
- When it happened?

Logs help answer these questions.

______________________________________________________________________

# Logging vs Monitoring

These terms are often confused.

### Logging

Logging is the process of recording events.

Example

```text id="log2302"
User Logged In

↓

Log Entry
```

______________________________________________________________________

### Monitoring

Monitoring continuously checks the health of your system.

Example

```text id="log2303"
CPU Usage

↓

Memory

↓

API Errors

↓

Alerts
```

Logging records information.

Monitoring watches that information and other metrics.

______________________________________________________________________

# Typical Request Flow

```text id="log2304"
Request

↓

Authentication

↓

Business Logic

↓

Database

↓

Response

↓

Logs
```

Logs should provide enough context

to understand what happened.

______________________________________________________________________

# What Should We Log?

Good candidates include:

- Login attempts
- Authentication failures
- Authorization failures
- API requests
- Exceptions
- File uploads
- Payment events
- Administrative actions

These events are useful for troubleshooting and auditing.

______________________________________________________________________

# What Should NEVER Be Logged?

Never log:

- Passwords
- JWT tokens
- API keys
- Database passwords
- Credit card numbers
- OTPs
- Encryption keys

Example

❌ Bad

```python id="log2305"
logger.info(
    f"Password: {password}"
)
```

Good

```python id="log2306"
logger.info(
    "User login attempt"
)
```

______________________________________________________________________

# Log Levels

Python provides several log levels.

| Level | Purpose |
| -------- | --------------------------------------------- |
| DEBUG | Detailed debugging information |
| INFO | Normal application events |
| WARNING | Unexpected but recoverable situations |
| ERROR | Request or operation failed |
| CRITICAL | Serious failure requiring immediate attention |

______________________________________________________________________

# Example

```python id="log2307"
import logging

logger = logging.getLogger(__name__)

logger.info("Application started")
```

Error example

```python id="log2308"
logger.error(
    "Database connection failed"
)
```

______________________________________________________________________

# Structured Logging

Instead of writing free-form text,

log structured information.

Bad

```text id="log2309"
Something went wrong
```

Better

```text id="log2310"
{
    "event": "login_failed",
    "user_id": 42,
    "ip": "192.168.1.10"
}
```

Structured logs are easier to search,

filter,

and analyze.

______________________________________________________________________

# Correlation IDs

Suppose one API request travels through:

- API Gateway
- FastAPI
- Payment Service
- Notification Service

How do you identify

all logs related to the same request?

Use a

```text id="log2311"
Correlation ID
```

Workflow

```text id="log2312"
Request

↓

Correlation ID

↓

Every Service Logs It
```

Now,

you can trace

the entire request

across multiple services.

This becomes extremely important

when we study Microservices.

______________________________________________________________________

# Exception Logging

Always log exceptions.

Example

```python id="log2313"
try:
    process_payment()

except Exception:
    logger.exception(
        "Payment processing failed"
    )
```

`logger.exception()`

automatically includes

the stack trace.

______________________________________________________________________

# Monitoring

Monitoring focuses on metrics.

Examples:

- Request count
- Response time
- Error rate
- CPU usage
- Memory usage
- Disk usage
- Database latency

These metrics help detect issues

before users notice them.

______________________________________________________________________

# Alerts

Monitoring becomes useful

when it generates alerts.

Example

```text id="log2314"
Error Rate > 5%

↓

Alert

↓

Developer Notified
```

Common alert scenarios:

- High CPU usage
- Database unavailable
- Too many HTTP 500 responses
- Excessive login failures

______________________________________________________________________

# FastAPI Logging

Typical request lifecycle

```text id="log2315"
Incoming Request

↓

Log Request

↓

Business Logic

↓

Exception?

↓

Log Exception

↓

Return Response
```

Avoid logging

every variable.

Log only meaningful events.

______________________________________________________________________

# Centralized Logging

Production applications

often send logs

to a central system.

Example

```text id="log2316"
FastAPI

↓

Log Aggregator

↓

Search

↓

Dashboard
```

Common tools include:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Grafana Loki
- Splunk
- Datadog

______________________________________________________________________

# Defense in Depth

Logging supports

every security layer.

```text id="log2317"
Authentication

↓

Authorization

↓

Rate Limiting

↓

Logging

↓

Monitoring

↓

Alerting
```

Without logs,

detecting attacks becomes much harder.

______________________________________________________________________

# Best Practices

✅ Log meaningful events.

✅ Never log secrets.

✅ Use structured logging.

✅ Include Correlation IDs.

✅ Monitor application health.

✅ Configure alerts.

✅ Retain logs securely.

______________________________________________________________________

# Common Mistakes

### Logging Passwords

Sensitive information

should never appear in logs.

______________________________________________________________________

### Logging Everything

Too many logs

create noise

and increase storage costs.

Focus on meaningful events.

______________________________________________________________________

### Ignoring Failed Login Attempts

Repeated failures

may indicate

a brute-force attack.

______________________________________________________________________

### No Correlation IDs

Tracing requests

across multiple services

becomes very difficult.

______________________________________________________________________

### No Monitoring

Logs alone

are not enough.

Monitoring helps detect problems proactively.

______________________________________________________________________

# Quick Comparison

| Poor Practice | Better Practice |
| ------------------- | -------------------- |
| Plain text logs | Structured logs |
| Log passwords | Log events only |
| No request tracking | Correlation IDs |
| No alerts | Automated monitoring |
| Local logs only | Centralized logging |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why are logging and monitoring important for backend security?

Logging records important application events such as authentication failures, authorization failures, exceptions, and
administrative actions, providing an audit trail for troubleshooting and security investigations. Monitoring
continuously observes application health and performance metrics, generating alerts when abnormal behavior occurs.
Together, they help detect attacks, diagnose problems, and maintain system reliability while ensuring sensitive
information is never logged.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Logging vs Monitoring
- Log levels
- Structured logging
- Correlation IDs
- Exception logging
- Monitoring
- Alerts
- Centralized logging
- Best practices

______________________________________________________________________

# What's Next

[Dependency Security](24-dependency-security.md)
