# Security - Part 21

# Secrets Management

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What secrets are
- Why secrets management is important
- Common mistakes developers make
- Environment variables
- `.env` files
- Docker Secrets
- Cloud Secret Managers
- Secret rotation
- FastAPI best practices

______________________________________________________________________

# What is a Secret?

A **secret** is any piece of information that should be known only to authorized systems or people.

Examples:

- Database passwords
- JWT secret keys
- API keys
- OAuth client secrets
- Encryption keys
- AWS access keys
- SMTP passwords
- Redis passwords

If an attacker gets access to a secret,

they may gain access to your infrastructure.

______________________________________________________________________

# Why Secrets Matter

Imagine your application connects to PostgreSQL.

```text id="sec2101"
FastAPI

↓

Database Password

↓

PostgreSQL
```

If someone steals that password,

they may gain access to your database.

The application code might be perfectly secure,

but the exposed secret compromises everything.

______________________________________________________________________

# Common Mistake 1

## Hardcoding Secrets

Bad Example

```python id="sec2102"
DATABASE_PASSWORD = "mypassword"

JWT_SECRET = "mysecret"

API_KEY = "abcdef123456"
```

Problems:

- Visible in source code
- Easy to accidentally commit
- Difficult to rotate
- Shared across environments

Never hardcode secrets.

______________________________________________________________________

# Better Solution

Use environment variables.

```python id="sec2103"
import os

DATABASE_PASSWORD = os.getenv(
    "DATABASE_PASSWORD"
)

JWT_SECRET = os.getenv(
    "JWT_SECRET"
)
```

Now,

the secret lives outside

your application code.

______________________________________________________________________

# Environment Variables

Environment variables

allow the operating system

to provide configuration.

```text id="sec2104"
Operating System

↓

Environment Variables

↓

FastAPI
```

Different environments

can use different values.

Example

```text id="sec2105"
Development

↓

JWT_SECRET=dev-secret

Production

↓

JWT_SECRET=random-production-secret
```

______________________________________________________________________

# `.env` Files

During development,

many projects use

```text id="sec2106"
.env
```

Example

```text id="sec2107"
DATABASE_URL=postgresql://...

JWT_SECRET=...

REDIS_PASSWORD=...
```

Python example

```python id="sec2108"
from dotenv import load_dotenv

load_dotenv()
```

______________________________________________________________________

# Important Rule

`.env`

is for **local development**.

Never commit it.

Always add it to

```text id="sec2109"
.gitignore
```

Example

```text id="sec2110"
.env

.env.local

.env.production
```

______________________________________________________________________

# Common Mistake 2

## Committing Secrets to Git

Suppose you accidentally commit:

```text id="sec2111"
JWT_SECRET

DATABASE_PASSWORD

AWS_SECRET_ACCESS_KEY
```

Even if you delete them later,

they remain

in Git history.

Assume any committed secret

is compromised.

Rotate it immediately.

______________________________________________________________________

# Secret Rotation

Sometimes,

a secret must be replaced.

Examples:

- Employee leaves the company
- Secret accidentally exposed
- Routine security maintenance

Workflow

```text id="sec2112"
Old Secret

↓

Generate New Secret

↓

Update Applications

↓

Remove Old Secret
```

This is called

**Secret Rotation**.

______________________________________________________________________

# Docker Secrets

When deploying containers,

avoid passing secrets

inside the Docker image.

Instead,

use

```text id="sec2113"
Docker Secrets
```

Workflow

```text id="sec2114"
Docker Secret

↓

Container

↓

Application
```

The secret exists

outside the image,

making it easier to manage securely.

______________________________________________________________________

# Cloud Secret Managers

Production systems

often use dedicated services.

Examples:

- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- HashiCorp Vault

Workflow

```text id="sec2115"
Application

↓

Secret Manager

↓

Retrieve Secret

↓

Use Secret
```

Advantages:

- Encryption
- Access control
- Audit logs
- Automatic rotation
- Centralized management

______________________________________________________________________

# FastAPI Configuration Example

Instead of

```python id="sec2116"
SECRET_KEY = "secret123"
```

Use

```python id="sec2117"
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str
    database_url: str

settings = Settings()
```

Now,

FastAPI reads configuration

from the environment,

keeping secrets out of the codebase.

______________________________________________________________________

# Least Privilege

Even secrets

should have limited permissions.

Example

Instead of one database account

with full administrator access,

create separate accounts.

```text id="sec2118"
Application

↓

Read / Write

↓

Cannot Drop Database
```

If the application credentials leak,

the attacker has limited capabilities.

______________________________________________________________________

# Secret Lifecycle

A secret should have a lifecycle.

```text id="sec2119"
Generate

↓

Store

↓

Use

↓

Rotate

↓

Revoke

↓

Delete
```

Managing secrets properly

is an ongoing process,

not a one-time task.

______________________________________________________________________

# Defense in Depth

Secure secret management combines:

```text id="sec2120"
Environment Variables

↓

Secret Manager

↓

Least Privilege

↓

Rotation

↓

Audit Logging
```

______________________________________________________________________

# Best Practices

✅ Never hardcode secrets.

✅ Use environment variables.

✅ Add `.env` to `.gitignore`.

✅ Rotate secrets regularly.

✅ Use cloud secret managers in production.

✅ Limit permissions associated with secrets.

✅ Audit secret usage.

______________________________________________________________________

# Common Mistakes

### Hardcoding Credentials

Secrets should never appear

in application code.

______________________________________________________________________

### Committing `.env`

Treat `.env`

as sensitive.

Never push it to Git.

______________________________________________________________________

### Reusing Secrets Everywhere

Different environments

should have different secrets.

Development,

testing,

and production

should never share credentials.

______________________________________________________________________

### Never Rotating Secrets

Secrets should be replaced periodically,

especially after suspected exposure.

______________________________________________________________________

### Using One Database User for Everything

Follow the Principle of Least Privilege.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------------- | ------------------------------------ |
| Hardcoded secrets | Environment variables |
| Secrets in Git | `.gitignore` + Secret Manager |
| One secret forever | Secret rotation |
| Shared credentials | Separate credentials per environment |
| Full database permissions | Least privilege |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Secrets Management, and why is it important?

Secrets Management is the practice of securely storing, accessing, rotating, and monitoring sensitive credentials such
as API keys, passwords, JWT secrets, and encryption keys. Proper secrets management prevents accidental exposure,
simplifies credential rotation, improves auditability, and reduces the impact of compromised credentials. In production,
secrets should be stored outside the application code using environment variables or dedicated secret management
services.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What secrets are
- Why secrets management matters
- Environment variables
- `.env` files
- Docker Secrets
- Cloud Secret Managers
- Secret rotation
- FastAPI configuration
- Best practices

______________________________________________________________________

# What's Next

[Rate Limiting](22-rate-limiting.md)
