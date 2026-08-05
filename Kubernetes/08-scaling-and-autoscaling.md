# 08-scaling-and-autoscaling.md

# Scaling & Autoscaling in Kubernetes

> **🎯 This chapter explains one of Kubernetes' biggest advantages over running Docker containers manually.**
>
> Imagine your FastAPI service suddenly receives **10× more traffic** because a new feature goes viral.
>
> Without Kubernetes, engineers wake up in the middle of the night to manually create more containers.
>
> With Kubernetes, scaling can happen automatically.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 35–45 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Scaling is one of the main reasons companies adopt Kubernetes.

Interviewers want to know if you understand:

- Horizontal vs Vertical Scaling
- Horizontal Pod Autoscaler (HPA)
- Vertical Pod Autoscaler (VPA)
- Cluster Autoscaler
- Resource Requests
- Resource Limits
- CPU & Memory management
- OOMKilled errors
- Production scaling strategies

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- Different types of scaling
- How HPA works
- When VPA is useful
- How Cluster Autoscaler adds nodes
- Resource Requests vs Limits
- CPU throttling
- Memory limits
- Why Pods get OOMKilled

______________________________________________________________________

# Let's Start With a Problem

Suppose your architecture looks like this.

```text
                Users

                  │

                  ▼

             FastAPI Pod
```

Everything works.

Traffic

```
200 requests/sec
```

______________________________________________________________________

Suddenly

a marketing campaign launches.

Traffic becomes

```
20,000 requests/sec
```

Your Pod reaches

```text
CPU

100%
```

Latency increases.

Requests time out.

Eventually

the application becomes unusable.

______________________________________________________________________

# First Solution

Buy a bigger server.

This is called

```
Vertical Scaling
```

______________________________________________________________________

# Vertical Scaling

Current

```text
2 CPU

4 GB RAM
```

Upgrade

↓

```text
16 CPU

64 GB RAM
```

Same Pod.

More resources.

______________________________________________________________________

# Advantages

- Simple
- No application changes
- Useful for databases

______________________________________________________________________

# Disadvantages

There is always

a hardware limit.

Eventually,

you can't buy

a bigger machine.

______________________________________________________________________

# Backend Engineering Analogy

Imagine one backend engineer.

Instead of hiring more engineers,

you simply ask

one engineer

to work

20 hours a day.

Eventually,

that's impossible.

______________________________________________________________________

# Horizontal Scaling

Instead of making

one Pod bigger,

create

more Pods.

Current

```text
1 Pod
```

↓

```text
5 Pods
```

↓

```text
20 Pods
```

Traffic is shared.

______________________________________________________________________

# Visual

Before

```text
Users

↓

Pod
```

After

```text
Users

↓

Service

↓

Pod

Pod

Pod

Pod

Pod
```

Much better.

______________________________________________________________________

# Which Is Better?

Generally

stateless backend APIs

prefer

Horizontal Scaling.

Databases often require

Vertical Scaling

or specialized clustering.

______________________________________________________________________

# Manual Scaling

Suppose

traffic increases.

You run

```bash
kubectl scale deployment api --replicas=10
```

Deployment creates

10 Pods.

Works.

But requires

human intervention.

______________________________________________________________________

# Autoscaling

Question

Why should engineers

watch CPU graphs

all day?

Instead,

Kubernetes can

watch metrics

and scale automatically.

______________________________________________________________________

# Horizontal Pod Autoscaler (HPA)

HPA changes

the number of Pods.

Example

Current

```text
3 Pods
```

Average CPU

```
90%
```

HPA decides

```
Need More Pods
```

↓

Creates

```text
6 Pods
```

CPU drops.

______________________________________________________________________

# Visual

```text
CPU

95%

↓

HPA

↓

More Pods

↓

CPU

45%
```

______________________________________________________________________

# How HPA Works

Simplified flow

```text
Metrics Server

↓

Current CPU

↓

HPA

↓

Deployment

↓

ReplicaSet

↓

Pods
```

Notice

HPA never creates Pods directly.

It updates

the Deployment.

______________________________________________________________________

# Example

Target CPU

```text
70%
```

Current

```text
95%
```

HPA

↓

Increase replicas.

______________________________________________________________________

Current

```text
20%
```

HPA

↓

Reduce replicas.

______________________________________________________________________

# HPA Example YAML

```yaml
apiVersion: autoscaling/v2

kind: HorizontalPodAutoscaler

spec:

  minReplicas: 2

  maxReplicas: 20

  metrics:

    averageUtilization: 70
```

Don't memorize.

Understand

- Minimum Pods
- Maximum Pods
- Target utilization

______________________________________________________________________

# What Metrics Can HPA Use?

Most commonly

- CPU
- Memory

With custom metrics

also:

- Requests per second
- Kafka lag
- Queue length
- Custom Prometheus metrics

______________________________________________________________________

# Vertical Pod Autoscaler (VPA)

Instead of changing

the number of Pods,

VPA changes

Pod resources.

Example

Current

```text
CPU

1 Core
```

↓

```text
2 Cores
```

Pod becomes bigger.

______________________________________________________________________

# Difference

HPA

↓

More Pods

______________________________________________________________________

VPA

↓

Bigger Pods

______________________________________________________________________

# Can We Use Both?

Sometimes.

But be careful.

Both modifying CPU

can create conflicts.

A common production pattern is:

- HPA for stateless APIs
- VPA recommendations for tuning resource requests
- Avoid having both automatically change the same resource without careful planning

______________________________________________________________________

# Cluster Autoscaler

Question

Suppose

HPA wants

20 Pods.

Cluster has

resources for only

10 Pods.

What now?

Need

more machines.

______________________________________________________________________

Cluster Autoscaler

adds Worker Nodes.

Flow

```text
HPA

↓

Needs Pods

↓

No Capacity

↓

Cluster Autoscaler

↓

New Worker Node

↓

Pods Scheduled
```

______________________________________________________________________

# Three Levels of Scaling

```text
Application

↓

HPA

↓

Pods

↓

Cluster Autoscaler

↓

Nodes
```

Remember this hierarchy.

______________________________________________________________________

# Resource Requests

Every Pod

declares

minimum resources.

Example

```yaml
requests:

  cpu: 500m

  memory: 512Mi
```

Meaning

"I need at least this much."

Scheduler uses

Requests

when choosing

Worker Nodes.

______________________________________________________________________

# Resource Limits

Applications

can also specify

maximum resources.

Example

```yaml
limits:

  cpu: 1

  memory: 1Gi
```

The Pod

cannot exceed these limits.

______________________________________________________________________

# Requests vs Limits

| Requests | Limits |
|-----------|--------|
| Guaranteed minimum | Maximum allowed |
| Used by Scheduler | Enforced during runtime |

______________________________________________________________________

# CPU Limits

Suppose

Limit

```
1 CPU
```

Application tries

to use

```
2 CPUs
```

Kubernetes

throttles CPU usage.

Application slows down,

but usually continues running.

______________________________________________________________________

# Memory Limits

Suppose

Limit

```
1 GB
```

Application uses

```
2 GB
```

Unlike CPU,

memory cannot be safely throttled.

Linux kills the process.

Pod status

```text
OOMKilled
```

______________________________________________________________________

# What Is OOMKilled?

OOM

means

```
Out Of Memory
```

Example

```text
Memory Limit

512 MB
```

Application

allocates

800 MB.

Kernel kills it.

Deployment starts

a new Pod.

Problem repeats.

______________________________________________________________________

# Backend Analogy

Imagine renting

a meeting room

for

10 people.

Twenty people arrive.

CPU case:

People squeeze in.

Memory case:

Fire marshal empties the room.

______________________________________________________________________

# Production Example

FastAPI

↓

Deployment

↓

HPA

↓

Service

↓

Users

Traffic spikes.

↓

CPU reaches

85%.

↓

HPA

creates

additional Pods.

↓

Traffic spreads.

↓

Latency drops.

______________________________________________________________________

# YAML Example

```yaml
resources:

  requests:

    cpu: "500m"

    memory: "512Mi"

  limits:

    cpu: "1"

    memory: "1Gi"
```

This is one of the most common Kubernetes interview snippets.

______________________________________________________________________

# kubectl Commands

View HPA

```bash
kubectl get hpa
```

______________________________________________________________________

Describe HPA

```bash
kubectl describe hpa
```

______________________________________________________________________

View Node Usage

```bash
kubectl top nodes
```

______________________________________________________________________

View Pod Usage

```bash
kubectl top pods
```

Requires

Metrics Server.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Not setting Requests.

Scheduler cannot make informed placement decisions.

______________________________________________________________________

## Mistake 2

Setting very low Memory Limits.

Applications repeatedly become

OOMKilled.

______________________________________________________________________

## Mistake 3

Thinking CPU and Memory behave the same.

CPU is generally throttled.

Memory exhaustion often terminates the process.

______________________________________________________________________

## Mistake 4

Using only Vertical Scaling.

Horizontal scaling is usually better for stateless backend APIs.

______________________________________________________________________

## Mistake 5

Assuming HPA creates Worker Nodes.

HPA creates Pods.

Cluster Autoscaler creates Nodes.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Kubernetes supports both horizontal and vertical scaling. Stateless backend services typically use Horizontal Pod Autoscaler, which increases or decreases the number of Pods based on metrics such as CPU utilization. If the cluster doesn't have enough capacity for the new Pods, the Cluster Autoscaler adds Worker Nodes. Resource Requests define the minimum resources a Pod needs, while Limits define the maximum resources it can consume."

______________________________________________________________________

### Common Follow-up Questions

**Q. What's the difference between HPA and VPA?**

HPA changes the number of Pods.

VPA changes the resources allocated to each Pod.

______________________________________________________________________

**Q. What happens if HPA creates Pods but the cluster has no capacity?**

Cluster Autoscaler adds more Worker Nodes if configured and supported by the infrastructure.

______________________________________________________________________

**Q. Why do Pods become OOMKilled?**

The application exceeded its memory limit.

______________________________________________________________________

**Q. Does CPU limit kill a Pod?**

Typically no.

CPU usage is throttled instead.

______________________________________________________________________

**Q. Which is better for FastAPI?**

Horizontal scaling is usually preferred because FastAPI applications are generally stateless.

______________________________________________________________________

# Pattern Summary

| Concept | Purpose |
|----------|---------|
| Vertical Scaling | Bigger Pods |
| Horizontal Scaling | More Pods |
| HPA | Automatically scales Pods |
| VPA | Automatically adjusts Pod resources |
| Cluster Autoscaler | Adds or removes Worker Nodes |
| Requests | Minimum guaranteed resources |
| Limits | Maximum allowed resources |
| CPU Limit | Throttling |
| Memory Limit | OOMKilled if exceeded |

______________________________________________________________________

# Quick Revision

- Kubernetes supports horizontal and vertical scaling.
- Stateless APIs usually use Horizontal Pod Autoscaler.
- HPA changes the replica count of Deployments.
- Cluster Autoscaler adds Worker Nodes when needed.
- Requests are used by the Scheduler.
- Limits are enforced at runtime.
- CPU overuse is generally throttled.
- Memory overuse usually results in OOMKilled.
- Monitor resource usage before choosing Requests and Limits.
- Scaling Pods and scaling Nodes are different operations.

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Kubernetes scales at multiple levels.**

It can scale **applications** by creating more Pods, **individual Pods** by adjusting their resources, and **the cluster
itself** by adding more Worker Nodes. Understanding which layer to scale—and when—is a fundamental production skill for
backend engineers running applications on Kubernetes.

______________________________________________________________________

# Next

[09-statefulsets-jobs-cronjobs.md](09-statefulsets-jobs-cronjobs.md)
