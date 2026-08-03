# System Design - Part 69

# Disaster Recovery & Backups

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Disaster Recovery (DR) is
- Why Disaster Recovery is important
- What Backups are
- Backup Strategies
- Full, Incremental & Differential Backups
- RPO & RTO
- High Availability vs Disaster Recovery
- Multi-Region Architecture
- Failover
- Backup Verification
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

runs

in

one cloud region.

Everything

works perfectly.

Suddenly,

an entire

data center

goes offline.

Possible reasons:

- Power outage
- Fire
- Flood
- Network failure
- Cloud provider issue

Question.

What happens

to

our application?

______________________________________________________________________

# The Problem

Suppose

our architecture

looks like this.

```text id="dr6901"
Users

↓

Application

↓

Database
```

Everything

runs

inside

one region.

If

that region

fails,

the application

becomes unavailable.

______________________________________________________________________

# Another Problem

Suppose

someone

accidentally executes

```sql id="dr6902"
DELETE FROM books;
```

The data

is gone.

Replication

copies

the deletion

to

all replicas.

Question.

Can replication

recover

the deleted data?

No.

Replication

is **not**

a backup.

______________________________________________________________________

# The Idea

Prepare

for failure

before

it happens.

Maintain

backups,

replicas,

and

recovery procedures

that allow

the system

to continue

operating.

______________________________________________________________________

# What is Disaster Recovery?

**Disaster Recovery (DR)**

is the process

of restoring

applications,

data,

and infrastructure

after

a major failure

or disaster.

Its goal

is to minimize

downtime

and

data loss.

______________________________________________________________________

# What is a Backup?

A **Backup**

is

an independent

copy

of data

that can be used

to restore

information

if

the original data

is lost

or corrupted.

______________________________________________________________________

# Backup vs Replication

Interview favorite.

| Backup | Replication |
| ---------------------- | --------------------- |
| Historical copy | Live copy |
| Recovery from deletion | High availability |
| Disaster recovery | Read scalability |
| Point-in-time restore | Mirrors current state |

Replication

cannot replace

backups.

______________________________________________________________________

# Full Backup

A **Full Backup**

copies

the entire dataset.

```text id="dr6903"
Database

↓

Full Backup
```

Advantages

✅ Simple restore

Disadvantages

❌ Large storage

❌ Longer backup time

______________________________________________________________________

# Incremental Backup

Only

changes

since

the previous backup

are stored.

```text id="dr6904"
Full Backup

↓

Increment 1

↓

Increment 2

↓

Increment 3
```

Advantages

✅ Small backups

✅ Fast backup

Disadvantages

❌ Restore

requires

multiple backup files.

______________________________________________________________________

# Differential Backup

Stores

all changes

since

the last

Full Backup.

```text id="dr6905"
Full Backup

↓

Diff 1

↓

Diff 2

↓

Diff 3
```

Advantages

✅ Faster restore

than Incremental

Disadvantages

❌ Larger backups

than Incremental.

______________________________________________________________________

# Backup Strategy Comparison

| Strategy | Backup Speed | Restore Speed | Storage |
| ------------ | ------------ | ------------- | ------- |
| Full | Slow | Fast | High |
| Incremental | Fast | Slow | Low |
| Differential | Medium | Medium | Medium |

______________________________________________________________________

# RPO

Interview favorite.

**Recovery Point Objective (RPO)**

defines

how much data

you can afford

to lose.

Example

```text id="dr6906"
RPO

5 Minutes
```

If

the system

fails,

losing

up to

5 minutes

of data

is acceptable.

______________________________________________________________________

# RTO

Interview favorite.

**Recovery Time Objective (RTO)**

defines

how quickly

the system

must be restored.

Example

```text id="dr6907"
RTO

15 Minutes
```

The application

must be

available again

within

15 minutes.

______________________________________________________________________

# High Availability vs Disaster Recovery

Interview favorite.

| High Availability | Disaster Recovery |
| ------------------ | ---------------------- |
| Prevent downtime | Recover after disaster |
| Replication | Backups |
| Automatic failover | Data restoration |
| Minutes or seconds | Minutes to hours |

Large systems

need

both.

______________________________________________________________________

# Point-in-Time Recovery (PITR)

Suppose

someone

accidentally deletes

data

at

10:30 AM.

You want

to restore

the database

to

10:29 AM.

This is called

**Point-in-Time Recovery (PITR).**

Many databases,

including PostgreSQL,

support PITR

using

transaction logs.

______________________________________________________________________

# Multi-Region Deployment

Instead of

running

everything

in

one region,

deploy

to

multiple regions.

```text id="dr6908"
Region A

↔

Region B
```

If

Region A

fails,

traffic

moves

to

Region B.

______________________________________________________________________

# Failover

Suppose

Region A

becomes unavailable.

```text id="dr6909"
Users

↓

DNS

↓

Region B
```

Traffic

is redirected

automatically.

______________________________________________________________________

# Cold, Warm & Hot Standby

Interview favorite.

| Type | Ready? | Cost | Recovery |
| ---- | ----------- | ------ | -------- |
| Cold | No | Low | Slow |
| Warm | Partially | Medium | Medium |
| Hot | Fully Ready | High | Fast |

______________________________________________________________________

## Cold Standby

Infrastructure

is not running.

Restore

from backups

when needed.

Lowest cost.

Highest downtime.

______________________________________________________________________

## Warm Standby

Infrastructure

is running,

but

not serving

production traffic.

Recovery

is faster.

______________________________________________________________________

## Hot Standby

A complete

production environment

runs

continuously.

Traffic

can switch

almost immediately.

Highest cost.

Lowest downtime.

______________________________________________________________________

# Object Storage Backups

Databases

are not

the only systems

that need backups.

Object Storage

should also

be backed up

or replicated.

Examples:

- Images
- Videos
- Documents
- AI Models

______________________________________________________________________

# Backup Verification

A backup

is useless

if

it cannot

be restored.

Regularly perform

restore tests.

```text id="dr6910"
Backup

↓

Restore Test

↓

Success
```

Always verify

backup integrity.

______________________________________________________________________

# FastAPI Example

Suppose

the application

stores

book metadata

in PostgreSQL

and

PDF books

in

Object Storage.

Backup plan:

- PostgreSQL daily backups
- WAL archiving for PITR
- Object Storage replication
- Regular restore testing

______________________________________________________________________

# Kubernetes Example

Pods

are ephemeral.

Never rely

on

Pod storage

for backups.

Use:

- Persistent Volumes
- Database snapshots
- Object Storage
- Managed backup services

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

stores:

- Training datasets
- Model checkpoints
- Fine-tuned models
- Vector indexes

Losing

any of these

could require

weeks

of retraining.

Regular backups

are essential.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Recovery plan:

- PostgreSQL PITR
- Redis rebuilt from database
- Elasticsearch reindexed
- Object Storage replicated
- Kubernetes redeploys services

Within minutes,

the platform

is operational again.

______________________________________________________________________

# Disaster Recovery Plan (DRP)

Every production system

should document:

- What to restore
- Restore order
- Responsible teams
- Contact information
- Recovery procedures
- Validation steps

A documented plan

reduces

recovery time.

______________________________________________________________________

# Benefits

Disaster Recovery provides:

✅ Business continuity

✅ Data protection

✅ Faster recovery

✅ Reduced downtime

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Additional infrastructure cost

❌ Backup storage costs

❌ Operational complexity

❌ Regular testing effort

______________________________________________________________________

# When NOT to Skip Backups

Never assume

Replication

or

RAID

is enough.

Neither

protects against:

- Accidental deletion
- Data corruption
- Ransomware
- Application bugs

Backups

remain essential.

______________________________________________________________________

# Best Practices

✅ Define RPO and RTO.

✅ Automate backups.

✅ Test restores regularly.

✅ Store backups

in

a separate location.

______________________________________________________________________

# Common Mistakes

### Never Testing Restores

A backup

that cannot

be restored

is useless.

______________________________________________________________________

### Keeping Backups

in the Same Region

Regional disasters

can destroy

both

production

and

backups.

Store backups

in

another region

or

another account.

______________________________________________________________________

### No Backup Retention Policy

Keep

multiple backup versions

to recover

from

older issues

that were

not detected

immediately.

______________________________________________________________________

### Ignoring Business Requirements

Different systems

require

different

RPO

and

RTO values.

Critical payment systems

often require

much lower

RPO/RTO

than

internal reporting systems.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between High Availability and Disaster Recovery?

High Availability focuses on keeping services running during component failures by using techniques such as replication,
load balancing, and automatic failover. Its goal is to minimize or eliminate downtime. Disaster Recovery focuses on
restoring systems and data after major failures such as regional outages, accidental deletions, or data corruption.
Disaster Recovery relies on backups, recovery procedures, and predefined RPO and RTO targets. High Availability keeps
services online, while Disaster Recovery restores services after catastrophic failures.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Disaster Recovery is
- Backup strategies
- Full, Incremental & Differential backups
- RPO & RTO
- Point-in-Time Recovery
- High Availability vs Disaster Recovery
- Multi-Region deployments
- Failover
- Best practices

______________________________________________________________________

# 🧠 Deployment & Operations Progress

You have now completed the **Deployment & Operations** module:

- ✅ Blue-Green & Canary Deployments
- ✅ Disaster Recovery & Backups

You now understand how modern systems are deployed, protected, and recovered in production.

______________________________________________________________________

# 🎉 Foundation Course Status

You have now completed **69 out of 70** core System Design lessons.

Only **one final foundation lesson remains**, and it's one of the most important because it brings together everything
you've learned.

______________________________________________________________________

# What's Next

[End-to-End System Design Methodology](70-end-to-end-system-design-methodology.md)
