# System Design – Search Autocomplete

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how to design a scalable Search Autocomplete system like Google, Amazon, YouTube, or Netflix using Tries, caching, ranking, distributed search, and real-time updates.

______________________________________________________________________

# Introduction

Every major application

provides

search suggestions.

Examples

```
Google

↓

"python"

↓

python tutorial

python download

python interview questions
```

```
Amazon

↓

"iphone"

↓

iphone 16

iphone charger

iphone case
```

The challenge

is

returning

relevant suggestions

within

milliseconds.

______________________________________________________________________

# Functional Requirements

Assume

the system

supports

- Search suggestions
- Prefix search
- Trending searches
- Personalized suggestions
- Real-time updates
- Typo tolerance (optional)

______________________________________________________________________

# Non-Functional Requirements

Need

- Low latency (\<100 ms)
- High Availability
- Massive Scalability
- High Read Throughput
- Fault Tolerance

______________________________________________________________________

# Step 1

# High-Level Architecture

```
                    Users
                       │
                       ▼
                 Load Balancer
                       │
                       ▼
                 API Gateway
                       │
                       ▼
              Search Service
                 │         │
                 ▼         ▼
             Redis      Trie Cache
                 │
                 ▼
          Search Database
                 │
                 ▼
         Analytics Pipeline
```

______________________________________________________________________

# Core Services

Separate

the application

into

multiple services.

- Search Service
- Suggestion Service
- Ranking Service
- Analytics Service
- Index Builder
- Cache Service

______________________________________________________________________

# APIs

Search Suggestions

```
GET /autocomplete?q=py
```

Response

```json
[
  "python",
  "python tutorial",
  "python interview questions"
]
```

______________________________________________________________________

# Step 2

# Why SQL Isn't Enough

Suppose

the database

contains

```
100 Million Queries
```

Searching

every row

for

every keystroke

would be

too slow.

Need

specialized

data structures.

______________________________________________________________________

# Trie

Interview favorite.

A Trie

(Prefix Tree)

stores

characters

instead of

complete words.

______________________________________________________________________

# Example

Words

```
cat

car

cart
```

Trie

```
        Root
       /   \
      c
      |
      a
     / \
    t   r
         \
          t
```

Common prefixes

are shared.

______________________________________________________________________

# Why Trie?

Searching

for

```
ca
```

immediately

narrows

the search

to

```
cat

car

cart
```

Complexity

depends

mainly

on

the prefix length,

not

the number

of stored words.

______________________________________________________________________

# Search Flow

```
User Types

↓

"py"

↓

Trie

↓

Suggestions
```

Very fast.

______________________________________________________________________

# Step 3

# Ranking Suggestions

Returning

every match

is

not useful.

Need

ranking.

Factors

include

- Search frequency
- Recency
- User history
- Popularity
- Click-through rate

______________________________________________________________________

# Example

Prefix

```
py
```

Possible

matches

```
python

pyramid

pygame
```

Rank

using

popularity.

______________________________________________________________________

# Personalized Results

Suppose

one user

often searches

```
python
```

Another

searches

```
pytorch
```

Same prefix

↓

Different suggestions.

Personalization

improves

user experience.

______________________________________________________________________

# Step 4

# Caching

Interview favorite.

Popular prefixes

are requested

frequently.

Example

```
a

i

p

s
```

Store

their suggestions

inside

Redis.

```
"py"

↓

Redis

↓

Suggestions
```

______________________________________________________________________

# Cache Miss

```
Redis

↓

Trie

↓

Store In Cache

↓

Return Result
```

______________________________________________________________________

# Step 5

# Analytics

Every search

creates

an event.

```
Search

↓

Kafka

↓

Analytics
```

Later

used

to improve

ranking.

______________________________________________________________________

# Step 6

# Updating Suggestions

Suppose

a new movie

is released.

Searches

increase.

Ranking

should update.

Instead of

rebuilding

the Trie

for

every search,

batch

or stream

updates

through

an indexing pipeline.

______________________________________________________________________

# Index Builder

```
Search Logs

↓

Analytics

↓

Index Builder

↓

New Trie
```

Then

deploy

updated indexes.

______________________________________________________________________

# Step 7

# Typo Tolerance

Interview bonus.

User types

```
pyhton
```

Suggestions

may still

return

```
python
```

Possible techniques

include

edit-distance algorithms

or

fuzzy matching

implemented

alongside

the main index.

______________________________________________________________________

# Step 8

# Distributed Search

One server

cannot store

all data.

Split

the index

across

multiple servers.

```
Users

↓

Load Balancer

↓

Search Node A

Search Node B

Search Node C
```

______________________________________________________________________

# Sharding

Shard

using

alphabet

or

hash.

Example

```
A-F

↓

Node 1
```

```
G-M

↓

Node 2
```

```
N-Z

↓

Node 3
```

Many production systems

prefer

hash-based

or

balanced partitioning

to avoid

hotspots.

______________________________________________________________________

# Replication

Each node

has

replicas.

```
Primary

↓

Replica

↓

Replica
```

Provides

high availability.

______________________________________________________________________

# Monitoring

Monitor

- Query latency
- Cache hit ratio
- Search volume
- Popular queries
- Error rate
- Ranking freshness

______________________________________________________________________

# Failure Scenarios

## Cache Failure

Fallback

to

Trie

or

search index.

______________________________________________________________________

## Search Node Failure

Route

traffic

to

replicas.

______________________________________________________________________

## Analytics Failure

Suggestions

continue working.

Ranking updates

are delayed.

______________________________________________________________________

## Index Build Failure

Continue

serving

the previous

stable index.

______________________________________________________________________

# Typical Architecture

```
                     Users
                        │
                        ▼
                 Load Balancer
                        │
                        ▼
                 Search Service
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
        Redis Cache           Search Index
            │                       │
            ▼                       ▼
        Ranking Engine      Trie / Search Nodes
            │
            ▼
      Kafka Analytics
            │
            ▼
       Index Builder
```

______________________________________________________________________

# Complexity

Trie

Insertion

```
O(L)
```

Search

```
O(L)
```

Where

```
L

=

Length of Prefix
```

______________________________________________________________________

# Common Interview Questions

## Why use a Trie?

A Trie shares common prefixes and enables efficient prefix-based lookups whose complexity depends mainly on the prefix
length rather than the total number of stored words.

______________________________________________________________________

## Why cache autocomplete results?

Popular prefixes are requested repeatedly. Caching their suggestions significantly reduces latency and backend load.

______________________________________________________________________

## Why separate ranking from searching?

Searching finds candidate suggestions, while ranking determines which suggestions are most relevant based on popularity,
personalization, and other signals.

______________________________________________________________________

## How are suggestions updated?

Search events are collected, analytics generate updated rankings, and an indexing pipeline periodically or continuously
rebuilds and deploys refreshed indexes.

______________________________________________________________________

# Common Mistakes

## Querying SQL For Every Keystroke

Traditional

database queries

do not scale

well

for

autocomplete.

______________________________________________________________________

## Returning Every Match

Always

rank

results.

______________________________________________________________________

## No Cache

Popular prefixes

should be

cached.

______________________________________________________________________

## Ignoring Personalization

Different users

may expect

different suggestions.

______________________________________________________________________

## Rebuilding Index Continuously

Use

batch

or

incremental

updates.

______________________________________________________________________

# Best Practices

✅ Use Tries or specialized search indexes.

✅ Cache popular prefixes.

✅ Separate search from ranking.

✅ Collect analytics continuously.

✅ Rebuild indexes safely.

✅ Replicate search nodes.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is a Trie commonly used for autocomplete?

### Answer

A Trie efficiently stores words by shared prefixes, allowing prefix searches to complete in time proportional to the
prefix length instead of scanning the full dataset.

______________________________________________________________________

## Question

Why isn't Redis enough for autocomplete?

### Answer

Redis is excellent for caching frequently requested prefixes, but it is not a complete replacement for the underlying
search index. The index remains the source for uncached queries and updates.

______________________________________________________________________

## Question

How would you scale autocomplete to billions of searches?

### Answer

Distribute the search index across multiple nodes, replicate each shard for availability, cache popular prefixes,
process search analytics asynchronously, and periodically rebuild or incrementally update ranking indexes.

______________________________________________________________________

# Practice Exercise

Design

Search Autocomplete

for

Google.

Explain

1. API design
1. Trie structure
1. Ranking strategy
1. Caching
1. Analytics pipeline
1. Index updates
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Personalization
1. Trade-offs

Present

your solution

within

45 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

Search Autocomplete is a classic System Design interview problem because it combines efficient data structures with
large-scale distributed architecture.

A strong solution should demonstrate

- Trie-based prefix searching
- Ranking
- Caching
- Analytics
- Index rebuilding
- Replication
- Sharding
- High availability
- Low latency
- Trade-off analysis

Mastering Search Autocomplete prepares you for interviews involving search engines, e-commerce platforms, media
services, and recommendation systems.

______________________________________________________________________

# Next

[System Design – Distributed Cache](31-design-distributed-cache.md)
