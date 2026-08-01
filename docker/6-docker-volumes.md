# Docker - Part 6

# Docker Volumes

______________________________________________________________________

# Introduction

So far, we've learned:

- Docker Fundamentals
- Docker Architecture
- Images
- Containers
- Dockerfiles
- Building Images

Now we'll learn one of the most important Docker concepts:

> **Where does container data go?**

Suppose you're running PostgreSQL inside Docker.

You insert

```text id="docker601"
10 Million Rows
```

Then accidentally remove the container.

What happens to your data?

If you haven't configured persistent storage,

**it's gone.**

This chapter explains why.

______________________________________________________________________

# The Container Filesystem

Every container has its own writable filesystem.

```text id="docker602"
Image

↓

Writable Layer

↓

Container
```

When your application creates a file,

it is written into the container's writable layer.

Example

```text id="docker603"
/app/log.txt
```

The file exists

inside the container.

______________________________________________________________________

# The Problem

Suppose

```bash id="docker604"
docker run postgres
```

You create

```text id="docker605"
Customer Records
```

Everything looks fine.

Then

```bash id="docker606"
docker rm postgres-container
```

The writable layer is removed with the container.

Your data disappears.

______________________________________________________________________

# Why?

Remember

Containers are designed to be

```text id="docker607"
Disposable
```

Application

↓

Crash

↓

Create New Container

This is a feature,

not a bug.

______________________________________________________________________

# Solution

Docker provides

```text id="docker608"
Volumes
```

Volumes store data

outside

the container's writable layer.

______________________________________________________________________

# Architecture

Without Volume

```text id="docker609"
Container

↓

Writable Layer

↓

Deleted
```

Data disappears.

______________________________________________________________________

With Volume

```text id="docker610"
Container

↓

Volume

↓

Host Storage
```

Delete the container.

The volume still exists.

______________________________________________________________________

# What Is a Volume?

A Docker Volume is

a persistent storage location

managed by Docker.

Volumes exist independently of containers.

You can remove a container

without removing its volume.

______________________________________________________________________

# Why Volumes?

Volumes provide

- Data persistence
- Data sharing
- Easier backups
- Better isolation
- Improved portability

______________________________________________________________________

# Create a Volume

```bash id="docker611"
docker volume create postgres-data
```

List volumes

```bash id="docker612"
docker volume ls
```

Example

```text id="docker613"
postgres-data
```

______________________________________________________________________

# Mount a Volume

Suppose

PostgreSQL stores data in

```text id="docker614"
/var/lib/postgresql/data
```

Run

```bash id="docker615"
docker run \

-v postgres-data:/var/lib/postgresql/data \

postgres
```

Meaning

```text id="docker616"
Docker Volume

↓

Container Directory
```

______________________________________________________________________

# Visualizing It

```text id="docker617"
            PostgreSQL Container

                     │

                     ▼

        /var/lib/postgresql/data

                     │

                     ▼

             Docker Volume

                     │

                     ▼

               Host Storage
```

Data now survives container removal.

______________________________________________________________________

# Demonstration

Step 1

Start PostgreSQL.

```bash id="docker618"
docker run \

--name my-postgres \

-v postgres-data:/var/lib/postgresql/data \

postgres
```

Step 2

Insert data.

Step 3

Remove the container.

```bash id="docker619"
docker rm my-postgres
```

Step 4

Create a new container

using the same volume.

```bash id="docker620"
docker run \

-v postgres-data:/var/lib/postgresql/data \

postgres
```

All data is still there.

______________________________________________________________________

# Named Volumes

Example

```text id="docker621"
postgres-data
```

Advantages

- Managed by Docker
- Easy to reuse
- Easy to back up
- Platform-independent

This is the recommended approach for most database containers.

______________________________________________________________________

# Bind Mounts

Instead of a Docker-managed volume,

use a directory from your computer.

Example

```bash id="docker622"
docker run \

-v $(pwd):/app \

python-app
```

Meaning

```text id="docker623"
Current Folder

↓

Container

/app
```

Changes are immediately visible on both sides.

> **Note:** On Windows, the syntax differs (for example, using PowerShell variables or absolute paths).

______________________________________________________________________

# Named Volume vs Bind Mount

Named Volume

```text id="docker624"
Docker

↓

Manages Storage
```

Bind Mount

```text id="docker625"
You

↓

Choose Directory
```

______________________________________________________________________

# When to Use Each?

| Use Case | Recommended |
| ----------------------------- | ------------------ |
| PostgreSQL Data | Named Volume |
| Redis Persistence | Named Volume |
| Kafka Data | Named Volume |
| Local Development Source Code | Bind Mount |
| Configuration Files | Usually Bind Mount |

______________________________________________________________________

# Anonymous Volumes

Docker can also create

anonymous volumes.

Example

```bash id="docker626"
docker run \

-v /app/data \

python-app
```

Docker creates

a volume

with a generated name.

Usually,

named volumes are easier to manage.

______________________________________________________________________

# Inspecting Volumes

```bash id="docker627"
docker volume inspect postgres-data
```

Shows

- Mount location
- Driver
- Metadata

Useful for troubleshooting.

______________________________________________________________________

# Removing Volumes

```bash id="docker628"
docker volume rm postgres-data
```

Warning

Removing a volume

deletes the stored data.

Be certain before doing this.

______________________________________________________________________

# Sharing Data

Two containers

can share

the same volume.

```text id="docker629"
Container A

↓

Volume

↑

Container B
```

This is useful in some scenarios, but for databases, it's generally recommended that only the database process writes to
its data directory.

______________________________________________________________________

# Example

FastAPI

writes uploads

↓

Shared Volume

↓

Nginx

serves uploads

This is a common pattern.

______________________________________________________________________

# Volumes vs Image Layers

Image Layers

↓

Read-only

Volume

↓

Persistent

Writable

Independent

______________________________________________________________________

# Why Not Store Data Inside Images?

Images are

```text id="docker630"
Immutable
```

Data changes

belong in

Volumes,

not images.

______________________________________________________________________

# Common Mistakes

### Database Without Volume

Removing the container

removes all database data.

______________________________________________________________________

### Using Bind Mounts in Production Without Planning

Bind mounts depend on the host filesystem layout.

Named volumes are often easier to manage in production.

______________________________________________________________________

### Deleting Volumes Accidentally

Containers can be recreated.

Volumes may contain critical data.

______________________________________________________________________

### Treating Volumes Like Backups

Volumes provide persistence,

not backup.

You still need a backup strategy.

______________________________________________________________________

# Best Practices

- Use named volumes for databases.
- Use bind mounts for local source code during development.
- Back up important volumes.
- Separate application code from persistent data.
- Never rely on the container's writable layer for important information.

______________________________________________________________________

# Hands-on Exercise

1. Create a Docker volume.
1. Start PostgreSQL using that volume.
1. Insert sample data.
1. Remove the container.
1. Start a new container using the same volume.
1. Verify the data still exists.
1. Inspect the volume.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should PostgreSQL data be stored in a Docker volume instead of inside the container?

A container's writable layer is ephemeral and is removed when the container is deleted. A Docker volume stores data
independently of the container, allowing database files to survive container recreation. This enables persistent
storage, easier backups, and safer upgrades while keeping containers disposable.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Container filesystems
- Why container storage is ephemeral
- Docker volumes
- Named volumes
- Bind mounts
- Anonymous volumes
- Volume mounting
- Volume inspection
- Data persistence
- Sharing volumes
- Best practices for persistent storage

In the next lecture, we'll learn about **Docker Networking**, including how containers communicate with each other and
how FastAPI connects to PostgreSQL, Redis, and Kafka inside Docker.

______________________________________________________________________

## Next File

[Docker Networking](7-docker-networking.md)
