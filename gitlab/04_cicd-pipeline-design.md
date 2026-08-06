# CI/CD Pipeline Design

> File: `04_cicd-pipeline-design.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Design production-ready CI/CD pipelines
- Build an end-to-end pipeline for a Python backend
- Understand every stage in a CI pipeline
- Separate CI and CD responsibilities
- Design pipelines for microservices
- Design pipelines for monorepos
- Explain pipeline architecture in interviews
- Understand release strategies

______________________________________________________________________

# Table of Contents

1. What is a CI/CD Pipeline?
1. Pipeline Architecture
1. Pipeline Stages
1. Python Backend Pipeline
1. Docker Integration
1. Security Scanning
1. Branch Strategies
1. Pull Request Pipelines
1. Release Pipelines
1. Deployment Pipelines
1. Monorepo Pipelines
1. Microservice Pipelines
1. Pipeline Optimization
1. Real Company Example
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# What is a CI/CD Pipeline?

A CI/CD pipeline is a sequence of automated stages that transform source code into a deployable application.

```
Developer

    │

git push

    │

    ▼

GitHub Actions

    │

    ▼

Build

    │

    ▼

Test

    │

    ▼

Package

    │

    ▼

Deploy

    │

    ▼

Production
```

Instead of manually executing every step, GitHub Actions orchestrates the entire process.

______________________________________________________________________

# Typical Backend Pipeline

A production backend pipeline usually looks like this.

```
Checkout Code

        │

        ▼

Install Dependencies

        │

        ▼

Lint

        │

        ▼

Unit Tests

        │

        ▼

Integration Tests

        │

        ▼

Security Scan

        │

        ▼

Build Docker Image

        │

        ▼

Push Docker Image

        │

        ▼

Deploy

        │

        ▼

Smoke Test

        │

        ▼

Notify Team
```

Every stage has one responsibility.

______________________________________________________________________

# Why Multiple Stages?

Imagine deploying immediately after building.

```
Build

↓

Deploy
```

What if tests fail?

What if formatting is broken?

What if security vulnerabilities exist?

A staged pipeline prevents bad code from reaching production.

______________________________________________________________________

# Pipeline Stage 1 — Checkout

Every workflow begins by downloading the repository.

```
Repository

↓

Runner

↓

Checkout
```

Workflow

```yaml
- uses: actions/checkout@v4
```

Without checkout, the runner has no project files.

______________________________________________________________________

# Stage 2 — Setup Runtime

For Python projects:

```yaml
- uses: actions/setup-python@v5

  with:
    python-version: "3.12"
```

For Node.js:

```yaml
actions/setup-node
```

For Java:

```yaml
actions/setup-java
```

The runtime depends on the project.

______________________________________________________________________

# Stage 3 — Install Dependencies

Python

```bash
pip install -r requirements.txt
```

or

```bash
poetry install
```

or

```bash
uv sync
```

Always install dependencies before testing.

______________________________________________________________________

# Stage 4 — Linting

Linting checks code quality.

Popular Python tools

```
Ruff

Flake8

Black

isort
```

Example

```bash
ruff check .
```

If linting fails,

pipeline stops.

______________________________________________________________________

# Why Lint Before Tests?

Imagine

```
Formatting Errors

↓

Unit Tests
```

The project already violates coding standards.

Running tests wastes compute time.

Linting is fast.

Run it first.

______________________________________________________________________

# Stage 5 — Unit Tests

Run automated tests.

Example

```bash
pytest
```

A failing test should fail the pipeline.

```
Tests Failed

↓

Deployment Blocked
```

______________________________________________________________________

# Stage 6 — Integration Tests

Integration tests verify interaction between components.

Example

```
API

↓

Database

↓

Redis

↓

Kafka
```

Example

```bash
pytest tests/integration
```

Usually slower than unit tests.

______________________________________________________________________

# Stage 7 — Coverage

Measure tested code.

Example

```bash
pytest --cov
```

Many companies require

```
80%

90%

95%
```

minimum coverage.

Coverage itself is not quality, but it highlights untested code.

______________________________________________________________________

# Stage 8 — Security Scanning

Common Python tools

```
Bandit

Safety

pip-audit
```

Container scanning

```
Trivy
```

Security checks often include:

- Vulnerable dependencies
- Hardcoded secrets
- Unsafe code
- CVEs in Docker images

______________________________________________________________________

# Stage 9 — Build Docker Image

Instead of deploying source code,

build a Docker image.

```
Application

↓

Docker Build

↓

Image
```

Example

```bash
docker build -t backend:v1 .
```

______________________________________________________________________

# Stage 10 — Push Image

After building,

push to a registry.

Examples

```
Docker Hub

Amazon ECR

GitHub Container Registry

Azure Container Registry
```

```
Docker Image

↓

Registry

↓

Deployment
```

______________________________________________________________________

# Stage 11 — Deployment

Deployment depends on infrastructure.

Possible targets

```
EC2

ECS

Kubernetes

Docker Compose

Azure

GCP

Heroku
```

Deployment should happen only after all previous stages succeed.

______________________________________________________________________

# Stage 12 — Smoke Test

A smoke test validates the deployed application.

Example

```
GET /health
```

Expected

```
200 OK
```

If smoke tests fail,

rollback.

______________________________________________________________________

# Stage 13 — Notifications

Notify developers.

Examples

```
Slack

Microsoft Teams

Email
```

Typical notification

```
Deployment Successful

Version v2.1

Production

Duration 4m 12s
```

______________________________________________________________________

# CI vs CD

Many companies separate them.

```
CI Workflow

↓

Lint

↓

Test

↓

Build
```

Another workflow

```
CD Workflow

↓

Deploy
```

Advantages

- Easier maintenance
- Better permissions
- Separate approvals
- Independent execution

______________________________________________________________________

# Branch Strategies

## Feature Branches

```
main

│

├── feature/login

├── feature/orders

└── feature/payment
```

Developers work independently.

______________________________________________________________________

## GitFlow

```
main

↓

develop

↓

feature

↓

release

↓

hotfix
```

Good for structured releases.

______________________________________________________________________

## Trunk-Based Development

```
main
```

Small frequent merges.

Common in large companies.

______________________________________________________________________

# Pull Request Pipeline

When a PR is opened,

run

```
Checkout

↓

Lint

↓

Unit Tests

↓

Security Scan
```

Do **not**

deploy.

Purpose

```
Validate Code

↓

Approve Merge
```

______________________________________________________________________

# Merge Pipeline

After merging into `main`

```
Checkout

↓

Build

↓

Push Image

↓

Deploy Staging
```

Production deployment often requires approval.

______________________________________________________________________

# Release Pipeline

Tag

```
v1.2.0
```

Triggers

```
Build

↓

Package

↓

Release Notes

↓

Publish

↓

Deploy
```

______________________________________________________________________

# Deployment Environments

Typical environments

```
Development

↓

Testing

↓

Staging

↓

Production
```

Each environment has different:

- Database
- Secrets
- Configuration
- Permissions

______________________________________________________________________

# Monorepo Pipeline

Monorepo example

```
services/

    auth/

    orders/

    payment/

shared/

frontend/
```

Instead of rebuilding everything,

build only changed services.

```
Changed Files

↓

Affected Services

↓

Build Only Those
```

Reduces execution time.

______________________________________________________________________

# Microservice Pipeline

Each service has its own pipeline.

```
Auth Service

↓

CI

↓

Docker

↓

Deploy
```

```
Order Service

↓

CI

↓

Docker

↓

Deploy
```

Independent deployments reduce risk.

______________________________________________________________________

# Pipeline Optimization

## Parallel Jobs

Instead of

```
Lint

↓

Tests

↓

Security
```

Run

```
        Lint

      /

Start

      \

        Tests

      \

        Security
```

Much faster.

______________________________________________________________________

## Dependency Cache

Don't reinstall packages every run.

```
Restore Cache

↓

Install Missing

↓

Run Tests
```

______________________________________________________________________

## Docker Layer Cache

Only rebuild changed layers.

Can reduce Docker build time dramatically.

______________________________________________________________________

## Fail Fast

Stop pipeline immediately after critical failures.

Don't continue running expensive jobs unnecessarily.

______________________________________________________________________

# Real Company Example

Imagine a FastAPI service.

Pipeline

```
Checkout

↓

Setup Python

↓

Install Dependencies

↓

Ruff

↓

Pytest

↓

Coverage

↓

Bandit

↓

Docker Build

↓

Push ECR

↓

Deploy ECS

↓

Smoke Test

↓

Slack Notification
```

This is a common production pipeline for Python backend services.

______________________________________________________________________

# Best Practices

- Separate CI and CD workflows.
- Run linting before tests.
- Keep jobs focused on one responsibility.
- Fail fast on critical errors.
- Build immutable Docker images.
- Scan dependencies regularly.
- Tag releases consistently.
- Deploy only from trusted branches.
- Require approvals for production deployments.
- Use environment-specific secrets.

______________________________________________________________________

# Common Mistakes

## Deploying Untested Code

Never skip testing.

______________________________________________________________________

## Running Everything Sequentially

Parallelize independent stages.

______________________________________________________________________

## One Huge Workflow

Split CI and CD.

______________________________________________________________________

## No Rollback Plan

Always have a rollback strategy.

______________________________________________________________________

## Deploying from Feature Branches

Only deploy from controlled branches.

______________________________________________________________________

## Hardcoding Environment Values

Use GitHub Variables and Secrets.

______________________________________________________________________

# Interview Deep Dive

## Q1. Describe a typical CI/CD pipeline.

### Answer

A typical pipeline starts by checking out the source code, setting up the runtime, installing dependencies, running
linting and automated tests, performing security scans, building a Docker image, pushing it to a container registry,
deploying it to the target environment, running smoke tests, and finally notifying the team of the deployment result.

______________________________________________________________________

## Q2. Why should linting run before tests?

### Answer

Linting is significantly faster than running automated tests. Detecting formatting or static analysis issues early
prevents unnecessary execution of slower stages, reducing pipeline time and compute cost.

______________________________________________________________________

## Q3. Why separate CI and CD?

### Answer

Separating CI and CD improves security, simplifies maintenance, enables different permissions and approval processes,
and allows deployments to be triggered independently of code validation.

______________________________________________________________________

## Q4. What is a smoke test?

### Answer

A smoke test is a lightweight validation executed immediately after deployment to verify that the application has
started successfully and that critical functionality, such as a health endpoint, is working before considering the
deployment successful.

______________________________________________________________________

## Q5. Why build Docker images instead of deploying source code?

### Answer

Docker images provide a consistent and immutable deployment artifact. The same image tested during CI is deployed to
staging and production, reducing environment-related issues and ensuring repeatable deployments.

______________________________________________________________________

## Q6. How would you optimize a slow CI pipeline?

### Answer

I would parallelize independent jobs, cache dependencies, enable Docker layer caching, fail fast on critical errors,
build only affected services in monorepos, and avoid redundant workflow execution.

______________________________________________________________________

## Q7. What is the difference between unit tests and integration tests?

### Answer

Unit tests validate individual components in isolation, while integration tests verify that multiple components, such as
APIs, databases, message queues, or external services, work together correctly.

______________________________________________________________________

## Q8. Why are production deployments often protected by approvals?

### Answer

Production deployments affect end users and business operations. Requiring approvals provides an additional verification
step, reduces accidental releases, and helps ensure that deployment policies are followed.

______________________________________________________________________

# Summary

In this chapter you learned:

- CI/CD pipeline architecture
- Pipeline stages
- Python backend pipeline design
- Linting
- Unit testing
- Integration testing
- Coverage
- Security scanning
- Docker build and registry
- Deployments
- Smoke tests
- Notifications
- Branch strategies
- Pull request pipelines
- Release pipelines
- Monorepo pipelines
- Microservice pipelines
- Pipeline optimization
- Production best practices

______________________________________________________________________

# Next

[Real World Pipelines](05_real-world-pipelines.md)
