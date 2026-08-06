# Cookies

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 4 - Request Data
>
> **File:** `19_cookies.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Cookies are
- Why Cookies are Used
- Cookies vs Headers
- Reading Cookies
- Setting Cookies
- Updating Cookies
- Deleting Cookies
- Cookie Attributes
- Security Considerations
- Production Best Practices

______________________________________________________________________

# What are Cookies?

A **Cookie** is a small piece of data stored by the client's browser.

The server sends a cookie,

and the browser automatically includes it in future requests.

Flow

```
Server

↓

Set Cookie

↓

Browser Stores Cookie

↓

Future Requests Include Cookie
```

______________________________________________________________________

# HTTP Cookie Flow

First Request

```
Client

↓

Login

↓

Server

↓

Set-Cookie
```

Later Requests

```
Browser

↓

Cookie

↓

Server
```

The browser automatically sends stored cookies to the appropriate domain.

______________________________________________________________________

# Why Do We Use Cookies?

Cookies commonly store

- Session IDs
- Authentication Tokens
- User Preferences
- Theme Selection
- Language
- Shopping Cart IDs

They help the server recognize returning clients.

______________________________________________________________________

# Cookie vs Header

Cookie

```
Automatically Sent

By Browser
```

Header

```
Usually Added

By Client
```

Example

```
Cookie:

session=abc123
```

```
Authorization:

Bearer token
```

______________________________________________________________________

# Reading Cookies

FastAPI provides

```python
Cookie
```

Import

```python
from fastapi import Cookie
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/")

def home(

    session: str = Cookie()

):

    return {

        "session": session

    }
```

______________________________________________________________________

# Request

```
GET /

Cookie:

session=abc123
```

Response

```json
{
    "session": "abc123"
}
```

______________________________________________________________________

# Optional Cookie

```python
from typing import Optional

session:

Optional[str] = Cookie(

    default=None
)
```

If missing

```python
session == None
```

______________________________________________________________________

# Required Cookie

```python
session: str = Cookie()
```

If absent

```
422

Validation Error
```

______________________________________________________________________

# Setting Cookies

Cookies are set on the response.

Example

```python
from fastapi import Response
```

```python
@app.get("/login")

def login(

    response: Response

):

    response.set_cookie(

        key="session",

        value="abc123"

    )

    return {

        "message": "Logged In"

    }
```

______________________________________________________________________

# Response Flow

```
Route

↓

Response

↓

Set-Cookie Header

↓

Browser Stores Cookie
```

______________________________________________________________________

# Updating Cookies

Calling

```python
set_cookie()
```

again with the same key replaces the existing value.

Example

```python
response.set_cookie(

    key="session",

    value="xyz789"
)
```

The browser updates the stored cookie.

______________________________________________________________________

# Deleting Cookies

Example

```python
response.delete_cookie(

    key="session"
)
```

The browser removes the cookie.

Common during logout.

______________________________________________________________________

# Cookie Lifetime

Session Cookie

```
Browser Closed

↓

Cookie Removed
```

Persistent Cookie

```
Expires

↓

Future Date
```

______________________________________________________________________

# Max Age

```python
response.set_cookie(

    key="session",

    value="abc123",

    max_age=3600
)
```

Cookie expires after

```
3600 Seconds
```

______________________________________________________________________

# Expiration Date

```python
expires=...
```

Allows setting a specific expiration time instead of a relative duration.

______________________________________________________________________

# HttpOnly

```python
httponly=True
```

Browser JavaScript

```
Cannot Read Cookie
```

This helps reduce the impact of cross-site scripting (XSS) attacks.

______________________________________________________________________

# Secure Cookie

```python
secure=True
```

Cookie is sent only over

```
HTTPS
```

Recommended for production environments.

______________________________________________________________________

# SameSite

```python
samesite="lax"
```

Common values

- strict
- lax
- none

Helps protect against Cross-Site Request Forgery (CSRF).

______________________________________________________________________

# Cookie Attributes

| Attribute | Purpose |
|------------|----------|
| max_age | Relative lifetime |
| expires | Expiration date |
| httponly | Blocks JavaScript access |
| secure | HTTPS only |
| samesite | CSRF protection |
| path | URL scope |
| domain | Domain scope |

______________________________________________________________________

# Example

```python
response.set_cookie(

    key="session",

    value="abc123",

    httponly=True,

    secure=True,

    samesite="lax"
)
```

A common production configuration.

______________________________________________________________________

# Cookies vs JWT

Cookie

```
Browser Storage

↓

Automatic
```

JWT

```
Token

↓

Usually Authorization Header
```

Both can be used for authentication,

depending on the application's architecture.

______________________________________________________________________

# Session Authentication

Typical flow

```
Login

↓

Database

↓

Session Created

↓

Session ID Cookie

↓

Future Requests

↓

Session Lookup
```

The cookie stores only the session identifier,

not the user's entire session data.

______________________________________________________________________

# Logout

```
Delete Session

↓

Delete Cookie

↓

User Logged Out
```

Both server-side session cleanup and cookie removal are typically required.

______________________________________________________________________

# Security Risks

Poor configuration

```
Cookie

↓

JavaScript Access

↓

XSS Risk
```

Missing HTTPS

```
Cookie

↓

Network

↓

Possible Interception
```

______________________________________________________________________

# FastAPI Flow

```
Browser

↓

Cookie

↓

FastAPI

↓

Cookie()

↓

Route
```

Reading cookies is automatic.

______________________________________________________________________

# Common Mistakes

❌ Storing sensitive information directly inside cookies

❌ Forgetting `HttpOnly`

❌ Using cookies over HTTP in production

❌ Forgetting to delete cookies during logout

❌ Trusting cookie contents without server-side verification

______________________________________________________________________

# Production Best Practices

- Store only identifiers, not sensitive data.
- Enable `HttpOnly` for authentication cookies.
- Enable `Secure` in production.
- Configure `SameSite` appropriately.
- Delete cookies during logout.
- Validate sessions on the server.
- Use HTTPS.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should authentication cookies usually be configured with `HttpOnly` and `Secure`?**

### Answer

`HttpOnly` prevents client-side JavaScript from reading the cookie, reducing the impact of XSS attacks.

`Secure` ensures the cookie is transmitted only over HTTPS, protecting it from interception on unencrypted connections.

Together, these settings significantly improve the security of session-based authentication.

______________________________________________________________________

# Summary

In this chapter you learned:

- Cookies
- Reading Cookies
- Setting Cookies
- Updating Cookies
- Deleting Cookies
- Cookie Attributes
- Session Cookies
- Authentication Cookies
- Security Best Practices

Cookies provide a convenient mechanism for maintaining state between requests, and FastAPI offers simple APIs for
reading and managing them while supporting modern security features.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a cookie?
1. How does a cookie differ from a request header?
1. Why are cookies used?

______________________________________________________________________

## FastAPI

4. How do you read a cookie in FastAPI?
1. How do you set a cookie?
1. How do you delete a cookie?

______________________________________________________________________

## Cookie Attributes

7. What does `HttpOnly` do?
1. What does `Secure` do?
1. What does `SameSite` protect against?

______________________________________________________________________

## Authentication

10. Why should cookies store session IDs instead of sensitive user information?
01. How does session-based authentication use cookies?
01. Why should cookies be deleted during logout?

______________________________________________________________________

## Security

13. Why shouldn't authentication cookies be accessible from JavaScript?
01. Why is HTTPS important when using cookies?
01. Why should cookie contents still be validated on the server?

______________________________________________________________________

## Scenario-Based

16. Your application stores a user's password directly in a browser cookie. Why is this a serious security issue?
01. A user logs out, but the browser still sends the old session cookie. What steps should the application take?
01. Your production application sets authentication cookies without `Secure=True`. What risks does this introduce?
01. Your application is vulnerable to XSS attacks. How does `HttpOnly` help reduce the impact on authentication cookies?
01. Your team is deciding between session cookies and JWT bearer tokens for authentication. What are the key architectural differences between these approaches?

______________________________________________________________________

# Next

[Forms & File Uploads](20_forms_file_uploads.md)
