# Real World Pipelines

> File: `05_real-world-pipelines.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Design CI/CD pipelines used in real companies
- Build pipelines for FastAPI and Flask applications
- Design pipelines for microservices and monorepos
- Handle database migrations safely
- Implement deployment strategies like Blue-Green and Canary
- Understand rollback strategies
- Design production release pipelines
- Explain real-world CI/CD architectures in interviews

______________________________________________________________________

# Table of Contents

1. Real World CI/CD
1. FastAPI Pipeline
1. Flask Pipeline
1. Microservice Pipelines
1. Monorepo Pipelines
1. Database Migration Strategy
1. Blue-Green Deployment
1. Canary Deployment
1. Rolling Deployment
1. Feature Flags
1. Rollback Strategy
1. Versioning
1. Release Pipelines
1. Notifications
1. Production Pipeline Example
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# Real World CI/CD

Interview questions usually don't ask:

> "How do you write YAML?"

Instead they ask:

> "How would you design CI/CD for our backend services?"

They want to evaluate your engineering thinking.

A production pipeline is designed around:

- Reliability
- Repeatability
- Security
- Rollback capability
- Fast feedback
- Zero downtime

______________________________________________________________________

# Example Company Architecture

Imagine an e-commerce application.

```
                Users

                  │

                  ▼

            Load Balancer

      ┌───────────┼────────────┐

      ▼           ▼            ▼

 Auth Service  Order Service  Payment Service

      │           │            │

      └──────┬────┴────┬───────┘

             ▼

          PostgreSQL

             ▼

            Redis

             ▼

            Kafka
```

Each service has its own repository and CI/CD pipeline.

______________________________________________________________________

# FastAPI Pipeline

Typical production pipeline

```
Checkout

↓

Setup Python

↓

Install Dependencies

↓

Lint

↓

Run Unit Tests

↓

Run Integration Tests

↓

Security Scan

↓

Build Docker Image

↓

Push to ECR

↓

Deploy

↓

Smoke Test

↓

Notify Team
```

______________________________________________________________________

## GitHub Actions Flow

```
Push

↓

CI Workflow

↓

Docker Image

↓

Container Registry

↓

Deployment Workflow

↓

Production
```

Notice that CI and CD are separated.

______________________________________________________________________

# Flask Pipeline

The process is nearly identical.

```
Checkout

↓

Install

↓

Lint

↓

Pytest

↓

Build Docker

↓

Push Registry

↓

Deploy
```

Frameworks change.

Pipeline philosophy doesn't.

______________________________________________________________________

# Pipeline per Microservice

Suppose you have

```
auth-service

order-service

payment-service

inventory-service
```

Each service should have

- Independent repository
- Independent Docker image
- Independent deployment
- Independent rollback

Example

```
Auth Service

↓

CI

↓

Deploy
```

```
Order Service

↓

CI

↓

Deploy
```

Updating the authentication service should not redeploy every other service.

______________________________________________________________________

# Shared Libraries

Suppose multiple services use

```
company-utils
```

Pipeline

```
Build Library

↓

Publish Internal Package

↓

Services Upgrade Version
```

This keeps common code centralized.

______________________________________________________________________

# Monorepo Pipeline

Some companies use one repository.

```
services/

    auth/

    payment/

    order/

shared/

frontend/
```

Challenge:

One file changes.

Should every service rebuild?

No.

______________________________________________________________________

## Path-Based Builds

Suppose

```
services/auth/

changed
```

Only execute

```
Auth Pipeline
```

instead of

```
Auth

Order

Payment

Inventory
```

GitHub Actions supports path filters to trigger workflows only when relevant files change.

Benefits:

- Faster builds
- Lower cost
- Smaller deployments

______________________________________________________________________

# Database Migrations

One of the biggest production risks.

Suppose deployment order is

```
Deploy App

↓

Run Migration
```

Application crashes because the new code expects a column that doesn't exist yet.

______________________________________________________________________

## Correct Order

```
Migration

↓

Deploy

↓

Smoke Test
```

Sometimes even this isn't enough.

______________________________________________________________________

## Backward-Compatible Migrations

Good deployment

```
Add New Column

↓

Deploy New Code

↓

Remove Old Column Later
```

Bad deployment

```
Remove Column

↓

Deploy

↓

Old Version Crashes
```

Always design migrations to support both old and new application versions during deployment.

______________________________________________________________________

# Alembic Example

For FastAPI and SQLAlchemy

```
alembic upgrade head
```

Typical deployment

```
Build Image

↓

Deploy Migration Job

↓

Deploy API
```

______________________________________________________________________

# Flyway

Common in Java ecosystems.

Pipeline

```
Flyway Migration

↓

Application Deployment
```

______________________________________________________________________

# Liquibase

Another migration tool.

Common in enterprise applications.

The principle remains the same.

______________________________________________________________________

# Blue-Green Deployment

Goal:

Zero downtime.

Two identical environments exist.

```
Blue

Green
```

Current production

```
Blue
```

Deploy new version to

```
Green
```

Test it.

If everything succeeds

```
Traffic

↓

Green
```

Old environment remains available.

If deployment fails

```
Traffic

↓

Blue
```

Rollback is almost immediate.

______________________________________________________________________

## Visualization

```
Users

↓

Load Balancer

↓

Blue (Current)

Green (New)

↓

Switch

↓

Green
```

Advantages

- Near-zero downtime
- Instant rollback
- Safe releases

Disadvantages

- Higher infrastructure cost
- Duplicate environments

______________________________________________________________________

# Canary Deployment

Instead of switching everyone,

deploy gradually.

```
Version 1

95%

Version 2

5%
```

Monitor.

If healthy

```
50%

↓

100%
```

If errors increase

```
Rollback
```

______________________________________________________________________

## Example

```
1000 Users

↓

50 Users

↓

New Version

↓

Monitor
```

Only a small percentage experiences the new release initially.

______________________________________________________________________

# Rolling Deployment

Common in Kubernetes.

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

Application remains available throughout.

______________________________________________________________________

# Feature Flags

Sometimes deployment and feature release should be separate.

Instead of

```
Deploy

↓

Feature Enabled
```

Use

```
Deploy

↓

Feature Disabled

↓

Enable Later
```

Benefits

- Safer deployments
- Easy rollback
- Gradual rollout
- A/B testing

Popular tools

- LaunchDarkly
- Unleash
- ConfigCat

______________________________________________________________________

# Rollback Strategy

Every deployment should answer:

> "What if this fails?"

Possible rollback methods

______________________________________________________________________

## Redeploy Previous Image

```
v12

↓

Problem

↓

Deploy v11
```

Fast and simple.

______________________________________________________________________

## Switch Blue-Green

```
Green Broken

↓

Blue Active
```

Almost instant.

______________________________________________________________________

## Kubernetes Rollback

```
kubectl rollout undo deployment backend
```

Very common interview discussion.

______________________________________________________________________

## Database Rollback

Be careful.

Rolling back schema changes is often harder than rolling back application code.

Prefer forward-compatible migrations over destructive schema changes.

______________________________________________________________________

# Versioning

Use Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Example

```
2.4.1
```

Meaning

```
Major Breaking Changes

Minor Features

Patch Bug Fixes
```

Git tags commonly match versions.

```
v2.4.1
```

______________________________________________________________________

# Release Pipeline

Typical release process

```
Merge Main

↓

Run CI

↓

Build Docker Image

↓

Push Registry

↓

Create Git Tag

↓

Generate Release Notes

↓

Deploy Staging

↓

Approval

↓

Deploy Production

↓

Smoke Test

↓

Notify Team
```

______________________________________________________________________

# Notifications

Notify after deployment.

Examples

Slack

```
Deployment Successful

Version: v2.4.1

Environment: Production

Duration: 5m 21s
```

Teams

Email

PagerDuty (for failures)

______________________________________________________________________

# Production Pipeline Example

Imagine a FastAPI microservice deployed to AWS ECS.

```
Push Code

↓

Lint

↓

Unit Tests

↓

Integration Tests

↓

Bandit

↓

Docker Build

↓

Push Amazon ECR

↓

Deploy Amazon ECS

↓

Run Alembic Migration

↓

Health Check

↓

Smoke Test

↓

Slack Notification
```

This is very close to what many production backend teams use.

______________________________________________________________________

# Best Practices

- Keep CI and CD separate.
- Deploy immutable Docker images.
- Automate rollback procedures.
- Make database migrations backward compatible.
- Deploy one service independently of others.
- Use semantic versioning.
- Introduce feature flags for risky features.
- Validate deployments with smoke tests.
- Monitor applications immediately after release.
- Tag every production release.

______________________________________________________________________

# Common Mistakes

## Deploying All Services Together

Independent services should have independent deployments whenever possible.

______________________________________________________________________

## Destructive Database Changes

Dropping columns before application updates can cause outages.

______________________________________________________________________

## No Rollback Plan

Every deployment should have a documented rollback strategy.

______________________________________________________________________

## Large Feature Releases

Smaller, more frequent deployments reduce risk.

______________________________________________________________________

## No Monitoring After Deployment

A successful deployment isn't complete until the application is verified.

______________________________________________________________________

# Interview Deep Dive

## Q1. How would you design a CI/CD pipeline for a FastAPI application?

### Answer

I would separate CI and CD. The CI pipeline would check out the code, install dependencies, run Ruff, execute unit and
integration tests, perform security scans, build a Docker image, and push it to Amazon ECR. The CD pipeline would deploy
the image to the target environment, execute database migrations if required, run smoke tests, and notify the team after
successful deployment.

______________________________________________________________________

## Q2. Why should each microservice have its own pipeline?

### Answer

Independent pipelines allow services to be tested, deployed, and rolled back independently. This reduces deployment
risk, shortens release cycles, and prevents unrelated services from being affected by a single change.

______________________________________________________________________

## Q3. Explain Blue-Green Deployment.

### Answer

Blue-Green deployment maintains two identical environments. The current production environment serves traffic while the
new version is deployed to the inactive environment. After validation, traffic is switched to the new environment. If
problems occur, traffic can immediately be redirected to the previous environment.

______________________________________________________________________

## Q4. Explain Canary Deployment.

### Answer

Canary deployment gradually releases a new version to a small percentage of users while monitoring application health.
If no issues are detected, traffic is increased progressively until the new version serves all users. This limits the
impact of faulty releases.

______________________________________________________________________

## Q5. Why are backward-compatible database migrations important?

### Answer

During deployment, old and new application versions may run simultaneously. Backward-compatible migrations ensure that
both versions can operate safely until the rollout is complete, reducing downtime and preventing application failures.

______________________________________________________________________

## Q6. What is a feature flag?

### Answer

A feature flag is a configuration mechanism that allows features to be enabled or disabled independently of deployments.
It supports gradual rollouts, A/B testing, safer releases, and quick deactivation without requiring a new deployment.

______________________________________________________________________

## Q7. How would you roll back a failed deployment?

### Answer

The rollback approach depends on the platform. Common strategies include redeploying the previous Docker image,
switching traffic back to the previous environment in Blue-Green deployments, or using platform-specific rollback
mechanisms such as `kubectl rollout undo` in Kubernetes. Database rollbacks require additional care and are ideally
avoided through backward-compatible schema changes.

______________________________________________________________________

## Q8. How would you design CI/CD for a monorepo?

### Answer

I would detect changed paths and trigger builds only for affected services. Shared libraries would be rebuilt only when
necessary, and independent jobs would run in parallel. This reduces build time, lowers infrastructure costs, and keeps
deployments focused on impacted components.

______________________________________________________________________

# Summary

In this chapter you learned:

- Production CI/CD architecture
- FastAPI and Flask pipelines
- Microservice pipelines
- Monorepo pipelines
- Path-based builds
- Database migration strategies
- Blue-Green deployment
- Canary deployment
- Rolling deployment
- Feature flags
- Rollback strategies
- Semantic versioning
- Release pipelines
- Deployment notifications
- Real-world backend CI/CD practices

______________________________________________________________________

# Next

[Deployments AWS Docker Kubernetes](06_deployments-aws-docker-kubernetes.md)
