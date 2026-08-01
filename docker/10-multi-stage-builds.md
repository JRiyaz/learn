# Docker - Part 10

# Multi-Stage Builds

______________________________________________________________________

# Introduction

So far, we've learned how to build Docker images.

A typical Dockerfile looks like this.

```dockerfile id="docker1001"
FROM python:3.12-slim

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

This works well.

But production Docker images should be:

- Smaller
- Faster
- More secure
- Easier to deploy

This is where **Multi-Stage Builds** help.

______________________________________________________________________

# The Problem

Suppose you're building an application that requires compilation.

Examples

- C Extensions
- Rust libraries
- Cython
- Go applications
- Java applications
- Frontend applications (React, Vue, Angular)

During the build,

you install

```text id="docker1002"
gcc

make

build-essential

headers
```

These are needed

only

while building.

They shouldn't exist

inside the final production image.

______________________________________________________________________

# Traditional Build

```text id="docker1003"
Build Tools

↓

Application

↓

Production
```

Everything remains inside the image.

Result

↓

Large image.

______________________________________________________________________

# Multi-Stage Build

Instead

```text id="docker1004"
Stage 1

↓

Build

↓

Stage 2

↓

Production
```

Only the required files

are copied

to the final image.

______________________________________________________________________

# Visual Architecture

```text id="docker1005"
Builder Image

↓

Compile

↓

Artifacts

↓

Production Image
```

The builder image is discarded.

______________________________________________________________________

# Why Is This Better?

The final image contains

- Application
- Runtime
- Required libraries

It does **not** contain

- GCC
- Make
- Build tools
- Temporary files

This reduces size and attack surface.

______________________________________________________________________

# Stage 1

Example

```dockerfile id="docker1006"
FROM python:3.12 AS builder

WORKDIR /app
```

Notice

```dockerfile
AS builder
```

We're giving this stage

a name.

______________________________________________________________________

# Install Dependencies

```dockerfile id="docker1007"
COPY requirements.txt .

RUN pip install \

    --prefix=/install \

    -r requirements.txt
```

Instead of installing into the system location, this example installs packages into `/install`, making it easy to copy
only the installed artifacts into the final image.

______________________________________________________________________

# Copy Source

```dockerfile id="docker1008"
COPY . .
```

Everything required

for building

is available.

______________________________________________________________________

# Stage 2

```dockerfile id="docker1009"
FROM python:3.12-slim

WORKDIR /app
```

Notice

we started

a completely new image.

The previous stage

is isolated.

______________________________________________________________________

# Copy Installed Packages

```dockerfile id="docker1010"
COPY \

--from=builder \

/install \

/usr/local
```

This copies

only

the installed packages.

______________________________________________________________________

# Copy Application

```dockerfile id="docker1011"
COPY . .
```

Now

the application

exists

inside the production image.

______________________________________________________________________

# Start Application

```dockerfile id="docker1012"
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

# Complete Multi-Stage Dockerfile

```dockerfile id="docker1013"
FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --prefix=/install \
    -r requirements.txt

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

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

# What Gets Copied?

Builder

```text id="docker1014"
Python

Compiler

Requirements

Application
```

Production

```text id="docker1015"
Python

Dependencies

Application
```

Compiler

↓

Removed.

______________________________________________________________________

# Layer Comparison

Single Stage

```text id="docker1016"
Compiler

↓

Application

↓

Production
```

Multi-Stage

```text id="docker1017"
Builder

↓

Artifacts

↓

Production
```

Cleaner.

Smaller.

______________________________________________________________________

# Real Example

Suppose

React Frontend.

Builder

```text id="docker1018"
Node.js

↓

npm install

↓

npm run build
```

Output

```text id="docker1019"
dist/
```

Production

```text id="docker1020"
Nginx

↓

Copy dist/

↓

Serve Static Files
```

Node.js

doesn't exist

inside production.

______________________________________________________________________

# Another Example

Go

Builder

```text id="docker1021"
Go Compiler

↓

Compile Binary
```

Production

```text id="docker1022"
Minimal Runtime

↓

Binary
```

Only

the executable

is copied.

______________________________________________________________________

# Why Python Uses Multi-Stage

Although many Python applications don't require compilation,

Multi-Stage Builds are still useful when:

- Building wheels
- Installing system packages
- Compiling native extensions
- Separating build dependencies from runtime dependencies

______________________________________________________________________

# Build Cache Still Works

Each stage

has

its own cache.

Changing

```text id="docker1023"
app.py
```

doesn't necessarily rebuild

everything.

Proper Dockerfile ordering remains important.

______________________________________________________________________

# Image Size

Typical comparison

```text id="docker1024"
Single Stage

↓

Large

Multi-Stage

↓

Smaller
```

The exact savings depend on the application and its dependencies.

______________________________________________________________________

# Security Benefits

Smaller images mean

- Fewer packages
- Smaller attack surface
- Fewer vulnerabilities
- Faster security scanning

Security improves because unnecessary tools aren't shipped.

______________________________________________________________________

# Build Command

Exactly the same.

```bash id="docker1025"
docker build \

-t fastapi-app .
```

Docker automatically processes

both stages.

______________________________________________________________________

# Common Mistakes

### Copying the Entire Builder

Don't copy everything.

Only copy

what the application needs.

______________________________________________________________________

### Installing Build Tools in Production

The production image

should contain

only runtime dependencies.

______________________________________________________________________

### Ignoring Image Size

Smaller images

download faster

and deploy more quickly.

______________________________________________________________________

### Mixing Build and Runtime Dependencies

Separate them

into different stages.

______________________________________________________________________

# Best Practices

- Use Multi-Stage Builds for production.
- Keep the final image minimal.
- Copy only required artifacts.
- Remove unnecessary build tools.
- Combine with `.dockerignore`.
- Continue using layer caching effectively.

______________________________________________________________________

# Hands-on Exercise

1. Convert a single-stage Dockerfile into a multi-stage build.
1. Build the image.
1. Compare image sizes.
1. Inspect the final image.
1. Verify that build tools aren't included.
1. Rebuild after changing only `app.py` and observe caching.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why are Multi-Stage Builds considered a Docker best practice?

Multi-Stage Builds separate the build environment from the runtime environment. Build tools, compilers, and temporary
files remain in the builder stage, while only the required application artifacts are copied into the final image. This
produces smaller, more secure images that download faster, deploy more quickly, and contain fewer unnecessary packages.

______________________________________________________________________

# Summary

In this chapter, you learned:

- What Multi-Stage Builds are
- Builder and production stages
- Copying artifacts between stages
- Image size optimization
- Security improvements
- Python use cases
- Frontend and Go examples
- Layer caching with multiple stages
- Production Dockerfile best practices

You've now learned how to build production-ready Docker images.

In the next chapter, we'll learn **Docker Compose**, where we'll manage multiple containers such as FastAPI, PostgreSQL,
Redis, and Kafka using a single configuration file.

______________________________________________________________________

## Next File

[Docker Compose](11-docker-compose.md)
