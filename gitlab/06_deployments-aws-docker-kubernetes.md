# Deployments AWS Docker Kubernetes

> File: `06_deployments-aws-docker-kubernetes.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Deploy applications using GitHub Actions
- Understand deployment workflows for AWS
- Push Docker images to Amazon ECR
- Deploy to Amazon ECS
- Deploy to Kubernetes
- Deploy applications using Helm
- Secure deployments using GitHub OIDC
- Configure GitHub Environments
- Implement production approvals
- Design zero-downtime deployment pipelines
- Answer deployment-related interview questions

______________________________________________________________________

# Table of Contents

1. Deployment Overview
1. Deployment Targets
1. Docker Image Pipeline
1. Deploying to Amazon ECR
1. Deploying to Amazon ECS
1. Deploying to EC2
1. Deploying to Kubernetes
1. Deploying with Helm
1. GitHub Environments
1. Manual Approvals
1. GitHub Secrets
1. OIDC Authentication
1. SSH Deployment
1. Deployment Strategies
1. Zero Downtime Deployment
1. Production Deployment Flow
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# Deployment Overview

CI validates code.

CD deploys code.

Typical flow

```
Developer

↓

GitHub Actions

↓

Docker Image

↓

Container Registry

↓

Deployment Platform

↓

Application Running
```

______________________________________________________________________

# Common Deployment Targets

GitHub Actions can deploy to almost any platform.

Examples

```
Amazon EC2

Amazon ECS

Amazon EKS

Kubernetes

Azure Kubernetes Service

Google Kubernetes Engine

Docker Swarm

Virtual Machines

On-prem Servers
```

The deployment logic changes,

the CI pipeline usually doesn't.

______________________________________________________________________

# Container Deployment Flow

Modern applications rarely deploy source code.

Instead,

```
Source Code

↓

Docker Build

↓

Docker Image

↓

Container Registry

↓

Deployment
```

The same Docker image moves through

Development

↓

Staging

↓

Production

This guarantees consistency.

______________________________________________________________________

# Docker Build Pipeline

Typical steps

```
Checkout

↓

Install Dependencies

↓

Run Tests

↓

Build Docker Image

↓

Push Image

↓

Deploy
```

Docker build

```bash
docker build -t backend:v1 .
```

______________________________________________________________________

# Docker Tagging

Images should have meaningful tags.

Examples

```
latest

v1.2.0

20260807

abc1234
```

Many companies push multiple tags.

```
backend:v1.2.0

backend:latest

backend:abc1234
```

______________________________________________________________________

# Deploying to Amazon ECR

Amazon ECR is AWS's managed Docker registry.

Flow

```
Docker Build

↓

Authenticate

↓

Push Image

↓

Amazon ECR
```

Typical GitHub Actions sequence

```text
Configure AWS Credentials

↓

Login to ECR

↓

Build Docker Image

↓

Push Docker Image
```

After the push,

deployment systems pull the image from ECR.

______________________________________________________________________

# Deploying to Amazon ECS

Amazon ECS runs Docker containers.

Deployment flow

```
GitHub Actions

↓

Amazon ECR

↓

Amazon ECS

↓

Running Containers
```

Typical production deployment

```
Build Image

↓

Push ECR

↓

Update ECS Task Definition

↓

Deploy Service

↓

Wait for Healthy Tasks
```

______________________________________________________________________

## ECS Rolling Update

Suppose

```
Version 1

Running
```

Deployment

```
Start New Tasks

↓

Health Check

↓

Stop Old Tasks
```

No downtime if configured correctly.

______________________________________________________________________

# Deploying to Amazon EC2

Older but still common.

Flow

```
GitHub Actions

↓

SSH

↓

EC2

↓

Pull Docker Image

↓

Restart Container
```

Typical deployment commands

```bash
docker pull backend:v2
```

```bash
docker stop backend
```

```bash
docker run ...
```

______________________________________________________________________

## EC2 Deployment Diagram

```
GitHub Actions

↓

SSH

↓

EC2 Server

↓

Docker Pull

↓

Docker Run
```

Simple,

but requires server management.

______________________________________________________________________

# Deploying to Kubernetes

Kubernetes is one of the most common interview topics.

Flow

```
GitHub Actions

↓

Docker Image

↓

Container Registry

↓

kubectl

↓

Kubernetes Cluster
```

Deployment

```bash
kubectl apply -f deployment.yaml
```

or

```bash
kubectl rollout restart deployment backend
```

______________________________________________________________________

# Kubernetes Rolling Update

Suppose

```
5 Pods
```

Deployment

```
Pod 1 Updated

↓

Pod 2 Updated

↓

Pod 3 Updated

↓

Pod 4 Updated

↓

Pod 5 Updated
```

Traffic remains available.

______________________________________________________________________

# Monitoring Deployment

Useful commands

```bash
kubectl get pods
```

```bash
kubectl describe deployment backend
```

```bash
kubectl rollout status deployment backend
```

______________________________________________________________________

# Rollback

If deployment fails

```bash
kubectl rollout undo deployment backend
```

Very common interview question.

______________________________________________________________________

# Deploying with Helm

Instead of managing dozens of YAML files,

Helm packages them into a chart.

Without Helm

```
deployment.yaml

service.yaml

configmap.yaml

secret.yaml

ingress.yaml
```

With Helm

```
helm upgrade

↓

Chart

↓

Deployment
```

Typical command

```bash
helm upgrade backend chart/
```

Benefits

- Versioned deployments
- Reusable templates
- Easier configuration
- Rollback support

______________________________________________________________________

# GitHub Environments

GitHub provides deployment environments.

Example

```
Development

Testing

Staging

Production
```

Each environment can have

- Secrets
- Variables
- Protection rules
- Required reviewers

Example

```
Environment

↓

Production

↓

Requires Approval
```

______________________________________________________________________

# Manual Approvals

Many companies protect production.

Pipeline

```
Deploy Staging

↓

Approval

↓

Deploy Production
```

GitHub pauses the workflow until an authorized reviewer approves it.

Benefits

- Prevent accidental releases
- Better governance
- Safer deployments

______________________________________________________________________

# GitHub Secrets

Never store credentials in the repository.

Bad

```yaml
AWS_SECRET_KEY=abc123
```

Good

```
Repository

↓

Secrets

↓

AWS_SECRET_ACCESS_KEY
```

Workflow

```yaml
env:

  AWS_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY_ID }}
```

______________________________________________________________________

# OIDC Authentication

## Traditional Method

Historically,

GitHub Actions authenticated to AWS using long-lived IAM user credentials stored as GitHub Secrets.

```
GitHub Actions

↓

AWS Access Key

↓

AWS Secret Key

↓

AWS
```

Problems

- Long-lived credentials
- Secret rotation required
- Higher risk if leaked

______________________________________________________________________

## Modern Method — OIDC

OIDC (OpenID Connect) allows GitHub Actions to request **temporary AWS credentials** without storing AWS access keys.

Flow

```
GitHub Actions

↓

OIDC Token

↓

AWS IAM Role

↓

Temporary Credentials

↓

Deploy
```

Advantages

- No long-lived AWS keys
- Short-lived credentials
- Better security
- Easier credential management
- Recommended by AWS and GitHub

______________________________________________________________________

## High-Level Setup

1. Create an IAM Role in AWS.
1. Configure GitHub as an OIDC identity provider.
1. Allow the repository to assume the role.
1. Use the AWS credentials action in GitHub Actions.
1. Deploy using temporary credentials.

You don't need to memorize every setup step for interviews, but you should understand **why OIDC is preferred**.

______________________________________________________________________

# SSH Deployment

Sometimes applications are deployed directly to virtual machines.

Flow

```
GitHub Actions

↓

SSH

↓

Linux Server

↓

Restart Application
```

Usually performed using

- SSH keys
- Deployment scripts
- Docker Compose

Less common in modern Kubernetes-based organizations but still widely used.

______________________________________________________________________

# Deployment Strategies

Different systems deploy differently.

______________________________________________________________________

## Recreate

```
Stop Old Version

↓

Start New Version
```

Simple,

but causes downtime.

______________________________________________________________________

## Rolling

```
Old

↓

New

↓

Old

↓

New
```

Minimal downtime.

Most common.

______________________________________________________________________

## Blue-Green

```
Blue

↓

Green

↓

Switch Traffic
```

Instant rollback.

______________________________________________________________________

## Canary

```
5%

↓

25%

↓

50%

↓

100%
```

Gradual rollout.

______________________________________________________________________

# Zero Downtime Deployment

Requirements

- Health checks
- Multiple application instances
- Load balancer
- Rolling or Blue-Green deployment
- Readiness probes (Kubernetes)

Pipeline

```
Build

↓

Deploy New Version

↓

Health Check

↓

Switch Traffic

↓

Remove Old Version
```

Users experience no interruption.

______________________________________________________________________

# Production Deployment Flow

Example for a FastAPI service on Amazon ECS

```
Developer Push

↓

CI

↓

Tests

↓

Docker Build

↓

Push Amazon ECR

↓

Approval

↓

Deploy Amazon ECS

↓

Health Check

↓

Smoke Test

↓

Slack Notification
```

Production deployments should always be observable.

______________________________________________________________________

# Best Practices

- Deploy immutable Docker images.
- Never deploy directly from feature branches.
- Use GitHub Environments for staging and production.
- Prefer OIDC over long-lived AWS credentials.
- Keep deployment logic separate from CI.
- Perform smoke tests after deployment.
- Use rolling or Blue-Green deployments for production.
- Tag Docker images consistently.
- Monitor deployments until healthy.
- Keep rollback procedures documented and tested.

______________________________________________________________________

# Common Mistakes

## Deploying Untagged Images

Always use versioned image tags.

______________________________________________________________________

## Storing Cloud Credentials in Git

Use GitHub Secrets or OIDC.

______________________________________________________________________

## No Health Checks

A deployment isn't complete until the application is healthy.

______________________________________________________________________

## Deploying Without Rollback

Every deployment should have a recovery plan.

______________________________________________________________________

## Manual Server Changes

Avoid making production changes directly on servers.

Prefer automated deployments.

______________________________________________________________________

## Mixing CI and Production Deployment Logic

Keep validation and deployment as separate workflows when possible.

______________________________________________________________________

# Interview Deep Dive

## Q1. How would you deploy a Dockerized FastAPI application using GitHub Actions?

### Answer

I would build the Docker image after successful testing, tag it appropriately, push it to a container registry such as
Amazon ECR, and trigger a deployment workflow that updates the target platform, such as Amazon ECS or Kubernetes. After
deployment, I would run health checks and smoke tests before considering the deployment successful.

______________________________________________________________________

## Q2. Why is Amazon ECR used?

### Answer

Amazon ECR is a managed container registry that stores Docker images securely. CI pipelines push versioned images to
ECR, and deployment platforms such as ECS or EKS pull those images during deployment.

______________________________________________________________________

## Q3. Why is OIDC preferred over AWS access keys?

### Answer

OIDC eliminates the need to store long-lived AWS credentials in GitHub. GitHub Actions exchanges an OIDC token for
temporary AWS credentials by assuming an IAM role. This improves security, simplifies credential management, and reduces
the risk of leaked secrets.

______________________________________________________________________

## Q4. What is the difference between ECS and Kubernetes deployments?

### Answer

Both deploy containers, but ECS is AWS's managed container orchestration service with tight AWS integration and simpler
operational overhead. Kubernetes is cloud-agnostic, offers greater flexibility and portability, and supports advanced
orchestration features at the cost of additional complexity.

______________________________________________________________________

## Q5. What is the purpose of GitHub Environments?

### Answer

GitHub Environments provide deployment-specific configuration, secrets, variables, protection rules, and required
approvals. They help secure production deployments and separate environment-specific settings.

______________________________________________________________________

## Q6. How would you achieve zero downtime deployments?

### Answer

I would use rolling, Blue-Green, or Canary deployment strategies with multiple application instances behind a load
balancer. Health checks and readiness probes ensure traffic is routed only to healthy instances before old versions are
removed.

______________________________________________________________________

## Q7. What would you do if a deployment fails?

### Answer

I would stop further rollout, investigate logs and health checks, and roll back to the previous stable version.
Depending on the platform, this might involve redeploying the previous Docker image, using `kubectl rollout undo`, or
switching traffic back to the previous environment in a Blue-Green deployment.

______________________________________________________________________

## Q8. Why should Docker images be immutable?

### Answer

Immutable images ensure that the exact artifact tested during CI is the same artifact deployed to staging and
production. This improves reproducibility, simplifies debugging, and reduces environment-specific inconsistencies.

______________________________________________________________________

# Summary

In this chapter you learned:

- Deployment architecture
- Docker deployment pipeline
- Amazon ECR
- Amazon ECS
- Amazon EC2 deployment
- Kubernetes deployment
- Helm deployments
- GitHub Environments
- Manual approvals
- GitHub Secrets
- OIDC authentication
- SSH deployments
- Deployment strategies
- Zero-downtime deployments
- Production deployment flow
- Deployment interview questions

______________________________________________________________________

# Next

[Debugging Best Practices Security](07_debugging-best-practices-security.md)
