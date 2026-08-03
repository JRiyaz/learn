# System Design - Part 88

# Elasticsearch System Design (How Elasticsearch Works Internally)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Why Elasticsearch exists
- Lucene Architecture
- Inverted Index
- Documents & Indexes
- Mappings
- Analyzers
- Shards
- Replicas
- Query Execution
- Aggregations
- Cluster Architecture
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Elasticsearch.**

Previously,

we used Elasticsearch

for:

- Product Search
- User Search
- Log Search
- Document Search

Now,

we'll understand

how Elasticsearch

works internally.

______________________________________________________________________

# Why Elasticsearch?

Suppose

you have

a database

with

100 million products.

Searching

using SQL

like

```sql id="es8801"
WHERE name LIKE '%iphone%'
```

becomes

slow

because

the database

must scan

many rows.

Elasticsearch

is built

for

fast,

full-text search.

______________________________________________________________________

# High-Level Architecture

```text id="es8802"
Application

↓

Elasticsearch Cluster

↓

Lucene
```

Elasticsearch

is built

on top of

Apache Lucene.

Lucene

handles

the actual indexing

and searching.

______________________________________________________________________

# What is an Index?

Interview favorite.

An Index

is similar

to

a database.

Example

```text id="es8803"
products

users

orders
```

Each index

contains

many documents.

______________________________________________________________________

# What is a Document?

A document

is

similar

to

a database row.

Example

```json id="es8804"
{
  "id": 101,
  "name": "iPhone 16",
  "brand": "Apple",
  "price": 79999
}
```

Documents

are stored

as

JSON.

______________________________________________________________________

# Mapping

Interview favorite.

Mappings

define

the schema

of documents.

Example

```text id="es8805"
name

↓

text
```

```text id="es8806"
price

↓

integer
```

Mappings

control

how fields

are indexed

and searched.

______________________________________________________________________

# Inverted Index

Interview favorite.

This is

the heart

of Elasticsearch.

Suppose

we have

three documents.

```text id="es8807"
Doc1

Redis Kafka

Doc2

Kafka Java

Doc3

Redis Python
```

Normal storage

stores

documents.

An

Inverted Index

stores

words.

Example

```text id="es8808"
Kafka

↓

Doc1

Doc2

Redis

↓

Doc1

Doc3
```

Searching

becomes

very fast.

______________________________________________________________________

# Why is it Called "Inverted"?

Instead of

```text id="es8809"
Document

↓

Words
```

it stores

```text id="es8810"
Word

↓

Documents
```

The relationship

is inverted.

______________________________________________________________________

# Analyzer

Interview favorite.

Before indexing,

text

is processed.

Pipeline

```text id="es8811"
Text

↓

Tokenizer

↓

Lowercase

↓

Stemmer

↓

Index
```

______________________________________________________________________

# Tokenization

Example

```text id="es8812"
System Design Course
```

↓

```text id="es8813"
System

Design

Course
```

These words

become

searchable tokens.

______________________________________________________________________

# Stemming

Example

```text id="es8814"
running

runs

runner
```

↓

```text id="es8815"
run
```

Searching

for

"run"

matches

all forms.

______________________________________________________________________

# Sharding

Interview favorite.

Suppose

an index

contains

10 TB

of data.

One server

cannot

store

everything.

Split

the index

into

shards.

```text id="es8816"
Products

↓

Shard 1

Shard 2

Shard 3
```

Each shard

is

a Lucene index.

______________________________________________________________________

# Replicas

Interview favorite.

Every shard

can have

replicas.

```text id="es8817"
Primary Shard

↓

Replica

↓

Replica
```

Benefits:

- High availability
- Faster reads

______________________________________________________________________

# Cluster

Interview favorite.

Multiple nodes

form

a cluster.

```text id="es8818"
Node A

Node B

Node C
```

Shards

are distributed

across nodes.

______________________________________________________________________

# Query Flow

```text id="es8819"
Application

↓

Coordinator Node

↓

Relevant Shards

↓

Merge Results

↓

Return
```

The coordinator

collects

results

from

multiple shards.

______________________________________________________________________

# Search Execution

Suppose

there are

5 shards.

```text id="es8820"
Query

↓

Shard 1

Shard 2

Shard 3

Shard 4

Shard 5
```

Each shard

searches

its own

documents.

Results

are merged.

______________________________________________________________________

# Relevance Scoring

Interview favorite.

Not every

matching document

is equally relevant.

Elasticsearch

computes

a relevance score.

Factors include:

- Term frequency
- Inverse document frequency
- Field length
- BM25 algorithm

Documents

with higher scores

appear first.

______________________________________________________________________

# Aggregations

Interview favorite.

Search

isn't

the only feature.

Example

```text id="es8821"
Average Price
```

```text id="es8822"
Products per Brand
```

```text id="es8823"
Top Categories
```

Aggregations

allow

analytics

without

moving data

to another system.

______________________________________________________________________

# Write Flow

Workflow

```text id="es8824"
Application

↓

Primary Shard

↓

Replica Shards
```

The primary

handles

the write.

Replicas

receive

the update.

______________________________________________________________________

# Refresh

Interview favorite.

Writes

are not

immediately searchable.

Elasticsearch

periodically

refreshes

its indexes.

Default

is approximately

```text id="es8825"
1 Second
```

Trade-off:

Frequent refreshes

improve

search freshness,

but

reduce

write throughput.

______________________________________________________________________

# Near Real-Time Search

Interview favorite.

Elasticsearch

is

Near Real-Time,

not

strictly real-time.

There is

usually

a small delay

before

new documents

become searchable.

______________________________________________________________________

# Scaling

Scale

by adding:

- Nodes
- Shards

```text id="es8826"
Node A

Node B

Node C

Node D
```

The cluster

rebalances

shards.

______________________________________________________________________

# Failure Scenario

Suppose

Node B

fails.

Replica shards

are promoted

to

Primary.

The cluster

continues

serving queries.

______________________________________________________________________

# Another Failure

Suppose

one shard

is unavailable.

Queries

may return

partial results,

depending

on

cluster settings.

Once

the node

recovers,

the shard

is synchronized.

______________________________________________________________________

# End-to-End Architecture

```text id="es8827"
Application

↓

Coordinator Node

↓

Primary Shards

↓

Replica Shards

↓

Lucene Segments

↓

Disk
```

______________________________________________________________________

# Trade-offs

More Shards

vs

Fewer Shards

| More | Fewer |
| ------------------ | ----------------- |
| Better parallelism | Simpler |
| More metadata | Lower overhead |
| Higher scalability | Easier management |

______________________________________________________________________

Replicas

vs

No Replicas

| Replicas | No Replicas |
| ---------------------- | ------------- |
| High availability | Lower storage |
| Faster reads | No redundancy |
| Better fault tolerance | Simpler |

______________________________________________________________________

Elasticsearch

vs

SQL Database

| Elasticsearch | SQL |
| ----------------- | ------------ |
| Full-text search | Transactions |
| Relevance ranking | ACID |
| Analytics | Joins |

______________________________________________________________________

# Best Practices

✅ Choose the correct number of shards.

✅ Use replicas for fault tolerance.

✅ Design mappings carefully.

✅ Monitor cluster health.

✅ Use keyword fields for exact matches.

✅ Use text fields for full-text search.

______________________________________________________________________

# Common Mistakes

### Using Elasticsearch as the Primary Database

Elasticsearch

is optimized

for

search,

not

transactions.

Keep

a relational

or

NoSQL database

as

the source of truth.

______________________________________________________________________

### Too Many Shards

Every shard

consumes:

- Memory
- CPU
- File handles

Avoid

creating

thousands

of tiny shards.

______________________________________________________________________

### Ignoring Mappings

Poor mappings

lead to:

- Slow queries
- Incorrect search results
- Increased storage

______________________________________________________________________

### Refreshing Too Frequently

Very frequent

refreshes

reduce

indexing throughput.

Balance

search freshness

against

write performance.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Elasticsearch?

Design Elasticsearch as a distributed search engine built on Apache Lucene. Organize data into indexes containing JSON
documents. Before indexing, process text through analyzers that tokenize, normalize, and stem words to build an inverted
index. Partition indexes into shards for horizontal scalability and replicate shards across nodes for fault tolerance
and faster reads. Route search requests through a coordinator node that queries relevant shards in parallel, merges the
results, ranks them using BM25 relevance scoring, and returns the top matches. Support aggregations for analytics,
configure mappings carefully, and treat Elasticsearch as a search engine rather than the system of record.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Lucene architecture
- Documents & indexes
- Mappings
- Inverted index
- Tokenization
- Stemming
- Shards
- Replicas
- Query execution
- BM25 ranking
- Aggregations
- Near real-time search
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ Apache Kafka Internals
- ✅ Redis Internals
- ✅ Nginx Internals
- ✅ Elasticsearch Internals

You now understand the four infrastructure technologies that power most modern backend systems:

- Messaging (Kafka)
- Caching (Redis)
- Reverse Proxy & Load Balancing (Nginx)
- Search (Elasticsearch)

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll begin **Advanced Distributed Systems** with one of the most frequently asked senior-level interview topics:

- Mutual exclusion
- Distributed coordination
- Redis locks
- Redlock algorithm
- ZooKeeper
- etcd
- Lease-based locking
- Failure scenarios

We'll design **Distributed Locking**.

______________________________________________________________________

# What's Next

[Distributed Locking System Design](89-distributed-locking-system-design.md)
