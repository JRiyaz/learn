# File: roadmap.md

# Backend Engineering Roadmap
## Python Backend Engineer (Intermediate → Senior)

---

# Phase 1 - Advanced Python

## Module 1 - Python Object Model & Memory

- Memory Management & Object Model
- Reference Counting
- Garbage Collection
- Shallow Copy vs Deep Copy
- Mutable Default Arguments
- Small Integer Caching
- Interning
- LEGB Scope
- Closures
- Decorators
- First-Class Functions
- Higher-Order Functions
- Lambda Functions
- Iterators
- Iterator Protocol
- Generators
- Generator Expressions
- Context Managers
- Magic Methods (Dunder Methods)
- Dataclasses
- NamedTuple
- Enums

---

## Module 2 - Advanced OOP

- Inheritance
- Multiple Inheritance
- Method Resolution Order (MRO)
- Composition vs Inheritance
- Abstract Base Classes (ABC)
- Mixins
- Class Methods
- Static Methods
- Properties
- Descriptors
- __slots__
- __new__
- Metaclasses (Question Level)

---

## Module 3 - Functional Python

- map()
- filter()
- reduce()
- zip()
- enumerate()
- any()
- all()
- functools
- itertools
- collections module

---

## Module 4 - Built in types

- str
- int
- list
- set
- tuple
- dict

---

## Module 5 - Concurrency

- Processes vs Threads
- Threading
- Multiprocessing
- GIL
- Async Programming
- AsyncIO
- async
- await
- Event Loop
- Futures
- Coroutines
- asyncio.gather()
- asyncio.create_task()
Lesson 56 — Futures & Low-Level Asyncio
    asyncio.Future
    Relationship between Futures and Tasks
    loop.create_future()
    Callback-based APIs
    Bridging old and new async code
Lesson 57 — Async Generators & Async Iterators
    async for
    async with
    __aiter__
    __anext__
    Streaming large datasets
    Server-Sent Events (SSE)
Lesson 58 — Executors & Blocking Code
    run_in_executor()
    asyncio.to_thread()
    ThreadPoolExecutor
    ProcessPoolExecutor
    Integrating synchronous libraries
Lesson 59 — Async Context Managers & Resource Lifecycle
    __aenter__
    __aexit__
    Connection pools
    HTTP clients
    Database sessions
    Cleanup patterns
Lesson 60 — Structured Concurrency
    asyncio.TaskGroup
    Exception groups
    Python 3.11 improvements
    Why TaskGroup is preferred over raw create_task()
Lesson 61 — Debugging & Performance
    Debug mode
    Detecting blocking calls
    Slow callbacks
    Task inspection
    Profiling async applications
Lesson 62 — CPython Async Internals
    Coroutine objects
    Frame objects
    Awaitable protocol
    Bytecode (GET_AWAITABLE, SEND, etc.)
    Suspension and resumption
Lesson 63 — Event Loop Internals
    SelectorEventLoop
    ProactorEventLoop
    epoll
    kqueue
    IOCP
    Readiness notifications
    How Uvicorn drives the loop
Lesson 64 — Production Async Patterns
    Fan-out/fan-in
    Backpressure
    Worker pools
    Pipelines
    Rate limiting
    Circuit breakers
    Retries
    Graceful shutdown
Lesson 65 — Concurrency Capstone (A complete production-style backend project combining):
    FastAPI
    PostgreSQL
    Redis
    Background workers
    Async queues
    Timeouts
    Cancellation
    TaskGroups
    Semaphores
    Structured logging
    Production architecture review
---

## Module 6 - Production Python

- Logging
- Exception Handling
- Custom Exceptions
- Type Hinting
- Typing Module
- Pydantic
- Configuration Management
- Environment Variables
- Virtual Environments
- Packaging
- Project Structure
- Dependency Injection
- Profiling
- Memory Optimization

---

## Module 7 - Testing

- unittest
- pytest
- Fixtures
- Mocking
- Monkeypatch
- Coverage
- Integration Testing
- API Testing

---

## Module 8 – Computer Networking & Sockets

- Networking & TCP Sockets
- UDP Sockets
- Multi-Client TCP Server
- Non-Blocking Sockets & Selectors
- WebSockets

---

# Phase 2 - SQL

## Database Fundamentals

- ACID
- Transactions
- Normalization
- Constraints

## SQL Queries

- Joins
- Group By
- Having
- CTE
- Window Functions
- Subqueries
- Recursive Queries

## Performance

- Indexes
- Query Optimization
- Execution Plans
- Locking
- Deadlocks
- Isolation Levels
- Partitioning

---

# Phase 3 - Redis

- Redis Introduction
- Installation
- Redis CLI
- Data Types
- Strings
- Lists
- Sets
- Hashes
- Sorted Sets
- Streams
- Pub/Sub
- TTL
- Expiry
- Persistence
- Caching Strategies
- Session Management
- Rate Limiting
- Distributed Locking
- Redis in FastAPI
- Production Best Practices

---

# Phase 4 - Docker

- Docker Basics
- Images
- Containers
- Layers
- Volumes
- Networks
- Docker Compose
- Multi-stage Builds
- Environment Variables
- Health Checks
- Debugging Containers
- Docker Best Practices

---

# Phase 5 - Kafka

- Kafka Architecture
- Brokers
- Topics
- Partitions
- Producers
- Consumers
- Consumer Groups
- Offsets
- Delivery Guarantees
- Rebalancing
- Serialization
- Schema Registry (Overview)
- Dead Letter Queue
- Retry Strategies
- Event-Driven Architecture
- Kafka with FastAPI
- Kafka Best Practices

---

# Phase 6 - FastAPI Advanced

- Dependency Injection
- Middleware
- Background Tasks
- Lifespan Events
- Authentication
- Authorization
- JWT
- OAuth2
- File Uploads
- WebSockets
- Pagination
- Rate Limiting
- Caching
- Testing
- Project Structure

---

# Phase 7 - AWS

- Cloud Fundamentals
- IAM
- EC2
- VPC Basics
- Security Groups
- S3
- RDS
- CloudWatch
- ECS
- ECR
- Lambda
- API Gateway
- Secrets Manager
- Parameter Store
- Load Balancer
- Auto Scaling

---

# Phase 8 - CI/CD

- Git Advanced
- GitHub Actions
- GitLab CI
- Docker Deployment
- Automated Testing
- Versioning
- Release Management

---

# Phase 9 - System Design

## Fundamentals

- Scalability
- Availability
- Reliability
- CAP Theorem
- Load Balancing
- Caching
- Database Scaling

## Design Problems

- URL Shortener
- Chat Application
- Notification System
- Rate Limiter
- Payment System
- Order Management
- File Storage
- API Gateway
- Logging Service

---

# Phase 10 - Capstone Projects

## Project 1

Production Ready REST API

Technologies:

- FastAPI
- PostgreSQL
- Docker
- Redis
- JWT

---

## Project 2

E-commerce Backend

Technologies:

- FastAPI
- PostgreSQL
- Redis
- Kafka
- Docker
- Pytest

---

## Project 3

Microservices Backend

Technologies:

- FastAPI
- Kafka
- Redis
- Docker Compose
- PostgreSQL

---

## Project 4

Production Deployment

Technologies:

- AWS
- Docker
- GitHub Actions
- Nginx
- SSL
- Monitoring

---

# Final Preparation

- Python Questions
- SQL Questions
- Redis Questions
- Kafka Questions
- FastAPI Questions
- Docker Questions
- AWS Questions
- System Design Questions
- Mock Questions
- Resume Review
- GitHub Review
- LinkedIn Review
