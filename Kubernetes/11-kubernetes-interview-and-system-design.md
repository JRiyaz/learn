# 11-kubernetes-interview-and-system-design.md

# Kubernetes Interview & System Design

> **🎯 This is the final Kubernetes chapter before Helm.**
>
> Up to this point, you've learned every major Kubernetes concept.
>
> Now let's connect everything together the way it appears in **real production systems** and **Senior Backend interviews**.
>
> This chapter focuses on:
>
> - How Kubernetes fits into a backend architecture
> - Real production deployments
> - Interview questions
> - Common debugging scenarios
> - End-to-end request flow

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 45–60 minutes |
| Revision Time | 30 minutes |

______________________________________________________________________

# Why Interviewers Ask This

By 5+ years of experience, interviewers expect more than Kubernetes definitions.

They expect you to explain:

- How your application is deployed
- How traffic flows
- How scaling works
- How failures are handled
- How you debug production issues
- Why certain Kubernetes objects are used

This chapter brings together everything you've learned.

______________________________________________________________________

# A Typical Production Architecture

Imagine an e-commerce platform.

```text
                      Internet
                          │
                          ▼
                 Cloud Load Balancer
                          │
                          ▼
                      Ingress
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 User Service        Order Service      Payment Service
 (Deployment)        (Deployment)       (Deployment)
      │                   │                   │
      ▼                   ▼                   ▼
   Service             Service            Service
      │                   │                   │
      └──────────────┬────┴──────────────┬────┘
                     ▼                   ▼
                  Redis              PostgreSQL
               (StatefulSet)      (Managed DB / StatefulSet)
                     │
                     ▼
                   Kafka
               (StatefulSet)
```

Every component we've learned now fits together.

______________________________________________________________________

# End-to-End Request Flow

Suppose a user opens:

```
https://shop.company.com/orders
```

What happens?

______________________________________________________________________

## Step 1

Browser sends request.

```text
Browser

↓

Internet
```

______________________________________________________________________

## Step 2

Cloud Load Balancer receives it.

```text
AWS ALB

or

Azure Load Balancer
```

↓

Ingress.

______________________________________________________________________

## Step 3

Ingress examines:

- Host
- Path

Rule

```text
/orders

↓

Order Service
```

______________________________________________________________________

## Step 4

Service receives request.

Service selects healthy Pods.

```text
Service

↓

Pod A

Pod B

Pod C
```

Load balancing happens automatically.

______________________________________________________________________

## Step 5

FastAPI processes request.

Example

```python
GET /orders/123
```

↓

Business Logic.

______________________________________________________________________

## Step 6

Application calls

```text
PostgreSQL

Redis

Kafka
```

______________________________________________________________________

## Step 7

Response

travels back

through

```text
Pod

↓

Service

↓

Ingress

↓

Load Balancer

↓

Browser
```

______________________________________________________________________

# Complete Request Flow

```text
Browser

↓

Cloud Load Balancer

↓

Ingress

↓

Service

↓

FastAPI Pod

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Response
```

This diagram alone answers many interview questions.

______________________________________________________________________

# Where Every Kubernetes Object Fits

| Object | Responsibility |
|---------|----------------|
| Pod | Runs application |
| Deployment | Keeps Pods running |
| ReplicaSet | Maintains replica count |
| Service | Stable networking |
| Ingress | External routing |
| ConfigMap | Configuration |
| Secret | Sensitive configuration |
| PVC | Persistent storage |
| StatefulSet | Databases & Kafka |
| HPA | Scale Pods |
| Cluster Autoscaler | Scale Nodes |

______________________________________________________________________

# Production Scenario 1

## One Pod Crashes

Architecture

```text
Deployment

↓

3 Pods
```

One Pod crashes.

Question

Does the application stop?

No.

Flow

```text
Pod

↓

Crash

↓

ReplicaSet notices

↓

New Pod created

↓

Service routes traffic
```

Users usually don't notice.

______________________________________________________________________

# Production Scenario 2

## Traffic Suddenly Increases

Current

```text
3 Pods
```

CPU

```
95%
```

Flow

```text
Metrics

↓

HPA

↓

Deployment

↓

10 Pods
```

If nodes are full

↓

Cluster Autoscaler

↓

Adds Worker Node.

______________________________________________________________________

# Production Scenario 3

## New Release

Current

```
v1
```

Need

```
v2
```

Deployment performs

Rolling Update.

```text
V1

↓

V2

↓

V2

↓

V2
```

No downtime.

______________________________________________________________________

# Production Scenario 4

## Bug in Version 2

Deployment history

already exists.

Rollback.

```text
V2

↓

Rollback

↓

V1
```

Usually

seconds.

______________________________________________________________________

# Production Scenario 5

## Database Restart

PostgreSQL Pod

↓

Restart.

StatefulSet

↓

Same Pod Name

↓

Same PVC

↓

Same Disk

↓

Data preserved.

______________________________________________________________________

# Production Scenario 6

## Worker Node Failure

Worker Node

↓

Power failure.

Pods disappear.

Scheduler

↓

New Node

↓

ReplicaSet

↓

Pods recreated.

______________________________________________________________________

# Debugging Workflow

Suppose users report:

```
API is down.
```

Where do you start?

______________________________________________________________________

## Step 1

Check Pods.

```bash
kubectl get pods
```

Are they Running?

______________________________________________________________________

## Step 2

Describe Pod.

```bash
kubectl describe pod
```

Check

- Events
- Scheduling
- ImagePullBackOff
- OOMKilled

______________________________________________________________________

## Step 3

Check Logs.

```bash
kubectl logs
```

Application exceptions?

Database errors?

______________________________________________________________________

## Step 4

Check Service.

```bash
kubectl get service
```

Correct selector?

Correct endpoints?

______________________________________________________________________

## Step 5

Check Ingress.

Routing issue?

TLS issue?

Wrong hostname?

______________________________________________________________________

## Step 6

Check Metrics.

CPU?

Memory?

Latency?

______________________________________________________________________

## Step 7

Check Database.

Connection pool?

Slow queries?

Locks?

______________________________________________________________________

# Common Production Issues

## CrashLoopBackOff

Cause

Application crashes repeatedly.

Typical reasons

- Wrong environment variables
- Missing Secret
- Code exception
- Database unavailable

______________________________________________________________________

## ImagePullBackOff

Cause

Image can't be downloaded.

Check

- Repository
- Tag
- Registry authentication

______________________________________________________________________

## Pending

Pod waiting.

Possible reasons

- No CPU
- No Memory
- No available Worker Node
- PVC not bound

______________________________________________________________________

## OOMKilled

Application exceeded

memory limit.

Increase memory

or

fix memory leak.

______________________________________________________________________

# Real Backend Example

Suppose

FastAPI

uses

Redis

Kafka

PostgreSQL.

Deployment

```text
FastAPI

↓

Deployment

↓

Service

↓

Ingress
```

Configuration

```text
ConfigMap

↓

Redis Host

Kafka Host
```

Sensitive Data

```text
Secrets

↓

Database Password

JWT Secret
```

Persistence

```text
PostgreSQL

↓

StatefulSet

↓

PVC
```

Scaling

```text
HPA

↓

Deployment
```

Observability

```text
Prometheus

Grafana

Loki
```

This is a common production architecture.

______________________________________________________________________

# Senior Backend Interview Questions

______________________________________________________________________

## Q1

Why use Kubernetes instead of Docker?

### Answer

Docker packages applications into containers.

Kubernetes manages those containers by providing orchestration features such as self-healing, scaling, service
discovery, rolling updates, and scheduling across multiple machines.

______________________________________________________________________

## Q2

Why shouldn't applications use Pod IPs?

### Answer

Pods are ephemeral.

Whenever a Pod is recreated, it receives a new IP address.

Services provide stable networking.

______________________________________________________________________

## Q3

What's the difference between a Deployment and a StatefulSet?

### Answer

Deployments manage stateless workloads.

StatefulSets provide stable identities, ordered deployment, and persistent storage for stateful applications.

______________________________________________________________________

## Q4

How does Kubernetes perform self-healing?

### Answer

The Controller Manager continuously compares the desired state with the actual state. If Pods disappear, the ReplicaSet
creates replacements automatically.

______________________________________________________________________

## Q5

How does Kubernetes scale applications?

### Answer

Horizontal Pod Autoscaler increases or decreases the number of Pods based on metrics such as CPU utilization. If cluster
capacity is insufficient, the Cluster Autoscaler can add Worker Nodes.

______________________________________________________________________

## Q6

How do users reach your FastAPI application?

### Answer

Browser → Cloud Load Balancer → Ingress → Service → FastAPI Pod.

______________________________________________________________________

## Q7

Where should configuration be stored?

### Answer

Use ConfigMaps for non-sensitive configuration and Secrets for passwords, API keys, and certificates.

______________________________________________________________________

## Q8

How do you debug a failing Pod?

### Answer

Check Pod status, describe the Pod, inspect logs, review events, verify resource usage, and confirm networking through
Services and Ingress.

______________________________________________________________________

# Production Best Practices

## Use Deployments

Don't create Pods directly.

______________________________________________________________________

## Keep Applications Stateless

Store session data in Redis.

Store files in object storage.

Store database data in persistent storage.

______________________________________________________________________

## Use Health Probes

Always configure:

- Startup
- Readiness
- Liveness

______________________________________________________________________

## Configure Requests & Limits

Prevent resource starvation.

______________________________________________________________________

## Use Multiple Replicas

Avoid single points of failure.

______________________________________________________________________

## Externalize Configuration

Use ConfigMaps and Secrets.

______________________________________________________________________

## Centralize Logging

Never rely on Pod filesystem logs.

______________________________________________________________________

## Monitor Everything

Prometheus

-

Grafana

-

Alerts.

______________________________________________________________________

## Use Rolling Updates

Avoid downtime during deployments.

______________________________________________________________________

## Keep Databases Separate

Prefer managed databases when practical.

If running databases inside Kubernetes, use StatefulSets with persistent storage.

______________________________________________________________________

# System Design Perspective

When discussing Kubernetes during a system design interview, don't start with Pods.

Instead, explain:

1. External traffic enters through a Load Balancer.
1. Ingress routes requests.
1. Services provide stable networking.
1. Deployments manage stateless applications.
1. StatefulSets manage databases and messaging systems.
1. HPA scales Pods.
1. Cluster Autoscaler scales infrastructure.
1. Monitoring and logging provide observability.

This demonstrates architectural thinking rather than object memorization.

______________________________________________________________________

# Complete Kubernetes Cheat Sheet

```text
Deployment

↓

ReplicaSet

↓

Pods

↓

Service

↓

Ingress

↓

Load Balancer

↓

Internet
```

Storage

```text
Pod

↓

PVC

↓

PV

↓

StorageClass

↓

Cloud Disk
```

Scaling

```text
HPA

↓

Pods

↓

Cluster Autoscaler

↓

Nodes
```

Observability

```text
Logs

Metrics

Traces
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Explaining Kubernetes as just "container management."

It is an orchestration platform that continuously maintains the desired state.

______________________________________________________________________

## Mistake 2

Confusing Services with Ingress.

Ingress handles external HTTP/HTTPS routing.

Services provide stable networking inside the cluster.

______________________________________________________________________

## Mistake 3

Running stateful databases as simple Deployments.

Prefer StatefulSets when stable identity and persistent storage are required.

______________________________________________________________________

## Mistake 4

Ignoring observability.

Production systems need logs, metrics, traces, and alerts.

______________________________________________________________________

## Mistake 5

Thinking Kubernetes solves everything automatically.

It provides powerful primitives, but applications still need good architecture, monitoring, backups, and operational
practices.

______________________________________________________________________

# Final Kubernetes Summary

| Topic | Key Idea |
|--------|----------|
| Cluster | Group of machines |
| Control Plane | Makes decisions |
| Worker Node | Runs Pods |
| Pod | Smallest deployable unit |
| Deployment | Manages stateless applications |
| ReplicaSet | Maintains replica count |
| Service | Stable networking |
| Ingress | External routing |
| ConfigMap | Non-sensitive configuration |
| Secret | Sensitive configuration |
| PVC | Requests storage |
| StatefulSet | Stateful applications |
| DaemonSet | One Pod per node |
| Job | One-time work |
| CronJob | Scheduled work |
| HPA | Scale Pods |
| Cluster Autoscaler | Scale Nodes |

______________________________________________________________________

# Quick Revision

- Kubernetes manages the desired state of applications.
- Deployments are used for stateless services.
- StatefulSets are used for databases and messaging systems.
- Services provide stable networking.
- Ingress exposes HTTP/HTTPS traffic.
- ConfigMaps and Secrets separate configuration from code.
- PVCs provide persistent storage.
- HPA scales Pods.
- Monitoring, logging, and tracing are essential for production.
- Debug systematically: Pods → Logs → Services → Ingress → Metrics.

______________________________________________________________________

# Key Takeaway

The most important thing to remember about Kubernetes is:

> **Kubernetes is not a collection of YAML files—it's a distributed control system that continuously works to keep your applications healthy, scalable, and available.**

As a senior backend engineer, your goal isn't just to know what a Pod or Service is. It's to understand **how all the
Kubernetes building blocks work together** to run real production systems. Once you can explain the end-to-end request
flow, deployment lifecycle, scaling strategy, and debugging process, you're well prepared for most senior backend
Kubernetes interview discussions.

______________________________________________________________________

# Next

[12-helm-package-manager.md](12-helm-package-manager.md)
