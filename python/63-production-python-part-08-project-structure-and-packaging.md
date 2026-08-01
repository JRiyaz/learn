# File: python/63-production-python-part-08-project-structure-and-packaging.md

# Production Python

# Part 1: Project Structure, Packages & Production-Grade Code Organization

> **Course:** Backend Engineering Roadmap
>
> **Module:** Production Python
>
> **Lesson:** 56
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 8–10 Hours

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Why project structure matters
- How Python packages work internally
- The difference between modules and packages
- How imports are resolved
- Absolute vs relative imports
- Production project layouts
- Separation of concerns
- Layered architecture
- Circular import problems
- Best practices used in large backend applications

______________________________________________________________________

# Recap

So far, you've learned how to write efficient Python code and how Python executes concurrent workloads.

However, writing good code is only part of software engineering.

The next step is learning how to organise thousands of lines of code into a maintainable application.

A backend service rarely consists of a single file.

Instead, a production project might look like this:

```text
50 packages

↓

300 modules

↓

20,000+ lines of code
```

Poor organisation makes systems difficult to maintain, test, and extend.

______________________________________________________________________

# Why Project Structure Matters

Imagine this project:

```text
project/

app.py

database.py

models.py

users.py

orders.py

payments.py

emails.py

cache.py

utils.py

helpers.py

...
```

As the application grows:

- Finding code becomes difficult.
- Merge conflicts increase.
- Imports become tangled.
- Testing becomes painful.

A good project structure solves these problems.

______________________________________________________________________

# Module vs Package

A **module** is a single Python file.

Example:

```text
users.py
```

A **package** is a directory containing Python modules.

Example:

```text
users/

    __init__.py

    service.py

    repository.py

    schemas.py
```

Packages help group related functionality.

______________________________________________________________________

# How Imports Work

When Python executes:

```python
from users.service import create_user
```

It searches:

1. Built-in modules
1. Current project
1. Installed packages
1. `sys.path`

Python does **not** search the entire filesystem.

Understanding this search order helps explain many import errors.

______________________________________________________________________

# The Role of `__init__.py`

Traditionally, a directory became a package by containing:

```text
__init__.py
```

Although modern Python supports namespace packages, most production projects still include `__init__.py` because it:

- Clearly marks packages.
- Allows package initialisation.
- Exposes a public package API.

Example:

```python
from .service import UserService

__all__ = ["UserService"]
```

______________________________________________________________________

# Absolute Imports

Example:

```python
from app.services.user import UserService
```

Advantages:

- Explicit
- Easy to understand
- Easier to refactor
- Preferred in large codebases

______________________________________________________________________

# Relative Imports

Example:

```python
from .repository import UserRepository
```

Useful within the same package.

Avoid deeply nested imports like:

```python
from ....database.connection import Database
```

These quickly become difficult to read.

______________________________________________________________________

# A Typical Production Layout

```text
my_app/

├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── core/
│   ├── config/
│   ├── database/
│   └── utils/
│
├── tests/
│
├── scripts/
│
├── docs/
│
├── pyproject.toml
│
└── README.md
```

Every directory has a clear responsibility.

______________________________________________________________________

# Layered Architecture

A common backend architecture looks like this:

```text
HTTP Request

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

Database
```

Each layer has a single responsibility.

______________________________________________________________________

# Example

Suppose a request arrives:

```
POST /users
```

The flow becomes:

```text
API

↓

UserService

↓

UserRepository

↓

PostgreSQL
```

Notice that:

- The API layer knows nothing about SQL.
- The repository knows nothing about HTTP.
- The service contains business rules.

This separation makes applications easier to test and maintain.

______________________________________________________________________

# Circular Imports

One of the most common issues in growing Python projects.

Example:

```text
users.py

↓

imports

↓

orders.py

↓

imports

↓

users.py
```

Python cannot finish importing either module.

Result:

```text
ImportError

or

AttributeError

(partially initialized module)
```

______________________________________________________________________

# How to Avoid Circular Imports

Instead of tightly coupling modules:

```text
UserService

↓

OrderService
```

introduce a shared abstraction or move common functionality into another module.

General strategies:

- Keep dependencies one-directional.
- Extract shared code.
- Import locally only when appropriate.
- Design clear module boundaries.

______________________________________________________________________

# Naming Packages

Good:

```text
users
payments
inventory
notifications
```

Avoid:

```text
helpers
misc
common_stuff
random
```

Package names should describe a business capability or technical responsibility.

______________________________________________________________________

# Configuration Files

A production Python project usually includes:

```text
pyproject.toml
```

This file can define:

- Project metadata
- Dependencies
- Build configuration
- Tool configuration

It has become the standard entry point for modern Python projects.

______________________________________________________________________

# Repository Layout Example

```text
inventory-service/

├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── database/
│   ├── config/
│   └── utils/
│
├── tests/
├── migrations/
├── scripts/
├── docs/
├── pyproject.toml
├── README.md
└── .gitignore
```

This structure scales well from small services to large backend systems.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Putting all code into:

```text
app.py
```

______________________________________________________________________

## Mistake 2

Creating generic folders such as:

```text
helpers/
misc/
common/
```

without clear ownership.

______________________________________________________________________

## Mistake 3

Mixing HTTP logic, business rules, and database code in the same module.

______________________________________________________________________

## Mistake 4

Ignoring circular dependencies until they become difficult to untangle.

______________________________________________________________________

# Best Practices

✅ Organise code by responsibility.

✅ Prefer absolute imports for cross-package references.

✅ Keep packages cohesive.

✅ Separate business logic from infrastructure.

✅ Design with future growth in mind.

❌ Don't create "god modules."

❌ Don't mix unrelated responsibilities.

______________________________________________________________________

# Production Insight

Large engineering teams optimise for **maintainability**, not just correctness.

A well-structured codebase enables:

- Faster onboarding.
- Easier testing.
- Safer refactoring.
- Clear ownership.
- Better code reviews.

Many production issues are caused not by incorrect algorithms, but by unclear architecture and tightly coupled code.

______________________________________________________________________

# Questions

### Question

> What is the difference between a module and a package?

### Answer

A module is a single Python file, while a package is a directory that groups related modules into a logical unit.

______________________________________________________________________

### Question

> Why are absolute imports generally preferred?

### Answer

They are more explicit, easier to understand, and less fragile during refactoring.

______________________________________________________________________

### Question

> What causes circular imports?

### Answer

They occur when two or more modules depend on each other during import, preventing Python from completing module
initialisation.

______________________________________________________________________

### Question

> Why separate services and repositories?

### Answer

Services implement business logic, while repositories handle data persistence. Separating them improves maintainability
and testability.

______________________________________________________________________

### Question

> Why is project structure important?

### Answer

A good structure reduces complexity, clarifies responsibilities, and allows a codebase to scale as the application
grows.

______________________________________________________________________

# Practical Lesson

Create a new project with the following structure:

```text
bookstore/

├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── database/
│   ├── config/
│   └── utils/
│
├── tests/
├── scripts/
├── docs/
├── pyproject.toml
└── README.md
```

Then:

1. Create a `BookService`.
1. Create a `BookRepository`.
1. Add a simple `Book` model.
1. Keep each layer responsible for only one concern.

______________________________________________________________________

# Questions

## Question 1

Why is layered architecture beneficial in backend applications?

### Answer

It separates concerns, making the codebase easier to maintain, test, and extend.

______________________________________________________________________

## Question 2

What are the advantages of packages over large individual modules?

### Answer

Packages group related functionality, reduce complexity, improve discoverability, and encourage modular design.

______________________________________________________________________

## Question 3

How can circular imports be avoided?

### Answer

By designing one-directional dependencies, extracting shared logic, and maintaining clear module boundaries.

______________________________________________________________________

## Question 4

Why are generic folders like `helpers` discouraged?

### Answer

Because they accumulate unrelated functionality, making ownership and discoverability unclear.

______________________________________________________________________

## Question 5

What role does `pyproject.toml` play in modern Python projects?

### Answer

It serves as the standard configuration file for project metadata, dependencies, builds, and development tools.

______________________________________________________________________

# Assignment

## Exercise 1

Restructure one of your existing Flask or FastAPI projects into a layered architecture.

______________________________________________________________________

## Exercise 2

Identify any circular dependencies in your project and propose a redesign.

______________________________________________________________________

## Exercise 3

Create a package with multiple modules and expose only its public API through `__init__.py`.

______________________________________________________________________

## Exercise 4

Draw the architecture of one of your backend services, showing:

- API Layer
- Service Layer
- Repository Layer
- Database

Explain the responsibility of each layer.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ The difference between modules and packages.
- ✅ How Python resolves imports.
- ✅ Absolute vs relative imports.
- ✅ Layered architecture.
- ✅ Avoiding circular imports.
- ✅ Production project organisation.
- ✅ Best practices for scalable backend applications.

______________________________________________________________________

# Next Lesson

**File:** [64-production-python-part-09-packaging](64-production-python-part-09-packaging.md)
