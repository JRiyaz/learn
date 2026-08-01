# Docker - Part 7

# Docker Networking

______________________________________________________________________

# Introduction

In the previous lecture, we learned how Docker Volumes provide persistent storage.

Now let's answer another important question.

Suppose we have

- FastAPI
- PostgreSQL
- Redis
- Kafka

each running inside its own container.

How do they communicate?

```text id="docker701"
FastAPI

↓

PostgreSQL
```

or

```text id="docker702"
FastAPI

↓

Redis
```

or

```text id="docker703"
FastAPI

↓

Kafka
```

They're running in separate containers.

How do they find each other?

This is where Docker Networking comes in.

______________________________________________________________________

# What is Docker Networking?

Docker Networking allows containers to communicate securely.

Without networking

```text id="docker704"
Container A

×

Container B
```

No communication.

With networking

```text id="docker705"
Container A

⇄

Container B
```

Containers can exchange data.

______________________________________________________________________

# Real Example

Our future application

```text id="docker706"
                Docker Network

      ┌─────────────┬─────────────┬─────────────┐

      ▼             ▼             ▼             ▼

  FastAPI      PostgreSQL      Redis        Kafka
```

Every service belongs to

the same Docker network.

______________________________________________________________________

# Why Not Use localhost?

This is the most common beginner mistake.

Suppose

FastAPI

tries

```python id="docker707"
DATABASE_URL = (

    "postgresql://localhost:5432"

)
```

Inside the FastAPI container,

`localhost`

means

```text id="docker708"
FastAPI Container
```

NOT

```text id="docker709"
PostgreSQL Container
```

Every container has its own network namespace.

______________________________________________________________________

# Correct Way

Instead of

```text id="docker710"
localhost
```

Use

```text id="docker711"
postgres
```

Example

```python id="docker712"
DATABASE_URL = (

"postgresql://user:password@postgres:5432/library"

)
```

Where

```text id="docker713"
postgres
```

is the container or service name.

Docker's internal DNS resolves it automatically.

______________________________________________________________________

# Docker Network

Think of a Docker network as

a private LAN.

```text id="docker714"
FastAPI

↓

Docker Network

↓

PostgreSQL
```

Every container receives

an internal IP address.

______________________________________________________________________

# DNS Resolution

Instead of remembering

```text id="docker715"
172.18.0.4
```

Docker provides

automatic DNS.

```text id="docker716"
postgres

↓

172.18.0.4
```

The application only uses

the container name.

______________________________________________________________________

# Container Communication

Example

```text id="docker717"
FastAPI

↓

redis:6379

↓

Redis Container
```

Exactly like communicating with a remote server,

except everything stays inside Docker.

______________________________________________________________________

# Default Bridge Network

When Docker is installed,

it creates a default

```text id="docker718"
bridge
```

network.

Containers connected to the same user-defined bridge network can communicate with each other using container names.

For most multi-container applications, it's recommended to create your own bridge network rather than relying on the
default one.

______________________________________________________________________

# Creating a Network

```bash id="docker719"
docker network create backend-network
```

List networks

```bash id="docker720"
docker network ls
```

Example

```text id="docker721"
bridge

host

none

backend-network
```

______________________________________________________________________

# Running Containers

PostgreSQL

```bash id="docker722"
docker run \

--network backend-network \

--name postgres \

postgres
```

Redis

```bash id="docker723"
docker run \

--network backend-network \

--name redis \

redis
```

FastAPI

```bash id="docker724"
docker run \

--network backend-network \

--name api \

fastapi-app
```

Now

all three

can communicate.

______________________________________________________________________

# Architecture

```text id="docker725"
           backend-network

      ┌──────────┬──────────┐

      ▼          ▼          ▼

   api       postgres     redis
```

______________________________________________________________________

# Network Drivers

Docker supports

```text id="docker726"
Bridge

Host

None

Overlay

Macvlan
```

We'll focus on the most common ones.

______________________________________________________________________

# Bridge Network

Most commonly used.

```text id="docker727"
Container

↓

Bridge

↓

Container
```

Ideal for

single-machine applications.

______________________________________________________________________

# Host Network

Instead of isolated networking,

the container shares the host's network stack.

```text id="docker728"
Container

↓

Host Network
```

Characteristics:

- No network isolation
- No Docker NAT
- Container ports are the host ports

Primarily available on Linux.

Use only when appropriate.

______________________________________________________________________

# None Network

```text id="docker729"
Container

↓

No Network
```

Useful for specialized workloads that don't require network access.

______________________________________________________________________

# Overlay Network

Used across multiple Docker hosts.

```text id="docker730"
Server A

↓

Overlay

↓

Server B
```

This is commonly used with Docker Swarm and other clustered environments.

We'll revisit similar concepts when learning Kubernetes.

______________________________________________________________________

# Macvlan Network

Containers receive IP addresses from the physical network.

```text id="docker731"
Router

↓

Container
```

Useful for specialized networking scenarios where containers need to appear as physical devices on the network.

______________________________________________________________________

# Port Mapping

Suppose

FastAPI listens on

```text id="docker732"
8000
```

Inside the container.

To access it from your host,

run

```bash id="docker733"
docker run \

-p 8000:8000 \

fastapi-app
```

Meaning

```text id="docker734"
Host

8000

↓

Container

8000
```

General format

```text id="docker735"
HostPort:ContainerPort
```

______________________________________________________________________

# Another Example

PostgreSQL

```bash id="docker736"
docker run \

-p 5432:5432 \

postgres
```

Redis

```bash id="docker737"
docker run \

-p 6379:6379 \

redis
```

Kafka

```bash id="docker738"
docker run \

-p 9092:9092 \

kafka
```

______________________________________________________________________

# Internal vs External Communication

Containers

inside the network

should use

```text id="docker739"
postgres

redis

kafka
```

Host machine

uses

```text id="docker740"
localhost

mapped ports
```

This distinction is important.

______________________________________________________________________

# Inspect Network

```bash id="docker741"
docker network inspect backend-network
```

Displays

- Connected containers
- Network ID
- Subnet
- Gateway
- IP addresses

Useful for debugging.

______________________________________________________________________

# Common Mistakes

### Using localhost Between Containers

Each container has its own localhost.

Use the container or service name instead.

______________________________________________________________________

### Forgetting Port Mapping

Without `-p`,

the application isn't accessible from the host.

Containers on the same Docker network can still communicate internally without published ports.

______________________________________________________________________

### Exposing Every Service

PostgreSQL and Redis often don't need to be exposed to the outside world.

Only expose services that must be accessed externally.

______________________________________________________________________

### Putting Everything on the Default Network

Create a dedicated network for each application stack.

It improves organization and isolation.

______________________________________________________________________

# Best Practices

- Use user-defined bridge networks.
- Communicate using container names.
- Expose only required ports.
- Keep databases on internal networks whenever possible.
- Use separate networks for unrelated applications.

______________________________________________________________________

# Hands-on Exercise

1. Create a Docker network.
1. Start PostgreSQL on that network.
1. Start Redis on that network.
1. Start a FastAPI container on the same network.
1. Configure FastAPI to connect to PostgreSQL using the container name.
1. Inspect the network.
1. Verify that the containers can communicate.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why shouldn't one Docker container connect to another using `localhost`?

Inside a container, `localhost` refers only to that container itself. Every container has its own isolated network
namespace. To communicate with another container, applications should use the other container's name (or service name in
Docker Compose), which Docker resolves automatically using its internal DNS.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Docker networking
- Container communication
- Docker DNS
- Container names
- Bridge networks
- Host networks
- None networks
- Overlay networks
- Macvlan networks
- Port mapping
- Internal vs external communication
- Network inspection
- Networking best practices

In the next lecture, we'll learn about **Environment Variables & Secrets**, including configuration management, runtime
configuration, and why sensitive information should never be hardcoded into Docker images.

______________________________________________________________________

## Next File

[Environment Variables & Secrets](8-environment-variables-and-secrets.md)
