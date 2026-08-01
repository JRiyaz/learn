# Security - Part 18

# API Security

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What API Security is
- Common API security risks
- Authentication vs Authorization
- Input validation
- Rate limiting
- API versioning
- Pagination
- Secure API design
- FastAPI best practices

______________________________________________________________________

# What is API Security?

API Security is the practice of protecting APIs from unauthorized access, misuse, data leaks, and abuse.

Every request that reaches your API should answer these questions:

```text id="api1801"
Who is making the request?

↓

Are they allowed?

↓

Is the request valid?

↓

Can the request be processed safely?
```

______________________________________________________________________

# Why Is API Security Important?

Your backend is the heart of your application.

It has access to:

- Users
- Database
- Payments
- Files
- Authentication
- Business Logic

If your API is insecure,

your entire application is insecure.

______________________________________________________________________

# Typical API Request

```text id="api1802"
Client

↓

HTTPS

↓

Authentication

↓

Authorization

↓

Validation

↓

Business Logic

↓

Database

↓

Response
```

Every step is an opportunity to improve security.

______________________________________________________________________

# Authentication

The first question is:

```text id="api1803"
Who is the user?
```

Common authentication methods:

- JWT
- OAuth2
- Session Cookies
- API Keys

Never allow protected endpoints

without authentication.

______________________________________________________________________

# Authorization

After authentication,

verify permissions.

```text id="api1804"
Authenticated User

↓

Can Access Resource?

↓

Yes

↓

Return Data
```

Authentication alone is never enough.

______________________________________________________________________

# Input Validation

Every request should be validated.

FastAPI makes this easy

using Pydantic.

Example

```python id="api1805"
from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    price: float
```

Invalid data

should never reach

your business logic.

______________________________________________________________________

# Secure Response Models

Never return

your database models directly.

Example

Instead of

```python id="api1806"
return user
```

Use

```python id="api1807"
class UserResponse(BaseModel):
    id: int
    username: str
```

Return only

the required fields.

______________________________________________________________________

# Rate Limiting

Protect your API

against abuse.

Example

```text id="api1808"
100 Requests

↓

1 Minute

↓

Allowed

101st Request

↓

429 Too Many Requests
```

This helps prevent:

- Brute-force attacks
- API abuse
- Denial-of-Service attempts

We'll build a rate limiter later in this course.

______________________________________________________________________

# Pagination

Never return

an unlimited number of records.

Bad

```text id="api1809"
GET /books

↓

500,000 Records
```

Better

```text id="api1810"
GET /books

?page=1

&limit=20
```

Pagination:

- Improves performance
- Reduces bandwidth
- Prevents accidental overload

______________________________________________________________________

# API Versioning

As APIs evolve,

breaking changes become necessary.

Example

```text id="api1811"
/api/v1/books

↓

/api/v2/books
```

Versioning allows

old clients

to continue working.

______________________________________________________________________

# Error Handling

Bad Example

```text id="api1812"
Database Password Invalid

Host: 10.0.0.5
```

Good Example

```text id="api1813"
Internal Server Error
```

Detailed errors

belong in logs,

not API responses.

______________________________________________________________________

# Logging

Log:

- Authentication failures
- Authorization failures
- Unexpected exceptions
- Suspicious activity

Avoid logging:

- Passwords
- JWTs
- API keys
- Sensitive personal data

______________________________________________________________________

# HTTPS

Every production API

should use HTTPS.

```text id="api1814"
Client

↓

TLS

↓

Encrypted Communication

↓

Backend
```

Never expose authentication tokens

over HTTP.

______________________________________________________________________

# CORS

If browsers access your API,

configure CORS carefully.

Bad

```python id="api1815"
allow_origins=["*"]
```

Better

```python id="api1816"
allow_origins=[
    "https://library.example.com"
]
```

We'll discuss CORS in detail

in the next lesson.

______________________________________________________________________

# Secure Headers

Consider sending

security headers such as:

- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy

These provide additional protection

for browser-based clients.

______________________________________________________________________

# Secure API Workflow

```text id="api1817"
HTTPS

↓

Authentication

↓

Authorization

↓

Validation

↓

Rate Limiting

↓

Business Logic

↓

Logging

↓

Response Model
```

This is the workflow

you should aim for

in production APIs.

______________________________________________________________________

# API Security Checklist

Before deploying an API,

verify:

✅ HTTPS enabled

✅ Authentication required

✅ Authorization enforced

✅ Input validated

✅ Response models used

✅ Rate limiting configured

✅ Logging enabled

✅ Secrets secured

✅ Pagination implemented where needed

✅ Error messages reviewed

______________________________________________________________________

# Defense in Depth

API security

is never one feature.

It combines:

```text id="api1818"
HTTPS

↓

Authentication

↓

Authorization

↓

Validation

↓

Rate Limiting

↓

Logging

↓

Monitoring
```

______________________________________________________________________

# Common Mistakes

### Returning Database Models

Always use

response models.

______________________________________________________________________

### Trusting Client Input

Validate

everything.

______________________________________________________________________

### Forgetting Authorization

Authentication

is not authorization.

______________________________________________________________________

### Unlimited Responses

Always paginate

large collections.

______________________________________________________________________

### Logging Sensitive Data

Logs should help debugging,

not leak secrets.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------- | ------------------- |
| HTTP | HTTPS |
| No authentication | JWT/OAuth2 |
| No authorization | RBAC / Ownership |
| No validation | Pydantic validation |
| Unlimited records | Pagination |
| Raw database models | Response models |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the key components of a secure REST API?

A secure REST API should use HTTPS, authenticate users, authorize every protected request, validate all incoming data,
return only necessary information through response models, implement rate limiting, paginate large datasets, protect
secrets, log security events without exposing sensitive information, and follow secure coding practices throughout the
request lifecycle.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What API Security is
- Authentication
- Authorization
- Validation
- Response models
- Rate limiting
- Pagination
- Versioning
- HTTPS
- Logging
- Secure API workflow

______________________________________________________________________

# What's Next

[CORS (Cross-Origin Resource Sharing)](19-cors.md)
