# Dependency Injection

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 7 - Dependency Injection
>
> **File:** `26_dependency_injection.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Dependency Injection (DI) is
- Why Dependency Injection is Needed
- The `Depends()` Function
- Dependency Lifecycle
- Nested Dependencies
- Reusable Dependencies
- Dependency Caching
- Dependency Scope
- Common Use Cases
- Production Best Practices

______________________________________________________________________

# What is Dependency Injection?

Dependency Injection (DI) is a design pattern where FastAPI **provides required objects or values** to your route
functions automatically.

Instead of creating dependencies yourself,

FastAPI creates and injects them.

Without DI

```
Route

↓

Create Database

↓

Authenticate User

↓

Business Logic
```

With DI

```
Route

↓

Depends()

↓

Ready-to-use Objects
```

______________________________________________________________________

# Why Do We Need Dependency Injection?

Imagine every endpoint requires

- Database Connection
- Current User
- Configuration
- Logger

Without DI

```python
@app.get("/users")

def users():

    db = Database()

    user = authenticate()

    ...
```

Repeated everywhere.

______________________________________________________________________

# With Dependency Injection

```python
@app.get("/users")

def users(

    db = Depends(

        get_db

    ),

    user = Depends(

        get_current_user

    )

):

    ...
```

Cleaner,

reusable,

testable.

______________________________________________________________________

# Import

```python
from fastapi import Depends
```

______________________________________________________________________

# Creating a Dependency

Example

```python
def get_message():

    return "Hello"
```

Use it

```python
@app.get("/")

def home(

    message: str = Depends(

        get_message

    )

):

    return {

        "message": message

    }
```

______________________________________________________________________

# Internal Flow

```
Request

↓

Dependency

↓

Return Value

↓

Route
```

The route receives the dependency's return value.

______________________________________________________________________

# Dependency Lifecycle

```
HTTP Request

↓

Dependency Created

↓

Route Executes

↓

Response

↓

Cleanup (if needed)
```

Dependencies can also manage resources that require cleanup.

______________________________________________________________________

# Dependency with Parameters

Example

```python
def get_limit():

    return 100
```

```python
@app.get("/items")

def items(

    limit: int = Depends(

        get_limit

    )

):

    ...
```

______________________________________________________________________

# Reusable Dependencies

One dependency

```
Database

↓

Users Route

↓

Orders Route

↓

Products Route
```

Write once,

reuse everywhere.

______________________________________________________________________

# Authentication Example

```python
def get_current_user():

    return {

        "username": "riyaz"
    }
```

```python
@app.get("/profile")

def profile(

    user = Depends(

        get_current_user

    )

):

    return user
```

Every protected endpoint can reuse the same dependency.

______________________________________________________________________

# Database Dependency

```python
def get_db():

    db = Database()

    return db
```

Instead of creating a database connection inside every route,

inject it automatically.

______________________________________________________________________

# Dependency Chain

Dependencies can depend on other dependencies.

Example

```
Route

↓

Current User

↓

Database
```

FastAPI resolves the chain automatically.

______________________________________________________________________

# Nested Dependency Example

```python
def get_db():

    ...

def get_user(

    db = Depends(

        get_db

    )

):

    ...
```

Route

```python
@app.get("/")

def home(

    user = Depends(

        get_user

    )

):

    ...
```

Flow

```
Route

↓

get_user()

↓

get_db()
```

______________________________________________________________________

# Dependency Graph

```
Route

↓

User Dependency

↓

Database Dependency

↓

Configuration Dependency
```

FastAPI builds and resolves the graph automatically.

______________________________________________________________________

# Dependency Caching

Within a single request,

FastAPI caches dependency results.

Example

```
Route

↓

Depends(get_db)

↓

Called Once
```

Even if multiple dependencies require the same `get_db()` result,

it is reused by default.

______________________________________________________________________

# Why Caching Matters

Without caching

```
Route

↓

Database

↓

Database

↓

Database
```

Three connections.

With caching

```
Route

↓

Database

↓

Shared Instance
```

More efficient.

______________________________________________________________________

# Yield Dependencies

Some resources require cleanup.

Example

```python
def get_db():

    db = Database()

    try:

        yield db

    finally:

        db.close()
```

Flow

```
Create

↓

Route

↓

Cleanup
```

Ideal for database sessions.

______________________________________________________________________

# Dependency Scope

Dependencies typically exist for

```
One Request
```

Every new request gets a fresh dependency instance,

unless explicitly managed otherwise.

______________________________________________________________________

# Global Dependencies

Apply to the entire application.

Example

```python
app = FastAPI(

    dependencies=[

        Depends(

            verify_api_key

        )

    ]
)
```

Every endpoint executes the dependency.

______________________________________________________________________

# Router Dependencies

```python
router = APIRouter(

    dependencies=[

        Depends(

            authenticate

        )

    ]
)
```

All routes in that router are protected.

______________________________________________________________________

# Decorator vs Dependency

Bad

```python
@app.get("/")

def home():

    authenticate()

    ...
```

Good

```python
@app.get("/")

def home(

    user = Depends(

        authenticate

    )

):

    ...
```

The route declares its requirements explicitly.

______________________________________________________________________

# Dependency vs Middleware

Middleware

```
Runs

Every Request
```

Dependency

```
Runs

Only

Where Declared
```

Examples

Middleware

- Logging
- Metrics
- CORS

Dependencies

- Authentication
- Database
- Current User

______________________________________________________________________

# Common Use Cases

Dependencies commonly provide

- Database Sessions
- Current User
- API Keys
- Configuration
- Logger
- Tenant Information
- Pagination Defaults

______________________________________________________________________

# Architecture

```
Client

↓

Route

↓

Dependency

↓

Service

↓

Repository

↓

Database
```

Dependencies prepare resources.

Services perform business logic.

______________________________________________________________________

# Common Mistakes

❌ Creating database connections directly in routes

❌ Duplicating authentication code

❌ Using middleware instead of dependencies for request-specific resources

❌ Ignoring dependency cleanup

❌ Writing business logic inside dependencies

______________________________________________________________________

# Production Best Practices

- Keep dependencies focused on resource acquisition.
- Reuse dependencies across routes.
- Use `yield` for resources requiring cleanup.
- Let services contain business logic.
- Use router-level dependencies for shared authentication.
- Take advantage of dependency caching.
- Keep dependency functions small and testable.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is Dependency Injection considered one of FastAPI's most powerful features?**

### Answer

Dependency Injection promotes modular, reusable, and testable code.

Benefits include:

- Eliminates duplicated setup code.
- Simplifies authentication.
- Manages database sessions cleanly.
- Supports automatic dependency resolution.
- Provides request-scoped caching.
- Makes unit testing easier by allowing dependencies to be replaced or overridden.

As applications grow, dependency injection helps maintain a clean separation of concerns.

______________________________________________________________________

# Summary

In this chapter you learned:

- Dependency Injection
- `Depends()`
- Dependency Lifecycle
- Nested Dependencies
- Dependency Caching
- Yield Dependencies
- Global Dependencies
- Router Dependencies
- Production Best Practices

Dependency Injection is one of FastAPI's defining features, enabling clean architecture, resource management, and
reusable request-scoped components with minimal boilerplate.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Dependency Injection?
1. Why is Dependency Injection useful?
1. What does `Depends()` do?

______________________________________________________________________

## Dependencies

4. How do you create a dependency?
1. How are dependencies injected into routes?
1. What is a nested dependency?

______________________________________________________________________

## Lifecycle

7. Why are `yield` dependencies useful?
1. When does dependency cleanup occur?
1. How does dependency caching work?

______________________________________________________________________

## Architecture

10. Why should authentication be implemented as a dependency?
01. Why should database sessions be injected instead of created in routes?
01. What responsibilities belong in dependencies versus services?

______________________________________________________________________

## Comparison

13. What is the difference between middleware and dependencies?
01. When should global dependencies be used?
01. When should router-level dependencies be used?

______________________________________________________________________

## Scenario-Based

16. Every endpoint in your application opens a new database connection manually. How can dependency injection improve this design?
01. Your authentication logic is duplicated across dozens of routes. How would `Depends()` simplify the codebase?
01. A dependency creates a database session but never closes it. What problems could this cause, and how would you fix it?
01. Two different dependencies both require access to the same database session during one request. How does FastAPI avoid creating multiple sessions?
01. Your application needs to replace the real database with a mock implementation during unit testing. How does dependency injection make this easier?

______________________________________________________________________

# Next

[Dependency Overrides & Testing](27_dependency_overrides_testing.md)
