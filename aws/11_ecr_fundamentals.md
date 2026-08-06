# ECR Fundamentals

> **Course:** AWS for Backend Engineers
>
> **Module:** 6
>
> **File:** `11_ecr_fundamentals.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Amazon ECR is
- Why ECR exists
- Docker Images
- Container Registries
- Public vs Private Repositories
- ECR Architecture
- Authentication
- Image Tags
- Image Digests
- AWS Console
- AWS CLI
- Docker CLI
- AWS SDK (Python boto3)
- Common ECR Operations
- Production Best Practices

______________________________________________________________________

# What is Amazon ECR?

**Amazon Elastic Container Registry (ECR)** is AWS's **managed Docker container registry**.

It stores container images securely so they can later be deployed to:

- ECS
- EKS
- AWS Lambda (container images)
- EC2
- Local Docker environments

Think of ECR as **GitHub for Docker images**.

Instead of storing source code,

it stores container images.

______________________________________________________________________

# Why Was ECR Created?

Imagine building a Docker image.

```
Backend API

↓

Docker Build

↓

Image
```

Where should the image be stored?

Without a registry,

every deployment machine would have to build the image again.

Instead

```
Developer

↓

Docker Image

↓

ECR

↓

ECS

↓

Production
```

One image.

Many deployments.

______________________________________________________________________

# Real World Analogy

Imagine a warehouse.

```
Products

↓

Warehouse

↓

Stores
```

In Docker

```
Image

↓

ECR

↓

Containers
```

The warehouse stores products.

Stores receive products when needed.

______________________________________________________________________

# Container Registry

A Container Registry stores container images.

Popular registries

- Amazon ECR
- Docker Hub
- GitHub Container Registry
- Google Artifact Registry
- Azure Container Registry

______________________________________________________________________

# What is a Docker Image?

A Docker Image is a **read-only template** used to create containers.

Example

```
Python

↓

FastAPI

↓

Dependencies

↓

Application Code

↓

Docker Image
```

______________________________________________________________________

# Image vs Container

Image

```
Blueprint
```

Container

```
Running Application
```

Exactly like

```
Class

↓

Object
```

You can create many containers from one image.

______________________________________________________________________

# ECR Architecture

```
Developer

↓

Docker Build

↓

Docker Image

↓

ECR Repository

↓

ECS

↓

Running Container
```

______________________________________________________________________

# Repository

Repositories organize images.

Examples

```
backend-api

frontend

payment-service

notification-service
```

Each repository stores multiple image versions.

______________________________________________________________________

# Image Tags

Tags identify different image versions.

Example

```
backend-api

↓

v1.0

↓

v1.1

↓

v2.0

↓

latest
```

Tags are human-friendly labels.

______________________________________________________________________

# What is "latest"?

Many developers use

```
latest
```

This is only a **tag**, not a special version.

Example

```
backend-api:latest
```

Tomorrow,

"latest" may point to a different image.

For production deployments,

prefer immutable version tags.

______________________________________________________________________

# Image Digest

Every image also has a unique digest.

Example

```
sha256:98ab3....
```

Unlike tags,

digests never change.

Production deployments often pin images by digest for maximum reproducibility.

______________________________________________________________________

# Private Repository

Only authorized users can access.

Example

```
Company Backend

↓

Private ECR
```

Most production applications use private repositories.

______________________________________________________________________

# Public Repository

Anyone on the internet can pull images.

Useful for:

- Open-source software
- Public base images
- Tutorials

______________________________________________________________________

# Private vs Public Repository

| Feature | Private | Public |
|----------|----------|---------|
| Login Required | Usually Yes | Often No (for pulls) |
| Production Applications | ✅ | ❌ |
| Open Source | ❌ | ✅ |

______________________________________________________________________

# Authentication

Before Docker can push or pull images,

it must authenticate with ECR.

Flow

```
AWS CLI

↓

Authentication Token

↓

Docker Login

↓

ECR
```

Authentication tokens expire and should be refreshed as needed.

______________________________________________________________________

# AWS Console

Using the Console you can:

- Create Repositories
- Delete Repositories
- View Images
- View Image Tags
- Enable Image Scanning
- Configure Lifecycle Policies
- View Push/Pull History

______________________________________________________________________

# Docker Build

Example

```bash
docker build -t backend-api .
```

Creates

```
backend-api
```

Docker image.

______________________________________________________________________

# Create Repository (AWS CLI)

```bash
aws ecr create-repository \
    --repository-name backend-api
```

______________________________________________________________________

# Authenticate Docker

```bash
aws ecr get-login-password \
| docker login \
--username AWS \
--password-stdin \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
```

This logs Docker into your ECR registry.

______________________________________________________________________

# Tag Image

```bash
docker tag backend-api:latest \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/backend-api:1.0
```

______________________________________________________________________

# Push Image

```bash
docker push \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/backend-api:1.0
```

Image is uploaded to ECR.

______________________________________________________________________

# Pull Image

```bash
docker pull \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/backend-api:1.0
```

______________________________________________________________________

# List Repositories

```bash
aws ecr describe-repositories
```

______________________________________________________________________

# List Images

```bash
aws ecr list-images \
    --repository-name backend-api
```

______________________________________________________________________

# Delete Image

```bash
aws ecr batch-delete-image \
    --repository-name backend-api \
    --image-ids imageTag=1.0
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

ecr = boto3.client("ecr")
```

______________________________________________________________________

## List Repositories

```python
response = ecr.describe_repositories()

for repo in response["repositories"]:
    print(repo["repositoryName"])
```

______________________________________________________________________

## Create Repository

```python
ecr.create_repository(
    repositoryName="backend-api"
)
```

______________________________________________________________________

## List Images

```python
response = ecr.list_images(
    repositoryName="backend-api"
)

print(response["imageIds"])
```

______________________________________________________________________

# Common ECR Operations

Daily operations include:

- Build Images
- Push Images
- Pull Images
- Delete Old Images
- View Image Tags
- Enable Image Scanning
- Review Repository Policies

______________________________________________________________________

# Typical CI/CD Flow

```
Developer

↓

Git Push

↓

GitHub Actions

↓

Docker Build

↓

Push Image

↓

ECR

↓

Deploy ECS
```

ECR is commonly used as the artifact repository for container deployments.

______________________________________________________________________

# Common Mistakes

❌ Deploying production using the `latest` tag

❌ Forgetting to authenticate Docker before pushing

❌ Storing large unused images indefinitely

❌ Giving broad repository permissions

❌ Keeping secrets inside Docker images

❌ Rebuilding identical images unnecessarily

______________________________________________________________________

# Production Best Practices

- Use immutable version tags (for example, `v1.2.3`).
- Prefer image digests for production deployments.
- Enable image scanning.
- Remove unused images regularly.
- Use least-privilege IAM permissions.
- Keep repositories private unless public access is required.
- Store secrets outside container images.
- Automate image publishing through CI/CD.
- Use multi-stage Docker builds to reduce image size.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should production deployments avoid using the `latest` image tag?**

### Answer

The `latest` tag is mutable and can point to different image versions over time.

Using immutable version tags or image digests provides:

1. Reproducible deployments.
1. Easier rollbacks.
1. Better debugging because the deployed image is precisely identified.
1. Safer deployments across multiple environments.
1. Consistent behavior in automated CI/CD pipelines.

Many production systems deploy using image digests instead of tags to guarantee the exact image version.

______________________________________________________________________

# Summary

In this chapter you learned:

- What Amazon ECR is
- Container Registries
- Docker Images
- Repositories
- Image Tags
- Image Digests
- Public vs Private Repositories
- Authentication
- AWS Console
- AWS CLI
- Docker CLI
- boto3 SDK
- CI/CD integration
- Production best practices

Amazon ECR is the central storage location for container images used by ECS, EKS, Lambda container images, and many
modern deployment pipelines.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Amazon ECR?
1. Why was ECR created?
1. What is a Container Registry?
1. What is a Docker Image?
1. What is the difference between an Image and a Container?

______________________________________________________________________

## Repositories

6. What is an ECR Repository?
1. What are Image Tags?
1. What is an Image Digest?
1. Why are Image Digests preferred in production?
1. Why is the `latest` tag discouraged?

______________________________________________________________________

## Authentication

11. Why must Docker authenticate before pushing to ECR?
01. How does `aws ecr get-login-password` work?
01. What happens when the authentication token expires?

______________________________________________________________________

## CLI & SDK

14. Which CLI command creates an ECR repository?
01. Which Docker command uploads an image?
01. Which boto3 method creates a repository?
01. Which CLI command lists images in a repository?

______________________________________________________________________

## Architecture

18. Explain how ECR fits into a CI/CD pipeline.
01. Why is ECR commonly paired with ECS?
01. Why should secrets never be stored inside Docker images?

______________________________________________________________________

## Scenario-Based

21. Your deployment unexpectedly starts running a newer application version without any code changes. The deployment uses the `latest` tag. What likely happened?
01. Your ECR repository contains thousands of old images that are no longer deployed. What operational problems could this create?
01. Your CI/CD pipeline fails while pushing images to ECR with an authentication error. What would you investigate first?
01. Your security team requires every deployed container image to be traceable to a specific build. Would you deploy by tag or digest? Why?
01. Your organization is migrating from Docker Hub to Amazon ECR. What advantages would ECR provide for workloads already running in AWS?

______________________________________________________________________

## Next

[ECR Advanced](12_ecr_advanced.md)
