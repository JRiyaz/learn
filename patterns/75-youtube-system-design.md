# System Design - Part 75

# YouTube System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Video Upload
- Video Processing Pipeline
- Transcoding
- Adaptive Streaming
- CDN
- Search
- Recommendation System
- View Counting
- Database Design
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design YouTube.**

Unlike

Twitter

or

Instagram,

YouTube

is

a

video streaming platform.

Its biggest challenges

are:

- Huge file uploads
- Video processing
- Global streaming
- Recommendations
- Massive storage

Every minute,

thousands

of hours

of video

are uploaded.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Upload videos
- Watch videos
- Search videos
- Like videos
- Subscribe to channels
- Comment on videos
- Recommendations
- Watch history

Optional

- Live Streaming
- Shorts
- Playlists
- Captions

______________________________________________________________________

# Non-Functional Requirements

- Very high availability
- Massive scalability
- Low playback latency
- Durable storage
- Global delivery

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

YouTube has

2 Billion users.

Daily Active Users

```text id="yt7501"
700 Million
```

Video Uploads

```text id="yt7502"
2 Million/day
```

Video Streams

```text id="yt7503"
Several Billion/day
```

Storage

grows

by

petabytes

every month.

Reads

are

far higher

than writes.

______________________________________________________________________

# Step 3

# API Design

Upload Video

```http id="yt7504"
POST /videos
```

______________________________________________________________________

Watch Video

```http id="yt7505"
GET /videos/{id}
```

______________________________________________________________________

Search

```http id="yt7506"
GET /search?q=python
```

______________________________________________________________________

Like

```http id="yt7507"
POST /videos/{id}/like
```

______________________________________________________________________

Subscribe

```http id="yt7508"
POST /channels/{id}/subscribe
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="yt7509"
Client

↓

Load Balancer

↓

API Gateway

↓

Video Service

↓

Object Storage
```

Additional services

include:

- Upload Service
- Processing Service
- Recommendation Service
- Search Service
- CDN
- Analytics Service

______________________________________________________________________

# Video Upload Flow

Interview favorite.

Users

upload

large videos.

The application

should **not**

proxy

gigabyte-sized files.

Workflow

```text id="yt7510"
Client

↓

Presigned URL

↓

Object Storage
```

After upload,

the client

notifies

the Video Service.

______________________________________________________________________

# Video Metadata

Database

stores

only metadata.

Example

```text id="yt7511"
video_id

title

description

channel_id

duration

status

created_at
```

The video file

remains

inside

Object Storage.

______________________________________________________________________

# Video Processing Pipeline

After upload,

processing

begins.

```text id="yt7512"
Upload Complete

↓

Kafka

↓

Video Worker

↓

Transcoding
```

The user

doesn't wait

for processing.

______________________________________________________________________

# Why Transcoding?

Interview favorite.

Different devices

support

different resolutions.

Original upload

may be

4K.

Generate

multiple versions.

Example

```text id="yt7513"
4K

↓

1080p

↓

720p

↓

480p

↓

360p
```

Users

receive

the version

best suited

to

their device

and

network speed.

______________________________________________________________________

# Adaptive Streaming

Modern platforms

don't stream

an entire video

as one file.

Instead,

videos

are split

into

small chunks.

```text id="yt7514"
Video

↓

Chunk 1

Chunk 2

Chunk 3
```

The player

downloads

chunks

one at a time.

______________________________________________________________________

# Adaptive Bitrate Streaming

Suppose

the user's

internet speed

drops.

Instead of

stopping playback,

the player

switches

to

a lower-quality stream.

```text id="yt7515"
1080p

↓

720p

↓

480p
```

Playback

continues smoothly.

______________________________________________________________________

# CDN

Interview favorite.

Videos

are extremely large.

Serving them

from

one region

would create

high latency.

Workflow

```text id="yt7516"
Object Storage

↓

CDN

↓

Users
```

Edge servers

deliver videos

close

to

the user.

______________________________________________________________________

# Search

Video metadata

is indexed

inside

Elasticsearch

or

OpenSearch.

Users

can search

by:

- Title
- Description
- Tags
- Channel

______________________________________________________________________

# Recommendation System

Interview favorite.

Recommendations

consider:

- Watch History
- Likes
- Search History
- Subscriptions
- Similar Users
- Video Embeddings
- ML Models

The Recommendation Service

returns

ranked videos.

______________________________________________________________________

# View Counting

Question.

Should

every video view

immediately

update

the database?

No.

Workflow

```text id="yt7517"
View Event

↓

Kafka

↓

Analytics Worker

↓

Database
```

Views

are aggregated

asynchronously.

______________________________________________________________________

# Comments

Comments

are stored

inside

the database.

Popular comments

may be cached

inside Redis.

______________________________________________________________________

# Notifications

Subscribers

receive

notifications

when

new videos

are published.

Workflow

```text id="yt7518"
Upload Complete

↓

Kafka

↓

Notification Service

↓

Push Notification
```

______________________________________________________________________

# Watch History

Watch history

helps:

- Resume playback
- Recommendations
- Analytics

Schema

```text id="yt7519"
user_id

video_id

watched_at

position
```

______________________________________________________________________

# Caching

Redis stores:

- Popular videos
- Channel information
- Video metadata
- Trending videos
- Session data

Large video files

are **not**

stored

inside Redis.

______________________________________________________________________

# Scaling

Stateless services

scale horizontally.

```text id="yt7520"
Load Balancer

↓

Video Service 1

Video Service 2

Video Service 3
```

Object Storage

scales independently.

Processing workers

can also

scale horizontally.

______________________________________________________________________

# AI/ML Example

Machine Learning

powers:

- Recommendations
- Video classification
- Thumbnail selection
- Spam detection
- Copyright detection
- Caption generation

Modern systems

may combine:

- Search Engines
- Vector Databases
- LLMs

for

better recommendations.

______________________________________________________________________

# Failure Scenario

Suppose

the Processing Service

fails.

The uploaded video

remains

inside

Object Storage.

Kafka

retains

the processing event.

Workers

resume processing

after recovery.

No upload

is lost.

______________________________________________________________________

# Another Failure

Suppose

the CDN

has an outage

in one region.

Traffic

is redirected

to

another edge location.

Playback

continues,

although

latency

may increase.

______________________________________________________________________

# End-to-End Architecture

```text id="yt7521"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Video Service

↓

Object Storage

↓

Kafka

↓

Video Processing Workers

↓

CDN

↓

Recommendation Service

↓

Search Engine

↓

Redis

↓

PostgreSQL
```

______________________________________________________________________

# Trade-offs

Object Storage

vs

Database

| Object Storage | Database |
| -------------- | ------------------ |
| Video files | Metadata |
| Cheap | Structured queries |

______________________________________________________________________

CDN

vs

Origin Server

| CDN | Origin |
| ------------ | --------------- |
| Low latency | High latency |
| Edge caching | Source of truth |

______________________________________________________________________

Synchronous

vs

Asynchronous Processing

| Synchronous | Asynchronous |
| ------------ | ------------------ |
| Slow uploads | Fast uploads |
| User waits | Background workers |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design YouTube?

Begin by storing uploaded videos directly in Object Storage using presigned URLs so the application servers do not
handle large files. Store only metadata in a relational database. After upload, publish an event to Kafka, where
background workers transcode the video into multiple resolutions for adaptive streaming. Serve processed videos through
a CDN to reduce global latency. Use Elasticsearch or OpenSearch for video search, Redis for caching metadata and
trending content, and machine learning models for personalized recommendations. Process view counts asynchronously and
scale stateless services, processing workers, and storage independently to support billions of video streams.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Video upload
- Object Storage
- Transcoding
- Adaptive streaming
- CDN
- Search
- Recommendations
- View counting
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

You now understand systems focused on:

- URL Redirection
- Real-Time Messaging
- Social Media
- Timeline Generation
- Global Video Streaming

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design **Netflix**, focusing on:

- Global video streaming
- Content delivery
- Recommendation engine
- Playback architecture
- Multi-region deployment
- Personalized home page
- Resilience at global scale

______________________________________________________________________

# What's Next

[Netflix System Design](76-netflix-system-design.md)
