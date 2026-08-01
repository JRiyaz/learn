# Docker - Part 3

# Docker Images, Containers & Layers

______________________________________________________________________

# Introduction

In the previous lecture, we learned about Docker's architecture.

We now know:

- Docker CLI
- Docker Daemon
- Docker Engine
- Container Runtime

But one question still remains:

> **What exactly is an Image?**

> **How is it different from a Container?**

This is one of the most common Docker interview topics.

By the end of this chapter, you'll understand:

- Images
- Containers
- Layers
- Copy-on-Write
- Why Docker images are small
- Why containers start quickly

______________________________________________________________________

# Image vs Container

The easiest way to understand this is with an analogy.

Think of Microsoft Word.

```text id="docker301"
Document Template

↓

New Document
```

The template is never modified.

Every new document starts from the template.

Docker works the same way.

```text id="docker302"
Docker Image

↓

Container
```

The image is the template.

The container is the running instance.

______________________________________________________________________

# Docker Image

A Docker Image is

- Read-only
- Immutable
- A template
- Used to create containers

It contains

- Application
- Python
- Libraries
- Dependencies
- Files
- Configuration

An image is **not running**.

______________________________________________________________________

# Container

A Container is

- Running
- Writable
- Isolated
- Created from an image

Every time you execute

```bash id="docker303"
docker run nginx
```

Docker creates

```text id="docker304"
Image

↓

Container
```

______________________________________________________________________

# Multiple Containers

One image

can create many containers.

```text id="docker305"
Python Image

        │

 ┌──────┼──────┐

 ▼      ▼      ▼

C1     C2     C3
```

Each container is independent.

______________________________________________________________________

# Real Example

Suppose

we have the Redis image.

```text id="docker306"
Redis Image
```

Run

```bash id="docker307"
docker run redis

docker run redis

docker run redis
```

Result

```text id="docker308"
Redis Container 1

Redis Container 2

Redis Container 3
```

One image.

Three containers.

______________________________________________________________________

# What Is Inside an Image?

A Docker image consists of multiple layers.

```text id="docker309"
Application Layer

↓

Python Packages

↓

Python Runtime

↓

Operating System Libraries
```

Each layer is read-only.

______________________________________________________________________

# Why Layers?

Suppose

two applications

use

Python 3.12.

Without layers

```text id="docker310"
Python

↓

Copied Twice
```

Wasteful.

With layers

```text id="docker311"
Python Layer

↓

Shared
```

Both images reuse the same layer.

______________________________________________________________________

# Layer Example

Image A

```text id="docker312"
FastAPI App

↓

Python

↓

Ubuntu
```

Image B

```text id="docker313"
Flask App

↓

Python

↓

Ubuntu
```

Docker stores

```text id="docker314"
Ubuntu

↓

One Copy

Python

↓

One Copy
```

Only the application layer differs.

______________________________________________________________________

# Image Layer Stack

Example

```text id="docker315"
Layer 4

Application

────────────

Layer 3

Requirements

────────────

Layer 2

Python

────────────

Layer 1

Ubuntu
```

Every layer builds on top of the previous one.

______________________________________________________________________

# Why Are Images Small?

Suppose

100 images

use Ubuntu.

Docker stores

Ubuntu

only once.

This saves

disk space

and download time.

______________________________________________________________________

# Copy-on-Write

Containers

do **not**

modify the image.

Instead,

Docker creates

one additional

writable layer.

```text id="docker316"
Container

↓

Writable Layer

↓

Image Layers
```

______________________________________________________________________

# Example

Suppose

container writes

```text id="docker317"
/tmp/data.txt
```

The file is written only to

```text id="docker318"
Writable Layer
```

The image

remains unchanged.

______________________________________________________________________

# Another Container

Container 2

starts from

the same image.

```text id="docker319"
Image

↓

New Writable Layer
```

It does

not

see files created by Container 1.

Containers are isolated.

______________________________________________________________________

# Visualizing Copy-on-Write

```text id="docker320"
             Image

      Ubuntu

      Python

      FastAPI

          │

──────────┼──────────

          │

     Container A

 Writable Layer

──────────┼──────────

          │

     Container B

 Writable Layer
```

Each container gets its own writable layer.

The image stays unchanged.

______________________________________________________________________

# Image Immutability

Suppose

you install

```bash id="docker321"
pip install pandas
```

inside

a running container.

Only

that container

changes.

The original image

is exactly the same.

Destroy the container,

and the change disappears.

______________________________________________________________________

# Why Containers Start So Fast?

Traditional Virtual Machine

```text id="docker322"
Boot OS

↓

Boot Services

↓

Start Application
```

Docker Container

```text id="docker323"
Create Writable Layer

↓

Start Process
```

Containers generally start much faster because they reuse the host kernel instead of booting a separate operating
system.

______________________________________________________________________

# Image IDs

Every image

has

a unique ID.

Example

```bash id="docker324"
docker images
```

Output

```text id="docker325"
REPOSITORY

TAG

IMAGE ID

redis

latest

abcd1234
```

The image ID uniquely identifies the image version stored locally.

______________________________________________________________________

# Container IDs

Similarly,

every container

has

its own ID.

```bash id="docker326"
docker ps
```

Example

```text id="docker327"
CONTAINER ID

a91f2d34
```

Even if two containers use the same image,

their container IDs are different.

______________________________________________________________________

# Image Lifecycle

```text id="docker328"
Dockerfile

↓

Build Image

↓

Store Image

↓

Run Container

↓

Stop Container

↓

Remove Container

↓

Image Still Exists
```

Deleting a container does **not** delete its image.

______________________________________________________________________

# Container Lifecycle

```text id="docker329"
Created

↓

Running

↓

Stopped

↓

Removed
```

Containers are intended to be disposable.

______________________________________________________________________

# Why Are Containers Disposable?

Instead of fixing a broken container,

modern applications usually

```text id="docker330"
Delete

↓

Create New One
```

This is a core container philosophy.

______________________________________________________________________

# Common Mistakes

### Confusing Images and Containers

Image

↓

Template

Container

↓

Running instance

______________________________________________________________________

### Storing Important Data Inside Containers

Container storage is ephemeral.

Persistent data belongs in **Volumes**, which we'll cover later.

______________________________________________________________________

### Modifying Running Containers

Build a new image instead of manually changing containers.

______________________________________________________________________

### Thinking Containers Share Files

Containers created from the same image each have their own writable layer.

______________________________________________________________________

# Best Practices

- Treat images as immutable.
- Treat containers as disposable.
- Build new images for changes.
- Keep images small.
- Reuse shared layers.
- Store persistent data outside containers.

______________________________________________________________________

# Hands-on Exercise

Answer these questions.

1. What is a Docker Image?
1. What is a Docker Container?
1. Why are images immutable?
1. What are Docker layers?
1. Why are layers useful?
1. What is Copy-on-Write?
1. Why doesn't modifying one container affect another?
1. Why do containers start faster than virtual machines?

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Copy-on-Write in Docker?

Docker images are made of read-only layers. When a container starts, Docker adds a new writable layer on top of those
image layers. Any files created or modified by the container are stored only in this writable layer, leaving the
original image unchanged. This allows multiple containers to share the same image efficiently while remaining isolated
from each other.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Docker Images
- Docker Containers
- Image Layers
- Shared Layers
- Copy-on-Write
- Writable Layers
- Image IDs
- Container IDs
- Image Lifecycle
- Container Lifecycle
- Container Immutability
- Why Containers Start Quickly

In the next lecture, we'll learn how to build our own images using **Dockerfiles**, including Docker instructions, build
caching, and image optimization.

______________________________________________________________________

## Next File

[Dockerfile Deep Dive](4-dockerfile-deep-dive.md)
