# AI Assisted Development Guide - Part 3

# Advanced Context Engineering & Token Optimization

> **Audience:** Software Engineers building medium to large software projects with AI coding assistants.

This guide explains how experienced engineers structure repositories and workflows to reduce token usage, improve
response quality, and keep AI assistants productive over long-running projects.

______________________________________________________________________

# Table of Contents

1. Context Engineering
1. How AI Uses Context
1. Context Layers
1. Stable vs Dynamic Context
1. Token Optimization
1. Repository Design
1. AI Development Workflows
1. Large Project Strategy
1. Documentation Strategy
1. Context Anti-Patterns
1. Future of AI Development

______________________________________________________________________

# 1. What is Context Engineering?

Prompt Engineering is about writing better prompts.

Context Engineering is about giving the AI the **right information** before it even reads your prompt.

Modern AI development has shifted toward Context Engineering.

Instead of writing:

```text
Implement startup synchronization.

Remember:
- Use logger
- Use f-strings
- Use retry logic
- Never poll
- Use WorkerState
- Follow architecture
```

You simply write:

```text
Implement startup synchronization.
```

Everything else already exists inside the repository.

______________________________________________________________________

# Prompt vs Context

Prompt Engineering

```text
Large Prompt

↓

Small Repository
```

Context Engineering

```text
Small Prompt

↓

Rich Repository
```

Context Engineering scales much better.

______________________________________________________________________

# 2. How AI Uses Context

Think of AI context as layers.

```text
Developer Prompt

        │

        ▼

Current Conversation

        │

        ▼

Instruction Files

        │

        ▼

Repository Docs

        │

        ▼

Relevant Code

        │

        ▼

Generated Response
```

Notice

The prompt is actually one of the smallest parts.

______________________________________________________________________

# 3. Context Layers

Layer 1

Prompt

Example

```text
Implement startup synchronization.
```

______________________________________________________________________

Layer 2

Instruction Files

Examples

```text
CLAUDE.md

copilot-instructions.md
```

______________________________________________________________________

Layer 3

Repository Documentation

Examples

```text
architecture.md

worker.md

protocol.md
```

______________________________________________________________________

Layer 4

Source Code

Relevant

Classes

Functions

Modules

______________________________________________________________________

Layer 5

Current Conversation

Recent discussions

Current design

Current feature

______________________________________________________________________

# 4. Stable vs Dynamic Context

One of the biggest mistakes is mixing these.

______________________________________________________________________

## Stable Context

Changes rarely.

Examples

Architecture

Coding standards

Naming conventions

Constraints

Technology stack

Testing strategy

Deployment strategy

Store these inside the repository.

______________________________________________________________________

## Dynamic Context

Changes frequently.

Examples

Current task

Current bug

Current feature

Current branch

Current discussion

These belong in the conversation.

______________________________________________________________________

# Rule

Never put temporary information into permanent documentation.

______________________________________________________________________

# 5. Token Optimization

Most developers try to reduce tokens by shortening prompts.

Experienced teams reduce tokens by improving repositories.

______________________________________________________________________

## Rule 1

Never repeat architecture.

Reference it.

Bad

```text
Architecture...

Manager...

Worker...

Protocol...
```

Good

```text
Implement startup synchronization.
```

______________________________________________________________________

## Rule 2

Never paste large files.

Bad

```python
worker.py

1000 lines
```

Good

```text
Review ReplicaWorker.notify().
```

______________________________________________________________________

## Rule 3

Keep documentation modular.

Good

```text
worker.md

manager.md

protocol.md
```

Bad

```text
Architecture.md

5000 lines
```

______________________________________________________________________

## Rule 4

Use one responsibility per document.

One document

One purpose.

______________________________________________________________________

## Rule 5

Summarize major discussions.

Instead of

20 conversations,

create

```text
Feature Summary
```

Future AI sessions become dramatically cheaper.

______________________________________________________________________

## Rule 6

Store architectural decisions.

Don't repeatedly explain

Why Event?

Why Threads?

Why Retry?

Instead

```text
docs/decisions.md
```

______________________________________________________________________

## Rule 7

Use examples.

AI understands examples better than abstract descriptions.

______________________________________________________________________

## Rule 8

Keep naming consistent.

Bad

```text
Worker

Processor

Consumer

Listener
```

Good

```text
Worker
```

everywhere.

______________________________________________________________________

## Rule 9

Avoid duplicate documentation.

One source of truth.

______________________________________________________________________

## Rule 10

Document interfaces.

Instead of documenting implementation,

document

Responsibilities

Inputs

Outputs

Guarantees

______________________________________________________________________

# 6. Repository Design

Bad

```text
src/

everything.py
```

Good

```text
replication/

worker.py

manager.py

protocol.py

storage.py
```

Smaller modules improve AI retrieval.

______________________________________________________________________

# Feature-Based Organization

Instead of

```text
models/

services/

utils/
```

consider

```text
authentication/

replication/

deployment/

monitoring/
```

AI understands features better than arbitrary folders.

______________________________________________________________________

# 7. AI Development Workflow

Recommended

```text
Requirements

↓

Architecture

↓

Implementation

↓

Review

↓

Tests

↓

Documentation

↓

Commit
```

Do not jump directly into coding.

______________________________________________________________________

# Feature Workflow

```text
Idea

↓

Design

↓

Implementation

↓

Testing

↓

Documentation

↓

Optimization
```

______________________________________________________________________

# Bug Fix Workflow

```text
Bug

↓

Reproduce

↓

Root Cause

↓

Fix

↓

Tests

↓

Documentation
```

______________________________________________________________________

# Refactoring Workflow

```text
Understand

↓

Design

↓

Refactor

↓

Tests

↓

Review
```

______________________________________________________________________

# Architecture Workflow

```text
Problem

↓

Options

↓

Trade-offs

↓

Decision

↓

Implementation
```

Document the decision.

______________________________________________________________________

# 8. Large Project Strategy

Small Project

```text
README

Architecture

Source
```

Medium Project

```text
README

Architecture

Feature Docs

Tests

Examples
```

Enterprise

```text
README

Architecture

Subsystem Docs

Decision Records

Examples

Deployment

Operations

Monitoring
```

______________________________________________________________________

# Documentation Hierarchy

```text
README

        │

        ▼

Architecture

        │

        ▼

Subsystem

        │

        ▼

Feature

        │

        ▼

Implementation
```

Never skip levels.

______________________________________________________________________

# 9. Context Anti-Patterns

❌ Huge prompts

❌ Huge README

❌ Huge CLAUDE.md

❌ Repeating architecture

❌ Duplicate docs

❌ Mixing temporary work

❌ No ADR

❌ Huge modules

❌ Poor naming

______________________________________________________________________

# 10. Future of AI Development

The industry is moving toward

Repository-first AI.

Instead of

Prompt

↓

AI

It becomes

Repository

↓

Retriever

↓

AI

↓

Developer

______________________________________________________________________

Emerging trends include

- Context Engineering
- Retrieval-Augmented Development
- Agentic coding workflows
- Repository memory
- Model Context Protocol (MCP)
- Multi-agent software engineering

The repository itself is becoming the primary source of truth, with prompts serving mainly to express the immediate
task.

______________________________________________________________________

# Practical Checklist

## Repository

- [ ] Modular documentation
- [ ] Architecture diagrams
- [ ] ADRs
- [ ] Examples
- [ ] Tests
- [ ] Consistent naming

## Prompts

- [ ] Focused on one task
- [ ] Do not repeat architecture
- [ ] Do not paste large files
- [ ] Reference documentation when appropriate

## Documentation

- [ ] One topic per document
- [ ] No duplication
- [ ] Updated after architectural changes
- [ ] Includes examples where useful

______________________________________________________________________

# Key Takeaways

1. Optimize the repository before optimizing prompts.
1. Keep permanent knowledge in documentation, not in conversations.
1. Separate stable context from dynamic context.
1. Prefer many focused documents over a few large ones.
1. Use Architecture Decision Records to preserve design rationale.
1. Let AI retrieve context instead of manually providing it.
1. Build repositories that are easy for both humans and AI to understand.

A well-designed repository can reduce prompt size dramatically, improve consistency across AI sessions, and make
long-term software development significantly more efficient.

## Next

[AI Tool Ecosystem & Choosing the Right Tool](part-7.md)
