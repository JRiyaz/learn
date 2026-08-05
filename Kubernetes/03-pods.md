# 03-pods.md

# Pods - The Smallest Deployable Unit in Kubernetes

> **🎯 Pods are the foundation of Kubernetes.**
>
> Beginners often think:
>
> > "Docker runs Containers, so Kubernetes must also run Containers."
>
> That's **not true**.
>
> Kubernetes **does not deploy Containers directly**.
>
> It deploys **Pods**.
>
> Understanding **why Pods exist** is one of the most important Kubernetes concepts.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–40 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers ask Pod questions to evaluate whether you understand:

- Kubernetes fundamentals
- Why Pods exist
- Container lifecycle
- Networking
- Shared storage
- Health checks
- Multi-container design
- Sidecar pattern

This knowledge is required before understanding:

- Deployments
- Services
- Autoscaling
- StatefulSets
- Jobs

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should be able to answer:

- What is a Pod?
- Why doesn't Kubernetes run Containers directly?
- Can a Pod contain multiple Containers?
- How do Containers inside a Pod communicate?
- When should multiple Containers share a Pod?
- What are Init Containers?
- What are Sidecar Containers?
- What are Liveness, Readiness, and Startup Probes?

______________________________________________________________________

# Before Kubernetes

Docker deployment

```text
Docker

↓

Container

↓

FastAPI
```

Simple.

One application.

One container.

______________________________________________________________________

# Kubernetes Changes the Model

Instead of

```text
Container
```

Kubernetes introduces

```text
Pod

↓

Container(s)
```

Notice

Pods sit **above** containers.

______________________________________________________________________

# What Is a Pod?

The official definition says:

> "A Pod is the smallest deployable unit in Kubernetes."

That's correct,

but not intuitive.

A better definition is:

> **A Pod is a wrapper around one or more tightly related containers.**

Think of it as a **small execution environment**.

______________________________________________________________________

# Backend Engineering Analogy

Imagine your backend service.

It needs:

- FastAPI
- Logging Agent
- Monitoring Agent

These components always work together.

Instead of deploying them separately,

Kubernetes groups them into

one Pod.

______________________________________________________________________

# Visual

```text
            Pod

   +---------------------+

      FastAPI

      Logging Agent

      Metrics Agent

   +---------------------+
```

The Pod owns:

- Networking
- Storage
- Lifecycle

______________________________________________________________________

# Why Not Run Containers Directly?

Excellent interview question.

Suppose Kubernetes deployed containers directly.

Questions arise.

- Which IP belongs to the application?
- How do related containers communicate?
- How do they share files?
- How do they start together?
- How do they stop together?

Managing each container independently becomes difficult.

Pods solve these problems.

______________________________________________________________________

# Think of a Pod as a Small Machine

Imagine

```text
Virtual Machine
```

Inside

```
Multiple Processes
```

Similarly

```text
Pod

↓

Multiple Containers
```

Containers behave like processes running on the same machine.

______________________________________________________________________

# Single Container Pod

Most Pods contain

exactly one container.

Example

```text
Pod

↓

FastAPI Container
```

This is by far the most common deployment.

______________________________________________________________________

# Multi-Container Pod

Sometimes

multiple containers

must always stay together.

Example

```text
Pod

↓

FastAPI

↓

Log Collector

↓

Metrics Exporter
```

All three share

the same lifecycle.

______________________________________________________________________

# What Does a Pod Share?

Containers inside the same Pod share several resources.

______________________________________________________________________

## Shared Network

Every Pod gets

exactly one IP.

Example

```text
Pod IP

10.1.2.15
```

Containers

```text
FastAPI

↓

localhost
```

```text
Logger

↓

localhost
```

They communicate using

```
localhost
```

No Service required.

______________________________________________________________________

# Backend Analogy

Imagine two processes

running on your laptop.

One process talks to another using

```text
localhost:8000
```

Containers inside the same Pod behave similarly.

______________________________________________________________________

# Shared Storage

Containers may also share volumes.

Example

```text
FastAPI

↓

Writes Logs
```

Shared Volume

↓

```text
Logging Agent

↓

Reads Logs
```

No network required.

______________________________________________________________________

# Shared Lifecycle

Containers inside a Pod

Start together.

Restart together.

Stop together.

Deleted together.

______________________________________________________________________

# Pod Lifecycle

A Pod doesn't immediately become Running.

Typical lifecycle

```text
Pending

↓

ContainerCreating

↓

Running

↓

Succeeded

or

Failed
```

______________________________________________________________________

## Pending

Pod accepted.

Waiting for scheduling.

______________________________________________________________________

## ContainerCreating

Images downloading.

Volumes mounting.

Network setup.

______________________________________________________________________

## Running

Application started.

Healthy.

Serving traffic.

______________________________________________________________________

## Succeeded

Job finished successfully.

Common for Jobs.

______________________________________________________________________

## Failed

Application crashed.

______________________________________________________________________

# Init Containers

Sometimes

your application

cannot start immediately.

Example

Need to

- Wait for Database
- Download Configurations
- Run Database Migration

Before FastAPI starts.

______________________________________________________________________

Instead of writing startup scripts,

Kubernetes provides

```
Init Containers
```

______________________________________________________________________

# Execution Order

```text
Init Container

↓

Init Container

↓

Main Container
```

Main application waits

until every Init Container succeeds.

______________________________________________________________________

# Example

```text
Migration Container

↓

Database Ready

↓

FastAPI Starts
```

______________________________________________________________________

# Sidecar Containers

A Sidecar is

a helper container

running beside your application.

______________________________________________________________________

Example

```text
Pod

↓

FastAPI

↓

Fluent Bit

↓

Prometheus Exporter
```

FastAPI handles requests.

Fluent Bit collects logs.

Prometheus exports metrics.

______________________________________________________________________

# Why Sidecars?

Without Sidecars,

every application

must implement

logging,

monitoring,

security.

With Sidecars,

those responsibilities become reusable.

______________________________________________________________________

# Real Production Example

```text
Pod

+----------------------------------+

FastAPI

↓

Writes Logs

↓

Shared Volume

↓

Fluent Bit

↓

ElasticSearch

+----------------------------------+
```

FastAPI knows nothing

about Elasticsearch.

Cleaner architecture.

______________________________________________________________________

# Pod Networking

Every Pod receives

its own IP.

Example

```text
Pod A

10.1.1.2
```

```text
Pod B

10.1.1.5
```

Pods communicate directly.

Later,

we'll learn

Services

which provide stable networking.

______________________________________________________________________

# Pod Is Ephemeral

This is one of the most important ideas.

Pods are

**temporary**.

Suppose

```text
Pod

↓

Crash
```

Kubernetes doesn't repair it.

Instead

```text
Delete Old Pod

↓

Create New Pod
```

New Pod

↓

New IP.

This is why

applications should never depend on Pod IPs.

______________________________________________________________________

# Health Checks

Question

How does Kubernetes know

whether your application is healthy?

Answer

```
Probes
```

______________________________________________________________________

# Liveness Probe

Question

> Is the application alive?

If

No

↓

Restart container.

______________________________________________________________________

Example

```text
FastAPI

↓

Deadlock

↓

Liveness Fails

↓

Restart
```

______________________________________________________________________

# Readiness Probe

Question

> Can this Pod receive traffic?

If

No

↓

Keep Pod running.

But

Don't send requests.

______________________________________________________________________

Example

```text
Application

↓

Loading Cache

↓

Not Ready

↓

Traffic Blocked
```

Once ready

↓

Traffic begins.

______________________________________________________________________

# Startup Probe

Question

> Has the application finished starting?

Useful for

slow applications.

Without Startup Probe,

Liveness might kill

applications

before startup finishes.

______________________________________________________________________

# Probe Comparison

| Probe | Purpose |
|--------|----------|
| Liveness | Restart unhealthy application |
| Readiness | Decide if traffic should be sent |
| Startup | Allow slow startup safely |

______________________________________________________________________

# Example Flow

```text
Pod Starts

↓

Startup Probe

↓

Readiness Probe

↓

Receives Traffic

↓

Liveness Probe

↓

Restart if Needed
```

______________________________________________________________________

# Production YAML Example

```yaml
apiVersion: v1

kind: Pod

metadata:
  name: fastapi-pod

spec:
  containers:
    - name: api
      image: my-fastapi:1.0

      ports:
        - containerPort: 8000

      livenessProbe:
        httpGet:
          path: /health
          port: 8000

      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
```

We won't memorize YAML now.

Focus on understanding

what each probe does.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Thinking Pods are permanent.

Pods are disposable.

______________________________________________________________________

## Mistake 2

Using Pod IPs directly.

Pod IPs change.

Services provide stable addresses.

______________________________________________________________________

## Mistake 3

Putting unrelated applications into one Pod.

Example

```text
User Service

+

Redis
```

Bad idea.

Different lifecycles.

Deploy separately.

______________________________________________________________________

## Mistake 4

Confusing Containers with Pods.

Containers run inside Pods.

Pods run inside Nodes.

______________________________________________________________________

## Mistake 5

Using Liveness when Readiness is needed.

Liveness

↓

Restart.

Readiness

↓

Stop traffic.

Very different.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A Pod is the smallest deployable unit in Kubernetes. It wraps one or more closely related containers that share networking, storage, and lifecycle. Most Pods contain a single application container, but multi-container Pods are useful when helper containers such as log collectors or metrics exporters must always run alongside the main application. Kubernetes uses health probes to determine whether a Pod should receive traffic or be restarted."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does Kubernetes use Pods instead of Containers?**

Pods provide shared networking, storage, and lifecycle management, making related containers behave as a single
deployable unit.

______________________________________________________________________

**Q. Can a Pod have multiple containers?**

Yes.

The containers should be tightly coupled and always run together.

______________________________________________________________________

**Q. Can two Pods communicate using localhost?**

No.

Only containers inside the same Pod share `localhost`.

Different Pods communicate over the network.

______________________________________________________________________

**Q. When should I use multiple containers in one Pod?**

For helper containers such as logging agents, proxies, metrics exporters, or security sidecars.

______________________________________________________________________

**Q. What happens if a Pod crashes?**

Kubernetes creates a new Pod rather than repairing the old one.

______________________________________________________________________

# Pattern Summary

| Concept | Purpose |
|----------|---------|
| Pod | Smallest deployable unit |
| Container | Runs inside a Pod |
| Single Container Pod | Most common deployment |
| Multi-Container Pod | Closely related containers |
| Init Container | Runs before the application |
| Sidecar | Helper container |
| Shared Network | Same Pod IP |
| Shared Storage | Shared Volumes |
| Liveness Probe | Restart unhealthy container |
| Readiness Probe | Control traffic |
| Startup Probe | Handle slow startup |

______________________________________________________________________

# Quick Revision

- Kubernetes deploys Pods, not containers.
- A Pod is a wrapper around one or more containers.
- Most Pods contain exactly one application container.
- Containers inside a Pod share networking, storage, and lifecycle.
- Every Pod receives its own IP address.
- Pod IPs are temporary and should not be relied upon.
- Init Containers complete before the main application starts.
- Sidecars provide supporting functionality like logging and monitoring.
- Liveness checks if the application should be restarted.
- Readiness determines whether traffic should be sent to the Pod.
- Startup Probes prevent premature restarts during slow initialization.

______________________________________________________________________

# Key Takeaway

The biggest mindset shift in Kubernetes is:

> **You never deploy a container—you deploy a Pod.**

A Pod is more than just a container. It is a complete execution environment with its own networking, storage, lifecycle,
and health management. Once you understand Pods, the rest of Kubernetes objects—Deployments, Services, and
Autoscaling—become much easier because they all manage or interact with Pods.

______________________________________________________________________

# Next

[04-deployments-and-replicasets.md](04-deployments-and-replicasets.md)
