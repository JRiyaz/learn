# AI Assisted Development Guide - Part 2A

# Claude Code Complete Guide

> **Audience:** Software Engineers using Claude Code for professional software development.

This guide explains how Claude Code understands your repository, how to organize projects for maximum productivity, and how to reduce token usage while improving response quality.

---

# Table of Contents

1. What is Claude Code?
2. How Claude Code Works
3. Repository Discovery
4. CLAUDE.md
5. Repository Organization
6. Context Loading Strategy
7. Working with Large Projects
8. Documentation Strategy
9. Token Optimization
10. Best Practices
11. Common Mistakes
12. Example Project
13. Recommended Workflow

---

# 1. What is Claude Code?

Claude Code is an AI-powered coding assistant designed to work with **entire software projects**, not just individual files.

Unlike traditional autocomplete tools, Claude Code attempts to understand:

* Repository structure
* Project architecture
* Documentation
* Related source code
* Existing implementation
* Coding conventions

Think of Claude Code as another software engineer joining your project.

The better your repository communicates knowledge, the better Claude performs.

---

# 2. How Claude Code Thinks

Many developers assume Claude works like this:

```text
Entire Repository

↓

LLM

↓

Answer
```

This is incorrect.

Instead the process looks more like:

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

Project Instructions

        │

        ▼

Related Documentation

        │

        ▼

Relevant Source Files

        │

        ▼

LLM
```

Claude tries to gather only the information necessary for the current task.

---

# Why This Matters

Suppose your repository contains

```text
200 Python files

150 Markdown files

500 Unit Tests
```

If Claude loaded everything,

every prompt would become

extremely slow and expensive.

Instead,

it loads only relevant information.

---

# 3. Repository Discovery

Claude typically begins by understanding

```
Repository

↓

README

↓

Project Instructions

↓

Documentation

↓

Source Code
```

Then it expands only when required.

Example

Prompt

```text
Implement startup synchronization.
```

Claude may retrieve

```
worker.py

manager.py

protocol.md

architecture.md
```

It usually does NOT need

```
deployment.md

testing.md

examples/

Dockerfiles
```

---

# Repository Organization

A well-organized repository allows Claude to retrieve

10 files

instead of

500 files.

This dramatically reduces token usage.

---

# 4. CLAUDE.md

The most important Claude-specific file.

Location

```
project/

CLAUDE.md
```

---

# Purpose

Think of

```
CLAUDE.md
```

as

Project Memory.

It should contain

stable information

about the project.

---

# Good Information

Project overview

Architecture summary

Technology stack

Coding standards

Project constraints

Naming conventions

Testing expectations

Documentation references

---

# Avoid

Meeting notes

Bug history

Sprint planning

TODO lists

Temporary work

Release notes

Large implementation details

---

# Keep It Small

Good

```
Project

Architecture

Constraints

Coding Standards

Testing
```

Bad

```
5000 lines

Everything

Every decision

Every bug

Every discussion
```

Remember

CLAUDE.md

is NOT another README.

---

# Example Structure

```
Project

Purpose

Architecture

Technology Stack

Coding Standards

Constraints

Testing

Documentation
```

Notice

Only headings.

Not implementation.

---

# When Should It Change?

Update

CLAUDE.md

only when

Architecture changes

Coding standards change

Python version changes

Major project constraints change

Not after every feature.

---

# 5. Repository Organization

Claude works best with

```
README.md

CLAUDE.md

docs/

src/

tests/
```

Avoid

```
README.md

4000 lines

Everything
```

---

# Documentation Organization

Good

```
docs/

architecture.md

protocol.md

worker.md

manager.md

deployment.md

testing.md

decisions.md
```

Bad

```
Everything.md
```

Claude retrieves

smaller focused documents

far better.

---

# 6. Context Loading

Think of context as layers.

```
Prompt

↓

CLAUDE.md

↓

README

↓

Architecture

↓

Related Docs

↓

Relevant Code

↓

Additional Files
```

Each layer is loaded only if necessary.

---

# Stable vs Dynamic Context

Stable Context

* Architecture

* Coding Standards

* Naming

* Constraints

Dynamic Context

* Current Task

* Open Files

* Related Source

* Current Branch

Stable information belongs

inside

CLAUDE.md

Dynamic information belongs

inside

the prompt.

---

# Good Prompt

```
Implement startup synchronization.
```

Bad Prompt

```
Implement startup synchronization.

Remember

Architecture

Logger

Python

Type hints

Threading

Worker

Manager

...
```

The repository should already contain this knowledge.

---

# 7. Working with Large Projects

For projects with

100+

modules,

split documentation.

Example

```
docs/

architecture.md

replication.md

storage.md

worker.md

manager.md

protocol.md
```

Don't create

```
Architecture.md

300 pages
```

---

# Documentation Hierarchy

```
README

↓

Architecture

↓

Subsystem

↓

Feature

↓

Implementation
```

Never skip levels.

---

# 8. Token Optimization

The biggest token savings come from

Repository Design

NOT

Prompt Engineering.

---

## Rule 1

Don't repeat architecture.

Reference it.

---

## Rule 2

Don't paste code.

Ask Claude to inspect files.

Instead of

```
Here's worker.py

800 lines
```

say

```
Review ReplicaWorker.notify().
```

---

## Rule 3

Keep documents modular.

Good

```
worker.md

manager.md

protocol.md
```

Bad

```
Everything.md
```

---

## Rule 4

One document.

One responsibility.

---

## Rule 5

Use Architecture Decision Records.

Instead of explaining

"Why Event?"

every chat,

write

```
docs/decisions.md
```

---

## Rule 6

Summarize after major work.

Instead of

20 conversations,

create

```
Feature Summary
```

Claude understands summaries much faster.

---

## Rule 7

Keep terminology consistent.

Bad

```
Worker

Processor

Consumer

Listener
```

Good

```
Worker
```

everywhere.

---

# 9. Working Session Strategy

Good

```
Implement startup sync.

↓

Review

↓

Improve

↓

Test

↓

Document
```

Bad

```
Implement

15 features

Fix

20 bugs

Refactor

Everything
```

Break work into

small tasks.

---

# Feature Workflow

```
Architecture

↓

Design

↓

Implementation

↓

Tests

↓

Documentation

↓

Review
```

Claude performs much better with

incremental development.

---

# 10. Common Mistakes

❌ Huge CLAUDE.md

❌ Huge README

❌ Duplicate documentation

❌ Mixing temporary notes

❌ Keeping outdated documentation

❌ Repeating architecture every prompt

❌ Pasting large source files

❌ Multiple names for one component

---

# 11. Example Repository

```
project/

README.md

CLAUDE.md

docs/

    architecture.md

    replication.md

    protocol.md

    worker.md

    manager.md

    testing.md

    deployment.md

    troubleshooting.md

    decisions.md

src/

tests/

examples/

configs/
```

---

# 12. Recommended Daily Workflow

```
Open Repository

↓

Claude reads

README

↓

CLAUDE.md

↓

Architecture

↓

Relevant Files

↓

Developer Prompt

↓

Claude Response

↓

Developer Review

↓

Tests

↓

Documentation Update
```

---

# 13. Repository Maintenance

Review

CLAUDE.md

occasionally.

Review

Architecture

after major changes.

Review

Decision Records

after architectural decisions.

Review

README

after public-facing changes.

The goal is to keep permanent knowledge inside the repository rather than inside repeated prompts.

---

# Final Recommendations

For Claude Code:

✅ Keep `CLAUDE.md` concise and stable.

✅ Organize documentation into small, focused files.

✅ Store architectural decisions in a dedicated document.

✅ Prefer references over repetition.

✅ Let the repository provide context; keep prompts focused on the task.

Claude Code performs best when the repository is treated as a long-lived knowledge base rather than relying on large prompts to re-establish context for every conversation.

## Next
[GitHub Copilot & Antigravity Complete Guide](part-5.md)
