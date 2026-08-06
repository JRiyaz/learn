# Exception Handling

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 5 - Middleware & Exception Handling
>
> **File:** `23_exception_handling.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Exceptions are
- Why Exception Handling is Important
- `HTTPException`
- Raising Exceptions
- Global Exception Handlers
- Custom Exceptions
- Exception Flow
- Error Response Design
- Logging Exceptions
- Production Best Practices

______________________________________________________________________

# What is an Exception?

An **Exception** is an error that occurs during program execution.

Examples

- User not found
- Database unavailable
- Invalid permissions
- Division by zero
- File not found

Without proper handling,

exceptions may crash the request or expose internal details.

______________________________________________________________________

# Why Exception Handling?

Suppose a user requests

```
GET

/users/999
```

But the user doesn't exist.

Without handling

```
Application Error

↓

500 Internal Server Error
```

Better

```
404

User Not Found
```

Clients receive meaningful responses.

______________________________________________________________________

# Common HTTP Errors

| Status | Meaning |
|---------|----------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

______________________________________________________________________

# HTTPException

FastAPI provides

```python
HTTPException
```

Import

```python
from fastapi import HTTPException
```

______________________________________________________________________

# Basic Example

```python
@app.get(

"/users/{id}"

)

def get_user(

    id: int

):

    raise HTTPException(

        status_code=404,

        detail="User not found"

    )
```

______________________________________________________________________

# Response

```json
{
    "detail": "User not found"
}
```

FastAPI automatically returns

```
404
```

______________________________________________________________________

# Internal Flow

```
Route

↓

HTTPException

↓

Exception Handler

↓

JSON Response
```

No manual response construction is required.

______________________________________________________________________

# Conditional Example

```python
@app.get(

"/users/{id}"

)

def get_user(

    id: int

):

    if id != 1:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )

    return {

        "id": 1
    }
```

______________________________________________________________________

# Raising Different Errors

Unauthorized

```python
raise HTTPException(

    status_code=401,

    detail="Authentication required"
)
```

Forbidden

```python
raise HTTPException(

    status_code=403,

    detail="Access denied"
)
```

Conflict

```python
raise HTTPException(

    status_code=409,

    detail="Email already exists"
)
```

______________________________________________________________________

# Exception Flow

```
Request

↓

Route

↓

Exception

↓

Handler

↓

JSON

↓

Client
```

______________________________________________________________________

# Why Use Exceptions?

Without exceptions

```python
if error:

    return {

        "error": ...

    }
```

Every route repeats error handling.

With exceptions

```
Raise Exception

↓

Global Handler

↓

Consistent Response
```

Cleaner architecture.

______________________________________________________________________

# Custom Headers

`HTTPException` supports response headers.

```python
raise HTTPException(

    status_code=401,

    detail="Unauthorized",

    headers={

        "WWW-Authenticate":

        "Bearer"

    }
)
```

Useful for authentication protocols.

______________________________________________________________________

# Custom Exceptions

Create your own exception class.

```python
class UserNotFound(

    Exception

):

    pass
```

Routes raise domain-specific exceptions instead of HTTP-specific ones.

______________________________________________________________________

# Global Exception Handler

Import

```python
from fastapi import Request

from fastapi.responses import JSONResponse
```

Example

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

# Flow

```
Route

↓

UserNotFound

↓

Global Handler

↓

JSON Response
```

The route remains focused on business logic.

______________________________________________________________________

# Why Custom Exceptions?

Instead of

```python
raise HTTPException(...)
```

inside service layers,

raise

```python
UserNotFound()
```

Benefits

- Cleaner services
- Better separation of concerns
- Easier testing
- Reusable exception handling

______________________________________________________________________

# Validation Errors

FastAPI automatically handles

- Path Validation
- Query Validation
- Header Validation
- Body Validation

Result

```
422

Validation Error
```

No custom code is required.

______________________________________________________________________

# Unexpected Exceptions

Example

```python
1 / 0
```

Without handling

```
500

Internal Server Error
```

Applications should log unexpected errors while returning safe responses.

______________________________________________________________________

# Logging Exceptions

Example

```python
try:

    ...

except Exception:

    logger.exception(

        "Unexpected error"
    )

    raise
```

Avoid swallowing exceptions silently.

______________________________________________________________________

# Error Response Design

Consistent structure

```json
{
    "detail": "User not found"
}
```

Larger APIs often standardize responses further.

Example

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User not found"
    }
}
```

Choose one format and use it consistently.

______________________________________________________________________

# Exception Hierarchy

```
Exception

↓

Application Exceptions

↓

HTTP Response
```

Separate business exceptions from HTTP concerns where practical.

______________________________________________________________________

# Production Architecture

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

↓

Response
```

Routes don't need to know how every error is converted into HTTP.

______________________________________________________________________

# Common Mistakes

❌ Returning HTTP 200 with an error message

❌ Catching every exception without logging

❌ Exposing stack traces to clients

❌ Raising `HTTPException` deep inside repository code

❌ Using inconsistent error formats

______________________________________________________________________

# Production Best Practices

- Raise meaningful HTTP status codes.
- Use custom exceptions for business errors.
- Handle exceptions globally.
- Log unexpected exceptions.
- Avoid exposing internal implementation details.
- Standardize error response formats.
- Separate business logic from HTTP concerns.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are global exception handlers preferred over returning error responses directly from every route?**

### Answer

Global exception handlers centralize error handling.

Benefits include:

- Consistent error responses.
- Reduced code duplication.
- Cleaner route handlers.
- Easier maintenance.
- Better separation between business logic and HTTP concerns.

Routes focus on application behavior,

while exception handlers translate failures into appropriate HTTP responses.

______________________________________________________________________

# Summary

In this chapter you learned:

- Exceptions
- HTTPException
- Custom Exceptions
- Global Exception Handlers
- Validation Errors
- Error Response Design
- Logging
- Production Best Practices

Proper exception handling improves API reliability, consistency, security, and maintainability while providing
meaningful feedback to API consumers.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is an exception?
1. Why should APIs handle exceptions?
1. What is `HTTPException`?

______________________________________________________________________

## HTTP Errors

4. When should HTTP 404 be returned?
1. What is the difference between HTTP 401 and HTTP 403?
1. When should HTTP 409 be used?

______________________________________________________________________

## Custom Exceptions

7. Why create custom exception classes?
1. What is the purpose of a global exception handler?
1. Why should service layers avoid raising `HTTPException` directly?

______________________________________________________________________

## Validation

10. Which validation errors does FastAPI handle automatically?
01. Why does FastAPI return HTTP 422 for validation failures?

______________________________________________________________________

## Production

12. Why shouldn't stack traces be returned to clients?
01. Why is consistent error formatting important?
01. Why should unexpected exceptions be logged?

______________________________________________________________________

## Scenario-Based

15. Your service layer discovers that a requested order does not exist. How would you design the exception flow from the service layer to the HTTP response?
01. A developer returns HTTP 200 with `{ "error": "User not found" }`. Why is this poor API design?
01. Your application experiences an unexpected database failure. What should the client receive, and what should happen internally?
01. Your organization wants every error response to include an error code, message, and request ID. Where would you implement this?
01. A teammate catches every exception with `except Exception: pass`. Why is this dangerous?
01. Your API currently duplicates the same `try/except` block in dozens of routes. How would global exception handlers simplify the architecture?

______________________________________________________________________

# Next

[Custom Exception Handlers](24_custom_exception_handlers.md)
