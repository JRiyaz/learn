# Security Basics (Authentication & Authorization)

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 8 - Security
>
> **File:** `28_security_basics.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What API Security is
- Authentication
- Authorization
- Authentication vs Authorization
- Common Authentication Methods
- API Keys
- Session Authentication
- JWT Authentication
- OAuth2 Overview
- Production Best Practices

______________________________________________________________________

# Why API Security?

Every public API is exposed to the internet.

Without security

```
Internet

↓

Anyone

↓

Database
```

With security

```
Internet

↓

Authentication

↓

Authorization

↓

Business Logic
```

Security protects both data and services.

______________________________________________________________________

# Two Core Concepts

Security consists of two separate concerns.

```
Authentication

↓

Who Are You?
```

```
Authorization

↓

What Can You Do?
```

Both are required in most production systems.

______________________________________________________________________

# Authentication

Authentication verifies identity.

Example

```
Username

+

Password

↓

Verified User
```

or

```
Bearer Token

↓

Verified User
```

______________________________________________________________________

# Authorization

Authorization determines permissions.

Example

```
Authenticated User

↓

Role

↓

Allowed?

↓

Yes / No
```

______________________________________________________________________

# Authentication vs Authorization

Example

```
Alice

↓

Login

↓

Authenticated
```

Later

```
Alice

↓

Delete User

↓

Admin Only

↓

Denied
```

Alice is authenticated,

but not authorized.

______________________________________________________________________

# Common Authentication Methods

Modern APIs commonly use

- API Keys
- Session Authentication
- JWT Tokens
- OAuth2
- OpenID Connect (OIDC)

______________________________________________________________________

# API Keys

Client sends

```
X-API-Key:

abc123
```

Server verifies

```
Key Valid?

↓

Allow
```

Often used for

- Internal APIs
- Service-to-Service Communication
- Simple integrations

______________________________________________________________________

# API Key Flow

```
Client

↓

API Key

↓

Server

↓

Lookup

↓

Allow / Reject
```

______________________________________________________________________

# Session Authentication

Typical web application flow

```
Login

↓

Session Created

↓

Session ID Cookie

↓

Future Requests

↓

Session Lookup
```

The browser automatically sends the session cookie.

______________________________________________________________________

# Session Authentication Flow

```
Browser

↓

Cookie

↓

Server

↓

Database / Cache

↓

Current User
```

Common for traditional web applications.

______________________________________________________________________

# JWT Authentication

JWT stands for

```
JSON Web Token
```

Instead of storing a session,

the client stores a signed token.

______________________________________________________________________

# JWT Flow

```
Login

↓

JWT Created

↓

Client Stores Token

↓

Authorization Header

↓

Server Verifies Signature
```

No server-side session lookup is required.

______________________________________________________________________

# Authorization Header

Typical request

```
Authorization:

Bearer eyJhbGciOi...
```

FastAPI commonly extracts this header using dependencies.

______________________________________________________________________

# JWT Advantages

- Stateless
- Scalable
- Good for APIs
- Mobile Friendly
- Microservice Friendly

______________________________________________________________________

# JWT Disadvantages

- Revocation is harder
- Token expiration must be managed
- Sensitive if leaked
- Signature verification is required

______________________________________________________________________

# Session vs JWT

| Session | JWT |
|----------|-----|
| Server stores session | Client stores token |
| Cookie-based | Header-based |
| Easy revocation | Harder revocation |
| Stateful | Stateless |

______________________________________________________________________

# OAuth2

OAuth2 is an **authorization framework**.

Instead of giving your password to another application,

you grant limited access.

Example

```
Login with Google

↓

Google

↓

Access Token

↓

Application
```

______________________________________________________________________

# OAuth2 Flow

```
User

↓

Google

↓

Consent

↓

Access Token

↓

Application
```

The application never sees the user's Google password.

______________________________________________________________________

# OpenID Connect (OIDC)

OIDC builds on OAuth2

to provide user identity.

OAuth2

```
Authorization
```

OIDC

```
Authentication

+

Authorization
```

Many identity providers support OIDC.

______________________________________________________________________

# Roles

Authorization often uses roles.

Example

```
User

↓

Read Profile
```

```
Admin

↓

Delete User
```

______________________________________________________________________

# Permission Flow

```
Authenticated User

↓

Role

↓

Permission Check

↓

Business Logic
```

______________________________________________________________________

# Security Layers

```
HTTPS

↓

Authentication

↓

Authorization

↓

Validation

↓

Business Logic
```

Security is layered,

not a single feature.

______________________________________________________________________

# FastAPI Security Components

FastAPI provides built-in support for

- OAuth2
- HTTP Basic
- HTTP Bearer
- API Keys
- Security Dependencies

These will be explored in later chapters.

______________________________________________________________________

# Common Security Threats

- Stolen Tokens
- Weak Passwords
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Credential Stuffing
- Brute Force Attacks

Good authentication is only one part of application security.

______________________________________________________________________

# Common Mistakes

❌ Confusing authentication with authorization

❌ Sending tokens over HTTP instead of HTTPS

❌ Storing passwords in plain text

❌ Trusting client-provided roles

❌ Implementing authorization only in the frontend

______________________________________________________________________

# Production Best Practices

- Always use HTTPS.
- Authenticate every protected request.
- Authorize every sensitive action.
- Hash passwords using a strong password hashing algorithm.
- Keep JWTs short-lived.
- Validate API keys securely.
- Apply the principle of least privilege.

______________________________________________________________________

# Interview Deep Dive

### Question

**What is the difference between authentication and authorization?**

### Answer

Authentication answers the question,

**"Who are you?"**

It verifies the identity of the client.

Authorization answers the question,

**"What are you allowed to do?"**

It determines whether an authenticated user has permission to perform a specific action.

Authentication always happens before authorization because permissions cannot be evaluated until identity is
established.

______________________________________________________________________

# Summary

In this chapter you learned:

- API Security
- Authentication
- Authorization
- API Keys
- Session Authentication
- JWT Authentication
- OAuth2
- OpenID Connect
- Production Best Practices

Authentication verifies identity, authorization enforces permissions, and together they form the foundation of secure
FastAPI applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is API security?
1. What is authentication?
1. What is authorization?

______________________________________________________________________

## Authentication

4. What are common authentication methods?
1. How does API key authentication work?
1. How does session authentication work?
1. How does JWT authentication work?

______________________________________________________________________

## Authorization

8. Why is authorization performed after authentication?
1. What are roles and permissions?
1. Why shouldn't authorization be enforced only in the frontend?

______________________________________________________________________

## OAuth2

11. What is OAuth2?
01. What problem does OAuth2 solve?
01. How is OpenID Connect different from OAuth2?

______________________________________________________________________

## Production

14. Why should HTTPS always be used?
01. Why should JWTs have expiration times?

______________________________________________________________________

## Scenario-Based

16. A user successfully logs in but receives HTTP 403 when attempting to delete another user's account. What does this indicate about authentication and authorization?
01. Your backend trusts a `role=admin` value sent by the client. Why is this insecure?
01. Your API stores user passwords in plain text. What risks does this create, and what should be done instead?
01. Your organization is building a mobile application and wants stateless authentication that scales across many servers. Would sessions or JWTs be a better fit? Why?
01. Your application allows users to sign in with Google without sharing their Google password. Which protocol enables this workflow, and how does it improve security?

______________________________________________________________________

# Next

[OAuth2 & JWT Authentication](29_oauth2_jwt_authentication.md)
