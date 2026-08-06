# GitHub Actions Deep Dive

> File: `03_github-actions-deep-dive.md`

______________________________________________________________________

# Learning Objectives

After completing this chapter, you will be able to:

- Understand every important workflow keyword
- Use expressions confidently
- Work with contexts
- Create reusable workflows
- Build Composite Actions
- Understand JavaScript and Docker Actions
- Secure workflows using secrets and permissions
- Configure concurrency and conditional execution
- Explain advanced GitHub Actions concepts in interviews

______________________________________________________________________

# Table of Contents

1. Workflow Keywords
1. Expressions
1. Contexts
1. Variables
1. Secrets
1. Conditional Execution
1. Outputs
1. Reusable Workflows
1. Composite Actions
1. Marketplace Actions
1. JavaScript Actions
1. Docker Actions
1. Local Actions
1. Permissions
1. Concurrency
1. Continue on Error
1. Best Practices
1. Common Mistakes
1. Interview Deep Dive
1. Summary

______________________________________________________________________

# Understanding Workflow Keywords

Let's revisit a workflow.

```yaml
name: Python CI

on:
  push:
    branches:
      - main

env:
  APP_NAME: backend-api

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
```

Although it looks simple, every keyword has a specific purpose.

______________________________________________________________________

## name

Human-readable workflow name.

```yaml
name: Backend CI
```

Shown in:

- Actions tab
- Workflow history
- Notifications

Use descriptive names.

Good:

```yaml
Backend CI Pipeline
```

Bad:

```yaml
Workflow 1
```

______________________________________________________________________

## on

Defines which event triggers the workflow.

Example

```yaml
on:
  push:
```

Multiple events

```yaml
on:

  push:

  pull_request:

  workflow_dispatch:
```

______________________________________________________________________

## jobs

Defines every job in the workflow.

```yaml
jobs:

  test:

  build:

  deploy:
```

______________________________________________________________________

## runs-on

Defines which runner executes the job.

```yaml
runs-on: ubuntu-latest
```

Other examples

```yaml
runs-on: windows-latest
```

```yaml
runs-on: macos-latest
```

```yaml
runs-on: self-hosted
```

______________________________________________________________________

## steps

List of tasks executed inside a job.

```yaml
steps:

- name:

- uses:

- run:
```

______________________________________________________________________

## uses

Executes an action.

```yaml
uses: actions/checkout@v4
```

GitHub downloads and executes the action.

______________________________________________________________________

## run

Runs shell commands.

```yaml
run: pytest
```

Another example

```yaml
run: python app.py
```

______________________________________________________________________

## with

Passes inputs to actions.

```yaml
uses: actions/setup-python@v5

with:
  python-version: "3.12"
```

Without `with`, the action uses its defaults.

______________________________________________________________________

## env

Defines environment variables.

Workflow level

```yaml
env:
  APP_ENV: production
```

Job level

```yaml
jobs:

  test:

    env:
      VERSION: "1.0"
```

Step level

```yaml
steps:

- run: echo $VERSION
```

______________________________________________________________________

## defaults

Sets default behavior.

Example

```yaml
defaults:

  run:

    shell: bash
```

Instead of specifying the shell on every step.

______________________________________________________________________

# Expressions

GitHub evaluates expressions inside

```text
${{ }}
```

Examples

```yaml
${{ github.actor }}
```

```yaml
${{ github.ref }}
```

```yaml
${{ github.repository }}
```

Expressions make workflows dynamic.

______________________________________________________________________

## Example

```yaml
run: echo "${{ github.actor }}"
```

Output

```
riyaz
```

______________________________________________________________________

## Another Example

```yaml
run: echo "${{ github.repository }}"
```

Output

```
company/backend
```

______________________________________________________________________

# Functions

GitHub provides helper functions.

______________________________________________________________________

## success()

Runs only if previous steps succeeded.

```yaml
if: success()
```

______________________________________________________________________

## failure()

Runs only when something failed.

```yaml
if: failure()
```

Useful for notifications.

______________________________________________________________________

## always()

Runs regardless of success or failure.

```yaml
if: always()
```

Useful for cleanup.

______________________________________________________________________

## cancelled()

Runs only if workflow was cancelled.

```yaml
if: cancelled()
```

______________________________________________________________________

# Contexts

Contexts provide workflow information.

Think of them as predefined objects.

```
github

runner

job

steps

env

vars

matrix

needs
```

______________________________________________________________________

# github Context

Contains repository information.

Example

```yaml
${{ github.actor }}
```

Current user.

______________________________________________________________________

```yaml
${{ github.ref }}
```

Current branch or tag.

______________________________________________________________________

```yaml
${{ github.repository }}
```

Repository name.

______________________________________________________________________

```yaml
${{ github.sha }}
```

Current commit SHA.

______________________________________________________________________

```yaml
${{ github.event_name }}
```

Triggering event.

______________________________________________________________________

# runner Context

Information about the runner.

```yaml
${{ runner.os }}
```

Example output

```
Linux
```

______________________________________________________________________

```yaml
${{ runner.arch }}
```

Output

```
X64
```

______________________________________________________________________

# job Context

Contains job metadata.

Example

```yaml
${{ job.status }}
```

Possible values

```
success

failure

cancelled
```

______________________________________________________________________

# steps Context

Access outputs from previous steps.

```yaml
steps.build.outputs.version
```

______________________________________________________________________

# env Context

Access environment variables.

```yaml
${{ env.APP_NAME }}
```

______________________________________________________________________

# vars Context

Repository variables.

Configured in:

```
Repository

↓

Settings

↓

Variables
```

Example

```yaml
${{ vars.REGION }}
```

______________________________________________________________________

# matrix Context

Used inside matrix builds.

```yaml
${{ matrix.python-version }}
```

Output

```
3.10

3.11

3.12
```

______________________________________________________________________

# needs Context

Access outputs from another job.

```yaml
needs.build.outputs.image
```

______________________________________________________________________

# Variables

There are three common variable types.

Workflow variables

```yaml
env:
```

Repository variables

```text
Settings

↓

Variables
```

Organization variables

Shared across repositories.

______________________________________________________________________

# Secrets

Secrets store sensitive information.

Examples

- AWS credentials
- API keys
- Database passwords
- Docker credentials
- SSH private keys

______________________________________________________________________

## Creating Secrets

Repository

↓

Settings

↓

Secrets and Variables

↓

Actions

↓

New Repository Secret

______________________________________________________________________

## Using Secrets

```yaml
env:

  TOKEN: ${{ secrets.API_TOKEN }}
```

or

```yaml
run: echo "${{ secrets.API_TOKEN }}"
```

Never print secrets in logs.

GitHub masks secret values automatically, but avoid echoing them entirely.

______________________________________________________________________

# Conditional Execution

You don't always want every step to run.

Example

Deploy only from `main`.

```yaml
if: github.ref == 'refs/heads/main'
```

______________________________________________________________________

Deploy only on tags.

```yaml
if: startsWith(github.ref, 'refs/tags/')
```

______________________________________________________________________

Only for pull requests.

```yaml
if: github.event_name == 'pull_request'
```

______________________________________________________________________

# Step Outputs

A step can generate outputs.

Example

```yaml
- id: version

  run: echo "tag=v1.0" >> "$GITHUB_OUTPUT"
```

Later

```yaml
${{ steps.version.outputs.tag }}
```

Output

```
v1.0
```

______________________________________________________________________

# Reusable Workflows

Imagine ten repositories.

Each has identical CI.

Without reusable workflows

```
Repo A

Repo B

Repo C

Repo D
```

Duplicate YAML everywhere.

______________________________________________________________________

With reusable workflows

```
Common Workflow

↓

All Repositories Use It
```

______________________________________________________________________

Calling a reusable workflow

```yaml
uses: company/platform/.github/workflows/python.yml@main
```

Benefits

- Single source of truth
- Easier maintenance
- Standardized CI/CD

______________________________________________________________________

# Composite Actions

Composite Actions package multiple steps into one reusable action.

Instead of

```yaml
Install

Lint

Test
```

Create

```
company/python-ci-action
```

Now simply

```yaml
uses: company/python-ci-action@v1
```

Great for internal engineering teams.

______________________________________________________________________

# Marketplace Actions

GitHub Marketplace contains thousands of actions.

Examples

Checkout

```
actions/checkout
```

Python

```
actions/setup-python
```

Node

```
actions/setup-node
```

Docker

```
docker/build-push-action
```

AWS

```
aws-actions/configure-aws-credentials
```

Azure

```
azure/login
```

Instead of writing integrations yourself, you reuse community-maintained actions.

______________________________________________________________________

# JavaScript Actions

Written using Node.js.

Useful for

- API calls
- GitHub integrations
- Automation logic

Structure

```
action.yml

index.js

package.json
```

______________________________________________________________________

# Docker Actions

Run inside Docker containers.

Structure

```
Dockerfile

action.yml
```

Advantages

- Same environment everywhere
- Dependency isolation
- Complex tooling support

______________________________________________________________________

# Local Actions

Reusable actions stored inside the repository.

Example

```
.github/actions/

deploy/

lint/
```

Use

```yaml
uses: ./.github/actions/deploy
```

Useful for organization-specific logic.

______________________________________________________________________

# Permissions

Every workflow receives a GitHub token.

```
GITHUB_TOKEN
```

Never grant more permissions than necessary.

Example

```yaml
permissions:

  contents: read
```

Instead of

```yaml
permissions:

  write-all
```

Principle:

**Least Privilege**

______________________________________________________________________

# Concurrency

Prevent duplicate workflow execution.

Without concurrency

```
Push 1

Push 2

Push 3

↓

Three deployments
```

With concurrency

```yaml
concurrency:

  group: production

  cancel-in-progress: true
```

Result

```
Push 1

Cancelled

Push 2

Cancelled

Push 3

Runs
```

Ideal for deployments.

______________________________________________________________________

# Continue on Error

Normally,

failed step

↓

workflow stops

Sometimes you want the workflow to continue.

```yaml
continue-on-error: true
```

Example

Security scan reports warnings but shouldn't block deployment in a development environment.

______________________________________________________________________

# Best Practices

- Use repository variables for configuration.
- Store credentials only in Secrets.
- Reuse workflows whenever possible.
- Keep permissions minimal.
- Use conditions instead of duplicate workflows.
- Prefer official GitHub Actions.
- Pin action versions (`@v4`, `@v5`) rather than floating references.
- Keep Composite Actions focused on one responsibility.

______________________________________________________________________

# Common Mistakes

## Printing Secrets

Never do this.

```yaml
echo ${{ secrets.API_KEY }}
```

______________________________________________________________________

## Duplicate YAML

Create reusable workflows instead.

______________________________________________________________________

## Using write-all Permissions

Grant only the permissions required.

______________________________________________________________________

## Hardcoding Branch Names Everywhere

Use repository variables or reusable workflows when appropriate.

______________________________________________________________________

## Ignoring Conditions

Don't run deployment steps for every pull request.

______________________________________________________________________

# Interview Deep Dive

## Q1. What is the purpose of `${{ }}`?

### Answer

`${{ }}` is the GitHub Actions expression syntax. It evaluates variables, contexts, functions, and conditions at
workflow runtime, allowing workflows to make decisions dynamically.

______________________________________________________________________

## Q2. What is the difference between Secrets and Variables?

### Answer

Variables store non-sensitive configuration such as regions or environment names, while Secrets store sensitive values
like passwords, API keys, and cloud credentials. Secrets are encrypted and masked in workflow logs.

______________________________________________________________________

## Q3. What are Contexts?

### Answer

Contexts are predefined objects that expose workflow information. Common contexts include `github`, `env`, `runner`,
`job`, `steps`, `matrix`, and `needs`. They provide metadata that workflows can use dynamically.

______________________________________________________________________

## Q4. What is a Composite Action?

### Answer

A Composite Action packages multiple workflow steps into a reusable action. It helps eliminate duplication and
standardize common processes across repositories.

______________________________________________________________________

## Q5. What is a Reusable Workflow?

### Answer

A reusable workflow is an entire workflow that can be invoked by other repositories or workflows using `workflow_call`.
It enables organizations to centralize CI/CD logic and enforce consistent pipelines.

______________________________________________________________________

## Q6. What is the difference between a Composite Action and a Reusable Workflow?

### Answer

A Composite Action groups multiple steps and runs inside a single job, making it suitable for reusable task sequences. A
reusable workflow contains complete jobs and can define its own runners, permissions, inputs, outputs, and multiple
stages, making it appropriate for sharing entire CI/CD pipelines.

______________________________________________________________________

## Q7. Why should workflow permissions follow the principle of least privilege?

### Answer

Granting only the required permissions reduces the impact of compromised workflows or actions. Limiting access minimizes
security risks and helps protect repository contents and deployment credentials.

______________________________________________________________________

## Q8. Why is concurrency useful?

### Answer

Concurrency prevents multiple workflows from performing the same operation simultaneously. It is commonly used to avoid
overlapping deployments, cancel outdated pipeline runs, and ensure only the latest changes are deployed.

______________________________________________________________________

# Summary

In this chapter you learned:

- Workflow keywords
- Expressions
- Functions
- Contexts
- Variables
- Secrets
- Conditional execution
- Step outputs
- Reusable workflows
- Composite Actions
- Marketplace Actions
- JavaScript Actions
- Docker Actions
- Local Actions
- Permissions
- Concurrency
- Continue-on-error
- Security best practices
- Advanced interview topics

______________________________________________________________________

# Next

[CI/CD Pipeline Design](04_cicd-pipeline-design.md)
