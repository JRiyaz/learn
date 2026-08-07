# Service Discovery

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how services locate each other in a microservices architecture, why Service Discovery is needed, and how to answer Service Discovery questions confidently in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

contains

only one service.

```
Client

↓

Backend
```

Simple.

Now imagine

a microservices system.

```
Authentication

Orders

Payments

Inventory

Notifications

Analytics

Recommendations
```

Suppose

Order Service

needs

Payment Service.

How does it know

where

Payment Service

is running?

Hardcoding

IP addresses

is not practical.

The solution is

```
Service Discovery
```

______________________________________________________________________

# What Is Service Discovery?

Service Discovery

is the mechanism

that allows

services

to automatically

find

other services.

Instead of

```
Order Service

↓

192.168.1.23
```

we use

```
Order Service

↓

Payment Service
```

The infrastructure

resolves

the actual address.

______________________________________________________________________

# Why Do We Need It?

In cloud environments,

containers

and virtual machines

are constantly

created,

destroyed,

and restarted.

Example

Today

```
Payment Service

↓

10.0.1.5
```

Tomorrow

```
Payment Service

↓

10.0.3.18
```

Hardcoding IPs

would constantly

break the application.

______________________________________________________________________

# Basic Architecture

```
             Service Registry
                  ▲
                  │
      Register    │     Lookup
                  │
Order Service ───►│◄─── Payment Service
                  │
                  ▼
           Inventory Service
```

Every service

registers itself

when it starts.

Other services

query

the registry.

______________________________________________________________________

# Components

A Service Discovery system

typically contains

- Service Registry
- Service Provider
- Service Consumer
- Health Checks

______________________________________________________________________

# Service Registry

The registry

stores

information about

running services.

Example

```
Payment Service

↓

10.0.1.15

↓

Port 8080
```

```
Inventory Service

↓

10.0.2.10

↓

Port 8081
```

Think of it as

a dynamic

phone book.

______________________________________________________________________

# Service Registration

When

a service starts,

it registers itself.

```
Payment Service

↓

Registry

↓

Registered
```

Now

other services

can discover it.

______________________________________________________________________

# Deregistration

Suppose

a service

stops.

It removes itself

from

the registry.

```
Payment Service

↓

Shutdown

↓

Registry Updated
```

Clients

no longer receive

its address.

______________________________________________________________________

# Health Checks

Suppose

a service crashes

without deregistering.

The registry

periodically checks

```
GET /health
```

If

the service

doesn't respond,

it is removed

from

the registry.

______________________________________________________________________

# Static Configuration

Without

Service Discovery

developers often use

```
payment.service.ip

=

192.168.1.50
```

Problems

- Manual updates
- Difficult deployments
- Frequent failures

______________________________________________________________________

# Dynamic Discovery

Instead

services ask

the registry.

```
Order Service

↓

Registry

↓

Payment Service Address

↓

Call Service
```

Much more flexible.

______________________________________________________________________

# Client-Side Discovery

The client

queries

the registry.

```
Order Service

↓

Registry

↓

Payment Instance

↓

Direct Request
```

The client

chooses

which instance

to call.

______________________________________________________________________

# Example

```
Payment

↓

Instance A

↓

Instance B

↓

Instance C
```

Registry

returns

all instances.

Client

selects one,

often using

Round Robin

or another algorithm.

______________________________________________________________________

# Server-Side Discovery

Instead,

the client

calls

a Load Balancer.

```
Order Service

↓

Load Balancer

↓

Registry

↓

Payment Instance
```

The Load Balancer

handles

instance selection.

The client

doesn't know

about

individual instances.

______________________________________________________________________

# Comparison

| Client-Side | Server-Side |
|-------------|-------------|
| Client chooses instance | Load Balancer chooses |
| Client queries registry | Gateway/LB queries registry |
| More client logic | Simpler client |

______________________________________________________________________

# Service Discovery Flow

```
Payment Service Starts

↓

Registers

↓

Registry

↓

Healthy

↓

Available
```

Another service

```
Lookup

↓

Registry

↓

Address

↓

Request
```

______________________________________________________________________

# Scaling Example

Suppose

Payment Service

scales

from

```
1 Instance

↓

5 Instances
```

All instances

register

automatically.

No application

configuration

changes

are required.

______________________________________________________________________

# Service Failure

Suppose

Instance 2

fails.

```
Payment Instance 2

↓

Crash
```

Health checks

detect

the failure.

Registry

removes

the instance.

Traffic

is routed

to

healthy instances.

______________________________________________________________________

# Service Discovery In Kubernetes

Kubernetes

provides

built-in

Service Discovery.

```
Pod

↓

Service

↓

DNS

↓

Other Pods
```

Instead of

remembering

pod IPs,

applications

use

service names.

Example

```
payment-service
```

______________________________________________________________________

# DNS-Based Discovery

Many systems

use DNS

for discovery.

Example

```
payment-service.default.svc.cluster.local
```

DNS

returns

the correct

service IP.

______________________________________________________________________

# Popular Service Registries

Examples

- Consul
- Eureka
- ZooKeeper
- etcd
- Kubernetes Service Discovery

Modern Kubernetes

clusters

often rely

on built-in

service discovery

instead of

external registries.

______________________________________________________________________

# Eureka

Popular

in

Spring Cloud.

Architecture

```
Services

↓

Register

↓

Eureka

↓

Lookup
```

______________________________________________________________________

# Consul

Supports

- Service Discovery
- Health Checks
- Configuration
- Key-Value Store

Widely used

outside

Kubernetes.

______________________________________________________________________

# etcd

Distributed

key-value store.

Used internally

by Kubernetes

to store

cluster state.

______________________________________________________________________

# ZooKeeper

Historically used

for

- Distributed coordination
- Leader election
- Service registration

Kafka

traditionally

used ZooKeeper,

though modern Kafka

can operate

without it

using KRaft.

______________________________________________________________________

# Service Discovery And Load Balancer

They solve

different problems.

Service Discovery

```
Find Services
```

Load Balancer

```
Distribute Requests
```

Many systems

use both.

______________________________________________________________________

# Service Discovery And API Gateway

API Gateway

may use

Service Discovery

to locate

backend services.

```
Client

↓

Gateway

↓

Registry

↓

Service
```

______________________________________________________________________

# Typical Microservice Architecture

```
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Service Registry

↓

Microservices

↓

Redis

↓

Database

↓

RabbitMQ
```

______________________________________________________________________

# Common Interview Questions

## Why not hardcode IP addresses?

Because cloud environments are dynamic. Services frequently restart, scale, or move to different hosts, causing
hardcoded addresses to become invalid.

______________________________________________________________________

## What happens if a service crashes?

Health checks detect the failure, and the Service Registry removes the unhealthy instance so it no longer receives
traffic.

______________________________________________________________________

## Does Service Discovery replace a Load Balancer?

No.

Service Discovery

helps locate services.

Load Balancers

distribute traffic

among available instances.

______________________________________________________________________

## Why is Service Discovery important in Kubernetes?

Pods are ephemeral and their IP addresses change. Kubernetes Service Discovery allows applications to communicate using
stable service names instead of changing IP addresses.

______________________________________________________________________

# Common Mistakes

## Hardcoding Service Addresses

Never assume

service IPs

remain constant.

______________________________________________________________________

## Ignoring Health Checks

Discovery

is only useful

if unhealthy instances

are removed.

______________________________________________________________________

## Confusing DNS With Service Discovery

DNS

may be part

of Service Discovery,

but

Service Discovery

also includes

registration,

health monitoring,

and dynamic updates.

______________________________________________________________________

## Thinking Every Service Needs External Discovery

Platforms like

Kubernetes

already provide

built-in mechanisms.

______________________________________________________________________

# Best Practices

✅ Use dynamic registration.

✅ Enable health checks.

✅ Avoid hardcoded addresses.

✅ Combine Service Discovery with Load Balancers.

✅ Use stable service names instead of IP addresses.

______________________________________________________________________

# Interview Deep Dive

## Question

What problem does Service Discovery solve?

### Answer

Service Discovery enables services to dynamically locate each other without relying on fixed IP addresses. This is
essential in environments where instances are frequently created, terminated, or rescheduled.

______________________________________________________________________

## Question

What is the difference between client-side and server-side discovery?

### Answer

In client-side discovery, the client queries the Service Registry and selects a service instance. In server-side
discovery, the client sends requests to a Load Balancer or API Gateway, which performs the lookup and routing.

______________________________________________________________________

## Question

Why is Service Discovery important in microservices?

### Answer

Microservices are independently deployed and scaled. Service Discovery allows them to communicate reliably despite
changing network locations, enabling dynamic scaling and resilient architectures.

______________________________________________________________________

# Practice Exercise

For each architecture,

identify

1. Is Service Discovery required?
1. Would client-side or server-side discovery be better?
1. How should health checks work?
1. Should DNS be involved?
1. Would Kubernetes simplify discovery?

Architectures

- E-commerce Platform
- Banking System
- Ride Sharing
- Food Delivery
- Social Media
- Video Streaming
- Chat Application

Explain

your reasoning

based on

scalability,

availability,

and

operational simplicity.

______________________________________________________________________

# Summary

Service Discovery is a critical component of modern distributed systems.

It enables

- Dynamic service registration
- Automatic service lookup
- Health monitoring
- Fault tolerance
- Horizontal scaling

It works closely with

- Load Balancers
- API Gateways
- Kubernetes
- DNS

Understanding Service Discovery is essential for designing resilient microservice architectures and is a common topic in
senior backend and System Design interviews.

______________________________________________________________________

# Next

[Database Partitioning (Horizontal vs Vertical)](19-database-partitioning.md)
