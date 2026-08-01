# Docker - Part 25

# Docker Project - Part 8

# Productionizing the Application

______________________________________________________________________

# Introduction

Our Library API is now fully functional.

It supports:

- FastAPI
- PostgreSQL
- Redis
- Kafka
- Docker Compose
- CRUD Operations
- Redis Caching
- Kafka Events

However,

there's a difference between

**working**

and

**production-ready**.

In this chapter,

we'll improve our application using production best practices.

______________________________________________________________________

# Current Architecture

```text
                Browser

                   │

                   ▼

               FastAPI

      ┌────────┼────────┐

      ▼        ▼        ▼

 PostgreSQL  Redis    Kafka
```

The architecture is good.

Now we'll improve how it's deployed.

______________________________________________________________________

# Production Checklist

A production application should have

```text
✓ Small Images

✓ Health Checks

✓ Non-root User

✓ Environment Variables

✓ Proper Logging

✓ Restart Policies

✓ Resource Limits
```

We'll review each of these.

______________________________________________________________________

# Multi-Stage Dockerfile

Instead of a single-stage build,

use a multi-stage build.

```dockerfile
FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --prefix=/install \
    -r requirements.txt

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

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

The final image

contains only

what the application needs.

______________________________________________________________________

# Running as a Non-Root User

Update

the runtime stage.

```dockerfile
RUN useradd \
    --create-home \
    appuser

USER appuser
```

The application

no longer runs

as

```text
root
```

______________________________________________________________________

# Health Check

Docker should know

whether the application

is healthy.

```dockerfile
HEALTHCHECK \
CMD curl -f http://localhost:8000/health || exit 1
```

If the endpoint fails,

Docker marks

the container

as unhealthy.

______________________________________________________________________

# Environment Variables

Never hardcode

configuration.

Good

```text
DATABASE_URL

REDIS_URL

KAFKA_BROKER
```

Bad

```python
DATABASE_URL = "postgresql://..."
```

The same image

should work

across development,

staging,

and production.

______________________________________________________________________

# Logging

Application logs

should be written to

```text
stdout

stderr
```

Avoid writing logs

to files inside containers.

Container platforms

collect stdout automatically.

______________________________________________________________________

# Restart Policy

Update

`compose.yaml`

```yaml
services:

  api:

    restart: unless-stopped
```

Now

Docker restarts

the application

after unexpected failures.

> Restart policies are useful for local development and standalone Docker deployments. In Kubernetes, restart behavior is managed by the orchestrator instead.

______________________________________________________________________

# Resource Limits

Limit CPU

and memory.

Example

```yaml
services:

  api:

    deploy:

      resources:

        limits:

          cpus: "1"

          memory: 512M
```

This prevents

one container

from consuming

all host resources.

> The `deploy` section is primarily used by Docker Swarm. For local Docker Compose, resource limit support depends on the Compose implementation. We'll revisit production resource management in the Kubernetes module.

______________________________________________________________________

# Image Versioning

Avoid

```text
latest
```

Use

```text
library-api:v1.0.0
```

Versioned images

make deployments

predictable

and easier to roll back.

______________________________________________________________________

# Database Credentials

Development

```text
compose.yaml
```

Production

```text
Secret Manager

↓

Environment Variables

↓

Application
```

Never commit

production credentials.

______________________________________________________________________

# Network Exposure

Current

```text
Browser

↓

FastAPI

↓

PostgreSQL
```

This isn't ideal.

Instead

```text
Browser

↓

FastAPI

↓

Internal Network

↓

PostgreSQL
```

Only FastAPI

should be publicly accessible.

Redis

Kafka

and PostgreSQL

should remain internal.

______________________________________________________________________

# Monitoring Readiness

Health endpoint

```http
GET /health
```

Expected

```json
{
    "status": "healthy"
}
```

Monitoring systems

can use this endpoint

to verify availability.

______________________________________________________________________

# Graceful Shutdown

When Docker stops

the application,

FastAPI should finish

active requests

before exiting.

```text
SIGTERM

↓

Finish Requests

↓

Shutdown
```

This improves reliability

during deployments.

______________________________________________________________________

# Build Process

Production build

```bash
docker build \
-t library-api:v1.0.0 .
```

Run

```bash
docker run \
-p 8000:8000 \
library-api:v1.0.0
```

Every deployment

uses

a specific version.

______________________________________________________________________

# Deployment Flow

```text
Code

↓

Build Image

↓

Push Image

↓

Deploy

↓

Health Check

↓

Serve Traffic
```

This is the basic lifecycle

used in many containerized deployments.

______________________________________________________________________

# Current Architecture

```text
             Browser

                │

                ▼

            FastAPI

      ┌─────────┼─────────┐

      ▼         ▼         ▼

 PostgreSQL   Redis     Kafka
```

Every component

is now

containerized

and production-ready

for a single-container deployment model.

______________________________________________________________________

# Common Mistakes

### Using latest

Always

version your images.

______________________________________________________________________

### Running as Root

Use

a dedicated application user.

______________________________________________________________________

### Exposing Internal Services

Only expose

services

that clients

must access.

______________________________________________________________________

### Hardcoding Secrets

Configuration belongs

outside

the image.

______________________________________________________________________

### Ignoring Health Checks

Health checks

help detect

failed applications

automatically.

______________________________________________________________________

# Best Practices

- Use multi-stage builds.
- Run as a non-root user.
- Keep images small.
- Version every image.
- Log to stdout.
- Keep secrets external.
- Publish only required ports.
- Configure restart policies.
- Add health checks.

______________________________________________________________________

# Hands-on Exercise

1. Convert your Dockerfile into a multi-stage build.
1. Create a non-root user.
1. Add a health check.
1. Add a restart policy.
1. Build a versioned image.
1. Remove hardcoded configuration.
1. Verify only the API is publicly exposed.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What changes would you make before deploying a Dockerized FastAPI application to production?

Before deployment, I would use a multi-stage Docker build, run the application as a non-root user, pin image versions,
externalize configuration through environment variables or a secret manager, expose only the required ports, add health
checks, configure restart policies where appropriate, log to stdout/stderr, and ensure the application uses a minimal
base image with only the required runtime dependencies.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Production Docker images
- Multi-stage builds
- Non-root users
- Health checks
- Restart policies
- Resource limits
- Versioned images
- Logging
- Secret management
- Deployment workflow

Our Docker project is now close to production quality.

In the next and final chapter, we'll review the complete project, discuss possible enhancements, provide additional
exercises, and summarize everything you've learned throughout the Docker module.

______________________________________________________________________

## Next File

[Docker Project - Part 9](26-docker-project-part-9.md)
