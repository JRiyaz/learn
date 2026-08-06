# End-to-End Backend Deployment

> **Course:** AWS for Backend Engineers
>
> **Module:** 8
>
> **File:** `16_end_to_end_backend_deployment.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- End-to-End AWS Architecture
- How All AWS Services Work Together
- Request Flow
- Deployment Flow
- Authentication Flow
- File Upload Flow
- Logging Flow
- Monitoring Flow
- Auto Scaling Flow
- Failure Recovery
- Disaster Recovery
- Production Best Practices

______________________________________________________________________

# The Big Picture

Throughout this course, we've learned individual AWS services.

Now we'll connect everything together into a **real production backend architecture**.

This architecture is similar to what many companies use for production web applications.

______________________________________________________________________

# Overall Architecture

```
                        Users
                           │
                           ▼
                  Route 53 (DNS)
                           │
                           ▼
                Application Load Balancer
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
   ECS Task (AZ-A)                      ECS Task (AZ-B)
        │                                     │
        └──────────────┬──────────────────────┘
                       ▼
                 FastAPI Application
                       │
        ┌──────────────┼──────────────────────┐
        ▼              ▼                      ▼
      Amazon S3     Amazon RDS        CloudWatch Logs
        │
        ▼
   User Uploads

```

Every service has a specific responsibility.

______________________________________________________________________

# Step 1 — User Request

User

```
https://api.company.com/login
```

↓

DNS resolves

↓

Application Load Balancer

↓

Healthy ECS Task

↓

FastAPI

↓

Response

______________________________________________________________________

# Step 2 — Load Balancer

The Application Load Balancer receives every request.

Responsibilities

- HTTPS termination
- SSL certificates
- Health checks
- Traffic distribution
- High availability

Instead of

```
Users

↓

Server
```

we use

```
Users

↓

ALB

↓

Many Containers
```

______________________________________________________________________

# Step 3 — ECS Service

The ECS Service maintains

```
Desired Tasks

↓

6
```

If one crashes

```
5 Running

↓

Launch New Task

↓

6 Running
```

Automatically.

______________________________________________________________________

# Step 4 — Docker Container

Each ECS Task runs

```
FastAPI

↓

Gunicorn

↓

Uvicorn Workers
```

The application itself remains stateless.

______________________________________________________________________

# Step 5 — Database Access

Application

↓

IAM Role

↓

Secrets Manager

↓

Database Password

↓

Amazon RDS

Database credentials are never stored in code.

______________________________________________________________________

# Step 6 — File Upload

Suppose the user uploads

```
profile.png
```

Flow

```
Client

↓

Backend

↓

Generate Presigned URL

↓

Client

↓

Amazon S3
```

Backend does **not** process large file uploads.

______________________________________________________________________

# Why Use Presigned URLs?

Bad

```
User

↓

Backend

↓

S3
```

Problems

- Higher bandwidth costs
- Increased CPU usage
- Slower uploads

Better

```
Backend

↓

Signed URL

↓

User

↓

S3
```

Much more scalable.

______________________________________________________________________

# Step 7 — Reading Files

User

↓

CloudFront (optional but common)

↓

S3

↓

Image

CloudFront caches content closer to users, reducing latency.

______________________________________________________________________

# Step 8 — Logging

Application

↓

stdout

↓

CloudWatch Logs

Log Example

```
INFO

POST /login

200

125 ms
```

______________________________________________________________________

# Step 9 — Monitoring

CloudWatch monitors

Infrastructure

- CPU
- Memory
- Network

Application

- Error Rate
- Latency
- Requests
- Business Metrics

Operations teams view dashboards and receive alarms.

______________________________________________________________________

# Step 10 — Auto Scaling

Suppose traffic increases.

```
500 Users

↓

5000 Users
```

CloudWatch detects

↓

High CPU

↓

Service Auto Scaling

↓

More ECS Tasks

↓

Load Balancer distributes traffic

No manual intervention required.

______________________________________________________________________

# Step 11 — Authentication

User

↓

JWT Login

↓

Application

↓

Database

↓

Generate JWT

↓

Client

AWS IAM is **not** used for authenticating application users.

IAM secures AWS resources.

Your application still needs its own authentication system.

______________________________________________________________________

# Step 12 — Secrets

Application needs

- Database Password
- API Keys
- JWT Secret

Flow

```
Task Role

↓

Secrets Manager

↓

Application
```

Never

```
GitHub

↓

Secrets
```

______________________________________________________________________

# Step 13 — Image Deployment

Developer

↓

Git Push

↓

GitHub Actions

↓

Run Tests

↓

Docker Build

↓

Push Image

↓

Amazon ECR

↓

Update ECS Service

↓

Rolling Deployment

No manual deployment.

______________________________________________________________________

# Step 14 — Failure Recovery

Suppose

```
Task Crash
```

↓

ECS detects failure

↓

Launch New Task

↓

ALB Health Check

↓

Traffic resumes

Users often never notice.

______________________________________________________________________

# Step 15 — Availability Zone Failure

Suppose

```
AZ-A

↓

Power Failure
```

Remaining architecture

```
ALB

↓

AZ-B

↓

Running Tasks
```

Application remains available, although capacity may temporarily decrease until replacement tasks start.

______________________________________________________________________

# Step 16 — Database Backup

Amazon RDS

↓

Automated Backups

↓

Snapshots

↓

Recovery

Production databases should always have backup strategies.

______________________________________________________________________

# Step 17 — Object Storage

Application never stores files inside containers.

Instead

```
Uploads

↓

S3

↓

Versioning

↓

Lifecycle Rules

↓

Archive
```

Containers remain disposable.

______________________________________________________________________

# Step 18 — IAM

Each ECS Task receives

```
Task Role
```

Permissions

```
Read S3

↓

Write CloudWatch

↓

Read Secrets

↓

Nothing Else
```

Least Privilege.

______________________________________________________________________

# Step 19 — Networking

```
Internet

↓

ALB

↓

Public Subnet

↓

Private Subnets

↓

ECS Tasks

↓

RDS
```

Only the ALB is publicly accessible.

______________________________________________________________________

# Step 20 — Security

Security layers

```
HTTPS

↓

Security Groups

↓

Private Subnets

↓

IAM

↓

Encryption

↓

Secrets Manager
```

Multiple layers reduce risk.

______________________________________________________________________

# Complete Production Flow

```
Client

↓

Route53

↓

Application Load Balancer

↓

ECS Service

↓

FastAPI

↓

Task Role

↓

Amazon RDS

↓

Amazon S3

↓

CloudWatch

↓

Response
```

______________________________________________________________________

# Complete CI/CD Flow

```
Developer

↓

Git Push

↓

GitHub Actions

↓

Run Tests

↓

Docker Build

↓

Push ECR

↓

Deploy ECS

↓

Rolling Deployment

↓

Health Checks

↓

Traffic Shift
```

______________________________________________________________________

# Monitoring Flow

```
Application

↓

CloudWatch Logs

↓

Metric Filters

↓

CloudWatch Metrics

↓

Alarms

↓

SNS

↓

Operations Team
```

______________________________________________________________________

# Scaling Flow

```
Traffic

↓

CloudWatch Metrics

↓

Target Tracking Policy

↓

ECS Auto Scaling

↓

Launch New Tasks

↓

ALB

↓

Users
```

______________________________________________________________________

# Failure Recovery Flow

```
Container Crash

↓

Health Check Failed

↓

ECS Stops Task

↓

Launch New Task

↓

Healthy

↓

Traffic Resumes
```

______________________________________________________________________

# Security Checklist

✅ Private Subnets

✅ HTTPS

✅ IAM Roles

✅ Secrets Manager

✅ CloudWatch Logs

✅ ECR Image Scanning

✅ Least Privilege

✅ Security Groups

✅ Versioned Deployments

______________________________________________________________________

# Cost Optimization Checklist

- Right-size task CPU and memory.
- Enable Auto Scaling.
- Use S3 Lifecycle Rules.
- Remove unused ECR images.
- Archive old logs.
- Delete unused resources.
- Monitor AWS costs regularly.

______________________________________________________________________

# Common Mistakes

❌ Uploading files through the backend instead of using Presigned URLs

❌ Storing uploads inside containers

❌ One ECS Task only

❌ No Load Balancer

❌ No Auto Scaling

❌ Hardcoded AWS credentials

❌ Public databases

❌ Mutable image tags

❌ No monitoring

______________________________________________________________________

# Production Best Practices

- Build stateless services.
- Use immutable Docker images.
- Deploy across multiple AZs.
- Keep databases private.
- Use IAM Roles.
- Enable monitoring and alarms.
- Store secrets securely.
- Automate deployments.
- Test rollback procedures.
- Design for failure.

______________________________________________________________________

# Interview Deep Dive

### Question

**Design a production-ready backend architecture on AWS for a FastAPI application that supports file uploads, automatic
scaling, and high availability.**

### Answer

A production architecture would include:

1. Route 53 for DNS.
1. An Application Load Balancer deployed across multiple Availability Zones.
1. An ECS Service (EC2 or Fargate) running multiple FastAPI tasks.
1. Auto Scaling based on CPU utilization or request count.
1. Amazon ECR to store container images.
1. Amazon RDS in private subnets for relational data.
1. Amazon S3 for user uploads using Presigned URLs.
1. IAM Task Roles for secure AWS access.
1. AWS Secrets Manager for database credentials and API secrets.
1. CloudWatch Logs, metrics, dashboards, and alarms for observability.
1. Rolling or Blue-Green deployments through an automated CI/CD pipeline.
1. Security Groups, private subnets, HTTPS, and least-privilege IAM policies for security.

This design provides scalability, resilience, operational visibility, and secure handling of application resources.

______________________________________________________________________

# Summary

You now understand how the following AWS services work together:

- IAM
- EC2
- S3
- VPC
- CloudWatch
- ECR
- ECS
- Application Load Balancer
- Route 53
- Secrets Manager
- Amazon RDS

Instead of thinking of these services independently, you should now view them as components of one production platform.

______________________________________________________________________

# Practice Questions

## Architecture

1. Explain the complete request flow from a user's browser to a FastAPI application running on ECS.
1. Why is an Application Load Balancer required?
1. Why should ECS Tasks remain stateless?
1. Why are uploads stored in S3 instead of inside containers?

______________________________________________________________________

## Security

5. How should an ECS application obtain database credentials?
1. Why are IAM Roles preferred over Access Keys?
1. Why should databases remain in private subnets?

______________________________________________________________________

## Deployment

8. Describe a CI/CD pipeline for deploying containerized applications on AWS.
1. Why are immutable image versions important?
1. Why is a rolling deployment safer than replacing every task simultaneously?

______________________________________________________________________

## Monitoring

11. Which CloudWatch features would you use to monitor this architecture?
01. How would you detect increased API error rates?
01. What metrics would you use for Auto Scaling?

______________________________________________________________________

## Failure Handling

14. What happens if an ECS Task crashes?
01. What happens if an entire Availability Zone becomes unavailable?
01. How would you recover from accidental database corruption?

______________________________________________________________________

## Scenario-Based

17. Your backend API becomes unavailable after a deployment. Which components would you investigate first?
01. Your application receives ten times more traffic than usual during a marketing campaign. How does the architecture respond?
01. Your security audit discovers AWS credentials committed to GitHub. How would you redesign the authentication approach?
01. A customer uploads a 5 GB video. Why should the backend avoid proxying the upload?
01. Your organization requires zero-downtime deployments and immediate rollback capability. Which deployment strategy would you recommend?
01. A new engineer asks why the application uses ECS, ECR, S3, CloudWatch, IAM, and an ALB instead of only EC2 instances. How would you explain the purpose of each service?

______________________________________________________________________

## Next

[AWS CLI Cookbook](17_aws_cli_cookbook.md)
