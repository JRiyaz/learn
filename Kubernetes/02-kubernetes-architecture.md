# 02-kubernetes-architecture.md

# Kubernetes Architecture

> **🎯 This is the most important conceptual chapter in Kubernetes.**
>
> If you truly understand this chapter, almost every Kubernetes object (Pods, Deployments, Services, etc.) will make sense.
>
> Don't memorize the components.
>
> Instead, understand **how they work together**.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–40 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Most Kubernetes interview questions eventually reduce to one question:

> **"What happens internally when I deploy an application?"**

If you can explain that flow, you've demonstrated a strong understanding of Kubernetes.

Interviewers use this topic to evaluate whether you understand:

- Cluster architecture
- Control Plane
- Worker Nodes
- Scheduling
- Desired State
- API-driven architecture
- Self-healing
- Kubernetes internals

______________________________________________________________________

# Learning Goal

By the end of this lesson, you should be able to answer:

- What is a Kubernetes Cluster?
- What is the Control Plane?
- What are Worker Nodes?
- What is the API Server?
- What is etcd?
- What is Scheduler?
- What is Controller Manager?
- What is kubelet?
- What is kube-proxy?
- What happens after running

```bash
kubectl apply -f deployment.yaml
```

______________________________________________________________________

# Before Learning the Architecture

Imagine a company.

```
CEO

↓

Managers

↓

Employees
```

Employees don't make company-wide decisions.

Managers coordinate work.

The CEO defines company goals.

Kubernetes works similarly.

______________________________________________________________________

# Kubernetes Is a Distributed System

Unlike Docker,

which usually runs on one machine,

Kubernetes manages many machines.

Example

```text
                Kubernetes Cluster

             +-----------------------+
             |  Many Computers       |
             |  Working Together     |
             +-----------------------+
```

These computers have different responsibilities.

______________________________________________________________________

# What Is a Cluster?

A Cluster is simply

> **A group of machines managed as one system.**

Example

```text
             Kubernetes Cluster

        +---------+   +---------+   +---------+
        | Node A  |   | Node B  |   | Node C  |
        +---------+   +---------+   +---------+
```

Instead of thinking

```
Three Computers
```

Kubernetes thinks

```
One Cluster
```

______________________________________________________________________

# High-Level Architecture

```text
                   Kubernetes Cluster

          +--------------------------------------+
          |          Control Plane               |
          |--------------------------------------|
          | API Server                           |
          | Scheduler                            |
          | Controller Manager                   |
          | etcd                                |
          +--------------------------------------+

             │             │              │

    +----------------+ +----------------+ +----------------+
    | Worker Node 1  | | Worker Node 2  | | Worker Node 3  |
    |----------------| |----------------| |----------------|
    | kubelet        | | kubelet        | | kubelet        |
    | kube-proxy     | | kube-proxy     | | kube-proxy     |
    | Pods           | | Pods           | | Pods           |
    +----------------+ +----------------+ +----------------+
```

Everything revolves around these components.

______________________________________________________________________

# Two Main Parts

Every Kubernetes cluster has only two major sections.

## Control Plane

The brain.

Makes decisions.

______________________________________________________________________

## Worker Nodes

The workers.

Run your applications.

______________________________________________________________________

Think of it like this.

```text
Brain

↓

Control Plane

Body

↓

Worker Nodes
```

______________________________________________________________________

# The Control Plane

The Control Plane never runs your application.

Instead,

it decides:

- What should run?
- Where should it run?
- How many copies?
- What if something crashes?
- What if a node dies?

Think of it as

```
Cluster Manager
```

______________________________________________________________________

# Worker Nodes

Worker Nodes actually execute your applications.

Example

```text
Worker Node

↓

Pod

↓

Container

↓

FastAPI
```

Your application never runs inside the Control Plane.

______________________________________________________________________

# Meet the Components

We'll now learn every component.

______________________________________________________________________

# 1. API Server

This is

the **front door** of Kubernetes.

Every request goes here.

Everything.

Examples

```bash
kubectl apply
```

↓

API Server

______________________________________________________________________

```bash
kubectl get pods
```

↓

API Server

______________________________________________________________________

Dashboard

↓

API Server

______________________________________________________________________

CI/CD

↓

API Server

______________________________________________________________________

Even internal Kubernetes components communicate through the API Server.

______________________________________________________________________

# Backend Engineering Analogy

Think of the API Server as

your FastAPI backend.

Clients never directly access

the database.

Instead

```text
Client

↓

FastAPI

↓

Database
```

Similarly

```text
kubectl

↓

API Server

↓

Cluster
```

______________________________________________________________________

# Responsibilities

The API Server

- Validates requests
- Authenticates users
- Authorizes operations
- Stores objects
- Returns responses

It is the central communication hub.

______________________________________________________________________

# 2. etcd

Suppose Kubernetes suddenly restarts.

How does it remember

- Pods?
- Deployments?
- Services?
- Secrets?

It stores everything in

```
etcd
```

______________________________________________________________________

# What Is etcd?

A distributed key-value database.

Think

```text
Dictionary

Key

↓

Value
```

Example

```text
Deployment

↓

3 Replicas
```

Stored inside

```
etcd
```

______________________________________________________________________

# Backend Analogy

Suppose your application uses PostgreSQL.

Without PostgreSQL,

every restart loses data.

Similarly,

without etcd,

Kubernetes forgets the entire cluster.

______________________________________________________________________

# Important Interview Fact

etcd stores

**Cluster State**

not

Application Data.

Your PostgreSQL database

should NOT live inside etcd.

______________________________________________________________________

# 3. Scheduler

Suppose you create

```text
10 Pods
```

Question

Which machine should run them?

Worker 1?

Worker 2?

Worker 3?

Scheduler decides.

______________________________________________________________________

# What Does Scheduler Consider?

- Available CPU
- Available Memory
- Node Labels
- Affinity Rules
- Taints
- Resource Requests

It chooses the best Worker Node.

______________________________________________________________________

# Visual

```text
New Pod

↓

Scheduler

↓

Node 2
```

Done.

______________________________________________________________________

# Backend Analogy

Imagine assigning customer support tickets.

Several engineers are available.

Manager chooses

the best engineer.

Scheduler works the same way.

______________________________________________________________________

# 4. Controller Manager

This is the component most beginners misunderstand.

It constantly asks

```
Reality

==

Desired State ?
```

______________________________________________________________________

Suppose

Deployment

```text
Replicas = 3
```

Current

```text
Running Pods = 2
```

Mismatch.

Controller Manager notices.

Creates

```
One More Pod
```

______________________________________________________________________

Suppose

Current

```
4 Pods
```

Desired

```
3
```

Deletes one.

______________________________________________________________________

This process is called

```
Reconciliation Loop
```

The heart of Kubernetes.

______________________________________________________________________

# Backend Analogy

Imagine your manager says

"We need exactly five backend engineers on call."

One engineer resigns.

Manager immediately finds a replacement.

Nobody waits for someone to complain.

That's exactly what the Controller Manager does.

______________________________________________________________________

# 5. kubelet

Every Worker Node has a kubelet.

Think of it as

the node's local manager.

______________________________________________________________________

Responsibilities

- Talks to API Server
- Starts Pods
- Stops Pods
- Reports Pod Health
- Runs Health Checks

______________________________________________________________________

Visual

```text
API Server

↓

kubelet

↓

Docker/containerd

↓

Container
```

______________________________________________________________________

# Backend Analogy

Suppose the Control Plane says

```
Run FastAPI
```

kubelet actually starts it.

______________________________________________________________________

# 6. kube-proxy

Pods have changing IP addresses.

Networking becomes difficult.

kube-proxy solves this.

Responsibilities

- Networking
- Service routing
- Load balancing
- Traffic forwarding

______________________________________________________________________

Example

```text
Users

↓

Service

↓

Pod A

Pod B

Pod C
```

kube-proxy routes requests.

______________________________________________________________________

# Container Runtime

Containers don't magically exist.

Someone must create them.

That's the Container Runtime.

Examples

- containerd
- CRI-O

Historically

Docker

Today,

containerd is more common.

______________________________________________________________________

# Putting Everything Together

Imagine you run

```bash
kubectl apply -f deployment.yaml
```

What actually happens?

______________________________________________________________________

# Step 1

```bash
kubectl
```

sends the Deployment manifest.

↓

API Server

______________________________________________________________________

# Step 2

API Server

- Validates YAML
- Checks permissions
- Stores desired state

↓

etcd

______________________________________________________________________

# Step 3

Controller Manager notices

```
Desired

3 Pods

Current

0 Pods
```

Need

```
3 Pods
```

______________________________________________________________________

# Step 4

Scheduler decides

```text
Pod 1

↓

Node A
```

```text
Pod 2

↓

Node B
```

```text
Pod 3

↓

Node C
```

______________________________________________________________________

# Step 5

Each kubelet receives instructions.

Starts containers.

______________________________________________________________________

# Step 6

Pods become

```
Running
```

Users can access them.

______________________________________________________________________

# Complete Flow Diagram

```text
Developer

│
│ kubectl apply
▼

API Server

│
│ Save Desired State
▼

etcd

│
│ Watch Changes
▼

Controller Manager

│
│ Need 3 Pods
▼

Scheduler

│
│ Choose Nodes
▼

kubelet

│
│ Start Containers
▼

Running Pods
```

This is the single most important diagram in Kubernetes.

______________________________________________________________________

# What Happens If a Pod Crashes?

Suppose

```text
Pod A

↓

Crash
```

kubelet reports

```
Pod Failed
```

↓

API Server updates state.

↓

Controller Manager notices

```
Desired

3

Actual

2
```

↓

Scheduler picks a node.

↓

kubelet starts a replacement Pod.

Self Healing complete.

______________________________________________________________________

# Why Kubernetes Is Called Declarative

Notice

You never wrote

```bash
start pod

restart pod

move pod

recover pod
```

Instead,

you simply declared

```
Replicas = 3
```

Kubernetes figured out

how

to make reality match that declaration.

This is called

```
Declarative Infrastructure
```

______________________________________________________________________

# Imperative vs Declarative

## Imperative

Tell the system

how.

Example

```text
Start Pod

Create Network

Restart Pod
```

______________________________________________________________________

## Declarative

Tell the system

what.

Example

```yaml
replicas: 3
```

Kubernetes figures out

how to achieve it.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Thinking the API Server runs applications.

It doesn't.

Worker Nodes do.

______________________________________________________________________

## Mistake 2

Thinking etcd stores application data.

It stores Kubernetes metadata and cluster state.

______________________________________________________________________

## Mistake 3

Confusing Scheduler with kubelet.

Scheduler chooses the node.

kubelet runs the Pod.

______________________________________________________________________

## Mistake 4

Thinking Controller Manager starts Pods.

It notices mismatches.

kubelet actually starts them.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Kubernetes follows a control-loop architecture. Every request goes through the API Server, which validates it and stores the desired state in etcd. The Controller Manager continuously compares the desired state with the actual cluster state. If changes are needed, the Scheduler selects appropriate worker nodes, and the kubelet on those nodes starts or stops Pods. kube-proxy provides networking and load balancing between Pods."

______________________________________________________________________

### Common Follow-up Questions

**Q. Which component is the brain of Kubernetes?**

The Control Plane.

______________________________________________________________________

**Q. Which component receives all requests?**

The API Server.

______________________________________________________________________

**Q. What does etcd store?**

Cluster state and Kubernetes objects.

______________________________________________________________________

**Q. Who decides where Pods run?**

The Scheduler.

______________________________________________________________________

**Q. Who actually starts the containers?**

The kubelet, using the container runtime.

______________________________________________________________________

**Q. Who keeps the desired number of Pods running?**

The Controller Manager through the reconciliation loop.

______________________________________________________________________

# Pattern Summary

| Component | Responsibility |
|-----------|----------------|
| Cluster | Collection of machines |
| Control Plane | Makes decisions |
| Worker Node | Runs applications |
| API Server | Front door of Kubernetes |
| etcd | Stores cluster state |
| Scheduler | Chooses worker nodes |
| Controller Manager | Maintains desired state |
| kubelet | Runs Pods on a node |
| kube-proxy | Networking and load balancing |
| Container Runtime | Creates containers |

______________________________________________________________________

# Quick Revision

- A Kubernetes Cluster consists of a Control Plane and Worker Nodes.
- The API Server is the entry point for every request.
- etcd stores the desired and current cluster state.
- The Controller Manager continuously reconciles desired and actual state.
- The Scheduler selects the best Worker Node for new Pods.
- kubelet runs and monitors Pods on each Worker Node.
- kube-proxy enables networking and Service load balancing.
- Kubernetes is declarative—you describe the desired state, and Kubernetes works to achieve it.
- The reconciliation loop is the core mechanism that keeps applications healthy.

______________________________________________________________________

# Key Takeaway

The biggest lesson from Kubernetes architecture is understanding that **Kubernetes is a distributed control system**.
Every component has a single responsibility:

- **API Server** receives requests.
- **etcd** remembers the cluster.
- **Controller Manager** watches for differences.
- **Scheduler** chooses where work should run.
- **kubelet** executes that work.
- **kube-proxy** connects everything together.

Once you understand this flow, the rest of Kubernetes becomes much easier because nearly every feature builds on this
architecture.

______________________________________________________________________

# Next

[03-pods.md](03-pods.md)
