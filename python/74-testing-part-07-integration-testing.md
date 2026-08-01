# File: python/74-testing-part-07-integration-testing.md

# Testing

# Part 7: Integration Testing – Verifying Components Work Together

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 74
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 12–15 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What integration testing is
- Unit vs Integration testing
- What should and should not be mocked
- Testing real databases
- Testing repositories
- Testing services
- Testing external dependencies
- Test databases
- Test isolation
- Integration testing strategies
- Production best practices

______________________________________________________________________

# Recap

So far, we've focused on **unit testing**.

In unit tests we replaced external dependencies with:

- Mocks
- Fixtures
- Fake objects
- Monkeypatch

This allowed us to test one piece of code in isolation.

However, unit tests cannot answer an equally important question:

> **Do all of our components actually work together?**

That's the purpose of integration testing.

______________________________________________________________________

# What is Integration Testing?

Integration testing verifies that multiple real components interact correctly.

Instead of testing a single function, we test a workflow.

```
Client

↓

Service

↓

Repository

↓

Database

↓

Response
```

Unlike unit tests, the goal is **not isolation**, but **interaction**.

______________________________________________________________________

# Unit Test vs Integration Test

Consider a user registration flow.

### Unit Test

```
UserService

↓

Mock Repository

↓

Mock Email Service
```

Only business logic is tested.

______________________________________________________________________

### Integration Test

```
UserService

↓

Repository

↓

PostgreSQL

↓

Response
```

The database is real.

The repository is real.

The SQL is real.

______________________________________________________________________

# Why Integration Tests Matter

Suppose the repository contains:

```python
INSERT INTO users (...)
```

Your unit tests pass because the repository is mocked.

But in production:

```
SQL Syntax Error
```

Unit tests cannot detect SQL problems.

Integration tests execute the real query.

______________________________________________________________________

# A Typical Backend Architecture

```
HTTP Request

↓

Router

↓

Service

↓

Repository

↓

Database
```

Each layer may work individually.

Integration testing verifies the entire chain.

______________________________________________________________________

# What Should Be Real?

In an integration test, core application components should usually be real.

```
Service

↓

Repository

↓

Database
```

Business logic and persistence work together exactly as they do in production.

______________________________________________________________________

# What Can Still Be Mocked?

Not everything must be real.

External systems can still be replaced.

Examples:

- Payment gateways
- Email providers
- SMS services
- Third-party APIs
- Cloud storage

Example:

```
Application

↓

Real PostgreSQL

↓

Mock Stripe API
```

The goal is to avoid relying on systems outside your control.

______________________________________________________________________

# Example Project

```text
app/

├── models.py

├── repository.py

├── service.py

├── database.py

└── tests/

    └── test_integration.py
```

Unlike unit tests, most components are real.

______________________________________________________________________

# Testing a Repository

Suppose:

```python
class UserRepository:

    def create(

        self,

        user

    ):

        ...
```

Integration test:

```python
def test_create_user(

    database,

    repository

):

    repository.create(

        User(

            name="Alice"

        )

    )

    user = repository.find_by_name(

        "Alice"

    )

    assert user.name == "Alice"
```

The repository talks to a real database.

______________________________________________________________________

# Why Use a Test Database?

Never run integration tests against production data.

Instead:

```
Application

↓

Test Database

↓

Delete After Tests
```

Common choices:

- SQLite (simple projects)
- PostgreSQL test instance
- Docker containers
- Temporary databases

______________________________________________________________________

# Database Isolation

Each test should start with a known state.

Bad:

```
Test A

↓

Creates User

↓

Test B

↓

Unexpected User Exists
```

Good:

```
Create Database State

↓

Run Test

↓

Rollback

↓

Next Test
```

Tests should never depend on previous tests.

______________________________________________________________________

# Transactions

A common approach is:

```
Start Transaction

↓

Run Test

↓

Rollback
```

Benefits:

- Fast
- Isolated
- No cleanup scripts required

This technique is widely used with SQLAlchemy.

______________________________________________________________________

# Fixtures for Integration Tests

Example:

```python
@pytest.fixture

def session():

    ...

    yield session

    session.rollback()

    session.close()
```

Each test receives a clean database session.

______________________________________________________________________

# Testing Services

Suppose:

```python
UserService

↓

Repository

↓

Database
```

Instead of mocking the repository:

```python
repository = Mock()
```

Use the real repository.

The service should be tested exactly as it runs in production.

______________________________________________________________________

# Testing Error Handling

Integration tests should verify failures as well.

Examples:

- Duplicate keys
- Constraint violations
- Missing records
- Invalid transactions

Example:

```python
with pytest.raises(

    IntegrityError

):

    repository.create(

        duplicate_user

    )
```

______________________________________________________________________

# Using Docker

Many backend teams use Docker for integration tests.

```
pytest

↓

Docker Compose

↓

PostgreSQL

↓

Redis

↓

Run Tests
```

Advantages:

- Same environment for every developer
- Same environment in CI
- Same database version

______________________________________________________________________

# Integration Test Pyramid

```
             End-to-End

                  ▲

        Integration Tests

                  ▲

           Unit Tests
```

Most tests should still be unit tests.

Integration tests verify communication between components.

______________________________________________________________________

# Example Workflow

Imagine registering a new user.

```
API Request

↓

Validation

↓

Service

↓

Repository

↓

Database

↓

Commit

↓

Response
```

An integration test verifies that the complete workflow succeeds.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Running integration tests against production resources.

______________________________________________________________________

## Mistake 2

Sharing the same database state between tests.

______________________________________________________________________

## Mistake 3

Mocking everything.

If everything is mocked, the test is no longer an integration test.

______________________________________________________________________

## Mistake 4

Making integration tests depend on internet access.

______________________________________________________________________

## Mistake 5

Combining unit and integration tests in the same test file.

Keep them organised separately.

______________________________________________________________________

# Best Practices

✅ Use a dedicated test database.

✅ Reset database state between tests.

✅ Mock only external systems.

✅ Test realistic workflows.

✅ Keep integration tests deterministic.

❌ Don't reuse production databases.

❌ Don't depend on test execution order.

______________________________________________________________________

# Production Insight

A typical CI pipeline for a FastAPI application may look like this:

```
Checkout Code

↓

Start PostgreSQL Container

↓

Apply Database Migrations

↓

Run Unit Tests

↓

Run Integration Tests

↓

Build Docker Image

↓

Deploy
```

Before integration tests begin:

- A clean PostgreSQL container is started.
- Database migrations are applied.
- The application connects using test configuration.

When the pipeline finishes, the container is destroyed.

This approach ensures every test run starts from a known environment, eliminating "it works on my machine" problems.

______________________________________________________________________

# Questions

### Question

> What is the purpose of an integration test?

### Answer

To verify that multiple real components work together correctly.

______________________________________________________________________

### Question

> Why are repositories usually real in integration tests?

### Answer

Because repository logic, SQL queries, and database interactions must be validated against a real database.

______________________________________________________________________

### Question

> Why should production databases never be used for testing?

### Answer

Tests may modify or delete data, making production databases unsafe for automated testing.

______________________________________________________________________

### Question

> Why are transactions commonly used during integration testing?

### Answer

They allow each test to be rolled back, providing isolation without requiring manual cleanup.

______________________________________________________________________

### Question

> Which dependencies are commonly mocked in integration tests?

### Answer

External systems such as payment gateways, email providers, cloud services, and third-party APIs.

______________________________________________________________________

# Practical Lesson

Create the following project:

```text
app/

├── database.py

├── models.py

├── repository.py

├── service.py

└── tests/

    └── test_integration.py
```

Implement:

- A real SQLite or PostgreSQL test database.
- A `UserRepository`.
- A `UserService`.
- A fixture that creates a database session.
- Tests that:
  - Create a user.
  - Retrieve the user.
  - Update the user.
  - Delete the user.
  - Verify duplicate-user errors.
  - Roll back changes after each test.

Then repeat the exercise using a Dockerised PostgreSQL instance.

______________________________________________________________________

# Knowledge Check

## Question 1

Why are integration tests slower than unit tests?

### Answer

Because they communicate with real infrastructure such as databases, file systems, or network services instead of
lightweight mocks.

______________________________________________________________________

## Question 2

Why should integration tests use dedicated infrastructure?

### Answer

Dedicated infrastructure prevents test data from affecting production systems and ensures predictable, repeatable
results.

______________________________________________________________________

## Question 3

When should external services still be mocked in integration tests?

### Answer

When the services are outside your application's control or would make tests slow, expensive, or unreliable.

______________________________________________________________________

## Question 4

Why is database rollback a common testing strategy?

### Answer

It restores the database to a clean state after each test, preventing tests from affecting one another.

______________________________________________________________________

## Question 5

How do unit tests and integration tests complement each other?

### Answer

Unit tests verify individual components in isolation, while integration tests verify that those components communicate
correctly when assembled into a working application.

______________________________________________________________________

# Assignment

## Exercise 1

Create a PostgreSQL test database for one of your existing FastAPI or Flask projects.

Write integration tests for every repository method.

______________________________________________________________________

## Exercise 2

Configure your integration tests to run inside Docker.

Ensure a fresh database container is created for every CI run.

______________________________________________________________________

## Exercise 3

Write integration tests covering:

- Successful insert.
- Duplicate primary key.
- Transaction rollback.
- Record update.
- Record deletion.
- Query returning no results.

______________________________________________________________________

## Exercise 4

Review your current unit tests.

Identify any tests that would provide greater confidence if converted into integration tests using real repositories and
a real database.

Explain your reasoning for each.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What integration testing is.
- ✅ How it differs from unit testing.
- ✅ Which components should be real.
- ✅ Which dependencies should remain mocked.
- ✅ Why dedicated test databases are important.
- ✅ Database isolation strategies.
- ✅ Transaction rollback techniques.
- ✅ Docker-based integration testing.
- ✅ Production best practices for backend integration testing.

______________________________________________________________________

# Next Lesson

**File:** [75-testing-part-08-api-testing](75-testing-part-08-api-testing.md)
