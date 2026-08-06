# Installation & Project Structure

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `02_installation_project_structure.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Installing FastAPI
- Installing Uvicorn
- Virtual Environments
- Project Structure
- Running a FastAPI Application
- Development Mode
- Hot Reload
- Production Server
- Dependency Management
- Recommended Project Layout
- Best Practices

______________________________________________________________________

# Prerequisites

You should have

- Python 3.10+
- pip
- Basic Python Knowledge
- Terminal Basics

Check Python

```bash
python --version
```

or

```bash
python3 --version
```

______________________________________________________________________

# Create a Project

```bash
mkdir fastapi-course

cd fastapi-course
```

______________________________________________________________________

# Create Virtual Environment

Linux / macOS

```bash
python3 -m venv .venv
```

Windows

```bash
python -m venv .venv
```

Project

```
fastapi-course/

│

└── .venv/
```

______________________________________________________________________

# Why Virtual Environments?

Without a virtual environment

```
Python

↓

Global Packages

↓

Version Conflicts
```

Example

Project A

```
Pydantic v1
```

Project B

```
Pydantic v2
```

Conflict.

______________________________________________________________________

# Activate Virtual Environment

Linux / macOS

```bash
source .venv/bin/activate
```

Windows CMD

```cmd
.venv\Scripts\activate
```

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

When activated

```
(.venv)

$
```

appears in the terminal.

______________________________________________________________________

# Install FastAPI

```bash
pip install fastapi
```

______________________________________________________________________

# Install Uvicorn

```bash
pip install uvicorn
```

Uvicorn is the ASGI server that runs FastAPI applications.

______________________________________________________________________

# Install Together

Most developers install both.

```bash
pip install fastapi uvicorn
```

______________________________________________________________________

# Verify Installation

```bash
pip list
```

Example

```
fastapi

uvicorn

starlette

pydantic
```

______________________________________________________________________

# Freeze Dependencies

```bash
pip freeze > requirements.txt
```

Example

```
fastapi==...

uvicorn==...

pydantic==...
```

Install later

```bash
pip install -r requirements.txt
```

______________________________________________________________________

# Create First File

```
project/

│

└── main.py
```

______________________________________________________________________

# First FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():

    return {

        "message":

        "Hello FastAPI"

    }
```

______________________________________________________________________

# Running the Application

```bash
uvicorn main:app
```

Meaning

```
main

↓

Python Module
```

```
app

↓

FastAPI Object
```

______________________________________________________________________

# Server Starts

Example

```
INFO:

Uvicorn running on

http://127.0.0.1:8000
```

Visit

```
http://127.0.0.1:8000
```

Response

```json
{
    "message": "Hello FastAPI"
}
```

______________________________________________________________________

# Hot Reload

Development

```bash
uvicorn

main:app

--reload
```

Now every code change automatically restarts the server.

______________________________________________________________________

# Why Use --reload?

Without

```
Change Code

↓

Restart Server
```

With

```
Change Code

↓

Automatic Restart
```

Useful only during development.

______________________________________________________________________

# Interactive API Documentation

FastAPI automatically creates

Swagger UI

```
http://127.0.0.1:8000/docs
```

______________________________________________________________________

# ReDoc

Another documentation page

```
http://127.0.0.1:8000/redoc
```

Both are generated automatically.

______________________________________________________________________

# Directory Structure (Beginner)

```
project/

│

├── main.py

├── requirements.txt

└── .venv/
```

Suitable for learning.

______________________________________________________________________

# Recommended Structure (Small Project)

```
project/

│

├── app/

│     main.py

│

├── requirements.txt

│

├── .env

│

└── README.md
```

______________________________________________________________________

# Recommended Structure (Production)

```
project/

│

├── app/

│

│     main.py

│

│     api/

│

│     models/

│

│     schemas/

│

│     services/

│

│     repositories/

│

│     dependencies/

│

│     middleware/

│

│     core/

│

│     utils/

│

├── tests/

│

├── requirements.txt

│

├── Dockerfile

│

├── docker-compose.yml

│

└── .env
```

We'll build toward this structure throughout the course.

______________________________________________________________________

# What Does Each Folder Do?

```
api/

↓

Routes
```

```
schemas/

↓

Pydantic Models
```

```
models/

↓

Database Models
```

```
services/

↓

Business Logic
```

```
repositories/

↓

Database Operations
```

```
dependencies/

↓

Dependency Injection
```

```
middleware/

↓

Request Processing
```

```
core/

↓

Configuration

Security

Settings
```

```
utils/

↓

Helper Functions
```

______________________________________________________________________

# Development Workflow

```
Write Code

↓

Save File

↓

Reload

↓

Test API

↓

Repeat
```

______________________________________________________________________

# Installing Development Tools

Useful packages

```bash
pip install

black

isort

pytest

httpx
```

Purpose

- Black → Code Formatter
- isort → Import Sorting
- pytest → Testing
- httpx → HTTP Client

______________________________________________________________________

# Running on Another Port

```bash
uvicorn

main:app

--reload

--port 9000
```

Visit

```
http://127.0.0.1:9000
```

______________________________________________________________________

# Running on Another Host

```bash
uvicorn

main:app

--host 0.0.0.0

--port 8000
```

Useful for

- Docker
- Virtual Machines
- Remote Servers

______________________________________________________________________

# Production Server

Development

```bash
uvicorn

main:app

--reload
```

Production

```bash
gunicorn

-k uvicorn.workers.UvicornWorker

-w 4

main:app
```

We'll cover deployment in detail later.

______________________________________________________________________

# Dependency Management

Avoid

```
Install Random Packages
```

Instead

```
requirements.txt

↓

Version Controlled

↓

Reproducible Builds
```

______________________________________________________________________

# Common Mistakes

❌ Installing packages globally

❌ Forgetting virtual environments

❌ Running production with `--reload`

❌ Keeping all code inside `main.py`

❌ Not pinning dependency versions

❌ Committing `.venv` to Git

______________________________________________________________________

# .gitignore

Example

```text
.venv/

__pycache__/

.env

.pytest_cache/

*.pyc
```

Never commit

- Virtual environments
- Secrets
- Temporary files

______________________________________________________________________

# Production Best Practices

- Always use virtual environments.
- Pin dependency versions.
- Keep production and development dependencies organized.
- Use a modular project structure.
- Store secrets in environment variables.
- Never run Uvicorn with `--reload` in production.
- Commit `requirements.txt` to version control.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should every FastAPI project use a virtual environment?**

### Answer

A virtual environment isolates project dependencies from the global Python installation.

Benefits include:

- Prevents dependency conflicts between projects.
- Allows different projects to use different package versions.
- Makes deployments reproducible.
- Simplifies collaboration across development teams.
- Keeps the global Python installation clean.

Virtual environments are considered a standard Python development practice.

______________________________________________________________________

# Summary

In this chapter you learned:

- Installing FastAPI
- Installing Uvicorn
- Virtual Environments
- Running FastAPI
- Hot Reload
- Swagger UI
- ReDoc
- Project Structure
- Dependency Management
- Production Best Practices

A well-organized project and isolated dependency management provide the foundation for maintainable and production-ready
FastAPI applications.

______________________________________________________________________

# Practice Questions

## Installation

1. How do you install FastAPI?
1. Why is Uvicorn required?
1. How do you create a virtual environment?
1. Why should packages not be installed globally?

______________________________________________________________________

## Running Applications

5. What does `uvicorn main:app` mean?
1. What does the `--reload` flag do?
1. Why shouldn't `--reload` be used in production?

______________________________________________________________________

## Documentation

8. Where is Swagger UI available?
1. Where is ReDoc available?
1. Why are these documentation pages useful?

______________________________________________________________________

## Project Structure

11. Why shouldn't all code remain in `main.py`?
01. What belongs in the `services/` directory?
01. What belongs in the `schemas/` directory?
01. Why should dependencies be version-pinned?

______________________________________________________________________

## Production

15. Why should `.venv` never be committed to Git?
01. Why should `.env` files be excluded from version control?

______________________________________________________________________

## Scenario-Based

17. Two developers work on different FastAPI projects, but installing a package for one project breaks the other. What likely caused this issue?
01. Your application works locally but fails in production because different package versions were installed. How could `requirements.txt` have helped?
01. Your Docker container cannot access the FastAPI application from outside the container. Which Uvicorn option is commonly required to expose the application?
01. Your team has grown from one developer to twenty developers. How would a modular project structure improve maintainability and collaboration?

______________________________________________________________________

# Next

[FastAPI Application Lifecycle](03_application_lifecycle.md)
