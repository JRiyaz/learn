# Python Backend Engineer Interview Preparation

> **4-Day Intensive Interview Preparation Course**\
> **Target:** Software Engineer / Senior Software Engineer — 5+ years Python backend experience\
> **Structure:** 47 topic files + this index\
> **Total Markdown files:** 48

______________________________________________________________________

## Course Goal

This course is designed specifically for a **5+ year Python backend engineer preparing for technical interviews**.

The goal is not to cover every technology or every advanced computer-science topic. Instead, it prioritizes the concepts
that are most useful for:

- Python backend interviews
- Senior software-engineer interviews
- API/backend development
- Database interviews
- Production engineering discussions
- Coding rounds
- Practical system-design rounds
- Project/resume deep dives
- Behavioral interviews

### Intentionally excluded

- AWS
- Kubernetes
- Advanced DSA
- Advanced distributed systems
- Deep/global-scale system design

### Included as overview only

- Flask
- Angular
- TypeScript
- NumPy
- Pandas
- Database scaling
- Advanced architecture concepts

______________________________________________________________________

# How Every Topic File Is Structured

Every file from **01 through 45** follows the same structure.

```text
Title
↓
Previous / Next relative references
↓
Objectives
↓
Topics / Detailed Content
↓
Practical Examples
↓
Backend Relevance
↓
Interview Questions & Answers
↓
Scenario-Based Questions
↓
Practice Exercises
↓
Quick Revision
↓
Completion Checklist
↓
Interview Readiness Test
↓
Previous / Next relative references
```

### Q&A requirement

**Every individual topic file must have a dedicated Interview Questions & Answers section.**

Questions will be directly related to the content covered in that file.

Answers should be appropriate for a **5+ year engineer** and should include follow-ups, trade-offs, practical examples,
or senior-level considerations where useful.

The final rapid-fire file is an additional revision bank; it does **not** replace the Q&A in individual files.

______________________________________________________________________

# Course Roadmap

## Phase 1 — Python Core

### 01. Python Runtime, Objects, Memory & Scope

[Open `01-python-core.md`](./01-python-core.md)

Covers:

- Python vs CPython
- Object model
- Names and references
- Identity and equality
- `is` vs `==`
- Mutable vs immutable objects
- Hashability
- Memory management
- Reference counting
- Garbage collection
- Reference cycles
- `del`
- Shallow/deep copy
- LEGB
- `global`
- `nonlocal`
- Namespaces
- Common Python traps

______________________________________________________________________

### 02. Functions & Functional Programming

[Open `02-python-functions.md`](./02-python-functions.md)

Covers:

- First-class functions
- Function arguments
- Positional and keyword arguments
- `*args`
- `**kwargs`
- Positional-only arguments
- Keyword-only arguments
- Lambda
- Higher-order functions
- `map`
- `filter`
- `reduce`
- `zip`
- `enumerate`
- `any`
- `all`
- Comprehensions
- `functools`
- `itertools`

______________________________________________________________________

### 03. Decorators & Context Managers

[Open `03-python-decorators-context-managers.md`](./03-python-decorators-context-managers.md)

Covers:

- Function decorators
- Parameterized decorators
- Multiple decorators
- `functools.wraps`
- Class decorators overview
- Context-manager protocol
- `__enter__`
- `__exit__`
- `contextlib`
- Resource cleanup
- Backend use cases

______________________________________________________________________

### 04. Iterators, Generators & Lazy Evaluation

[Open `04-python-iterators-generators.md`](./04-python-iterators-generators.md)

Covers:

- Iterable
- Iterator
- Iterator protocol
- `iter`
- `next`
- `StopIteration`
- Generators
- `yield`
- `yield from`
- Generator expressions
- Lazy evaluation
- Streaming
- Large-file processing
- Memory efficiency

______________________________________________________________________

### 05. Python Collections

[Open `05-python-collections.md`](./05-python-collections.md)

**Important dedicated topic.**

Covers:

- List
- Tuple
- Set
- Frozenset
- Dictionary
- String
- `collections` module
- `Counter`
- `defaultdict`
- `deque`
- `namedtuple`
- `ChainMap`
- Hash tables
- Dictionary internals overview
- Ordering
- Membership
- Time complexity
- Choosing the correct collection
- Common collection interview problems

______________________________________________________________________

### 06. Python Exception Handling

[Open `06-python-exceptions.md`](./06-python-exceptions.md)

Covers:

- Exception hierarchy
- `try` / `except` / `else` / `finally`
- Raising exceptions
- Custom exceptions
- Exception chaining
- Tracebacks
- Logging exceptions
- Backend error boundaries
- Business errors vs programming errors
- Retryable vs non-retryable errors
- Exception handling in workers
- Context-manager cleanup
- Common exception-handling mistakes

______________________________________________________________________

### 07. Python Modules, Packages & Virtual Environments

[Open `07-python-modules-packages.md`](./07-python-modules-packages.md)

Covers:

- Modules
- Packages
- `import`
- Absolute and relative imports
- `__init__.py`
- `__name__`
- `__main__`
- `sys.path`
- `sys.modules`
- Circular imports
- Virtual environments
- `venv`
- `pip`
- `requirements.txt`
- Dependency management
- Lock files
- Editable installs
- `pyproject.toml`
- Backend package structure

______________________________________________________________________

### 08. Python OOP & Object Model

[Open `08-python-oop.md`](./08-python-oop.md)

Covers:

- Classes
- Objects
- Instance attributes
- Class attributes
- Instance methods
- `classmethod`
- `staticmethod`
- Properties
- Encapsulation
- Inheritance
- Polymorphism
- Composition
- Dependency injection
- Dataclasses
- Enums
- Dunder methods
- Equality and hashing
- SOLID principles

______________________________________________________________________

### 09. Advanced Python OOP

[Open `09-python-advanced-oop.md`](./09-python-advanced-oop.md)

Covers:

- Multiple inheritance
- MRO
- `super()`
- Abstract base classes
- Mixins
- Descriptors
- `__slots__`
- `__new__`
- Metaclasses
- Duck typing
- Protocols

The focus is practical interview understanding rather than academic metaprogramming.

______________________________________________________________________

### 10. Python Concurrency & AsyncIO

[Open `10-python-concurrency.md`](./10-python-concurrency.md)

Covers:

- Process vs thread
- CPU-bound vs I/O-bound
- GIL
- Threading
- Locks
- Race conditions
- Deadlocks
- ThreadPoolExecutor
- Multiprocessing
- ProcessPoolExecutor
- AsyncIO
- Event loop
- Coroutines
- Tasks
- `await`
- `gather`
- Cancellation
- Timeouts
- Blocking code in async applications

______________________________________________________________________

### 11. Typing & Testing

[Open `11-python-exceptions-typing-testing.md`](./11-python-exceptions-typing-testing.md)

This file retains the typing and testing scope from the original plan; basic exception handling is covered separately in
File 06.

Covers:

- Type hints
- Generics
- `Optional`
- `Union`
- `Literal`
- `TypedDict`
- Protocol overview
- pytest
- Fixtures
- Mocking
- Monkeypatch
- Unit testing
- Integration testing
- API testing
- Testing strategy

______________________________________________________________________

# Phase 2 — Web & Backend

### 12. HTTP, TCP/IP, TLS & Networking

[Open `12-http-networking.md`](./12-http-networking.md)

Covers:

- DNS
- TCP
- UDP overview
- TCP handshake
- TLS
- HTTPS
- HTTP methods
- Status codes
- Headers
- Cookies
- Sessions
- Keep-alive
- HTTP/1.1
- HTTP/2 overview
- REST
- Idempotency

______________________________________________________________________

### 13. Complete Backend Request Lifecycle

[Open `13-request-lifecycle.md`](./13-request-lifecycle.md)

Covers the journey from:

**Client → DNS → TCP/TLS → CDN/WAF → Load Balancer → Reverse Proxy → ASGI → FastAPI → Middleware → Authentication →
Validation → Business Logic → ORM → Database → Serialization → Response**

Also covers:

- Request lifecycle
- Application servers
- Blocking vs non-blocking behavior
- Connection handling
- Failure points
- Observability

______________________________________________________________________

### 14. FastAPI Fundamentals

[Open `14-fastapi-core.md`](./14-fastapi-core.md)

Covers:

- FastAPI architecture
- ASGI
- Routing
- Path parameters
- Query parameters
- Request bodies
- Pydantic
- Validation
- Response models
- Serialization
- Routers
- OpenAPI
- API documentation
- API versioning
- Headers
- Cookies
- Forms
- File uploads

______________________________________________________________________

### 15. FastAPI Dependency Injection, Middleware & Errors

[Open `15-fastapi-di-middleware-errors.md`](./15-fastapi-di-middleware-errors.md)

Covers:

- Dependency injection
- Nested dependencies
- Dependency overrides
- Middleware
- Request lifecycle
- Exception handlers
- Custom exceptions
- Validation errors
- Authentication dependencies
- Testing dependencies

______________________________________________________________________

### 16. Production FastAPI

[Open `16-fastapi-production.md`](./16-fastapi-production.md)

Covers:

- Authentication
- Authorization
- JWT
- OAuth2
- RBAC
- Async endpoints
- Background tasks
- External API calls
- Retry
- Timeout
- Pagination
- Filtering
- Rate limiting
- Health checks
- Graceful shutdown
- Observability
- Metrics
- Production architecture

______________________________________________________________________

### 17. Flask

[Open `17-flask.md`](./17-flask.md)

Focused Flask coverage:

- Flask architecture
- Routing
- Request/response
- Blueprints
- Application factory
- Configuration
- Extensions
- REST APIs
- Authentication
- Testing
- WSGI
- Gunicorn
- Flask vs FastAPI

This is intentionally less detailed than the FastAPI coverage.

______________________________________________________________________

# Phase 3 — SQL & Databases

### 18. SQL Fundamentals

[Open `18-sql-fundamentals.md`](./18-sql-fundamentals.md)

Covers:

- Relational database concepts
- Tables
- Rows
- Columns
- Primary keys
- Foreign keys
- CRUD
- SELECT
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- NULL
- Constraints
- Joins
- Aggregate functions
- Common SQL interview problems

______________________________________________________________________

### 19. Database Design & Normalization

[Open `19-database-normalization.md`](./19-database-normalization.md)

**Important dedicated database-design topic.**

Covers:

- Database design fundamentals
- Redundancy
- Data anomalies
- Insert anomaly
- Update anomaly
- Delete anomaly
- Functional dependencies
- Candidate keys
- Primary keys
- 1NF
- 2NF
- 3NF
- BCNF overview
- Normalization examples
- Normalization vs denormalization
- When to denormalize
- Real-world backend trade-offs

Special focus:

> Interviewers often care more about understanding the trade-off than memorizing normalization definitions.

______________________________________________________________________

### 20. Advanced SQL Queries

[Open `20-sql-advanced.md`](./20-sql-advanced.md)

Covers:

- Subqueries
- Correlated subqueries
- `EXISTS`
- `IN`
- CTEs
- Window functions
- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `LAG`
- `LEAD`
- Set operations
- Common interview query patterns

______________________________________________________________________

### 21. SQL Indexes & Query Performance

[Open `21-sql-indexes-performance.md`](./21-sql-indexes-performance.md)

Covers:

- Why indexes
- B-tree overview
- Composite indexes
- Index ordering
- Selectivity
- Covering indexes
- Query plans
- `EXPLAIN`
- Slow-query diagnosis
- Index trade-offs
- Pagination performance

______________________________________________________________________

### 22. Transactions, ACID & Database Concurrency

[Open `22-sql-transactions.md`](./22-sql-transactions.md)

Covers:

- Transactions
- ACID
- Atomicity
- Consistency
- Isolation
- Durability
- Isolation levels
- Dirty reads
- Non-repeatable reads
- Phantom reads
- Locks
- Deadlocks
- MVCC
- Optimistic locking
- Pessimistic locking

______________________________________________________________________

### 23. SQLAlchemy ORM

[Open `23-sqlalchemy-core.md`](./23-sqlalchemy-core.md)

Covers:

- Engine
- Connection
- Session
- Session lifecycle
- Flush
- Commit
- Rollback
- Identity map
- Unit of work
- Models
- Relationships
- CRUD
- Transactions
- Connection pooling

______________________________________________________________________

### 24. SQLAlchemy Performance & Async

[Open `24-sqlalchemy-performance.md`](./24-sqlalchemy-performance.md)

Covers:

- Lazy loading
- Eager loading
- `joinedload`
- `selectinload`
- N+1
- Async SQLAlchemy
- Async sessions
- Connection pooling
- ORM vs raw SQL
- Query optimization
- FastAPI integration

______________________________________________________________________

### 25. Database Scaling — Practical Overview

[Open `25-database-scaling.md`](./25-database-scaling.md)

Covers:

- Vertical scaling
- Replication
- Read replicas
- Partitioning
- Sharding overview
- Denormalization
- Database bottlenecks
- Choosing a scaling strategy

Only practical interview-level coverage.

______________________________________________________________________

# Phase 4 — Redis & Messaging

### 26. Redis Fundamentals

[Open `26-redis.md`](./26-redis.md)

Covers:

- Redis architecture
- Strings
- Hashes
- Lists
- Sets
- Sorted sets
- Streams overview
- TTL
- Expiration
- Atomic operations
- Transactions

______________________________________________________________________

### 27. Redis Caching & Production

[Open `27-redis-caching.md`](./27-redis-caching.md)

Covers:

- Cache-aside
- Write-through
- Write-back
- Cache invalidation
- Cache stampede
- Cache penetration
- Cache avalanche
- Distributed locks
- `SET NX`
- Persistence
- RDB
- AOF
- Eviction
- LRU
- LFU
- Replication
- Sentinel
- Cluster

______________________________________________________________________

### 28. Kafka

[Open `28-kafka.md`](./28-kafka.md)

Covers:

- Broker
- Topic
- Partition
- Producer
- Consumer
- Offset
- Consumer groups
- Replication
- Ordering
- Consumer lag
- Delivery semantics
- At-most-once
- At-least-once
- Exactly-once concept
- Idempotency
- Retry
- Dead-letter handling
- Schema evolution

______________________________________________________________________

### 29. RabbitMQ & Celery

[Open `29-rabbitmq-celery.md`](./29-rabbitmq-celery.md)

RabbitMQ:

- Exchange
- Queue
- Binding
- Routing key
- ACK
- Prefetch
- TTL
- Dead-letter exchange
- Durability

Celery:

- Tasks
- Workers
- Broker
- Result backend
- Retry
- Timeout
- Beat
- Worker concurrency
- Idempotency
- FastAPI integration

Also includes:

**Kafka vs RabbitMQ vs Celery**

______________________________________________________________________

# Phase 5 — Production Engineering

### 30. Docker

[Open `30-docker.md`](./30-docker.md)

Covers:

- Images
- Containers
- Dockerfile
- Layers
- Multi-stage builds
- Volumes
- Networking
- Environment variables
- Secrets
- Health checks
- Resource limits
- Docker Compose
- FastAPI/Postgres/Redis setup
- Debugging

______________________________________________________________________

### 31. Linux for Backend Engineers

[Open `31-linux.md`](./31-linux.md)

Covers:

- Filesystem
- Permissions
- Users/groups
- Processes
- Threads
- Signals
- Shell
- Pipes
- Redirection
- grep
- awk
- sed
- SSH
- Networking
- Disk
- Memory
- systemd
- Logs
- cron

______________________________________________________________________

### 32. Production Debugging & Incident Response

[Open `32-production-debugging.md`](./32-production-debugging.md)

Scenario-driven debugging for:

- CPU at 100%
- Memory growth
- Disk full
- Slow APIs
- 502/503
- Database unavailable
- Connection pool exhaustion
- Redis unavailable
- Kafka consumer lag
- Duplicate messages
- Container restart
- Network problems
- Deadlocks

Includes a repeatable production-debugging methodology.

______________________________________________________________________

### 33. Backend Security

[Open `33-security.md`](./33-security.md)

Covers:

- OWASP fundamentals
- SQL injection
- XSS
- CSRF
- Broken authentication
- Broken authorization
- JWT
- OAuth2
- HTTPS
- CORS
- SSRF
- Command injection
- Path traversal
- File upload security
- Secrets
- Rate limiting
- Security headers
- Dependency security
- Least privilege

______________________________________________________________________

### 34. Git & Engineering Workflow

[Open `34-git.md`](./34-git.md)

Covers:

- Branching
- Merge
- Rebase
- Conflict resolution
- Reset
- Revert
- Stash
- Cherry-pick
- Squashing
- Reflog
- Bisect
- Pull requests
- Code reviews

______________________________________________________________________

# Phase 6 — DSA

### 35. DSA Fundamentals

[Open `35-dsa-foundations.md`](./35-dsa-foundations.md)

Covers:

- Big-O
- Arrays
- Strings
- Hash maps
- Sets
- Stacks
- Queues
- Linked lists
- Trees
- Recursion

______________________________________________________________________

### 36. DSA Interview Patterns

[Open `36-dsa-patterns.md`](./36-dsa-patterns.md)

Covers:

- Two pointers
- Sliding window
- Hash-map patterns
- Stack patterns
- Binary search
- BFS
- DFS
- Top-K
- Prefix/suffix
- Basic dynamic programming

**Advanced DSA is intentionally excluded.**

______________________________________________________________________

### 37. DSA Coding Practice

[Open `37-dsa-practice.md`](./37-dsa-practice.md)

Curated easy/medium problems.

Examples:

- Two Sum
- Contains Duplicate
- Group Anagrams
- Top K Frequent
- Longest Consecutive Sequence
- Valid Palindrome
- Container With Most Water
- Longest Substring Without Repeating Characters
- Valid Parentheses
- Daily Temperatures
- Reverse Linked List
- Linked List Cycle
- Merge Two Sorted Lists
- Binary Search
- Number of Islands
- Climbing Stairs
- House Robber
- Jump Game

Each problem includes:

- Problem
- Approach
- Brute force
- Optimal solution
- Python code
- Complexity
- Edge cases
- Follow-up questions

______________________________________________________________________

# Phase 7 — System Design

### 38. System Design Fundamentals

[Open `38-system-design-fundamentals.md`](./38-system-design-fundamentals.md)

Covers:

- Requirements
- Functional requirements
- Non-functional requirements
- Capacity estimation
- Scalability
- Availability
- Reliability
- Latency
- Throughput
- Stateless services
- Load balancing
- Caching
- Databases
- Queues
- Workers
- Rate limiting
- Monitoring
- Retry
- Timeout
- Circuit breaker
- Idempotency
- CAP

______________________________________________________________________

### 39. Backend Architecture Building Blocks

[Open `39-system-design-building-blocks.md`](./39-system-design-building-blocks.md)

Covers:

- Load balancer
- Reverse proxy
- CDN
- API gateway
- Cache
- Database
- Read replicas
- Message queues
- Pub/Sub
- Object storage
- Search
- WebSockets
- Long polling
- Webhooks
- Service discovery
- Monolith vs microservices

______________________________________________________________________

### 40. Practical System Design

[Open `40-system-design-practice.md`](./40-system-design-practice.md)

Practical designs:

1. URL shortener
1. Notification service
1. File upload service
1. Rate limiter
1. Chat service

Each design covers:

- Requirements
- APIs
- Data model
- Architecture
- Scaling
- Bottlenecks
- Failure handling
- Trade-offs
- Interview Q&A

**Advanced distributed-system design is intentionally excluded.**

______________________________________________________________________

# Phase 8 — TypeScript, Angular & Data Libraries

### 41. TypeScript, Angular Overview

[Open `41-typescript-angular.md`](./41-typescript-angular.md)

This is deliberately an **overview file**, not a deep-dive.

## TypeScript

- Types
- Interfaces
- Classes
- Generics
- Promises
- Async/await
- TypeScript vs JavaScript

## Angular

- SPA
- Components
- Templates
- Data binding
- Directives
- Services
- Dependency injection
- Routing
- Forms
- HTTP client
- Observables
- RxJS overview
- Lifecycle hooks
- Pipes
- Guards
- Interceptors
- Authentication
- Angular + FastAPI
- CORS

The goal is interview-ready awareness, not data-science specialization.

______________________________________________________________________

### 42. NumPy & Pandas Overview

[Open `42-numpy-pandas.md`](./42-numpy-pandas.md)

This is deliberately an **overview file**, not a deep-dive.

## NumPy

- `ndarray`
- Shape
- Dimensions
- dtype
- Indexing
- Slicing
- Views vs copies
- Reshape
- Vectorization
- Broadcasting
- Aggregations
- Basic operations
- NumPy vs Python lists

## Pandas

- Series
- DataFrame
- Indexing
- Filtering
- Grouping
- Aggregation
- Merge/join
- Missing values
- Reading/writing data
- Pandas vs NumPy

The goal is interview-ready awareness, not data-science specialization.

______________________________________________________________________

# Phase 9 — Senior Engineering

### 43. Design Patterns & Architecture

[Open `43-design-patterns-architecture.md`](./43-design-patterns-architecture.md)

Covers:

- SOLID
- Dependency Injection
- Factory
- Strategy
- Observer
- Adapter
- Decorator
- Repository
- Facade
- CQRS overview
- Event-driven architecture
- Layered architecture
- Clean Architecture
- Hexagonal Architecture
- DDD fundamentals
- Outbox
- Circuit breaker
- Bulkhead

Focus:

> When should I use it, and what trade-off does it introduce?

______________________________________________________________________

### 44. Behavioral & HR Interview

[Open `44-behavioral.md`](./44-behavioral.md)

Covers:

- Tell me about yourself
- Strengths
- Weaknesses
- Leadership
- Ownership
- Conflict
- Teamwork
- Failure
- Feedback
- Pressure
- Prioritization
- Production incidents
- Career motivation
- Why change?
- Why this company?
- Compensation discussions
- STAR framework

______________________________________________________________________

### 45. Resume & Project Deep Dive

[Open `45-resume-projects.md`](./45-resume-projects.md)

Covers how to discuss projects at a senior level:

- Problem
- Architecture
- Your contribution
- Technical decisions
- Database
- APIs
- Cache
- Messaging
- Scaling
- Security
- Testing
- Deployment
- Monitoring
- Production issues
- Challenges
- Achievements
- Trade-offs
- What you would change today

______________________________________________________________________

### 46. AI-Assisted Software Engineering

[Open `46-ai-assisted-development.md`](./46-ai-assisted-development.md)

Covers:

- AI-assisted coding
- Debugging
- Refactoring
- Test generation
- Code review
- Documentation
- Repository understanding
- Prompting
- Verification
- Hallucinations
- Security
- Privacy
- Dependency risks
- Human ownership
- Practical AI-assisted backend workflow

______________________________________________________________________

# Phase 10 — Final Interview Preparation

### 47. Rapid-Fire Python Backend Q&A

[Open `47-rapid-fire-python-backend.md`](./47-rapid-fire-python-backend.md)

Consolidated high-value questions covering:

- Python
- Collections
- OOP
- Concurrency
- AsyncIO
- FastAPI
- HTTP
- SQL
- Normalization
- SQLAlchemy
- Redis
- Kafka
- RabbitMQ
- Celery
- Docker
- Linux
- Security
- Git
- DSA
- System Design

This is the **last-minute revision bank**.

______________________________________________________________________

### 48. Technical Mock Interview & Final Revision

[Open `48-technical-mock-interview-final-revision.md`](./48-technical-mock-interview-final-revision.md)

Contains:

- Python mock interview
- Backend mock interview
- SQL mock interview
- Redis/messaging questions
- Production-debugging scenarios
- DSA coding round
- System-design round
- Behavioral crossover questions
- Senior-level follow-ups
- Final revision checklist
- Interview-day strategy

______________________________________________________________________

# Four-Day Study Plan

## Day 1 — Python

### Primary files

**01–11**

Focus:

- Python internals
- Functions
- Decorators
- Iterators/generators
- Collections
- OOP
- Advanced OOP
- Concurrency
- AsyncIO
- Exceptions
- Typing
- Testing

### Priority

**Very High**

For a Python backend role, this is the foundation.

______________________________________________________________________

# Day 2 — Web + Database

### Primary files

**12–25**

Focus:

- HTTP
- Networking
- Complete request lifecycle
- FastAPI
- Flask
- SQL
- Normalization
- Advanced SQL
- Indexes
- Transactions
- SQLAlchemy
- Database performance
- Database scaling

### Priority

**Very High**

The goal is to confidently explain:

> Client → API → Application → ORM → Database

and everything that happens around it.

______________________________________________________________________

# Day 3 — Production Backend

### Primary files

**26–34**

Focus:

- Redis
- Caching
- Kafka
- RabbitMQ
- Celery
- Docker
- Linux
- Production debugging
- Security
- Git

### Also review

**41 — TypeScript, Angular, NumPy & Pandas Overview**

### Priority

**High**

The goal is to demonstrate production engineering breadth rather than only framework knowledge.

______________________________________________________________________

# Day 4 — Senior Interview

### Primary files

**35–47**

Focus:

- DSA
- System design
- Architecture
- Design patterns
- Angular/data overview revision
- Behavioral questions
- Resume/project deep dive
- AI-assisted development
- Rapid-fire Q&A
- Mock interview
- Final revision

### Priority

**Very High**

The goal is to convert knowledge into interview performance.

______________________________________________________________________

# Topic Priority

## Tier 1 — Must Know Very Well

- Python
- Python Collections
- OOP
- Concurrency
- AsyncIO
- HTTP
- FastAPI
- SQL
- Database normalization
- SQLAlchemy
- Redis
- Testing
- Production debugging
- Resume/projects
- Behavioral

## Tier 2 — Strong Working Knowledge

- Kafka
- RabbitMQ
- Celery
- Docker
- Linux
- Security
- Git
- System design
- Design patterns

## Tier 3 — Interview-Ready Overview

- Flask
- Database scaling
- Angular
- TypeScript
- NumPy
- Pandas
- AI-assisted development

______________________________________________________________________

# Navigation Convention

Every numbered file contains previous/next references at both the beginning and end.

For example:

```markdown
# 19. Database Design & Normalization

**Previous:** [16. SQL Fundamentals](./18-sql-fundamentals.md)  
**Next:** [18. Advanced SQL Queries](./20-sql-advanced.md)

---

## Objectives

...

## Topics

...

# Interview Questions & Answers

...

---

**Previous:** [16. SQL Fundamentals](./18-sql-fundamentals.md)  
**Next:** [18. Advanced SQL Queries](./20-sql-advanced.md)
```

The index is:

```text
00-index.md
```

The course then runs sequentially from:

```text
01 → 47
```

______________________________________________________________________

# Final File Count

| Section | Files |
|---|---:|
| Python Core | 01–11 = **11** |
| Web & Backend | 12–17 = **6** |
| SQL & Database | 18–25 = **8** |
| Redis & Messaging | 26–29 = **4** |
| Production Engineering | 30–34 = **5** |
| DSA | 35–37 = **3** |
| System Design | 38–40 = **3** |
| TypeScript/Angular/Data | 41 = **1** |
| Senior Engineering | 42–45 = **4** |
| Final Preparation | 46–47 = **2** |
| **Topic files** | **47** |
| **Index** | **1** |
| **Total** | **48 Markdown files** |

______________________________________________________________________

# Definition of Done

The course is complete only when:

- [ ] All 47 topic files are created.
- [ ] Every file has previous/next relative links.
- [ ] Every file has objectives.
- [ ] Every file has detailed topic content.
- [ ] Every file has a dedicated Q&A section.
- [ ] Every file has practical/scenario-based questions where relevant.
- [ ] Every file has a completion checklist.
- [ ] Python Collections is explicitly covered.
- [ ] Database normalization is explicitly covered.
- [ ] NumPy and Pandas are combined into one overview file.
- [ ] Angular and TypeScript are covered at overview level.
- [ ] AWS is excluded.
- [ ] Kubernetes is excluded.
- [ ] Advanced DSA is excluded.
- [ ] Advanced system design is excluded.
- [ ] The course remains suitable for a 3–4 day intensive preparation schedule.

______________________________________________________________________

# Start Here

**[01. Python Runtime, Objects, Memory & Scope →](./01-python-core.md)**
