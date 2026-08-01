# Security - Part 25

# Secure Docker Containers

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Docker security matters
- Common Docker security mistakes
- Secure Dockerfile practices
- Running containers as non-root
- Image scanning
- Minimal base images
- Read-only file systems
- Container capabilities
- Best practices

______________________________________________________________________

# Why Docker Security Matters?

Containers make deployment easier,

but they are **not** security boundaries.

If a container is misconfigured,

an attacker may:

- Access sensitive files
- Escape the container (rare, but possible)
- Steal secrets
- Move laterally to other services

A secure application requires secure containers.

______________________________________________________________________

# Typical Deployment

```text id="dock2501"
FastAPI

↓

Docker Container

↓

Host Operating System

↓

Cloud
```

Security should be applied at every layer.

______________________________________________________________________

# Common Mistake 1

## Running as Root

Many beginners write:

```dockerfile id="dock2502"
FROM python:3.13

USER root
```

If the application is compromised,

the attacker gains root privileges inside the container.

______________________________________________________________________

# Better

Create a dedicated user.

```dockerfile id="dock2503"
FROM python:3.13-slim

RUN useradd -m appuser

USER appuser
```

This follows the **Principle of Least Privilege**.

______________________________________________________________________

# Common Mistake 2

## Using Large Base Images

Bad

```dockerfile id="dock2504"
FROM ubuntu
```

Large images include:

- More packages
- More binaries
- Larger attack surface

Better

```dockerfile id="dock2505"
FROM python:3.13-slim
```

or

```dockerfile id="dock2506"
FROM python:3.13-alpine
```

Choose a minimal image when it meets your application's requirements.

______________________________________________________________________

# Common Mistake 3

## Copying Everything

Bad

```dockerfile id="dock2507"
COPY . .
```

This may accidentally copy:

- `.env`
- `.git`
- SSH keys
- Test files
- Local configuration

______________________________________________________________________

# Better

Use

```text id="dock2508"
.dockerignore
```

Example

```text id="dock2509"
.git

.env

__pycache__/

tests/

*.pem
```

Only copy

what the application actually needs.

______________________________________________________________________

# Common Mistake 4

## Hardcoding Secrets

Bad

```dockerfile id="dock2510"
ENV JWT_SECRET=my-secret
```

Anyone with access to the image

can inspect it.

Instead,

provide secrets

at runtime

using:

- Environment variables
- Docker Secrets
- Cloud Secret Managers

______________________________________________________________________

# Common Mistake 5

## Installing Unnecessary Packages

Bad

```dockerfile id="dock2511"
RUN apt-get install -y \
    vim \
    curl \
    nano \
    ftp
```

Every extra package

increases the attack surface.

Install only

what your application requires.

______________________________________________________________________

# Multi-Stage Builds

Multi-stage builds

produce smaller,

cleaner images.

Example

```dockerfile id="dock2512"
FROM python:3.13 AS builder

# Install dependencies

FROM python:3.13-slim

# Copy only runtime files
```

Benefits:

- Smaller image
- Faster deployment
- Reduced attack surface

______________________________________________________________________

# Image Scanning

Before deploying,

scan Docker images

for known vulnerabilities.

Common tools:

- Docker Scout
- Trivy
- Snyk
- Grype

Workflow

```text id="dock2513"
Build Image

↓

Scan Image

↓

Fix Vulnerabilities

↓

Deploy
```

______________________________________________________________________

# Read-Only File System

If your application

doesn't need to write files,

run the container

with a read-only filesystem.

```text id="dock2514"
Container

↓

Read Only

↓

Reduced Risk
```

Attackers cannot easily modify application files.

______________________________________________________________________

# Limit Linux Capabilities

Containers inherit Linux capabilities.

Most applications

don't need all of them.

Drop unnecessary capabilities.

Example

```text id="dock2515"
Default Capabilities

↓

Remove Unused

↓

Least Privilege
```

______________________________________________________________________

# Resource Limits

Prevent one container

from consuming

all system resources.

Example

```text id="dock2516"
CPU Limit

Memory Limit

Restart Policy
```

These improve both

security

and stability.

______________________________________________________________________

# Secure Container Workflow

```text id="dock2517"
Minimal Base Image

↓

Non-root User

↓

Copy Required Files

↓

No Secrets

↓

Scan Image

↓

Deploy
```

______________________________________________________________________

# Defense in Depth

Secure containers use multiple protections.

```text id="dock2518"
Minimal Image

↓

Non-root User

↓

Image Scan

↓

Read-only FS

↓

Secrets Management

↓

Resource Limits
```

______________________________________________________________________

# Best Practices

✅ Use minimal base images.

✅ Run as a non-root user.

✅ Use `.dockerignore`.

✅ Never bake secrets into images.

✅ Scan images before deployment.

✅ Remove unnecessary packages.

✅ Use multi-stage builds.

✅ Configure resource limits.

______________________________________________________________________

# Common Mistakes

### Running Everything as Root

Containers should use

dedicated non-root users.

______________________________________________________________________

### Shipping Development Files

Exclude unnecessary files

using `.dockerignore`.

______________________________________________________________________

### Ignoring Image Vulnerabilities

Scan images regularly,

especially before production deployments.

______________________________________________________________________

### Treating Containers as Security Boundaries

Containers improve isolation,

but they are not a replacement

for secure application design.

______________________________________________________________________

### Forgetting Base Image Updates

Keep your base image

updated with security patches.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------- | ---------------------- |
| Root user | Non-root user |
| Large base image | Minimal base image |
| Secrets in image | Runtime secrets |
| No image scan | Scan before deployment |
| Copy entire project | Use `.dockerignore` |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the security best practices for Docker containers?

Secure Docker containers should use minimal base images, run applications as non-root users, avoid embedding secrets in
images, exclude unnecessary files using `.dockerignore`, scan images for known vulnerabilities, remove unused packages,
use multi-stage builds, configure resource limits, and follow the Principle of Least Privilege. Container security
complements, but does not replace, secure application development.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Docker security fundamentals
- Non-root containers
- Minimal base images
- `.dockerignore`
- Multi-stage builds
- Image scanning
- Read-only file systems
- Resource limits
- Best practices

______________________________________________________________________

# What's Next

[Security Checklist & Interview Revision](26-security-checklist.md)
