# Docker - Part 20

# Docker Project - Part 3

# Building the FastAPI Application

______________________________________________________________________

# Introduction

In the previous chapter,

we built the Docker infrastructure.

Now,

it's finally time to build our application.

In this chapter, we'll implement:

- FastAPI
- SQLModel
- Database connection
- Session management
- Health endpoint

At the end of this chapter,

our API will successfully connect to PostgreSQL running inside Docker.

______________________________________________________________________

# Project Structure

```text id="project301"
library-api/

├── app/

│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── crud.py

├── Dockerfile

├── compose.yaml

└── requirements.txt
```

______________________________________________________________________

# Required Packages

```text id="project302"
fastapi

uvicorn[standard]

sqlmodel

psycopg[binary]
```

Notice

we're using

```text id="project303"
psycopg
```

(PostgreSQL Driver Version 3)

which is the modern PostgreSQL driver recommended for new SQLAlchemy projects.

______________________________________________________________________

# Environment Variables

The application reads

```text id="project304"
DATABASE_URL

REDIS_URL

KAFKA_BROKER
```

from Docker Compose.

______________________________________________________________________

# Database Configuration

Create

```text id="project305"
database.py
```

______________________________________________________________________

# Reading Configuration

```python id="project306"
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)
```

No hardcoded values.

______________________________________________________________________

# Creating the Engine

```python id="project307"
from sqlmodel import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
```

Notice

```text id="project308"
pool_pre_ping=True
```

It checks database connections before using them,

helping avoid stale connections.

______________________________________________________________________

# Session Factory

Modern SQLModel

uses

```python id="project309"
from sqlmodel import Session


def get_session():

    with Session(engine) as session:

        yield session
```

Exactly the same pattern

we learned

during the SQLModel course.

______________________________________________________________________

# Dependency Injection

FastAPI

makes sessions available

through dependencies.

```python id="project310"
from typing import Annotated

from fastapi import Depends

from sqlmodel import Session


SessionDep = Annotated[
    Session,
    Depends(get_session)
]
```

Every request

gets its own database session.

______________________________________________________________________

# Database Model

Create

```text id="project311"
models.py
```

______________________________________________________________________

```python id="project312"
from sqlmodel import SQLModel
from sqlmodel import Field


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

A simple,

realistic model.

______________________________________________________________________

# API Schemas

Instead of exposing

database models directly,

define request and response schemas.

```python id="project313"
from sqlmodel import SQLModel


class BookCreate(SQLModel):

    title: str

    author: str


class BookRead(SQLModel):

    id: int

    title: str

    author: str

    available: bool
```

Separating database models

from API contracts

becomes increasingly valuable

as applications grow.

______________________________________________________________________

# Creating Tables

During startup,

create database tables.

```python id="project314"
from sqlmodel import SQLModel

from .database import engine


def create_db():

    SQLModel.metadata.create_all(
        engine
    )
```

> **Note:** In production, database schema changes are typically managed with migration tools such as Alembic rather than calling `create_all()`. We're using it here to keep the project simple.

______________________________________________________________________

# FastAPI Application

Create

```text id="project315"
main.py
```

______________________________________________________________________

```python id="project316"
from fastapi import FastAPI

app = FastAPI(
    title="Library API"
)
```

______________________________________________________________________

# Startup Event

Initialize the database.

```python id="project317"
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db()

    yield


app = FastAPI(
    lifespan=lifespan
)
```

FastAPI now uses the modern **lifespan** API instead of the older startup event.

______________________________________________________________________

# Health Endpoint

```python id="project318"
@app.get("/health")
async def health():

    return {

        "status": "healthy"

    }
```

Docker

will later

use this endpoint

for health checks.

______________________________________________________________________

# Root Endpoint

```python id="project319"
@app.get("/")
async def home():

    return {

        "message":

        "Library API"

    }
```

Simple,

but useful.

______________________________________________________________________

# Running the Application

Docker Compose

starts

FastAPI.

```text id="project320"
Browser

↓

localhost:8000

↓

FastAPI
```

Visit

```text id="project321"
http://localhost:8000
```

Expected response

```json id="project322"
{
    "message": "Library API"
}
```

______________________________________________________________________

# Testing Database Connectivity

Temporarily

add

a simple endpoint.

```python id="project323"
from sqlmodel import select


@app.get("/db-test")
async def test_db(
    session: SessionDep
):

    session.exec(
        select(Book)
    )

    return {

        "status":

        "database connected"

    }
```

If this endpoint succeeds,

FastAPI

is successfully communicating

with PostgreSQL.

______________________________________________________________________

# Request Lifecycle

```text id="project324"
HTTP Request

↓

FastAPI

↓

Dependency

↓

Session

↓

PostgreSQL

↓

Response
```

A new session

is created

for every request.

______________________________________________________________________

# Common Mistakes

### Using localhost

Inside Docker,

the database host

is

```text id="project325"
postgres
```

not

```text id="project326"
localhost
```

______________________________________________________________________

### Sharing Sessions

Never create

one global session.

Use

one session

per request.

______________________________________________________________________

### Forgetting Dependency Injection

Always obtain sessions

through

FastAPI dependencies.

______________________________________________________________________

### Calling create_all() in Production

Use

database migrations

for production deployments.

______________________________________________________________________

# Best Practices

- Use SQLModel models.
- Use one session per request.
- Read configuration from environment variables.
- Use `pool_pre_ping=True`.
- Separate API schemas from database models.
- Keep the application stateless.
- Use the FastAPI lifespan API for startup logic.

______________________________________________________________________

# Hands-on Exercise

1. Create `database.py`.
1. Configure the SQLModel engine.
1. Create the session dependency.
1. Create the `Book` model.
1. Create request and response schemas.
1. Initialize the database.
1. Implement `/`.
1. Implement `/health`.
1. Verify database connectivity.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should a FastAPI application create a new SQLAlchemy/SQLModel session for each request instead of
sharing one global session?

Database sessions are not intended to be shared across concurrent requests. Creating one session per request provides
proper transaction boundaries, avoids concurrency issues, ensures connections are returned to the connection pool
promptly, and makes error handling and rollbacks much more reliable.

______________________________________________________________________

# Summary

In this chapter, you learned:

- FastAPI project setup
- SQLModel configuration
- Database engine creation
- Session dependency injection
- SQLModel models
- API schemas
- Modern FastAPI lifespan
- Database initialization
- Health endpoint
- Database connectivity testing

In the next chapter, we'll implement the complete **CRUD layer**, including creating, reading, updating, deleting,
borrowing, and returning books using SQLModel.

______________________________________________________________________

## Next File

[Docker Project - Part 4](21-docker-project-part-4.md)
