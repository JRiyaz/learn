# Dependency Injection

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `08_dependency_injection.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Dependency Injection (DI) is
- Why Dependency Injection is Important
- The `Depends()` Function
- Dependency Resolution
- Reusable Dependencies
- Nested Dependencies
- Dependency Lifecycle
- Real-world Use Cases
- Common Mistakes
- Production Best Practices

______________________________________________________________________

# What is Dependency Injection?

Dependency Injection (DI) is a design pattern where an object receives the resources it needs instead of creating them
itself.

Instead of

```
Route

↓

Creates Database

↓

Creates Logger

↓

Creates Authentication
```

Use

```
Route

↓

Receives Database

↓

Receives Logger

↓

Receives Authentication
```

______________________________________________________________________

# Why Do We Need Dependency Injection?

Imagine every route does this:

```python
@app.get("/users")

def get_users():

    db = Database()

    logger = Logger()

    auth = AuthService()

    ...
```

Problems

- Duplicate code
- Difficult testing
- Tight coupling
- Poor maintainability

______________________________________________________________________

# Better Approach

```
Database

↓

Dependency

↓

FastAPI

↓

Inject

↓

Route
```

The route focuses only on business logic.

______________________________________________________________________

# What is Depends()?

FastAPI provides the `Depends()` function to declare dependencies.

Example

```python
from fastapi import Depends
```

______________________________________________________________________

# First Dependency

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

Response

```json
{
    "message": "Hello"
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

Route Function
```

FastAPI automatically executes the dependency.

______________________________________________________________________

# Real Database Example

Instead of

```python
db = Database()
```

Create

```python
def get_db():

    return Database()
```

Use

```python
@app.get("/users")

def users(

    db = Depends(

        get_db

    )

):

    ...
```

The route never creates the database connection directly.

______________________________________________________________________

# Why is This Better?

Without DI

```
Route

↓

Database

↓

Hard-Coded
```

With DI

```
Route

↓

Abstract Dependency

↓

Reusable
```

______________________________________________________________________

# Multiple Dependencies

Example

```python
@app.get("/users")

def users(

    db = Depends(get_db),

    logger = Depends(get_logger)

):

    ...
```

FastAPI resolves both dependencies automatically.

______________________________________________________________________

# Dependency Resolution Order

Example

```
Request

↓

Dependency A

↓

Dependency B

↓

Route
```

Dependencies are resolved before the route executes.

______________________________________________________________________

# Nested Dependencies

Dependencies can depend on other dependencies.

Example

```
Route

↓

Current User

↓

Database

↓

Database Session
```

This creates a dependency graph.

______________________________________________________________________

# Example

```python
def get_db():

    ...
```

```python
def get_user(

    db = Depends(get_db)

):

    ...
```

```python
@app.get("/profile")

def profile(

    user = Depends(get_user)

):

    ...
```

Flow

```
get_db()

↓

get_user()

↓

profile()
```

______________________________________________________________________

# Request Lifecycle

For each request

```
Request

↓

Resolve Dependencies

↓

Execute Route

↓

Cleanup
```

Dependencies are request-scoped by default.

______________________________________________________________________

# Cleanup with yield

Some resources must be cleaned up.

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
Create DB

↓

Route

↓

Close DB
```

This is the recommended pattern for database sessions.

______________________________________________________________________

# Why yield?

Without cleanup

```
Database Open

↓

Never Closed
```

With `yield`

```
Open

↓

Use

↓

Close
```

This prevents resource leaks.

______________________________________________________________________

# Authentication Dependency

Example

```python
def get_current_user():

    ...
```

Use

```python
@app.get("/profile")

def profile(

    user = Depends(

        get_current_user

    )

):

    ...
```

Authentication logic is reused across endpoints.

______________________________________________________________________

# Logging Dependency

Example

```python
def get_logger():

    return logger
```

Routes receive the logger instead of creating one.

______________________________________________________________________

# Configuration Dependency

```python
def get_settings():

    return settings
```

Useful for

- Database URLs
- API Keys
- Feature Flags

______________________________________________________________________

# Dependency vs Middleware

Dependency

```
Runs

Only

When Needed
```

Middleware

```
Runs

For Every Request
```

Example

Authentication

```
Dependency
```

Request Logging

```
Middleware
```

Choose based on scope.

______________________________________________________________________

# Dependency Caching

FastAPI caches dependency results during a single request.

Example

```
Route

↓

Depends(get_db)

↓

Depends(get_user)

↓

get_db()

Runs Once
```

The same dependency isn't executed repeatedly during one request.

______________________________________________________________________

# Dependency Tree

```
Request

↓

Settings

↓

Database

↓

Repository

↓

Service

↓

Route
```

Complex applications may have many layers of dependencies.

______________________________________________________________________

# Common Use Cases

Dependencies commonly provide

- Database Sessions
- Authentication
- Authorization
- Configuration
- Logging
- Rate Limiting
- External API Clients

______________________________________________________________________

# Benefits

Dependency Injection provides

- Reusability
- Loose Coupling
- Easier Testing
- Cleaner Routes
- Better Maintainability
- Consistent Resource Management

______________________________________________________________________

# Common Mistakes

❌ Creating database connections inside routes

❌ Repeating authentication logic

❌ Using global mutable state unnecessarily

❌ Performing heavy computations inside dependencies that run every request

❌ Forgetting cleanup for long-lived resources

______________________________________________________________________

# Production Best Practices

- Use `Depends()` for reusable functionality.
- Keep dependencies focused on one responsibility.
- Use `yield` for resources that require cleanup.
- Keep business logic in services, not dependencies.
- Reuse authentication and database dependencies.
- Avoid unnecessary work inside dependencies.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is Dependency Injection considered one of FastAPI's most important features?**

### Answer

Dependency Injection separates resource creation from business logic.

Benefits include:

- Reduced code duplication.
- Cleaner route handlers.
- Easier unit testing through dependency overrides or mocks.
- Better separation of concerns.
- Consistent management of shared resources such as database sessions and authentication.

FastAPI's `Depends()` mechanism makes these patterns easy to implement while remaining explicit and type-safe.

______________________________________________________________________

# Summary

In this chapter you learned:

- Dependency Injection
- `Depends()`
- Dependency Resolution
- Nested Dependencies
- `yield`
- Dependency Cleanup
- Authentication Dependencies
- Database Dependencies
- Dependency Caching
- Production Best Practices

Dependency Injection is one of FastAPI's defining features and enables clean, modular, and testable application
architecture.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Dependency Injection?
1. Why is Dependency Injection useful?
1. What does `Depends()` do?

______________________________________________________________________

## Dependencies

4. How are dependencies resolved?
1. What is a nested dependency?
1. Why are dependencies reusable?

______________________________________________________________________

## Resource Management

7. Why is `yield` used in dependencies?
1. What happens after the `yield` statement completes?
1. Why is cleanup important for database sessions?

______________________________________________________________________

## Architecture

10. How is a dependency different from middleware?
01. What kinds of resources are commonly provided through dependencies?
01. Why should dependencies have a single responsibility?

______________________________________________________________________

## Testing

13. Why does Dependency Injection make testing easier?
01. How does loose coupling improve maintainability?

______________________________________________________________________

## Scenario-Based

15. Every route in your application creates its own database connection. How would you redesign the application using dependencies?
01. Your authentication logic is duplicated across 40 endpoints. How can `Depends()` simplify the codebase?
01. A dependency opens a file but never closes it. What changes would you make?
01. Both `get_current_user()` and `get_orders()` depend on the same database session. How does FastAPI avoid creating multiple database sessions during a single request?
01. Your application needs to provide a shared configuration object to many routes. Why is a dependency a better solution than repeatedly constructing the configuration inside each endpoint?
01. A teammate puts complex business logic inside a dependency instead of a service layer. Why can this make the architecture harder to maintain?

______________________________________________________________________

# Next

[Pydantic Models](09_pydantic_models.md)
