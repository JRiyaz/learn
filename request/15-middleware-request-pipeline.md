# Complete HTTP Request Lifecycle Deep Dive

## 15. Middleware Request Pipeline

> **Target Audience:** Backend Engineers (Intermediate → Senior)
>
> **Goal:** Understand exactly what happens after Uvicorn hands the request to FastAPI, how middleware works internally, how the request travels through multiple middleware layers, how the response travels back, and what production middleware usually does.

______________________________________________________________________

# Introduction

In the previous chapter,

Uvicorn

created

the ASGI Scope

and called

```python
await app(scope, receive, send)
```

At this point,

FastAPI

has control.

Many people think

the request

immediately reaches

their API.

Like this.

```
Client

↓

FastAPI

↓

@app.get(...)
```

This is wrong.

Before

your endpoint executes,

the request

passes through

every middleware.

______________________________________________________________________

# Where We Are

```
Internet

↓

Linux Kernel

↓

Socket

↓

epoll()

↓

Uvicorn

↓

HTTP Parser

↓

ASGI

↓

FastAPI

↓

Middleware

⭐ You are here

↓

Dependency Injection

↓

Endpoint
```

______________________________________________________________________

# What Is Middleware?

Interview favorite.

Middleware

is code

that executes

before

and

after

your endpoint.

Think of it as

security gates.

```
Request

↓

Middleware 1

↓

Middleware 2

↓

Middleware 3

↓

Endpoint

↓

Middleware 3

↓

Middleware 2

↓

Middleware 1

↓

Response
```

Notice

the response

travels

back

through

the same middleware.

______________________________________________________________________

# Real Production Middleware Stack

```
Incoming Request

↓

Request ID

↓

Logging

↓

Trusted Host

↓

HTTPS Redirect

↓

CORS

↓

GZip

↓

Authentication

↓

Authorization

↓

Rate Limiting

↓

Custom Middleware

↓

FastAPI Endpoint
```

Response

travels back

in reverse order.

______________________________________________________________________

# Why Middleware?

Imagine

every endpoint

contains

```python
log_request()

authenticate()

authorize()

compress()

add_headers()
```

Every endpoint

would repeat

the same code.

Middleware

solves this.

______________________________________________________________________

# Request Flow

```
Client

↓

Middleware A

↓

Middleware B

↓

Middleware C

↓

Route Handler

↓

Middleware C

↓

Middleware B

↓

Middleware A

↓

Client
```

______________________________________________________________________

# Middleware Is Like An Onion

Interview favorite.

```
Outer Layer

↓

Middle Layer

↓

Inner Layer

↓

Endpoint

↓

Inner Layer

↓

Middle Layer

↓

Outer Layer
```

Each middleware

wraps

the next one.

______________________________________________________________________

# Example

Suppose

you have

three middleware.

```
Logging

↓

Authentication

↓

Compression
```

Request enters

```
Logging

↓

Authentication

↓

Compression

↓

Endpoint
```

Response leaves

```
Endpoint

↓

Compression

↓

Authentication

↓

Logging
```

______________________________________________________________________

# What Happens Internally?

When FastAPI starts,

it builds

a middleware chain.

Something similar

to this.

```
Middleware A

contains

Middleware B

contains

Middleware C

contains

Application
```

Instead of

calling

your endpoint directly,

FastAPI calls

the outermost middleware.

______________________________________________________________________

# Simplified Flow

```python
MiddlewareA(
    MiddlewareB(
        MiddlewareC(
            FastAPI()
        )
    )
)
```

Every request

starts

from

Middleware A.

______________________________________________________________________

# Example Middleware

```python
@app.middleware("http")
async def log(request, call_next):

    print("Before")

    response = await call_next(request)

    print("After")

    return response
```

Important

```
call_next()
```

passes

the request

to

the next middleware.

______________________________________________________________________

# Step 1

# Request Object Creation

Before middleware,

FastAPI creates

a Request object.

Internally

```
ASGI Scope

↓

Request Object
```

The Request object

contains

```
Method

↓

URL

↓

Headers

↓

Cookies

↓

Query Params
```

Notice

the body

has NOT

been parsed yet.

______________________________________________________________________

# Step 2

# Logging Middleware

Usually

the first middleware.

Responsibilities

```
Generate Request ID

↓

Record Start Time

↓

Log Request

↓

Call Next Middleware
```

Example log

```
GET /users

Started
```

______________________________________________________________________

# Why First?

If something crashes,

logging still works.

______________________________________________________________________

# Step 3

# Correlation ID

Interview favorite.

Production systems

generate

```
Request ID

or

Trace ID
```

Example

```
a5c2d3e7
```

This ID

travels

through

every service.

Useful

for

debugging.

______________________________________________________________________

# Step 4

# Trusted Host Middleware

Suppose

someone sends

```
Host:

evil.com
```

Instead of

```
api.company.com
```

Trusted Host

blocks it.

______________________________________________________________________

# Step 5

# HTTPS Redirect Middleware

Suppose

someone opens

```
http://company.com
```

Middleware returns

```
301

Redirect
```

to

```
https://company.com
```

______________________________________________________________________

# Step 6

# CORS Middleware

Interview favorite.

Browser sends

```
Origin

https://app.company.com
```

Middleware checks

```
Allowed?
```

If yes

adds

```
Access-Control-Allow-Origin
```

Otherwise

browser blocks

the request.

______________________________________________________________________

# What Actually Happens?

Browser

doesn't enforce

CORS.

The browser

enforces

the server's

CORS headers.

FastAPI

simply

returns

the headers.

______________________________________________________________________

# Step 7

# GZip Middleware

Suppose

response size

is

```
5 MB
```

Middleware compresses

```
JSON

↓

GZip

↓

500 KB
```

Bandwidth

reduces significantly.

______________________________________________________________________

# Step 8

# Authentication Middleware

Suppose

header contains

```
Authorization

Bearer JWT
```

Middleware extracts

the token.

Later

authentication

will verify it.

______________________________________________________________________

# Step 9

# Rate Limiting Middleware

Suppose

same IP

sends

```
1000 requests

per second
```

Middleware checks

Redis

or

memory.

```
Allowed?

↓

No

↓

429
```

Endpoint

never executes.

______________________________________________________________________

# Step 10

# Custom Middleware

Companies

often write

their own middleware.

Examples

```
Tenant Detection

↓

Feature Flags

↓

Audit Logging

↓

Maintenance Mode
```

______________________________________________________________________

# call_next()

Interview favorite.

Suppose

middleware

calls

```python
response = await call_next(request)
```

Internally

```
Current Middleware

↓

Next Middleware

↓

Next Middleware

↓

Endpoint
```

When endpoint

returns

execution resumes

after

call_next().

______________________________________________________________________

# Visual Execution

```
Logging

↓

Authentication

↓

Endpoint

↓

Authentication

↓

Logging
```

Notice

middleware

executes twice.

Before

and after.

______________________________________________________________________

# Request Context

Middleware

can attach

custom data.

Example

```python
request.state.user
```

or

```python
request.state.request_id
```

Later

dependencies

can use it.

______________________________________________________________________

# What Happens If Middleware Returns Early?

Suppose

authentication fails.

Middleware returns

```
401 Unauthorized
```

Immediately.

```
Request

↓

Authentication

↓

401

↓

Client
```

Endpoint

never executes.

______________________________________________________________________

# Middleware Ordering

Interview favorite.

Order matters.

Correct

```
Logging

↓

Authentication

↓

Authorization

↓

Business Logic
```

Bad

```
Authorization

↓

Authentication
```

Authorization

needs

an authenticated user.

______________________________________________________________________

# Exception Handling

Suppose

endpoint raises

```
ValueError
```

Exception middleware

intercepts it.

```
Endpoint

↓

Exception

↓

Exception Middleware

↓

500 Response
```

Application

doesn't crash.

______________________________________________________________________

# Performance

Each middleware

adds

small overhead.

Example

```
Logging

1 ms
```

```
Authentication

2 ms
```

```
Compression

5 ms
```

Total latency

increases.

Keep middleware

lightweight.

______________________________________________________________________

# Memory Usage

Middleware

shares

the same

Request object.

It does NOT

copy

the request

for every layer.

This reduces

memory usage.

______________________________________________________________________

# Common Production Middleware

```
Logging

↓

Tracing

↓

Metrics

↓

Authentication

↓

Rate Limiting

↓

Compression

↓

Caching

↓

Exception Handling
```

______________________________________________________________________

# Common Mistakes

## Reading Body Twice

Interview favorite.

Request body

is a stream.

If middleware

consumes it,

the endpoint

cannot read it

unless

it's restored.

______________________________________________________________________

## Blocking Middleware

Never use

```python
time.sleep()
```

inside middleware.

Use

```python
await asyncio.sleep()
```

______________________________________________________________________

## Heavy Database Calls

Avoid

expensive queries

inside middleware.

Every request

will become slower.

______________________________________________________________________

# What Happens In Memory?

```
ASGI Scope

↓

Request Object

↓

Middleware Stack

↓

Shared Request

↓

Response Object

↓

Shared Response
```

No unnecessary

copies

are created.

______________________________________________________________________

# Common Interview Questions

## Why use middleware instead of decorators?

Middleware runs for every request before route matching completes and is ideal for cross-cutting concerns like logging,
tracing, and CORS. Decorators apply only to specific endpoints.

______________________________________________________________________

## Why does middleware execute twice?

The request travels down the middleware chain to the endpoint, and the response travels back up the same chain, allowing
middleware to modify both requests and responses.

______________________________________________________________________

## Can middleware stop a request?

Yes.

Middleware can return a response immediately without calling `call_next()`. This is commonly used for authentication
failures, maintenance mode, or rate limiting.

______________________________________________________________________

## Does every middleware receive the same Request object?

Yes.

The same Request object is passed through the middleware chain. Middleware may attach additional information using
`request.state`.

______________________________________________________________________

## Why shouldn't middleware read the body unnecessarily?

The request body is streamed. Reading it consumes the stream, which can prevent downstream code from accessing it unless
it is buffered and restored.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when FastAPI receives a request.

### Answer

FastAPI constructs a Request object from the ASGI scope and invokes the outermost middleware. Each middleware performs
its work, optionally modifies the request, and calls `call_next()` to continue the chain. After the endpoint generates a
response, execution returns through the middleware stack in reverse order, allowing each middleware to inspect or modify
the response before it is sent back to Uvicorn.

______________________________________________________________________

# Summary

Middleware is the first layer inside your FastAPI application.

It provides

- Logging
- Correlation IDs
- CORS
- HTTPS Redirects
- Compression
- Authentication
- Rate Limiting
- Exception Handling
- Custom request processing

Every request and response passes through the middleware pipeline before reaching your endpoint or leaving your
application.

______________________________________________________________________

# Next

[16. Request Parsing and JSON Processing](16-request-parsing-and-json-processing.md)
