# System Design - Part 65

# Authentication & Authorization

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Authentication vs Authorization
- Identity
- Credentials
- Sessions
- Cookies
- JWT (JSON Web Token)
- OAuth 2.0
- OpenID Connect (OIDC)
- API Keys
- RBAC & ABAC
- Authentication Flow
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

has

three users.

- Member
- Librarian
- Administrator

A member

logs in

and

tries

to delete

the entire database.

Question.

Should

the system

allow it?

Of course not.

Before

allowing

any action,

the system

must answer

two questions.

1. Who are you?
1. What are you allowed to do?

These are

Authentication

and

Authorization.

______________________________________________________________________

# The Problem

Suppose

someone

calls

our API.

```text id="auth6501"
DELETE

/books/101
```

How do

we know

who

made

the request?

Without authentication,

anyone

can access

our APIs.

______________________________________________________________________

# Another Problem

Suppose

the user

is authenticated.

Does that mean

they should

be allowed

to perform

every action?

No.

Being identified

is different

from

having permission.

______________________________________________________________________

# Authentication

**Authentication**

answers

the question:

> **Who are you?**

Examples:

- Username & Password
- Google Login
- GitHub Login
- Face ID
- Fingerprint
- OTP

Authentication

verifies

identity.

______________________________________________________________________

# Authorization

**Authorization**

answers

the question:

> **What are you allowed to do?**

Example

A Librarian

can

issue books.

A Member

cannot.

Authorization

checks

permissions.

______________________________________________________________________

# Authentication vs Authorization

Interview favorite.

| Authentication | Authorization |
| --------------------- | ---------------------------- |
| Who are you? | What can you do? |
| Identity verification | Permission verification |
| Happens first | Happens after authentication |

______________________________________________________________________

# Typical Request Flow

```text id="auth6502"
Login

↓

Authentication

↓

Token

↓

API Request

↓

Authorization

↓

Response
```

Both

steps

are required.

______________________________________________________________________

# Credentials

Credentials

prove

a user's identity.

Examples:

- Username
- Password
- OTP
- API Key
- Biometric Data

Never store

passwords

in plain text.

______________________________________________________________________

# Password Hashing

Interview favorite.

Passwords

should be

hashed

before

being stored.

```text id="auth6503"
Password

↓

Hash

↓

Database
```

Popular algorithms:

- bcrypt
- Argon2
- scrypt

Never

store

plain-text passwords.

______________________________________________________________________

# Session-Based Authentication

Traditional web applications

often use

Sessions.

Workflow

```text id="auth6504"
Login

↓

Session Created

↓

Session ID

↓

Cookie
```

The browser

stores

only

the Session ID.

The server

stores

the session data.

______________________________________________________________________

# Cookies

A **Cookie**

is

a small piece

of data

stored

by

the browser.

Example

```text id="auth6505"
session_id=abc123
```

The browser

automatically sends

the cookie

with

future requests.

______________________________________________________________________

# JWT (JSON Web Token)

Modern APIs

often use

JWT.

Workflow

```text id="auth6506"
Login

↓

JWT

↓

Client

↓

API Requests
```

The server

doesn't need

to store

session state.

______________________________________________________________________

# JWT Structure

Interview favorite.

A JWT

contains

three parts.

```text id="auth6507"
Header

.

Payload

.

Signature
```

The Signature

prevents

tampering.

______________________________________________________________________

# JWT Payload

Example

```json id="auth6508"
{
  "user_id": 101,
  "role": "member"
}
```

The payload

should not

contain

sensitive data,

because

it can be decoded.

______________________________________________________________________

# JWT Expiration

JWTs

should expire.

Example

```text id="auth6509"
Expires

15 Minutes
```

Short-lived tokens

reduce

security risks.

______________________________________________________________________

# Refresh Tokens

Instead of

making

Access Tokens

last forever,

use

Refresh Tokens.

Workflow

```text id="auth6510"
Login

↓

Access Token

15 min

↓

Refresh Token

30 days
```

When

the Access Token

expires,

the client

uses

the Refresh Token

to obtain

a new one.

______________________________________________________________________

# API Keys

Some services

authenticate

applications,

not users.

Example

```text id="auth6511"
API-Key:

abc123
```

Commonly used

for:

- Internal APIs
- Third-party integrations
- Server-to-server communication

______________________________________________________________________

# OAuth 2.0

Interview favorite.

OAuth 2.0

allows

users

to grant

limited access

to

another application

without

sharing

their password.

Example

```text id="auth6512"
Login with Google
```

Your application

never sees

the user's

Google password.

______________________________________________________________________

# OpenID Connect (OIDC)

OIDC

is built

on top of

OAuth 2.0.

OAuth

provides

authorization.

OIDC

adds

authentication

and

identity information.

Example

```text id="auth6513"
Login with Microsoft
```

______________________________________________________________________

# RBAC

Role-Based Access Control.

Permissions

are assigned

to

roles.

Example

```text id="auth6514"
Admin

↓

All Permissions
```

```text id="auth6515"
Member

↓

Read Books
```

Simple

and widely used.

______________________________________________________________________

# ABAC

Attribute-Based Access Control.

Permissions

depend

on

attributes.

Examples:

- Department
- Country
- Resource Owner
- Time
- Device

ABAC

is more flexible

than RBAC,

but

also

more complex.

______________________________________________________________________

# Authentication Flow

```text id="auth6516"
Client

↓

Login

↓

Identity Verified

↓

JWT Issued

↓

Protected API

↓

Authorization Check
```

______________________________________________________________________

# FastAPI Example

Suppose

a client

calls

```python id="auth6517"
GET /books
```

FastAPI

extracts

the JWT,

verifies

its signature,

checks

expiration,

and

loads

the user.

Only then

does

the endpoint

execute.

______________________________________________________________________

# Microservices Example

Suppose

the API Gateway

authenticates

the user.

```text id="auth6518"
Client

↓

API Gateway

↓

JWT Verified

↓

Loan Service

↓

Notification Service
```

Downstream services

receive

the user's identity

without

requiring

another login.

______________________________________________________________________

# AI/ML Example

Suppose

an LLM platform

offers

different models.

Basic users

can access

smaller models.

Enterprise users

can access

premium models.

Authentication

identifies

the customer.

Authorization

determines

which models

they may use.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

A customer

logs in

and

receives

a JWT.

Every request

includes

the token.

When

the customer

attempts

to cancel

another user's order,

Authorization

rejects

the request.

______________________________________________________________________

# Session vs JWT

Interview favorite.

| Session | JWT |
| --------------------- | ------------------- |
| Server stores session | Client stores token |
| Stateful | Stateless |
| Easy revocation | Better scalability |
| Common in web apps | Common in APIs |

Neither

is always better.

Choose

based on

system requirements.

______________________________________________________________________

# OAuth vs JWT

Another

interview favorite.

| OAuth 2.0 | JWT |
| ----------------------- | -------------- |
| Authorization framework | Token format |
| Delegates access | Carries claims |
| Often uses JWT | Not required |

OAuth

and JWT

solve

different problems.

______________________________________________________________________

# Benefits

Modern authentication provides:

✅ Secure identity verification

✅ Fine-grained permissions

✅ Scalable APIs

✅ Third-party login support

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Token management

❌ Key rotation

❌ Session expiration

❌ Authorization complexity

______________________________________________________________________

# When NOT to Use JWT

Avoid JWT

when:

- Sessions

are sufficient

- Immediate token revocation

is critical

- Simple server-rendered

applications

benefit

from

traditional sessions

______________________________________________________________________

# Best Practices

✅ Hash passwords.

✅ Use HTTPS.

✅ Keep Access Tokens short-lived.

✅ Store secrets securely.

✅ Apply the Principle of Least Privilege.

______________________________________________________________________

# Common Mistakes

### Storing Passwords in Plain Text

Always

store

password hashes,

never

raw passwords.

______________________________________________________________________

### Long-Lived Tokens

Access Tokens

should expire

quickly.

Use

Refresh Tokens

instead.

______________________________________________________________________

### Trusting JWT Without Verification

Always verify:

- Signature
- Expiration
- Issuer
- Audience

before

accepting

a token.

______________________________________________________________________

### Confusing Authentication with Authorization

A user

may be

authenticated,

yet

still

lack permission

to perform

an action.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between Authentication and Authorization?

Authentication verifies a user's identity by answering the question, "Who are you?" It typically uses credentials such
as passwords, OTPs, biometrics, or third-party identity providers. Authorization determines what an authenticated user
is allowed to do by checking permissions, roles, or policies. Authentication always happens before authorization. In
modern distributed systems, authentication is commonly implemented using sessions, JWTs, OAuth 2.0, or OpenID Connect,
while authorization is often implemented using Role-Based Access Control (RBAC) or Attribute-Based Access Control
(ABAC).

______________________________________________________________________

# Summary

In this lesson, you learned:

- Authentication
- Authorization
- Sessions
- Cookies
- JWT
- Refresh Tokens
- OAuth 2.0
- OpenID Connect
- RBAC
- ABAC
- Best practices

______________________________________________________________________

# 🧠 Security Progress

You have started the **Security** module:

- ✅ Authentication & Authorization

Next, we'll cover one of the most frequently asked backend interview topics and one of the most important production
protections:

> **Rate Limiting**

______________________________________________________________________

# What's Next

[Rate Limiting](66-rate-limiting.md)
