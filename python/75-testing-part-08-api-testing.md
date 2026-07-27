# File: python/75-testing-part-08-api-testing.md

# Testing
# Part 8: API Testing – Testing REST APIs with FastAPI and Flask

> **Course:** Backend Engineering Roadmap
>
> **Module:** Testing
>
> **Lesson:** 75
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 14–16 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- What API testing is
- Unit vs Integration vs API testing
- Testing HTTP endpoints
- FastAPI `TestClient`
- Flask testing client
- Testing request validation
- Testing authentication
- Testing error responses
- Testing CRUD APIs
- Best practices for API testing
- Production testing strategies

---

# Recap

In the previous lesson, we learned about **integration testing**, where multiple real components work together.

API testing goes one step further.

Instead of directly calling:

```python
UserService.create_user()
```

we send a real HTTP request.

```
HTTP Request

↓

Router

↓

Validation

↓

Service

↓

Repository

↓

Database

↓

HTTP Response
```

API tests verify the behaviour of your application from a client's perspective.

---

# What is API Testing?

API testing verifies that an application's HTTP interface behaves correctly.

Instead of testing internal functions, API tests interact with endpoints exactly as a client would.

Example:

```
POST /users

↓

HTTP Request

↓

Application

↓

HTTP Response
```

The internal implementation is irrelevant.

Only the observable behaviour matters.

---

# Where API Testing Fits

```
                End-to-End

                     ▲

              API Testing

                     ▲

          Integration Testing

                     ▲

             Unit Testing
```

Each layer provides a different level of confidence.

---

# What Should an API Test Verify?

A good API test should verify:

- Status code
- Response body
- Response headers
- Validation
- Authentication
- Authorisation
- Database changes
- Error handling

---

# FastAPI TestClient

FastAPI provides:

```python
from fastapi.testclient import TestClient
```

Example:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
```

Requests are made exactly like real HTTP requests.

---

# Your First API Test

Application:

```python
@app.get("/health")

def health():

    return {

        "status": "ok"

    }
```

Test:

```python
def test_health():

    response = client.get(

        "/health"

    )

    assert response.status_code == 200

    assert response.json() == {

        "status": "ok"

    }
```

---

# Testing POST Requests

Endpoint:

```python
@app.post("/users")
```

Test:

```python
response = client.post(

    "/users",

    json={

        "name": "Alice",

        "email": "alice@example.com"

    }

)

assert response.status_code == 201
```

The `json=` argument automatically serialises the payload.

---

# Testing Response Headers

Example:

```python
assert (

    response.headers["content-type"]

    == "application/json"

)
```

Headers are part of the API contract and should be verified when important.

---

# Testing JSON Responses

Example:

```python
data = response.json()

assert data["name"] == "Alice"

assert data["email"] == "alice@example.com"
```

Avoid comparing large JSON documents unless necessary.

Instead, verify the fields relevant to the test.

---

# Testing Path Parameters

Endpoint:

```python
GET /users/{id}
```

Test:

```python
response = client.get(

    "/users/1"

)

assert response.status_code == 200
```

Also test:

```
Unknown ID

↓

404 Not Found
```

---

# Testing Query Parameters

Endpoint:

```python
GET /users?page=1
```

Test:

```python
response = client.get(

    "/users",

    params={

        "page": 1,

        "limit": 20

    }

)

assert response.status_code == 200
```

---

# Testing Validation

FastAPI automatically validates requests.

Example:

```python
response = client.post(

    "/users",

    json={

        "name": "Alice"

    }

)
```

Suppose the `email` field is required.

Expected:

```python
assert response.status_code == 422
```

Validation failures should be tested just as carefully as successful requests.

---

# Testing Authentication

Suppose the endpoint requires a JWT.

Request:

```python
response = client.get(

    "/profile",

    headers={

        "Authorization":

        "Bearer TOKEN"

    }

)
```

Expected:

```python
assert response.status_code == 200
```

Also test:

```
Missing Token

↓

401 Unauthorized
```

```
Invalid Token

↓

401 Unauthorized
```

```
Expired Token

↓

401 Unauthorized
```

---

# Testing Error Responses

Example:

```
GET /users/999
```

Expected:

```python
assert response.status_code == 404
```

Verify the response body as well.

```python
assert response.json()["detail"] == "User not found"
```

---

# Testing CRUD APIs

Suppose our application supports:

```
POST

↓

Create User
```

```
GET

↓

Retrieve User
```

```
PUT

↓

Update User
```

```
DELETE

↓

Delete User
```

A complete API test suite should verify each operation.

---

# Testing Database Changes

Suppose:

```
POST /users
```

The API returns:

```
201 Created
```

The test should also verify:

```
Database

↓

User Exists
```

Checking only the HTTP response is often insufficient.

---

# Flask Testing Client

Flask provides a similar client.

```python
app.test_client()
```

Example:

```python
client = app.test_client()

response = client.get(

    "/health"

)

assert response.status_code == 200
```

The testing concepts are the same as FastAPI.

---

# API Test Structure

A typical API test follows:

```
Arrange

↓

Act

↓

Assert
```

Arrange:

- Prepare data.

Act:

- Send HTTP request.

Assert:

- Verify response and side effects.

---

# Common Mistakes

## Mistake 1

Testing only successful responses.

Always include failure scenarios.

---

## Mistake 2

Ignoring response headers.

---

## Mistake 3

Using production databases.

Always use test databases.

---

## Mistake 4

Depending on test execution order.

---

## Mistake 5

Making assertions on unnecessary fields.

Focus on the behaviour relevant to the test.

---

# Best Practices

✅ Test every endpoint.

✅ Test both success and failure paths.

✅ Verify status codes.

✅ Verify response payloads.

✅ Verify database changes.

✅ Use fixtures for setup.

✅ Keep tests independent.

❌ Don't hardcode production credentials.

❌ Don't rely on external APIs during API tests.

---

# Production Insight

A mature backend project's CI pipeline commonly executes API tests after unit and integration tests.

```
Checkout Code

↓

Start PostgreSQL

↓

Apply Migrations

↓

Start Application

↓

Run API Tests

↓

Build Docker Image

↓

Deploy
```

API tests validate the application's public contract.

If an endpoint accidentally changes its status code, response structure, validation rules, or authentication behaviour, the pipeline detects the regression before deployment.

This is particularly important because frontend applications, mobile apps, and third-party integrations all depend on that contract remaining stable.

---

# Questions

### Question

> What is the purpose of API testing?

### Answer

To verify that an application's HTTP interface behaves correctly from the perspective of an API client.

---

### Question

> Why should API tests verify both the response and the database?

### Answer

Because a successful HTTP response does not necessarily guarantee that the expected data was actually stored or modified correctly.

---

### Question

> Why should validation failures be tested?

### Answer

To ensure invalid input is rejected consistently and appropriate error responses are returned.

---

### Question

> Why are authentication tests important?

### Answer

They verify that protected endpoints cannot be accessed without valid credentials and that authorised users receive the expected responses.

---

### Question

> Why should API tests remain independent?

### Answer

Independent tests are repeatable, can run in any order, and are easier to debug when failures occur.

---

# Practical Lesson

Create a small FastAPI or Flask application with the following endpoints:

```text
POST   /users

GET    /users/{id}

PUT    /users/{id}

DELETE /users/{id}

GET    /health
```

Write API tests that verify:

- Health check.
- User creation.
- User retrieval.
- User update.
- User deletion.
- Invalid requests.
- Missing required fields.
- Non-existent users.
- Authentication failures (if implemented).

Use a dedicated test database and ensure each test runs in isolation.

---

# Knowledge Check

## Question 1

How does API testing differ from integration testing?

### Answer

Integration testing focuses on interactions between internal components, while API testing verifies the application's public HTTP interface as experienced by clients.

---

## Question 2

Why should API tests include negative scenarios?

### Answer

Because clients frequently send invalid requests, and the application must respond with correct status codes and error messages.

---

## Question 3

What should always be verified after a successful `POST` request?

### Answer

The status code, response body, and any expected side effects, such as records being created in the database.

---

## Question 4

Why are status codes part of the API contract?

### Answer

Clients rely on them to determine whether a request succeeded, failed due to validation, lacked authentication, or encountered another error.

---

## Question 5

Why are API tests valuable in CI/CD pipelines?

### Answer

They detect regressions in endpoint behaviour, request validation, authentication, and response formats before changes are deployed.

---

# Assignment

## Exercise 1

Write API tests for every endpoint in one of your existing FastAPI or Flask projects.

Ensure both successful and unsuccessful scenarios are covered.

---

## Exercise 2

For every endpoint, create tests covering:

- Valid request.
- Invalid request body.
- Missing required fields.
- Invalid path parameter.
- Resource not found.
- Unexpected server error (where applicable).

---

## Exercise 3

Implement authentication for one endpoint and write tests for:

- Valid token.
- Missing token.
- Invalid token.
- Expired token.

---

## Exercise 4

Configure your CI pipeline to run:

1. Unit tests.
2. Integration tests.
3. API tests.

Verify that the build fails if any API contract is broken.

---

# Summary

In this lesson, you learned:

- ✅ What API testing is.
- ✅ How API testing differs from unit and integration testing.
- ✅ Using FastAPI's `TestClient`.
- ✅ Using Flask's testing client.
- ✅ Testing GET, POST, PUT, and DELETE endpoints.
- ✅ Testing validation and authentication.
- ✅ Verifying database side effects.
- ✅ Production best practices for API testing.

---

# Next Lesson

**File:**
[76-networking-part-01-tcp-sockets](76-networking-part-01-tcp-sockets.md)
