# ECS Fargate

> **Course:** AWS for Backend Engineers
>
> **Module:** 7
>
> **File:** `14_ecs_fargate.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- EC2 Launch Type
- AWS Fargate
- EC2 vs Fargate
- Fargate Architecture
- Task Networking
- Task Execution Flow
- IAM Roles
- CPU & Memory Configuration
- Storage
- Scaling
- Cost Model
- Security
- Production Best Practices
- When to Choose EC2
- When to Choose Fargate

______________________________________________________________________

# Why Two Launch Types?

ECS manages containers.

But where should the containers actually run?

AWS provides two options.

```
ECS

↓

EC2

or

↓

Fargate
```

The orchestration layer is the same.

The compute layer changes.

______________________________________________________________________

# EC2 Launch Type

With EC2 launch type,

**you manage the servers.**

Architecture

```
ECS

↓

EC2 Instances

↓

Docker

↓

Containers
```

You are responsible for:

- EC2 provisioning
- OS updates
- Security patches
- Instance scaling
- Capacity planning
- AMI updates

______________________________________________________________________

# Real World Analogy

EC2 Launch Type

Imagine renting an apartment.

You must manage:

- Electricity
- Furniture
- Repairs
- Maintenance

You have full control,

but also full responsibility.

______________________________________________________________________

# Fargate

**AWS Fargate is serverless compute for containers.**

There are still servers,

but AWS manages them.

You only define:

- Docker Image
- CPU
- Memory
- Networking

AWS runs everything else.

______________________________________________________________________

# Real World Analogy

Fargate is like staying in a hotel.

You simply request a room.

The hotel manages:

- Building
- Cleaning
- Electricity
- Repairs

You only use the room.

______________________________________________________________________

# EC2 vs Fargate

```
Developer

↓

Docker Image

↓

ECS

↓

EC2

↓

Containers
```

vs

```
Developer

↓

Docker Image

↓

ECS

↓

Fargate

↓

Containers
```

Same application.

Different infrastructure management.

______________________________________________________________________

# Fargate Architecture

```
Internet

↓

Application Load Balancer

↓

ECS Service

↓

Fargate Tasks

↓

CloudWatch Logs

↓

RDS

↓

S3
```

No EC2 instances are visible to you.

______________________________________________________________________

# What AWS Manages

With Fargate,

AWS manages:

- Servers
- Operating System
- Docker Runtime
- Capacity
- Scaling Infrastructure
- Availability

You manage:

- Application
- Container Image
- IAM
- Networking
- Application Configuration

______________________________________________________________________

# Task Networking

Each Fargate Task receives:

- Elastic Network Interface (ENI)
- Private IP Address
- Security Groups

Tasks appear as first-class network resources inside your VPC.

______________________________________________________________________

# Fargate Task Lifecycle

```
Task Definition

↓

Task Requested

↓

AWS Allocates Compute

↓

Container Starts

↓

Application Runs

↓

Task Stops
```

No server management required.

______________________________________________________________________

# Task Execution Flow

```
Task Definition

↓

Pull Image

↓

Amazon ECR

↓

Start Container

↓

Health Check

↓

Running
```

______________________________________________________________________

# CPU & Memory Configuration

Unlike EC2,

you don't choose an instance type.

Instead,

choose resources for the task.

Example

```
CPU

0.5 vCPU

Memory

1 GB
```

or

```
CPU

2 vCPU

Memory

4 GB
```

Only supported CPU-memory combinations can be selected.

______________________________________________________________________

# Ephemeral Storage

Each Fargate task receives temporary storage.

Useful for:

- Temporary files
- Downloads
- Processing

Do **not** store important application data here.

Persistent data belongs in services like:

- Amazon S3
- Amazon RDS
- Amazon EFS

______________________________________________________________________

# Persistent Storage

Applications should remain stateless.

Example

```
Container

↓

Upload Image

↓

Amazon S3
```

Instead of

```
Container

↓

Local Disk
```

______________________________________________________________________

# IAM Roles

Fargate uses:

Task Role

↓

Application Permissions

Task Execution Role

↓

Infrastructure Permissions

Exactly the same concepts used with ECS on EC2.

______________________________________________________________________

# Scaling

Scaling works exactly like ECS.

```
Traffic Increases

↓

ECS Service Auto Scaling

↓

More Fargate Tasks
```

No EC2 instances need to be created or managed manually.

______________________________________________________________________

# Cost Model

With EC2

Pay for:

```
Entire Server
```

Even if only one container is running.

______________________________________________________________________

With Fargate

Pay for:

```
CPU

+

Memory

Used by Running Tasks
```

This is often economical for variable workloads and smaller services.

______________________________________________________________________

# Startup Time

Fargate

```
Request Task

↓

AWS Allocates Compute

↓

Container Starts
```

Startup may be slightly slower than launching on already-running EC2 capacity, depending on the environment and
workload.

______________________________________________________________________

# Security Advantages

Since there is no server management,

you don't worry about:

- OS patching
- Docker updates
- Kernel maintenance

AWS manages the underlying infrastructure.

You still remain responsible for:

- IAM
- Application security
- Container image security
- Secrets management

______________________________________________________________________

# Fargate Limitations

Compared to EC2,

you have less control.

Examples

Cannot manage:

- Host Operating System
- Host-level software
- Custom kernel modules
- Direct access to underlying hardware

______________________________________________________________________

# When to Use Fargate

Excellent for:

- APIs
- Microservices
- Backend services
- Scheduled jobs
- Event-driven applications
- Teams without infrastructure specialists

______________________________________________________________________

# When to Use EC2 Launch Type

Prefer EC2 when you need:

- Host-level customization
- Specialized hardware
- GPU workloads (where supported through ECS on EC2)
- Daemon containers
- Maximum infrastructure control
- Very large, consistently utilized clusters where cost optimization justifies managing servers

______________________________________________________________________

# ECS EC2 vs Fargate

| Feature | EC2 | Fargate |
|----------|------|----------|
| Server Management | You | AWS |
| OS Updates | You | AWS |
| Capacity Planning | You | AWS |
| Infrastructure Control | High | Limited |
| Simplicity | Lower | Higher |
| Operational Overhead | Higher | Lower |
| Pay For | EC2 Instances | Running Tasks |

______________________________________________________________________

# Fargate Deployment Flow

```
Git Push

↓

GitHub Actions

↓

Docker Build

↓

Push Image

↓

Amazon ECR

↓

Update ECS Service

↓

Launch Fargate Tasks
```

______________________________________________________________________

# Example Production Architecture

```
Internet

↓

Application Load Balancer

↓

Fargate Service

↓

Task Role

↓

CloudWatch Logs

↓

Amazon RDS

↓

Amazon S3

↓

Secrets Manager
```

No EC2 administration required.

______________________________________________________________________

# Common Mistakes

❌ Treating Fargate tasks like virtual machines

❌ Storing uploaded files inside containers

❌ Giving Task Roles excessive permissions

❌ Hardcoding secrets inside images

❌ Ignoring task CPU and memory sizing

❌ Running stateful workloads without external storage

______________________________________________________________________

# Production Best Practices

- Build stateless applications.
- Store uploads in S3.
- Store persistent data in RDS or EFS.
- Use Task Roles.
- Store secrets in AWS Secrets Manager or Systems Manager Parameter Store.
- Send logs to CloudWatch.
- Use Application Load Balancers.
- Enable Service Auto Scaling.
- Deploy across multiple Availability Zones.
- Version Task Definitions.

______________________________________________________________________

# Interview Deep Dive

### Question

**Your team wants to migrate from ECS on EC2 to ECS on Fargate. What changes in your operational responsibilities?**

### Answer

The application architecture can remain largely the same, but infrastructure responsibilities change.

With ECS on EC2, the team manages:

1. EC2 instances
1. Operating system updates
1. Docker runtime updates
1. Capacity planning
1. Auto Scaling Groups
1. AMIs and patching

With Fargate, AWS manages the underlying compute infrastructure.

The engineering team continues to manage:

- Container images
- Task Definitions
- IAM Roles
- Networking
- Scaling policies
- Application code
- Logging and monitoring

Operational overhead is reduced because there are no servers to administer.

______________________________________________________________________

# Summary

In this chapter you learned:

- EC2 Launch Type
- AWS Fargate
- Task Networking
- CPU & Memory Configuration
- Ephemeral Storage
- IAM Roles
- Scaling
- Cost Model
- Security
- EC2 vs Fargate
- Production architecture
- Best practices

AWS Fargate enables teams to run containers without managing servers, making it an excellent choice for many modern
microservice architectures.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is AWS Fargate?
1. Why was Fargate created?
1. What is the primary difference between ECS on EC2 and ECS on Fargate?
1. Why is Fargate considered "serverless"?

______________________________________________________________________

## Architecture

5. What infrastructure does AWS manage in Fargate?
1. What infrastructure does the customer still manage?
1. What resources does each Fargate Task receive?
1. Explain the Fargate task lifecycle.

______________________________________________________________________

## Storage

9. What is ephemeral storage?
1. Why shouldn't uploaded user files be stored inside Fargate containers?
1. Which AWS services should be used for persistent storage?

______________________________________________________________________

## Scaling & Cost

12. How does Fargate scale?
01. How is Fargate pricing different from ECS on EC2?
01. Why can EC2 be more cost-effective for consistently high utilization?

______________________________________________________________________

## Security

15. What is the difference between a Task Role and a Task Execution Role?
01. Which security responsibilities remain with the customer when using Fargate?
01. Why should secrets be stored outside container images?

______________________________________________________________________

## Architecture Decisions

18. When is Fargate a good choice?
01. When would you choose ECS on EC2 instead?
01. Why are stateless applications recommended for Fargate?

______________________________________________________________________

## Scenario-Based

21. Your startup has a small DevOps team and wants to minimize infrastructure management. Which ECS launch type would you recommend?
01. Your application requires installing custom kernel modules on the host operating system. Can Fargate support this requirement? Why or why not?
01. Your backend service stores uploaded files in `/tmp` inside a Fargate container. What risks does this create?
01. Your workload experiences unpredictable traffic spikes throughout the day. How does Fargate help simplify operations?
01. Your company runs thousands of long-lived containers with stable resource usage. What factors would you consider when choosing between EC2 launch type and Fargate?

______________________________________________________________________

## Next

[ECS Production](15_ecs_production.md)
