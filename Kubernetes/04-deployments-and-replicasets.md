# 04-deployments-and-replicasets.md

# Deployments & ReplicaSets

> **🎯 This is where Kubernetes becomes truly powerful.**
>
> In the previous lesson, we learned that **Pods are temporary**.
>
> That naturally raises an important question:
>
> > **If Pods are temporary, who makes sure my application is always running?**
>
> The answer is:
>
> **Deployments** and **ReplicaSets**.
>
> These two Kubernetes objects are responsible for keeping your applications alive, updated, and available.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 35–45 minutes |
| Revision Time | 25 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the most frequently discussed Kubernetes topics.

Interviewers want to know whether you understand:

- Desired State
- Self Healing
- Rolling Updates
- Rollbacks
- ReplicaSets
- Deployment lifecycle
- Production deployments

This chapter forms the basis for understanding:

- Auto Scaling
- Canary Deployments
- Blue-Green Deployments
- CI/CD
- Helm

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- Why Pods should never be created directly
- What a ReplicaSet is
- What a Deployment is
- Relationship between Deployment → ReplicaSet → Pod
- Rolling Updates
- Rollbacks
- Reconciliation Loop
- Production deployment strategies

______________________________________________________________________

# The Biggest Mistake Beginners Make

Suppose you create a Pod directly.

```yaml
kind: Pod
```

Everything works.

FastAPI starts.

Users access your API.

Looks perfect.

______________________________________________________________________

Now imagine

```
Pod Crashes
```

or

```
Server Reboots
```

or

```
Someone Deletes the Pod
```

Your application disappears.

Because nothing is managing it.

______________________________________________________________________

# Real Production Analogy

Imagine hiring a backend engineer.

One engineer joins.

Everything works.

Now imagine:

```
Engineer resigns.
```

Does the company stop building software?

No.

Management hires another engineer.

The **role** remains,

even though the individual changes.

Pods work exactly the same way.

______________________________________________________________________

# Kubernetes Philosophy

Kubernetes doesn't care about

**individual Pods**.

It cares about

**the desired state**.

Example

You declare:

```text
I want

3

FastAPI Pods
```

Kubernetes continuously checks reality.

If reality differs,

it fixes it automatically.

______________________________________________________________________

# Desired State vs Actual State

Suppose

Desired

```text
3 Pods
```

Reality

```text
3 Pods
```

Everything is good.

______________________________________________________________________

Now one Pod crashes.

Reality becomes

```text
2 Pods
```

Mismatch.

Kubernetes notices.

Creates another Pod.

Reality returns to

```text
3 Pods
```

______________________________________________________________________

This is called

```
Reconciliation
```

______________________________________________________________________

# Meet ReplicaSet

ReplicaSet is responsible for

maintaining the desired number of Pods.

Think of it as

```
Pod Manager
```

______________________________________________________________________

Example

Desired

```
3 Pods
```

ReplicaSet continuously checks.

If

```
Running < Desired
```

↓

Create Pods.

If

```
Running > Desired
```

↓

Delete Pods.

______________________________________________________________________

# Visual

```text
ReplicaSet

↓

Pod

Pod

Pod
```

Crash

↓

```text
ReplicaSet

↓

Pod

❌

Pod
```

↓

Automatically

↓

```text
ReplicaSet

↓

Pod

Pod (New)

Pod
```

______________________________________________________________________

# Backend Engineering Analogy

Imagine your engineering manager.

Company policy says:

```
Backend Team

=

5 Engineers
```

One engineer leaves.

Manager immediately starts hiring.

Exactly what ReplicaSet does.

______________________________________________________________________

# But ReplicaSet Has a Problem

ReplicaSet can maintain Pods.

But what if you want to deploy

Version 2?

Current

```text
FastAPI v1
```

Need

```text
FastAPI v2
```

ReplicaSet doesn't know

how to upgrade applications.

Need something smarter.

______________________________________________________________________

# Meet Deployment

Deployment manages

ReplicaSets.

Hierarchy

```text
Deployment

↓

ReplicaSet

↓

Pods

↓

Containers
```

This hierarchy is extremely important.

______________________________________________________________________

# Think of It Like This

```text
CEO

↓

Manager

↓

Employees
```

Deployment

↓

ReplicaSet

↓

Pods

______________________________________________________________________

Deployment never creates Pods directly.

ReplicaSet does.

______________________________________________________________________

# Responsibilities

## ReplicaSet

Maintains Pod count.

______________________________________________________________________

## Deployment

Manages ReplicaSets.

Handles

- Updates
- Rollbacks
- Version history
- Deployment strategy

______________________________________________________________________

# Complete Architecture

```text
Deployment

↓

ReplicaSet

↓

Pod

↓

FastAPI Container
```

If you remember only one diagram,

remember this one.

______________________________________________________________________

# What Happens During Deployment?

Suppose

Current

```text
FastAPI v1
```

Deployment

↓

ReplicaSet

↓

3 Pods

______________________________________________________________________

Now change image

```text
v1

↓

v2
```

Question

Will Deployment edit existing Pods?

No.

Pods are immutable.

Instead,

Deployment creates

a brand new ReplicaSet.

______________________________________________________________________

# Rolling Update

Current

```text
ReplicaSet A

↓

v1
```

Deployment creates

```text
ReplicaSet B

↓

v2
```

Then gradually shifts traffic.

______________________________________________________________________

Visual

```text
V1 V1 V1 V1
```

↓

```text
V2 V1 V1 V1
```

↓

```text
V2 V2 V1 V1
```

↓

```text
V2 V2 V2 V1
```

↓

```text
V2 V2 V2 V2
```

Users never notice.

______________________________________________________________________

# Why Not Replace Everything At Once?

Suppose

Current

```
10 Pods
```

Stop all.

Start new.

Timeline

```text
Stop

↓

No Pods

↓

Downtime

↓

New Pods
```

Bad.

Rolling Update avoids downtime.

______________________________________________________________________

# What If Version 2 Is Broken?

Imagine

Version 2

contains a bug.

Users cannot log in.

Deployment remembers

ReplicaSet A.

Rollback.

```text
ReplicaSet B

↓

Delete
```

↓

```text
ReplicaSet A

↓

Scale Up
```

Application restored.

______________________________________________________________________

# Rollback Flow

```text
Version 1

↓

Deploy Version 2

↓

Bug

↓

Rollback

↓

Version 1
```

Usually

one command.

______________________________________________________________________

# Reconciliation Loop

One of Kubernetes' core ideas.

Deployment constantly asks

```text
Desired

==

Actual ?
```

Example

Desired

```
5 Pods
```

Actual

```
4 Pods
```

Deployment notices.

ReplicaSet creates one more.

______________________________________________________________________

# Production Example

Suppose

FastAPI Deployment

```text
Replicas

=

4
```

Architecture

```text
Deployment

↓

ReplicaSet

↓

Pod

Pod

Pod

Pod
```

Traffic

```text
Users

↓

Service

↓

4 Pods
```

If one Pod crashes

```text
Users

↓

Service

↓

Pod

❌

Pod

Pod
```

ReplicaSet creates another Pod.

Users keep working.

______________________________________________________________________

# Scaling

Need more capacity?

Current

```text
Replicas

=

3
```

Traffic increases.

Change

```yaml
replicas: 10
```

Deployment

↓

ReplicaSet

↓

Creates

7

new Pods.

Done.

______________________________________________________________________

# Deployment YAML

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: fastapi

spec:
  replicas: 3

  selector:
    matchLabels:
      app: fastapi

  template:
    metadata:
      labels:
        app: fastapi

    spec:
      containers:
        - name: api
          image: my-fastapi:v1

          ports:
            - containerPort: 8000
```

Don't memorize it.

Focus on understanding:

- Deployment
- Replica count
- Pod template

______________________________________________________________________

# What Is the Pod Template?

Notice

```yaml
template:
```

This is

the blueprint

for creating Pods.

ReplicaSet repeatedly uses

this template.

______________________________________________________________________

# kubectl Commands

Create Deployment

```bash
kubectl apply -f deployment.yaml
```

______________________________________________________________________

View Deployments

```bash
kubectl get deployments
```

______________________________________________________________________

View ReplicaSets

```bash
kubectl get replicasets
```

______________________________________________________________________

View Pods

```bash
kubectl get pods
```

______________________________________________________________________

Scale

```bash
kubectl scale deployment fastapi --replicas=5
```

______________________________________________________________________

Rollback

```bash
kubectl rollout undo deployment fastapi
```

______________________________________________________________________

Deployment History

```bash
kubectl rollout history deployment fastapi
```

______________________________________________________________________

# Common Deployment Strategies

## Rolling Update (Default)

Replace Pods gradually.

No downtime.

Most common.

______________________________________________________________________

## Recreate

Delete everything first.

Then create new Pods.

Simple,

but causes downtime.

______________________________________________________________________

## Blue-Green (Concept)

Two complete environments.

```text
Blue

↓

Current
```

```text
Green

↓

New
```

Switch traffic instantly.

Very safe.

Higher infrastructure cost.

______________________________________________________________________

## Canary (Concept)

Release to

5%

↓

20%

↓

50%

↓

100%

Useful for

large-scale production.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating Pods directly.

Production applications should almost always use Deployments.

______________________________________________________________________

## Mistake 2

Thinking Deployment creates Pods.

Deployment creates ReplicaSets.

ReplicaSets create Pods.

______________________________________________________________________

## Mistake 3

Editing Pods directly.

Pods are treated as disposable.

Update the Deployment instead.

______________________________________________________________________

## Mistake 4

Deleting Pods manually to restart the application.

Delete the Pod if needed,

ReplicaSet will recreate it.

But configuration changes should always go through the Deployment.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Pods are temporary and should not be managed directly in production. A ReplicaSet ensures that the desired number of Pods is always running. A Deployment sits above the ReplicaSet and provides higher-level features such as rolling updates, rollbacks, scaling, and version history. During an update, the Deployment creates a new ReplicaSet and gradually replaces old Pods with new ones without causing downtime."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why shouldn't we create Pods directly?**

Because Pods are ephemeral and lack self-healing, scaling, and deployment management.

______________________________________________________________________

**Q. Who creates Pods?**

ReplicaSet.

______________________________________________________________________

**Q. Who creates ReplicaSets?**

Deployment.

______________________________________________________________________

**Q. Does Deployment update existing Pods?**

No.

It creates new Pods from a new ReplicaSet and gradually replaces the old ones.

______________________________________________________________________

**Q. Why is a rolling update better than deleting all Pods at once?**

It keeps the application available while the new version is being deployed.

______________________________________________________________________

**Q. Can I scale a Deployment?**

Yes.

Changing the replica count causes the ReplicaSet to create or remove Pods.

______________________________________________________________________

# Pattern Summary

| Object | Responsibility |
|---------|----------------|
| Pod | Runs containers |
| ReplicaSet | Maintains desired Pod count |
| Deployment | Manages ReplicaSets |
| Reconciliation Loop | Keeps desired and actual state aligned |
| Rolling Update | Zero-downtime deployment |
| Rollback | Restore previous ReplicaSet |
| Scaling | Increase or decrease Pod count |

______________________________________________________________________

# Quick Revision

- Pods should rarely be created directly in production.
- ReplicaSet ensures the correct number of Pods is running.
- Deployment manages ReplicaSets.
- Deployment → ReplicaSet → Pod is the core hierarchy.
- Deployments provide rolling updates and rollbacks.
- Kubernetes continuously reconciles desired and actual state.
- Pods are replaced, not modified.
- Scaling changes the number of Pods by updating the Deployment.
- Rolling updates minimize downtime.
- Rollbacks quickly restore a previous stable version.

______________________________________________________________________

# Key Takeaway

The biggest mindset shift in Kubernetes is:

> **You don't manage Pods—you manage the desired state.**

Instead of saying:

> "Start this Pod."

You declare:

> "I always want three healthy Pods running."

Kubernetes continuously works to make reality match that declaration. The combination of **Deployment + ReplicaSet** is
what gives Kubernetes its powerful self-healing, scaling, and zero-downtime deployment capabilities.

______________________________________________________________________

# Next

[05-services-and-networking.md](05-services-and-networking.md)
