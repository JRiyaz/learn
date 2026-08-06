# Workflows Jobs Steps Runners

> File: `02_workflows-jobs-steps-runners.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Understand the complete workflow architecture
- Create workflows with multiple jobs
- Execute jobs sequentially and in parallel
- Understand runners and when to use each type
- Pass data between jobs
- Use environment variables
- Configure matrix builds
- Cache dependencies
- Upload and download artifacts
- Explain these concepts confidently in interviews

______________________________________________________________________

# Table of Contents

1. Workflow Architecture
1. Workflow Anatomy
1. Jobs
1. Steps
1. Actions
1. Runners
1. Multiple Jobs
1. Job Dependencies
1. Parallel Execution
1. Matrix Strategy
1. Environment Variables
1. Outputs
1. Artifacts
1. Dependency Caching
1. Timeout & Concurrency
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# Workflow Architecture

Everything in GitHub Actions follows one hierarchy.

```
Workflow
    │
    ├── Job
    │      │
    │      ├── Step
    │      ├── Step
    │      └── Step
    │
    ├── Job
    │      │
    │      ├── Step
    │      └── Step
    │
    └── Job
           │
           ├── Step
           └── Step
```

Think of it like:

- Workflow → Entire project
- Job → One phase
- Step → One task

______________________________________________________________________

# Workflow Anatomy

A typical workflow looks like this.

```yaml
name: Python CI

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Tests
        run: pytest
```

______________________________________________________________________

## Breaking It Down

```
Workflow

├── Trigger
│
├── Job
│
├── Runner
│
├── Steps
│
└── Commands
```

______________________________________________________________________

# Jobs

A workflow contains one or more jobs.

Example:

```yaml
jobs:

  lint:

  test:

  build:

  deploy:
```

Each job represents one logical stage.

For example:

```
Lint

↓

Test

↓

Build

↓

Deploy
```

______________________________________________________________________

# Why Multiple Jobs?

Instead of doing everything in one job,

```
Install

↓

Lint

↓

Test

↓

Build

↓

Deploy
```

we separate responsibilities.

```
Job 1 → Lint

Job 2 → Test

Job 3 → Build

Job 4 → Deploy
```

Advantages:

- Easier debugging
- Parallel execution
- Better readability
- Reusable pipeline design

______________________________________________________________________

# Steps

Each job contains steps.

Example

```yaml
steps:

- Checkout

- Install Python

- Install Dependencies

- Run Tests

- Upload Artifact
```

Each step executes one task.

______________________________________________________________________

# Two Types of Steps

## run

Executes shell commands.

```yaml
- run: python app.py
```

Another example

```yaml
- run: pytest
```

______________________________________________________________________

## uses

Runs reusable GitHub Actions.

```yaml
- uses: actions/checkout@v4
```

Instead of writing checkout logic yourself, GitHub downloads the action.

______________________________________________________________________

# Common Actions

## Checkout

```yaml
- uses: actions/checkout@v4
```

Downloads repository code.

______________________________________________________________________

## Setup Python

```yaml
- uses: actions/setup-python@v5
```

Installs Python.

______________________________________________________________________

## Upload Artifact

```yaml
- uses: actions/upload-artifact@v4
```

Stores build output.

______________________________________________________________________

## Download Artifact

```yaml
- uses: actions/download-artifact@v4
```

Downloads artifacts from previous jobs.

______________________________________________________________________

# Runners

A runner is the machine executing your workflow.

```
GitHub

↓

Allocates Runner

↓

Runner Executes Jobs
```

______________________________________________________________________

# GitHub Hosted Runners

Most common.

Supported operating systems:

```text
ubuntu-latest

windows-latest

macos-latest
```

Example

```yaml
runs-on: ubuntu-latest
```

GitHub creates a fresh VM for every workflow.

Advantages

- No maintenance
- Always clean
- Easy setup

Disadvantages

- Limited customization
- Usage minutes may be billed on some plans

______________________________________________________________________

# Self Hosted Runners

Instead of GitHub providing the machine, your organization provides one.

```
GitHub

↓

Your Server

↓

Workflow Runs
```

Common reasons:

- Internal network access
- Special hardware
- Large builds
- GPUs
- Custom software

Example

```yaml
runs-on: self-hosted
```

______________________________________________________________________

# Runner Lifecycle

```
Workflow Starts

↓

Runner Allocated

↓

Repository Checked Out

↓

Steps Execute

↓

Runner Cleaned Up
```

GitHub-hosted runners are ephemeral.

Every workflow starts with a clean machine.

______________________________________________________________________

# Multiple Jobs

Example

```yaml
jobs:

  lint:

  test:

  build:
```

Visualization

```
Workflow

├── Lint

├── Test

└── Build
```

______________________________________________________________________

# Sequential Jobs

Sometimes deployment should only happen after testing.

```yaml
jobs:

  test:

  build:
    needs: test

  deploy:
    needs: build
```

Execution

```
Test

↓

Build

↓

Deploy
```

______________________________________________________________________

# Parallel Jobs

Independent jobs can execute simultaneously.

```yaml
jobs:

  lint:

  test:

  security:
```

Execution

```
        Lint

      /

Start

      \

        Test

      \

        Security
```

Parallel jobs reduce total execution time.

______________________________________________________________________

# Matrix Strategy

Suppose your application supports multiple Python versions.

Instead of writing three jobs:

```
Python 3.10

Python 3.11

Python 3.12
```

GitHub generates them automatically.

```yaml
strategy:
  matrix:
    python-version:
      - "3.10"
      - "3.11"
      - "3.12"
```

Then:

```yaml
uses: actions/setup-python@v5

with:
  python-version: ${{ matrix.python-version }}
```

GitHub automatically creates

```
Job 1 → Python 3.10

Job 2 → Python 3.11

Job 3 → Python 3.12
```

Very common interview topic.

______________________________________________________________________

# Environment Variables

Environment variables avoid hardcoding values.

Workflow level

```yaml
env:
  APP_NAME: backend
```

Job level

```yaml
jobs:

  build:

    env:
      VERSION: "1.0"
```

Step level

```yaml
steps:

- run: echo $VERSION
```

Priority

```
Step

↓

Job

↓

Workflow
```

The closest scope overrides outer scopes.

______________________________________________________________________

# Passing Data Between Jobs

Sometimes one job produces data used later.

Example

```
Build

↓

Image Tag

↓

Deploy
```

Job outputs make this possible.

Build job

```yaml
outputs:
  image: ${{ steps.build.outputs.image }}
```

Deploy job

```yaml
needs.build.outputs.image
```

We'll cover syntax in detail later.

______________________________________________________________________

# Artifacts

Artifacts store files generated during a workflow.

Examples

- Test reports
- Coverage reports
- Docker image metadata
- Logs
- ZIP files
- Compiled binaries

Upload

```yaml
- uses: actions/upload-artifact@v4

  with:
    name: coverage

    path: coverage.xml
```

Download

```yaml
- uses: actions/download-artifact@v4

  with:
    name: coverage
```

Artifacts are available after the workflow finishes.

______________________________________________________________________

# Dependency Caching

Installing dependencies every run wastes time.

Without cache

```
Install Packages

↓

5 Minutes
```

With cache

```
Restore Cache

↓

30 Seconds
```

Example

```yaml
- uses: actions/cache@v4
```

Typical cache targets

Python

```
~/.cache/pip
```

Node.js

```
node_modules
```

Gradle

```
.gradle
```

Maven

```
.m2
```

______________________________________________________________________

# Cache Keys

Every cache needs a key.

Example

```yaml
key: pip-${{ hashFiles('requirements.txt') }}
```

If requirements change,

cache changes automatically.

______________________________________________________________________

# Cache Hit

```
Cache Found

↓

Skip Installation
```

______________________________________________________________________

# Cache Miss

```
No Cache

↓

Install Packages

↓

Save Cache
```

______________________________________________________________________

# Timeout

Prevent workflows from hanging forever.

```yaml
timeout-minutes: 20
```

If exceeded,

GitHub stops the job.

______________________________________________________________________

# Concurrency

Imagine two developers pushing repeatedly.

Without concurrency

```
Deploy

Deploy

Deploy

Deploy
```

All execute.

With concurrency

```
Deploy

Cancel Previous

Deploy Latest
```

Example

```yaml
concurrency:

  group: production

  cancel-in-progress: true
```

Useful for deployments.

______________________________________________________________________

# Best Practices

- One responsibility per job
- Use descriptive job names
- Run independent jobs in parallel
- Keep deployments separate from CI
- Cache dependencies
- Upload useful artifacts
- Set reasonable timeouts
- Avoid duplicated logic

______________________________________________________________________

# Common Mistakes

## Everything in One Job

Hard to debug.

______________________________________________________________________

## No Cache

Long execution times.

______________________________________________________________________

## Hardcoded Versions

Prefer variables or matrices when appropriate.

______________________________________________________________________

## Missing Dependencies

Deploying before tests finish.

Use `needs`.

______________________________________________________________________

## Uploading Huge Artifacts

Artifacts consume storage.

Only upload useful files.

______________________________________________________________________

# Interview Deep Dive

## Q1. What is the difference between a workflow and a job?

### Answer

A workflow is the complete automation process triggered by repository events. A workflow can contain multiple jobs, each
representing a logical stage such as testing, building, or deployment.

______________________________________________________________________

## Q2. What is the difference between a job and a step?

### Answer

A job is a collection of related steps executed on a runner. A step is a single task inside that job, such as checking
out code, installing dependencies, or running tests.

______________________________________________________________________

## Q3. What is the difference between `run` and `uses`?

### Answer

`run` executes shell commands directly on the runner, while `uses` executes a reusable GitHub Action. `uses` is
preferred for common tasks like checking out code or setting up language runtimes because it avoids reimplementing
standard functionality.

______________________________________________________________________

## Q4. What is a runner?

### Answer

A runner is the machine that executes workflow jobs. GitHub provides hosted runners for Linux, Windows, and macOS, while
organizations can configure self-hosted runners for custom environments or internal infrastructure.

______________________________________________________________________

## Q5. When would you use a self-hosted runner?

### Answer

Self-hosted runners are useful when workflows require access to private networks, custom software, specialized hardware
such as GPUs, or when organizations want greater control over the execution environment.

______________________________________________________________________

## Q6. Why use a matrix strategy?

### Answer

A matrix strategy allows the same job to run across multiple configurations, such as different Python versions or
operating systems, reducing duplication and improving test coverage.

______________________________________________________________________

## Q7. What is the difference between artifacts and caches?

### Answer

Artifacts are files preserved after a workflow finishes, such as test reports or compiled binaries, and are intended for
later retrieval. Caches store reusable dependencies between workflow runs to speed up execution and are restored
automatically when cache keys match.

______________________________________________________________________

## Q8. What does `needs` do?

### Answer

The `needs` keyword creates dependencies between jobs. A job configured with `needs` will start only after the specified
job completes successfully, enabling sequential pipeline stages such as testing before deployment.

______________________________________________________________________

# Summary

In this chapter you learned:

- Workflow hierarchy
- Jobs
- Steps
- Actions
- Runners
- GitHub-hosted vs self-hosted runners
- Sequential jobs
- Parallel jobs
- Matrix builds
- Environment variables
- Job outputs
- Artifacts
- Dependency caching
- Timeouts
- Concurrency
- Best practices
- Common interview questions

______________________________________________________________________

# Next

[GitHub Actions Deep Dive](03_github-actions-deep-dive.md)
