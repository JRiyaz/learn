# 7. Python Modules, Packages & Virtual Environments

**Previous:** [6. Exception Handling & Error Management](./06-python-exceptions.md)

**Next:** [8. Python OOP & Design Principles](./08-python-oop.md)

______________________________________________________________________

## Objectives

By the end of this chapter, you should be able to:

- Explain Python modules and packages.
- Understand how Python imports and resolves modules.
- Use `import`, `from ... import`, and aliases correctly.
- Explain `__name__` and `__main__`.
- Understand `__init__.py`.
- Understand absolute vs relative imports.
- Explain circular imports and how to avoid them.
- Understand `sys.path` at an interview level.
- Explain virtual environments and why they matter.
- Understand `venv`, `pip`, and dependency management.
- Explain `requirements.txt` and lock files conceptually.
- Understand package installation and editable installs.
- Understand common backend project structures.
- Recognize common import and dependency-management mistakes.

______________________________________________________________________

# 1. What Is a Module?

A Python module is typically a `.py` file containing Python code.

Example:

```text
utils.py
```

could contain:

```python
def add(a, b):
    return a + b
```

Another file can import it:

```python
import utils

print(utils.add(1, 2))
```

A module provides a namespace for related code.

______________________________________________________________________

# 2. Why Modules Matter

Modules help with:

- Code organization
- Reusability
- Namespaces
- Separation of concerns
- Testing
- Dependency management

Instead of placing an entire backend application into one file, functionality can be separated into modules.

______________________________________________________________________

# 3. `import`

Basic import:

```python
import math

print(math.sqrt(16))
```

The module is imported under the name:

```python
math
```

This keeps the module namespace explicit.

______________________________________________________________________

# 4. `from ... import`

You can import specific names:

```python
from math import sqrt

print(sqrt(16))
```

This can make code shorter, but excessive use of direct imports can sometimes make it less obvious where a name
originated.

______________________________________________________________________

# 5. Import Aliases

Aliases are useful for long or conflicting names.

```python
import numpy as np
```

or:

```python
from collections import defaultdict as DD
```

Use aliases that are conventional and readable.

Avoid obscure aliases that make code difficult to understand.

______________________________________________________________________

# 6. Module Namespace

A module is a namespace.

Suppose:

```python
# users.py

DEFAULT_ROLE = "user"

def create_user():
    ...
```

Then:

```python
import users

users.DEFAULT_ROLE
users.create_user()
```

The module name separates its contents from names in the importing module.

This helps prevent naming collisions.

______________________________________________________________________

# 7. `__name__`

Every Python module has a `__name__` attribute.

If the file is executed directly:

```python
python app.py
```

then:

```python
__name__ == "__main__"
```

If it is imported:

```python
import app
```

then:

```python
__name__
```

is normally the module's import name.

______________________________________________________________________

# 8. The `if __name__ == "__main__"` Pattern

Common pattern:

```python
def main():
    print("Application started")


if __name__ == "__main__":
    main()
```

This means:

> Run `main()` only when this file is executed directly, not when it is imported.

This is useful for modules that can be both imported and executed.

______________________________________________________________________

# 9. What Is a Package?

A package is a way to organize related modules under a common namespace.

Example:

```text
app/
    users/
        service.py
        repository.py
```

You can import:

```python
from app.users.service import UserService
```

Packages are essential for structuring larger Python applications.

______________________________________________________________________

# 10. `__init__.py`

Historically, a regular Python package contains:

```text
__init__.py
```

Example:

```text
app/
    __init__.py
    users/
        __init__.py
        service.py
```

`__init__.py` can:

- Mark/package the package in traditional package semantics.
- Run package initialization code.
- Expose selected names.

Modern Python also supports namespace packages without `__init__.py`, but normal application packages commonly still use
it.

______________________________________________________________________

# 11. Package Initialization

Consider:

```python
# users/__init__.py

from .service import UserService
```

Then:

```python
from users import UserService
```

can expose the class at the package level.

Be careful not to put heavy initialization or side effects in `__init__.py`.

______________________________________________________________________

# 12. Absolute Imports

Example:

```python
from app.users.service import UserService
```

This explicitly describes the package path from the import root.

Absolute imports are generally easier to understand in larger applications.

______________________________________________________________________

# 13. Relative Imports

Inside a package:

```python
from .service import UserService
```

means import from the current package.

Another example:

```python
from ..database import get_connection
```

moves to the parent package.

Relative imports can be useful within cohesive packages, but excessive nesting can make dependencies harder to
understand.

______________________________________________________________________

# 14. Absolute vs Relative Imports

### Absolute

```python
from app.users.service import UserService
```

Advantages:

- Explicit
- Easier to search
- Clear package relationship

### Relative

```python
from .service import UserService
```

Advantages:

- Concise
- Useful inside reusable package structures
- Less dependent on the top-level package name

The best choice depends on project structure and conventions.

______________________________________________________________________

# 15. How Python Finds Imports

When Python executes:

```python
import mymodule
```

it searches locations on its module search path.

A major source of that information is:

```python
sys.path
```

Example:

```python
import sys

print(sys.path)
```

The exact entries depend on how Python was launched and the environment.

______________________________________________________________________

# 16. `sys.path`

`sys.path` is a list of locations Python searches for importable modules/packages.

It can include:

- The script/application location
- Standard library paths
- Site-packages
- Environment-specific paths
- Other configured import locations

Manually modifying `sys.path` to fix project imports is usually a code smell.

Prefer correct package structure and environment configuration.

______________________________________________________________________

# 17. Import Caching

Python caches imported modules.

After:

```python
import users
```

the loaded module is generally stored in:

```python
sys.modules
```

Therefore, repeated imports do not normally re-execute the module from scratch.

Example:

```python
import sys

print("users" in sys.modules)
```

This is useful for understanding import behavior.

______________________________________________________________________

# 18. Module-Level Code Executes on Import

Consider:

```python
# config.py

print("Loading configuration")

PORT = 8000
```

When:

```python
import config
```

occurs, the module-level code executes as the module is initialized.

This is why modules should avoid unnecessary side effects during import.

______________________________________________________________________

# 19. Importing a Module Multiple Times

Python normally initializes a module once per interpreter process.

After it is loaded, subsequent imports generally reuse the cached module object from:

```python
sys.modules
```

This is not the same as saying imports are globally permanent; interpreter restarts create a new process and module
state.

______________________________________________________________________

# 20. Circular Imports

A circular import occurs when modules depend on each other.

Example:

```text
users.py → orders.py
orders.py → users.py
```

This can cause partially initialized modules and confusing import errors.

Circular imports are often a sign that module responsibilities or dependency direction need improvement.

______________________________________________________________________

# 21. Example of a Circular Import

Suppose:

```python
# a.py

from b import B

class A:
    ...
```

and:

```python
# b.py

from a import A

class B:
    ...
```

Importing either module can create a cycle.

Python may encounter a partially initialized module while trying to resolve the dependency.

______________________________________________________________________

# 22. How to Avoid Circular Imports

Possible approaches:

### Refactor shared functionality

Move common code into:

```text
common.py
```

### Improve dependency direction

For example:

```text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

instead of modules depending on each other bidirectionally.

### Local import

Sometimes:

```python
def function():
    from module_b import helper
```

can break an import cycle.

However, this should not become the default solution.

______________________________________________________________________

# 23. Imports and Type Hints

Sometimes type annotations contribute to circular dependencies.

Modern Python provides tools such as:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_b import SomeType
```

Then use a forward reference where appropriate.

This can reduce runtime import dependencies while retaining type-checking information.

______________________________________________________________________

# 24. `__all__`

A module can define:

```python
__all__ = [
    "UserService",
    "UserRepository",
]
```

This communicates which names are intended as the module's public export surface, particularly for wildcard imports.

However:

```python
from module import *
```

is generally discouraged in application code because it makes dependencies less explicit.

______________________________________________________________________

# 25. Wildcard Imports

Avoid:

```python
from module import *
```

because:

- It hides where names came from.
- It can cause naming conflicts.
- It makes static analysis harder.
- It reduces readability.

Prefer explicit imports:

```python
from module import UserService, UserRepository
```

______________________________________________________________________

# 26. What Is a Virtual Environment?

A virtual environment provides an isolated Python environment for a project.

Without isolation, projects can conflict over dependency versions.

For example:

```text
Project A → requests 2.x
Project B → requests 3.x
```

A virtual environment lets each project maintain its own installed dependencies.

______________________________________________________________________

# 27. Creating a Virtual Environment

Python includes:

```bash
python -m venv .venv
```

This creates an environment in:

```text
.venv/
```

Activation depends on the operating system and shell.

After activation:

```bash
python
pip
```

refer to the environment's interpreter/tools.

______________________________________________________________________

# 28. Why Virtual Environments Matter

They provide:

- Dependency isolation
- Reproducibility
- Cleaner development environments
- Fewer version conflicts
- Safer project experimentation

They are a fundamental part of Python backend development.

______________________________________________________________________

# 29. `pip`

`pip` is the standard Python package installer.

Example:

```bash
pip install requests
```

It installs a package and its dependencies into the current environment.

You should understand that `pip` installs packages; it is not itself a full dependency-locking or project-management
solution.

______________________________________________________________________

# 30. `requirements.txt`

A common dependency file is:

```text
requirements.txt
```

Example:

```text
fastapi==...
uvicorn==...
requests==...
```

Install:

```bash
pip install -r requirements.txt
```

A requirements file is commonly used to describe dependencies needed by an environment.

______________________________________________________________________

# 31. Pinning Dependencies

A loose dependency:

```text
requests
```

allows a compatible/latest version according to package resolution rules.

A pinned dependency:

```text
requests==2.x.x
```

specifies an exact version.

Pinning can improve reproducibility, but dependency management also needs to consider transitive dependencies and
security updates.

______________________________________________________________________

# 32. Direct vs Transitive Dependencies

Suppose your application directly depends on:

```text
FastAPI
```

FastAPI itself depends on other packages.

Those are transitive dependencies.

A robust dependency-management strategy distinguishes:

```text
Direct dependencies
        ↓
Transitive dependencies
```

This becomes important when reproducing production environments.

______________________________________________________________________

# 33. Dependency Locking

Modern Python projects may use dependency managers/tools that generate lock files.

A lock file records a resolved dependency graph, often including exact versions and metadata.

The goal is:

> Resolve dependencies once and reproduce the same environment consistently.

You should understand the concept even if a particular project uses a different tool.

______________________________________________________________________

# 34. Editable Installs

During development, a package can often be installed in editable mode:

```bash
pip install -e .
```

This allows the installed package to point to the source tree so code changes can be reflected without reinstalling the
package after every modification.

This is common when developing a Python package or monorepo component.

______________________________________________________________________

# 35. `pyproject.toml`

Modern Python projects commonly use:

```text
pyproject.toml
```

for project metadata and tool configuration.

It can describe:

- Project metadata
- Build configuration
- Dependencies
- Optional dependencies
- Tool configuration

The exact dependency-management workflow depends on the project tooling.

You should recognize `pyproject.toml` as an important modern Python project file.

______________________________________________________________________

# 36. Package vs Distribution

These terms are sometimes confused.

A Python import package describes the structure used by Python imports.

A distribution is the installable project artifact published to a package repository.

For example, the name used by:

```bash
pip install ...
```

does not always have to match the name used in:

```python
import ...
```

Understanding this distinction helps diagnose dependency/import problems.

______________________________________________________________________

# 37. Standard Library vs Third-Party Packages

### Standard library

Included with Python:

```python
import json
import os
import pathlib
import collections
```

### Third-party

Installed separately:

```python
import fastapi
import numpy
import requests
```

Backend projects commonly combine both.

______________________________________________________________________

# 38. Dependency Injection and Imports

Large applications often structure dependencies so that modules do not instantiate everything globally.

Instead of:

```python
repository = Repository()
service = Service(repository)
```

at import time everywhere, dependency construction can happen at application startup or through an explicit
dependency-injection mechanism.

This reduces import-time side effects and makes testing easier.

______________________________________________________________________

# 39. Common Module and Package Mistakes

## Mistake 1 — Huge `__init__.py`

Putting substantial application logic into `__init__.py` can create hidden side effects and import cycles.

______________________________________________________________________

## Mistake 2 — Modifying `sys.path`

Manually adding project paths often masks packaging problems.

Fix the package structure instead.

______________________________________________________________________

## Mistake 3 — Wildcard imports

```python
from module import *
```

makes dependencies unclear.

______________________________________________________________________

## Mistake 4 — Circular imports

Bidirectional module dependencies often indicate poor dependency direction.

______________________________________________________________________

## Mistake 5 — Global initialization at import time

Database connections, network calls or expensive setup during import can make testing and startup behavior difficult.

______________________________________________________________________

## Mistake 6 — Installing globally

Installing project dependencies globally can create conflicts between projects.

Use a virtual environment.

______________________________________________________________________

# 40. Backend Project Structure

A typical backend might look like:

```text
project/
├── pyproject.toml
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── models/
│       ├── __init__.py
│       └── user.py
└── tests/
```

The exact structure varies, but the important principle is separation of responsibilities and controlled dependency
direction.

______________________________________________________________________

# 41. Module Design Principles

A good module should generally have:

- A clear responsibility
- Minimal unnecessary coupling
- Explicit dependencies
- A small public API
- Limited import-time side effects

Avoid creating modules solely because a file has become long.

The organization should reflect domain or responsibility boundaries.

______________________________________________________________________

# 42. Interview Questions & Answers

## Q1. What is a Python module?

**Answer:**

A module is typically a Python file containing code such as functions, classes and variables that can be imported into
another module.

______________________________________________________________________

## Q2. What is a package?

**Answer:**

A package organizes related Python modules under a common namespace.

It is used to structure larger applications and libraries.

______________________________________________________________________

## Q3. What is `__init__.py`?

**Answer:**

It is a package initialization module traditionally used to define package behavior and exports.

Modern Python also supports namespace packages without it, but normal application packages commonly use it.

______________________________________________________________________

## Q4. What is `__name__`?

**Answer:**

`__name__` identifies the current module.

When a file is executed directly, it is typically:

```python
"__main__"
```

When imported, it normally contains the module's import name.

______________________________________________________________________

## Q5. Why use `if __name__ == "__main__"`?

**Answer:**

It allows code such as a `main()` function to execute only when the file is run directly, not when imported.

______________________________________________________________________

## Q6. What is the difference between absolute and relative imports?

**Answer:**

An absolute import specifies the package path from the import root:

```python
from app.users.service import UserService
```

A relative import references the current/parent package:

```python
from .service import UserService
```

______________________________________________________________________

## Q7. What is `sys.path`?

**Answer:**

It is the list of locations Python searches for importable modules and packages.

It is influenced by the Python installation, execution environment and how the application is launched.

______________________________________________________________________

## Q8. What is `sys.modules`?

**Answer:**

It is a mapping containing modules that have been loaded in the current Python interpreter.

It is part of Python's import machinery and helps prevent normal modules from being initialized repeatedly.

______________________________________________________________________

## Q9. What is a circular import?

**Answer:**

A circular import occurs when module A depends on module B while module B also depends on module A.

It can lead to partially initialized modules and import errors.

______________________________________________________________________

## Q10. How can circular imports be fixed?

**Answer:**

Prefer refactoring responsibilities and dependency direction.

Other options include moving shared code into a third module or using carefully scoped local imports when appropriate.

______________________________________________________________________

## Q11. Why avoid wildcard imports?

**Answer:**

They make dependencies and name origins unclear, can cause collisions, and make code harder to analyze and maintain.

______________________________________________________________________

## Q12. What is a virtual environment?

**Answer:**

A virtual environment isolates a project's Python interpreter and installed dependencies from other projects and the
system environment.

______________________________________________________________________

## Q13. Why use virtual environments?

**Answer:**

They prevent dependency conflicts and make development environments more reproducible and isolated.

______________________________________________________________________

## Q14. What is `pip`?

**Answer:**

`pip` is Python's standard package installer used to install and manage Python distributions.

______________________________________________________________________

## Q15. What is `requirements.txt`?

**Answer:**

It is a commonly used file containing dependencies required by an environment, which can be installed with:

```bash
pip install -r requirements.txt
```

______________________________________________________________________

## Q16. What is the difference between direct and transitive dependencies?

**Answer:**

Direct dependencies are packages your project explicitly depends on.

Transitive dependencies are dependencies required by those packages.

______________________________________________________________________

## Q17. Why are lock files useful?

**Answer:**

They record a resolved dependency graph so environments can reproduce compatible package versions more consistently.

______________________________________________________________________

## Q18. What is an editable install?

**Answer:**

An editable install such as:

```bash
pip install -e .
```

installs a project so changes to its source tree are reflected without repeatedly reinstalling the package.

______________________________________________________________________

## Q19. What is `pyproject.toml`?

**Answer:**

It is a modern Python project configuration file used for project metadata, build configuration, dependencies and tool
configuration depending on the project's tooling.

______________________________________________________________________

## Q20. Why is import-time side effect a problem?

**Answer:**

Code executed during import can cause unexpected network calls, database connections, expensive startup work, circular
imports and difficult-to-test behavior.

______________________________________________________________________

# 43. Scenario-Based Questions

## Scenario 1 — Works Locally but Import Fails in Production

A developer runs:

```python
from app.services.user import UserService
```

locally, but production reports:

```text
ModuleNotFoundError
```

**Question:** What would you investigate?

**Answer:**

Check:

- Project/package structure
- How the application is launched
- Python environment
- Installed package
- Working directory
- `sys.path`
- Packaging configuration

Avoid blindly modifying `sys.path`.

______________________________________________________________________

## Scenario 2 — Two Projects Need Different Package Versions

Project A requires one version of a dependency while Project B requires another.

**Question:** What should you use?

**Answer:**

Separate virtual environments for the projects, with each environment managing its own dependencies.

______________________________________________________________________

## Scenario 3 — Importing the Application Opens a Database Connection

A module contains:

```python
db = connect_to_database()
```

at module scope.

Tests importing the module unexpectedly connect to the database.

**Question:** What design issue exists?

**Answer:**

The module has an import-time side effect.

Move resource creation to explicit application startup/dependency construction so importing the module does not
unexpectedly perform external operations.

______________________________________________________________________

## Scenario 4 — Circular Service Imports

You have:

```text
user_service.py → order_service.py
order_service.py → user_service.py
```

and imports fail.

**Question:** What would you do?

**Answer:**

First examine whether the service responsibilities are too tightly coupled.

Refactor shared logic into a third module or introduce a higher-level orchestration layer with clearer dependency
direction.

Use local imports only as a targeted solution when restructuring is not practical.

______________________________________________________________________

## Scenario 5 — Dependency Works on Developer Laptop

The application runs locally but fails in a clean deployment because a package is missing.

**Question:** What process should prevent this?

**Answer:**

Declare dependencies explicitly in the project's dependency configuration and build/deployment process.

Use a reproducible environment strategy, including appropriate version constraints/lock information.

Do not rely on packages installed manually on a developer's machine.

______________________________________________________________________

# 44. Practice Exercises

## Exercise 1 — Create a Package

Create:

```text
app/
    __init__.py
    users/
        __init__.py
        service.py
        repository.py
```

Implement a simple service and import it from another module.

______________________________________________________________________

## Exercise 2 — `__main__`

Create a module containing:

```python
def main():
    ...
```

Use:

```python
if __name__ == "__main__":
    main()
```

Demonstrate the difference between running the module and importing it.

______________________________________________________________________

## Exercise 3 — Circular Import

Intentionally create two modules that import each other.

Observe the failure.

Then refactor the shared functionality into a third module.

______________________________________________________________________

## Exercise 4 — Virtual Environment

Create:

```bash
python -m venv .venv
```

Install a small package and verify that it is available inside the environment.

Then compare the environment with the system interpreter.

______________________________________________________________________

## Exercise 5 — Dependency File

Create a small project with declared dependencies.

Practice installing them into a clean virtual environment.

Verify that the project works without relying on globally installed packages.

______________________________________________________________________

## Exercise 6 — Import-Time Side Effects

Create a module that performs work at import time.

Then refactor it so importing the module only defines functions/classes and explicit application startup performs the
work.

______________________________________________________________________

# 45. Quick Revision

| Concept | Key Point |
|---|---|
| Module | Usually a Python `.py` file |
| Package | Namespace for related modules |
| `__init__.py` | Package initialization/export module |
| `__name__` | Current module name |
| `__main__` | Name used when executed directly |
| Absolute import | Import from package root |
| Relative import | Import relative to current package |
| `sys.path` | Import search locations |
| `sys.modules` | Loaded module cache/mapping |
| Circular import | Modules depend on each other cyclically |
| `__all__` | Declares intended exports |
| Wildcard import | Generally avoid in application code |
| Virtual environment | Isolated Python environment |
| `pip` | Package installer |
| `requirements.txt` | Common dependency specification |
| Direct dependency | Explicit project dependency |
| Transitive dependency | Dependency of another dependency |
| Lock file | Records resolved dependency graph |
| Editable install | Source-linked development installation |
| `pyproject.toml` | Modern project/build/tool configuration |
| Import-time side effect | Work performed just by importing a module |

______________________________________________________________________

# 46. Completion Checklist

Before moving to File 8, make sure you can explain:

- [ ] Modules
- [ ] Packages
- [ ] `import`
- [ ] `from ... import`
- [ ] Import aliases
- [ ] Module namespaces
- [ ] `__name__`
- [ ] `__main__`
- [ ] `if __name__ == "__main__"`
- [ ] `__init__.py`
- [ ] Package exports
- [ ] Absolute imports
- [ ] Relative imports
- [ ] `sys.path`
- [ ] `sys.modules`
- [ ] Module caching
- [ ] Module-level execution
- [ ] Circular imports
- [ ] Circular-import solutions
- [ ] `TYPE_CHECKING`
- [ ] `__all__`
- [ ] Wildcard imports
- [ ] Virtual environments
- [ ] `venv`
- [ ] `pip`
- [ ] `requirements.txt`
- [ ] Dependency pinning
- [ ] Direct vs transitive dependencies
- [ ] Lock files
- [ ] Editable installs
- [ ] `pyproject.toml`
- [ ] Package vs distribution
- [ ] Import-time side effects
- [ ] Backend package structure
- [ ] Dependency direction

______________________________________________________________________

# 47. Interview Readiness Test

Without looking at the notes, answer these aloud:

1. What is a Python module?
1. What is a package?
1. What is the purpose of `__init__.py`?
1. What is `__name__`?
1. What does `if __name__ == "__main__"` achieve?
1. Explain absolute vs relative imports.
1. How does Python find an imported module?
1. What is `sys.path`?
1. What is `sys.modules`?
1. Why does Python cache imported modules?
1. What is a circular import?
1. How would you fix a circular import?
1. Why should wildcard imports generally be avoided?
1. What is a virtual environment?
1. Why are virtual environments important for backend development?
1. What is `pip`?
1. What is `requirements.txt`?
1. What are direct and transitive dependencies?
1. Why are dependency lock files useful?
1. What is an editable install?
1. What is `pyproject.toml`?
1. Why are import-time side effects dangerous?
1. How would you diagnose `ModuleNotFoundError` in production?
1. How would you structure dependencies between API, service and repository modules?

If you can answer these clearly and implement the exercises without relying heavily on the notes, this chapter is
complete.

______________________________________________________________________

**Previous:** [6. Exception Handling & Error Management](./06-python-exceptions.md)

**Next:** [8. Python OOP & Design Principles](./08-python-oop.md)
