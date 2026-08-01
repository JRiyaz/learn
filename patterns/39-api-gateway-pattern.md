# Software Architecture - Part 39

# API Gateway Pattern

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What an API Gateway is
- Why API Gateways exist
- Problems they solve
- Request routing
- Authentication
- Rate limiting
- Request aggregation
- Backend for Frontend (BFF)
- FastAPI examples
- Real-world production examples
- When NOT to use an API Gateway

______________________________________________________________________

# Before We Start

Suppose

your company

has

these microservices.

```text id="api3901"
Book Service

Member Service

Payment Service

Recommendation Service

Notification Service
```

A mobile app

needs data

from

all five.

Should

the mobile app

call

each service

individually?

Technically,

yes.

Should it?

Usually,

no.

______________________________________________________________________

# The Problem

Suppose

the mobile app

opens

the dashboard.

It needs:

- User profile
- Borrowed books
- Pending fines
- Recommendations
- Notifications

Without

an API Gateway,

the client

must make

multiple requests.

```text id="api3902"
Mobile

↓

Member Service

↓

Books Service

↓

Payment Service

↓

Recommendation Service

↓

Notification Service
```

Problems:

❌ Too many network calls

❌ Authentication repeated

❌ Client knows service locations

❌ Versioning becomes difficult

______________________________________________________________________

# Another Problem

Tomorrow,

Book Service

moves

to

another server.

Now,

every client

must update

its configuration.

______________________________________________________________________

# The Idea

Place

one component

in front

of

all services.

Clients

communicate

only

with

that component.

______________________________________________________________________

# What is an API Gateway?

An **API Gateway**

is

a single entry point

for clients

to access

backend services.

It receives

client requests,

performs

common tasks,

and routes

requests

to

the appropriate service.

______________________________________________________________________

# Architecture

```text id="api3903"
Client

↓

API Gateway

↓

Book Service

Payment Service

Member Service

Notification Service
```

The client

never talks

to services

directly.

______________________________________________________________________

# Request Routing

The gateway

decides

where

requests go.

Example

```text id="api3904"
/books

↓

Book Service
```

```text id="api3905"
/payments

↓

Payment Service
```

Clients

don't need

to know

where services

are deployed.

______________________________________________________________________

# Authentication

Without Gateway

every service

implements

authentication.

```text id="api3906"
Book Service

↓

JWT Validation
```

```text id="api3907"
Payment Service

↓

JWT Validation
```

Repeated

everywhere.

______________________________________________________________________

# With Gateway

```text id="api3908"
Client

↓

API Gateway

↓

JWT Validation

↓

Services
```

Authentication

is centralized.

______________________________________________________________________

# Authorization

The gateway

may also

check permissions.

Example

```text id="api3909"
Admin

↓

Admin APIs
```

```text id="api3910"
Member

↓

Member APIs
```

Unauthorized requests

can be rejected

before reaching

backend services.

______________________________________________________________________

# Rate Limiting

Suppose

someone

sends

10,000 requests

per second.

Without protection,

services

may fail.

Gateway

can enforce

limits.

Example

```text id="api3911"
100 Requests

↓

Allowed

101st Request

↓

429 Too Many Requests
```

One implementation

protects

all services.

______________________________________________________________________

# Request Aggregation

One request

can fetch data

from

multiple services.

Example

Client requests

```text id="api3912"
/dashboard
```

Gateway performs

```text id="api3913"
Member Service

↓

Book Service

↓

Payment Service

↓

Recommendation Service
```

Then

returns

one combined response.

The client

makes

only one request.

______________________________________________________________________

# Response Transformation

Different services

may return

different formats.

Example

Book Service

```json id="api3914"
{
  "book_name": "Clean Code"
}
```

Recommendation Service

```json id="api3915"
{
  "title": "Design Patterns"
}
```

Gateway

can normalize

the response

before

returning it.

______________________________________________________________________

# Backend for Frontend (BFF)

Different clients

often need

different data.

Example

```text id="api3916"
Mobile

↓

Mobile Gateway
```

```text id="api3917"
Web

↓

Web Gateway
```

Each gateway

optimizes

responses

for

its client.

This is called

**Backend for Frontend (BFF).**

______________________________________________________________________

# FastAPI Example

A gateway

can expose

routes like

```python id="api3918"
@app.get("/dashboard")
```

Internally,

it calls

multiple services

using

HTTP clients

or

gRPC clients,

combines

their responses,

and returns

a single result.

______________________________________________________________________

# gRPC Example

Instead of

REST,

the gateway

may communicate

with services

using

gRPC.

```text id="api3919"
Client

↓

REST

↓

Gateway

↓

gRPC

↓

Services
```

Clients

use REST.

Internal communication

uses gRPC.

______________________________________________________________________

# Service Discovery

Suppose

Book Service

has

10 instances.

The gateway

asks

Service Discovery

which instance

should receive

the request.

We'll study

Service Discovery

later.

______________________________________________________________________

# Gateway vs Load Balancer

A common

interview question.

| Load Balancer | API Gateway |
| -------------------------------- | ------------------------------------- |
| Distributes traffic | Manages API requests |
| Network layer | Application layer |
| Doesn't understand business APIs | Understands routes, auth, rate limits |

Many systems

use both.

Example

```text id="api3920"
Client

↓

Load Balancer

↓

API Gateway

↓

Microservices
```

______________________________________________________________________

# Gateway vs Reverse Proxy

Another common question.

A Reverse Proxy

(such as Nginx)

primarily handles

HTTP traffic,

TLS termination,

and routing.

An API Gateway

builds on these ideas

by adding

application-level features

such as:

- Authentication
- Rate Limiting
- Request Aggregation
- API Versioning
- API Keys

______________________________________________________________________

# Popular API Gateways

Common production gateways

include:

- Kong
- NGINX
- Envoy
- Traefik
- Amazon API Gateway
- Azure API Management

Many organizations

also build

custom gateways

using

FastAPI,

Spring Boot,

or Node.js.

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

contains:

- Prompt Service
- Embedding Service
- RAG Service
- LLM Service
- Billing Service

Clients

send

one request

to

```text id="api3921"
AI Gateway
```

The gateway

coordinates

the backend services

and returns

one response.

______________________________________________________________________

# Benefits

API Gateways provide:

✅ Single entry point

✅ Centralized authentication

✅ Centralized rate limiting

✅ Request aggregation

✅ Easier client development

✅ Better security

______________________________________________________________________

# Drawbacks

They also introduce:

❌ One additional network hop

❌ Potential bottleneck

❌ More infrastructure

❌ Gateway failures

if not made highly available.

______________________________________________________________________

# Real Company Example

Netflix,

Amazon,

Uber,

and many

large-scale platforms

use API Gateways

to expose

public APIs

while hiding

internal microservice

topologies.

Clients

interact

with one endpoint,

not

hundreds of services.

______________________________________________________________________

# When NOT to Use an API Gateway

Don't introduce

an API Gateway

if

you have:

- One backend service
- A simple internal tool
- Very small applications

The additional layer

may provide

little benefit.

______________________________________________________________________

# Best Practices

✅ Keep the gateway lightweight.

✅ Put business logic inside services.

✅ Centralize authentication.

✅ Use request aggregation sparingly.

______________________________________________________________________

# Common Mistakes

### Business Logic in the Gateway

The gateway

should route,

authenticate,

and coordinate.

Business rules

belong

inside

the services.

______________________________________________________________________

### Calling Every Service

Not every request

needs

aggregation.

Forward requests

directly

when possible.

______________________________________________________________________

### Single Point of Failure

Deploy

multiple gateway instances

behind

a load balancer.

______________________________________________________________________

### Gateway Becoming a Monolith

Keep

gateway responsibilities

focused.

Don't move

the entire application

into

the gateway.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is an API Gateway, and why is it important in a microservices architecture?

An API Gateway is a single entry point that sits between clients and backend microservices. It handles cross-cutting
concerns such as authentication, authorization, request routing, rate limiting, request aggregation, API versioning, and
response transformation. This simplifies client applications by hiding the complexity of the underlying microservice
architecture. API Gateways are a common component of large distributed systems, but they should remain lightweight and
avoid containing core business logic.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What an API Gateway is
- Request routing
- Authentication
- Rate limiting
- Request aggregation
- Backend for Frontend (BFF)
- FastAPI example
- AI/ML example
- Gateway vs Load Balancer
- Gateway vs Reverse Proxy
- Best practices

______________________________________________________________________

# 🧠 Microservices Progress

You now understand:

- ✅ Monolith vs Microservices
- ✅ Database per Service
- ✅ Synchronous vs Asynchronous communication
- ✅ API Gateway

Next, we'll learn the **Saga Pattern**, which solves one of the biggest problems in distributed systems:

> **How do you keep multiple microservices consistent when one step fails?**

______________________________________________________________________

# What's Next

[Saga Pattern](40-saga-pattern.md)
