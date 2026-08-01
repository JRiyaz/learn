# Docker - Part 19

# Docker Project - Part 2

# Building the Docker Compose Stack

______________________________________________________________________

# Introduction

In the previous chapter, we designed our project architecture.

Now we'll build the infrastructure that powers the application.

By the end of this chapter, we'll have a Docker Compose stack containing:

- FastAPI
- PostgreSQL
- Redis
- Kafka

All services will be able to communicate with each other.

The application itself will be implemented in the following chapters.

______________________________________________________________________

# Project Structure

```text id="composeproj001"
library-api/

├── app/

├── Dockerfile

├── compose.yaml

├── requirements.txt

├── .dockerignore

└── init/

    └── 01-schema.sql
```

______________________________________________________________________

# Designing the Compose File

Our stack consists of four services.

```text id="composeproj002"
api

↓

postgres

↓

redis

↓

kafka
```

Each service has a single responsibility.

______________________________________________________________________

# Complete Compose File

```yaml id="composeproj003"
services:

  api:

    build: .

    container_name: library-api

    ports:

      - "8000:8000"

    environment:

      DATABASE_URL: postgresql://appuser:secret123@postgres:5432/library

      REDIS_URL: redis://redis:6379/0

      KAFKA_BROKER: kafka:9092

      APP_ENV: development

    depends_on:

      - postgres

      - redis

      - kafka

  postgres:

    image: postgres:17

    container_name: postgres

    environment:

      POSTGRES_USER: appuser

      POSTGRES_PASSWORD: secret123

      POSTGRES_DB: library

    ports:

      - "5432:5432"

    volumes:

      - postgres-data:/var/lib/postgresql/data

      - ./init:/docker-entrypoint-initdb.d

  redis:

    image: redis:8

    container_name: redis

    ports:

      - "6379:6379"

    volumes:

      - redis-data:/data

  kafka:

    image: apache/kafka:latest

    container_name: kafka

    ports:

      - "9092:9092"

    environment:

      KAFKA_NODE_ID: 1

      KAFKA_PROCESS_ROLES: broker,controller

      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093

      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

volumes:

  postgres-data:

  redis-data:
```

This gives us a complete development stack.

______________________________________________________________________

# Service Overview

```text id="composeproj004"
api

↓

Business Logic
```

```text id="composeproj005"
postgres

↓

Persistent Data
```

```text id="composeproj006"
redis

↓

Cache
```

```text id="composeproj007"
kafka

↓

Events
```

______________________________________________________________________

# Environment Variables

The API receives

```text id="composeproj008"
DATABASE_URL

REDIS_URL

KAFKA_BROKER

APP_ENV
```

The application code won't know whether it's running locally,

inside Docker,

or eventually inside Kubernetes.

______________________________________________________________________

# PostgreSQL Initialization

Compose mounts

```text id="composeproj009"
./init
```

to

```text id="composeproj010"
/docker-entrypoint-initdb.d
```

When PostgreSQL starts for the first time,

it automatically executes every SQL file in that directory.

______________________________________________________________________

# Persistent Storage

```text id="composeproj011"
PostgreSQL

↓

postgres-data
```

```text id="composeproj012"
Redis

↓

redis-data
```

Both databases survive container recreation.

______________________________________________________________________

# Networking

Docker Compose automatically creates a network.

```text id="composeproj013"
library-api

↓

postgres

↓

redis

↓

kafka
```

Containers communicate using service names.

______________________________________________________________________

# Service Discovery

FastAPI connects using

```text id="composeproj014"
postgres

redis

kafka
```

Never

```text id="composeproj015"
localhost
```

inside Docker.

______________________________________________________________________

# Starting the Stack

```bash id="composeproj016"
docker compose up
```

Docker Compose will

- Build the API image
- Pull required images
- Create the network
- Create volumes
- Start every container

______________________________________________________________________

# Running in Background

```bash id="composeproj017"
docker compose up -d
```

The terminal becomes available immediately.

______________________________________________________________________

# Verify Running Containers

```bash id="composeproj018"
docker compose ps
```

Example

```text id="composeproj019"
library-api

postgres

redis

kafka
```

All services should be running.

______________________________________________________________________

# Viewing Logs

Entire stack

```bash id="composeproj020"
docker compose logs
```

API only

```bash id="composeproj021"
docker compose logs api
```

Kafka only

```bash id="composeproj022"
docker compose logs kafka
```

______________________________________________________________________

# Stopping the Stack

```bash id="composeproj023"
docker compose down
```

Containers are removed,

but named volumes remain.

______________________________________________________________________

# Removing Everything

```bash id="composeproj024"
docker compose down -v
```

This also removes

```text id="composeproj025"
postgres-data

redis-data
```

All persisted data is deleted.

______________________________________________________________________

# Current Request Flow

At this point,

the infrastructure exists,

but the API doesn't yet contain any endpoints.

```text id="composeproj026"
Browser

↓

FastAPI

↓

(No Business Logic Yet)
```

We'll implement the application next.

______________________________________________________________________

# Common Mistakes

### Expecting `depends_on` to Wait for PostgreSQL

It controls startup order only.

Applications should still retry database connections if PostgreSQL is still initializing.

______________________________________________________________________

### Using `localhost`

Inside Docker,

always use service names.

______________________________________________________________________

### Forgetting Volumes

Without volumes,

database data disappears after container removal.

______________________________________________________________________

### Editing Configuration Inside Containers

Configuration should live in

```text id="composeproj027"
compose.yaml
```

or environment variables,

not inside running containers.

______________________________________________________________________

# Best Practices

- One service per container.
- Keep configuration in Compose.
- Use named volumes.
- Use service names.
- Keep secrets outside source code.
- Rebuild after dependency changes.
- Treat containers as disposable.

______________________________________________________________________

# Hands-on Exercise

1. Create the `compose.yaml` file.
1. Add all four services.
1. Configure environment variables.
1. Add named volumes.
1. Start the stack.
1. Verify all containers are running.
1. Inspect the Docker network.
1. Stop and restart the stack.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should infrastructure such as PostgreSQL, Redis, and Kafka be defined in Docker Compose instead of
being started manually?

Docker Compose provides a declarative definition of the entire application stack. Every developer runs the same services
with the same configuration, networks, and volumes using a single command. This reduces setup errors, improves
reproducibility, and makes development, testing, and CI environments consistent.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Building a complete Compose stack
- Service configuration
- Environment variables
- Named volumes
- Automatic networking
- Service discovery
- Startup workflow
- Logs
- Container lifecycle
- Compose best practices

In the next chapter, we'll start implementing the **FastAPI application**, beginning with the project structure,
SQLModel configuration, database connection, and session management.

______________________________________________________________________

## Next File

[Docker Project - Part 3](20-docker-project-part-3.md)
