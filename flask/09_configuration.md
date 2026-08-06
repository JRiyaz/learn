# Configuration Management

> **Course:** Flask for Backend Engineers
>
> **Module:** 3
>
> **File:** `09_configuration.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Configuration Management is
- Why Configuration Matters
- Flask Configuration System
- Configuration Sources
- Environment Variables
- Configuration Classes
- Development vs Production
- Secrets Management
- Loading Configuration
- Instance Folders
- `.env` Files
- Production Best Practices

______________________________________________________________________

# What is Configuration?

Configuration is the collection of values that control how an application behaves.

Examples

- Debug Mode
- Database URL
- Secret Key
- API Keys
- Redis URL
- Logging Level
- Email Configuration

Instead of hardcoding these values,

they are stored separately from the application code.

______________________________________________________________________

# Why is Configuration Important?

Imagine writing:

```python
DATABASE_URL = "postgres://admin:password@localhost/db"

SECRET_KEY = "my-secret"

DEBUG = True
```

Problems

- Passwords in source code
- Same configuration everywhere
- Difficult deployments
- Security risks

Instead

```
Application

↓

Configuration

↓

Environment Variables
```

______________________________________________________________________

# Twelve-Factor Principle

One of the core principles of modern applications is:

> **Store configuration in the environment.**

This allows the same application code to run in:

- Development
- Testing
- Staging
- Production

Only the configuration changes.

______________________________________________________________________

# Flask Configuration Object

Every Flask application has

```python
app.config
```

Example

```python
app.config["DEBUG"] = True
```

Retrieve value

```python
app.config["DEBUG"]
```

______________________________________________________________________

# Common Configuration Keys

| Key | Purpose |
|------|----------|
| DEBUG | Enable Debug Mode |
| TESTING | Testing Environment |
| SECRET_KEY | Session Security |
| SQLALCHEMY_DATABASE_URI | Database |
| MAX_CONTENT_LENGTH | Upload Limits |
| SESSION_COOKIE_SECURE | Secure Cookies |

______________________________________________________________________

# Configuration Classes

Instead of writing configuration everywhere,

create classes.

```python
class Config:

    DEBUG = False
```

______________________________________________________________________

# Development Configuration

```python
class DevelopmentConfig(Config):

    DEBUG = True

    DATABASE = "dev.db"
```

______________________________________________________________________

# Testing Configuration

```python
class TestingConfig(Config):

    TESTING = True

    DATABASE = "test.db"
```

______________________________________________________________________

# Production Configuration

```python
class ProductionConfig(Config):

    DEBUG = False

    DATABASE = "prod.db"
```

Production should never enable debug mode.

______________________________________________________________________

# Loading Configuration

```python
app.config.from_object(

    DevelopmentConfig
)
```

or

```python
app.config.from_object(

    ProductionConfig
)
```

______________________________________________________________________

# Configuration Flow

```
Application Starts

↓

Load Config Class

↓

Load Environment Variables

↓

Application Ready
```

______________________________________________________________________

# Environment Variables

Instead of

```python
SECRET_KEY = "password123"
```

Use

```bash
export SECRET_KEY=abc123
```

Read

```python
import os

secret = os.getenv(
    "SECRET_KEY"
)
```

______________________________________________________________________

# Why Environment Variables?

Advantages

- No secrets in source code
- Easy deployment
- Different environments
- Better security

______________________________________________________________________

# Using os.environ

```python
import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL"
)
```

Provide defaults when appropriate

```python
DEBUG = os.getenv(
    "DEBUG",
    "False"
)
```

______________________________________________________________________

# Using python-dotenv

Install

```bash
pip install python-dotenv
```

______________________________________________________________________

# .env File

Example

```text
SECRET_KEY=my-secret

DATABASE_URL=postgresql://...

REDIS_URL=redis://localhost

DEBUG=True
```

______________________________________________________________________

# Loading .env

```python
from dotenv import load_dotenv

load_dotenv()
```

Now

```python
os.getenv(
    "SECRET_KEY"
)
```

works.

______________________________________________________________________

# Important Note

`.env`

is excellent for

- Local Development
- Testing

In production,

cloud providers typically inject environment variables directly.

______________________________________________________________________

# Secrets

Never store

```
Database Password

JWT Secret

API Keys

AWS Credentials
```

inside

- Git
- Source Code
- Docker Images

Instead use

- Environment Variables
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

depending on your platform.

______________________________________________________________________

# SECRET_KEY

Flask uses

```
SECRET_KEY
```

for

- Sessions
- CSRF Tokens
- Cookie Signing

Example

```python
SECRET_KEY = os.getenv(
    "SECRET_KEY"
)
```

Never hardcode it.

______________________________________________________________________

# Upload Limits

Prevent users from uploading extremely large files.

```python
app.config[
    "MAX_CONTENT_LENGTH"
] = 10 * 1024 * 1024
```

Maximum

```
10 MB
```

______________________________________________________________________

# Database Configuration

```python
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL"
)
```

Different environments

↓

Different databases.

______________________________________________________________________

# Email Configuration

```python
MAIL_SERVER

MAIL_PORT

MAIL_USERNAME

MAIL_PASSWORD
```

Should all come from configuration.

______________________________________________________________________

# Logging Configuration

Development

```
DEBUG
```

Production

```
WARNING

ERROR
```

Different logging levels improve observability.

______________________________________________________________________

# Instance Folder

Flask supports an

```
instance/
```

directory.

Example

```
project/

│

├── app/

├── instance/

│      config.py

│

└── run.py
```

Useful for machine-specific configuration and local databases.

______________________________________________________________________

# Configuration Hierarchy

Typical order

```
Default Config

↓

Configuration Class

↓

Environment Variables

↓

Runtime Overrides
```

More specific sources override defaults.

______________________________________________________________________

# Production Architecture

```
Git Repository

↓

Application

↓

Environment Variables

↓

Secrets Manager

↓

Production Server
```

Sensitive values never enter version control.

______________________________________________________________________

# Example Production Config

```python
class ProductionConfig:

    DEBUG = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )
```

______________________________________________________________________

# Common Mistakes

❌ Hardcoding passwords

❌ Committing `.env` files to Git

❌ Running production with `DEBUG=True`

❌ Using one configuration for every environment

❌ Storing AWS credentials inside source code

______________________________________________________________________

# Production Best Practices

- Separate configuration from code.
- Use configuration classes.
- Store secrets in environment variables or a secrets manager.
- Never commit `.env` files.
- Disable debug mode in production.
- Keep development and production configurations separate.
- Validate required configuration values during startup.
- Rotate secrets periodically.

______________________________________________________________________

# Interview Deep Dive

### Question

**How should configuration and secrets be managed in a production Flask application?**

### Answer

Production applications should separate configuration from application code.

A common approach is:

1. Store default values in configuration classes.
1. Load environment-specific values using environment variables.
1. Retrieve sensitive information such as database passwords and API keys from a secure secrets manager or injected environment variables.
1. Disable debug mode.
1. Validate required configuration values during startup.
1. Never commit secrets or `.env` files to version control.

This approach improves security, portability, and maintainability.

______________________________________________________________________

# Summary

In this chapter you learned:

- Flask Configuration
- Configuration Classes
- Environment Variables
- `.env` Files
- `python-dotenv`
- Secrets
- Instance Folder
- Production Configuration
- Best Practices

Good configuration management is essential for building secure, portable, and maintainable Flask applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is configuration management?
1. Why should configuration be separated from application code?
1. What is `app.config`?

______________________________________________________________________

## Configuration Classes

4. Why create separate configuration classes?
1. How do you load a configuration class?
1. Why should production and development use different configurations?

______________________________________________________________________

## Environment Variables

7. Why are environment variables preferred for secrets?
1. How do you read an environment variable in Python?
1. What is the purpose of `python-dotenv`?

______________________________________________________________________

## Security

10. Why should `.env` files not be committed to Git?
01. Why must `SECRET_KEY` remain secret?
01. Where should production secrets be stored?

______________________________________________________________________

## Production

13. Why should `DEBUG=False` in production?
01. Why should upload size limits be configured?
01. What is the purpose of the Flask `instance/` folder?

______________________________________________________________________

## Scenario-Based

16. A developer accidentally commits the `.env` file containing database credentials to GitHub. What steps should the team take immediately?
01. Your production application crashes because `DATABASE_URL` is missing. How would you design startup validation to detect this earlier?
01. Your team currently uses the same database for development, testing, and production. What problems can this cause, and how would you redesign the configuration?
01. A new developer hardcodes AWS credentials directly into the Flask source code. Why is this dangerous, and what alternatives should be used?
01. Your application is deployed to Docker, Kubernetes, and AWS ECS. How can environment variables help keep the application portable across all three environments?

______________________________________________________________________

# Next

[Database Integration with SQLAlchemy](10_database_sqlalchemy.md)
