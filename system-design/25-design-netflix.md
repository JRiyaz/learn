# System Design Case Study – Netflix

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design a global video streaming platform like Netflix by applying concepts such as CDN, object storage, caching, video encoding, recommendation systems, message queues, and distributed systems.

______________________________________________________________________

# Introduction

Netflix

is one of

the most popular

System Design interviews.

Unlike

WhatsApp

or

Uber,

Netflix focuses on

```
Video Streaming
```

The biggest challenges are

- Massive video storage
- Global content delivery
- Video encoding
- Recommendation engine
- Low latency streaming
- High availability

______________________________________________________________________

# Step 1

# Clarify Requirements

Before

designing,

ask questions.

Example

```
Video Streaming?
```

```
Movie Upload?
```

```
TV Shows?
```

```
Adaptive Streaming?
```

```
Recommendations?
```

```
Search?
```

```
Watch History?
```

______________________________________________________________________

# Functional Requirements

Assume

Netflix supports

- User registration
- Login
- Video streaming
- Search
- Watch history
- Recommendations
- Continue watching
- Ratings

______________________________________________________________________

# Non-Functional Requirements

Need

- Extremely high availability
- Low startup latency
- Global scalability
- Fault tolerance
- Massive storage
- High throughput

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
300 Million Users
```

```
150 Million DAU
```

Suppose

```
50 Million

Concurrent Streams
```

Average

video bitrate

```
5 Mbps
```

Bandwidth

required

```
250 Tbps
```

Clearly,

a CDN

is mandatory.

______________________________________________________________________

# Storage Estimation

Suppose

Netflix stores

```
100,000 Videos
```

Average

size

```
5 GB
```

Storage

```
≈500 TB
```

In reality,

multiple encoded versions,

subtitles,

and metadata

increase storage

significantly.

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
       ┌─────────┬──────────┬─────────────┐
       ▼         ▼          ▼
 User Service Search   Streaming Service
       │         │          │
       ▼         ▼          ▼
    Redis     Database   CDN
                          │
                          ▼
                   Object Storage
```

______________________________________________________________________

# Core Services

Split

the platform

into

microservices.

- User Service
- Streaming Service
- Search Service
- Recommendation Service
- Watch History Service
- Billing Service
- Notification Service
- Encoding Service

______________________________________________________________________

# APIs

Get Home Page

```
GET /home
```

Play Video

```
GET /videos/{id}
```

Search

```
GET /search?q=batman
```

Continue Watching

```
GET /continue
```

______________________________________________________________________

# Step 4

# Video Upload

Content creators

upload

high-quality videos.

```
Upload

↓

Object Storage

↓

Encoding Queue
```

Original videos

are never

served directly.

______________________________________________________________________

# Step 5

# Video Encoding

Interview favorite.

Original video

↓

Encoding Workers

↓

Generate

- 240p
- 360p
- 480p
- 720p
- 1080p
- 4K

Each version

is stored

in

Object Storage.

______________________________________________________________________

# Why Multiple Versions?

Different users

have

different

internet speeds.

Adaptive streaming

selects

the most appropriate

quality.

______________________________________________________________________

# Adaptive Bitrate Streaming

Example

```
Fast Internet

↓

1080p
```

```
Slow Internet

↓

480p
```

Quality

changes

automatically

during playback.

Protocols such as

HLS

or

MPEG-DASH

are commonly used.

______________________________________________________________________

# Step 6

# CDN

Interview favorite.

Videos

should not

be streamed

directly

from

Object Storage.

```
User

↓

CDN

↓

Nearest Edge Server

↓

Object Storage
```

Benefits

- Lower latency
- Reduced bandwidth
- Better user experience

______________________________________________________________________

# Step 7

# Caching

Redis

stores

- User sessions
- Continue Watching
- Trending movies
- Search suggestions
- Frequently accessed metadata

Large video files

remain

on

the CDN,

not Redis.

______________________________________________________________________

# Step 8

# Search

Search

requires

fast indexing.

```
Search Service

↓

Search Engine
```

Common choice

```
Elasticsearch
```

Supports

full-text search

and ranking.

______________________________________________________________________

# Step 9

# Recommendation Engine

Interview favorite.

Recommendations

are generated

using

- Watch history
- Ratings
- Viewing patterns
- Similar users
- Popularity
- ML models

______________________________________________________________________

# Recommendation Flow

```
Watch Event

↓

Kafka

↓

Recommendation Engine

↓

Recommended Videos
```

Recommendations

are updated

asynchronously.

______________________________________________________________________

# Step 10

# Watch History

Every playback

creates

events.

```
Play

Pause

Resume

Complete
```

Store

history

asynchronously.

______________________________________________________________________

# Continue Watching

When

a user

stops

at

```
32:15
```

Store

the playback position.

Next login

continues

from

that timestamp.

______________________________________________________________________

# Step 11

# Billing

Billing

should be

an independent service.

```
Subscription

↓

Payment Gateway

↓

Billing Service
```

______________________________________________________________________

# Step 12

# Notifications

Examples

- New season
- New recommendations
- Subscription expiry

Notifications

should be

asynchronous.

```
Kafka

↓

Notification Service

↓

Push Notification
```

______________________________________________________________________

# Step 13

# Database Design

Users

| id | profile |

Videos

| id | title | duration |

History

| user | video | timestamp |

Subscriptions

| user | plan |

Recommendations

| user | video |

______________________________________________________________________

# Step 14

# Replication

```
Primary

↓

Replica

↓

Replica
```

Improves

availability

for

metadata

and

user information.

______________________________________________________________________

# Step 15

# Sharding

As

watch history

grows,

shard

using

```
User ID
```

Large-scale

history tables

benefit

from

horizontal scaling.

______________________________________________________________________

# Step 16

# Message Queue

Kafka

is well suited

for

- Playback events
- Recommendations
- Analytics
- Logging
- Notifications

______________________________________________________________________

# Step 17

# Monitoring

Monitor

- Video startup time
- Buffering ratio
- CDN hit ratio
- API latency
- Search latency
- Encoding failures
- Playback failures

______________________________________________________________________

# Failure Scenarios

## CDN Node Failure

Traffic

is routed

to

another edge location.

Users

may experience

slightly higher latency,

but

streaming continues.

______________________________________________________________________

## Encoding Worker Failure

Encoding jobs

remain

inside

the queue

until

another worker

processes them.

______________________________________________________________________

## Database Failure

Replica

becomes

new primary.

______________________________________________________________________

## Object Storage Failure

Redundant storage

across

multiple availability zones

or regions

reduces

the impact

of failures.

______________________________________________________________________

# CAP Discussion

Streaming

prioritizes

Availability.

Recommendation updates

can be

eventually consistent.

Billing

requires

strong consistency.

Different services

choose

different trade-offs.

______________________________________________________________________

# Typical Architecture

```
                     Users
                        │
                        ▼
                 Load Balancer
                        │
                        ▼
                  API Gateway
                        │
       ┌─────────┬──────────────┬────────────┐
       ▼         ▼              ▼
 Streaming  Recommendation   Search Service
   Service      Service
       │         │              │
       ▼         ▼              ▼
     CDN      Kafka       Elasticsearch
       │         │
       ▼         ▼
 Object Storage Redis
       │
       ▼
  Encoding Workers
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why use a CDN?

Streaming large video files directly from the origin would create excessive latency and bandwidth costs. CDNs cache
content close to users, reducing startup time and improving playback.

______________________________________________________________________

## Why encode videos into multiple qualities?

Users have different devices and network conditions. Multiple encoded versions enable adaptive bitrate streaming for a
smoother viewing experience.

______________________________________________________________________

## Why use Kafka?

Playback generates billions of events that feed analytics, recommendations, and monitoring systems. Kafka efficiently
handles high-throughput event streaming.

______________________________________________________________________

## Why store watch history separately?

Watch history grows continuously and is accessed differently from video metadata. Separating it improves scalability and
enables independent sharding.

______________________________________________________________________

## Why not store videos in MySQL?

Relational databases are not designed to efficiently store and stream very large binary objects. Object storage provides
better scalability, durability, and lower cost.

______________________________________________________________________

# Common Mistakes

## Streaming Directly From Object Storage

Use

a CDN

for

global delivery.

______________________________________________________________________

## Storing Videos In Database

Store

only metadata

inside

the database.

______________________________________________________________________

## Ignoring Adaptive Streaming

Users

have

different

network speeds.

______________________________________________________________________

## Synchronous Recommendations

Recommendation generation

should be

asynchronous.

______________________________________________________________________

## Ignoring Monitoring

Playback quality

must be

continuously monitored.

______________________________________________________________________

# Best Practices

✅ Store videos in Object Storage.

✅ Deliver content through a CDN.

✅ Encode multiple video qualities.

✅ Use Kafka for playback events.

✅ Cache metadata with Redis.

✅ Shard watch history by user.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is a CDN essential for Netflix?

### Answer

A CDN caches video content at edge locations close to users, reducing latency, minimizing buffering, lowering bandwidth
costs, and decreasing load on the origin infrastructure.

______________________________________________________________________

## Question

How does adaptive bitrate streaming work?

### Answer

Each video is encoded into multiple quality levels. During playback, the client dynamically switches between these
versions based on current network conditions and device capabilities to provide smooth streaming.

______________________________________________________________________

## Question

What is the biggest challenge in designing Netflix?

### Answer

Delivering high-quality video to millions of concurrent users worldwide with minimal startup delay and buffering while
efficiently managing storage, encoding, recommendations, and global content distribution.

______________________________________________________________________

# Practice Exercise

Design Netflix

for

500 Million Users.

Explain

1. API design
1. Capacity estimation
1. Video upload
1. Encoding pipeline
1. CDN architecture
1. Adaptive streaming
1. Recommendation engine
1. Search
1. Replication
1. Sharding
1. Monitoring
1. Trade-offs

Present

your complete design

within

45–60 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

Netflix is one of the best case studies for learning large-scale content delivery systems.

A strong design should demonstrate

- Requirement gathering
- Capacity estimation
- Object storage
- Video encoding
- CDN architecture
- Adaptive streaming
- Search
- Recommendations
- Event-driven processing
- Replication
- Sharding
- High availability

Mastering Netflix prepares you for interviews involving large-scale media platforms, content delivery systems, and
globally distributed applications.

______________________________________________________________________

# Next

[System Design Case Study – Amazon](26-design-amazon.md)
