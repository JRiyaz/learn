# Docker - Part 11

# Docker Compose

______________________________________________________________________

# Introduction

So far, we've learned how to run individual containers.

For example,

PostgreSQL

```bash id="compose001"
docker run \

--name postgres \

-p 5432:5432 \

-v postgres-data:/var/lib/postgresql/data \

postgres
```

Redis

```bash id="compose002"
docker run \

--name redis \

-p 6379:6379 \

redis
```

FastAPI

```bash id="compose003"
docker run \

--name api \

-p 8000:8000 \

fastapi-app
```

Now imagine adding Kafka, Zookeeper, Prometheus, Grafana, and Nginx.

Soon you'll be running ten or more `docker run` commands.

Managing them becomes difficult.

Docker Compose solves this problem.

______________________________________________________________________

# What is Docker Compose?

Docker Compose is a tool for defining and running **multi-container applications** using a single configuration file.

Instead of

```text id="compose004"
docker run

docker run

docker run

docker run
```

we define everything in

```text id="compose005"
compose.yaml
```

and start the entire application with one command.

______________________________________________________________________

# Why Docker Compose?

Imagine our backend.

```text id="compose006"
FastAPI

↓

PostgreSQL

↓

Redis

↓

Kafka
```

Every service depends on another service.

Docker Compose manages all of them together.

______________________________________________________________________

# Before Docker Compose

```text id="compose007"
Run PostgreSQL

↓

Run Redis

↓

Run Kafka

↓

Run FastAPI
```

Many manual steps.

______________________________________________________________________

# With Docker Compose

```text id="compose008"
docker compose up
```

Everything starts automatically.

______________________________________________________________________

# Docker Compose Architecture

```text id="compose009"
             compose.yaml

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

  FastAPI      PostgreSQL      Redis

                    │

                    ▼

                  Kafka
```

The compose file becomes the blueprint for your application stack.

______________________________________________________________________

# Compose File

Modern Docker uses

```text id="compose010"
compose.yaml
```

(or `docker-compose.yml` for older setups).

This file describes:

- Services
- Networks
- Volumes
- Environment variables
- Ports
- Build instructions

______________________________________________________________________

# Basic Compose File

```yaml id="compose011"
services:

  api:

    image: fastapi-app
```

This defines

one service

named

```text id="compose012"
api
```

______________________________________________________________________

# Multiple Services

```yaml id="compose013"
services:

  api:

    image: fastapi-app

  postgres:

    image: postgres

  redis:

    image: redis
```

Compose knows

three containers

should be created.

______________________________________________________________________

# Building Instead of Pulling

Instead of

```yaml id="compose014"
image: fastapi-app
```

build the image.

```yaml id="compose015"
services:

  api:

    build: .
```

Compose builds

the Dockerfile

automatically.

______________________________________________________________________

# Port Mapping

Exactly like

`docker run`

```yaml id="compose016"
services:

  api:

    ports:

      - "8000:8000"
```

Meaning

```text id="compose017"
Host

8000

↓

Container

8000
```

______________________________________________________________________

# Environment Variables

```yaml id="compose018"
services:

  api:

    environment:

      APP_ENV: development

      REDIS_HOST: redis

      DATABASE_HOST: postgres
```

The container receives

these variables

at runtime.

______________________________________________________________________

# Volumes

Persist PostgreSQL data.

```yaml id="compose019"
services:

  postgres:

    image: postgres

    volumes:

      - postgres-data:/var/lib/postgresql/data
```

Volume declaration

```yaml id="compose020"
volumes:

  postgres-data:
```

______________________________________________________________________

# Networks

Compose automatically creates a network for the application if you don't define one explicitly.

You can also define your own.

```yaml id="compose021"
networks:

  backend:
```

Attach services.

```yaml id="compose022"
services:

  api:

    networks:

      - backend

  postgres:

    networks:

      - backend
```

Now

they communicate

using service names.

______________________________________________________________________

# Service Names

Inside FastAPI

```python id="compose023"
DATABASE_URL = (

"postgresql://user:password@postgres:5432/library"

)
```

Notice

```text id="compose024"
postgres
```

is

the Compose service name.

Compose automatically provides DNS resolution.

______________________________________________________________________

# Complete Example

```yaml id="compose025"
services:

  api:

    build: .

    ports:

      - "8000:8000"

    environment:

      DATABASE_HOST: postgres

      REDIS_HOST: redis

    depends_on:

      - postgres

      - redis

  postgres:

    image: postgres

    volumes:

      - postgres-data:/var/lib/postgresql/data

  redis:

    image: redis

volumes:

  postgres-data:
```

______________________________________________________________________

# What Does `depends_on` Do?

Example

```yaml id="compose026"
depends_on:

  - postgres

  - redis
```

Compose starts

PostgreSQL

and

Redis

before starting FastAPI.

> **Important:** `depends_on` controls startup order, but it does **not** guarantee that PostgreSQL or Redis are fully ready to accept connections. We'll address this later using health checks and application retry logic.

______________________________________________________________________

# Starting the Stack

```bash id="compose027"
docker compose up
```

Compose

- Builds images (if required)
- Creates the network
- Creates volumes
- Starts containers

______________________________________________________________________

# Detached Mode

```bash id="compose028"
docker compose up -d
```

Containers continue running

in the background.

______________________________________________________________________

# View Running Services

```bash id="compose029"
docker compose ps
```

Example

```text id="compose030"
api

postgres

redis
```

______________________________________________________________________

# View Logs

All services

```bash id="compose031"
docker compose logs
```

Single service

```bash id="compose032"
docker compose logs api
```

Very useful for debugging.

______________________________________________________________________

# Stop the Stack

```bash id="compose033"
docker compose down
```

Compose stops

and removes

the containers.

Named volumes remain unless explicitly removed.

______________________________________________________________________

# Remove Volumes

```bash id="compose034"
docker compose down -v
```

Use with caution.

This also removes named volumes created by the Compose project.

______________________________________________________________________

# Rebuilding

Suppose

application code changes.

```bash id="compose035"
docker compose up --build
```

Compose rebuilds

the image

before starting the containers.

______________________________________________________________________

# Project Structure

```text id="compose036"
project/

├── app.py

├── Dockerfile

├── compose.yaml

├── requirements.txt

└── .dockerignore
```

This is a common layout for small to medium-sized projects.

______________________________________________________________________

# Real Backend Architecture

```text id="compose037"
              Docker Compose

                     │

     ┌───────────────┼───────────────┐

     ▼               ▼               ▼

 FastAPI        PostgreSQL        Redis

                     │

                     ▼

                   Kafka
```

One command

starts everything.

______________________________________________________________________

# Common Mistakes

### Using `localhost`

Inside Compose,

containers communicate

using

service names,

not `localhost`.

______________________________________________________________________

### Assuming `depends_on` Waits for Readiness

It only controls startup order.

Use health checks and retry logic for application readiness.

______________________________________________________________________

### Forgetting Volumes

Without volumes,

database data disappears

when containers are removed.

______________________________________________________________________

### Publishing Every Port

Expose only the ports that need to be accessed from outside the Compose network.

______________________________________________________________________

# Best Practices

- Keep one service per container.
- Use descriptive service names.
- Use named volumes for databases.
- Use service names for communication.
- Keep secrets outside the Compose file when possible.
- Combine health checks with retry logic.
- Use `compose.yaml` as the single source of truth for local development.

______________________________________________________________________

# Hands-on Exercise

1. Create a `compose.yaml`.
1. Add FastAPI.
1. Add PostgreSQL.
1. Add Redis.
1. Configure environment variables.
1. Create a named volume.
1. Start the stack.
1. View logs.
1. Stop the stack.
1. Rebuild after changing the application.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Docker Compose preferred over multiple `docker run` commands for local development?

Docker Compose allows an entire multi-container application to be defined declaratively in a single configuration file.
It manages services, networks, volumes, environment variables, and startup commands together, making applications easier
to start, stop, reproduce, and share across development teams.

______________________________________________________________________

# Summary

In this chapter, you learned:

- What Docker Compose is
- `compose.yaml`
- Services
- Build vs Image
- Port mappings
- Environment variables
- Volumes
- Networks
- Service discovery
- `depends_on`
- `docker compose up`
- `docker compose down`
- Logs
- Rebuilding containers
- Docker Compose best practices

In the next chapter, we'll containerize a **FastAPI application** from start to finish using everything you've learned
so far.

______________________________________________________________________

## Next File

[Containerizing FastAPI](12-containerizing-fastapi.md)
