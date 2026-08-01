# AI Assisted Development Guide - Part 2

# AI Coding Assistants

## Claude Code • GitHub Copilot • Antigravity

> This document explains how modern AI coding assistants understand your repository, what project instruction files they support, and how to organize your repository for each tool.

______________________________________________________________________

# Table of Contents

1. How AI Coding Assistants Work
1. Context Loading
1. Claude Code
1. GitHub Copilot
1. Antigravity
1. Comparison Matrix
1. Best Practices
1. Recommended Repository Layout

______________________________________________________________________

# 1. How AI Coding Assistants Work

A common misconception is:

> AI reads the entire repository.

This is **not true**.

Almost every AI coding assistant attempts to minimize context.

Typical flow:

```text
Developer Prompt

        │

        ▼

Repository Discovery

        │

        ▼

Relevant Files

        │

        ▼

Instruction Files

        │

        ▼

LLM
```

Only the files that appear relevant are loaded.

The better your repository is organized,

the less context needs to be loaded.

______________________________________________________________________

# Context Priority

Most coding assistants roughly prioritize context in this order.

```text
Current Prompt

↓

Open Files

↓

Instruction Files

↓

Repository Documentation

↓

Related Source Code

↓

Remaining Repository
```

Instruction files therefore become extremely important because they influence nearly every response.

______________________________________________________________________

# 2. Claude Code

Claude Code is currently one of the most repository-aware AI coding assistants.

It is designed to work on large codebases and long-running projects.

Unlike traditional chat interfaces,

Claude Code attempts to maintain project-level understanding.

______________________________________________________________________

## Primary Instruction File

```text
CLAUDE.md
```

Usually placed at

```text
project/

    CLAUDE.md
```

______________________________________________________________________

## Purpose

Think of CLAUDE.md as

> Project Memory

It should contain stable information.

Good examples

- project purpose
- architecture overview
- coding standards
- constraints
- preferred libraries
- testing requirements
- naming conventions

Avoid

- TODOs
- temporary bugs
- sprint planning
- implementation details

______________________________________________________________________

## Example Sections

```text
Project Overview

Architecture

Coding Standards

Testing

Constraints

Documentation

Important Notes
```

No need to write implementation details.

Just enough for Claude to understand the project.

______________________________________________________________________

## Typical Repository

```text
project/

README.md

CLAUDE.md

docs/

src/

tests/
```

______________________________________________________________________

## Context Flow

```text
Prompt

↓

CLAUDE.md

↓

README

↓

Relevant docs

↓

Relevant source

↓

Response
```

______________________________________________________________________

## Best Practices

Keep CLAUDE.md

Small

Stable

High-level

Do not turn it into another README.

______________________________________________________________________

## Things NOT to Put

Don't put

- bug history
- meeting notes
- release notes
- temporary work
- huge architecture explanations

Those belong elsewhere.

______________________________________________________________________

## When to Update

Update CLAUDE.md when

- architecture changes

- coding standards change

- supported Python version changes

- project constraints change

Not every day.

______________________________________________________________________

# 3. GitHub Copilot

GitHub Copilot integrates directly into IDEs.

Unlike Claude Code,

Copilot is primarily completion-oriented,

although newer versions include chat and agent features.

______________________________________________________________________

## Primary Instruction File

```text
.github/

    copilot-instructions.md
```

______________________________________________________________________

## Purpose

Guide Copilot's code generation.

Good information

- coding conventions

- preferred patterns

- formatting

- naming

- testing

- review expectations

______________________________________________________________________

## Example Sections

```text
Coding Style

Logging

Exceptions

Testing

Naming

Architecture Notes
```

______________________________________________________________________

## Context Flow

```text
Prompt

↓

Open Editor Files

↓

copilot-instructions.md

↓

Nearby Source Code

↓

Repository
```

Notice

Copilot relies heavily on

Open Files.

If a file isn't open,

Copilot may rely less on it.

______________________________________________________________________

## Best Practices

Keep instructions concise.

Good

```text
Always use logger.

Use pytest.

Use typing.

Prefer dependency injection.
```

Bad

```text
Entire Architecture

300 pages
```

______________________________________________________________________

## Things NOT to Put

Deployment documentation

Huge architecture

Meeting notes

Design discussions

______________________________________________________________________

# 4. Antigravity

Antigravity is newer compared to Claude Code and Copilot.

Its capabilities evolve quickly.

Unlike Claude Code,

there is currently **no widely adopted standard instruction file** comparable to `CLAUDE.md`.

Always check the latest Antigravity documentation, as support may change over time.

______________________________________________________________________

## Current Behaviour

Typically understands

Repository

README

Open files

Related code

Project structure

It also benefits greatly from

well-organized documentation.

______________________________________________________________________

## Repository Recommendations

Keep

README

docs

examples

clean.

Because Antigravity uses repository context extensively.

______________________________________________________________________

## Best Practices

Small markdown documents.

Clear folder names.

Architecture diagrams.

Examples.

Consistent naming.

______________________________________________________________________

## Things to Avoid

Huge markdown files.

Duplicated documentation.

Outdated documents.

______________________________________________________________________

# 5. Comparison Matrix

| Feature | Claude Code | GitHub Copilot | Antigravity |
| -------------------------- | -------------- | ------------------------- | -------------------------- |
| Repository Understanding | Excellent | Good | Good |
| Dedicated Instruction File | ✔ CLAUDE.md | ✔ copilot-instructions.md | No widely adopted standard |
| Reads README | Yes | Yes | Yes |
| Reads Documentation | Yes | Limited | Yes |
| Uses Open Files | Yes | Heavy | Heavy |
| Large Repository Support | Excellent | Good | Good |
| Best For | Large Projects | Coding Assistance | Repository Navigation |

______________________________________________________________________

# Repository Layout

Recommended

```text
project/

README.md

CLAUDE.md

docs/

architecture.md

protocol.md

worker.md

manager.md

testing.md

deployment.md

decisions.md

.github/

copilot-instructions.md

src/

tests/

examples/

configs/
```

______________________________________________________________________

# What Goes Where?

| File | Purpose |
| ----------------------- | ------------------------ |
| README.md | Project overview |
| CLAUDE.md | Claude project memory |
| copilot-instructions.md | Copilot coding rules |
| architecture.md | High-level design |
| protocol.md | Communication protocol |
| worker.md | Worker lifecycle |
| manager.md | Manager responsibilities |
| testing.md | Testing strategy |
| deployment.md | Deployment |
| decisions.md | Architecture decisions |

______________________________________________________________________

# Should Information Be Duplicated?

No.

Example

Architecture belongs in

```text
docs/architecture.md
```

Don't repeat it inside

README

CLAUDE.md

copilot-instructions.md

Instead

Reference it.

______________________________________________________________________

# Documentation Flow

```text
README

        │

        ▼

Architecture

        │

        ▼

Worker

Manager

Protocol

Testing

Deployment
```

______________________________________________________________________

# AI Friendly Repository

Good

```text
README

↓

Architecture

↓

Implementation

↓

Tests
```

Bad

```text
README

Everything

Architecture

Testing

Deployment

Examples

Troubleshooting

4000 lines
```

______________________________________________________________________

# Token Optimization

The biggest token savings come from

Small documents

Consistent naming

Instruction files

Well-organized repository

Not from prompt engineering.

______________________________________________________________________

# Common Mistakes

❌ Huge CLAUDE.md

❌ Huge README

❌ Duplicate documentation

❌ No examples

❌ No architecture diagrams

❌ Outdated docs

❌ Temporary notes inside instruction files

______________________________________________________________________

# Enterprise Recommendation

For long-term projects

```text
README

↓

Instruction Files

↓

Architecture

↓

Feature Documents

↓

Source Code
```

Every layer has a single responsibility.

This makes it easier for both developers and AI assistants.

______________________________________________________________________

# Final Recommendations

## Use README for

Project introduction.

______________________________________________________________________

## Use CLAUDE.md for

Stable Claude-specific project instructions.

______________________________________________________________________

## Use copilot-instructions.md for

Coding conventions.

______________________________________________________________________

## Use docs/

Architecture.

Protocol.

Deployment.

Testing.

Design decisions.

______________________________________________________________________

## Never Use Instruction Files For

Sprint planning

Bug tracking

Meeting notes

Temporary work

Release notes

Large architecture explanations

______________________________________________________________________

# Summary

A repository optimized for AI assistants is one that minimizes duplicated information and keeps long-lived knowledge in
stable, discoverable locations.

- **Claude Code** benefits most from a concise `CLAUDE.md` plus modular documentation.
- **GitHub Copilot** is guided by `.github/copilot-instructions.md` and the files currently open in your IDE.
- **Antigravity** relies heavily on overall repository organization and documentation quality, without a standardized project instruction file.

The common principle across all tools is the same: keep documentation focused, avoid duplication, and let the repository
carry the project context so prompts can remain short and task-specific.

## Next

[AI-Friendly Repository Structure & Context Engineering](part-3.md)
