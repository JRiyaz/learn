# System Design - Part 74

# Twitter/X System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Tweet Publishing
- Timeline Generation
- Fan-out on Write vs Fan-out on Read
- Retweets
- Likes
- Trending Hashtags
- Search
- Caching
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Twitter (X).**

Twitter

looks similar

to Instagram,

but

its workload

is different.

Instead of

large media files,

Twitter

primarily handles

small text messages

called Tweets.

However,

it processes

millions

of tweets,

likes,

retweets,

and searches

every minute.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Publish Tweets
- Follow users
- View Timeline
- Like Tweets
- Retweet
- Reply
- Search Tweets
- Trending Hashtags
- Notifications

Optional

- Spaces
- Bookmarks
- Communities
- Polls

______________________________________________________________________

# Non-Functional Requirements

- Very low latency
- High availability
- High read throughput
- Horizontal scalability
- Timeline consistency

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Twitter has

500 Million users.

Daily Active Users

```text id="tw7401"
250 Million
```

Tweets

per day

```text id="tw7402"
600 Million
```

Timeline Reads

```text id="tw7403"
Several Billion/day
```

Observation.

Reads

are

far higher

than writes.

______________________________________________________________________

# Step 3

# API Design

Create Tweet

```http id="tw7404"
POST /tweets
```

______________________________________________________________________

Timeline

```http id="tw7405"
GET /timeline
```

______________________________________________________________________

Like Tweet

```http id="tw7406"
POST /tweets/{id}/like
```

______________________________________________________________________

Retweet

```http id="tw7407"
POST /tweets/{id}/retweet
```

______________________________________________________________________

Search

```http id="tw7408"
GET /search?q=system+design
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="tw7409"
Client

↓

Load Balancer

↓

API Gateway

↓

Tweet Service

↓

Timeline Service

↓

Redis

↓

Database
```

Additional services:

- Search Service
- Notification Service
- Trend Service
- Recommendation Service

______________________________________________________________________

# Tweet Publishing

Workflow

```text id="tw7410"
User

↓

Tweet Service

↓

Database

↓

Kafka

↓

Timeline Service
```

The Tweet

is stored first.

Then

an event

is published.

______________________________________________________________________

# Database Schema

Tweets

```text id="tw7411"
tweet_id

user_id

text

created_at

reply_to

media_url
```

______________________________________________________________________

Followers

```text id="tw7412"
follower_id

following_id
```

______________________________________________________________________

Likes

```text id="tw7413"
tweet_id

user_id
```

______________________________________________________________________

Retweets

```text id="tw7414"
tweet_id

user_id
```

______________________________________________________________________

# Timeline Generation

Interview favorite.

Question.

When

a user

opens

Twitter,

how is

the timeline

generated?

Two approaches

exist.

______________________________________________________________________

# Fan-out on Write

When

a tweet

is created,

copy it

into

every follower's

timeline.

```text id="tw7415"
Tweet

↓

Followers

↓

Timeline Cache
```

Advantages

✅ Fast timeline reads

Disadvantages

❌ Expensive

for celebrities.

______________________________________________________________________

# Celebrity Problem

Suppose

Elon Musk

publishes

a tweet.

Millions

of followers

must receive

timeline updates.

Updating

every timeline

immediately

is expensive.

______________________________________________________________________

# Fan-out on Read

Instead

store

tweets once.

Generate

the timeline

when

the user

opens

the app.

```text id="tw7416"
Open Timeline

↓

Fetch Tweets

↓

Rank

↓

Return
```

Advantages

✅ Cheap writes

Disadvantages

❌ More work

during reads.

______________________________________________________________________

# Hybrid Strategy

Interview favorite.

Normal users

↓

Fan-out on Write

Celebrities

↓

Fan-out on Read

This is

the strategy

used

by many

large-scale

social platforms.

______________________________________________________________________

# Timeline Ranking

Twitter

doesn't simply

sort

by time.

Ranking considers:

- Follow relationships
- Likes
- Retweets
- Replies
- Recency
- Engagement
- Machine Learning score

______________________________________________________________________

# Retweets

Retweets

should not

block

the user.

Workflow

```text id="tw7417"
Retweet

↓

Kafka

↓

Timeline Update

↓

Notifications
```

Everything

happens

asynchronously.

______________________________________________________________________

# Likes

Likes

are handled

similarly.

```text id="tw7418"
Like

↓

Kafka

↓

Analytics

↓

Notification
```

The API

returns quickly.

______________________________________________________________________

# Trending Hashtags

Interview favorite.

Question.

How does

Twitter know

what is trending?

Continuously

count

hashtags

from

incoming tweets.

Example

```text id="tw7419"
#AI
```

↓

Increase Counter

↓

Ranking Engine

Trending

is usually

computed

over

a sliding

time window,

not

all-time counts.

______________________________________________________________________

# Search

Tweets

are indexed

inside

Elasticsearch

or

OpenSearch.

This enables:

- Keyword search
- Hashtag search
- User search
- Filtering

______________________________________________________________________

# Caching

Redis stores:

- Timeline fragments
- User profiles
- Follow counts
- Popular tweets
- Trending hashtags

Hot data

is served

from cache.

______________________________________________________________________

# Notifications

Examples:

- New follower
- Like
- Reply
- Mention
- Retweet

Workflow

```text id="tw7420"
Event

↓

Kafka

↓

Notification Service

↓

Push Notification
```

______________________________________________________________________

# Media

Although

Twitter

is

text-first,

images

and videos

should be stored

in

Object Storage.

Serve them

through

a CDN.

______________________________________________________________________

# Scaling

All stateless services

scale

horizontally.

```text id="tw7421"
Load Balancer

↓

Tweet Service 1

Tweet Service 2

Tweet Service 3
```

The Tweet Database

can use:

- Replication
- Sharding

as data grows.

______________________________________________________________________

# AI/ML Example

Twitter

uses ML

for:

- Timeline ranking
- Content recommendation
- Spam detection
- Bot detection
- Abuse detection
- Advertisement ranking

Modern recommendation systems

may combine

Search Engines

and

Vector Databases.

______________________________________________________________________

# Failure Scenario

Suppose

Redis

fails.

Timeline generation

falls back

to

the database.

Latency

increases,

but

users

can still

view tweets.

______________________________________________________________________

# Another Failure

Suppose

Kafka

is unavailable.

Tweets

are still

stored

in

the database,

but

timeline updates,

notifications,

and analytics

may be delayed.

Workers

can replay

events

once Kafka

recovers.

______________________________________________________________________

# End-to-End Architecture

```text id="tw7422"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Tweet Service

↓

Timeline Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Notification Service

↓

Search Engine

↓

Trend Service

↓

Object Storage

↓

CDN

↓

Recommendation Service
```

______________________________________________________________________

# Trade-offs

Fan-out on Write

vs

Fan-out on Read

| Fan-out on Write | Fan-out on Read |
| ------------------------- | ----------------------- |
| Fast timeline reads | Faster tweet publishing |
| Expensive for celebrities | Higher read latency |
| More storage | Less storage |

______________________________________________________________________

Search Engine

vs

Database

| Search Engine | Database |
| ---------------- | --------------- |
| Full-text search | Source of truth |
| Ranking | Transactions |
| Filtering | Persistence |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| -------------- | ------------- |
| Timeline cache | Tweet storage |
| In-memory | Persistent |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Twitter's timeline?

Start by storing tweets in a durable database and publishing tweet events to a message broker such as Kafka. Use a
Timeline Service to generate user feeds. Fan-out on Write pushes tweets into followers' timeline caches immediately,
providing fast reads but expensive writes. Fan-out on Read generates timelines dynamically when users request them,
reducing write amplification but increasing read latency. Most production systems use a hybrid approach, applying
Fan-out on Write for normal users and Fan-out on Read for celebrities. Redis caches timeline fragments, Elasticsearch
powers tweet search, Kafka supports asynchronous processing, and machine learning models rank tweets based on
engagement, relevance, and user interests.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Timeline generation
- Fan-out strategies
- Trending hashtags
- Search
- Timeline ranking
- Notifications
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram
- ✅ Twitter/X

You now understand four major categories of large-scale systems:

- URL Shortening
- Real-Time Messaging
- Media-Centric Social Networks
- Timeline-Based Social Networks

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design **YouTube**, covering:

- Video uploads
- Video transcoding
- Object Storage
- CDN
- Recommendations
- Streaming
- Watch history
- Search
- View counting

______________________________________________________________________

# What's Next

[YouTube System Design](75-youtube-system-design.md)
