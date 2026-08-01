# Docker - Part 17

# Docker Security Best Practices

______________________________________________________________________

# Introduction

By now, you can:

- Build Docker images
- Containerize FastAPI
- Run PostgreSQL, Redis, and Kafka
- Use Docker Compose
- Debug Docker applications

But there's one important topic left before we build our final project:

**Security.**

Many Docker tutorials stop after teaching `docker run`.

Real production systems require much more.

This chapter focuses on practical Docker security that every backend engineer should know.

______________________________________________________________________

# Why Docker Security Matters?

Imagine your application is running on the Internet.

An attacker gains access to your container.

If your container is poorly configured,

they may be able to:

- Read sensitive files
- Steal credentials
- Install malicious software
- Consume excessive resources
- Exploit unnecessary packages

Security starts before deployment.

It starts with how the image is built.

______________________________________________________________________

# Principle of Least Privilege

One of the most important security principles is:

```text id="security001"
Give

Only

The Permissions

Required
```

Nothing more.

______________________________________________________________________

# Running as Root

By default,

many Docker images run as

```text id="security002"
root
```

This means

the application

has administrative privileges

inside the container.

This is usually unnecessary.

______________________________________________________________________

# Creating a Non-Root User

Dockerfile

```dockerfile id="security003"
FROM python:3.12-slim

RUN useradd \
    --create-home \
    appuser

USER appuser
```

Now

the application

runs as

```text id="security004"
appuser
```

instead of `root`.

______________________________________________________________________

# Why Is This Better?

Suppose

an attacker exploits your application.

Instead of

```text id="security005"
Administrator Access
```

they receive

```text id="security006"
Limited User
```

The impact of the compromise is reduced.

______________________________________________________________________

# File Permissions

Instead of

```text id="security007"
Everyone

↓

Everything
```

restrict access.

Example

```dockerfile id="security008"
COPY --chown=appuser:appuser . .
```

Your application files

are owned

by the non-root user.

______________________________________________________________________

# Keep Images Small

Large images

contain

more packages.

More packages

often mean

more potential vulnerabilities.

Prefer

```dockerfile id="security009"
python:3.12-slim
```

over larger images when appropriate.

______________________________________________________________________

# Remove Unnecessary Packages

Avoid installing

tools you don't need.

Example

```dockerfile id="security010"
RUN apt-get update && \
    apt-get install -y curl
```

If `curl` is only needed during the build,

it shouldn't remain in the final runtime image.

Multi-stage builds help with this.

______________________________________________________________________

# Pin Image Versions

Avoid

```dockerfile id="security011"
FROM python:latest
```

Prefer

```dockerfile id="security012"
FROM python:3.12-slim
```

Pinned versions improve consistency and reduce unexpected changes.

______________________________________________________________________

# Pin Dependency Versions

Avoid

```text id="security013"
fastapi

sqlalchemy
```

Prefer

```text id="security014"
fastapi==0.116.1

sqlalchemy==2.0.43
```

Using explicit versions helps create reproducible builds.

Update them intentionally as part of your maintenance process.

______________________________________________________________________

# Don't Store Secrets

Never write

```dockerfile id="security015"
ENV DATABASE_PASSWORD=secret123
```

Secrets become part of the image metadata.

Instead,

provide them

at runtime.

______________________________________________________________________

# Environment Variables

Better

```bash id="security016"
docker run \
-e DATABASE_PASSWORD=secret123 \
api
```

Or,

for production,

use dedicated secret-management systems.

______________________________________________________________________

# Don't Commit `.env`

Usually,

your repository should contain

```text id="security017"
.gitignore
```

including

```text id="security018"
.env
```

Production secrets

don't belong

in Git.

______________________________________________________________________

# Read-Only Containers

Many applications

don't need

to modify their filesystem.

Docker supports

a read-only root filesystem.

```bash id="security019"
docker run \
--read-only \
api
```

Only explicitly mounted writable locations remain writable.

______________________________________________________________________

# Resource Limits

Limit

CPU

and

memory.

```bash id="security020"
docker run \
--cpus=2 \
--memory=1g \
api
```

This reduces the impact of runaway processes or denial-of-service scenarios.

______________________________________________________________________

# Drop Linux Capabilities

Linux processes have capabilities.

Most applications

don't need

all of them.

Example

```bash id="security021"
docker run \
--cap-drop ALL \
api
```

Then add back only the capabilities that are actually required.

This is an advanced hardening technique.

______________________________________________________________________

# Avoid Privileged Containers

Never run

```bash id="security022"
docker run \
--privileged
```

unless absolutely necessary.

Privileged containers have extensive access to the host system.

______________________________________________________________________

# Scan Images

Before deployment,

scan images

for known vulnerabilities.

Examples

```text id="security023"
Docker Scout

Trivy

Grype
```

Regular scanning helps identify outdated packages and security issues.

______________________________________________________________________

# Verify Image Sources

Use

trusted images.

Prefer

- Official Docker images
- Well-maintained vendor images
- Internal company images

Avoid unknown images from untrusted publishers.

______________________________________________________________________

# Sign Images

In large organizations,

images may be digitally signed

to verify authenticity.

This helps ensure deployed images haven't been tampered with.

______________________________________________________________________

# Network Isolation

Don't place

every container

on the same network.

Example

```text id="security024"
Frontend Network

↓

API Network

↓

Database Network
```

Separate networks reduce unnecessary communication paths.

______________________________________________________________________

# Expose Only Required Ports

Bad

```text id="security025"
5432

6379

9092

8000

All Public
```

Better

```text id="security026"
8000

Public

↓

Database

Internal

↓

Redis

Internal
```

Only publish ports that external clients must access.

______________________________________________________________________

# Health Checks

Health checks

improve reliability,

but they also reduce the chance of sending traffic to unhealthy containers when used with orchestration platforms.

______________________________________________________________________

# Logging

Never log

```text id="security027"
Passwords

Tokens

Secrets
```

Logs often end up in centralized systems.

Treat them as potentially accessible.

______________________________________________________________________

# Rootless Docker

Docker itself can also run without root privileges on the host in supported environments.

This provides another layer of security by reducing the privileges of the Docker daemon.

______________________________________________________________________

# Update Regularly

Old images

may contain

known vulnerabilities.

Rebuild images regularly

with updated base images and dependencies.

______________________________________________________________________

# Security Checklist

```text id="security028"
✓ Non-root User

✓ Small Image

✓ Pinned Versions

✓ Secrets External

✓ Resource Limits

✓ Health Checks

✓ Image Scanning

✓ Network Isolation

✓ Minimal Packages
```

This checklist covers many common production recommendations.

______________________________________________________________________

# Common Mistakes

### Running Everything as Root

Use a dedicated application user whenever possible.

______________________________________________________________________

### Using `latest`

Pin versions.

______________________________________________________________________

### Committing Secrets

Keep secrets outside source control.

______________________________________________________________________

### Exposing Databases Publicly

Databases should generally remain on internal networks.

______________________________________________________________________

### Ignoring Security Updates

Regularly update base images and dependencies.

______________________________________________________________________

# Best Practices

- Run as a non-root user.
- Pin image and dependency versions.
- Keep images small.
- Remove unnecessary packages.
- Use multi-stage builds.
- Keep secrets out of images.
- Limit resources.
- Scan images.
- Publish only required ports.
- Update images regularly.

______________________________________________________________________

# Hands-on Exercise

1. Modify your FastAPI Dockerfile to use a non-root user.
1. Pin dependency versions.
1. Add a `.gitignore` entry for `.env`.
1. Run the container with a read-only filesystem.
1. Add CPU and memory limits.
1. Scan the image using a vulnerability scanner.
1. Verify that PostgreSQL is accessible only on the internal network.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the most important Docker security practices for production?

A secure Docker deployment should use minimal base images, run applications as non-root users, pin image and dependency
versions, keep secrets out of Dockerfiles, publish only required ports, set resource limits, scan images for
vulnerabilities, and keep images updated. These practices reduce the attack surface and improve the overall security and
reliability of containerized applications.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Docker security principles
- Non-root users
- File ownership
- Small images
- Pinned versions
- Secret management
- Read-only filesystems
- Resource limits
- Linux capabilities
- Privileged containers
- Image scanning
- Trusted images
- Network isolation
- Security best practices

Congratulations!

You have now completed the **Docker Fundamentals** portion of the course.

In the next chapter, we'll begin building a **complete multi-container backend project** using:

- FastAPI
- PostgreSQL
- Redis
- Kafka
- Docker Compose

You'll see how everything we've learned fits together in a realistic backend application.

______________________________________________________________________

## Next File

[Docker Project - Part 1](18-docker-project-part-1.md)
