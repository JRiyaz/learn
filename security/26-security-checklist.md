# Security - Part 26

# Security Checklist & Interview Revision

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll have:

- A complete backend security checklist
- A deployment security checklist
- A FastAPI security checklist
- Common interview questions
- A quick revision guide
- A production-ready mindset

______________________________________________________________________

# Why Do We Need a Security Checklist?

Security isn't one feature.

It is a collection of good practices applied throughout your application.

Before every deployment, ask yourself:

> "Did I verify the security of my application?"

A checklist helps ensure nothing important is forgotten.

______________________________________________________________________

# Authentication Checklist

✅ Passwords are hashed using bcrypt or Argon2.

✅ JWT tokens have expiration times.

✅ Refresh tokens are rotated.

✅ Strong password policies are enforced.

✅ Rate limiting is enabled on login endpoints.

✅ Generic error messages are returned during authentication.

✅ HTTPS is used for login requests.

______________________________________________________________________

# Authorization Checklist

✅ Every protected endpoint verifies authorization.

✅ Role-Based Access Control (RBAC) is implemented where needed.

✅ Resource ownership is validated.

✅ Users cannot access another user's data.

✅ Administrative endpoints require administrator privileges.

______________________________________________________________________

# API Security Checklist

✅ HTTPS enabled.

✅ Request validation using Pydantic.

✅ Response models prevent data leakage.

✅ Rate limiting enabled.

✅ Pagination implemented for large collections.

✅ Proper HTTP status codes returned.

✅ Versioning strategy defined.

______________________________________________________________________

# Database Security Checklist

✅ Parameterized queries or ORM used.

✅ SQL Injection prevented.

✅ Database credentials stored securely.

✅ Database backups encrypted.

✅ Least privilege database accounts.

______________________________________________________________________

# Secret Management Checklist

✅ No secrets committed to Git.

✅ `.env` excluded using `.gitignore`.

✅ Environment variables used.

✅ Secrets rotated periodically.

✅ Production uses a secret manager.

______________________________________________________________________

# Docker Checklist

✅ Non-root user.

✅ Minimal base image.

✅ Multi-stage builds.

✅ `.dockerignore` configured.

✅ No secrets inside Docker image.

✅ Image scanned before deployment.

______________________________________________________________________

# Logging Checklist

✅ Authentication failures logged.

✅ Authorization failures logged.

✅ Exceptions logged.

✅ Correlation IDs used.

✅ No passwords or tokens in logs.

✅ Monitoring and alerts configured.

______________________________________________________________________

# File Upload Checklist

✅ File size limits enforced.

✅ File types validated.

✅ Content validation performed.

✅ Malware scanning enabled (if applicable).

✅ Random filenames generated.

✅ Files stored outside the web root.

______________________________________________________________________

# Infrastructure Checklist

✅ HTTPS configured.

✅ HSTS enabled.

✅ Reverse proxy configured.

✅ Firewall configured.

✅ TLS certificates valid.

✅ Servers regularly updated.

______________________________________________________________________

# Dependency Checklist

✅ Dependency versions pinned.

✅ `pip-audit` executed regularly.

✅ Dependabot enabled.

✅ Unused packages removed.

______________________________________________________________________

# Common Security Mistakes

Avoid these:

❌ Trusting user input

❌ Returning database models directly

❌ Logging passwords

❌ Hardcoding secrets

❌ Running Docker containers as root

❌ Using `shell=True`

❌ Ignoring dependency updates

❌ Allowing unlimited requests

❌ Disabling authentication for testing and forgetting to restore it

______________________________________________________________________

# Security Layers

Think of security as multiple layers.

```text id="sc2601"
HTTPS

↓

Authentication

↓

Authorization

↓

Validation

↓

Rate Limiting

↓

Business Logic

↓

Logging

↓

Monitoring
```

If one layer fails,

another layer still provides protection.

This concept is called

**Defense in Depth**.

______________________________________________________________________

# Secure FastAPI Request Lifecycle

```text id="sc2602"
Client

↓

HTTPS

↓

Rate Limiting

↓

Authentication

↓

Authorization

↓

Input Validation

↓

Business Logic

↓

Database

↓

Response Model

↓

Logging

↓

Response
```

This is a good mental model

for every production API.

______________________________________________________________________

# Top Interview Questions

Here are some of the most common backend security interview questions.

______________________________________________________________________

## Authentication

- What is the difference between Authentication and Authorization?
- Why shouldn't passwords be encrypted?
- Why is bcrypt preferred over SHA256?
- What is JWT?
- What is OAuth2?
- What is RBAC?

______________________________________________________________________

## API Security

- What is Rate Limiting?
- What is CORS?
- Why doesn't CORS secure an API?
- What is SSRF?
- What is IDOR?
- What is Path Traversal?

______________________________________________________________________

## OWASP

- Explain SQL Injection.
- Explain XSS.
- Explain CSRF.
- Explain Broken Authentication.
- Explain Broken Access Control.
- Explain Security Misconfiguration.
- Explain Sensitive Data Exposure.

______________________________________________________________________

## Infrastructure

- Why should Docker containers run as non-root users?
- What is HTTPS?
- What is TLS?
- What is HSTS?
- What are environment variables?

______________________________________________________________________

# How to Answer Security Questions

A good interview answer usually follows this structure:

```text id="sc2603"
1. Define the vulnerability

↓

2. Explain how it happens

↓

3. Explain the impact

↓

4. Explain the prevention
```

Example:

**Question:** What is SQL Injection?

1. It is a vulnerability where user input changes the intended SQL query.
1. It happens when applications concatenate SQL strings.
1. Attackers may read, modify, or delete database data.
1. Prevent it using parameterized queries, ORM frameworks, input validation, and least-privilege database accounts.

This structure works for almost every security topic.

______________________________________________________________________

# Real-World Advice

As a backend developer:

- Assume every user input is untrusted.
- Validate everything.
- Authenticate before authorizing.
- Keep secrets outside your code.
- Keep dependencies updated.
- Never expose internal errors.
- Review logs regularly.
- Think about security during development, not after deployment.

Security is not a one-time task—it is part of the software development lifecycle.

______________________________________________________________________

# Final Revision Sheet

Remember these principles:

- Never trust user input.
- Validate all requests.
- Use HTTPS.
- Hash passwords.
- Store secrets securely.
- Authorize every protected request.
- Return only necessary data.
- Log important events, not secrets.
- Rate limit sensitive endpoints.
- Keep dependencies updated.
- Follow the Principle of Least Privilege.
- Apply Defense in Depth.

If you consistently follow these practices, you'll avoid many common security vulnerabilities.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** As a backend developer, what are the most important security principles you follow?

I follow a defense-in-depth approach. I validate all user input, use HTTPS for secure communication, hash passwords with
bcrypt or Argon2, implement authentication and authorization on every protected endpoint, store secrets outside the
codebase, prevent SQL Injection using parameterized queries or ORMs, protect APIs with rate limiting, avoid exposing
sensitive information in logs or responses, keep dependencies updated, and apply the Principle of Least Privilege
throughout the application and infrastructure.

______________________________________________________________________

# Congratulations!

You've completed the **Security** module.

You now understand:

- OWASP Top 10
- Authentication & Authorization
- JWT & OAuth2
- Secure API Design
- Docker Security
- Secrets Management
- HTTPS & TLS
- Rate Limiting
- Logging & Monitoring
- Dependency Security
- File Upload Security
- Common backend vulnerabilities
- Production security practices

This foundation is more than enough for most Python/FastAPI backend engineering interviews and day-to-day development.

______________________________________________________________________

# What's Next

[Principle of Least Privilege](27.principle-of-least-privilege.md)
