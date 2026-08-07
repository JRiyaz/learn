# Complete HTTP Request Lifecycle Deep Dive

## 17. Authentication Deep Dive

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand what authentication is, how it works in modern backend applications, different authentication mechanisms, the complete login flow, password hashing, JWT authentication, refresh tokens, and common security attacks.

______________________________________________________________________

# Introduction

The request has successfully passed

- Network
- Web Server
- Middleware
- Request Validation

Now,

the backend asks

a very important question.

```
Who is making this request?
```

This process is called

```
Authentication
```

______________________________________________________________________

# What is Authentication?

Interview favorite.

Authentication is the process of verifying

the identity

of a user.

Examples

- Username & Password
- JWT Token
- API Key
- OAuth Login
- Session Cookie
- Biometric Login

Authentication answers

```
Who are you?
```

______________________________________________________________________

# Authentication vs Authorization

Interview favorite.

Authentication

```
Who are you?
```

Authorization

```
What are you allowed to do?
```

Example

```
Login

↓

Authentication

↓

User Identified

↓

Authorization

↓

Can Delete User?
```

______________________________________________________________________

# Login Flow

```
Client

↓

POST /login

↓

Username & Password

↓

Backend

↓

Verify Credentials

↓

Generate Token

↓

Return Token

↓

Client Stores Token
```

______________________________________________________________________

# Example Login Request

```http
POST /login
```

```json
{
    "email": "riyaz@gmail.com",
    "password": "MyPassword123"
}
```

______________________________________________________________________

# Step 1

# Validate Request

Before authentication,

FastAPI validates

the request body.

```
JSON

↓

Pydantic Validation

↓

Python Object
```

If validation fails

```
422 Unprocessable Entity
```

______________________________________________________________________

# Step 2

# Find User

The backend queries

the database.

Example

```sql
SELECT *

FROM users

WHERE email='riyaz@gmail.com';
```

If the user

doesn't exist

return

```
401 Unauthorized
```

Avoid messages like

```
User not found
```

because they help

attackers enumerate

valid accounts.

______________________________________________________________________

# Step 3

# Password Verification

Interview favorite.

Passwords should

never

be stored

as plain text.

Database stores

only

the password hash.

Example

```
Password

↓

Hash Function

↓

Stored Hash
```

During login

```
Entered Password

↓

Hash Again

↓

Compare

↓

Match?
```

______________________________________________________________________

# Password Hashing Algorithms

Modern algorithms

- Argon2 ✅
- bcrypt ✅
- scrypt ✅

Avoid

- MD5 ❌
- SHA1 ❌

They are too fast

and unsuitable

for password storage.

______________________________________________________________________

# Why Not Store Plain Passwords?

Suppose

the database

is leaked.

If passwords

are stored

as plain text,

every account

is compromised.

Hashing

protects

user credentials.

______________________________________________________________________

# Salting

Interview favorite.

A random value

called

a salt

is added

before hashing.

```
Password

+

Random Salt

↓

Hash
```

Benefits

- Prevents rainbow table attacks
- Same password results in different hashes

______________________________________________________________________

# Step 4

# Generate Token

If credentials

are correct,

the backend

creates

an authentication token.

Popular choices

- JWT
- Session ID

______________________________________________________________________

# JWT (JSON Web Token)

Interview favorite.

A JWT has

three parts.

```
Header

.

Payload

.

Signature
```

Example

```
xxxxx.yyyyy.zzzzz
```

______________________________________________________________________

# JWT Payload

Example

```json
{
    "sub": "123",
    "email": "riyaz@gmail.com",
    "role": "admin",
    "exp": 1760000000
}
```

Common claims

- sub (User ID)
- exp (Expiration)
- iat (Issued At)
- iss (Issuer)
- aud (Audience)

______________________________________________________________________

# JWT Signature

The signature

ensures

the token

has not

been modified.

If someone

changes

the payload,

signature verification

fails.

______________________________________________________________________

# Step 5

# Return Token

Backend returns

```json
{
    "access_token": "...",
    "token_type": "Bearer"
}
```

______________________________________________________________________

# Step 6

# Store Token

The client

stores

the token.

Common options

- HttpOnly Cookie ✅
- Secure Cookie ✅
- Memory ✅
- localStorage (use carefully)

______________________________________________________________________

# Using the Token

Every protected request

includes

```
Authorization:

Bearer <token>
```

Example

```http
GET /profile
Authorization: Bearer eyJhbGci...
```

______________________________________________________________________

# Token Verification

For every request,

the backend

checks

- Signature
- Expiration
- Issuer
- Audience

If verification fails

```
401 Unauthorized
```

______________________________________________________________________

# Refresh Tokens

Interview favorite.

Access Tokens

should be

short-lived.

Example

```
15 Minutes
```

Refresh Tokens

last longer.

Example

```
30 Days
```

Flow

```
Access Token Expired

↓

Refresh Token

↓

New Access Token
```

______________________________________________________________________

# Why Use Refresh Tokens?

Benefits

- Better security
- Short-lived access tokens
- Better user experience

______________________________________________________________________

# Session-Based Authentication

Older applications

often use

sessions.

Flow

```
Login

↓

Create Session

↓

Store in Server

↓

Send Session ID Cookie
```

Every request

includes

the session cookie.

______________________________________________________________________

# JWT vs Session

| JWT | Session |
|------|----------|
| Stateless | Stateful |
| No server storage | Server stores session |
| Easy for microservices | Simpler for traditional apps |
| Better scalability | Easier revocation |

______________________________________________________________________

# API Key Authentication

Often used

for

machine-to-machine

communication.

Example

```http
X-API-Key: abc123
```

______________________________________________________________________

# OAuth 2.0

Used for

social login.

Examples

- Google
- GitHub
- Facebook
- Microsoft

Instead of

managing passwords,

your application

trusts

the identity provider.

______________________________________________________________________

# Multi-Factor Authentication (MFA)

Interview favorite.

Authentication requires

more than

one factor.

Examples

```
Password

+

OTP
```

or

```
Password

+

Authenticator App
```

Provides

additional security.

______________________________________________________________________

# Logout

JWTs

cannot always

be immediately revoked.

Common approaches

- Short expiration
- Refresh token revocation
- Token blacklist

Sessions

can simply

be deleted

from the server.

______________________________________________________________________

# Common Authentication Attacks

## Brute Force Attack

Attacker

tries

many passwords.

Mitigation

- Rate limiting
- Account lockout
- MFA

______________________________________________________________________

## Credential Stuffing

Uses

stolen credentials

from other websites.

Mitigation

- MFA
- Password monitoring

______________________________________________________________________

## Password Spray

One common password

against

many accounts.

Example

```
Welcome123
```

Mitigation

- Strong password policy
- MFA

______________________________________________________________________

## JWT Tampering

Attacker modifies

the JWT payload.

Mitigation

Always verify

the signature.

______________________________________________________________________

## Token Theft

If a token

is stolen,

the attacker

can impersonate

the user.

Mitigation

- HTTPS
- HttpOnly Cookies
- Short token lifetime

______________________________________________________________________

# Best Practices

- Always use HTTPS
- Hash passwords with Argon2 or bcrypt
- Use strong password policies
- Enable MFA
- Keep access tokens short-lived
- Rotate refresh tokens
- Never log passwords
- Never expose sensitive token data

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Password Hashing | Argon2, bcrypt |
| Token | JWT |
| Session Store | Redis |
| Social Login | OAuth 2.0 |
| Identity | OpenID Connect (OIDC) |
| MFA | TOTP, Authenticator Apps |

______________________________________________________________________

# Common Interview Questions

## Why hash passwords instead of encrypting them?

Passwords need to be verified, not decrypted. Hashing is a one-way operation, making it much safer if the database is
compromised.

______________________________________________________________________

## What is the difference between Authentication and Authorization?

Authentication verifies identity. Authorization determines what an authenticated user is allowed to access.

______________________________________________________________________

## Why use short-lived access tokens?

If an access token is stolen, its usefulness is limited because it expires quickly.

______________________________________________________________________

## Why is Argon2 preferred over SHA-256 for passwords?

Argon2 is intentionally slow and memory-intensive, making brute-force attacks much more difficult. SHA-256 is designed
to be fast, which is undesirable for password storage.

______________________________________________________________________

## What is the purpose of a Refresh Token?

A Refresh Token allows the client to obtain a new Access Token without requiring the user to log in again.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain the complete authentication flow in a modern backend application.

### Answer

The client submits login credentials to the backend. The request is validated, the user is looked up in the database,
and the submitted password is hashed and compared with the stored password hash. If the credentials are valid, the
server generates an access token (and often a refresh token) and returns it to the client. For subsequent requests, the
client includes the access token in the `Authorization` header. The backend verifies the token before allowing access to
protected resources.

______________________________________________________________________

# Summary

Authentication is responsible for verifying

the identity

of a user before allowing access

to protected resources.

Modern applications commonly use

- Password hashing
- JWT
- Refresh Tokens
- OAuth
- MFA

After a user is authenticated,

the next step is determining

**what they are allowed to do**, which is handled by **Authorization**.

______________________________________________________________________

# Next

[18. Authorization Deep Dive](18-authorization-deep-dive.md)
