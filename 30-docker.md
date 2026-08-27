# 30. Docker

**Previous:** [29. RabbitMQ & Celery](./29-rabbitmq-celery.md)

**Next:** [31. Linux for Backend Engineers](./31-linux.md)

______________________________________________________________________

## Objectives

By the end of this topic, you should be able to:

- Explain Docker images and containers.
- Understand how Dockerfiles build images.
- Explain image layers and caching.
- Write production-oriented Dockerfiles for Python/FastAPI applications.
- Use multi-stage builds to reduce image size.
- Understand Docker volumes and persistent data.
- Explain Docker networking.
- Configure environment variables safely.
- Understand Docker secrets and their limitations.
- Configure health checks.
- Understand container resource limits.
- Use Docker Compose for local multi-service development.
- Run FastAPI, PostgreSQL and Redis together.
- Debug common Docker problems.
- Discuss Docker trade-offs in backend interviews.

______________________________________________________________________

# 1. What Is Docker?

Docker is a containerization platform used to package and run applications in isolated environments.

Instead of installing an application and all of its dependencies directly on a host machine, Docker packages the
application and its runtime environment into an image.

A simplified model is:

```text
Dockerfile
    ↓
Docker Image
    ↓
Container
    ↓
Running Application
```

______________________________________________________________________

# 2. Why Docker?

Docker helps provide:

- Consistent development environments
- Reproducible application builds
- Dependency isolation
- Easier deployment
- Service isolation
- Portable application packaging

A common backend setup is:

```text
FastAPI container
PostgreSQL container
Redis container
```

Each service can have its own runtime and configuration.

______________________________________________________________________

# 3. Image vs Container

This is one of the most important Docker interview questions.

### Image

An image is a packaged, immutable template containing the application and its required filesystem/runtime components.

### Container

A container is a running instance of an image.

Conceptually:

```text
Image
 ├── Container 1
 ├── Container 2
 └── Container 3
```

One image can be used to create multiple containers.

______________________________________________________________________

# 4. Docker Image

An image contains filesystem layers needed to run an application.

For a Python application, an image may contain:

- Base operating-system files
- Python runtime
- Installed dependencies
- Application source
- Runtime configuration

Images are normally built from a Dockerfile or another image.

______________________________________________________________________

# 5. Container

A container provides an isolated process environment based on an image.

Important point:

> A container is not a lightweight virtual machine in the traditional sense.

Containers share the host kernel while providing process/filesystem/network isolation.

______________________________________________________________________

# 6. Container Lifecycle

A simplified lifecycle is:

```text
Image
  ↓
docker run
  ↓
Created
  ↓
Running
  ↓
Stopped
  ↓
Removed
```

A stopped container can retain its writable container filesystem until it is removed.

______________________________________________________________________

# 7. Dockerfile

A Dockerfile contains instructions for building an image.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

The Dockerfile describes the desired image construction process.

______________________________________________________________________

# 8. Common Dockerfile Instructions

Important instructions include:

- `FROM`
- `WORKDIR`
- `COPY`
- `ADD`
- `RUN`
- `CMD`
- `ENTRYPOINT`
- `ENV`
- `ARG`
- `EXPOSE`
- `USER`
- `HEALTHCHECK`

You should understand the difference between the commonly used instructions.

______________________________________________________________________

# 9. FROM

`FROM` specifies the base image.

Example:

```dockerfile
FROM python:3.12-slim
```

The base image becomes the starting point for the image's filesystem and runtime environment.

______________________________________________________________________

# 10. WORKDIR

`WORKDIR` sets the working directory for subsequent instructions and the container's default working directory.

Example:

```dockerfile
WORKDIR /app
```

It is generally preferable to explicitly set a working directory rather than relying on the image default.

______________________________________________________________________

# 11. COPY

`COPY` copies files from the build context into the image.

Example:

```dockerfile
COPY requirements.txt .
COPY app ./app
```

Prefer `COPY` when you simply need to copy files.

______________________________________________________________________

# 12. ADD

`ADD` can copy files and has additional behavior such as archive extraction.

For most application Dockerfiles, `COPY` is clearer and more predictable.

Use `ADD` only when its additional behavior is actually required.

______________________________________________________________________

# 13. RUN

`RUN` executes commands while building the image.

Example:

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

The resulting filesystem changes become part of the image.

______________________________________________________________________

# 14. CMD

`CMD` defines the default command used when a container starts.

Example:

```dockerfile
CMD ["uvicorn", "app.main:app"]
```

A Docker image can define a default command that can be overridden at runtime.

______________________________________________________________________

# 15. ENTRYPOINT

`ENTRYPOINT` defines the executable that the container is intended to run.

Example:

```dockerfile
ENTRYPOINT ["python"]
```

`CMD` can provide default arguments to an entrypoint.

A useful interview distinction:

> `ENTRYPOINT` defines the main executable behavior, while `CMD` commonly provides default command/arguments.

______________________________________________________________________

# 16. CMD vs ENTRYPOINT

Example:

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

The effective default execution is conceptually:

```text
python app.py
```

Runtime arguments can change how these interact.

For application containers, use the combination deliberately rather than adding `ENTRYPOINT` without understanding
override behavior.

______________________________________________________________________

# 17. ENV

`ENV` defines environment variables in the image/container environment.

Example:

```dockerfile
ENV PYTHONUNBUFFERED=1
```

Application configuration can also be supplied at runtime rather than baked into the image.

______________________________________________________________________

# 18. ARG

`ARG` defines build-time variables.

Example:

```dockerfile
ARG PYTHON_VERSION=3.12
```

A key distinction:

```text
ARG → build time
ENV → runtime environment
```

Do not use `ARG` as a secure mechanism for secrets.

______________________________________________________________________

# 19. EXPOSE

`EXPOSE` documents the port the application expects to use.

Example:

```dockerfile
EXPOSE 8000
```

Important:

> `EXPOSE` does not publish the port to the host by itself.

Port publishing is configured when the container is run or through orchestration/Compose configuration.

______________________________________________________________________

# 20. USER

A production container should generally avoid running the application as root when root privileges are unnecessary.

Example:

```dockerfile
RUN useradd --create-home appuser
USER appuser
```

This reduces the impact of some container-level security issues.

______________________________________________________________________

# 21. Docker Build Context

When running:

```bash
docker build .
```

the `.` represents the build context.

Files in the context can be copied into the image using `COPY`.

The build context can become unnecessarily large if it contains:

- `.git`
- Virtual environments
- Test artifacts
- Large datasets
- Local caches
- Build outputs

______________________________________________________________________

# 22. .dockerignore

Use `.dockerignore` to exclude unnecessary files from the build context.

Example:

```text
.git
.venv
__pycache__
*.pyc
.pytest_cache
.env
dist
build
```

This can improve build performance and prevent unnecessary files from being sent to the Docker daemon/build system.

______________________________________________________________________

# 23. Docker Image Layers

Docker images are composed of layers.

Each relevant Dockerfile instruction can contribute to the resulting image filesystem/layer structure.

Conceptually:

```text
Application Layer
Dependency Layer
Python Layer
Base Image
```

Layers enable caching and reuse.

______________________________________________________________________

# 24. Why Layers Matter

If a dependency-installation step has not changed, Docker can often reuse its cached result.

For example:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

Changing application source does not necessarily invalidate the dependency installation layer.

______________________________________________________________________

# 25. Poor Layer Ordering

This pattern is less efficient:

```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

Changing any application file can invalidate the layer containing dependency installation.

A better pattern is usually:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

This improves build-cache reuse.

______________________________________________________________________

# 26. Docker Build Cache

Docker can reuse previous build results when the relevant inputs have not changed.

Cache effectiveness depends on:

- Instruction ordering
- Files copied
- Build arguments
- Base image
- Command changes

Good Dockerfiles are designed to maximize useful cache reuse without sacrificing correctness.

______________________________________________________________________

# 27. Multi-Stage Builds

Multi-stage builds use multiple build stages in one Dockerfile.

Example:

```dockerfile
FROM python:3.12 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

CMD ["python", "app.py"]
```

The final image does not need to contain all build-stage tooling.

______________________________________________________________________

# 28. Why Multi-Stage Builds?

Benefits can include:

- Smaller final images
- Fewer build tools in production
- Reduced attack surface
- Cleaner separation between build and runtime

The exact implementation depends on the application's build requirements.

______________________________________________________________________

# 29. Python Multi-Stage Builds

For Python applications, multi-stage builds can be useful when dependencies require compilation.

For example:

```text
Builder
 ├── Compiler
 ├── Development libraries
 └── Build dependencies

Runtime
 ├── Python
 ├── Runtime libraries
 └── Application
```

The final runtime image can omit unnecessary compiler tooling.

______________________________________________________________________

# 30. Dependency Management

A Python container should install dependencies reproducibly.

Common approaches include:

```text
requirements.txt
pyproject.toml
lock files
```

Pinning or locking dependencies improves reproducibility.

______________________________________________________________________

# 31. Python Dependency Layer

A common pattern is:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
```

This separates relatively stable dependencies from frequently changing source code.

______________________________________________________________________

# 32. Docker Volumes

Containers have writable filesystems, but data written there is tied to the container lifecycle.

Volumes provide persistent storage outside the container's writable layer.

Conceptually:

```text
Container
   ↓
Volume
   ↓
Persistent data
```

______________________________________________________________________

# 33. Why Use Volumes?

Volumes are useful for stateful data such as:

- PostgreSQL data
- Redis data when persistence is required
- Uploaded files
- Application-generated persistent data

A container can be removed while the volume remains.

______________________________________________________________________

# 34. Bind Mounts vs Volumes

### Bind mount

Maps a host path into the container.

Useful for local development.

```text
Host directory
      ↓
Container directory
```

### Named volume

Managed by Docker and commonly used for persistent service data.

______________________________________________________________________

# 35. Development Bind Mount

For local FastAPI development:

```text
./app
  ↓
/app
```

This allows source changes on the host to be visible inside the container.

The application can run with a development reload mechanism.

______________________________________________________________________

# 36. Production Storage

For production databases, container-local writable storage should not be treated as durable application storage.

Use appropriate persistent storage provided by the deployment environment.

For PostgreSQL specifically, database durability must be designed independently of the application container lifecycle.

______________________________________________________________________

# 37. Docker Networking

Docker provides virtual networking between containers.

A user-defined Docker network allows containers to communicate using service/container names.

Conceptually:

```text
FastAPI
   ↓
postgres:5432

FastAPI
   ↓
redis:6379
```

The service name can act as the hostname within the Docker network.

______________________________________________________________________

# 38. localhost Inside a Container

This is a very common interview/debugging issue.

Inside a FastAPI container:

```text
localhost
```

refers to the FastAPI container itself.

It does not automatically refer to PostgreSQL or Redis.

For example, if PostgreSQL is another Compose service, the application typically connects using:

```text
postgres:5432
```

rather than:

```text
localhost:5432
```

______________________________________________________________________

# 39. Container Ports vs Host Ports

Suppose PostgreSQL listens on:

```text
5432
```

inside the container.

You can publish it as:

```text
15432:5432
```

This means:

```text
Host port 15432
        ↓
Container port 5432
```

Other containers on the same network can normally use the container/service port directly.

______________________________________________________________________

# 40. Port Publishing

Example:

```yaml
ports:
  - "8000:8000"
```

means:

```text
Host:8000
   ↓
Container:8000
```

Port publishing is primarily about exposing a container service outside its network.

______________________________________________________________________

# 41. Environment Variables

Environment variables are commonly used for runtime configuration.

Example:

```text
DATABASE_URL
REDIS_URL
JWT_SECRET
LOG_LEVEL
```

A FastAPI application can read these values from its environment.

______________________________________________________________________

# 42. Configuration vs Secrets

Not all configuration has the same sensitivity.

Examples:

```text
LOG_LEVEL=INFO
```

is generally configuration.

Whereas:

```text
DATABASE_PASSWORD=...
JWT_SECRET=...
```

is sensitive.

Sensitive values should be handled using appropriate secret-management mechanisms rather than committed to source
control.

______________________________________________________________________

# 43. .env Files

A `.env` file is convenient for local development.

Example:

```text
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

Do not commit real production credentials into `.env` files stored in source control.

Use:

```text
.env
```

in `.gitignore` where appropriate.

______________________________________________________________________

# 44. Docker Secrets

Docker and deployment platforms provide mechanisms for injecting sensitive data without putting secrets directly into
images.

The exact secret mechanism depends on how Docker is deployed.

Important principle:

> Secrets should not be baked into the image.

______________________________________________________________________

# 45. Secrets in Dockerfile

Avoid:

```dockerfile
ENV DATABASE_PASSWORD=my-secret
```

and:

```dockerfile
COPY .env .
```

for production credentials.

Once sensitive data is baked into an image layer, removing it from a later layer does not necessarily remove it from
image history.

______________________________________________________________________

# 46. Health Checks

A health check determines whether a containerized service is responding as expected.

Example:

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
```

The exact command depends on the image.

______________________________________________________________________

# 47. Liveness vs Readiness

These concepts are particularly important in production deployments.

### Liveness

Asks:

> Is the process alive?

### Readiness

Asks:

> Is the application ready to receive traffic?

An application can be alive but not ready.

______________________________________________________________________

# 48. FastAPI Health Endpoint

A simple endpoint might be:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

A more meaningful readiness check may verify critical dependencies, depending on the architecture.

Avoid making liveness checks depend on every external dependency.

______________________________________________________________________

# 49. Health Check Pitfall

Suppose:

```text
FastAPI
  ↓
PostgreSQL
```

If the database temporarily fails and the liveness check fails because it checks PostgreSQL, the orchestrator might
repeatedly restart a perfectly healthy application process.

Separate liveness and readiness semantics when appropriate.

______________________________________________________________________

# 50. Resource Limits

Containers can be constrained by:

- CPU
- Memory
- Other runtime resources depending on platform

Resource limits help prevent one service from consuming all host resources.

______________________________________________________________________

# 51. Why Resource Limits Matter

Suppose:

```text
Container A → memory leak
Container B → API
Container C → Redis
```

Without appropriate isolation/limits, Container A can negatively affect the host and other workloads.

Limits provide an important operational boundary.

______________________________________________________________________

# 52. CPU Limits

CPU constraints can prevent a container from consuming unlimited CPU resources.

The exact Docker/Compose syntax varies by deployment/runtime version.

The important interview concept is:

> Resource limits should match expected workload and service dependencies.

______________________________________________________________________

# 53. Memory Limits

Memory limits are particularly important for Python applications.

If a container exceeds its memory limit, the runtime may terminate the process/container depending on configuration and
environment.

Monitor memory behavior rather than choosing arbitrary limits.

______________________________________________________________________

# 54. Docker Compose

Docker Compose is useful for defining and running multi-container applications.

A typical local backend may include:

```text
FastAPI
PostgreSQL
Redis
```

A Compose file can define:

- Services
- Networks
- Volumes
- Environment
- Ports
- Health checks
- Dependencies

______________________________________________________________________

# 55. Example Compose Architecture

```text
┌──────────────┐
│   FastAPI    │
└──────┬───────┘
       │
 ┌─────┴─────┐
 ↓           ↓
PostgreSQL  Redis
```

All services can communicate over a shared Compose network.

______________________________________________________________________

# 56. Example Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://app:password@postgres:5432/app
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7

volumes:
  postgres_data:
```

This is suitable as a learning/development example. Production credentials and deployment configuration should be
handled more securely.

______________________________________________________________________

# 57. FastAPI Dockerfile

A simple development-oriented example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

______________________________________________________________________

# 58. Why Bind to 0.0.0.0?

Inside a container, binding only to:

```text
127.0.0.1
```

can make the application inaccessible from outside the container.

For a server intended to receive traffic through the container network, use an appropriate bind address such as:

```text
0.0.0.0
```

______________________________________________________________________

# 59. Docker Compose Service Discovery

Given:

```yaml
services:
  api:
    ...
  postgres:
    ...
```

the API container can generally reach PostgreSQL using:

```text
postgres
```

as the hostname on the shared Compose network.

This is a major practical difference from local development where applications often use `localhost`.

______________________________________________________________________

# 60. depends_on

`depends_on` expresses service startup/dependency relationships.

However:

> `depends_on` does not automatically mean that the dependency is ready to accept requests.

For robust startup behavior, use health checks and application-level retry/readiness logic where appropriate.

______________________________________________________________________

# 61. Startup Race Condition

Example:

```text
Compose starts API
        ↓
API immediately connects to PostgreSQL
        ↓
PostgreSQL still initializing
        ↓
Connection fails
```

A robust application should tolerate dependency startup timing rather than assuming that container start means service
readiness.

______________________________________________________________________

# 62. Debugging Containers

Common commands include:

```bash
docker ps
docker ps -a
docker images
docker logs <container>
docker inspect <container>
docker exec -it <container> sh
docker network ls
docker volume ls
```

Know what each command is useful for.

______________________________________________________________________

# 63. docker ps

Shows running containers.

```bash
docker ps
```

Useful for checking:

- Container status
- Ports
- Names
- IDs

______________________________________________________________________

# 64. docker ps -a

Shows running and stopped containers.

Useful when a container starts and immediately exits.

______________________________________________________________________

# 65. docker logs

Use:

```bash
docker logs <container>
```

to inspect application/container output.

For a FastAPI service that immediately exits, logs are one of the first places to investigate.

______________________________________________________________________

# 66. docker exec

Use:

```bash
docker exec -it <container> sh
```

to enter a running container.

This is useful for debugging:

- Files
- Environment variables
- Network connectivity
- Installed packages
- Process state

______________________________________________________________________

# 67. Debugging "Container Exits Immediately"

Check:

1. Container logs.
1. Command/CMD.
1. Entrypoint.
1. Environment variables.
1. Application startup exception.
1. Working directory.
1. Missing files/dependencies.

A container exits when its main process exits.

______________________________________________________________________

# 68. Debugging "Cannot Connect to PostgreSQL"

Check:

```text
Is PostgreSQL running?
       ↓
Correct hostname?
       ↓
Correct port?
       ↓
Correct credentials?
       ↓
Same Docker network?
       ↓
Is PostgreSQL ready?
       ↓
Firewall/network configuration?
```

Inside Compose, the database hostname is typically the service name, not `localhost`.

______________________________________________________________________

# 69. Debugging "Port Already in Use"

If:

```text
8000:8000
```

fails because host port 8000 is occupied, use another host port:

```text
8001:8000
```

The application can still listen on 8000 inside the container.

______________________________________________________________________

# 70. Debugging Build Problems

Check:

- Build context
- `.dockerignore`
- `COPY` paths
- Dependency files
- Python version
- OS-level dependencies
- Build cache

A common mistake is assuming a host-installed dependency is automatically available inside the image.

______________________________________________________________________

# 71. Debugging Environment Variables

Inside the container:

```bash
docker exec -it <container> env
```

can help inspect environment configuration.

Do not expose sensitive production secrets in logs or diagnostic output.

______________________________________________________________________

# 72. Debugging Network Connectivity

Useful checks include:

```bash
docker network ls
docker inspect <container>
```

Then verify:

- Network membership
- Service names
- Ports
- Application bind address

A network issue should be diagnosed separately from an application-level authentication issue.

______________________________________________________________________

# 73. Docker Security Basics

Important practices:

- Do not run as root unnecessarily.
- Do not bake secrets into images.
- Use trusted/minimal base images.
- Keep dependencies updated.
- Use `.dockerignore`.
- Avoid unnecessary packages.
- Scan images where appropriate.
- Limit container resources.
- Expose only required ports.

______________________________________________________________________

# 74. Minimal Base Images

Examples include:

```text
python:slim
```

or other appropriately maintained minimal images.

Smaller images can reduce:

- Download time
- Storage
- Attack surface

But overly minimal images can make debugging or dependency installation harder.

Choose a practical base image.

______________________________________________________________________

# 75. Docker Image Tagging

Avoid relying blindly on:

```text
latest
```

for reproducible deployments.

Use explicit versions/tags where appropriate.

For production systems, image immutability and traceability are important.

______________________________________________________________________

# 76. Image Immutability

A useful deployment principle is:

```text
Build once
   ↓
Test image
   ↓
Deploy same image
```

Do not modify the running container manually and expect the change to become the new deployment artifact.

Instead:

```text
Change source
 ↓
Build new image
 ↓
Test
 ↓
Deploy
```

______________________________________________________________________

# 77. Docker and CI/CD

A common pipeline is:

```text
Git push
  ↓
CI
  ↓
Run tests
  ↓
Build image
  ↓
Scan image
  ↓
Push image registry
  ↓
Deploy
```

The exact deployment platform can vary.

______________________________________________________________________

# 78. Docker Image Registry

A registry stores container images.

Examples include:

- Docker Hub
- Private organizational registries
- Cloud container registries

The important concept is:

```text
Build
 ↓
Registry
 ↓
Deployment environment
```

______________________________________________________________________

# 79. Production FastAPI Container

A production-oriented container should consider:

- Non-root user
- Minimal runtime image
- Pinned dependencies
- Proper process command
- Health checks
- Logging to stdout/stderr
- Runtime configuration
- Resource limits
- Graceful shutdown
- Security updates

______________________________________________________________________

# 80. Logging in Containers

Containers should generally write application logs to:

```text
stdout
stderr
```

rather than depending on application-local log files inside the ephemeral container filesystem.

The container platform can then collect and centralize logs.

______________________________________________________________________

# 81. Graceful Shutdown

When a container is stopped, the application may receive a termination signal.

A production FastAPI deployment should allow the application server and application to shut down gracefully:

```text
Termination signal
       ↓
Stop accepting new work
       ↓
Finish/close active work where appropriate
       ↓
Close resources
       ↓
Exit
```

This becomes particularly important for database connections, background tasks and message consumers.

______________________________________________________________________

# 82. Docker vs Virtual Machine

### Virtual machine

Typically virtualizes a complete operating system environment.

### Container

Shares the host kernel while isolating processes and filesystem/network resources.

Containers generally have less overhead than full VMs, but they are not a replacement for every VM use case.

______________________________________________________________________

# 83. Docker Networking Interview Model

Know these concepts:

```text
Bridge/network
Container IP
Service name
Port publishing
Container port
Host port
DNS/service discovery
```

The most common practical issue is confusing:

```text
localhost
```

with:

```text
service name
```

inside a container network.

______________________________________________________________________

# 84. Common Dockerfile Improvements

### Basic

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production considerations

Add where appropriate:

```text
Non-root user
Multi-stage build
Pinned dependencies
Health check
Minimal files
Proper logging
Runtime configuration
```

______________________________________________________________________

# 85. Docker Anti-Patterns

## Anti-pattern 1 — Baking secrets into images

Bad:

```dockerfile
ENV PASSWORD=secret
```

## Anti-pattern 2 — Copying everything

Bad:

```dockerfile
COPY . .
```

without a `.dockerignore` and without considering what enters the image.

## Anti-pattern 3 — Running as root unnecessarily

Use a non-root user where practical.

## Anti-pattern 4 — Huge images

Installing compilers/build tools into the final runtime image when they are not required increases size and attack
surface.

## Anti-pattern 5 — Treating container filesystem as durable storage

Containers are replaceable runtime units.

## Anti-pattern 6 — Using localhost for other services

Inside a container, `localhost` refers to that container.

## Anti-pattern 7 — Assuming depends_on means ready

Startup ordering is not equivalent to dependency readiness.

______________________________________________________________________

# 86. Interview Questions & Answers

## Q1. What is Docker?

**Answer:**

Docker is a containerization platform used to package and run applications in isolated, reproducible environments.

______________________________________________________________________

## Q2. What is the difference between an image and a container?

**Answer:**

An image is an immutable packaged template. A container is a running instance of that image.

______________________________________________________________________

## Q3. Is a container a VM?

**Answer:**

No. Containers share the host kernel while providing process, filesystem and network isolation. A VM typically includes
a complete guest operating system.

______________________________________________________________________

## Q4. What is a Dockerfile?

**Answer:**

A Dockerfile is a set of instructions used to build a Docker image.

______________________________________________________________________

## Q5. What is `FROM`?

**Answer:**

It specifies the base image from which the image build starts.

______________________________________________________________________

## Q6. What is `RUN`?

**Answer:**

`RUN` executes a command during image construction and records its resulting filesystem changes in the image.

______________________________________________________________________

## Q7. What is `COPY`?

**Answer:**

`COPY` copies files from the build context into the image.

______________________________________________________________________

## Q8. COPY vs ADD?

**Answer:**

`ADD` provides additional behavior such as archive extraction, while `COPY` is simpler and generally preferred when
straightforward file copying is all that is required.

______________________________________________________________________

## Q9. What is `CMD`?

**Answer:**

`CMD` defines the default command or arguments used when a container starts.

______________________________________________________________________

## Q10. What is `ENTRYPOINT`?

**Answer:**

`ENTRYPOINT` defines the main executable behavior of a container. `CMD` can commonly provide default arguments.

______________________________________________________________________

## Q11. CMD vs ENTRYPOINT?

**Answer:**

`ENTRYPOINT` is generally used for the main executable, while `CMD` provides defaults that can be overridden. They can
also be combined to create an executable plus default arguments.

______________________________________________________________________

## Q12. What is `WORKDIR`?

**Answer:**

It sets the working directory for subsequent Dockerfile instructions and the default working directory when the
container runs.

______________________________________________________________________

## Q13. What is `EXPOSE`?

**Answer:**

It documents the port an application expects to use. It does not itself publish that port to the host.

______________________________________________________________________

## Q14. What is `.dockerignore`?

**Answer:**

It excludes unnecessary files from the Docker build context, reducing build overhead and helping prevent unwanted files
from entering the image.

______________________________________________________________________

## Q15. What are Docker layers?

**Answer:**

Docker images are built from filesystem layers associated with image construction steps. Layers allow reuse and build
caching.

______________________________________________________________________

## Q16. Why does Dockerfile ordering matter?

**Answer:**

Changing an earlier instruction or its inputs can invalidate later cache layers. Putting stable dependency installation
before frequently changing application source can improve cache reuse.

______________________________________________________________________

## Q17. What is a multi-stage build?

**Answer:**

A Dockerfile with multiple build stages that allows build-time tools and artifacts to be separated from the final
runtime image.

______________________________________________________________________

## Q18. Why use multi-stage builds?

**Answer:**

To reduce final image size, remove unnecessary build tooling and reduce the production attack surface.

______________________________________________________________________

## Q19. What is a Docker volume?

**Answer:**

A Docker-managed persistent storage mechanism that allows data to survive container replacement.

______________________________________________________________________

## Q20. Volume vs bind mount?

**Answer:**

A volume is managed by Docker, while a bind mount maps a specific host path into the container. Bind mounts are common
in development; volumes are often useful for persistent service data.

______________________________________________________________________

## Q21. What is Docker networking?

**Answer:**

Docker networking allows containers to communicate over isolated virtual networks and provides mechanisms such as
service-name-based discovery.

______________________________________________________________________

## Q22. Why does `localhost` cause problems in Docker?

**Answer:**

Inside a container, `localhost` refers to the container itself, not another container such as PostgreSQL or Redis.

______________________________________________________________________

## Q23. How does FastAPI connect to PostgreSQL in Docker Compose?

**Answer:**

If the services share a Compose network and PostgreSQL is named `postgres`, the application would typically connect to
`postgres:5432`, not `localhost:5432`.

______________________________________________________________________

## Q24. What is port mapping?

**Answer:**

It maps a host port to a container port, for example `8000:8000`.

______________________________________________________________________

## Q25. What is the difference between container and host ports?

**Answer:**

The container port is where the application listens inside the container. The host port is the port exposed on the host
that forwards traffic to the container port.

______________________________________________________________________

## Q26. What is Docker Compose?

**Answer:**

Docker Compose is a tool for defining and running multi-container applications using a declarative configuration file.

______________________________________________________________________

## Q27. Why use Docker Compose for FastAPI development?

**Answer:**

It allows FastAPI, PostgreSQL, Redis and other services to be defined and started together with consistent networking,
environment and volume configuration.

______________________________________________________________________

## Q28. Does `depends_on` mean the database is ready?

**Answer:**

No. It can establish startup dependency ordering, but service startup does not necessarily mean the dependency is ready
to accept requests.

______________________________________________________________________

## Q29. How do you handle startup races?

**Answer:**

Use health checks/readiness mechanisms and application-level retry logic where appropriate rather than assuming
dependency startup means readiness.

______________________________________________________________________

## Q30. How do you store secrets in Docker?

**Answer:**

Do not bake secrets into images or source control. Inject them through appropriate runtime secret/configuration
mechanisms provided by the deployment environment.

______________________________________________________________________

## Q31. Why should secrets not be placed in a Dockerfile?

**Answer:**

Image layers and build history can retain sensitive data even if later instructions remove it.

______________________________________________________________________

## Q32. What is a Docker health check?

**Answer:**

A health check periodically verifies whether a service is responding according to a configured health command.

______________________________________________________________________

## Q33. Liveness vs readiness?

**Answer:**

Liveness asks whether the process is alive. Readiness asks whether it is ready to receive traffic.

______________________________________________________________________

## Q34. Why should liveness not always check the database?

**Answer:**

A temporary database outage should not necessarily cause the application process to be restarted. Readiness and liveness
have different purposes.

______________________________________________________________________

## Q35. Why use container resource limits?

**Answer:**

To prevent a single workload from consuming excessive host resources and affecting other services.

______________________________________________________________________

## Q36. What happens if a container exceeds its memory limit?

**Answer:**

The runtime/environment can terminate the process or container depending on the configured limits and platform behavior.

______________________________________________________________________

## Q37. Why run containers as non-root?

**Answer:**

It reduces privileges and limits the potential impact of a container compromise.

______________________________________________________________________

## Q38. Why use `0.0.0.0` for FastAPI inside Docker?

**Answer:**

It allows the application to listen on the container's network interfaces so traffic can reach it through Docker
networking and published ports.

______________________________________________________________________

## Q39. How would you debug a container that exits immediately?

**Answer:**

Check `docker ps -a`, inspect `docker logs`, verify the command/entrypoint, environment variables, working directory,
files, dependencies and application startup errors.

______________________________________________________________________

## Q40. How would you debug API-to-PostgreSQL connectivity?

**Answer:**

Verify both containers are running, check their network membership, use the PostgreSQL service name rather than
`localhost`, verify the port and credentials, and confirm PostgreSQL is ready.

______________________________________________________________________

## Q41. How would you reduce Docker image size?

**Answer:**

Use a suitable minimal base image, multi-stage builds, `.dockerignore`, avoid unnecessary packages and keep build-only
dependencies out of the final image.

______________________________________________________________________

## Q42. Why pin Python dependencies?

**Answer:**

Pinned or locked dependencies improve build reproducibility and reduce unexpected changes between builds.

______________________________________________________________________

## Q43. Why avoid `latest` in production?

**Answer:**

A moving tag can point to different image versions over time, reducing deployment reproducibility and traceability.

______________________________________________________________________

## Q44. Where should application logs go in containers?

**Answer:**

Generally stdout/stderr so the container platform can collect and centralize them rather than relying on ephemeral files
inside the container.

______________________________________________________________________

## Q45. What happens when the container's main process exits?

**Answer:**

The container stops. A container's lifecycle is tied to its main process.

______________________________________________________________________

## Q46. How do containers communicate?

**Answer:**

Through Docker networks. On user-defined networks and Compose networks, service/container names can be used for service
discovery.

______________________________________________________________________

## Q47. How would you design a production FastAPI Docker image?

**Answer:**

Use a minimal maintained base image, reproducible dependencies, a non-root user, a clean build context, multi-stage
builds where useful, runtime configuration through the environment/secret mechanism, appropriate health checks and a
correct application server command.

______________________________________________________________________

## Q48. What is the Docker build context?

**Answer:**

The set of files available to the Docker build. It is determined by the path supplied to the build command and can be
reduced using `.dockerignore`.

______________________________________________________________________

## Q49. Why is `.dockerignore` important?

**Answer:**

It reduces build context size, improves build performance and helps prevent unnecessary or sensitive local files from
being included.

______________________________________________________________________

## Q50. Give a senior-level Docker answer.

**Answer:**

"I treat containers as immutable, replaceable application runtime units. I build reproducible images with pinned
dependencies, use sensible layer ordering for cache reuse, multi-stage builds when they reduce the runtime image, and
avoid baking secrets into images. For FastAPI I expose the appropriate application port, bind to the container network
interface, run with least privilege, emit logs to stdout/stderr and define meaningful health checks. For local
development I use Compose to run FastAPI, PostgreSQL and Redis on a shared network, using service names for
communication and volumes for persistent database data. In production I also consider resource limits, graceful
shutdown, image scanning, registry traceability and the deployment platform's persistent-storage and secret-management
mechanisms."

______________________________________________________________________

# 87. Scenario-Based Questions

## Scenario 1 — FastAPI Cannot Connect to PostgreSQL

Your Compose setup contains:

```text
api
postgres
```

The application uses:

```text
localhost:5432
```

and fails.

**Answer:**

Inside the API container, `localhost` refers to the API container. Use the PostgreSQL Compose service name, for example:

```text
postgres:5432
```

assuming both services share the same network.

______________________________________________________________________

## Scenario 2 — API Container Starts Before PostgreSQL

The API immediately attempts a database connection and fails because PostgreSQL is still initializing.

**Answer:**

Do not rely solely on `depends_on`. Add appropriate health/readiness checks and application-level retry behavior.

______________________________________________________________________

## Scenario 3 — Container Uses Too Much Memory

A Python worker gradually consumes memory until the host becomes unstable.

**Answer:**

Investigate the application's memory behavior, configure an appropriate container memory limit and monitor the service.
Resource limits provide isolation but do not fix the underlying leak.

______________________________________________________________________

## Scenario 4 — Docker Image Is 2 GB

The application is a small FastAPI service.

**Answer:**

Inspect image layers and dependencies. Use `.dockerignore`, a suitable slim runtime image, remove unnecessary packages
and use a multi-stage build if build tooling is responsible for image size.

______________________________________________________________________

## Scenario 5 — Secret Appears in Git

A developer commits:

```text
.env
```

containing database credentials.

**Answer:**

Treat the secret as compromised: rotate it, remove it from source-control history as appropriate, add `.env` to
`.gitignore`, and use runtime secret injection.

______________________________________________________________________

## Scenario 6 — Container Works Locally but Not in Production

The image starts but requests fail.

**Answer:**

Check:

- Application bind address
- Port mapping
- Environment variables
- Secrets
- Network configuration
- Dependency connectivity
- Health/readiness behavior
- Logs

Do not assume the application code is the only possible failure point.

______________________________________________________________________

## Scenario 7 — Database Data Disappears

A PostgreSQL container is removed and its data disappears.

**Answer:**

The database was relying on container-local storage. Use a persistent volume or the deployment environment's appropriate
persistent storage mechanism.

______________________________________________________________________

## Scenario 8 — Health Check Causes Restart Loop

The FastAPI health check fails whenever PostgreSQL is unavailable, causing the container to restart continuously.

**Answer:**

Separate liveness and readiness semantics. A temporary dependency outage should generally make the application unready
rather than necessarily indicate that the process itself is dead.

______________________________________________________________________

## Scenario 9 — Docker Build Is Slow

Every small source change causes dependencies to reinstall.

**Answer:**

Review Dockerfile layer ordering. Copy stable dependency files and install dependencies before copying frequently
changing application source.

______________________________________________________________________

## Scenario 10 — Database Overloaded

Increasing API container replicas causes PostgreSQL to become overloaded.

**Answer:**

Application scaling and database capacity must be considered together. Add appropriate connection-pool limits, optimize
queries, control application concurrency and scale the database appropriately rather than blindly adding containers.

______________________________________________________________________

# 88. Practice Exercises

## Exercise 1 — Basic FastAPI Image

Create a Dockerfile for:

```text
FastAPI
Python 3.12
Uvicorn
```

Run it and expose port 8000.

______________________________________________________________________

## Exercise 2 — Add PostgreSQL

Create a Compose setup containing:

```text
FastAPI
PostgreSQL
```

Configure FastAPI to connect using:

```text
postgres
```

as the hostname.

______________________________________________________________________

## Exercise 3 — Add Redis

Extend the Compose setup:

```text
FastAPI
PostgreSQL
Redis
```

Connect FastAPI to Redis using:

```text
redis
```

as the hostname.

______________________________________________________________________

## Exercise 4 — Persistent PostgreSQL

Add a named volume:

```text
postgres_data
```

Destroy/recreate the PostgreSQL container and verify that database data remains.

______________________________________________________________________

## Exercise 5 — Layer Optimization

Build two Dockerfiles:

### Version A

```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

### Version B

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Change application source and compare build behavior.

______________________________________________________________________

## Exercise 6 — Multi-Stage Build

Create a multi-stage Python image where build dependencies exist only in the builder stage.

Compare final image sizes.

______________________________________________________________________

## Exercise 7 — Non-Root User

Run the FastAPI application as a non-root user.

Verify the process user inside the container.

______________________________________________________________________

## Exercise 8 — Health Check

Add:

```text
GET /health
```

and configure a container health check.

Test healthy and unhealthy states.

______________________________________________________________________

## Exercise 9 — Resource Limits

Run a CPU/memory-intensive test container.

Experiment with resource limits and observe the behavior.

______________________________________________________________________

## Exercise 10 — Docker Networking

Create two containers and verify communication using a Docker network.

Demonstrate why:

```text
localhost
```

does not refer to the other container.

______________________________________________________________________

## Exercise 11 — Debug a Broken Container

Create a deliberately broken container with:

- Incorrect command
- Missing environment variable
- Missing dependency

Use:

```bash
docker ps -a
docker logs
docker inspect
docker exec
```

to diagnose the problem.

______________________________________________________________________

## Exercise 12 — Startup Race

Configure FastAPI to connect to PostgreSQL during startup.

Make PostgreSQL initialization slow enough to expose the race.

Implement appropriate retry/readiness handling.

______________________________________________________________________

## Exercise 13 — Secret Handling

Remove credentials from the Dockerfile and source code.

Configure them through runtime environment/secret mechanisms.

______________________________________________________________________

## Exercise 14 — Production Dockerfile

Create a production-oriented FastAPI image with:

- Slim base image
- Pinned dependencies
- Non-root user
- `.dockerignore`
- Health check
- Correct application command

______________________________________________________________________

## Exercise 15 — Senior Design

Design:

```text
FastAPI
PostgreSQL
Redis
Celery
RabbitMQ
```

using Docker Compose for development.

Explain:

- Network design
- Volumes
- Environment variables
- Secrets
- Health checks
- Startup dependencies
- Resource limits
- Logging
- Graceful shutdown
- Debugging strategy

______________________________________________________________________

# 89. Quick Revision

| Concept | Key Point |
|---|---|
| Docker | Containerization platform |
| Image | Immutable packaged template |
| Container | Running instance of an image |
| Dockerfile | Image build instructions |
| `FROM` | Base image |
| `WORKDIR` | Working directory |
| `COPY` | Copy build-context files |
| `ADD` | Copy plus additional behavior |
| `RUN` | Build-time command |
| `CMD` | Default runtime command/arguments |
| `ENTRYPOINT` | Main executable behavior |
| `ENV` | Runtime environment variable |
| `ARG` | Build-time variable |
| `EXPOSE` | Documents container port |
| `USER` | Runtime user |
| Build context | Files available to build |
| `.dockerignore` | Excludes files from context |
| Layer | Image filesystem/build unit |
| Build cache | Reuses unchanged build results |
| Multi-stage | Separates build and runtime stages |
| Volume | Docker-managed persistent storage |
| Bind mount | Host path mounted into container |
| Network | Container communication mechanism |
| Service name | Common Compose network hostname |
| `localhost` | Current container/host context |
| Port mapping | Host port → container port |
| Environment variable | Runtime configuration |
| Secret | Sensitive runtime data |
| Health check | Service health verification |
| Liveness | Process alive |
| Readiness | Ready for traffic |
| Resource limit | CPU/memory boundary |
| Compose | Multi-container application definition |
| `depends_on` | Startup dependency relationship |
| Non-root | Reduced container privilege |
| Registry | Stores container images |
| Immutable image | Build/test/deploy same artifact |
| Container logs | Usually stdout/stderr |
| Graceful shutdown | Controlled application termination |

______________________________________________________________________

# 90. Completion Checklist

Before moving to File 31, make sure you can explain:

- [ ] Docker purpose
- [ ] Image vs container
- [ ] Container vs VM
- [ ] Dockerfile
- [ ] `FROM`
- [ ] `WORKDIR`
- [ ] `COPY`
- [ ] `ADD`
- [ ] `RUN`
- [ ] `CMD`
- [ ] `ENTRYPOINT`
- [ ] `CMD` vs `ENTRYPOINT`
- [ ] `ENV`
- [ ] `ARG`
- [ ] `EXPOSE`
- [ ] `USER`
- [ ] Build context
- [ ] `.dockerignore`
- [ ] Image layers
- [ ] Build cache
- [ ] Dockerfile layer ordering
- [ ] Multi-stage builds
- [ ] Python dependency packaging
- [ ] Volumes
- [ ] Bind mounts
- [ ] Container networking
- [ ] Service discovery
- [ ] `localhost` behavior
- [ ] Container vs host ports
- [ ] Environment variables
- [ ] Secret handling
- [ ] Docker secrets concept
- [ ] Health checks
- [ ] Liveness
- [ ] Readiness
- [ ] Resource limits
- [ ] Docker Compose
- [ ] FastAPI/PostgreSQL/Redis Compose setup
- [ ] `depends_on`
- [ ] Startup races
- [ ] Docker debugging
- [ ] Container logs
- [ ] `docker exec`
- [ ] Network debugging
- [ ] Volume debugging
- [ ] Container security
- [ ] Minimal images
- [ ] Image tagging
- [ ] Image immutability
- [ ] CI/CD image flow
- [ ] Container registry
- [ ] Production FastAPI container
- [ ] Container logging
- [ ] Graceful shutdown

______________________________________________________________________

# 91. Interview Readiness Test

Answer these aloud without looking at the notes:

1. What is Docker?
1. Image vs container?
1. Is a container a VM?
1. What is a Dockerfile?
1. Explain `FROM`.
1. Explain `RUN`.
1. Explain `COPY`.
1. COPY vs ADD?
1. Explain `CMD`.
1. Explain `ENTRYPOINT`.
1. CMD vs ENTRYPOINT?
1. What is WORKDIR?
1. What is EXPOSE?
1. What is ARG?
1. ARG vs ENV?
1. What is `.dockerignore`?
1. What is the Docker build context?
1. What are Docker image layers?
1. Why does Dockerfile instruction ordering matter?
1. What is Docker build cache?
1. What is a multi-stage build?
1. Why use multi-stage builds for Python?
1. What is a Docker volume?
1. Volume vs bind mount?
1. How does Docker networking work?
1. Why is localhost problematic inside containers?
1. How does FastAPI connect to PostgreSQL in Compose?
1. What is the difference between container and host ports?
1. What is an environment variable?
1. How should secrets be handled?
1. Why should secrets not be baked into images?
1. What is a health check?
1. Liveness vs readiness?
1. Why should liveness not always depend on PostgreSQL?
1. Why use resource limits?
1. What happens when memory limits are exceeded?
1. What is Docker Compose?
1. How would you run FastAPI + PostgreSQL + Redis?
1. Does `depends_on` mean PostgreSQL is ready?
1. How would you solve startup races?
1. How would you debug a container that exits immediately?
1. How would you debug API-to-PostgreSQL connectivity?
1. How would you debug a port conflict?
1. How would you reduce image size?
1. Why use a slim base image?
1. Why run as a non-root user?
1. Why pin dependencies?
1. Why avoid `latest` in production?
1. Where should container logs go?
1. What happens when the main container process exits?
1. How do containers discover each other?
1. How would you design a production FastAPI Docker image?
1. How would you handle persistent PostgreSQL storage?
1. How would you make Docker builds faster?
1. Give a senior-level Docker architecture answer.

______________________________________________________________________

# 92. Final Senior Interview Scenario

You are responsible for containerizing a Python backend:

```text
FastAPI
PostgreSQL
Redis
Celery
RabbitMQ
```

The application must support local development and production deployment.

Design the Docker setup.

Your answer should cover:

1. Dockerfile structure.
1. Image layers.
1. Dependency caching.
1. Multi-stage builds.
1. `.dockerignore`.
1. Non-root execution.
1. Environment configuration.
1. Secret management.
1. Docker networking.
1. Service discovery.
1. Port publishing.
1. PostgreSQL persistence.
1. Redis persistence requirements.
1. Health checks.
1. Liveness/readiness.
1. Startup dependencies.
1. Resource limits.
1. Logging.
1. Graceful shutdown.
1. Image tagging.
1. Registry flow.
1. CI/CD.
1. Debugging strategy.
1. Security.
1. Reproducibility.

A strong senior answer should make the key architectural distinction:

> **Containers are replaceable runtime units; images are immutable deployment artifacts; persistent business data belongs in appropriate persistent storage; configuration and secrets should be supplied at runtime rather than baked into images.**

______________________________________________________________________

**Previous:** [29. RabbitMQ & Celery](./29-rabbitmq-celery.md)

**Next:** [31. Linux for Backend Engineers](./31-linux.md)
