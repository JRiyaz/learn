# System Design - Part 84

# Retrieval-Augmented Generation (RAG) System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- High-Level Architecture
- Document Ingestion
- Chunking Strategies
- Embeddings
- Vector Databases
- Hybrid Search
- Re-ranking
- Prompt Augmentation
- Hallucination Reduction
- Metadata Filtering
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design a Retrieval-Augmented Generation (RAG) System.**

Unlike

ChatGPT,

which relies

primarily

on

its trained knowledge,

RAG

allows

an LLM

to answer

questions

using

external documents.

Examples:

- Company Knowledge Base
- Legal Documents
- Medical Records
- Product Manuals
- Internal Wiki
- Research Papers

The biggest challenge

is

finding

the right information

quickly

and

providing

it

to

the LLM.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Upload documents
- Index documents
- Ask questions
- Retrieve relevant content
- Generate answers
- Cite sources

Optional

- Multi-document search
- Multi-language support
- Access control
- Feedback collection

______________________________________________________________________

# Non-Functional Requirements

- Low latency
- High retrieval accuracy
- Scalable indexing
- Secure document access
- Low hallucination rate

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

the platform

contains

```text id="rag8401"
100 Million Documents
```

Average Document

```text id="rag8402"
50 Pages
```

Daily Queries

```text id="rag8403"
20 Million
```

Observation.

The bottleneck

is

retrieval quality,

not

document storage.

______________________________________________________________________

# Step 3

# API Design

Upload Document

```http id="rag8404"
POST /documents
```

______________________________________________________________________

Ask Question

```http id="rag8405"
POST /query
```

______________________________________________________________________

Delete Document

```http id="rag8406"
DELETE /documents/{id}
```

______________________________________________________________________

Search

```http id="rag8407"
GET /search?q=redis
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="rag8408"
Client

↓

API Gateway

↓

Query Service

↓

Retriever

↓

LLM

↓

Streaming
```

Supporting services:

- Document Service
- Embedding Service
- Vector Database
- Metadata Database
- Object Storage

______________________________________________________________________

# Document Ingestion Pipeline

Interview favorite.

When

a document

is uploaded,

it is

not

immediately

searchable.

Workflow

```text id="rag8409"
Upload

↓

Object Storage

↓

Text Extraction

↓

Chunking

↓

Embedding

↓

Vector Database
```

______________________________________________________________________

# Step 5

# Text Extraction

Documents

may be:

- PDF
- Word
- HTML
- Markdown
- Images (OCR)

Extract

plain text

before

chunking.

______________________________________________________________________

# Step 6

# Chunking

Interview favorite.

LLMs

cannot process

very large documents

efficiently.

Split documents

into

small chunks.

Example

```text id="rag8410"
500-page PDF

↓

Chunk 1

↓

Chunk 2

↓

Chunk N
```

______________________________________________________________________

# Chunk Size

Typical chunk size

```text id="rag8411"
300–800 Tokens
```

Too small

↓

Lose context

Too large

↓

Poor retrieval

______________________________________________________________________

# Chunk Overlap

Interview favorite.

Use

overlapping chunks.

Example

```text id="rag8412"
Chunk 1

Paragraphs 1–5

↓

Chunk 2

Paragraphs 4–8
```

Benefits:

- Preserves context
- Improves answer quality

______________________________________________________________________

# Embeddings

Interview favorite.

Each chunk

is converted

into

a vector.

```text id="rag8413"
Text

↓

Embedding Model

↓

1536-Dimensional Vector
```

Similar meanings

produce

nearby vectors.

______________________________________________________________________

# Vector Database

Store

embeddings

inside:

- Pinecone
- Milvus
- Weaviate
- Qdrant
- pgvector

Schema

```text id="rag8414"
chunk_id

embedding

metadata
```

______________________________________________________________________

# Metadata

Store

additional information.

Example

```text id="rag8415"
Document ID

Page Number

Department

Author

Created Date
```

Metadata

supports

filtered search.

______________________________________________________________________

# Query Flow

Interview favorite.

```text id="rag8416"
Question

↓

Embedding

↓

Vector Search

↓

Top-K Chunks

↓

LLM
```

Only

the most relevant

chunks

are sent

to

the LLM.

______________________________________________________________________

# Top-K Retrieval

Instead

of retrieving

every chunk,

retrieve

only

the best matches.

Example

```text id="rag8417"
Top 5

Chunks
```

This reduces

token usage

and

improves accuracy.

______________________________________________________________________

# Hybrid Search

Interview favorite.

Vector search

alone

isn't always enough.

Combine:

- Keyword Search
- Vector Search

```text id="rag8418"
BM25

+

Vector Search
```

This is called

Hybrid Search.

______________________________________________________________________

# Re-ranking

Interview favorite.

Initial retrieval

may return

20 chunks.

A re-ranking model

sorts them

again.

Workflow

```text id="rag8419"
20 Chunks

↓

Re-ranker

↓

Top 5
```

Re-ranking

improves

answer quality.

______________________________________________________________________

# Prompt Augmentation

The retrieved chunks

are inserted

into

the prompt.

```text id="rag8420"
System Prompt

↓

Retrieved Context

↓

User Question
```

The LLM

answers

using

this context.

______________________________________________________________________

# Citation Support

Good RAG systems

return

sources.

Example

```text id="rag8421"
Answer

↓

Document A

Page 12
```

Users

can verify

the response.

______________________________________________________________________

# Hallucination Reduction

Interview favorite.

If

no relevant chunks

are found,

the system

should say

"I don't know"

instead of

inventing

an answer.

Confidence thresholds

help decide

when

to answer.

______________________________________________________________________

# Security

Documents

may contain

sensitive information.

Before retrieval,

check:

- Authentication
- Authorization
- Tenant isolation

Users

should only

retrieve

documents

they can access.

______________________________________________________________________

# Caching

Redis stores:

- Recent queries
- Embeddings
- Search results
- Session data

Frequently asked

questions

can avoid

repeated retrieval.

______________________________________________________________________

# Scaling

Scale independently:

- Embedding Service
- Retriever
- Vector Database
- LLM Inference
- Document Processing

Document ingestion

and

query serving

should use

separate pipelines.

______________________________________________________________________

# AI/ML Example

Modern RAG systems

may use:

- Dense retrieval
- Sparse retrieval
- Cross-encoder re-ranking
- Query rewriting
- Multi-query retrieval
- Context compression

These techniques

improve

retrieval accuracy.

______________________________________________________________________

# Failure Scenario

Suppose

the Vector Database

is unavailable.

The system

may:

- Fall back to keyword search
- Return limited results
- Notify the user

Chat

should degrade

gracefully.

______________________________________________________________________

# Another Failure

Suppose

the Embedding Service

fails

during ingestion.

Store

the document

and

place it

in

a retry queue.

Do not

lose

uploaded documents.

______________________________________________________________________

# End-to-End Architecture

```text id="rag8422"
User

↓

API Gateway

↓

Query Service

↓

Authentication

↓

Embedding Service

↓

Retriever

↓

Vector Database

↓

Metadata Database

↓

LLM

↓

Streaming Service

↓

Redis

↓

Object Storage

↓

Document Processing Workers
```

______________________________________________________________________

# Trade-offs

Vector Search

vs

Keyword Search

| Vector | Keyword |
| ------------------- | ---------------------- |
| Semantic similarity | Exact matches |
| Better meaning | Better for identifiers |
| Higher compute | Faster |

______________________________________________________________________

Large Chunks

vs

Small Chunks

| Large | Small |
| ----------------- | ---------------- |
| More context | Better precision |
| Higher token cost | Lower token cost |
| Fewer chunks | More chunks |

______________________________________________________________________

Hybrid Search

vs

Vector Only

| Hybrid | Vector Only |
| --------------- | ------------- |
| Better accuracy | Simpler |
| More complexity | Lower latency |

______________________________________________________________________

# Best Practices

✅ Use overlapping chunks.

✅ Store metadata separately.

✅ Use Hybrid Search.

✅ Re-rank retrieved chunks.

✅ Return citations.

✅ Don't answer when confidence is low.

______________________________________________________________________

# Common Mistakes

### Sending Entire Documents

Never

send

a complete

500-page document

to the LLM.

Retrieve

only

relevant chunks.

______________________________________________________________________

### Ignoring Metadata

Without metadata,

you cannot:

- Filter by user
- Filter by department
- Filter by date

Metadata

is essential.

______________________________________________________________________

### Using Only Vector Search

Exact identifiers

like:

- Invoice #12345
- Employee ID
- Error Code

often work better

with keyword search.

Hybrid search

combines both strengths.

______________________________________________________________________

### Recomputing Embeddings

Embeddings

should be created

during ingestion,

not

for every query.

Only

the user's query

requires

a new embedding.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design a RAG system?

Start by separating document ingestion from query serving. During ingestion, upload documents to Object Storage, extract
text, split it into overlapping chunks, generate embeddings, and store them in a vector database along with metadata.
During query execution, convert the user's question into an embedding, retrieve the most relevant chunks using vector or
hybrid search, optionally re-rank the results, and augment the prompt with the retrieved context before sending it to
the LLM. Return the generated answer along with citations, enforce access control before retrieval, cache common
queries, and design the system so ingestion, retrieval, and LLM inference can scale independently.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Document ingestion
- Chunking
- Embeddings
- Vector databases
- Hybrid search
- Re-ranking
- Prompt augmentation
- Metadata filtering
- Hallucination reduction
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram
- ✅ Twitter/X
- ✅ YouTube
- ✅ Netflix
- ✅ Spotify
- ✅ Google Drive
- ✅ Uber
- ✅ Amazon
- ✅ Payment Gateway
- ✅ Notification Service
- ✅ ChatGPT / LLM
- ✅ RAG System

You now understand the complete architecture behind modern enterprise AI applications, from document ingestion to
semantic retrieval and LLM-powered answer generation.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll begin the **Distributed Infrastructure Deep Dive** by designing the internals of **Apache Kafka** itself,
including:

- Brokers
- Partitions
- Replication
- Leader election
- Consumer groups
- Offset management
- Exactly-once semantics
- High availability

______________________________________________________________________

# What's Next

[Apache Kafka System Design](85-apache-kafka-system-design.md)
