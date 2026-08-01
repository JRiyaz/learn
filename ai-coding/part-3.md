# AI Assisted Development Guide - Part 1

## AI-Friendly Repository Structure & Context Engineering

> **Audience:** Software Engineers using AI coding assistants such as Claude Code, GitHub Copilot, Antigravity, Codex, Cursor, Aider, and similar tools.

______________________________________________________________________

# Table of Contents

1. Introduction
1. Prompt Engineering vs Context Engineering
1. Goals of an AI-Friendly Repository
1. Repository Structure
1. Common Repository Files
1. Documentation Strategy
1. Architecture Documentation
1. Design Decision Records (ADR)
1. Best Practices
1. Token Optimization
1. Common Mistakes
1. Repository Checklist

______________________________________________________________________

# 1. Introduction

Modern AI coding assistants do much more than generate code.

They attempt to understand:

- Repository structure
- Documentation
- Architecture
- Source code
- Configuration
- Coding conventions
- Design decisions

A well-organized repository produces significantly better AI-generated code than a poorly documented one.

Think of your repository as **long-term memory** for the AI.

______________________________________________________________________

# Prompt Engineering vs Context Engineering

## Traditional Prompt Engineering

Every prompt repeats project information.

Example:

```text
Implement startup synchronization.

Use logger.
Use type hints.
Use f-strings.
Don't use polling.
Follow our architecture.
Use retry logic.
```

This wastes tokens.

______________________________________________________________________

## Context Engineering

Instead of repeating project knowledge,

the repository stores it permanently.

Prompt becomes:

```text
Implement startup synchronization.
```

The AI already understands:

- coding standards
- architecture
- naming conventions
- project constraints
- testing requirements

This is called **Context Engineering**.

Modern AI development is moving from Prompt Engineering to Context Engineering.

______________________________________________________________________

# Benefits

- Smaller prompts
- Lower token consumption
- Better consistency
- Better architecture decisions
- Less repeated explanations
- Easier onboarding
- Better documentation

______________________________________________________________________

# 2. Goals of an AI-Friendly Repository

A repository should provide:

✓ Clear architecture

✓ Consistent naming

✓ Modular documentation

✓ Design decisions

✓ Coding standards

✓ Deployment instructions

✓ Testing strategy

✓ Small focused documents

✓ Easy navigation

______________________________________________________________________

# 3. Recommended Repository Structure

```text
project/
│
├── README.md
│
├── docs/
│   ├── architecture.md
│   ├── coding-guidelines.md
│   ├── deployment.md
│   ├── testing.md
│   ├── troubleshooting.md
│   ├── protocol.md
│   ├── decisions.md
│   ├── worker.md
│   └── manager.md
│
├── src/
│
├── tests/
│
├── configs/
│
├── scripts/
│
└── examples/
```

______________________________________________________________________

## Repository Layers

```text
                    Repository

      ┌──────────────┼──────────────┐

      │              │              │

 Documentation     Source         Tests

      │              │              │

      ▼              ▼              ▼

    docs/          src/          tests/
```

Every directory should have a clear responsibility.

______________________________________________________________________

# 4. Common Repository Files

These files are useful regardless of which AI assistant you use.

______________________________________________________________________

## README.md

### Purpose

Repository entry point.

Usually the first document read by developers and AI.

### Typical Information

- Project overview
- Installation
- Running
- Configuration
- Features
- Folder structure
- High-level architecture

### Example Headings

```text
Project Overview

Installation

Running

Configuration

Architecture

Testing

Contributing
```

______________________________________________________________________

## docs/

This is the heart of project knowledge.

Instead of one massive document,

create multiple focused documents.

Good

```text
docs/

architecture.md

worker.md

manager.md

protocol.md
```

Bad

```text
docs/

Everything.md
```

Smaller documents improve retrieval quality.

______________________________________________________________________

## tests/

Contains

- Unit tests
- Integration tests
- Fixtures
- Test utilities

______________________________________________________________________

## configs/

Contains

- Example configurations
- Environment templates
- Production samples

______________________________________________________________________

## examples/

Contains

- Example usage
- Sample applications
- Tutorials
- Quick starts

Examples help AI understand intended usage patterns.

______________________________________________________________________

## scripts/

Contains

- Build scripts
- Deployment scripts
- Helper utilities
- Release automation

______________________________________________________________________

# 5. Documentation Strategy

Instead of

```text
Architecture.md

4000 lines
```

prefer

```text
architecture.md

worker.md

manager.md

protocol.md

testing.md

deployment.md
```

Each document should answer one question.

Example

| Question | Document |
| -------------------------- | --------------- |
| How does the system work? | architecture.md |
| How does replication work? | protocol.md |
| How do workers behave? | worker.md |
| How are deployments done? | deployment.md |
| How is testing performed? | testing.md |

______________________________________________________________________

# 6. Architecture Documentation

The architecture document should explain

- Components
- Responsibilities
- Data flow
- Communication
- High-level diagrams

Example

```text
Client

↓

API

↓

Manager

↓

Workers

↓

Storage
```

Avoid

- TODOs
- Bug history
- Meeting notes
- Temporary decisions

______________________________________________________________________

# 7. Design Decision Records (ADR)

One of the most valuable documents.

Purpose

Explain

- Why a decision was made
- Alternatives considered
- Why alternatives were rejected

Example

```text
Decision

Use threading.Event.

Reason

Consumes zero CPU while idle.

Alternatives

Polling

Rejected

Consumes unnecessary CPU.
```

Instead of repeatedly explaining

"Why Event?"

the AI can simply read

```text
docs/decisions.md
```

______________________________________________________________________

# 8. Best Practices

## Keep Documents Small

Ideal

200–500 lines.

Avoid

2000-line markdown files.

______________________________________________________________________

## One Responsibility Per Document

Good

```text
worker.md
```

Bad

```text
EverythingAboutWorkersManagersArchitecture.md
```

______________________________________________________________________

## Avoid Duplicate Information

If architecture exists in

```text
architecture.md
```

don't repeat it in

- README
- testing
- deployment

Reference instead of copying.

______________________________________________________________________

## Keep Documentation Updated

Whenever architecture changes,

update documentation.

Documentation should never lag behind implementation.

______________________________________________________________________

## Use Consistent Terminology

Choose one name.

Example

Good

```text
Worker
```

Bad

```text
Worker

Consumer

Processor

Listener
```

All referring to the same component.

______________________________________________________________________

# 9. Token Optimization

Most token savings come from repository organization.

Not prompt engineering.

Instead of

```text
Architecture...

Worker...

Protocol...

Constraints...

Coding Style...
```

the prompt becomes

```text
Implement startup synchronization.
```

AI retrieves

- architecture.md
- worker.md
- protocol.md

instead.

______________________________________________________________________

## Techniques

### Modular Documentation

Good

```text
worker.md

manager.md

protocol.md
```

Bad

```text
Architecture.md

4000 lines
```

______________________________________________________________________

### Don't Repeat Information

Reference documents instead.

______________________________________________________________________

### Keep Stable Knowledge in Documentation

Examples

- Architecture
- Coding standards
- Constraints
- Design decisions

Avoid placing these repeatedly in prompts.

______________________________________________________________________

### Use Consistent Folder Names

Good

```text
docs/

tests/

configs/
```

Avoid confusing structures.

______________________________________________________________________

# 10. Common Mistakes

❌ Huge README

❌ Huge architecture document

❌ Duplicate documentation

❌ Outdated documentation

❌ Mixing deployment with architecture

❌ Mixing testing with implementation

❌ No examples

❌ No ADRs

❌ Inconsistent naming

______________________________________________________________________

# 11. Repository Checklist

## Repository

- [ ] README.md
- [ ] docs/
- [ ] src/
- [ ] tests/
- [ ] examples/
- [ ] configs/
- [ ] scripts/

______________________________________________________________________

## Documentation

- [ ] architecture.md
- [ ] coding-guidelines.md
- [ ] testing.md
- [ ] deployment.md
- [ ] troubleshooting.md
- [ ] protocol.md (if applicable)
- [ ] decisions.md

______________________________________________________________________

## Quality

- [ ] Small focused documents
- [ ] No duplication
- [ ] Consistent terminology
- [ ] Updated regularly
- [ ] Architecture diagrams included

______________________________________________________________________

# Summary

An AI-friendly repository is one where the **repository itself provides the context**, allowing AI assistants to focus
on the task instead of reconstructing project knowledge from every prompt.

The key principles are:

- Organize documentation into small, focused files.
- Separate architecture, implementation, deployment, and testing.
- Record important design decisions.
- Keep documentation current.
- Let the repository provide context so prompts remain concise.

This foundation works with virtually every modern AI coding assistant, regardless of vendor or IDE.

## Next

[Claude Code Complete Guide](part-4.md)
