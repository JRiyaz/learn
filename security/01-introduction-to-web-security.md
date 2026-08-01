# Security - Part 1

# Introduction to Backend Security

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll understand:

- Why backend security matters
- The CIA Triad
- Authentication vs Authorization
- Trust Boundaries
- Defense in Depth
- Principle of Least Privilege
- Secure by Default
- The major security vulnerabilities we'll cover in this course

______________________________________________________________________

# Why Should Backend Developers Care About Security?

Imagine you've built a Library Management System.

Your backend provides APIs like:

```text
POST   /login

GET    /books

POST   /borrow

DELETE /books/123
```

Everything works perfectly.

But...

What if someone sends:

- Malicious input?
- Fake JWT tokens?
- Millions of requests?
- Requests pretending to be another user?
- SQL commands instead of usernames?

If your application trusts every request,

it will eventually be compromised.

Backend security is about **never trusting input by default**.

______________________________________________________________________

# The Security Mindset

One of the biggest mindset changes you'll make as a backend engineer is this:

> **Every request is potentially malicious until proven otherwise.**

Instead of asking:

> "How can I make this feature work?"

also ask:

> "How can this feature be abused?"

______________________________________________________________________

# Real-World Example

Suppose your API accepts this request.

```http
POST /login
```

Request Body

```json
{
    "username": "riyaz",
    "password": "password123"
}
```

A normal user sends valid data.

An attacker may instead send:

- Extremely long strings
- Unexpected data types
- Missing fields
- Modified JWTs
- Requests for another user's data

Your backend must safely handle all of these.

______________________________________________________________________

# Typical Backend Architecture

```text
                 Internet
                     │
                     ▼
              Client / Browser
                     │
                     ▼
             Load Balancer (Optional)
                     │
                     ▼
               FastAPI Backend
                │          │
                │          │
                ▼          ▼
             PostgreSQL   Redis
                     │
                     ▼
               Cloud Services
```

Every connection in this architecture is a potential attack surface.

______________________________________________________________________

# What is an Attack Surface?

An **attack surface** is any place where an attacker can interact with your system.

Examples:

- Login API
- Registration API
- File uploads
- Search endpoints
- Admin APIs
- Database queries
- External API calls
- WebSockets

The more entry points your application has,

the more carefully they must be secured.

______________________________________________________________________

# The CIA Triad

Almost every security concept is built around three goals.

```text
Confidentiality

↓

Integrity

↓

Availability
```

Let's understand each.

______________________________________________________________________

# Confidentiality

Only authorized users should access sensitive information.

Examples:

- Passwords
- Email addresses
- Credit card numbers
- Medical records
- JWT secrets

Example violation:

A user downloads another user's profile.

Confidentiality has failed.

______________________________________________________________________

# Integrity

Data should not be modified without authorization.

Example:

A student changes:

```text
Marks = 65
```

to

```text
Marks = 100
```

The data has been altered.

Integrity has been compromised.

______________________________________________________________________

# Availability

The system should remain available to legitimate users.

Example:

```text
Millions of Requests

↓

Server Overloaded

↓

Real Users Cannot Access API
```

Availability has failed.

______________________________________________________________________

# CIA Triad Summary

| Goal | Question |
| --------------- | --------------------------------------- |
| Confidentiality | Who can read the data? |
| Integrity | Who can modify the data? |
| Availability | Can legitimate users access the system? |

Almost every attack we'll study targets one or more of these goals.

______________________________________________________________________

# Authentication vs Authorization

These two terms are frequently confused.

______________________________________________________________________

## Authentication

Authentication answers:

> **Who are you?**

Examples:

- Username & Password
- JWT Token
- Google Login
- OAuth2

Example

```text
Login

↓

Identity Verified
```

______________________________________________________________________

## Authorization

Authorization answers:

> **What are you allowed to do?**

Example

```text
User

↓

Can Borrow Books

↓

Cannot Delete Books
```

Authentication comes first.

Authorization comes second.

______________________________________________________________________

# Real-World Example

Suppose Alice logs in.

Authentication confirms:

```text
This is Alice.
```

Authorization decides:

```text
Alice

✓ Borrow Books

✓ Return Books

✗ Delete Users

✗ Access Admin Panel
```

______________________________________________________________________

# Trust Boundaries

A trust boundary is where data moves from an untrusted source into your system.

Example

```text
Internet

↓

FastAPI

↓

Database
```

The Internet is **untrusted**.

Your backend is responsible for validating everything before it crosses the boundary.

Never assume client input is safe.

______________________________________________________________________

# Defense in Depth

Don't rely on a single security mechanism.

Instead,

use multiple layers.

```text
Firewall

↓

HTTPS

↓

Authentication

↓

Authorization

↓

Input Validation

↓

Parameterized SQL

↓

Database Permissions
```

If one layer fails,

another layer still protects the system.

______________________________________________________________________

# Principle of Least Privilege

Every user,

service,

and application

should have only the permissions they actually need.

Example

Instead of

```text
Database User

↓

Full Access
```

Prefer

```text
Application

↓

Read & Write Books

↓

Cannot Drop Database
```

Less privilege means less damage if something goes wrong.

______________________________________________________________________

# Secure by Default

A secure application should start in a secure configuration.

Examples:

Good Defaults

- HTTPS enabled
- Debug mode disabled
- Strong password hashing
- Secure cookies
- Parameterized SQL
- Authentication required
- Secrets stored outside source code

Avoid insecure defaults that require developers to remember to "turn security on."

______________________________________________________________________

# Never Trust User Input

One of the most important rules in backend development.

Everything coming from the client should be treated as untrusted.

Examples:

- Query parameters
- Path parameters
- Request bodies
- Headers
- Cookies
- Uploaded files

Validate,

sanitize where appropriate,

and verify before using the data.

______________________________________________________________________

# Security Vulnerabilities We'll Learn

During this module,

we'll cover:

- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Broken Authentication
- Broken Access Control
- JWT Security
- OAuth2
- Cryptographic Failures
- Security Misconfiguration
- Sensitive Data Exposure
- SSRF
- XXE (Overview)
- Insecure Deserialization
- Command Injection
- Path Traversal
- File Upload Security
- API Security
- CORS
- HTTPS & TLS
- Secrets Management
- Rate Limiting
- Logging & Monitoring
- Dependency Security
- Secure Docker
- Secure FastAPI Applications

By the end of this module,

you'll understand how each vulnerability works,

how to prevent it,

and how to implement secure solutions in Python and FastAPI.

______________________________________________________________________

# Common Security Principles

Whenever you build an API,

remember these principles:

- Never trust client input.
- Validate everything.
- Authenticate before authorizing.
- Use least privilege.
- Fail securely.
- Keep secrets out of source code.
- Log important security events.
- Keep dependencies updated.
- Assume attackers will try unexpected inputs.

These principles apply regardless of the programming language or framework.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the most important security principles for a backend developer?

A backend developer should never trust client input, should validate all incoming data, authenticate users before
authorizing access, follow the Principle of Least Privilege, implement Defense in Depth, use secure defaults, protect
sensitive data, and continuously monitor and update the application to reduce security risks.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Why backend security matters
- The security mindset
- Attack surfaces
- The CIA Triad
- Authentication vs Authorization
- Trust Boundaries
- Defense in Depth
- Principle of Least Privilege
- Secure by Default
- The roadmap for the security module

______________________________________________________________________

# What's Next

[SQL Injection](02-sql-injection.md)
