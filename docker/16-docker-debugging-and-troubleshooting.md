# Docker - Part 16

# Docker Debugging & Troubleshooting

______________________________________________________________________

# Introduction

Building containers is only half the job.

The other half is debugging them.

Every backend engineer eventually encounters errors like:

```text id="debug001"
Container Exited

Connection Refused

Image Build Failed

Health Check Failed

Port Already In Use

Database Connection Error
```

Knowing how to debug these problems is a valuable skill.

This chapter focuses on systematic troubleshooting rather than guessing.

______________________________________________________________________

# A Debugging Mindset

When something fails,

don't immediately rebuild everything.

Instead, ask:

```text id="debug002"
Is the container running?

↓

Can I access its logs?

↓

Can containers communicate?

↓

Is the application healthy?

↓

Are environment variables correct?

↓

Are volumes mounted?

↓

Are ports exposed?
```

Following a checklist is much faster than random experimentation.

______________________________________________________________________

# Step 1 — Is the Container Running?

The first command should usually be

```bash id="debug003"
docker ps
```

Example

```text id="debug004"
CONTAINER ID

NAME

STATUS

api

Up 10 minutes

postgres

Exited
```

If the container isn't running,

investigate why before looking elsewhere.

______________________________________________________________________

# Show All Containers

```bash id="debug005"
docker ps -a
```

Now you'll also see

- Exited containers
- Created containers
- Stopped containers

______________________________________________________________________

# Step 2 — Check Logs

The most useful command.

```bash id="debug006"
docker logs api
```

Example

```text id="debug007"
ModuleNotFoundError

No module named fastapi
```

The problem becomes obvious.

______________________________________________________________________

# Follow Logs

Watch logs continuously.

```bash id="debug008"
docker logs -f api
```

Useful while sending requests.

______________________________________________________________________

# Docker Compose Logs

Entire application

```bash id="debug009"
docker compose logs
```

Single service

```bash id="debug010"
docker compose logs postgres
```

______________________________________________________________________

# Step 3 — Enter the Container

Sometimes

you need to inspect

the running environment.

```bash id="debug011"
docker exec -it api bash
```

If `bash` isn't installed,

use

```bash id="debug012"
docker exec -it api sh
```

Once inside,

you can inspect files,

processes,

and configuration.

______________________________________________________________________

# Verify Files

Example

```bash id="debug013"
ls

pwd
```

Check

whether your application files

exist where you expect them.

______________________________________________________________________

# Verify Environment Variables

Inside the container

```bash id="debug014"
printenv
```

or

```bash id="debug015"
env
```

Look for

```text id="debug016"
DATABASE_URL

REDIS_URL

APP_ENV
```

Many configuration problems are caused by incorrect environment variables.

______________________________________________________________________

# Step 4 — Inspect the Container

```bash id="debug017"
docker inspect api
```

Useful information

- Network
- Volumes
- Environment variables
- Health status
- Restart policy
- Port mappings

______________________________________________________________________

# Step 5 — Check Resource Usage

```bash id="debug018"
docker stats
```

Example

```text id="debug019"
api

CPU 98%

Memory 450 MB
```

Unexpected resource usage may explain poor performance.

______________________________________________________________________

# Step 6 — Verify Networking

Suppose

FastAPI can't connect

to PostgreSQL.

Check

```bash id="debug020"
docker network ls
```

Then

```bash id="debug021"
docker network inspect backend-network
```

Verify

both containers

are attached

to the same network.

______________________________________________________________________

# Common Networking Mistake

FastAPI

```python id="debug022"
DATABASE_URL = (

"postgresql://localhost/library"

)
```

Wrong.

Inside Docker,

use

```python id="debug023"
DATABASE_URL = (

"postgresql://postgres/library"

)
```

Service names,

not localhost.

______________________________________________________________________

# Test Connectivity

Enter the FastAPI container.

```bash id="debug024"
docker exec -it api sh
```

If tools are available,

test connectivity.

```bash id="debug025"
ping postgres
```

or

```bash id="debug026"
nc -z postgres 5432
```

Some minimal images don't include these utilities, so you may need to install them temporarily or use alternative tools.

______________________________________________________________________

# Step 7 — Verify Volumes

List volumes.

```bash id="debug027"
docker volume ls
```

Inspect

```bash id="debug028"
docker volume inspect postgres-data
```

Verify

the expected volume

is mounted.

______________________________________________________________________

# Step 8 — Check Port Mapping

List running containers.

```bash id="debug029"
docker ps
```

Example

```text id="debug030"
0.0.0.0:8000->8000/tcp
```

No mapping?

The application won't be reachable from the host.

______________________________________________________________________

# Port Already in Use

Example

```text id="debug031"
Bind

address already in use
```

Another application

is already using

that host port.

Solutions

- Stop the conflicting application
- Choose another host port

______________________________________________________________________

# Image Build Failures

Example

```text id="debug032"
COPY failed

File not found
```

Check

- Dockerfile
- Build context
- File paths
- `.dockerignore`

______________________________________________________________________

# Dependency Errors

Example

```text id="debug033"
ModuleNotFoundError
```

Usually means

- Missing dependency
- Incorrect `requirements.txt`
- Image wasn't rebuilt after dependency changes

Rebuild

```bash id="debug034"
docker compose up --build
```

______________________________________________________________________

# Health Check Failures

Example

```text id="debug035"
STATUS

Unhealthy
```

Investigate

- Health endpoint
- Application logs
- Startup timing
- Health check command

______________________________________________________________________

# PostgreSQL Connection Errors

Example

```text id="debug036"
Connection Refused
```

Possible causes

- PostgreSQL still starting
- Wrong hostname
- Wrong credentials
- Wrong port
- Different Docker network

______________________________________________________________________

# Redis Errors

Example

```text id="debug037"
Connection refused
```

Verify

```text id="debug038"
redis:6379
```

and ensure Redis is running.

______________________________________________________________________

# Kafka Errors

Common issue

```text id="debug039"
Broker not available
```

Check

- Advertised listeners
- Service name
- Broker logs
- KRaft configuration

______________________________________________________________________

# Disk Usage

Docker stores

- Images
- Containers
- Volumes
- Networks
- Build cache

View usage

```bash id="debug040"
docker system df
```

______________________________________________________________________

# Cleaning Up

Remove unused resources.

```bash id="debug041"
docker system prune
```

Warning

Unused images,

stopped containers,

and build cache

may be removed.

Read the prompt carefully before confirming.

______________________________________________________________________

# Container Lifecycle Debugging

```text id="debug042"
Created

↓

Running

↓

Exited

↓

Removed
```

Knowing

where a container failed

helps narrow the investigation.

______________________________________________________________________

# Debugging Checklist

```text id="debug043"
✓ Container Running

✓ Logs

✓ Environment Variables

✓ Network

✓ Volume

✓ Ports

✓ Health Check

✓ Resource Usage
```

Use this checklist consistently.

______________________________________________________________________

# Common Mistakes

### Guessing

Use logs and inspection first.

______________________________________________________________________

### Rebuilding Immediately

Determine whether the issue is configuration, networking, or application logic before rebuilding.

______________________________________________________________________

### Ignoring Logs

Logs often contain the exact error.

______________________________________________________________________

### Using localhost

Inside Docker,

communicate

using service names.

______________________________________________________________________

### Ignoring Health Status

A running container

isn't always

a healthy application.

______________________________________________________________________

# Best Practices

- Start with `docker ps`.
- Read logs before changing anything.
- Use `docker inspect`.
- Verify environment variables.
- Verify networks.
- Verify volumes.
- Check resource usage.
- Follow a repeatable debugging process.

______________________________________________________________________

# Hands-on Exercise

1. Stop PostgreSQL.
1. Observe the FastAPI error.
1. Read logs.
1. Fix the database.
1. Verify the health check.
1. Inspect the network.
1. Inspect the volume.
1. Monitor resource usage.
1. Rebuild the application after changing dependencies.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** A FastAPI container cannot connect to PostgreSQL inside Docker. How would you troubleshoot it?

I would first verify that both containers are running using `docker ps`. Then I'd inspect the FastAPI logs for
connection errors. Next, I'd confirm both containers are attached to the same Docker network and that the application is
using the PostgreSQL service name instead of `localhost`. I'd verify the environment variables, ensure PostgreSQL is
healthy and listening on the expected port, and test connectivity from inside the FastAPI container if needed. This
structured approach isolates the root cause without unnecessary changes.

______________________________________________________________________

# Summary

In this chapter, you learned:

- A structured Docker debugging workflow
- Container inspection
- Logs
- Shell access
- Environment variable debugging
- Network debugging
- Volume debugging
- Port debugging
- Health checks
- Resource monitoring
- Common production issues
- Docker cleanup

You now have the skills to troubleshoot most day-to-day Docker problems.

In the next chapter, we'll learn **Docker Security Best Practices**, including running containers as non-root users,
minimizing attack surfaces, image scanning, and protecting secrets.

______________________________________________________________________

## Next File

[Docker Security Best Practices](17-docker-security-best-practices.md)
