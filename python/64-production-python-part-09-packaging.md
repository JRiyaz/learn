# File: python/63-production-python-part-09-packaging.md

# Production Python
# Part 8: Packaging – Building Installable and Reusable Python Projects

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 63
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

---

# Learning Objectives

By the end of this lesson, you will understand:

- What Python packaging is
- Why packaging exists
- Packages vs distributions
- Modern Python packaging
- `pyproject.toml`
- Build systems
- Installing local packages
- Editable installs
- Source distributions
- Wheels
- Versioning
- Best practices
- Common mistakes

---

# Recap

Virtual environments isolate dependencies.

However, we still have a problem.

Suppose you've written a useful library:

```text
authentication/

├── jwt.py
├── hashing.py
└── permissions.py
```

How do you reuse it in another project?

Copy and paste?

No.

Instead, Python allows applications and libraries to be **packaged**.

---

# What is Packaging?

Packaging is the process of turning Python code into a reusable, installable project.

Instead of:

```
Copy Files

↓

Paste Files

↓

Repeat
```

You simply install the package.

```
pip install my-package
```

---

# Package vs Distribution

These terms are often confused.

A **Python package** is:

```text
my_app/

├── __init__.py
├── users.py
└── orders.py
```

A **distribution** is:

```
A build artifact

↓

Wheel (.whl)

or

Source Distribution (.tar.gz)
```

One is source code.

The other is something that can be installed.

---

# Modern Python Packaging

Today, almost every modern Python project uses:

```text
pyproject.toml
```

This file describes:

- Project metadata
- Dependencies
- Build system
- Optional dependencies
- Tool configuration

It is now the standard entry point for Python packaging.

---

# Example `pyproject.toml`

```toml
[project]
name = "inventory-service"
version = "1.0.0"
description = "Inventory management service"
requires-python = ">=3.11"

dependencies = [
    "fastapi",
    "sqlalchemy",
    "uvicorn"
]
```

This file replaces much of the older packaging configuration that used multiple files.

---

# Build Systems

A build system converts your source code into installable distributions.

Common build backends include:

- Hatchling
- Setuptools
- Flit
- PDM Backend

Your choice of backend does not usually affect how users install your package.

---

# Installing Local Projects

From the project directory:

```bash
pip install .
```

This:

- Builds the package.
- Installs it into the active virtual environment.
- Makes it available like any other installed package.

---

# Editable Installation

During development, repeatedly reinstalling a package becomes inconvenient.

Instead:

```bash
pip install -e .
```

The `-e` means **editable**.

```
Project Source

↓

Editable Install

↓

Python Imports Directly From Source
```

Changes to your code are immediately reflected without reinstalling the package.

This is how most developers work on local projects.

---

# Source Distribution (sdist)

A source distribution contains:

- Python source code
- Project metadata
- Build configuration

Typical extension:

```text
.tar.gz
```

Users build and install it on their own machine.

---

# Wheel

A wheel is a pre-built distribution.

Extension:

```text
.whl
```

Advantages:

- Faster installation
- No build step
- Standard installation format

Whenever possible, users install wheels rather than building from source.

---

# Dependency Management

Dependencies belong in:

```toml
[project]

dependencies = [
    "fastapi",
    "sqlalchemy"
]
```

Avoid asking users to install dependencies manually.

Packaging should describe everything required to run the project.

---

# Versioning

Most Python projects follow Semantic Versioning.

Example:

```text
1.4.2
```

Meaning:

```
Major.Minor.Patch
```

| Part | Meaning |
|------|----------|
| Major | Breaking changes |
| Minor | New backward-compatible features |
| Patch | Bug fixes |

This helps users understand upgrade compatibility.

---

# Optional Dependencies

Some features are optional.

Example:

```toml
[project.optional-dependencies]

dev = [

    "pytest",

    "black",

    "ruff"

]
```

Developers install:

```bash
pip install .[dev]
```

Production deployments can omit development tools.

---

# Entry Points

Applications often expose command-line tools.

Example:

```toml
[project.scripts]

inventory = "app.main:main"
```

After installation:

```bash
inventory
```

runs your application's `main()` function.

This removes the need to execute Python files directly.

---

# Backend Example

Suppose your company develops an internal authentication library.

Instead of copying it into every service:

```
auth-library

↓

Package

↓

Internal Package Registry

↓

pip install auth-library
```

Every backend service now uses the same implementation.

Updates are centralised.

Bug fixes propagate through version upgrades.

---

# Common Mistakes

## Mistake 1

Copying shared code between repositories.

---

## Mistake 2

Not specifying dependency versions.

---

## Mistake 3

Confusing packages with distributions.

---

## Mistake 4

Using editable installs in production.

Editable installs are intended for development.

---

## Mistake 5

Keeping project metadata in multiple unrelated files.

Prefer modern packaging centred around:

```text
pyproject.toml
```

---

# Best Practices

✅ Use `pyproject.toml`.

✅ Use editable installs during development.

✅ Publish wheels when distributing packages.

✅ Version releases consistently.

✅ Keep dependencies explicit.

❌ Don't duplicate shared libraries across projects.

❌ Don't modify installed packages manually.

---

# Production Insight

Packaging is not only for open-source libraries.

Large organisations often maintain dozens or hundreds of internal Python packages.

Examples include:

- Authentication libraries
- Logging utilities
- Database clients
- SDKs
- Shared business logic

Packaging allows these components to be versioned, tested, and reused consistently across multiple services.

---

# Questions

### Question

> What is the difference between a package and a distribution?

### Answer

A package is Python source code organised into modules, while a distribution is the installable artifact, such as a wheel or source distribution.

---

### Question

> Why is `pyproject.toml` important?

### Answer

It provides a standard place to define project metadata, dependencies, and build configuration.

---

### Question

> What is an editable installation?

### Answer

An editable installation links the installed package directly to the project source, allowing code changes to take effect immediately without reinstalling.

---

### Question

> Why are wheels preferred?

### Answer

They are pre-built, install quickly, and avoid building from source during installation.

---

### Question

> Why package internal libraries?

### Answer

Packaging promotes reuse, consistent versioning, easier maintenance, and simpler updates across multiple projects.

---

# Practical Lesson

Create a new project:

```text
calculator-lib/

├── calculator/
│   ├── __init__.py
│   └── operations.py
│
├── tests/
│
└── pyproject.toml
```

Complete the following steps:

1. Add project metadata to `pyproject.toml`.
2. Install the project using:

```bash
pip install -e .
```

3. Create another Python script outside the package.
4. Import and use the installed package.
5. Modify the source code.
6. Verify that the changes are immediately available because of the editable installation.

---

# Knowledge Check

## Question 1

Why should reusable code be packaged instead of copied?

### Answer

Packaging creates a single source of truth, making updates, maintenance, testing, and versioning much easier.

---

## Question 2

When should editable installations be used?

### Answer

During development, when the source code changes frequently and reinstalling after every modification would be inefficient.

---

## Question 3

Why are wheels commonly distributed?

### Answer

Because they install quickly without requiring the package to be built on the target machine.

---

## Question 4

What role does `pyproject.toml` play?

### Answer

It serves as the central configuration file for project metadata, dependencies, and the build system.

---

## Question 5

Why is semantic versioning important?

### Answer

It communicates the impact of a release, helping users understand whether an upgrade contains bug fixes, new features, or breaking changes.

---

# Assignment

## Exercise 1

Create a small reusable Python library.

Package it using `pyproject.toml`.

---

## Exercise 2

Install the library using:

```bash
pip install -e .
```

Modify the source code and verify that the changes are reflected immediately.

---

## Exercise 3

Review one of your existing backend projects.

Identify whether any duplicated code could be extracted into a reusable package.

---

## Exercise 4

Research one popular Python package you use (such as FastAPI, Requests, or SQLAlchemy).

Inspect its `pyproject.toml` and identify:

- Project metadata
- Dependencies
- Optional dependencies
- Build backend

---

# Summary

In this lesson, you learned:

- ✅ What Python packaging is.
- ✅ The difference between packages and distributions.
- ✅ Modern packaging with `pyproject.toml`.
- ✅ Editable installations.
- ✅ Source distributions and wheels.
- ✅ Dependency management.
- ✅ Semantic versioning.
- ✅ Packaging best practices.

---

# Next Lesson

**File:**
[65-production-python-part-10-dependency-injection](65-production-python-part-10-dependency-injection.md)
