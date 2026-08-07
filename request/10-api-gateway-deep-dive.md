# Complete HTTP Request Lifecycle Deep Dive

## 10. API Gateway Deep Dive

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand why API Gateways exist, how they work internally, what happens when a request reaches an API Gateway, and why almost every microservice architecture uses one.

______________________________________________________________________

# Introduction

The request has now passed through

- Browser
- DNS
- TCP
- TLS
- CDN
- WAF
- Load Balancer
- Reverse Proxy

Finally,

it reaches

your backend infrastructure.

Most people think

the request now

goes directly

to

FastAPI.

That is true only for

small applications.

Large systems

such as

Amazon,

Netflix,

Uber,

Microsoft,

Airbnb

use

an

API Gateway.

______________________________________________________________________

# High-Level Flow

```
Client

↓

CDN

↓

WAF

↓

Load Balancer

↓

Reverse Proxy

↓

API Gateway

↓

User Service

↓

Order Service

↓

Payment Service

↓

Inventory Service
```

______________________________________________________________________

# Why Do We Need An API Gateway?

Imagine

you have

20 microservices.

```
User Service

Order Service

Inventory Service

Payment Service

Notification Service

Search Service

Analytics Service
```

Should

the browser

know

all of these

URLs?

Example

```
users.company.com

orders.company.com

inventory.company.com

payment.company.com
```

No.

Instead

everything goes through

one endpoint.

```
api.company.com
```

______________________________________________________________________

# Without API Gateway

```
Browser

↓

User Service

↓

Order Service

↓

Payment Service

↓

Inventory Service

↓

Notification Service
```

Problems

- Too many endpoints
- Authentication duplicated
- Logging duplicated
- Rate limiting duplicated
- Difficult versioning

______________________________________________________________________

# With API Gateway

```
Browser

↓

api.company.com

↓

API Gateway

↓

User Service

↓

Order Service

↓

Inventory Service

↓

Payment Service
```

Much cleaner.

______________________________________________________________________

# Real Production Architecture

```
Internet

↓

Cloudflare

↓

AWS WAF

↓

Application Load Balancer

↓

Nginx

↓

API Gateway

↓

Microservices
```

______________________________________________________________________

# Responsibilities

Interview favorite.

API Gateway

is responsible for

```
Routing

↓

Authentication

↓

Authorization

↓

Rate Limiting

↓

API Keys

↓

Logging

↓

Metrics

↓

Versioning

↓

Request Transformation

↓

Response Transformation
```

______________________________________________________________________

# What Happens Internally?

```
Incoming Request

↓

Parse HTTP Request

↓

Authentication

↓

Authorization

↓

Rate Limiting

↓

Route Matching

↓

Service Discovery

↓

Forward Request

↓

Receive Response

↓

Transform Response

↓

Return Client
```

Notice

the gateway

usually

doesn't execute

business logic.

______________________________________________________________________

# Step 1

# Receive Request

Browser sends

```
GET /users/123
```

Gateway receives

the request.

______________________________________________________________________

# Step 2

# Parse Request

Gateway parses

```
HTTP Method

↓

Headers

↓

Cookies

↓

JWT

↓

Body

↓

Query Parameters
```

Everything

is available

before

routing.

______________________________________________________________________

# Step 3

# Authentication

Interview favorite.

Gateway verifies

who

the user is.

Example

```
Authorization

Bearer JWT
```

Gateway checks

```
Signature

↓

Expiration

↓

Issuer

↓

Audience
```

If invalid

```
401 Unauthorized
```

The request

never reaches

FastAPI.

______________________________________________________________________

# Why Authenticate Here?

Instead of

every microservice

verifying

JWT,

the Gateway

does it

once.

Benefits

- Faster
- Simpler
- Consistent

______________________________________________________________________

# Step 4

# Authorization

Now

Gateway asks

```
Can this user

access

this API?
```

Example

```
Admin

↓

DELETE /users

Allowed
```

```
Normal User

↓

DELETE /users

Forbidden
```

Response

```
403 Forbidden
```

______________________________________________________________________

# Step 5

# Rate Limiting

Suppose

one client sends

```
10,000 Requests

per minute
```

Gateway detects

```
Limit Exceeded
```

Returns

```
429

Too Many Requests
```

Backend

never receives

the request.

______________________________________________________________________

# Common Algorithms

Interview favorite.

```
Token Bucket

↓

Leaky Bucket

↓

Sliding Window

↓

Fixed Window
```

We'll study

these

in depth

later.

______________________________________________________________________

# Step 6

# API Key Validation

Many APIs

require

```
X-API-Key
```

Gateway validates

the key

before

routing.

If invalid

```
403 Forbidden
```

______________________________________________________________________

# Step 7

# Route Matching

Gateway decides

which service

should receive

the request.

Example

```
GET /users

↓

User Service
```

```
POST /payments

↓

Payment Service
```

```
GET /products

↓

Catalog Service
```

______________________________________________________________________

# Path-Based Routing

```
/users/*

↓

User Service
```

```
/orders/*

↓

Order Service
```

```
/payments/*

↓

Payment Service
```

______________________________________________________________________

# Host-Based Routing

```
api.company.com

↓

API Cluster
```

```
admin.company.com

↓

Admin Cluster
```

______________________________________________________________________

# Step 8

# Service Discovery

Interview favorite.

Gateway

must find

the service.

Instead of

hardcoding

IP addresses,

it asks

Service Discovery.

```
Gateway

↓

Service Registry

↓

User Service

↓

10.1.4.12
```

Examples

- Kubernetes DNS
- Consul
- Eureka

______________________________________________________________________

# Step 9

# Request Transformation

Sometimes

the client

doesn't send

exactly

what

the service expects.

Gateway

can modify

the request.

Example

Add

```
Correlation ID
```

or

```
User ID
```

or

```
Tenant ID
```

______________________________________________________________________

# Example

Incoming

```
GET /orders
```

Gateway adds

```
X-User-ID

12345
```

Backend

doesn't need

to parse

the JWT again.

______________________________________________________________________

# Step 10

# Forward Request

Gateway opens

(or reuses)

a connection.

```
Gateway

↓

User Service
```

Only now

does

FastAPI

receive

the request.

______________________________________________________________________

# Step 11

# Response Transformation

Suppose

backend returns

```
Internal Fields

↓

Debug Data

↓

Database IDs
```

Gateway

removes

unnecessary data

before

returning

the response.

______________________________________________________________________

# Response Aggregation

Interview favorite.

Suppose

the mobile app

needs

```
User

Orders

Cart

Recommendations
```

Without Gateway

the app

makes

4 requests.

With Gateway

```
Browser

↓

Gateway

↓

User Service

↓

Order Service

↓

Cart Service

↓

Recommendation Service

↓

One Response
```

Gateway aggregates

everything.

______________________________________________________________________

# Versioning

Interview favorite.

Gateway supports

multiple versions.

```
/api/v1/users
```

```
/api/v2/users
```

Allows

old clients

to continue working.

______________________________________________________________________

# Canary Routing

Gateway

can send

```
95%

↓

Version 1
```

```
5%

↓

Version 2
```

Useful

for

safe deployments.

______________________________________________________________________

# A/B Testing

Different users

may receive

different versions.

Gateway decides

which version

to serve.

______________________________________________________________________

# Circuit Breaker

Interview favorite.

Suppose

Payment Service

is down.

Without protection

every request

waits

30 seconds.

Gateway

opens

the circuit.

```
Fail Fast
```

Users receive

an immediate

error

instead of

waiting.

______________________________________________________________________

# Retry Policy

Gateway

may retry

temporary failures.

```
Request

↓

Timeout

↓

Retry

↓

Success
```

Should only

retry

safe operations.

______________________________________________________________________

# Timeout

Gateway

prevents

requests

from hanging forever.

Example

```
Timeout

3 Seconds
```

After that

```
504 Gateway Timeout
```

______________________________________________________________________

# Observability

Gateway logs

every request.

Example

```
Timestamp

↓

Method

↓

URL

↓

User ID

↓

Latency

↓

Status Code
```

Metrics

and

traces

also begin

here.

______________________________________________________________________

# What Happens Inside The OS?

```
NIC

↓

Kernel

↓

Socket

↓

Gateway Process

↓

Authentication

↓

Routing

↓

Backend Socket

↓

Microservice
```

Gateway

is just another

server process

using sockets,

threads

or

event loops.

______________________________________________________________________

# API Gateway vs Reverse Proxy

Interview favorite.

| Reverse Proxy | API Gateway |
|---------------|-------------|
| Routes traffic | Routes APIs |
| SSL Termination | Authentication |
| Compression | Authorization |
| Static Files | API Keys |
| Caching | Rate Limiting |
| Proxy Headers | Versioning |
| Backend Routing | Response Aggregation |

Many products

support both.

Example

Envoy.

______________________________________________________________________

# Common Failures

## Authentication Server Down

Gateway

may reject

all requests

or

use cached tokens.

______________________________________________________________________

## Service Registry Down

Gateway

cannot locate

backend services.

______________________________________________________________________

## Slow Backend

Gateway

returns

```
504

Gateway Timeout
```

______________________________________________________________________

# Common Attacks

## JWT Tampering

Modified token.

Gateway verifies

signature.

Blocked.

______________________________________________________________________

## API Key Theft

Stolen key.

Gateway

supports

rotation

and revocation.

______________________________________________________________________

## Rate Limit Bypass

Attackers

use

multiple IPs.

Gateway combines

rate limiting

with

user identity.

______________________________________________________________________

## Header Spoofing

Attacker sets

```
X-User-ID
```

Gateway

must overwrite

trusted headers

before

forwarding.

______________________________________________________________________

# Popular API Gateways

Cloud

```
AWS API Gateway

Azure API Management

Google API Gateway
```

Open Source

```
Kong

Apache APISIX

Envoy

Traefik

NGINX Plus
```

Service Mesh

```
Istio Gateway
```

______________________________________________________________________

# Technologies Used

| Feature | Technologies |
|----------|--------------|
| API Gateway | Kong, APISIX, AWS API Gateway |
| Authentication | JWT, OAuth2, OIDC |
| Discovery | Consul, Eureka, Kubernetes DNS |
| Rate Limiting | Redis, Token Bucket |
| Observability | OpenTelemetry, Prometheus |

______________________________________________________________________

# Common Interview Questions

## Why use an API Gateway?

An API Gateway centralizes authentication, authorization, routing, rate limiting, logging, API versioning, and request
transformation, allowing microservices to focus on business logic.

______________________________________________________________________

## How is an API Gateway different from a Reverse Proxy?

A Reverse Proxy primarily forwards traffic and handles infrastructure concerns such as TLS termination and compression.
An API Gateway adds API-specific functionality such as JWT validation, API key management, response aggregation, and
versioning.

______________________________________________________________________

## Why authenticate at the Gateway instead of every microservice?

Validating tokens once at the Gateway reduces duplicate work, simplifies microservices, improves consistency, and
reduces latency.

______________________________________________________________________

## What is response aggregation?

The API Gateway calls multiple backend services, combines their responses into one payload, and returns a single
response to the client.

______________________________________________________________________

## What is service discovery?

Service discovery allows the Gateway to dynamically locate backend services without hardcoding IP addresses, enabling
autoscaling and rolling deployments.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when a request reaches an API Gateway.

### Answer

The API Gateway parses the HTTP request, validates authentication credentials such as JWTs or API keys, performs
authorization checks, applies rate limiting and other policies, determines the target service using routing rules and
service discovery, forwards the request to the appropriate backend service, optionally transforms the request or
response, records logs and metrics, and returns the final response to the client.

______________________________________________________________________

# Summary

The API Gateway is the entry point to a microservice architecture.

Key concepts include

- Authentication
- Authorization
- API Keys
- Rate Limiting
- Service Discovery
- Request Transformation
- Response Aggregation
- Versioning
- Circuit Breakers
- Retries
- Timeouts
- Observability

At this point, the request has successfully entered your application platform and is about to reach the **application
server** (such as Uvicorn/Gunicorn) that will hand it over to your FastAPI application.

______________________________________________________________________

# Next

[11. Service Discovery and Service Mesh](11-service-discovery-and-service-mesh.md)
