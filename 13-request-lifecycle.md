# 13. Complete Backend Request Lifecycle

**Previous:** [12. HTTP, TCP/IP, TLS & Networking](./12-http-networking.md)

**Next:** [14. FastAPI Fundamentals](./14-fastapi-core.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain the complete journey of a backend request.
- Trace a request from the client through DNS, TCP/TLS, CDN/WAF, load balancer and reverse proxy.
- Explain what an application server does.
- Understand how ASGI fits into a Python backend.
- Explain how FastAPI receives and processes a request.
- Understand middleware, authentication and validation in the request path.
- Explain where business logic, ORM and database operations happen.
- Understand serialization and response generation.
- Distinguish blocking and non-blocking work during the request.
- Identify common failure points at every layer.
- Understand connection handling and connection pools.
- Explain observability for a production request.
- Debug slow or failed requests systematically.
- Answer senior-level backend request-lifecycle interview questions.

______________________________________________________________________

# 1. The Complete Request Path

A useful high-level model is:

```text
Client
  ↓
DNS
  ↓
TCP / TLS
  ↓
CDN / WAF
  ↓
Load Balancer
  ↓
Reverse Proxy
  ↓
ASGI Server
  ↓
FastAPI
  ↓
Middleware
  ↓
Authentication
  ↓
Validation
  ↓
Business Logic
  ↓
ORM / Repository
  ↓
Database
  ↓
Serialization
  ↓
HTTP Response
  ↓
Client
```

This is not present in exactly this form in every deployment.

For example:

- A service may not use a CDN.
- A WAF may be integrated into another layer.
- A load balancer and reverse proxy may be provided by the same infrastructure.
- The application may use a different Python framework.
- The application may access a database without an ORM.

The important interview skill is understanding the responsibility of each layer.

______________________________________________________________________

# 2. Start With a Concrete Example

Suppose the client sends:

```http
GET /users/42
Host: api.example.com
Authorization: Bearer <token>
Accept: application/json
```

The request eventually needs to:

1. Resolve `api.example.com`.
1. Establish a network connection.
1. Negotiate TLS if HTTPS is used.
1. Pass through edge/security infrastructure.
1. Reach the appropriate backend instance.
1. Enter the Python application server.
1. Pass through application middleware.
1. Authenticate the request.
1. Validate parameters.
1. Execute business logic.
1. Query the database.
1. Convert the result into the API response format.
1. Send the response back through the network.

______________________________________________________________________

# 3. Step 1 — Client

The client can be:

- Browser
- Mobile application
- Frontend application
- Another backend service
- CLI tool
- Automated job

The client constructs the HTTP request.

For example:

```http
GET /users/42
```

with relevant headers.

Before the request reaches your Python application, multiple networking layers may process it.

______________________________________________________________________

# 4. Step 2 — DNS

The client needs to resolve:

```text
api.example.com
```

to an IP address.

Conceptually:

```text
api.example.com
        ↓
      DNS
        ↓
    IP address
```

DNS can involve:

- Local caches
- OS resolver
- Recursive resolver
- Authoritative DNS server

If DNS fails, the request never reaches the backend application.

______________________________________________________________________

# 5. Step 3 — TCP

For a traditional HTTPS-over-TCP connection, the client establishes a TCP connection to the destination.

The connection starts with:

```text
SYN
SYN-ACK
ACK
```

The TCP layer provides reliable, ordered byte-stream delivery.

Connection setup contributes to latency when a connection cannot be reused.

______________________________________________________________________

# 6. Step 4 — TLS

For HTTPS, TLS is established over the TCP connection.

At a high level:

```text
TCP connection
      ↓
TLS handshake
      ↓
Encrypted HTTP traffic
```

TLS establishes:

- Secure communication
- Server authentication
- Encryption
- Integrity protection

If certificate validation fails, the HTTP request may never reach the application.

______________________________________________________________________

# 7. Connection Reuse

A client may maintain connection pools and reuse existing connections.

With connection reuse, the request may avoid repeating:

```text
TCP handshake
TLS handshake
```

This can significantly reduce latency for repeated requests.

Connection reuse can exist between multiple layers of the infrastructure as well.

______________________________________________________________________

# 8. Step 5 — CDN

A CDN can sit at the edge of the infrastructure.

It may:

- Cache responses
- Serve static content
- Terminate TLS
- Route traffic
- Reduce geographic latency
- Absorb traffic spikes

For dynamic API requests, the CDN may forward the request to the origin infrastructure.

Not every backend API uses a CDN.

______________________________________________________________________

# 9. Step 6 — WAF

A WAF (**Web Application Firewall**) can inspect HTTP requests for potentially malicious traffic.

It can enforce rules involving:

- IP reputation
- Request patterns
- Known attack signatures
- Rate limits
- Request size
- Suspicious payloads

A WAF can reject a request before it reaches your application.

This is an important failure point when debugging production traffic.

______________________________________________________________________

# 10. CDN vs WAF

They have different primary responsibilities.

### CDN

Primarily focuses on:

- Edge delivery
- Caching
- Traffic distribution
- Latency reduction

### WAF

Primarily focuses on:

- HTTP/application-layer security
- Request inspection
- Security rules

A single provider can offer both capabilities.

______________________________________________________________________

# 11. Step 7 — Load Balancer

The load balancer distributes requests across backend instances.

Example:

```text
                 ┌── Application 1
Client → LB ─────┼── Application 2
                 └── Application 3
```

The load balancer can consider:

- Health checks
- Backend availability
- Routing rules
- Connection capacity
- Load distribution

Its exact behavior depends on the infrastructure.

______________________________________________________________________

# 12. Health Checks

A load balancer typically needs to know whether an instance is healthy.

For example:

```http
GET /health
```

A health check might verify:

- Process availability
- Basic application readiness
- Required dependencies
- Database connectivity, depending on design

Be careful about making health checks excessively expensive.

______________________________________________________________________

# 13. Load Balancer Failure Points

Possible problems include:

- No healthy backend instances
- Incorrect target configuration
- Connection timeout
- TLS configuration mismatch
- Incorrect routing
- Backend overload
- Health checks failing

A request can therefore fail before reaching FastAPI.

______________________________________________________________________

# 14. Step 8 — Reverse Proxy

A reverse proxy receives requests on behalf of backend services.

Common responsibilities include:

- TLS termination
- Routing
- Header manipulation
- Connection management
- Compression
- Request-size limits
- Access logging
- Proxy timeouts

The reverse proxy may be:

- Nginx
- HAProxy
- Envoy
- Cloud infrastructure

The exact deployment varies.

______________________________________________________________________

# 15. Load Balancer vs Reverse Proxy

They can overlap.

### Load balancer

Primary concern:

> Which backend should receive this request?

### Reverse proxy

Primary concern:

> How should this request be handled and forwarded to the backend service?

In real systems, one component can perform both roles.

______________________________________________________________________

# 16. Step 9 — ASGI

ASGI stands for **Asynchronous Server Gateway Interface**.

It defines an interface between asynchronous Python application servers and Python web frameworks/applications.

FastAPI is ASGI-compatible.

A common deployment looks like:

```text
Reverse Proxy
      ↓
Uvicorn / another ASGI server
      ↓
FastAPI application
```

______________________________________________________________________

# 17. What Does the ASGI Server Do?

An ASGI server is responsible for handling network-level application connections and translating them into the ASGI
interface expected by the application.

Examples include:

- Uvicorn
- Hypercorn

The server handles protocol-level concerns and invokes the ASGI application.

______________________________________________________________________

# 18. ASGI vs WSGI

### WSGI

Traditional Python web-server interface designed primarily around synchronous request handling.

### ASGI

Designed to support asynchronous applications and protocols.

ASGI is particularly important for modern Python frameworks such as FastAPI.

______________________________________________________________________

# 19. Step 10 — FastAPI Routing

FastAPI receives the request through the ASGI interface.

It determines which route matches:

```http
GET /users/42
```

For example:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    ...
```

The route defines:

- HTTP method
- URL pattern
- Handler
- Parameters
- Dependencies
- Response behavior

______________________________________________________________________

# 20. Step 11 — Middleware

Middleware wraps request processing.

Conceptually:

```text
Request
   ↓
Middleware A
   ↓
Middleware B
   ↓
Route handler
   ↓
Middleware B
   ↓
Middleware A
   ↓
Response
```

Middleware can implement cross-cutting behavior such as:

- Logging
- Request IDs
- Authentication-related processing
- CORS
- Metrics
- Timing
- Error handling

______________________________________________________________________

# 21. Middleware Order Matters

Suppose you have:

```text
Logging
Authentication
Route
```

versus:

```text
Authentication
Logging
Route
```

The observed behavior can differ.

Middleware execution order should therefore be intentional.

This becomes particularly important when middleware depends on headers, request state or exception handling.

______________________________________________________________________

# 22. Step 12 — Authentication

Authentication answers:

> Who is making this request?

For example:

```http
Authorization: Bearer <token>
```

The application may validate:

- Token signature
- Expiration
- Issuer
- Audience
- Session
- API key

If authentication fails, the request should normally stop before protected business logic executes.

______________________________________________________________________

# 23. Authentication vs Authorization

These are different.

### Authentication

Who are you?

### Authorization

What are you allowed to do?

Example:

```text
Authenticated user
       ↓
Is admin?
       ↓
Allow / deny
```

A user can be successfully authenticated but still receive:

```text
403 Forbidden
```

because they lack permission.

______________________________________________________________________

# 24. Step 13 — Validation

Validation ensures incoming data satisfies expected requirements.

Examples:

```text
user_id must be integer
email must be valid
age must be positive
required field must exist
```

FastAPI commonly uses type annotations and validation models to define API input requirements.

Validation should happen before business logic relies on invalid input.

______________________________________________________________________

# 25. Path, Query and Body Validation

A request can contain data in different locations.

### Path

```http
/users/42
```

### Query

```http
/users?page=2&limit=20
```

### Body

```json
{
    "name": "Riyaz"
}
```

The framework can validate each according to the endpoint definition.

______________________________________________________________________

# 26. Validation Failure

If input is invalid, the application should return an appropriate client error rather than allowing malformed data into
business logic.

For example:

```text
Client
  ↓
Request validation
  ↓
Invalid
  ↓
4xx response
```

The database should not be queried unnecessarily when the request is already invalid.

______________________________________________________________________

# 27. Step 14 — Business Logic

After authentication and validation, the request reaches the application's business logic.

Example:

```python
async def get_user(user_id: int):
    user = await repository.get_by_id(user_id)

    if user is None:
        raise UserNotFound()

    return user
```

Business logic should contain domain behavior rather than networking concerns.

______________________________________________________________________

# 28. Service Layer

A common backend structure is:

```text
API / Router
     ↓
Service
     ↓
Repository
     ↓
Database
```

The router handles HTTP concerns.

The service handles business rules.

The repository handles persistence.

This separation is useful but should not become unnecessary abstraction.

______________________________________________________________________

# 29. Step 15 — ORM / Repository

The service may call a repository or ORM.

Example:

```text
Service
   ↓
Repository
   ↓
ORM
   ↓
Database driver
   ↓
Database
```

An ORM maps application objects to database structures and provides a higher-level interface for database operations.

Not every application uses an ORM.

______________________________________________________________________

# 30. Database Connection Pool

Applications typically avoid opening a brand-new database connection for every query.

Instead, they use a connection pool.

Conceptually:

```text
Application
    ↓
Connection Pool
    ├── Connection
    ├── Connection
    ├── Connection
    └── Connection
         ↓
      Database
```

The pool controls how many database connections can be active.

______________________________________________________________________

# 31. Connection Pool Exhaustion

Suppose:

```text
1000 concurrent requests
```

but:

```text
Database pool = 20 connections
```

Only a limited number can actively use database connections at once.

Excess requests may wait.

If waiting exceeds a timeout, requests can fail.

This is one reason why application concurrency must be designed around database capacity.

______________________________________________________________________

# 32. Database Query

The repository may execute:

```sql
SELECT id, name, email
FROM users
WHERE id = 42;
```

The database:

1. Parses the query.
1. Determines an execution plan.
1. Reads relevant data.
1. Applies constraints/locking as needed.
1. Returns the result.

The exact internal process depends on the database engine.

______________________________________________________________________

# 33. Database as a Latency Source

An endpoint can be slow even when Python code is fast.

Possible database causes include:

- Missing indexes
- Large scans
- Poor query plans
- Lock contention
- Connection-pool waits
- Network latency
- Expensive joins
- Excessive queries

This is why request tracing should include database timing.

______________________________________________________________________

# 34. N+1 Queries

A common ORM performance problem is:

```text
1 query for users
+
1 query per user for orders
```

For 100 users:

```text
101 database queries
```

This can create significant latency.

Solutions depend on the ORM and use case:

- Eager loading
- Explicit joins
- Batch queries
- Prefetching
- Query redesign

______________________________________________________________________

# 35. Step 16 — Business Result

The database result returns to the application.

The service may:

- Apply business rules
- Transform data
- Combine multiple sources
- Calculate derived values
- Remove sensitive fields

Only after business processing is complete should the API construct its response.

______________________________________________________________________

# 36. Step 17 — Serialization

The application converts internal objects into an API representation.

Example:

```python
User(
    id=42,
    name="Riyaz",
)
```

becomes:

```json
{
    "id": 42,
    "name": "Riyaz"
}
```

Serialization can include:

- Field selection
- Type conversion
- JSON encoding
- Response-model validation
- Sensitive-field exclusion

______________________________________________________________________

# 37. Response Models

A response model provides a defined API contract.

For example:

```python
class UserResponse(BaseModel):
    id: int
    name: str
```

Returning a controlled response model helps prevent accidental exposure of internal fields.

For example, an internal model might contain:

```text
password_hash
internal_notes
```

while the public response contains only:

```text
id
name
```

______________________________________________________________________

# 38. Step 18 — HTTP Response

FastAPI produces an HTTP response.

Conceptually:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 42,
    "name": "Riyaz"
}
```

The response travels back through the infrastructure to the client.

______________________________________________________________________

# 39. Response Path

The reverse journey may look like:

```text
FastAPI
  ↓
ASGI server
  ↓
Reverse proxy
  ↓
Load balancer
  ↓
CDN / edge
  ↓
Network
  ↓
Client
```

Each layer can affect:

- Headers
- Compression
- Connection behavior
- Caching
- Timeouts
- Observability

______________________________________________________________________

# 40. Blocking vs Non-Blocking

This is one of the most important aspects of the lifecycle for Python backend engineers.

Consider:

```python
async def endpoint():
    response = await async_client.get(url)
    return response
```

The asynchronous HTTP operation can allow other tasks to progress while waiting.

But:

```python
async def endpoint():
    response = requests.get(url)
    return response
```

contains a blocking call.

It can block the event-loop thread.

______________________________________________________________________

# 41. Blocking Database Operations

The same issue applies to database access.

If an async endpoint uses a synchronous database driver directly:

```python
async def endpoint():
    result = sync_db.execute(...)
```

the database call can block the event loop.

Use an async-compatible driver when appropriate, or deliberately isolate blocking work from the event loop.

______________________________________________________________________

# 42. CPU-Bound Work

CPU-heavy work can also block an async application.

Example:

```python
async def endpoint():
    result = expensive_calculation()
    return result
```

If the calculation takes a long time, other tasks sharing the event loop can be delayed.

Consider:

- Process pools
- Background workers
- Dedicated compute services

for significant CPU-heavy workloads.

______________________________________________________________________

# 43. Connection Handling Across Layers

A single logical request may involve several connections:

```text
Client
  ↓ connection
Load Balancer
  ↓ connection
Reverse Proxy
  ↓ connection
ASGI/Application
  ↓ connection
Database
```

These connections may be pooled or reused independently.

A bottleneck in one pool can increase request latency even when other layers are healthy.

______________________________________________________________________

# 44. Timeouts

Timeouts should exist at appropriate boundaries.

Examples:

```text
Client timeout
Load balancer timeout
Reverse proxy timeout
Application timeout
HTTP client timeout
Database timeout
```

The timeout configuration should be intentional.

A downstream service should not be allowed to hold resources indefinitely.

______________________________________________________________________

# 45. Failure Points

A request can fail at many stages:

```text
DNS
 ↓
TCP
 ↓
TLS
 ↓
CDN/WAF
 ↓
Load Balancer
 ↓
Reverse Proxy
 ↓
ASGI
 ↓
FastAPI
 ↓
Authentication
 ↓
Validation
 ↓
Business Logic
 ↓
Database
 ↓
Serialization
 ↓
Response
```

The status code and logs can help identify where the failure occurred.

______________________________________________________________________

# 46. Failure Examples

| Failure | Possible result |
|---|---|
| DNS failure | Client cannot resolve host |
| TCP failure | Connection refused/timeout |
| TLS failure | Certificate/handshake error |
| WAF rejection | 4xx/security response |
| No healthy backend | 503/edge-specific response |
| Proxy timeout | 504 |
| Authentication failure | 401 |
| Authorization failure | 403 |
| Validation failure | 4xx |
| Business conflict | 409 |
| Database timeout | 5xx or application-specific error |
| Unhandled exception | 500 |
| Serialization failure | 5xx |

Exact responses depend on the infrastructure and application.

______________________________________________________________________

# 47. Observability

Production systems need visibility into requests.

The three common observability pillars are:

### Logs

Detailed events.

### Metrics

Numerical measurements over time.

### Traces

Request journeys across services/components.

______________________________________________________________________

# 48. Request ID

A request ID can be generated or propagated:

```text
Request ID: abc-123
```

Then the same identifier can appear in:

```text
Load balancer logs
Reverse proxy logs
Application logs
Database-related logs
Downstream service logs
```

This makes debugging a single request much easier.

______________________________________________________________________

# 49. Distributed Tracing

Consider:

```text
API
 ↓
User Service
 ↓
Payment Service
 ↓
Database
```

A distributed trace can show the time spent in each component.

Conceptually:

```text
Total request: 800ms

API              800ms
 ├─ User Service 200ms
 ├─ Payment      500ms
 │   └─ DB       400ms
 └─ Serialization 20ms
```

This helps identify the actual bottleneck.

______________________________________________________________________

# 50. Metrics

Useful request metrics include:

- Request count
- Request rate
- Error rate
- Latency
- p50
- p95
- p99
- Status-code distribution
- Active connections
- Database pool utilization

Average latency alone can hide serious tail-latency problems.

______________________________________________________________________

# 51. Logs

Good application logs should provide useful context without leaking sensitive information.

Useful fields include:

```text
timestamp
request_id
route
method
status_code
latency
user/service identity where appropriate
error type
```

Avoid logging:

- Passwords
- Tokens
- Secrets
- Sensitive personal data unnecessarily

______________________________________________________________________

# 52. Request Lifecycle Timing

For a slow request, break down:

```text
DNS
TCP
TLS
Edge
LB
Proxy
Application
Database
External APIs
Serialization
Response
```

Then identify which stage dominates.

Do not optimize Python code before confirming that Python is actually the bottleneck.

______________________________________________________________________

# 53. Complete Example

Suppose:

```http
GET /orders/100
```

The journey could be:

```text
1. Client resolves api.example.com
2. DNS returns an address
3. Client establishes/reuses TCP connection
4. TLS is established/reused
5. CDN/WAF receives the request
6. Load balancer selects an application instance
7. Reverse proxy forwards the request
8. ASGI server receives it
9. FastAPI matches the route
10. Middleware records request metadata
11. Authentication validates the caller
12. FastAPI validates order_id
13. Service executes business logic
14. Repository queries the database
15. Database returns order data
16. Service applies business rules
17. Response model serializes the result
18. ASGI sends the response
19. Proxy/load balancer forwards it
20. Client receives the response
```

This is the complete mental model you should be able to explain in an interview.

______________________________________________________________________

# 54. Senior-Level Debugging Approach

If an API suddenly becomes slow:

### Step 1 — Establish scope

Is it:

- One endpoint?
- All endpoints?
- One customer?
- One region?
- All instances?

### Step 2 — Check metrics

Look at:

- Request rate
- Error rate
- p95/p99 latency
- CPU
- Memory
- Connection pools

### Step 3 — Check traces

Find where the request spends time.

### Step 4 — Check logs

Use request IDs to correlate events.

### Step 5 — Check dependencies

Inspect:

- Database
- Redis
- External APIs
- Message systems

### Step 6 — Identify the bottleneck

Only then optimize.

______________________________________________________________________

# 55. Common Request-Lifecycle Mistakes

## Mistake 1 — Thinking the request goes directly from client to FastAPI

There may be several infrastructure layers before the application.

______________________________________________________________________

## Mistake 2 — Treating the load balancer and reverse proxy as always separate

They may be separate components or combined responsibilities.

______________________________________________________________________

## Mistake 3 — Assuming `async def` makes all operations non-blocking

Blocking libraries can still block the event loop.

______________________________________________________________________

## Mistake 4 — Ignoring connection pools

Database and HTTP client pools can become bottlenecks.

______________________________________________________________________

## Mistake 5 — Looking only at application logs

The problem may be DNS, TLS, proxy, load balancer or a downstream service.

______________________________________________________________________

## Mistake 6 — Measuring only average latency

p95/p99 latency can reveal serious production problems hidden by averages.

______________________________________________________________________

## Mistake 7 — Logging secrets

Observability must not compromise security.

______________________________________________________________________

# 56. Interview Questions & Answers

## Q1. Explain the complete lifecycle of an HTTP request to a FastAPI application.

**Answer:**

A typical path is:

```text
Client
→ DNS
→ TCP/TLS
→ CDN/WAF
→ Load Balancer
→ Reverse Proxy
→ ASGI server
→ FastAPI
→ Middleware
→ Authentication
→ Validation
→ Business Logic
→ ORM/Repository
→ Database
→ Serialization
→ Response
```

Not every deployment contains every layer.

______________________________________________________________________

## Q2. What happens before a request reaches FastAPI?

**Answer:**

Depending on the architecture, DNS resolution, TCP/TLS setup, CDN/WAF processing, load balancing and reverse-proxy
forwarding can occur before the request reaches the ASGI server and FastAPI.

______________________________________________________________________

## Q3. What is the role of an ASGI server?

**Answer:**

It handles network/application protocol concerns and exposes the ASGI interface through which asynchronous Python
applications such as FastAPI receive requests.

______________________________________________________________________

## Q4. FastAPI vs Uvicorn?

**Answer:**

FastAPI is the web framework/application layer.

Uvicorn is an ASGI server that runs the application and handles the server-side network/application protocol
integration.

______________________________________________________________________

## Q5. What does middleware do?

**Answer:**

Middleware wraps request processing and provides cross-cutting functionality such as logging, metrics, CORS, request IDs
and error handling.

______________________________________________________________________

## Q6. Why does middleware order matter?

**Answer:**

Middleware wraps other middleware and the endpoint.

Changing order can change which middleware sees a request first and how responses/errors propagate.

______________________________________________________________________

## Q7. Authentication vs authorization?

**Answer:**

Authentication determines who the caller is.

Authorization determines what the authenticated caller is allowed to do.

______________________________________________________________________

## Q8. Where does validation happen?

**Answer:**

At the API boundary, before business logic relies on the incoming data.

FastAPI can validate path, query and body data according to endpoint definitions and models.

______________________________________________________________________

## Q9. What belongs in business logic?

**Answer:**

Domain rules and application behavior.

It should generally not be tightly coupled to HTTP-specific concerns.

______________________________________________________________________

## Q10. What is the role of a repository?

**Answer:**

A repository can provide an abstraction around persistence operations, allowing business logic to interact with stored
data without directly embedding database access details.

______________________________________________________________________

## Q11. What is an ORM?

**Answer:**

An ORM maps application-level objects and operations to relational database structures and queries.

______________________________________________________________________

## Q12. Why use a database connection pool?

**Answer:**

Creating database connections repeatedly is expensive.

A pool reuses connections and controls the number of simultaneous database connections.

______________________________________________________________________

## Q13. What happens if the database pool is exhausted?

**Answer:**

Requests needing a connection may wait.

If they cannot obtain one before the configured timeout, they can fail.

This can increase latency and trigger cascading failures.

______________________________________________________________________

## Q14. What is serialization?

**Answer:**

Serialization converts internal application data into a representation suitable for transmission, such as JSON.

______________________________________________________________________

## Q15. Why are response models useful?

**Answer:**

They define and enforce a response contract and can prevent accidental exposure of internal fields.

______________________________________________________________________

## Q16. What is the difference between blocking and non-blocking work?

**Answer:**

Blocking work prevents the current execution context from progressing until the operation completes.

Non-blocking asynchronous operations can suspend and allow other work to progress while waiting.

______________________________________________________________________

## Q17. Why is blocking code dangerous in an async FastAPI application?

**Answer:**

Blocking code can block the event-loop thread, preventing other asynchronous requests/tasks from making progress.

______________________________________________________________________

## Q18. Is database access always blocking?

**Answer:**

No.

It depends on the driver and API being used.

An async-compatible database driver can perform non-blocking I/O from an async application, while a synchronous driver
can block.

______________________________________________________________________

## Q19. What happens if CPU-heavy work runs inside an async endpoint?

**Answer:**

It can block the event loop and increase latency for other tasks.

Significant CPU-heavy work should generally be moved to processes, worker systems or another appropriate execution
model.

______________________________________________________________________

## Q20. Where can a request fail?

**Answer:**

Almost anywhere:

```text
DNS
TCP
TLS
WAF
Load Balancer
Proxy
ASGI
Authentication
Validation
Business Logic
Database
External services
Serialization
```

The correct diagnosis requires identifying the first failing layer.

______________________________________________________________________

## Q21. What is a request ID?

**Answer:**

A unique identifier associated with a request that can be propagated through infrastructure and services to correlate
logs and traces.

______________________________________________________________________

## Q22. What are the three pillars of observability?

**Answer:**

Logs, metrics and traces.

______________________________________________________________________

## Q23. What metrics would you monitor for an API?

**Answer:**

At minimum:

- Request rate
- Error rate
- Latency
- p95/p99 latency
- Status-code distribution
- Resource utilization
- Connection-pool utilization

______________________________________________________________________

## Q24. Why are p95 and p99 useful?

**Answer:**

They describe tail latency.

A service can have a good average while a significant minority of requests are extremely slow.

______________________________________________________________________

## Q25. How would you debug a slow endpoint?

**Answer:**

Start with metrics, then use traces to identify where time is spent, correlate logs using request IDs, inspect
database/external dependencies and only then optimize the confirmed bottleneck.

______________________________________________________________________

## Q26. CDN vs WAF?

**Answer:**

A CDN primarily improves edge delivery, caching and latency.

A WAF primarily inspects and protects HTTP traffic.

A provider can offer both.

______________________________________________________________________

## Q27. Load balancer vs reverse proxy?

**Answer:**

A load balancer primarily distributes traffic among available backend instances.

A reverse proxy receives requests on behalf of backend services and can handle routing, connection management, TLS
termination and other proxy responsibilities.

The roles can overlap in real deployments.

______________________________________________________________________

## Q28. Why can a request be slow even when Python execution is fast?

**Answer:**

Time may be spent in:

- Network setup
- Proxying
- Database queries
- Connection-pool waits
- External APIs
- Serialization
- Downstream services

The complete request path must be measured.

______________________________________________________________________

## Q29. What is an N+1 query problem?

**Answer:**

The application performs one query for a collection and then an additional query for each item, resulting in many
database round trips.

It can often be addressed through batching, eager loading, joins or query redesign.

______________________________________________________________________

## Q30. Why should health checks be lightweight?

**Answer:**

They may execute frequently.

An expensive health check can consume resources and can incorrectly make an otherwise healthy service appear
unavailable.

______________________________________________________________________

## Q31. How can timeouts cause cascading failures?

**Answer:**

If upstream requests wait too long, they consume threads/tasks/connections.

As concurrency grows, resource pools can become exhausted and cause additional requests to time out.

______________________________________________________________________

## Q32. How would you explain the lifecycle to a non-networking engineer?

**Answer:**

Start with the simple chain:

```text
Find the server
→ establish secure connection
→ pass through infrastructure
→ route to application
→ authenticate/validate
→ execute business logic
→ access data
→ build response
→ send it back
```

Then expand each stage only when needed.

______________________________________________________________________

# 57. Scenario-Based Questions

## Scenario 1 — FastAPI Is Healthy but Clients Get 503

Application logs show no incoming requests.

**Question:** Where would you investigate?

**Answer:**

Look before FastAPI:

- Load balancer health checks
- Reverse proxy
- Target registration
- Network connectivity
- WAF/CDN
- Routing
- Backend health

If requests never reach the application, application logs cannot explain the failure.

______________________________________________________________________

## Scenario 2 — API Has High p99 Latency

Average latency is 100 ms, but p99 is 5 seconds.

**Question:** What would you investigate?

**Answer:**

Use traces and request-level data to identify whether slow requests are caused by:

- Database waits
- Connection-pool exhaustion
- External APIs
- Lock contention
- Network issues
- CPU saturation

Do not optimize based only on average latency.

______________________________________________________________________

## Scenario 3 — Database Pool Exhaustion

The application has:

```text
500 concurrent requests
20 database connections
```

Many requests are waiting.

**Question:** What would you do?

**Answer:**

Do not simply increase the pool.

Investigate:

- Query latency
- Connection hold time
- N+1 queries
- Transaction duration
- Database capacity
- Application concurrency

Then choose an appropriate pool size and concurrency limit.

______________________________________________________________________

## Scenario 4 — Blocking HTTP Client

An async FastAPI endpoint uses:

```python
requests.get(...)
```

**Question:** What is the problem?

**Answer:**

The synchronous call can block the event loop.

Use an async HTTP client or isolate the blocking operation in a thread/executor.

______________________________________________________________________

## Scenario 5 — CPU Spike

An endpoint performs a large data transformation.

CPU reaches 100% and all endpoints become slower.

**Question:** Why can one endpoint affect unrelated endpoints?

**Answer:**

If CPU-heavy work runs on shared application workers/event-loop threads, it can consume execution capacity needed by
other requests.

Move CPU-heavy work to appropriate worker/process capacity or scale the service.

______________________________________________________________________

## Scenario 6 — 504 from Reverse Proxy

The application eventually completes successfully, but clients receive 504 responses.

**Question:** What could be happening?

**Answer:**

The proxy timeout may be shorter than the application's processing time.

Investigate:

- Proxy timeout
- Load-balancer timeout
- Application timeout
- Database latency
- External calls

The correct fix may be reducing application latency rather than simply increasing the timeout.

______________________________________________________________________

## Scenario 7 — Authentication Is Slow

A request takes 700 ms before business logic starts.

Tracing shows 600 ms in authentication.

**Question:** What would you investigate?

**Answer:**

Determine what authentication is doing:

- Remote token introspection
- Database lookup
- External identity provider
- Cryptographic processing
- Network connection setup

Then optimize or cache appropriate information without weakening security.

______________________________________________________________________

## Scenario 8 — Serialization Bottleneck

Database and business logic complete quickly, but response generation takes significant time.

**Question:** What could cause this?

**Answer:**

Possible causes include:

- Very large response objects
- Expensive model conversion
- Deep nested serialization
- Large JSON encoding
- Unnecessary fields

Reduce payload size and serialization work where appropriate.

______________________________________________________________________

## Scenario 9 — Debugging One Customer's Slow Requests

Only requests from one customer are slow.

**Question:** How would you investigate?

**Answer:**

Use request/customer identifiers and traces to compare:

```text
Normal request
vs
Affected request
```

Look for differences in:

- Data size
- Database queries
- Authorization rules
- External calls
- Routing
- Region
- Cache behavior

______________________________________________________________________

## Scenario 10 — Missing Logs

A request fails in production but application logs cannot be correlated with the client's report.

**Question:** What would you improve?

**Answer:**

Introduce a request/correlation ID and propagate it across relevant infrastructure and services.

Ensure logs include the ID and useful request metadata without exposing sensitive data.

______________________________________________________________________

# 58. Practice Exercises

## Exercise 1 — Draw the Lifecycle

From memory, write:

```text
Client → DNS → TCP/TLS → CDN/WAF → Load Balancer → Reverse Proxy → ASGI → FastAPI → Middleware → Authentication → Validation → Business Logic → ORM → Database → Serialization → Response
```

Then explain each layer in one sentence.

______________________________________________________________________

## Exercise 2 — Trace a FastAPI Request

Take a simple endpoint:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    ...
```

Document what happens from the client sending the request until the response reaches the client.

______________________________________________________________________

## Exercise 3 — Identify Blocking Operations

Review a FastAPI endpoint and classify every operation as:

```text
CPU-bound
Blocking I/O
Non-blocking I/O
```

Identify anything that could block the event loop.

______________________________________________________________________

## Exercise 4 — Failure Mapping

For each failure:

```text
DNS failure
TCP timeout
TLS failure
WAF rejection
503
401
403
422
500
502
504
Database timeout
```

Identify the most likely layer.

______________________________________________________________________

## Exercise 5 — Connection Pools

Given:

```text
Application concurrency: 200
DB pool: 20
Average DB operation: 100 ms
```

Explain what happens when all requests require the database.

Identify potential bottlenecks.

______________________________________________________________________

## Exercise 6 — Observability Design

Design observability for a backend service.

Include:

- Request ID
- Structured logs
- Metrics
- Distributed traces
- p95/p99 latency
- Error rate
- Database timing

Explain how these tools work together.

______________________________________________________________________

## Exercise 7 — Slow Request Investigation

A request has:

```text
Total: 3 seconds
DNS: 10 ms
TLS: 20 ms
Application: 2.7 seconds
Database: 2.5 seconds
Serialization: 20 ms
```

Identify the likely bottleneck and propose the first three things you would investigate.

______________________________________________________________________

## Exercise 8 — N+1 Detection

Create an endpoint that loads:

```text
100 users
```

and then fetches each user's orders separately.

Measure the number of database queries.

Refactor it to use batching/eager loading.

______________________________________________________________________

## Exercise 9 — Timeout Chain

Design timeout values across:

```text
Client
Load Balancer
Reverse Proxy
Application
HTTP Client
Database
```

Explain why the values should be intentionally coordinated.

______________________________________________________________________

## Exercise 10 — Senior Interview Explanation

Explain this scenario aloud:

> A user sends an HTTPS request to an API. Explain everything that happens until the user receives JSON.

Your explanation should take approximately 3–5 minutes and cover every major layer without getting lost in
implementation details.

______________________________________________________________________

# 59. Quick Revision

| Layer / Concept | Key Point |
|---|---|
| Client | Creates the HTTP request |
| DNS | Resolves hostname |
| TCP | Reliable transport connection |
| TLS | Secures HTTPS traffic |
| CDN | Edge delivery/caching |
| WAF | HTTP/application-layer protection |
| Load Balancer | Distributes traffic |
| Reverse Proxy | Receives and forwards requests |
| ASGI | Python async application interface |
| ASGI Server | Runs the ASGI application |
| FastAPI | Python web framework |
| Middleware | Cross-cutting request/response processing |
| Authentication | Identifies caller |
| Authorization | Determines permissions |
| Validation | Checks incoming data |
| Business Logic | Implements domain behavior |
| Repository | Persistence abstraction |
| ORM | Maps application operations to database structures |
| Connection Pool | Reuses/limits database connections |
| Database | Persists and queries data |
| Serialization | Converts internal data to response format |
| Response Model | Defines API response contract |
| Request ID | Correlates request logs |
| Metrics | Quantitative system measurements |
| Logs | Detailed events |
| Traces | Request journey across components |
| p95/p99 | Tail latency |
| Blocking | Prevents current execution context from progressing |
| Non-blocking | Allows other work to progress while waiting |
| N+1 | Excessive per-item database queries |
| Timeout | Bounds waiting time |

______________________________________________________________________

# 60. Completion Checklist

Before moving to File 14, make sure you can explain:

- [ ] Complete request lifecycle
- [ ] Client
- [ ] DNS
- [ ] TCP
- [ ] TLS
- [ ] Connection reuse
- [ ] CDN
- [ ] WAF
- [ ] CDN vs WAF
- [ ] Load balancer
- [ ] Health checks
- [ ] Load-balancer failure points
- [ ] Reverse proxy
- [ ] Load balancer vs reverse proxy
- [ ] ASGI
- [ ] ASGI server
- [ ] ASGI vs WSGI
- [ ] FastAPI routing
- [ ] Middleware
- [ ] Middleware order
- [ ] Authentication
- [ ] Authentication vs authorization
- [ ] Request validation
- [ ] Path/query/body validation
- [ ] Business logic
- [ ] Service layer
- [ ] Repository
- [ ] ORM
- [ ] Database connection pools
- [ ] Pool exhaustion
- [ ] Database latency
- [ ] N+1 queries
- [ ] Serialization
- [ ] Response models
- [ ] Blocking vs non-blocking
- [ ] Blocking database calls
- [ ] CPU-bound work
- [ ] Connection handling
- [ ] Timeouts
- [ ] Failure points
- [ ] Logs
- [ ] Metrics
- [ ] Distributed traces
- [ ] Request IDs
- [ ] p95/p99
- [ ] Senior-level debugging approach

______________________________________________________________________

# 61. Interview Readiness Test

Answer these aloud without looking at the notes:

1. Explain the complete lifecycle of an HTTP request to a FastAPI application.
1. What happens before a request reaches FastAPI?
1. What is the role of an ASGI server?
1. FastAPI vs Uvicorn?
1. What does middleware do?
1. Why does middleware order matter?
1. Authentication vs authorization?
1. Where should request validation happen?
1. What belongs in business logic?
1. What is the role of a repository?
1. What is an ORM?
1. Why use a database connection pool?
1. What happens when the pool is exhausted?
1. What is serialization?
1. Why are response models useful?
1. Blocking vs non-blocking?
1. Why is blocking code dangerous in async FastAPI?
1. Is database access always blocking?
1. What happens when CPU-heavy work runs in an async endpoint?
1. Where can a request fail?
1. What is a request ID?
1. What are the three pillars of observability?
1. What API metrics would you monitor?
1. Why are p95 and p99 more useful than average latency alone?
1. How would you debug a slow endpoint?
1. CDN vs WAF?
1. Load balancer vs reverse proxy?
1. Why can an API be slow even when Python execution is fast?
1. What is an N+1 query problem?
1. Why should health checks be lightweight?
1. How can timeout configuration cause cascading failures?
1. Explain the full lifecycle of `GET /users/42`.
1. An API returns 503 but FastAPI has no incoming-request logs. Where would you investigate?
1. An API has good p50 but terrible p99. What would you investigate?
1. Database pool utilization reaches 100%. What would you check before increasing the pool?
1. An async FastAPI endpoint uses `requests.get()`. What is wrong?
1. One CPU-heavy endpoint makes unrelated endpoints slow. Why?
1. The application completes in 10 seconds but the reverse proxy returns 504 after 5 seconds. Explain the failure.
1. Authentication consumes most of the request latency. How would you investigate?
1. Serialization becomes the bottleneck for large responses. What would you optimize?
1. Only one customer experiences slow requests. How would you isolate the problem?
1. How would you correlate a client-reported failure with logs across multiple services?
1. Explain the complete client-to-database-to-client path in 3–5 minutes.

If you can explain the lifecycle clearly without confusing infrastructure responsibilities with application
responsibilities, this topic is complete.

______________________________________________________________________

**Previous:** [12. HTTP, TCP/IP, TLS & Networking](./12-http-networking.md)

**Next:** [14. FastAPI Fundamentals](./14-fastapi-core.md)
