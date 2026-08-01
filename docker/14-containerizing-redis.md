# Docker - Part 14

# Containerizing Redis

______________________________________________________________________

# Introduction

In the previous chapter, we containerized PostgreSQL.

Now we'll do the same for **Redis**.

Unlike PostgreSQL,

Redis is an **in-memory database**.

That means most data is stored in RAM instead of on disk.

This makes Redis extremely fast,

but it also introduces different considerations for persistence and configuration.

By the end of this chapter, you'll know how to:

- Run Redis in Docker
- Configure Redis
- Enable persistence
- Connect FastAPI to Redis
- Use Redis inside Docker Compose
- Debug common Redis issues

______________________________________________________________________

# Why Containerize Redis?

Without Docker

```text id="redis001"
Install Redis

↓

Configure Redis

↓

Start Redis Server

↓

Connect Application
```

Every developer repeats the setup.

______________________________________________________________________

With Docker

```text id="redis002"
docker compose up
```

Redis is ready immediately.

______________________________________________________________________

# Official Redis Image

Docker Hub provides the official Redis image.

```text id="redis003"
redis
```

You can also pin a version.

```text id="redis004"
redis:8

redis:7
```

Pinning versions makes deployments predictable.

______________________________________________________________________

# Running Redis

```bash id="redis005"
docker run \
--name redis \
-p 6379:6379 \
redis:8
```

Redis is now running.

______________________________________________________________________

# Connecting From FastAPI

Redis connection

```python id="redis006"
from redis import Redis

client = Redis(

    host="redis",

    port=6379,

    decode_responses=True

)
```

Notice

```text id="redis007"
redis
```

is the container or service name.

Not

```text id="redis008"
localhost
```

when both containers run inside Docker.

______________________________________________________________________

# Redis in Docker Compose

```yaml id="redis009"
services:

  redis:

    image: redis:8

    ports:

      - "6379:6379"
```

Simple.

______________________________________________________________________

# Testing Redis

Store a value.

```python id="redis010"
client.set(

    "framework",

    "FastAPI"

)
```

Retrieve it.

```python id="redis011"
client.get(
    "framework"
)
```

Output

```text id="redis012"
FastAPI
```

______________________________________________________________________

# Is Redis Persistent?

By default,

Redis stores data in memory.

If the container is removed,

data may be lost unless persistence is configured.

______________________________________________________________________

# Redis Persistence

Redis supports two major persistence mechanisms.

```text id="redis013"
RDB Snapshots

AOF

Append Only File
```

We'll briefly review them.

______________________________________________________________________

# RDB Snapshots

Redis periodically saves the dataset to disk.

```text id="redis014"
Memory

↓

Snapshot

↓

Disk
```

Advantages

- Small files
- Faster recovery

Disadvantages

- Recent writes may be lost if Redis crashes before the next snapshot.

______________________________________________________________________

# Append Only File (AOF)

Every write operation is appended to a log.

```text id="redis015"
SET

↓

Append Log

↓

Disk
```

Advantages

- Better durability

Disadvantages

- Larger files
- More disk activity

______________________________________________________________________

# Persistence in Docker

Store Redis data

inside a Docker volume.

```bash id="redis016"
docker run \
-v redis-data:/data \
redis:8
```

Redis writes persistence files

to

```text id="redis017"
/data
```

______________________________________________________________________

# Docker Compose Volume

```yaml id="redis018"
services:

  redis:

    image: redis:8

    volumes:

      - redis-data:/data

volumes:

  redis-data:
```

Now

Redis data

survives

container recreation,

provided persistence is enabled.

______________________________________________________________________

# Custom Configuration

Instead of defaults,

create

```text id="redis019"
redis.conf
```

Example

```text id="redis020"
appendonly yes
```

Enable

Append Only File.

______________________________________________________________________

# Mount Configuration

```yaml id="redis021"
services:

  redis:

    image: redis:8

    volumes:

      - ./redis.conf:/usr/local/etc/redis/redis.conf

    command:

      [

        "redis-server",

        "/usr/local/etc/redis/redis.conf"

      ]
```

Redis now starts

using your configuration file.

______________________________________________________________________

# Health Check

Redis provides

```bash id="redis022"
redis-cli ping
```

Expected output

```text id="redis023"
PONG
```

______________________________________________________________________

# Docker Compose Health Check

```yaml id="redis024"
services:

  redis:

    image: redis:8

    healthcheck:

      test:

        [

          "CMD",

          "redis-cli",

          "ping"

        ]

      interval: 10s

      timeout: 5s

      retries: 5
```

______________________________________________________________________

# Connecting Using redis-py

Example

```python id="redis025"
from redis import Redis

client = Redis(

    host="redis",

    port=6379,

    decode_responses=True

)

client.set(
    "user:1",
    "Riyaz"
)

print(
    client.get("user:1")
)
```

No Docker-specific code is required.

______________________________________________________________________

# Redis URL

Instead of separate parameters,

use a URL.

```python id="redis026"
from redis import Redis

client = Redis.from_url(

    "redis://redis:6379/0",

    decode_responses=True

)
```

This is common in production applications.

______________________________________________________________________

# Environment Variables

```python id="redis027"
import os

REDIS_URL = os.getenv(
    "REDIS_URL"
)
```

Compose

```yaml id="redis028"
environment:

  REDIS_URL: redis://redis:6379/0
```

Configuration remains external to the application.

______________________________________________________________________

# Logs

View logs

```bash id="redis029"
docker logs redis
```

Useful for

- Startup
- Persistence
- Configuration errors
- Memory warnings

______________________________________________________________________

# Inspect Container

```bash id="redis030"
docker inspect redis
```

Shows

- Volumes
- Networks
- Ports
- Health status
- Environment variables

______________________________________________________________________

# Real Backend Architecture

```text id="redis031"
              Docker Compose

                     │

      ┌──────────────┼──────────────┐

      ▼              ▼              ▼

   FastAPI      PostgreSQL      Redis
```

FastAPI

communicates with Redis

using

```text id="redis032"
redis:6379
```

______________________________________________________________________

# Common Mistakes

### Using localhost

Inside Docker,

use

```text id="redis033"
redis
```

not

```text id="redis034"
localhost
```

______________________________________________________________________

### Assuming Redis Is Always Persistent

Redis is primarily an in-memory database.

Configure persistence if your use case requires it.

______________________________________________________________________

### Forgetting Volumes

Persistence files

should be stored

in a Docker volume.

______________________________________________________________________

### Not Pinning Redis Version

Use

```text id="redis035"
redis:8
```

instead of relying on `latest`.

______________________________________________________________________

### Ignoring Memory Usage

Redis stores data in RAM.

Monitor memory usage and configure eviction policies when appropriate.

______________________________________________________________________

# Best Practices

- Use the official Redis image.
- Pin image versions.
- Use named volumes when persistence is required.
- Use service names for networking.
- Configure persistence intentionally.
- Add health checks.
- Read configuration from environment variables.

______________________________________________________________________

# Hands-on Exercise

1. Start Redis in Docker.
1. Create a named volume.
1. Enable AOF persistence.
1. Connect using `redis-py`.
1. Add a Docker health check.
1. Integrate Redis into Docker Compose.
1. Verify data persistence after recreating the container.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why does Redis often use Docker volumes even though it is an in-memory database?

Redis stores its active dataset in memory, but when persistence is enabled using RDB snapshots or the Append Only File
(AOF), it writes data to disk. A Docker volume ensures these persistence files survive container recreation, allowing
Redis to recover data after restarts while still benefiting from its in-memory performance.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Running Redis in Docker
- Docker Compose configuration
- Redis persistence
- RDB snapshots
- Append Only File (AOF)
- Docker volumes
- Custom Redis configuration
- Health checks
- `redis-py` integration
- Environment variables
- Redis Docker best practices

In the next chapter, we'll containerize **Kafka**, including KRaft mode, brokers, networking, health checks, and
integrating Kafka with FastAPI.

______________________________________________________________________

## Next File

[Containerizing Kafka](15-containerizing-kafka.md)
