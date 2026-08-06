# ECS Concepts

> **Course:** AWS for Backend Engineers
>
> **Module:** 7
>
> **File:** `13_ecs_concepts.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Amazon ECS is
- Why ECS exists
- Containers vs Virtual Machines
- Container Orchestration
- ECS Architecture
- Clusters
- Tasks
- Task Definitions
- Services
- Scheduler
- Capacity Providers
- ECS Networking
- IAM Roles
- ECS Launch Types
- ECS vs Kubernetes
- Console
- AWS CLI
- AWS SDK (Python boto3)
- Production Architecture

______________________________________________________________________

# What is Amazon ECS?

**Amazon ECS (Elastic Container Service)** is AWS's **fully managed container orchestration service**.

It manages containers running your applications.

Instead of managing servers yourself,

you tell ECS:

> "Run 10 containers of my application."

ECS handles the rest.

______________________________________________________________________

# Why Was ECS Created?

Imagine running Docker manually.

```
docker run

↓

Server-1
```

Later

```
Server Crashes
```

Now someone must

- Restart containers
- Launch new servers
- Monitor failures
- Scale manually

This quickly becomes difficult.

______________________________________________________________________

# Real World Analogy

Imagine a hotel.

Guests

↓

Rooms

↓

Hotel Manager

The hotel manager ensures:

- Enough rooms
- Clean rooms
- New guests get rooms
- Broken rooms replaced

ECS is the manager.

Containers are the guests.

______________________________________________________________________

# Before ECS

```
Developer

↓

SSH

↓

docker run

↓

docker stop

↓

docker restart
```

Everything is manual.

______________________________________________________________________

# After ECS

```
Developer

↓

Deploy

↓

ECS

↓

Run Containers

↓

Monitor

↓

Replace Failed Containers

↓

Scale Automatically
```

______________________________________________________________________

# What is Container Orchestration?

Container Orchestration means

automatically managing containers.

Tasks include:

- Scheduling
- Scaling
- Restarting
- Networking
- Service Discovery
- Rolling Updates
- Load Balancing

ECS performs these tasks automatically.

______________________________________________________________________

# ECS Architecture

```
ECS Cluster

↓

Service

↓

Tasks

↓

Containers
```

______________________________________________________________________

# ECS Components

The major ECS components are:

- Cluster
- Task Definition
- Task
- Service
- Scheduler
- Capacity Provider

Let's understand each.

______________________________________________________________________

# Cluster

A Cluster is a logical grouping of compute capacity where containers run.

Example

```
Production Cluster

↓

Backend API

↓

Frontend

↓

Redis
```

Clusters organize workloads.

______________________________________________________________________

# Task Definition

A Task Definition is a blueprint for running containers.

Similar to

```
AMI

↓

EC2
```

Task Definition

↓

Task

It defines:

- Docker Image
- CPU
- Memory
- Environment Variables
- Ports
- Logging
- IAM Roles
- Volumes

______________________________________________________________________

# Example Task Definition

```
Image

↓

backend-api:v2.0

CPU

↓

512

Memory

↓

1024 MB

Port

↓

8000
```

______________________________________________________________________

# Task

A Task is a **running instance** of a Task Definition.

Example

```
Task Definition

↓

Launch

↓

Task
```

Think of it as

```
Docker Image

↓

Running Container
```

______________________________________________________________________

# Service

A Service keeps the desired number of Tasks running.

Example

```
Desired Tasks

↓

5
```

If one task crashes

```
Running

4

↓

ECS

↓

Launch New Task

↓

Running

5
```

Exactly like an Auto Scaling Group for containers.

______________________________________________________________________

# Scheduler

The Scheduler decides:

- Where containers run
- When to replace them
- When to stop them
- When to launch new ones

Developers don't need to make these decisions manually.

______________________________________________________________________

# Capacity Provider

A Capacity Provider tells ECS **where** tasks should run.

Examples

- EC2 Instances
- AWS Fargate

It allows flexible scaling and capacity management.

______________________________________________________________________

# ECS Launch Types

ECS supports two primary launch types:

- EC2
- Fargate

A detailed comparison is covered in the next chapter.

______________________________________________________________________

# ECS Networking

Every task requires networking.

ECS integrates with:

- VPC
- Subnets
- Security Groups
- Elastic Network Interfaces

Containers become part of your AWS network.

______________________________________________________________________

# awsvpc Network Mode

The most commonly used network mode.

Each task receives:

- Private IP
- Elastic Network Interface (ENI)
- Security Groups

Tasks behave similarly to EC2 instances from a networking perspective.

______________________________________________________________________

# IAM Roles

ECS supports two important IAM roles.

______________________________________________________________________

## Task Role

Permissions used **by the application**.

Example

```
Application

↓

Read S3

↓

Task Role
```

______________________________________________________________________

## Task Execution Role

Permissions used by ECS itself.

Examples

- Pull image from ECR
- Write logs to CloudWatch

The application normally doesn't use this role directly.

______________________________________________________________________

# Logging

Applications running in ECS commonly send logs to

```
CloudWatch Logs
```

Benefits

- Centralized logging
- Easier debugging
- Searchable logs
- Integration with CloudWatch alarms

______________________________________________________________________

# Load Balancer Integration

Typical architecture

```
Users

↓

Application Load Balancer

↓

ECS Service

↓

Tasks
```

Traffic is distributed automatically.

______________________________________________________________________

# Service Discovery

Applications often need to communicate.

Example

```
Payment Service

↓

Inventory Service
```

Instead of hardcoding IP addresses,

ECS integrates with service discovery mechanisms so services can locate each other reliably.

______________________________________________________________________

# ECS Deployment Flow

```
Git Push

↓

CI/CD

↓

Docker Build

↓

Push ECR

↓

Update ECS Service

↓

Rolling Deployment
```

______________________________________________________________________

# ECS vs Docker

Docker

- Runs containers

ECS

- Manages containers

Analogy

Docker

```
Car
```

ECS

```
Traffic Management System
```

______________________________________________________________________

# ECS vs Kubernetes

| Feature | ECS | Kubernetes |
|----------|-----|------------|
| AWS Native | ✅ | ❌ |
| Easier to Learn | ✅ | ❌ |
| Operational Complexity | Lower | Higher |
| Vendor Neutral | ❌ | ✅ |
| Ecosystem | AWS-focused | Large, multi-cloud |

Choose based on organizational requirements.

______________________________________________________________________

# AWS Console

Using the Console you can:

- Create Clusters
- Register Task Definitions
- Deploy Services
- Scale Services
- View Running Tasks
- Update Images
- Monitor Deployments

______________________________________________________________________

# AWS CLI

## List Clusters

```bash
aws ecs list-clusters
```

______________________________________________________________________

## Create Cluster

```bash
aws ecs create-cluster \
    --cluster-name production
```

______________________________________________________________________

## List Services

```bash
aws ecs list-services \
    --cluster production
```

______________________________________________________________________

## List Tasks

```bash
aws ecs list-tasks \
    --cluster production
```

______________________________________________________________________

## Describe Tasks

```bash
aws ecs describe-tasks \
    --cluster production \
    --tasks TASK_ID
```

______________________________________________________________________

# AWS SDK (Python boto3)

## Installation

```bash
pip install boto3
```

______________________________________________________________________

## Create Client

```python
import boto3

ecs = boto3.client("ecs")
```

______________________________________________________________________

## List Clusters

```python
response = ecs.list_clusters()

print(response["clusterArns"])
```

______________________________________________________________________

## Create Cluster

```python
ecs.create_cluster(
    clusterName="production"
)
```

______________________________________________________________________

## List Tasks

```python
response = ecs.list_tasks(
    cluster="production"
)

print(response["taskArns"])
```

______________________________________________________________________

# Typical Production Architecture

```
Internet

↓

Application Load Balancer

↓

ECS Service

↓

Tasks

↓

ECR

↓

CloudWatch Logs

↓

RDS

↓

S3
```

______________________________________________________________________

# Common ECS Operations

Daily operations include:

- Register new Task Definitions
- Deploy new application versions
- Scale Services
- Restart failed Tasks
- View logs
- Update environment variables
- Roll back deployments
- Monitor container health

______________________________________________________________________

# Common Mistakes

❌ Running stateful applications inside containers without persistent storage

❌ Using one huge container for every service

❌ Hardcoding secrets into Docker images

❌ Using excessive CPU and memory reservations

❌ Running containers without health checks

❌ Giving Task Roles excessive permissions

❌ Ignoring container logs

______________________________________________________________________

# Production Best Practices

- Build stateless containers.
- Store persistent data outside containers.
- Use IAM Task Roles.
- Store secrets in Secrets Manager or Parameter Store.
- Send logs to CloudWatch.
- Deploy behind an Application Load Balancer.
- Use health checks.
- Keep Task Definitions versioned.
- Automate deployments through CI/CD.

______________________________________________________________________

# Interview Deep Dive

### Question

**Explain the relationship between an ECS Cluster, Service, Task Definition, and Task.**

### Answer

The components build on each other:

1. A **Cluster** provides the logical environment where containers run.
1. A **Task Definition** is the blueprint describing how a container should run (image, CPU, memory, ports, environment variables, IAM roles, etc.).
1. A **Task** is a running instance of a Task Definition.
1. A **Service** manages Tasks by maintaining the desired number of running instances, replacing failed Tasks, and supporting deployments.

The relationship can be summarized as:

```
Cluster

↓

Service

↓

Task Definition

↓

Running Tasks
```

______________________________________________________________________

# Summary

In this chapter you learned:

- What Amazon ECS is
- Container Orchestration
- Clusters
- Task Definitions
- Tasks
- Services
- Scheduler
- Capacity Providers
- ECS Networking
- IAM Task Roles
- Task Execution Roles
- Logging
- Load Balancer Integration
- ECS vs Docker
- ECS vs Kubernetes
- AWS Console
- AWS CLI
- boto3 SDK
- Production best practices

Amazon ECS simplifies running containerized applications by automating scheduling, scaling, networking, health
monitoring, and deployments.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon ECS?
1. Why was ECS created?
1. What is Container Orchestration?
1. How is ECS different from Docker?
1. How is ECS different from Kubernetes?

______________________________________________________________________

## Core Components

6. What is an ECS Cluster?
1. What is a Task Definition?
1. What is a Task?
1. What is an ECS Service?
1. What is the purpose of the ECS Scheduler?
1. What is a Capacity Provider?

______________________________________________________________________

## Networking & Security

12. What is the `awsvpc` network mode?
01. Why does each ECS Task receive its own ENI?
01. What is the difference between a Task Role and a Task Execution Role?
01. Why should applications use IAM Task Roles?

______________________________________________________________________

## Deployment

16. How does ECS integrate with ECR?
01. Why is an Application Load Balancer commonly used with ECS?
01. Why are health checks important?
01. Why should containers remain stateless?

______________________________________________________________________

## CLI & SDK

20. Which CLI command lists ECS clusters?
01. Which CLI command creates a cluster?
01. Which boto3 method creates a cluster?

______________________________________________________________________

## Scenario-Based

23. Your application currently runs with five ECS Tasks. One task crashes unexpectedly. What will the ECS Service do?
01. Your backend API needs to read files from Amazon S3. Which IAM role should receive the S3 permissions?
01. Your team stores database passwords directly inside the Docker image. Why is this a poor practice, and what would you recommend instead?
01. Your organization deploys new application versions every day. How do Task Definitions help manage deployments?
01. Your application is experiencing uneven traffic throughout the day. Which ECS components would you combine with Auto Scaling and a Load Balancer to maintain availability while controlling costs?

______________________________________________________________________

## Next

[ECS Fargate](14_ecs_fargate.md)
