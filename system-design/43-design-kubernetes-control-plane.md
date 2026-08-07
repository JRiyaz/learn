# Advanced Distributed Systems – Designing Kubernetes Control Plane

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand how Kubernetes Control Plane works internally, how Pods are scheduled, how desired state is maintained, and how Kubernetes achieves fault tolerance and scalability.

______________________________________________________________________

# Introduction

Most developers

know

how to use

Kubernetes.

Few understand

how Kubernetes

actually works.

This topic

is becoming

increasingly common

for

Senior Backend,

Platform,

and

Cloud Engineer

interviews.

The biggest idea

behind Kubernetes is

```
Desired State

↓

Actual State

↓

Continuously Reconciled
```

______________________________________________________________________

# What Is Kubernetes?

Kubernetes

is a

Container Orchestration

platform.

Responsibilities

include

- Scheduling containers
- Self-healing
- Service discovery
- Scaling
- Rolling deployments
- Secret management
- Configuration
- Networking

______________________________________________________________________

# Control Plane

Interview favorite.

The Control Plane

manages

the cluster.

```
                Control Plane

        ┌──────────┬──────────┐

        ▼          ▼          ▼

    API Server   Scheduler   Controller

        │

        ▼

        etcd
```

______________________________________________________________________

# Worker Nodes

Worker nodes

run

containers.

```
Worker

↓

Kubelet

↓

Container Runtime

↓

Pods
```

______________________________________________________________________

# High-Level Architecture

```
                  kubectl

                     │

                     ▼

                API Server

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

 Scheduler   Controller Manager   etcd

        │

        ▼

     Worker Nodes

        │

        ▼

      Kubelet

        │

        ▼

     Container Runtime

        │

        ▼

        Pods
```

______________________________________________________________________

# API Server

Interview favorite.

The API Server

is

the entry point

to Kubernetes.

Everything

goes through

the API Server.

Examples

```
kubectl apply

↓

API Server
```

```
kubectl get pods

↓

API Server
```

______________________________________________________________________

# Responsibilities

- Authentication
- Authorization
- Validation
- Admission Control
- API processing
- Persistence

______________________________________________________________________

# etcd

Interview favorite.

etcd

is

Kubernetes'

distributed

key-value database.

Stores

- Pods
- Nodes
- Deployments
- Secrets
- ConfigMaps
- Services

Everything

about

cluster state.

______________________________________________________________________

# Why etcd?

Need

Strong Consistency.

Cluster state

must remain

correct.

etcd

uses

```
Raft
```

for consensus.

______________________________________________________________________

# Desired State

Example

Deployment

```
Replicas

=

3
```

Desired state

is

```
3 Pods
```

______________________________________________________________________

# Actual State

Suppose

one Pod

crashes.

Actual state

becomes

```
2 Pods
```

______________________________________________________________________

# Reconciliation Loop

Interview favorite.

Controller

continuously checks

```
Desired

↓

Actual

↓

Different?

↓

Fix
```

This is

the heart

of Kubernetes.

______________________________________________________________________

# Controller Manager

Contains

multiple

controllers.

Examples

- Deployment Controller
- ReplicaSet Controller
- Node Controller
- Job Controller
- Namespace Controller

Each

maintains

its own

desired state.

______________________________________________________________________

# Deployment Controller

Example

Desired

```
5 Pods
```

Current

```
3 Pods
```

Controller

creates

```
2 New Pods
```

Automatically.

______________________________________________________________________

# Scheduler

Interview favorite.

Pods

start

without

a node.

Scheduler

chooses

where

they run.

```
Pending Pod

↓

Scheduler

↓

Worker Node
```

______________________________________________________________________

# Scheduling Factors

Scheduler considers

- CPU
- Memory
- Affinity
- Taints
- Tolerations
- Node labels
- Resource requests
- Resource limits

______________________________________________________________________

# Kubelet

Every worker

runs

Kubelet.

Responsibilities

- Watch assigned Pods
- Start containers
- Stop containers
- Report status

______________________________________________________________________

# Container Runtime

Examples

- containerd
- CRI-O

The runtime

actually starts

containers.

______________________________________________________________________

# Pod Lifecycle

```
Pending

↓

Running

↓

Succeeded

or

Failed
```

______________________________________________________________________

# Creating A Pod

```
kubectl apply

↓

API Server

↓

etcd

↓

Scheduler

↓

Node

↓

Kubelet

↓

Container Runtime

↓

Running Pod
```

______________________________________________________________________

# Services

Pods

have

changing IPs.

Services

provide

stable networking.

```
Service

↓

Stable IP

↓

Pods
```

______________________________________________________________________

# kube-proxy

Runs

on every node.

Handles

network routing

between

Services

and

Pods.

______________________________________________________________________

# ReplicaSet

Guarantees

the correct

number

of Pods.

Example

```
Desired

↓

3 Pods
```

If

one Pod dies

ReplicaSet

creates

another.

______________________________________________________________________

# Horizontal Pod Autoscaler

Interview favorite.

Automatically

scales Pods.

Example

```
CPU

80%

↓

Scale

3

↓

6 Pods
```

______________________________________________________________________

# Cluster Autoscaler

Adds

or removes

worker nodes.

```
Pods Pending

↓

New Node
```

______________________________________________________________________

# Rolling Update

Interview favorite.

Suppose

Deployment

changes

from

Version 1

to

Version 2.

Kubernetes

updates

Pods

gradually.

```
V1

↓

V1 + V2

↓

V2
```

No downtime.

______________________________________________________________________

# Rollback

Suppose

deployment fails.

```
Version 2

↓

Rollback

↓

Version 1
```

Automatic

or

manual.

______________________________________________________________________

# Self Healing

Suppose

container crashes.

```
Crash

↓

Kubelet

↓

Restart
```

Suppose

node dies.

```
Node Down

↓

Controller

↓

New Pods

On Another Node
```

______________________________________________________________________

# Health Checks

Interview favorite.

Types

```
Liveness Probe
```

```
Readiness Probe
```

```
Startup Probe
```

______________________________________________________________________

# Liveness

Checks

whether

container

should restart.

______________________________________________________________________

# Readiness

Checks

whether

container

can receive

traffic.

______________________________________________________________________

# Startup Probe

Useful

for

slow-starting

applications.

Prevents

premature

restarts.

______________________________________________________________________

# Secrets

Sensitive data

is stored

inside

```
Secret
```

Examples

- Passwords
- API Keys
- Tokens

______________________________________________________________________

# ConfigMaps

Store

configuration

outside

containers.

Example

```
DATABASE_URL
```

______________________________________________________________________

# Networking

Every Pod

gets

its own IP.

Pods

communicate

directly.

Services

provide

stable endpoints.

______________________________________________________________________

# Ingress

Interview favorite.

External traffic

enters

through

Ingress.

```
Internet

↓

Ingress

↓

Service

↓

Pods
```

______________________________________________________________________

# Namespaces

Provide

logical isolation.

Example

```
Production
```

```
Development
```

```
Testing
```

______________________________________________________________________

# RBAC

Role-Based

Access Control.

Defines

who

can perform

which actions.

______________________________________________________________________

# Monitoring

Monitor

- Pod restarts
- Node health
- CPU
- Memory
- API latency
- Scheduling failures
- etcd latency

______________________________________________________________________

# Failure Scenarios

## API Server Failure

Deploy

multiple

API Servers

behind

a Load Balancer.

______________________________________________________________________

## etcd Failure

Restore

from

replicas

or backups.

Because

etcd

stores

cluster state,

protecting it

is critical.

______________________________________________________________________

## Scheduler Failure

Pending Pods

cannot

be scheduled,

but

running Pods

continue operating.

Run

multiple schedulers

or

highly available

control-plane components.

______________________________________________________________________

## Worker Failure

Pods

are recreated

on

healthy nodes.

______________________________________________________________________

## Kubelet Failure

Node

is marked

```
Not Ready
```

Pods

are eventually

rescheduled.

______________________________________________________________________

# High Availability Control Plane

```
            Load Balancer

                 │

     ┌───────────┼───────────┐

     ▼           ▼           ▼

 API Server API Server API Server

     │           │           │

     └───────────┼───────────┘

                 ▼

               etcd Cluster
```

______________________________________________________________________

# Common Interview Questions

## Why does Kubernetes use etcd?

etcd provides a strongly consistent distributed key-value store for all cluster state. It uses the Raft consensus
algorithm to maintain correctness during failures.

______________________________________________________________________

## What does the Scheduler do?

The Scheduler assigns pending Pods to appropriate worker nodes by evaluating available resources, scheduling policies,
affinity rules, taints, tolerations, and other constraints.

______________________________________________________________________

## What is the reconciliation loop?

Controllers continuously compare the desired state stored in etcd with the actual cluster state. If differences exist,
they take actions to restore the desired state.

______________________________________________________________________

## Why do Pods need Services?

Pod IP addresses are not stable across restarts. Services provide stable networking and load balancing for groups of
Pods.

______________________________________________________________________

## What is the difference between Liveness and Readiness probes?

Liveness determines whether a container should be restarted. Readiness determines whether a container is ready to
receive traffic.

______________________________________________________________________

# Common Mistakes

## Thinking Scheduler Starts Containers

Scheduler

only selects

a node.

Kubelet

starts

containers.

______________________________________________________________________

## Ignoring etcd

Everything

about

cluster state

lives

inside

etcd.

______________________________________________________________________

## Confusing Deployment And ReplicaSet

Deployment

manages

ReplicaSets.

ReplicaSets

manage

Pods.

______________________________________________________________________

## No Health Probes

Always

configure

appropriate probes.

______________________________________________________________________

## Single Control Plane

Use

high availability

for

production clusters.

______________________________________________________________________

# Best Practices

✅ Run multiple API Servers.

✅ Protect etcd with backups.

✅ Configure liveness and readiness probes.

✅ Use rolling updates.

✅ Enable autoscaling where appropriate.

✅ Monitor control-plane health.

✅ Keep the control plane highly available.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the most important concept in Kubernetes?

### Answer

The reconciliation loop. Controllers continuously compare the desired state with the actual state and automatically take
corrective actions to converge the system.

______________________________________________________________________

## Question

Why is etcd critical?

### Answer

etcd is the source of truth for the Kubernetes cluster. Losing etcd means losing cluster state unless backups or
replicas are available.

______________________________________________________________________

## Question

What happens when a node crashes?

### Answer

The Node Controller marks the node as unavailable. The scheduler and controllers recreate affected Pods on healthy nodes
according to the desired state.

______________________________________________________________________

# Practice Exercise

Design

the Kubernetes

Control Plane.

Explain

1. API Server
1. etcd
1. Scheduler
1. Controllers
1. Kubelet
1. Pod lifecycle
1. Services
1. Rolling updates
1. Autoscaling
1. High availability
1. Failure recovery
1. Trade-offs

Present

your solution

within

60 minutes,

similar to

a Senior Platform Engineer

or

Senior Backend Engineer

System Design interview.

______________________________________________________________________

# Summary

The Kubernetes Control Plane is one of the most important distributed systems to understand for senior backend and
platform engineering roles.

A strong solution should demonstrate

- API Server
- etcd
- Scheduler
- Controller Manager
- Reconciliation loop
- Kubelet
- Services
- Rolling updates
- Autoscaling
- High availability
- Monitoring
- Trade-off analysis

Mastering the Kubernetes Control Plane prepares you for interviews at cloud providers, platform engineering teams,
DevOps-focused organizations, and companies building large-scale containerized infrastructure.

______________________________________________________________________

# Next

[44. Senior Behavioral Interviews](44-senior-behavioral-interviews.md)
