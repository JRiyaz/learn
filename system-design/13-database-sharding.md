# Database Sharding (Horizontal Partitioning)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand database sharding, why it is needed, different sharding strategies, common challenges, and how to answer sharding questions confidently in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

has grown

to

```
1 Billion Users
```

Your database

already has

- Replication
- SSD storage
- More CPU
- More RAM

Yet,

performance

is still degrading.

```
Database

↓

CPU 100%

↓

Memory Full

↓

Storage Huge

↓

Writes Slow
```

Adding

more replicas

doesn't help.

Why?

Because

all writes

still go

to

one database.

How do companies

like

Instagram,

Facebook,

Uber,

and Amazon

solve this?

The answer is

```
Sharding
```

______________________________________________________________________

# What Is Sharding?

Sharding means

splitting

one large database

into

multiple smaller databases.

Instead of

```
Application

↓

One Database
```

we get

```
Application

↓

Shard A

Shard B

Shard C

Shard D
```

Each shard

stores

only

part of the data.

______________________________________________________________________

# Why Do We Need Sharding?

One database

has limits.

Eventually

you cannot

keep increasing

CPU,

RAM,

or storage.

Sharding provides

```
Horizontal Scaling
```

Instead of

buying

a larger server,

add

more servers.

______________________________________________________________________

# Replication vs Sharding

Many candidates

confuse these.

Replication

```
Same Data

↓

Multiple Copies
```

Sharding

```
Different Data

↓

Different Servers
```

______________________________________________________________________

# Example

Without Sharding

```
Users

↓

One Database

↓

1 Billion Records
```

With Sharding

```
Users A-F

↓

Shard 1
```

```
Users G-M

↓

Shard 2
```

```
Users N-S

↓

Shard 3
```

```
Users T-Z

↓

Shard 4
```

Each database

stores

less data.

______________________________________________________________________

# Benefits

Sharding improves

- Write scalability
- Storage capacity
- Performance
- Availability
- Horizontal scaling

______________________________________________________________________

# Basic Architecture

```
Application

↓

Shard Router

↓

Shard A

Shard B

Shard C
```

The router

decides

which shard

contains

the data.

______________________________________________________________________

# Sharding Key

One of the most important

interview concepts.

A

```
Sharding Key
```

determines

where

data is stored.

Choosing

the wrong key

causes

major problems.

______________________________________________________________________

# Example

User ID

```
User 101

↓

Shard 1
```

```
User 205

↓

Shard 2
```

```
User 980

↓

Shard 5
```

The application

always knows

where to look.

______________________________________________________________________

# Sharding Strategies

Several strategies exist.

Each has

advantages

and disadvantages.

______________________________________________________________________

# 1. Range-Based Sharding

Split data

by ranges.

Example

```
1–1,000,000

↓

Shard A
```

```
1,000,001–2,000,000

↓

Shard B
```

Simple.

Easy to understand.

______________________________________________________________________

# Problem

Suppose

new users

always receive

larger IDs.

Eventually

only

the last shard

receives

all new writes.

```
Hotspot
```

______________________________________________________________________

# 2. Hash-Based Sharding

Very common.

Formula

```
Hash(User ID)

↓

Shard Number
```

Example

```
101

↓

Hash

↓

Shard 2
```

Advantages

- Even distribution
- Fewer hotspots

Disadvantages

Range queries

become harder.

______________________________________________________________________

# 3. Geographic Sharding

Users

are stored

by region.

Example

```
India

↓

Mumbai Database
```

```
Germany

↓

Frankfurt Database
```

```
USA

↓

Virginia Database
```

Benefits

- Lower latency
- Easier compliance
- Regional isolation

______________________________________________________________________

# 4. Directory-Based Sharding

Maintain

a lookup table.

Example

```
User

↓

Lookup Service

↓

Shard 5
```

Flexible.

But

the lookup service

must itself

be reliable.

______________________________________________________________________

# Consistent Hashing

Interview favorite.

Problem

Suppose

you add

a new shard.

Simple hashing

causes

many users

to move.

Consistent Hashing

minimizes

data movement.

Widely used

in

distributed systems.

We'll cover

it

in detail

later.

______________________________________________________________________

# Shard Router

Applications

usually don't

query

every shard.

Instead

```
Application

↓

Router

↓

Correct Shard
```

The router

knows

where

the data lives.

______________________________________________________________________

# Cross-Shard Queries

Suppose

you ask

```
Total Users
```

Data exists

across

10 shards.

Now

all shards

must participate.

More expensive

than

a single database.

______________________________________________________________________

# Cross-Shard Joins

SQL joins

become

much harder.

Example

```
Orders

↓

Shard A
```

```
Users

↓

Shard D
```

Joining

requires

communication

between shards.

Many systems

avoid

cross-shard joins.

______________________________________________________________________

# Rebalancing

Suppose

Shard A

becomes

full.

New shard

is added.

Some data

must move.

This process

is called

```
Rebalancing
```

It can be

expensive.

______________________________________________________________________

# Hot Shards

Suppose

one celebrity

has

100 million followers.

All requests

go

to

one shard.

```
Hot Shard
```

One server

becomes overloaded

while others

remain mostly idle.

______________________________________________________________________

# Choosing A Good Sharding Key

A good key

should

- Distribute data evenly
- Avoid hotspots
- Rarely change
- Support query patterns

Good examples

- User ID
- Order ID
- Customer ID

Poor examples

- Country (few values)
- Gender
- Boolean fields

______________________________________________________________________

# Auto-Increment IDs

Auto-increment

may create

write hotspots

because

new rows

always target

the newest range.

Hashing

or

UUIDs

can reduce

this issue,

depending on

requirements.

______________________________________________________________________

# Sharding And Replication

Large systems

often use

both.

```
Application

↓

Shard Router

↓

Shard A

↓

Replicas
```

```
Shard B

↓

Replicas
```

Each shard

can have

its own replicas.

______________________________________________________________________

# Failure Scenario

Suppose

Shard B

fails.

Only

users

stored

in

Shard B

are affected.

Other shards

continue working.

Better

fault isolation.

______________________________________________________________________

# SQL vs NoSQL

Both

support sharding.

Examples

SQL

- PostgreSQL (various extensions)
- MySQL (application or middleware)

NoSQL

- MongoDB
- Cassandra
- DynamoDB

Many NoSQL systems

provide

built-in sharding.

______________________________________________________________________

# Typical Architecture

```
Users

↓

Load Balancer

↓

Application

↓

Shard Router

↓

Shard A

Shard B

Shard C

↓

Replicas

↓

Backups
```

______________________________________________________________________

# Common Interview Questions

## Why not keep adding bigger servers?

Vertical scaling

has physical

and financial limits.

Sharding

allows

horizontal scaling

across many servers.

______________________________________________________________________

## Does sharding improve writes?

Yes.

Different shards

handle

different write traffic,

reducing contention

on a single database.

______________________________________________________________________

## Can replication replace sharding?

No.

Replication

improves

read scalability

and availability.

Sharding

improves

write scalability

and storage capacity.

______________________________________________________________________

## What is the hardest part of sharding?

Choosing

the correct

sharding key

and handling

rebalancing,

cross-shard queries,

and operational complexity.

______________________________________________________________________

# Common Mistakes

## Choosing A Bad Sharding Key

This causes

uneven distribution

and hotspots.

______________________________________________________________________

## Forgetting Cross-Shard Queries

Queries

across shards

are expensive.

______________________________________________________________________

## Sharding Too Early

Don't shard

before

there is

a real scaling need.

Complexity

increases significantly.

______________________________________________________________________

## Thinking Sharding Solves Everything

Sharding

helps with

storage

and writes,

but introduces

many operational challenges.

______________________________________________________________________

# Best Practices

✅ Choose a stable, high-cardinality sharding key.

✅ Combine sharding with replication.

✅ Monitor shard utilization.

✅ Plan for rebalancing.

✅ Avoid unnecessary cross-shard joins.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between replication and sharding?

### Answer

Replication creates multiple copies of the same data to improve availability and read scalability. Sharding splits data
across multiple databases to improve write scalability and storage capacity.

______________________________________________________________________

## Question

What makes a good sharding key?

### Answer

A good sharding key distributes data evenly, minimizes hotspots, supports common query patterns, and rarely changes over
time.

______________________________________________________________________

## Question

Should every application use sharding?

### Answer

No. Sharding introduces significant complexity. It should only be used when a single database can no longer meet storage
or write throughput requirements after simpler scaling techniques have been exhausted.

______________________________________________________________________

# Practice Exercise

For each application,

answer

1. Would sharding be required?
1. What would the sharding key be?
1. Which sharding strategy would you choose?
1. Would replication also be needed?
1. What operational challenges would you expect?

Applications

- Instagram
- WhatsApp
- Banking System
- Netflix
- Online Shopping
- URL Shortener
- Ride Sharing
- Food Delivery

Explain

your decisions

using

expected traffic,

query patterns,

consistency,

and scalability requirements.

______________________________________________________________________

# Summary

Sharding is the primary technique for scaling databases beyond the limits of a single server.

It enables

- Horizontal scaling
- Higher write throughput
- Larger storage capacity
- Better fault isolation

However,

it also introduces

- Routing complexity
- Rebalancing
- Cross-shard queries
- Hotspot management

Understanding when to shard—and when **not** to—is a key skill expected in Senior Software Engineer System Design
interviews.

______________________________________________________________________

# Next

[CAP Theorem](14-cap-theorem.md)
