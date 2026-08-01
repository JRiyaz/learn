# Software Architecture - Part 47

# Consensus Algorithms (Raft & Paxos)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Consensus is
- Why Consensus is difficult
- What problems Consensus solves
- Leader Election
- Log Replication
- Raft Algorithm
- Paxos Algorithm
- Raft vs Paxos
- Kubernetes example
- Database examples
- Interview questions

______________________________________________________________________

# Before We Start

You've learned

about

CAP Theorem.

One question

still remains.

Suppose

three servers

store

the same data.

```text id="con4701"
Server A

Server B

Server C
```

One server

fails.

Another

loses

network connectivity.

How do

the remaining servers

agree

on

the correct state?

This problem

is called

**Consensus**.

______________________________________________________________________

# The Problem

Let's continue

with our

**Library Management System**.

Suppose

inventory data

is replicated

across

three nodes.

```text id="con4702"
Node A

Node B

Node C
```

A member

borrows

the last copy

of a book.

Which node

should update first?

What happens

if

two nodes

accept

different updates

at

the same time?

______________________________________________________________________

# Another Problem

Suppose

the leader

crashes.

```text id="con4703"
Leader

❌
```

Who becomes

the new leader?

How do

all servers

agree

on

the replacement?

______________________________________________________________________

# What is Consensus?

**Consensus**

is the process

by which

multiple distributed nodes

agree

on

a single value

or

a single sequence

of operations,

even

when

machines fail

or

network partitions occur.

______________________________________________________________________

# Why is Consensus Needed?

Without Consensus,

different nodes

may contain

different truths.

Example

```text id="con4704"
Node A

Book Available
```

```text id="con4705"
Node B

Book Borrowed
```

Which one

is correct?

Consensus

ensures

all healthy nodes

eventually agree.

______________________________________________________________________

# Requirements

A Consensus Algorithm

must guarantee:

- Safety
- Liveness
- Fault Tolerance

Let's understand

each one.

______________________________________________________________________

# Safety

Safety means

two nodes

must never

decide

different values

for

the same operation.

Example

The last book

cannot be

both

available

and

borrowed.

______________________________________________________________________

# Liveness

Liveness means

the system

continues

making progress,

even

after

some failures.

If

a leader crashes,

the cluster

should recover.

______________________________________________________________________

# Fault Tolerance

Consensus Algorithms

continue working

even

if

some nodes fail.

Example

Three-node cluster.

One node

fails.

The cluster

still operates.

______________________________________________________________________

# Majority (Quorum)

Most Consensus Algorithms

use

a **majority**

to make decisions.

Example

Three nodes.

```text id="con4706"
A

B

C
```

Majority

\=

2 votes.

Five nodes.

Majority

\=

3 votes.

This is called

a **Quorum**.

______________________________________________________________________

# Leader-Based Consensus

Most modern

algorithms

elect

one leader.

```text id="con4707"
Leader

↓

Followers
```

Clients

send writes

to

the leader.

Followers

replicate

the changes.

______________________________________________________________________

# Leader Election

Suppose

the leader

fails.

Followers

start

an election.

One node

wins.

```text id="con4708"
Follower

↓

Leader
```

The cluster

continues

without

manual intervention.

______________________________________________________________________

# Log Replication

Suppose

the leader

receives

a write.

```text id="con4709"
Borrow Book
```

The leader

appends

the operation

to its log.

Then

replicates

the log

to followers.

Once

a majority

acknowledges,

the operation

is committed.

______________________________________________________________________

# Why Logs?

Consensus Algorithms

don't replicate

database rows.

They replicate

**operations.**

Example

```text id="con4710"
Borrow Book

↓

Return Book

↓

Pay Fine
```

Every node

executes

the same sequence

of operations.

______________________________________________________________________

# Raft Algorithm

Raft

was designed

to be

easier

to understand

than Paxos.

It consists

of

three major components.

- Leader Election
- Log Replication
- Safety

______________________________________________________________________

# Raft States

Every node

is

one of

three states.

```text id="con4711"
Leader

Follower

Candidate
```

Normally,

most nodes

are Followers.

______________________________________________________________________

# Leader Election in Raft

Suppose

Followers

stop hearing

from

the Leader.

After

a timeout,

they become

Candidates.

They request votes.

If

a node

receives

a majority,

it becomes

the new Leader.

______________________________________________________________________

# Heartbeats

Leaders

periodically send

heartbeat messages.

```text id="con4712"
Leader

↓

Heartbeat

↓

Followers
```

If

heartbeats stop,

Followers

assume

the leader

has failed.

______________________________________________________________________

# Commit Rule

The Leader

doesn't commit

a write

immediately.

It waits

until

a majority

of Followers

have replicated

the log entry.

Only then

is

the operation

considered committed.

______________________________________________________________________

# Paxos Algorithm

Paxos

is

another

Consensus Algorithm.

It is

mathematically elegant,

but

notoriously difficult

to understand

and implement.

Many systems

prefer

Raft

because

its behavior

is easier

to reason about.

______________________________________________________________________

# Raft vs Paxos

| Raft | Paxos |
| ------------------------------- | ------------------------------------ |
| Easier to understand | More mathematically rigorous |
| Leader-based | Multiple variants exist |
| Widely adopted | Historically influential |
| Common in modern infrastructure | Common in research and older systems |

______________________________________________________________________

# Kubernetes Example

Kubernetes

stores

cluster state

inside

**etcd**.

etcd

uses

the

Raft Algorithm.

This ensures

every control plane node

agrees

on

the cluster state.

If

the leader

fails,

Raft

elects

a new leader

automatically.

______________________________________________________________________

# Database Examples

Several databases

use

Consensus Algorithms.

Examples:

- etcd → Raft
- Consul → Raft
- TiKV → Raft
- CockroachDB → Raft

These systems

replicate

data safely

across

multiple nodes.

______________________________________________________________________

# AI/ML Example

Suppose

multiple

Model Registry nodes

manage

approved models.

Consensus

ensures

every node

agrees

on

the active model version,

even

if

one server

fails.

Without consensus,

different inference servers

could load

different model versions.

______________________________________________________________________

# Consensus vs Replication

Interview favorite.

| Replication | Consensus |
| ----------- | ------------------------------ |
| Copies data | Agrees on the order of updates |
| May diverge | Guarantees agreement |
| Simpler | More complex |

Replication

without

Consensus

can still

produce conflicts.

______________________________________________________________________

# Consensus vs Distributed Transactions

| Consensus | Distributed Transaction |
| ----------------------- | ------------------------------ |
| Agreement on operations | Agreement on commits |
| Cluster coordination | Business workflow coordination |

They solve

different problems.

______________________________________________________________________

# Real Backend Example

Suppose

a configuration service

stores

feature flags.

Every server

must agree

that

```text id="con4713"
New Feature

Enabled
```

Consensus

ensures

all servers

see

the same

configuration.

______________________________________________________________________

# CAP Connection

Consensus Algorithms

generally favor

Consistency

during

network partitions.

They typically

lean toward

the **CP**

side

of

the CAP Theorem.

Some requests

may be rejected

to avoid

split-brain

or

conflicting decisions.

______________________________________________________________________

# Benefits

Consensus provides:

✅ Strong consistency

✅ Automatic leader election

✅ Fault tolerance

✅ Reliable replication

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Majority requirements

❌ Network overhead

❌ Write latency

❌ Operational complexity

______________________________________________________________________

# Split Brain

One of

the biggest dangers

in distributed systems.

Suppose

two leaders

exist

at

the same time.

```text id="con4714"
Leader A

Leader B
```

Both accept

different writes.

Consensus Algorithms

prevent

this situation

through

quorum

and

leader election.

______________________________________________________________________

# When NOT to Use Consensus

Don't use

Consensus Algorithms

for:

- Simple CRUD applications
- Single-node databases
- Small internal tools

They are intended

for

distributed infrastructure,

not

ordinary application code.

______________________________________________________________________

# Best Practices

✅ Use odd numbers of nodes.

✅ Maintain quorum.

✅ Monitor leader elections.

✅ Keep clocks reasonably synchronized.

______________________________________________________________________

# Common Mistakes

### Even Number of Nodes

Four nodes

still require

three votes

for a majority.

Odd-sized clusters

provide

the same fault tolerance

with

fewer machines.

______________________________________________________________________

### Assuming Replication Equals Consensus

Replication

copies data.

Consensus

decides

which data

is authoritative.

______________________________________________________________________

### Ignoring Network Partitions

Distributed systems

must assume

partitions

will happen.

Consensus Algorithms

are designed

for

that reality.

______________________________________________________________________

### Multiple Writers

Allowing

multiple leaders

without coordination

can create

conflicting histories.

Consensus

avoids

this problem.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Consensus Algorithm, and why is Raft commonly preferred over Paxos?

A Consensus Algorithm enables multiple distributed nodes to agree on a single sequence of operations despite failures or
network partitions. It ensures safety, liveness, and fault tolerance through mechanisms such as leader election,
quorum-based voting, and log replication. Raft is commonly preferred over Paxos because it separates the problem into
understandable components—leader election, log replication, and safety—making it easier to learn, implement, and debug.
Many modern distributed systems, including etcd and Consul, use Raft to maintain strongly consistent replicated state.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Consensus is
- Why it is needed
- Leader Election
- Quorum
- Log Replication
- Raft
- Paxos
- Kubernetes example
- CAP connection
- Best practices

______________________________________________________________________

# 🎯 Architecture Journey Complete

You have now completed the **Software Architecture & Distributed Systems** module, including:

- ✅ Design Principles (SOLID, DRY, KISS, YAGNI)
- ✅ Design Patterns
- ✅ Architectural Styles
- ✅ DDD
- ✅ Microservices
- ✅ Reliability Patterns
- ✅ Distributed Transactions
- ✅ CAP Theorem
- ✅ Consensus Algorithms

This is the knowledge expected of many senior backend engineers before moving into advanced system design interviews.

______________________________________________________________________

# What's Next

[System Design Fundamentals](48-system-design-fundamentals.md)
