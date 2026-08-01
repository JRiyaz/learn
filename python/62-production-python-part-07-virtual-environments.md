# File: python/62-production-python-part-07-virtual-environments.md

# Production Python

# Part 7: Virtual Environments – Isolating Python Projects

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 62
>
> **Difficulty:** ⭐⭐⭐☆☆
>
> **Estimated Time:** 5–6 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why virtual environments exist
- Problems with global package installation
- How `venv` works
- Creating and activating virtual environments
- Installing dependencies
- `requirements.txt`
- Reproducible environments
- Common mistakes
- Production best practices

______________________________________________________________________

# Recap

Every Python project depends on external packages.

For example:

- FastAPI
- Flask
- SQLAlchemy
- Requests
- Celery

Suppose Project A requires:

```text
FastAPI 0.95
```

while Project B requires:

```text
FastAPI 0.116
```

If both projects share the same global Python installation, dependency conflicts become inevitable.

Virtual environments solve this problem by isolating each project's dependencies.

______________________________________________________________________

# What is a Virtual Environment?

A virtual environment is an isolated Python environment containing:

- Its own Python executable
- Its own installed packages
- Its own scripts

Each project can therefore manage its dependencies independently.

______________________________________________________________________

# Why Isolation Matters

Without virtual environments:

```
Python

↓

Global Packages

↓

Project A

Project B

Project C
```

Installing or upgrading a package for one project may break another.

With virtual environments:

```
Project A

↓

venv

↓

Packages
```

```
Project B

↓

venv

↓

Packages
```

Each project has its own isolated environment.

______________________________________________________________________

# Creating a Virtual Environment

Create a new environment:

```bash
python -m venv .venv
```

This creates a directory named:

```text
.venv/
```

containing the isolated environment.

______________________________________________________________________

# Typical Structure

```text
project/

├── .venv/

├── app/

├── tests/

├── requirements.txt

└── README.md
```

The `.venv` directory should not be committed to version control.

______________________________________________________________________

# Activating the Environment

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

Once activated, `python` and `pip` refer to the virtual environment rather than the global installation.

______________________________________________________________________

# Installing Packages

```bash
pip install fastapi
```

The package is installed only inside the active virtual environment.

Other projects remain unaffected.

______________________________________________________________________

# Recording Dependencies

Export installed packages:

```bash
pip freeze > requirements.txt
```

Example:

```text
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.43
```

Another developer can recreate the environment using:

```bash
pip install -r requirements.txt
```

______________________________________________________________________

# Reproducible Environments

Imagine a teammate clones your repository.

Instead of manually installing packages one by one, they can recreate the exact dependency set from:

```text
requirements.txt
```

This ensures everyone develops against the same versions.

______________________________________________________________________

# Updating Dependencies

When adding a new package:

```bash
pip install redis
```

Update the dependency list:

```bash
pip freeze > requirements.txt
```

Commit the updated file along with your code changes.

______________________________________________________________________

# Version Control

A common `.gitignore` entry:

```text
.venv/
__pycache__/
*.pyc
```

Never commit:

- Virtual environments
- Compiled Python files
- Temporary caches

Only commit dependency declarations such as `requirements.txt`.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Installing packages globally.

______________________________________________________________________

## Mistake 2

Forgetting to activate the virtual environment before installing packages.

______________________________________________________________________

## Mistake 3

Committing `.venv` to Git.

______________________________________________________________________

## Mistake 4

Forgetting to update `requirements.txt`.

______________________________________________________________________

## Mistake 5

Assuming another developer has the same packages installed.

______________________________________________________________________

# Best Practices

✅ Create one virtual environment per project.

✅ Keep the virtual environment outside version control.

✅ Record project dependencies.

✅ Recreate environments from dependency files.

❌ Don't share one virtual environment across unrelated projects.

❌ Don't rely on globally installed packages.

______________________________________________________________________

# Production Insight

Virtual environments are primarily a **development tool**.

In production, dependency isolation is often provided by:

- Docker containers
- Virtual machines
- Managed deployment platforms

Even then, the application's dependencies should still be declared explicitly so deployments remain reproducible.

______________________________________________________________________

# Questions

### Question

> Why are virtual environments important?

### Answer

They isolate project dependencies, preventing version conflicts between different Python projects.

______________________________________________________________________

### Question

> Why shouldn't `.venv` be committed to Git?

### Answer

It is platform-specific, can be recreated easily, and unnecessarily increases repository size.

______________________________________________________________________

### Question

> What is the purpose of `requirements.txt`?

### Answer

It records project dependencies so the environment can be reproduced consistently on another machine.

______________________________________________________________________

### Question

> Why activate a virtual environment?

### Answer

Activation ensures Python and `pip` use the project's isolated environment instead of the global installation.

______________________________________________________________________

### Question

> Are virtual environments used directly in production?

### Answer

Usually not. Production environments often use containers or virtual machines, but dependency declarations remain
essential.

______________________________________________________________________

# Practical Lesson

Create a new project:

```text
inventory-service/
```

Complete the following steps:

1. Create a virtual environment.
1. Activate it.
1. Install `fastapi`, `uvicorn`, and `sqlalchemy`.
1. Export dependencies to `requirements.txt`.
1. Add `.venv/` to `.gitignore`.
1. Delete the virtual environment and recreate it using `requirements.txt`.

Observe that the recreated environment behaves identically.

______________________________________________________________________

# Knowledge Check

## Question 1

Why are global package installations discouraged?

### Answer

Because projects often require different dependency versions, leading to conflicts and unpredictable behaviour.

______________________________________________________________________

## Question 2

Why should dependency versions be recorded?

### Answer

To ensure every developer and deployment uses compatible package versions.

______________________________________________________________________

## Question 3

What does activating a virtual environment change?

### Answer

It changes the Python interpreter and package installation path to the project's isolated environment.

______________________________________________________________________

## Question 4

Why shouldn't virtual environments be committed to source control?

### Answer

They are machine-specific, easily recreated, and unnecessarily increase repository size.

______________________________________________________________________

## Question 5

How do virtual environments contribute to reproducible development?

### Answer

They ensure each project uses its own isolated dependencies, avoiding interference from globally installed packages.

______________________________________________________________________

# Assignment

## Exercise 1

Create a new virtual environment for one of your existing projects.

______________________________________________________________________

## Exercise 2

Delete and recreate the environment using only `requirements.txt`.

______________________________________________________________________

## Exercise 3

Compare the output of:

```bash
which python
```

(or `where python` on Windows)

before and after activating the virtual environment.

______________________________________________________________________

## Exercise 4

Review one of your repositories.

Verify that:

- `.venv/` is ignored.
- Dependencies are version-pinned.
- Another developer could recreate the environment using only the repository contents.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why virtual environments exist.
- ✅ How dependency isolation works.
- ✅ Creating and activating `venv`.
- ✅ Managing project dependencies.
- ✅ Using `requirements.txt`.
- ✅ Best practices for reproducible development.

______________________________________________________________________

# Next Lesson

**File:**
[63-production-python-part-08-project-structure-and-packaging](63-production-python-part-08-project-structure-and-packaging.md)
