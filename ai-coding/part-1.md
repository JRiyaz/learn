# AI Assisted Development Guide - Part 1

## Repository Structure & AI-Friendly Project Organization

> **Scope**
>
> This document explains how to organize a software project so modern AI coding assistants can understand it efficiently while minimizing token usage.
>
> This part is **AI tool independent** and applies to almost every coding assistant.

______________________________________________________________________

# Table of Contents

1. Introduction
1. Prompt Engineering vs Context Engineering
1. Goals of an AI-Friendly Repository
1. Recommended Repository Structure
1. Common Repository Files
1. Documentation Structure
1. Architecture Documentation
1. Design Decision Records
1. Best Practices
1. Token Optimization Techniques
1. Common Mistakes
1. Repository Checklist

______________________________________________________________________

# 1. Introduction

Modern AI coding assistants no longer rely only on your prompt.

Instead they understand:

- Repository structure
- Documentation
- Source code
- Build files
- Configuration
- Previous conversations
- Project instructions

A well-organized repository provides better AI-generated code than a poorly documented repository.

Think of documentation as giving AI permanent memory.

______________________________________________________________________

# Prompt Engineering vs Context Engineering

Traditionally developers focused on writing better prompts.

Example:

```text
Implement startup synchronization.

Use logger.
Use f-strings.
Use typing.
Don't poll.
Follow architecture.
Use retry logic.
```

Every prompt repeats the same information.

Modern AI development focuses on **Context Engineering**.

Instead:

```text
Implement startup synchronization.
```

The AI already understands:

- architecture
- coding conventions
- constraints
- documentation
- repository layout

because the project has been organized correctly.

This reduces:

- prompt size
- token consumption
- repeated explanations
- inconsistencies

______________________________________________________________________

# 2. Goals of an AI-Friendly Repository

An AI-friendly repository should provide:

✓ Clear architecture

✓ Modular documentation

✓ Coding standards

✓ Design decisions

✓ Testing guidelines

✓ Deployment instructions

✓ Small independent documents

✓ Easy navigation

______________________________________________________________________

# 3. Repository Structure

Recommended layout:

```text
project/
│
├── README.md
│
├── docs/
│   ├── architecture.md
│   ├── coding-guidelines.md
│   ├── protocol.md
│   ├── deployment.md
│   ├── testing.md
│   ├── troubleshooting.md
│   ├── decisions.md
│   ├── worker.md
│   └── manager.md
│
├── src/
│
├── tests/
│
├── scripts/
│
├── examples/
│
└── configs/
```

______________________________________________________________________

Repository overview

```
                 Repository
                      │
      ┌───────────────┼───────────────┐
      │               │               │
   Source          Documentation    Tests
      │               │               │
      │               │               │
      ▼               ▼               ▼

   src/             docs/           tests/
```

Keep documentation outside source code.

Documentation should describe the system.

Source code should implement it.

______________________________________________________________________

# 4. Common Repository Files

These files are useful regardless of which AI assistant you use.

______________________________________________________________________

## README.md

Purpose

Repository entry point.

Usually the first document read by both humans and AI.

Typical contents

- Project overview
- Installation
- Running
- Configuration
- Build
- Testing
- Folder structure
- High-level architecture

Example headings

```
Project Overview

Features

Installation

Running

Configuration

Testing

Architecture

Contributing
```

README should explain **what** the project does.

Avoid putting implementation details here.

______________________________________________________________________

## docs/

This is the most important directory.

Instead of one huge document

```
Architecture.md
```

with 500 pages,

split documentation into logical modules.

Good

```
docs/

architecture.md

worker.md

manager.md

protocol.md
```

Bad

```
docs/

everything.md
```

AI retrieves smaller documents much more efficiently.

______________________________________________________________________

## tests/

Contains

- Unit tests
- Integration tests
- Fixtures
- Mock data

Documentation belongs in docs/.

Tests belong in tests/.

______________________________________________________________________

## scripts/

Contains helper scripts.

Example

```
start.sh

deploy.py

generate_docs.py

release.py
```

______________________________________________________________________

## configs/

Configuration examples.

Example

```
development.conf

production.conf

docker.conf
```

______________________________________________________________________

## examples/

Contains

- sample applications
- API examples
- tutorials
- quick starts

Very useful for AI because examples often explain intended usage better than documentation.

______________________________________________________________________

# 5. Documentation Structure

Recommended:

```
docs/

architecture.md

coding-guidelines.md

deployment.md

testing.md

protocol.md

worker.md

manager.md

troubleshooting.md

decisions.md
```

Each document should answer one topic.

______________________________________________________________________

# architecture.md

Purpose

Explains the entire system.

Should contain

- Components
- Responsibilities
- Data flow
- Communication
- High-level diagrams

Example

```
User

↓

API

↓

Manager

↓

Workers

↓

Storage
```

Should NOT contain

- TODOs
- Bug history
- Coding standards

______________________________________________________________________

# coding-guidelines.md

Purpose

Project coding conventions.

Example sections

```
Naming

Logging

Exceptions

Formatting

Typing

Comments

Documentation
```

Avoid implementation details.

______________________________________________________________________

# testing.md

Purpose

Testing strategy.

Possible sections

```
Unit Tests

Integration Tests

Mocking

Fixtures

Coverage

Performance Tests
```

______________________________________________________________________

# deployment.md

Purpose

Deployment instructions.

Possible sections

```
Requirements

Docker

Kubernetes

Environment Variables

Production Checklist

Monitoring
```

______________________________________________________________________

# protocol.md

Useful when a project communicates over a network.

Contains

- protocol overview
- message flow
- packet structure
- retries
- acknowledgements
- versioning

______________________________________________________________________

# troubleshooting.md

Purpose

Known issues.

Common errors.

Typical fixes.

Useful sections

```
Symptoms

Possible Causes

Solutions

Debug Commands
```

______________________________________________________________________

# worker.md

Describes

- lifecycle
- responsibilities
- state transitions

Example

```
CONNECTING

↓

IDLE

↓

SYNCING

↓

STOPPED
```

______________________________________________________________________

# manager.md

Describes

- responsibilities
- worker management
- notification flow
- health monitoring

______________________________________________________________________

# 6. Design Decision Records (ADR)

One of the most useful documents for both humans and AI.

Example

```
Decision

Use threading.Event

Reason

Consumes zero CPU while idle.

Alternatives

Polling

Rejected

Consumes unnecessary CPU.
```

Instead of repeatedly explaining

"Why Event?"

AI can simply read

```
docs/decisions.md
```

______________________________________________________________________

# 7. Architecture Diagram

Example

```
                Client

                  │

                  ▼

              API Layer

                  │

                  ▼

          Replication Manager

          ┌────────┼─────────┐

          │        │         │

          ▼        ▼         ▼

      Worker1  Worker2   Worker3

          │        │         │

          ▼        ▼         ▼

      Replica1 Replica2 Replica3
```

Simple ASCII diagrams are often sufficient.

Mermaid diagrams are also an excellent choice because they are text-based and render well on platforms like GitHub.

______________________________________________________________________

# 8. Best Practices

## Keep documents focused

Good

```
worker.md
```

Bad

```
EverythingAboutWorkersManagersArchitecture.md
```

______________________________________________________________________

## Keep files reasonably small

Ideal

200–500 lines

Avoid

2000-line markdown files.

______________________________________________________________________

## Separate architecture from implementation

Architecture

```
docs/
```

Implementation

```
src/
```

______________________________________________________________________

## Keep examples separate

Do not mix examples inside architecture documents.

Use

```
examples/
```

______________________________________________________________________

## Version documentation

Whenever architecture changes,

update documentation.

Do not let documentation become stale.

______________________________________________________________________

## Record important decisions

Instead of explaining them repeatedly,

write them once.

______________________________________________________________________

# 9. Token Optimization

One of the biggest reasons to organize documentation.

Instead of

```
Prompt

Architecture...

Constraints...

Naming...

Protocol...

Worker...
```

Prompt becomes

```
Implement startup synchronization.
```

AI retrieves

```
worker.md

architecture.md

protocol.md
```

instead.

Huge token savings.

______________________________________________________________________

# Token Reduction Techniques

## Modular Documentation

Good

```
worker.md

manager.md

protocol.md
```

Bad

```
architecture.md

(3000 lines)
```

______________________________________________________________________

## Don't duplicate information

If worker lifecycle exists in

```
worker.md
```

don't repeat it in README.

______________________________________________________________________

## Prefer references

Instead of

```
Architecture...

Worker...

Protocol...
```

say

```
Follow worker.md.
```

______________________________________________________________________

## Use consistent terminology

Avoid

```
Worker

Thread

Consumer

Processor

Listener
```

for the same component.

Pick one name.

Consistency improves AI understanding.

______________________________________________________________________

# 10. Common Mistakes

❌ Huge markdown files

❌ Architecture inside README

❌ No documentation

❌ Duplicate documentation

❌ Outdated documentation

❌ Mixing deployment with architecture

❌ Putting implementation details into architecture

❌ No design decision records

❌ Inconsistent naming

______________________________________________________________________

# Repository Checklist

## Repository

- [ ] README.md exists
- [ ] docs/ exists
- [ ] tests/ exists
- [ ] examples/ exists
- [ ] configs/ exists

## Documentation

- [ ] architecture.md
- [ ] testing.md
- [ ] deployment.md
- [ ] troubleshooting.md
- [ ] protocol.md (if applicable)
- [ ] coding-guidelines.md
- [ ] decisions.md

## Documentation Quality

- [ ] Small focused files
- [ ] No duplication
- [ ] Updated regularly
- [ ] Consistent terminology
- [ ] Includes diagrams where useful

______________________________________________________________________

# Summary

A well-structured repository is the foundation of AI-assisted software development. Regardless of whether you use Claude
Code, GitHub Copilot, Antigravity, or another assistant, the same principles apply:

- Keep documentation modular.
- Separate architecture, implementation, and operational guides.
- Record important design decisions.
- Prefer many focused documents over one massive document.
- Let the repository provide context so prompts can stay concise.

In the next part, we'll build on this foundation by looking at how specific AI tools (Claude Code, GitHub Copilot, and
Antigravity) discover and use project context, what special instruction files they support, and how to optimize each
tool for the best development experience.

## Next

[AI Assisted Development Guide](part-2.md)
