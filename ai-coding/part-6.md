# AI Assisted Development Guide - Part 3

# Advanced Context Engineering & Token Optimization

> **Audience:** Software Engineers building medium to large software projects with AI coding assistants.

This guide explains how experienced engineers structure repositories and workflows to reduce token usage, improve response quality, and keep AI assistants productive over long-running projects.

---

# Table of Contents

1. Context Engineering
2. How AI Uses Context
3. Context Layers
4. Stable vs Dynamic Context
5. Token Optimization
6. Repository Design
7. AI Development Workflows
8. Large Project Strategy
9. Documentation Strategy
10. Context Anti-Patterns
11. Future of AI Development

---

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

---

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

---

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

---

# 3. Context Layers

Layer 1

Prompt

Example

```text
Implement startup synchronization.
```

---

Layer 2

Instruction Files

Examples

```text
CLAUDE.md

copilot-instructions.md
```

---

Layer 3

Repository Documentation

Examples

```text
architecture.md

worker.md

protocol.md
```

---

Layer 4

Source Code

Relevant

Classes

Functions

Modules

---

Layer 5

Current Conversation

Recent discussions

Current design

Current feature

---

# 4. Stable vs Dynamic Context

One of the biggest mistakes is mixing these.

---

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

---

## Dynamic Context

Changes frequently.

Examples

Current task

Current bug

Current feature

Current branch

Current discussion

These belong in the conversation.

---

# Rule

Never put temporary information into permanent documentation.

---

# 5. Token Optimization

Most developers try to reduce tokens by shortening prompts.

Experienced teams reduce tokens by improving repositories.

---

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

---

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

---

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

---

## Rule 4

Use one responsibility per document.

One document

One purpose.

---

## Rule 5

Summarize major discussions.

Instead of

20 conversations,

create

```text
Feature Summary
```

Future AI sessions become dramatically cheaper.

---

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

---

## Rule 7

Use examples.

AI understands examples better than abstract descriptions.

---

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

---

## Rule 9

Avoid duplicate documentation.

One source of truth.

---

## Rule 10

Document interfaces.

Instead of documenting implementation,

document

Responsibilities

Inputs

Outputs

Guarantees

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

Emerging trends include

* Context Engineering
* Retrieval-Augmented Development
* Agentic coding workflows
* Repository memory
* Model Context Protocol (MCP)
* Multi-agent software engineering

The repository itself is becoming the primary source of truth, with prompts serving mainly to express the immediate task.

---

# Practical Checklist

## Repository

* [ ] Modular documentation
* [ ] Architecture diagrams
* [ ] ADRs
* [ ] Examples
* [ ] Tests
* [ ] Consistent naming

## Prompts

* [ ] Focused on one task
* [ ] Do not repeat architecture
* [ ] Do not paste large files
* [ ] Reference documentation when appropriate

## Documentation

* [ ] One topic per document
* [ ] No duplication
* [ ] Updated after architectural changes
* [ ] Includes examples where useful

---

# Key Takeaways

1. Optimize the repository before optimizing prompts.
2. Keep permanent knowledge in documentation, not in conversations.
3. Separate stable context from dynamic context.
4. Prefer many focused documents over a few large ones.
5. Use Architecture Decision Records to preserve design rationale.
6. Let AI retrieve context instead of manually providing it.
7. Build repositories that are easy for both humans and AI to understand.

A well-designed repository can reduce prompt size dramatically, improve consistency across AI sessions, and make long-term software development significantly more efficient.

## Next
[AI Tool Ecosystem & Choosing the Right Tool](part-7.md)
