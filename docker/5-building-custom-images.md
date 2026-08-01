# Docker - Part 5

# Building Custom Images

______________________________________________________________________

# Introduction

In the previous lecture, we learned how to write a Dockerfile.

Now we'll build **production-quality Docker images**.

This chapter focuses on:

- Building images
- Image tagging
- Image optimization
- Base image selection
- `.dockerignore`
- Inspecting images
- Best practices

By the end of this chapter, you'll understand how experienced backend engineers build efficient Docker images.

______________________________________________________________________

# Our Example Project

We'll use a simple FastAPI application.

```text id="docker501"
project/

├── app.py

├── requirements.txt

├── Dockerfile

└── .dockerignore
```

______________________________________________________________________

# Application

**app.py**

```python id="docker502"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello Docker!"
    }
```

______________________________________________________________________

# Requirements

```text id="docker503"
fastapi

uvicorn
```

______________________________________________________________________

# First Dockerfile

```dockerfile id="docker504"
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [

    "uvicorn",

    "app:app",

    "--host",

    "0.0.0.0",

    "--port",

    "8000"

]
```

______________________________________________________________________

# Building the Image

```bash id="docker505"
docker build -t fastapi-app .
```

Breakdown

```text id="docker506"
docker build

↓

Build Image

-t

↓

Tag

fastapi-app

.

↓

Current Directory
```

______________________________________________________________________

# What Is a Tag?

A tag identifies a specific version of an image.

Example

```text id="docker507"
fastapi-app:1.0

fastapi-app:2.0

fastapi-app:latest
```

Think of tags like software versions.

______________________________________________________________________

# Building Different Versions

```bash id="docker508"
docker build -t fastapi-app:v1 .

docker build -t fastapi-app:v2 .
```

Now both images exist locally.

______________________________________________________________________

# Viewing Images

```bash id="docker509"
docker images
```

Example

```text id="docker510"
REPOSITORY

TAG

IMAGE ID

fastapi-app

v1

a91fd2

fastapi-app

v2

bc4218
```

______________________________________________________________________

# Running the Image

```bash id="docker511"
docker run fastapi-app:v1
```

Docker creates

a container

from the image.

______________________________________________________________________

# Image Layers

Suppose the Dockerfile is

```dockerfile id="docker512"
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

Layers

```text id="docker513"
Application

↓

Dependencies

↓

Python

↓

Base OS
```

Each instruction builds on previous layers.

______________________________________________________________________

# Choosing a Base Image

Several options exist.

```dockerfile id="docker514"
FROM python:3.12
```

or

```dockerfile id="docker515"
FROM python:3.12-slim
```

or

```dockerfile id="docker516"
FROM python:3.12-alpine
```

Each has trade-offs.

______________________________________________________________________

# Standard Image

```dockerfile id="docker517"
FROM python:3.12
```

Advantages

- Complete environment
- Excellent compatibility
- Easier debugging

Disadvantages

- Larger image size

______________________________________________________________________

# Slim Image

```dockerfile id="docker518"
FROM python:3.12-slim
```

Advantages

- Much smaller
- Faster downloads
- Lower storage usage

Disadvantages

- Some OS packages are not included and may need to be installed manually.

For many Python backend services, `slim` is a good default choice.

______________________________________________________________________

# Alpine Image

```dockerfile id="docker519"
FROM python:3.12-alpine
```

Advantages

- Very small image

Disadvantages

- Uses a different C standard library (`musl` instead of `glibc`).
- Some Python packages with native extensions may require additional build steps or have compatibility considerations.

Use Alpine only when you understand these trade-offs.

______________________________________________________________________

# Which Base Image Should You Choose?

| Base Image | Recommended Use |
| ------------------ | ----------------------------------------------------------------------------------- |
| python:3.12 | Learning and development |
| python:3.12-slim | Most production Python services |
| python:3.12-alpine | Specialized cases where image size is critical and compatibility has been evaluated |

______________________________________________________________________

# Image Size

Example

```text id="docker520"
Standard

↓

Large

Slim

↓

Smaller

Alpine

↓

Usually Smallest
```

Smaller images

generally download faster

and use less storage.

______________________________________________________________________

# `.dockerignore`

Just like `.gitignore`,

Docker supports

```text id="docker521"
.dockerignore
```

Example

```text id="docker522"
__pycache__/

.git/

.env

.venv/

*.log

.pytest_cache/
```

These files won't be copied into the build context.

______________________________________________________________________

# Why `.dockerignore` Matters

Without it

```text id="docker523"
Project

↓

Everything

↓

Docker Image
```

Including

- Git history
- Cache
- Logs
- Virtual environments

This increases build time and image size.

______________________________________________________________________

# Inspecting Images

```bash id="docker524"
docker image inspect fastapi-app
```

Shows

- Metadata
- Environment variables
- Layers
- Entry point
- Working directory
- Configuration

Useful for debugging.

______________________________________________________________________

# Image History

```bash id="docker525"
docker history fastapi-app
```

Displays

every layer

created during the build.

Example

```text id="docker526"
FROM

↓

COPY

↓

RUN

↓

COPY

↓

CMD
```

This helps explain image size and layer creation.

______________________________________________________________________

# Rebuilding Images

Suppose

you change

```text id="docker527"
app.py
```

Rebuild

```bash id="docker528"
docker build -t fastapi-app:v2 .
```

Docker reuses cached layers whenever possible.

______________________________________________________________________

# Removing Images

```bash id="docker529"
docker image rm fastapi-app:v1
```

Deletes

the image.

Containers created from that image must be removed before the image can usually be deleted.

______________________________________________________________________

# Multiple Projects

Suppose

```text id="docker530"
Inventory API

User API

Payment API
```

Each project

should have

its own Dockerfile

and its own image.

______________________________________________________________________

# Common Mistakes

### Using `latest` Everywhere

Instead of

```text id="docker531"
latest
```

prefer versioned tags.

Example

```text id="docker532"
v1.0.0

v1.1.0
```

Versioned images make deployments more predictable.

______________________________________________________________________

### Copying Everything

Use

`.dockerignore`

to reduce the build context.

______________________________________________________________________

### Choosing Alpine Without Understanding It

Alpine is not always the best production choice for Python applications.

______________________________________________________________________

### Using Large Base Images Unnecessarily

Choose the smallest image that meets your application's requirements.

______________________________________________________________________

# Best Practices

- Use descriptive image names.
- Use version tags.
- Prefer `python:3.12-slim` for many production Python APIs.
- Use `.dockerignore`.
- Inspect images during debugging.
- Rebuild images after application changes.
- Keep images small and secure.

______________________________________________________________________

# Hands-on Exercise

1. Create a Dockerfile for a FastAPI application.
1. Build version `v1`.
1. Build version `v2`.
1. Inspect the image.
1. View image history.
1. Create a `.dockerignore` file.
1. Compare image sizes using different base images.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do many production Python applications use `python:3.12-slim` instead of the full Python image?

The `slim` image removes many packages that aren't needed for most applications, making the image significantly smaller.
Smaller images download faster, consume less storage, and often reduce deployment times while still providing good
compatibility for typical Python backend services.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Building Docker images
- Image tags
- Versioning
- Base images
- Standard vs Slim vs Alpine
- `.dockerignore`
- Image inspection
- Image history
- Image optimization
- Production image best practices

In the next lecture, we'll learn about **Docker Volumes**, including why container storage is ephemeral and how to
persist application and database data safely.

______________________________________________________________________

## Next File

[Docker Volumes](6-docker-volumes.md)
