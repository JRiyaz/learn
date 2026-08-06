# FastAPI Application Lifecycle

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `03_application_lifecycle.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What the FastAPI Application Lifecycle is
- How a Request is Processed
- ASGI Request Flow
- Lifespan Events
- Startup Events
- Shutdown Events
- Request Lifecycle
- Middleware Flow
- Dependency Resolution
- Response Lifecycle
- Production Considerations

______________________________________________________________________

# Why Learn the Lifecycle?

Many developers know how to write

```python
@app.get("/")
```

but don't know what happens internally.

Interviewers commonly ask

> **"What happens internally when a request reaches FastAPI?"**

Understanding the lifecycle helps you

- Debug applications
- Write middleware
- Manage resources
- Design scalable systems

______________________________________________________________________

# High-Level Lifecycle

```
Application Starts

↓

Startup Events

↓

Application Ready

↓

Receive Requests

↓

Process Requests

↓

Return Responses

↓

Shutdown Events

↓

Application Stops
```

______________________________________________________________________

# Complete Production Flow

```
Browser

↓

Load Balancer

↓

Nginx

↓

Uvicorn

↓

FastAPI

↓

Middleware

↓

Dependency Injection

↓

Route

↓

Business Logic

↓

Database

↓

Response

↓

Middleware

↓

Browser
```

______________________________________________________________________

# ASGI Flow

FastAPI follows the ASGI specification.

```
Browser

↓

HTTP Request

↓

Uvicorn (ASGI Server)

↓

FastAPI Application

↓

HTTP Response
```

Unlike WSGI,

ASGI supports

- Async Requests
- WebSockets
- Long-lived Connections
- Streaming Responses

______________________________________________________________________

# Application Startup

When the application starts,

FastAPI initializes resources.

Examples

- Database Connections
- Redis Clients
- Configuration
- Logging
- Machine Learning Models
- External Service Clients

This happens **once**, not for every request.

______________________________________________________________________

# Lifespan Events

Modern FastAPI applications use the **lifespan** mechanism.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting...")

    yield

    print("Stopping...")

app = FastAPI(

    lifespan=lifespan
)
```

Everything before

```
yield
```

runs during startup.

Everything after

```
yield
```

runs during shutdown.

______________________________________________________________________

# Why Lifespan?

Before FastAPI introduced lifespan,

developers commonly used

```python
@app.on_event("startup")
```

and

```python
@app.on_event("shutdown")
```

The lifespan API provides one unified lifecycle mechanism and is the recommended approach for new applications.

______________________________________________________________________

# Startup Tasks

Examples

```
Connect Database

↓

Connect Redis

↓

Load Configuration

↓

Initialize Logger

↓

Application Ready
```

These tasks should complete before the application begins serving requests.

______________________________________________________________________

# Shutdown Tasks

Examples

```
Close Database

↓

Close Redis

↓

Flush Logs

↓

Release Resources
```

Proper cleanup prevents resource leaks.

______________________________________________________________________

# What Happens When a Request Arrives?

Example

```
GET /users/10
```

Flow

```
HTTP Request

↓

Uvicorn

↓

FastAPI

↓

Middleware

↓

Dependency Injection

↓

Validation

↓

Route

↓

Business Logic

↓

Database

↓

Serialization

↓

Response
```

______________________________________________________________________

# Step 1

## Uvicorn Receives the Request

```
Client

↓

TCP Connection

↓

HTTP Request

↓

Uvicorn
```

Uvicorn parses the HTTP request and forwards it to the FastAPI application.

______________________________________________________________________

# Step 2

## Middleware Executes

Request middleware runs before the route.

Example responsibilities

- Logging
- Authentication
- CORS
- Timing
- Request IDs

Flow

```
Request

↓

Middleware

↓

Route
```

______________________________________________________________________

# Step 3

## Route Matching

FastAPI matches the URL.

Example

```python
@app.get("/users/{id}")
```

Incoming request

```
/users/10
```

Route found.

If no route matches,

```
404
```

is returned.

______________________________________________________________________

# Step 4

## Dependency Injection

Before the route executes,

FastAPI resolves dependencies.

Example

```python
Depends(

    get_db

)
```

Dependencies may provide

- Database Sessions
- Current User
- Configuration
- Services

We'll study dependency injection in detail later.

______________________________________________________________________

# Step 5

## Parameter Validation

Example

```python
def get_user(

    id: int
)
```

Incoming

```
abc
```

FastAPI automatically returns

```
422

Validation Error
```

The route function is never executed.

______________________________________________________________________

# Step 6

## Request Body Validation

Example

```python
class User(

    BaseModel

):

    name: str
```

Incoming JSON

```json
{
    "name": 123
}
```

Validation fails.

FastAPI returns a structured validation error automatically.

______________________________________________________________________

# Step 7

## Route Function Executes

```python
@app.get("/users/{id}")

def get_user(

    id: int
):

    ...
```

Business logic begins.

______________________________________________________________________

# Step 8

## Service Layer

Good architecture

```
Route

↓

Service

↓

Repository

↓

Database
```

Routes should remain thin.

Business logic belongs in services.

______________________________________________________________________

# Step 9

## Database Access

Example

```
PostgreSQL

↓

Query

↓

User
```

Data is retrieved or modified.

______________________________________________________________________

# Step 10

## Response Serialization

Example

Python

```python
return {

    "id": 10,

    "name": "Riyaz"

}
```

FastAPI converts the Python object into JSON automatically.

______________________________________________________________________

# Step 11

## Response Validation

If a response model exists,

FastAPI validates the response before sending it.

Example

```python
response_model=UserResponse
```

Benefits

- Prevents accidental data leakage
- Ensures consistent API responses

______________________________________________________________________

# Step 12

## Middleware Executes Again

Response middleware runs.

Example

```
Route

↓

Middleware

↓

Browser
```

Typical tasks

- Logging
- Timing
- Security Headers

______________________________________________________________________

# Complete Request Flow

```
Request

↓

Uvicorn

↓

Middleware

↓

Dependency Injection

↓

Validation

↓

Route

↓

Service

↓

Repository

↓

Database

↓

Response Validation

↓

Middleware

↓

Browser
```

______________________________________________________________________

# Exception Flow

Suppose the database fails.

```
Database

↓

Exception

↓

Exception Handler

↓

JSON Response
```

Global exception handlers convert errors into HTTP responses.

______________________________________________________________________

# Request Context

Every request has its own execution context.

```
Request A

↓

Independent
```

```
Request B

↓

Independent
```

This isolation allows many requests to be processed concurrently.

______________________________________________________________________

# Async Lifecycle

```
Request

↓

Await Database

↓

Other Requests Continue

↓

Database Responds

↓

Continue Execution
```

This is one of the key advantages of ASGI.

______________________________________________________________________

# Startup vs Request

Startup

```
Runs Once
```

Request

```
Runs

For Every Request
```

Examples

Startup

- Database Pool
- Redis Client

Request

- Validation
- Authentication
- Business Logic

______________________________________________________________________

# Production Lifecycle

```
Application Starts

↓

Load Config

↓

Connect Database

↓

Connect Redis

↓

Start Workers

↓

Accept Requests

↓

Shutdown

↓

Close Resources
```

______________________________________________________________________

# Common Mistakes

❌ Opening database connections inside every route

❌ Loading configuration on every request

❌ Putting business logic in middleware

❌ Performing expensive initialization during request processing

❌ Forgetting to clean up resources during shutdown

______________________________________________________________________

# Production Best Practices

- Use lifespan events for startup and shutdown tasks.
- Initialize shared resources only once.
- Use dependency injection for request-scoped resources.
- Keep middleware lightweight.
- Validate all requests using Pydantic.
- Keep business logic outside routes.
- Cleanly release resources during shutdown.

______________________________________________________________________

# Interview Deep Dive

### Question

**Explain what happens internally when an HTTP request reaches a FastAPI application.**

### Answer

A typical request follows this sequence:

1. The client sends an HTTP request.
1. Uvicorn receives the request through the ASGI interface.
1. FastAPI executes request middleware.
1. The router matches the requested path.
1. Dependencies are resolved.
1. Path, query, header, and body parameters are validated.
1. The route function executes.
1. Business logic accesses databases or external services.
1. The response is serialized and optionally validated.
1. Response middleware executes.
1. Uvicorn sends the HTTP response back to the client.

This pipeline provides automatic validation, dependency injection, and consistent request handling with minimal
boilerplate.

______________________________________________________________________

# Summary

In this chapter you learned:

- FastAPI Application Lifecycle
- ASGI Request Flow
- Lifespan Events
- Startup
- Shutdown
- Middleware
- Dependency Injection
- Validation
- Response Serialization
- Production Lifecycle

Understanding the application lifecycle is essential for debugging, writing middleware, managing resources, and
explaining FastAPI internals during interviews.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is the FastAPI application lifecycle?
1. What is the purpose of the lifespan API?
1. What is the difference between startup events and request processing?

______________________________________________________________________

## Request Flow

4. What component receives HTTP requests before FastAPI?
1. What happens before a route function executes?
1. When does dependency injection occur?
1. When does request validation occur?
1. When does response serialization occur?

______________________________________________________________________

## Architecture

9. Why should business logic remain outside route handlers?
1. Why should expensive initialization happen during startup instead of per request?

______________________________________________________________________

## ASGI

11. Why is ASGI important for FastAPI?
01. How does ASGI differ from WSGI at a high level?

______________________________________________________________________

## Production

13. What resources are commonly initialized during startup?
01. Why should resources be released during shutdown?
01. Why should middleware remain lightweight?

______________________________________________________________________

## Scenario-Based

16. A developer opens a new database connection inside every API endpoint instead of using dependency injection. What problems might this cause?
01. Your application loads a 2 GB machine learning model every time a request arrives. How should this be redesigned?
01. An incoming request contains `"id": "abc"` where the endpoint expects an integer. At what stage does FastAPI reject the request?
01. Your middleware measures request duration. At which points in the request lifecycle should the timing begin and end?
01. During application shutdown, database connections remain open and logs are not flushed. Which lifecycle mechanism should be used to clean up these resources?

______________________________________________________________________

# Next

[Path Parameters](04_path_parameters.md)
