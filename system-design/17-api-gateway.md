# API Gateway

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand what an API Gateway is, why it is used in microservices, how it differs from a Load Balancer and Reverse Proxy, and how to confidently answer API Gateway questions in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

you have

only

one service.

```
Client

↓

Backend
```

Simple.

Now imagine

a real application.

```
Authentication

Order

Payment

Inventory

Notification

Analytics

Recommendation
```

Should

the mobile app

call

all these services

directly?

Probably not.

Instead,

we introduce

an

```
API Gateway
```

______________________________________________________________________

# What Is An API Gateway?

An API Gateway

is

the single entry point

for clients.

Instead of

```
Client

↓

10 Services
```

we have

```
Client

↓

API Gateway

↓

Microservices
```

The client

communicates

with

only

one endpoint.

______________________________________________________________________

# Why Do We Need An API Gateway?

Without API Gateway

```
Mobile App

↓

Authentication

↓

Orders

↓

Payments

↓

Inventory

↓

Notification

↓

Analytics
```

The client

must know

every service.

Very difficult

to maintain.

______________________________________________________________________

# With API Gateway

```
Client

↓

API Gateway

↓

Authentication

↓

Orders

↓

Payments

↓

Inventory
```

The client

knows

only

the gateway.

______________________________________________________________________

# Real World Example

Imagine

an airport.

Passengers

don't go

directly

to

runways.

Instead,

they go through

```
Security

↓

Check-in

↓

Immigration

↓

Boarding
```

The airport entrance

acts like

an API Gateway.

Every request

passes

through

one place.

______________________________________________________________________

# Basic Architecture

```
                Client
                   │
                   ▼
          ┌────────────────┐
          │  API Gateway   │
          └───────┬────────┘
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 Auth Service  Order Service  Payment Service
                    │
                    ▼
             Inventory Service
```

______________________________________________________________________

# Responsibilities

An API Gateway

can perform

many tasks.

- Routing
- Authentication
- Authorization
- SSL Termination
- Rate Limiting
- Logging
- Request Validation
- Response Aggregation
- Caching
- Monitoring

Think of it as

the front door

to your backend.

______________________________________________________________________

# Request Routing

Suppose

the client calls

```
GET /orders
```

Gateway routes

the request

to

```
Order Service
```

Example

```
/auth/*

↓

Authentication Service
```

```
/payments/*

↓

Payment Service
```

```
/users/*

↓

User Service
```

______________________________________________________________________

# Authentication

Instead of

every service

verifying JWT tokens,

the gateway

can verify them

once.

```
Client

↓

JWT

↓

Gateway

↓

Verified

↓

Forward Request
```

Services

receive

trusted requests.

______________________________________________________________________

# Authorization

The Gateway

can check

permissions.

Example

```
Admin

↓

Allowed
```

```
Guest

↓

403 Forbidden
```

Some organizations

also perform

fine-grained authorization

inside individual services.

______________________________________________________________________

# SSL Termination

Instead of

every service

handling HTTPS,

the gateway

decrypts

HTTPS traffic.

```
HTTPS

↓

Gateway

↓

HTTP

↓

Services
```

Benefits

- Less CPU usage
- Easier certificate management

______________________________________________________________________

# Rate Limiting

Interview favorite.

Suppose

one user

sends

```
100,000 Requests
```

The gateway

can stop

abuse.

Example

```
100 Requests

Per Minute
```

Extra requests

receive

```
429

Too Many Requests
```

______________________________________________________________________

# Request Validation

Gateway

can reject

invalid requests

before

they reach

backend services.

Example

Missing

Authorization Header

↓

Reject

______________________________________________________________________

# Response Aggregation

Suppose

the client

needs

```
User

Orders

Recommendations
```

Without Gateway

```
Client

↓

3 API Calls
```

With Gateway

```
Client

↓

One Request

↓

Gateway

↓

3 Services

↓

Combined Response
```

Very useful

for mobile applications.

______________________________________________________________________

# Request Transformation

Suppose

an old client

sends

```
firstName
```

New service

expects

```
given_name
```

Gateway

can transform

requests

without changing

the client.

______________________________________________________________________

# Response Transformation

Similarly,

responses

can also

be modified.

Example

Internal format

↓

Public API format

Useful

during API version upgrades.

______________________________________________________________________

# API Versioning

Gateway

can route

different versions.

Example

```
/v1/users

↓

Service V1
```

```
/v2/users

↓

Service V2
```

Allows

gradual migration.

______________________________________________________________________

# Caching

Gateway

can cache

responses.

Example

```
GET /countries
```

Static data.

No need

to call

the backend

every time.

______________________________________________________________________

# Logging

Every request

passes

through

the Gateway.

Perfect place

to log

- User
- IP
- Endpoint
- Response Time
- Status Code

______________________________________________________________________

# Monitoring

Gateway

can collect

metrics.

Example

- Requests/sec
- Error Rate
- Latency
- Active Users
- Authentication Failures

Useful

for dashboards

and alerts.

______________________________________________________________________

# Circuit Breaker

Suppose

Payment Service

is down.

Gateway

can stop

sending requests

temporarily.

Instead of

waiting

30 seconds,

respond quickly

with

```
Service Unavailable
```

Improves

user experience.

______________________________________________________________________

# API Gateway vs Load Balancer

Interview favorite.

Load Balancer

```
Distributes

Traffic
```

API Gateway

```
Processes

API Requests
```

Load Balancer

operates

primarily

at

network

or

application level

to distribute traffic.

API Gateway

adds

application-specific features.

______________________________________________________________________

# API Gateway vs Reverse Proxy

Reverse Proxy

```
Routes

Requests
```

API Gateway

```
Routes

+

Authentication

+

Rate Limiting

+

Caching

+

Monitoring

+

Transformation
```

An API Gateway

often includes

reverse proxy

capabilities,

plus much more.

______________________________________________________________________

# Internal vs External Gateway

Large organizations

sometimes use

two gateways.

```
Internet

↓

External Gateway

↓

Internal Gateway

↓

Microservices
```

Adds

security

and

better separation.

______________________________________________________________________

# Typical Microservice Architecture

```
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Authentication

↓

Orders

↓

Payments

↓

Inventory

↓

RabbitMQ

↓

Notifications
```

Notice

the Gateway

comes

after

the Load Balancer.

______________________________________________________________________

# Popular API Gateways

Examples

- Kong
- NGINX
- Traefik
- Envoy
- AWS API Gateway
- Apigee
- Spring Cloud Gateway

Interviewers

care

more about

concepts

than products.

______________________________________________________________________

# Common Interview Questions

## Why not let clients call services directly?

Direct communication

creates

tight coupling,

exposes

internal architecture,

and increases

client complexity.

An API Gateway

provides

one stable interface.

______________________________________________________________________

## Does an API Gateway replace a Load Balancer?

No.

A Load Balancer

distributes traffic.

An API Gateway

handles

API-specific concerns

such as

authentication,

rate limiting,

routing,

and aggregation.

Many systems

use both.

______________________________________________________________________

## Should every microservice have its own authentication?

Usually,

authentication

is performed

at the Gateway,

while services

may still enforce

authorization

based on business rules.

______________________________________________________________________

## Can an API Gateway become a bottleneck?

Yes.

Because

all requests

pass through it.

Solutions

include

horizontal scaling,

multiple gateway instances,

and load balancing.

______________________________________________________________________

# Common Mistakes

## Putting Business Logic Inside Gateway

The Gateway

should focus

on

cross-cutting concerns,

not

core business logic.

______________________________________________________________________

## Using Gateway As Database

The Gateway

never

stores

business data.

______________________________________________________________________

## Forgetting High Availability

Gateway

must itself

be scalable

and redundant.

______________________________________________________________________

## Confusing Gateway With Service Discovery

Service discovery

helps services

find each other.

Gateway

helps clients

reach services.

Different responsibilities.

______________________________________________________________________

# Best Practices

✅ Keep the Gateway lightweight.

✅ Centralize authentication and rate limiting.

✅ Scale the Gateway horizontally.

✅ Avoid business logic.

✅ Monitor latency and error rates.

✅ Version APIs cleanly.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the primary purpose of an API Gateway?

### Answer

An API Gateway provides a single entry point for clients, handling request routing, authentication, rate limiting,
logging, monitoring, and other cross-cutting concerns before forwarding requests to backend services.

______________________________________________________________________

## Question

Why is response aggregation useful?

### Answer

Instead of forcing clients to make multiple API calls, the Gateway can collect responses from multiple services and
return a single combined response, reducing network overhead and improving client performance.

______________________________________________________________________

## Question

Can an API Gateway become a Single Point of Failure?

### Answer

Yes. That's why production systems deploy multiple Gateway instances behind a Load Balancer with health checks and
automatic failover.

______________________________________________________________________

# Practice Exercise

For each application,

answer

1. Would an API Gateway be useful?
1. Which responsibilities should the Gateway handle?
1. Should it perform authentication?
1. Would response aggregation help?
1. Would caching be appropriate?

Applications

- E-commerce Platform
- Banking System
- Food Delivery
- Ride Sharing
- Netflix
- Social Media
- Chat Application
- Online Learning Platform

Explain

your reasoning

based on

security,

performance,

and

client simplicity.

______________________________________________________________________

# Summary

An API Gateway is the front door of a microservices architecture.

It provides

- A single entry point
- Request routing
- Authentication
- Rate limiting
- Logging
- Monitoring
- Response aggregation
- API versioning
- Cross-cutting concerns

It simplifies clients, improves security, and centralizes common functionality, making it a core component of modern
distributed systems and a frequent topic in System Design interviews.

______________________________________________________________________

# Next

[Service Discovery](18-service-discovery.md)
