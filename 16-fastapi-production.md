# 16. Production FastAPI

**Previous:** [15. FastAPI Dependency Injection, Middleware & Errors](./15-fastapi-di-middleware-errors.md)

**Next:** [17. Flask](./17-flask.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain how to make a FastAPI service production-ready.
- Design authentication and authorization flows.
- Explain JWT and OAuth2 at an interview-ready level.
- Implement practical RBAC concepts.
- Understand async endpoint design and its limitations.
- Use background tasks appropriately.
- Call external APIs safely.
- Design retry and timeout behavior.
- Implement pagination and filtering.
- Explain rate limiting strategies.
- Design liveness and readiness health checks.
- Understand graceful shutdown.
- Apply production observability and metrics.
- Explain a practical FastAPI production architecture.
- Identify common production failure modes and trade-offs.

______________________________________________________________________

# 1. From FastAPI Application to Production Service

A development application can be as simple as:

```text
Client
  ↓
FastAPI
  ↓
Database
```

A production service commonly looks more like:

```text
Client
  ↓
CDN / WAF
  ↓
Load Balancer
  ↓
Reverse Proxy
  ↓
FastAPI / ASGI Workers
  ↓
Database / Redis / External APIs
```

Production readiness means handling:

- Security
- Failure
- Concurrency
- Timeouts
- Resource limits
- Observability
- Shutdown
- Scaling
- Operational maintenance

______________________________________________________________________

# 2. Authentication

Authentication answers:

> Who is the caller?

Common mechanisms include:

- Session-based authentication
- API keys
- JWT-based authentication
- OAuth2/OIDC-based authentication

For APIs, the appropriate mechanism depends on the client architecture and security requirements.

______________________________________________________________________

# 3. Authorization

Authorization answers:

> What is this authenticated caller allowed to do?

For example:

```text
User
 ↓
Authenticated
 ↓
Has permission?
 ↓
Allow / Deny
```

A successfully authenticated user can still be forbidden from performing an operation.

______________________________________________________________________

# 4. JWT

JWT stands for JSON Web Token.

A JWT commonly contains:

```text
Header
Payload
Signature
```

It can carry claims such as:

```text
sub
iss
aud
exp
iat
roles/scopes
```

The exact claims depend on the authentication system.

______________________________________________________________________

# 5. JWT Structure

A JWT has three encoded sections:

```text
header.payload.signature
```

The important interview point is:

> A JWT is normally signed, not encrypted.

Therefore, sensitive information should not be placed in a JWT merely because the token is encoded.

______________________________________________________________________

# 6. JWT Verification

A service receiving a JWT should verify appropriate properties such as:

- Signature
- Algorithm
- Expiration
- Issuer
- Audience
- Required claims

Do not blindly trust the payload.

______________________________________________________________________

# 7. JWT Advantages

JWTs can be useful because:

- They can carry claims.
- Services can validate signatures without calling a session database for every request.
- They work well in distributed environments.

But JWTs also introduce trade-offs.

______________________________________________________________________

# 8. JWT Trade-offs

A major issue is revocation.

Once a valid JWT is issued, invalidating it before expiration requires additional mechanisms.

Possible approaches include:

- Short-lived access tokens
- Refresh tokens
- Token revocation infrastructure
- Token introspection
- Key rotation

JWT is not automatically better than server-side sessions.

______________________________________________________________________

# 9. OAuth2

OAuth2 is an authorization framework.

It defines ways for a client to obtain access to protected resources.

OAuth2 should not be confused with authentication itself.

Modern authentication systems commonly combine OAuth2 with OpenID Connect (OIDC) when identity information is required.

______________________________________________________________________

# 10. OAuth2 Flow — High Level

A simplified authorization-code flow is:

```text
User
 ↓
Client
 ↓
Authorization Server
 ↓
Authorization Code
 ↓
Client
 ↓
Token Exchange
 ↓
Access Token
 ↓
Resource Server/API
```

The exact flow depends on the client type and security requirements.

______________________________________________________________________

# 11. Access Token vs Refresh Token

An access token is used to access protected resources.

A refresh token can be used to obtain a new access token without requiring the user to authenticate again, subject to
the authorization server's rules.

Typical design:

```text
Short-lived access token
        +
Longer-lived refresh token
```

This reduces the lifetime of the credential used on API requests.

______________________________________________________________________

# 12. RBAC

RBAC stands for Role-Based Access Control.

Instead of assigning permissions directly to every user:

```text
User → Permission
```

you can use:

```text
User → Role → Permissions
```

Example:

```text
Admin
 ├── users:read
 ├── users:write
 └── users:delete
```

______________________________________________________________________

# 13. RBAC in FastAPI

Authorization can be represented using dependencies.

Conceptually:

```python
async def require_admin(
    user=Depends(get_current_user),
):
    if "admin" not in user.roles:
        raise HTTPException(status_code=403)
    return user
```

Then protected endpoints depend on `require_admin`.

______________________________________________________________________

# 14. Authentication vs Authorization in FastAPI

A practical dependency chain is:

```text
Token
 ↓
Authentication
 ↓
Current user
 ↓
Authorization
 ↓
Endpoint
```

This keeps security checks reusable and explicit.

______________________________________________________________________

# 15. Async Endpoints

FastAPI supports asynchronous endpoints:

```python
@app.get("/users")
async def users():
    ...
```

Async is especially useful for I/O-bound operations such as:

- HTTP calls
- Async database access
- Network operations

It does not automatically make CPU-heavy work faster.

______________________________________________________________________

# 16. Blocking Code in Async Endpoints

This is dangerous:

```python
@app.get("/data")
async def data():
    result = requests.get("https://example.com")
    return result.json()
```

`requests.get()` is synchronous.

The blocking call can prevent the event loop from processing other work.

Use an async-compatible client or deliberately isolate blocking work.

______________________________________________________________________

# 17. Async Does Not Mean Unlimited Concurrency

Even with asynchronous endpoints, the application can be constrained by:

- Database connection pool
- HTTP connection pool
- CPU
- Memory
- File descriptors
- External service limits

Concurrency must be bounded according to system capacity.

______________________________________________________________________

# 18. Background Tasks

FastAPI provides `BackgroundTasks` for lightweight work that can run after returning a response.

Example:

```python
from fastapi import BackgroundTasks


def write_audit_log(user_id: int):
    ...


@app.post("/users")
async def create_user(
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_audit_log, 42)
    return {"created": True}
```

______________________________________________________________________

# 19. When BackgroundTasks Are Appropriate

Good examples:

- Lightweight logging
- Small notifications
- Non-critical post-response work

They are not a replacement for a durable task queue.

______________________________________________________________________

# 20. Background Task Limitations

A background task tied to an application process can be lost if that process crashes or is terminated.

For durable jobs, consider:

```text
FastAPI
 ↓
Message Broker / Task Queue
 ↓
Worker
```

Examples include Celery or other queue-based worker architectures.

______________________________________________________________________

# 21. External API Calls

Production applications frequently call external services.

Examples:

```text
FastAPI
 ↓
Payment API
 ↓
Email API
 ↓
Identity provider
```

Every external call introduces:

- Latency
- Failure
- Rate limits
- Authentication requirements
- Dependency on another system

Treat external APIs as unreliable dependencies.

______________________________________________________________________

# 22. HTTP Client Reuse

Avoid creating a completely new HTTP client/connection for every request when the client library supports connection
pooling.

Prefer a managed application-level client/pool where appropriate.

Benefits include:

- Connection reuse
- Lower latency
- Fewer TCP/TLS handshakes
- Controlled connection limits

______________________________________________________________________

# 23. External API Timeout

Every external API request should have a deliberate timeout.

Without a timeout:

```text
FastAPI request
      ↓
External API
      ↓
wait...
      ↓
wait...
      ↓
resources remain occupied
```

A timeout prevents an unhealthy dependency from holding application resources indefinitely.

______________________________________________________________________

# 24. Retry

Retries can help with transient failures.

Potential retryable failures include:

- Temporary network errors
- Connection resets
- Some 5xx responses
- Rate limiting when the server provides retry guidance

Do not retry every failure.

______________________________________________________________________

# 25. Exponential Backoff

A common retry strategy increases the wait between attempts:

```text
Attempt 1 → immediate
Attempt 2 → short delay
Attempt 3 → longer delay
Attempt 4 → longer delay
```

Jitter can be added to reduce synchronized retry spikes.

______________________________________________________________________

# 26. Retry Amplification

Suppose:

```text
1000 requests
```

each retries three times.

A failing dependency could receive thousands of requests instead of the original traffic.

This can make an outage worse.

Retries should therefore be:

- Limited
- Selective
- Backed off
- Jittered where appropriate
- Combined with timeouts

______________________________________________________________________

# 27. Idempotency and Retry

Retries are safe only when repeating the operation is safe.

For example:

```text
GET /users/42
```

is naturally safe to repeat.

A payment request may not be.

For important write operations, idempotency keys can allow the server to recognize duplicate attempts.

______________________________________________________________________

# 28. Timeout + Retry Budget

Suppose:

```text
Total request budget = 2 seconds
```

Do not configure:

```text
3 retries × 2 second timeout
```

because the operation could exceed the overall request budget significantly.

A senior engineer should reason about the **total latency budget**, not only individual timeout values.

______________________________________________________________________

# 29. Pagination

Returning thousands or millions of records in one API response is usually a bad idea.

Pagination limits response size.

Common styles:

### Offset pagination

```http
GET /users?offset=100&limit=20
```

### Cursor pagination

```http
GET /users?cursor=abc123&limit=20
```

______________________________________________________________________

# 30. Offset vs Cursor Pagination

### Offset

Simple:

```text
OFFSET 100 LIMIT 20
```

But large offsets can become expensive and results can shift when data changes.

### Cursor

The client continues from a position represented by a cursor.

Cursor pagination is often more stable and efficient for large/changing datasets.

______________________________________________________________________

# 31. Pagination Design

A production API should define:

- Maximum page size
- Default page size
- Ordering
- Stable sort key
- Cursor format if using cursors
- Behavior when records disappear/change

Never allow unlimited client-controlled page sizes.

______________________________________________________________________

# 32. Filtering

Filtering lets clients restrict returned data.

Example:

```http
GET /orders?status=completed
```

Multiple filters might be:

```http
GET /orders?status=completed&customer_id=42
```

Validate and constrain filters rather than allowing arbitrary database expressions.

______________________________________________________________________

# 33. Filtering and Indexes

API filters should align with database access patterns.

If clients frequently request:

```text
status + created_at
```

the database may need an appropriate index depending on query patterns.

API design and database design should not be considered independently.

______________________________________________________________________

# 34. Rate Limiting

Rate limiting controls how frequently clients can access an API.

Example:

```text
100 requests / minute / client
```

It can protect:

- Application capacity
- Database capacity
- External dependencies
- Authentication endpoints

______________________________________________________________________

# 35. Rate Limiting Algorithms

Common approaches include:

- Fixed window
- Sliding window
- Token bucket
- Leaky bucket

The choice depends on the traffic pattern and desired behavior.

______________________________________________________________________

# 36. Distributed Rate Limiting

With multiple FastAPI instances:

```text
Client
  ↓
Load Balancer
 ├── App 1
 ├── App 2
 └── App 3
```

An in-memory counter on one instance does not provide a global limit.

A shared store such as Redis can be used for distributed rate limiting.

______________________________________________________________________

# 37. Health Checks

Production services commonly expose health endpoints.

Examples:

```text
/health/live
/health/ready
```

______________________________________________________________________

# 38. Liveness vs Readiness

### Liveness

> Is the process alive?

A liveness check should generally be lightweight.

### Readiness

> Is the instance ready to receive traffic?

Readiness may check important dependencies depending on the deployment design.

These checks should not be confused.

______________________________________________________________________

# 39. Health Check Pitfall

Do not automatically make liveness depend on every external dependency.

For example:

```text
Database unavailable
     ↓
Liveness = failed
     ↓
Container restarts
     ↓
Database still unavailable
     ↓
Restart again
```

This can create restart loops.

Use readiness and liveness intentionally.

______________________________________________________________________

# 40. Graceful Shutdown

When an application is shutting down, it should avoid abruptly terminating active work where possible.

A graceful shutdown may:

1. Stop accepting new traffic.
1. Allow in-flight requests to finish.
1. Stop background activity.
1. Close database/HTTP clients.
1. Release resources.
1. Exit.

______________________________________________________________________

# 41. Why Graceful Shutdown Matters

Without graceful shutdown:

- Requests can be interrupted.
- Database transactions may be affected.
- Messages can be lost or redelivered.
- Connections may not close cleanly.
- Deployments can cause avoidable errors.

Graceful shutdown is particularly important during rolling deployments.

______________________________________________________________________

# 42. FastAPI Lifespan

FastAPI supports application lifespan handling.

Application-level resources can be initialized and cleaned up during the application lifecycle.

Conceptually:

```text
Startup
 ↓
Initialize shared resources
 ↓
Serve requests
 ↓
Shutdown
 ↓
Close resources
```

This is useful for:

- HTTP clients
- Database engines
- Connection pools
- Other shared resources

______________________________________________________________________

# 43. Observability

A production API should provide visibility into:

```text
What happened?
How often?
How long did it take?
Where did it fail?
```

Use:

- Logs
- Metrics
- Traces

______________________________________________________________________

# 44. Structured Logging

Prefer structured logs over arbitrary strings.

Example fields:

```text
timestamp
request_id
route
method
status_code
duration_ms
error_code
```

Structured logs are easier to search and aggregate.

Never log secrets or sensitive credentials.

______________________________________________________________________

# 45. Metrics

Useful API metrics include:

- Requests per second
- Error rate
- Latency
- p50
- p95
- p99
- Active requests
- Database pool usage
- External API latency
- External API error rate
- Process CPU
- Process memory

______________________________________________________________________

# 46. Tracing

Distributed tracing helps identify where a request spends time.

Example:

```text
API
 ↓
User Service
 ↓
Payment Service
 ↓
Database
```

A trace can reveal whether latency comes from:

- API processing
- Database
- External API
- Network
- Queue

______________________________________________________________________

# 47. Request Correlation

A request ID should ideally be propagated across services.

Example:

```text
Client
  ↓ request_id=abc
API
  ↓ request_id=abc
Payment Service
  ↓ request_id=abc
Database-related logs
```

This makes production debugging much easier.

______________________________________________________________________

# 48. Production Metrics and Alerts

Metrics are useful only when connected to actionable thresholds.

Examples:

```text
p99 latency > threshold
error rate > threshold
database pool saturation
high CPU
high memory
external dependency failures
```

Avoid creating alerts for every minor fluctuation.

______________________________________________________________________

# 49. Production Architecture

A practical architecture may be:

```text
                 ┌── Redis
                 │
Client → LB → FastAPI → Database
                 │
                 ├── External APIs
                 │
                 └── Task Queue → Workers
```

Additional infrastructure may include:

- CDN
- WAF
- Reverse proxy
- Metrics system
- Log aggregation
- Distributed tracing

The exact architecture should follow actual requirements.

______________________________________________________________________

# 50. Stateless FastAPI Workers

Prefer stateless application workers when practical.

That means:

```text
Worker 1
Worker 2
Worker 3
```

can independently handle requests without relying on local mutable session state.

State can instead be stored in:

- Database
- Redis
- Object storage
- Other appropriate shared systems

Statelessness makes horizontal scaling easier.

______________________________________________________________________

# 51. Configuration

Production configuration should generally come from environment/configuration management rather than hard-coded values.

Examples:

```text
DATABASE_URL
REDIS_URL
JWT_ISSUER
EXTERNAL_API_URL
```

Secrets should be managed using an appropriate secret-management system rather than committed to source control.

______________________________________________________________________

# 52. Resource Limits

Production services should consider limits for:

- Request body size
- File uploads
- Concurrent requests
- Database connections
- HTTP connections
- Response size
- Background work

Unbounded resources can turn abnormal traffic into an outage.

______________________________________________________________________

# 53. Dependency Failure Strategy

For every important dependency, ask:

```text
What happens if it is slow?
What happens if it returns errors?
What happens if it is unavailable?
What happens if it recovers?
```

Then define:

- Timeout
- Retry policy
- Fallback where appropriate
- Error response
- Monitoring
- Capacity limits

______________________________________________________________________

# 54. Graceful Degradation

Not every dependency failure should make the entire application unavailable.

For example:

```text
Recommendation service unavailable
        ↓
Return products without recommendations
```

when the recommendation feature is non-critical.

This is graceful degradation.

Do not degrade critical security or financial operations in unsafe ways.

______________________________________________________________________

# 55. Production Checklist

Before calling a FastAPI service production-ready, review:

```text
Authentication
Authorization
Input validation
Timeouts
Retries
Rate limiting
Pagination
Resource limits
Health checks
Graceful shutdown
Structured logs
Metrics
Tracing
Secrets management
Database pooling
External API handling
Error handling
Testing
```

______________________________________________________________________

# 56. Common Production FastAPI Mistakes

## Mistake 1 — No timeouts

External services can hold resources indefinitely.

______________________________________________________________________

## Mistake 2 — Blind retries

Retries can amplify outages.

______________________________________________________________________

## Mistake 3 — Unlimited pagination

Clients can request huge datasets and exhaust resources.

______________________________________________________________________

## Mistake 4 — In-memory rate limiting in a multi-instance service

Each instance may enforce a different limit.

______________________________________________________________________

## Mistake 5 — Treating background tasks as durable queues

Process termination can lose background work.

______________________________________________________________________

## Mistake 6 — Blocking inside async endpoints

A blocking operation can stall the event loop.

______________________________________________________________________

## Mistake 7 — Liveness checks that depend on everything

This can create restart loops during dependency outages.

______________________________________________________________________

## Mistake 8 — No graceful shutdown

Deployments can interrupt active requests.

______________________________________________________________________

## Mistake 9 — Logging credentials

Logs can become a major security risk.

______________________________________________________________________

# 57. Interview Questions & Answers

## Q1. How would you make a FastAPI application production-ready?

**Answer:**

I would address security, resource limits, timeouts, retries, rate limiting, health checks, graceful shutdown,
database/HTTP connection pooling, structured logging, metrics, tracing and failure handling.

I would also make sure the service is horizontally scalable and that dependencies have explicit failure policies.

______________________________________________________________________

## Q2. What is authentication?

**Answer:**

Authentication determines who the caller is.

______________________________________________________________________

## Q3. What is authorization?

**Answer:**

Authorization determines what an authenticated caller is allowed to do.

______________________________________________________________________

## Q4. What is JWT?

**Answer:**

JWT is a token format containing claims that can be signed so a service can verify their integrity.

A JWT is normally encoded and signed, not inherently encrypted.

______________________________________________________________________

## Q5. Is JWT encrypted?

**Answer:**

Not normally.

Standard JWTs are generally signed tokens whose payload can be decoded by anyone possessing the token.

Do not place sensitive information in them unless an appropriate encryption mechanism is intentionally used.

______________________________________________________________________

## Q6. What should you validate in a JWT?

**Answer:**

At minimum, depending on the authentication design:

- Signature
- Algorithm
- Expiration
- Issuer
- Audience
- Required claims

______________________________________________________________________

## Q7. What is the main JWT revocation challenge?

**Answer:**

A valid token generally remains usable until it expires unless additional revocation/introspection mechanisms exist.

Short-lived access tokens and controlled refresh-token strategies can reduce the risk.

______________________________________________________________________

## Q8. What is OAuth2?

**Answer:**

OAuth2 is an authorization framework that defines ways for clients to obtain access to protected resources.

Authentication is often implemented alongside OAuth2 using OpenID Connect.

______________________________________________________________________

## Q9. What is RBAC?

**Answer:**

Role-Based Access Control maps users to roles and roles to permissions.

For example:

```text
User → Admin → users:delete
```

______________________________________________________________________

## Q10. How would you implement RBAC in FastAPI?

**Answer:**

A common approach is to use dependencies:

```text
Authentication dependency
        ↓
Current user
        ↓
Role/permission dependency
        ↓
Endpoint
```

______________________________________________________________________

## Q11. When should you use `async def`?

**Answer:**

Use it when the endpoint performs asynchronous I/O and the libraries involved support non-blocking operations.

______________________________________________________________________

## Q12. Does `async def` automatically make an endpoint non-blocking?

**Answer:**

No.

Calling synchronous blocking libraries inside the endpoint can still block the event loop.

______________________________________________________________________

## Q13. When are FastAPI background tasks useful?

**Answer:**

They are useful for lightweight post-response work that does not require durable execution.

For critical or long-running work, use a durable task queue/worker architecture.

______________________________________________________________________

## Q14. Why are background tasks not equivalent to Celery?

**Answer:**

A FastAPI background task runs within the application process.

A durable task queue provides independent workers, persistence/retry mechanisms and better isolation for long-running or
important jobs.

______________________________________________________________________

## Q15. Why do external API calls need timeouts?

**Answer:**

Without timeouts, an unhealthy external service can cause requests and connection resources to remain occupied
indefinitely.

______________________________________________________________________

## Q16. When should you retry an external API call?

**Answer:**

Retry only failures that are likely transient and safe to retry.

Use limited attempts, backoff and often jitter.

______________________________________________________________________

## Q17. Why is retrying every error dangerous?

**Answer:**

Permanent failures do not become successful through retries, and retry traffic can amplify load on an already failing
dependency.

______________________________________________________________________

## Q18. What is exponential backoff?

**Answer:**

It increases the delay between retry attempts, reducing pressure on the failing dependency.

______________________________________________________________________

## Q19. What is retry jitter?

**Answer:**

Jitter adds controlled randomness to retry delays so many clients do not retry simultaneously.

______________________________________________________________________

## Q20. What is idempotency?

**Answer:**

An operation is idempotent when repeating the same logical operation produces the same intended result.

This is particularly important when retrying write operations.

______________________________________________________________________

## Q21. What is an idempotency key?

**Answer:**

It is a client-provided identifier that allows the server to recognize repeated attempts of the same logical operation
and avoid duplicate processing.

______________________________________________________________________

## Q22. Offset vs cursor pagination?

**Answer:**

Offset pagination is simple but can become inefficient for large offsets and can behave poorly when data changes.

Cursor pagination can be more efficient and stable for large, changing datasets.

______________________________________________________________________

## Q23. Why should page size be limited?

**Answer:**

To prevent clients from requesting huge result sets that consume excessive database, memory, network and serialization
resources.

______________________________________________________________________

## Q24. What is rate limiting?

**Answer:**

Rate limiting controls how frequently a client can access a service within a defined policy.

______________________________________________________________________

## Q25. Why doesn't in-memory rate limiting work reliably across multiple instances?

**Answer:**

Each instance has its own counter.

A client can distribute requests across instances and bypass a per-instance limit.

A shared store such as Redis can coordinate limits.

______________________________________________________________________

## Q26. What is the difference between liveness and readiness?

**Answer:**

Liveness asks whether the process is alive.

Readiness asks whether the instance is ready to receive traffic.

______________________________________________________________________

## Q27. Why should liveness checks be lightweight?

**Answer:**

A liveness failure can trigger process/container restarts.

Making it depend on every external service can cause restart loops during dependency outages.

______________________________________________________________________

## Q28. What is graceful shutdown?

**Answer:**

It allows the service to stop accepting new work, finish or safely handle in-flight work and close resources before
exiting.

______________________________________________________________________

## Q29. Why is graceful shutdown important?

**Answer:**

It reduces interrupted requests, incomplete work, connection leaks and deployment-related errors.

______________________________________________________________________

## Q30. What is FastAPI lifespan used for?

**Answer:**

It provides application startup/shutdown lifecycle handling for resources such as shared HTTP clients, database engines
and connection pools.

______________________________________________________________________

## Q31. What observability should a production FastAPI service have?

**Answer:**

At minimum:

- Structured logs
- Request/correlation IDs
- Metrics
- Latency percentiles
- Error rates
- Distributed tracing where appropriate

______________________________________________________________________

## Q32. Which API latency metrics matter?

**Answer:**

p50 shows typical latency, while p95 and p99 show tail latency.

Tail latency is particularly important because a small percentage of very slow requests can represent a poor user
experience.

______________________________________________________________________

## Q33. Why should HTTP clients be reused?

**Answer:**

Reusable clients can maintain connection pools, reducing repeated TCP/TLS setup and controlling outbound connection
concurrency.

______________________________________________________________________

## Q34. How do timeouts and retries interact?

**Answer:**

The retry policy must fit within an overall request latency budget.

Retries with long timeouts can multiply total latency and exhaust resources.

______________________________________________________________________

## Q35. What is graceful degradation?

**Answer:**

It means maintaining core functionality when a non-critical dependency fails.

For example, an optional recommendation service can fail while the main product API still works.

______________________________________________________________________

## Q36. What is a stateless FastAPI worker?

**Answer:**

A worker that does not depend on process-local mutable state to preserve user/session application state across requests.

Shared state is stored in appropriate external systems.

______________________________________________________________________

## Q37. How would you handle secrets in production?

**Answer:**

Keep secrets out of source control and use appropriate environment/configuration and secret-management mechanisms.

Do not expose them through logs or API responses.

______________________________________________________________________

## Q38. What resource limits should an API have?

**Answer:**

Depending on the service:

- Request size
- Upload size
- Page size
- Concurrent requests
- Database connections
- Outbound HTTP connections
- Response size
- Background workload

______________________________________________________________________

## Q39. How would you design failure handling for an external dependency?

**Answer:**

Define:

```text
Timeout
Retry policy
Backoff/jitter
Fallback if appropriate
Error mapping
Monitoring
Capacity limits
```

and ensure the total policy respects the endpoint's latency budget.

______________________________________________________________________

## Q40. What are the most common production mistakes in FastAPI?

**Answer:**

Common mistakes include blocking async endpoints, missing timeouts, uncontrolled retries, unlimited pagination, unsafe
logging, poor shutdown handling, weak resource limits and incorrect health checks.

______________________________________________________________________

# 58. Scenario-Based Questions

## Scenario 1 — External API Takes 30 Seconds

Your FastAPI endpoint calls a payment provider with no timeout.

**Question:** What is wrong?

**Answer:**

The dependency can hold application resources for an unbounded period.

Add a deliberate timeout and decide how the application should handle the failure.

______________________________________________________________________

## Scenario 2 — Retry Storm

A downstream service is unavailable.

Your API retries every failed request three times immediately.

**Question:** Why is this dangerous?

**Answer:**

The failing dependency receives amplified traffic precisely when it is unhealthy.

Use limited retries with exponential backoff and jitter, and consider whether the operation is safe to retry.

______________________________________________________________________

## Scenario 3 — Duplicate Payment

A payment request times out after the provider may already have processed it.

The client retries.

**Question:** How can you prevent duplicate processing?

**Answer:**

Use an idempotency key and have the payment operation recognize repeated attempts of the same logical request.

______________________________________________________________________

## Scenario 4 — Rate Limit Bypass

You have three FastAPI instances.

Each instance allows:

```text
100 requests/minute
```

A client sends requests through all three.

**Question:** Can the client effectively exceed 100 requests/minute?

**Answer:**

Yes.

Each instance has its own counter.

Use a shared rate-limiting mechanism when the limit needs to apply globally.

______________________________________________________________________

## Scenario 5 — Container Restart Loop

The database goes down.

Your liveness endpoint checks database connectivity.

Containers repeatedly restart.

**Question:** What is wrong?

**Answer:**

Liveness is coupled too tightly to a dependency.

Liveness should generally answer whether the process is alive, while readiness can determine whether it should receive
traffic.

______________________________________________________________________

## Scenario 6 — Slow Pagination

An endpoint uses:

```sql
OFFSET 1000000 LIMIT 50
```

and becomes increasingly slow.

**Question:** What would you consider?

**Answer:**

Evaluate cursor/keyset pagination and appropriate indexes.

Large offsets can require the database to process/skip many rows.

______________________________________________________________________

## Scenario 7 — Background Email

An endpoint creates a user and sends a non-critical email after the response.

**Question:** Is `BackgroundTasks` appropriate?

**Answer:**

Potentially, if the task is lightweight and losing it during process termination is acceptable.

If the email must be reliably delivered, use a durable queue/worker architecture.

______________________________________________________________________

## Scenario 8 — CPU-Heavy Endpoint

A PDF processing endpoint performs expensive CPU work inside `async def`.

**Question:** What problem can this cause?

**Answer:**

CPU-heavy work can block the event loop and reduce responsiveness for unrelated requests.

Move substantial CPU work to appropriate worker/process infrastructure.

______________________________________________________________________

## Scenario 9 — p99 Explosion

Your service reports:

```text
p50 = 50 ms
p95 = 100 ms
p99 = 4 seconds
```

**Question:** What does this suggest?

**Answer:**

Most requests are fast, but a small tail is extremely slow.

Investigate traces and correlate slow requests with database waits, connection-pool exhaustion, external API latency,
CPU contention or other resource bottlenecks.

______________________________________________________________________

## Scenario 10 — Production Deployment

During every deployment, some users receive connection errors.

**Question:** What would you investigate?

**Answer:**

Check whether instances are being terminated before active requests complete.

Implement graceful shutdown, appropriate readiness handling and deployment behavior that allows traffic to drain from
terminating instances.

______________________________________________________________________

# 59. Practice Exercises

## Exercise 1 — Authentication Design

Design a JWT-based authentication flow for:

```text
POST /login
GET /profile
POST /refresh
```

Document:

- Token contents
- Expiration
- Verification
- Refresh strategy
- Revocation considerations

______________________________________________________________________

## Exercise 2 — RBAC

Implement roles:

```text
USER
ADMIN
```

with permissions:

```text
users:read
users:write
users:delete
```

Create FastAPI dependencies for permission checks.

______________________________________________________________________

## Exercise 3 — External API Client

Build an async HTTP client abstraction with:

- Connection reuse
- Timeout
- Limited retries
- Exponential backoff
- Jitter

Document which failures should be retried.

______________________________________________________________________

## Exercise 4 — Idempotent Endpoint

Design:

```http
POST /payments
Idempotency-Key: abc123
```

Explain how you would store and retrieve the result for duplicate requests.

______________________________________________________________________

## Exercise 5 — Pagination

Implement both:

```text
offset + limit
```

and:

```text
cursor + limit
```

pagination.

Compare their behavior on a large changing dataset.

______________________________________________________________________

## Exercise 6 — Rate Limiting

Design a distributed rate limiter using Redis.

Define:

```text
key
window
limit
expiration
```

and explain what happens when multiple application instances receive requests concurrently.

______________________________________________________________________

## Exercise 7 — Health Endpoints

Design:

```text
/health/live
/health/ready
```

Explain what each should check and what should happen when the database is unavailable.

______________________________________________________________________

## Exercise 8 — Graceful Shutdown

Design the shutdown sequence for:

```text
FastAPI
 ↓
HTTP client pool
 ↓
Database pool
 ↓
Background workers
```

Explain the order and why it matters.

______________________________________________________________________

## Exercise 9 — Observability

Define a minimum production dashboard containing:

- Request rate
- Error rate
- p50/p95/p99
- CPU
- Memory
- DB pool utilization
- External API latency
- External API error rate

Add alerts for meaningful failure conditions.

______________________________________________________________________

## Exercise 10 — Production Architecture Review

Take a FastAPI application and review:

```text
Authentication
Authorization
Timeouts
Retries
Pagination
Rate limiting
Health checks
Shutdown
Observability
Resource limits
```

For each, identify one risk and one improvement.

______________________________________________________________________

# 60. Quick Revision

| Concept | Key Point |
|---|---|
| Authentication | Identifies caller |
| Authorization | Determines permissions |
| JWT | Signed token format carrying claims |
| JWT encryption | Not provided by ordinary signed JWTs |
| OAuth2 | Authorization framework |
| OIDC | Identity layer commonly used with OAuth2 |
| RBAC | User → Role → Permissions |
| Async endpoint | Useful for async I/O |
| Blocking call | Can block event loop |
| BackgroundTasks | Lightweight in-process post-response work |
| Task queue | Durable/independent background processing |
| External API | Unreliable dependency |
| Timeout | Bounds waiting |
| Retry | Handles selected transient failures |
| Backoff | Spreads retry attempts |
| Jitter | Reduces synchronized retries |
| Idempotency | Safe repeated logical operation |
| Idempotency key | Deduplicates repeated write attempts |
| Offset pagination | Simple, can degrade at large offsets |
| Cursor pagination | Often efficient/stable for large datasets |
| Filtering | Restricts returned records |
| Rate limiting | Controls request frequency |
| Distributed rate limiting | Requires shared coordination |
| Liveness | Process is alive |
| Readiness | Instance can receive traffic |
| Graceful shutdown | Safely drains/cleans up service |
| Lifespan | Application startup/shutdown lifecycle |
| Logs | Detailed events |
| Metrics | Quantitative measurements |
| Traces | Request journey |
| Request ID | Correlates activity |
| Stateless worker | Does not rely on process-local request state |
| Resource limits | Prevent unbounded consumption |
| Graceful degradation | Preserve core functionality during optional dependency failure |

______________________________________________________________________

# 61. Completion Checklist

Before moving to File 17, make sure you can explain:

- [ ] Production FastAPI architecture
- [ ] Authentication
- [ ] Authorization
- [ ] JWT
- [ ] JWT structure
- [ ] JWT verification
- [ ] JWT trade-offs
- [ ] JWT revocation
- [ ] OAuth2
- [ ] OAuth2 authorization-code flow
- [ ] Access tokens
- [ ] Refresh tokens
- [ ] RBAC
- [ ] RBAC implementation using dependencies
- [ ] Async endpoints
- [ ] Blocking operations
- [ ] Async concurrency limitations
- [ ] Background tasks
- [ ] Background task limitations
- [ ] Durable task queues
- [ ] External API calls
- [ ] HTTP client reuse
- [ ] External API timeouts
- [ ] Retryable failures
- [ ] Exponential backoff
- [ ] Jitter
- [ ] Retry amplification
- [ ] Idempotency
- [ ] Idempotency keys
- [ ] Retry/timeout budget
- [ ] Pagination
- [ ] Offset pagination
- [ ] Cursor pagination
- [ ] Pagination limits
- [ ] Filtering
- [ ] Filtering and database indexes
- [ ] Rate limiting
- [ ] Rate-limit algorithms
- [ ] Distributed rate limiting
- [ ] Health checks
- [ ] Liveness
- [ ] Readiness
- [ ] Health-check pitfalls
- [ ] Graceful shutdown
- [ ] FastAPI lifespan
- [ ] Structured logging
- [ ] Metrics
- [ ] Distributed tracing
- [ ] Request correlation
- [ ] Production alerts
- [ ] Stateless workers
- [ ] Configuration
- [ ] Secrets
- [ ] Resource limits
- [ ] Dependency failure strategies
- [ ] Graceful degradation
- [ ] Common production mistakes

______________________________________________________________________

# 62. Interview Readiness Test

Answer these aloud without looking at the notes:

1. How would you make a FastAPI application production-ready?
1. Authentication vs authorization?
1. What is JWT?
1. Is JWT encrypted?
1. What should you validate in a JWT?
1. What is the main JWT revocation challenge?
1. What is OAuth2?
1. OAuth2 vs authentication?
1. What is RBAC?
1. How would you implement RBAC in FastAPI?
1. When should you use `async def`?
1. Does `async def` guarantee non-blocking execution?
1. Why is blocking code dangerous?
1. When are FastAPI background tasks appropriate?
1. Why aren't background tasks equivalent to a durable task queue?
1. How would you safely call an external API?
1. Why are timeouts necessary?
1. Which external failures should be retried?
1. Why use exponential backoff?
1. What is retry jitter?
1. What is retry amplification?
1. How does idempotency relate to retries?
1. What is an idempotency key?
1. Offset vs cursor pagination?
1. Why should page size be bounded?
1. How would you design filtering for a large table?
1. What is rate limiting?
1. Why doesn't in-memory rate limiting work globally across instances?
1. Explain fixed-window vs token-bucket rate limiting.
1. Liveness vs readiness?
1. Why should liveness usually be lightweight?
1. What is graceful shutdown?
1. What is FastAPI lifespan?
1. What should happen during application shutdown?
1. What observability should a production API have?
1. Which latency percentiles would you monitor?
1. Why should HTTP clients be reused?
1. How should timeout and retry policies interact?
1. What is graceful degradation?
1. How would you keep FastAPI workers stateless?
1. How should production secrets be managed?
1. What resource limits would you enforce?
1. How would you design failure handling for an external dependency?
1. A payment request times out and the client retries. How do you prevent duplicate payment?
1. A client bypasses a per-instance rate limit by distributing traffic across instances. How do you fix it?
1. The database goes down and all containers start restarting. What is wrong with the health checks?
1. An external API takes 30 seconds. How do you prevent it from exhausting FastAPI resources?
1. A retry storm is making an outage worse. How would you fix it?
1. An endpoint's p99 latency is 4 seconds while p50 is 50 ms. How would you investigate?
1. During deployments, users see connection errors. How would graceful shutdown and readiness help?

If you can answer these confidently and complete the exercises, this topic is complete.

______________________________________________________________________

**Previous:** [15. FastAPI Dependency Injection, Middleware & Errors](./15-fastapi-di-middleware-errors.md)

**Next:** [17. Flask](./17-flask.md)
