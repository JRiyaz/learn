# Security - Part 28

# Basic Authentication

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Basic Authentication is
- How it works
- Base64 encoding
- Why HTTPS is mandatory
- Basic Auth in FastAPI
- Basic Auth vs JWT
- When to use Basic Auth
- Best practices

______________________________________________________________________

# What is Basic Authentication?

Basic Authentication (Basic Auth) is one of the oldest HTTP authentication mechanisms.

The client sends:

- Username
- Password

with **every request**.

Unlike JWT,

the server usually verifies the username and password on every request.

______________________________________________________________________

# Typical Flow

```text id="ba2801"
Client

↓

Username + Password

↓

Server

↓

Verify Credentials

↓

Allow Request
```

Every protected request includes the credentials.

______________________________________________________________________

# How Does Basic Auth Work?

Suppose the user enters

```text id="ba2802"
Username

riyaz

Password

password123
```

These are combined into one string.

```text id="ba2803"
riyaz:password123
```

The string is then encoded using

```text id="ba2804"
Base64
```

Example

```text id="ba2805"
cml5YXo6cGFzc3dvcmQxMjM=
```

Finally,

the client sends

```http id="ba2806"
Authorization:

Basic cml5YXo6cGFzc3dvcmQxMjM=
```

______________________________________________________________________

# Important Misconception

Many beginners think

Base64 means encryption.

It does **not**.

Base64 is simply

an encoding format.

Anyone can decode it.

Example

```text id="ba2807"
Base64

↓

Decode

↓

Original Username & Password
```

Because of this,

Basic Authentication **must always use HTTPS**.

______________________________________________________________________

# HTTP vs HTTPS

Using Basic Auth over HTTP

is extremely dangerous.

```text id="ba2808"
Username

↓

Password

↓

Internet

↓

Visible
```

Using HTTPS

```text id="ba2809"
Username

↓

Password

↓

TLS Encryption

↓

Protected
```

Without HTTPS,

an attacker can capture the credentials.

______________________________________________________________________

# FastAPI Example

FastAPI provides built-in support.

```python id="ba2810"
from fastapi.security import HTTPBasic

security = HTTPBasic()
```

Using it

```python id="ba2811"
from fastapi import Depends

@app.get("/profile")
def profile(
    credentials = Depends(security)
):
    ...
```

FastAPI extracts

the username

and password

from the Authorization header.

Your application still needs to verify them.

______________________________________________________________________

# Credential Verification

Typical workflow

```text id="ba2812"
Receive Credentials

↓

Lookup User

↓

Verify Password Hash

↓

Return Response
```

Passwords should still be stored

using bcrypt or Argon2,

never in plain text.

______________________________________________________________________

# Basic Auth vs JWT

| Basic Auth | JWT |
| ----------------------------------------- | -------------------------- |
| Username & password sent every request | Token sent every request |
| Server verifies credentials every request | Server verifies token |
| No logout mechanism | Token expiration supported |
| Stateless | Usually stateless |
| Simpler | More flexible |

JWT is generally preferred

for modern web applications.

______________________________________________________________________

# Basic Auth vs Session Authentication

| Basic Auth | Sessions |
| --------------------------------- | ------------------------ |
| Credentials sent every request | Session ID sent |
| Server checks password repeatedly | Server checks session |
| No server session storage | Session stored on server |
| Simpler | Better user experience |

______________________________________________________________________

# When Should You Use Basic Auth?

Basic Auth is still useful for:

- Internal APIs
- Small internal tools
- Development environments
- Simple administration panels
- CI/CD systems
- Reverse proxy authentication

It is generally **not recommended** for public web applications where users log in through a browser.

______________________________________________________________________

# When Should You NOT Use It?

Avoid Basic Auth for:

- Mobile applications
- Public REST APIs
- Large consumer applications
- Applications requiring logout
- Applications needing token expiration
- Single Sign-On (SSO)

JWT or OAuth2 are usually better choices.

______________________________________________________________________

# Browser Behavior

Browsers recognize

Basic Authentication automatically.

When a protected endpoint returns

```http id="ba2813"
401 Unauthorized
```

with

```http id="ba2814"
WWW-Authenticate: Basic
```

the browser displays

its built-in login dialog.

This behavior is useful for simple admin interfaces

but not ideal for modern web applications.

______________________________________________________________________

# Security Considerations

Basic Auth has several limitations.

- Credentials are sent with every request.
- No built-in expiration.
- No refresh tokens.
- No logout mechanism.
- Difficult to revoke without changing the password.

Because of these limitations,

modern applications usually prefer JWT or OAuth2.

______________________________________________________________________

# Defense in Depth

Secure Basic Authentication uses:

```text id="ba2815"
HTTPS

↓

Strong Password Hashing

↓

Rate Limiting

↓

Authentication

↓

Authorization

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Always use HTTPS.

✅ Store passwords using bcrypt or Argon2.

✅ Rate limit login attempts.

✅ Use strong passwords.

✅ Return generic authentication errors.

✅ Use Basic Auth only where appropriate.

______________________________________________________________________

# Common Mistakes

### Thinking Base64 Is Encryption

Base64 provides

no security.

It simply changes the representation of data.

______________________________________________________________________

### Using HTTP

Basic Authentication

without HTTPS

exposes usernames and passwords.

______________________________________________________________________

### Storing Plain-Text Passwords

Always hash passwords

before storing them.

______________________________________________________________________

### Using Basic Auth for Modern User Authentication

For most production applications,

JWT or OAuth2

provide a better user experience

and stronger security features.

______________________________________________________________________

# Quick Comparison

| Basic Auth | JWT |
| ---------------------------------- | ---------------------------- |
| Sends username/password | Sends signed token |
| Credentials verified every request | Token verified every request |
| No expiration | Expiration supported |
| No refresh token | Refresh token supported |
| Simple setup | Better for modern APIs |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Basic Authentication, and why should it always be used with HTTPS?

Basic Authentication is an HTTP authentication mechanism in which the client sends a Base64-encoded username and
password in the `Authorization` header with every request. Since Base64 is only an encoding format and provides no
encryption, anyone intercepting the traffic can recover the original credentials. Therefore, Basic Authentication must
always be used over HTTPS, which encrypts the communication using TLS. For modern APIs, JWT or OAuth2 are generally
preferred over Basic Authentication.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Basic Authentication is
- How it works
- Base64 encoding
- Why HTTPS is mandatory
- FastAPI support
- Basic Auth vs JWT
- Basic Auth vs Sessions
- Best practices

______________________________________________________________________

# What's Next

[Session-Based Authentication](29-session-based-authentication.md)
