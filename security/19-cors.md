# Security - Part 19

# CORS (Cross-Origin Resource Sharing)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What CORS is
- Why browsers enforce CORS
- What an Origin is
- Same-Origin Policy
- Preflight Requests
- CORS Headers
- Secure CORS configuration in FastAPI
- Common misconceptions
- Best practices

______________________________________________________________________

# What is CORS?

CORS stands for

**Cross-Origin Resource Sharing**.

It is a **browser security mechanism** that controls whether a web page is allowed to make requests to another origin.

> **Important:** CORS is enforced by browsers, not by your FastAPI application.

______________________________________________________________________

# What is an Origin?

An **Origin** consists of three parts:

```text id="cors1901"
Protocol

+

Domain

+

Port
```

Example

```text id="cors1902"
https://library.example.com:443
```

Here:

- Protocol → `https`
- Domain → `library.example.com`
- Port → `443`

If **any one** of these changes,

the origin is different.

______________________________________________________________________

# Example Origins

| URL | Same Origin? |
| -------------------------------- | -------------------- |
| https://library.example.com | ✅ |
| https://library.example.com:443 | ✅ |
| http://library.example.com | ❌ (Protocol changed) |
| https://api.library.example.com | ❌ (Domain changed) |
| https://library.example.com:8080 | ❌ (Port changed) |

______________________________________________________________________

# Same-Origin Policy (SOP)

Browsers follow the

**Same-Origin Policy**.

Without CORS,

a webpage can freely communicate only with its own origin.

Example

```text id="cors1903"
Frontend

https://library.example.com

↓

Backend

https://library.example.com

↓

Allowed
```

But

```text id="cors1904"
Frontend

https://library.example.com

↓

Backend

https://api.othercompany.com

↓

Blocked by Browser
```

______________________________________________________________________

# Why Does CORS Exist?

Imagine you're logged into:

```text id="cors1905"
https://bank.com
```

Now you visit

```text id="cors1906"
https://evil.com
```

Without browser protections,

the malicious website could freely make requests to your bank.

CORS helps reduce this risk by restricting cross-origin access.

______________________________________________________________________

# Important Clarification

CORS **does not protect your API** from all clients.

Example

```text id="cors1907"
Browser

↓

CORS Applies
```

But

```text id="cors1908"
Python Script

↓

curl

↓

Postman

↓

CORS Does NOT Apply
```

This is one of the biggest interview questions.

Attackers using:

- curl
- Python
- Postman

can still call your API.

Your API must still implement:

- Authentication
- Authorization

______________________________________________________________________

# Simple Request

Some requests are considered

simple requests.

Example

```http id="cors1909"
GET /books
```

If the server returns

the proper CORS headers,

the browser allows the response.

______________________________________________________________________

# Preflight Request

Some requests require

a preflight check.

Example

```text id="cors1910"
Browser

↓

OPTIONS Request

↓

Server

↓

Allowed?

↓

Actual Request
```

The browser first asks

whether the real request

is permitted.

______________________________________________________________________

# Why Preflight?

Suppose the frontend wants to send:

- Authorization header
- PUT request
- DELETE request

Instead of sending it immediately,

the browser first sends

an

```text id="cors1911"
OPTIONS
```

request.

The server replies

with the allowed:

- Methods
- Headers
- Origins

Only then

does the browser send

the real request.

______________________________________________________________________

# Important CORS Headers

Common response headers include:

```text id="cors1912"
Access-Control-Allow-Origin

Access-Control-Allow-Methods

Access-Control-Allow-Headers

Access-Control-Allow-Credentials
```

These tell the browser

what is permitted.

______________________________________________________________________

# FastAPI Configuration

FastAPI provides

built-in CORS middleware.

```python id="cors1913"
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://library.example.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

______________________________________________________________________

# Why Not `allow_origins=["*"]`?

Bad Example

```python id="cors1914"
allow_origins=["*"]
```

This allows

every website

to access your API

from a browser.

For public APIs,

this may be acceptable.

For authenticated applications,

it's usually not.

______________________________________________________________________

# Better Configuration

Specify trusted origins.

Example

```python id="cors1915"
allow_origins=[
    "https://library.example.com",
    "https://admin.library.example.com",
]
```

Now only these frontends

can access the API

through a browser.

______________________________________________________________________

# CORS and JWT

Suppose your frontend sends

```http id="cors1916"
Authorization: Bearer <JWT>
```

The browser performs

a preflight request first.

Your server must allow:

```text id="cors1917"
Authorization
```

as an allowed header.

Otherwise,

the browser blocks the request.

______________________________________________________________________

# CORS vs CSRF

These are frequently confused.

| CORS | CSRF |
| ------------------------------- | -------------------------------------------------- |
| Browser policy | Attack |
| Controls cross-origin requests | Tricks browser into sending authenticated requests |
| Browser-enforced | Application must defend against it |
| Not an authentication mechanism | Exploits automatic authentication (cookies) |

Remember:

CORS is **not** a substitute for authentication or CSRF protection.

______________________________________________________________________

# Defense in Depth

A secure web application uses:

```text id="cors1918"
HTTPS

↓

Authentication

↓

Authorization

↓

CORS

↓

CSRF Protection (if using cookies)

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Allow only trusted origins.

✅ Use HTTPS.

✅ Configure CORS deliberately.

✅ Allow only required methods.

✅ Allow only required headers.

✅ Continue enforcing authentication and authorization.

______________________________________________________________________

# Common Mistakes

### Thinking CORS Secures the API

CORS only affects browsers.

It does not stop:

- curl
- Postman
- Python scripts
- Mobile applications

______________________________________________________________________

### Using `allow_origins=["*"]` Everywhere

This is rarely appropriate

for authenticated web applications.

______________________________________________________________________

### Confusing CORS with Authentication

Even if CORS allows a request,

the API must still authenticate

and authorize the user.

______________________________________________________________________

### Forgetting Preflight Requests

If your frontend sends:

- Authorization headers
- PUT
- PATCH
- DELETE

ensure your CORS configuration supports them.

______________________________________________________________________

# Quick Comparison

| Misconception | Reality |
| ---------------------------- | ---------------------------------- |
| CORS secures APIs | CORS only controls browsers |
| CORS replaces authentication | Authentication is still required |
| `*` is always safe | Restrict origins whenever possible |
| CORS and CSRF are the same | They solve different problems |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is CORS, and why is it not considered an API security mechanism?

CORS (Cross-Origin Resource Sharing) is a browser-enforced mechanism that controls whether a webpage from one origin may
access resources from another origin. It is designed to protect users from unauthorized cross-origin interactions in
browsers. It is not an API security mechanism because non-browser clients such as curl, Postman, Python scripts, and
mobile applications are not restricted by CORS. APIs must still implement proper authentication, authorization, and
input validation regardless of their CORS configuration.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What CORS is
- Origins
- Same-Origin Policy
- Preflight requests
- CORS headers
- FastAPI CORS middleware
- CORS vs CSRF
- Common misconceptions
- Best practices

______________________________________________________________________

# What's Next

[HTTPS & TLS](20-https-and-tls.md)
