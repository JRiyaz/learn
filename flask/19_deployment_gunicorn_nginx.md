# Deploying Flask with Gunicorn & Nginx

> **Course:** Flask for Backend Engineers
>
> **Module:** 9
>
> **File:** `19_deployment_gunicorn_nginx.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Flask's Development Server Should Not Be Used
- What Gunicorn Is
- What Nginx Is
- Reverse Proxy
- WSGI
- Request Flow
- Static File Serving
- HTTPS
- Process Management
- Deployment Architecture
- Production Best Practices

______________________________________________________________________

# Why Can't We Use Flask's Built-in Server?

Most beginners start applications like this.

```python
app.run(
    debug=True
)
```

or

```bash
flask run
```

This server is designed **only for development**.

It is **not** suitable for production because it lacks:

- Performance optimizations
- Process management
- Security hardening
- Efficient concurrency
- Production-grade request handling

______________________________________________________________________

# Production Architecture

Instead of

```
Browser

↓

Flask
```

Use

```
Browser

↓

Nginx

↓

Gunicorn

↓

Flask
```

This is one of the most common deployment architectures.

______________________________________________________________________

# What is WSGI?

WSGI

\=

**Web Server Gateway Interface**

It is a standard that allows Python web applications to communicate with web servers.

```
Browser

↓

Web Server

↓

WSGI Server

↓

Flask
```

Gunicorn is a WSGI server.

______________________________________________________________________

# What is Gunicorn?

Gunicorn

\=

**Green Unicorn**

A production-ready WSGI server for Python applications.

Responsibilities

- Run multiple worker processes
- Accept HTTP requests from Nginx
- Execute Flask application code
- Return responses

______________________________________________________________________

# Why Gunicorn?

Benefits

- Multiple workers
- Stable production performance
- Graceful worker restarts
- Better concurrency
- Easy deployment

______________________________________________________________________

# Install Gunicorn

```bash
pip install gunicorn
```

______________________________________________________________________

# Running Gunicorn

Example

```bash
gunicorn app:app
```

Meaning

```
module

:

Flask App
```

Application Factory

```bash
gunicorn "app:create_app()"
```

______________________________________________________________________

# Multiple Workers

Example

```bash
gunicorn

-w 4

app:app
```

Flow

```
Requests

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

Multiple workers improve throughput on multi-core systems.

______________________________________________________________________

# Worker Types

Common worker classes

- Sync (default)
- Gevent
- Eventlet
- Uvicorn Worker (for ASGI apps)

The appropriate worker type depends on the application's workload.

______________________________________________________________________

# What is Nginx?

Nginx is a high-performance web server and reverse proxy.

Responsibilities

- Accept client connections
- Serve static files
- Handle HTTPS
- Load balance requests
- Forward requests to Gunicorn

______________________________________________________________________

# Reverse Proxy

```
Browser

↓

Nginx

↓

Gunicorn

↓

Flask
```

Clients communicate with Nginx,

not directly with Gunicorn.

______________________________________________________________________

# Why Use Nginx?

Benefits

- Very fast static file serving
- SSL/TLS termination
- Compression
- Caching
- Load balancing
- Security features

______________________________________________________________________

# Request Flow

```
Browser

↓

HTTPS

↓

Nginx

↓

Gunicorn

↓

Flask

↓

Database
```

Response

```
Database

↓

Flask

↓

Gunicorn

↓

Nginx

↓

Browser
```

______________________________________________________________________

# Static Files

Instead of

```
Browser

↓

Flask

↓

logo.png
```

Use

```
Browser

↓

Nginx

↓

logo.png
```

Nginx is optimized for serving static content.

______________________________________________________________________

# HTTPS

Nginx commonly terminates TLS.

```
Browser

↓

HTTPS

↓

Nginx

↓

HTTP

↓

Gunicorn
```

The internal connection is often protected by the private network.

______________________________________________________________________

# Basic Nginx Configuration

Example

```nginx
server {

    listen 80;

    server_name example.com;

    location / {

        proxy_pass http://127.0.0.1:8000;

    }
}
```

This forwards requests to Gunicorn.

______________________________________________________________________

# Serving Static Files

Example

```nginx
location /static/ {

    alias /var/www/app/static/;

}
```

Requests for static assets never reach Flask.

______________________________________________________________________

# Process Management

Gunicorn processes should be managed by a service manager.

Common choices

- systemd
- Supervisor

This enables

- Automatic restart
- Startup on boot
- Monitoring

______________________________________________________________________

# Example systemd Flow

```
Linux Starts

↓

systemd

↓

Gunicorn

↓

Flask
```

If Gunicorn crashes,

systemd can restart it.

______________________________________________________________________

# Logging

Nginx

↓

Access Logs

Error Logs

Gunicorn

↓

Application Logs

Flask

↓

Business Logs

Each layer provides different diagnostic information.

______________________________________________________________________

# Scaling

One Server

```
Nginx

↓

Gunicorn

↓

Flask
```

Multiple Servers

```
Load Balancer

↓

Nginx

↓

Gunicorn

↓

Flask

↓

Database
```

Applications can scale horizontally.

______________________________________________________________________

# Deployment Flow

```
Git Pull

↓

Install Dependencies

↓

Run Migrations

↓

Restart Gunicorn

↓

Application Live
```

Deployments should be automated where possible.

______________________________________________________________________

# Health Checks

Load balancers and orchestration platforms often call

```
GET /health
```

Example response

```json
{
    "status": "healthy"
}
```

Health endpoints help detect unhealthy instances.

______________________________________________________________________

# Environment Variables

Production configuration should use

```
Environment Variables
```

instead of hardcoded values.

Examples

- Database URL
- Secret Key
- Redis URL

______________________________________________________________________

# Common Mistakes

❌ Using `flask run` in production

❌ Serving static files through Flask

❌ Running a single Gunicorn worker on a multi-core server

❌ Enabling debug mode

❌ Running without HTTPS

❌ Not using a process manager

______________________________________________________________________

# Production Best Practices

- Deploy behind Nginx.
- Use Gunicorn as the WSGI server.
- Configure multiple workers.
- Serve static files through Nginx.
- Enable HTTPS.
- Use environment variables.
- Use a process manager.
- Automate deployments.
- Expose health check endpoints.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is Nginx placed in front of Gunicorn instead of exposing Gunicorn directly to the internet?**

### Answer

Nginx provides capabilities that Gunicorn is not primarily designed to handle efficiently.

These include:

1. Serving static files.
1. SSL/TLS termination.
1. Request buffering.
1. Load balancing.
1. Compression.
1. Security features.
1. Rate limiting (when configured).

Gunicorn focuses on executing Python application code, while Nginx efficiently handles client-facing web server
responsibilities.

This separation improves scalability, security, and performance.

______________________________________________________________________

# Summary

In this chapter you learned:

- WSGI
- Gunicorn
- Nginx
- Reverse Proxy
- Static File Serving
- HTTPS
- Worker Processes
- Process Management
- Deployment Architecture
- Production Best Practices

Deploying Flask with Gunicorn and Nginx is one of the most widely used production architectures for Python web
applications.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. Why should `flask run` not be used in production?
1. What is WSGI?
1. What is Gunicorn?
1. What is Nginx?

______________________________________________________________________

## Architecture

5. Why is Nginx placed in front of Gunicorn?
1. What is a reverse proxy?
1. Why should static files be served by Nginx?

______________________________________________________________________

## Gunicorn

8. Why run multiple Gunicorn workers?
1. What responsibilities does Gunicorn handle?
1. Why is a process manager useful?

______________________________________________________________________

## Production

11. Why should HTTPS terminate at Nginx?
01. Why should environment variables be used?
01. Why are health check endpoints important?

______________________________________________________________________

## Scaling

14. How does the deployment architecture change when scaling to multiple application servers?
01. Why should deployments be automated?

______________________________________________________________________

## Scenario-Based

16. Your Flask application is deployed using `flask run` on a public server. What risks and limitations does this introduce?
01. Users report that image downloads are slow because every request reaches Flask. How would you redesign the deployment?
01. Your Gunicorn process crashes unexpectedly at 3:00 AM. How can `systemd` help improve reliability?
01. A security audit finds that Gunicorn is directly exposed to the internet without Nginx. What features and protections are missing?
01. Your production server has 8 CPU cores, but Gunicorn is configured with only one worker. What performance implications might this have?

______________________________________________________________________

# Next

[Dockerizing Flask Applications](20_docker_flask.md)
