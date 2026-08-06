# Flask Introduction

> **Course:** Flask for Backend Engineers
>
> **Module:** 1
>
> **File:** `01_flask_introduction.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Flask is
- Why Flask was created
- When to use Flask
- Flask Architecture
- Flask Request Lifecycle
- WSGI
- Werkzeug
- Jinja2
- Installation
- Project Structure
- Running Flask Applications
- Production Overview

______________________________________________________________________

# What is Flask?

**Flask** is a lightweight Python web framework used to build:

- REST APIs
- Backend Services
- Web Applications
- Microservices

Flask provides only the essentials required to build web applications.

Unlike larger frameworks, Flask lets you choose which libraries and tools you want to use.

______________________________________________________________________

# Why Was Flask Created?

Imagine writing a web server from scratch.

```
Socket

↓

Parse HTTP

↓

Routing

↓

Request Parsing

↓

Response Formatting
```

This is a lot of work.

Flask provides all of these capabilities while remaining small and flexible.

______________________________________________________________________

# Real World Analogy

Imagine building a house.

Option 1

```
Buy Every Brick

↓

Build Everything Yourself
```

Option 2

```
Buy a Basic House

↓

Customize It
```

Flask is the second option.

It provides the basic structure while allowing you to customize almost everything.

______________________________________________________________________

# Why is Flask Called a "Micro" Framework?

"Micro" does **not** mean small applications.

It means Flask only includes the core functionality.

Included:

- Routing
- Request Handling
- Response Handling
- Development Server
- Template Engine

Not included by default:

- Authentication
- Database ORM
- Background Jobs
- Admin Panel

You choose the additional libraries you need.

______________________________________________________________________

# What Can Flask Build?

Flask is commonly used for:

- REST APIs
- Authentication Services
- Internal Tools
- Dashboards
- Microservices
- AI/ML APIs
- Backend Systems

Large companies have successfully used Flask in production.

______________________________________________________________________

# Flask Architecture

```
Client

↓

HTTP Request

↓

Flask

↓

Route

↓

Business Logic

↓

Database

↓

Response
```

Flask sits between the client and your application logic.

______________________________________________________________________

# Flask Request Lifecycle

```
Browser

↓

HTTP Request

↓

Flask

↓

URL Routing

↓

View Function

↓

Business Logic

↓

Response Object

↓

HTTP Response
```

Every request follows this flow.

______________________________________________________________________

# What is WSGI?

WSGI stands for

**Web Server Gateway Interface**

It is the standard interface between:

```
Web Server

↓

Python Application
```

Flask is a WSGI application.

Production servers such as Gunicorn use WSGI to communicate with Flask.

______________________________________________________________________

# What is Werkzeug?

Werkzeug is the library that powers much of Flask.

It provides:

- Routing
- Request Objects
- Response Objects
- URL Handling
- Development Server
- Debug Utilities

Flask is built on top of Werkzeug.

______________________________________________________________________

# What is Jinja2?

Jinja2 is Flask's template engine.

Example

```
User

↓

Flask

↓

Jinja2

↓

HTML Page
```

Although many backend engineers primarily build APIs, Jinja2 remains useful for server-rendered applications.

______________________________________________________________________

# Installing Flask

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install Flask.

```bash
pip install flask
```

Verify installation.

```bash
python -c "import flask; print(flask.__version__)"
```

______________________________________________________________________

# Your First Flask Application

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

______________________________________________________________________

# Running the Application

```bash
python app.py
```

Output

```
Running on:

http://127.0.0.1:5000
```

Visit

```
http://localhost:5000
```

Browser

↓

```
Hello, Flask!
```

______________________________________________________________________

# How Flask Works

When a request arrives

```
GET /

↓

Flask

↓

Find Matching Route

↓

Execute Function

↓

Return Response
```

______________________________________________________________________

# Minimal Project Structure

```
project/

│

├── app.py

├── requirements.txt

└── venv/
```

As applications grow, this structure evolves into packages, blueprints, and configuration modules.

______________________________________________________________________

# Development Server

The built-in Flask server is intended for development.

Advantages

- Simple
- Automatic reload
- Debug mode

Limitations

- Not optimized for production
- Not designed for high concurrency

Production deployments typically use Gunicorn behind Nginx or another reverse proxy.

______________________________________________________________________

# Flask in Production

Typical production architecture

```
Client

↓

Nginx

↓

Gunicorn

↓

Flask

↓

PostgreSQL
```

This architecture is covered later in the course.

______________________________________________________________________

# Common Mistakes

❌ Running the development server in production

❌ Hardcoding configuration values

❌ Ignoring virtual environments

❌ Putting all code into one file

❌ Mixing business logic directly inside route functions

______________________________________________________________________

# Production Best Practices

- Use virtual environments.
- Separate configuration from code.
- Keep business logic outside routes.
- Structure applications using Blueprints.
- Use Gunicorn in production.
- Store dependencies in `requirements.txt`.
- Use environment variables for secrets.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is Flask called a micro framework? Does that mean it is only suitable for small applications?**

### Answer

Flask is called a micro framework because it includes only the core functionality required to build web applications,
such as routing, request handling, and response generation.

It intentionally does not include components like an ORM, authentication, or an admin interface by default.

This does **not** limit Flask to small applications. Many production systems and microservices use Flask successfully
because developers can add only the libraries they need, keeping applications lightweight and flexible.

______________________________________________________________________

# Summary

In this chapter you learned:

- What Flask is
- Why Flask exists
- Flask Architecture
- Request Lifecycle
- WSGI
- Werkzeug
- Jinja2
- Installation
- First Flask Application
- Development vs Production

Flask provides a simple but powerful foundation for building modern Python web applications and APIs.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Flask?
1. Why was Flask created?
1. Why is Flask called a micro framework?
1. What kinds of applications are commonly built with Flask?

______________________________________________________________________

## Architecture

5. Explain the Flask request lifecycle.
1. What is WSGI?
1. What is Werkzeug?
1. What is Jinja2?

______________________________________________________________________

## Development

9. How do you install Flask?
1. Why should you use a virtual environment?
1. Why shouldn't the built-in development server be used in production?

______________________________________________________________________

## Scenario-Based

12. A Flask application grows to several thousand lines in a single file. What architectural improvements would you recommend?
01. A team deploys Flask using `app.run()` in production. What problems could this cause?
01. Your application requires authentication and database support. How does Flask's micro-framework philosophy influence your design choices?

______________________________________________________________________

# Next

[Flask Routing](02_flask_routing.md)
