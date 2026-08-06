# Flask Interview Questions & System Design

> **Course:** Flask for Backend Engineers
>
> **Module:** 10
>
> **File:** `22_flask_interview_questions.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will be able to confidently answer interview questions related to:

- Flask Fundamentals
- Routing
- Request Lifecycle
- Templates
- Blueprints
- Application Factory
- SQLAlchemy
- Authentication
- Authorization
- REST APIs
- Deployment
- Docker
- Kubernetes
- Production Architecture
- System Design

______________________________________________________________________

# Interview Strategy

For a **5+ years Backend Engineer**, interviewers expect you to explain

- Why
- Trade-offs
- Production Considerations
- Best Practices

rather than just definitions.

Whenever possible, answer using

```
Concept

↓

Reason

↓

Real Example

↓

Trade-offs
```

______________________________________________________________________

# Question 1

## What happens internally when a request reaches a Flask application?

### Answer

The request lifecycle is:

```
Browser

↓

Nginx

↓

Gunicorn

↓

WSGI

↓

Flask

↓

Middleware

↓

Blueprint

↓

Route

↓

Service Layer

↓

Database

↓

Response

↓

Gunicorn

↓

Nginx

↓

Browser
```

Internally, Flask creates request and application contexts, matches the route, executes the view function, generates a
response, and finally tears down the request context.

______________________________________________________________________

# Question 2

## Why should large Flask applications use Blueprints?

### Answer

Blueprints organize applications by feature instead of keeping hundreds of routes in one file.

Benefits include:

- Better maintainability
- Modular development
- Easier testing
- Reduced merge conflicts
- Reusable components

They improve code organization but should not contain business logic.

______________________________________________________________________

# Question 3

## Why is the Application Factory Pattern considered a best practice?

### Answer

It separates application creation from application usage.

Benefits:

- Multiple environments
- Easier testing
- Better extension initialization
- Reduced circular imports
- Cleaner architecture

Almost every production Flask application uses this pattern.

______________________________________________________________________

# Question 4

## Explain Flask's request context and application context.

### Answer

Flask uses context objects to avoid passing application and request objects everywhere.

Application Context

Provides

- `current_app`
- `g`

Request Context

Provides

- `request`
- `session`

Each incoming request gets its own request context.

Contexts are automatically pushed before request processing and popped afterward.

______________________________________________________________________

# Question 5

## Why shouldn't business logic be placed inside Flask routes?

### Answer

Routes should only handle HTTP concerns.

Responsibilities include:

- Read Request
- Validate Input
- Call Service
- Return Response

Business rules belong in service classes.

Benefits:

- Easier testing
- Better reuse
- Cleaner architecture

______________________________________________________________________

# Question 6

## Explain SQLAlchemy Session.

### Answer

The Session is a Unit of Work.

Flow

```
Objects

↓

Tracked

↓

Commit

↓

Database
```

The session tracks changes until `commit()`.

If an error occurs,

`rollback()` restores a consistent state.

______________________________________________________________________

# Question 7

## Difference between Authentication and Authorization?

### Answer

Authentication

```
Who are you?
```

Authorization

```
What can you do?
```

Authentication identifies the user.

Authorization checks permissions after authentication succeeds.

______________________________________________________________________

# Question 8

## Why should passwords be hashed instead of encrypted?

### Answer

Authentication requires verification,

not recovery of the original password.

Hashing is one-way,

making stolen password databases significantly harder to exploit.

Encryption is reversible,

making it less appropriate for password storage.

______________________________________________________________________

# Question 9

## Why use JWT instead of Sessions?

### Answer

Sessions

- Browser applications
- Server-side session storage
- Cookie-based

JWT

- APIs
- Mobile applications
- Stateless authentication

JWT scales well for distributed APIs,

but token revocation and lifecycle management require careful design.

______________________________________________________________________

# Question 10

## Explain REST.

### Answer

REST is an architectural style where resources are exposed through HTTP.

Example

```
GET /users

POST /users

PATCH /users/1

DELETE /users/1
```

Characteristics

- Stateless
- Resource-oriented
- Standard HTTP methods
- Consistent interfaces

______________________________________________________________________

# Question 11

## Why shouldn't Flask serve static files in production?

### Answer

Flask is optimized for dynamic application logic.

Nginx is significantly better at:

- Static file serving
- Compression
- Caching
- HTTPS
- Load balancing

Static assets should be served by Nginx or a CDN.

______________________________________________________________________

# Question 12

## Explain Gunicorn.

### Answer

Gunicorn is a WSGI server.

Responsibilities

- Run multiple worker processes
- Execute Flask code
- Return responses

Gunicorn is usually deployed behind Nginx.

______________________________________________________________________

# Question 13

## Why Docker?

### Answer

Docker packages

- Application
- Python
- Dependencies

into a portable container.

Benefits

- Environment consistency
- Easier deployment
- Faster onboarding
- Better scalability

______________________________________________________________________

# Question 14

## Why Kubernetes?

### Answer

Docker manages containers.

Kubernetes manages thousands of containers.

Features

- Auto-healing
- Auto-scaling
- Rolling updates
- Service discovery
- Load balancing

______________________________________________________________________

# Question 15

## Explain the production deployment architecture.

### Answer

```
Internet

↓

Load Balancer

↓

Nginx

↓

Gunicorn

↓

Flask

↓

Redis

↓

PostgreSQL
```

Background jobs

```
Celery

↓

Redis

↓

Workers
```

Monitoring

```
Prometheus

↓

Grafana
```

Logging

```
CloudWatch

or

ELK
```

______________________________________________________________________

# System Design Question 1

## Design a URL Shortener

Requirements

- Generate Short URLs
- Redirect Quickly
- Analytics
- Expiration

Architecture

```
Load Balancer

↓

Flask API

↓

Redis Cache

↓

PostgreSQL

↓

Celery

↓

Analytics Worker
```

Discussion Points

- Base62 encoding
- Cache popular URLs
- Rate limiting
- Database indexing

______________________________________________________________________

# System Design Question 2

## Design an E-commerce Backend

Architecture

```
API Gateway

↓

Flask Services

↓

Authentication

↓

Orders

↓

Inventory

↓

Payments

↓

Redis

↓

RabbitMQ

↓

Celery

↓

PostgreSQL
```

Topics to Discuss

- Inventory consistency
- Payment retries
- Background tasks
- Event-driven communication
- Idempotency

______________________________________________________________________

# System Design Question 3

## Design a Notification Service

Requirements

- Email
- SMS
- Push Notifications

Architecture

```
API

↓

Queue

↓

Celery

↓

Workers

↓

Email

SMS

Push
```

Topics

- Retries
- Dead Letter Queues
- Rate limiting
- Monitoring

______________________________________________________________________

# System Design Question 4

## Design a File Upload Service

Architecture

```
Browser

↓

Pre-signed URL

↓

Amazon S3

↓

Notification

↓

Flask

↓

Database
```

Advantages

- Reduced server load
- Faster uploads
- Better scalability

______________________________________________________________________

# Frequently Asked Follow-up Questions

- Why Blueprints?
- Why Application Factory?
- Why Gunicorn?
- Why Nginx?
- Why SQLAlchemy?
- Why JWT?
- Why Celery?
- Why Redis?
- Why Docker?
- Why Kubernetes?
- Why REST?
- Why Microservices?
- Why API Gateway?

Interviewers often ask "Why?" after every technical decision.

Be prepared to discuss trade-offs rather than presenting technologies as universally correct.

______________________________________________________________________

# Last-Minute Revision Checklist

✅ Flask Request Lifecycle

✅ Routing

✅ Blueprints

✅ Application Factory

✅ SQLAlchemy

✅ Alembic

✅ Authentication

✅ Authorization

✅ REST APIs

✅ Error Handling

✅ Logging

✅ Testing

✅ Celery

✅ Gunicorn

✅ Nginx

✅ Docker

✅ Kubernetes

✅ Deployment

______________________________________________________________________

# Summary

Congratulations!

You have completed the Flask course.

You now understand:

- Flask Fundamentals
- Production Architecture
- Authentication
- Authorization
- SQLAlchemy
- REST APIs
- Celery
- Docker
- Kubernetes
- Deployment
- Enterprise Best Practices

This knowledge covers the core Flask topics commonly expected in backend engineering interviews and production
application development.

______________________________________________________________________

# Final Practice Questions

1. Explain the complete lifecycle of a Flask request.
1. Why use Blueprints?
1. Why use the Application Factory Pattern?
1. Explain SQLAlchemy Sessions.
1. What is the difference between Authentication and Authorization?
1. Why hash passwords?
1. Explain JWT Authentication.
1. Design a production-ready Flask deployment.
1. Explain Docker vs Kubernetes.
1. Design a scalable Flask backend for an e-commerce platform.
1. How would you secure a Flask REST API?
1. How would you deploy Flask on AWS using ECS or Kubernetes?
1. How would you scale a Flask application to handle millions of requests?
1. Explain how Celery integrates with Flask.
1. What architectural changes would you make when migrating a Flask monolith to microservices?

______________________________________________________________________

# End of Course 🎉

You have completed all **22 files** of the Flask course.

The next step is to strengthen your understanding by solving practical problems and answering interview-style questions.
A dedicated question bank and mini-project series would be a natural continuation of this course.
