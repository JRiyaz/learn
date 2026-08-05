# 10-production-kubernetes.md

# Production Kubernetes

> **🎯 This chapter is where Kubernetes moves from "I know the concepts" to "I can operate production systems."**
>
> Most backend interviews for 5+ years of experience don't stop at Pods and Deployments.
>
> Instead, they ask:
>
> - How do you monitor Kubernetes?
> - How do you debug production issues?
> - How do you secure workloads?
> - How do you optimize resources?
> - What happens when something goes wrong?
>
> This chapter answers those questions.

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

Senior backend engineers are expected to understand production operations.

Interviewers want to know whether you understand:

- Logging
- Monitoring
- Metrics
- Alerting
- Distributed Tracing
- Debugging
- Security
- Namespaces
- RBAC
- Resource optimization
- Production best practices

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- How to observe Kubernetes workloads
- How to troubleshoot failures
- How logs, metrics, and traces differ
- Kubernetes security basics
- Resource optimization
- Production deployment checklist

______________________________________________________________________

# What Does "Production Ready" Mean?

Many developers think:

> "If my Pod is Running, my application is healthy."

Not necessarily.

A production-ready application should be:

- Available
- Observable
- Secure
- Scalable
- Recoverable
- Efficient

______________________________________________________________________

# The Three Pillars of Observability

Every production system relies on three types of telemetry.

```text
Logs

Metrics

Traces
```

Understanding the difference is extremely important.

______________________________________________________________________

# 1. Logs

Logs answer:

> **What happened?**

Example

```text
2026-08-05 10:05:23

User 101 logged in
```

```text
Database connection failed
```

```text
Kafka timeout
```

Logs are event-based.

______________________________________________________________________

# Backend Analogy

Python

```python
logger.info("Payment completed")
```

Those messages become Kubernetes logs.

______________________________________________________________________

# kubectl Logs

View logs

```bash
kubectl logs payment-api-12345
```

Follow logs

```bash
kubectl logs -f payment-api-12345
```

Previous container logs

```bash
kubectl logs --previous payment-api-12345
```

Useful after crashes.

______________________________________________________________________

# Production Logging

Applications shouldn't store logs locally.

Instead

```text
FastAPI

↓

stdout

↓

Fluent Bit

↓

Elasticsearch

↓

Kibana
```

or

```text
FastAPI

↓

stdout

↓

Fluent Bit

↓

Loki

↓

Grafana
```

This is called

```
Centralized Logging
```

______________________________________________________________________

# Why Not Store Logs in Pods?

Pods disappear.

Logs disappear too.

Always send logs

to centralized storage.

______________________________________________________________________

# 2. Metrics

Metrics answer:

> **How is the system behaving?**

Examples

- CPU usage
- Memory usage
- Requests/sec
- Error rate
- Response time

Metrics are numbers

measured over time.

______________________________________________________________________

# Prometheus

The most common monitoring tool.

Responsibilities

- Collect metrics
- Store time-series data
- Evaluate alerts

______________________________________________________________________

# Example Metrics

```text
CPU

72%
```

```text
Memory

850 MB
```

```text
Requests/sec

2300
```

______________________________________________________________________

# Grafana

Prometheus stores metrics.

Grafana visualizes them.

Example Dashboard

```text
CPU Usage

███████
```

```text
Memory

████
```

```text
Latency

██
```

Most production teams use

Prometheus + Grafana together.

______________________________________________________________________

# Alerts

Monitoring isn't enough.

Need notifications.

Example

```text
CPU > 90%

for 10 minutes
```

↓

Send Slack.

↓

Create PagerDuty incident.

↓

Notify On-call Engineer.

______________________________________________________________________

# 3. Distributed Tracing

Logs tell

what happened.

Metrics tell

how much.

Tracing tells

**where time was spent.**

______________________________________________________________________

# Backend Example

User

↓

API Gateway

↓

User Service

↓

Payment Service

↓

Kafka

↓

Notification Service

Request becomes slow.

Which service caused it?

Tracing answers that.

______________________________________________________________________

# OpenTelemetry

The modern standard

for collecting traces.

Popular backends

- Jaeger
- Zipkin
- Grafana Tempo

______________________________________________________________________

# Visual

```text
Browser

↓

API Gateway

↓

User Service

↓

Payment Service

↓

Database
```

Each step

records timing.

______________________________________________________________________

# Production Debugging

Suppose users report:

```
Checkout is slow.
```

How would you debug?

Step 1

Check

Metrics.

CPU?

Memory?

Latency?

______________________________________________________________________

Step 2

Check

Logs.

Exceptions?

Timeouts?

Errors?

______________________________________________________________________

Step 3

Check

Traces.

Which service

is slow?

______________________________________________________________________

Step 4

Inspect

Pods.

```bash
kubectl get pods
```

______________________________________________________________________

Step 5

Describe

Pod.

```bash
kubectl describe pod
```

______________________________________________________________________

Step 6

Check events.

Scheduling?

OOMKilled?

CrashLoopBackOff?

______________________________________________________________________

# Common Pod States

Running

Healthy.

______________________________________________________________________

Pending

Waiting for resources.

______________________________________________________________________

CrashLoopBackOff

Application starts.

Crashes.

Restarts.

Repeats.

Usually

application bug

or

configuration issue.

______________________________________________________________________

ImagePullBackOff

Image

cannot be downloaded.

Common causes

- Wrong image name
- Authentication issue
- Missing repository

______________________________________________________________________

OOMKilled

Exceeded

memory limit.

______________________________________________________________________

# Security Basics

Security deserves

an entire course,

but backend engineers

should know the basics.

______________________________________________________________________

# Namespaces

Namespaces

logically separate workloads.

Example

```text
development

staging

production
```

Applications

can use

the same names

inside different namespaces.

______________________________________________________________________

# RBAC

RBAC

means

Role-Based Access Control.

Example

Developer

↓

Read Pods

Only.

______________________________________________________________________

Admin

↓

Everything.

______________________________________________________________________

Principle

Least Privilege.

Give only

the permissions

required.

______________________________________________________________________

# Network Policies

Default

Pods often

can communicate freely.

Sometimes

that's dangerous.

Network Policies

control

who can talk to whom.

Example

```text
Frontend

↓

Backend

Allowed
```

```text
Frontend

↓

Database

Blocked
```

______________________________________________________________________

# Secrets

Never

store passwords

inside Docker images

or source code.

Use

Kubernetes Secrets

or

external secret managers.

______________________________________________________________________

# Resource Optimization

One of the biggest production mistakes

is

incorrect Requests

and

Limits.

______________________________________________________________________

Too Small

↓

OOMKilled

______________________________________________________________________

Too Large

↓

Cluster wastes resources.

______________________________________________________________________

Good tuning

reduces cloud cost.

______________________________________________________________________

# Production Best Practices

## 1. Always Use Deployments

Avoid

creating Pods directly.

______________________________________________________________________

## 2. Configure Health Probes

Use

- Startup
- Readiness
- Liveness

______________________________________________________________________

## 3. Set Resource Requests & Limits

Prevent

resource starvation

and runaway memory usage.

______________________________________________________________________

## 4. Use Multiple Replicas

Never

run

one Pod

in production.

______________________________________________________________________

## 5. Externalize Configuration

Use

ConfigMaps

and

Secrets.

______________________________________________________________________

## 6. Centralize Logs

Never rely

on Pod filesystem logs.

______________________________________________________________________

## 7. Use Monitoring

Prometheus

-

Grafana.

______________________________________________________________________

## 8. Enable Autoscaling

Especially

for stateless APIs.

______________________________________________________________________

## 9. Back Up Databases

Persistent Volumes

are not backups.

______________________________________________________________________

## 10. Use Rolling Updates

Avoid downtime.

______________________________________________________________________

# Production Architecture

```text
                Internet

                    │

            Cloud Load Balancer

                    │

                 Ingress

                    │

              FastAPI Deployment

                    │

              Multiple Pods

                    │

           Prometheus Metrics

                    │

                Grafana

                    │

               Fluent Bit

                    │

                  Loki

                    │

              PostgreSQL
```

Everything works together.

______________________________________________________________________

# Common kubectl Commands

Cluster Info

```bash
kubectl cluster-info
```

______________________________________________________________________

View Events

```bash
kubectl get events
```

______________________________________________________________________

Describe Pod

```bash
kubectl describe pod <pod-name>
```

______________________________________________________________________

View Logs

```bash
kubectl logs <pod-name>
```

______________________________________________________________________

Execute Shell

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

Very useful

for debugging.

______________________________________________________________________

View Resource Usage

```bash
kubectl top pods
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using

`kubectl delete pod`

to solve every problem.

Find

the root cause.

______________________________________________________________________

## Mistake 2

Ignoring Requests

and Limits.

______________________________________________________________________

## Mistake 3

Running

one replica

in production.

______________________________________________________________________

## Mistake 4

No health probes.

Kubernetes

can't determine

application health.

______________________________________________________________________

## Mistake 5

Keeping logs

inside containers.

Pods disappear.

Logs disappear.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A production Kubernetes environment requires much more than running Pods. We need centralized logging, metrics, tracing, security controls, health probes, resource management, and monitoring. When debugging, I typically start with metrics to identify symptoms, logs to understand failures, and distributed traces to locate latency across services. I also inspect Pod events and resource usage to identify Kubernetes-specific issues."

______________________________________________________________________

### Common Follow-up Questions

**Q. What's the difference between logs, metrics, and traces?**

- Logs describe individual events.
- Metrics provide aggregated numerical measurements over time.
- Traces show how a request flows through multiple services.

______________________________________________________________________

**Q. What causes CrashLoopBackOff?**

The application repeatedly starts and crashes.

______________________________________________________________________

**Q. Why is OOMKilled different from CrashLoopBackOff?**

OOMKilled specifically indicates the process exceeded its memory limit.

CrashLoopBackOff is a restart state that can have many underlying causes.

______________________________________________________________________

**Q. Why use Namespaces?**

To isolate environments or teams within the same cluster.

______________________________________________________________________

**Q. Why centralize logs?**

Pods are temporary.

Local logs disappear when Pods are deleted.

______________________________________________________________________

# Pattern Summary

| Concept | Purpose |
|----------|---------|
| Logs | Record events |
| Metrics | Measure system health |
| Traces | Follow request flow |
| Prometheus | Metrics collection |
| Grafana | Dashboards |
| Loki | Log storage |
| Fluent Bit | Log forwarding |
| OpenTelemetry | Distributed tracing |
| RBAC | Authorization |
| Namespaces | Logical isolation |
| Network Policies | Traffic control |

______________________________________________________________________

# Quick Revision

- Production systems require observability.
- Logs explain events.
- Metrics measure performance.
- Traces show request paths.
- Prometheus collects metrics.
- Grafana visualizes metrics.
- Centralize logs using tools like Fluent Bit and Loki.
- Use Namespaces to isolate workloads.
- RBAC enforces least privilege.
- Always configure health probes and resource limits.

______________________________________________________________________

# Production Checklist

Before deploying a backend service:

- ✅ Deployment
- ✅ Multiple replicas
- ✅ Service
- ✅ Ingress
- ✅ ConfigMap
- ✅ Secret
- ✅ Resource Requests
- ✅ Resource Limits
- ✅ Health Probes
- ✅ Autoscaling
- ✅ Centralized Logging
- ✅ Metrics
- ✅ Alerts
- ✅ Backups
- ✅ Rolling Updates

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Running an application is easy. Operating it in production is the real challenge.**

Production Kubernetes is about much more than Pods and Deployments. It's about making applications **observable, secure,
scalable, and resilient**. A senior backend engineer should be comfortable not only deploying services but also
debugging failures, monitoring health, tuning resources, and following operational best practices.

______________________________________________________________________

# Next

[11-kubernetes-interview-and-system-design.md](11-kubernetes-interview-and-system-design.md)
