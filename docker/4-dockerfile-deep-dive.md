# Docker - Part 4

# Dockerfile Deep Dive

______________________________________________________________________

# Introduction

So far, we've learned:

- Docker Fundamentals
- Docker Architecture
- Images
- Containers
- Layers
- Copy-on-Write

Until now, we've only used images created by someone else.

For example

```bash id="docker401"
docker run redis

docker run postgres

docker run nginx
```

But in real projects,

you'll build your own Docker images.

That's where the **Dockerfile** comes in.

______________________________________________________________________

# What is a Dockerfile?

A Dockerfile is simply a text file that contains instructions for building a Docker image.

Think of it as

```text id="docker402"
Recipe

↓

Cake
```

Dockerfile

↓

Docker Image

______________________________________________________________________

# Docker Build Process

```text id="docker403"
Dockerfile

↓

docker build

↓

Docker Image

↓

docker run

↓

Container
```

Every image starts with a Dockerfile.

______________________________________________________________________

# First Dockerfile

```dockerfile id="docker404"
FROM python:3.12

WORKDIR /app

COPY . .

CMD ["python", "app.py"]
```

Only four instructions,

yet enough to build a simple Python application.

We'll understand every line.

______________________________________________________________________

# Dockerfile Instructions

The most commonly used instructions are:

```text id="docker405"
FROM

WORKDIR

COPY

RUN

ENV

EXPOSE

CMD

ENTRYPOINT
```

There are others, but these cover the majority of real-world Dockerfiles.

______________________________________________________________________

# FROM

Every Dockerfile begins with

```dockerfile id="docker406"
FROM
```

Example

```dockerfile id="docker407"
FROM python:3.12
```

Meaning

```text id="docker408"
Start with

Python 3.12 Image
```

Everything else builds on top of it.

______________________________________________________________________

# Base Image

```text id="docker409"
Ubuntu

↓

Python

↓

Your App
```

The first layer is called the **Base Image**.

Choosing a good base image affects image size, security, and compatibility.

______________________________________________________________________

# WORKDIR

Instead of

```bash id="docker410"
cd /app
```

Docker provides

```dockerfile id="docker411"
WORKDIR /app
```

Every following instruction runs from this directory.

______________________________________________________________________

# COPY

Copy files from your computer

into the image.

```dockerfile id="docker412"
COPY . .
```

Meaning

```text id="docker413"
Current Folder

↓

Image

/app
```

______________________________________________________________________

# COPY Specific Files

Instead of everything,

copy only what you need.

```dockerfile id="docker414"
COPY requirements.txt .
```

This is important for build caching.

We'll see why later.

______________________________________________________________________

# RUN

`RUN` executes commands while **building the image**.

Example

```dockerfile id="docker415"
RUN pip install -r requirements.txt
```

This installs dependencies during the build process.

The results become part of the image.

______________________________________________________________________

# CMD

`CMD` specifies the default command executed **when the container starts**.

Example

```dockerfile id="docker416"
CMD ["python", "app.py"]
```

When you execute

```bash id="docker417"
docker run my-app
```

Docker runs

```bash id="docker418"
python app.py
```

inside the container.

______________________________________________________________________

# ENV

Environment variables.

Example

```dockerfile id="docker419"
ENV APP_ENV=production

ENV PORT=8000
```

Your application can read these values at runtime.

Python

```python id="docker420"
import os

environment = os.getenv(
    "APP_ENV"
)
```

______________________________________________________________________

# EXPOSE

Suppose

FastAPI runs on

```text id="docker421"
8000
```

Tell Docker

```dockerfile id="docker422"
EXPOSE 8000
```

This documents that the application listens on port `8000`.

> **Note:** `EXPOSE` does **not** publish the port to your host machine. Port publishing is done when running the container (for example, with `-p`), which we'll cover later.

______________________________________________________________________

# Putting Everything Together

```dockerfile id="docker423"
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [

    "python",

    "app.py"

]
```

A simple but complete Dockerfile.

______________________________________________________________________

# How Docker Builds Images

Docker executes instructions

one at a time.

```text id="docker424"
FROM

↓

WORKDIR

↓

COPY

↓

RUN

↓

COPY

↓

CMD
```

Each instruction creates

a new image layer

(except some metadata instructions, which may not create filesystem layers).

______________________________________________________________________

# Docker Build Cache

Suppose

you modify

```text id="docker425"
app.py
```

but

```text id="docker426"
requirements.txt
```

doesn't change.

Docker can reuse previously built layers instead of rebuilding everything.

This makes builds much faster.

______________________________________________________________________

# Why Copy Requirements First?

Bad

```dockerfile id="docker427"
COPY . .

RUN pip install -r requirements.txt
```

Change one Python file

↓

Everything rebuilds,

including dependency installation.

______________________________________________________________________

Good

```dockerfile id="docker428"
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

Now,

changing application code doesn't force Docker to reinstall dependencies if `requirements.txt` is unchanged.

______________________________________________________________________

# Layer Visualization

```text id="docker429"
Layer 5

Application Code

────────────

Layer 4

Python Packages

────────────

Layer 3

Requirements

────────────

Layer 2

Working Directory

────────────

Layer 1

Python Base Image
```

Only the layers affected by a change need rebuilding.

______________________________________________________________________

# Build Command

Build an image

```bash id="docker430"
docker build -t my-fastapi-app .
```

Meaning

```text id="docker431"
Current Directory

↓

Dockerfile

↓

Image

↓

Tag

my-fastapi-app
```

______________________________________________________________________

# Running the Image

```bash id="docker432"
docker run my-fastapi-app
```

Docker creates

a container

from the image.

______________________________________________________________________

# Naming Images

Good examples

```text id="docker433"
inventory-api

user-service

order-service

payment-service
```

Avoid

```text id="docker434"
test

new

myapp123
```

Use descriptive names.

______________________________________________________________________

# Common Mistakes

### Forgetting `.dockerignore`

Without a `.dockerignore` file,

Docker may copy:

- `.git`
- Virtual environments
- Cache files
- Logs
- IDE folders

into the image,

making it unnecessarily large.

We'll create one later.

______________________________________________________________________

### Installing Dependencies After Copying Everything

This reduces build cache effectiveness.

______________________________________________________________________

### Using `RUN` Instead of `CMD`

Remember

`RUN`

↓

During image build

`CMD`

↓

When the container starts

______________________________________________________________________

### Hardcoding Secrets

Never put passwords or API keys directly in a Dockerfile.

Use environment variables or secret management solutions.

______________________________________________________________________

# Best Practices

- Start from a trusted base image.
- Keep Dockerfiles readable.
- Copy dependency files before application code.
- Use build caching effectively.
- Avoid unnecessary files.
- Never bake secrets into images.
- Keep images as small as practical.

______________________________________________________________________

# Hands-on Exercise

Create a Dockerfile for a simple FastAPI application that:

1. Uses Python 3.12.
1. Sets `/app` as the working directory.
1. Copies `requirements.txt`.
1. Installs dependencies.
1. Copies the application code.
1. Exposes port `8000`.
1. Starts the application.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do Dockerfiles usually copy `requirements.txt` before copying the application source code?

Docker builds images layer by layer and caches each layer. If `requirements.txt` is copied and dependencies are
installed before copying the application code, Docker can reuse the cached dependency layer whenever only the source
code changes. This avoids reinstalling dependencies on every build, making builds significantly faster.

______________________________________________________________________

# Summary

In this chapter, you learned:

- What a Dockerfile is
- Docker build process
- `FROM`
- `WORKDIR`
- `COPY`
- `RUN`
- `CMD`
- `ENV`
- `EXPOSE`
- Layer creation
- Build cache
- Docker build command
- Dockerfile best practices

In the next lecture, we'll build multiple real Dockerfiles for Python applications and learn image optimization
techniques, including choosing base images and reducing image size.

______________________________________________________________________

## Next File

[Building Custom Images](5-building-custom-images.md)
