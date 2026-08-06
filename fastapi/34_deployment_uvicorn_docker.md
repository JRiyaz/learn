# Deployment (Uvicorn, Gunicorn & Docker)

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 11 - Deployment
>
> **File:** `34_deployment_uvicorn_docker.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Deployment is
- Development vs Production
- ASGI Servers
- Uvicorn
- Gunicorn
- Worker Processes
- Reverse Proxies
- Docker Deployment
- Environment Variables
- Production Best Practices

______________________________________________________________________

# What is Deployment?

Deployment is the process of making your application available to users.

Development

```
Laptop

↓

localhost
```

Production

```
Internet

↓

Real Users
```

______________________________________________________________________

# Development vs Production

Development

- Debugging
- Auto Reload
- Single User
- Local Machine

Production

- High Performance
- Secure
- Multiple Users
- Fault Tolerant

______________________________________________________________________

# Development Server

Typical command

```bash
uvicorn app.main:app --reload
```

The `--reload` flag watches files and restarts automatically.

Do **not** use it in production.

______________________________________________________________________

# What is ASGI?

ASGI stands for

```
Asynchronous

Server

Gateway

Interface
```

It is the modern Python interface for asynchronous web applications.

FastAPI is an ASGI application.

______________________________________________________________________

# ASGI Flow

```
Client

↓

ASGI Server

↓

FastAPI

↓

Response
```

The ASGI server receives network requests and invokes your application.

______________________________________________________________________

# What is Uvicorn?

Uvicorn is a lightweight,

high-performance ASGI server.

Responsibilities

- Accept HTTP connections
- Run the FastAPI application
- Send responses

______________________________________________________________________

# Running Uvicorn

Development

```bash
uvicorn app.main:app --reload
```

Production

```bash
uvicorn app.main:app
```

______________________________________________________________________

# Uvicorn Workers

Production example

```bash
uvicorn app.main:app --workers 4
```

Flow

```
Incoming Requests

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

Each worker is a separate process.

______________________________________________________________________

# Why Multiple Workers?

Single Worker

```
One CPU Core
```

Multiple Workers

```
Multiple CPU Cores
```

More workers generally improve concurrency,

up to the limits of available CPU and memory.

______________________________________________________________________

# What is Gunicorn?

Gunicorn is a process manager.

It manages multiple worker processes.

Example

```
Gunicorn

↓

Worker

↓

Worker

↓

Worker
```

Historically,

Gunicorn has been widely used to manage Uvicorn workers on Linux.

______________________________________________________________________

# Gunicorn + Uvicorn

Example

```bash
gunicorn app.main:app \

-k uvicorn.workers.UvicornWorker \

-w 4
```

Gunicorn

↓

Starts workers

↓

Workers run FastAPI.

> **Note:** Newer versions of Uvicorn also support built-in worker management (`uvicorn --workers`), and many deployments use that instead of Gunicorn.

______________________________________________________________________

# Worker Lifecycle

```
Request

↓

Worker

↓

FastAPI

↓

Response
```

If one worker crashes,

the process manager can start a replacement.

______________________________________________________________________

# Reverse Proxy

Clients usually do **not** connect directly to FastAPI.

Typical production architecture

```
Internet

↓

Nginx

↓

Uvicorn

↓

FastAPI
```

______________________________________________________________________

# Why Reverse Proxy?

A reverse proxy can provide

- HTTPS termination
- Load balancing
- Static file serving
- Compression
- Request buffering
- Security features

Common reverse proxies include

- Nginx
- Apache
- Traefik
- Caddy

______________________________________________________________________

# Deployment Flow

```
Browser

↓

HTTPS

↓

Nginx

↓

Uvicorn

↓

FastAPI
```

______________________________________________________________________

# Docker

Docker packages the application and its dependencies into a portable container.

Benefits

- Consistent environments
- Easy deployment
- Isolation
- Reproducibility

______________________________________________________________________

# Simple Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [

"uvicorn",

"app.main:app",

"--host",

"0.0.0.0",

"--port",

"8000"

]
```

______________________________________________________________________

# Build Image

```bash
docker build -t fastapi-app .
```

Creates a Docker image.

______________________________________________________________________

# Run Container

```bash
docker run -p 8000:8000 fastapi-app
```

Access

```
http://localhost:8000
```

______________________________________________________________________

# Environment Variables

Avoid hard-coding secrets.

Bad

```python
DATABASE_URL =

"postgres://..."
```

Better

```python
DATABASE_URL =

os.getenv(

    "DATABASE_URL"
)
```

Common configuration

- Database URL
- Secret Keys
- API Keys
- Logging Level

______________________________________________________________________

# Health Checks

Many deployments expose

```
GET /health
```

Response

```json
{
    "status": "healthy"
}
```

Load balancers and orchestration platforms use health checks to determine whether the application is ready to receive
traffic.

______________________________________________________________________

# Logging

Production applications should log

- Startup
- Shutdown
- Requests
- Errors
- Warnings

Avoid relying on `print()` statements.

______________________________________________________________________

# Graceful Shutdown

```
SIGTERM

↓

Finish Requests

↓

Close Database

↓

Shutdown
```

Graceful shutdown minimizes interrupted requests.

______________________________________________________________________

# Scaling

Single Server

```
Users

↓

FastAPI
```

Horizontal Scaling

```
Users

↓

Load Balancer

↓

FastAPI

FastAPI

FastAPI
```

Multiple application instances share traffic.

______________________________________________________________________

# Deployment Checklist

- HTTPS Enabled
- Environment Variables
- Logging Configured
- Health Check Endpoint
- Database Migrations Applied
- Monitoring Enabled
- Secrets Managed Securely
- Auto Restart Configured

______________________________________________________________________

# Common Mistakes

❌ Running with `--reload` in production

❌ Hard-coding secrets

❌ Running only one worker for high traffic

❌ Exposing development settings publicly

❌ Skipping health checks

______________________________________________________________________

# Production Best Practices

- Use an ASGI server such as Uvicorn.
- Run multiple workers when appropriate.
- Place a reverse proxy in front of the application.
- Containerize with Docker.
- Store configuration in environment variables.
- Enable structured logging.
- Expose health endpoints.
- Apply database migrations during deployment.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is a reverse proxy commonly placed in front of a FastAPI application in production?**

### Answer

A reverse proxy improves security, performance, and operational flexibility.

It can provide:

- HTTPS termination.
- Load balancing.
- Static file serving.
- Request buffering.
- Compression.
- Security filtering.
- Centralized access logging.

FastAPI focuses on application logic,

while the reverse proxy handles network-level responsibilities.

______________________________________________________________________

# Summary

In this chapter you learned:

- Deployment
- ASGI
- Uvicorn
- Gunicorn
- Worker Processes
- Reverse Proxy
- Docker
- Environment Variables
- Health Checks
- Production Best Practices

Deploying FastAPI for production involves much more than starting a server. A robust deployment includes an ASGI server,
proper process management, containerization, secure configuration, logging, health checks, and infrastructure components
such as reverse proxies.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is deployment?
1. What is ASGI?
1. Why does FastAPI require an ASGI server?

______________________________________________________________________

## Uvicorn

4. What is Uvicorn?
1. Why shouldn't `--reload` be used in production?
1. Why use multiple workers?

______________________________________________________________________

## Gunicorn

7. What is Gunicorn?
1. How does Gunicorn differ from Uvicorn?
1. When would you use Gunicorn with Uvicorn workers?

______________________________________________________________________

## Infrastructure

10. What is a reverse proxy?
01. Why are reverse proxies commonly used?
01. Why are health check endpoints important?

______________________________________________________________________

## Docker

13. Why containerize a FastAPI application?
01. Why should configuration come from environment variables?
01. Why should secrets never be committed to source control?

______________________________________________________________________

## Scenario-Based

16. Your FastAPI application is running with `uvicorn --reload` in production. What problems could this cause?
01. Your application receives far more traffic than a single CPU core can handle. What deployment changes would improve throughput?
01. Your backend is deployed behind Nginx. Which responsibilities should Nginx handle, and which should FastAPI handle?
01. Your Docker image contains hard-coded database credentials. Why is this insecure, and how should configuration be managed instead?
01. Your load balancer needs to determine whether application instances are healthy before routing requests. How does a health check endpoint support this?

______________________________________________________________________

# Next

[Observability (Logging, Health Checks)](35_observability.md)
