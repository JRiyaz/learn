# AI Assisted Development Guide - Part 7

# Context Optimization Libraries & Repository Indexing

> **Audience:** Developers building medium to large projects with AI coding assistants.

This guide introduces the most widely used libraries and tools for reducing AI token consumption by retrieving only the
relevant project context instead of sending entire repositories.

______________________________________________________________________

# Table of Contents

1. Why Context Optimization?
1. How AI Context Works
1. Context Optimization Techniques
1. Popular Libraries
1. Repository Indexing
1. Recommended Project Architecture
1. Choosing the Right Tool
1. Best Practices

______________________________________________________________________

# 1. Why Context Optimization?

The biggest cost in AI-assisted development is usually **context**, not the prompt itself.

Bad workflow

```text
Entire Repository

↓

LLM

↓

Response
```

Good workflow

```text
Repository

↓

Indexer

↓

Retriever

↓

Relevant Files

↓

LLM
```

Instead of sending

- 500 Python files
- 100 Markdown files
- 100 Tests

the AI receives only

- worker.py
- manager.py
- protocol.py
- architecture.md

This significantly reduces:

- Token usage
- Response time
- Hallucinations
- Cost

______________________________________________________________________

# 2. Context Optimization Techniques

There are four common approaches.

## A. Documentation

The simplest and most effective.

Store architecture in

```text
docs/
```

instead of repeating it in prompts.

______________________________________________________________________

## B. Retrieval

Find only the relevant documents.

Instead of

```text
Entire Repository
```

retrieve

```text
worker.py

manager.py
```

______________________________________________________________________

## C. Semantic Search

Instead of filename matching,

find files based on meaning.

Example

Developer asks

```text
Implement startup synchronization.
```

Retriever finds

```text
worker.py

protocol.py

startup.md
```

even if "startup synchronization" isn't written exactly that way.

______________________________________________________________________

## D. Code Indexing

Understand

- functions
- classes
- methods
- symbols

instead of plain text.

______________________________________________________________________

# 3. Popular Libraries

______________________________________________________________________

# Tree-sitter ⭐⭐⭐⭐⭐

Purpose

Parse source code into syntax trees.

Supports

- Python
- Go
- Java
- Rust
- C
- C++
- JavaScript
- TypeScript
- and many more.

Use Cases

- Find functions
- Find classes
- Find methods
- Repository navigation
- AI code retrieval

Example

Instead of sending

```python
worker.py

1500 lines
```

retrieve

```python
ReplicaWorker.run()

ReplicaWorker.notify()
```

Only.

______________________________________________________________________

How to install

```bash
pip install tree-sitter
```

When should you use it?

Large repositories.

Libraries.

Frameworks.

Enterprise codebases.

______________________________________________________________________

# LlamaIndex ⭐⭐⭐⭐⭐

Purpose

Build searchable indexes over

- Markdown
- PDFs
- Source code
- Documentation
- Databases

Works very well for

Repository documentation.

Example

```text
docs/

↓

LlamaIndex

↓

Index

↓

Claude
```

Install

```bash
pip install llama-index
```

Use when

Your project has

lots of documentation.

______________________________________________________________________

# FAISS ⭐⭐⭐⭐☆

Facebook AI Similarity Search.

Purpose

Fast vector similarity search.

Works with

Embeddings.

Use Cases

- Semantic retrieval
- Documentation search
- Code search

Install

```bash
pip install faiss-cpu
```

Usually combined with

OpenAI embeddings

or

Sentence Transformers.

______________________________________________________________________

# LanceDB ⭐⭐⭐⭐⭐

Modern vector database.

Purpose

Store embeddings locally.

Advantages

- Fast
- Lightweight
- Local development
- Python friendly

Example

```text
Repository

↓

Embeddings

↓

LanceDB

↓

Retriever

↓

LLM
```

Install

```bash
pip install lancedb
```

Excellent choice for local AI development.

______________________________________________________________________

# ChromaDB ⭐⭐⭐⭐☆

Another popular vector database.

Very easy to use.

Install

```bash
pip install chromadb
```

Good for

- Local projects
- RAG
- Documentation search

______________________________________________________________________

# Sentence Transformers ⭐⭐⭐⭐⭐

Purpose

Generate embeddings.

Install

```bash
pip install sentence-transformers
```

Example

```text
Markdown

↓

Embedding

↓

Vector Database
```

Usually paired with

- FAISS

- LanceDB

- ChromaDB

______________________________________________________________________

# LLMLingua ⭐⭐⭐⭐☆

Purpose

Compress prompts before sending them to the LLM.

Instead of

```text
5000 tokens
```

send

```text
1000 tokens
```

Useful for

- Long conversations
- Long documentation
- Meeting notes

Install

```bash
pip install llmlingua
```

Use only when

retrieval alone isn't enough.

______________________________________________________________________

# Tree-sitter + Vector Database

One of the most effective combinations.

```text
Repository

↓

Tree-sitter

↓

Functions

↓

Embeddings

↓

Vector Database

↓

Retriever

↓

LLM
```

Instead of indexing

files,

index

functions.

______________________________________________________________________

# 4. Repository Architecture

Small Project

```text
Repository

↓

Claude Code
```

No additional tooling needed.

______________________________________________________________________

Medium Project

```text
Repository

↓

Documentation

↓

Claude Code
```

Still simple.

______________________________________________________________________

Large Project

```text
Repository

↓

Tree-sitter

↓

Embeddings

↓

Vector DB

↓

Retriever

↓

Claude
```

______________________________________________________________________

Enterprise

```text
Repository

↓

Indexer

↓

Retriever

↓

Knowledge Base

↓

AI Assistant
```

______________________________________________________________________

# 5. How to Use Them

## Small Projects (\<20K LOC)

Use

- README
- CLAUDE.md
- Good documentation

Nothing else.

______________________________________________________________________

## Medium Projects (20K–100K LOC)

Add

Tree-sitter

for code navigation.

______________________________________________________________________

## Large Projects (>100K LOC)

Add

- Tree-sitter
- Sentence Transformers
- LanceDB

or

FAISS.

______________________________________________________________________

## Documentation Heavy Projects

Use

LlamaIndex

to index Markdown.

______________________________________________________________________

# Example Project

```text
project/

README.md

CLAUDE.md

docs/

src/

scripts/

ai/

    index.py

    retrieve.py

    embed.py

    database.py
```

______________________________________________________________________

# Example Workflow

```text
Developer

↓

Ask Question

↓

Retriever

↓

Relevant Files

↓

Claude Code

↓

Answer
```

Notice

Claude never receives

the entire repository.

______________________________________________________________________

# 6. Which Tool Should I Choose?

| Tool | Best For |
| --------------------- | ---------------------------------- |
| Tree-sitter | Code parsing and symbol extraction |
| LlamaIndex | Documentation indexing |
| Sentence Transformers | Embedding generation |
| LanceDB | Local vector database |
| FAISS | High-performance similarity search |
| ChromaDB | Simple local RAG |
| LLMLingua | Prompt compression |

______________________________________________________________________

# 7. Recommended Stack

## Small Projects

```text
README

↓

CLAUDE.md

↓

Claude Code
```

______________________________________________________________________

## Medium Projects

```text
Repository

↓

Tree-sitter

↓

Claude Code
```

______________________________________________________________________

## Large Projects

```text
Repository

↓

Tree-sitter

↓

Sentence Transformers

↓

LanceDB

↓

Retriever

↓

Claude Code
```

______________________________________________________________________

## Documentation-Heavy Projects

```text
Markdown

↓

LlamaIndex

↓

Claude Code
```

______________________________________________________________________

# Best Practices

- Keep documentation modular.
- Prefer retrieval over sending large prompts.
- Index functions instead of entire files when possible.
- Store embeddings locally for faster searches.
- Update indexes whenever the repository changes.
- Use prompt compression only after you've optimized retrieval.

______________________________________________________________________

# Final Recommendation

For most Python projects, you **do not need every library**.

A practical progression is:

| Project Size | Recommendation |
| ------------------------ | --------------------------------------------- |
| Small | README + CLAUDE.md + docs |
| Medium | Add Tree-sitter |
| Large | Tree-sitter + Sentence Transformers + LanceDB |
| Documentation-heavy | Add LlamaIndex |
| Very large conversations | Consider LLMLingua |

The biggest improvements come from **better repository organization and retrieval**, not from compressing prompts. Start
with a well-structured repository, then add indexing and vector search only when your project grows large enough to
justify the additional complexity.

## Next

[Model Context Protocol (MCP) Complete Guide](part-10.md)
