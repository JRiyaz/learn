# Testing Flask Applications

> **Course:** Flask for Backend Engineers
>
> **Module:** 7
>
> **File:** `17_testing.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Testing is Important
- Testing Pyramid
- Types of Tests
- pytest
- Flask Test Client
- Unit Testing
- Integration Testing
- Mocking
- Fixtures
- Database Testing
- API Testing
- Code Coverage
- Best Practices

______________________________________________________________________

# Why Testing Matters

Imagine deploying an application without testing.

```
Developer

↓

Deploy

↓

Production

↓

Everything Breaks
```

Testing reduces bugs before deployment.

Benefits

- Faster development
- Safer refactoring
- Better code quality
- Higher confidence during deployments

______________________________________________________________________

# The Testing Pyramid

```
        End-to-End
      (Few, Slow)

    Integration Tests

 Unit Tests
(Many, Fast)
```

A healthy project contains many unit tests, fewer integration tests, and relatively few end-to-end tests.

______________________________________________________________________

# Types of Tests

| Test | Purpose |
|------|----------|
| Unit Test | Test one function/class |
| Integration Test | Test interaction between components |
| API Test | Test HTTP endpoints |
| End-to-End Test | Test complete workflows |

______________________________________________________________________

# What is pytest?

`pytest` is the most popular Python testing framework.

Install

```bash
pip install pytest
```

Run tests

```bash
pytest
```

______________________________________________________________________

# Project Structure

```
project/

│

├── app/

├── tests/

│      test_users.py

│      test_auth.py

│      test_orders.py

│

└── pytest.ini
```

Keep tests separate from application code.

______________________________________________________________________

# Your First Test

Function

```python
def add(a, b):

    return a + b
```

Test

```python
def test_add():

    assert add(2, 3) == 5
```

Run

```bash
pytest
```

______________________________________________________________________

# Test Naming

Good

```
test_login.py

test_users.py

test_orders.py
```

Functions

```python
def test_create_user():
    ...
```

pytest automatically discovers files and functions following these conventions.

______________________________________________________________________

# Flask Test Client

Flask provides a built-in HTTP client.

```python
client = app.test_client()
```

This allows requests without starting a real server.

______________________________________________________________________

# GET Request Test

```python
def test_home(client):

    response = client.get("/")

    assert response.status_code == 200
```

______________________________________________________________________

# POST Request Test

```python
response = client.post(

    "/login",

    json={

        "username": "riyaz",

        "password": "password"

    }

)
```

______________________________________________________________________

# Testing JSON

```python
response = client.get("/users")

data = response.get_json()

assert data["success"] is True
```

______________________________________________________________________

# Testing Status Codes

```python
assert response.status_code == 201
```

Never assume a request succeeded without checking the response.

______________________________________________________________________

# Fixtures

Fixtures provide reusable setup code.

```python
import pytest

@pytest.fixture

def app():

    app = create_app(

        TestingConfig

    )

    return app
```

______________________________________________________________________

# Client Fixture

```python
@pytest.fixture

def client(app):

    return app.test_client()
```

Now every test can use

```python
client
```

______________________________________________________________________

# Testing Database

Use

```
Production Database

❌ Never
```

Instead

```
Temporary Test Database
```

Each test should be isolated.

______________________________________________________________________

# Setup & Teardown

Example

```python
@pytest.fixture

def database():

    db.create_all()

    yield

    db.drop_all()
```

Setup happens before the test.

Cleanup happens afterward.

______________________________________________________________________

# Unit Testing

Test one component.

Example

```
Password Validation

↓

Expected Result
```

No database.

No HTTP requests.

Very fast.

______________________________________________________________________

# Integration Testing

Tests interaction between components.

Example

```
API

↓

Database

↓

Response
```

Integration tests are slower but verify collaboration between layers.

______________________________________________________________________

# Mocking

Sometimes external systems should not be called.

Example

```
Payment Gateway
```

Replace with a mock.

______________________________________________________________________

# unittest.mock

```python
from unittest.mock import patch
```

Example

```python
@patch(

    "services.email.send"

)
def test_email(mock_send):

    ...
```

Now

```
Real Email

❌ Not Sent
```

______________________________________________________________________

# Testing Authentication

Example

```
POST /login

↓

JWT

↓

Access Protected Route
```

Verify

- Login succeeds
- Invalid credentials fail
- Protected endpoints require authentication

______________________________________________________________________

# Testing Validation

Example

```
POST /users

↓

Missing Email

↓

400
```

Always test invalid input.

______________________________________________________________________

# Testing Errors

Example

```
Unknown User

↓

404
```

Verify

- Status Code
- Error Message
- JSON Structure

______________________________________________________________________

# Database Rollback

Some projects wrap each test in a transaction.

```
Run Test

↓

Rollback

↓

Clean Database
```

This keeps tests independent and fast.

______________________________________________________________________

# Code Coverage

Install

```bash
pip install pytest-cov
```

Run

```bash
pytest --cov=app
```

Coverage measures how much code is exercised by tests.

High coverage does **not** automatically mean high-quality tests.

______________________________________________________________________

# Continuous Integration

Typical flow

```
Git Push

↓

GitHub Actions

↓

Run Tests

↓

Deploy
```

Applications should not deploy if critical tests fail.

______________________________________________________________________

# Testing Architecture

```
Unit Tests

↓

Integration Tests

↓

API Tests

↓

Deployment
```

Testing becomes part of the development workflow.

______________________________________________________________________

# Common Mistakes

❌ Testing against the production database

❌ Writing only happy-path tests

❌ Ignoring edge cases

❌ Depending on test execution order

❌ Sharing state between tests

❌ Not mocking external services

______________________________________________________________________

# Production Best Practices

- Write many unit tests.
- Add integration tests for critical workflows.
- Test both success and failure cases.
- Keep tests independent.
- Use fixtures for reusable setup.
- Mock external services.
- Automate tests in CI/CD.
- Monitor code coverage without treating it as the only quality metric.

______________________________________________________________________

# Interview Deep Dive

### Question

**What is the difference between unit testing and integration testing?**

### Answer

A unit test verifies a single unit of code, such as a function or class, in isolation.

Example

```
Password Validation Function
```

An integration test verifies that multiple components work together.

Example

```
HTTP Request

↓

Route

↓

Database

↓

Response
```

Unit tests are faster and easier to isolate.

Integration tests provide confidence that the application behaves correctly as a whole.

A well-tested application typically includes both.

______________________________________________________________________

# Summary

In this chapter you learned:

- Testing
- pytest
- Flask Test Client
- Fixtures
- Unit Tests
- Integration Tests
- Mocking
- Database Testing
- API Testing
- Code Coverage
- CI/CD Integration

Testing is one of the most valuable engineering practices because it reduces regressions, improves confidence, and
enables safer refactoring.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. Why is testing important?
1. What is the testing pyramid?
1. What is pytest?

______________________________________________________________________

## Flask Testing

4. What is the Flask test client?
1. Why use fixtures?
1. How do you test JSON responses?
1. Why should status codes always be asserted?

______________________________________________________________________

## Test Types

8. What is a unit test?
1. What is an integration test?
1. When should external services be mocked?

______________________________________________________________________

## Database

11. Why shouldn't tests use the production database?
01. What is setup and teardown?
01. Why are transactions useful during testing?

______________________________________________________________________

## CI/CD

14. Why should automated tests run in a CI pipeline?
01. Does high code coverage guarantee good tests? Why or why not?

______________________________________________________________________

## Scenario-Based

16. Your test suite sends real emails to customers during execution. How would you redesign the tests?
01. Tests pass individually but fail when run together. What kinds of problems might cause this?
01. Your API accepts invalid input but no test detects it. Which additional tests would you add?
01. Your application integrates with a payment gateway that charges real credit cards. Why should those calls be mocked during automated testing?
01. A teammate wants to skip automated tests to speed up deployments. What risks does this introduce?

______________________________________________________________________

# Next

[Background Tasks with Celery](18_background_tasks.md)
