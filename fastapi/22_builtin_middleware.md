# Built-in Middleware (CORS, GZip, TrustedHost, HTTPSRedirect)

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 5 - Middleware & Exception Handling
>
> **File:** `22_builtin_middleware.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Built-in Middleware is
- CORS Middleware
- GZip Middleware
- TrustedHost Middleware
- HTTPSRedirect Middleware
- Middleware Registration
- Middleware Order
- Real-world Use Cases
- Common Mistakes
- Production Best Practices

______________________________________________________________________

# What is Built-in Middleware?

FastAPI is built on **Starlette**, which provides several production-ready middleware.

Instead of writing common functionality yourself,

you can use built-in middleware.

Examples

- CORS
- GZip Compression
- Trusted Host Validation
- HTTPS Redirection

______________________________________________________________________

# Why Use Built-in Middleware?

Instead of writing

```
Custom CORS

↓

Hundreds of Lines
```

Use

```
CORSMiddleware

↓

Few Lines
```

Advantages

- Well Tested
- Secure Defaults
- Easy Configuration
- Production Ready

______________________________________________________________________

# Adding Middleware

Import

```python
app.add_middleware(...)
```

General syntax

```python
app.add_middleware(

    MiddlewareClass,

    configuration...
)
```

______________________________________________________________________

# What is CORS?

CORS stands for

```
Cross-Origin Resource Sharing
```

It controls whether a browser allows one website to access resources from another origin.

______________________________________________________________________

# What is an Origin?

An origin consists of

```
Protocol

+

Domain

+

Port
```

Example

```
https://example.com
```

Different origin

```
https://api.example.com
```

Different origin

```
http://example.com
```

Different origin

```
https://example.com:8080
```

______________________________________________________________________

# Why is CORS Needed?

Suppose

Frontend

```
https://myapp.com
```

Backend

```
https://api.myapp.com
```

Browser

```
Blocks Request

↓

Unless CORS Allows It
```

______________________________________________________________________

# CORS Flow

```
Browser

↓

Cross-Origin Request

↓

CORS Middleware

↓

Allowed?

↓

Yes

↓

Route

↓

Response
```

______________________________________________________________________

# Adding CORS

Import

```python
from fastapi.middleware.cors import CORSMiddleware
```

______________________________________________________________________

# Example

```python
app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "https://myapp.com"

    ],

    allow_methods=["*"],

    allow_headers=["*"]
)
```

______________________________________________________________________

# allow_origins

Allowed websites

```python
allow_origins=[

    "https://example.com"
]
```

Avoid

```python
["*"]
```

for authenticated production APIs unless you fully understand the security implications.

______________________________________________________________________

# allow_methods

```python
allow_methods=[

    "GET",

    "POST"
]
```

or

```python
["*"]
```

______________________________________________________________________

# allow_headers

Allowed request headers

```python
allow_headers=[

    "Authorization",

    "Content-Type"
]
```

or

```python
["*"]
```

______________________________________________________________________

# allow_credentials

```python
allow_credentials=True
```

Required for

- Cookies
- Session Authentication
- Credentialed Requests

When enabled, `allow_origins` cannot be `"*"`.

______________________________________________________________________

# What is GZip?

Large responses

```
1 MB JSON
```

can be compressed before sending.

```
JSON

↓

GZip

↓

Smaller Response
```

Benefits

- Less bandwidth
- Faster downloads
- Lower network costs

______________________________________________________________________

# Adding GZip

Import

```python
from fastapi.middleware.gzip import GZipMiddleware
```

Example

```python
app.add_middleware(

    GZipMiddleware,

    minimum_size=1000
)
```

Only responses larger than 1000 bytes are compressed.

______________________________________________________________________

# Compression Flow

```
Large Response

↓

GZip

↓

Compressed Response

↓

Browser
```

The browser automatically decompresses supported responses.

______________________________________________________________________

# What is TrustedHost Middleware?

Attackers can manipulate the HTTP

```
Host
```

header.

TrustedHostMiddleware allows requests only from approved hostnames.

______________________________________________________________________

# Example

Import

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware
```

Configuration

```python
app.add_middleware(

    TrustedHostMiddleware,

    allowed_hosts=[

        "example.com",

        "*.example.com"
    ]
)
```

Requests with unexpected `Host` headers are rejected.

______________________________________________________________________

# Trusted Host Flow

```
Incoming Host

↓

Allowed?

↓

Yes

↓

Continue
```

```
No

↓

Reject
```

______________________________________________________________________

# What is HTTPSRedirectMiddleware?

Some users may access

```
http://
```

instead of

```
https://
```

The middleware automatically redirects them.

______________________________________________________________________

# Example

Import

```python
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
```

Configuration

```python
app.add_middleware(

    HTTPSRedirectMiddleware
)
```

______________________________________________________________________

# Redirect Flow

```
HTTP

↓

Redirect

↓

HTTPS

↓

Application
```

Useful when the application directly handles HTTP traffic.

______________________________________________________________________

# Middleware Registration

Example

```python
app.add_middleware(

    CORSMiddleware,

    ...
)

app.add_middleware(

    GZipMiddleware,

    ...
)

app.add_middleware(

    TrustedHostMiddleware,

    ...
)

app.add_middleware(

    HTTPSRedirectMiddleware
)
```

______________________________________________________________________

# Middleware Stack

```
Request

↓

Trusted Host

↓

HTTPS Redirect

↓

CORS

↓

GZip

↓

Route
```

Response

```
Route

↓

GZip

↓

CORS

↓

Client
```

______________________________________________________________________

# Real Production Architecture

```
Browser

↓

Load Balancer

↓

Nginx

↓

FastAPI

↓

Trusted Host

↓

CORS

↓

Routes
```

In many deployments, the reverse proxy also handles HTTPS termination and compression.

______________________________________________________________________

# When Not to Use HTTPSRedirectMiddleware

If HTTPS is already enforced by

- Nginx
- Apache
- AWS ALB
- Cloudflare
- Kubernetes Ingress

additional application-level redirection may be unnecessary.

______________________________________________________________________

# Common Mistakes

❌ Using

```python
allow_origins=["*"]
```

with credentialed requests

❌ Allowing every origin in production without a reason

❌ Compressing very small responses

❌ Forgetting trusted host validation for public deployments

❌ Assuming middleware alone replaces proper infrastructure security

______________________________________________________________________

# Production Best Practices

- Explicitly configure allowed origins.
- Enable credentials only when required.
- Compress large responses.
- Restrict allowed hostnames.
- Enforce HTTPS.
- Prefer reverse proxies for TLS termination in production.
- Review middleware order carefully.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is `CORSMiddleware` necessary even though the backend itself can technically handle requests from any client?**

### Answer

CORS is primarily enforced by web browsers, not the backend server.

Without appropriate CORS headers,

the browser blocks JavaScript running on one origin from accessing resources on another origin.

`CORSMiddleware` sends the required HTTP headers so browsers know which origins, methods, and headers are permitted.

This enables secure communication between frontend applications and backend APIs while limiting unauthorized
cross-origin access.

______________________________________________________________________

# Summary

In this chapter you learned:

- Built-in Middleware
- CORSMiddleware
- GZipMiddleware
- TrustedHostMiddleware
- HTTPSRedirectMiddleware
- Middleware Order
- Production Deployment
- Security Considerations
- Best Practices

FastAPI's built-in middleware provides production-ready solutions for common concerns such as cross-origin requests,
response compression, host validation, and HTTPS enforcement with minimal configuration.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is built-in middleware?
1. Why should built-in middleware be preferred over custom implementations for common concerns?
1. How do you register middleware in FastAPI?

______________________________________________________________________

## CORS

4. What does CORS stand for?
1. What defines an origin?
1. Why do browsers enforce CORS?
1. What is the purpose of `allow_origins`?
1. Why shouldn't `"*"` be used with authenticated APIs?

______________________________________________________________________

## GZip

9. What problem does GZip middleware solve?
1. What does `minimum_size` control?
1. Why isn't every response compressed?

______________________________________________________________________

## Trusted Host

12. What problem does `TrustedHostMiddleware` solve?
01. What happens when a request uses an untrusted `Host` header?

______________________________________________________________________

## HTTPS

14. What does `HTTPSRedirectMiddleware` do?
01. When might it be unnecessary to use it?

______________________________________________________________________

## Scenario-Based

16. Your React frontend is hosted at `https://app.example.com` and your FastAPI backend is at `https://api.example.com`. Browser requests fail with CORS errors. How would you configure the backend?
01. Your API returns large JSON reports that are several megabytes in size. Which middleware would improve performance?
01. Your FastAPI application is deployed behind an AWS Application Load Balancer that already redirects HTTP to HTTPS. Would you still enable `HTTPSRedirectMiddleware`? Why or why not?
01. Your public API receives requests with forged `Host` headers. Which middleware helps mitigate this issue?
01. A teammate configures `allow_origins=["*"]` together with `allow_credentials=True`. Why is this configuration invalid and what would you recommend instead?

______________________________________________________________________

# Next

[Exception Handling](23_exception_handling.md)
