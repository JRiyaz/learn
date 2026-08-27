# 45. Resume & Project Deep Dive

**Previous:** [44. Behavioral & HR Interview](./44-behavioral.md)

**Next:** [46. AI-Assisted Software Engineering](./46-ai-assisted-development.md)

______________________________________________________________________

## Objective

For a senior backend interview, your resume is not just a document.

It is a map of topics the interviewer can explore.

Anything you claim on your resume can become a follow-up question:

```text
"How did you build it?"
"Why did you choose this?"
"What alternatives did you consider?"
"What was your contribution?"
"What went wrong?"
"How did you scale it?"
"How did you test it?"
"How did you deploy it?"
"How did you monitor it?"
"What would you change today?"
```

This topic teaches a structured way to discuss projects at a senior level.

The goal is not to memorize project descriptions.

The goal is to be able to move from:

```text
Resume bullet
     ↓
Project context
     ↓
Architecture
     ↓
Technical decisions
     ↓
Your contribution
     ↓
Trade-offs
     ↓
Production experience
```

______________________________________________________________________

# 1. The Project Deep-Dive Framework

For every major project on your resume, prepare these areas:

```text
1. Problem
2. Architecture
3. Your contribution
4. Technical decisions
5. Database
6. APIs
7. Cache
8. Messaging
9. Scaling
10. Security
11. Testing
12. Deployment
13. Monitoring
14. Production issues
15. Challenges
16. Achievements
17. Trade-offs
18. What you would change today
```

You do not need every area for every project.

But for senior-level projects, you should be prepared to discuss most of them when relevant.

______________________________________________________________________

# Part 1 — Problem

# 2. Start With the Problem

Do not begin with:

```text
"We used FastAPI, PostgreSQL and Redis."
```

Start with:

```text
What problem were we solving?
Who had the problem?
Why did it matter?
```

Example:

```text
The system was responsible for processing customer requests that
required asynchronous backend processing and status tracking.
```

Then explain why the system existed.

______________________________________________________________________

# 3. Problem Statement Formula

Use:

```text
Before
→ Problem
→ Impact
→ Solution
```

Example:

```text
Previously, requests were processed synchronously.

As processing time increased, API response times became unpredictable.

We moved long-running work into background workers and returned
a tracking identifier to the client.
```

This establishes the reason behind the architecture.

______________________________________________________________________

# 4. Business Context

Understand:

```text
Who uses the system?
What business process does it support?
What happens if it fails?
What is the scale?
```

Possible dimensions:

```text
Users
Requests/day
Transactions/day
Data volume
Latency requirements
Availability requirements
```

You do not need to invent exact numbers.

If you know approximate values, state that they are approximate.

______________________________________________________________________

# Part 2 — Architecture

# 5. Explain the Architecture

A simple explanation might be:

```text
Client
  ↓
Load Balancer
  ↓
FastAPI
  ↓
Service Layer
  ↓
PostgreSQL
```

If asynchronous processing exists:

```text
Client
  ↓
FastAPI
  ↓
Database
  ↓
Message Broker
  ↓
Worker
  ↓
External Service
```

Explain the responsibility of each component.

______________________________________________________________________

# 6. Architecture Explanation Order

A useful order is:

```text
Entry point
→ Request processing
→ Business logic
→ Data storage
→ Async processing
→ External systems
→ Response
```

This follows the request flow and makes the architecture easier to explain.

______________________________________________________________________

# 7. Explain Why, Not Just What

Weak:

```text
We used Redis.
```

Strong:

```text
We used Redis to cache frequently accessed data because the same
information was being requested repeatedly and the database was
becoming a bottleneck.
```

Then discuss:

```text
TTL
Invalidation
Consistency
Failure behavior
```

______________________________________________________________________

# 8. Architecture Diagram

Prepare a simple diagram for every important project.

Example:

```text
                   ┌─────────────┐
                   │   Client    │
                   └──────┬──────┘
                          ↓
                   ┌─────────────┐
                   │ Load Balancer│
                   └──────┬──────┘
                          ↓
                   ┌─────────────┐
                   │   FastAPI   │
                   └──────┬──────┘
                          ↓
                  ┌───────┴────────┐
                  ↓                ↓
            PostgreSQL          Redis
                  ↓
             Outbox/Event
                  ↓
                Kafka
                  ↓
               Workers
```

You should be able to draw the relevant version on a whiteboard.

______________________________________________________________________

# Part 3 — Your Contribution

# 9. Clearly Separate Team Work From Your Work

This is one of the most important areas.

Do not say:

```text
"I built the entire platform."
```

if it was a team effort.

Instead:

```text
The team built the platform.

I owned the API layer, database design for X and the asynchronous
processing workflow.
```

This is more credible.

______________________________________________________________________

# 10. Contribution Formula

Explain:

```text
What existed
→ What you owned
→ What you changed
→ Why you changed it
→ Result
```

Example:

```text
The initial implementation processed jobs synchronously.

I owned the processing workflow and moved long-running operations
to workers using a message queue.

This reduced request latency and allowed processing capacity to
scale independently.
```

______________________________________________________________________

# 11. Senior-Level Contribution

Senior contribution is not limited to writing code.

It can include:

```text
Architecture
Technical design
Performance
Reliability
Incident response
Mentoring
Code reviews
Migration
Operational improvements
Technical decision-making
```

Be prepared to explain decisions you influenced even if you did not implement every line.

______________________________________________________________________

# Part 4 — Technical Decisions

# 12. Every Major Decision Has a Reason

For each important technology, ask:

```text
Why this?
What alternatives existed?
Why did we reject them?
What trade-off did we accept?
```

Example:

```text
Why PostgreSQL?

Because the system required relational consistency, transactions and
complex queries.

A document database was considered but was not necessary for the
data model.
```

______________________________________________________________________

# 13. Decision Framework

Use:

```text
Requirement
→ Options
→ Evaluation criteria
→ Decision
→ Trade-off
```

Example:

```text
Requirement:
Need fast access to frequently requested data.

Options:
PostgreSQL
Redis

Decision:
Redis for caching.

Trade-off:
Better latency but introduces cache invalidation and consistency
complexity.
```

______________________________________________________________________

# 14. Avoid Technology-Driven Explanations

Weak:

```text
We used Kafka because Kafka is scalable.
```

Better:

```text
We needed asynchronous event processing with multiple independent
consumers and durable event retention.

Kafka fit those requirements, although it introduced operational
and delivery-semantics complexity.
```

______________________________________________________________________

# Part 5 — Database

# 15. Be Ready to Explain the Data Model

Know:

```text
Tables
Primary keys
Foreign keys
Indexes
Relationships
Constraints
Transactions
```

You should be able to explain the important tables without opening the code.

______________________________________________________________________

# 16. Database Questions

Expect questions such as:

```text
Why PostgreSQL?
How did you design the schema?
Why this primary key?
Which columns were indexed?
Why those indexes?
What queries were slow?
How did you optimize them?
What isolation level did you use?
How did you handle concurrent updates?
```

______________________________________________________________________

# 17. Database Trade-Offs

Be ready to discuss:

```text
Normalization
vs
Denormalization

Consistency
vs
Performance

Transactions
vs
Throughput

Indexes
vs
Write overhead
```

A strong answer acknowledges the trade-off instead of presenting one solution as universally correct.

______________________________________________________________________

# Part 6 — APIs

# 18. Explain Important APIs

Know the major endpoints:

```text
HTTP method
Path
Request
Response
Authentication
Validation
Errors
```

Example:

```text
POST /orders
GET /orders/{id}
GET /orders
PATCH /orders/{id}
```

______________________________________________________________________

# 19. API Design Questions

Be prepared for:

```text
Why REST?
How did you version APIs?
How did you validate requests?
How did you handle errors?
How did you handle pagination?
How did you authenticate?
How did you make operations idempotent?
```

______________________________________________________________________

# 20. Idempotency

If an API performs an important operation:

```text
POST /payments
```

consider what happens if the client retries the request.

A common approach:

```text
Client
 ↓
Idempotency-Key
 ↓
API
 ↓
Check existing operation
 ↓
Process once
```

Explain whether your actual project used this or another mechanism.

Do not claim it did if it did not.

______________________________________________________________________

# Part 7 — Cache

# 21. Why Was Caching Needed?

Explain:

```text
What was slow?
How frequently was it accessed?
Why was caching appropriate?
What consistency was required?
```

Example:

```text
A configuration object was read frequently but changed rarely.

We cached it with a TTL to reduce repeated database reads.
```

______________________________________________________________________

# 22. Cache Questions

Expect:

```text
What did you cache?
Why Redis?
What was the TTL?
How did invalidation work?
What happens if Redis is unavailable?
What happens on a cache miss?
How did you prevent cache stampede?
```

______________________________________________________________________

# 23. Cache Trade-Off

Caching provides:

```text
Lower latency
Reduced database load
Higher throughput
```

but introduces:

```text
Stale data
Invalidation complexity
Memory usage
Additional infrastructure
Failure modes
```

Always discuss both sides.

______________________________________________________________________

# Part 8 — Messaging

# 24. Why Use a Message Broker?

Typical reasons:

```text
Asynchronous processing
Decoupling
Load smoothing
Independent scaling
Event distribution
```

Example:

```text
API
 ↓
Queue
 ↓
Worker
```

The API does not need to wait for the worker to finish.

______________________________________________________________________

# 25. Messaging Questions

Be prepared for:

```text
Why Kafka/RabbitMQ?
How were messages acknowledged?
What happened on failure?
What was the retry strategy?
Could messages be duplicated?
How did you handle duplicates?
What was the delivery guarantee?
What happened to poison messages?
```

______________________________________________________________________

# 26. Idempotent Consumers

If a message can be delivered more than once:

```text
Message
 ↓
Consumer
 ↓
Processing
```

the consumer should be designed so repeated delivery does not incorrectly repeat the business operation.

Possible techniques include:

```text
Idempotency keys
Unique database constraints
Processed-message records
Transactional state changes
```

Choose the mechanism appropriate to the system.

______________________________________________________________________

# Part 9 — Scaling

# 27. Know Your Bottleneck

Do not say:

```text
"We scaled horizontally."
```

without explaining why.

Start with:

```text
What was the bottleneck?
```

Possible bottlenecks:

```text
CPU
Memory
Database
Network
Connection pool
External API
Queue
Disk
Lock contention
```

______________________________________________________________________

# 28. Scaling Example

Suppose:

```text
API CPU → 90%
```

Possible response:

```text
Horizontal application scaling
+
Load balancing
```

But if:

```text
Database CPU → 95%
```

adding API instances may not solve the underlying problem.

You may instead need:

```text
Query optimization
Indexes
Caching
Read replicas
Schema changes
Partitioning
```

______________________________________________________________________

# 29. Scaling Questions

Be ready to answer:

```text
What happens if traffic increases 10x?
What becomes the first bottleneck?
Can the application scale horizontally?
Is the application stateless?
Can the database scale?
What happens to cache capacity?
What happens to the queue?
```

______________________________________________________________________

# Part 10 — Security

# 30. Know the Security Model

Be prepared to explain:

```text
Authentication
Authorization
Secrets
Encryption
Input validation
Rate limiting
CORS
Security headers
Dependency security
```

______________________________________________________________________

# 31. Authentication vs Authorization

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Example:

```text
JWT proves identity
RBAC determines permissions
```

Know what your project actually used.

______________________________________________________________________

# 32. Security Questions

Expect:

```text
How were users authenticated?
How were permissions enforced?
Where were secrets stored?
How were passwords protected?
How did you prevent SQL injection?
How did you secure file uploads?
How did you protect internal endpoints?
```

______________________________________________________________________

# Part 11 — Testing

# 33. Testing Strategy

Know what types of tests existed:

```text
Unit tests
Integration tests
API tests
End-to-end tests
```

Explain what each layer protected.

______________________________________________________________________

# 34. Unit Testing

Unit tests isolate a small piece of behavior.

Example:

```text
OrderService
```

can be tested with:

```text
Mock repository
Mock payment gateway
```

This helps verify business logic independently.

______________________________________________________________________

# 35. Integration Testing

Integration tests verify that components work together.

Examples:

```text
FastAPI
+
Database

Worker
+
Message broker
```

These tests can catch problems that unit tests cannot.

______________________________________________________________________

# 36. Testing Questions

Expect:

```text
How much test coverage did you have?
What did you mock?
What did you test against a real database?
How did you test failures?
How did you test APIs?
How did you test asynchronous workflows?
```

Avoid focusing only on the percentage.

Explain what the tests actually protect.

______________________________________________________________________

# Part 12 — Deployment

# 37. Explain How Code Reached Production

Know the deployment pipeline:

```text
Developer
 ↓
Git
 ↓
CI
 ↓
Tests
 ↓
Build
 ↓
Container
 ↓
Deployment
 ↓
Health checks
 ↓
Production
```

Adapt this to the actual project.

______________________________________________________________________

# 38. Deployment Questions

Be ready for:

```text
Docker?
Kubernetes?
VMs?
Cloud platform?
CI/CD?
Environment configuration?
Secrets?
Database migrations?
Rollback?
Zero-downtime deployment?
Health checks?
```

Do not claim tools you only know theoretically.

______________________________________________________________________

# Part 13 — Monitoring

# 39. What Did You Monitor?

A production service should provide visibility into:

```text
Metrics
Logs
Traces
Health
Errors
Latency
Resource usage
Dependencies
```

______________________________________________________________________

# 40. Important API Metrics

Examples:

```text
Request count
Error rate
p50 latency
p95 latency
p99 latency
Throughput
```

For dependencies:

```text
Database latency
Connection pool utilization
Redis latency
Queue depth
Consumer lag
External API errors
```

______________________________________________________________________

# 41. Observability Questions

Expect:

```text
How did you know something was broken?
What alerts existed?
How did you investigate incidents?
What dashboards did you use?
How did you correlate requests?
```

______________________________________________________________________

# Part 14 — Production Issues

# 42. Prepare Real Incidents

For each important project, prepare at least:

```text
One production incident
One performance problem
One reliability problem
One difficult debugging problem
```

Use real examples.

______________________________________________________________________

# 43. Incident Structure

Use:

```text
Detection
→ Impact
→ Investigation
→ Mitigation
→ Root cause
→ Fix
→ Prevention
```

Example:

```text
Monitoring detected elevated 5xx errors.

I checked application logs and dependency metrics and narrowed the
problem to database connection exhaustion.

We restored service by reducing the immediate load and restarting
the affected workers.

The permanent fix addressed connection handling and added monitoring
for pool utilization.
```

______________________________________________________________________

# Part 15 — Challenges

# 44. "What Was the Most Difficult Part?"

Do not choose something difficult only because it was technically complicated.

Choose a problem that demonstrates:

```text
Reasoning
Decision-making
Persistence
Technical depth
Impact
```

______________________________________________________________________

# 45. Challenge Answer

Use:

```text
Challenge
→ Why it was difficult
→ Options considered
→ What you did
→ Result
→ Learning
```

______________________________________________________________________

# 46. Technical Challenge Example

```text
The difficult part was maintaining consistency while allowing
multiple workers to process tasks concurrently.

The main challenge was avoiding duplicate processing while still
keeping throughput high.

I evaluated locking and idempotency approaches and chose an
idempotent processing model backed by database constraints.

This reduced duplicate side effects while allowing workers to scale.
```

Adapt this to your actual experience.

______________________________________________________________________

# Part 16 — Achievements

# 47. Explain Impact

A technical achievement should connect:

```text
Change
→ Metric/business outcome
```

Examples:

```text
Reduced latency
Reduced infrastructure cost
Improved reliability
Increased throughput
Reduced incidents
Reduced deployment time
Improved developer productivity
```

______________________________________________________________________

# 48. Before vs After

A powerful format:

```text
Before:
p95 latency = X

Change:
Optimized query + added appropriate index

After:
p95 latency = Y
```

Or:

```text
Before:
Manual deployment

After:
Automated CI/CD pipeline
```

Use real measurements whenever available.

______________________________________________________________________

# Part 17 — Trade-Offs

# 49. Senior Engineers Discuss Trade-Offs

Almost every technical decision has a cost.

Examples:

```text
Cache
→ performance vs consistency

Microservices
→ independent scaling vs operational complexity

Async processing
→ responsiveness vs eventual consistency

Indexes
→ read performance vs write/storage cost

Normalization
→ consistency vs query complexity

Denormalization
→ read simplicity/performance vs update complexity

Kafka
→ durable event streaming vs operational complexity

Repository abstraction
→ separation vs additional indirection
```

______________________________________________________________________

# 50. How to Explain a Trade-Off

Use:

```text
We needed X.

We considered A and B.

We chose A because of Y.

The downside was Z.

We accepted that trade-off because the requirement was more important.
```

This is much stronger than:

```text
"Technology A is better."
```

______________________________________________________________________

# Part 18 — What Would You Change Today?

# 51. "If You Built It Today, What Would You Change?"

This is a very common senior-level question.

Do not say:

```text
Nothing.
```

Real systems evolve.

______________________________________________________________________

# 52. Good Answer

A good response might be:

```text
Given what we knew at the time, the original design was reasonable.

If I rebuilt it today, I would change X because we now understand Y.

I would not change Z because that trade-off still makes sense.
```

This demonstrates judgment.

______________________________________________________________________

# 53. Avoid Hindsight Bias

Do not criticize the old design simply because you now know more.

Explain:

```text
Original constraints
+
Information available at the time
→
Original decision
```

Then:

```text
New requirements/knowledge
→
Potential improvement today
```

______________________________________________________________________

# Part 19 — Resume Bullet Deep Dive

# 54. Every Resume Bullet Is a Question

Suppose your resume says:

```text
Improved API performance by 40%.
```

Expect:

```text
How?
What was slow?
How did you measure it?
What did you change?
Why did that fix work?
How did you verify it?
What trade-offs did it introduce?
```

Prepare the complete story behind the number.

______________________________________________________________________

# 55. "Built a Scalable API"

If your resume says:

```text
Built scalable FastAPI services.
```

be prepared for:

```text
What made it scalable?
How did you load balance?
Was it stateless?
What was the bottleneck?
How did the database scale?
How did you handle caching?
What happened under high load?
How did you measure scalability?
```

Avoid vague claims unless you can defend them.

______________________________________________________________________

# 56. "Designed Microservices"

Expect:

```text
Why microservices?
Why not a monolith?
How were services split?
How did they communicate?
How did you handle transactions?
How did you handle failures?
How did you deploy them?
How did you monitor them?
```

______________________________________________________________________

# 57. "Implemented Kafka"

Expect:

```text
Why Kafka?
What were the topics?
How many partitions?
How were consumer groups used?
How did you handle offsets?
What delivery semantics?
How did you handle duplicates?
What happened when consumers failed?
How did you monitor lag?
```

Know the actual answers for your project.

______________________________________________________________________

# 58. "Implemented Redis Caching"

Expect:

```text
What did you cache?
Why Redis?
What was the TTL?
How did invalidation work?
What happened during a cache miss?
How did you handle Redis failure?
How did you prevent stale data?
```

______________________________________________________________________

# 59. "Optimized Database Queries"

Expect:

```text
Which query?
Why was it slow?
What did EXPLAIN show?
What index did you add?
Why that index?
What was the before/after latency?
Did writes become slower?
```

______________________________________________________________________

# Part 20 — Project One-Minute Summary

# 60. Prepare a One-Minute Version

Every major project should have a concise explanation.

Template:

```text
I worked on [system], which solved [problem].

The architecture consisted of [major components].

My main responsibility was [your contribution].

One of the main technical challenges was [challenge].

We solved it by [solution].

The result was [impact].
```

This is your starting point.

The interviewer can then choose the area to explore.

______________________________________________________________________

# 61. Project Five-Minute Version

For deeper discussion:

```text
1. Problem
2. Users/scale
3. Architecture
4. Your contribution
5. Key technical decisions
6. Database
7. APIs
8. Async/messaging
9. Scaling
10. Security
11. Testing
12. Deployment
13. Monitoring
14. Incident
15. Trade-offs
```

You should be able to expand each section when asked.

______________________________________________________________________

# Part 21 — Project Knowledge Map

# 62. Create a Project Map

For each major project, maintain:

```text
Project
│
├── Problem
├── Architecture
│   ├── API
│   ├── Services
│   ├── Database
│   ├── Cache
│   └── Messaging
│
├── Your Contribution
│
├── Decisions
│   ├── Why technology X?
│   ├── Why architecture Y?
│   └── Alternatives
│
├── Operations
│   ├── Deployment
│   ├── Monitoring
│   └── Incidents
│
└── Results
    ├── Performance
    ├── Reliability
    └── Business impact
```

______________________________________________________________________

# 63. Project Numbers

Know approximate values where possible:

```text
Requests/day
Peak requests/second
Database size
Number of tables
Number of services
Number of workers
Queue throughput
Cache size
Typical latency
p95/p99 latency
Availability
Deployment frequency
```

Do not invent numbers.

If you only know an approximate range:

```text
"Roughly tens of thousands of requests per day."
```

is better than creating a false precise number.

______________________________________________________________________

# Part 22 — Interview Follow-Up Chains

# 64. Expect the Interviewer to Go Deeper

Example:

```text
You:
"We added Redis caching."

Interviewer:
Why?

You:
"Database load was high."

Interviewer:
Why was database load high?

You:
"One endpoint repeatedly queried the same data."

Interviewer:
Why didn't you optimize the query?

You:
"The query was already efficient; the problem was repeated access
to relatively static data."

Interviewer:
How did you invalidate the cache?

You:
...
```

This is why you need to understand the underlying reasoning rather than memorize keywords.

______________________________________________________________________

# 65. The Five Whys

For important technical decisions, ask:

```text
Why?
Why?
Why?
Why?
Why?
```

Example:

```text
Why Redis?
→ Reduce database reads.

Why were database reads high?
→ Same data requested repeatedly.

Why couldn't the data be stored in application memory?
→ Multiple application instances needed shared cache state.

Why not only database optimization?
→ Query latency was acceptable, but request volume was the problem.

Why Redis?
→ Shared low-latency cache with TTL matched the workload.
```

This prepares you for deeper questioning.

______________________________________________________________________

# Part 23 — Common Senior-Level Questions

## Q1. What was the most important technical decision in the project?

Answer with:

```text
Decision
→ Context
→ Alternatives
→ Trade-offs
→ Outcome
```

______________________________________________________________________

## Q2. What would you redesign?

Explain:

```text
What changed
→ Why the old approach became limiting
→ New approach
→ Trade-offs
```

______________________________________________________________________

## Q3. What was the biggest bottleneck?

Do not answer only:

```text
"Database."
```

Explain:

```text
How you discovered it
→ Why it was the bottleneck
→ What you changed
→ How you measured improvement
```

______________________________________________________________________

## Q4. What was your biggest contribution?

Focus on:

```text
Ownership
Complexity
Impact
```

______________________________________________________________________

## Q5. What was the hardest bug?

Explain:

```text
Symptoms
→ Investigation
→ Hypotheses
→ Evidence
→ Root cause
→ Fix
```

______________________________________________________________________

## Q6. What would happen if traffic increased 10x?

Discuss:

```text
Application
→ Load balancing
→ Database
→ Cache
→ Queue
→ External dependencies
```

Identify the first bottleneck rather than claiming everything scales automatically.

______________________________________________________________________

## Q7. What happens if the database goes down?

Explain the actual system behavior:

```text
Detection
→ Connection failures
→ API behavior
→ Retry/timeout
→ Degraded mode if applicable
→ Recovery
```

Do not claim a failover strategy unless the project actually had one.

______________________________________________________________________

## Q8. What happens if Redis goes down?

Discuss:

```text
Cache misses
→ Database load
→ Timeout behavior
→ Recovery
```

The answer depends on whether Redis was:

```text
Optional cache
```

or:

```text
Required application state
```

______________________________________________________________________

## Q9. What happens if the message broker goes down?

Discuss:

```text
Producer behavior
Consumer behavior
Retries
Persistence
Backlog
Recovery
```

Again, explain the actual system rather than an ideal architecture.

______________________________________________________________________

## Q10. How did you ensure reliability?

Possible areas:

```text
Timeouts
Retries
Idempotency
Transactions
Health checks
Monitoring
Graceful failure
Circuit breakers
Dead-letter handling
```

Only mention mechanisms actually used or clearly distinguish improvements you would add.

______________________________________________________________________

# Part 24 — Red Flags During Project Discussions

# 66. Claiming Ownership of Everything

Bad:

```text
"I designed everything."
```

Better:

```text
"I owned the API and processing architecture while other team members
owned infrastructure and frontend."
```

______________________________________________________________________

# 67. Naming Technologies Without Understanding Them

Bad:

```text
"We used Kafka, Redis, Kubernetes and microservices."
```

Then being unable to explain:

```text
Why?
How?
Failure behavior?
Trade-offs?
```

Only put technologies on your resume that you can discuss.

______________________________________________________________________

# 68. Giving Architecture Without Requirements

Bad:

```text
"We used microservices for scalability."
```

Better:

```text
"We had independently scaling workloads and separate ownership
boundaries, so we chose service separation. The trade-off was higher
deployment and operational complexity."
```

______________________________________________________________________

# 69. Ignoring Failure Cases

Senior engineers should naturally consider:

```text
What if the database fails?
What if Redis fails?
What if a message is duplicated?
What if an external API times out?
What if a worker crashes?
What if traffic spikes?
```

______________________________________________________________________

# 70. Ignoring Observability

If you claim a production system is reliable, expect:

```text
How did you know?
```

Be ready to discuss:

```text
Logs
Metrics
Traces
Alerts
Dashboards
Health checks
```

______________________________________________________________________

# Part 25 — Project Preparation Template

Use this template for each major resume project.

```text
PROJECT:
________________________________________

PROBLEM:
________________________________________

USERS / SCALE:
________________________________________

ARCHITECTURE:
________________________________________

MY CONTRIBUTION:
________________________________________

KEY TECHNICAL DECISIONS:
1. ______________________________________
2. ______________________________________
3. ______________________________________

DATABASE:
________________________________________

APIs:
________________________________________

CACHE:
________________________________________

MESSAGING:
________________________________________

SCALING:
________________________________________

SECURITY:
________________________________________

TESTING:
________________________________________

DEPLOYMENT:
________________________________________

MONITORING:
________________________________________

PRODUCTION INCIDENT:
________________________________________

HARDEST CHALLENGE:
________________________________________

BIGGEST ACHIEVEMENT:
________________________________________

IMPORTANT TRADE-OFF:
________________________________________

WHAT I WOULD CHANGE TODAY:
________________________________________
```

______________________________________________________________________

# Part 26 — Final Interview Readiness Checklist

## Project Understanding

- [ ] Explain the problem.
- [ ] Explain the users.
- [ ] Explain approximate scale.
- [ ] Draw the architecture.
- [ ] Explain each major component.
- [ ] Explain your exact contribution.
- [ ] Explain important technical decisions.

## Database

- [ ] Explain schema.
- [ ] Explain relationships.
- [ ] Explain indexes.
- [ ] Explain transactions.
- [ ] Explain concurrency considerations.
- [ ] Explain performance issues.

## APIs

- [ ] Explain important endpoints.
- [ ] Explain request/response models.
- [ ] Explain validation.
- [ ] Explain authentication.
- [ ] Explain authorization.
- [ ] Explain pagination.
- [ ] Explain idempotency.

## Cache

- [ ] Explain what was cached.
- [ ] Explain why.
- [ ] Explain TTL.
- [ ] Explain invalidation.
- [ ] Explain cache failure behavior.

## Messaging

- [ ] Explain why messaging was needed.
- [ ] Explain producer/consumer behavior.
- [ ] Explain delivery semantics.
- [ ] Explain retries.
- [ ] Explain duplicate handling.
- [ ] Explain dead-letter handling if applicable.

## Scaling

- [ ] Identify the main bottleneck.
- [ ] Explain horizontal scaling.
- [ ] Explain database scaling.
- [ ] Explain caching.
- [ ] Explain queue/worker scaling.
- [ ] Explain what happens under 10x traffic.

## Security

- [ ] Authentication.
- [ ] Authorization.
- [ ] Secrets.
- [ ] Input validation.
- [ ] Common attack prevention.

## Testing

- [ ] Unit tests.
- [ ] Integration tests.
- [ ] API tests.
- [ ] Failure testing.
- [ ] Async workflow testing.

## Production

- [ ] Deployment.
- [ ] Health checks.
- [ ] Monitoring.
- [ ] Metrics.
- [ ] Logs.
- [ ] Alerts.
- [ ] Production incidents.
- [ ] Recovery process.

## Senior-Level Discussion

- [ ] Explain trade-offs.
- [ ] Explain alternatives.
- [ ] Explain failures.
- [ ] Explain what you would change today.
- [ ] Distinguish team work from your contribution.
- [ ] Quantify results where possible.
- [ ] Explain decisions using requirements.

______________________________________________________________________

# 27. Final Takeaways

For every important project, be able to answer:

```text
What problem did it solve?

Why was the architecture designed this way?

What exactly did I own?

Why did we choose these technologies?

What were the alternatives?

What were the bottlenecks?

How did we scale?

How did we secure it?

How did we test it?

How did we deploy it?

How did we monitor it?

What went wrong in production?

What was the hardest technical challenge?

What was the biggest achievement?

What trade-offs did we make?

What would I change today?
```

The most important principle is:

> **If it is on your resume, be prepared to defend it.**

A senior-level project discussion should move naturally from:

```text
Problem
 ↓
Architecture
 ↓
Your contribution
 ↓
Technical decisions
 ↓
Trade-offs
 ↓
Production reality
 ↓
Lessons learned
```

Do not try to make the project sound perfect.

Real systems have:

```text
Constraints
Trade-offs
Failures
Technical debt
Operational problems
Changing requirements
```

Being able to explain those honestly is often stronger than presenting an unrealistically perfect architecture.

The interviewer is not only evaluating whether you built something.

They are evaluating whether you understand:

```text
Why it was built
How it works
Why it works
Where it fails
How you would improve it
```

That is the difference between:

```text
"I worked on this project."
```

and:

```text
"I understand this system deeply and can make informed engineering
decisions about it."
```

______________________________________________________________________

**Previous:** [44. Behavioral & HR Interview](./44-behavioral.md)

**Next:** [46. AI-Assisted Software Engineering](./46-ai-assisted-development.md)
