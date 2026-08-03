# System Design - Part 61

# Vector Databases

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a Vector Database is
- Why Vector Databases exist
- Embeddings
- Vector Search
- Similarity Search
- Approximate Nearest Neighbor (ANN)
- Indexing Algorithms (HNSW, IVF)
- Metadata Filtering
- RAG Architecture
- Vector Databases vs Elasticsearch
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

contains

10 million books.

A user

searches

for

```text id="vec6101"
books about backend development
```

But

none

of the books

contain

those exact words.

Instead,

the database contains

books titled

- Python Microservices
- Building REST APIs
- System Design Interview
- FastAPI in Action

A keyword search

may return

nothing.

But

these books

are

actually relevant.

How can

the system

understand

meaning,

not just words?

______________________________________________________________________

# The Problem

Traditional Search Engines

match

keywords.

Example

```text id="vec6102"
car
```

doesn't always

match

```text id="vec6103"
automobile
```

Although

they mean

the same thing.

Humans

understand meaning.

Traditional search

mostly

doesn't.

______________________________________________________________________

# The Idea

Instead of

storing words,

convert

text

into

numbers

that represent

its meaning.

These numbers

are called

**Embeddings**.

______________________________________________________________________

# What is an Embedding?

An **Embedding**

is

a numerical vector

that captures

the semantic meaning

of text,

images,

audio,

or other data.

Example

```text id="vec6104"
"Python"

↓

[0.42, -0.18, 0.91, ...]
```

The vector

may contain

hundreds

or

thousands

of dimensions.

______________________________________________________________________

# Similar Meaning

Suppose

we create

embeddings

for

three words.

```text id="vec6105"
Car

↓

[ ... ]
```

```text id="vec6106"
Automobile

↓

[ ... ]
```

```text id="vec6107"
Banana

↓

[ ... ]
```

The vectors

for

Car

and

Automobile

will be

very close.

Banana

will be

far away.

______________________________________________________________________

# What is a Vector Database?

A **Vector Database**

stores

high-dimensional vectors

and allows

fast similarity search

instead of

exact matching.

Rather than asking

"What contains this word?"

we ask

"What is most similar?"

______________________________________________________________________

# Architecture

```text id="vec6108"
Application

↓

Embedding Model

↓

Vector Database

↓

Similarity Search
```

______________________________________________________________________

# Document Ingestion

Suppose

we upload

a book.

Workflow

```text id="vec6109"
Book

↓

Embedding Model

↓

Vector

↓

Vector Database
```

Each document

becomes

a vector.

______________________________________________________________________

# Search Flow

Suppose

the user

asks

```text id="vec6110"
How do I build REST APIs?
```

Workflow

```text id="vec6111"
Question

↓

Embedding Model

↓

Vector

↓

Vector Search

↓

Similar Documents
```

Notice

the database

compares vectors,

not words.

______________________________________________________________________

# Similarity Search

Interview favorite.

The Vector Database

finds

vectors

closest

to

the query vector.

Popular similarity metrics:

- Cosine Similarity
- Euclidean Distance
- Dot Product

The closer

the vectors,

the more

similar

their meanings.

______________________________________________________________________

# Cosine Similarity

One of

the most common

similarity metrics.

Instead of

comparing

absolute values,

Cosine Similarity

compares

the angle

between vectors.

Values

close to

```text id="vec6112"
1.0
```

mean

high similarity.

______________________________________________________________________

# Why Not SQL?

Suppose

you have

100 million vectors.

Comparing

every vector

would take

too long.

Instead,

Vector Databases

use

specialized indexes.

______________________________________________________________________

# Approximate Nearest Neighbor (ANN)

Interview favorite.

Rather than

checking

every vector,

ANN algorithms

find

very close matches

extremely quickly.

They trade

a tiny amount

of accuracy

for

massive speed.

______________________________________________________________________

# HNSW

One of

the most popular

ANN algorithms.

**HNSW**

stands for

**Hierarchical Navigable Small World**.

Benefits:

- Very fast search
- High recall
- Excellent for production AI systems

Many modern

Vector Databases

use HNSW.

______________________________________________________________________

# IVF (Inverted File Index)

Another

ANN algorithm.

Instead of

searching

every vector,

vectors

are grouped

into clusters.

Only

relevant clusters

are searched.

Benefits:

- Faster search
- Lower memory usage

Trade-off:

Slightly lower recall

than HNSW.

______________________________________________________________________

# Metadata Filtering

Suppose

users ask

```text id="vec6113"
Python books
```

Only

from

```text id="vec6114"
2025
```

The search

can combine

semantic similarity

with

metadata filters.

Example

```text id="vec6115"
Category

Programming
```

```text id="vec6116"
Year

2025
```

______________________________________________________________________

# RAG (Retrieval-Augmented Generation)

One of

the biggest

AI use cases.

Workflow

```text id="vec6117"
Question

↓

Embedding

↓

Vector Database

↓

Relevant Documents

↓

LLM

↓

Answer
```

The LLM

answers

using

retrieved documents,

not

only

its training data.

______________________________________________________________________

# FastAPI Example

Suppose

a user

asks

a question.

```python id="vec6118"
POST /chat
```

Workflow

```text id="vec6119"
Question

↓

Generate Embedding

↓

Vector Search

↓

LLM

↓

Response
```

______________________________________________________________________

# AI Chatbot Example

Suppose

your company

has

10,000 documents.

Instead of

sending

all documents

to

the LLM,

retrieve

only

the most relevant ones

using

the Vector Database.

This reduces:

- Token usage
- Cost
- Latency

while improving

answer quality.

______________________________________________________________________

# Recommendation Example

Suppose

a user

likes

a Python book.

Instead of

matching

categories,

find

books

with

similar embeddings.

Recommendations

become

more meaningful.

______________________________________________________________________

# Image Search

Embeddings

aren't limited

to text.

Images

can also

be converted

into vectors.

Users

can search

using

another image

instead of

keywords.

______________________________________________________________________

# Popular Vector Databases

Examples:

- Pinecone
- Milvus
- Weaviate
- Qdrant
- Chroma
- pgvector (PostgreSQL extension)

Each supports

vector similarity search,

metadata filtering,

and ANN indexes.

______________________________________________________________________

# Elasticsearch vs Vector Database

Interview favorite.

| Elasticsearch | Vector Database |
| -------------- | ---------------- |
| Keyword search | Semantic search |
| Inverted Index | Vector Index |
| Text matching | Meaning matching |

Modern systems

often use

both together.

______________________________________________________________________

# PostgreSQL + pgvector

Many applications

don't need

a dedicated

Vector Database.

Instead,

they use

PostgreSQL

with

the

**pgvector**

extension.

This enables

vector similarity

inside

PostgreSQL.

Suitable

for

small

to medium-sized

AI applications.

______________________________________________________________________

# Hybrid Search

Modern AI systems

often combine

both approaches.

```text id="vec6120"
Keyword Search

+

Vector Search

↓

Merged Results
```

This is called

**Hybrid Search**.

It often produces

better results

than

either technique

alone.

______________________________________________________________________

# Real Backend Example

Suppose

an HR platform.

A recruiter

searches

for

```text id="vec6121"
Python backend engineer with cloud experience
```

Candidates

may not

contain

those exact words,

but

their resumes

describe

similar skills.

Vector Search

finds them

based on

meaning.

______________________________________________________________________

# Benefits

Vector Databases provide:

✅ Semantic search

✅ Fast similarity search

✅ Better recommendations

✅ AI-ready architecture

✅ Metadata filtering

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Embedding generation cost

❌ Additional infrastructure

❌ Index maintenance

❌ Model dependency

______________________________________________________________________

# When NOT to Use a Vector Database

Avoid

Vector Databases

when:

- Exact lookups

are sufficient

- Small datasets

fit

traditional SQL

- No semantic search

is required

______________________________________________________________________

# Best Practices

✅ Store metadata

alongside vectors.

✅ Use Hybrid Search.

✅ Choose the right embedding model.

✅ Update embeddings

when

documents change.

______________________________________________________________________

# Common Mistakes

### Using Vector Search for Exact Lookups

If

you need

```text id="vec6122"
Book ID = 123
```

use

a database,

not

a Vector Database.

______________________________________________________________________

### Ignoring Metadata

Filtering

only by vectors

can produce

irrelevant results.

Combine

semantic search

with metadata.

______________________________________________________________________

### Recomputing Embeddings Unnecessarily

Embeddings

should only

be regenerated

when

the source content

changes.

______________________________________________________________________

### Assuming Bigger Embeddings Are Always Better

Higher-dimensional vectors

increase

storage

and

search cost.

Choose

an embedding model

that balances

accuracy,

latency,

and cost.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a Vector Database, and why is it used in AI systems?

A Vector Database stores high-dimensional embeddings and enables fast similarity search based on semantic meaning rather
than exact keyword matching. Instead of searching for identical words, it compares vectors using similarity metrics such
as cosine similarity or dot product to find the most relevant results. Modern AI systems use Vector Databases in
Retrieval-Augmented Generation (RAG), recommendation systems, semantic search, image search, and document retrieval.
They commonly employ Approximate Nearest Neighbor (ANN) algorithms such as HNSW and IVF to search millions of vectors
efficiently.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a Vector Database is
- Embeddings
- Similarity Search
- ANN
- HNSW
- IVF
- Metadata Filtering
- RAG
- Hybrid Search
- Best practices

______________________________________________________________________

# 🧠 Storage Systems Progress

You now understand the complete storage layer:

- ✅ Database Replication
- ✅ Database Sharding
- ✅ Object Storage
- ✅ Search Engines
- ✅ Vector Databases

These technologies power nearly every modern cloud application, search platform, and AI system.

______________________________________________________________________

# 🚀 What's Coming Next

We've completed the **Storage Systems** module.

Next, we'll move into **Observability**, where you'll learn how production systems are monitored and debugged.

This includes:

- Logging
- Monitoring
- Metrics
- Alerting
- Distributed Tracing

These topics are essential for operating systems reliably in production.

______________________________________________________________________

# What's Next

[Logging](62-logging.md)
