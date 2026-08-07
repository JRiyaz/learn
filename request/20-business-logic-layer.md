# Complete HTTP Request Lifecycle Deep Dive

## 20. Business Logic Layer

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand the purpose of the Business Logic Layer, why it should be separated from controllers and database code, how it processes requests, interacts with other services, and prepares responses.

______________________________________________________________________

# Introduction

The request has successfully passed through

- Middleware
- Validation
- Authentication
- Authorization
- Sanitization

Now,

for the first time,

your application's

actual functionality

begins.

This is called

the

```
Business Logic Layer
```

______________________________________________________________________

# High Level Flow

```
HTTP Request

↓

Controller

↓

Business Logic

↓

Cache

↓

Database

↓

External APIs

↓

Business Logic

↓

Response
```

The Business Logic Layer

is the heart

of the application.

______________________________________________________________________

# What is Business Logic?

Interview favorite.

Business Logic

contains

the rules

that define

how

your application works.

Examples

- Login users
- Create orders
- Calculate discounts
- Process payments
- Book tickets
- Send notifications

Without business logic,

an application

cannot provide

any useful functionality.

______________________________________________________________________

# Example

Suppose

an e-commerce application

receives

```
POST /orders
```

Business Logic

may perform

the following steps

```
Validate Product

↓

Check Inventory

↓

Calculate Price

↓

Apply Discount

↓

Create Order

↓

Reserve Stock

↓

Send Notification
```

______________________________________________________________________

# What Should NOT Be Business Logic?

Business Logic

should NOT contain

- HTTP request handling
- SQL queries
- JSON serialization
- Authentication logic
- API documentation

Those belong

to other layers.

______________________________________________________________________

# Typical Architecture

```
Controller

↓

Service

↓

Repository

↓

Database
```

Where

```
Controller

↓

Receives Request
```

```
Service

↓

Business Logic
```

```
Repository

↓

Database Access
```

______________________________________________________________________

# Example Structure

```
app/

├── routers/

├── services/

├── repositories/

├── models/

├── schemas/
```

Business Logic

usually lives

inside

```
services/
```

______________________________________________________________________

# Example Flow

User requests

```
Create Order
```

```
Route

↓

Order Service

↓

Inventory Repository

↓

Payment Service

↓

Order Repository

↓

Response
```

______________________________________________________________________

# Controller Example

```python
@app.post("/orders")
async def create_order(
    order: OrderRequest
):
    return await order_service.create(order)
```

Notice

the controller

contains

very little logic.

______________________________________________________________________

# Service Example

```python
class OrderService:

    async def create(order):

        check_stock()

        calculate_price()

        save_order()
```

The service

contains

the business rules.

______________________________________________________________________

# Why Separate Business Logic?

Interview favorite.

Benefits

- Easier testing
- Better code reuse
- Cleaner controllers
- Easier maintenance
- Better separation of concerns

______________________________________________________________________

# Business Logic May Call Multiple Components

Example

```
Business Logic

↓

Redis

↓

Database

↓

Payment API

↓

Email Service

↓

Kafka
```

It coordinates

everything.

______________________________________________________________________

# Cache Lookup

Business Logic

often checks

cache first.

```
Redis

↓

Hit?

↓

Return Data

↓

Miss?

↓

Database
```

Improves performance.

______________________________________________________________________

# Database Access

If cache misses,

Business Logic

calls

the Repository.

```
Service

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL
```

______________________________________________________________________

# External API Calls

Example

Payment Gateway

```
Business Logic

↓

Stripe API

↓

Payment Result
```

Or

Shipping Service

```
↓

FedEx API

↓

Tracking Number
```

______________________________________________________________________

# Event Publishing

Modern applications

often publish events.

Example

```
Order Created

↓

Kafka

↓

Notification Service

↓

Email
```

Business Logic

doesn't always

perform everything

synchronously.

______________________________________________________________________

# Error Handling

Suppose

payment fails.

Business Logic

decides

what happens.

Example

```
Payment Failed

↓

Cancel Order

↓

Return Error
```

______________________________________________________________________

# Transactions

Interview favorite.

Suppose

creating an order

requires

multiple database updates.

```
Create Order

↓

Reduce Inventory

↓

Create Payment
```

If

one step fails,

everything

should roll back.

This is called

a

```
Database Transaction
```

______________________________________________________________________

# Idempotency

Suppose

the client

retries

the same request.

Business Logic

should avoid

creating

duplicate orders

or payments.

Example

```
Idempotency Key

↓

Already Processed?

↓

Return Existing Result
```

______________________________________________________________________

# Business Rules

Examples

```
Order Total

>

₹1000

↓

Free Shipping
```

```
Age

<

18

↓

Reject Loan
```

```
Stock

=

0

↓

Cannot Purchase
```

These rules

belong

inside

the Business Logic Layer.

______________________________________________________________________

# Validation vs Business Rules

Interview favorite.

Validation

checks

```
Age

↓

Integer?
```

Business Logic

checks

```
Age

↓

Eligible

for Loan?
```

They solve

different problems.

______________________________________________________________________

# Logging

Business Logic

may log

important events.

Example

```
Order Created

↓

User ID

↓

Amount

↓

Timestamp
```

Useful

for

auditing

and debugging.

______________________________________________________________________

# Metrics

Business Logic

can publish

metrics.

Examples

- Orders Created
- Payment Success Rate
- Login Failures
- Average Response Time

These metrics

are collected

by monitoring tools.

______________________________________________________________________

# Exception Handling

Suppose

inventory

is unavailable.

Business Logic

raises

an exception.

Controller

returns

```
409 Conflict
```

or

```
400 Bad Request
```

depending

on the situation.

______________________________________________________________________

# Good Practices

- Keep controllers thin
- Keep services focused
- Reuse common logic
- Write unit tests
- Keep business rules centralized
- Avoid duplicated logic

______________________________________________________________________

# Common Mistakes

## Fat Controllers

Bad

```python
@app.post(...)
```

contains

500 lines

of business logic.

Instead,

move

the logic

to

a service.

______________________________________________________________________

## Business Logic in SQL

Avoid

embedding

complex business rules

inside SQL queries

when they belong

in the application layer.

______________________________________________________________________

## Duplicate Logic

Don't repeat

the same business rule

in multiple endpoints.

Create

reusable services.

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Framework | FastAPI |
| Business Layer | Service Classes |
| ORM | SQLAlchemy |
| Cache | Redis |
| Messaging | Kafka, RabbitMQ |
| Monitoring | Prometheus |

______________________________________________________________________

# Common Interview Questions

## What is the Business Logic Layer?

The Business Logic Layer contains the application's core rules and workflows. It coordinates validation results,
database access, external services, and business decisions.

______________________________________________________________________

## Why shouldn't controllers contain business logic?

Controllers should focus on handling HTTP requests and responses. Moving business logic to services improves
maintainability, testing, and code reuse.

______________________________________________________________________

## What is the difference between validation and business rules?

Validation ensures input is correctly formatted, while business rules determine whether the requested operation is
allowed according to application requirements.

______________________________________________________________________

## Why use a Service Layer?

A Service Layer centralizes business rules, reduces code duplication, and makes applications easier to test and
maintain.

______________________________________________________________________

## When should business logic use transactions?

Whenever multiple database operations must either all succeed or all fail together, such as creating an order and
reducing inventory.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain the role of the Business Logic Layer in a backend application.

### Answer

The Business Logic Layer contains the application's core business rules and workflows. It receives validated and
authorized requests from the controller, coordinates operations such as cache lookups, database access, external API
calls, and event publishing, applies business rules, handles errors, and prepares the final result that is returned to
the client.

______________________________________________________________________

# Summary

The Business Logic Layer

is the core

of every backend application.

It coordinates

- Business rules
- Cache
- Database
- External APIs
- Transactions
- Event publishing

while keeping

controllers

clean

and maintainable.

After the business logic finishes,

the application usually interacts with the **database through an ORM or repository layer**, which we'll explore next.

______________________________________________________________________

# Next

[21. ORM and Database Interaction](21-orm-and-database-interaction.md)
