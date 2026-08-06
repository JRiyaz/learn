# Error Handling

> **Course:** Flask for Backend Engineers
>
> **Module:** 6
>
> **File:** `15_error_handling.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Error Handling is
- Types of Errors
- Flask Exception Handling
- HTTP Exceptions
- Custom Error Handlers
- Global Error Handling
- Custom Exceptions
- Validation Errors
- Logging Errors
- Debug Mode
- Production Error Responses
- Best Practices

______________________________________________________________________

# Why Error Handling Matters

No application is perfect.

Errors happen because of:

- Invalid user input
- Missing resources
- Database failures
- Network issues
- Programming mistakes
- Third-party API failures

A production application should handle these failures gracefully.

______________________________________________________________________

# Error Flow

```
Request

↓

Route

↓

Business Logic

↓

Exception

↓

Error Handler

↓

Response
```

Instead of crashing,

the application returns a meaningful response.

______________________________________________________________________

# Types of Errors

### Client Errors (4xx)

The client sent an invalid request.

Examples

```
400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Unprocessable Entity
```

______________________________________________________________________

### Server Errors (5xx)

Something failed on the server.

Examples

```
500 Internal Server Error

502 Bad Gateway

503 Service Unavailable

504 Gateway Timeout
```

______________________________________________________________________

# Common Python Exceptions

```
ValueError

TypeError

KeyError

FileNotFoundError

ZeroDivisionError

TimeoutError
```

These may occur inside Flask routes or services.

______________________________________________________________________

# Basic Exception Handling

```python
try:

    value = 10 / 2

except Exception:

    return "Error"
```

Useful,

but too generic for production.

______________________________________________________________________

# Flask abort()

Flask provides

```python
from flask import abort
```

Example

```python
@app.route("/users/<int:id>")

def user(id):

    if id < 1:

        abort(400)

    return "User"
```

______________________________________________________________________

# Common abort() Codes

```python
abort(400)

abort(401)

abort(403)

abort(404)

abort(500)
```

______________________________________________________________________

# Custom Error Handler

```python
@app.errorhandler(404)

def not_found(error):

    return "Not Found", 404
```

Now every

```
404
```

uses the same handler.

______________________________________________________________________

# JSON Error Response

```python
@app.errorhandler(404)

def not_found(error):

    return jsonify(

        {

            "success": False,

            "error": "Resource not found"

        }

    ), 404
```

Useful for REST APIs.

______________________________________________________________________

# Global Exception Handler

```python
@app.errorhandler(Exception)

def handle_exception(error):

    return jsonify(

        {

            "success": False,

            "error": "Internal Server Error"

        }

    ), 500
```

This acts as a final safety net.

______________________________________________________________________

# Custom Exceptions

Example

```python
class UserNotFound(

    Exception

):

    pass
```

Raise

```python
raise UserNotFound()
```

______________________________________________________________________

# Handle Custom Exception

```python
@app.errorhandler(

    UserNotFound

)
def user_not_found(error):

    return jsonify(

        {

            "error": "User not found"

        }

    ), 404
```

______________________________________________________________________

# Validation Errors

Example

```python
if not data.get("email"):

    abort(400)
```

Better

```python
return jsonify(

    {

        "error":

        "Email is required"

    }

), 400
```

Specific messages help API consumers.

______________________________________________________________________

# Database Errors

Example

```python
try:

    db.session.commit()

except Exception:

    db.session.rollback()

    raise
```

Always rollback failed transactions before continuing.

______________________________________________________________________

# External API Errors

```
Application

↓

Payment Gateway

↓

Timeout

↓

Retry

↓

Return Error
```

Do not expose internal details to clients.

______________________________________________________________________

# Logging Errors

Never silently ignore exceptions.

Example

```python
import logging

logging.exception(

    "Unexpected Error"

)
```

`logging.exception()` automatically includes the stack trace when called inside an exception handler.

______________________________________________________________________

# Debug Mode

Development

```python
app.run(

    debug=True
)
```

Shows

- Stack Trace
- Interactive Debugger
- Variable Values

______________________________________________________________________

# Production

Never enable

```
DEBUG=True
```

Reasons

- Sensitive Information
- Source Code Exposure
- Security Risks

______________________________________________________________________

# Error Response Structure

Recommended

```json
{
    "success": false,
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User not found"
    }
}
```

Consistent error responses simplify client-side handling.

______________________________________________________________________

# Exception Hierarchy

```
Exception

↓

ApplicationError

↓

ValidationError

↓

UserNotFound

↓

PaymentFailed
```

Creating a hierarchy makes large applications easier to manage.

______________________________________________________________________

# Error Handling Architecture

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

Global Handler

↓

JSON Response
```

Business layers raise exceptions.

The HTTP layer converts them into responses.

______________________________________________________________________

# Avoid try/except Everywhere

Bad

```
Route

↓

try

↓

Service

↓

try

↓

Repository

↓

try
```

Better

```
Repository

↓

Raise Exception

↓

Global Handler

↓

Response
```

Centralized handling keeps code cleaner.

______________________________________________________________________

# Common Mistakes

❌ Catching every exception without logging

❌ Returning stack traces to users

❌ Using HTTP 200 for failures

❌ Forgetting `rollback()` after failed commits

❌ Ignoring external API failures

❌ Swallowing exceptions silently

______________________________________________________________________

# Production Best Practices

- Use custom exception classes.
- Handle expected errors explicitly.
- Use global error handlers.
- Log unexpected exceptions.
- Return consistent JSON error responses.
- Never expose internal stack traces.
- Roll back failed database transactions.
- Monitor application errors using centralized logging.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is a global exception handler useful in a Flask application?**

### Answer

A global exception handler provides a centralized location for handling unexpected errors.

Benefits include:

1. Prevents application crashes from reaching users.
1. Returns consistent error responses.
1. Logs unexpected exceptions.
1. Prevents exposure of internal implementation details.
1. Reduces duplicated error-handling code across routes.

Expected business errors should still be handled appropriately, while unexpected exceptions can fall back to the global
handler.

______________________________________________________________________

# Summary

In this chapter you learned:

- Error Handling
- HTTP Errors
- Flask Error Handlers
- Global Exception Handling
- Custom Exceptions
- Validation Errors
- Logging
- Debug Mode
- Production Best Practices

Robust error handling improves reliability, security, maintainability, and the overall developer and user experience.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. Why is error handling important?
1. What is the difference between client errors and server errors?
1. When should a 404 response be returned?

______________________________________________________________________

## Flask

4. What does `abort()` do?
1. How do you register a custom error handler?
1. What is the purpose of a global exception handler?

______________________________________________________________________

## Exceptions

7. Why create custom exception classes?
1. Why should database transactions be rolled back after failures?
1. Why shouldn't every function contain its own `try/except` block?

______________________________________________________________________

## Logging

10. Why should exceptions be logged?
01. What information does `logging.exception()` include?
01. Why should stack traces never be returned to API clients?

______________________________________________________________________

## Production

13. Why should `DEBUG=True` never be enabled in production?
01. Why should REST APIs return consistent JSON error responses?
01. How should external service failures be handled?

______________________________________________________________________

## Scenario-Based

16. A database commit fails due to a unique constraint violation. What steps should your application take before returning an error?
01. Your API returns raw Python tracebacks to users after an exception. Why is this dangerous?
01. A developer catches every exception with `except Exception: pass`. What problems can this cause?
01. Your application integrates with a payment gateway that occasionally times out. How should the error be handled and communicated to the client?
01. A large Flask application contains hundreds of duplicated `try/except` blocks inside route handlers. How would you redesign the error-handling architecture?

______________________________________________________________________

# Next

[Logging](16_logging.md)
