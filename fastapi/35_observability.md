# Observability (Logging & Health Checks)

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 11 - Deployment
>
> **File:** `35_observability.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Observability is
- The Three Pillars of Observability
- Logging
- Health Checks
- Readiness & Liveness Probes
- Structured Logging
- Correlation IDs
- Log Levels
- Monitoring Integration
- Production Best Practices

______________________________________________________________________

# What is Observability?

Observability is the ability to understand **what is happening inside your application** without directly accessing the
server.

When something goes wrong,

observability helps answer questions like

- What failed?
- When did it fail?
- Why did it fail?
- Which request caused it?
- Which service is affected?

______________________________________________________________________

# Why Observability Matters

Without observability

```
User Reports Error

↓

No Logs

↓

No Metrics

↓

No Clue
```

With observability

```
User Reports Error

↓

Logs

↓

Request ID

↓

Database Error

↓

Fix
```

______________________________________________________________________

# Three Pillars of Observability

Modern systems rely on

```
Logs
```

```
Metrics
```

```
Traces
```

This chapter focuses on **Logs** and **Health Checks**.

______________________________________________________________________

# What is Logging?

Logging is the process of recording important application events.

Examples

- Application Started
- User Logged In
- Order Created
- API Error
- Database Timeout

Logs help diagnose issues after they occur.

______________________________________________________________________

# Why Not `print()`?

Bad

```python
print("User logged in")
```

Problems

- No timestamps
- No log levels
- Difficult to search
- Difficult to filter

Use Python's logging module instead.

______________________________________________________________________

# Python Logging

Import

```python
import logging
```

Create a logger

```python
logger = logging.getLogger(__name__)
```

______________________________________________________________________

# Basic Logging

```python
logger.info(

    "Application started"
)
```

```python
logger.warning(

    "Cache unavailable"
)
```

```python
logger.error(

    "Database connection failed"
)
```

______________________________________________________________________

# Log Levels

```
DEBUG

↓

INFO

↓

WARNING

↓

ERROR

↓

CRITICAL
```

Each level represents increasing severity.

______________________________________________________________________

# When to Use Each Level

DEBUG

```
Detailed debugging information
```

INFO

```
Normal application events
```

WARNING

```
Unexpected but recoverable conditions
```

ERROR

```
Request or operation failed
```

CRITICAL

```
Application cannot continue
```

______________________________________________________________________

# Logging Exceptions

Instead of

```python
logger.error(

    "Error"
)
```

Prefer

```python
logger.exception(

    "Unexpected error"
)
```

`logger.exception()` includes the stack trace automatically when called inside an exception handler.

______________________________________________________________________

# Structured Logging

Instead of

```
User logged in
```

Use structured data

```json
{
    "event": "login",
    "user_id": 42,
    "request_id": "abc123"
}
```

Structured logs are easier to search and analyze.

______________________________________________________________________

# Correlation IDs

Every request receives a unique identifier.

Example

```
X-Request-ID

↓

f93ab2...
```

Include this ID in every log message.

______________________________________________________________________

# Correlation Flow

```
Client

↓

Request ID

↓

FastAPI

↓

Database

↓

External API

↓

Logs
```

One ID ties all related events together.

______________________________________________________________________

# Request Logging

Common information

- HTTP Method
- URL
- Status Code
- Response Time
- Client IP
- Request ID

Example

```
GET /users

200

24 ms
```

______________________________________________________________________

# Logging Middleware

Middleware commonly records

```
Request

↓

Start Time

↓

Route

↓

Response

↓

Duration
```

This provides consistent request logs.

______________________________________________________________________

# Health Checks

A health check endpoint reports whether the application is functioning.

Example

```
GET /health
```

Response

```json
{
    "status": "healthy"
}
```

______________________________________________________________________

# Why Health Checks?

Infrastructure uses them to determine whether an instance should receive traffic.

Examples

- Docker
- Kubernetes
- AWS Load Balancer
- Nginx
- Cloud Platforms

______________________________________________________________________

# Liveness Probe

Question

```
Is the application running?
```

Example

```
GET /live
```

If this fails,

the process may need to be restarted.

______________________________________________________________________

# Readiness Probe

Question

```
Can the application accept traffic?
```

Example

```
GET /ready
```

Checks may include

- Database connectivity
- Cache availability
- External dependencies

If readiness fails,

the instance stays alive but does not receive new requests.

______________________________________________________________________

# Liveness vs Readiness

| Liveness | Readiness |
|----------|-----------|
| Is the app alive? | Is the app ready? |
| Restart if unhealthy | Stop sending traffic |
| Usually simple | Often checks dependencies |

______________________________________________________________________

# Example Health Endpoint

```python
@app.get("/health")

def health():

    return {

        "status": "healthy"
    }
```

Simple,

fast,

and lightweight.

______________________________________________________________________

# Advanced Health Check

Example

```python
@app.get("/ready")

def ready():

    database_ok = check_database()

    if not database_ok:

        return {

            "status":

            "unhealthy"
        }

    return {

        "status":

        "ready"
    }
```

______________________________________________________________________

# Monitoring Systems

Logs and health checks integrate with tools such as

- Prometheus
- Grafana
- ELK Stack
- OpenSearch
- Datadog
- CloudWatch

These systems collect and visualize operational data.

______________________________________________________________________

# What Should Be Logged?

Good candidates

- Startup
- Shutdown
- Authentication events
- API requests
- Errors
- External service failures
- Background task failures

Avoid logging sensitive information.

______________________________________________________________________

# Never Log

❌ Passwords

❌ JWT Tokens

❌ API Secrets

❌ Credit Card Numbers

❌ Personally sensitive information unless required and properly protected

Logs are often widely accessible within an organization.

______________________________________________________________________

# Common Mistakes

❌ Using `print()` instead of logging

❌ Logging sensitive data

❌ Logging everything at `ERROR` level

❌ Creating slow health check endpoints

❌ Omitting request IDs from logs

______________________________________________________________________

# Production Best Practices

- Use structured logging.
- Include timestamps and request IDs.
- Log exceptions with stack traces.
- Keep health checks lightweight.
- Separate liveness and readiness endpoints.
- Avoid logging secrets.
- Integrate logs with centralized monitoring.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should production applications expose both liveness and readiness endpoints instead of a single health endpoint?**

### Answer

Liveness and readiness answer different operational questions.

- **Liveness** determines whether the application process is still running correctly.
- **Readiness** determines whether the application is prepared to handle incoming traffic.

For example,

if the database is temporarily unavailable,

the application may still be alive,

but it is **not ready** to serve requests.

Separating these checks allows orchestration systems such as Kubernetes to make better decisions about restarting
instances versus temporarily removing them from load balancing.

______________________________________________________________________

# Summary

In this chapter you learned:

- Observability
- Logging
- Log Levels
- Structured Logging
- Correlation IDs
- Health Checks
- Liveness
- Readiness
- Monitoring Integration
- Production Best Practices

Good observability makes production systems easier to monitor, debug, and maintain by providing visibility into
application behavior and operational health.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is observability?
1. What are the three pillars of observability?
1. Why is logging important?

______________________________________________________________________

## Logging

4. Why is `logging` preferred over `print()`?
1. What are the common log levels?
1. When should `logger.exception()` be used?
1. Why is structured logging useful?

______________________________________________________________________

## Health Checks

8. What is a health check endpoint?
1. What is the difference between liveness and readiness?
1. Why should health check endpoints be lightweight?

______________________________________________________________________

## Monitoring

11. Why are correlation IDs useful?
01. Why shouldn't passwords or JWTs be logged?
01. Which systems commonly consume logs and health check information?

______________________________________________________________________

## Production

14. What events should typically be logged?
01. Why are centralized logging systems valuable?

______________________________________________________________________

## Scenario-Based

16. Your Kubernetes deployment repeatedly restarts application pods because the liveness probe fails. What does this indicate?
01. Your application starts successfully, but the database is temporarily unavailable. Should the liveness or readiness endpoint fail, and why?
01. A support engineer receives a request ID from a customer. How can this help diagnose the issue?
01. Your application logs every incoming JWT token for debugging. What security risks does this introduce?
01. Your team currently uses `print()` statements throughout the application. How would adopting structured logging improve debugging and production monitoring?

______________________________________________________________________

# End of Course 🎉

You have completed the FastAPI Backend Engineering course covering:

- FastAPI Fundamentals
- Routing
- Request Handling
- Middleware
- Exception Handling
- Background Tasks
- Dependency Injection
- Security
- Database Integration
- Project Architecture
- Deployment
- Observability

By mastering these topics, you'll be well-prepared to build production-ready FastAPI applications and confidently answer
FastAPI interview questions for mid-to-senior backend engineering roles.
