# OAuth2 & JWT Authentication

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 8 - Security
>
> **File:** `29_oauth2_jwt_authentication.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- OAuth2 in FastAPI
- JWT Authentication Flow
- Access Tokens
- Refresh Tokens
- OAuth2PasswordBearer
- Token Generation
- Token Verification
- Protecting Routes
- Token Expiration
- Production Best Practices

______________________________________________________________________

# Why JWT Authentication?

Imagine a distributed application.

```
Client

↓

Server 1

↓

Server 2

↓

Server 3
```

Using server-side sessions,

every server must share session state.

JWT removes this requirement.

```
Client

↓

JWT

↓

Any Server

↓

Verify Signature

↓

Authenticated
```

______________________________________________________________________

# JWT Authentication Flow

```
User Login

↓

Username & Password

↓

Verify Credentials

↓

Generate JWT

↓

Return Token

↓

Client Stores Token

↓

Authorization Header

↓

Protected API

↓

Verify Token

↓

Current User
```

______________________________________________________________________

# JWT Structure

A JWT has three parts.

```
Header

.

Payload

.

Signature
```

Example

```
xxxxx

.

yyyyy

.

zzzzz
```

Each section is Base64URL encoded.

______________________________________________________________________

# JWT Header

Contains metadata.

Example

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

______________________________________________________________________

# JWT Payload

Contains claims.

Example

```json
{
    "sub": "riyaz",

    "role": "admin",

    "exp": 1750000000
}
```

Typical claims

- `sub` (Subject)
- `exp` (Expiration)
- `iat` (Issued At)
- `nbf` (Not Before)

______________________________________________________________________

# JWT Signature

```
Header

+

Payload

+

Secret Key

↓

Signature
```

The server verifies the signature to detect tampering.

______________________________________________________________________

# Access Token

Access tokens are

- Short-lived
- Sent with every request
- Used to access protected resources

Typical lifetime

```
5 Minutes

↓

1 Hour
```

depending on application requirements.

______________________________________________________________________

# Refresh Token

Refresh tokens are

- Longer-lived
- Used to obtain new access tokens
- Not sent with every API request

Typical flow

```
Access Token Expires

↓

Refresh Token

↓

New Access Token
```

______________________________________________________________________

# OAuth2PasswordBearer

FastAPI provides

```python
OAuth2PasswordBearer
```

Import

```python
from fastapi.security import OAuth2PasswordBearer
```

______________________________________________________________________

# Create OAuth2 Scheme

```python
oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="login"
)
```

`tokenUrl` points to the endpoint that issues tokens.

______________________________________________________________________

# Using the Dependency

```python
@app.get("/profile")

def profile(

    token: str = Depends(

        oauth2_scheme

    )

):

    return {

        "token": token

    }
```

FastAPI extracts the bearer token automatically.

______________________________________________________________________

# Incoming Request

```
Authorization:

Bearer eyJhbGciOi...
```

Dependency

↓

```
Token String
```

The dependency does **not** verify the token.

It only extracts it.

______________________________________________________________________

# Login Endpoint

Typical flow

```
Username

↓

Password

↓

Verify Credentials

↓

Generate JWT

↓

Return Access Token
```

______________________________________________________________________

# Generating a JWT

Common libraries

- `python-jose`
- `PyJWT`

Example (conceptual)

```python
token = jwt.encode(

    payload,

    SECRET_KEY,

    algorithm="HS256"
)
```

______________________________________________________________________

# Verifying a JWT

Example (conceptual)

```python
payload = jwt.decode(

    token,

    SECRET_KEY,

    algorithms=["HS256"]
)
```

Verification checks

- Signature
- Expiration
- Claims

______________________________________________________________________

# Authentication Dependency

Typical flow

```python
def get_current_user(

    token = Depends(

        oauth2_scheme

    )

):

    payload = verify_token(

        token

    )

    return payload
```

Protected routes depend on `get_current_user()`,

not directly on the raw token.

______________________________________________________________________

# Route Protection

```
Request

↓

Bearer Token

↓

OAuth2 Dependency

↓

Verify JWT

↓

Current User

↓

Route
```

______________________________________________________________________

# Expired Tokens

If

```
exp

↓

Past Time
```

Verification fails.

Response

```
401 Unauthorized
```

The client should obtain a new access token.

______________________________________________________________________

# Invalid Signature

If the token is modified,

the signature no longer matches.

```
JWT

↓

Signature Check

↓

Fail

↓

401
```

The request is rejected.

______________________________________________________________________

# Missing Token

Request

```
GET /profile
```

Without

```
Authorization
```

FastAPI automatically returns

```
401 Unauthorized
```

when using `OAuth2PasswordBearer`.

______________________________________________________________________

# Authorization Flow

```
JWT

↓

Current User

↓

Role

↓

Permission Check

↓

Business Logic
```

Authentication establishes identity.

Authorization checks permissions.

______________________________________________________________________

# Access vs Refresh Tokens

| Access Token | Refresh Token |
|--------------|---------------|
| Short-lived | Long-lived |
| Used frequently | Used rarely |
| Access resources | Issue new access tokens |
| Expires quickly | Better protected |

______________________________________________________________________

# Token Storage

Common approaches

Browser

- HttpOnly Cookies
- Memory (depending on architecture)

Mobile

- Secure platform storage

Avoid storing sensitive tokens in insecure locations.

______________________________________________________________________

# Secret Keys

Never hard-code secrets.

Bad

```python
SECRET_KEY = "12345"
```

Better

```
Environment Variables

↓

Secrets Manager

↓

Configuration
```

______________________________________________________________________

# Production Flow

```
Login

↓

Verify Password

↓

Generate Access Token

↓

Generate Refresh Token

↓

Return Both

↓

Protected APIs

↓

Refresh When Needed
```

______________________________________________________________________

# Common Mistakes

❌ Storing passwords inside JWTs

❌ Creating tokens without expiration

❌ Hard-coding secret keys

❌ Trusting JWT payloads without verifying the signature

❌ Using very long-lived access tokens

______________________________________________________________________

# Production Best Practices

- Use HTTPS.
- Keep access tokens short-lived.
- Verify every JWT signature.
- Store secret keys securely.
- Use refresh tokens for long-lived sessions.
- Include only necessary claims.
- Protect sensitive routes with dependencies.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are access tokens usually short-lived while refresh tokens are long-lived?**

### Answer

Access tokens are sent with almost every authenticated request.

If an access token is compromised,

a short expiration limits the attack window.

Refresh tokens are used much less frequently and can issue new access tokens after successful validation.

This design balances

- Security
- User experience
- Scalability

by reducing repeated logins while limiting exposure from leaked access tokens.

______________________________________________________________________

# Summary

In this chapter you learned:

- OAuth2PasswordBearer
- JWT Structure
- Access Tokens
- Refresh Tokens
- Token Generation
- Token Verification
- Protected Routes
- Authentication Flow
- Production Best Practices

JWT-based authentication enables scalable, stateless APIs by allowing servers to verify user identity without
maintaining server-side session state.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is JWT?
1. Why is JWT considered stateless?
1. What are the three parts of a JWT?

______________________________________________________________________

## OAuth2

4. What is `OAuth2PasswordBearer`?
1. What does `tokenUrl` represent?
1. Does `OAuth2PasswordBearer` verify JWT signatures?

______________________________________________________________________

## JWT

7. What information is typically stored in the JWT payload?
1. Why is the JWT signature important?
1. What happens if the payload is modified?

______________________________________________________________________

## Tokens

10. What is the difference between access tokens and refresh tokens?
01. Why should access tokens expire quickly?
01. Why shouldn't passwords be stored inside JWTs?

______________________________________________________________________

## Security

13. Why should secret keys never be hard-coded?
01. Why should JWTs always be transmitted over HTTPS?
01. Why should every protected request verify the JWT signature?

______________________________________________________________________

## Scenario-Based

16. Your API accepts a bearer token but never verifies its signature. What security vulnerability does this introduce?
01. A user's access token expires while using your application. How can refresh tokens improve the user experience?
01. Your application uses a single access token that never expires. What are the security risks?
01. Your backend is deployed behind multiple load-balanced servers. Why is JWT authentication often preferred over server-side sessions in this architecture?
01. Your FastAPI endpoint currently reads the `Authorization` header manually. How does `OAuth2PasswordBearer` and a dedicated authentication dependency improve the design?

______________________________________________________________________

# Next

[Database Integration (SQLAlchemy)](30_database_integration_sqlalchemy.md)
