# Middleware

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 5 - Middleware & Exception Handling
>
> **File:** `21_middleware.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Middleware is
- Why Middleware is Needed
- Request-Response Lifecycle
- Creating Middleware
- Multiple Middleware
- Middleware Order
- Common Middleware
- Middleware vs Dependencies
- Performance Considerations
- Production Best Practices

______________________________________________________________________

# What is Middleware?

Middleware is code that executes **before and after** every request.

Think of middleware as a checkpoint through which every request and response passes.

```
Request

↓

Middleware

↓

Route

↓

Middleware

↓

Response
```

Unlike dependencies,

middleware executes for every matching request.

______________________________________________________________________

# Why Do We Need Middleware?

Without middleware

```
Route A

↓

Logging
```

```
Route B

↓

Logging
```

```
Route C

↓

Logging
```

Duplicate code everywhere.

With middleware

```
Request

↓

Logging Middleware

↓

All Routes
```

Write once,

reuse everywhere.

______________________________________________________________________

# Request Lifecycle

```
Client

↓

Middleware

↓

Authentication

↓

Dependency Injection

↓

Route

↓

Business Logic

↓

Response

↓

Middleware

↓

Client
```

Middleware wraps the entire request lifecycle.

______________________________________________________________________

# Common Use Cases

Middleware is commonly used for

- Logging
- Request Timing
- CORS
- Compression
- Authentication (sometimes)
- Request IDs
- Rate Limiting
- Metrics
- Security Headers

______________________________________________________________________

# Creating Middleware

Import

```python
from fastapi import Request
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI

from fastapi import Request

app = FastAPI()

@app.middleware("http")

async def log_requests(

    request: Request,

    call_next

):

    response = await call_next(

        request

    )

    return response
```

______________________________________________________________________

# Understanding `call_next`

```
Request

↓

Middleware

↓

call_next()

↓

Route

↓

Response

↓

Middleware
```

`call_next()` passes the request to the next stage.

Without it,

the request never reaches the route.

______________________________________________________________________

# Execution Order

Example

```python
@app.middleware("http")

async def middleware(

    request,

    call_next

):

    print("Before")

    response = await call_next(

        request

    )

    print("After")

    return response
```

Console

```
Before

↓

Route

↓

After
```

______________________________________________________________________

# Internal Flow

```
Incoming Request

↓

Middleware

↓

Dependencies

↓

Route

↓

Response

↓

Middleware

↓

Client
```

______________________________________________________________________

# Logging Middleware

```python
@app.middleware("http")

async def logger(

    request: Request,

    call_next

):

    print(

        request.method,

        request.url

    )

    response = await call_next(

        request

    )

    return response
```

Useful for request auditing.

______________________________________________________________________

# Request Timing

```python
import time
```

```python
start = time.time()

response = await call_next(

    request

)

duration = time.time() - start
```

Useful for

- Performance Monitoring
- Metrics
- Debugging

______________________________________________________________________

# Adding Response Headers

```python
response.headers[

    "X-Time"

] = str(duration)
```

Clients now receive

```
X-Time

↓

0.023
```

Useful for diagnostics.

______________________________________________________________________

# Reading Headers

```python
request.headers
```

Example

```
Authorization

↓

Bearer ...
```

Middleware can inspect request metadata before routing.

______________________________________________________________________

# Reading Client Information

```python
request.client.host
```

Useful for

- Logging
- Rate Limiting
- Analytics

Be aware that reverse proxies may affect the apparent client IP.

______________________________________________________________________

# Multiple Middleware

Example

```python
Middleware A

↓

Middleware B

↓

Route
```

Response

```
Route

↓

Middleware B

↓

Middleware A
```

Middleware behaves like nested layers.

______________________________________________________________________

# Middleware Stack

```
Request

↓

Logger

↓

Timer

↓

CORS

↓

Route

↓

CORS

↓

Timer

↓

Logger

↓

Response
```

______________________________________________________________________

# Middleware Order

Registration order matters.

Example

```python
Logger

↓

Authentication

↓

Route
```

Changing the order changes behavior.

______________________________________________________________________

# Middleware vs Dependencies

Middleware

```
Runs

For Every Request
```

Dependency

```
Runs

Only

When Used
```

Examples

Middleware

- Logging
- Metrics
- CORS

Dependency

- Database Session
- Current User
- Configuration

______________________________________________________________________

# Middleware vs Route Logic

Middleware

```
Cross-Cutting Concerns
```

Routes

```
Business Logic
```

Keep responsibilities separate.

______________________________________________________________________

# Exception Handling

If the route raises an exception

```
Route

↓

Exception Handler

↓

Middleware

↓

Response
```

Middleware still participates in the response flow unless an unhandled error aborts execution.

______________________________________________________________________

# Performance

Every middleware adds processing.

```
Request

↓

Middleware 1

↓

Middleware 2

↓

Middleware 3

↓

Route
```

Keep middleware lightweight.

______________________________________________________________________

# CORS Middleware

One of the most common middleware.

```
Browser

↓

Cross-Origin Request

↓

CORS Middleware

↓

Response
```

We'll cover CORS in a dedicated chapter.

______________________________________________________________________

# Compression Middleware

Automatically compresses responses.

```
Large JSON

↓

GZip

↓

Smaller Response
```

Reduces bandwidth usage.

______________________________________________________________________

# Request IDs

Middleware often generates

```
X-Request-ID

↓

Unique ID
```

Every log entry includes the same ID.

Useful for distributed systems.

______________________________________________________________________

# Metrics

Middleware commonly records

- Request Count
- Error Count
- Response Time
- Request Size
- Response Size

These metrics feed monitoring systems like Prometheus.

______________________________________________________________________

# Common Mistakes

❌ Putting business logic inside middleware

❌ Opening database connections inside middleware unnecessarily

❌ Performing slow blocking operations

❌ Forgetting to call `call_next()`

❌ Creating too many middleware layers

______________________________________________________________________

# Production Best Practices

- Keep middleware lightweight.
- Use middleware only for cross-cutting concerns.
- Use dependencies for request-specific resources.
- Record request timing and metrics.
- Add correlation IDs.
- Avoid blocking I/O.
- Register middleware in the correct order.

______________________________________________________________________

# Interview Deep Dive

### Question

**What is the difference between FastAPI middleware and dependencies?**

### Answer

Middleware wraps the entire request-response lifecycle and executes for every applicable request.

Dependencies execute only for endpoints that declare them.

Middleware is best for cross-cutting concerns such as:

- Logging
- Metrics
- CORS
- Request IDs

Dependencies are best for request-specific resources such as:

- Database sessions
- Authentication
- Configuration
- Current user information

Choosing the appropriate mechanism results in cleaner, more maintainable applications.

______________________________________________________________________

# Summary

In this chapter you learned:

- Middleware
- Request Lifecycle
- `call_next()`
- Middleware Order
- Logging
- Request Timing
- Response Headers
- Middleware vs Dependencies
- Performance Considerations
- Production Best Practices

Middleware is a powerful mechanism for implementing cross-cutting functionality that should apply consistently across
many or all requests.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is middleware?
1. Why is middleware useful?
1. Where does middleware execute in the request lifecycle?

______________________________________________________________________

## FastAPI

4. What is the purpose of `call_next()`?
1. What happens if `call_next()` is never called?
1. How do you register middleware?

______________________________________________________________________

## Execution

7. How does middleware behave when multiple middleware are registered?
1. Why does middleware execute again after the route returns a response?
1. Why does middleware registration order matter?

______________________________________________________________________

## Architecture

10. When should middleware be used instead of dependencies?
01. What responsibilities belong in middleware?
01. What responsibilities should remain in route handlers or services?

______________________________________________________________________

## Performance

13. Why should middleware remain lightweight?
01. Why is request timing commonly implemented using middleware?
01. Why are request IDs useful in distributed systems?

______________________________________________________________________

## Scenario-Based

16. Every endpoint in your application logs the request method and URL. How can middleware eliminate this duplication?
01. Your API should include an `X-Response-Time` header for every response. Where would you implement this?
01. A teammate performs complex database queries inside middleware for every request. Why is this a poor architectural choice?
01. Your application has logging, timing, and CORS middleware. In what order are they executed for requests and responses?
01. Your application exposes hundreds of endpoints. Why is middleware a better place for metrics collection than adding timing logic inside every route?

______________________________________________________________________

# Next

[Built-in Middleware (CORS, GZip, TrustedHost, HTTPSRedirect)](22_builtin_middleware.md)
