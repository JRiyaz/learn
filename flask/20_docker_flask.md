# Dockerizing Flask Applications

> **Course:** Flask for Backend Engineers
>
> **Module:** 9
>
> **File:** `20_docker_flask.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Docker is Used
- Containers vs Virtual Machines
- Dockerizing Flask
- Writing a Dockerfile
- Multi-stage Builds
- Docker Compose
- Environment Variables
- Persistent Volumes
- Networking
- Health Checks
- Production Best Practices

______________________________________________________________________

# Why Docker?

Imagine this situation.

Developer A

```
Works Perfectly
```

Developer B

```
Python Version Different

↓

Package Conflict

↓

Application Fails
```

Docker solves this problem by packaging the application with everything it needs.

______________________________________________________________________

# What is a Container?

A container packages

```
Application

+

Python

+

Libraries

+

Dependencies

↓

Single Portable Unit
```

The same container runs consistently across different environments.

______________________________________________________________________

# Containers vs Virtual Machines

| Containers | Virtual Machines |
|------------|------------------|
| Lightweight | Heavy |
| Share Host Kernel | Separate OS |
| Fast Startup | Slower Startup |
| Lower Memory Usage | Higher Memory Usage |
| Ideal for Microservices | Ideal for Full OS Isolation |

______________________________________________________________________

# Docker Architecture

```
Flask App

↓

Docker Image

↓

Docker Container
```

______________________________________________________________________

# Dockerfile

A Dockerfile defines how to build an image.

Example

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

______________________________________________________________________

# Build Image

```bash
docker build -t flask-app .
```

Result

```
Source Code

↓

Docker Image
```

______________________________________________________________________

# Run Container

```bash
docker run -p 5000:5000 flask-app
```

Mapping

```
Host

5000

↓

Container

5000
```

______________________________________________________________________

# Better Production Command

Instead of

```dockerfile
CMD ["python", "app.py"]
```

Use

```dockerfile
CMD [

"gunicorn",

"-w",

"4",

"app:app"

]
```

Production containers should run Gunicorn instead of Flask's development server.

______________________________________________________________________

# Layer Caching

Docker builds images in layers.

Example

```dockerfile
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

Dependencies are cached unless `requirements.txt` changes.

This makes rebuilds significantly faster.

______________________________________________________________________

# .dockerignore

Example

```
__pycache__/

.git/

.env

tests/

*.pyc
```

Exclude unnecessary files from the build context.

______________________________________________________________________

# Environment Variables

Run

```bash
docker run \

-e SECRET_KEY=abc \

-e DATABASE_URL=... \

flask-app
```

Never bake secrets into images.

______________________________________________________________________

# Multi-stage Builds

Without multi-stage

```
Compiler

↓

Final Image
```

Large image.

______________________________________________________________________

With multi-stage

```
Build Stage

↓

Copy Artifacts

↓

Small Runtime Image
```

Cleaner and smaller production images.

______________________________________________________________________

# Example Multi-stage Dockerfile

```dockerfile
FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim

COPY --from=builder /install /usr/local

COPY . .

CMD [

"gunicorn",

"app:app"

]
```

______________________________________________________________________

# Docker Compose

Applications usually need more than Flask.

Example

```
Flask

↓

PostgreSQL

↓

Redis
```

Docker Compose manages multiple containers together.

______________________________________________________________________

# docker-compose.yml

Example

```yaml
services:

  web:

    build: .

  redis:

    image: redis

  postgres:

    image: postgres
```

One command starts the entire stack.

______________________________________________________________________

# Start Services

```bash
docker compose up
```

Detached

```bash
docker compose up -d
```

______________________________________________________________________

# Stop Services

```bash
docker compose down
```

______________________________________________________________________

# Volumes

Without a volume

```
Container Deleted

↓

Database Lost
```

With a volume

```
Container Deleted

↓

Data Preserved
```

Volumes provide persistent storage.

______________________________________________________________________

# Networking

Docker Compose automatically creates a network.

Example

```
Flask

↓

Redis

↓

PostgreSQL
```

Containers communicate using service names.

Example

```
postgres

redis
```

instead of IP addresses.

______________________________________________________________________

# Health Checks

Docker supports health checks.

Example

```dockerfile
HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
```

Orchestrators can restart unhealthy containers.

______________________________________________________________________

# Container Logs

View logs

```bash
docker logs

container_id
```

Applications should write logs to stdout/stderr so Docker and orchestration platforms can collect them.

______________________________________________________________________

# Image Size

Good Practices

- Use slim base images
- Remove temporary files
- Use multi-stage builds
- Install only required packages

Smaller images deploy faster.

______________________________________________________________________

# Production Architecture

```
Load Balancer

↓

Nginx

↓

Gunicorn

↓

Flask Container

↓

Redis

↓

PostgreSQL
```

Each service runs in its own container.

______________________________________________________________________

# Deployment Flow

```
Git Push

↓

Build Docker Image

↓

Run Tests

↓

Push Image

↓

Deploy Containers
```

Container images become deployment artifacts.

______________________________________________________________________

# Common Mistakes

❌ Running Flask development server inside containers

❌ Copying `.env` into images

❌ Building unnecessarily large images

❌ Running containers as the root user

❌ Ignoring health checks

❌ Storing persistent data inside ephemeral containers

______________________________________________________________________

# Production Best Practices

- Use slim base images.
- Use multi-stage builds.
- Run Gunicorn inside containers.
- Store configuration in environment variables.
- Use Docker Compose for local development.
- Persist important data using volumes.
- Add health checks.
- Run containers with a non-root user where practical.
- Keep images small and secure.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are multi-stage Docker builds recommended for production applications?**

### Answer

Multi-stage builds separate the build environment from the runtime environment.

Benefits include:

1. Smaller image sizes.
1. Reduced attack surface.
1. Faster deployments.
1. Fewer unnecessary build tools in production.
1. Cleaner runtime environments.

Only the files required to run the application are copied into the final image, making production images more efficient
and secure.

______________________________________________________________________

# Summary

In this chapter you learned:

- Docker
- Containers
- Dockerfile
- Docker Compose
- Multi-stage Builds
- Environment Variables
- Volumes
- Networking
- Health Checks
- Production Best Practices

Docker provides a consistent deployment environment and is one of the most widely used technologies for packaging and
deploying Flask applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What problem does Docker solve?
1. What is the difference between a Docker image and a Docker container?
1. How do containers differ from virtual machines?

______________________________________________________________________

## Dockerfile

4. What is a Dockerfile?
1. Why should dependencies be copied before application code?
1. Why shouldn't production containers run `python app.py`?

______________________________________________________________________

## Docker Compose

7. Why use Docker Compose?
1. What kinds of services are commonly defined in `docker-compose.yml`?
1. How do containers communicate with one another in Docker Compose?

______________________________________________________________________

## Production

10. Why should environment variables be used for configuration?
01. Why are multi-stage builds recommended?
01. Why are health checks important?
01. Why should logs be written to stdout/stderr?

______________________________________________________________________

## Storage

14. Why are Docker volumes necessary?
01. What happens if a database container is removed without a persistent volume?

______________________________________________________________________

## Scenario-Based

16. Your Docker image is over 2 GB because it contains compilers and build tools that are not needed at runtime. How would you reduce its size?
01. A developer copies the `.env` file into the Docker image and pushes it to a public registry. What security risks does this introduce?
01. Your Flask application cannot connect to PostgreSQL because it is using `localhost` inside the container. Why does this fail, and how should the application connect instead?
01. Your production container exits immediately after startup because it is running the Flask development server. What changes would you make?
01. Your application stores uploaded files inside the container filesystem, and they disappear after every deployment. How would you redesign the storage architecture?

______________________________________________________________________

# Next

[Kubernetes Deployment for Flask](21_kubernetes_flask.md)
