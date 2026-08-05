# 09-statefulsets-jobs-cronjobs.md

# StatefulSets, DaemonSets, Jobs & CronJobs

> **🎯 So far, almost everything we've deployed has been a long-running API service.**
>
> But production systems contain many other workloads:
>
> - PostgreSQL
> - Kafka
> - Redis Cluster
> - Daily backup jobs
> - Nightly report generation
> - Log collection agents
>
> Kubernetes provides different workload types for each use case.
>
> **Choosing the correct workload is a very common interview topic.**

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 40–50 minutes |
| Revision Time | 25 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers want to know whether you understand:

- Deployment vs StatefulSet
- Stateless vs Stateful applications
- DaemonSets
- Jobs
- CronJobs
- Stable identities
- Batch processing
- Scheduled tasks

One of the most common interview questions is:

> **"When would you use a Deployment instead of a StatefulSet?"**

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- What is a StatefulSet?
- When should StatefulSets be used?
- What is a DaemonSet?
- What is a Job?
- What is a CronJob?
- Which Kubernetes workload fits which use case?

______________________________________________________________________

# Before We Start

Until now,

we've been using

```text
Deployment
```

for everything.

That's not always correct.

Different applications

have different requirements.

______________________________________________________________________

# Stateless vs Stateful

This is the first thing to understand.

______________________________________________________________________

## Stateless

Every instance

is identical.

Example

```text
FastAPI

Pod A

==

Pod B

==

Pod C
```

Delete one.

Create another.

Nothing changes.

Deployment is perfect.

______________________________________________________________________

## Stateful

Every instance

has its own identity.

Example

```text
Kafka Broker 1

Kafka Broker 2

Kafka Broker 3
```

Each broker is different.

Replacing one incorrectly

can cause problems.

Need StatefulSet.

______________________________________________________________________

# Backend Engineering Analogy

Imagine backend engineers.

Stateless

```text
Customer Support

Engineer A

=

Engineer B
```

Either person

can answer tickets.

______________________________________________________________________

Stateful

```text
CEO

CTO

CFO
```

Each role

has a unique identity.

You can't randomly swap them.

______________________________________________________________________

# StatefulSet

A StatefulSet manages

applications that require

stable identity.

______________________________________________________________________

# What Makes StatefulSets Special?

Every Pod gets

a permanent identity.

Example

```text
postgres-0

postgres-1

postgres-2
```

Delete

```
postgres-1
```

New Pod

is still called

```
postgres-1
```

Unlike Deployments,

Pod names remain stable.

______________________________________________________________________

# Stable Storage

StatefulSets

also preserve storage.

Example

```text
postgres-0

↓

PVC

↓

Disk A
```

Even after restart,

same Pod

↓

same storage.

______________________________________________________________________

# Ordered Deployment

Deployments

start Pods

in any order.

StatefulSets

start Pods

one at a time.

Example

```text
postgres-0

↓

postgres-1

↓

postgres-2
```

Shutdown happens

in reverse order.

Useful for databases.

______________________________________________________________________

# When Should You Use StatefulSets?

Common examples

- PostgreSQL
- MySQL
- MongoDB
- Kafka
- ZooKeeper
- Redis Cluster
- Elasticsearch

Anything needing

stable identity

or

persistent storage.

______________________________________________________________________

# Deployment vs StatefulSet

| Deployment | StatefulSet |
|------------|-------------|
| Stateless | Stateful |
| Random Pod names | Stable Pod names |
| Easy scaling | Ordered scaling |
| Ephemeral storage | Persistent storage |
| FastAPI | PostgreSQL |

______________________________________________________________________

# DaemonSet

Imagine

every Worker Node

needs

a monitoring agent.

Instead of manually

creating Pods,

Kubernetes provides

DaemonSets.

______________________________________________________________________

# Rule

One Pod

per Worker Node.

______________________________________________________________________

Visual

```text
Node A

↓

Monitoring Agent
```

```text
Node B

↓

Monitoring Agent
```

```text
Node C

↓

Monitoring Agent
```

Every node

gets exactly one.

______________________________________________________________________

# Common DaemonSet Applications

- Fluent Bit
- Fluentd
- Prometheus Node Exporter
- Filebeat
- Security Agents
- Monitoring Agents

______________________________________________________________________

# Backend Analogy

Imagine

every office

must have

one security guard.

As new offices open,

new guards arrive automatically.

______________________________________________________________________

# Job

Deployments

run forever.

Sometimes

you only want

to run once.

Example

```text
Database Migration
```

Complete.

Exit.

Done.

That's a Job.

______________________________________________________________________

# Job Lifecycle

```text
Start

↓

Run

↓

Finish

↓

Succeeded
```

No restarting

after successful completion.

______________________________________________________________________

# Common Job Examples

- Database migrations
- Data imports
- ML model preprocessing
- Batch analytics
- Report generation

______________________________________________________________________

# CronJob

Suppose

you want

a Job

every night.

Instead of manually

starting it,

use

CronJob.

______________________________________________________________________

# Examples

Every night

```text
Database Backup
```

Every hour

```text
Cache Cleanup
```

Every Sunday

```text
Generate Reports
```

______________________________________________________________________

# Backend Analogy

Linux

```text
cron
```

Kubernetes

```text
CronJob
```

Exactly the same idea.

______________________________________________________________________

# Cron Schedule

Example

Every midnight

```text
0 0 * * *
```

Every hour

```text
0 * * * *
```

Every Sunday

```text
0 0 * * 0
```

______________________________________________________________________

# Visual

```text
12:00 AM

↓

CronJob

↓

Job

↓

Backup Database

↓

Finish
```

Next day

repeat.

______________________________________________________________________

# Complete Workload Comparison

```text
Deployment

↓

Long-running APIs
```

______________________________________________________________________

```text
StatefulSet

↓

Databases

Kafka

Redis Cluster
```

______________________________________________________________________

```text
DaemonSet

↓

One Pod

per Node
```

______________________________________________________________________

```text
Job

↓

Run Once
```

______________________________________________________________________

```text
CronJob

↓

Run on Schedule
```

______________________________________________________________________

# Real Production Architecture

Imagine an e-commerce platform.

```text
Users

↓

Ingress

↓

FastAPI

(Deployment)

↓

PostgreSQL

(StatefulSet)

↓

Fluent Bit

(DaemonSet)

↓

Nightly Backup

(CronJob)
```

Different workloads.

Different Kubernetes objects.

______________________________________________________________________

# Example YAML

## StatefulSet

```yaml
kind: StatefulSet

spec:

  serviceName: postgres

  replicas: 3
```

______________________________________________________________________

## DaemonSet

```yaml
kind: DaemonSet

spec:

  template:
```

______________________________________________________________________

## Job

```yaml
kind: Job
```

______________________________________________________________________

## CronJob

```yaml
kind: CronJob

spec:

  schedule: "0 0 * * *"
```

Again,

focus on understanding

the purpose,

not memorizing YAML.

______________________________________________________________________

# kubectl Commands

View StatefulSets

```bash
kubectl get statefulsets
```

______________________________________________________________________

View DaemonSets

```bash
kubectl get daemonsets
```

______________________________________________________________________

View Jobs

```bash
kubectl get jobs
```

______________________________________________________________________

View CronJobs

```bash
kubectl get cronjobs
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Running PostgreSQL

as a Deployment.

Use StatefulSet

when stable identity and storage are required.

______________________________________________________________________

## Mistake 2

Using StatefulSets

for FastAPI.

Stateless APIs

usually use Deployments.

______________________________________________________________________

## Mistake 3

Creating one monitoring Pod

manually

per node.

DaemonSets

do this automatically.

______________________________________________________________________

## Mistake 4

Using Deployments

for scheduled tasks.

Use CronJobs.

______________________________________________________________________

## Mistake 5

Thinking Jobs

run forever.

Jobs finish.

Deployments don't.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Deployments are designed for stateless, long-running applications such as FastAPI services. StatefulSets are used when applications require stable identities and persistent storage, such as PostgreSQL or Kafka. DaemonSets ensure exactly one Pod runs on every Worker Node, making them ideal for monitoring and logging agents. Jobs execute one-time tasks, while CronJobs schedule Jobs to run at specific times."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why not deploy PostgreSQL using a Deployment?**

Because PostgreSQL benefits from stable Pod identities and persistent storage, which StatefulSets provide.

______________________________________________________________________

**Q. When should I use a DaemonSet?**

When every Worker Node must run the same Pod, such as a log collector or monitoring agent.

______________________________________________________________________

**Q. What's the difference between a Job and a Deployment?**

A Job finishes after completing its task.

A Deployment is intended to run continuously.

______________________________________________________________________

**Q. What's the difference between a Job and a CronJob?**

A Job runs once.

A CronJob creates Jobs on a schedule.

______________________________________________________________________

**Q. Can a StatefulSet use Persistent Volumes?**

Yes.

StatefulSets are commonly paired with Persistent Volume Claims for stable storage.

______________________________________________________________________

# Pattern Summary

| Workload | Best For |
|----------|----------|
| Deployment | Stateless applications |
| StatefulSet | Databases and stateful systems |
| DaemonSet | One Pod per Worker Node |
| Job | One-time tasks |
| CronJob | Scheduled tasks |

______________________________________________________________________

# Quick Revision

- Deployments manage stateless applications.
- StatefulSets provide stable identities and persistent storage.
- DaemonSets run one Pod on every Worker Node.
- Jobs execute tasks once and then finish.
- CronJobs schedule Jobs.
- PostgreSQL and Kafka commonly use StatefulSets.
- Monitoring and logging agents commonly use DaemonSets.
- Database migrations are a good fit for Jobs.
- Nightly backups are a good fit for CronJobs.

______________________________________________________________________

# Production Decision Guide

| Scenario | Recommended Workload |
|----------|----------------------|
| FastAPI API | Deployment |
| Flask API | Deployment |
| PostgreSQL | StatefulSet |
| Kafka | StatefulSet |
| Redis Cluster | StatefulSet |
| Log Collector | DaemonSet |
| Prometheus Node Exporter | DaemonSet |
| Database Migration | Job |
| Nightly Backup | CronJob |
| Weekly Analytics Report | CronJob |

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Not every application should be deployed the same way.**

Kubernetes provides specialized workload types because different applications have different lifecycle requirements.
Stateless APIs are best served by **Deployments**, databases require **StatefulSets**, node-level agents belong in
**DaemonSets**, one-time work should use **Jobs**, and recurring work belongs in **CronJobs**. Choosing the correct
workload is an essential production skill and a frequent interview topic.

______________________________________________________________________

# Next

[10-production-kubernetes.md](10-production-kubernetes.md)
