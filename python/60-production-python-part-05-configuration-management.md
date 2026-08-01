# File: python/60-production-python-part-05-configuration-management.md

# Production Python

# Part 5: Configuration Management – Building Configurable and Deployable Applications

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 60
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 10–12 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why configuration management is important
- Configuration vs code
- Configuration sources
- The Twelve-Factor App principle
- Configuration precedence
- Centralised configuration
- Application settings
- Secrets management
- Configuration validation
- Configuration for different environments
- Production best practices
- questions

______________________________________________________________________

# Recap

Imagine your application contains:

```python
DATABASE_URL = "postgresql://admin:password@localhost:5432/shop"

REDIS_URL = "redis://localhost:6379"

DEBUG = True
```

This works during development.

But what happens when you deploy the application?

Production uses:

- Different databases
- Different Redis servers
- Different API keys
- Different logging levels

Changing the source code for every deployment is not practical.

This is where configuration management becomes essential.

______________________________________________________________________

# What is Configuration?

Configuration is **data that changes between deployments without changing application logic**.

Examples include:

- Database connection strings
- API keys
- Logging levels
- Cache configuration
- Feature flags
- Service endpoints
- Timeouts
- Ports

Your application code should remain the same while configuration changes.

______________________________________________________________________

# Code vs Configuration

Bad

```python
DEBUG = True

DATABASE = "localhost"

API_KEY = "abc123"
```

Good

```python
DEBUG = config.debug

DATABASE = config.database_url

API_KEY = config.api_key
```

Notice that the application reads configuration instead of hardcoding it.

______________________________________________________________________

# Why Separate Configuration?

Suppose your company has three environments:

```text
Development

↓

Testing

↓

Production
```

Only the configuration should change.

The application code should remain identical.

Benefits include:

- Easier deployments
- Fewer mistakes
- Better security
- Simpler automation

______________________________________________________________________

# The Twelve-Factor App

One of the most influential principles in modern backend development is the **Twelve-Factor App**.

One of its key recommendations is:

> **Store configuration in the environment.**

This allows the same application artifact to be deployed across multiple environments with different settings.

______________________________________________________________________

# Configuration Sources

Applications can load configuration from several sources.

Common sources include:

```text
Environment Variables

↓

Configuration Files

↓

Command-Line Arguments

↓

Secret Managers

↓

Default Values
```

Production applications often combine several of these.

______________________________________________________________________

# Configuration Precedence

When multiple configuration sources exist, define a clear order of precedence.

Example:

```text
Command-Line Arguments

↓

Environment Variables

↓

Configuration File

↓

Application Defaults
```

The first available value wins.

Having a predictable precedence prevents unexpected behaviour.

______________________________________________________________________

# Centralised Configuration

Avoid scattering configuration throughout your codebase.

Bad

```python
# database.py

TIMEOUT = 30
```

```python
# cache.py

TIMEOUT = 60
```

```python
# api.py

TIMEOUT = 15
```

Instead:

```text
config.py
```

contains all application settings.

Other modules import from a single source.

______________________________________________________________________

# Example Configuration Class

```python
import os


class Config:

    APP_NAME = "BookStore"

    DEBUG = os.getenv("DEBUG", "False") == "True"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///books.db"
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379"
    )
```

Every module reads from this class rather than accessing environment variables directly.

______________________________________________________________________

# Configuration Validation

Configuration is user input.

It should be validated.

Bad:

```python
PORT = int(os.getenv("PORT"))
```

If `PORT` is missing or invalid:

```text
ValueError
```

Better:

```python
port = os.getenv("PORT")

if port is None:
    raise RuntimeError(
        "PORT environment variable is required."
    )

PORT = int(port)
```

Fail fast during startup rather than after deployment.

______________________________________________________________________

# Development vs Production

Consider:

```text
Development

DEBUG=True
```

```text
Production

DEBUG=False
```

Other examples:

| Setting | Development | Production |
|----------|-------------|------------|
| Database | Local | Managed PostgreSQL |
| Logging | Console | Centralised logging |
| Cache | Optional | Redis Cluster |
| Secrets | Local | Secret Manager |

The application code is identical.

Only configuration changes.

______________________________________________________________________

# Secrets Are Configuration

Examples of secrets:

- Database passwords
- JWT signing keys
- OAuth client secrets
- Cloud credentials
- Encryption keys

Never hardcode them.

Never commit them to Git.

Treat secrets differently from normal configuration.

______________________________________________________________________

# Configuration Caching

Reading configuration repeatedly is inefficient.

Instead:

```
Application Starts

↓

Load Configuration

↓

Validate

↓

Store in Memory

↓

Use Throughout Application
```

Most applications load configuration once during startup.

______________________________________________________________________

# Feature Flags

Configuration can control behaviour.

Example:

```python
ENABLE_NEW_CHECKOUT = False
```

Changing configuration enables or disables features without modifying code.

This allows safer deployments and gradual rollouts.

______________________________________________________________________

# Backend Example

Imagine a FastAPI service.

```
Application Startup

↓

Load Config

↓

Validate Config

↓

Connect Database

↓

Connect Redis

↓

Start HTTP Server
```

If required configuration is missing:

```
Startup Fails

↓

Error Logged

↓

Application Exits
```

This is preferable to discovering configuration errors after serving requests.

______________________________________________________________________

# Configuration Anti-Patterns

## Hardcoded Values

```python
DATABASE_URL = "localhost"
```

______________________________________________________________________

## Reading Environment Variables Everywhere

Bad

```python
os.getenv(...)
```

in dozens of files.

Read once.

Expose through a configuration object.

______________________________________________________________________

## Hidden Defaults

Unexpected defaults can hide deployment mistakes.

For critical settings,

prefer failing fast.

______________________________________________________________________

## Configuration Duplication

Avoid copying the same configuration value into multiple modules.

Maintain a single source of truth.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Hardcoding secrets.

______________________________________________________________________

## Mistake 2

Mixing configuration with business logic.

______________________________________________________________________

## Mistake 3

Not validating configuration.

______________________________________________________________________

## Mistake 4

Reading environment variables throughout the codebase.

______________________________________________________________________

## Mistake 5

Using different configuration mechanisms for different modules.

______________________________________________________________________

# Best Practices

✅ Separate configuration from code.

✅ Load configuration during startup.

✅ Validate required settings.

✅ Use a single configuration object.

✅ Define clear precedence rules.

✅ Fail fast on invalid configuration.

❌ Never commit secrets to version control.

❌ Don't scatter configuration across the application.

______________________________________________________________________

# Production Insight

Configuration management is a key part of cloud-native application design.

Whether deploying to:

- Docker
- Kubernetes
- AWS
- Azure
- Google Cloud

the application image should remain unchanged.

Only configuration differs between deployments.

This principle enables repeatable, reliable deployments and supports modern CI/CD pipelines.

______________________________________________________________________

# Questions

### Question

> Why should configuration be separated from code?

### Answer

Because configuration changes between deployments, while application logic should remain the same.

______________________________________________________________________

### Question

> What is the purpose of configuration validation?

### Answer

To detect invalid or missing settings during application startup instead of failing later during runtime.

______________________________________________________________________

### Question

> Why centralise configuration?

### Answer

It creates a single source of truth, simplifies maintenance, and prevents inconsistent behaviour across modules.

______________________________________________________________________

### Question

> Why are secrets treated differently from other configuration?

### Answer

Because exposing secrets can compromise application security and user data.

______________________________________________________________________

### Question

> Why should applications fail fast on invalid configuration?

### Answer

Because configuration errors are deployment problems that should be detected before the application begins serving
requests.

______________________________________________________________________

# Practical Lesson

Create:

```text
config.py
```

Implement:

- A `Config` class.
- Database URL.
- Redis URL.
- Debug mode.
- Application name.
- Port number.

Load values using `os.getenv()`.

Validate required settings during startup.

Then update another module to consume the configuration object instead of calling `os.getenv()` directly.

______________________________________________________________________

# Questions

## Question 1

What is configuration management?

### Answer

It is the practice of separating deployment-specific settings from application code so the same application can run in
multiple environments.

______________________________________________________________________

## Question 2

Why should configuration be loaded once during startup?

### Answer

Loading once avoids repeated lookups, ensures consistent values, and allows validation before the application begins
handling requests.

______________________________________________________________________

## Question 3

What is configuration precedence?

### Answer

It defines which configuration source takes priority when the same setting exists in multiple places.

______________________________________________________________________

## Question 4

Why should secrets never be hardcoded?

### Answer

Hardcoded secrets are difficult to rotate, can leak through source control, and create significant security risks.

______________________________________________________________________

## Question 5

How does configuration management support CI/CD?

### Answer

It allows the same application artifact to be deployed across environments, with only configuration changing between
deployments.

______________________________________________________________________

# Assignment

## Exercise 1

Refactor one of your Flask or FastAPI projects to use a single configuration class.

______________________________________________________________________

## Exercise 2

Identify every hardcoded configuration value in one of your projects.

Move each into the configuration layer.

______________________________________________________________________

## Exercise 3

Implement configuration validation that prevents application startup if required settings are missing.

______________________________________________________________________

## Exercise 4

Document the configuration required for one of your backend services.

Categorise each setting as:

- Required
- Optional
- Secret
- Environment-specific

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ What configuration management is.
- ✅ Why configuration should be separated from code.
- ✅ Common configuration sources.
- ✅ Configuration precedence.
- ✅ Centralised configuration.
- ✅ Validation strategies.
- ✅ Secrets management principles.
- ✅ Production configuration best practices.

______________________________________________________________________

# Next Lesson

**File:** [61-production-python-part-06-environment-variables](61-production-python-part-06-environment-variables.md)
