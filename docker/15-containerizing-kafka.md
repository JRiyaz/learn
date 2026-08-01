# Docker - Part 15

# Containerizing Kafka (KRaft Mode)

______________________________________________________________________

# Introduction

In the previous chapter, we containerized Redis.

Now we'll containerize **Apache Kafka**.

Unlike PostgreSQL or Redis,

Kafka is a **distributed event streaming platform**.

Kafka introduces concepts like:

- Brokers
- Topics
- Producers
- Consumers
- Partitions

We've already learned these concepts in the Kafka module.

Our goal here is to learn **how to run Kafka inside Docker** using production-friendly practices.

We'll use **KRaft mode**, which is the modern architecture introduced to remove the dependency on ZooKeeper.

______________________________________________________________________

# Why Containerize Kafka?

Without Docker

```text id="kafka001"
Install Java

↓

Install Kafka

↓

Configure Broker

↓

Configure Controller

↓

Start Kafka
```

A lengthy setup.

______________________________________________________________________

With Docker

```text id="kafka002"
docker compose up
```

Kafka starts automatically.

______________________________________________________________________

# Kafka Architecture

Even in a simple setup,

Kafka has multiple components.

```text id="kafka003"
Producer

↓

Kafka Broker

↓

Topic

↓

Consumer
```

Inside Docker,

our FastAPI application communicates with the Kafka broker.

______________________________________________________________________

# KRaft Mode

Older Kafka versions required

```text id="kafka004"
ZooKeeper
```

Modern Kafka

supports

```text id="kafka005"
KRaft
```

where Kafka manages its own metadata.

Advantages

- Simpler deployment
- Fewer containers
- Easier maintenance
- Recommended for new deployments

______________________________________________________________________

# Choosing an Image

Several Kafka images exist.

Examples

```text id="kafka006"
apache/kafka

bitnami/kafka

confluentinc/cp-kafka
```

For learning,

we'll use

```text id="kafka007"
apache/kafka
```

because it closely follows the Apache project.

______________________________________________________________________

# Basic Compose Configuration

```yaml id="kafka008"
services:

  kafka:

    image: apache/kafka:latest
```

We'll expand this configuration.

______________________________________________________________________

# Required Environment Variables

Kafka needs some configuration.

```yaml id="kafka009"
environment:

  KAFKA_NODE_ID: 1

  KAFKA_PROCESS_ROLES: broker,controller

  KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
```

These variables configure the broker for KRaft mode.

______________________________________________________________________

# Listeners

One of Kafka's most important concepts.

```text id="kafka010"
Producer

↓

Listener

↓

Broker

↓

Listener

↓

Consumer
```

Listeners tell Kafka

where clients connect.

______________________________________________________________________

# Example Configuration

```yaml id="kafka011"
environment:

  KAFKA_LISTENERS: >

    PLAINTEXT://:9092,

    CONTROLLER://:9093
```

Meaning

```text id="kafka012"
9092

↓

Client Connections

9093

↓

Controller Communication
```

______________________________________________________________________

# Advertised Listeners

Kafka clients don't just connect.

The broker also tells clients

how to reach it.

Example

```yaml id="kafka013"
environment:

  KAFKA_ADVERTISED_LISTENERS: >

    PLAINTEXT://kafka:9092
```

Notice

```text id="kafka014"
kafka
```

is the Docker service name.

This is critical.

______________________________________________________________________

# Why Not localhost?

Suppose

FastAPI

tries

```python id="kafka015"
bootstrap_servers=[

    "localhost:9092"

]
```

Inside the FastAPI container,

`localhost`

means

the FastAPI container itself,

not

the Kafka container.

Use

```text id="kafka016"
kafka:9092
```

instead.

______________________________________________________________________

# Docker Volume

Kafka stores

logs

on disk.

Use a volume.

```yaml id="kafka017"
services:

  kafka:

    volumes:

      - kafka-data:/var/lib/kafka/data

volumes:

  kafka-data:
```

This preserves broker data

between container recreations.

______________________________________________________________________

# Health Check

Kafka doesn't have

a single universal health endpoint.

One simple approach

is checking whether the broker accepts client connections.

Example

```yaml id="kafka018"
healthcheck:

  test:

    [

      "CMD-SHELL",

      "nc -z localhost 9092"

    ]

  interval: 15s

  timeout: 5s

  retries: 5
```

> Depending on the Kafka image, utilities such as `nc` may not be installed. In production, health checks are often implemented using Kafka CLI tools or application-specific readiness checks.

______________________________________________________________________

# Complete Compose Example

```yaml id="kafka019"
services:

  kafka:

    image: apache/kafka:latest

    ports:

      - "9092:9092"

    environment:

      KAFKA_NODE_ID: 1

      KAFKA_PROCESS_ROLES: broker,controller

      KAFKA_LISTENERS: >

        PLAINTEXT://:9092,

        CONTROLLER://:9093

      KAFKA_ADVERTISED_LISTENERS: >

        PLAINTEXT://kafka:9092

      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

    volumes:

      - kafka-data:/var/lib/kafka/data

volumes:

  kafka-data:
```

For a real production deployment, additional KRaft settings are required (such as controller quorum voters and cluster
ID), but this example focuses on the core concepts.

______________________________________________________________________

# FastAPI Producer

```python id="kafka020"
from kafka import KafkaProducer

producer = KafkaProducer(

    bootstrap_servers=[

        "kafka:9092"

    ]

)
```

No Docker-specific code

other than the hostname.

______________________________________________________________________

# FastAPI Consumer

```python id="kafka021"
from kafka import KafkaConsumer

consumer = KafkaConsumer(

    "orders",

    bootstrap_servers=[

        "kafka:9092"

    ]

)
```

Exactly the same.

______________________________________________________________________

# Environment Variables

Instead of hardcoding,

```python id="kafka022"
import os

KAFKA_BROKER = os.getenv(
    "KAFKA_BROKER"
)
```

Compose

```yaml id="kafka023"
environment:

  KAFKA_BROKER: kafka:9092
```

______________________________________________________________________

# Logs

View logs.

```bash id="kafka024"
docker logs kafka
```

Useful for

- Startup
- Topic creation
- Listener configuration
- Connection failures

______________________________________________________________________

# Inspect Container

```bash id="kafka025"
docker inspect kafka
```

Shows

- Networks
- Volumes
- Environment
- Ports
- Health status

______________________________________________________________________

# Real Backend Architecture

```text id="kafka026"
               Docker Compose

                      │

      ┌───────────────┼───────────────┐

      ▼               ▼               ▼

   FastAPI       PostgreSQL       Redis

                      │

                      ▼

                    Kafka
```

FastAPI

publishes events

to

```text id="kafka027"
kafka:9092
```

______________________________________________________________________

# Common Mistakes

### Using localhost

Inside Docker,

use

```text id="kafka028"
kafka:9092
```

instead.

______________________________________________________________________

### Forgetting Advertised Listeners

Kafka clients

won't know

how to reconnect

correctly.

This is one of the most common Kafka configuration issues.

______________________________________________________________________

### No Persistent Volume

Broker logs

may be lost

after container recreation.

______________________________________________________________________

### Using latest

Pin versions

for predictable deployments.

______________________________________________________________________

### Ignoring KRaft Configuration

Modern Kafka deployments

should prefer

KRaft

instead of ZooKeeper

unless maintaining an existing deployment.

______________________________________________________________________

# Best Practices

- Use KRaft mode for new deployments.
- Pin Kafka versions.
- Configure advertised listeners correctly.
- Use Docker volumes.
- Keep broker configuration in environment variables.
- Use service names for networking.
- Add health checks where appropriate.

______________________________________________________________________

# Hands-on Exercise

1. Create a Kafka service in Docker Compose.
1. Configure KRaft mode.
1. Add a Docker volume.
1. Create a producer.
1. Create a consumer.
1. Publish a message.
1. Consume the message.
1. Verify communication with FastAPI.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is `KAFKA_ADVERTISED_LISTENERS` important when Kafka runs inside Docker?

After a client connects to a Kafka broker, the broker tells the client how to reach it for future communication.
`KAFKA_ADVERTISED_LISTENERS` defines those advertised addresses. If it is configured incorrectly—for example,
advertising `localhost` inside Docker—other containers won't be able to communicate with the broker. Using the Docker
service name, such as `kafka:9092`, ensures clients inside the Docker network can connect successfully.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Running Kafka in Docker
- KRaft mode
- Kafka listeners
- Advertised listeners
- Docker volumes
- Producer configuration
- Consumer configuration
- Environment variables
- Health checks
- Kafka Docker best practices

You've now containerized every major component we've built:

- FastAPI
- PostgreSQL
- Redis
- Kafka

In the next chapter, we'll learn **Docker Debugging & Troubleshooting**, where you'll diagnose real-world container
failures, networking issues, startup problems, and performance bottlenecks like a production engineer.

______________________________________________________________________

## Next File

[Docker Debugging & Troubleshooting](16-docker-debugging-and-troubleshooting.md)
