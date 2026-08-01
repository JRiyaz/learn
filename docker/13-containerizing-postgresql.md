# Docker - Part 13

# Containerizing PostgreSQL

______________________________________________________________________

# Introduction

In the previous chapter, we containerized our FastAPI application.

Now let's containerize the database.

Running PostgreSQL in Docker is extremely common during development, testing, CI/CD pipelines, and many production
deployments.

By the end of this chapter, you'll know how to:

- Run PostgreSQL in Docker
- Persist database data
- Configure users and passwords
- Initialize databases automatically
- Connect FastAPI to PostgreSQL
- Debug common PostgreSQL container issues

______________________________________________________________________

# Why Containerize PostgreSQL?

Without Docker

```text id="postgres001"
Install PostgreSQL

↓

Configure User

↓

Create Database

↓

Configure Port

↓

Start Service
```

Every developer performs these steps manually.

______________________________________________________________________

With Docker

```text id="postgres002"
docker compose up
```

PostgreSQL starts

automatically

with the correct configuration.

______________________________________________________________________

# Official PostgreSQL Image

Docker Hub provides

the official PostgreSQL image.

```text id="postgres003"
postgres
```

This image supports

- Multiple PostgreSQL versions
- Environment variables
- Initialization scripts
- Persistent volumes

______________________________________________________________________

# Running PostgreSQL

```bash id="postgres004"
docker run \
--name postgres \
-e POSTGRES_USER=appuser \
-e POSTGRES_PASSWORD=secret123 \
-e POSTGRES_DB=library \
-p 5432:5432 \
postgres:17
```

This starts PostgreSQL version 17.

______________________________________________________________________

# Understanding the Command

```bash id="postgres005"
--name postgres
```

Container name.

______________________________________________________________________

```bash id="postgres006"
POSTGRES_USER
```

Creates the database user.

______________________________________________________________________

```bash id="postgres007"
POSTGRES_PASSWORD
```

Sets the password.

______________________________________________________________________

```bash id="postgres008"
POSTGRES_DB
```

Creates the initial database.

______________________________________________________________________

```bash id="postgres009"
-p 5432:5432
```

Maps the host port

to the PostgreSQL container.

______________________________________________________________________

# Connecting From FastAPI

Connection string

```python id="postgres010"
DATABASE_URL = (
    "postgresql://"
    "appuser:"
    "secret123@"
    "postgres:"
    "5432/"
    "library"
)
```

Notice

```text id="postgres011"
postgres
```

is the Docker service or container name,

not

```text id="postgres012"
localhost
```

when both applications run inside Docker.

______________________________________________________________________

# Persistent Storage

Without a volume

```text id="postgres013"
Container Removed

↓

Database Lost
```

______________________________________________________________________

With a volume

```text id="postgres014"
Container Removed

↓

Volume

↓

Database Preserved
```

Always use a named volume for PostgreSQL.

______________________________________________________________________

# Docker Volume

```bash id="postgres015"
docker run \
-v postgres-data:/var/lib/postgresql/data \
postgres:17
```

The directory

```text id="postgres016"
/var/lib/postgresql/data
```

contains PostgreSQL's database files.

______________________________________________________________________

# Docker Compose

Instead of

a long command,

use

```yaml id="postgres017"
services:

  postgres:

    image: postgres:17

    environment:

      POSTGRES_USER: appuser

      POSTGRES_PASSWORD: secret123

      POSTGRES_DB: library

    ports:

      - "5432:5432"

    volumes:

      - postgres-data:/var/lib/postgresql/data

volumes:

  postgres-data:
```

One command

starts PostgreSQL.

______________________________________________________________________

# Initialization Scripts

Suppose

you want to

- Create tables
- Insert sample data
- Create extensions

automatically.

The official PostgreSQL image supports initialization scripts.

______________________________________________________________________

# Project Structure

```text id="postgres018"
project/

├── compose.yaml

└── init/

    ├── 01-schema.sql

    └── 02-seed.sql
```

______________________________________________________________________

# Mount Initialization Folder

```yaml id="postgres019"
services:

  postgres:

    image: postgres:17

    volumes:

      - postgres-data:/var/lib/postgresql/data

      - ./init:/docker-entrypoint-initdb.d
```

______________________________________________________________________

# How Initialization Works

When PostgreSQL starts

for the **first time** on a new data directory,

it automatically executes

```text id="postgres020"
/docker-entrypoint-initdb.d
```

Files are processed in alphabetical order.

______________________________________________________________________

# Example Schema

`01-schema.sql`

```sql id="postgres021"
CREATE TABLE books (

    id SERIAL PRIMARY KEY,

    title TEXT NOT NULL,

    author TEXT NOT NULL
);
```

______________________________________________________________________

# Seed Data

`02-seed.sql`

```sql id="postgres022"
INSERT INTO books (

    title,

    author

)

VALUES

(

'Clean Code',

'Robert C. Martin'

);
```

The first time the database initializes,

the table and sample data are created automatically.

______________________________________________________________________

# Important Note

Initialization scripts run **only when PostgreSQL initializes a new data directory**.

If the volume already contains database files,

the scripts are **not** executed again.

This surprises many beginners.

______________________________________________________________________

# Connecting From SQLAlchemy

```python id="postgres023"
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL
)
```

No Docker-specific code is required.

SQLAlchemy simply connects using the configured host.

______________________________________________________________________

# Health Check

A common health check

uses

```dockerfile id="postgres024"
HEALTHCHECK \
CMD pg_isready \
-U appuser
```

`pg_isready`

checks whether PostgreSQL is accepting connections.

______________________________________________________________________

# Docker Compose Health Check

```yaml id="postgres025"
services:

  postgres:

    image: postgres:17

    healthcheck:

      test:

        [

          "CMD-SHELL",

          "pg_isready -U appuser"

        ]

      interval: 10s

      timeout: 5s

      retries: 5
```

This marks the container healthy

once PostgreSQL is ready.

______________________________________________________________________

# Logs

View logs

```bash id="postgres026"
docker logs postgres
```

Useful messages include

- Server started
- Initialization complete
- Connection errors
- Authentication failures

______________________________________________________________________

# Inspecting the Container

```bash id="postgres027"
docker inspect postgres
```

Shows

- Volumes
- Ports
- Networks
- Environment variables
- Health status

______________________________________________________________________

# Connecting With psql

If the PostgreSQL client is available,

connect using

```bash id="postgres028"
psql \
-h localhost \
-U appuser \
-d library
```

Or connect from inside the container.

```bash id="postgres029"
docker exec -it postgres \
psql \
-U appuser \
-d library
```

Both approaches are useful during development.

______________________________________________________________________

# Real Backend Architecture

```text id="postgres030"
               Docker Compose

                      │

      ┌───────────────┴───────────────┐

      ▼                               ▼

   FastAPI                     PostgreSQL

                                      │

                                      ▼

                               Docker Volume
```

Database files remain

outside

the container lifecycle.

______________________________________________________________________

# Common Mistakes

### No Volume

Removing the container

removes the database.

______________________________________________________________________

### Using localhost

Inside Docker,

FastAPI should connect using

```text id="postgres031"
postgres
```

instead of `localhost`.

______________________________________________________________________

### Weak Passwords

Use strong passwords,

especially outside local development.

______________________________________________________________________

### Expecting Init Scripts to Run Every Time

They execute only during the first initialization of a new data directory.

______________________________________________________________________

### Committing Sensitive Configuration

Avoid committing production passwords into version control.

Use environment variables or secret management.

______________________________________________________________________

# Best Practices

- Use the official PostgreSQL image.
- Pin a PostgreSQL version instead of relying on `latest`.
- Always use named volumes.
- Use initialization scripts for development.
- Add health checks.
- Use service names for networking.
- Keep credentials outside source code.

______________________________________________________________________

# Hands-on Exercise

1. Create a PostgreSQL container.
1. Configure a database, user, and password.
1. Add a named volume.
1. Create an initialization script.
1. Insert sample data automatically.
1. Connect using SQLAlchemy.
1. Add a health check.
1. Verify data persists after recreating the container.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do PostgreSQL initialization scripts sometimes appear to "stop working" after the first run?

The official PostgreSQL Docker image executes initialization scripts only when it initializes a new, empty data
directory. If a persistent volume already contains an initialized database, PostgreSQL skips the initialization phase
and does not rerun the scripts. To execute them again, you must use a fresh data directory or apply changes manually
through migrations or SQL commands.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Running PostgreSQL in Docker
- Environment variables
- Named volumes
- Docker Compose configuration
- Initialization scripts
- SQLAlchemy connectivity
- Health checks
- Logs
- Container inspection
- PostgreSQL Docker best practices

In the next chapter, we'll containerize **Redis**, including persistence options, configuration, networking, health
checks, and integration with FastAPI.

______________________________________________________________________

## Next File

[Containerizing Redis](14-containerizing-redis.md)
