# 39. Backend Architecture Building Blocks

**Previous:** [38. System Design Fundamentals](./38-system-design-fundamentals.md)

**Next:** [40. Practical System Design](./40-system-design-practice.md)

______________________________________________________________________

## Objective

By the end of this topic, you should be able to:

- Explain the purpose of the major components used in backend architectures.
- Understand where load balancers and reverse proxies fit.
- Explain the role of CDNs and API gateways.
- Understand cache placement and responsibilities.
- Understand primary databases and read replicas.
- Explain message queues and Pub/Sub.
- Understand object storage.
- Understand when a search engine is appropriate.
- Compare WebSockets, long polling and webhooks.
- Understand service discovery.
- Compare monoliths and microservices.
- Choose components based on requirements rather than technology trends.
- Explain the trade-offs and failure modes introduced by each building block.

> **Scope:** This topic focuses on practical architecture understanding. It does not attempt to provide complete implementation guides for every infrastructure component.

______________________________________________________________________

# 1. Architecture Building Blocks

A production backend is usually assembled from several reusable building blocks.

A simplified architecture might contain:

```text
Client
  ↓
CDN / API Gateway
  ↓
Load Balancer
  ↓
Reverse Proxy
  ↓
Application
  ├── Cache
  ├── Database
  ├── Search
  ├── Queue → Workers
  └── Object Storage
```

Not every system needs every component.

The key question is:

> **What problem does this component solve?**

______________________________________________________________________

# 2. Load Balancer

A load balancer distributes incoming traffic across multiple backend instances.

Conceptually:

```text
              Load Balancer
              /     |     \
            App1   App2   App3
```

Its responsibilities can include:

- Traffic distribution
- Health checks
- Connection handling
- Failover
- TLS termination in some architectures
- Routing

______________________________________________________________________

# 3. Why Use a Load Balancer?

Suppose one application server handles:

```text
1,000 RPS
```

and traffic grows to:

```text
3,000 RPS
```

Instead of relying on one server:

```text
             App
              ↑
            Clients
```

use:

```text
             Load Balancer
             /     |     \
           App1   App2   App3
```

This enables horizontal scaling.

______________________________________________________________________

# 4. Load-Balancing Algorithms

Common approaches include:

### Round Robin

Requests are distributed sequentially:

```text
App1 → App2 → App3 → App1
```

### Least Connections

Send traffic toward an instance with fewer active connections.

### Weighted Routing

More powerful instances receive more traffic.

### Hash-Based Routing

A value such as a client identifier can influence which backend receives the request.

The appropriate algorithm depends on workload and requirements.

______________________________________________________________________

# 5. Load Balancer Health Checks

A load balancer should avoid routing traffic to unhealthy instances.

Common checks include:

```text
/health
/readiness
```

Distinguish:

### Liveness

Is the process alive?

### Readiness

Can this instance safely receive traffic?

An application can be alive but not ready.

______________________________________________________________________

# 6. Load Balancer Failure

A load balancer can itself become a failure point.

Production architectures commonly use:

```text
Redundancy
Failover
Managed load-balancing infrastructure
```

The exact mechanism depends on the deployment environment.

The important system-design question is:

> What happens if this component fails?

______________________________________________________________________

# 7. Reverse Proxy

A reverse proxy sits in front of backend services.

Conceptually:

```text
Client
  ↓
Reverse Proxy
  ↓
Application
```

Examples of responsibilities:

- Routing
- TLS termination
- Request buffering
- Compression
- Static content handling
- Header manipulation
- Access control
- Connection management

______________________________________________________________________

# 8. Reverse Proxy vs Forward Proxy

### Forward proxy

Acts on behalf of the client.

```text
Client
 ↓
Forward Proxy
 ↓
Internet
```

### Reverse proxy

Acts on behalf of servers.

```text
Internet
 ↓
Reverse Proxy
 ↓
Backend
```

This distinction is commonly asked in interviews.

______________________________________________________________________

# 9. Load Balancer vs Reverse Proxy

These concepts can overlap.

A reverse proxy can perform load balancing:

```text
Reverse Proxy
 ├── App1
 ├── App2
 └── App3
```

A dedicated load balancer may provide additional infrastructure-level capabilities.

The important point is:

> The terms describe roles, and a single product can perform multiple roles.

______________________________________________________________________

# 10. CDN

A Content Delivery Network caches and serves content from geographically distributed edge locations.

Conceptually:

```text
User
 ↓
Nearest CDN Edge
 ↓ cache hit
Response
```

On a cache miss:

```text
User
 ↓
CDN
 ↓
Origin
```

______________________________________________________________________

# 11. What Belongs in a CDN?

CDNs are especially useful for content such as:

```text
Images
CSS
JavaScript
Videos
Downloads
Static files
Cacheable API responses
```

The exact caching policy depends on the application's requirements.

______________________________________________________________________

# 12. CDN Benefits

A CDN can provide:

- Lower latency
- Reduced origin traffic
- Better handling of geographic distribution
- Edge caching
- Traffic absorption
- Some security capabilities

But caching introduces freshness and invalidation concerns.

______________________________________________________________________

# 13. CDN Cache Invalidation

Suppose an image changes:

```text
/logo.png
```

but the CDN still has the old version.

Possible strategies:

```text
Short TTL
Purge/invalidation
Versioned filenames
```

A common approach is:

```text
logo.v2.png
```

so the new resource has a different cache key.

______________________________________________________________________

# 14. CDN vs Application Cache

### CDN

Usually closer to the user and optimized for edge delivery.

### Application cache

Usually closer to the application and often used for dynamic application data.

Example:

```text
User
 ↓
CDN
 ↓
Application
 ↓
Redis
 ↓
Database
```

These layers can coexist.

______________________________________________________________________

# 15. API Gateway

An API gateway is an entry point for APIs and can provide cross-cutting functionality.

Possible responsibilities:

```text
Authentication
Authorization
Routing
Rate limiting
Request transformation
Logging
Observability
TLS termination
```

______________________________________________________________________

# 16. Why Use an API Gateway?

Suppose there are several services:

```text
Users
Orders
Payments
Notifications
```

Without a gateway, clients may need to know about each service.

With a gateway:

```text
Client
  ↓
API Gateway
  ├── Users
  ├── Orders
  ├── Payments
  └── Notifications
```

The gateway provides a stable external entry point.

______________________________________________________________________

# 17. API Gateway Trade-Offs

Benefits:

```text
Centralized cross-cutting concerns
Simpler client integration
Routing control
```

Costs:

```text
Additional component
Potential bottleneck
Operational complexity
Failure impact
```

Do not introduce a gateway merely because a system has multiple services.

______________________________________________________________________

# 18. API Gateway vs Reverse Proxy

They can overlap.

A reverse proxy primarily provides infrastructure/network-level proxying.

An API gateway is typically more API-aware and may handle:

```text
Authentication
Rate limiting
API policies
Version routing
Request transformation
```

The exact boundary depends on the platform.

______________________________________________________________________

# 19. Cache

A cache stores frequently accessed data in a faster layer.

Typical architecture:

```text
Application
 ↓
Cache
 ↓ miss
Database
```

Common cache technologies provide in-memory access and expiration mechanisms.

______________________________________________________________________

# 20. Cache Placement

Caching can occur at several levels:

```text
Browser
CDN
API Gateway
Application
Redis
Database/page cache
```

Each layer solves different problems.

______________________________________________________________________

# 21. Cache-Aside

A common pattern:

```text
Application
 ↓
Cache
 ↓ miss
Database
 ↓
Cache
```

Typical flow:

1. Check cache.
1. If hit, return value.
1. If miss, read database.
1. Store result in cache.
1. Return result.

______________________________________________________________________

# 22. Cache Invalidation

When data changes:

```text
Database updated
```

the cached value may become stale.

Strategies include:

```text
Delete cache key
Update cache
TTL expiration
Versioned keys
```

There is no universal invalidation strategy.

______________________________________________________________________

# 23. Cache Stampede

Suppose a popular cache entry expires.

Many requests arrive simultaneously:

```text
Request 1 ─┐
Request 2 ─┤
Request 3 ─┼→ Database
Request 4 ─┤
Request 5 ─┘
```

The database suddenly receives many identical requests.

Possible mitigations:

```text
Request coalescing
Locking
Jittered TTLs
Early refresh
Stale-while-revalidate
```

______________________________________________________________________

# 24. Database

The database is usually the durable source of truth for application data.

Examples of responsibilities:

```text
Persistence
Transactions
Queries
Constraints
Relationships
Indexes
Concurrency control
```

Database choice should follow access patterns and consistency requirements.

______________________________________________________________________

# 25. Primary Database

A primary database typically handles writes.

Example:

```text
Application
    ↓
Primary DB
```

In a replicated architecture:

```text
             Primary
            /       \
           ↓         ↓
       Replica 1  Replica 2
```

Writes generally go to the primary while replicas can serve eligible reads.

______________________________________________________________________

# 26. Read Replicas

Read replicas copy data from a primary database and can serve read traffic.

Benefits:

```text
Higher read capacity
Reduced primary load
Geographic distribution possibilities
```

Trade-offs:

```text
Replication lag
Additional operational complexity
Read-after-write concerns
```

______________________________________________________________________

# 27. Read-After-Write Problem

Suppose:

```text
Write → Primary
Read  → Replica
```

If replication is delayed, the read may not see the new value.

Possible strategies include:

```text
Read from primary for critical reads
Session/consistency-aware routing
Wait for replication
```

The appropriate strategy depends on the consistency requirement.

______________________________________________________________________

# 28. When Read Replicas Help

Read replicas are useful when:

```text
Reads significantly exceed writes
```

For example:

```text
90% reads
10% writes
```

But replicas do not solve every database bottleneck.

If the bottleneck is:

```text
Write throughput
```

adding read replicas may not help.

______________________________________________________________________

# 29. Message Queue

A message queue decouples producers from consumers.

```text
Producer
   ↓
 Queue
   ↓
Consumer
```

The producer does not necessarily wait for the consumer to finish processing.

______________________________________________________________________

# 30. Why Use a Queue?

Queues are useful for:

- Background jobs
- Burst absorption
- Asynchronous processing
- Retryable operations
- Decoupling services
- Smoothing traffic

Example:

```text
FastAPI
 ↓
Queue
 ↓
Worker
 ↓
Email provider
```

______________________________________________________________________

# 31. Queue Semantics

Important questions include:

```text
Can messages be lost?
Can messages be duplicated?
Does order matter?
How long should messages be retained?
What happens after repeated failures?
```

These requirements determine queue configuration and consumer design.

______________________________________________________________________

# 32. Consumer Idempotency

At-least-once delivery can produce duplicate messages.

Example:

```text
Message received
 ↓
Database update succeeds
 ↓
Consumer crashes before ACK
 ↓
Message delivered again
```

The consumer should therefore be designed to handle duplicates safely when using at-least-once semantics.

______________________________________________________________________

# 33. Pub/Sub

Publish/Subscribe allows a producer to publish an event that multiple subscribers can consume.

```text
             Publisher
                 ↓
              Topic
           /     |     \
          ↓      ↓      ↓
       Service A B     C
```

This differs from a traditional work queue where one message is typically processed by one consumer in a
competing-consumer model.

______________________________________________________________________

# 34. Queue vs Pub/Sub

### Queue

Often used for:

```text
Do this work
```

Example:

```text
Generate report
```

### Pub/Sub

Often used for:

```text
Something happened
```

Example:

```text
OrderCreated
```

Multiple services may react independently.

______________________________________________________________________

# 35. Event-Driven Architecture

Pub/Sub enables event-driven systems.

Example:

```text
Order Service
     ↓
OrderCreated
     ↓
 ┌───┼────┬──────┐
 ↓   ↓    ↓      ↓
Email Inventory Analytics Fraud
```

The producer does not need to synchronously call every downstream consumer.

______________________________________________________________________

# 36. Eventual Consistency

Event-driven systems often introduce eventual consistency.

Example:

```text
Order created
 ↓
Inventory event processing
 ↓
Email event processing
 ↓
Analytics event processing
```

These updates may happen at different times.

The system may therefore be temporarily inconsistent across services.

______________________________________________________________________

# 37. Object Storage

Object storage is designed for large files/blobs.

Examples:

```text
Images
Videos
Backups
Reports
Documents
Logs
Data exports
```

Typical architecture:

```text
Application
 ↓
Object Storage
```

The database stores metadata rather than large binary content when appropriate.

______________________________________________________________________

# 38. Why Not Store Large Files in the Database?

Large files in a relational database can:

```text
Increase database size
Increase backup cost
Increase I/O pressure
Complicate scaling
```

Object storage is optimized for large objects and independent scaling.

This is not an absolute rule; the correct choice depends on access patterns and requirements.

______________________________________________________________________

# 39. Direct-to-Object-Storage Uploads

For large uploads:

```text
Client
 ↓
Application
 ↓
Object Storage
```

can make the application server a bottleneck.

A common design is:

```text
Client
 ↓
Application → signed upload URL
 ↓
Object Storage
```

The client then uploads directly to object storage.

______________________________________________________________________

# 40. Search

Search engines are optimized for search-oriented workloads.

Examples of requirements:

```text
Full-text search
Ranking
Fuzzy matching
Filtering
Faceting
Autocomplete
```

A relational database can handle many search requirements, but specialized search systems become useful when search
complexity or scale demands them.

______________________________________________________________________

# 41. Search Architecture

A common architecture is:

```text
Primary Database
      ↓
Change/Event Pipeline
      ↓
Search Index
      ↓
Search API
```

The search index is often derived from the database rather than being the only source of truth.

______________________________________________________________________

# 42. Search Indexing

When data changes:

```text
Database
 ↓
Index update
 ↓
Search engine
```

The search index may temporarily lag behind the database.

This introduces another form of eventual consistency.

______________________________________________________________________

# 43. Search vs Database

Use the database when the primary requirement is:

```text
Transactional storage
```

Use a search engine when the primary requirement is:

```text
Rich search
Ranking
Text analysis
```

In many production systems, both are used.

______________________________________________________________________

# 44. WebSockets

WebSockets provide a persistent, bidirectional communication channel.

Conceptually:

```text
Client ←────────→ Server
       connection
```

Unlike normal request/response HTTP communication, either side can send messages after the connection is established.

______________________________________________________________________

# 45. WebSocket Use Cases

Common examples:

```text
Chat
Live notifications
Real-time dashboards
Collaborative editing
Online gaming
Live status updates
```

______________________________________________________________________

# 46. WebSocket Architecture

A simplified architecture:

```text
Client
 ↓
Load Balancer
 ↓
WebSocket Servers
 ↓
Shared State / Pub/Sub
```

When multiple WebSocket servers exist, messages may need a shared coordination mechanism.

For example:

```text
Client A → Server 1
Client B → Server 2
```

A message intended for B may require Pub/Sub or another shared messaging mechanism.

______________________________________________________________________

# 47. WebSocket Scaling

WebSocket connections are long-lived.

This means capacity planning must consider:

```text
Number of concurrent connections
Memory per connection
Connection limits
Load balancer behavior
Idle timeouts
Message throughput
```

RPS alone is insufficient for WebSocket capacity planning.

______________________________________________________________________

# 48. Long Polling

Long polling uses HTTP requests that remain open until data becomes available or a timeout occurs.

Conceptually:

```text
Client → Server
         waits...
Client ← Response
```

The client then starts another request.

______________________________________________________________________

# 49. Long Polling Use Cases

Long polling can be useful when:

```text
Real-time requirements are moderate
WebSockets are unnecessary
Infrastructure is primarily HTTP-based
```

It is generally simpler than WebSockets but can generate repeated request/connection overhead.

______________________________________________________________________

# 50. WebSockets vs Long Polling

| Feature | WebSockets | Long Polling |
|---|---|---|
| Connection | Persistent | Repeated HTTP requests |
| Direction | Bidirectional | Usually server response |
| Real-time | Excellent | Good |
| Infrastructure | More specialized | HTTP-friendly |
| Connection management | More complex | Simpler |
| Typical use | Chat/live systems | Notifications/basic updates |

Choose based on requirements rather than assuming WebSockets are always better.

______________________________________________________________________

# 51. Webhooks

A webhook allows one system to notify another system through an HTTP callback.

Example:

```text
Payment Provider
      ↓
POST /webhooks/payment
      ↓
Your API
```

This is useful when an external provider needs to notify your system about an event.

______________________________________________________________________

# 52. Webhook Design

A robust webhook endpoint should consider:

```text
Authentication/signature verification
Idempotency
Duplicate delivery
Retries
Timeouts
Fast acknowledgement
Asynchronous processing
```

A common design is:

```text
Webhook
 ↓
Validate
 ↓
Store/enqueue event
 ↓
Return 2xx
 ↓
Worker processes event
```

______________________________________________________________________

# 53. Webhook Security

Never blindly trust incoming webhook requests.

Common protections:

```text
Signature verification
HTTPS
Timestamp validation
Replay protection
Secret rotation
Rate limiting
```

The exact mechanism depends on the provider.

______________________________________________________________________

# 54. Webhook vs Polling

### Polling

Your system asks:

```text
"Has anything changed?"
```

### Webhook

The external system tells you:

```text
"Something changed."
```

Webhooks reduce unnecessary polling but require your endpoint to be reliably reachable.

______________________________________________________________________

# 55. Service Discovery

In distributed systems, services need to locate one another.

Example:

```text
Order Service
     ↓
? Payment Service
```

Service discovery maps a logical service name to available instances.

```text
payment-service
       ↓
10.0.0.4
10.0.0.5
10.0.0.6
```

______________________________________________________________________

# 56. Why Service Discovery Is Needed

Instances may change because of:

```text
Scaling
Deployments
Failures
Autoscaling
Dynamic infrastructure
```

Hard-coding:

```text
10.0.0.4
```

is fragile.

A logical service name is more resilient.

______________________________________________________________________

# 57. Client-Side vs Server-Side Discovery

### Client-side

The client discovers instances and chooses one.

```text
Service
 ↓
Registry
 ↓
Instance selection
```

### Server-side

The client calls a stable endpoint and infrastructure performs discovery/routing.

```text
Client
 ↓
Load Balancer
 ↓
Service instance
```

______________________________________________________________________

# 58. Service Registry

A registry may track:

```text
Service name
Instance address
Port
Health
Metadata
```

The exact implementation depends on the infrastructure platform.

______________________________________________________________________

# 59. Monolith

A monolith packages most application functionality into one deployable application.

Example:

```text
                Application
 ┌──────────┬──────────┬──────────┐
 │ Users    │ Orders   │ Payments │
 └──────────┴──────────┴──────────┘
```

This does not necessarily mean poorly designed code.

A monolith can have strong internal module boundaries.

______________________________________________________________________

# 60. Monolith Advantages

Benefits:

```text
Simple deployment
Simple local development
Simple debugging
Easy transactions across modules
Lower operational complexity
```

For many teams and products, a well-structured monolith is a good starting point.

______________________________________________________________________

# 61. Monolith Challenges

Potential problems:

```text
Large deployment unit
Scaling individual components is harder
Tight coupling can develop
Large codebase
Longer build/deploy cycles
```

These problems are not automatic; architecture and engineering practices matter.

______________________________________________________________________

# 62. Microservices

Microservices split an application into independently deployable services.

Example:

```text
Users
Orders
Payments
Notifications
```

Each service may own:

```text
Code
Deployment
Data
Scaling
```

The exact ownership model varies.

______________________________________________________________________

# 63. Microservices Advantages

Potential benefits:

```text
Independent deployment
Independent scaling
Team ownership
Failure isolation
Technology flexibility
```

______________________________________________________________________

# 64. Microservices Challenges

Microservices introduce distributed-system complexity:

```text
Network calls
Latency
Retries
Timeouts
Service discovery
Distributed tracing
Data consistency
Deployment coordination
Operational overhead
```

The system may be more scalable organizationally while becoming more complex technically.

______________________________________________________________________

# 65. Monolith vs Microservices

| Area | Monolith | Microservices |
|---|---|---|
| Deployment | Simpler | More complex |
| Network calls | Fewer internal calls | Many |
| Scaling | Application-level | Per-service |
| Transactions | Easier | More difficult |
| Debugging | Usually simpler | Distributed tracing needed |
| Operations | Lower overhead | Higher overhead |
| Team autonomy | Lower at large scale | Higher potential |
| Failure modes | Mostly local | Distributed |

______________________________________________________________________

# 66. Modular Monolith

A modular monolith can provide a middle ground.

```text
One deployment
      |
 ┌────┼────┬────┐
 ↓    ↓    ↓    ↓
Users Orders Payments Reports
```

The modules have explicit boundaries even though they run in one application.

This can provide:

```text
Low operational complexity
+
Strong architectural boundaries
```

______________________________________________________________________

# 67. When to Choose a Monolith

A monolith is often appropriate when:

```text
Product is early
Team is small
Domain boundaries are unclear
Operational simplicity matters
```

It can also remain appropriate at significant scale if the architecture is well designed.

______________________________________________________________________

# 68. When Microservices Make Sense

Microservices may make sense when there are strong reasons such as:

```text
Independent scaling requirements
Strong domain boundaries
Independent release cycles
Large teams requiring autonomy
Different reliability requirements
```

Do not split services only because:

> "Microservices are modern."

______________________________________________________________________

# 69. Architecture Evolution

A system may evolve:

```text
Simple application
      ↓
Modular monolith
      ↓
Extract selected services
      ↓
Distributed architecture
```

This is often safer than starting with dozens of services.

______________________________________________________________________

# 70. Choosing the Right Building Block

Use the requirement to drive the decision.

| Requirement | Potential Component |
|---|---|
| Distribute HTTP traffic | Load balancer |
| Route/proxy traffic | Reverse proxy |
| Reduce geographic latency | CDN |
| Centralize API policies | API gateway |
| Reduce repeated reads | Cache |
| Durable transactional data | Database |
| Scale reads | Read replicas |
| Async work | Message queue |
| Notify multiple consumers | Pub/Sub |
| Store large files | Object storage |
| Full-text/ranked search | Search engine |
| Bidirectional real-time communication | WebSockets |
| HTTP-based near-real-time updates | Long polling |
| External event callback | Webhook |
| Locate dynamic service instances | Service discovery |
| Simple deployment/domain | Monolith |
| Independent scaling/ownership | Microservices |

______________________________________________________________________

# 71. Layered Architecture Example

A production request path might look like:

```text
User
 ↓
CDN
 ↓
API Gateway
 ↓
Load Balancer
 ↓
Reverse Proxy
 ↓
FastAPI
 ├── Cache
 ├── Database
 ├── Search
 ├── Queue
 └── Object Storage
```

Not every layer is required.

Adding components without a clear reason increases complexity.

______________________________________________________________________

# 72. Example — E-Commerce Backend

Possible architecture:

```text
                 Client
                    ↓
                  CDN
                    ↓
              API Gateway
                    ↓
             Load Balancer
                    ↓
               FastAPI
          ┌─────────┼─────────┐
          ↓         ↓         ↓
        Redis    Database    Queue
                              ↓
                            Workers
```

Possible responsibilities:

```text
CDN
→ static assets

API Gateway
→ API policies

Load Balancer
→ traffic distribution

FastAPI
→ business logic

Redis
→ caching

Database
→ source of truth

Queue
→ asynchronous workflows

Workers
→ background processing
```

______________________________________________________________________

# 73. Example — Image Upload System

Requirement:

> Users upload large images and later view them.

Possible design:

```text
Client
 ↓
API
 ↓
Signed upload URL
 ↓
Object Storage
```

For viewing:

```text
Client
 ↓
CDN
 ↓
Object Storage
```

This prevents large files from unnecessarily passing through the application server.

______________________________________________________________________

# 74. Example — Search System

Requirement:

> Users need fast full-text product search.

Possible design:

```text
Product DB
    ↓
Indexing pipeline
    ↓
Search Engine
    ↓
Search API
    ↓
Client
```

The database remains the authoritative source while the search index is optimized for search queries.

______________________________________________________________________

# 75. Example — Real-Time Notifications

Requirement:

> Users should receive notifications immediately.

Possible architecture:

```text
Event Producer
      ↓
     Pub/Sub
      ↓
Notification Service
      ↓
WebSocket
      ↓
Client
```

If the client is not continuously connected, another delivery mechanism may be needed.

______________________________________________________________________

# 76. Example — Payment Webhook

Requirement:

> Receive payment status updates from an external provider.

Possible design:

```text
Payment Provider
       ↓
Webhook API
       ↓
Validate signature
       ↓
Store/enqueue event
       ↓
Worker
       ↓
Database
```

The endpoint should acknowledge quickly and process expensive work asynchronously.

______________________________________________________________________

# 77. Failure Analysis

For each building block, ask:

```text
What happens if it fails?
```

Examples:

### Cache fails

Can the database handle cache-miss traffic?

### Queue fails

Can requests still be accepted?

### Search fails

Can users still browse using the database?

### CDN fails

Can traffic reach origin?

### Read replica lags

Should critical reads go to primary?

### WebSocket server fails

How does the client reconnect?

### Webhook is delivered twice

Is processing idempotent?

These questions turn a component diagram into a real system design.

______________________________________________________________________

# 78. Avoiding Cascading Failures

A failure can propagate:

```text
Cache failure
 ↓
Database traffic increases
 ↓
Database slows
 ↓
API latency increases
 ↓
Requests timeout
 ↓
Clients retry
 ↓
Traffic increases further
```

This is why building blocks cannot be considered independently.

Possible protections:

```text
Timeouts
Circuit breakers
Rate limiting
Load shedding
Caching
Connection limits
Bounded concurrency
```

______________________________________________________________________

# 79. Architecture Trade-Off Matrix

| Building Block | Main Benefit | Main Cost/Risk |
|---|---|---|
| Load balancer | Horizontal distribution | Infrastructure dependency |
| Reverse proxy | Routing/proxy control | Extra layer |
| CDN | Low-latency delivery | Cache invalidation |
| API gateway | Centralized API policies | Potential bottleneck |
| Cache | Low latency | Stale data |
| Read replicas | Read scalability | Replication lag |
| Queue | Async decoupling | Eventual processing |
| Pub/Sub | Loose coupling | Eventual consistency |
| Object storage | Scalable file storage | Separate metadata/data model |
| Search | Powerful search | Index synchronization |
| WebSockets | Real-time communication | Long-lived connection complexity |
| Long polling | HTTP-compatible updates | Repeated connection overhead |
| Webhooks | Push-based integration | Delivery/retry/security complexity |
| Service discovery | Dynamic service location | Distributed infrastructure |
| Monolith | Simplicity | Coarse scaling/deployment |
| Microservices | Independent scaling/ownership | Distributed complexity |

______________________________________________________________________

# 80. Interview Questions & Answers

## Q1. What is the purpose of a load balancer?

**Answer:**

It distributes incoming traffic across multiple backend instances and can perform health checks and routing/failover
functions.

______________________________________________________________________

## Q2. What is a reverse proxy?

**Answer:**

A reverse proxy sits in front of backend servers and forwards client requests to them. It can provide routing, TLS
termination, buffering, compression, header handling and other infrastructure capabilities.

______________________________________________________________________

## Q3. What is the difference between a forward proxy and reverse proxy?

**Answer:**

A forward proxy represents clients when accessing external resources. A reverse proxy represents servers and receives
traffic on their behalf.

______________________________________________________________________

## Q4. Can a reverse proxy be a load balancer?

**Answer:**

Yes. Many reverse proxies can distribute traffic among multiple backend instances.

______________________________________________________________________

## Q5. What does a CDN do?

**Answer:**

A CDN caches and serves content from geographically distributed edge locations, reducing latency for users and reducing
traffic reaching the origin.

______________________________________________________________________

## Q6. What is the difference between a CDN and Redis?

**Answer:**

A CDN is primarily an edge delivery/cache layer close to users. Redis is typically an application-side in-memory data
store used for dynamic data, caching, counters, locks and other use cases.

______________________________________________________________________

## Q7. What is an API gateway?

**Answer:**

An API gateway provides a controlled entry point for APIs and can centralize concerns such as authentication,
authorization, routing, rate limiting, request transformation and observability.

______________________________________________________________________

## Q8. Is an API gateway mandatory for microservices?

**Answer:**

No. It is useful when its capabilities solve real requirements, but adding one introduces another component and
potential failure/bottleneck.

______________________________________________________________________

## Q9. What is cache-aside?

**Answer:**

The application first checks the cache. On a miss, it reads the source of truth, stores the result in the cache and
returns it.

______________________________________________________________________

## Q10. What happens when a cache expires for a very popular key?

**Answer:**

Many requests may simultaneously miss the cache and hit the database, causing a cache stampede. Locking, request
coalescing, TTL jitter or early refresh can mitigate it.

______________________________________________________________________

## Q11. Why use read replicas?

**Answer:**

To distribute read traffic and reduce load on the primary database when the workload is read-heavy.

______________________________________________________________________

## Q12. What is the main drawback of read replicas?

**Answer:**

Replication lag can cause stale reads. Applications must decide how to handle read-after-write consistency.

______________________________________________________________________

## Q13. Would read replicas solve a write bottleneck?

**Answer:**

Generally no. Read replicas primarily increase read capacity. A write bottleneck requires a different solution.

______________________________________________________________________

## Q14. Why use a message queue?

**Answer:**

To decouple producers and consumers, handle asynchronous work, absorb bursts and provide mechanisms for retryable
processing.

______________________________________________________________________

## Q15. Queue vs Pub/Sub?

**Answer:**

A queue commonly represents work that should be processed by a consumer. Pub/Sub represents an event that can be
consumed independently by multiple subscribers.

______________________________________________________________________

## Q16. Why is idempotency important for queue consumers?

**Answer:**

At-least-once delivery can result in duplicate messages. Idempotent processing prevents duplicate deliveries from
causing duplicate business effects.

______________________________________________________________________

## Q17. What is object storage best suited for?

**Answer:**

Large unstructured objects such as images, videos, documents, backups, reports and exports.

______________________________________________________________________

## Q18. Why might an application upload directly to object storage?

**Answer:**

Large files do not need to consume application-server bandwidth and connections. A signed URL can allow the client to
upload directly to storage.

______________________________________________________________________

## Q19. Why use a search engine if you already have PostgreSQL?

**Answer:**

A relational database may handle basic search, but a specialized search engine can provide more sophisticated full-text
search, ranking, fuzzy matching and search-oriented indexing at appropriate scale.

______________________________________________________________________

## Q20. Should the search engine be the source of truth?

**Answer:**

Usually the transactional database remains the authoritative source and the search index is derived from it, although
architecture varies by system.

______________________________________________________________________

## Q21. What are WebSockets?

**Answer:**

WebSockets provide a persistent, bidirectional communication channel between a client and server, making them useful for
real-time applications.

______________________________________________________________________

## Q22. Why are WebSockets harder to scale than ordinary HTTP requests?

**Answer:**

Connections remain open for long periods, so capacity depends on concurrent connections, memory, connection limits,
load-balancer behavior and message throughput in addition to ordinary request traffic.

______________________________________________________________________

## Q23. When would you use long polling instead of WebSockets?

**Answer:**

When near-real-time updates are needed but full bidirectional persistent connections are unnecessary or the
infrastructure is strongly HTTP-oriented.

______________________________________________________________________

## Q24. What is a webhook?

**Answer:**

A webhook is an HTTP callback where one system sends an event notification to another system's endpoint.

______________________________________________________________________

## Q25. How should webhook endpoints handle duplicate events?

**Answer:**

Use idempotency or event deduplication, typically by storing a unique event identifier or idempotency key before
applying the business effect.

______________________________________________________________________

## Q26. Why should webhook processing often be asynchronous?

**Answer:**

External providers usually need a timely HTTP response. Validating and enqueueing the event quickly allows the endpoint
to acknowledge it while a worker performs expensive processing.

______________________________________________________________________

## Q27. What is service discovery?

**Answer:**

Service discovery allows services to locate currently available instances of another service without relying on
hard-coded addresses.

______________________________________________________________________

## Q28. Why is hard-coding service IP addresses problematic?

**Answer:**

Instances can change because of scaling, deployment and failures. Dynamic discovery or stable service endpoints allow
infrastructure to change without requiring application code changes.

______________________________________________________________________

## Q29. What are the advantages of a monolith?

**Answer:**

Simpler deployment, local development, debugging, transactions and lower operational overhead.

______________________________________________________________________

## Q30. What are the advantages of microservices?

**Answer:**

Independent deployment and scaling, clearer service ownership and potentially better isolation between domains or teams.

______________________________________________________________________

## Q31. What is the biggest cost of microservices?

**Answer:**

Distributed-system complexity: network failures, latency, retries, timeouts, service discovery, observability, data
consistency and operational overhead.

______________________________________________________________________

## Q32. Is a monolith always bad at scale?

**Answer:**

No. A well-structured modular monolith can scale significantly. Architecture quality matters more than simply whether
the deployment is one process or multiple services.

______________________________________________________________________

## Q33. What is a modular monolith?

**Answer:**

A single deployable application with strong internal module boundaries and explicit separation of responsibilities.

______________________________________________________________________

## Q34. When would you split a monolith into microservices?

**Answer:**

When there is a concrete reason such as independent scaling, strong domain boundaries, independent release requirements
or organizational/team needs.

______________________________________________________________________

## Q35. Why shouldn't you introduce every building block into every system?

**Answer:**

Each component adds operational complexity, failure modes and maintenance cost. Architecture should be driven by
requirements and bottlenecks.

______________________________________________________________________

## Q36. What happens if a cache fails?

**Answer:**

If the cache is non-authoritative, the application may fall back to the source of truth. However, the resulting
cache-miss storm must be considered because it can overload the database.

______________________________________________________________________

## Q37. What happens if a read replica is stale?

**Answer:**

The application may return outdated data. Critical read-after-write operations may need to use the primary or another
consistency-aware strategy.

______________________________________________________________________

## Q38. What happens if a queue is unavailable?

**Answer:**

The system needs an explicit policy. It might reject asynchronous requests, temporarily buffer work elsewhere or degrade
functionality. Silently accepting work that cannot be safely queued can cause data loss.

______________________________________________________________________

## Q39. How would you design real-time messaging at scale?

**Answer:**

A typical design might use WebSocket servers for connections, Pub/Sub or a message broker for cross-instance message
distribution, shared durable storage where required and appropriate load-balancer support for long-lived connections.

______________________________________________________________________

## Q40. What is the key principle when choosing an architecture component?

**Answer:**

Start with the requirement and bottleneck, then choose the simplest component that solves the problem while
understanding its failure modes and operational trade-offs.

______________________________________________________________________

# 81. Practical Architecture Exercises

## Exercise 1 — High-Traffic Read API

Requirement:

> Build an API that serves frequently accessed product information.

Consider:

```text
CDN
Load Balancer
FastAPI
Redis
Database
Read replicas
```

Questions:

- Which data should be cached?
- What happens on cache miss?
- What happens when Redis fails?
- Can replicas serve all reads?
- How do you handle product updates?

______________________________________________________________________

## Exercise 2 — Large File Upload

Requirement:

> Users upload 500 MB videos.

Design:

```text
Client
→ API
→ Signed URL
→ Object Storage
```

Questions:

- Why avoid routing the entire file through FastAPI?
- How do you authenticate uploads?
- How do you track upload status?
- How do you process the video asynchronously?
- Where does the CDN fit?

______________________________________________________________________

## Exercise 3 — Product Search

Requirement:

> Search millions of products by name, category and free-text query.

Consider:

```text
Database
Search Index
API
Cache
```

Questions:

- Which system is the source of truth?
- How is the search index updated?
- What happens if indexing is delayed?
- Should search results be cached?

______________________________________________________________________

## Exercise 4 — Real-Time Chat

Requirement:

> Users need real-time one-to-one messaging.

Consider:

```text
Load Balancer
WebSocket Servers
Pub/Sub
Database
```

Questions:

- How are connections distributed?
- How does Server 1 send a message to a user connected to Server 2?
- How are offline messages stored?
- What happens when a WebSocket disconnects?
- How do you prevent duplicate message processing?

______________________________________________________________________

## Exercise 5 — Payment Webhook

Requirement:

> Receive payment status events from a payment provider.

Consider:

```text
Webhook API
Signature Verification
Queue
Worker
Database
```

Questions:

- How do you verify authenticity?
- How do you handle duplicate events?
- Why enqueue instead of performing everything synchronously?
- What happens if the worker fails?
- How do you safely retry?

______________________________________________________________________

# 82. Architecture Review Checklist

When reviewing a backend design, ask:

### Traffic

- [ ] How does traffic enter the system?
- [ ] Is load balancing needed?
- [ ] Are there geographic users?
- [ ] Would a CDN help?

### API

- [ ] Is there a clear API boundary?
- [ ] Is an API gateway justified?
- [ ] Are rate limiting and authentication handled?

### Data

- [ ] What is the source of truth?
- [ ] Does caching help?
- [ ] Are read replicas useful?
- [ ] What consistency is required?

### Asynchronous Processing

- [ ] Is a queue needed?
- [ ] Is Pub/Sub useful?
- [ ] Are consumers idempotent?
- [ ] How are retries handled?

### Files/Search

- [ ] Should large objects use object storage?
- [ ] Does search require a specialized index?

### Real Time

- [ ] Are WebSockets actually required?
- [ ] Would long polling be sufficient?
- [ ] Does the system need webhooks?

### Distributed Architecture

- [ ] Is service discovery needed?
- [ ] Is microservices complexity justified?
- [ ] Could a modular monolith be sufficient?

### Reliability

- [ ] What happens if each dependency fails?
- [ ] Are timeouts configured?
- [ ] Are retries bounded?
- [ ] Can failures cascade?

______________________________________________________________________

# 83. Final Interview Readiness Checklist

Before moving to File 40, make sure you can:

- [ ] Explain a load balancer.
- [ ] Explain load-balancing strategies.
- [ ] Explain health checks.
- [ ] Distinguish liveness and readiness.
- [ ] Explain a reverse proxy.
- [ ] Distinguish forward and reverse proxies.
- [ ] Explain reverse proxy vs load balancer.
- [ ] Explain a CDN.
- [ ] Explain CDN caching and invalidation.
- [ ] Explain CDN vs application cache.
- [ ] Explain an API gateway.
- [ ] Explain API gateway trade-offs.
- [ ] Explain cache-aside.
- [ ] Explain cache invalidation.
- [ ] Explain cache stampede.
- [ ] Explain databases as sources of truth.
- [ ] Explain primary/replica architecture.
- [ ] Explain read replicas.
- [ ] Explain replication lag.
- [ ] Explain read-after-write problems.
- [ ] Explain message queues.
- [ ] Explain queue delivery concerns.
- [ ] Explain consumer idempotency.
- [ ] Explain Pub/Sub.
- [ ] Explain queue vs Pub/Sub.
- [ ] Explain event-driven architecture.
- [ ] Explain eventual consistency.
- [ ] Explain object storage.
- [ ] Explain direct-to-object-storage uploads.
- [ ] Explain search engines.
- [ ] Explain database vs search index.
- [ ] Explain WebSockets.
- [ ] Explain WebSocket scaling.
- [ ] Explain long polling.
- [ ] Compare WebSockets and long polling.
- [ ] Explain webhooks.
- [ ] Explain webhook security.
- [ ] Explain webhook idempotency.
- [ ] Explain service discovery.
- [ ] Explain client-side vs server-side discovery.
- [ ] Compare monolith and microservices.
- [ ] Explain modular monoliths.
- [ ] Explain when microservices are justified.
- [ ] Identify unnecessary architecture complexity.
- [ ] Analyze component failure modes.
- [ ] Identify cascading failures.
- [ ] Explain architecture trade-offs.
- [ ] Design a basic production backend architecture.

______________________________________________________________________

# 84. Final Takeaways

Backend architecture is built from reusable building blocks.

The important skill is not memorizing technology names.

It is recognizing the problem:

```text
Need traffic distribution
→ Load balancer

Need proxy/routing
→ Reverse proxy

Need edge delivery
→ CDN

Need centralized API policies
→ API gateway

Need faster repeated reads
→ Cache

Need durable transactional state
→ Database

Need more read capacity
→ Read replicas

Need asynchronous work
→ Queue

Need multiple independent consumers
→ Pub/Sub

Need large-file storage
→ Object storage

Need sophisticated search
→ Search engine

Need bidirectional real-time communication
→ WebSockets

Need HTTP-based near-real-time updates
→ Long polling

Need external event callbacks
→ Webhooks

Need dynamic service locations
→ Service discovery

Need simple deployment
→ Monolith/modular monolith

Need independent service scaling or ownership
→ Microservices
```

The senior-level question is always:

> **What requirement justifies this component, and what new failure mode or complexity does it introduce?**

A good architecture is not the one with the most boxes.

It is the simplest architecture that satisfies the requirements while remaining scalable, observable, reliable and
maintainable.

______________________________________________________________________

**Previous:** [38. System Design Fundamentals](./38-system-design-fundamentals.md)

**Next:** [40. Practical System Design](./40-system-design-practice.md)
