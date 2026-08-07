# Complete HTTP Request Lifecycle Deep Dive

## 11. Service Discovery and Service Mesh

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how microservices find each other, why hardcoding IP addresses doesn't work, how Service Discovery works internally, and how a Service Mesh transparently manages communication between services.

______________________________________________________________________

# Introduction

In the previous chapter,

the API Gateway

received

the request.

Now

it knows

the request

should go to

```
User Service
```

Question:

```
Where is

User Service?
```

Years ago,

people simply

hardcoded

IP addresses.

Example

```
User Service

↓

10.10.2.45
```

This doesn't work

in cloud-native

applications.

______________________________________________________________________

# Why?

Imagine

your application

runs on Kubernetes.

```
User Service

↓

Pod A

↓

10.10.2.45
```

One minute later

Pod crashes.

Kubernetes creates

another Pod.

```
User Service

↓

Pod B

↓

10.10.5.81
```

The IP changed.

Hardcoded IPs

are now invalid.

______________________________________________________________________

# The Solution

```
Service Discovery
```

Instead of

asking

"Which IP?"

applications ask

```
Where is

User Service?
```

The Service Discovery

system replies

```
10.10.5.81
```

______________________________________________________________________

# High Level Flow

```
API Gateway

↓

Service Discovery

↓

User Service

↓

FastAPI
```

______________________________________________________________________

# What Is Service Discovery?

Service Discovery

is a registry

that keeps track

of

every running service.

It knows

- Service Name
- IP Address
- Port
- Health
- Metadata

______________________________________________________________________

# Real Example

Instead of

```
10.10.4.32
```

applications use

```
user-service
```

The registry

maps

```
user-service

↓

10.10.4.32
```

______________________________________________________________________

# Service Registration

When

a service starts

it registers itself.

```
User Service

↓

Service Registry

↓

Register

↓

IP

↓

Port
```

Now

other services

can find it.

______________________________________________________________________

# What Happens If The Service Dies?

Suppose

```
User Service

↓

Crash
```

The registry

removes

the service.

Future requests

will never

be routed there.

______________________________________________________________________

# What Happens Internally?

```
FastAPI Starts

↓

Read Configuration

↓

Open Network Port

↓

Register

↓

Heartbeat

↓

Ready
```

______________________________________________________________________

# Heartbeats

Interview favorite.

Services

periodically send

```
Heartbeat
```

Example

every

10 seconds.

```
Service

↓

Registry

↓

I'm Alive
```

No heartbeat?

↓

Remove service.

______________________________________________________________________

# Health Checks

Service Discovery

often performs

its own

health checks.

Example

```
GET /health
```

Returns

```
200 OK
```

Healthy.

______________________________________________________________________

# DNS-Based Service Discovery

Interview favorite.

Kubernetes

uses

DNS.

Example

```
user-service.default.svc.cluster.local
```

↓

```
10.96.0.25
```

Applications

never see

Pod IPs.

______________________________________________________________________

# Client Side Discovery

Example

Netflix.

```
Client

↓

Registry

↓

Choose Server

↓

Connect
```

The client

chooses

the server.

______________________________________________________________________

# Server Side Discovery

Example

Kubernetes.

```
Client

↓

Load Balancer

↓

Registry

↓

Service
```

The client

doesn't know

anything.

Infrastructure

handles

everything.

______________________________________________________________________

# Popular Technologies

```
Consul

↓

Eureka

↓

ZooKeeper

↓

etcd

↓

Kubernetes DNS
```

______________________________________________________________________

# Kubernetes Service Discovery

Interview favorite.

Suppose

3 Pods

exist.

```
Pod1

10.0.1.5
```

```
Pod2

10.0.2.8
```

```
Pod3

10.0.4.1
```

Kubernetes

creates

one Service.

```
user-service

↓

ClusterIP

↓

10.96.0.10
```

Applications

always use

```
user-service
```

never

Pod IPs.

______________________________________________________________________

# What Is A Service Mesh?

Interview favorite.

Suppose

100 microservices

exist.

Every service

needs

- TLS
- Retries
- Timeouts
- Logging
- Metrics
- Tracing
- Load Balancing

Should every team

implement

all of this?

No.

Instead

we use

a

```
Service Mesh
```

______________________________________________________________________

# High Level Architecture

```
User Service

↓

Sidecar Proxy

↓

Network

↓

Sidecar Proxy

↓

Order Service
```

Applications

never talk

directly.

Sidecars

communicate.

______________________________________________________________________

# Sidecar Pattern

Every service

gets

its own proxy.

```
FastAPI

↓

Envoy
```

```
Order Service

↓

Envoy
```

Communication

always happens

through Envoy.

______________________________________________________________________

# What Happens Internally?

```
FastAPI

↓

localhost

↓

Envoy

↓

mTLS

↓

Envoy

↓

Order Service
```

FastAPI

doesn't know

the mesh exists.

______________________________________________________________________

# Why Service Mesh?

Responsibilities

```
Service Discovery

↓

mTLS

↓

Retries

↓

Timeouts

↓

Load Balancing

↓

Circuit Breaker

↓

Tracing

↓

Metrics
```

______________________________________________________________________

# Automatic mTLS

Interview favorite.

Without Mesh

developers

must configure

TLS.

With Mesh

```
Service A

↓

Encrypted

↓

Service B
```

Automatically.

______________________________________________________________________

# Traffic Splitting

Suppose

Version 2

is deployed.

```
90%

↓

Version 1
```

```
10%

↓

Version 2
```

The mesh

handles

traffic routing.

______________________________________________________________________

# Circuit Breaker

Suppose

Payment Service

is down.

Instead of

waiting

30 seconds

the mesh

immediately

fails.

```
Circuit Open
```

______________________________________________________________________

# Retries

Temporary failure.

```
Request

↓

Timeout

↓

Retry

↓

Success
```

Configured

centrally.

______________________________________________________________________

# Distributed Tracing

Every request

gets

```
Trace ID
```

The mesh

propagates

the Trace ID

automatically.

Useful

for

OpenTelemetry.

______________________________________________________________________

# Observability

Mesh collects

```
Latency

↓

Errors

↓

Traffic

↓

Retries

↓

Failures
```

No application code

required.

______________________________________________________________________

# Service Discovery + Mesh

```
API Gateway

↓

Service Discovery

↓

Envoy

↓

FastAPI

↓

Envoy

↓

PostgreSQL
```

______________________________________________________________________

# Popular Service Meshes

```
Istio

↓

Linkerd

↓

Consul Connect

↓

Kuma
```

______________________________________________________________________

# What Happens Inside Kubernetes?

```
Gateway

↓

DNS

↓

ClusterIP

↓

iptables/IPVS

↓

Pod

↓

Envoy

↓

FastAPI
```

Notice

Kubernetes

handles

service discovery,

while

Istio

handles

service communication.

______________________________________________________________________

# Common Interview Questions

## Why can't microservices use hardcoded IP addresses?

Containers and Pods are frequently recreated, causing IP addresses to change. Service Discovery provides stable service
names that always resolve to healthy instances.

______________________________________________________________________

## What is the difference between Service Discovery and a Service Mesh?

Service Discovery answers **"Where is the service?"**

Service Mesh answers **"How should services communicate securely and reliably?"**

______________________________________________________________________

## What is a Sidecar Proxy?

A Sidecar Proxy (such as Envoy) runs alongside every application instance and transparently handles networking concerns
like retries, TLS, metrics, tracing, and load balancing.

______________________________________________________________________

## Does Kubernetes provide a Service Mesh?

No.

Kubernetes provides Service Discovery and networking primitives.

Istio, Linkerd, and similar projects build a Service Mesh on top of Kubernetes.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain Service Discovery and Service Mesh.

### Answer

Service Discovery maintains a registry of available services and their network locations, allowing applications to
communicate using logical service names instead of IP addresses. A Service Mesh builds on top of this by inserting
sidecar proxies that transparently manage secure communication, retries, load balancing, timeouts, traffic routing, and
observability without requiring application code changes.

______________________________________________________________________

# Summary

Modern microservices never communicate using hardcoded IP addresses.

Instead they rely on

- Service Discovery
- DNS
- ClusterIP
- Sidecar Proxies
- Service Mesh

Together they provide

- Dynamic service location
- Secure communication
- Automatic retries
- Load balancing
- Distributed tracing
- Traffic management

At this point,

the request has successfully reached the correct application instance.

The next step is understanding **what happens inside the application server (Uvicorn/Gunicorn) before FastAPI receives
the request**.

______________________________________________________________________

# Next

[12. Request Routing and Traffic Management](12-request-routing-and-traffic-management.md)
