# 43. Design Patterns & Architecture

**Previous:** [42. NumPy & Pandas Overview](./42-numpy-pandas.md)

**Next:** [44. Behavioral & HR Interview](./44-behavioral.md)

______________________________________________________________________

## Objective

This topic introduces commonly used software design patterns and backend architecture styles.

The focus is not on memorizing pattern definitions.

The key interview question is:

> **When should I use it, and what trade-off does it introduce?**

You should be able to recognize a pattern in an existing Python backend, explain why it is useful, identify when it is
unnecessary, and discuss the complexity it introduces.

______________________________________________________________________

# Part 1 — SOLID Principles

# 1. What Is SOLID?

SOLID is a collection of five object-oriented design principles:

```text
S → Single Responsibility Principle
O → Open/Closed Principle
L → Liskov Substitution Principle
I → Interface Segregation Principle
D → Dependency Inversion Principle
```

The goal is generally to make software:

```text
Easier to change
Easier to test
Easier to understand
Less tightly coupled
```

SOLID is guidance, not a set of absolute rules.

______________________________________________________________________

# 2. Single Responsibility Principle

A class or module should have a focused responsibility and a reason to change.

Poor example:

```python
class UserService:
    def create_user(self):
        ...

    def send_email(self):
        ...

    def generate_pdf_report(self):
        ...
```

These responsibilities may change independently.

A more focused design might separate:

```text
UserService
EmailService
ReportService
```

### When useful

Use SRP when responsibilities are becoming difficult to understand, test or change independently.

### Trade-off

Too much decomposition can create:

```text
Too many classes
More indirection
More files
Harder navigation
```

______________________________________________________________________

# 3. Open/Closed Principle

Software entities should generally be:

```text
Open for extension
Closed for modification
```

Suppose notification behavior keeps growing:

```python
if channel == "email":
    ...
elif channel == "sms":
    ...
elif channel == "push":
    ...
```

A strategy-based design could allow new channel implementations without repeatedly modifying the central logic.

### When useful

Useful when behavior is expected to grow through interchangeable implementations.

### Trade-off

Abstractions can make simple code unnecessarily complex.

______________________________________________________________________

# 4. Liskov Substitution Principle

A subtype should be usable wherever its base type is expected without breaking the program's expected behavior.

The important idea is:

```text
Inheritance should preserve behavioral expectations.
```

If a subclass violates assumptions made by callers, the inheritance relationship may be wrong.

### When useful

Useful when designing inheritance hierarchies and interfaces.

### Trade-off

Trying to force every class into an inheritance hierarchy can produce poor designs.

______________________________________________________________________

# 5. Interface Segregation Principle

Clients should not be forced to depend on methods they do not need.

Instead of:

```python
class Worker:
    def read(self): ...
    def write(self): ...
    def delete(self): ...
    def reboot(self): ...
```

different consumers may need smaller interfaces.

Conceptually:

```text
Readable
Writable
Deletable
```

### When useful

Useful when interfaces become large and different consumers use only subsets.

### Trade-off

Too many tiny interfaces can make the design fragmented.

______________________________________________________________________

# 6. Dependency Inversion Principle

High-level code should depend on abstractions rather than tightly coupling itself to concrete implementations.

Instead of:

```python
class OrderService:
    def __init__(self):
        self.repository = PostgresOrderRepository()
```

you can inject the dependency:

```python
class OrderService:
    def __init__(self, repository):
        self.repository = repository
```

Now the service can work with different implementations.

### When useful

Especially useful for:

```text
Testing
Swappable implementations
Infrastructure boundaries
Large applications
```

### Trade-off

Dependency abstractions introduce more types and indirection.

______________________________________________________________________

# 7. SOLID in Practice

The principles work together.

A backend might look like:

```text
API
 ↓
Service
 ↓
Repository interface
 ↓
Postgres repository
```

Testing can replace:

```text
Postgres repository
```

with:

```text
Fake repository
```

This is one practical application of dependency inversion and dependency injection.

______________________________________________________________________

# Part 2 — Dependency Injection

# 8. What Is Dependency Injection?

Dependency Injection means a component receives dependencies instead of constructing them internally.

Without DI:

```python
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()
```

With DI:

```python
class OrderService:
    def __init__(self, db):
        self.db = db
```

The caller controls the dependency.

______________________________________________________________________

# 9. Why Use Dependency Injection?

DI can provide:

```text
Loose coupling
Testability
Configuration flexibility
Replaceable implementations
```

Example:

```text
Production
→ RealPaymentGateway

Test
→ FakePaymentGateway
```

______________________________________________________________________

# 10. Dependency Injection in FastAPI

FastAPI has a dependency-injection mechanism.

Example:

```python
from fastapi import Depends

def get_service():
    return OrderService()

@app.get("/orders")
def get_orders(
    service: OrderService = Depends(get_service)
):
    return service.list_orders()
```

The framework resolves the dependency.

______________________________________________________________________

# 11. DI Trade-Off

DI is valuable, but do not inject everything simply because you can.

Excessive DI can produce:

```text
Complex constructors
Many abstractions
Hard-to-follow object graphs
Overengineering
```

Use it where dependency boundaries provide real value.

______________________________________________________________________

# Part 3 — Factory Pattern

# 12. Factory

A Factory centralizes creation of objects.

Example:

```python
def create_storage(storage_type):
    if storage_type == "postgres":
        return PostgresStorage()
    if storage_type == "redis":
        return RedisStorage()

    raise ValueError("Unsupported storage")
```

Callers do not need to know how each implementation is constructed.

______________________________________________________________________

# 13. When to Use Factory

Use a Factory when:

```text
Object creation is complex
Multiple implementations exist
Creation logic should be centralized
Construction depends on configuration/input
```

______________________________________________________________________

# 14. Factory Trade-Off

Factory introduces:

```text
An additional abstraction
Centralized branching
More indirection
```

For two simple constructors, a Factory may be unnecessary.

______________________________________________________________________

# Part 4 — Strategy Pattern

# 15. Strategy

Strategy encapsulates interchangeable algorithms or behaviors.

Example:

```python
class PaymentStrategy:
    def pay(self, amount):
        raise NotImplementedError
```

Implementations:

```text
CardPayment
UPIPayment
WalletPayment
```

The service selects the appropriate strategy.

______________________________________________________________________

# 16. Strategy Example

```python
class CheckoutService:
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def checkout(self, amount):
        return self.payment_strategy.pay(amount)
```

Now the checkout logic does not need to know the details of each payment method.

______________________________________________________________________

# 17. When to Use Strategy

Use Strategy when:

```text
Several algorithms solve the same problem
Behavior varies at runtime
Conditional branching keeps growing
Algorithms should be independently testable
```

______________________________________________________________________

# 18. Strategy Trade-Off

Trade-offs include:

```text
More classes
More abstraction
Selection logic
Indirection
```

If there are only two trivial branches, a simple conditional may be clearer.

______________________________________________________________________

# Part 5 — Observer Pattern

# 19. Observer

Observer allows one object/event source to notify multiple interested consumers.

Conceptually:

```text
Event
 ├── Listener A
 ├── Listener B
 └── Listener C
```

Backend examples:

```text
OrderCreated
 ↓
Email handler
Analytics handler
Inventory handler
```

______________________________________________________________________

# 20. Observer and Event-Driven Systems

A message broker can provide a distributed form of this idea:

```text
Producer
   ↓
Event
   ↓
Broker
 ├── Consumer A
 ├── Consumer B
 └── Consumer C
```

This reduces direct coupling between producers and consumers.

______________________________________________________________________

# 21. When to Use Observer

Useful when:

```text
One event has multiple consumers
Consumers should be loosely coupled
New consumers may be added independently
```

______________________________________________________________________

# 22. Observer Trade-Off

It introduces:

```text
Indirect control flow
Debugging complexity
Event ordering concerns
Failure-handling complexity
Potential eventual consistency
```

The caller may no longer know immediately what downstream work happens.

______________________________________________________________________

# Part 6 — Adapter Pattern

# 23. Adapter

An Adapter converts one interface into another interface expected by the application.

Suppose the application expects:

```python
payment.charge(amount)
```

but a third-party provider exposes:

```python
provider.create_payment(value)
```

An adapter can translate between them.

______________________________________________________________________

# 24. Adapter Example

```python
class PaymentAdapter:
    def __init__(self, provider):
        self.provider = provider

    def charge(self, amount):
        return self.provider.create_payment(amount)
```

The rest of the application depends on the application's interface rather than the provider's API.

______________________________________________________________________

# 25. When to Use Adapter

Useful for:

```text
Third-party integrations
Legacy systems
Replacing providers
Normalizing inconsistent APIs
```

______________________________________________________________________

# 26. Adapter Trade-Off

Trade-offs:

```text
Additional layer
Mapping code
Potential abstraction leakage
```

The adapter is worthwhile when it isolates an external interface that would otherwise spread throughout the application.

______________________________________________________________________

# Part 7 — Decorator Pattern

# 27. Decorator

A Decorator adds behavior around an existing object/function without changing its core implementation.

Example:

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print("calling")
        result = func(*args, **kwargs)
        print("finished")
        return result

    return wrapper
```

Usage:

```python
@log_call
def process():
    ...
```

______________________________________________________________________

# 28. Backend Uses of Decorators

Decorators are commonly used for:

```text
Logging
Authorization
Caching
Metrics
Retries
Validation
Tracing
```

Frameworks often use decorators to declare behavior.

______________________________________________________________________

# 29. When to Use Decorator

Use when:

```text
Cross-cutting behavior should wrap existing behavior
Multiple functions need the same wrapper
Behavior should be composable
```

______________________________________________________________________

# 30. Decorator Trade-Off

Too many decorators can make execution flow difficult to understand.

Example:

```python
@auth
@retry
@cache
@metrics
@trace
def operation():
    ...
```

The behavior is powerful but less obvious.

______________________________________________________________________

# Part 8 — Repository Pattern

# 31. Repository

A Repository abstracts access to persistent data.

Instead of service code directly constructing SQL queries:

```python
class UserService:
    def get_user(self, user_id):
        ...
```

the service can depend on:

```python
class UserRepository:
    def get_by_id(self, user_id):
        ...
```

Implementation:

```text
UserRepository
      ↓
SQLAlchemy
      ↓
PostgreSQL
```

______________________________________________________________________

# 32. Repository Example

```python
class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id):
        return (
            self.session.query(User)
            .filter(User.id == user_id)
            .first()
        )
```

The service focuses on business logic:

```python
class UserService:
    def __init__(self, repository):
        self.repository = repository

    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)
```

______________________________________________________________________

# 33. When to Use Repository

Useful when:

```text
Persistence logic is complex
Multiple persistence implementations exist
Business logic should be separated from storage details
Testing benefits from an abstraction
```

______________________________________________________________________

# 34. Repository Trade-Off

A Repository can become an unnecessary abstraction over an ORM.

For a small CRUD application:

```text
Service
→ SQLAlchemy
```

may be simpler.

Do not create a repository layer only because it is a pattern.

______________________________________________________________________

# Part 9 — Facade Pattern

# 35. Facade

A Facade provides a simpler interface over a complex subsystem.

Suppose checkout requires:

```text
Inventory
Payment
Order
Shipping
Notification
```

Instead of exposing all of these to the API:

```text
CheckoutFacade
```

can provide:

```python
checkout(order)
```

______________________________________________________________________

# 36. Facade Example

```text
API
 ↓
CheckoutFacade
 ├── InventoryService
 ├── PaymentService
 ├── OrderService
 ├── ShippingService
 └── NotificationService
```

The caller sees one simple interface.

______________________________________________________________________

# 37. When to Use Facade

Useful when:

```text
Subsystem is complicated
Callers need only a common workflow
You want to hide implementation details
```

______________________________________________________________________

# 38. Facade Trade-Off

A badly designed Facade can become a:

```text
God object
```

containing too much business logic.

The Facade should coordinate rather than become an enormous catch-all service.

______________________________________________________________________

# Part 10 — CQRS Overview

# 39. What Is CQRS?

CQRS means:

> **Command Query Responsibility Segregation**

The basic idea is to separate:

```text
Commands
→ change state

Queries
→ read state
```

Conceptually:

```text
              Application
              /         \
        Commands       Queries
           ↓              ↓
      Write Model     Read Model
```

______________________________________________________________________

# 40. Why CQRS?

CQRS can be useful when:

```text
Read and write workloads differ substantially
Read models need different structures
Complex domain behavior exists
Independent scaling is valuable
```

______________________________________________________________________

# 41. CQRS Trade-Off

CQRS introduces complexity:

```text
Multiple models
Synchronization
Eventual consistency
More infrastructure
More operational work
```

Do not introduce CQRS for a simple CRUD application.

______________________________________________________________________

# Part 11 — Event-Driven Architecture

# 42. Event-Driven Architecture

In an event-driven architecture, components communicate through events.

Example:

```text
Order Service
     ↓
OrderCreated
     ↓
Event Broker
 ├── Inventory
 ├── Notification
 └── Analytics
```

The producer does not need direct synchronous calls to every consumer.

______________________________________________________________________

# 43. Events vs Commands

A useful distinction:

### Command

```text
"Do this."
```

Example:

```text
CreateOrder
```

### Event

```text
"This happened."
```

Example:

```text
OrderCreated
```

Events generally describe facts that have already occurred.

______________________________________________________________________

# 44. When to Use Event-Driven Architecture

Useful when:

```text
Services need loose coupling
Multiple consumers react to events
Asynchronous processing is useful
Systems need independent scaling
```

______________________________________________________________________

# 45. Event-Driven Trade-Off

Costs include:

```text
Eventual consistency
Harder debugging
Ordering concerns
Duplicate delivery
Schema evolution
Operational complexity
```

A synchronous call can be easier when immediate consistency and simple control flow are required.

______________________________________________________________________

# Part 12 — Layered Architecture

# 46. Layered Architecture

A common backend structure:

```text
API / Presentation
        ↓
Application / Service
        ↓
Domain
        ↓
Infrastructure / Data
```

For example:

```text
FastAPI endpoint
      ↓
OrderService
      ↓
Order domain logic
      ↓
Repository
      ↓
SQLAlchemy
      ↓
PostgreSQL
```

______________________________________________________________________

# 47. Why Layered Architecture?

Benefits:

```text
Separation of concerns
Clear responsibilities
Easier testing
Predictable project structure
```

______________________________________________________________________

# 48. Layered Architecture Trade-Off

Too many layers can create:

```text
Boilerplate
Mapping code
Indirection
Slow development
```

A small application may not need five layers for every CRUD operation.

______________________________________________________________________

# Part 13 — Clean Architecture

# 49. Clean Architecture

Clean Architecture emphasizes dependency direction.

A simplified model:

```text
Frameworks / Infrastructure
          ↓
Interface Adapters
          ↓
Application / Use Cases
          ↓
Domain
```

The central business rules should not depend heavily on external infrastructure.

______________________________________________________________________

# 50. Dependency Direction

The important idea is:

```text
Outer layers
     ↓
Inner layers
```

Infrastructure depends on application/domain abstractions rather than the core business logic becoming tightly coupled
to infrastructure.

______________________________________________________________________

# 51. When to Use Clean Architecture

Useful for:

```text
Large applications
Long-lived systems
Complex business rules
Teams needing strong boundaries
Systems with replaceable infrastructure
```

______________________________________________________________________

# 52. Clean Architecture Trade-Off

It can introduce:

```text
Many abstractions
More files
More interfaces
More mapping
More upfront design
```

For simple CRUD systems, this may be unnecessary.

______________________________________________________________________

# Part 14 — Hexagonal Architecture

# 53. Hexagonal Architecture

Also called:

> **Ports and Adapters**

The core application communicates through ports.

```text
             Database Adapter
                    ↓
External API → [ Application ] ← Message Adapter
                    ↑
              CLI / HTTP Adapter
```

The core does not need to know the concrete infrastructure implementation.

______________________________________________________________________

# 54. Ports

A port defines what the application needs.

Example:

```python
class PaymentGateway(Protocol):
    def charge(self, amount: int):
        ...
```

Adapters implement that port:

```text
StripeAdapter
MockPaymentAdapter
AnotherProviderAdapter
```

______________________________________________________________________

# 55. When to Use Hexagonal Architecture

Useful when:

```text
External integrations are numerous
Infrastructure changes are expected
Testability is important
Domain logic should be isolated
```

______________________________________________________________________

# 56. Hexagonal Trade-Off

Similar to Clean Architecture:

```text
More abstractions
More interfaces
More indirection
More initial complexity
```

The benefit is stronger isolation from infrastructure.

______________________________________________________________________

# Part 15 — DDD Fundamentals

# 57. What Is Domain-Driven Design?

DDD focuses software design around the business domain.

Important concepts include:

```text
Domain
Entity
Value Object
Aggregate
Repository
Domain Service
Bounded Context
Ubiquitous Language
```

This file provides only the fundamentals.

______________________________________________________________________

# 58. Entity

An Entity is an object whose identity matters.

Example:

```text
User
Order
Invoice
```

Two Orders may have identical data but still represent different entities because their identities differ.

______________________________________________________________________

# 59. Value Object

A Value Object is generally defined by its value rather than identity.

Examples:

```text
Money
EmailAddress
Address
DateRange
```

For example:

```text
Money(100, "USD")
```

can be compared by value.

______________________________________________________________________

# 60. Aggregate

An Aggregate is a consistency boundary around related domain objects.

It has an:

```text
Aggregate Root
```

External code generally interacts with the root rather than directly modifying every internal object.

Example:

```text
Order
 ├── OrderItem
 ├── OrderItem
 └── ShippingAddress
```

`Order` may be the aggregate root.

______________________________________________________________________

# 61. Bounded Context

A Bounded Context defines a boundary within which domain terminology and models have a specific meaning.

For example:

```text
Sales Context
→ Customer
→ Order

Shipping Context
→ Customer
→ Shipment
```

The same word can represent different concepts in different contexts.

______________________________________________________________________

# 62. Ubiquitous Language

DDD encourages a shared language between:

```text
Developers
Product owners
Domain experts
```

If the business calls something:

```text
Subscription
```

the code should ideally use the same meaningful terminology where appropriate.

______________________________________________________________________

# 63. When Is DDD Useful?

DDD is particularly useful when:

```text
Business rules are complex
Domain concepts are important
Multiple teams work on a large system
Business terminology must be modeled carefully
```

______________________________________________________________________

# 64. DDD Trade-Off

DDD can be excessive for:

```text
Simple CRUD
Small internal tools
Very simple domains
```

It can introduce substantial modeling and organizational complexity.

______________________________________________________________________

# Part 16 — Outbox Pattern

# 65. The Distributed Transaction Problem

Suppose an order service needs to:

```text
1. Save order to database
2. Publish OrderCreated event
```

What if:

```text
Database commit succeeds
Event publishing fails
```

Now the order exists but consumers never receive the event.

______________________________________________________________________

# 66. Outbox Pattern

Store the event in the same database transaction:

```text
Transaction
 ├── Save Order
 └── Save Outbox Event
        ↓
      COMMIT
```

A separate publisher reads the outbox:

```text
Outbox
 ↓
Publisher
 ↓
Broker
```

______________________________________________________________________

# 67. Why Outbox Works

The order and event are committed atomically in the same database.

Either both are persisted:

```text
Order ✓
Outbox Event ✓
```

or neither is.

The event can then be published asynchronously.

______________________________________________________________________

# 68. Outbox Trade-Off

Outbox introduces:

```text
Extra table
Publisher process
Duplicate publishing concerns
Cleanup
Monitoring
Eventual delivery
```

Consumers should still be idempotent because publishing can be retried.

______________________________________________________________________

# Part 17 — Circuit Breaker

# 69. Circuit Breaker

A Circuit Breaker prevents repeated calls to an unhealthy dependency.

Typical states:

```text
CLOSED
   ↓ failures
OPEN
   ↓ timeout
HALF-OPEN
   ↓ test succeeds
CLOSED
```

______________________________________________________________________

# 70. Why Circuit Breakers?

Without a circuit breaker:

```text
Application
 ↓
Failing dependency
 ↓
Timeout
 ↓
Retry
 ↓
Timeout
 ↓
Retry
```

This can consume application resources and amplify an outage.

A circuit breaker can fail fast after a threshold is reached.

______________________________________________________________________

# 71. When to Use Circuit Breaker

Useful for:

```text
Remote services
External APIs
Unreliable dependencies
Expensive network calls
```

______________________________________________________________________

# 72. Circuit Breaker Trade-Off

It introduces:

```text
State management
Configuration complexity
Failure-mode complexity
Possible false positives
```

A poorly configured breaker can reject healthy traffic.

______________________________________________________________________

# Part 18 — Bulkhead Pattern

# 73. Bulkhead

The Bulkhead pattern isolates resources so that failure in one workload does not consume everything.

Conceptually:

```text
Application
 ├── Pool A → Payment calls
 ├── Pool B → Search calls
 └── Pool C → Notifications
```

If Search becomes slow, it should not consume every connection/thread/task needed by Payment.

______________________________________________________________________

# 74. Bulkhead Example

Without isolation:

```text
All requests
    ↓
One shared worker pool
    ↓
Slow dependency
    ↓
Pool exhausted
    ↓
Everything affected
```

With isolation:

```text
Payment → Pool A
Search  → Pool B
Email   → Pool C
```

A failure can be contained.

______________________________________________________________________

# 75. When to Use Bulkhead

Useful when:

```text
Multiple independent workloads share resources
One dependency can become slow
Resource exhaustion could cascade
Availability isolation matters
```

______________________________________________________________________

# 76. Bulkhead Trade-Off

Isolation requires:

```text
More resource pools
More configuration
Potential underutilization
More operational complexity
```

You are trading efficiency for resilience.

______________________________________________________________________

# Part 19 — Choosing the Right Pattern

Do not choose a pattern because it appears in an interview checklist.

Start with the problem.

| Problem | Possible Pattern |
|---|---|
| Complex object creation | Factory |
| Interchangeable algorithms | Strategy |
| One event, many consumers | Observer/Event-driven |
| Third-party API mismatch | Adapter |
| Add cross-cutting behavior | Decorator |
| Isolate persistence | Repository |
| Simplify complex subsystem | Facade |
| Separate read/write models | CQRS |
| Complex event-based integration | Event-driven |
| Organize application layers | Layered |
| Isolate business rules | Clean Architecture |
| Isolate core from infrastructure | Hexagonal |
| Complex business domain | DDD |
| DB update + event publishing | Outbox |
| Failing remote dependency | Circuit Breaker |
| Prevent resource exhaustion | Bulkhead |

______________________________________________________________________

# 77. Pattern vs Architecture

A useful distinction:

### Design Pattern

Usually solves a more focused design problem.

Examples:

```text
Factory
Strategy
Adapter
Decorator
Repository
Facade
```

### Architecture

Defines larger system organization and boundaries.

Examples:

```text
Layered Architecture
Clean Architecture
Hexagonal Architecture
Event-Driven Architecture
```

______________________________________________________________________

# 78. Patterns Can Be Combined

Real systems often use several patterns.

Example:

```text
FastAPI
 ↓
Facade
 ↓
Service
 ↓
Repository
 ↓
Database
```

Dependency Injection can connect them:

```text
DI
 ↓
Facade
 ↓
Service
 ↓
Repository
```

An external payment integration might use:

```text
Port
 ↓
Payment Adapter
 ↓
External Provider
```

An asynchronous notification workflow might use:

```text
Event
 ↓
Queue
 ↓
Worker
 ↓
Strategy
```

Patterns are building blocks, not mutually exclusive choices.

______________________________________________________________________

# 79. Avoid Pattern Overuse

Consider:

```python
class UserFactory:
    def create_user_repository_strategy_factory(self):
        ...
```

If the underlying problem is:

```python
users = repository.get_users()
```

the abstraction may be hurting more than helping.

A good design question is:

> **What problem does this abstraction solve?**

If the answer is unclear, reconsider it.

______________________________________________________________________

# 80. Practical Architecture Example

A production backend could combine several concepts:

```text
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Service    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Repository   │
                    └──────┬───────┘
                           ↓
                       Database

Service
  ↓
Event
  ↓
Queue/Broker
  ↓
Worker
  ↓
External Provider
```

Possible supporting patterns:

```text
Dependency Injection
Adapter
Strategy
Decorator
Outbox
Circuit Breaker
Bulkhead
```

The exact selection should come from requirements.

______________________________________________________________________

# 81. Architecture Trade-Off Matrix

| Approach | Main Benefit | Main Cost |
|---|---|---|
| Simple layered | Easy to understand | Can become rigid |
| Clean Architecture | Strong dependency boundaries | More boilerplate |
| Hexagonal | Infrastructure isolation | More abstractions |
| Event-driven | Loose coupling | Eventual consistency |
| CQRS | Independent read/write models | Significant complexity |
| DDD | Strong domain modeling | High modeling cost |

______________________________________________________________________

# 82. How to Choose an Architecture

Ask:

```text
1. How complex is the business domain?
2. How large is the application?
3. How many teams work on it?
4. How frequently will requirements change?
5. Are infrastructure implementations likely to change?
6. Is eventual consistency acceptable?
7. Do read and write workloads differ?
8. Are external integrations numerous?
9. What level of operational complexity can the team support?
```

Then choose the simplest architecture that satisfies the requirements.

______________________________________________________________________

# 83. Interview Questions & Answers

## Q1. What is SOLID?

**Answer:**

SOLID is a group of five object-oriented design principles intended to improve maintainability, flexibility, testability
and separation of responsibilities.

______________________________________________________________________

## Q2. What is Single Responsibility Principle?

**Answer:**

A component should have a focused responsibility and a clear reason to change. The goal is to avoid combining unrelated
responsibilities in one component.

______________________________________________________________________

## Q3. What is Dependency Inversion?

**Answer:**

High-level business logic should not be tightly coupled to low-level implementation details. Both should depend on
appropriate abstractions.

______________________________________________________________________

## Q4. What is Dependency Injection?

**Answer:**

Dependency Injection supplies a component's dependencies from outside rather than having the component construct those
dependencies itself.

______________________________________________________________________

## Q5. Dependency Inversion vs Dependency Injection?

**Answer:**

Dependency Inversion is a design principle about dependency direction. Dependency Injection is a technique for supplying
dependencies from outside the component.

______________________________________________________________________

## Q6. When would you use Factory?

**Answer:**

When object creation is complex, varies based on configuration/input, or multiple implementations need centralized
construction logic.

______________________________________________________________________

## Q7. When would you use Strategy?

**Answer:**

When multiple interchangeable algorithms or behaviors solve the same problem and the implementation may vary at runtime.

______________________________________________________________________

## Q8. Strategy vs Factory?

**Answer:**

A Factory focuses primarily on **creating/selecting an object**. Strategy focuses on **encapsulating interchangeable
behavior**. They can be used together.

______________________________________________________________________

## Q9. When would you use Observer?

**Answer:**

When one event or state change needs to notify multiple independent consumers without tightly coupling the producer to
each consumer.

______________________________________________________________________

## Q10. What is an Adapter?

**Answer:**

An Adapter translates one interface into another interface expected by the application. It is especially useful for
third-party and legacy integrations.

______________________________________________________________________

## Q11. What is a Decorator?

**Answer:**

A Decorator wraps an existing component or function to add behavior without modifying its core implementation.

______________________________________________________________________

## Q12. What is the Repository pattern?

**Answer:**

Repository abstracts persistence access so application/business logic does not need to directly depend on storage
implementation details.

______________________________________________________________________

## Q13. Should every FastAPI application use Repository?

**Answer:**

No. For simple CRUD applications, adding a repository layer can create unnecessary abstraction. Use it when persistence
complexity or a meaningful boundary justifies it.

______________________________________________________________________

## Q14. What is a Facade?

**Answer:**

A Facade provides a simpler interface over a complex subsystem and coordinates multiple underlying components.

______________________________________________________________________

## Q15. What is CQRS?

**Answer:**

CQRS separates command operations that change state from query operations that read state. This can allow independent
models and scaling but introduces additional complexity.

______________________________________________________________________

## Q16. What is Event-Driven Architecture?

**Answer:**

It is an architecture in which components communicate through events, often asynchronously, allowing producers and
consumers to be more loosely coupled.

______________________________________________________________________

## Q17. Command vs Event?

**Answer:**

A command asks a system to perform an action. An event communicates that something has already happened.

______________________________________________________________________

## Q18. What is Layered Architecture?

**Answer:**

It organizes an application into layers with defined responsibilities, such as API, application/service, domain and
infrastructure.

______________________________________________________________________

## Q19. What is Clean Architecture?

**Answer:**

Clean Architecture organizes the system so core business rules remain relatively independent from frameworks and
infrastructure, with dependency direction toward the core.

______________________________________________________________________

## Q20. What is Hexagonal Architecture?

**Answer:**

Hexagonal Architecture, or Ports and Adapters, isolates the application core behind ports while external systems
interact through adapters.

______________________________________________________________________

## Q21. Clean Architecture vs Hexagonal Architecture?

**Answer:**

Both aim to isolate core business logic from infrastructure and control dependency direction. They use different
terminology and organizational models, but their goals overlap significantly.

______________________________________________________________________

## Q22. What is DDD?

**Answer:**

Domain-Driven Design is an approach that models software around important business concepts and domain behavior, using
concepts such as entities, value objects, aggregates and bounded contexts.

______________________________________________________________________

## Q23. What is an Aggregate?

**Answer:**

An Aggregate is a consistency boundary around related domain objects, accessed through an Aggregate Root.

______________________________________________________________________

## Q24. What is a Bounded Context?

**Answer:**

A Bounded Context is a boundary within which domain terminology and models have a specific meaning. Different contexts
can model the same real-world concept differently.

______________________________________________________________________

## Q25. When should you use DDD?

**Answer:**

DDD is most valuable when the business domain contains significant complexity and business rules are central to the
application's design.

______________________________________________________________________

## Q26. What problem does the Outbox pattern solve?

**Answer:**

It addresses the reliability problem of updating a database and publishing an event as separate operations. The business
change and outbox event are stored in the same database transaction, after which a publisher sends the event.

______________________________________________________________________

## Q27. Does Outbox provide exactly-once delivery?

**Answer:**

Not by itself. The event publisher can retry and potentially publish duplicates, so consumers should generally be
designed to handle duplicate delivery idempotently.

______________________________________________________________________

## Q28. What is a Circuit Breaker?

**Answer:**

A Circuit Breaker prevents repeated calls to a failing dependency by temporarily stopping calls and allowing controlled
recovery checks.

______________________________________________________________________

## Q29. What are the Circuit Breaker states?

**Answer:**

Common states are:

```text
Closed
Open
Half-open
```

Closed allows normal calls, Open fails fast, and Half-open tests whether the dependency has recovered.

______________________________________________________________________

## Q30. What is the Bulkhead pattern?

**Answer:**

Bulkhead isolates resources or workloads so that failure or saturation in one area does not consume resources needed by
other areas.

______________________________________________________________________

## Q31. Circuit Breaker vs Bulkhead?

**Answer:**

Circuit Breaker primarily controls calls to an unhealthy dependency. Bulkhead isolates resources so one workload cannot
exhaust resources needed by another.

______________________________________________________________________

## Q32. Why shouldn't you use every design pattern?

**Answer:**

Every abstraction introduces complexity. Patterns should solve real problems rather than be added simply because they
are considered best practices.

______________________________________________________________________

## Q33. What is the most important question when choosing a pattern?

**Answer:**

Ask:

> **What problem does this pattern solve, and is that problem significant enough to justify the complexity it introduces?**

______________________________________________________________________

# 84. Scenario-Based Interview Q&A

## Scenario 1 — Third-Party Payment Provider

You have:

```text
Application
 ↓
Stripe
```

You may later replace Stripe with another provider.

### What pattern?

**Answer:**

An Adapter is a strong candidate.

```text
Application
 ↓
Payment interface
 ↓
Stripe Adapter
 ↓
Stripe
```

The application is isolated from provider-specific APIs.

______________________________________________________________________

## Scenario 2 — Multiple Payment Algorithms

The application supports:

```text
Credit Card
UPI
Wallet
```

and the checkout process should work with any payment implementation.

### What pattern?

**Answer:**

Strategy is appropriate because the payment behavior is interchangeable.

______________________________________________________________________

## Scenario 3 — One Event, Many Consumers

When an order is created:

```text
Inventory
Notification
Analytics
```

all need to react.

### What pattern?

**Answer:**

Observer/event-driven architecture is appropriate.

For distributed systems, a message broker can implement the event distribution.

______________________________________________________________________

## Scenario 4 — Database + Event

You need:

```text
Save Order
Publish OrderCreated
```

and cannot tolerate losing the event after the database commits.

### What pattern?

**Answer:**

Use the Outbox pattern.

______________________________________________________________________

## Scenario 5 — External API Is Unhealthy

A payment provider is timing out repeatedly.

### What pattern?

**Answer:**

A Circuit Breaker can prevent the application from repeatedly waiting on an unhealthy dependency.

Timeouts and bounded retries should still be used appropriately.

______________________________________________________________________

## Scenario 6 — Search Is Consuming All Workers

Search requests are slow and consume the shared worker pool, affecting payment requests.

### What pattern?

**Answer:**

A Bulkhead approach can isolate search resources from payment resources.

______________________________________________________________________

## Scenario 7 — Very Complex Business Domain

The system has:

```text
Complex pricing
Contracts
Subscriptions
Billing rules
Entitlements
Multiple business teams
```

### What approach?

**Answer:**

DDD may be appropriate because domain modeling and business rules are central to the system.

______________________________________________________________________

## Scenario 8 — Simple CRUD API

The application has:

```text
10 endpoints
Simple CRUD
Few business rules
One database
```

### Should you introduce Clean Architecture + CQRS + DDD?

**Answer:**

Probably not. Start with a simpler architecture. Add complexity when requirements justify it.

______________________________________________________________________

# 85. Pattern Selection Cheat Sheet

```text
Need object creation?
→ Factory

Need interchangeable behavior?
→ Strategy

Need notification of events?
→ Observer

Need to integrate incompatible API?
→ Adapter

Need cross-cutting behavior?
→ Decorator

Need persistence abstraction?
→ Repository

Need to simplify a subsystem?
→ Facade

Need separate read/write models?
→ CQRS

Need asynchronous event communication?
→ Event-driven architecture

Need clear application layers?
→ Layered Architecture

Need strong business/infrastructure separation?
→ Clean Architecture

Need ports/adapters around a core?
→ Hexagonal Architecture

Need complex domain modeling?
→ DDD

Need reliable DB + event publishing?
→ Outbox

Need protection from failing dependencies?
→ Circuit Breaker

Need resource isolation?
→ Bulkhead
```

______________________________________________________________________

# 86. Final Interview Readiness Checklist

## SOLID

- [ ] Explain all five SOLID principles.
- [ ] Give a practical example for each.
- [ ] Explain the trade-off of overapplying SOLID.
- [ ] Explain Dependency Inversion vs Dependency Injection.

## Design Patterns

- [ ] Factory
- [ ] Strategy
- [ ] Observer
- [ ] Adapter
- [ ] Decorator
- [ ] Repository
- [ ] Facade

For each:

- [ ] Explain the problem.
- [ ] Explain when to use it.
- [ ] Give a backend example.
- [ ] Explain the trade-off.
- [ ] Explain when not to use it.

## Architecture

- [ ] Explain CQRS.
- [ ] Explain event-driven architecture.
- [ ] Explain layered architecture.
- [ ] Explain Clean Architecture.
- [ ] Explain Hexagonal Architecture.
- [ ] Compare Clean and Hexagonal.
- [ ] Explain DDD fundamentals.
- [ ] Explain Entity.
- [ ] Explain Value Object.
- [ ] Explain Aggregate.
- [ ] Explain Bounded Context.
- [ ] Explain Ubiquitous Language.
- [ ] Explain Outbox.
- [ ] Explain Circuit Breaker.
- [ ] Explain Bulkhead.

## Interview Reasoning

- [ ] Start with the problem rather than the pattern.
- [ ] Explain why the pattern is needed.
- [ ] Explain the complexity introduced.
- [ ] Identify simpler alternatives.
- [ ] Discuss failure modes.
- [ ] Discuss operational implications.
- [ ] Avoid overengineering.

______________________________________________________________________

# 87. Final Takeaways

The most important lesson is:

> **Design patterns are tools, not requirements.**

A good engineer does not ask:

> "Which pattern can I use?"

A better question is:

> **"What problem am I solving, and what is the simplest design that solves it well?"**

Keep this mental model:

```text
Problem
 ↓
Constraints
 ↓
Simple design
 ↓
Identify pressure points
 ↓
Introduce abstraction/pattern where justified
 ↓
Measure the resulting complexity
```

Remember the core trade-off:

```text
More abstraction
      ↓
More flexibility
      +
More complexity
```

For example:

```text
Repository
→ isolates persistence
→ but may duplicate a thin ORM abstraction

CQRS
→ separates read/write concerns
→ but introduces multiple models and consistency complexity

Event-driven
→ reduces direct coupling
→ but introduces eventual consistency and harder debugging

Clean/Hexagonal
→ protects the domain from infrastructure
→ but adds interfaces and indirection

Circuit Breaker
→ protects against failing dependencies
→ but introduces state and configuration

Bulkhead
→ contains resource exhaustion
→ but can reduce resource sharing efficiency
```

In interviews, always explain both sides.

The strongest answer is rarely:

> "Use pattern X."

It is:

> **"I would use X because of this specific problem. It gives us these benefits, but introduces these costs. If the system were simpler, I would avoid it."**

That demonstrates engineering judgment rather than pattern memorization.

______________________________________________________________________

**Previous:** [42. NumPy & Pandas Overview](./42-numpy-pandas.md)

**Next:** [44. Behavioral & HR Interview](./44-behavioral.md)
