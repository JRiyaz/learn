# AI Assisted Development Guide - Part 8

# Model Context Protocol (MCP) Complete Guide

> **Audience:** Software Engineers, AI Engineers, and Tool Developers

This guide explains what the **Model Context Protocol (MCP)** is, why it was created, how it works internally, and how
you can use it in your own projects.

______________________________________________________________________

# Table of Contents

1. What is MCP?
1. Why MCP Was Created
1. Problems Before MCP
1. MCP Architecture
1. MCP Components
1. Resources
1. Tools
1. Prompts
1. MCP Client
1. MCP Server
1. Transport Layer
1. Python Example
1. Repository Structure
1. Best Practices
1. Future of MCP

______________________________________________________________________

# 1. What is MCP?

**Model Context Protocol (MCP)** is an **open protocol** that standardizes how AI models interact with external systems.

Think of MCP as:

> **USB-C for AI applications**

Instead of every AI tool implementing its own custom integrations for Git, databases, cloud services, documentation, or
file systems, MCP defines a common protocol.

Without MCP

```text id="yq0oxv"
Claude

↓

Custom Git API

↓

Custom Database API

↓

Custom Filesystem API
```

Every AI assistant builds everything separately.

With MCP

```text id="6j7bz9"
Claude

↓

MCP

↓

Git

Database

Filesystem

Slack

GitHub

Jira
```

One protocol.

Many integrations.

______________________________________________________________________

# 2. Why Was MCP Created?

Before MCP every AI application had to implement

- Git
- GitHub
- Filesystem
- PostgreSQL
- MySQL
- Slack
- Jira
- Docker
- Kubernetes

individually.

Every AI tool duplicated work.

______________________________________________________________________

Example

```text id="fh95sy"
Claude Code

↓

Git Integration
```

```text id="t6g0xv"
Cursor

↓

Git Integration
```

```text id="gnxz4k"
Codex

↓

Git Integration
```

Three different implementations.

______________________________________________________________________

MCP solves this.

```text id="ljz4lf"
Git MCP Server

↓

Any AI Tool
```

______________________________________________________________________

# 3. High-Level Architecture

```text id="j2mvlw"
                 AI Assistant

                      │

                      ▼

                 MCP Client

                      │

═══════════════════════════════════════

                MCP Protocol

═══════════════════════════════════════

                      │

                      ▼

                 MCP Server

        ┌──────────┼──────────┐

        ▼          ▼          ▼

     GitHub     PostgreSQL   Filesystem
```

______________________________________________________________________

# 4. MCP Components

There are four major components.

## AI Application

Examples

- Claude Code
- Cursor
- VS Code extensions
- Desktop AI apps

______________________________________________________________________

## MCP Client

Lives inside the AI application.

Responsibilities

- Connect to servers
- Send requests
- Receive responses
- Maintain sessions

______________________________________________________________________

## MCP Server

Provides capabilities.

Example

Filesystem Server

Git Server

Database Server

Browser Server

______________________________________________________________________

## External System

Actual resource.

Example

Git repository

Database

Operating System

Slack Workspace

______________________________________________________________________

# 5. Resources

Resources are **read-only context**.

Think

> Documentation.

Examples

```
README.md

architecture.md

worker.py

settings.json

logs.txt
```

A model can request

```text id="xyxjcl"
Read

README.md
```

The server returns

the content.

______________________________________________________________________

Example

```
docs/

↓

MCP Resource

↓

Claude
```

Resources provide information.

They do not perform actions.

______________________________________________________________________

# 6. Tools

Tools perform actions.

Examples

```
Run Tests

Create File

Delete File

Commit Git

Restart Docker

Run Ruff

Execute SQL
```

Unlike resources,

tools change something.

Example

```
Claude

↓

Tool

↓

git commit
```

______________________________________________________________________

Example Tool

```
run_tests()

↓

pytest
```

______________________________________________________________________

# 7. Prompts

MCP also allows reusable prompts.

Instead of writing

```
Review this architecture...
```

every time,

an MCP server can expose

```
Architecture Review
```

prompt.

Think of prompts as reusable templates.

______________________________________________________________________

# 8. Resources vs Tools

| Resource | Tool |
| ------------- | ---------------- |
| Read-only | Performs actions |
| Documentation | Execute commands |
| Source code | Git operations |
| Configuration | Run tests |
| Architecture | Deploy |

Simple rule

Resources

→ Information

Tools

→ Actions

______________________________________________________________________

# 9. MCP Client

Lives inside the AI application.

Responsibilities

- Connect

- Authenticate

- Discover servers

- Read resources

- Invoke tools

- Handle responses

Example

```
Claude Code

↓

MCP Client

↓

Filesystem Server
```

______________________________________________________________________

# 10. MCP Server

Server exposes

Resources

Tools

Prompts

Example

```
Filesystem Server

Resources

README.md

worker.py

Tools

write_file()

delete_file()

mkdir()
```

______________________________________________________________________

# 11. Communication Flow

Developer

↓

Claude

↓

MCP Client

↓

Filesystem Server

↓

Read File

↓

Return Content

↓

Claude Responds

______________________________________________________________________

# Tool Flow

Developer

↓

Claude

↓

MCP Tool

↓

Run Ruff

↓

Return Output

↓

Claude

______________________________________________________________________

# 12. Transport Layer

MCP doesn't force one transport.

Common transports

- Standard Input / Output (stdio)
- HTTP
- WebSocket

Most local development uses

```
stdio
```

Cloud services often use

HTTP.

______________________________________________________________________

# 13. Python Example

A minimal MCP server conceptually looks like:

```python id="kqdfc8"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool()
def hello(name: str) -> str:
    return f"Hello {name}"


@mcp.resource("docs://readme")
def readme() -> str:
    return "# My Project"


if __name__ == "__main__":
    mcp.run()
```

This exposes

- one tool
- one resource

to any MCP-compatible client.

______________________________________________________________________

# 14. Repository Structure

Example

```text id="mg5pzt"
project/

src/

docs/

mcp/

server.py

tools.py

resources.py

prompts.py
```

Large projects

```text id="frivj0"
mcp/

filesystem/

git/

database/

docker/

github/
```

Each server

one responsibility.

______________________________________________________________________

# 15. Practical Examples

Filesystem Server

Resources

```
README.md

Architecture.md

worker.py
```

Tools

```
write_file()

delete_file()

rename()
```

______________________________________________________________________

Git Server

Resources

```
Current Branch

Commit History
```

Tools

```
git status

git add

git commit

git checkout
```

______________________________________________________________________

Database Server

Resources

```
Schema

Tables

Views
```

Tools

```
Run Query

Create Table

Migration
```

______________________________________________________________________

CI/CD Server

Resources

```
Pipeline Status

Logs
```

Tools

```
Run Pipeline

Cancel Pipeline

Restart Job
```

______________________________________________________________________

# 16. How Claude Uses MCP

Typical flow

```text id="hyzkp5"
Developer

↓

"Fix failing tests."

↓

Claude

↓

Discover Tools

↓

Run pytest

↓

Read Output

↓

Modify Code

↓

Run pytest Again

↓

Respond
```

Notice

The model never directly executes commands.

Everything goes through MCP.

______________________________________________________________________

# 17. Best Practices

## One Responsibility Per Server

Good

```
Filesystem

Git

Database
```

Bad

```
Everything Server
```

______________________________________________________________________

## Resources Should Be Read-Only

Don't modify files

inside resources.

Use tools instead.

______________________________________________________________________

## Small Tools

Good

```
run_tests()

format_code()

commit_changes()
```

Bad

```
build_everything_and_deploy()
```

______________________________________________________________________

## Small Resources

Expose

```
README

Architecture

API Docs
```

instead of

```
Entire Repository
```

______________________________________________________________________

## Keep Servers Stateless

Whenever possible,

don't store session state.

This makes servers easier to scale and debug.

______________________________________________________________________

# 18. Security

MCP servers may expose powerful capabilities.

Examples

```
Delete Files

Execute Shell Commands

Database Access

Cloud APIs
```

Always:

- Validate inputs.
- Limit permissions.
- Avoid exposing dangerous operations unnecessarily.
- Follow the principle of least privilege.

______________________________________________________________________

# 19. Why MCP Matters

Without MCP

Every AI tool builds

its own integrations.

With MCP

Every AI tool speaks

the same language.

Benefits

- Reusable integrations
- Easier maintenance
- Better interoperability
- Less duplicated effort

______________________________________________________________________

# 20. Future of MCP

MCP is becoming a common integration layer for AI applications.

As adoption grows, you can expect:

- More reusable MCP servers.
- More IDE support.
- Better interoperability between AI assistants.
- Easier access to development tools, documentation, and infrastructure.

______________________________________________________________________

# Final Takeaways

- **MCP is a protocol, not an AI model.**
- **Resources** provide information.
- **Tools** perform actions.
- **Prompts** provide reusable templates.
- **Clients** consume MCP services.
- **Servers** expose capabilities.
- Multiple AI assistants can use the same MCP server without custom integrations.

Think of MCP as the standard communication layer that allows AI assistants to interact with external systems in a
consistent and reusable way, much like HTTP standardized communication for web applications.
