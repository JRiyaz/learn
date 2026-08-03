# System Design - Part 73

# Instagram System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Feed Generation
- Fan-out on Write vs Fan-out on Read
- Media Uploads
- Followers & Social Graph
- Likes & Comments
- News Feed Ranking
- Caching
- CDN
- Database Design
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Instagram.**

Instagram

is much more

than

photo sharing.

It combines:

- Social Network
- Object Storage
- CDN
- Recommendation Engine
- Search
- Notifications
- Messaging

At scale,

billions

of photos,

videos,

likes,

and comments

are processed

every day.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Register/Login
- Upload photos/videos
- Follow users
- Like posts
- Comment on posts
- View News Feed
- User Profiles
- Notifications

Optional

- Stories
- Reels
- Direct Messages
- Search

______________________________________________________________________

# Non-Functional Requirements

- Low latency
- High availability
- Massive scalability
- High read throughput
- Durable media storage

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Instagram has

2 Billion users.

Daily Active Users

```text id="ig7301"
500 Million
```

New Posts

```text id="ig7302"
100 Million/day
```

Feed Requests

```text id="ig7303"
Several Billion/day
```

Observation.

Reads

far exceed

writes.

______________________________________________________________________

# Step 3

# API Design

Create Post

```http id="ig7304"
POST /posts
```

______________________________________________________________________

Get Feed

```http id="ig7305"
GET /feed
```

______________________________________________________________________

Like Post

```http id="ig7306"
POST /posts/{id}/like
```

______________________________________________________________________

Follow User

```http id="ig7307"
POST /users/{id}/follow
```

______________________________________________________________________

Comment

```http id="ig7308"
POST /posts/{id}/comments
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="ig7309"
Client

↓

Load Balancer

↓

API Gateway

↓

Post Service

↓

Object Storage

↓

Database
```

Additional services

include:

- Feed Service
- Follow Service
- Notification Service
- Recommendation Service
- Search Service

______________________________________________________________________

# Upload Flow

Users

upload photos

or videos.

Workflow

```text id="ig7310"
Client

↓

Presigned URL

↓

Object Storage

↓

Store Metadata

↓

Return Success
```

Large media

should never

pass through

the application server.

______________________________________________________________________

# Database Design

Posts

```text id="ig7311"
post_id

user_id

media_url

caption

created_at
```

______________________________________________________________________

Followers

```text id="ig7312"
follower_id

following_id
```

______________________________________________________________________

Likes

```text id="ig7313"
user_id

post_id
```

______________________________________________________________________

Comments

```text id="ig7314"
comment_id

post_id

user_id

text
```

______________________________________________________________________

# Social Graph

Interview favorite.

Instagram

maintains

a

social graph.

Example

```text id="ig7315"
User A

↓

User B

↓

User C
```

The graph

defines

who follows whom.

______________________________________________________________________

# News Feed

The biggest

interview topic.

Question.

When

User A

opens

Instagram,

how do

we build

their feed?

______________________________________________________________________

# Option 1

# Fan-out on Write

Suppose

User A

posts

a photo.

Immediately

copy

the post

to

every follower's feed.

```text id="ig7316"
New Post

↓

Followers

↓

Feed Tables
```

Advantages

✅ Fast reads

Disadvantages

❌ Expensive writes

Especially

for celebrities.

______________________________________________________________________

# Celebrity Problem

Suppose

Cristiano Ronaldo

posts

one photo.

Hundreds

of millions

of followers

must receive

feed updates.

Writing

to every feed

immediately

becomes expensive.

______________________________________________________________________

# Option 2

# Fan-out on Read

Store

posts once.

When

users

open

their feed,

retrieve

recent posts

from

followed users.

```text id="ig7317"
Open Feed

↓

Query Posts

↓

Rank

↓

Return
```

Advantages

✅ Cheap writes

Disadvantages

❌ Slower reads

______________________________________________________________________

# Hybrid Approach

Interview favorite.

Most large systems

combine

both approaches.

Normal users

↓

Fan-out on Write

Celebrities

↓

Fan-out on Read

This balances

cost

and

performance.

______________________________________________________________________

# Feed Ranking

Instagram

doesn't simply

sort

by time.

Ranking considers:

- Likes
- Comments
- Shares
- Watch Time
- Relationship
- User Interests
- ML Predictions

The Feed Service

returns

ranked content.

______________________________________________________________________

# Recommendation Service

AI models

predict

what

users

are likely

to engage with.

Inputs include:

- Previous likes
- Watch history
- Followers
- Search history

Output

is

a relevance score.

______________________________________________________________________

# Likes

Should

likes

update

the database

synchronously?

No.

Instead

publish

an event.

```text id="ig7318"
Like

↓

Kafka

↓

Analytics

↓

Notification
```

The user

receives

an immediate response.

______________________________________________________________________

# Comments

Comments

are stored

in

the database.

Popular posts

may cache

recent comments

inside Redis.

______________________________________________________________________

# Notifications

When

someone

likes

a post,

publish

an event.

```text id="ig7319"
Like Event

↓

Notification Service

↓

Push Notification
```

Notifications

should be

asynchronous.

______________________________________________________________________

# Search

Search users

using

Elasticsearch

or

OpenSearch.

Search posts

using:

- Hashtags
- Captions
- Usernames

______________________________________________________________________

# CDN

Interview favorite.

Media files

are huge.

Store them

inside

Object Storage.

Serve them

through

a CDN.

```text id="ig7320"
Object Storage

↓

CDN

↓

Users
```

This reduces

latency

globally.

______________________________________________________________________

# Caching

Redis stores:

- User Profiles
- Popular Posts
- Session Data
- Feed Fragments
- Follow Counts

Avoid

caching

everything.

Cache

hot data.

______________________________________________________________________

# Scaling

Scale

all stateless services

horizontally.

```text id="ig7321"
Load Balancer

↓

API 1

API 2

API 3
```

Use

database replication

for reads.

Shard

very large tables.

______________________________________________________________________

# AI/ML Example

Instagram

uses ML

for:

- Feed ranking
- Reels recommendation
- Spam detection
- Fake account detection
- Image moderation
- Content recommendation

Vector Databases

may be used

for

semantic recommendations.

______________________________________________________________________

# Failure Scenario

Suppose

Redis

fails.

The application

queries

the database.

Latency

increases,

but

the system

continues working.

______________________________________________________________________

# Another Failure

Suppose

Object Storage

becomes unavailable.

Users

can still:

- Login
- Browse cached feeds
- View metadata

But

new media uploads

may fail.

______________________________________________________________________

# End-to-End Architecture

```text id="ig7322"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Post Service

↓

Feed Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Notification Service

↓

Object Storage

↓

CDN

↓

Recommendation Service

↓

Search Engine
```

______________________________________________________________________

# Trade-offs

Fan-out on Write

vs

Fan-out on Read

| Fan-out on Write | Fan-out on Read |
| ----------------------- | ---------------------- |
| Fast feed reads | Slow feed reads |
| Expensive writes | Cheap writes |
| Better for normal users | Better for celebrities |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| ----- | --------------- |
| Fast | Durable |
| Cache | Source of truth |

______________________________________________________________________

Object Storage

vs

Database

| Object Storage | Database |
| -------------- | ------------------ |
| Media files | Metadata |
| Cheap | Structured queries |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Instagram's News Feed?

Begin by storing user posts in a durable database while media files are uploaded directly to Object Storage using
presigned URLs. Maintain follower relationships in a social graph and use a Feed Service to generate personalized
timelines. Two common strategies exist: Fan-out on Write, where new posts are pushed to followers' feeds immediately,
and Fan-out on Read, where feeds are generated when users request them. Most production systems use a hybrid
approach—Fan-out on Write for normal users and Fan-out on Read for celebrities. Redis caches frequently accessed data,
Kafka handles asynchronous notifications and analytics, a CDN serves media globally, and machine learning models rank
posts based on relevance rather than simple chronological order.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Feed generation
- Fan-out on Write
- Fan-out on Read
- Hybrid Feed
- Social Graph
- CDN
- Object Storage
- Recommendation Service
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram

These designs demonstrate three different classes of distributed systems:

- URL Shortening
- Real-Time Messaging
- Social Media Feed Systems

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design **Twitter/X**, focusing on:

- Tweet publishing
- Timeline generation
- Retweets
- Trending hashtags
- Search
- Followers
- Fan-out strategies
- Celebrity scaling

______________________________________________________________________

# What's Next

[Twitter/X System Design](74-twitter-system-design.md)
