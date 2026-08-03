# System Design - Part 92

# Global Scale Architecture System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Global Architecture is needed
- Single Region vs Multi Region
- Active-Active
- Active-Passive
- Global Load Balancing
- Geo DNS
- Data Replication
- Disaster Recovery
- CAP Theorem in Practice
- Consistency Models
- Multi-Region Databases
- Scaling Strategies
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a globally distributed application like Google, Netflix, Amazon, or ChatGPT.**

This is the final topic

because

it combines

everything

you have learned.

Large systems

don't run

inside

one data center.

They run

across

continents.

______________________________________________________________________

# Why Multiple Regions?

Suppose

your application

runs only

in

India.

Users

from

USA

experience

high latency.

If

the India region

fails,

the application

goes offline.

Multiple regions

solve

both problems.

______________________________________________________________________

# Single Region

```text id="gs9201"
Users

↓

India Region

↓

Database
```

Problems

- High latency
- Single point of failure
- Disaster recovery difficult

______________________________________________________________________

# Multi Region

```text id="gs9202"
Users

↓

USA

Europe

India

↓

Regional Databases
```

Benefits

- Lower latency
- High availability
- Disaster recovery
- Regulatory compliance

______________________________________________________________________

# Global Architecture

```text id="gs9203"
Users

↓

Geo DNS

↓

Global Load Balancer

↓

Nearest Region

↓

Regional Services
```

______________________________________________________________________

# Geo DNS

Interview favorite.

Geo DNS

routes users

to

the nearest

healthy region.

Example

```text id="gs9204"
India User

↓

Mumbai Region
```

```text id="gs9205"
US User

↓

Virginia Region
```

Benefits

- Lower latency
- Better availability

______________________________________________________________________

# Global Load Balancer

Interview favorite.

Unlike

a normal

load balancer,

this chooses

between

regions.

Example

```text id="gs9206"
Global LB

↓

US-East

Europe

Asia
```

Selection

depends on:

- Latency
- Health
- Capacity
- Geography

______________________________________________________________________

# Active-Passive

Interview favorite.

Only

one region

serves traffic.

```text id="gs9207"
Primary

↓

Secondary (Standby)
```

If

Primary fails,

traffic

moves

to

Secondary.

Advantages

- Simpler
- Strong consistency

Disadvantages

- Secondary resources remain idle
- Slower failover

______________________________________________________________________

# Active-Active

Interview favorite.

Every region

serves traffic.

```text id="gs9208"
US

↓

Users
```

```text id="gs9209"
Europe

↓

Users
```

```text id="gs9210"
Asia

↓

Users
```

Advantages

- Better latency
- Better utilization
- Higher availability

Disadvantages

- More complex replication
- Conflict resolution

______________________________________________________________________

# Data Replication

Interview favorite.

Data

must be

replicated

between

regions.

```text id="gs9211"
India

↔

Europe

↔

USA
```

Replication

may be

- Synchronous
- Asynchronous

______________________________________________________________________

# Synchronous Replication

Write

is complete

only after

all replicas

acknowledge.

Benefits

- Strong consistency

Disadvantages

- Higher latency

______________________________________________________________________

# Asynchronous Replication

Write

completes

locally.

Replication

occurs later.

Benefits

- Lower latency

Disadvantages

- Eventual consistency

______________________________________________________________________

# CAP Theorem

Interview favorite.

During

a network partition,

a distributed system

can guarantee

only two

of the following:

- Consistency (C)
- Availability (A)
- Partition Tolerance (P)

Since

network partitions

cannot be eliminated,

systems

typically choose

between:

- CP
- AP

depending

on business needs.

______________________________________________________________________

# Conflict Resolution

Interview favorite.

Suppose

the same profile

is edited

in

two regions.

Possible strategies:

- Last Write Wins
- Version Vectors
- CRDTs
- Manual resolution

Choose

based on

business requirements.

______________________________________________________________________

# Read Local

Common optimization.

```text id="gs9212"
Read

↓

Nearest Region
```

Reads

stay local,

reducing latency.

______________________________________________________________________

# Write Local

Possible architecture.

```text id="gs9213"
Write

↓

Nearest Region

↓

Replication
```

Useful

for

social media

and

collaborative systems.

______________________________________________________________________

# Multi-Primary Database

Interview favorite.

Every region

accepts writes.

```text id="gs9214"
US

↔

Europe

↔

Asia
```

Requires

conflict resolution.

Examples

include:

- Google Spanner
- CockroachDB
- YugabyteDB

______________________________________________________________________

# Primary-Replica Database

Only

one region

accepts writes.

Others

serve reads.

```text id="gs9215"
Primary

↓

Replica

↓

Replica
```

Simpler,

but

writes

travel

to

the primary.

______________________________________________________________________

# Disaster Recovery (DR)

Interview favorite.

Suppose

an entire region

fails.

```text id="gs9216"
Mumbai

↓

Offline
```

Geo DNS

routes traffic

to

another region.

Services

continue

operating.

______________________________________________________________________

# RTO & RPO

Interview favorite.

## RTO

Recovery Time Objective

How long

until

the service

is restored.

Example

```text id="gs9217"
5 Minutes
```

______________________________________________________________________

## RPO

Recovery Point Objective

Maximum

acceptable

data loss.

Example

```text id="gs9218"
30 Seconds
```

______________________________________________________________________

# CDN Integration

Static content

should not

come

from

application servers.

Workflow

```text id="gs9219"
Users

↓

CDN Edge

↓

Origin Region
```

Benefits

- Lower latency
- Reduced backend traffic

______________________________________________________________________

# Regional Caches

Every region

has

its own

Redis cluster.

```text id="gs9220"
India

↓

Redis
```

```text id="gs9221"
USA

↓

Redis
```

Avoid

cross-region

cache lookups.

______________________________________________________________________

# Message Replication

Kafka

may operate

across

multiple regions.

```text id="gs9222"
Region A

↓

Mirror

↓

Region B
```

Useful

for

analytics

and

disaster recovery.

______________________________________________________________________

# Monitoring

Monitor

each region

independently.

Key metrics:

- Latency
- Error Rate
- Throughput
- Replication Lag
- CPU
- Memory
- Regional Health

______________________________________________________________________

# Failure Scenario

Suppose

Europe

goes offline.

Workflow

```text id="gs9223"
Europe

↓

Unavailable

↓

Geo DNS

↓

USA
```

Users

are redirected

automatically.

______________________________________________________________________

# Another Failure

Suppose

cross-region replication

stops.

Each region

continues

serving traffic.

Replication

catches up

when

connectivity

is restored.

This may result

in

temporary

eventual consistency.

______________________________________________________________________

# End-to-End Architecture

```text id="gs9224"
Users

↓

Geo DNS

↓

Global Load Balancer

↓

Regional API Gateway

↓

Regional Services

↓

Regional Redis

↓

Regional Database

↕

Cross-Region Replication

↓

Kafka Mirror

↓

Object Storage

↓

CDN
```

______________________________________________________________________

# Trade-offs

Active-Active

vs

Active-Passive

| Active-Active | Active-Passive |
| ------------------- | ------------------------ |
| Better latency | Simpler |
| Higher availability | Easier consistency |
| Conflict resolution | Faster recovery planning |

______________________________________________________________________

Synchronous

vs

Asynchronous Replication

| Synchronous | Asynchronous |
| -------------------- | ------------------------ |
| Strong consistency | Lower latency |
| Higher write latency | Eventual consistency |
| Less data loss | Possible replication lag |

______________________________________________________________________

Primary-Replica

vs

Multi-Primary

| Primary-Replica | Multi-Primary |
| ------------------ | -------------------------- |
| Simpler | More scalable |
| Centralized writes | Regional writes |
| Easier consistency | Conflict handling required |

______________________________________________________________________

# Best Practices

✅ Deploy across multiple regions.

✅ Keep reads local whenever possible.

✅ Replicate data asynchronously unless strong consistency is required.

✅ Define RTO and RPO targets.

✅ Continuously test disaster recovery procedures.

✅ Design applications to tolerate regional failures.

______________________________________________________________________

# Common Mistakes

### Treating Multi-Region as Multi-AZ

Availability Zones

protect

against

data center failures.

Regions

protect

against

large-scale disasters.

They solve

different problems.

______________________________________________________________________

### Cross-Region Database Calls

Applications

should avoid

making

database requests

across continents.

Keep

application

and

database

in

the same region.

______________________________________________________________________

### Assuming Zero Data Loss

Without

synchronous replication,

some data

may be lost

during

a regional disaster.

Design

according

to

acceptable RPO.

______________________________________________________________________

### Ignoring Replication Lag

Applications

must tolerate

temporary differences

between regions

when

using

asynchronous replication.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a globally distributed application?

Deploy the application across multiple geographic regions and use Geo DNS or a global load balancer to route users to
the nearest healthy region. Keep application services, caches, and databases local to each region to minimize latency.
Replicate data between regions using synchronous replication when strong consistency is required or asynchronous
replication when low latency is more important. Choose between Active-Passive and Active-Active deployments based on
business requirements, define clear RTO and RPO objectives for disaster recovery, and design applications to handle
regional failures, replication lag, and conflict resolution gracefully. Serve static content through a CDN and
continuously monitor regional health, latency, and replication status.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Multi-region architecture
- Geo DNS
- Global Load Balancer
- Active-Active
- Active-Passive
- CAP Theorem
- Replication
- Disaster Recovery
- RTO & RPO
- Conflict resolution
- Global scaling
- Trade-offs

______________________________________________________________________

# 🎉 Congratulations!

You have completed the **Complete System Design Course**.

You now understand:

## Foundation

- Requirements gathering
- Capacity estimation
- Databases
- Caching
- Load balancing
- CDNs
- Messaging
- Microservices

## Real Systems

- TinyURL
- WhatsApp
- Instagram
- Twitter/X
- YouTube
- Netflix
- Spotify
- Google Drive
- Uber
- Amazon
- Payment Gateway
- Notification Service
- ChatGPT
- RAG

## Infrastructure

- Kafka
- Redis
- Nginx
- Elasticsearch

## Advanced Distributed Systems

- Distributed Locking
- Distributed Transactions
- CQRS & Event Sourcing
- Global Scale Architecture

By mastering these topics, you'll be prepared for the vast majority of senior backend and system design interviews,
while also building a strong foundation for architecting large-scale AI and distributed systems.

______________________________________________________________________

# 🎯 Suggested Next Learning Path

After completing System Design, the next high-impact topics are:

1. Low-Level Design (LLD) & Design Patterns
1. Kubernetes (dedicated course)
1. Cloud Architecture (AWS/GCP/Azure)
1. Database Internals (PostgreSQL, MySQL)
1. Operating Systems & Networking
1. Distributed Consensus (Raft, Paxos)
1. AI Infrastructure (Model Serving, Distributed Training, Vector Search)

These will take you from being a strong backend engineer to a well-rounded systems architect and AI platform engineer.
