# GitHub Actions Crash Course

# 01 - GitHub Actions Fundamentals

> **Prerequisites**
>
> - Basic Git
> - Basic GitHub
> - Basic command line
> - Basic YAML (not mandatory)

______________________________________________________________________

# Learning Objectives

After completing this chapter, you should be able to:

- Explain what CI and CD are.
- Understand why GitHub Actions exists.
- Explain the workflow lifecycle.
- Understand events that trigger workflows.
- Read a simple workflow file.
- Navigate the GitHub Actions UI.
- Run workflows using the GitHub CLI.
- Answer common interview questions confidently.

______________________________________________________________________

# Table of Contents

1. What is CI?
1. What is CD?
1. Why Do We Need CI/CD?
1. What is GitHub Actions?
1. GitHub Actions vs Jenkins vs GitLab CI
1. Core Terminology
1. GitHub Actions Workflow Lifecycle
1. Repository Structure
1. Workflow Events
1. Your First Workflow
1. YAML Basics
1. Expressions
1. GitHub Actions UI
1. GitHub CLI
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# What is CI?

CI stands for **Continuous Integration**.

Continuous Integration is the practice of automatically validating code whenever developers push changes to a shared
repository.

Instead of waiting until release day to find problems, every code change is automatically:

- Built
- Tested
- Validated
- Checked for formatting
- Checked for security issues

before it reaches production.

______________________________________________________________________

## Without CI

Imagine three developers.

```
Developer A
        \
Developer B -----> Main Branch
        /
Developer C
```

Everyone writes code for a week.

On Friday:

- Merge everything
- Build project
- Run tests

Suddenly:

- Build fails
- Tests fail
- Dependencies conflict
- Nobody knows which commit caused it

Now everyone spends hours—or days—finding the issue.

This situation is commonly called **Integration Hell**.

______________________________________________________________________

## With CI

Every push automatically runs:

```
Push Code
     │
     ▼
Build Project
     │
     ▼
Run Tests
     │
     ▼
Lint Code
     │
     ▼
Security Scan
     │
     ▼
Success / Failure
```

Problems are detected within minutes instead of days.

______________________________________________________________________

## Benefits of CI

- Faster feedback
- Fewer bugs
- Easier collaboration
- Higher code quality
- Easier deployments
- Increased developer confidence

______________________________________________________________________

# What is CD?

CD can mean two different things.

______________________________________________________________________

## Continuous Delivery

Every successful build is ready for production, but a human decides when to deploy.

```
Push

↓

Tests

↓

Build

↓

Ready for Production

↓

Manual Approval

↓

Deploy
```

Most companies use Continuous Delivery.

______________________________________________________________________

## Continuous Deployment

Every successful build is automatically deployed.

```
Push

↓

Tests

↓

Deploy Automatically
```

No manual approval.

Common for:

- Internal tools
- Small services
- High-automation teams

______________________________________________________________________

## Delivery vs Deployment

| Continuous Delivery | Continuous Deployment |
|----------------------|-----------------------|
| Manual release | Automatic release |
| Human approval | No approval |
| More common | Less common |
| Lower risk | Faster delivery |

______________________________________________________________________

# Why Do We Need CI/CD?

Modern applications are deployed frequently.

Some companies deploy:

- Once a day
- Hundreds of times a day
- Thousands of times a day

Without automation this becomes impossible.

Automation handles:

- Build
- Test
- Lint
- Security scan
- Package
- Deploy
- Notify team

______________________________________________________________________

# What is GitHub Actions?

GitHub Actions is GitHub's built-in automation platform.

It allows you to automate almost anything inside your repository.

Examples:

- Run tests
- Build Docker images
- Deploy to AWS
- Deploy to Kubernetes
- Publish Python packages
- Publish npm packages
- Send Slack notifications
- Generate documentation
- Create releases
- Run scheduled jobs

Think of it as:

> **"If something happens in GitHub, automatically perform these tasks."**

______________________________________________________________________

## Real Example

Developer pushes code.

```
git push

↓

GitHub receives push

↓

Workflow starts

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

↓

Notify Team
```

Nobody manually performs these steps.

______________________________________________________________________

# GitHub Actions vs Jenkins vs GitLab CI

| Feature | GitHub Actions | Jenkins | GitLab CI |
|----------|---------------|----------|------------|
| Built into GitHub | ✅ | ❌ | ❌ |
| Easy setup | ✅ | ❌ | ✅ |
| Plugins | Moderate | Huge | Moderate |
| Maintenance | Very Low | High | Medium |
| Cloud Hosted | Yes | Optional | Yes |
| Self Hosted | Yes | Yes | Yes |

______________________________________________________________________

## Why Companies Prefer GitHub Actions

- No additional server
- Integrated with GitHub
- Huge action marketplace
- Easy YAML syntax
- Fast setup
- Good community support

______________________________________________________________________

# Core Terminology

These are interview favorites.

______________________________________________________________________

## Workflow

A complete automation process.

Example:

```
Build Application

↓

Run Tests

↓

Deploy
```

Stored as a YAML file.

______________________________________________________________________

## Job

A workflow contains one or more jobs.

```
Workflow

├── Build Job

├── Test Job

└── Deploy Job
```

Jobs can run:

- Sequentially
- In parallel

______________________________________________________________________

## Step

A job consists of steps.

```
Job

├── Checkout Code

├── Install Python

├── Install Dependencies

├── Run Tests
```

______________________________________________________________________

## Action

An action is reusable code.

Instead of writing everything yourself:

```
uses: actions/checkout@v4
```

GitHub downloads the action and executes it.

______________________________________________________________________

## Runner

A runner is the machine executing your workflow.

Can be:

- Ubuntu
- Windows
- macOS

GitHub-hosted runners are the most common.

______________________________________________________________________

# GitHub Actions Workflow Lifecycle

```
Developer Pushes Code

↓

GitHub Detects Event

↓

Workflow Starts

↓

Runner Allocated

↓

Jobs Execute

↓

Steps Execute

↓

Results Uploaded

↓

Workflow Completes
```

______________________________________________________________________

# Repository Structure

GitHub Actions only looks inside:

```
.github/
└── workflows/
    ├── ci.yml
    ├── deploy.yml
    └── release.yml
```

Any `.yml` or `.yaml` file inside `.github/workflows/` is treated as a workflow.

______________________________________________________________________

# Workflow Events

Workflows don't run by themselves.

An event triggers them.

______________________________________________________________________

## Push

```yaml
on:
  push:
```

Runs whenever code is pushed.

______________________________________________________________________

## Pull Request

```yaml
on:
  pull_request:
```

Runs when a PR is opened, updated, or synchronized.

______________________________________________________________________

## Manual Trigger

```yaml
on:
  workflow_dispatch:
```

Allows you to click **Run workflow** in GitHub.

Very useful for deployments.

______________________________________________________________________

## Scheduled

```yaml
on:
  schedule:
    - cron: "0 0 * * *"
```

Runs automatically on a schedule.

Example:

- Backup
- Cleanup
- Report generation

______________________________________________________________________

## Release

```yaml
on:
  release:
```

Runs whenever a GitHub release is published.

______________________________________________________________________

## Tag

```yaml
on:
  push:
    tags:
      - "v*"
```

Example:

```
v1.0
v2.3
v5.1
```

______________________________________________________________________

# Your First Workflow

Create:

```
.github/workflows/hello.yml
```

```yaml
name: Hello Workflow

on:
  push:

jobs:
  hello:
    runs-on: ubuntu-latest

    steps:
      - name: Print Message
        run: echo "Hello GitHub Actions!"
```

______________________________________________________________________

## Understanding It

### Name

```yaml
name: Hello Workflow
```

Workflow name shown in GitHub UI.

______________________________________________________________________

### Event

```yaml
on:
  push:
```

Trigger on every push.

______________________________________________________________________

### Job

```yaml
jobs:
```

Defines one or more jobs.

______________________________________________________________________

### Runner

```yaml
runs-on: ubuntu-latest
```

Use GitHub's Ubuntu VM.

______________________________________________________________________

### Step

```yaml
steps:
```

List of commands.

______________________________________________________________________

### Run

```yaml
run: echo "Hello"
```

Runs a shell command.

______________________________________________________________________

# YAML Basics

GitHub Actions uses YAML.

______________________________________________________________________

## Key-Value Pair

```yaml
name: Build Project
```

______________________________________________________________________

## Lists

```yaml
steps:
  - name: Step One

  - name: Step Two
```

______________________________________________________________________

## Nested Objects

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

______________________________________________________________________

## Indentation

Correct:

```yaml
jobs:
  build:
    steps:
```

Wrong:

```yaml
jobs:
 build:
      steps:
```

YAML is indentation-sensitive.

______________________________________________________________________

# Expressions

GitHub Actions uses expressions inside:

```text
${{ }}
```

Example:

```yaml
${{ github.ref }}
```

Example:

```yaml
${{ github.actor }}
```

Example:

```yaml
${{ github.repository }}
```

We'll cover expressions in detail later.

______________________________________________________________________

# GitHub Actions UI

Navigate to:

```
Repository

↓

Actions Tab
```

You can view:

- Running workflows
- Completed workflows
- Logs
- Jobs
- Steps
- Duration
- Failures
- Artifacts

______________________________________________________________________

## Reading Logs

Logs are organized as:

```
Workflow

↓

Job

↓

Step

↓

Command Output
```

Always start debugging from the failed step.

______________________________________________________________________

# GitHub CLI

GitHub provides the `gh` CLI for interacting with repositories and workflows.

______________________________________________________________________

## Installation

### macOS

```bash
brew install gh
```

### Ubuntu

```bash
sudo apt install gh
```

### Windows

```powershell
winget install GitHub.cli
```

Or install using the official installer from GitHub.

______________________________________________________________________

## Authenticate

```bash
gh auth login
```

______________________________________________________________________

## List Workflows

```bash
gh workflow list
```

______________________________________________________________________

## Run Workflow

```bash
gh workflow run hello.yml
```

______________________________________________________________________

## List Runs

```bash
gh run list
```

______________________________________________________________________

## Watch Workflow

```bash
gh run watch
```

______________________________________________________________________

## View Logs

```bash
gh run view
```

______________________________________________________________________

## Re-run Failed Workflow

```bash
gh run rerun
```

______________________________________________________________________

## Cancel Workflow

```bash
gh run cancel RUN_ID
```

______________________________________________________________________

# Best Practices

- Keep workflows small and focused.
- Give workflows descriptive names.
- Use separate workflows for CI and deployment.
- Keep secrets out of the repository.
- Pin action versions instead of using floating versions when possible.
- Test changes on feature branches before merging.
- Read logs from the first failed step instead of guessing.

______________________________________________________________________

# Common Mistakes

### Wrong Indentation

YAML parsing fails immediately.

______________________________________________________________________

### Forgetting Event

No event means the workflow never starts.

______________________________________________________________________

### Wrong File Location

The workflow must be inside:

```
.github/workflows/
```

______________________________________________________________________

### Hardcoding Secrets

Never write:

```yaml
AWS_SECRET_KEY=abcd1234
```

Use GitHub Secrets instead.

______________________________________________________________________

### Ignoring Logs

Most failures are explained directly in the workflow logs.

______________________________________________________________________

# Interview Deep Dive

## Q1. What is Continuous Integration?

### Answer

Continuous Integration (CI) is the practice of automatically building, testing, and validating code whenever changes are
pushed to a shared repository. It helps detect integration issues early, improves code quality, and allows teams to
merge changes more frequently with confidence.

______________________________________________________________________

## Q2. What is the difference between Continuous Delivery and Continuous Deployment?

### Answer

In Continuous Delivery, every successful build is ready for production, but deployment requires manual approval. In
Continuous Deployment, successful builds are automatically deployed to production without human intervention.

______________________________________________________________________

## Q3. What is GitHub Actions?

### Answer

GitHub Actions is GitHub's built-in automation platform that executes workflows based on repository events. It is
commonly used for CI/CD, testing, deployments, release automation, and repository maintenance.

______________________________________________________________________

## Q4. What is a workflow?

### Answer

A workflow is a YAML-defined automation process stored under `.github/workflows`. It contains one or more jobs that
execute when specified events occur.

______________________________________________________________________

## Q5. What is a job?

### Answer

A job is a collection of related steps executed on a runner. Jobs within a workflow can run sequentially using
dependencies or in parallel when independent.

______________________________________________________________________

## Q6. What is a step?

### Answer

A step is an individual task inside a job. Steps can execute shell commands using `run` or reusable actions using
`uses`.

______________________________________________________________________

## Q7. What is a runner?

### Answer

A runner is the machine that executes a workflow. GitHub provides hosted runners for Ubuntu, Windows, and macOS, and
organizations can also configure self-hosted runners.

______________________________________________________________________

## Q8. What are common workflow triggers?

### Answer

Common triggers include `push`, `pull_request`, `workflow_dispatch`, `schedule`, `release`, and tag-based pushes. These
events determine when a workflow starts.

______________________________________________________________________

# Summary

In this chapter you learned:

- CI fundamentals
- CD fundamentals
- Continuous Delivery vs Continuous Deployment
- Why CI/CD is important
- GitHub Actions architecture
- Workflows
- Jobs
- Steps
- Actions
- Runners
- Workflow events
- Repository structure
- Basic YAML
- GitHub Actions UI
- GitHub CLI
- Common interview questions

______________________________________________________________________

# Next

[Workflows Jobs Steps Runners](02_workflows-jobs-steps-runners.md)
