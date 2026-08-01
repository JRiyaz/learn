# Docker - Part 9

# Resource Limits & Health Checks

______________________________________________________________________

# Introduction

So far, we've learned how to:

- Build Docker images
- Persist data with volumes
- Connect containers using networks
- Configure applications using environment variables

Now let's answer an important production question.

Suppose one container starts consuming

```text id="docker901"
100%

CPU
```

or

```text id="docker902"
32 GB

RAM
```

What happens?

Without limits,

that single container can affect other applications running on the same machine.

Docker allows us to control resource usage and monitor application health.

______________________________________________________________________

# Why Resource Limits?

Imagine a server running

```text id="docker903"
FastAPI

PostgreSQL

Redis

Kafka
```

Suppose FastAPI has a bug.

```python id="docker904"
while True:
    pass
```

CPU usage

↓

100%

Now

every other container

becomes slower.

______________________________________________________________________

# Resource Isolation

Docker allows each container to have its own limits.

```text id="docker905"
Server

│

├── FastAPI

│     CPU 1

│     RAM 512 MB

│

├── PostgreSQL

│     CPU 2

│     RAM 2 GB

│

├── Redis

│     CPU 1

│     RAM 512 MB

│

└── Kafka

      CPU 2

      RAM 2 GB
```

Each service gets predictable resources.

______________________________________________________________________

# CPU Limits

Limit CPU usage.

Example

```bash id="docker906"
docker run \

--cpus=2 \

fastapi-app
```

Meaning

```text id="docker907"
Maximum

2 CPU Cores
```

The container can use up to the equivalent of two CPU cores.

______________________________________________________________________

# Why CPU Limits?

Suppose

one application enters

an infinite loop.

Without limits

```text id="docker908"
Entire Server

↓

Slow
```

With limits

```text id="docker909"
Only One Container

↓

Limited
```

Other containers continue running more predictably.

______________________________________________________________________

# Memory Limits

Example

```bash id="docker910"
docker run \

--memory=512m \

fastapi-app
```

Maximum memory

```text id="docker911"
512 MB
```

______________________________________________________________________

# What Happens If Memory Is Exceeded?

If a container exceeds its memory limit,

the Linux kernel may terminate it (commonly referred to as an OOM kill).

This protects the host from one container exhausting all available memory.

______________________________________________________________________

# Combining Limits

```bash id="docker912"
docker run \

--cpus=2 \

--memory=1g \

fastapi-app
```

Now

both CPU

and memory

are controlled.

______________________________________________________________________

# Why Not Give Unlimited Resources?

Imagine

10 containers.

Each uses

```text id="docker913"
Unlimited RAM
```

Eventually

the host runs out of memory.

Limits help prevent resource contention.

______________________________________________________________________

# Monitoring Containers

Docker provides

```bash id="docker914"
docker stats
```

Example

```text id="docker915"
NAME

CPU

MEMORY

api

5%

120 MB

postgres

12%

850 MB

redis

1%

20 MB
```

Useful for identifying resource-hungry containers.

______________________________________________________________________

# Health Checks

A running container

isn't always

a healthy application.

Example

```text id="docker916"
Container

Running

↓

Application

Crashed
```

Docker only knows

the process is alive.

Health checks determine whether the application is actually functioning.

______________________________________________________________________

# Example

Suppose

FastAPI

starts successfully.

Later,

database connection fails.

The process

continues running,

but every request returns

```text id="docker917"
500 Internal Server Error
```

Docker needs a way

to detect this.

______________________________________________________________________

# HEALTHCHECK

Dockerfile

```dockerfile id="docker918"
HEALTHCHECK \

CMD curl -f http://localhost:8000/health || exit 1
```

Docker periodically executes the command.

Success

↓

Healthy

Failure

↓

Unhealthy

______________________________________________________________________

# Health Endpoint

FastAPI

```python id="docker919"
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():

    return {

        "status": "healthy"

    }
```

Docker calls this endpoint.

______________________________________________________________________

# Health Check Flow

```text id="docker920"
Docker

↓

GET /health

↓

200 OK

↓

Healthy
```

If the check repeatedly fails,

the container is marked unhealthy.

______________________________________________________________________

# Viewing Health Status

```bash id="docker921"
docker ps
```

Example

```text id="docker922"
STATUS

Up 10 minutes

(healthy)
```

or

```text id="docker923"
STATUS

Up 10 minutes

(unhealthy)
```

______________________________________________________________________

# Health Check Options

Docker supports

```dockerfile id="docker924"
HEALTHCHECK \

--interval=30s \

--timeout=5s \

--retries=3 \

CMD curl -f http://localhost:8000/health || exit 1
```

Meaning

- Check every 30 seconds
- Wait up to 5 seconds
- Mark unhealthy after 3 consecutive failures

______________________________________________________________________

# Restart Policies

Suppose

application crashes.

Instead of manually restarting,

Docker can restart it automatically.

Example

```bash id="docker925"
docker run \

--restart=always \

fastapi-app
```

______________________________________________________________________

# Restart Policy Types

```text id="docker926"
no

on-failure

unless-stopped

always
```

______________________________________________________________________

## no

Default behavior.

Container isn't restarted automatically.

______________________________________________________________________

## on-failure

Restart only

if the application exits with an error.

______________________________________________________________________

## unless-stopped

Restart automatically,

except when you intentionally stop it.

______________________________________________________________________

## always

Restart whenever the container stops, including after a Docker daemon restart.

______________________________________________________________________

# Real Backend Example

```text id="docker927"
FastAPI

↓

Health Check

↓

Healthy?

↓

Yes

↓

Continue

No

↓

Restart
```

Health checks and restart policies complement each other, although Docker itself doesn't automatically restart a
container solely because it is marked unhealthy. In practice, orchestration platforms or external automation often react
to health status.

______________________________________________________________________

# Resource Reservations

In orchestration platforms like Kubernetes,

you'll also define

```text id="docker928"
Requested CPU

Requested Memory
```

These help the scheduler place workloads appropriately.

We'll revisit this later.

______________________________________________________________________

# Logs

Health issues

often appear in logs.

View logs

```bash id="docker929"
docker logs container_name
```

Always inspect logs

before restarting containers.

______________________________________________________________________

# Inspect Container

```bash id="docker930"
docker inspect container_name
```

Useful information

- Health status
- Environment variables
- Mounts
- Networking
- Resource limits

______________________________________________________________________

# Common Mistakes

### No Memory Limits

One container can consume excessive memory.

______________________________________________________________________

### No Health Checks

A running process doesn't guarantee a healthy application.

______________________________________________________________________

### Restarting Without Debugging

Check logs first.

Understand the failure before restarting repeatedly.

______________________________________________________________________

### Overly Aggressive Limits

Setting limits too low can cause unnecessary failures.

Measure before tuning.

______________________________________________________________________

# Best Practices

- Set CPU limits.
- Set memory limits.
- Add health checks.
- Use restart policies appropriately.
- Monitor resource usage.
- Inspect logs before troubleshooting.
- Size limits based on real workloads.

______________________________________________________________________

# Hands-on Exercise

1. Run a FastAPI container with CPU and memory limits.
1. View resource usage using `docker stats`.
1. Add a `/health` endpoint.
1. Configure a Docker `HEALTHCHECK`.
1. Run the container with a restart policy.
1. Inspect the container and verify its health status.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should Docker containers have resource limits and health checks?

Resource limits prevent one container from consuming excessive CPU or memory and affecting other workloads on the same
host. Health checks verify that the application is functioning correctly rather than merely running. Together, these
features improve stability, reliability, and operational visibility in production environments.

______________________________________________________________________

# Summary

In this chapter, you learned:

- CPU limits
- Memory limits
- Resource isolation
- `docker stats`
- Health checks
- `HEALTHCHECK`
- Restart policies
- Health endpoints
- Logging
- Container inspection
- Production best practices

In the next chapter, we'll learn **Multi-Stage Builds**, one of the most important techniques for creating smaller,
faster, and more secure production Docker images.

______________________________________________________________________

## Next File

[Multi-Stage Builds](10-multi-stage-builds.md)
