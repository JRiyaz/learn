# System Design - Part 89

# Distributed Locking System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Distributed Locking is needed
- Problems without locks
- Mutex vs Distributed Lock
- Lock Lifecycle
- Redis Locks
- SET NX EX
- Lease-Based Locks
- Redlock Algorithm
- ZooKeeper Locks
- etcd Locks
- Failure Handling
- Best Practices
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a Distributed Locking System.**

Distributed locking

is one of

the most common

Senior Backend

interview topics.

Whenever

multiple services

modify

the same resource,

we must ensure

only one service

does it

at a time.

______________________________________________________________________

# Why Do We Need Distributed Locks?

Suppose

there is

only

one product

left.

Two users

click

"Buy Now"

at exactly

the same time.

```text id="dl8901"
User A

↓

Inventory

↑

User B
```

Without locking,

both requests

may reduce

inventory

from

1

to

0

simultaneously.

Result:

```text id="dl8902"
Overselling
```

______________________________________________________________________

# Another Example

Money Transfer

```text id="dl8903"
Balance = ₹1000
```

Two requests

withdraw

₹800.

Both

read

₹1000.

Both succeed.

Final balance

becomes

incorrect.

______________________________________________________________________

# What is a Lock?

A lock

is simply

a permission

to modify

a resource.

```text id="dl8904"
Acquire Lock

↓

Modify Resource

↓

Release Lock
```

Only

one process

holds

the lock

at a time.

______________________________________________________________________

# Local Lock vs Distributed Lock

Interview favorite.

Local Lock

```text id="dl8905"
Thread A

↓

Mutex

↓

Shared Memory
```

Works

only

inside

one process.

______________________________________________________________________

Distributed Lock

```text id="dl8906"
Service A

↓

Lock Server

↑

Service B
```

Works

across

multiple servers.

______________________________________________________________________

# Lock Lifecycle

```text id="dl8907"
Acquire

↓

Success

↓

Critical Section

↓

Release
```

If

Acquire fails,

retry

or wait.

______________________________________________________________________

# Redis Lock

Interview favorite.

Redis

supports

atomic operations.

Acquire lock

using

```redis id="dl8908"
SET order:123 lock123 NX EX 30
```

Meaning:

- NX → Only if key doesn't exist
- EX → Expire after 30 seconds

If successful,

the client

owns

the lock.

______________________________________________________________________

# Why Expiration?

Suppose

the application

crashes

after

acquiring

the lock.

Without

expiration,

the lock

remains forever.

```text id="dl8909"
Crash

↓

Lock Never Released
```

Expiration

prevents

deadlocks.

______________________________________________________________________

# Releasing the Lock

Interview favorite.

Wrong way

```redis id="dl8910"
DEL order:123
```

Why?

Another service

might have

already acquired

a new lock.

Instead,

delete

only

if

the lock value

matches.

Example

```text id="dl8911"
Lock Owner

↓

Compare Value

↓

Delete
```

Use

a Lua script

to make

comparison

and deletion

atomic.

______________________________________________________________________

# Lease-Based Locks

Interview favorite.

A lock

is actually

a lease.

```text id="dl8912"
30 Seconds
```

If

the holder

needs more time,

it must

renew

the lease.

Otherwise,

the lock

expires automatically.

______________________________________________________________________

# Redlock Algorithm

Interview favorite.

Question.

What if

the Redis server

fails?

One server

may lose

the lock.

Redlock

uses

multiple

independent Redis nodes.

Example

```text id="dl8913"
Redis 1

Redis 2

Redis 3

Redis 4

Redis 5
```

The client

must acquire

a majority.

Example

```text id="dl8914"
3 of 5
```

Only then

is the lock

considered valid.

______________________________________________________________________

# ZooKeeper Lock

Interview favorite.

ZooKeeper

uses

ephemeral sequential nodes.

Workflow

```text id="dl8915"
Client

↓

Create Sequential Node

↓

Smallest Node Wins
```

When

the client

disconnects,

its node

disappears automatically.

The next client

acquires

the lock.

______________________________________________________________________

# etcd Lock

Modern systems

often use

etcd.

Workflow

```text id="dl8916"
Lease

↓

Lock

↓

Automatic Expiration
```

Common

in

Kubernetes

control planes.

______________________________________________________________________

# Lock Granularity

Interview favorite.

Fine-Grained

```text id="dl8917"
Lock Order 101
```

Better concurrency.

______________________________________________________________________

Coarse-Grained

```text id="dl8918"
Lock Entire Inventory
```

Simpler,

but

reduces throughput.

______________________________________________________________________

# Retry Strategy

Suppose

the lock

is unavailable.

Options:

- Immediate retry
- Exponential backoff
- Queue request

Avoid

busy waiting.

______________________________________________________________________

# Deadlocks

Interview favorite.

Distributed locks

can also

deadlock.

Example

```text id="dl8919"
Service A

↓

Lock X

↓

Needs Y
```

```text id="dl8920"
Service B

↓

Lock Y

↓

Needs X
```

Neither

can continue.

Solutions:

- Lock ordering
- Timeouts
- Lease expiration

______________________________________________________________________

# Fencing Tokens

Interview favorite.

Question.

Suppose

a client's lock

expires,

but

it continues

working.

Another client

gets

a new lock.

Now

both operate

simultaneously.

Solution:

Issue

monotonically

increasing

fencing tokens.

```text id="dl8921"
Token 101

↓

Token 102
```

The resource

accepts

only

the newest token.

______________________________________________________________________

# Database Locking

Sometimes

a distributed lock

is unnecessary.

Use:

- Row-level locks
- Optimistic locking
- Serializable transactions

Choose

the simplest

solution first.

______________________________________________________________________

# Failure Scenario

Suppose

Redis

crashes

immediately

after

granting

a lock.

A single-node

lock

may be lost.

Use:

- Redlock
- ZooKeeper
- etcd

when

higher reliability

is required.

______________________________________________________________________

# Another Failure

Suppose

the application

holds

the lock,

then crashes.

The lease

expires.

Another client

can safely

acquire

the lock.

______________________________________________________________________

# End-to-End Architecture

```text id="dl8922"
Application A

↓

Lock Service

↓

Redis / ZooKeeper / etcd

↑

Application B
```

______________________________________________________________________

# Trade-offs

Redis

vs

ZooKeeper

| Redis | ZooKeeper |
| ----------- | --------------------- |
| Faster | Stronger coordination |
| Simple | More complex |
| Cache-based | Consensus-based |

______________________________________________________________________

Fine Lock

vs

Coarse Lock

| Fine | Coarse |
| ------------------ | ---------------- |
| Higher concurrency | Simpler |
| More locks | Lower throughput |

______________________________________________________________________

Lease

vs

Permanent Lock

| Lease | Permanent |
| ------------------ | ---------------- |
| Automatic recovery | Risk of deadlock |
| Safer | Manual cleanup |

______________________________________________________________________

# Best Practices

✅ Always use lock expiration.

✅ Store a unique lock value.

✅ Release locks atomically.

✅ Keep critical sections small.

✅ Use fencing tokens for critical systems.

______________________________________________________________________

# Common Mistakes

### Forgetting Expiration

A crashed process

can block

the resource

forever.

______________________________________________________________________

### Deleting Someone Else's Lock

Never

delete

a lock

without verifying

ownership.

______________________________________________________________________

### Holding Locks Too Long

Long-running

critical sections

reduce concurrency

and

increase contention.

______________________________________________________________________

### Using Distributed Locks Everywhere

Many problems

can be solved

with:

- Optimistic locking
- Database transactions
- Version numbers

Distributed locks

should be

the last option.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a distributed locking system?

Design a centralized coordination mechanism that allows only one client to acquire a lock for a given resource at a
time. For Redis, use `SET key value NX EX` to atomically create a lock with an expiration time, and release it only
after verifying ownership using a Lua script. Treat locks as leases that automatically expire to avoid deadlocks caused
by crashed processes. For stronger consistency and coordination guarantees, use ZooKeeper or etcd, which provide
ephemeral nodes or lease-based locking. Implement retry strategies with exponential backoff, keep critical sections
short, and use fencing tokens to prevent stale lock holders from modifying shared resources after their lease has
expired.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Distributed locking
- Redis locks
- SET NX EX
- Lease-based locks
- Redlock
- ZooKeeper
- etcd
- Fencing tokens
- Deadlocks
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ Kafka Internals
- ✅ Redis Internals
- ✅ Nginx Internals
- ✅ Elasticsearch Internals
- ✅ Distributed Locking

You now understand how distributed systems coordinate access to shared resources without corrupting data.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll cover another cornerstone of distributed systems:

- ACID vs BASE
- Two-Phase Commit (2PC)
- Three-Phase Commit (3PC)
- Saga Pattern
- Choreography vs Orchestration
- Outbox Pattern
- Idempotency
- Exactly-once processing
- Compensation transactions

We'll design **Distributed Transactions**.

______________________________________________________________________

# What's Next

[Distributed Transactions System Design](90-distributed-transactions-system-design.md)
