# Custom Exception Handlers

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 5 - Middleware & Exception Handling
>
> **File:** `24_custom_exception_handlers.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Custom Exception Handlers are
- Why Custom Handlers are Needed
- Creating Custom Exceptions
- Registering Exception Handlers
- Handling Multiple Exceptions
- Returning Custom Error Responses
- Exception Hierarchy
- Logging Exceptions
- Production Error Design
- Best Practices

______________________________________________________________________

# What is a Custom Exception Handler?

A **Custom Exception Handler** converts application exceptions into HTTP responses.

Instead of every route doing

```python
raise HTTPException(...)
```

we separate

```
Business Error

↓

Exception Handler

↓

HTTP Response
```

______________________________________________________________________

# Why Use Custom Exception Handlers?

Imagine

```
User Service

↓

User Not Found
```

Without handlers

Every route converts

```
UserNotFound

↓

HTTP 404
```

Repeated logic.

Better

```
Route

↓

Service

↓

UserNotFound

↓

Global Handler

↓

404 Response
```

______________________________________________________________________

# Creating a Custom Exception

```python
class UserNotFound(

    Exception

):

    pass
```

Business-specific exceptions should describe the domain,

not HTTP.

______________________________________________________________________

# Another Example

```python
class OrderNotFound(

    Exception

):

    pass
```

```python
class PaymentFailed(

    Exception

):

    pass
```

Each exception represents a business event.

______________________________________________________________________

# Raising the Exception

Service

```python
def get_user(

    user_id: int

):

    raise UserNotFound()
```

Notice

No HTTP code appears here.

______________________________________________________________________

# Registering a Handler

Import

```python
from fastapi import Request

from fastapi.responses import JSONResponse
```

______________________________________________________________________

# Basic Handler

```python
@app.exception_handler(

    UserNotFound

)

async def user_handler(

    request: Request,

    exc: UserNotFound

):

    return JSONResponse(

        status_code=404,

        content={

            "detail":

            "User not found"

        }

    )
```

______________________________________________________________________

# Internal Flow

```
Request

↓

Route

↓

Service

↓

UserNotFound

↓

Handler

↓

JSON

↓

Client
```

______________________________________________________________________

# Rich Error Response

```python
return JSONResponse(

    status_code=404,

    content={

        "error": {

            "code":

            "USER_NOT_FOUND",

            "message":

            "User not found"

        }

    }
)
```

Many production APIs use structured error payloads.

______________________________________________________________________

# Multiple Handlers

```python
@app.exception_handler(

    UserNotFound

)
```

```python
@app.exception_handler(

    OrderNotFound

)
```

Each exception can have its own response.

______________________________________________________________________

# Shared Handler

Several exceptions may map to the same HTTP response.

Example

```
ProductNotFound

↓

CustomerNotFound

↓

404
```

The response format remains consistent.

______________________________________________________________________

# Exception Hierarchy

```
ApplicationError

↓

UserNotFound

↓

OrderNotFound

↓

PaymentFailed
```

A common base class makes exception management easier.

______________________________________________________________________

# Example

```python
class ApplicationError(

    Exception

):

    pass
```

```python
class UserNotFound(

    ApplicationError

):

    pass
```

______________________________________________________________________

# Logging

Inside the handler

```python
logger.error(

    str(exc)
)
```

or

```python
logger.exception(

    "Application Error"
)
```

Logging helps diagnose production failures.

______________________________________________________________________

# Request Information

The handler receives

```python
request: Request
```

Useful information includes

```python
request.url
```

```python
request.method
```

```python
request.headers
```

These details are often logged.

______________________________________________________________________

# Returning Headers

Example

```python
return JSONResponse(

    status_code=429,

    headers={

        "Retry-After":

        "60"

    },

    content={

        "detail":

        "Too many requests"

    }
)
```

______________________________________________________________________

# Unexpected Exceptions

Catch all remaining errors

```python
@app.exception_handler(

    Exception

)
```

Return

```
500

Internal Server Error
```

Do **not** expose stack traces to clients.

______________________________________________________________________

# Exception Flow

```
Business Logic

↓

Raise Exception

↓

Global Handler

↓

JSON Response
```

The route remains clean.

______________________________________________________________________

# Layered Architecture

```
Route

↓

Service

↓

Repository

↓

Database

↓

Exception

↓

Handler
```

Business layers remain independent of HTTP.

______________________________________________________________________

# Error Codes

Instead of

```json
{
    "detail": "Not Found"
}
```

Production APIs often return

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User not found"
    }
}
```

Machine-readable codes make client applications easier to build.

______________________________________________________________________

# Correlation IDs

A production error response may include

```json
{
    "request_id": "abc123"
}
```

Support teams can locate the corresponding logs quickly.

______________________________________________________________________

# Common Mistakes

❌ Raising `HTTPException` from repository code

❌ Returning different error formats for different endpoints

❌ Exposing internal exception messages

❌ Ignoring logging

❌ Catching every exception and silently continuing

______________________________________________________________________

# Production Best Practices

- Create domain-specific exceptions.
- Register global exception handlers.
- Standardize error responses.
- Log unexpected failures.
- Keep HTTP concerns outside business logic.
- Include request IDs when available.
- Never expose internal implementation details.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should service layers raise custom exceptions instead of `HTTPException`?**

### Answer

Service layers implement business logic and should remain independent of the web framework.

By raising domain-specific exceptions such as `UserNotFound`,

the service can be reused by

- HTTP APIs
- Background workers
- CLI tools
- Scheduled jobs

The FastAPI layer is responsible for translating those exceptions into HTTP responses.

This separation improves maintainability, portability, and testability.

______________________________________________________________________

# Summary

In this chapter you learned:

- Custom Exception Handlers
- Custom Exceptions
- Exception Registration
- Structured Error Responses
- Logging
- Exception Hierarchies
- Layered Architecture
- Production Best Practices

Custom exception handlers separate business errors from HTTP concerns, leading to cleaner architecture, reusable
services, and consistent error handling across the application.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a custom exception handler?
1. Why are custom exception handlers useful?
1. Why should business logic avoid `HTTPException`?

______________________________________________________________________

## Exceptions

4. How do you create a custom exception?
1. How do you register an exception handler?
1. What information does an exception handler receive?

______________________________________________________________________

## Architecture

7. Why should repository and service layers remain independent of HTTP?
1. What are the advantages of domain-specific exceptions?
1. Why is a common base exception class useful?

______________________________________________________________________

## Error Responses

10. Why should error responses be standardized?
01. Why are machine-readable error codes valuable?
01. Why might a request ID be included in an error response?

______________________________________________________________________

## Logging

13. Why should exceptions be logged?
01. What request information is useful when logging an error?
01. Why shouldn't stack traces be returned to clients?

______________________________________________________________________

## Scenario-Based

16. Your `OrderService` raises `HTTPException(status_code=404)` directly. How would you redesign this using custom exceptions?
01. Your API currently returns different JSON structures for different errors. How would you standardize them?
01. A customer reports an intermittent failure, but support cannot find the matching logs. How could correlation IDs improve troubleshooting?
01. Your application is reused by both a FastAPI server and a background worker. Why does keeping business exceptions independent of HTTP make this easier?
01. Your team has duplicated `try/except` blocks across dozens of routes. How do custom exception handlers simplify the architecture?

______________________________________________________________________

# Next

[Background Tasks](25_background_tasks.md)
