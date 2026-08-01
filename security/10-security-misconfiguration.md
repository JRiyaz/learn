# Security - Part 10

# Security Misconfiguration

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Security Misconfiguration is
- Why it happens
- Common backend misconfigurations
- Secure FastAPI deployment practices
- Secure Docker configurations
- Environment management
- Best practices

______________________________________________________________________

# What is Security Misconfiguration?

Security Misconfiguration occurs when an application, server, database, or infrastructure is configured in an insecure
way.

Unlike SQL Injection or XSS,

the application code may be perfectly correct.

The problem is **how the application is configured**.

______________________________________________________________________

# Why Does It Happen?

Most applications start in development mode.

Example:

```text id="sm1001"
Debug Mode

↓

Open CORS

↓

Default Password

↓

Development Database
```

If these settings accidentally reach production,

they become security vulnerabilities.

______________________________________________________________________

# Real-World Example

Imagine deploying a FastAPI application.

During development,

you enable debugging.

```python id="sm1002"
DEBUG = True
```

Everything works.

Later,

the same configuration reaches production.

Now,

unexpected errors expose internal details to users.

______________________________________________________________________

# Typical Deployment

```text id="sm1003"
Developer

↓

Docker

↓

Cloud

↓

Production
```

Every stage should use secure configuration.

______________________________________________________________________

# Common Misconfiguration 1

## Debug Mode Enabled

Development

```python id="sm1004"
DEBUG = True
```

Production

```python id="sm1005"
DEBUG = False
```

Debug mode often exposes:

- Stack traces
- Environment information
- File paths
- Internal configuration

Attackers can use this information to plan further attacks.

______________________________________________________________________

# Common Misconfiguration 2

## Open CORS

Bad Example

```python id="sm1006"
allow_origins=["*"]
```

This allows requests from every website.

For many public APIs,

this may be acceptable.

For authenticated web applications,

it often isn't.

We'll cover CORS in detail later.

______________________________________________________________________

# Better Configuration

```python id="sm1007"
allow_origins=[
    "https://library.example.com"
]
```

Only trusted origins are allowed.

______________________________________________________________________

# Common Misconfiguration 3

## Default Credentials

Bad Example

```text id="sm1008"
Username

admin

Password

admin
```

or

```text id="sm1009"
postgres

postgres
```

Always change default credentials before deployment.

______________________________________________________________________

# Common Misconfiguration 4

## Exposed Secrets

Bad Example

```python id="sm1010"
DATABASE_PASSWORD = "mypassword"

JWT_SECRET = "secret123"
```

If this code reaches GitHub,

your secrets are exposed.

Instead,

use environment variables.

```python id="sm1011"
import os

JWT_SECRET = os.getenv("JWT_SECRET")
```

______________________________________________________________________

# Common Misconfiguration 5

## Running Containers as Root

Bad Dockerfile

```dockerfile id="sm1012"
FROM python:3.13

USER root
```

If an attacker escapes the application,

they now have root privileges inside the container.

Better

```dockerfile id="sm1013"
RUN useradd appuser

USER appuser
```

Run containers with the least privilege necessary.

______________________________________________________________________

# Common Misconfiguration 6

## Directory Listing

Suppose your web server allows directory browsing.

Example

```text id="sm1014"
/uploads/

↓

photo1.jpg

photo2.jpg

backup.zip
```

Users may discover files that were never intended to be public.

Disable directory listing unless explicitly required.

______________________________________________________________________

# Common Misconfiguration 7

## Unnecessary Services

Suppose your server runs:

```text id="sm1015"
SSH

FTP

Database

Redis

Mail Server

Unused Service
```

Every running service increases the attack surface.

Disable services that are not needed.

______________________________________________________________________

# Common Misconfiguration 8

## Verbose Error Messages

Bad Example

```text id="sm1016"
Database connection failed.

Password: mypassword

Host: 10.0.0.5
```

This reveals sensitive information.

Better

```text id="sm1017"
Internal Server Error
```

Log detailed errors internally,

not in API responses.

______________________________________________________________________

# Secure FastAPI Configuration

Typical production settings

```text id="sm1018"
HTTPS

↓

Debug Disabled

↓

Environment Variables

↓

Secure Headers

↓

Restricted CORS

↓

Authentication

↓

Logging
```

______________________________________________________________________

# Secure Environment Separation

Keep environments separate.

```text id="sm1019"
Development

↓

Testing

↓

Staging

↓

Production
```

Never share:

- Secrets
- Databases
- API keys

between environments.

______________________________________________________________________

# Configuration Management

Store configuration outside your code.

Example

```text id="sm1020"
Application

↓

Environment Variables

↓

Configuration
```

This allows:

- Safer deployments
- Easier secret rotation
- Different settings per environment

______________________________________________________________________

# Defense in Depth

A secure deployment combines:

```text id="sm1021"
Secure Docker

↓

Secure Cloud

↓

HTTPS

↓

Firewall

↓

Authentication

↓

Logging

↓

Monitoring
```

Configuration is one layer,

not the only layer.

______________________________________________________________________

# Best Practices

✅ Disable debug mode in production.

✅ Restrict CORS.

✅ Store secrets securely.

✅ Use HTTPS.

✅ Run containers as non-root users.

✅ Disable unused services.

✅ Hide detailed error messages.

✅ Separate environments.

______________________________________________________________________

# Common Mistakes

### Deploying Development Configuration

Development settings

should never reach production.

______________________________________________________________________

### Committing Secrets

Secrets belong in:

- Environment variables
- Secret managers

not Git.

______________________________________________________________________

### Running Everything as Root

Follow the Principle of Least Privilege.

______________________________________________________________________

### Exposing Internal Errors

Return generic errors to users.

Log detailed information internally.

______________________________________________________________________

### Forgetting Production Reviews

Before deployment,

review every configuration setting.

Many security incidents occur because of incorrect configuration,

not vulnerable code.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| --------------------- | --------------------------------- |
| Debug enabled | Debug disabled |
| `allow_origins=["*"]` | Allow trusted origins |
| Hardcoded secrets | Environment variables |
| Root container | Non-root container |
| Verbose errors | Generic responses + internal logs |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Security Misconfiguration?

Security Misconfiguration occurs when an application or infrastructure is deployed with insecure settings rather than
vulnerable code. Common examples include enabled debug mode, default credentials, overly permissive CORS policies,
exposed secrets, running applications as root, verbose error messages, and unnecessary services. Preventing security
misconfiguration requires secure defaults, environment separation, proper secret management, and regular configuration
reviews.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Security Misconfiguration is
- Common deployment mistakes
- FastAPI production configuration
- Secure Docker configuration
- Environment separation
- Secret management
- Best practices

______________________________________________________________________

# What's Next

[Sensitive Data Exposure](11-sensitive-data-exposure.md)
