# 15. FastAPI Dependency Injection, Middleware & Errors

**Previous:** [14. FastAPI Fundamentals](./14-fastapi-core.md)

**Next:** [16. Production FastAPI](./16-production-fastapi.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain FastAPI dependency injection and why it is useful.
- Define reusable dependencies with `Depends`.
- Understand nested dependencies and dependency graphs.
- Use dependencies for authentication, database access and shared request logic.
- Override dependencies in tests.
- Understand FastAPI middleware and its position in the request lifecycle.
- Distinguish middleware from dependencies.
- Create custom exception classes.
- Register exception handlers.
- Understand validation errors and how to expose consistent API errors.
- Test endpoints that use dependencies.
- Design dependency structures that remain maintainable as an application grows.
- Answer senior-level FastAPI DI, middleware and error-handling questions.

______________________________________________________________________

# 1. What Is Dependency Injection?

Dependency injection means providing an object or service that another piece of code needs instead of making that code
construct the dependency itself.

Without dependency injection:

```python
async def get_user():
    db = Database()
    ...
```

The function creates its own dependency.

With dependency injection:

```python
async def get_user(db=Depends(get_db)):
    ...
```

The framework supplies the dependency.

This improves:

- Reuse
- Testability
- Separation of concerns
- Configuration
- Composition

______________________________________________________________________

# 2. `Depends`

FastAPI provides `Depends` for declaring dependencies.

Example:

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_config():
    return {"environment": "production"}


@app.get("/health")
def health(config=Depends(get_config)):
    return config
```

FastAPI resolves `get_config()` before invoking the endpoint.

______________________________________________________________________

# 3. Dependency as a Function

A dependency can be a normal function:

```python
def get_settings():
    return settings
```

It can also be asynchronous:

```python
async def get_current_user():
    ...
```

FastAPI handles the dependency according to whether it is synchronous or asynchronous.

______________________________________________________________________

# 4. Why Dependency Injection Is Useful

Imagine many endpoints need:

- Database session
- Current user
- Configuration
- Tenant information
- Permission checks
- Request metadata

Without DI, each endpoint may duplicate setup logic.

With DI:

```text
Endpoint
   ↓
Dependency
   ↓
Shared resource
```

The dependency can be reused across many endpoints.

______________________________________________________________________

# 5. Database Dependency

A common FastAPI pattern is:

```python
async def get_db():
    db = create_session()
    try:
        yield db
    finally:
        await db.close()
```

Then:

```python
@app.get("/users")
async def users(db=Depends(get_db)):
    ...
```

The dependency manages the resource lifecycle.

______________________________________________________________________

# 6. Dependencies Using `yield`

Dependencies can use `yield` when setup and cleanup are needed.

Conceptually:

```text
Create resource
      ↓
yield resource
      ↓
Endpoint executes
      ↓
Cleanup
```

Example:

```python
def get_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)
```

This pattern is useful for:

- Database sessions
- Temporary resources
- Context-like setup/cleanup

______________________________________________________________________

# 7. Dependency Graphs

Dependencies can depend on other dependencies.

Example:

```python
def get_db():
    ...


def get_repository(db=Depends(get_db)):
    ...


def get_service(repo=Depends(get_repository)):
    ...


@app.get("/users")
async def users(service=Depends(get_service)):
    ...
```

The dependency graph is:

```text
Endpoint
   ↓
Service
   ↓
Repository
   ↓
Database
```

FastAPI resolves the graph before calling the endpoint.

______________________________________________________________________

# 8. Nested Dependencies

Nested dependencies allow each layer to declare what it needs.

For example:

```python
def get_current_user(token=Depends(get_token)):
    ...


def require_admin(user=Depends(get_current_user)):
    ...


@app.delete("/users/{user_id}")
async def delete_user(
    user=Depends(require_admin),
):
    ...
```

The endpoint does not need to know how authentication and authorization are implemented.

______________________________________________________________________

# 9. Authentication Dependency

Authentication is a common use case for dependencies.

Conceptually:

```text
Request
   ↓
Authentication dependency
   ↓
Current user
   ↓
Endpoint
```

Example:

```python
async def get_current_user(
    token=Depends(oauth2_scheme),
):
    return validate_token(token)
```

Then:

```python
@app.get("/profile")
async def profile(user=Depends(get_current_user)):
    return user
```

______________________________________________________________________

# 10. Authorization Dependency

Authentication identifies the caller.

Authorization determines whether the caller has permission.

A dependency can enforce authorization:

```python
async def require_admin(
    user=Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )
    return user
```

Then:

```python
@app.delete("/users/{user_id}")
async def delete_user(
    user=Depends(require_admin),
):
    ...
```

______________________________________________________________________

# 11. Dependency Composition

Good dependencies tend to have one clear responsibility.

For example:

```text
get_token
    ↓
get_current_user
    ↓
require_admin
    ↓
endpoint
```

This is easier to reason about than one dependency performing:

```text
token parsing
database setup
authorization
business logic
email sending
```

all at once.

______________________________________________________________________

# 12. Dependency Scope and Caching

FastAPI can cache dependency results within a request.

If multiple parts of the dependency graph request the same dependency, FastAPI can reuse the resolved value for that
request by default.

Conceptually:

```text
Endpoint A
   ↓
get_current_user
   ↑
Endpoint dependency graph
```

The same resolved dependency can be reused rather than recomputed unnecessarily.

Dependency behavior can be configured when required.

______________________________________________________________________

# 13. When Dependency Caching Matters

Caching within a request is useful when a dependency:

- Performs database work
- Parses authentication
- Loads configuration
- Creates a shared request-scoped object

Be careful when a dependency must intentionally execute multiple times.

FastAPI's dependency options allow controlling caching behavior where necessary.

______________________________________________________________________

# 14. Dependency Overrides

FastAPI supports dependency overrides, which are particularly useful for testing.

Example:

```python
app.dependency_overrides[get_db] = override_get_db
```

A test can replace a production dependency with a controlled test dependency.

For example:

```text
Production:
Endpoint → Real DB

Test:
Endpoint → Test DB
```

______________________________________________________________________

# 15. Why Dependency Overrides Matter

Suppose an endpoint depends on:

```python
get_current_user
```

A test should not necessarily need to:

- Generate real authentication tokens
- Call a real identity provider
- Perform unnecessary authentication infrastructure work

Instead, the test can override the dependency and provide a known user.

This makes tests:

- Faster
- More deterministic
- Easier to write

______________________________________________________________________

# 16. Dependency Override Cleanup

Overrides are application-level configuration.

Tests should restore or clear overrides after use.

Example:

```python
app.dependency_overrides[get_db] = override_get_db

try:
    ...
finally:
    app.dependency_overrides.clear()
```

This prevents one test's configuration from leaking into another.

______________________________________________________________________

# 17. Testing Authentication Dependencies

Instead of testing every endpoint through the complete authentication stack, endpoint tests can override the
current-user dependency.

For example:

```python
async def override_current_user():
    return User(id=1, is_admin=True)


app.dependency_overrides[get_current_user] = override_current_user
```

Then the endpoint can be tested independently of token infrastructure.

Authentication itself should still have dedicated tests.

______________________________________________________________________

# 18. Dependency Injection vs Global State

A dependency is often preferable to a global mutable object.

Global state can cause:

- Difficult tests
- Hidden coupling
- Initialization-order problems
- Concurrency issues
- Configuration complexity

DI makes dependencies explicit.

______________________________________________________________________

# 19. What Is Middleware?

Middleware is code that runs around request processing.

Conceptually:

```text
Request
   ↓
Middleware
   ↓
Application
   ↓
Middleware
   ↓
Response
```

It is suitable for behavior that applies broadly across requests.

______________________________________________________________________

# 20. Middleware Execution

Conceptually:

```text
Request
 ↓
Middleware A
 ↓
Middleware B
 ↓
Endpoint
 ↑
Middleware B
 ↑
Middleware A
 ↑
Response
```

The order matters.

Middleware can perform work before and after the downstream application.

______________________________________________________________________

# 21. Common Middleware Use Cases

Middleware is commonly used for:

- Request IDs
- Logging
- Timing
- Metrics
- CORS
- Security headers
- Request/response processing
- Global error handling
- Tracing

______________________________________________________________________

# 22. Simple Middleware

FastAPI/Starlette supports middleware using decorators or middleware classes.

A simple example:

```python
@app.middleware("http")
async def log_request(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start
    logger.info(
        "request completed",
        extra={"duration": duration},
    )

    return response
```

The middleware executes around the request.

______________________________________________________________________

# 23. Middleware vs Dependency

This is an important interview distinction.

### Middleware

Best for cross-cutting behavior that applies broadly.

Examples:

```text
request ID
logging
metrics
CORS
```

### Dependency

Best for endpoint-related reusable logic.

Examples:

```text
current user
database session
permissions
tenant
```

______________________________________________________________________

# 24. Example: Request ID

Middleware can generate or propagate a request ID:

```text
Incoming request
      ↓
Request ID middleware
      ↓
request.state.request_id
      ↓
Endpoint
      ↓
Logs
```

This allows application logs to correlate events belonging to the same request.

______________________________________________________________________

# 25. Middleware and Exceptions

Middleware can observe exceptions raised by downstream processing.

A simplified structure:

```text
Middleware
   ↓
Route
   ↓
Exception
   ↑
Middleware/error handling
```

The exact behavior depends on middleware order and the framework's exception-handling stack.

______________________________________________________________________

# 26. What Is an Exception?

An exception represents an abnormal condition in application execution.

Examples:

```python
ValueError
PermissionError
DatabaseError
TimeoutError
```

Backend applications should translate internal failures into appropriate API responses.

______________________________________________________________________

# 27. `HTTPException`

FastAPI provides `HTTPException` for common HTTP-level errors.

Example:

```python
from fastapi import HTTPException


if user is None:
    raise HTTPException(
        status_code=404,
        detail="User not found",
    )
```

This communicates an HTTP error to the client.

______________________________________________________________________

# 28. Custom Exceptions

For domain-specific errors, define application exceptions.

Example:

```python
class UserNotFoundError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass
```

The service layer can raise them without knowing HTTP details.

______________________________________________________________________

# 29. Why Custom Exceptions?

Consider:

```python
async def transfer_money(...):
    if balance < amount:
        raise InsufficientBalanceError()
```

The service does not need to know that the API should return:

```text
409 Conflict
```

An exception handler can translate the domain error into an HTTP response.

This keeps domain logic separate from transport concerns.

______________________________________________________________________

# 30. Exception Handlers

FastAPI allows custom exception handlers.

Conceptually:

```python
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"},
    )
```

Then:

```text
Domain exception
      ↓
Exception handler
      ↓
HTTP response
```

______________________________________________________________________

# 31. Centralized Error Handling

A consistent API should avoid every endpoint manually formatting errors.

Instead:

```text
Service
  ↓
Domain exception
  ↓
Global handler
  ↓
Standard API error
```

This creates a consistent contract.

______________________________________________________________________

# 32. Error Response Format

A project may standardize errors:

```json
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User not found",
        "request_id": "abc-123"
    }
}
```

The exact format is an application design choice.

The important principle is consistency.

______________________________________________________________________

# 33. Validation Errors

FastAPI validates incoming request data.

Invalid input can result in a validation error response.

For example:

```text
GET /users/abc
```

when:

```python
user_id: int
```

is expected.

Or a request body can fail model validation.

Validation errors should be distinguishable from internal server errors.

______________________________________________________________________

# 34. Handling Validation Errors

FastAPI/Starlette provide exception handling mechanisms for validation errors.

You can customize the response when the application's API contract requires a specific error format.

For example:

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    ...
```

Do not hide useful validation details unnecessarily.

______________________________________________________________________

# 35. Internal Errors

Unexpected exceptions should not expose internal implementation details.

Avoid returning:

```text
database password
SQL query internals
stack trace
secret keys
internal infrastructure information
```

to clients.

Instead, return a controlled server error and log the detailed exception internally.

______________________________________________________________________

# 36. Logging Exceptions

When an unexpected error occurs, logs should contain enough information for debugging.

Useful context includes:

- Request ID
- Endpoint
- HTTP method
- Error type
- Stack trace
- Relevant non-sensitive identifiers

Do not log secrets or sensitive data unnecessarily.

______________________________________________________________________

# 37. Exception Boundaries

A useful architecture is:

```text
Router
 ↓
Service
 ↓
Repository
 ↓
Database
```

Errors can be translated at appropriate boundaries.

For example:

```text
DatabaseError
   ↓
Repository/Service
   ↓
Domain-specific exception
   ↓
HTTP exception handler
   ↓
API response
```

Do not blindly catch every exception at every layer.

______________________________________________________________________

# 38. Avoid Broad Exception Catching

This is dangerous:

```python
try:
    ...
except Exception:
    return {"error": "something went wrong"}
```

Problems:

- Hides programming bugs
- Loses stack traces
- Makes debugging difficult
- Can return incorrect status codes

Catch exceptions when you have a meaningful recovery or translation strategy.

______________________________________________________________________

# 39. Error Translation

A good boundary translates errors appropriately.

Example:

```text
Database duplicate-key error
        ↓
Repository/service recognizes conflict
        ↓
ResourceAlreadyExistsError
        ↓
Exception handler
        ↓
409 Conflict
```

This keeps database implementation details away from API clients.

______________________________________________________________________

# 40. Dependency Errors

Dependencies can also fail.

For example:

```text
Request
 ↓
Authentication dependency
 ↓
Token invalid
```

The dependency can raise an authentication-related exception.

The request should stop rather than executing protected business logic.

______________________________________________________________________

# 41. Nested Dependency Failure

Consider:

```text
Endpoint
  ↓
require_admin
  ↓
get_current_user
  ↓
get_token
```

If `get_token` fails:

```text
get_current_user
```

cannot resolve.

Therefore:

```text
require_admin
```

and the endpoint do not execute normally.

Understanding dependency graphs is important for debugging.

______________________________________________________________________

# 42. Dependency Override Architecture

A maintainable application can define dependencies such as:

```text
get_settings
get_db
get_current_user
get_repository
get_service
```

Tests can override selected nodes:

```text
Production:

Endpoint
 ↓
Service
 ↓
Repository
 ↓
Real DB

Test:

Endpoint
 ↓
Service
 ↓
Repository
 ↓
Test DB
```

or replace a higher-level dependency when appropriate.

______________________________________________________________________

# 43. Dependency Testing Strategy

Test dependencies at multiple levels.

### Unit tests

Test the dependency's own logic.

### Integration tests

Test dependency interaction with real infrastructure where appropriate.

### Endpoint tests

Override expensive/external dependencies to isolate API behavior.

Do not use overrides as a reason to never test the real integration.

______________________________________________________________________

# 44. Middleware Testing Strategy

Middleware should be tested for:

- Request processing
- Response processing
- Headers
- Request IDs
- Timing
- Exception behavior
- Edge cases

Example:

```text
Request
 ↓
Middleware
 ↓
Test endpoint
 ↓
Response
```

Assert the middleware's externally observable behavior.

______________________________________________________________________

# 45. Middleware Performance

Middleware runs for many requests.

Avoid expensive work such as:

```text
large database query
external API call
CPU-heavy calculation
```

unless the middleware genuinely requires it.

A small inefficiency multiplied by every request can become a major production cost.

______________________________________________________________________

# 46. Middleware Ordering Example

Suppose:

```text
Request ID middleware
Authentication middleware
Logging middleware
Endpoint
```

If logging needs the request ID, request-ID processing should occur early enough for the logging layer to access it.

Design middleware order based on dependencies between cross-cutting concerns.

______________________________________________________________________

# 47. Authentication: Middleware or Dependency?

For endpoint-specific authorization, dependencies are often a better fit.

For broad request processing, middleware may be appropriate.

Example:

```text
Middleware:
  Generate request ID
  Add tracing context

Dependency:
  Parse authentication
  Load current user
  Check permissions
```

This is not an absolute rule; architecture depends on the application's needs.

______________________________________________________________________

# 48. Exception Handler vs Middleware

Use an exception handler when you want to map a particular exception type to a response.

Use middleware when you need broad request/response processing or cross-cutting behavior.

For example:

```text
Custom domain exception
       ↓
Exception handler
       ↓
409 response
```

while:

```text
Every request
       ↓
Timing middleware
       ↓
Endpoint
       ↓
Response
```

______________________________________________________________________

# 49. Lifespan and Dependencies

Application-wide resources such as:

- Database engines
- HTTP clients
- Connection pools
- Configuration

often have application-level lifecycles.

Do not create expensive application-wide resources repeatedly inside request dependencies unless there is a deliberate
reason.

A dependency can retrieve a shared application resource while still managing request-specific resources separately.

______________________________________________________________________

# 50. Common FastAPI DI and Error-Handling Mistakes

## Mistake 1 — One giant dependency

Avoid a dependency that handles:

```text
authentication
authorization
database
business logic
logging
```

Keep dependencies focused.

______________________________________________________________________

## Mistake 2 — Using middleware for everything

Not every reusable operation belongs in middleware.

Endpoint-specific dependencies are often clearer as FastAPI dependencies.

______________________________________________________________________

## Mistake 3 — Returning raw internal exceptions

Do not expose internal stack traces or database errors to clients.

______________________________________________________________________

## Mistake 4 — Catching `Exception` everywhere

This hides bugs and makes observability worse.

______________________________________________________________________

## Mistake 5 — Forgetting dependency override cleanup

Test overrides can leak between tests.

______________________________________________________________________

## Mistake 6 — Doing expensive work in middleware

Middleware executes broadly and can become a system-wide bottleneck.

______________________________________________________________________

# 51. Interview Questions & Answers

## Q1. What is dependency injection?

**Answer:**

Dependency injection means providing an object or service to a component instead of having that component construct the
dependency itself.

FastAPI uses `Depends` to declare and resolve dependencies.

______________________________________________________________________

## Q2. Why is dependency injection useful?

**Answer:**

It improves reuse, testability, separation of concerns and configuration.

It also makes dependencies explicit.

______________________________________________________________________

## Q3. What is `Depends`?

**Answer:**

`Depends` declares that an endpoint or another dependency requires a value produced by a dependency function.

FastAPI resolves the dependency before executing the dependent callable.

______________________________________________________________________

## Q4. Can dependencies be asynchronous?

**Answer:**

Yes.

Dependencies can be synchronous or asynchronous, and FastAPI handles them according to their callable type.

______________________________________________________________________

## Q5. What are nested dependencies?

**Answer:**

A dependency can itself depend on other dependencies.

For example:

```text
Endpoint
 ↓
Authorization
 ↓
Authentication
 ↓
Token extraction
```

FastAPI resolves the dependency graph.

______________________________________________________________________

## Q6. What is a `yield` dependency?

**Answer:**

It is a dependency that can perform setup before `yield` and cleanup afterward.

It is useful for resources such as database sessions.

______________________________________________________________________

## Q7. Why use `yield` for database dependencies?

**Answer:**

It allows the dependency to acquire a session before the endpoint and reliably release/close it afterward.

______________________________________________________________________

## Q8. What are dependency overrides?

**Answer:**

They allow tests or other controlled environments to replace an application's normal dependency with an alternative
implementation.

______________________________________________________________________

## Q9. Why are dependency overrides useful in tests?

**Answer:**

They let tests replace real databases, authentication systems or external services with deterministic test
implementations.

______________________________________________________________________

## Q10. Why should dependency overrides be cleaned up?

**Answer:**

Because overrides are application configuration and can affect subsequent tests if they are left installed.

______________________________________________________________________

## Q11. What is middleware?

**Answer:**

Middleware is code that wraps request/response processing and is commonly used for cross-cutting concerns.

______________________________________________________________________

## Q12. Give examples of middleware use cases.

**Answer:**

Examples include:

- Logging
- Request IDs
- Metrics
- CORS
- Tracing
- Security headers
- Request timing

______________________________________________________________________

## Q13. Middleware vs dependency?

**Answer:**

Middleware is generally appropriate for broad cross-cutting request/response behavior.

Dependencies are generally better for reusable endpoint-related logic such as authentication, authorization, database
sessions and current-user resolution.

______________________________________________________________________

## Q14. Why does middleware order matter?

**Answer:**

Middleware wraps downstream processing, so changing the order changes which middleware executes first and which context
is available to other middleware.

______________________________________________________________________

## Q15. What is `HTTPException`?

**Answer:**

It is a FastAPI mechanism for raising an HTTP-level error response, such as 404 or 403.

______________________________________________________________________

## Q16. Why use custom exceptions?

**Answer:**

Custom exceptions allow domain/service code to express meaningful failures without coupling business logic directly to
HTTP response details.

______________________________________________________________________

## Q17. What is an exception handler?

**Answer:**

An exception handler maps a particular exception type to an HTTP response.

______________________________________________________________________

## Q18. Why centralize exception handling?

**Answer:**

It creates consistent API error responses and prevents every endpoint from duplicating error formatting.

______________________________________________________________________

## Q19. How should validation errors be handled?

**Answer:**

They should return a clear client-facing validation response while preserving enough detail for the client to correct
the request.

Applications can customize FastAPI's validation exception handling when a standardized error contract is required.

______________________________________________________________________

## Q20. Why shouldn't internal exceptions be returned directly?

**Answer:**

They can expose implementation details, stack traces, database information or secrets and create an unstable API
contract.

______________________________________________________________________

## Q21. Why is `except Exception` dangerous?

**Answer:**

It can hide programming bugs, destroy useful debugging information and incorrectly convert unrelated failures into
generic responses.

______________________________________________________________________

## Q22. How would you map a business exception to HTTP?

**Answer:**

Define a domain exception such as:

```python
class UserNotFoundError(Exception):
    pass
```

Then register an exception handler that converts it into the appropriate HTTP response.

______________________________________________________________________

## Q23. How would you test an authenticated endpoint?

**Answer:**

Override the authentication/current-user dependency with a controlled test dependency, then separately test the actual
authentication implementation.

______________________________________________________________________

## Q24. How would you test a database dependency?

**Answer:**

Override the production database dependency with a test database/session or controlled repository implementation,
depending on the test level.

______________________________________________________________________

## Q25. Can a dependency depend on another dependency?

**Answer:**

Yes.

This is one of the core features of FastAPI's dependency system.

______________________________________________________________________

## Q26. What happens if a nested dependency fails?

**Answer:**

FastAPI cannot resolve the dependent dependency/endpoint normally, so the endpoint execution is stopped and the
resulting exception/error is handled according to the application's exception handling.

______________________________________________________________________

## Q27. Should authentication be middleware or a dependency?

**Answer:**

For endpoint-specific authentication and authorization, dependencies are often clearer because they integrate naturally
with route requirements.

Middleware can still be useful for broad authentication-related processing or request context.

______________________________________________________________________

## Q28. What should go into middleware?

**Answer:**

Cross-cutting behavior that applies broadly across requests, such as request IDs, tracing, metrics, CORS and request
timing.

______________________________________________________________________

## Q29. What should not go into middleware?

**Answer:**

Endpoint-specific business rules and expensive operations that do not need to execute for every request.

______________________________________________________________________

## Q30. Why can middleware become a performance bottleneck?

**Answer:**

It can execute for a large percentage of requests, so even small amounts of unnecessary work are multiplied across the
entire service.

______________________________________________________________________

## Q31. How do dependencies help separation of concerns?

**Answer:**

They allow endpoint code to declare what it needs without embedding setup and shared logic directly inside the route
handler.

______________________________________________________________________

## Q32. How would you design a clean authentication dependency chain?

**Answer:**

A possible chain is:

```text
token extraction
      ↓
token validation
      ↓
current user
      ↓
authorization check
      ↓
endpoint
```

Each dependency has a focused responsibility.

______________________________________________________________________

## Q33. How do you standardize API errors?

**Answer:**

Define a consistent error schema and map known domain/validation/authentication exceptions to that schema through
centralized exception handlers.

______________________________________________________________________

## Q34. How would you debug an endpoint that suddenly returns 500?

**Answer:**

Use the request ID to find the corresponding logs and trace.

Identify the exception and stack trace, determine the failing dependency/service/database operation and fix the
underlying issue rather than hiding it with a broad exception handler.

______________________________________________________________________

## Q35. How can timeout failures propagate through dependencies?

**Answer:**

A dependency may call a database or external service.

If that operation blocks or times out, the dependency can fail, preventing the endpoint from executing and potentially
consuming request resources until the timeout is reached.

______________________________________________________________________

# 52. Scenario-Based Questions

## Scenario 1 — Real Database in Unit Tests

Every endpoint test creates a connection to the production-like database.

**Question:** What would you change?

**Answer:**

Introduce a database dependency and override it in tests with a test database/session or controlled implementation.

Keep separate integration tests for the real database integration.

______________________________________________________________________

## Scenario 2 — Authentication in Every Route

Twenty endpoints repeat:

```python
token = ...
user = ...
validate_user(...)
```

**Question:** How would you improve this?

**Answer:**

Create a reusable authentication/current-user dependency and inject it into protected endpoints.

______________________________________________________________________

## Scenario 3 — Admin Authorization

Many endpoints require an admin user.

**Question:** Would you duplicate:

```python
if not user.is_admin:
    ...
```

in every route?

**Answer:**

Create a reusable authorization dependency such as:

```text
require_admin
```

that depends on the current-user dependency.

______________________________________________________________________

## Scenario 4 — Domain Exception

The service raises:

```python
UserNotFoundError
```

but the API currently returns 500.

**Question:** What would you do?

**Answer:**

Register an exception handler mapping `UserNotFoundError` to the appropriate API response, such as 404.

______________________________________________________________________

## Scenario 5 — Database Error Leakage

A duplicate-key database exception reaches the client with raw database details.

**Question:** What's wrong?

**Answer:**

Database implementation details should not become the API contract.

Translate the known persistence failure into a domain/application exception and return a controlled response.

______________________________________________________________________

## Scenario 6 — One Huge Middleware

A team creates middleware that:

```text
loads user
queries database
calls external API
calculates permissions
logs request
formats response
```

**Question:** What concerns do you have?

**Answer:**

It mixes unrelated responsibilities, runs expensive work broadly and makes testing/debugging harder.

Move endpoint-specific logic into focused dependencies/services and retain only true cross-cutting behavior in
middleware.

______________________________________________________________________

## Scenario 7 — Dependency Override Leaks

Test A overrides:

```python
get_db
```

Test B unexpectedly uses Test A's database.

**Question:** Why?

**Answer:**

The dependency override was not cleared after Test A.

Use fixture-based setup/teardown or explicit cleanup.

______________________________________________________________________

## Scenario 8 — Blocking Dependency

An async dependency performs:

```python
requests.get(...)
```

to an external service.

**Question:** What is the concern?

**Answer:**

The blocking call can block the event loop.

Use an async HTTP client or isolate the blocking operation appropriately.

______________________________________________________________________

## Scenario 9 — Middleware Adds 100 ms

Every API request is now approximately 100 ms slower after adding middleware.

**Question:** What would you investigate?

**Answer:**

Profile the middleware.

Determine whether it performs:

- Network calls
- Database operations
- Expensive serialization
- CPU-heavy processing
- Excessive logging

Because middleware runs broadly, the added latency affects the whole service.

______________________________________________________________________

## Scenario 10 — Validation Error Format

The frontend expects:

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "fields": {}
    }
}
```

but FastAPI returns its default validation structure.

**Question:** How would you handle it?

**Answer:**

Register an appropriate validation exception handler and translate validation details into the application's
standardized error schema.

______________________________________________________________________

# 53. Practice Exercises

## Exercise 1 — Basic Dependency

Create:

```python
get_settings()
```

and inject it into an endpoint.

______________________________________________________________________

## Exercise 2 — Database Dependency

Create a dependency that:

1. Creates a database session.
1. Yields it.
1. Closes it in `finally`.

Explain the lifecycle.

______________________________________________________________________

## Exercise 3 — Nested Dependencies

Implement:

```text
get_token
    ↓
get_current_user
    ↓
require_admin
    ↓
admin endpoint
```

Test both allowed and denied users.

______________________________________________________________________

## Exercise 4 — Dependency Override

Override the database dependency in tests.

Verify that the endpoint does not access the production database.

______________________________________________________________________

## Exercise 5 — Authentication Override

Override the current-user dependency.

Test:

```text
normal user
admin user
```

without generating real authentication tokens.

______________________________________________________________________

## Exercise 6 — Request-ID Middleware

Implement middleware that:

1. Reads an incoming request ID if available.
1. Generates one if absent.
1. Makes it available to the application.
1. Adds it to the response.
1. Logs it.

______________________________________________________________________

## Exercise 7 — Timing Middleware

Measure:

```text
request start
endpoint execution
response completion
```

Log the duration.

______________________________________________________________________

## Exercise 8 — Custom Exception

Create:

```python
class UserNotFoundError(Exception):
    pass
```

Raise it from the service layer and translate it into:

```text
404
```

using an exception handler.

______________________________________________________________________

## Exercise 9 — Standard Error Schema

Design a common error response:

```json
{
    "error": {
        "code": "...",
        "message": "...",
        "request_id": "..."
    }
}
```

Use it for at least:

```text
404
409
422
500
```

______________________________________________________________________

## Exercise 10 — Error Boundaries

Create a flow:

```text
Repository
 ↓
Database error
 ↓
Service/domain exception
 ↓
Exception handler
 ↓
HTTP response
```

Explain why each translation occurs at its boundary.

______________________________________________________________________

# 54. Quick Revision

| Concept | Key Point |
|---|---|
| Dependency Injection | Supply dependencies instead of constructing them inside consumers |
| `Depends` | Declares a FastAPI dependency |
| Nested dependency | Dependency can depend on another dependency |
| `yield` dependency | Supports setup + cleanup |
| Dependency graph | Resolved before endpoint execution |
| Dependency caching | Reuses dependency result within request by default |
| Dependency override | Replace dependency, especially in tests |
| Middleware | Wraps request/response processing |
| Middleware order | Determines execution/context order |
| Authentication | Identifies caller |
| Authorization | Checks permissions |
| `HTTPException` | Raises HTTP-level error |
| Custom exception | Represents domain/application failure |
| Exception handler | Maps exception to response |
| Validation error | Invalid API input |
| Centralized error handling | Consistent API error contract |
| Request ID | Correlates request activity |
| Broad exception catch | Often hides bugs |
| Middleware performance | Affects many/all requests |
| Dependency testing | Test independently and through endpoints |

______________________________________________________________________

# 55. Completion Checklist

Before moving to File 16, make sure you can explain:

- [ ] Dependency injection
- [ ] `Depends`
- [ ] Synchronous dependencies
- [ ] Asynchronous dependencies
- [ ] Database dependencies
- [ ] `yield` dependencies
- [ ] Dependency graphs
- [ ] Nested dependencies
- [ ] Authentication dependencies
- [ ] Authorization dependencies
- [ ] Dependency composition
- [ ] Dependency caching
- [ ] Dependency overrides
- [ ] Override cleanup
- [ ] Testing authentication dependencies
- [ ] DI vs global state
- [ ] Middleware
- [ ] Middleware execution
- [ ] Middleware use cases
- [ ] Middleware implementation
- [ ] Middleware vs dependency
- [ ] Request IDs
- [ ] Middleware exception behavior
- [ ] `HTTPException`
- [ ] Custom exceptions
- [ ] Exception handlers
- [ ] Centralized error handling
- [ ] Standard error responses
- [ ] Validation errors
- [ ] Internal error handling
- [ ] Exception logging
- [ ] Exception boundaries
- [ ] Avoiding broad exception catching
- [ ] Error translation
- [ ] Dependency failures
- [ ] Nested dependency failures
- [ ] Testing dependency overrides
- [ ] Testing middleware
- [ ] Middleware performance
- [ ] Middleware ordering
- [ ] Authentication middleware vs dependency
- [ ] Exception handler vs middleware
- [ ] Application-level resource lifecycle
- [ ] Common DI/error-handling mistakes

______________________________________________________________________

# 56. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is dependency injection?
1. Why is dependency injection useful?
1. What is `Depends`?
1. Can FastAPI dependencies be asynchronous?
1. What is a `yield` dependency?
1. Why is `yield` useful for database sessions?
1. What is a dependency graph?
1. What are nested dependencies?
1. How would you build an authentication dependency?
1. How would you build an authorization dependency?
1. What is dependency caching?
1. When might you disable dependency caching?
1. What are dependency overrides?
1. Why are dependency overrides useful in testing?
1. How should overrides be cleaned up?
1. How would you test an authenticated endpoint without real authentication?
1. What is middleware?
1. How does middleware execute around a request?
1. Why does middleware order matter?
1. Give five middleware use cases.
1. Middleware vs dependency?
1. How would you implement request-ID middleware?
1. How can middleware observe exceptions?
1. What is `HTTPException`?
1. When should you use custom exceptions?
1. What is an exception handler?
1. Why centralize exception handling?
1. How should validation errors be handled?
1. Why shouldn't internal exceptions be returned directly?
1. Why is `except Exception` dangerous?
1. How would you map a domain exception to an HTTP response?
1. How should database errors be translated?
1. What happens when a dependency fails?
1. What happens when a nested dependency fails?
1. Should authentication be middleware or a dependency?
1. What should go into middleware?
1. What should not go into middleware?
1. Why can middleware become a performance bottleneck?
1. How would you test middleware?
1. How would you test a database dependency?
1. How would you test a current-user dependency?
1. How would you standardize API errors?
1. How would you debug a sudden 500 response?
1. How can timeouts in dependencies affect the request?
1. How would you design a clean authentication dependency chain?
1. How would you prevent dependency overrides from leaking between tests?
1. An async dependency uses a blocking HTTP client. What is wrong?
1. A middleware adds 100 ms to every request. How would you investigate?
1. A duplicate-key database error is reaching clients. How would you fix it?
1. Explain the difference between middleware, dependency injection and exception handlers in one request lifecycle.

If you can answer these clearly and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [14. FastAPI Fundamentals](./14-fastapi-core.md)

**Next:** [16. Production FastAPI](./16-production-fastapi.md)
