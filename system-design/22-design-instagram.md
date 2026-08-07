# System Design Case Study – Instagram

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design Instagram from scratch by applying System Design concepts such as CDN, caching, sharding, message queues, object storage, feed generation, and scaling strategies.

______________________________________________________________________

# Introduction

Instagram

is one of

the most common

System Design interviews.

It combines

almost everything

you've learned.

- API Design
- Object Storage
- CDN
- Redis
- Database
- Sharding
- Replication
- Message Queues
- Feed Generation
- Caching
- Search
- Notifications

This chapter

focuses on

designing

Instagram's

core platform.

______________________________________________________________________

# Step 1

# Clarify Requirements

Never

start drawing

architecture.

Ask questions.

Example

```
Can users

upload photos?
```

```
Should videos

be supported?
```

```
Do we need

stories?
```

```
Should comments

exist?
```

```
Should likes

be real-time?
```

```
Should notifications

exist?
```

Interviewers

expect

clarification.

______________________________________________________________________

# Functional Requirements

Assume

Instagram supports

- User registration
- Login
- Upload photos
- View feed
- Like posts
- Comment
- Follow users
- Notifications

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Low Latency
- Massive Scalability
- Fault Tolerance
- High Read Throughput
- Reliable Media Storage

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
1 Billion Users
```

```
300 Million DAU
```

Each user

uploads

```
2 Photos/day
```

Daily uploads

```
600 Million Photos
```

______________________________________________________________________

# Image Storage

Suppose

each photo

is

```
2 MB
```

Daily storage

```
600M

×

2 MB

=

1.2 PB/day
```

Object storage

is mandatory.

______________________________________________________________________

# Read Traffic

Suppose

each user

views

```
200 Posts/day
```

Daily feed requests

```
60 Billion
```

Read-heavy system.

______________________________________________________________________

# Step 3

# High-Level Architecture

```
                    Users
                       │
                       ▼
                     DNS
                       │
                       ▼
                Load Balancer
                       │
                       ▼
                 API Gateway
                       │
     ┌──────────┬──────────┬──────────┐
     ▼          ▼          ▼
 User API   Feed API   Upload API
     │          │          │
     ▼          ▼          ▼
 Redis      Database   Object Storage
     │                      │
     ▼                      ▼
 Notifications         CDN
```

______________________________________________________________________

# Core Services

Split

the application

into

microservices.

- User Service
- Feed Service
- Media Service
- Like Service
- Comment Service
- Follow Service
- Notification Service
- Search Service

______________________________________________________________________

# API Design

Upload

```
POST /posts
```

Feed

```
GET /feed
```

Like

```
POST /posts/{id}/like
```

Comment

```
POST /posts/{id}/comments
```

Follow

```
POST /users/{id}/follow
```

______________________________________________________________________

# Step 4

# Database Design

Users

| id | username | profile |

Posts

| id | user_id | image_url | created_at |

Followers

| follower | following |

Comments

| id | post_id | comment |

Likes

| user_id | post_id |

______________________________________________________________________

# Which Database?

User relationships

fit well

in relational databases.

Posts

can also be stored

in relational databases

at moderate scale,

while some architectures

use NoSQL

for feed-related data.

The key

is

explaining

trade-offs.

______________________________________________________________________

# Step 5

# Image Storage

Never

store images

inside

the database.

Instead

```
Upload

↓

Object Storage

↓

URL Stored

↓

Database
```

Database

stores

metadata.

Object Storage

stores

media.

______________________________________________________________________

# Why Object Storage?

Object Storage

provides

- Massive scalability
- High durability
- Low cost
- Easy CDN integration

______________________________________________________________________

# Step 6

# CDN

Users

should not

download

images

directly

from Object Storage.

```
User

↓

CDN

↓

Object Storage
```

Benefits

- Lower latency
- Reduced bandwidth
- Global delivery

______________________________________________________________________

# Step 7

# Feed Generation

Interview favorite.

How do users

see

their feed?

Two approaches.

______________________________________________________________________

# Fan-Out On Write

When

a user

uploads

a photo

```
Upload

↓

Followers

↓

Feed Updated
```

Feeds

are

precomputed.

Reads

become

extremely fast.

______________________________________________________________________

# Advantages

- Fast feed loading
- Low read latency

______________________________________________________________________

# Disadvantages

Celebrity problem.

Suppose

a celebrity

has

100 Million Followers.

Generating

100 Million feeds

is expensive.

______________________________________________________________________

# Fan-Out On Read

Instead

generate

the feed

when requested.

```
User Opens Feed

↓

Query Posts

↓

Return Feed
```

Writes

become cheap.

Reads

become expensive.

______________________________________________________________________

# Hybrid Approach

Instagram-like systems

often combine

both approaches.

Normal users

↓

Fan-Out On Write

Celebrities

↓

Fan-Out On Read

Balances

performance

and cost.

______________________________________________________________________

# Step 8

# Caching

Redis

stores

- User profiles
- Feed
- Popular posts
- Session tokens
- Follow counts

Without Redis

database load

would be enormous.

______________________________________________________________________

# Feed Cache

Example

```
User 101

↓

Feed

↓

Redis
```

Opening

the app

becomes

very fast.

______________________________________________________________________

# Step 9

# Likes

Likes

must feel

instant.

Flow

```
User Likes

↓

Redis Counter

↓

Database

↓

Async Update
```

Counters

can later

be synchronized,

depending on

consistency requirements.

______________________________________________________________________

# Step 10

# Comments

Comments

are write-heavy.

Store

inside

database.

Popular comments

can be cached.

______________________________________________________________________

# Step 11

# Notifications

Notifications

should be

asynchronous.

```
Like

↓

RabbitMQ / Kafka

↓

Notification Service

↓

Push Notification
```

User

doesn't wait

for

notification delivery.

______________________________________________________________________

# Step 12

# Search

Searching

by username

requires

indexes.

Large-scale

search

often uses

a dedicated

search engine.

Example

```
Search Service

↓

Elasticsearch
```

______________________________________________________________________

# Step 13

# Database Replication

```
Primary

↓

Replica

↓

Replica
```

Reads

go

to replicas.

Writes

go

to

primary.

______________________________________________________________________

# Step 14

# Database Sharding

Eventually

billions

of users

exist.

Shard

using

```
User ID
```

or

another

high-cardinality key.

______________________________________________________________________

# Step 15

# Consistent Hashing

Adding

new shards

should

move

minimal data.

Consistent Hashing

helps

with

horizontal scaling.

______________________________________________________________________

# Step 16

# Message Queue

Used for

- Notifications
- Analytics
- Feed generation
- Image processing
- Spam detection

______________________________________________________________________

# Step 17

# Image Processing

Original image

↓

Queue

↓

Worker

↓

Generate

- Thumbnail
- Medium
- Large

Store

all versions

in

Object Storage.

______________________________________________________________________

# Step 18

# Analytics

Every action

creates

an event.

```
Like

↓

Kafka

↓

Analytics
```

Large-scale

event streaming

fits well.

______________________________________________________________________

# Step 19

# Rate Limiting

Prevent

spam.

Example

```
100 Posts/day
```

```
1000 Likes/hour
```

```
500 Comments/hour
```

______________________________________________________________________

# Step 20

# High Availability

```
Multiple API Servers

↓

Redis Cluster

↓

Replicated Database

↓

Object Storage

↓

CDN
```

No

single point

of failure.

______________________________________________________________________

# Failure Scenarios

## Redis Down

Fallback

to

database.

Performance

decreases.

______________________________________________________________________

## Object Storage Unavailable

New uploads

may fail,

while previously cached

content

may still be served

from the CDN

until cache entries expire.

______________________________________________________________________

## Database Primary Down

Replica

becomes

new primary.

______________________________________________________________________

## Queue Failure

Events

remain

inside

the queue

until

workers recover.

______________________________________________________________________

# Read vs Write Ratio

Reads

far exceed

writes.

Optimize

for

reading.

______________________________________________________________________

# CAP Discussion

Feed

can tolerate

slight delay.

Notifications

can tolerate

slight delay.

Likes

can tolerate

eventual consistency

for counts,

while user interactions

should still

feel immediate.

______________________________________________________________________

# Monitoring

Monitor

- Feed latency
- Image upload latency
- Cache hit ratio
- Queue length
- API latency
- Error rate
- Storage usage

______________________________________________________________________

# Possible Improvements

- Stories
- Reels
- Live Streaming
- AI Recommendations
- Hashtags
- Image Recognition
- Spam Detection
- Content Moderation
- Draft Posts

______________________________________________________________________

# Complete Architecture

```
                     Users
                        │
                        ▼
                      DNS
                        │
                        ▼
                 Load Balancer
                        │
                        ▼
                  API Gateway
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   User Service    Feed Service    Media Service
        │               │                │
        ▼               ▼                ▼
      Redis        Primary DB      Object Storage
        │               │                │
        │         Read Replicas          ▼
        │               │               CDN
        └───────────────┼────────────────┘
                        ▼
                 RabbitMQ / Kafka
                        │
      ┌─────────────────┼────────────────┐
      ▼                 ▼                ▼
Notifications     Analytics      Image Workers
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why not store images in the database?

Databases are optimized for structured data, not large binary objects. Object storage offers better scalability,
durability, and cost efficiency for media files.

______________________________________________________________________

## Why use a CDN?

Images are requested globally and represent most of the bandwidth. A CDN serves cached copies from edge locations close
to users, reducing latency and load on the origin storage.

______________________________________________________________________

## Why is feed generation difficult?

Users follow different numbers of accounts. Precomputing every feed is fast to read but expensive to write, while
generating feeds on demand is the opposite. Large systems often use a hybrid approach.

______________________________________________________________________

## Why use Kafka for analytics?

Instagram generates billions of events such as likes, comments, follows, and views. Kafka handles high-throughput event
streaming and allows multiple downstream consumers.

______________________________________________________________________

## How would you handle celebrity users?

Avoid pushing every new post into millions of follower feeds. Instead, generate feeds dynamically (Fan-Out on Read) for
celebrity accounts while continuing to precompute feeds for regular users.

______________________________________________________________________

# Common Mistakes

## Storing Images In SQL

Store only

metadata

inside

the database.

______________________________________________________________________

## Ignoring CDN

Serving

billions

of images

directly

from storage

would be inefficient.

______________________________________________________________________

## Making Notifications Synchronous

Notifications

should be

asynchronous.

______________________________________________________________________

## Forgetting Feed Caching

Feed

is

one of

the most accessed

parts

of Instagram.

______________________________________________________________________

## Using Only Fan-Out On Write

Celebrity accounts

make

pure Fan-Out On Write

very expensive.

______________________________________________________________________

# Best Practices

✅ Store media in Object Storage.

✅ Serve media through a CDN.

✅ Cache feeds and profiles.

✅ Process notifications asynchronously.

✅ Use replication and sharding as the system grows.

✅ Use a hybrid feed generation strategy.

______________________________________________________________________

# Interview Deep Dive

## Question

Why doesn't Instagram store images in MySQL?

### Answer

Relational databases are not designed to efficiently store and serve billions of large media files. Object storage
provides better scalability, durability, lower cost, and integrates naturally with CDNs.

______________________________________________________________________

## Question

What is the biggest challenge in designing Instagram?

### Answer

Feed generation is one of the most challenging problems because it must balance low read latency with efficient write
processing while handling users with vastly different follower counts.

______________________________________________________________________

## Question

Would you choose RabbitMQ or Kafka?

### Answer

RabbitMQ is suitable for background jobs like notifications, while Kafka is an excellent choice for large-scale event
streaming, analytics, and activity pipelines. Many production systems use both for different workloads.

______________________________________________________________________

# Practice Exercise

Design Instagram

for

2 Billion Users.

Explain

1. APIs
1. Capacity estimation
1. Feed generation strategy
1. Object storage
1. CDN
1. Cache strategy
1. Database design
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Trade-offs

Try explaining

the complete design

within

45 minutes,

as if you were

in a real

System Design interview.

______________________________________________________________________

# Summary

Instagram is an excellent case study because it combines nearly every major distributed systems concept.

A strong design should demonstrate

- Requirement gathering
- Capacity estimation
- Object storage
- CDN integration
- Feed generation strategies
- Caching
- Asynchronous processing
- Replication
- Sharding
- High availability
- Trade-off analysis

Mastering Instagram prepares you for many real-world System Design interviews involving social media, content platforms,
and large-scale distributed applications.

______________________________________________________________________

# Next

[System Design Case Study – WhatsApp](23-design-whatsapp.md)
