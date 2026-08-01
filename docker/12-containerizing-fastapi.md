# Docker - Part 12

# Containerizing FastAPI

______________________________________________________________________

# Introduction

So far, we've learned:

- Docker Fundamentals
- Docker Architecture
- Images & Containers
- Dockerfiles
- Multi-Stage Builds
- Docker Networking
- Volumes
- Docker Compose

Now it's time to build our **first real containerized application**.

We'll containerize a FastAPI project using production-ready practices.

By the end of this chapter, you'll understand how backend teams package and run FastAPI applications inside Docker.

______________________________________________________________________

# Project Structure

Our project looks like this.

```text id="fastapi001"
library-api/

├── app/

│   ├── __init__.py

│   ├── main.py

│   ├── api/

│   ├── models/

│   ├── services/

│   └── repositories/

│

├── requirements.txt

├── Dockerfile

├── compose.yaml

└── .dockerignore
```

This is similar to the structure we'll use in future projects.

______________________________________________________________________

# FastAPI Application

`app/main.py`

```python id="fastapi002"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():

    return {
        "message": "Hello Docker!"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }
```

The `/health` endpoint will later be used by Docker health checks.

______________________________________________________________________

# Requirements

`requirements.txt`

```text id="fastapi003"
fastapi

uvicorn[standard]
```

______________________________________________________________________

# Choosing the Base Image

For production,

we'll use

```dockerfile id="fastapi004"
FROM python:3.12-slim
```

Why?

- Smaller image
- Faster downloads
- Good compatibility
- Suitable for most Python backend applications

______________________________________________________________________

# Complete Dockerfile

```dockerfile id="fastapi005"
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

Notice

```dockerfile id="fastapi006"
--host 0.0.0.0
```

This is important.

______________________________________________________________________

# Why Not localhost?

Inside a container,

```text id="fastapi007"
localhost
```

means

the container itself.

If Uvicorn listens only on

```text id="fastapi008"
127.0.0.1
```

other machines (including your host through port mapping) can't reach it.

Using

```text id="fastapi009"
0.0.0.0
```

binds the server to all network interfaces inside the container.

______________________________________________________________________

# Build the Image

```bash id="fastapi010"
docker build \
-t library-api .
```

Docker

↓

Reads Dockerfile

↓

Builds Image

↓

Stores Image

______________________________________________________________________

# Run the Container

```bash id="fastapi011"
docker run \
-p 8000:8000 \
library-api
```

Now visit

```text id="fastapi012"
http://localhost:8000
```

You should receive

```json id="fastapi013"
{
    "message": "Hello Docker!"
}
```

______________________________________________________________________

# Running in Detached Mode

```bash id="fastapi014"
docker run \
-d \
-p 8000:8000 \
library-api
```

The container runs in the background.

______________________________________________________________________

# Naming Containers

Instead of

```bash id="fastapi015"
docker run library-api
```

use

```bash id="fastapi016"
docker run \
--name library-api \
library-api
```

Container names make management easier.

______________________________________________________________________

# Environment Variables

Suppose

our application

needs a database.

```python id="fastapi017"
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)
```

Run

```bash id="fastapi018"
docker run \
-e DATABASE_URL=postgresql://postgres/library \
library-api
```

No code changes required.

______________________________________________________________________

# Adding a Health Check

Dockerfile

```dockerfile id="fastapi019"
HEALTHCHECK \
--interval=30s \
CMD curl -f http://localhost:8000/health || exit 1
```

Docker now verifies

that the application

is responding.

> **Note:** If you use `curl` in a slim image, you may need to install it, or you can use another health check approach that's already available in the image.

______________________________________________________________________

# Creating `.dockerignore`

```text id="fastapi020"
.git

.venv

__pycache__

.pytest_cache

*.log

.env
```

This keeps

the image

small

and clean.

______________________________________________________________________

# Docker Compose

Instead of

multiple commands,

create

```yaml id="fastapi021"
services:

  api:

    build: .

    ports:

      - "8000:8000"
```

Run

```bash id="fastapi022"
docker compose up
```

The application starts immediately.

______________________________________________________________________

# Development vs Production

Development

```text id="fastapi023"
Bind Mount

↓

Auto Reload

↓

Frequent Code Changes
```

Production

```text id="fastapi024"
Immutable Image

↓

No Source Mount

↓

Stable Deployment
```

The workflow is different.

______________________________________________________________________

# Auto Reload

During development,

Uvicorn supports

```bash id="fastapi025"
uvicorn app.main:app --reload
```

Inside Docker,

you'll typically pair this with a bind mount so code changes are reflected immediately.

For production,

do **not** use `--reload`.

______________________________________________________________________

# Logging

FastAPI writes logs

to

```text id="fastapi026"
stdout

stderr
```

Docker automatically captures them.

View logs

```bash id="fastapi027"
docker logs library-api
```

Avoid writing application logs to files inside the container unless there's a specific requirement.

______________________________________________________________________

# Inspect the Container

```bash id="fastapi028"
docker inspect library-api
```

Useful information

- Environment variables
- Networks
- Volumes
- Health status
- Port mappings

______________________________________________________________________

# Production Improvements

As projects grow,

consider

- Running the application as a non-root user
- Pinning dependency versions
- Multi-stage builds
- Smaller base images
- Health checks
- Resource limits

We'll implement several of these improvements in later chapters.

______________________________________________________________________

# Typical Request Flow

```text id="fastapi029"
Browser

↓

Host Port 8000

↓

Docker Port Mapping

↓

FastAPI Container

↓

Uvicorn

↓

FastAPI
```

Understanding this flow helps when debugging connectivity issues.

______________________________________________________________________

# Common Mistakes

### Using localhost Inside Docker

Use

```text id="fastapi030"
0.0.0.0
```

for the server,

and service names for inter-container communication.

______________________________________________________________________

### Forgetting Port Mapping

Without

```bash id="fastapi031"
-p
```

the application won't be reachable from the host.

______________________________________________________________________

### Running Production with `--reload`

Reload is for development only.

______________________________________________________________________

### Committing `.env`

Sensitive configuration

shouldn't be committed to Git.

______________________________________________________________________

# Best Practices

- Use `python:3.12-slim`.
- Bind to `0.0.0.0`.
- Add a health endpoint.
- Use `.dockerignore`.
- Read configuration from environment variables.
- Keep images immutable.
- Log to stdout/stderr.
- Separate development and production configurations.

______________________________________________________________________

# Hands-on Exercise

1. Create the FastAPI project.
1. Write the Dockerfile.
1. Build the image.
1. Run the container.
1. Add environment variables.
1. Add a health endpoint.
1. Add a health check.
1. Create a `compose.yaml`.
1. Start the application with Docker Compose.
1. Inspect the running container.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should a FastAPI application inside Docker listen on `0.0.0.0` instead of `127.0.0.1`?

Inside a container, `127.0.0.1` refers only to the loopback interface of that container. If Uvicorn binds only to
`127.0.0.1`, external connections—including requests forwarded through Docker's port mapping—cannot reach the
application. Binding to `0.0.0.0` allows the application to accept connections on all network interfaces within the
container.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Containerizing a FastAPI application
- Production Dockerfile
- Running Uvicorn in Docker
- Port mapping
- Environment variables
- Health endpoints
- Health checks
- Docker Compose integration
- Development vs production
- Logging
- Container inspection
- Production best practices

In the next chapter, we'll containerize **PostgreSQL**, including persistent storage, initialization scripts, users,
passwords, databases, and production-ready configuration.

______________________________________________________________________

## Next File

[Containerizing PostgreSQL](13-containerizing-postgresql.md)
