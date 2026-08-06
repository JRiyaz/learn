# Request Headers

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 4 - Request Data
>
> **File:** `18_request_headers.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What HTTP Headers are
- Request Headers vs Response Headers
- Reading Headers in FastAPI
- Header Validation
- Optional Headers
- Required Headers
- Aliases
- Duplicate Headers
- Common Production Headers
- Best Practices

______________________________________________________________________

# What are HTTP Headers?

HTTP Headers are **key-value pairs** sent along with every HTTP request and response.

Example

```
GET /users HTTP/1.1

Host: example.com

Authorization: Bearer token123

User-Agent: Chrome

Accept: application/json
```

Headers provide metadata about the request.

______________________________________________________________________

# HTTP Request Structure

```
HTTP Request

↓

Request Line

↓

Headers

↓

Blank Line

↓

Body (Optional)
```

Example

```
POST /users

Headers

↓

Authorization

↓

Content-Type

↓

Accept

↓

Body
```

______________________________________________________________________

# Why are Headers Used?

Headers communicate information that is **not part of the resource itself**.

Examples

- Authentication
- Content Type
- Language
- Compression
- Caching
- Client Information
- Correlation IDs

______________________________________________________________________

# Common Request Headers

| Header | Purpose |
|----------|----------|
| Authorization | Authentication |
| Content-Type | Request body format |
| Accept | Expected response type |
| User-Agent | Client application |
| Host | Requested host |
| Accept-Language | Preferred language |
| X-Request-ID | Request tracing |

______________________________________________________________________

# Reading Headers

FastAPI provides

```python
Header
```

Import

```python
from fastapi import Header
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/")

def home(

    user_agent: str = Header()

):

    return {

        "user_agent": user_agent

    }
```

______________________________________________________________________

# Request

```
GET /

User-Agent: Chrome
```

Response

```json
{
    "user_agent": "Chrome"
}
```

______________________________________________________________________

# Internal Flow

```
HTTP Request

↓

Headers

↓

Header()

↓

Validation

↓

Route
```

______________________________________________________________________

# Optional Headers

```python
from typing import Optional

user_agent:

Optional[str] = Header(

    default=None
)
```

If the header is missing,

the value becomes

```python
None
```

______________________________________________________________________

# Required Headers

```python
authorization: str = Header()
```

If missing,

FastAPI returns

```
422

Validation Error
```

______________________________________________________________________

# Header Names

Python variables

```
user_agent
```

HTTP headers

```
User-Agent
```

FastAPI automatically converts

```
_

↓

-
```

______________________________________________________________________

# Equivalent Headers

Python

```python
user_agent
```

HTTP

```
User-Agent
```

Python

```python
content_type
```

HTTP

```
Content-Type
```

No extra configuration is required.

______________________________________________________________________

# Aliases

Sometimes header names don't map cleanly.

Example

```python
request_id: str = Header(

    alias="X-Request-ID"
)
```

Request

```
X-Request-ID

↓

12345
```

Python

```python
request_id
```

______________________________________________________________________

# Duplicate Headers

Some headers may appear multiple times.

Example

```
X-Tag: backend

X-Tag: api

X-Tag: production
```

Read them as a list.

```python
from typing import List

tags:

List[str] = Header()
```

Result

```python
[

    "backend",

    "api",

    "production"

]
```

______________________________________________________________________

# Authorization Header

Example

```
Authorization:

Bearer eyJhbGci...
```

FastAPI

```python
authorization: str = Header()
```

Authentication systems commonly extract tokens from this header.

______________________________________________________________________

# Content-Type

Example

```
Content-Type:

application/json
```

Tells the server how to interpret the request body.

Common values

- application/json
- multipart/form-data
- application/xml
- text/plain

______________________________________________________________________

# Accept Header

Example

```
Accept:

application/json
```

Indicates the response formats the client can process.

______________________________________________________________________

# User-Agent

Example

```
User-Agent:

Mozilla/5.0
```

Useful for

- Analytics
- Debugging
- Compatibility Checks

Avoid relying on it for security decisions.

______________________________________________________________________

# Correlation IDs

Large systems often include

```
X-Request-ID

↓

123456789
```

Every service logs the same ID.

Benefits

- Easier debugging
- Distributed tracing
- Log correlation

______________________________________________________________________

# Validation

Headers support type conversion.

Example

```python
retry: int = Header()
```

Incoming

```
Retry: 5
```

Result

```python
5
```

Type

```
int
```

______________________________________________________________________

# Combining Request Data

```python
@app.get(

"/users/{id}"

)

def user(

    id: int,

    page: int,

    authorization: str = Header()

):

    ...
```

FastAPI automatically identifies

```
id

↓

Path
```

```
page

↓

Query
```

```
authorization

↓

Header
```

______________________________________________________________________

# Security

Never trust incoming headers.

Examples

```
User-Agent

↓

Can Be Spoofed
```

```
X-Forwarded-For

↓

May Be Modified
```

Always validate or verify security-sensitive values.

______________________________________________________________________

# Common Mistakes

❌ Reading headers manually from the request object for simple cases

❌ Trusting client-provided headers without verification

❌ Forgetting that underscores map to hyphens

❌ Storing authentication logic inside route handlers

❌ Assuming every request includes optional headers

______________________________________________________________________

# Production Best Practices

- Use `Header()` for typed header extraction.
- Keep authentication logic in dependencies.
- Validate required headers.
- Use aliases for custom header names.
- Use correlation IDs for distributed tracing.
- Treat client-provided headers as untrusted input.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are HTTP headers commonly used for authentication instead of query parameters?**

### Answer

Headers separate metadata from the resource URL.

Using headers for authentication provides several advantages:

- Keeps access tokens out of URLs.
- Prevents tokens from appearing in browser history and many server logs.
- Follows HTTP standards.
- Works consistently across clients and API gateways.
- Integrates naturally with authorization middleware and security frameworks.

For these reasons, authentication information is typically sent using the `Authorization` header.

______________________________________________________________________

# Summary

In this chapter you learned:

- HTTP Headers
- Header Extraction
- Required Headers
- Optional Headers
- Aliases
- Duplicate Headers
- Authorization
- Content-Type
- Correlation IDs
- Production Best Practices

Request headers carry important metadata about client requests, and FastAPI provides automatic parsing, validation, and
documentation through the `Header()` dependency.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What are HTTP request headers?
1. How are request headers different from the request body?
1. Why are headers considered metadata?

______________________________________________________________________

## FastAPI

4. How do you read a request header in FastAPI?
1. How does FastAPI map Python variable names to HTTP header names?
1. How can you make a header optional?

______________________________________________________________________

## Headers

7. What is the purpose of the `Authorization` header?
1. What is the purpose of the `Content-Type` header?
1. What is the purpose of the `Accept` header?

______________________________________________________________________

## Validation

10. How does FastAPI validate header values?
01. When would you use a header alias?
01. How do you read duplicate headers?

______________________________________________________________________

## Security

13. Why shouldn't client-provided headers always be trusted?
01. Why are correlation IDs useful in distributed systems?
01. Why is the `Authorization` header preferred over query parameters for authentication?

______________________________________________________________________

## Scenario-Based

16. Your API requires an `X-Request-ID` header for request tracing. How would you read it in FastAPI?
01. A client sends three `X-Tag` headers. How can your endpoint receive all of them?
01. Your route currently extracts the bearer token manually from the request object. How could dependencies improve this design?
01. A developer uses the `User-Agent` header to determine whether a request is trustworthy. Why is this a poor security practice?
01. Your API receives a `Retry: abc` header, but your endpoint expects an integer. What happens before the route function executes?

______________________________________________________________________

# Next

[Cookies](19_cookies.md)
