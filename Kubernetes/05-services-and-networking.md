# 05-services-and-networking.md

# Services & Networking

> **🎯 This is one of the most important Kubernetes interview topics.**
>
> So far, we have learned:
>
> - Pods run applications
> - Deployments manage Pods
>
> But we still have one major problem:
>
> **How do users find a Pod?**
>
> This chapter answers that question.

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

Networking is where many Kubernetes beginners struggle.

Interviewers want to know whether you understand:

- Why Services exist
- Why Pod IPs cannot be used
- Service Discovery
- DNS
- kube-proxy
- ClusterIP
- NodePort
- LoadBalancer
- Headless Services
- Ingress (high-level)

______________________________________________________________________

# Learning Goals

By the end of this lesson, you should understand:

- Why Pods are not directly accessible
- Why Pod IPs change
- What a Service is
- How Services find Pods
- Labels & Selectors
- kube-proxy
- Internal DNS
- Types of Services
- Request flow from user to Pod

______________________________________________________________________

# Let's Start With a Problem

Suppose your Deployment creates

```text
3 Pods
```

```text
Pod A

10.10.1.5
```

```text
Pod B

10.10.1.8
```

```text
Pod C

10.10.1.12
```

Question

How does your frontend know

which IP to call?

______________________________________________________________________

Suppose it chooses

```
10.10.1.5
```

Everything works.

Now Pod A crashes.

ReplicaSet creates

```text
Pod D

10.10.8.25
```

The old IP disappears.

Frontend still calls

```
10.10.1.5
```

Application breaks.

______________________________________________________________________

# Why Pod IPs Cannot Be Trusted

Pods are

**ephemeral**.

Whenever a Pod is recreated,

it receives

a **new IP**.

Example

```text
Old Pod

10.10.1.5
```

↓

Crash

↓

```text
New Pod

10.10.8.25
```

Applications should never depend on Pod IPs.

______________________________________________________________________

# Backend Engineering Analogy

Imagine calling your friend.

Instead of saving

their phone number,

you remember

their house number.

One day they move.

House number changes.

You can't reach them.

Instead,

you save

their name

from your contacts.

Services work exactly like that.

______________________________________________________________________

# Meet Kubernetes Service

A Service provides

a **stable network identity**.

Instead of calling

```text
10.10.1.5
```

Applications call

```text
user-service
```

The Service always knows

which Pods are currently running.

______________________________________________________________________

# Visual

Without Service

```text
Frontend

↓

10.10.1.5

❌
```

______________________________________________________________________

With Service

```text
Frontend

↓

user-service

↓

Pod A

Pod B

Pod C
```

Pods may change.

Service stays the same.

______________________________________________________________________

# What Is a Service?

A Service is

> **A stable network endpoint that forwards requests to one or more Pods.**

It provides:

- Stable IP
- Stable DNS name
- Load Balancing
- Service Discovery

______________________________________________________________________

# Labels & Selectors

Question

How does a Service know

which Pods belong to it?

Using

```
Labels
```

______________________________________________________________________

Example

Pod

```yaml
labels:
  app: user-service
```

Service

```yaml
selector:
  app: user-service
```

Kubernetes matches them.

______________________________________________________________________

# Visual

```text
             Service

          app=user-service

                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼

Pod        Pod        Pod

app=user-service
```

Different labels?

Not selected.

______________________________________________________________________

# Backend Analogy

Think of labels as

database filters.

Example

```sql
SELECT *

FROM pods

WHERE app='user-service'
```

That's essentially

what the Service is doing.

______________________________________________________________________

# Request Flow

Suppose

Frontend

calls

```text
http://user-service
```

Flow

```text
Frontend

↓

DNS

↓

Service

↓

Pod

↓

FastAPI
```

Frontend never knows

which Pod handled the request.

______________________________________________________________________

# kube-proxy

Question

Who forwards traffic?

Answer

```
kube-proxy
```

Every Worker Node runs

kube-proxy.

Responsibilities

- Routing
- Load Balancing
- Network Rules

______________________________________________________________________

# Visual

```text
User

↓

Service

↓

kube-proxy

↓

Pod A

Pod B

Pod C
```

______________________________________________________________________

# Service Discovery

Imagine

Order Service

needs

User Service.

Instead of

```text
http://10.10.1.5
```

it calls

```text
http://user-service
```

DNS resolves

the correct Service.

Pods may change.

Applications don't care.

______________________________________________________________________

# Kubernetes DNS

Every Service automatically receives

a DNS name.

Example

```text
user-service
```

Inside the cluster,

applications simply call

```python
http://user-service:8000
```

No IP management.

______________________________________________________________________

# Types of Services

There are

four important types.

______________________________________________________________________

# 1. ClusterIP

Most common.

Default.

Accessible

only

inside the cluster.

______________________________________________________________________

Visual

```text
Frontend Pod

↓

ClusterIP Service

↓

Backend Pods
```

Perfect for

microservice communication.

______________________________________________________________________

Use Cases

- User Service
- Payment Service
- Order Service
- Redis
- PostgreSQL

Anything

internal.

______________________________________________________________________

# 2. NodePort

Need access

from outside

without a cloud load balancer.

Kubernetes opens

a port

on every Worker Node.

Example

```text
Node

192.168.1.10

↓

30080
```

Users call

```text
192.168.1.10:30080
```

Traffic

↓

Service

↓

Pods

______________________________________________________________________

Use Cases

- Development
- Testing
- Local clusters

Rare in production.

______________________________________________________________________

# 3. LoadBalancer

Cloud providers

(AWS, Azure, GCP)

create

an external load balancer.

Example

```text
Internet

↓

AWS Load Balancer

↓

Service

↓

Pods
```

Most production APIs

use this

or Ingress.

______________________________________________________________________

# 4. ExternalName

Sometimes

the application needs

an external service.

Example

Database

hosted outside Kubernetes.

Instead of hardcoding

```text
db.company.com
```

Applications call

```text
database
```

Service redirects.

Rarely used,

but useful.

______________________________________________________________________

# 5. Headless Service

Normally

Services

load balance.

Sometimes

applications need

individual Pod identities.

Example

Kafka

Redis Cluster

StatefulSet

Headless Service

returns

Pod IPs

instead of

one virtual IP.

We'll revisit this

when studying StatefulSets.

______________________________________________________________________

# Comparison

| Service Type | External Access | Load Balancing | Common Use |
|---------------|----------------|----------------|------------|
| ClusterIP | ❌ | ✅ | Internal microservices |
| NodePort | ✅ | ✅ | Development |
| LoadBalancer | ✅ | ✅ | Production APIs |
| ExternalName | External DNS | ❌ | External systems |
| Headless | Internal | ❌ | Stateful applications |

______________________________________________________________________

# Complete Request Flow

Let's trace

a request

to your FastAPI service.

```text
Browser

↓

Load Balancer

↓

Service

↓

kube-proxy

↓

Pod

↓

FastAPI

↓

Response
```

Users never communicate

directly with Pods.

______________________________________________________________________

# Production Architecture

```text
                Internet

                    │

                    ▼

          Cloud Load Balancer

                    │

                    ▼

              user-service

                    │

          ┌─────────┼─────────┐

          ▼         ▼         ▼

        Pod       Pod       Pod

       FastAPI   FastAPI   FastAPI
```

One Service.

Many Pods.

Automatic load balancing.

______________________________________________________________________

# What Happens If a Pod Crashes?

Suppose

```text
Pod B

↓

Crash
```

ReplicaSet creates

```text
Pod D
```

Service updates automatically.

Users continue calling

```
user-service
```

Nothing changes.

This is why Services are essential.

______________________________________________________________________

# Service YAML

```yaml
apiVersion: v1

kind: Service

metadata:
  name: user-service

spec:
  selector:
    app: user-service

  ports:
    - port: 80
      targetPort: 8000

  type: ClusterIP
```

Notice

Only

- Selector
- Port
- Type

No Pod IPs.

______________________________________________________________________

# Common kubectl Commands

View Services

```bash
kubectl get services
```

______________________________________________________________________

Describe Service

```bash
kubectl describe service user-service
```

______________________________________________________________________

View Endpoints

```bash
kubectl get endpoints
```

Endpoints show

which Pods

the Service currently forwards to.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using Pod IPs directly.

Pod IPs change.

Always use Services.

______________________________________________________________________

## Mistake 2

Forgetting labels.

If labels don't match,

Service finds

zero Pods.

______________________________________________________________________

## Mistake 3

Using NodePort in production.

Prefer

LoadBalancer

or

Ingress.

______________________________________________________________________

## Mistake 4

Thinking Services create Pods.

They don't.

Deployments create Pods.

Services only route traffic.

______________________________________________________________________

## Mistake 5

Confusing

Service

with

Ingress.

Service routes

inside

the cluster.

Ingress manages

external HTTP/HTTPS traffic.

We'll learn Ingress next.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Pods are ephemeral and receive new IP addresses whenever they are recreated, so applications should never communicate using Pod IPs. Kubernetes solves this with Services, which provide a stable IP address and DNS name. A Service selects Pods using labels and forwards traffic to healthy Pods through kube-proxy. Different Service types exist depending on whether traffic is internal to the cluster or comes from outside."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why can't we use Pod IPs directly?**

Because Pods are temporary and receive new IP addresses when recreated.

______________________________________________________________________

**Q. How does a Service know which Pods belong to it?**

Using labels and selectors.

______________________________________________________________________

**Q. Does a Service create Pods?**

No.

Deployments create Pods.

Services only provide networking.

______________________________________________________________________

**Q. What's the default Service type?**

ClusterIP.

______________________________________________________________________

**Q. What's the difference between ClusterIP and LoadBalancer?**

ClusterIP is internal only.

LoadBalancer exposes the application externally through a cloud load balancer.

______________________________________________________________________

**Q. What component forwards traffic to Pods?**

kube-proxy.

______________________________________________________________________

# Pattern Summary

| Concept | Purpose |
|----------|---------|
| Service | Stable network endpoint |
| Labels | Identify Pods |
| Selectors | Choose Pods |
| ClusterIP | Internal communication |
| NodePort | External access via Node |
| LoadBalancer | Cloud external access |
| ExternalName | External DNS alias |
| Headless Service | Direct Pod access |
| kube-proxy | Traffic forwarding |
| DNS | Stable Service names |

______________________________________________________________________

# Quick Revision

- Pod IPs are temporary.
- Services provide stable networking.
- Services select Pods using labels.
- kube-proxy forwards traffic to Pods.
- Internal communication typically uses ClusterIP.
- LoadBalancer exposes applications externally.
- NodePort is mostly for development or testing.
- Services automatically adapt when Pods are recreated.
- Applications should communicate using Service DNS names, not Pod IPs.

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Pods are temporary, but Services are permanent.**

Pods may be created, destroyed, rescheduled, or assigned new IP addresses at any time. Services hide that complexity by
providing a stable network identity and automatically routing traffic to healthy Pods. This abstraction is what makes
Kubernetes applications resilient and scalable.

______________________________________________________________________

# Next

[06-ingress-configmaps-secrets.md](06-ingress-configmaps-secrets.md)
