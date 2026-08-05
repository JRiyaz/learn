# 06-ingress-configmaps-secrets.md

# Ingress, ConfigMaps & Secrets

> **🎯 This chapter connects Kubernetes to the real world.**
>
> So far, we've learned how applications run inside the cluster.
>
> But production applications also need:
>
> - A way for users on the Internet to access them
> - Configuration that changes between environments
> - Secure handling of passwords, API keys, and certificates
>
> This lesson covers all three.

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

This topic is extremely common because almost every production application uses:

- Ingress
- ConfigMaps
- Secrets

Interviewers want to know:

- Why Ingress exists
- Difference between Ingress and LoadBalancer
- Difference between ConfigMaps and Secrets
- How applications receive configuration
- How TLS/HTTPS works
- Production best practices

______________________________________________________________________

# Learning Goals

By the end of this lesson you should understand:

- What Ingress is
- Why Ingress exists
- What an Ingress Controller does
- HTTPS termination
- TLS certificates
- ConfigMaps
- Secrets
- Environment Variables
- Mounting configuration files

______________________________________________________________________

# Part 1 — Ingress

______________________________________________________________________

# Let's Start With a Problem

Suppose you have

three backend services.

```text
User Service

Order Service

Payment Service
```

Each has

its own

LoadBalancer.

Architecture

```text
Internet

↓

LB

↓

User Service
```

______________________________________________________________________

```text
Internet

↓

LB

↓

Order Service
```

______________________________________________________________________

```text
Internet

↓

LB

↓

Payment Service
```

Three cloud load balancers.

Three public IPs.

Three costs.

Three configurations.

Not ideal.

______________________________________________________________________

# Better Solution

Use

one

Load Balancer.

```text
Internet

↓

Load Balancer

↓

Ingress

↓

User

↓

Order

↓

Payment
```

Much cleaner.

______________________________________________________________________

# What Is Ingress?

Ingress is

a collection of routing rules.

Example

```text
/users

↓

User Service
```

______________________________________________________________________

```text
/orders

↓

Order Service
```

______________________________________________________________________

```text
/payments

↓

Payment Service
```

It decides

where incoming HTTP requests should go.

______________________________________________________________________

# Backend Engineering Analogy

Imagine FastAPI.

```python
@app.get("/users")

@app.get("/orders")

@app.get("/payments")
```

FastAPI routes

requests

to handlers.

Ingress routes

requests

to Services.

Same concept.

______________________________________________________________________

# URL Routing Example

Suppose

Browser requests

```text
company.com/users
```

Ingress

↓

User Service

______________________________________________________________________

Request

```text
company.com/orders
```

↓

Order Service

______________________________________________________________________

Request

```text
company.com/payments
```

↓

Payment Service

______________________________________________________________________

# Host-Based Routing

Not only paths.

Also domains.

Example

```text
api.company.com

↓

API
```

______________________________________________________________________

```text
admin.company.com

↓

Admin
```

______________________________________________________________________

```text
docs.company.com

↓

Documentation
```

One Load Balancer.

Many applications.

______________________________________________________________________

# Visual

```text
                Internet

                    │

                    ▼

             Cloud Load Balancer

                    │

                    ▼

                 Ingress

      ┌────────────┼─────────────┐

      ▼            ▼             ▼

User Service   Order Service   Payment Service
```

______________________________________________________________________

# Does Ingress Route Directly to Pods?

No.

Flow

```text
Browser

↓

Load Balancer

↓

Ingress

↓

Service

↓

Pods
```

Remember

Ingress talks to

Services,

not Pods.

______________________________________________________________________

# What Is an Ingress Controller?

Common interview question.

Ingress itself

is only

a configuration.

Someone must actually

read those rules

and route traffic.

That component is

the

Ingress Controller.

______________________________________________________________________

# Popular Ingress Controllers

- NGINX Ingress
- Traefik
- HAProxy
- AWS ALB Controller
- Istio Gateway

NGINX is the most common.

______________________________________________________________________

# HTTPS and TLS

Production APIs

almost always use

HTTPS.

Question

Where does TLS terminate?

Usually

at the Ingress.

Flow

```text
Browser

HTTPS

↓

Ingress

Decrypt

↓

HTTP

↓

Service

↓

Pod
```

The application

often receives

plain HTTP

inside the cluster.

______________________________________________________________________

# TLS Certificates

Ingress stores

TLS certificates

inside Kubernetes Secrets.

Example

```text
Browser

↓

HTTPS

↓

Certificate

↓

Ingress
```

We'll connect this

to Secrets shortly.

______________________________________________________________________

# Example Ingress YAML

```yaml
apiVersion: networking.k8s.io/v1

kind: Ingress

metadata:
  name: api

spec:
  rules:
    - host: api.company.com

      http:
        paths:
          - path: /

            backend:
              service:
                name: user-service

                port:
                  number: 80
```

Focus on

- Host
- Path
- Service

______________________________________________________________________

# Part 2 — ConfigMaps

______________________________________________________________________

# The Problem

Suppose

Development

uses

```text
Redis

localhost
```

Production

uses

```text
redis.internal
```

Should you edit

the source code?

No.

Configuration

should live

outside

the application.

______________________________________________________________________

# What Is a ConfigMap?

A ConfigMap stores

non-sensitive configuration.

Examples

- Database host
- Redis host
- Kafka broker
- Log level
- Feature flags
- Application settings

______________________________________________________________________

# Backend Analogy

Think of

```python
settings.py
```

or

```
.env
```

files.

ConfigMaps

are Kubernetes'

version of external configuration.

______________________________________________________________________

# Example

```yaml
data:

  DATABASE_HOST: postgres

  REDIS_HOST: redis

  LOG_LEVEL: INFO
```

Application reads

these values

during startup.

______________________________________________________________________

# Environment Variables

ConfigMaps

can become

environment variables.

Example

```yaml
env:

- name: DATABASE_HOST

  valueFrom:

    configMapKeyRef:
```

Application

simply reads

```python
os.getenv("DATABASE_HOST")
```

Exactly like

Docker.

______________________________________________________________________

# Mount as Files

Sometimes

applications need

configuration files.

Example

```text
nginx.conf

application.yml

config.json
```

ConfigMaps

can mount

them as files.

______________________________________________________________________

# Part 3 — Secrets

______________________________________________________________________

# Why Not Store Passwords in ConfigMaps?

Suppose

```text
DB_PASSWORD

admin123
```

ConfigMaps are

not intended

for sensitive data.

Need

Secrets.

______________________________________________________________________

# What Is a Secret?

A Secret stores

sensitive information.

Examples

- Database Passwords
- API Keys
- OAuth Tokens
- JWT Secrets
- TLS Certificates
- SSH Keys

______________________________________________________________________

# Backend Analogy

Imagine

AWS Secrets Manager

Vault

Azure Key Vault

Kubernetes Secrets

solve a similar problem

inside the cluster.

______________________________________________________________________

# Example

```yaml
kind: Secret

data:

  password:

  username:
```

Values are stored

Base64 encoded.

______________________________________________________________________

# Important Interview Fact

Base64

is **NOT encryption**.

It is only encoding.

Many beginners misunderstand this.

Real production clusters

often combine

Secrets

with

external secret managers.

______________________________________________________________________

# Using Secrets

Secrets

can become

Environment Variables.

```python
DATABASE_PASSWORD

=

os.getenv(...)
```

Exactly like ConfigMaps.

______________________________________________________________________

Or

they can be

mounted as files.

Useful for

TLS certificates.

______________________________________________________________________

# ConfigMap vs Secret

| ConfigMap | Secret |
|------------|---------|
| Non-sensitive | Sensitive |
| Database Host | Database Password |
| Redis Host | API Key |
| Log Level | JWT Secret |
| Feature Flags | TLS Certificate |

______________________________________________________________________

# Complete Production Flow

```text
Browser

↓

HTTPS

↓

Ingress

↓

Service

↓

Pod

↓

FastAPI

↓

Reads ConfigMap

↓

Reads Secret

↓

Connects to PostgreSQL
```

Everything works together.

______________________________________________________________________

# Production Example

FastAPI

needs

```text
DATABASE_HOST

DATABASE_USER

DATABASE_PASSWORD
```

Store

```text
Host

↓

ConfigMap
```

Store

```text
Password

↓

Secret
```

Application

receives both

as environment variables.

______________________________________________________________________

# YAML Example

## ConfigMap

```yaml
apiVersion: v1

kind: ConfigMap

metadata:
  name: api-config

data:
  LOG_LEVEL: INFO
  DATABASE_HOST: postgres
```

______________________________________________________________________

## Secret

```yaml
apiVersion: v1

kind: Secret

metadata:
  name: api-secret

type: Opaque

data:
  DATABASE_PASSWORD: YWRtaW4xMjM=
```

______________________________________________________________________

# Common kubectl Commands

View ConfigMaps

```bash
kubectl get configmaps
```

______________________________________________________________________

View Secrets

```bash
kubectl get secrets
```

______________________________________________________________________

Describe ConfigMap

```bash
kubectl describe configmap api-config
```

______________________________________________________________________

Describe Secret

```bash
kubectl describe secret api-secret
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Putting passwords

inside ConfigMaps.

Use Secrets.

______________________________________________________________________

## Mistake 2

Thinking Base64

means encryption.

It doesn't.

______________________________________________________________________

## Mistake 3

Thinking Ingress replaces Services.

Ingress routes

to Services.

Services route

to Pods.

______________________________________________________________________

## Mistake 4

Creating one LoadBalancer

per service.

Ingress usually provides

a cleaner architecture.

______________________________________________________________________

## Mistake 5

Hardcoding environment-specific values

inside application code.

Use ConfigMaps

or Secrets.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Ingress provides HTTP/HTTPS routing into a Kubernetes cluster. It typically works with an Ingress Controller such as NGINX and routes requests to Kubernetes Services based on hostnames or URL paths. ConfigMaps store non-sensitive configuration, while Secrets store sensitive data such as passwords, API keys, and TLS certificates. Applications usually consume both through environment variables or mounted files."

______________________________________________________________________

### Common Follow-up Questions

**Q. What's the difference between Ingress and LoadBalancer?**

A LoadBalancer exposes one Service.

Ingress allows one external entry point to route traffic to many Services.

______________________________________________________________________

**Q. Does Ingress communicate directly with Pods?**

No.

Ingress routes to Services.

Services route to Pods.

______________________________________________________________________

**Q. What's the difference between ConfigMap and Secret?**

ConfigMap stores non-sensitive configuration.

Secret stores sensitive configuration.

______________________________________________________________________

**Q. Are Kubernetes Secrets encrypted?**

Not by default.

Their values are Base64 encoded. Additional encryption mechanisms can be enabled, and many organizations integrate
external secret management solutions.

______________________________________________________________________

**Q. Why use ConfigMaps instead of changing code for each environment?**

They separate configuration from application code, making deployments more portable and easier to manage.

______________________________________________________________________

# Pattern Summary

| Component | Responsibility |
|-----------|----------------|
| Ingress | HTTP/HTTPS routing |
| Ingress Controller | Implements Ingress rules |
| ConfigMap | Non-sensitive configuration |
| Secret | Sensitive configuration |
| TLS | HTTPS certificates |
| Environment Variables | Application configuration |
| Mounted Files | File-based configuration |

______________________________________________________________________

# Quick Revision

- Ingress is the entry point for HTTP/HTTPS traffic.
- Ingress routes requests to Services.
- An Ingress Controller implements the routing logic.
- ConfigMaps store non-sensitive configuration.
- Secrets store passwords, tokens, and certificates.
- Both ConfigMaps and Secrets can be exposed as environment variables or mounted as files.
- Base64 encoding is not encryption.
- Separate configuration from application code.

______________________________________________________________________

# Key Takeaway

The biggest lesson from this chapter is:

> **Applications should be portable, configurable, and secure.**

Ingress gives applications a clean public entry point. ConfigMaps let the same application run in different environments
without changing code. Secrets protect sensitive information from being hardcoded into images or source code. Together,
these objects make Kubernetes applications production-ready.

______________________________________________________________________

# Next

[07-storage.md](07-storage.md)
