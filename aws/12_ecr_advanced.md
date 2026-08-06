# ECR Advanced

> **Course:** AWS for Backend Engineers
>
> **Module:** 6
>
> **File:** `12_ecr_advanced.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Image Scanning
- Enhanced Scanning
- Repository Policies
- Lifecycle Policies
- Cross-Region Replication
- Cross-Account Access
- Image Signing Concepts
- Image Digests
- Multi-Architecture Images
- Docker Manifest Lists
- Pull Through Cache
- Encryption
- Authentication Flow
- CI/CD Integration
- Production Deployment Strategies
- Cost Optimization
- Security Best Practices

______________________________________________________________________

# Why Advanced ECR?

Storing Docker images is only the beginning.

Production systems require answers to questions like:

- Is my image vulnerable?
- Can another AWS account pull this image?
- How do I delete old images automatically?
- How do I replicate images across Regions?
- How do I deploy exactly the same image everywhere?
- How do I secure my container registry?

Advanced ECR addresses these concerns.

______________________________________________________________________

# Image Scanning

Container images may contain vulnerable packages.

Example

```
Ubuntu Image

↓

OpenSSL

↓

Known Vulnerability
```

If deployed,

the application may be exposed.

ECR can scan images for known software vulnerabilities.

______________________________________________________________________

# Basic vs Enhanced Scanning

## Basic Scanning

- Repository-level scanning
- Identifies known package vulnerabilities
- Suitable for many workloads

______________________________________________________________________

## Enhanced Scanning

Powered by **Amazon Inspector**.

Provides:

- Continuous scanning
- Updated vulnerability findings
- More detailed security information

Recommended for production environments.

______________________________________________________________________

# Example

```
Docker Image

↓

Push to ECR

↓

Scan

↓

Critical Vulnerability Found

↓

Deployment Blocked
```

This prevents vulnerable images from reaching production.

______________________________________________________________________

# Repository Policies

Repository Policies control **who can access an ECR repository**.

Examples

Allow

```
Pull Images
```

Deny

```
Delete Repository
```

They are similar in concept to S3 Bucket Policies.

______________________________________________________________________

# Example Architecture

```
Repository

↓

Repository Policy

↓

IAM User

↓

IAM Role

↓

Access Granted
```

______________________________________________________________________

# IAM Policy vs Repository Policy

| Feature | IAM Policy | Repository Policy |
|----------|------------|-------------------|
| Attached To | User / Group / Role | Repository |
| Controls | Identity Permissions | Repository Access |
| Cross-Account Access | Yes | Commonly Used |

Both may participate in the final permission decision.

______________________________________________________________________

# Lifecycle Policies

Repositories accumulate images over time.

Example

```
v1

v2

v3

...

v500
```

Old images increase storage costs.

Lifecycle Policies automatically remove unused images.

______________________________________________________________________

# Example Lifecycle Policy

```
Keep

Latest 20 Images

↓

Delete Older Images
```

Or

```
Delete Images

Older Than

180 Days
```

Cleanup becomes automatic.

______________________________________________________________________

# Benefits

- Lower storage costs
- Cleaner repositories
- Reduced operational effort
- Better compliance

______________________________________________________________________

# Cross-Region Replication

Large companies often deploy applications in multiple AWS Regions.

Without replication

```
Mumbai

↓

Push Image
```

Need to manually push again

```
Frankfurt

↓

Push Image
```

Instead

```
Mumbai

↓

Automatic Replication

↓

Frankfurt
```

______________________________________________________________________

# Why Replicate Images?

Benefits

- Disaster Recovery
- Faster regional deployments
- Lower deployment latency
- Multi-region applications

______________________________________________________________________

# Cross-Account Access

Suppose

```
Shared Platform Account

↓

Stores Images
```

Development and Production accounts both need access.

Architecture

```
Shared ECR

↓

Repository Policy

↓

Development Account

↓

Production Account
```

No duplicate repositories required.

______________________________________________________________________

# Image Digest

Tags can change.

Example

```
backend-api:latest
```

may point to a different image tomorrow.

Digest

```
sha256:ab123...
```

never changes.

Production deployments should preferably use digests.

______________________________________________________________________

# Image Signing (Concept)

Organizations often want proof that an image was produced by an approved build pipeline.

Image signing provides:

- Authenticity
- Integrity
- Supply-chain security

The exact implementation depends on the tooling used.

______________________________________________________________________

# Multi-Architecture Images

Modern environments may include:

```
AMD64

ARM64
```

Instead of maintaining separate image names,

Docker supports **Multi-Architecture Images**.

One image reference

↓

Multiple architectures

Docker automatically downloads the correct image.

______________________________________________________________________

# Manifest Lists

A Manifest List (also called a multi-platform manifest) points to multiple architecture-specific images.

Example

```
backend-api:1.0

↓

AMD64 Image

↓

ARM64 Image
```

Clients receive the correct image automatically.

______________________________________________________________________

# Pull Through Cache

Organizations often pull base images repeatedly.

Example

```
docker pull python:3.12
```

Instead,

ECR can cache supported upstream images.

Benefits

- Faster pulls
- Reduced dependence on external registries
- Improved reliability

______________________________________________________________________

# Encryption

Images stored in ECR are encrypted at rest.

Options include:

- AWS-managed encryption
- AWS KMS customer-managed keys

Choose based on compliance requirements.

______________________________________________________________________

# Authentication Flow

```
AWS CLI

↓

Authentication Token

↓

Docker Login

↓

Push

↓

ECR
```

Tokens are temporary.

CI/CD systems usually authenticate automatically.

______________________________________________________________________

# CI/CD Integration

Typical workflow

```
Git Push

↓

GitHub Actions

↓

Run Tests

↓

Docker Build

↓

Image Scan

↓

Push ECR

↓

Deploy ECS
```

Only validated images reach production.

______________________________________________________________________

# Blue-Green Deployment

```
Current

↓

Image v1.0
```

Deploy

```
Image v2.0

↓

New Environment

↓

Switch Traffic
```

Rollback is simple.

______________________________________________________________________

# Rolling Deployment

```
10 Tasks

↓

Deploy 2

↓

Healthy

↓

Deploy Next 2
```

Image versions are updated gradually.

______________________________________________________________________

# Immutable Deployment

Production environments should avoid changing an existing image.

Instead

```
v1.0

↓

v1.1

↓

v1.2
```

Every release produces a new image.

Never rebuild an existing production tag.

______________________________________________________________________

# Cost Optimization

- Remove unused images.
- Use Lifecycle Policies.
- Compress images with multi-stage builds.
- Avoid duplicate repositories.
- Replicate only where necessary.
- Delete abandoned development images.

______________________________________________________________________

# Security Best Practices

- Enable Enhanced Scanning.
- Use immutable image tags.
- Deploy by image digest.
- Restrict repository permissions.
- Enable encryption.
- Store secrets outside images.
- Regularly patch base images.
- Rebuild images when vulnerabilities are fixed.
- Review repository access periodically.

______________________________________________________________________

# Production Architecture

```
Developer

↓

Git Push

↓

GitHub Actions

↓

Docker Build

↓

Enhanced Scan

↓

Push

↓

Amazon ECR

↓

Cross-Region Replication

↓

ECS Deployment

↓

Production
```

______________________________________________________________________

# Common Mistakes

❌ Using mutable tags in production

❌ Ignoring vulnerability reports

❌ Never deleting unused images

❌ Granting overly broad repository permissions

❌ Storing credentials inside container images

❌ Using outdated base images

❌ Skipping image scanning in CI/CD

______________________________________________________________________

# Interview Deep Dive

### Question

**How would you design a secure container image pipeline using Amazon ECR?**

### Answer

A production-ready pipeline would include:

1. Developers commit code to the source repository.
1. The CI/CD pipeline builds the Docker image.
1. Automated tests run successfully.
1. The image is scanned for vulnerabilities before deployment.
1. The image is tagged with an immutable version and pushed to ECR.
1. Lifecycle Policies remove outdated images automatically.
1. ECS deployments reference the image by digest.
1. Repository access is restricted using IAM and Repository Policies.
1. Images are replicated to additional Regions if required for disaster recovery or global deployments.

______________________________________________________________________

# Summary

In this chapter you learned:

- Image Scanning
- Enhanced Scanning
- Repository Policies
- Lifecycle Policies
- Cross-Region Replication
- Cross-Account Access
- Image Digests
- Image Signing concepts
- Multi-Architecture Images
- Manifest Lists
- Pull Through Cache
- Encryption
- CI/CD Integration
- Deployment strategies
- Production security practices

These features transform Amazon ECR from a simple image registry into a secure enterprise container artifact repository.

______________________________________________________________________

# Practice Questions

## Security

1. What is ECR Image Scanning?
1. What is the difference between Basic and Enhanced Scanning?
1. Why should container images be scanned before deployment?
1. Why are immutable tags preferred?

______________________________________________________________________

## Repository Management

5. What is a Repository Policy?
1. How does a Repository Policy differ from an IAM Policy?
1. What is a Lifecycle Policy?
1. How do Lifecycle Policies reduce costs?

______________________________________________________________________

## Replication

9. What is Cross-Region Replication?
1. Why would a company replicate container images?
1. How can multiple AWS accounts securely share one ECR repository?

______________________________________________________________________

## Images

12. What is an Image Digest?
01. Why are Image Digests preferred over tags?
01. What are Multi-Architecture Images?
01. What is a Manifest List?

______________________________________________________________________

## CI/CD

16. Explain a production container image pipeline.
01. Why should image scanning occur before deployment?
01. Why should images never contain application secrets?

______________________________________________________________________

## Architecture

19. What is Pull Through Cache?
01. Why is encryption important for container images?
01. What is an immutable deployment strategy?

______________________________________________________________________

## Scenario-Based

22. Your production deployment unexpectedly starts using a different container image even though the deployment configuration hasn't changed. The deployment references the `latest` tag. What is the likely cause?
01. Your security team discovers a critical vulnerability in a commonly used base image. What actions should your engineering team take?
01. Your organization operates in India and Europe and wants faster deployments in both Regions. Which ECR feature would you recommend?
01. Your ECR storage costs continue increasing because development images are never removed. How would you solve this?
01. Your CI/CD pipeline should prevent vulnerable images from reaching production. Which ECR capabilities would you integrate into the deployment pipeline?

______________________________________________________________________

## Next

[ECS Concepts](13_ecs_concepts.md)
