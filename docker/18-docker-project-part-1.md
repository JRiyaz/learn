# Docker - Part 18

# Docker Project - Part 1

# Library Management API

______________________________________________________________________

# Project Overview

Throughout this Docker module, we've learned how to containerize individual services.

Now we'll combine everything into one application.

Our project is a simple **Library Management API**.

The application allows users to:

- Add books
- Borrow books
- Return books
- Cache frequently requested books using Redis
- Publish events to Kafka
- Store data in PostgreSQL

Everything runs inside Docker.

______________________________________________________________________

# Why This Project?

This project demonstrates almost everything we've learned.

It includes

- FastAPI
- PostgreSQL
- Redis
- Kafka
- Docker Compose
- Docker Networking
- Docker Volumes
- Environment Variables
- Health Checks

without introducing microservices yet.

______________________________________________________________________

# Final Architecture

```text id="project001"
                    Browser

                       │

                       ▼

                  FastAPI API

        ┌──────────┼──────────┐

        ▼          ▼          ▼

 PostgreSQL     Redis      Kafka
```

Everything runs

inside Docker.

______________________________________________________________________

# Project Structure

```text id="project002"
library-api/

├── app/

│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── cache.py
│   ├── kafka.py
│   └── routes.py

├── requirements.txt

├── Dockerfile

├── compose.yaml

├── .dockerignore

└── init/

    └── 01-schema.sql
```

Notice

everything still lives

inside one application.

______________________________________________________________________

# Tech Stack

| Component | Technology |
| ------------- | -------------- |
| API | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Messaging | Kafka |
| ORM | SQLModel |
| Containers | Docker |
| Orchestration | Docker Compose |

______________________________________________________________________

# Features

The API will expose

```text id="project003"
POST   /books

GET    /books

GET    /books/{id}

PUT    /books/{id}

DELETE /books/{id}

POST   /books/{id}/borrow

POST   /books/{id}/return

GET    /health
```

______________________________________________________________________

# Request Flow

```text id="project004"
Client

↓

FastAPI

↓

Repository

↓

SQLModel

↓

PostgreSQL
```

If data exists

inside Redis,

the database isn't queried.

______________________________________________________________________

# Cache Flow

```text id="project005"
Request

↓

Redis

│

├── Hit

│      ↓

│   Return Book

│

└── Miss

       ↓

 PostgreSQL

       ↓

 Save to Redis

       ↓

 Return Book
```

______________________________________________________________________

# Kafka Flow

Every important action

creates an event.

```text id="project006"
Book Created

↓

Kafka

↓

Topic

↓

Consumer
```

Later,

after learning Microservices,

other services will consume these events.

For now,

we'll simply publish them.

______________________________________________________________________

# Docker Compose Architecture

```text id="project007"
                Docker Compose

                       │

     ┌─────────────────┼─────────────────┐

     ▼                 ▼                 ▼

  FastAPI         PostgreSQL         Redis

                       │

                       ▼

                     Kafka
```

One command starts everything.

______________________________________________________________________

# Environment Variables

FastAPI

will receive

```text id="project008"
DATABASE_URL

REDIS_URL

KAFKA_BROKER

APP_ENV
```

No hardcoded configuration.

______________________________________________________________________

# Database Model

Book

```text id="project009"
id

title

author

available
```

Simple,

but realistic.

______________________________________________________________________

# SQLModel

```python id="project010"
from sqlmodel import SQLModel, Field


class Book(

    SQLModel,

    table=True

):

    id: int | None = Field(

        default=None,

        primary_key=True

    )

    title: str

    author: str

    available: bool = True
```

______________________________________________________________________

# FastAPI Endpoints

```text id="project011"
Create Book

↓

Save Database

↓

Publish Kafka Event

↓

Return Response
```

______________________________________________________________________

Retrieve Book

```text id="project012"
Check Redis

│

├── Cache Hit

│

└── Cache Miss

      ↓

PostgreSQL

↓

Update Cache

↓

Return Response
```

______________________________________________________________________

# Docker Services

Compose will contain

```text id="project013"
api

postgres

redis

kafka
```

Each service

has

its own container.

______________________________________________________________________

# Volumes

Persistent storage

```text id="project014"
postgres-data

redis-data

kafka-data
```

FastAPI

doesn't need

persistent storage.

______________________________________________________________________

# Networks

Compose creates

one private network.

```text id="project015"
api

↓

postgres

↓

redis

↓

kafka
```

Services communicate

using

their service names.

______________________________________________________________________

# Development Workflow

```text id="project016"
Write Code

↓

docker compose up --build

↓

Test API

↓

Modify Code

↓

Rebuild

↓

Test Again
```

Exactly how many backend teams work during development.

______________________________________________________________________

# What We'll Build

Over the next chapters

we'll implement

- Dockerfile
- Compose File
- PostgreSQL
- Redis
- Kafka
- FastAPI
- CRUD Operations
- Health Checks
- End-to-End Testing

step by step.

______________________________________________________________________

# Hands-on Exercise

Before the next chapter,

create the following project structure.

```text id="project017"
library-api/

├── app/

├── Dockerfile

├── compose.yaml

├── requirements.txt

└── .dockerignore
```

Don't write any code yet.

We'll implement each file together.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Docker Compose useful even for a relatively small application like this?

Docker Compose allows all application dependencies to be defined in a single configuration file. Instead of manually
starting FastAPI, PostgreSQL, Redis, and Kafka with separate commands, the entire stack can be built and started
consistently with a single command. This makes local development, onboarding, testing, and CI/CD workflows much simpler
and more reliable.

______________________________________________________________________

# Summary

In this chapter, you learned:

- The project architecture
- The technologies involved
- The request flow
- The cache flow
- The event flow
- The Docker Compose architecture
- The project structure
- The development workflow

In the next chapter, we'll build the complete **Docker Compose configuration** that wires together FastAPI, PostgreSQL,
Redis, and Kafka into a working application.

______________________________________________________________________

## Next File

[Docker Project - Part 2](19-docker-project-part-2.md)
