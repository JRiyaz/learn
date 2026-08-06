# Kubernetes Deployment for Flask

> **Course:** Flask for Backend Engineers
>
> **Module:** 9
>
> **File:** `21_kubernetes_flask.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Kubernetes is Used
- Kubernetes Architecture
- Pods
- Deployments
- Services
- ConfigMaps
- Secrets
- Ingress
- Horizontal Pod Autoscaler (HPA)
- Rolling Updates
- Health Checks
- Production Best Practices

______________________________________________________________________

# Why Kubernetes?

Imagine your application is running inside Docker.

```
Flask

↓

Docker Container
```

This works well.

But what happens if

- The container crashes?
- Traffic suddenly increases?
- A server fails?
- You need zero-downtime deployments?

Managing containers manually becomes difficult.

Kubernetes automates these tasks.

______________________________________________________________________

# What is Kubernetes?

Kubernetes (K8s) is a container orchestration platform.

Responsibilities

- Deploy containers
- Scale applications
- Restart failed containers
- Load balance traffic
- Perform rolling updates
- Manage secrets and configuration

______________________________________________________________________

# Kubernetes Architecture

```
Client

↓

Ingress

↓

Service

↓

Pods

↓

Container

↓

Flask
```

______________________________________________________________________

# Kubernetes Components

```
Cluster

↓

Nodes

↓

Pods

↓

Containers
```

______________________________________________________________________

# What is a Cluster?

A cluster is a collection of machines that run Kubernetes workloads.

```
Cluster

↓

Node 1

Node 2

Node 3
```

______________________________________________________________________

# What is a Node?

A node is a worker machine.

It can be

- Physical
- Virtual

Each node runs

- Pods
- kubelet
- Container Runtime

______________________________________________________________________

# What is a Pod?

A Pod is the smallest deployable unit in Kubernetes.

```
Pod

↓

Flask Container
```

Usually,

one Flask application runs in one Pod.

______________________________________________________________________

# Pod Lifecycle

```
Pending

↓

Running

↓

Succeeded

or

↓

Failed
```

If a Pod fails,

Kubernetes replaces it.

______________________________________________________________________

# Deployment

Pods should not be created manually.

Instead,

use a Deployment.

```
Deployment

↓

ReplicaSet

↓

Pods
```

Deployments ensure the desired number of Pods are always running.

______________________________________________________________________

# Deployment Example

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:

  name: flask-app

spec:

  replicas: 3

  selector:

    matchLabels:

      app: flask

  template:

    metadata:

      labels:

        app: flask

    spec:

      containers:

      - name: flask

        image: flask-app:latest
```

______________________________________________________________________

# Replicas

```
Deployment

↓

3 Replicas

↓

Pod 1

Pod 2

Pod 3
```

If one Pod crashes,

another is created automatically.

______________________________________________________________________

# Service

Pods receive dynamic IP addresses.

Instead of connecting directly,

clients connect through a Service.

```
Client

↓

Service

↓

Pods
```

______________________________________________________________________

# Service Types

| Type | Purpose |
|------|----------|
| ClusterIP | Internal Communication |
| NodePort | Expose on Node |
| LoadBalancer | Cloud Load Balancer |
| ExternalName | External DNS Mapping |

______________________________________________________________________

# Service Example

```yaml
apiVersion: v1

kind: Service

metadata:

  name: flask-service

spec:

  selector:

    app: flask

  ports:

  - port: 80

    targetPort: 5000
```

______________________________________________________________________

# Ingress

Instead of exposing every service individually,

Ingress routes external traffic.

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

# Ingress Example

```yaml
apiVersion: networking.k8s.io/v1

kind: Ingress

metadata:

  name: flask

spec:

  rules:

  - host: api.example.com
```

______________________________________________________________________

# ConfigMaps

Configuration should not be hardcoded.

Example

```
DEBUG=False

LOG_LEVEL=INFO
```

Store these values in a ConfigMap.

______________________________________________________________________

# Secrets

Sensitive values belong in Kubernetes Secrets.

Examples

- Database Password
- JWT Secret
- AWS Credentials

Never store secrets directly in Deployment YAML files.

______________________________________________________________________

# Using Environment Variables

```yaml
env:

- name: DATABASE_URL

  valueFrom:

    secretKeyRef:

      name: db-secret

      key: DATABASE_URL
```

______________________________________________________________________

# Liveness Probe

Checks whether the application is still running.

Example

```yaml
livenessProbe:

  httpGet:

    path: /health

    port: 5000
```

If the probe fails,

Kubernetes restarts the Pod.

______________________________________________________________________

# Readiness Probe

Checks whether the application is ready to receive traffic.

```
Pod Starts

↓

Database Connects

↓

Ready

↓

Receive Requests
```

Unready Pods do not receive traffic.

______________________________________________________________________

# Rolling Updates

Old version

```
Pod v1
```

↓

New version

```
Pod v2
```

Kubernetes replaces Pods gradually,

avoiding downtime.

______________________________________________________________________

# Rolling Update Flow

```
3 Pods

↓

Replace One

↓

Health Check

↓

Replace Next

↓

Deployment Complete
```

______________________________________________________________________

# Horizontal Pod Autoscaler (HPA)

Automatically scales Pods.

Example

```
CPU 20%

↓

2 Pods
```

```
CPU 90%

↓

8 Pods
```

Scaling is based on metrics.

______________________________________________________________________

# Resource Requests

Example

```yaml
resources:

  requests:

    cpu: "200m"

    memory: "256Mi"
```

Requests reserve resources.

______________________________________________________________________

# Resource Limits

```yaml
resources:

  limits:

    cpu: "500m"

    memory: "512Mi"
```

Limits prevent a container from consuming excessive resources.

______________________________________________________________________

# Logging

Applications should write logs to

```
stdout

stderr
```

Kubernetes collects container logs.

______________________________________________________________________

# Monitoring

Common tools

- Prometheus
- Grafana
- Kubernetes Dashboard

Monitor

- CPU
- Memory
- Restarts
- Response Times

______________________________________________________________________

# Production Architecture

```
Internet

↓

Load Balancer

↓

Ingress

↓

Service

↓

Flask Pods

↓

Redis

↓

PostgreSQL
```

______________________________________________________________________

# Deployment Flow

```
Build Docker Image

↓

Push Image

↓

Update Deployment

↓

Rolling Update

↓

Pods Restart

↓

Application Live
```

______________________________________________________________________

# Common Mistakes

❌ Running only one replica

❌ Hardcoding secrets

❌ No health checks

❌ No resource limits

❌ Using `latest` image tags in production

❌ Logging to files inside containers

______________________________________________________________________

# Production Best Practices

- Deploy using Deployments.
- Use multiple replicas.
- Configure liveness and readiness probes.
- Store configuration in ConfigMaps.
- Store secrets in Kubernetes Secrets.
- Set CPU and memory requests/limits.
- Use rolling updates.
- Monitor cluster health.
- Use specific image tags instead of `latest`.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are Kubernetes Deployments preferred over creating Pods manually?**

### Answer

Pods are temporary and can fail or be deleted.

A Deployment continuously ensures that the desired number of Pods are running.

Benefits include:

1. Automatic Pod recovery.
1. Rolling updates.
1. Rollback support.
1. Horizontal scaling.
1. Declarative application management.

Deployments make applications highly available and much easier to operate in production.

______________________________________________________________________

# Summary

In this chapter you learned:

- Kubernetes
- Cluster
- Node
- Pod
- Deployment
- Service
- Ingress
- ConfigMaps
- Secrets
- Health Checks
- HPA
- Rolling Updates

Kubernetes provides automated deployment, scaling, self-healing, and traffic management, making it the de facto standard
for running containerized Flask applications in production.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Kubernetes?
1. Why is Kubernetes needed if Docker already exists?
1. What is a Pod?

______________________________________________________________________

## Core Components

4. What is the difference between a Pod and a Deployment?
1. Why are Services required?
1. What is an Ingress?

______________________________________________________________________

## Configuration

7. What is a ConfigMap?
1. What is a Kubernetes Secret?
1. Why shouldn't secrets be stored in Deployment YAML files?

______________________________________________________________________

## Health Checks

10. What is a liveness probe?
01. What is a readiness probe?
01. What is the difference between them?

______________________________________________________________________

## Scaling

13. What is the Horizontal Pod Autoscaler?
01. Why are resource requests and limits important?

______________________________________________________________________

## Production

15. Why should applications write logs to stdout/stderr?
01. Why should rolling updates be preferred over stopping all Pods at once?

______________________________________________________________________

## Scenario-Based

17. One of your Flask Pods crashes unexpectedly. How does Kubernetes recover from this?
01. Your application experiences a sudden spike from 100 to 10,000 requests per minute. Which Kubernetes feature can automatically help handle the increased load?
01. Your new deployment contains a bug, and users begin receiving errors after half the Pods are updated. How do rolling updates reduce the impact of this issue?
01. A developer stores database passwords directly inside the Deployment manifest. Why is this a poor security practice, and what Kubernetes feature should be used instead?

______________________________________________________________________

# Next

[Flask Interview Questions & System Design](22_flask_interview_questions.md)
