# Project Structure & Clean Architecture

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 10 - Project Structure
>
> **File:** `33_project_structure_clean_architecture.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Project Structure Matters
- Monolithic vs Layered Architecture
- Clean Architecture
- Folder Organization
- Responsibilities of Each Layer
- Request Flow
- Dependency Direction
- Benefits of Clean Architecture
- Common Mistakes
- Production Best Practices

______________________________________________________________________

# Why Project Structure Matters

A small FastAPI project may begin with

```
main.py
```

As features grow,

everything ends up in one file.

Example

```
Authentication

↓

Users

↓

Orders

↓

Payments

↓

Notifications

↓

Database
```

The project becomes difficult to maintain.

______________________________________________________________________

# Small Project

```
project/

│

└── main.py
```

Good for learning,

not for production.

______________________________________________________________________

# Growing Project

```
main.py

↓

3000 Lines

↓

Impossible to Maintain
```

Problems include

- Merge conflicts
- Difficult debugging
- Poor reusability
- Tight coupling

______________________________________________________________________

# Layered Architecture

Separate responsibilities.

```
Routes

↓

Services

↓

Repositories

↓

Database
```

Each layer has one primary responsibility.

______________________________________________________________________

# Clean Architecture

Clean Architecture separates

- Business Logic
- Infrastructure
- Framework
- Database

Business rules remain independent of implementation details.

______________________________________________________________________

# Dependency Direction

```
Routes

↓

Services

↓

Repositories

↓

Database
```

Never

```
Database

↓

Route
```

Dependencies point inward,

not outward.

______________________________________________________________________

# Typical Project Structure

```text
app/

├── api/

│   ├── routes/

│   └── dependencies/

│

├── core/

│   ├── config.py

│   └── security.py

│

├── db/

│   ├── models/

│   ├── session.py

│   └── migrations/

│

├── repositories/

│

├── services/

│

├── schemas/

│

├── middleware/

│

├── exceptions/

│

├── utils/

│

└── main.py
```

______________________________________________________________________

# Routes Layer

Responsibilities

- Receive HTTP Requests
- Validate Input
- Call Services
- Return Responses

Routes should remain thin.

______________________________________________________________________

# Service Layer

Responsibilities

- Business Rules
- Validation
- Workflows
- Coordination

Example

```
Create Order

↓

Validate Inventory

↓

Calculate Total

↓

Save Order

↓

Send Notification
```

______________________________________________________________________

# Repository Layer

Responsibilities

- Database Queries
- CRUD Operations
- Transactions

Repositories know SQLAlchemy.

Services should not contain SQL queries.

______________________________________________________________________

# Schema Layer

Contains Pydantic models.

```
Request Models

↓

Response Models
```

These are separate from ORM models.

______________________________________________________________________

# Database Layer

Contains

- Engine
- Session
- Models
- Alembic

Only database-related code belongs here.

______________________________________________________________________

# Core Layer

Contains application-wide configuration.

Examples

- Environment Variables
- Security
- Logging
- Settings

______________________________________________________________________

# Middleware Layer

Contains

- Logging
- Request Timing
- CORS
- Metrics

Cross-cutting concerns belong here.

______________________________________________________________________

# Exception Layer

Contains

- Custom Exceptions
- Global Exception Handlers

Keeps routes clean.

______________________________________________________________________

# Utils Layer

Contains reusable helper functions.

Examples

- Date Utilities
- File Helpers
- String Utilities

Avoid placing business logic here.

______________________________________________________________________

# Request Flow

```
Client

↓

Route

↓

Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

Route

↓

Client
```

______________________________________________________________________

# Example

```
POST /orders

↓

Order Route

↓

Order Service

↓

Order Repository

↓

Database
```

______________________________________________________________________

# Authentication Flow

```
Request

↓

Dependency

↓

Current User

↓

Route

↓

Service
```

Authentication happens before business logic.

______________________________________________________________________

# Configuration Flow

```
Environment

↓

Settings

↓

Application
```

Configuration should come from one central place.

______________________________________________________________________

# ORM vs Schemas

Database

```
User Model
```

API

```
UserResponse
```

Keep them separate.

______________________________________________________________________

# Feature-Based Structure

Large applications sometimes organize by feature.

Example

```text
users/

    routes.py

    service.py

    repository.py

    schemas.py

orders/

    routes.py

    service.py

    repository.py

    schemas.py
```

This improves modularity for very large codebases.

______________________________________________________________________

# Monolith vs Microservices

Monolith

```
Single Application
```

Microservices

```
Users Service

Orders Service

Payments Service
```

Even monoliths benefit from clean architecture.

______________________________________________________________________

# Benefits

- Easier Testing
- Better Separation of Concerns
- Reusable Code
- Easier Refactoring
- Cleaner Dependencies
- Better Scalability

______________________________________________________________________

# Common Mistakes

❌ SQL queries inside route handlers

❌ Business logic inside repositories

❌ Returning ORM models directly

❌ Huge utility modules

❌ Circular imports between layers

______________________________________________________________________

# Production Best Practices

- Keep routes thin.
- Put business rules in services.
- Keep repositories focused on persistence.
- Separate ORM and Pydantic models.
- Centralize configuration.
- Organize by feature as projects grow.
- Maintain one-way dependency flow.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should FastAPI route handlers remain thin in a production application?**

### Answer

Routes are responsible for HTTP concerns,

not business logic.

Keeping routes thin provides:

- Better readability.
- Easier testing.
- Reusable services.
- Cleaner separation of concerns.
- Easier maintenance.
- Simpler migration to other interfaces (CLI, background workers, GraphQL, etc.).

Routes receive requests,

services perform business logic,

repositories interact with the database.

______________________________________________________________________

# Summary

In this chapter you learned:

- Project Structure
- Clean Architecture
- Layered Design
- Folder Organization
- Request Flow
- Dependency Direction
- Feature-Based Organization
- Production Best Practices

A well-structured FastAPI project is easier to understand, test, scale, and maintain, especially as the codebase and
team grow.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. Why does project structure matter?
1. What is layered architecture?
1. What is clean architecture?

______________________________________________________________________

## Layers

4. What responsibilities belong in route handlers?
1. What responsibilities belong in services?
1. What responsibilities belong in repositories?

______________________________________________________________________

## Organization

7. Why should ORM models and API schemas be separated?
1. What belongs in the `core` package?
1. What belongs in the `middleware` package?

______________________________________________________________________

## Architecture

10. Why should dependencies flow from routes toward repositories?
01. Why should business logic remain independent of FastAPI?
01. Why are thin route handlers preferred?

______________________________________________________________________

## Production

13. When is feature-based organization beneficial?
01. Why should configuration be centralized?
01. Why should SQL queries stay out of routes?

______________________________________________________________________

## Scenario-Based

16. Your `users.py` file has grown to 4,000 lines and contains routes, SQL queries, validation, and email-sending logic. How would you restructure it?
01. Your service layer directly imports FastAPI's `Request` object. Why does this violate clean architecture principles?
01. Your repository performs inventory validation before saving data. Why should this logic move elsewhere?
01. Your API returns SQLAlchemy ORM models directly to clients. Why is this discouraged in a clean architecture?
01. Your team plans to expose the same business logic through a REST API, a CLI tool, and scheduled background jobs. How does clean architecture make this easier?

______________________________________________________________________

# Next

[Deployment (Uvicorn, Gunicorn, Docker)](34_deployment_uvicorn_docker.md)
