# Database Replication

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand database replication, how it improves availability and scalability, different replication strategies, failover mechanisms, and how to answer replication questions in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

has

one database.

```
Application

↓

Database
```

Everything works well

until

millions of users

start accessing

the system.

Problems appear.

```
High Read Traffic

↓

High CPU

↓

Slow Queries

↓

Database Overloaded
```

Even worse,

if the database crashes,

the entire application

stops working.

How do we solve this?

```
Replication
```

______________________________________________________________________

# What Is Replication?

Replication means

creating

one or more

copies

of a database.

Instead of

```
Application

↓

Database
```

we get

```
          Primary Database
                │
        ┌───────┴────────┐
        ▼                ▼
   Replica A        Replica B
```

All replicas

contain

the same data.

______________________________________________________________________

# Why Do We Need Replication?

Replication provides

- High Availability
- Read Scaling
- Disaster Recovery
- Fault Tolerance
- Backup Options

______________________________________________________________________

# Primary-Replica Architecture

Most common architecture.

```
          Application
                │
         Write Requests
                │
                ▼
        Primary Database
                │
      Replication Process
                │
      ┌─────────┴─────────┐
      ▼                   ▼
 Replica A           Replica B
```

______________________________________________________________________

# Write Flow

All writes

go to

the Primary.

```
INSERT

UPDATE

DELETE

↓

Primary Database
```

Replicas

receive

the changes.

______________________________________________________________________

# Read Flow

Reads

can be distributed.

```
Application

↓

Load Balancer

↓

Replica A

↓

Replica B

↓

Replica C
```

Primary

is protected

from heavy

read traffic.

______________________________________________________________________

# Example

Without Replication

```
100,000 Reads/sec

↓

Primary Database
```

With Replication

```
Primary

↓

Replica A

↓

Replica B

↓

Replica C
```

Each replica

handles

part of the load.

______________________________________________________________________

# Synchronous Replication

Write flow

```
Application

↓

Primary

↓

Replica

↓

Acknowledgement

↓

Success
```

The write

completes

only after

replicas confirm.

______________________________________________________________________

# Advantages

- Strong consistency
- No data loss
- Every replica is up-to-date

______________________________________________________________________

# Disadvantages

- Higher latency
- Slower writes
- Network delays affect performance

______________________________________________________________________

# Asynchronous Replication

Write flow

```
Application

↓

Primary

↓

Success Returned

↓

Background Replication

↓

Replica
```

Application

doesn't wait

for replicas.

______________________________________________________________________

# Advantages

- Fast writes
- Lower latency
- Better throughput

______________________________________________________________________

# Disadvantages

If the primary

fails immediately,

recent writes

may not exist

on replicas.

Possible

data loss.

______________________________________________________________________

# Semi-Synchronous Replication

Hybrid approach.

```
Application

↓

Primary

↓

One Replica Confirms

↓

Success
```

Remaining replicas

update

later.

Good balance

between

performance

and

consistency.

______________________________________________________________________

# Replication Lag

One of the most common

interview questions.

Suppose

Primary

receives

a write.

```
UPDATE User

↓

Primary Updated
```

Replica

may receive

the update

a few milliseconds later.

This delay

is called

```
Replication Lag
```

______________________________________________________________________

# Why Replication Lag Matters

Suppose

a user

updates

their profile.

Immediately afterwards,

the application

reads

from

Replica A.

Replica

hasn't updated yet.

The user

sees

old data.

This is called

```
Stale Read
```

______________________________________________________________________

# Solutions

For critical reads

use

```
Read Your Writes
```

Meaning

after writing,

temporarily

read

from

the Primary.

______________________________________________________________________

# Read Scaling

Applications

can distribute

read requests.

Example

```
Application

↓

Read Load Balancer

↓

Replica 1

↓

Replica 2

↓

Replica 3
```

Huge improvement

for

read-heavy systems.

______________________________________________________________________

# High Availability

Suppose

the Primary

fails.

```
Primary

↓

Crash
```

Without replication

everything stops.

With replication

```
Replica

↓

Promoted

↓

New Primary
```

Application

continues working.

______________________________________________________________________

# Automatic Failover

Monitoring systems

detect

database failure.

Example

```
Primary Down

↓

Promote Replica

↓

Update Clients

↓

Continue
```

Downtime

is minimized.

______________________________________________________________________

# Manual Failover

Sometimes

administrators

promote

a replica

manually.

Slower,

but

simpler.

______________________________________________________________________

# Failover Architecture

```
Application

↓

Database Proxy

↓

Primary

↓

Replica A

↓

Replica B
```

If Primary fails

Proxy

redirects traffic

to

the new Primary.

______________________________________________________________________

# Read Replica Use Cases

Excellent for

- Analytics
- Reporting
- Dashboards
- Search
- Product Catalog
- User Profiles

Avoid

critical writes.

______________________________________________________________________

# Backup vs Replication

Many candidates

confuse them.

Replication

```
High Availability
```

Backup

```
Recover Deleted Data
```

If you accidentally

delete

all records,

replicas

also receive

the deletion.

Replication

is NOT

a backup.

______________________________________________________________________

# Geo Replication

Large companies

replicate

across regions.

Example

```
Mumbai

↓

Singapore

↓

Frankfurt

↓

Virginia
```

Benefits

- Disaster recovery
- Lower latency
- Regional availability

______________________________________________________________________

# Multi-Primary Replication

Instead of

one Primary,

multiple databases

accept writes.

```
Primary A

⇄

Primary B
```

Much more complex.

Challenges

- Conflict resolution
- Consistency
- Write conflicts

Used carefully.

______________________________________________________________________

# Single Primary vs Multi Primary

| Single Primary | Multi Primary |
|----------------|---------------|
| Simple | Complex |
| Easier consistency | Conflict handling required |
| One writer | Multiple writers |
| Most common | Specialized systems |

______________________________________________________________________

# Replication And CAP

Replication

introduces

trade-offs.

During network partitions,

systems

must balance

Consistency

Availability

Partition Tolerance.

We'll study

CAP Theorem

later.

______________________________________________________________________

# Cloud Examples

AWS RDS

supports

Read Replicas.

Aurora

supports

multiple replicas

with automatic failover.

Most cloud databases

provide

built-in replication.

______________________________________________________________________

# Replication Monitoring

Always monitor

- Replication lag
- Replica health
- Disk usage
- Network latency
- Query performance

Healthy replicas

are essential.

______________________________________________________________________

# Typical Architecture

```
Users

↓

Load Balancer

↓

Application

↓

Redis

↓

Primary Database

↓

Read Replicas
```

Reads

go

to replicas.

Writes

go

to the primary.

______________________________________________________________________

# Common Interview Questions

## Why not write directly to replicas?

Replicas

are intended

to copy data

from the primary.

Allowing writes

to replicas

creates

consistency problems

in a single-primary architecture.

______________________________________________________________________

## Does replication improve write performance?

No.

Replication

primarily improves

read scalability

and availability.

Write performance

is usually limited

by the primary database.

______________________________________________________________________

## What happens if the primary crashes?

A healthy replica

is promoted

to become

the new primary.

Applications

then write

to the new primary.

______________________________________________________________________

## Can replication prevent data loss?

It reduces risk,

but asynchronous replication

may still lose

recent writes

if the primary fails

before replicas

receive updates.

______________________________________________________________________

# Common Mistakes

## Thinking Replication Is Backup

It isn't.

Both copies

receive

the same deletes

and updates.

______________________________________________________________________

## Sending Writes To Read Replicas

Read replicas

are usually

read-only.

______________________________________________________________________

## Ignoring Replication Lag

Eventual consistency

can affect

user experience.

______________________________________________________________________

## Assuming Infinite Scaling

Replication

improves reads,

not unlimited writes.

______________________________________________________________________

# Best Practices

✅ Use replicas for read-heavy workloads.

✅ Monitor replication lag.

✅ Use automatic failover.

✅ Keep backups in addition to replication.

✅ Route critical reads to the primary when necessary.

______________________________________________________________________

# Interview Deep Dive

## Question

Why do applications use read replicas?

### Answer

Read replicas distribute read traffic away from the primary database, improving scalability and reducing load on the
primary while keeping write operations centralized.

______________________________________________________________________

## Question

What is replication lag?

### Answer

Replication lag is the delay between a write occurring on the primary database and that write becoming visible on one or
more replicas. During this period, replicas may return stale data.

______________________________________________________________________

## Question

What is the difference between replication and backup?

### Answer

Replication keeps multiple live copies of the database synchronized for high availability and read scaling. A backup is
a point-in-time copy used for disaster recovery or restoring deleted or corrupted data.

______________________________________________________________________

# Practice Exercise

For each application,

answer

1. Is replication required?
1. Would you use synchronous or asynchronous replication?
1. Where would reads go?
1. How would failover work?
1. Would replication lag be acceptable?

Applications

- Banking System
- WhatsApp
- Instagram
- Netflix
- Food Delivery
- Online Shopping
- URL Shortener
- Hospital Management System

Explain

your reasoning

based on

consistency,

availability,

and scalability.

______________________________________________________________________

# Summary

Database replication is a fundamental technique for building scalable and highly available systems.

It enables

- Read scaling
- High availability
- Automatic failover
- Geographic redundancy
- Fault tolerance

However,

it also introduces

replication lag,

consistency trade-offs,

and operational complexity.

Understanding when and how to use replication is a core skill for every backend engineer and a frequent topic in System
Design interviews.

______________________________________________________________________

# Next

[Database Sharding (Horizontal Partitioning)](13-database-sharding.md)
