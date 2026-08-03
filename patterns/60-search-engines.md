# System Design - Part 60

# Search Engines (Elasticsearch & OpenSearch)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Search Engines exist
- What Full-Text Search is
- Database Search vs Search Engine
- Inverted Index
- Document Indexing
- Relevance Scoring
- Elasticsearch Architecture
- OpenSearch
- Sharding & Replication
- FastAPI Integration
- AI Search Pipeline
- Common interview questions

______________________________________________________________________

# Before We Start

Let's return

to

our

**Library Management System.**

Suppose

the library

contains

10 million books.

A member

searches

for

```text id="se6001"
python
```

The application

runs

a SQL query.

```sql id="se6002"
SELECT *

FROM books

WHERE title LIKE '%python%'
```

Initially,

everything works.

Until

the database

contains

millions

of records.

______________________________________________________________________

# The Problem

SQL databases

are excellent

at

storing data.

They are

not optimized

for

large-scale

text searching.

Problems:

❌ Slow LIKE queries

❌ Poor relevance ranking

❌ Limited typo handling

❌ Weak language analysis

______________________________________________________________________

# Example

Suppose

a user

searches

for

```text id="se6003"
pythn
```

Should

the system

return

nothing?

Users

expect

```text id="se6004"
Python
```

Search engines

can handle

these situations.

______________________________________________________________________

# The Idea

Instead of

searching

inside

the database,

copy

searchable data

into

a dedicated

Search Engine.

______________________________________________________________________

# What is a Search Engine?

A **Search Engine**

is a specialized

system

designed

to efficiently

index,

search,

and rank

large amounts

of text data.

It is optimized

for:

- Full-text search
- Relevance ranking
- Fuzzy search
- Filtering
- Aggregations

______________________________________________________________________

# Architecture

```text id="se6005"
Application

↓

PostgreSQL

↓

Indexer

↓

Search Engine
```

The database

remains

the source

of truth.

The Search Engine

stores

an optimized

search index.

______________________________________________________________________

# Search Flow

```text id="se6006"
Client

↓

Search API

↓

Search Engine

↓

Results
```

Notice

the application

doesn't query

PostgreSQL

for

search requests.

______________________________________________________________________

# Full-Text Search

Instead of

looking

for

exact matches,

Search Engines

understand

text.

Example

Searching

for

```text id="se6007"
machine learning
```

may also

match

- Machine Learning
- Learning Machines
- Machine-Learning

depending

on

the analyzer.

______________________________________________________________________

# What is an Index?

Interview favorite.

An **Index**

is

an optimized

data structure

that enables

fast searching.

Instead of

scanning

every document,

the Search Engine

uses

its index.

______________________________________________________________________

# Inverted Index

The core

of

most search engines.

Instead of

mapping

documents

to words,

it maps

words

to documents.

Example

```text id="se6008"
Python

↓

Doc 1

Doc 8

Doc 15
```

```text id="se6009"
FastAPI

↓

Doc 2

Doc 8
```

Searching

becomes

extremely fast.

______________________________________________________________________

# Document

Search Engines

store

**Documents**.

Example

```json id="se6010"
{
  "id": 101,
  "title": "Learning Python",
  "author": "John",
  "category": "Programming"
}
```

Documents

are usually

JSON objects.

______________________________________________________________________

# Indexing

Before

documents

can be searched,

they must

be indexed.

Workflow

```text id="se6011"
Database

↓

Indexer

↓

Search Engine
```

Indexing

creates

the inverted index.

______________________________________________________________________

# Keeping the Index Updated

Suppose

a book

changes title.

The database

updates first.

Then

an event

updates

the Search Engine.

```text id="se6012"
Database Update

↓

Kafka

↓

Indexer

↓

Search Engine
```

Event-Driven

index updates

are common

in production.

______________________________________________________________________

# Relevance Scoring

Interview favorite.

Search Engines

don't simply

return

matching documents.

They rank them.

Example

Searching

```text id="se6013"
python fastapi
```

Results

appear

from

most relevant

to

least relevant.

Ranking

considers

many factors,

including

term frequency,

field importance,

and

document statistics.

______________________________________________________________________

# Tokenization

Suppose

the title

is

```text id="se6014"
Learning FastAPI with Python
```

The Search Engine

breaks it

into tokens.

```text id="se6015"
Learning

FastAPI

Python
```

Searching

becomes easier.

______________________________________________________________________

# Stemming

Suppose

users search

for

```text id="se6016"
running
```

The Search Engine

recognizes

that

```text id="se6017"
run
```

and

```text id="se6018"
runs
```

may represent

the same word.

______________________________________________________________________

# Fuzzy Search

Suppose

a typo occurs.

```text id="se6019"
pythn
```

Search Engines

can still

return

```text id="se6020"
Python
```

This greatly

improves

user experience.

______________________________________________________________________

# Filters

Search results

can also

be filtered.

Example

```text id="se6021"
Category

Programming
```

```text id="se6022"
Language

English
```

Filtering

is much faster

than

application-side filtering.

______________________________________________________________________

# Aggregations

Suppose

you want

to know

how many books

exist

per category.

Example

```text id="se6023"
Programming

12,000
```

```text id="se6024"
Science

8,500
```

Search Engines

perform

aggregations

very efficiently.

______________________________________________________________________

# Elasticsearch

Elasticsearch

is

one of

the world's

most popular

distributed

search engines.

Built on

Apache Lucene,

it supports:

- Full-text search
- Aggregations
- Distributed indexing
- REST APIs

______________________________________________________________________

# OpenSearch

OpenSearch

is

an open-source

search engine

derived from

Elasticsearch.

Its APIs

are largely compatible,

making migration

straightforward

for many applications.

______________________________________________________________________

# Cluster Architecture

```text id="se6025"
Cluster

↓

Node 1

Node 2

Node 3
```

Data

is distributed

across

multiple nodes.

______________________________________________________________________

# Shards

Large indexes

are split

into

Shards.

```text id="se6026"
Books Index

↓

Shard 1

Shard 2

Shard 3
```

Each shard

stores

part

of

the index.

______________________________________________________________________

# Replica Shards

Like databases,

Search Engines

use

replicas.

Benefits:

- High availability
- Faster search
- Fault tolerance

______________________________________________________________________

# FastAPI Example

Suppose

the API

receives

```text id="se6027"
GET /search?q=python
```

Instead of

querying

PostgreSQL,

the API

queries

Elasticsearch

or

OpenSearch.

______________________________________________________________________

# AI/ML Example

Suppose

users search

for

research papers.

Traditional

Search Engines

find

keyword matches.

Later,

we'll study

Vector Databases,

which find

semantic similarity

instead.

Many AI systems

combine both.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Products

are stored

in PostgreSQL.

Search

uses

Elasticsearch.

When

a product

changes,

an event

updates

the search index.

Users

receive

fast,

ranked,

and typo-tolerant

search results.

______________________________________________________________________

# Search Engine vs Database

Interview favorite.

| Database | Search Engine |
| ----------------- | -------------------- |
| Source of truth | Search index |
| ACID transactions | Optimized for search |
| CRUD operations | Full-text search |
| SQL | Search DSL |

Most systems

use

both together.

______________________________________________________________________

# Search Engine vs Cache

| Cache | Search Engine |
| ------------------------------- | ------------------------- |
| Stores frequently accessed data | Builds searchable indexes |
| Redis | Elasticsearch/OpenSearch |
| Key-value lookups | Full-text search |

______________________________________________________________________

# Benefits

Search Engines provide:

✅ Extremely fast search

✅ Relevance ranking

✅ Typo tolerance

✅ Filtering

✅ Aggregations

______________________________________________________________________

# Drawbacks

They also introduce:

❌ Extra infrastructure

❌ Index synchronization

❌ Eventual consistency

❌ Additional storage

______________________________________________________________________

# When NOT to Use a Search Engine

Avoid

introducing

a Search Engine

when:

- Small datasets
- Exact key lookups
- Simple CRUD applications

A relational database

may be

sufficient.

______________________________________________________________________

# Best Practices

✅ Keep

the database

as

the source of truth.

✅ Update

the index

asynchronously.

✅ Monitor

index health.

✅ Design

appropriate mappings.

______________________________________________________________________

# Common Mistakes

### Treating Elasticsearch as the Primary Database

Search Engines

are optimized

for search,

not

as

the primary

transactional datastore.

______________________________________________________________________

### Forgetting Index Updates

If

the index

isn't updated,

users

see

stale search results.

______________________________________________________________________

### Indexing Everything

Not every field

needs

to be searchable.

Index only

what users

search or filter.

______________________________________________________________________

### Large Documents

Keep documents

focused.

Avoid

storing

unnecessary data

inside

the index.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why do large applications use Elasticsearch or OpenSearch instead of SQL `LIKE` queries?

Relational databases are designed for transactional workloads, while search engines are optimized for full-text search.
Elasticsearch and OpenSearch build inverted indexes that allow extremely fast keyword lookups, relevance ranking, fuzzy
matching, filtering, and aggregations. This enables applications to provide typo-tolerant, ranked search results over
millions of documents without overloading the primary database. The transactional database remains the source of truth,
while the search engine maintains a searchable index that is updated asynchronously.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Why Search Engines exist
- Full-Text Search
- Inverted Index
- Documents
- Indexing
- Relevance Scoring
- Elasticsearch
- OpenSearch
- Shards
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand modern data storage and retrieval:

- ✅ Database Replication
- ✅ Database Sharding
- ✅ Object Storage
- ✅ Search Engines

The next lesson covers one of the most important technologies in modern AI systems:

> **Vector Databases**, which power semantic search, Retrieval-Augmented Generation (RAG), recommendation systems, and LLM applications.

______________________________________________________________________

# What's Next

[Vector Databases](61-vector-databases.md)
