# Security - Part 24

# Dependency Security

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why dependency security matters
- Supply Chain Attacks
- Vulnerable dependencies
- Dependency confusion
- Dependency scanning
- Python dependency management
- Tools for auditing dependencies
- Best practices

______________________________________________________________________

# Why Should We Care About Dependencies?

Modern Python applications rely heavily on third-party packages.

A typical FastAPI project may use:

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Redis
- Alembic
- Celery
- Requests
- Cryptography

Your application may contain only 10,000 lines of code,

but it could depend on **hundreds of thousands of lines** written by others.

If one dependency is vulnerable,

your application may also become vulnerable.

______________________________________________________________________

# What is a Dependency?

A dependency is a library your application uses.

Example

```text id="dep2401"
FastAPI

↓

Uses Pydantic

↓

Uses typing libraries

↓

Uses many other packages
```

Dependencies themselves often depend on other libraries.

These are called

**transitive dependencies**.

______________________________________________________________________

# Typical Dependency Chain

```text id="dep2402"
Your Application

↓

FastAPI

↓

Starlette

↓

AnyIO

↓

Other Libraries
```

You may never install some libraries directly,

but they're still part of your application.

______________________________________________________________________

# Common Risk 1

## Vulnerable Packages

Suppose

your application uses:

```text id="dep2403"
package-x v1.0
```

Later,

a serious security vulnerability is discovered.

Your application remains vulnerable

until you upgrade.

______________________________________________________________________

# Common Risk 2

## Supply Chain Attacks

Instead of attacking

your application directly,

an attacker compromises

a dependency.

Workflow

```text id="dep2404"
Attacker

↓

Dependency

↓

Your Application
```

If your application installs

the compromised dependency,

the attack spreads.

This is called a

**Supply Chain Attack**.

______________________________________________________________________

# Common Risk 3

## Dependency Confusion

Imagine your company has

an internal package

called

```text id="dep2405"
company-utils
```

An attacker publishes

a public package

with the same name.

If your package manager

downloads the wrong package,

malicious code could enter your application.

This is known as

**Dependency Confusion**.

______________________________________________________________________

# Common Risk 4

## Installing Untrusted Packages

Suppose you search

PyPI

for a package.

Several packages

have similar names.

Choosing the wrong package

may introduce malicious code.

Always verify:

- Package name
- Author
- Popularity
- Maintenance
- Official documentation

______________________________________________________________________

# Pin Dependency Versions

Bad

```text id="dep2406"
fastapi
```

Good

```text id="dep2407"
fastapi==0.116.1
```

Version pinning helps ensure

every deployment

uses the same tested version.

______________________________________________________________________

# Dependency Auditing

Python provides tools

to scan dependencies

for known vulnerabilities.

Example

```bash id="dep2408"
pip-audit
```

Run

```bash id="dep2409"
pip-audit
```

Output

```text id="dep2410"
Package

↓

Known Vulnerability

↓

Recommended Upgrade
```

Fix the reported issues

as soon as practical.

______________________________________________________________________

# Safety

Another tool is

```text id="dep2411"
Safety
```

Example

```bash id="dep2412"
safety check
```

It compares installed packages

against known vulnerability databases.

______________________________________________________________________

# Dependabot

If your code is hosted on GitHub,

enable

```text id="dep2413"
Dependabot
```

Dependabot automatically:

- Detects vulnerable packages
- Creates upgrade Pull Requests
- Alerts you to security issues

This is highly recommended

for production projects.

______________________________________________________________________

# Updating Dependencies

Avoid two extremes.

❌ Never updating dependencies.

❌ Updating everything blindly.

Instead,

follow this process.

```text id="dep2414"
Read Release Notes

↓

Update

↓

Run Tests

↓

Deploy
```

Always verify

that updates

do not break your application.

______________________________________________________________________

# Lock Files

Use dependency lock files

to ensure consistent installations.

Examples:

```text id="dep2415"
requirements.txt

poetry.lock

uv.lock
```

Every environment

should install

the same dependency versions.

______________________________________________________________________

# Minimal Dependencies

Ask yourself:

> Do I really need this package?

Every dependency increases:

- Attack surface
- Maintenance effort
- Update frequency

Sometimes,

the Python standard library

is sufficient.

______________________________________________________________________

# Secure CI/CD Workflow

A secure pipeline

should include

dependency scanning.

```text id="dep2416"
Developer

↓

Commit

↓

Dependency Scan

↓

Tests

↓

Deploy
```

If vulnerabilities are found,

the deployment can be blocked

until they are addressed.

______________________________________________________________________

# Defense in Depth

Secure dependency management includes:

```text id="dep2417"
Trusted Packages

↓

Pinned Versions

↓

Dependency Scan

↓

Automated Updates

↓

Testing
```

______________________________________________________________________

# Best Practices

✅ Install packages from trusted sources.

✅ Pin dependency versions.

✅ Run `pip-audit` regularly.

✅ Enable Dependabot.

✅ Remove unused dependencies.

✅ Read release notes before upgrading.

✅ Scan dependencies in CI/CD.

______________________________________________________________________

# Common Mistakes

### Installing Random Packages

Always verify

the package

before installing it.

______________________________________________________________________

### Never Updating Dependencies

Old packages

may contain

known vulnerabilities.

______________________________________________________________________

### Updating Everything in Production

Test updates

before deployment.

______________________________________________________________________

### Ignoring Security Warnings

Dependency scanners

exist for a reason.

Review and fix reported issues.

______________________________________________________________________

### Adding Unnecessary Libraries

Every dependency

introduces additional risk.

Use only what you need.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ----------------- | -------------------- |
| Unpinned versions | Pinned versions |
| No auditing | `pip-audit` / Safety |
| Ignore updates | Regular review |
| Unknown packages | Trusted packages |
| Manual tracking | Dependabot |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is dependency security important in backend applications?

Modern backend applications depend on many third-party libraries. A vulnerability in any dependency can affect the
security of the entire application. Developers should install packages only from trusted sources, pin dependency
versions, regularly scan for known vulnerabilities using tools such as `pip-audit`, enable automated update tools like
Dependabot, and test dependency updates before deploying them to production.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Dependency security
- Supply chain attacks
- Dependency confusion
- Version pinning
- `pip-audit`
- Safety
- Dependabot
- CI/CD scanning
- Best practices

______________________________________________________________________

# What's Next

[Secure Docker Containers](25-secure-docker-containers.md)
