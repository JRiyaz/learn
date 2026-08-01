# Docker - Part 8

# Environment Variables & Secrets

______________________________________________________________________

# Introduction

So far, we've built Docker images and learned how containers communicate.

Now imagine the following situation.

Your FastAPI application contains:

```python
DATABASE_URL = "postgresql://admin:my_password@postgres:5432/library"
```

Looks fine...

until you push the project to GitHub.

Now your database password is public.

This is one of the biggest security mistakes beginners make.

Docker provides a better way to configure applications without changing the source code.

______________________________________________________________________

# What Are Environment Variables?

Environment variables are key-value pairs provided to an application **at runtime**.

Instead of

```python
DATABASE_URL = "postgresql://localhost/library"
```

we write

```python
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)
```

Now the application doesn't know the actual value.

Docker provides it.

______________________________________________________________________

# Why Environment Variables?

Suppose you have three environments.

```text
Development

↓

Testing

↓

Production
```

Each environment has a different database.

Development

```text
localhost
```

Testing

```text
test-db
```

Production

```text
prod-db
```

Instead of changing your Python code,

change the environment variable.

______________________________________________________________________

# Configuration Without Environment Variables

```text
app.py

↓

Modify Code

↓

Commit

↓

Deploy
```

Every environment requires code changes.

Not ideal.

______________________________________________________________________

# Configuration With Environment Variables

```text
Same Code

↓

Different Environment Variables

↓

Different Behavior
```

Much cleaner.

______________________________________________________________________

# Reading Variables in Python

```python
import os

database_url = os.getenv(
    "DATABASE_URL"
)

redis_host = os.getenv(
    "REDIS_HOST"
)

environment = os.getenv(
    "APP_ENV"
)
```

The application stays the same.

Only configuration changes.

______________________________________________________________________

# Setting Environment Variables

Example

```bash
docker run \

-e APP_ENV=development \

-e DATABASE_URL=postgresql://postgres/library \

my-fastapi-app
```

Now

inside the container

```text
APP_ENV

↓

development
```

______________________________________________________________________

# Multiple Variables

Example

```bash
docker run \

-e DATABASE_HOST=postgres \

-e DATABASE_PORT=5432 \

-e REDIS_HOST=redis \

-e REDIS_PORT=6379 \

fastapi-app
```

Your application reads them normally.

______________________________________________________________________

# Using Defaults

Sometimes

a variable may not exist.

```python
import os

environment = os.getenv(
    "APP_ENV",
    "development"
)
```

If

`APP_ENV`

doesn't exist,

Python returns

```text
development
```

______________________________________________________________________

# Environment Variables vs Hardcoding

Hardcoded

```python
PASSWORD = "secret123"
```

Environment Variable

```python
PASSWORD = os.getenv(
    "PASSWORD"
)
```

Always prefer the second approach.

______________________________________________________________________

# Common Application Variables

```text
DATABASE_URL

REDIS_HOST

REDIS_PORT

KAFKA_BROKER

APP_ENV

LOG_LEVEL

API_PORT
```

These values change between environments.

______________________________________________________________________

# What About Passwords?

Environment variables are convenient,

but they're **not** a complete secret-management solution.

For small projects and local development,

they're commonly used.

For production,

dedicated secret-management systems are often preferred.

We'll discuss those shortly.

______________________________________________________________________

# Secrets

A secret is sensitive information.

Examples

```text
Database Password

API Key

JWT Secret

OAuth Client Secret

Cloud Credentials
```

Never hardcode these values.

______________________________________________________________________

# Why Not Store Secrets in Git?

Suppose

```python
API_KEY = "abcd123456"
```

You push to GitHub.

Now

everyone can read it.

Even if you delete it later,

Git history may still contain it.

______________________________________________________________________

# Dockerfile Mistake

Never do this.

```dockerfile
ENV DATABASE_PASSWORD=mysecret
```

The value becomes part of the image metadata.

Anyone with access to the image may be able to inspect it.

______________________________________________________________________

# Better Approach

Provide the value

when running the container.

```bash
docker run \

-e DATABASE_PASSWORD=mysecret \

fastapi-app
```

Now

the Dockerfile

remains generic.

______________________________________________________________________

# `.env` Files

Instead of writing

many

`-e`

flags,

create

```text
.env
```

Example

```text
DATABASE_HOST=postgres

DATABASE_PORT=5432

REDIS_HOST=redis

APP_ENV=development
```

Many tools (including Docker Compose) can read values from `.env` files.

______________________________________________________________________

# Python Example

Using the standard library,

environment variables are already available.

```python
import os

database_host = os.getenv(
    "DATABASE_HOST"
)
```

For local development, many projects also use libraries such as `python-dotenv` to load values from a `.env` file into
the environment.

______________________________________________________________________

# Different Environments

Development

```text
APP_ENV=development
```

Testing

```text
APP_ENV=test
```

Production

```text
APP_ENV=production
```

Same code.

Different behavior.

______________________________________________________________________

# Feature Flags

Suppose

```text
ENABLE_CACHE

↓

true
```

Python

```python
import os

cache_enabled = (
    os.getenv(
        "ENABLE_CACHE",
        "false"
    ).lower() == "true"
)
```

Now

features can be enabled

without changing code.

______________________________________________________________________

# Twelve-Factor App

One of the principles of the Twelve-Factor App methodology is:

```text
Configuration

↓

Environment
```

Configuration should live outside the application code.

______________________________________________________________________

# Production Secrets

Large companies typically use dedicated secret-management systems.

Examples include

- Kubernetes Secrets
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager

These provide stronger security and access control than plain environment variables.

We'll revisit this later when we learn Kubernetes.

______________________________________________________________________

# Inspecting Environment Variables

Inside a running container

```bash
env
```

or

```bash
printenv
```

Displays

all environment variables.

Be careful not to expose sensitive values in logs or screenshots.

______________________________________________________________________

# Common Mistakes

### Hardcoding Passwords

Never commit secrets into source code.

______________________________________________________________________

### Storing Secrets in Dockerfiles

Images may be shared.

Keep secrets out of images.

______________________________________________________________________

### Committing `.env`

Usually

```text
.env
```

should be added to

```text
.gitignore
```

unless it intentionally contains only non-sensitive defaults.

______________________________________________________________________

### Logging Secrets

Avoid printing passwords,

tokens,

or API keys.

______________________________________________________________________

# Best Practices

- Read configuration from environment variables.
- Keep code environment-independent.
- Don't hardcode secrets.
- Use `.env` for local development.
- Ignore sensitive `.env` files in Git.
- Use dedicated secret-management solutions in production.

______________________________________________________________________

# Hands-on Exercise

1. Replace hardcoded configuration with environment variables.
1. Create a `.env` file.
1. Read values using `os.getenv()`.
1. Run the application with Docker environment variables.
1. Add `.env` to `.gitignore`.
1. Add a feature flag using an environment variable.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why should applications use environment variables instead of hardcoded configuration values?

Environment variables separate configuration from application code. The same application image can run in development,
testing, and production with different configuration values without modifying or rebuilding the code. This improves
portability, security, and deployment flexibility while reducing the risk of exposing sensitive information in source
code.

______________________________________________________________________

# Summary

In this chapter, you learned:

- Environment variables
- Runtime configuration
- Reading variables in Python
- Passing variables to Docker
- `.env` files
- Secrets
- Configuration management
- Feature flags
- Twelve-Factor App principles
- Production secret management
- Security best practices

In the next chapter, we'll learn about **Resource Limits & Health Checks**, including CPU limits, memory limits, restart
policies, and how Docker determines whether a container is healthy.

______________________________________________________________________

## Next File

[Resource Limits & Health Checks](9-resource-limits-and-health-checks.md)
