# Debugging Best Practices Security

> File: `07_debugging-best-practices-security.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Debug GitHub Actions workflows efficiently
- Read workflow logs like an experienced engineer
- Troubleshoot common CI/CD failures
- Secure GitHub Actions pipelines
- Optimize workflow performance
- Reduce CI/CD costs
- Follow production-ready best practices
- Answer scenario-based interview questions

______________________________________________________________________

# Table of Contents

1. Debugging Mindset
1. Reading Workflow Logs
1. Common Failures
1. Debugging Docker Builds
1. Debugging Deployments
1. Performance Optimization
1. Security Best Practices
1. Branch Protection
1. GitHub Token Permissions
1. Workflow Design Best Practices
1. Cost Optimization
1. Real Production Incidents
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# Debugging Mindset

One of the biggest mistakes developers make is randomly changing YAML hoping the workflow will pass.

Professional debugging follows a process.

```
Failure

↓

Read Logs

↓

Identify Failed Step

↓

Understand Root Cause

↓

Fix

↓

Re-run
```

Never guess.

Always investigate first.

______________________________________________________________________

# Reading Workflow Logs

GitHub logs are organized hierarchically.

```
Workflow

↓

Job

↓

Step

↓

Command Output
```

Example

```
Python CI

↓

Run Tests

↓

pytest

↓

FAILED test_login.py
```

The important information is usually near the bottom of the failed step.

______________________________________________________________________

# Debugging Example

Suppose your workflow fails.

```
Run Tests

❌ Failed
```

Expand the step.

```
==================================

FAILED

ModuleNotFoundError

==================================
```

Now you know

The project cannot import a module.

Instead of editing random YAML,

fix the dependency.

______________________________________________________________________

# Common Failure 1

## YAML Syntax Error

Example

```yaml
steps

- run: pytest
```

Missing colon.

Correct

```yaml
steps:

- run: pytest
```

______________________________________________________________________

# Common Failure 2

## Wrong Indentation

Bad

```yaml
jobs:

build:

steps:
```

Correct

```yaml
jobs:

  build:

    steps:
```

YAML is indentation-sensitive.

______________________________________________________________________

# Common Failure 3

## Missing Checkout

Workflow

```yaml
run: pytest
```

Failure

```
No such file

requirements.txt not found

Module not found
```

Cause

Repository was never downloaded.

Fix

```yaml
- uses: actions/checkout@v4
```

______________________________________________________________________

# Common Failure 4

## Wrong Python Version

```
SyntaxError

match statement
```

Cause

Running Python 3.9

Code requires Python 3.10+

Fix

```yaml
actions/setup-python
```

______________________________________________________________________

# Common Failure 5

## Dependency Installation Failed

```
pip install

↓

Package not found
```

Possible reasons

- Wrong package name
- Private repository
- Network issue
- Incorrect Python version

______________________________________________________________________

# Common Failure 6

## Tests Fail

```
pytest

↓

FAILED
```

Remember

This is not a CI problem.

It's an application problem.

Fix the tests.

______________________________________________________________________

# Common Failure 7

## Docker Build Failed

Example

```
COPY failed

↓

File not found
```

Possible reasons

- Wrong Dockerfile path
- Missing files
- Incorrect `.dockerignore`
- Build context issue

______________________________________________________________________

# Common Failure 8

## Authentication Failed

```
Access Denied
```

Possible reasons

- Expired credentials
- Wrong IAM permissions
- Missing GitHub Secret
- Incorrect OIDC configuration

______________________________________________________________________

# Common Failure 9

## Artifact Missing

```
Artifact not found
```

Usually

- Wrong artifact name
- Upload step skipped
- Download in another workflow instead of another job

Remember:

Artifacts are scoped to a workflow run.

______________________________________________________________________

# Common Failure 10

## Cache Miss

```
Cache restored

↓

No cache found
```

Usually caused by

- Changed cache key
- Different operating system
- Dependency file changed

Not an error.

Only slower.

______________________________________________________________________

# Common Failure 11

## Runner Out of Disk

Example

```
No space left on device
```

Common during

- Large Docker builds
- Android builds
- Machine learning projects

Solutions

- Delete temporary files
- Reduce artifacts
- Use larger runners
- Optimize Docker layers

______________________________________________________________________

# Common Failure 12

## Deployment Failed

Example

```
Health check failed
```

Possible reasons

- Wrong environment variables
- Database unavailable
- Migration failed
- Container crash
- Wrong image

______________________________________________________________________

# Debugging Docker Builds

When Docker fails,

don't start with GitHub Actions.

Start locally.

```
docker build .
```

If it fails locally,

it will fail in CI.

______________________________________________________________________

Useful commands

```bash
docker build .
```

```bash
docker run image
```

```bash
docker logs container
```

______________________________________________________________________

# Debugging Kubernetes Deployments

Useful commands

```bash
kubectl get pods
```

______________________________________________________________________

```bash
kubectl describe pod POD_NAME
```

______________________________________________________________________

```bash
kubectl logs POD_NAME
```

______________________________________________________________________

```bash
kubectl rollout status deployment backend
```

______________________________________________________________________

```bash
kubectl rollout undo deployment backend
```

______________________________________________________________________

# Debugging ECS

Useful AWS commands

Describe Service

↓

Describe Task

↓

View Logs

↓

Check Health

Always investigate the first unhealthy task.

______________________________________________________________________

# Performance Optimization

Large companies optimize pipelines aggressively.

______________________________________________________________________

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

Tests

Security
```

simultaneously.

______________________________________________________________________

## Dependency Cache

Without cache

```
pip install

↓

4 minutes
```

With cache

```
Restore Cache

↓

15 seconds
```

______________________________________________________________________

## Docker Layer Cache

Only changed layers rebuild.

Huge improvement.

______________________________________________________________________

## Skip Unnecessary Jobs

Example

Documentation change.

Don't rebuild Docker.

Use path filters.

______________________________________________________________________

## Build Only Changed Services

Monorepo

```
Auth Changed

↓

Build Auth Only
```

______________________________________________________________________

# Security Best Practices

Never trust CI/CD blindly.

Security should be built into every workflow.

______________________________________________________________________

## Use Least Privilege

Bad

```
permissions:

write-all
```

Good

```yaml
permissions:

  contents: read
```

Only request what is necessary.

______________________________________________________________________

## Never Store Secrets in Git

Bad

```python
PASSWORD="abcd123"
```

Good

```
GitHub Secrets
```

______________________________________________________________________

## Rotate Credentials

Secrets should change periodically.

Especially

- Cloud credentials
- API tokens
- SSH keys

______________________________________________________________________

## Prefer OIDC

Avoid long-lived AWS access keys.

Use temporary credentials whenever possible.

______________________________________________________________________

## Pin Action Versions

Bad

```yaml
uses: actions/checkout@main
```

Good

```yaml
uses: actions/checkout@v4
```

Even better (for high-security environments)

```
Commit SHA
```

Pinning avoids unexpected changes.

______________________________________________________________________

## Verify Third-Party Actions

Before using an action,

check

- Maintainer
- Popularity
- Source code
- Last update
- Permissions required

Prefer official GitHub actions when available.

______________________________________________________________________

# Branch Protection

Production branches should be protected.

Typical rules

- Pull request required
- Status checks required
- Code review required
- No force push
- No direct commits

This prevents accidental deployments.

______________________________________________________________________

# GitHub Token Permissions

Every workflow receives

```
GITHUB_TOKEN
```

Limit permissions.

Example

```yaml
permissions:

  contents: read
```

Instead of

```
write-all
```

______________________________________________________________________

# Workflow Design Best Practices

One workflow

↓

One responsibility

Examples

```
CI

CD

Release

Cleanup
```

Instead of

```
One Giant Workflow
```

______________________________________________________________________

## Name Jobs Clearly

Bad

```
job1
```

Good

```
Run Unit Tests
```

______________________________________________________________________

## Keep Deployments Separate

CI

↓

CD

↓

Release

Separate responsibilities.

______________________________________________________________________

## Fail Fast

Stop expensive jobs after critical failures.

______________________________________________________________________

## Upload Useful Artifacts

Examples

- Coverage report
- Test report
- Build logs

Avoid uploading

- Virtual environments
- Dependency caches
- Large temporary files

______________________________________________________________________

# Cost Optimization

GitHub-hosted runners consume minutes.

Reduce usage.

______________________________________________________________________

## Cache Dependencies

Saves minutes every run.

______________________________________________________________________

## Parallel Execution

Shorter pipelines.

______________________________________________________________________

## Cancel Old Runs

Use concurrency.

```
Developer pushes

↓

Push

↓

Push

↓

Cancel Previous
```

______________________________________________________________________

## Skip Unnecessary Workflows

Example

```
README Updated
```

Don't deploy.

Use

```
paths:
```

filters.

______________________________________________________________________

## Self-Hosted Runners

Large companies often use self-hosted runners for

- Lower long-term cost
- Specialized hardware
- Internal infrastructure

______________________________________________________________________

# Real Production Incidents

## Incident 1

Developer accidentally committed AWS credentials.

Result

```
Credential Leak
```

Solution

- Revoke credentials
- Rotate secrets
- Use GitHub Secrets
- Enable secret scanning

______________________________________________________________________

## Incident 2

Deployment passed.

Application crashed.

Cause

Migration wasn't backward compatible.

Lesson

Deploy safe schema changes.

______________________________________________________________________

## Incident 3

Two production deployments started simultaneously.

Result

Inconsistent application versions.

Solution

```
concurrency
```

______________________________________________________________________

## Incident 4

Docker image tagged as

```
latest
```

Rollback impossible.

Solution

Use immutable version tags.

______________________________________________________________________

## Incident 5

Pipeline took

```
35 minutes
```

Cause

No caching

Everything sequential

No path filtering

After optimization

```
9 minutes
```

______________________________________________________________________

# Interview Deep Dive

## Q1. A GitHub Actions workflow failed. What is your debugging process?

### Answer

I begin by identifying the failed job and step in the workflow logs. I read the complete error output instead of making
assumptions, determine whether the issue is related to the application, the workflow configuration, infrastructure, or
deployment, reproduce the problem locally if possible, apply the fix, and then re-run the workflow to verify the
solution.

______________________________________________________________________

## Q2. Why should Docker builds be tested locally first?

### Answer

If a Docker image cannot be built locally, it is unlikely to succeed in CI. Local testing allows faster iteration and
isolates Docker-related issues from GitHub Actions configuration problems.

______________________________________________________________________

## Q3. How would you optimize a GitHub Actions pipeline?

### Answer

I would parallelize independent jobs, cache dependencies, enable Docker layer caching, build only affected services in a
monorepo, skip unnecessary workflows using path filters, fail fast on critical errors, and cancel outdated workflow runs
using concurrency controls.

______________________________________________________________________

## Q4. Why should action versions be pinned?

### Answer

Pinning action versions prevents unexpected behavior caused by upstream changes. It ensures consistent and reproducible
workflow execution. In highly secure environments, pinning to a specific commit SHA provides even stronger guarantees.

______________________________________________________________________

## Q5. What are the most important GitHub Actions security practices?

### Answer

Use GitHub Secrets for sensitive values, prefer OIDC over long-lived cloud credentials, grant only the minimum required
permissions, protect important branches, pin action versions, verify third-party actions before use, and avoid printing
secrets in workflow logs.

______________________________________________________________________

## Q6. Why use branch protection?

### Answer

Branch protection prevents unauthorized or accidental changes to important branches. It can enforce pull requests,
required status checks, code reviews, and other policies before code is merged or deployed.

______________________________________________________________________

## Q7. Why should CI/CD workflows be separated?

### Answer

Separating CI and CD improves maintainability, reduces security risks, allows independent permissions and approval
processes, and makes workflows easier to understand and troubleshoot.

______________________________________________________________________

## Q8. How would you reduce GitHub Actions costs?

### Answer

I would cache dependencies, parallelize independent jobs, cancel outdated workflow runs, avoid triggering workflows for
irrelevant changes, build only affected services in monorepos, and consider self-hosted runners when appropriate for
large or frequent workloads.

______________________________________________________________________

# Summary

In this chapter you learned:

- Workflow debugging methodology
- Reading workflow logs
- Common GitHub Actions failures
- Docker debugging
- Kubernetes debugging
- ECS debugging
- Pipeline optimization
- Dependency caching
- Docker layer caching
- Path filtering
- Security best practices
- Branch protection
- Token permissions
- Workflow design principles
- Cost optimization
- Production incidents
- Advanced troubleshooting
- Interview scenarios

______________________________________________________________________

# Next

[Questions](08_questions.md)
