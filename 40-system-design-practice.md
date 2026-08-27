# 40. Practical System Design

**Previous:** [39. Backend Architecture Building Blocks](./39-system-design-building-blocks.md)

**Next:** [41. TypeScript, Angular Overview](./41-typescript-angular.md)

______________________________________________________________________

## Objective

This topic turns the system-design fundamentals from Files 38 and 39 into practical interview designs.

By the end of this file, you should be able to:

- Start a system-design problem by clarifying requirements.
- Define useful APIs and data models.
- Build a high-level architecture.
- Identify bottlenecks before they become failures.
- Explain how the design scales.
- Reason about reliability and failure handling.
- Discuss consistency, idempotency and trade-offs.
- Explain your architecture clearly in an interview.
- Recognize reusable patterns across different backend systems.

The five practical designs are:

1. URL Shortener
1. Notification Service
1. File Upload Service
1. Rate Limiter
1. Chat Service

______________________________________________________________________

# 1. How to Approach Practical System Design

For every design, follow the same sequence:

```text
Requirements
→ APIs
→ Data model
→ High-level architecture
→ Data flow
→ Scaling
→ Bottlenecks
→ Failure handling
→ Trade-offs
→ Interview Q&A
```

Do not begin by naming technologies.

Start with the problem.

______________________________________________________________________

# 2. Design 1 — URL Shortener

## 2.1 Problem

Design a service that converts a long URL into a short URL.

Example:

```text
Long:
https://example.com/products/category/item?id=12345

Short:
https://short.example/Ab3xK
```

When a user opens the short URL, the service redirects them to the original URL.

______________________________________________________________________

## 2.2 Requirements

### Functional Requirements

The system should:

- Create a short URL.
- Redirect a short URL to its original URL.
- Store the URL mapping.
- Optionally track basic usage.

### Non-Functional Requirements

Assume:

- High read volume.
- Low redirect latency.
- High availability.
- Short codes should be unique.
- Redirects should scale horizontally.

______________________________________________________________________

## 2.3 Clarifying Questions

In an interview, ask:

- Are URLs permanent or do they expire?
- Can users choose custom aliases?
- Is authentication required to create URLs?
- Do we need analytics?
- What is the expected read/write ratio?
- How long should mappings be retained?
- Can the same long URL produce multiple short URLs?

These answers affect the design.

______________________________________________________________________

# 3. URL Shortener APIs

## Create URL

```http
POST /urls
Content-Type: application/json

{
  "url": "https://example.com/very/long/path"
}
```

Response:

```http
201 Created

{
  "short_code": "Ab3xK",
  "short_url": "https://short.example/Ab3xK"
}
```

## Redirect

```http
GET /{short_code}
```

Response:

```http
302 Found
Location: https://example.com/very/long/path
```

The exact redirect status can depend on application requirements.

______________________________________________________________________

# 4. URL Shortener Data Model

A simple relational model:

```text
urls
--------------------------------
id
short_code
original_url
created_at
expires_at
user_id
```

Useful indexes:

```text
PRIMARY KEY(id)
UNIQUE(short_code)
INDEX(user_id)
```

The critical lookup is:

```text
short_code → original_url
```

______________________________________________________________________

# 5. URL Shortener Code Generation

A short code can be generated using:

```text
Auto-increment ID
→ Base62 encoding
```

Base62 uses:

```text
a-z
A-Z
0-9
```

Another approach is a random identifier.

The important requirement is uniqueness.

______________________________________________________________________

# 6. Base62 Concept

Suppose an integer ID is:

```text
125
```

Convert it to a representation using 62 possible characters.

This produces a compact string.

Benefits:

- Compact
- Deterministic
- Easy to generate

Potential concerns:

- Predictability
- Enumeration
- Information leakage

If predictability matters, use a different ID strategy.

______________________________________________________________________

# 7. URL Shortener Architecture

```text
Client
  ↓
Load Balancer
  ↓
URL Service
  ├──→ Redis
  └──→ Database
```

Creation:

```text
Client
 ↓
URL Service
 ↓
Database
 ↓
Return short code
```

Redirect:

```text
Client
 ↓
URL Service
 ↓
Redis
 ↓ miss
Database
 ↓
Redirect
```

______________________________________________________________________

# 8. Why Cache Redirects?

Redirect traffic is often much higher than URL creation traffic.

Caching:

```text
short_code → original_url
```

reduces database reads.

This improves:

```text
Latency
Database capacity
Throughput
```

______________________________________________________________________

# 9. URL Shortener Scaling

The application should be stateless:

```text
          Load Balancer
          /     |     \
        App1   App2   App3
```

Shared state lives in:

```text
Redis
Database
```

The database can later use:

```text
Read replicas
Partitioning
```

if scale requires them.

______________________________________________________________________

# 10. URL Shortener Bottlenecks

Potential bottlenecks:

```text
Database reads
Database writes
Cache capacity
Short-code generation
Hot URLs
Network latency
```

A very popular URL can become a hot key.

______________________________________________________________________

# 11. URL Shortener Failure Handling

### Redis fails

Fallback to the database if it can handle the load.

### Database fails

Existing cached redirects may continue working, but creation of new URLs may fail.

### Application instance fails

Load balancer routes traffic to another instance.

### Duplicate short code

Use a unique constraint and retry generation when necessary.

______________________________________________________________________

# 12. URL Shortener Trade-Offs

| Decision | Trade-off |
|---|---|
| Redis cache | Faster reads but cache invalidation |
| Random code | Harder to predict but collision handling needed |
| Sequential ID | Simple but predictable |
| SQL database | Strong transactional guarantees |
| No expiration | Simple but storage grows indefinitely |
| Analytics | More functionality but additional storage/work |

______________________________________________________________________

# 13. URL Shortener Interview Q&A

## Q1. What is the most important lookup?

**Answer:**

`short_code → original_url`.

The system should optimize this path because redirects are usually read-heavy.

## Q2. Why use Redis?

**Answer:**

To cache frequently accessed URL mappings and reduce database latency/load.

## Q3. How do you guarantee unique short codes?

**Answer:**

Use a unique database constraint and a collision-safe generation strategy.

## Q4. What happens if Redis fails?

**Answer:**

If Redis is only a cache, fall back to the database, provided the database can handle the additional traffic.

## Q5. Would you use a relational database?

**Answer:**

A relational database is a reasonable default because the mapping is simple and uniqueness/transactional guarantees are
useful. The final choice depends on scale and requirements.

______________________________________________________________________

# 14. Design 2 — Notification Service

## 14.1 Problem

Design a service that sends notifications through channels such as:

```text
Email
SMS
Push notification
```

Example:

```text
Order Service
      ↓
Notification Service
      ↓
 ┌────┼────┐
 ↓    ↓    ↓
Email SMS Push
```

______________________________________________________________________

# 15. Notification Requirements

### Functional

- Accept notification requests.
- Select a notification channel.
- Deliver notifications.
- Retry transient failures.
- Track notification status.

### Non-Functional

- Reliable delivery.
- Scalable processing.
- No duplicate business notifications where avoidable.
- Ability to handle traffic bursts.

______________________________________________________________________

# 16. Notification APIs

## Create Notification

```http
POST /notifications
```

Example:

```json
{
  "user_id": "123",
  "type": "ORDER_CONFIRMED",
  "channel": "email",
  "template_id": "order-confirmed",
  "data": {
    "order_id": "ORD-123"
  }
}
```

Response:

```http
202 Accepted

{
  "notification_id": "N-123"
}
```

Asynchronous processing is appropriate because external providers may be slow.

______________________________________________________________________

# 17. Notification Data Model

```text
notifications
--------------------------------
id
user_id
type
channel
template_id
status
provider_message_id
attempt_count
created_at
updated_at
```

Possible statuses:

```text
PENDING
PROCESSING
SENT
FAILED
```

______________________________________________________________________

# 18. Notification Architecture

```text
Producer
   ↓
Notification API
   ↓
Queue
   ↓
Workers
   ├──→ Email Provider
   ├──→ SMS Provider
   └──→ Push Provider
```

Database:

```text
Notification API
       ↓
   Database
```

Workers update delivery status.

______________________________________________________________________

# 19. Why Use a Queue?

Notification delivery is a classic asynchronous workload.

Without a queue:

```text
API
 ↓
Email provider
 ↓
Wait
 ↓
Response
```

With a queue:

```text
API
 ↓
Queue
 ↓
Worker
 ↓
Provider
```

The API can acknowledge the request quickly.

______________________________________________________________________

# 20. Notification Retry

External providers can fail transiently.

Use:

```text
Timeout
Retry
Exponential backoff
Jitter
Retry limit
```

Do not retry permanent failures indefinitely.

______________________________________________________________________

# 21. Duplicate Notifications

Suppose:

```text
Worker sends email
 ↓
Provider succeeds
 ↓
Worker crashes before marking SENT
 ↓
Message is retried
```

The notification may be sent twice.

Possible protections:

```text
Idempotency
Provider idempotency support
Deduplication
Persistent delivery state
```

Exactly-once external side effects are difficult, so design explicitly for duplicate handling.

______________________________________________________________________

# 22. Notification Scaling

Workers can scale horizontally:

```text
Queue
 ├── Worker 1
 ├── Worker 2
 ├── Worker 3
 └── Worker N
```

Scale based on:

```text
Queue depth
Processing latency
Provider limits
Worker utilization
```

______________________________________________________________________

# 23. Provider Rate Limits

External providers may impose limits:

```text
1000 messages/minute
```

If workers process faster than the provider allows, use:

```text
Concurrency limits
Rate limiting
Queues
Backoff
```

______________________________________________________________________

# 24. Notification Failure Handling

### Queue unavailable

Do not claim successful asynchronous acceptance unless the message is durably accepted.

### Provider unavailable

Retry suitable transient failures.

### Worker crashes

The message should be recoverable/re-delivered according to the queue's delivery semantics.

### Provider permanently rejects

Mark the notification failed and avoid endless retries.

______________________________________________________________________

# 25. Notification Trade-Offs

| Decision | Trade-off |
|---|---|
| Queue | Reliability/decoupling but async complexity |
| Multiple providers | Better resilience but more integration work |
| Retry | Recovers transient failures but can amplify load |
| Provider idempotency | Safer retries but depends on provider support |
| Persistent status | Better visibility but more writes |

______________________________________________________________________

# 26. Notification Interview Q&A

## Q1. Why should notification delivery be asynchronous?

**Answer:**

External providers can be slow or temporarily unavailable. A queue allows the API to respond quickly and lets workers
handle retries and delivery independently.

## Q2. How do you avoid duplicate notifications?

**Answer:**

Use an idempotency/deduplication strategy and provider-side idempotency where supported. The worker must tolerate
redelivery.

## Q3. What metric is important?

**Answer:**

Queue depth/lag, delivery latency, success rate, failure rate, retry count and provider error rate.

## Q4. How do you handle provider rate limits?

**Answer:**

Bound worker concurrency, rate-limit outbound requests and use retry/backoff when appropriate.

______________________________________________________________________

# 27. Design 3 — File Upload Service

## 27.1 Problem

Design a backend that allows users to upload large files.

Requirements:

- Upload large files.
- Track upload status.
- Store files durably.
- Allow users to download files.
- Process files asynchronously when required.

______________________________________________________________________

# 28. File Upload Requirements

Clarify:

- Maximum file size?
- Supported file types?
- Private or public files?
- Virus scanning required?
- Processing required?
- Retention period?
- Download traffic?
- Resumable uploads required?

These questions determine the architecture.

______________________________________________________________________

# 29. File Upload API

A common pattern is to request an upload URL.

```http
POST /files
```

Response:

```json
{
  "file_id": "F123",
  "upload_url": "..."
}
```

Then:

```text
Client
 ↓
Object Storage
```

The application does not need to stream the entire file through itself.

______________________________________________________________________

# 30. File Data Model

```text
files
--------------------------------
id
user_id
object_key
filename
content_type
size
status
created_at
updated_at
```

Possible statuses:

```text
UPLOADING
UPLOADED
PROCESSING
READY
FAILED
```

______________________________________________________________________

# 31. File Upload Architecture

```text
Client
   ↓
FastAPI
   ↓
Signed Upload URL
   ↓
Object Storage
   ↓
Event / Queue
   ↓
Worker
   ↓
Processing
```

Metadata is stored in the database.

______________________________________________________________________

# 32. Why Object Storage?

Large files can consume:

```text
Application bandwidth
Application connections
Memory
Disk
```

Object storage is designed for large objects and can scale independently from the application.

______________________________________________________________________

# 33. Signed URLs

The application can issue a temporary signed URL.

Conceptually:

```text
Client
 ↓
API
 ↓
Signed URL
 ↓
Object Storage
```

Benefits:

- Limited lifetime
- Controlled access
- Direct transfer
- Reduced application load

______________________________________________________________________

# 34. File Download

A similar pattern can be used for downloads:

```text
Client
 ↓
API
 ↓
Signed Download URL
 ↓
Object Storage/CDN
```

For frequently accessed public content, a CDN can reduce origin traffic.

______________________________________________________________________

# 35. File Processing

Suppose uploaded images need processing.

```text
Object Storage
      ↓
Queue
      ↓
Worker
      ↓
Processed Object
```

Examples:

```text
Thumbnail generation
Virus scanning
Metadata extraction
Video transcoding
Document processing
```

______________________________________________________________________

# 36. File Upload Security

Validate:

```text
Authentication
Authorization
File size
Content type
File signature/magic bytes
Filename
Object key
```

Also consider:

```text
Virus/malware scanning
Path traversal prevention
Unsafe file execution
Signed URLs
Expiration
```

Never assume a user-provided filename or content type is trustworthy.

______________________________________________________________________

# 37. File Upload Scaling

The application primarily handles:

```text
Metadata
Authentication
Signed URL generation
Status queries
```

Object storage handles:

```text
Large file transfer
Storage
Downloads
```

Workers handle:

```text
Processing
```

This separates scaling responsibilities.

______________________________________________________________________

# 38. File Upload Failure Handling

### Upload interrupted

Use resumable/multipart upload when requirements justify it.

### Worker crashes

Queue semantics should allow retry/reprocessing.

### Processing fails

Mark file status as failed and retain useful error information.

### Object storage unavailable

Do not report the file as successfully stored unless storage confirmed it.

______________________________________________________________________

# 39. File Upload Trade-Offs

| Decision | Trade-off |
|---|---|
| Direct object upload | Lower API load but more client/storage coordination |
| Signed URLs | Secure temporary access but URL management |
| CDN | Faster downloads but caching complexity |
| Async processing | Fast upload completion but eventual processing |
| Multipart upload | Better large-file resilience but more complexity |

______________________________________________________________________

# 40. File Upload Interview Q&A

## Q1. Why not upload the file through FastAPI?

**Answer:**

For large files, direct object-storage uploads reduce application bandwidth, connection usage and resource consumption.

## Q2. How do you secure uploads?

**Answer:**

Authenticate the user, authorize the target object, use short-lived signed URLs, validate file properties and
scan/process files where required.

## Q3. Where should metadata live?

**Answer:**

Usually in the database, while the actual large object is stored in object storage.

## Q4. How do you process uploaded files?

**Answer:**

Emit an event or enqueue a job after successful upload and process it asynchronously with workers.

______________________________________________________________________

# 41. Design 4 — Rate Limiter

## 41.1 Problem

Design a service that limits requests by a key such as:

```text
User
API key
IP address
Tenant
```

Example:

```text
100 requests/minute/user
```

______________________________________________________________________

# 42. Rate Limiter Requirements

The system should:

- Enforce a request limit.
- Work across multiple application instances.
- Respond with low latency.
- Support configurable limits.
- Return a clear response when the limit is exceeded.

______________________________________________________________________

# 43. Rate Limiter API Behavior

The limiter may be internal middleware rather than a public API.

Conceptually:

```python
allowed = rate_limiter.allow(key)
```

If allowed:

```text
Continue request
```

Otherwise:

```http
429 Too Many Requests
```

______________________________________________________________________

# 44. Rate Limiter Architecture

```text
Client
 ↓
Load Balancer
 ↓
API Instances
 ↓
Rate Limiter
 ↓
Redis
```

Redis is useful because rate-limit state must be shared across application instances.

______________________________________________________________________

# 45. Fixed Window

Example:

```text
100 requests
per one-minute window
```

State:

```text
user:123:10:00 → 87
```

At the next window:

```text
counter resets
```

Simple but has boundary effects.

______________________________________________________________________

# 46. Sliding Window

A sliding-window approach considers requests over the recent interval.

It gives more accurate enforcement but can require more state and processing.

______________________________________________________________________

# 47. Token Bucket

Imagine a bucket containing tokens.

```text
Tokens
 ↓
Request consumes 1 token
```

Tokens are replenished at a fixed rate.

Example:

```text
Capacity = 100
Refill = 10 tokens/sec
```

This allows controlled bursts while enforcing a long-term rate.

______________________________________________________________________

# 48. Rate Limiter Atomicity

Multiple application instances may update the same counter concurrently.

A naive flow:

```text
GET counter
check
INCR
```

can have race conditions.

Use an atomic Redis operation or Lua script when the algorithm requires multiple operations to be executed atomically.

______________________________________________________________________

# 49. Rate Limiter Scaling

Consider:

```text
10,000 API requests/sec
```

The limiter itself must handle high throughput.

Potential strategies:

```text
Efficient Redis operations
Local limiting where acceptable
Distributed shared state
Partitioning by key
```

The correct design depends on how strict global enforcement must be.

______________________________________________________________________

# 50. Rate Limiter Failure Handling

A major design question:

> What happens if Redis is unavailable?

Possible policies:

### Fail open

Allow requests.

Pros:

```text
Availability
```

Cons:

```text
Abuse protection may disappear
```

### Fail closed

Reject requests.

Pros:

```text
Protection
```

Cons:

```text
Availability suffers
```

The right answer depends on the endpoint and security requirements.

______________________________________________________________________

# 51. Rate Limiter Trade-Offs

| Decision | Trade-off |
|---|---|
| Fixed window | Simple but boundary bursts |
| Sliding window | More accurate but more state |
| Token bucket | Good burst control but more algorithmic complexity |
| Redis | Shared state but dependency |
| Fail open | Availability but weaker protection |
| Fail closed | Protection but availability impact |

______________________________________________________________________

# 52. Rate Limiter Interview Q&A

## Q1. Why use Redis?

**Answer:**

Multiple application instances need shared rate-limit state. Redis provides low-latency shared storage and atomic
operations useful for counters.

## Q2. Why can a local in-memory limiter be incorrect?

**Answer:**

Each application instance would maintain a separate counter, so a client could exceed the intended global limit by
distributing requests across instances.

## Q3. What status code should an API return?

**Answer:**

Typically `429 Too Many Requests`.

## Q4. What happens if Redis fails?

**Answer:**

Choose fail-open or fail-closed based on the endpoint's risk. There is no universal answer.

______________________________________________________________________

# 53. Design 5 — Chat Service

## 53.1 Problem

Design a one-to-one chat system.

Users should be able to:

- Send messages.
- Receive messages in real time.
- View message history.
- Receive messages after reconnecting.
- Handle multiple concurrent users.

______________________________________________________________________

# 54. Chat Requirements

Clarify:

- One-to-one or group chat?
- Maximum group size?
- Message ordering requirement?
- Delivery guarantee?
- Read receipts?
- Typing indicators?
- Offline message support?
- Message retention?
- Attachments?
- End-to-end encryption?

These questions materially change the architecture.

______________________________________________________________________

# 55. Chat APIs

## Send Message

A REST endpoint could be:

```http
POST /conversations/{conversation_id}/messages
```

Example:

```json
{
  "client_message_id": "c123",
  "text": "Hello"
}
```

## Message History

```http
GET /conversations/{conversation_id}/messages?cursor=...
```

## Real-Time Connection

```text
WebSocket
```

______________________________________________________________________

# 56. Chat Data Model

Possible relational model:

```text
users
----------------
id
name

conversations
----------------
id
created_at

conversation_members
----------------
conversation_id
user_id

messages
----------------
id
conversation_id
sender_id
client_message_id
sequence_number
content
created_at
```

Useful constraints:

```text
UNIQUE(conversation_id, client_message_id)
```

can help deduplicate client retries.

______________________________________________________________________

# 57. Chat Architecture

```text
Client
   ↓
Load Balancer
   ↓
WebSocket Servers
   ↓
Pub/Sub
   ↓
Message Service
   ↓
Database
```

The exact ordering of these components can vary by implementation.

______________________________________________________________________

# 58. Why WebSockets?

Chat needs:

```text
Server → Client
```

messages without requiring the client to continuously poll.

WebSockets provide a persistent bidirectional channel.

______________________________________________________________________

# 59. Cross-Server Messaging

Suppose:

```text
User A → WebSocket Server 1
User B → WebSocket Server 2
```

A message from A to B must reach Server 2.

Use shared messaging:

```text
Server 1
   ↓
Pub/Sub
   ↓
Server 2
   ↓
User B
```

______________________________________________________________________

# 60. Message Persistence

Do not rely only on WebSocket delivery.

Persist messages when history/offline delivery is required:

```text
Client
 ↓
Chat Service
 ↓
Database
```

The database becomes the durable source for message history.

______________________________________________________________________

# 61. Message Ordering

Ordering requirements should be clarified.

A simple strategy is a conversation-level sequence:

```text
Conversation 42

1001
1002
1003
1004
```

Consumers can use the sequence to identify ordering.

Global ordering across all conversations is usually unnecessary and expensive.

______________________________________________________________________

# 62. Duplicate Messages

A client may send:

```text
Message M
```

The server processes it, but the response is lost.

Client retries:

```text
Message M again
```

Use:

```text
client_message_id
```

with a uniqueness constraint to make processing idempotent.

______________________________________________________________________

# 63. Offline Users

If the recipient is disconnected:

```text
Message
 ↓
Database
```

When the user reconnects:

```text
Client
 ↓
Sync messages after last known sequence
```

This is more reliable than assuming the WebSocket was always available.

______________________________________________________________________

# 64. Chat Pagination

Do not return the entire conversation history.

Use cursor-based pagination:

```http
GET /conversations/42/messages?before=cursor
```

Cursor pagination is generally more stable than large offset pagination for frequently changing message streams.

______________________________________________________________________

# 65. Chat Scaling

WebSocket capacity depends heavily on:

```text
Concurrent connections
Messages/sec
Memory
Connection limits
```

Scale WebSocket servers horizontally.

Use shared infrastructure for:

```text
Message distribution
Durable message storage
Presence where required
```

______________________________________________________________________

# 66. Chat Failure Handling

### WebSocket server crashes

Client reconnects.

### Pub/Sub unavailable

Real-time delivery may fail, but persisted messages can support later synchronization if the write path remains
available.

### Database unavailable

Message persistence may fail. Decide whether the system can safely acknowledge messages without durable storage.

### Duplicate client message

Use idempotency/client message IDs.

______________________________________________________________________

# 67. Chat Trade-Offs

| Decision | Trade-off |
|---|---|
| WebSockets | Excellent real-time behavior but connection complexity |
| Pub/Sub | Cross-server delivery but distributed messaging dependency |
| SQL database | Durable history but write/storage scaling considerations |
| Cursor pagination | Stable large-history traversal but more complex API |
| Message IDs | Idempotency but extra state/constraints |
| Sequence numbers | Ordering visibility but additional coordination |

______________________________________________________________________

# 68. Chat Interview Q&A

## Q1. Why use WebSockets?

**Answer:**

Chat requires low-latency server-to-client communication. WebSockets provide a persistent bidirectional channel.

## Q2. Why is Pub/Sub needed?

**Answer:**

Users can be connected to different WebSocket servers. Pub/Sub allows an event received by one server to reach the
server hosting the recipient.

## Q3. How do you support offline users?

**Answer:**

Persist messages durably and synchronize messages missed since the client's last acknowledged sequence when the user
reconnects.

## Q4. How do you prevent duplicate messages?

**Answer:**

Give each client message a unique client-generated ID and enforce idempotent processing, for example with a uniqueness
constraint.

## Q5. How do you scale WebSockets?

**Answer:**

Horizontally scale connection servers and use shared messaging/state where required. Capacity planning should focus on
concurrent connections as well as message throughput.

______________________________________________________________________

# 69. Cross-Design Patterns

The five systems look different, but many architectural patterns repeat.

| Pattern | URL Shortener | Notification | File Upload | Rate Limiter | Chat |
|---|---:|---:|---:|---:|---:|
| Load balancing | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cache | ✓ | Optional | Optional | ✓ | Optional |
| Database | ✓ | ✓ | ✓ | Optional | ✓ |
| Queue | Optional | ✓ | ✓ | No | Optional |
| Pub/Sub | No | Optional | Optional | No | ✓ |
| Object storage | No | No | ✓ | No | Optional |
| WebSockets | No | Optional | No | No | ✓ |
| Idempotency | ✓ | ✓ | ✓ | ✓ | ✓ |
| Retry | Optional | ✓ | ✓ | Optional | ✓ |
| Rate limiting | Optional | ✓ | ✓ | Core | ✓ |
| Observability | ✓ | ✓ | ✓ | ✓ | ✓ |

The goal is to recognize these reusable patterns.

______________________________________________________________________

# 70. Common System Design Patterns

## Cache

Use when:

```text
Reads are frequent
Data is reusable
Low latency matters
```

______________________________________________________________________

## Queue

Use when:

```text
Work is asynchronous
Processing is slow
Traffic is bursty
Retries are useful
```

______________________________________________________________________

## Pub/Sub

Use when:

```text
One event has multiple independent consumers
```

______________________________________________________________________

## Object Storage

Use when:

```text
Large files/blobs need durable storage
```

______________________________________________________________________

## WebSockets

Use when:

```text
Low-latency bidirectional communication is required
```

______________________________________________________________________

## Read Replicas

Use when:

```text
Read workload dominates
```

______________________________________________________________________

## Idempotency

Use when:

```text
Retries or duplicate delivery can produce duplicate side effects
```

______________________________________________________________________

# 71. Failure-First Design

For every system, ask:

```text
What if the application crashes?
What if the cache fails?
What if the database is slow?
What if the queue is unavailable?
What if the network times out?
What if the client retries?
What if the dependency succeeds but our response is lost?
```

The last question is especially important.

Distributed systems often fail between:

```text
Side effect
```

and:

```text
Acknowledgement
```

That is why idempotency is so important.

______________________________________________________________________

# 72. Bottleneck-First Thinking

Do not automatically scale every component.

Find the limiting resource.

Examples:

### URL Shortener

```text
Database read capacity
```

may be the bottleneck.

### Notification Service

```text
External provider throughput
```

may be the bottleneck.

### File Upload

```text
Application bandwidth
```

may be the bottleneck if files pass through the API.

### Rate Limiter

```text
Shared counter storage
```

may be the bottleneck.

### Chat

```text
Concurrent WebSocket connections
```

may be the bottleneck.

______________________________________________________________________

# 73. Capacity Estimation Examples

## URL Shortener

Suppose:

```text
10 million redirects/day
```

Average:

```text
≈ 116 requests/sec
```

At 10× peak:

```text
≈ 1,160 RPS
```

This helps determine application/cache/database capacity.

______________________________________________________________________

## Notification Service

Suppose:

```text
1 million notifications/day
```

Average:

```text
≈ 12 notifications/sec
```

But if 50% occur during one hour:

```text
500,000 / 3,600
≈ 139 notifications/sec
```

Workers should be sized for the actual peak requirement.

______________________________________________________________________

## Chat

Suppose:

```text
100,000 concurrent connections
```

This is not equivalent to:

```text
100,000 RPS
```

Connection capacity and message throughput must be considered separately.

______________________________________________________________________

# 74. API Design Principles

Across these systems:

### Use appropriate status codes

Examples:

```text
201 Created
202 Accepted
302/307 Redirect
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
429 Too Many Requests
500 Internal Server Error
503 Service Unavailable
```

The exact status depends on semantics.

______________________________________________________________________

# 75. Pagination

For large collections, avoid returning everything.

Offset:

```http
?page=10&limit=50
```

Cursor:

```http
?cursor=eyJpZCI6...
```

Cursor pagination is often preferable for large, frequently changing datasets.

______________________________________________________________________

# 76. API Idempotency

Consider:

```text
POST /payments
```

A network timeout occurs.

The client retries.

Without idempotency:

```text
Payment 1
Payment 2
```

With an idempotency key:

```text
Payment 1
Retry → existing result
```

The same principle appears in:

```text
Notifications
File operations
Chat messages
URL creation
```

where duplicate side effects matter.

______________________________________________________________________

# 77. Observability Across All Designs

Every production design should expose:

### Metrics

```text
Request rate
Error rate
Latency
Queue depth
Database latency
Cache hit rate
```

### Logs

```text
request_id
user/resource ID where appropriate
operation
status
duration
error
```

### Traces

Useful for:

```text
API → service → database
API → queue → worker → provider
```

______________________________________________________________________

# 78. Interview Answer Structure

When asked to design a system, use:

## Step 1 — Clarify

```text
Users
Traffic
Data
Latency
Availability
Consistency
```

## Step 2 — APIs

Define:

```text
Endpoints
Inputs
Outputs
Status codes
```

## Step 3 — Data

Explain:

```text
Tables
Indexes
Keys
Storage
```

## Step 4 — Architecture

Explain:

```text
Client
→ Gateway/LB
→ Service
→ Cache/DB/Queue
```

## Step 5 — Scale

Discuss:

```text
Horizontal scaling
Caching
Replication
Partitioning
Workers
```

## Step 6 — Failure

Discuss:

```text
Timeout
Retry
Duplicate
Dependency failure
Recovery
```

## Step 7 — Trade-Offs

Explain:

```text
Why this design?
What does it cost?
What would change at larger scale?
```

______________________________________________________________________

# 79. Common Interview Mistakes

## Mistake 1 — Drawing technology first

Do not start with:

```text
Kafka + Redis + Kubernetes + Elasticsearch
```

Start with requirements.

______________________________________________________________________

## Mistake 2 — No capacity estimates

Even rough numbers make the design more concrete.

______________________________________________________________________

## Mistake 3 — Ignoring failure

Every dependency needs a failure strategy.

______________________________________________________________________

## Mistake 4 — Assuming exactly-once delivery

Exactly-once behavior is difficult, especially across external side effects.

Design for idempotency.

______________________________________________________________________

## Mistake 5 — Overengineering

Do not add:

```text
Microservices
Kafka
Sharding
Multi-region
```

without a requirement.

______________________________________________________________________

## Mistake 6 — Ignoring operational limits

External providers, database connections, Redis memory, network bandwidth and concurrent connections all have limits.

______________________________________________________________________

# 80. Interview Questions & Answers

## Q1. What is the first thing you do in a system-design interview?

**Answer:**

Clarify functional and non-functional requirements, scale, latency, availability, consistency and important constraints
before choosing components.

______________________________________________________________________

## Q2. Why should you estimate traffic?

**Answer:**

Traffic estimates determine whether the system needs horizontal scaling, caching, queues, replicas and other
capacity-related components.

______________________________________________________________________

## Q3. Why should the API be stateless?

**Answer:**

Stateless instances can be scaled horizontally because any healthy instance can process a request without depending on
local durable state.

______________________________________________________________________

## Q4. Why are queues useful?

**Answer:**

They decouple producers from consumers, support asynchronous work, absorb bursts and provide mechanisms for retryable
processing.

______________________________________________________________________

## Q5. When would you use Pub/Sub instead of a queue?

**Answer:**

Use Pub/Sub when multiple independent consumers need to react to the same event. Use a work queue when a unit of work
should be processed by one consumer from a competing-consumer group.

______________________________________________________________________

## Q6. How do you prevent duplicate processing?

**Answer:**

Use idempotency keys, unique business identifiers, deduplication records or database constraints depending on the
operation.

______________________________________________________________________

## Q7. Why are retries dangerous?

**Answer:**

They increase traffic and can amplify an outage. Retries should be bounded and use suitable backoff and jitter.

______________________________________________________________________

## Q8. Why are timeouts required?

**Answer:**

They prevent resources from waiting indefinitely on unhealthy dependencies and help bound request latency and resource
usage.

______________________________________________________________________

## Q9. How would you handle a failing external dependency?

**Answer:**

Use an appropriate timeout, limited retries for transient errors, exponential backoff with jitter and potentially a
circuit breaker. Also define what the application should return or degrade to.

______________________________________________________________________

## Q10. How do you identify a bottleneck?

**Answer:**

Measure resource utilization and latency across components. Look at CPU, memory, database latency, connection pools,
cache hit rate, queue depth, network and dependency performance.

______________________________________________________________________

## Q11. Why is a cache not a source of truth in many designs?

**Answer:**

Caches are generally optimized for speed and can lose entries or contain stale values. Durable state usually belongs in
the authoritative datastore unless the architecture explicitly makes another system authoritative.

______________________________________________________________________

## Q12. What happens when a cache fails?

**Answer:**

The application may fall back to the source of truth if it can handle the load. Otherwise, protective measures are
needed to avoid a cache-miss storm.

______________________________________________________________________

## Q13. Why use object storage for large files?

**Answer:**

It separates large-object transfer and storage from application compute, allowing those resources to scale
independently.

______________________________________________________________________

## Q14. Why use WebSockets for chat?

**Answer:**

They provide persistent bidirectional communication, allowing the server to push messages to connected clients without
repeated polling.

______________________________________________________________________

## Q15. Why does chat need a database if WebSockets are real time?

**Answer:**

WebSockets provide transport, not durable storage. A database is needed for message history and offline synchronization
when those are requirements.

______________________________________________________________________

## Q16. Why does chat need Pub/Sub?

**Answer:**

When users are connected to different WebSocket servers, Pub/Sub can distribute messages between those servers.

______________________________________________________________________

## Q17. Why does rate limiting require shared state?

**Answer:**

With multiple application instances, a global limit requires coordination. Shared state prevents a client from bypassing
the limit by sending requests to different instances.

______________________________________________________________________

## Q18. Fail-open or fail-closed for a rate limiter?

**Answer:**

It depends on the risk. Fail-open preserves availability but can remove protection. Fail-closed preserves protection but
can reject legitimate traffic during a limiter outage.

______________________________________________________________________

## Q19. Why are signed URLs useful?

**Answer:**

They allow temporary, controlled access to object storage without exposing permanent credentials or requiring the
application to proxy large file transfers.

______________________________________________________________________

## Q20. What is the most important skill in practical system design?

**Answer:**

Reasoning about requirements, bottlenecks, failure modes and trade-offs rather than memorizing predefined architectures.

______________________________________________________________________

# 81. Final Interview Readiness Checklist

Before moving to File 41, make sure you can design at least a basic version of:

- [ ] URL shortener
- [ ] Notification service
- [ ] File upload service
- [ ] Rate limiter
- [ ] Chat service

For each one, you should be able to explain:

- [ ] Functional requirements
- [ ] Non-functional requirements
- [ ] Clarifying questions
- [ ] Capacity estimates
- [ ] APIs
- [ ] Data model
- [ ] Important indexes/constraints
- [ ] High-level architecture
- [ ] Data flow
- [ ] Scaling strategy
- [ ] Bottlenecks
- [ ] Failure modes
- [ ] Retry strategy
- [ ] Timeout strategy
- [ ] Idempotency
- [ ] Observability
- [ ] Trade-offs

You should also be able to explain:

- [ ] When to use a cache.
- [ ] When to use a queue.
- [ ] When to use Pub/Sub.
- [ ] When to use object storage.
- [ ] When to use WebSockets.
- [ ] When to use read replicas.
- [ ] When to use cursor pagination.
- [ ] Why stateless services scale.
- [ ] Why retries can cause cascading failures.
- [ ] Why idempotency matters.
- [ ] Why every fallback can become a bottleneck.
- [ ] Why the simplest architecture is often the best starting point.

______________________________________________________________________

# 82. Final Takeaways

The purpose of practical system design is to turn isolated concepts into architectural reasoning.

The reusable thought process is:

```text
Requirement
→ Estimate scale
→ Define API
→ Define data
→ Choose components
→ Find bottlenecks
→ Plan scaling
→ Plan failure handling
→ Add observability
→ Explain trade-offs
```

The five designs demonstrate different combinations of the same building blocks:

```text
URL Shortener
→ Read-heavy + cache

Notification Service
→ Queue + workers + retries

File Upload Service
→ Object storage + signed URLs + async processing

Rate Limiter
→ Distributed shared state + atomic operations

Chat Service
→ WebSockets + Pub/Sub + durable messages
```

Do not memorize these architectures as fixed answers.

Instead, learn why each component exists.

A strong interview answer should make the interviewer think:

> **"This engineer understands the problem, knows where the bottlenecks are, and understands what happens when things fail."**

That is the goal of this practical system-design section.

______________________________________________________________________

**Previous:** [39. Backend Architecture Building Blocks](./39-system-design-building-blocks.md)

**Next:** [41. TypeScript, Angular Overview](./41-typescript-angular.md)
