# Security - Part 8

# OAuth2 for Backend Developers

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What OAuth2 is
- Why OAuth2 exists
- OAuth2 vs JWT
- The major OAuth2 roles
- Authorization Code Flow (high level)
- Access Tokens & Refresh Tokens
- OAuth2 in FastAPI
- Best practices

______________________________________________________________________

# Why Was OAuth2 Created?

Imagine this situation.

A website says:

```text id="oauth801"
Login with Google
```

You click the button.

The application **never asks for your Google password**.

Instead,

Google authenticates you.

This is the main idea behind OAuth2.

______________________________________________________________________

# What is OAuth2?

OAuth2 is an **authorization framework**.

It allows one application to access resources from another application **without sharing the user's password**.

Important:

OAuth2 is **not** a token format.

It is **not** JWT.

It is a protocol that defines how authorization works.

______________________________________________________________________

# Real-World Example

Suppose you're using Spotify.

You click

```text id="oauth802"
Login with Google
```

Workflow

```text id="oauth803"
User

↓

Spotify

↓

Google Login

↓

Google Verifies User

↓

Google Issues Token

↓

Spotify Receives User Information
```

Spotify never knows your Google password.

______________________________________________________________________

# OAuth2 Roles

OAuth2 defines four important roles.

```text id="oauth804"
Resource Owner

↓

Client

↓

Authorization Server

↓

Resource Server
```

Let's understand each.

______________________________________________________________________

# Resource Owner

The Resource Owner

is usually

the user.

Example

```text id="oauth805"
Riyaz
```

The user owns

their Google account,

GitHub account,

or Microsoft account.

______________________________________________________________________

# Client

The Client

is the application

requesting access.

Example

```text id="oauth806"
Library App

Spotify

Notion
```

______________________________________________________________________

# Authorization Server

This server

authenticates the user

and issues tokens.

Examples

```text id="oauth807"
Google

GitHub

Microsoft

Auth0
```

______________________________________________________________________

# Resource Server

This server

contains protected resources.

Example

```text id="oauth808"
Google Drive

Google Calendar

GitHub API
```

Access requires

a valid access token.

______________________________________________________________________

# Authorization Code Flow

This is the most common OAuth2 flow.

```text id="oauth809"
User

↓

Client

↓

Authorization Server

↓

Login

↓

Authorization Code

↓

Access Token

↓

Protected Resource
```

This is the flow used by:

- Google Login
- GitHub Login
- Microsoft Login

______________________________________________________________________

# Simplified Flow

Let's walk through it.

______________________________________________________________________

## Step 1

User clicks

```text id="oauth810"
Login with Google
```

______________________________________________________________________

## Step 2

Browser redirects to Google.

```text id="oauth811"
Application

↓

Google Login
```

______________________________________________________________________

## Step 3

User authenticates.

Google verifies

the username,

password,

and any additional security checks.

______________________________________________________________________

## Step 4

Google asks

for permission.

Example

```text id="oauth812"
Allow Library App

to view your email?
```

The user chooses:

Allow

or

Deny.

______________________________________________________________________

## Step 5

Google sends

an Authorization Code

back to the application.

______________________________________________________________________

## Step 6

The application exchanges

that code

for an Access Token.

______________________________________________________________________

## Step 7

The application uses

the Access Token

to access protected resources.

______________________________________________________________________

# OAuth2 vs JWT

This is a common interview question.

| OAuth2 | JWT |
| --------------------------- | ----------------------------- |
| Authorization protocol | Token format |
| Defines authentication flow | Stores user claims |
| Can issue JWTs | Often used within OAuth2 |
| Supports third-party login | Represents authenticated user |

OAuth2 and JWT

often work together,

but they are different things.

______________________________________________________________________

# OAuth2 Tokens

OAuth2 commonly uses

```text id="oauth813"
Access Token

↓

Refresh Token
```

Exactly like we discussed

in the previous lesson.

The Access Token

may be a JWT,

or it may be an opaque token,

depending on the provider.

______________________________________________________________________

# OAuth2 in FastAPI

FastAPI includes support

for OAuth2.

Example

```python id="oauth814"
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)
```

This dependency extracts

the Bearer token

from the Authorization header.

It does **not**

verify the token.

Your application

still needs to validate it.

______________________________________________________________________

# OAuth2 Password Flow

FastAPI documentation often demonstrates

the Password Flow.

```text id="oauth815"
Username

↓

Password

↓

JWT

↓

Protected API
```

This is useful

for learning,

but many production applications instead use:

- Authorization Code Flow
- OpenID Connect
- External identity providers

______________________________________________________________________

# OpenID Connect (OIDC)

OAuth2 answers:

```text id="oauth816"
Can this application access the resource?
```

OpenID Connect answers:

```text id="oauth817"
Who is this user?
```

Many modern systems

use:

```text id="oauth818"
OAuth2

+

OpenID Connect
```

When people say

"Login with Google,"

they're usually referring to

OAuth2 combined with OpenID Connect.

______________________________________________________________________

# Best Practices

✅ Use trusted identity providers.

✅ Use HTTPS.

✅ Validate every Access Token.

✅ Store tokens securely.

✅ Use short-lived Access Tokens.

✅ Rotate Refresh Tokens.

✅ Never expose client secrets.

______________________________________________________________________

# Common Mistakes

### Thinking OAuth2 Is JWT

OAuth2 defines

how authorization works.

JWT is simply

one possible token format.

______________________________________________________________________

### Skipping Token Validation

Receiving a token

doesn't mean

it's valid.

Always verify it.

______________________________________________________________________

### Hardcoding Client Secrets

Treat OAuth client secrets

like passwords.

Store them securely.

______________________________________________________________________

### Sending Tokens Over HTTP

Always use HTTPS.

OAuth tokens

must never travel

over insecure connections.

______________________________________________________________________

# Quick Comparison

| Authentication Method | Typical Use Case |
| --------------------- | ------------------------------------ |
| Username & Password | Traditional login |
| JWT | API authentication |
| OAuth2 | Third-party authorization |
| OAuth2 + OIDC | Login with Google, GitHub, Microsoft |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between OAuth2 and JWT?

OAuth2 is an authorization framework that defines how applications obtain permission to access protected resources on
behalf of a user. JWT (JSON Web Token) is a token format used to carry claims about a user or client. OAuth2 may issue
JWTs as access tokens, but it can also use other token formats. In short, OAuth2 defines the process, while JWT is one
possible way of representing the resulting token.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What OAuth2 is
- Why OAuth2 exists
- OAuth2 roles
- Authorization Code Flow
- OAuth2 vs JWT
- OAuth2 in FastAPI
- OpenID Connect
- Best practices

______________________________________________________________________

# What's Next

[Cryptographic Failures](09-cryptographic-failures.md)
