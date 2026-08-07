# Consistent Hashing

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand why Consistent Hashing is used in distributed systems, how it minimizes data movement, and how to confidently explain it in System Design interviews.

______________________________________________________________________

# Introduction

Suppose

your application

stores

millions of users.

You have

4 servers.

```
Application

↓

Server A

Server B

Server C

Server D
```

Everything works.

Then

traffic doubles.

You add

one more server.

```
Server E
```

Now,

where should

existing data go?

With normal hashing,

almost

everything

must move.

Very expensive.

Consistent Hashing

solves

this problem.

______________________________________________________________________

# The Problem With Normal Hashing

Normal hashing

uses

```
Hash(Key)

%

Number Of Servers
```

Example

```
Hash(User101)

↓

103

↓

103 % 4

↓

Server 3
```

Works well.

Until

you add

another server.

______________________________________________________________________

# Example

Initially

```
4 Servers
```

```
Hash(User101)

↓

103 % 4

↓

Server 3
```

After adding

Server E

```
103 % 5

↓

Server 4
```

Almost every key

gets assigned

to

a different server.

______________________________________________________________________

# Why Is This Bad?

Suppose

you have

```
100 Million Keys
```

Adding

one server

may require

moving

```
80–90%

of the data.
```

Extremely expensive.

______________________________________________________________________

# Consistent Hashing

Instead of

hashing

servers

into

a list,

we hash

both

servers

and

keys

onto

a circle.

This is called

```
Hash Ring
```

______________________________________________________________________

# Hash Ring

Imagine

a circle.

```
                0
             /     \
           /         \
        A              B
      /                  \
    D                      C
      \                  /
        \              /
            360°
```

Servers

are placed

around

the ring.

______________________________________________________________________

# Placing Keys

Now

hash

every key

onto

the same ring.

Example

```
User101

↓

Hash

↓

Between A and B
```

The key

belongs

to

the first server

clockwise.

______________________________________________________________________

# Rule

A key

is assigned

to

the first server

moving

clockwise.

Simple.

______________________________________________________________________

# Example

```
        User 1

           ↓

      A -------- B

      ↑          ↑

Server D      Server B
```

User1

belongs

to

Server B.

______________________________________________________________________

# Adding A New Server

Suppose

we add

```
Server E
```

Only

the keys

between

```
Server D

↓

Server E
```

move.

Everything else

remains

unchanged.

Huge improvement.

______________________________________________________________________

# Removing A Server

Suppose

Server B

fails.

Only

its keys

move

to

the next server.

Not

the entire system.

______________________________________________________________________

# Data Movement Comparison

Normal Hashing

```
Add One Server

↓

Move

Almost Everything
```

Consistent Hashing

```
Add One Server

↓

Move

Small Portion
```

This is

the biggest advantage.

______________________________________________________________________

# Why Is This Important?

Imagine

Redis Cluster,

Cassandra,

or

DynamoDB.

Servers

are frequently

added,

removed,

or replaced.

Without

Consistent Hashing,

every change

would require

massive data migration.

______________________________________________________________________

# Virtual Nodes

Interview favorite.

Suppose

Server A

is much more powerful

than

Server B.

One physical server

may appear

multiple times

on the ring.

Example

```
A1

A2

A3

A4
```

All represent

Server A.

These are called

```
Virtual Nodes

(VNodes)
```

______________________________________________________________________

# Why Virtual Nodes?

Without

virtual nodes,

servers

may receive

uneven traffic.

Example

```
Server A

80%

Server B

20%
```

Poor distribution.

______________________________________________________________________

# With Virtual Nodes

```
A1

B1

A2

C1

A3

D1

A4
```

Traffic

becomes

much more balanced.

______________________________________________________________________

# Load Distribution

Virtual nodes

improve

- Load balancing
- Fault tolerance
- Scalability
- Data distribution

Almost every

modern implementation

uses them.

______________________________________________________________________

# Failure Scenario

Suppose

Server C

fails.

Only

keys

assigned

to

Server C

move

to

the next server.

Everyone else

continues normally.

______________________________________________________________________

# Replication

Consistent Hashing

often works

together

with replication.

Example

```
Primary

↓

Next Two Nodes

↓

Replicas
```

If

one node fails,

replicas

already exist.

______________________________________________________________________

# Typical Architecture

```
Application

↓

Hash Ring

↓

Redis Nodes

↓

Replication
```

______________________________________________________________________

# Systems Using Consistent Hashing

Examples

- Cassandra
- DynamoDB
- Riak
- Redis Cluster
- Akamai
- Distributed Caches
- Distributed Object Storage

______________________________________________________________________

# Redis Cluster

Redis Cluster

uses

```
16,384

Hash Slots
```

instead of

a pure hash ring,

but

the goal

is similar—

efficiently distributing

data

across nodes

while minimizing

movement.

Interviewers

may appreciate

this distinction.

______________________________________________________________________

# Cassandra

Cassandra

uses

consistent hashing

to distribute

data

across

cluster nodes.

Adding

new nodes

requires

moving

only

a portion

of the data.

______________________________________________________________________

# DynamoDB

Amazon Dynamo

popularized

consistent hashing

for

highly available

distributed storage.

______________________________________________________________________

# Advantages

Consistent Hashing

provides

- Minimal data movement
- Easy horizontal scaling
- Better fault tolerance
- Balanced load
- High availability

______________________________________________________________________

# Disadvantages

Implementation

is more complex

than

simple hashing.

Requires

careful handling

of

- Virtual nodes
- Replication
- Rebalancing

______________________________________________________________________

# Common Interview Questions

## Why not use modulo hashing?

Because

adding

or removing

servers

causes

most keys

to be reassigned,

leading to

massive data movement.

______________________________________________________________________

## Why is a hash ring used?

The ring

allows

servers

to be added

or removed

while affecting

only

a small subset

of keys.

______________________________________________________________________

## What are Virtual Nodes?

Virtual nodes

allow

one physical server

to appear

multiple times

on the ring,

creating

more even

data distribution.

______________________________________________________________________

## Does Consistent Hashing eliminate rebalancing?

No.

Some rebalancing

still occurs,

but

far less

than

traditional hashing.

______________________________________________________________________

# Common Mistakes

## Thinking No Data Moves

Some data

always moves

when servers

change.

The goal

is to minimize

movement,

not eliminate it.

______________________________________________________________________

## Forgetting Virtual Nodes

Most production systems

use

virtual nodes.

______________________________________________________________________

## Confusing Replication With Consistent Hashing

Replication

creates copies.

Consistent Hashing

decides

where data lives.

______________________________________________________________________

## Assuming Every Distributed Database Uses A Ring

Different systems

implement

distribution differently.

Redis Cluster,

for example,

uses hash slots.

______________________________________________________________________

# Best Practices

✅ Use Consistent Hashing for distributed storage.

✅ Use virtual nodes for balanced distribution.

✅ Combine with replication.

✅ Plan for node failures.

✅ Monitor shard balance after scaling.

______________________________________________________________________

# Interview Deep Dive

## Question

What problem does Consistent Hashing solve?

### Answer

It minimizes data movement when servers are added or removed from a distributed system, allowing clusters to scale
efficiently without redistributing most of the stored data.

______________________________________________________________________

## Question

Why are virtual nodes important?

### Answer

Virtual nodes improve load balancing by distributing each physical server across multiple positions on the hash ring.
This reduces hotspots and results in a more even distribution of data.

______________________________________________________________________

## Question

Is Consistent Hashing the same as sharding?

### Answer

No. Sharding is the broader concept of splitting data across multiple databases or servers. Consistent Hashing is one
strategy for determining where that data should be stored while minimizing redistribution during scaling events.

______________________________________________________________________

# Practice Exercise

For each system,

answer

1. Would Consistent Hashing be useful?
1. Would virtual nodes improve distribution?
1. Would replication also be required?
1. What happens when a node fails?
1. How much data should move when a new node is added?

Systems

- Redis Cluster
- Cassandra
- Distributed Cache
- URL Shortener
- CDN Edge Nodes
- Object Storage
- Chat Application

Explain

your reasoning

using

scalability,

fault tolerance,

and

load balancing.

______________________________________________________________________

# Summary

Consistent Hashing is one of the key techniques that enables distributed systems to scale efficiently.

It

- Minimizes data movement
- Simplifies horizontal scaling
- Improves load balancing
- Supports fault tolerance
- Works well with replication

Understanding Consistent Hashing will help you explain how large-scale systems such as Redis clusters, Cassandra, and
distributed caches grow without expensive data redistribution.

______________________________________________________________________

# Next

[Message Queues (RabbitMQ, Kafka & Event-Driven Architecture)](16-message-queues.md)
