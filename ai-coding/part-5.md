# AI Assisted Development Guide - Part 2B

# GitHub Copilot & Antigravity Complete Guide

> **Audience:** Software Engineers using GitHub Copilot and Antigravity for professional software development.

This guide explains how GitHub Copilot and Antigravity understand your repository, what project instruction files they
support, how they differ from Claude Code, and the best practices for each tool.

______________________________________________________________________

# Table of Contents

1. GitHub Copilot
1. Copilot Repository Understanding
1. copilot-instructions.md
1. Copilot Best Practices
1. Antigravity
1. Antigravity Repository Understanding
1. Antigravity Best Practices
1. Claude vs Copilot vs Antigravity
1. Recommended Multi-AI Repository
1. Final Recommendations

______________________________________________________________________

# 1. GitHub Copilot

GitHub Copilot is primarily an **IDE-native AI assistant**.

Unlike Claude Code, Copilot spends most of its time helping while you write code.

Typical use cases

- Autocomplete
- Small implementations
- Unit tests
- Refactoring
- Documentation
- Code explanation
- Pull Request assistance

Modern versions also provide Chat and Agent capabilities.

______________________________________________________________________

# How Copilot Thinks

Many developers think Copilot understands the whole repository.

In reality it works more like this:

```text id="ajq3pv"
Current Cursor

        │

        ▼

Open Files

        │

        ▼

Nearby Symbols

        │

        ▼

Project Instructions

        │

        ▼

Related Files

        │

        ▼

LLM
```

The **currently opened editor** has a huge influence.

______________________________________________________________________

# Context Priority

Generally Copilot prioritizes

```text id="83r25d"
Current File

↓

Open Tabs

↓

copilot-instructions.md

↓

Nearby Source

↓

Repository
```

Notice

Current editor context is very important.

______________________________________________________________________

# 2. copilot-instructions.md

GitHub Copilot supports repository instructions.

Typical location

```text id="1t9y8e"
.github/

    copilot-instructions.md
```

______________________________________________________________________

# Purpose

Think of this file as

Coding Standards.

It should answer

How should code be written?

Not

How does the architecture work?

______________________________________________________________________

# Good Information

Coding conventions

Formatting

Naming

Testing

Logging

Error handling

Preferred libraries

Documentation expectations

______________________________________________________________________

# Avoid

Architecture

Deployment

Meeting notes

Bug history

Release planning

Sprint notes

Temporary discussions

______________________________________________________________________

# Example Structure

```text id="3fr8d9"
Coding Style

Logging

Exceptions

Testing

Naming

Documentation

Review Expectations
```

Keep it concise.

______________________________________________________________________

# Good Example

```text id="f8v11v"
Always use logger.

Always use type hints.

Use pytest.

Prefer dependency injection.

Use f-strings.

Document public APIs.
```

______________________________________________________________________

# Bad Example

```text id="xktyv4"
Entire Architecture

Database Design

Deployment

Networking

5000 lines...
```

______________________________________________________________________

# Working with Copilot

Good workflow

```text id="v6qv5r"
Open worker.py

↓

Open protocol.py

↓

Ask Copilot

↓

Generate code

↓

Review
```

Open the files related to your task.

Copilot performs significantly better.

______________________________________________________________________

# Working with Large Projects

For large repositories

Avoid

```text id="2dktum"
One huge module
```

Prefer

```text id="b4vgc6"
worker/

manager/

protocol/

storage/
```

Smaller modules help both developers and AI.

______________________________________________________________________

# Best Practices

Open related files.

Keep instructions short.

Review generated code.

Run tests.

Update documentation.

______________________________________________________________________

# Common Mistakes

❌ Huge copilot-instructions.md

❌ No tests

❌ Huge source files

❌ Duplicate code

❌ Inconsistent naming

______________________________________________________________________

# 3. Antigravity

Antigravity is another AI coding assistant designed around repository awareness.

Unlike Claude Code,

it currently does **not** have a widely adopted instruction file comparable to

```text id="rlg88e"
CLAUDE.md
```

Always refer to the latest Antigravity documentation, as features evolve rapidly.

______________________________________________________________________

# How Antigravity Understands Projects

Typical flow

```text id="nl5xgw"
Prompt

↓

Repository

↓

README

↓

Documentation

↓

Related Files

↓

LLM
```

Notice

Documentation quality becomes very important.

______________________________________________________________________

# Repository Recommendations

For Antigravity

Keep

README

Architecture

Examples

Documentation

up-to-date.

It benefits greatly from

well-structured repositories.

______________________________________________________________________

# Good Repository

```text id="6mqhm0"
README

↓

Architecture

↓

Subsystem Docs

↓

Source
```

______________________________________________________________________

# Poor Repository

```text id="wyfjr5"
README

Everything

Architecture

Testing

Deployment

Examples

500 pages
```

______________________________________________________________________

# Best Practices

Small markdown files.

Consistent naming.

Architecture diagrams.

Examples.

Clear module boundaries.

______________________________________________________________________

# Things to Avoid

Huge documentation.

Outdated documentation.

Duplicated documentation.

Mixing architecture with deployment.

______________________________________________________________________

# 4. Claude vs Copilot vs Antigravity

## Repository Understanding

| Capability | Claude Code | GitHub Copilot | Antigravity |
| ------------------------------ | ----------- | -------------- | ----------- |
| Project understanding | Excellent | Good | Good |
| Large repository support | Excellent | Good | Good |
| Long architectural discussions | Excellent | Moderate | Moderate |
| IDE integration | Good | Excellent | Good |
| Autocomplete | Good | Excellent | Good |

______________________________________________________________________

## Instruction Files

| Tool | Instruction File |
| -------------- | ------------------------------- |
| Claude Code | CLAUDE.md |
| GitHub Copilot | .github/copilot-instructions.md |
| Antigravity | No widely adopted standard |

______________________________________________________________________

## Best Use Cases

### Claude Code

Excellent for

- System Design
- Architecture
- Large Refactoring
- Code Review
- Documentation
- Complex Features

______________________________________________________________________

### GitHub Copilot

Excellent for

- Daily Coding
- Autocomplete
- Unit Tests
- Boilerplate
- Small Features

______________________________________________________________________

### Antigravity

Excellent for

- Repository navigation
- Feature implementation
- Understanding existing projects
- Documentation-assisted development

______________________________________________________________________

# 5. Multi-AI Repository

A repository can support multiple AI assistants simultaneously.

Example

```text id="ncldwi"
project/

README.md

CLAUDE.md

docs/

architecture.md

protocol.md

worker.md

manager.md

decisions.md

.github/

copilot-instructions.md

src/

tests/
```

Notice

Nothing conflicts.

Each tool simply consumes

the files it understands.

______________________________________________________________________

# Shared Documentation

All AI assistants benefit from

```text id="4yabkt"
README

Architecture

Examples

Testing

Decision Records
```

Only the instruction files differ.

______________________________________________________________________

# Documentation Flow

```text id="b1iqqm"
README

        │

        ▼

Architecture

        │

        ▼

Subsystem Docs

        │

        ▼

Source Code
```

Instruction files simply provide

additional guidance.

______________________________________________________________________

# Daily Development Workflow

```text id="g4qbrs"
Architecture

↓

Implement

↓

Review

↓

Test

↓

Document

↓

Commit
```

AI should assist

every stage.

______________________________________________________________________

# Repository Maintenance

Review periodically

README

Architecture

Instruction files

Decision records

Examples

Remove

Outdated documentation

Temporary notes

Duplicate information

______________________________________________________________________

# Final Recommendations

## For Claude Code

Use

```text id="pcrq6d"
CLAUDE.md
```

for

stable project memory.

______________________________________________________________________

## For GitHub Copilot

Use

```text id="ph74u8"
.github/copilot-instructions.md
```

for

coding conventions.

______________________________________________________________________

## For Antigravity

Focus on

repository organization

rather than tool-specific instruction files.

______________________________________________________________________

## Universal Principles

Regardless of the AI assistant,

the following practices consistently improve results:

- Keep documentation modular.
- Separate architecture from implementation.
- Maintain examples and design decisions.
- Avoid duplication.
- Use consistent terminology.
- Keep instruction files concise and stable.
- Treat the repository as the project's long-term knowledge base.

______________________________________________________________________

# Summary

Each AI assistant has different strengths:

- **Claude Code** excels at understanding large codebases, architecture, and long-running engineering tasks.
- **GitHub Copilot** excels at interactive coding, autocomplete, and IDE-assisted development.
- **Antigravity** benefits from clean repository organization and high-quality documentation, even without a standardized project instruction file.

A well-structured repository allows all three tools to work together effectively without requiring duplicate
documentation or tool-specific repository layouts. By separating permanent knowledge (documentation and instruction
files) from temporary work (prompts and conversations), you can achieve better code quality, lower token usage, and a
more maintainable development workflow.

## Next

[Advanced Context Engineering & Token Optimization](part-6.md)
