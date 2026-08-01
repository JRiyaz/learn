# File: python/61-production-python-part-06-environment-variables.md

# Production Python

# Part 6: Environment Variables – Secure and Flexible Application Configuration

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 61
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What environment variables are
- Why they are used
- How operating systems expose them
- Reading environment variables in Python
- Default values
- Required variables
- Environment variables in Docker
- Environment variables in Kubernetes
- Managing secrets
- Common mistakes
- Production best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned that configuration should be separated from application code.

One of the most common ways to provide configuration is through **environment variables**.

Instead of changing source code for every deployment:

```python
DATABASE_URL = "postgresql://localhost/shop"
```

we allow the operating system to provide the value.

______________________________________________________________________

# What is an Environment Variable?

An environment variable is a **key-value pair** maintained by the operating system and inherited by a process when it
starts.

Example:

```text
DATABASE_URL=postgresql://db:5432/shop
```

Your Python application simply reads this value.

______________________________________________________________________

# Why Use Environment Variables?

They allow the same application to run in different environments without modifying code.

Example:

| Environment | DATABASE_URL |
|-------------|--------------|
| Development | Local PostgreSQL |
| Testing | Test Database |
| Production | Managed PostgreSQL Cluster |

The application code never changes.

______________________________________________________________________

# Accessing Environment Variables

Python provides the `os` module.

```python
import os

database_url = os.getenv("DATABASE_URL")
```

If the variable exists, its value is returned.

Otherwise:

```python
None
```

is returned.

______________________________________________________________________

# Providing Default Values

Sometimes a sensible default is acceptable.

```python
import os

port = os.getenv("PORT", "8000")
```

If `PORT` is missing:

```text
8000
```

is used.

Use defaults only when appropriate.

______________________________________________________________________

# Required Variables

Some configuration is mandatory.

Example:

```python
import os

secret = os.getenv("SECRET_KEY")

if secret is None:

    raise RuntimeError(

        "SECRET_KEY is required."

    )
```

Fail during startup rather than after serving requests.

______________________________________________________________________

# Environment Variables are Strings

Every environment variable is initially read as a string.

```python
workers = os.getenv("WORKERS", "4")
```

To use it as an integer:

```python
workers = int(workers)
```

Likewise:

```python
timeout = float(
    os.getenv("TIMEOUT", "5.0")
)
```

Always validate conversions.

______________________________________________________________________

# Boolean Values

A common mistake:

```python
DEBUG = bool(
    os.getenv("DEBUG")
)
```

This is incorrect.

Even:

```text
False
```

is a non-empty string and evaluates to:

```python
True
```

A safer approach:

```python
DEBUG = (
    os.getenv("DEBUG", "false")
    .lower()
    == "true"
)
```

______________________________________________________________________

# Local Development

During development, developers often create environment variables manually or use tools that load them automatically.

Regardless of how they are provided, the application should always access them through the same configuration layer
rather than scattering `os.getenv()` calls throughout the codebase.

______________________________________________________________________

# Docker

Docker allows environment variables to be injected when a container starts.

```
Container Starts

↓

Environment Variables Injected

↓

Python Reads Values

↓

Application Starts
```

The Docker image remains identical across environments.

______________________________________________________________________

# Kubernetes

Kubernetes commonly provides environment variables from:

- ConfigMaps
- Secrets

This allows operations teams to update deployment configuration without rebuilding the application.

______________________________________________________________________

# Secrets

Environment variables often contain:

- Database passwords
- API keys
- JWT signing keys
- OAuth credentials

Although environment variables are widely used, remember that they are **configuration**, not encryption.

Access should still be restricted and secrets should be managed appropriately.

______________________________________________________________________

# Example Project Structure

```text
app/

├── config.py

├── database.py

├── api.py

└── main.py
```

Only:

```text
config.py
```

should access:

```python
os.getenv()
```

Other modules import configuration from there.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Hardcoding secrets.

______________________________________________________________________

## Mistake 2

Calling `os.getenv()` throughout the project.

______________________________________________________________________

## Mistake 3

Assuming environment variables already have the correct type.

______________________________________________________________________

## Mistake 4

Not validating required configuration.

______________________________________________________________________

## Mistake 5

Depending on hidden defaults for critical settings.

______________________________________________________________________

# Best Practices

✅ Read environment variables once during startup.

✅ Validate all required values.

✅ Convert values to the correct types.

✅ Keep a single configuration module.

✅ Fail fast if critical configuration is missing.

❌ Never commit secrets to source control.

❌ Don't duplicate configuration logic.

______________________________________________________________________

# Production Insight

In modern backend systems, applications are typically built once and deployed many times.

The deployment environment supplies:

- Database connections
- Cache servers
- API endpoints
- Feature flags
- Secrets

This approach enables immutable deployments and reliable CI/CD pipelines.

______________________________________________________________________

# Questions

### Question

> Why are environment variables preferred over hardcoded values?

### Answer

Because they allow configuration to change between environments without modifying or rebuilding the application.

______________________________________________________________________

### Question

> Why should environment variables be read from one place?

### Answer

To create a single source of truth, simplify maintenance, and avoid inconsistent configuration.

______________________________________________________________________

### Question

> Why is validation important?

### Answer

Because environment variables are external input and may be missing, malformed, or contain unexpected values.

______________________________________________________________________

### Question

> Why is `bool(os.getenv(...))` incorrect?

### Answer

Because every non-empty string evaluates to `True`, including the string `"False"`.

______________________________________________________________________

### Question

> Why should secrets never be hardcoded?

### Answer

Because they are difficult to rotate, may leak through version control, and create unnecessary security risks.

______________________________________________________________________

# Practical Lesson

Create:

```text
config.py
```

Implement a configuration class that loads:

- Application name
- Debug mode
- Database URL
- Redis URL
- Worker count
- HTTP port

Validate required settings and convert values to their correct types before the application starts.

______________________________________________________________________

# Knowledge Check

## Question 1

Why are environment variables widely used in cloud deployments?

### Answer

They allow deployment-specific configuration without changing application code or rebuilding deployment artifacts.

______________________________________________________________________

## Question 2

Why should applications fail during startup when required environment variables are missing?

### Answer

Because configuration problems are deployment issues that should be detected before the application begins serving
requests.

______________________________________________________________________

## Question 3

Why should environment variables be converted to appropriate data types?

### Answer

Because operating systems expose them as strings regardless of their intended meaning.

______________________________________________________________________

## Question 4

Why is a central configuration module recommended?

### Answer

It avoids duplicated configuration logic, improves maintainability, and ensures consistent behaviour across the
application.

______________________________________________________________________

## Question 5

What kinds of information are commonly stored in environment variables?

### Answer

Database connection strings, service endpoints, API keys, feature flags, logging configuration, and other
deployment-specific settings.

______________________________________________________________________

# Assignment

## Exercise 1

Move every `os.getenv()` call in one of your projects into a single configuration module.

______________________________________________________________________

## Exercise 2

Implement validation for all required environment variables.

______________________________________________________________________

## Exercise 3

Convert all numeric and boolean environment variables to their appropriate Python types.

______________________________________________________________________

## Exercise 4

Create documentation listing every environment variable your application requires, indicating whether it is:

- Required
- Optional
- Secret
- Environment-specific

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What environment variables are.
- ✅ How Python reads them.
- ✅ Default values.
- ✅ Required configuration.
- ✅ Type conversion.
- ✅ Secret management principles.
- ✅ Production best practices.

______________________________________________________________________

# Next Lesson

**File:** [62-production-python-part-07-virtual-environments](62-production-python-part-07-virtual-environments.md)
