# Security - Part 7

# JWT Security

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What JWT is
- JWT structure
- Common JWT security mistakes
- How to securely implement JWT in FastAPI
- Access Tokens vs Refresh Tokens
- Token expiration
- Token revocation
- Secret management
- Best practices

______________________________________________________________________

# What is JWT?

JWT stands for

**JSON Web Token**.

It is a compact,

digitally signed token

used to identify authenticated users.

Instead of storing session data on the server,

the server sends a signed token to the client.

Every future request includes that token.

______________________________________________________________________

# Typical JWT Authentication Flow

```text id="jwt701"
Login

↓

Verify Username & Password

↓

Generate JWT

↓

Client Stores JWT

↓

Every Request

↓

Verify JWT

↓

Access Protected Resource
```

______________________________________________________________________

# JWT Structure

A JWT has three parts.

```text id="jwt702"
Header

.

Payload

.

Signature
```

Example

```text id="jwt703"
xxxxx.yyyyy.zzzzz
```

______________________________________________________________________

# Header

The header describes

how the token was created.

Example

```json id="jwt704"
{
    "alg": "HS256",
    "typ": "JWT"
}
```

______________________________________________________________________

# Payload

The payload contains

claims.

Example

```json id="jwt705"
{
    "sub": "42",
    "username": "riyaz",
    "role": "admin",
    "exp": 1750000000
}
```

Notice

the payload is **not encrypted**.

Anyone holding the token

can decode it.

Never store sensitive data here.

______________________________________________________________________

# Signature

The signature ensures

the token has not been modified.

Workflow

```text id="jwt706"
Header

+

Payload

+

Secret Key

↓

Signature
```

If someone changes

the payload,

the signature becomes invalid.

______________________________________________________________________

# Important Rule

JWTs are **signed**,

not encrypted.

Anyone can read:

- Username
- User ID
- Roles
- Expiration time

Do **not** place secrets,

passwords,

or API keys

inside a JWT.

______________________________________________________________________

# Vulnerable Practice 1

## Never Trust the Payload Without Verification

Suppose a client sends

```text id="jwt707"
role = admin
```

Never trust it immediately.

First,

verify the JWT signature.

Then,

validate the claims.

______________________________________________________________________

# Secure Verification

Workflow

```text id="jwt708"
Receive JWT

↓

Verify Signature

↓

Check Expiration

↓

Extract User

↓

Authorize Request
```

Never skip verification.

______________________________________________________________________

# FastAPI Example

```python id="jwt709"
from jose import jwt, JWTError

payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

If verification fails,

reject the request.

______________________________________________________________________

# Vulnerable Practice 2

## Long-Lived Tokens

Bad Example

```text id="jwt710"
Token

↓

Valid Forever
```

If the token is stolen,

the attacker keeps access indefinitely.

______________________________________________________________________

# Better Approach

Use short-lived access tokens.

Example

```text id="jwt711"
Access Token

↓

15 Minutes
```

Then use

Refresh Tokens

to obtain new access tokens.

______________________________________________________________________

# Access Token vs Refresh Token

Access Token

```text id="jwt712"
Short Lifetime

↓

Access APIs
```

Refresh Token

```text id="jwt713"
Longer Lifetime

↓

Generate New Access Token
```

Typical workflow

```text id="jwt714"
Login

↓

Access Token (15 min)

+

Refresh Token (7 days)

↓

Access Token Expires

↓

Refresh Token

↓

New Access Token
```

This limits the damage

if an access token is stolen.

______________________________________________________________________

# Vulnerable Practice 3

## Weak Secret Keys

Bad Example

```python id="jwt715"
SECRET_KEY = "password"
```

or

```python id="jwt716"
SECRET_KEY = "123456"
```

These are easy to guess.

______________________________________________________________________

# Secure Secret

Use a long,

random,

cryptographically secure secret.

Example

```python id="jwt717"
import secrets

SECRET_KEY = secrets.token_hex(32)
```

Store it in:

- Environment variables
- Secret managers

Never hardcode it.

______________________________________________________________________

# Vulnerable Practice 4

## Hardcoding Secrets

Bad Example

```python id="jwt718"
SECRET_KEY = "my-super-secret-key"
```

committed to GitHub.

If the repository leaks,

every issued JWT can be forged.

______________________________________________________________________

# Secure Configuration

```python id="jwt719"
import os

SECRET_KEY = os.getenv("JWT_SECRET")
```

Even better,

use:

- Docker Secrets
- AWS Secrets Manager
- HashiCorp Vault

We'll cover these later.

______________________________________________________________________

# Vulnerable Practice 5

## Missing Expiration

Every JWT should contain

```text id="jwt720"
exp
```

Example

```python id="jwt721"
from datetime import datetime, timedelta

expire = datetime.utcnow() + timedelta(minutes=15)
```

Expired tokens

must be rejected.

______________________________________________________________________

# Vulnerable Practice 6

## No Revocation Strategy

Suppose a user logs out.

If the JWT is still valid,

it can still be used.

Possible solutions:

- Token blacklist (Redis)
- Token versioning
- Refresh token rotation

______________________________________________________________________

# Refresh Token Rotation

Instead of reusing

the same refresh token forever,

issue a new refresh token

each time one is used.

Workflow

```text id="jwt722"
Refresh Token

↓

Generate New Access Token

↓

Generate New Refresh Token

↓

Old Refresh Token Invalid
```

This reduces the impact

of stolen refresh tokens.

______________________________________________________________________

# JWT Middleware

In FastAPI,

authentication usually happens

before the endpoint executes.

```text id="jwt723"
Request

↓

JWT Verification

↓

Current User

↓

Endpoint
```

Endpoints should never manually decode JWTs repeatedly.

Use dependencies or middleware.

______________________________________________________________________

# Defense in Depth

Secure JWT authentication combines:

```text id="jwt724"
HTTPS

↓

Strong Secret

↓

JWT Signature

↓

Expiration

↓

Authorization

↓

Refresh Token

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Use HTTPS.

✅ Verify every JWT.

✅ Use short-lived access tokens.

✅ Use refresh tokens.

✅ Store secrets securely.

✅ Never put sensitive information inside JWT payloads.

✅ Validate expiration.

✅ Implement logout/revocation.

______________________________________________________________________

# Common Mistakes

### Storing Passwords Inside JWT

JWT payloads are readable.

Never store:

- Passwords
- API Keys
- Secrets

______________________________________________________________________

### Hardcoding Secret Keys

Always load secrets

from secure configuration.

______________________________________________________________________

### Never Expiring Tokens

Every JWT should expire.

______________________________________________________________________

### Skipping Signature Verification

Never trust

the payload

before verifying the signature.

______________________________________________________________________

### Using One Token Forever

Use:

- Access Tokens
- Refresh Tokens
- Rotation

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ----------------- | ------------------------------------- |
| Hardcoded secret | Environment variable / Secret manager |
| Permanent token | Short-lived access token |
| No refresh token | Refresh token rotation |
| Sensitive payload | Minimal claims |
| Skip verification | Verify signature every request |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the security best practices for JWT authentication?

JWTs should always be signed with a strong secret or private key, verified on every request, transmitted only over
HTTPS, and configured with short expiration times. Sensitive information should never be stored in the payload because
it is only encoded, not encrypted. Applications should use refresh tokens for long-lived sessions, securely manage
secrets, support token revocation or rotation, and perform authorization checks after successful authentication.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What JWT is
- JWT structure
- Signature verification
- Access vs Refresh Tokens
- Secret management
- Token expiration
- Token revocation
- Refresh token rotation
- FastAPI JWT workflow
- Best practices

______________________________________________________________________

# What's Next

[OAuth2 for Backend Developers](08-oauth2.md)
