# Docker - Part 2

# Docker Architecture

______________________________________________________________________

# Introduction

In the previous lecture, we learned

- Why Docker exists
- Images
- Containers
- Dockerfiles
- Registries

Now let's answer one of the most common interview questions:

> **What actually happens when you run a Docker container?**

To answer that, we need to understand Docker's architecture.

______________________________________________________________________

# High-Level Architecture

When you type

```bash id="docker201"
docker run nginx
```

a lot happens behind the scenes.

```text id="docker202"
          You

           │

           ▼

     Docker CLI

           │

           ▼

    Docker Daemon

           │

     ┌─────┴─────┐

     ▼           ▼

 Docker Images  Containers

           │

           ▼

 Linux Kernel
```

Each component has a different responsibility.

______________________________________________________________________

# Docker Components

Docker consists of four major parts.

```text id="docker203"
Docker CLI

↓

Docker Daemon

↓

Docker Engine

↓

Container Runtime
```

Let's study each one.

______________________________________________________________________

# Docker CLI

CLI stands for

```text id="docker204"
Command Line Interface
```

Examples

```bash id="docker205"
docker run

docker build

docker ps

docker stop
```

The CLI itself

doesn't create containers.

It only sends requests.

______________________________________________________________________

# Docker Daemon

The Docker Daemon is the background service that performs the actual work.

Responsibilities:

- Build images
- Start containers
- Stop containers
- Remove containers
- Manage networks
- Manage volumes
- Download images

Think of it as Docker's engine room.

______________________________________________________________________

# Communication

When you run

```bash id="docker206"
docker ps
```

Flow

```text id="docker207"
CLI

↓

Docker Daemon

↓

List Containers

↓

Return Result
```

The CLI and Daemon communicate using an API.

______________________________________________________________________

# Docker Engine

The Docker Engine includes:

```text id="docker208"
Docker CLI

+

Docker Daemon

+

REST API
```

These components work together to manage containers.

______________________________________________________________________

# Container Runtime

The runtime is responsible for actually creating and running containers.

```text id="docker209"
Docker Daemon

↓

Container Runtime

↓

Running Container
```

Modern Docker uses an Open Container Initiative (OCI) compatible runtime (commonly `runc`) under the hood.

You don't interact with it directly,

but it's an important part of the architecture.

______________________________________________________________________

# Image Store

Docker keeps downloaded images locally.

```text id="docker210"
Docker Images

↓

Image Store
```

Example

```bash id="docker211"
docker pull redis
```

Redis is downloaded

once

and stored locally.

Future containers reuse the same image.

______________________________________________________________________

# Container Store

Running containers are also tracked.

```text id="docker212"
Container

↓

Running

Stopped

Exited
```

Docker maintains their state.

______________________________________________________________________

# Registry

Where do images come from?

Usually

```text id="docker213"
Docker Hub
```

Flow

```text id="docker214"
Docker Hub

↓

Download Image

↓

Local Image Store

↓

Create Container
```

Later,

we'll build our own images.

______________________________________________________________________

# Example Workflow

Suppose

```bash id="docker215"
docker run redis
```

Internally

```text id="docker216"
CLI

↓

Daemon

↓

Image Exists?

├── Yes

│      ↓

│  Start Container

│

└── No

       ↓

 Download Image

       ↓

 Save Image

       ↓

 Start Container
```

______________________________________________________________________

# Why Doesn't Docker Download Every Time?

Because images are cached locally.

First run

↓

Download

Second run

↓

Reuse

Much faster.

______________________________________________________________________

# Multiple Containers

One image

can create many containers.

Example

```text id="docker217"
Redis Image

↓

Container 1

Container 2

Container 3
```

Each container is independent.

______________________________________________________________________

# Multiple Images

```text id="docker218"
FastAPI Image

↓

Container

PostgreSQL Image

↓

Container

Redis Image

↓

Container
```

Each service

gets its own image.

______________________________________________________________________

# Docker Client-Server Model

Docker follows

a client-server architecture.

```text id="docker219"
Client

↓

Request

↓

Daemon

↓

Response
```

This allows remote Docker management.

______________________________________________________________________

# Local vs Remote Daemon

Usually

```text id="docker220"
CLI

↓

Local Daemon
```

But it can also be

```text id="docker221"
CLI

↓

Remote Daemon
```

This is useful in build servers and remote infrastructure.

______________________________________________________________________

# Container Lifecycle

```text id="docker222"
Create

↓

Start

↓

Running

↓

Stop

↓

Restart

↓

Remove
```

Every container follows this lifecycle.

______________________________________________________________________

# What Happens During `docker run`?

Example

```bash id="docker223"
docker run nginx
```

Docker performs:

1. Check local image.
1. Download image if needed.
1. Create writable container layer.
1. Configure networking.
1. Mount volumes (if specified).
1. Start the container process.
1. Monitor the container.

All of this happens in seconds.

______________________________________________________________________

# Why Is Docker Fast?

Docker does **not** boot a complete operating system for every container.

Instead,

containers share the host operating system kernel.

This significantly reduces startup time and resource usage compared with traditional virtual machines.

We'll understand exactly how this works in the next lecture.

______________________________________________________________________

# Real Backend Example

Imagine our backend.

```text id="docker224"
FastAPI

↓

Redis

↓

PostgreSQL

↓

Kafka
```

Docker creates

four separate containers.

Each container

has:

- Its own process
- Its own filesystem
- Its own networking configuration

while still sharing the host kernel.

______________________________________________________________________

# Common Mistakes

### Thinking CLI Runs Containers

The CLI only sends commands.

The Daemon does the work.

______________________________________________________________________

### Thinking Images Are Containers

Images are templates.

Containers are running instances.

______________________________________________________________________

### Confusing Docker Engine and Docker Daemon

The Engine is the overall platform.

The Daemon is one of its core components.

______________________________________________________________________

### Assuming Every Container Downloads Again

Images are cached locally.

______________________________________________________________________

# Best Practices

- Keep one service per container.
- Reuse images whenever possible.
- Pull trusted images.
- Understand the container lifecycle.
- Learn how the Daemon works.
- Don't confuse Images with Containers.

______________________________________________________________________

# Hands-on Exercise

Answer these questions.

1. What is the Docker CLI?
1. What is the Docker Daemon?
1. What is Docker Engine?
1. What is a Container Runtime?
1. What happens during `docker run`?
1. Why doesn't Docker download an image every time?
1. Why can one image create many containers?
1. Why is Docker called a client-server architecture?

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What happens internally when you execute `docker run nginx`?

The Docker CLI sends the request to the Docker Daemon. The Daemon checks whether the `nginx` image exists locally. If
not, it downloads the image from a registry such as Docker Hub. It then creates a new container from that image,
configures networking and any requested volumes, starts the container's main process using the container runtime, and
monitors the container until it exits.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Docker architecture
- Docker CLI
- Docker Daemon
- Docker Engine
- Container Runtime
- Image Store
- Container Store
- Docker Registry
- Client-server model
- Container lifecycle
- What happens during `docker run`

In the next lecture, we'll explore one of the most important Docker concepts:

**Images, Containers, and Layers**, including Copy-on-Write and why Docker images are so efficient.

______________________________________________________________________

## Next File

[Docker Images, Containers & Layers](3-docker-images-containers-layers.md)
