# Kafka Docker Setup Guide

## Single Broker and 3 Broker KRaft Cluster

______________________________________________________________________

# Table of Contents

1. Kafka Docker Overview
1. Single Broker Kafka Setup
1. Single Broker Commands
1. Three Broker Kafka Cluster Setup
1. Cluster Commands
1. Replication Testing
1. Broker Failure Testing
1. Single Broker vs Cluster Comparison

______________________________________________________________________

# 1. Kafka Docker Overview

Kafka can be run in two common ways:

## Development Setup

Single broker:

```
Kafka

+----------------+
|                |
| Broker 1       |
|                |
| Controller     |
|                |
+----------------+
```

Characteristics:

- One Kafka process
- No fault tolerance
- Replication factor = 1
- Good for learning

______________________________________________________________________

## Production-like Setup

Three broker cluster:

```
                 Kafka Cluster


+-------------+-------------+-------------+
|             |             |             |
| Broker 1    | Broker 2    | Broker 3    |
|             |             |             |
| Controller  | Controller  | Controller  |
|             |             |             |
+-------------+-------------+-------------+


KRaft Controller Quorum
```

Characteristics:

- Multiple brokers
- Data replication
- Leader election
- Fault tolerance

______________________________________________________________________

# 2. Single Broker Kafka Setup

## Folder Structure

Create:

```
kafka-single/

├── docker-compose.yml
└── data/
```

______________________________________________________________________

# docker-compose.yml

```yaml
version: "3.8"

services:

  kafka:

    image: apache/kafka:latest

    container_name: kafka

    ports:
      - "9092:9092"


    environment:


      # Node ID

      KAFKA_NODE_ID: 1


      # KRaft mode

      KAFKA_PROCESS_ROLES: broker,controller


      # Controller quorum

      KAFKA_CONTROLLER_QUORUM_VOTERS:
        1@kafka:9093


      # Listeners

      KAFKA_LISTENERS:
        PLAINTEXT://:9092,CONTROLLER://:9093


      KAFKA_ADVERTISED_LISTENERS:
        PLAINTEXT://localhost:9092


      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:
        CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT


      KAFKA_CONTROLLER_LISTENER_NAMES:
        CONTROLLER



      # Single broker replication

      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1


      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1


      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1



      # Topic defaults

      KAFKA_NUM_PARTITIONS: 3


      KAFKA_DEFAULT_REPLICATION_FACTOR: 1



      # Durability

      KAFKA_MIN_INSYNC_REPLICAS: 1



    volumes:

      - ./data:/var/lib/kafka/data
```

______________________________________________________________________

# Start Single Kafka

Run:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

Expected:

```
kafka
```

______________________________________________________________________

# Enter Kafka Container

```bash
docker exec -it kafka bash
```

______________________________________________________________________

# Create Topic

```bash
/opt/kafka/bin/kafka-topics.sh \
--create \
--topic orders \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1
```

______________________________________________________________________

# List Topics

```bash
/opt/kafka/bin/kafka-topics.sh \
--list \
--bootstrap-server localhost:9092
```

______________________________________________________________________

# Describe Topic

```bash
/opt/kafka/bin/kafka-topics.sh \
--describe \
--topic orders \
--bootstrap-server localhost:9092
```

Example:

```
Topic: orders


Partition 0

Leader: 1


Partition 1

Leader: 1


Partition 2

Leader: 1
```

______________________________________________________________________

# 3. Three Broker Kafka Cluster Setup

Architecture:

```
                    Kafka Cluster


        +-------------+-------------+-------------+
        |             |             |             |
        | Broker 1    | Broker 2    | Broker 3    |
        |             |             |             |
        |Controller   |Controller   |Controller   |
        |             |             |             |
        +-------------+-------------+-------------+


              KRaft Controller Quorum
```

______________________________________________________________________

# Folder Structure

Create:

```
kafka-cluster/

├── docker-compose.yml

├── broker1-data/

├── broker2-data/

└── broker3-data/
```

______________________________________________________________________

# docker-compose.yml

```yaml
version: "3.8"


services:


  kafka1:

    image: apache/kafka:latest

    container_name: kafka1


    ports:

      - "9092:9092"


    environment:


      KAFKA_NODE_ID: 1


      KAFKA_PROCESS_ROLES: broker,controller


      KAFKA_CONTROLLER_QUORUM_VOTERS:

        1@kafka1:9093,
        2@kafka2:9093,
        3@kafka3:9093



      KAFKA_LISTENERS:

        PLAINTEXT://:9092,CONTROLLER://:9093



      KAFKA_ADVERTISED_LISTENERS:

        PLAINTEXT://localhost:9092



      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:

        CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT



      KAFKA_CONTROLLER_LISTENER_NAMES:

        CONTROLLER



      KAFKA_INTER_BROKER_LISTENER_NAME:

        PLAINTEXT



      KAFKA_DEFAULT_REPLICATION_FACTOR: 3


      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2


      KAFKA_MIN_INSYNC_REPLICAS: 2


      KAFKA_NUM_PARTITIONS: 6



    volumes:

      - ./broker1-data:/var/lib/kafka/data




  kafka2:


    image: apache/kafka:latest

    container_name: kafka2


    ports:

      - "9094:9092"


    environment:


      KAFKA_NODE_ID: 2


      KAFKA_PROCESS_ROLES: broker,controller


      KAFKA_CONTROLLER_QUORUM_VOTERS:

        1@kafka1:9093,
        2@kafka2:9093,
        3@kafka3:9093



      KAFKA_LISTENERS:

        PLAINTEXT://:9092,CONTROLLER://:9093



      KAFKA_ADVERTISED_LISTENERS:

        PLAINTEXT://localhost:9094



      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:

        CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT



      KAFKA_CONTROLLER_LISTENER_NAMES:

        CONTROLLER



      KAFKA_INTER_BROKER_LISTENER_NAME:

        PLAINTEXT



      KAFKA_DEFAULT_REPLICATION_FACTOR: 3


      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2


      KAFKA_MIN_INSYNC_REPLICAS: 2


      KAFKA_NUM_PARTITIONS: 6



    volumes:

      - ./broker2-data:/var/lib/kafka/data




  kafka3:


    image: apache/kafka:latest

    container_name: kafka3


    ports:

      - "9096:9092"


    environment:


      KAFKA_NODE_ID: 3


      KAFKA_PROCESS_ROLES: broker,controller


      KAFKA_CONTROLLER_QUORUM_VOTERS:

        1@kafka1:9093,
        2@kafka2:9093,
        3@kafka3:9093



      KAFKA_LISTENERS:

        PLAINTEXT://:9092,CONTROLLER://:9093



      KAFKA_ADVERTISED_LISTENERS:

        PLAINTEXT://localhost:9096



      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:

        CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT



      KAFKA_CONTROLLER_LISTENER_NAMES:

        CONTROLLER



      KAFKA_INTER_BROKER_LISTENER_NAME:

        PLAINTEXT



      KAFKA_DEFAULT_REPLICATION_FACTOR: 3


      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3


      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2


      KAFKA_MIN_INSYNC_REPLICAS: 2


      KAFKA_NUM_PARTITIONS: 6



    volumes:

      - ./broker3-data:/var/lib/kafka/data
```

______________________________________________________________________

# Start Cluster

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

Expected:

```
kafka1

kafka2

kafka3
```

______________________________________________________________________

# Create Replicated Topic

Connect:

```bash
docker exec -it kafka1 bash
```

Create topic:

```bash
/opt/kafka/bin/kafka-topics.sh \
--create \
--topic orders \
--bootstrap-server kafka1:9092 \
--partitions 3 \
--replication-factor 3
```

______________________________________________________________________

# Describe Topic

```bash
/opt/kafka/bin/kafka-topics.sh \
--describe \
--topic orders \
--bootstrap-server kafka1:9092
```

Example:

```
Partition 0

Leader: Broker 1

Replicas:

1,2,3



Partition 1

Leader: Broker 2

Replicas:

2,3,1



Partition 2

Leader: Broker 3

Replicas:

3,1,2
```

______________________________________________________________________

# 4. Test Producer

Enter container:

```bash
docker exec -it kafka1 bash
```

Run:

```bash
/opt/kafka/bin/kafka-console-producer.sh \
--topic orders \
--bootstrap-server kafka1:9092
```

Type:

```
order-1
order-2
order-3
```

______________________________________________________________________

# 5. Test Consumer

Open another terminal:

```bash
docker exec -it kafka1 bash
```

Run:

```bash
/opt/kafka/bin/kafka-console-consumer.sh \
--topic orders \
--bootstrap-server kafka1:9092 \
--from-beginning
```

______________________________________________________________________

# 6. Test Broker Failure

Stop broker1:

```bash
docker stop kafka1
```

Check:

```bash
docker exec -it kafka2 bash
```

Describe:

```bash
/opt/kafka/bin/kafka-topics.sh \
--describe \
--topic orders \
--bootstrap-server kafka2:9092
```

Kafka should show:

```
Old Leader:

Broker 1


New Leader:

Broker 2
```

______________________________________________________________________

# 7. Configuration Comparison

| Configuration | Single Broker | 3 Broker Cluster |
|---|---|---|
| brokers | 1 | 3 |
| replication factor | 1 | 3 |
| offsets replication | 1 | 3 |
| min ISR | 1 | 2 |
| fault tolerance | No | Yes |
| leader election | No practical failover | Yes |
| KRaft quorum | Single node | Three nodes |

______________________________________________________________________

# Recommended Learning Path

Run in this order:

1. Single broker
1. Create topics
1. Produce messages
1. Consume messages
1. Add partitions
1. Run 3 broker cluster
1. Test replication
1. Stop brokers
1. Observe leader election
1. Experiment with consumer groups

______________________________________________________________________

# End
