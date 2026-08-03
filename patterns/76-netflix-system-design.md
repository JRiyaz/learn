# System Design - Part 76

# Netflix System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Video Upload Pipeline
- Video Encoding
- Adaptive Streaming
- CDN
- Recommendation System
- Continue Watching
- Playback Service
- Multi-Region Deployment
- Database Design
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Netflix.**

Unlike

YouTube,

Netflix

doesn't allow

users

to upload videos.

Instead,

Netflix

owns

the content.

The biggest challenges

are:

- Global video streaming
- Personalized recommendations
- Low-latency playback
- Multi-region availability
- Massive CDN usage

Millions

of users

watch

videos

simultaneously.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Browse movies
- Watch videos
- Search content
- Personalized recommendations
- Continue Watching
- Watch history
- Multiple profiles
- Resume playback

Optional

- Downloads
- Live Events
- Watch Party

______________________________________________________________________

# Non-Functional Requirements

- Very low playback latency
- High availability
- Global scalability
- Reliable streaming
- High video quality

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Netflix has

300 Million users.

Concurrent viewers

```text id="nf7601"
30 Million
```

Daily Streams

```text id="nf7602"
500 Million
```

Peak Bandwidth

```text id="nf7603"
Hundreds of Tbps
```

Observation.

Bandwidth

is

the biggest challenge.

______________________________________________________________________

# Step 3

# API Design

Browse

```http id="nf7604"
GET /movies
```

______________________________________________________________________

Movie Details

```http id="nf7605"
GET /movies/{id}
```

______________________________________________________________________

Play Movie

```http id="nf7606"
POST /play/{id}
```

______________________________________________________________________

Continue Watching

```http id="nf7607"
GET /continue-watching
```

______________________________________________________________________

Search

```http id="nf7608"
GET /search?q=inception
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="nf7609"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Playback Service

↓

Recommendation Service

↓

Object Storage

↓

CDN
```

Supporting services:

- Search Service
- Metadata Service
- User Profile Service
- Analytics Service

______________________________________________________________________

# Content Ingestion

Netflix

licenses

or

produces

movies.

Workflow

```text id="nf7610"
Studio

↓

Upload

↓

Object Storage

↓

Encoding Pipeline
```

Unlike YouTube,

uploads

are performed

internally.

______________________________________________________________________

# Video Encoding

Interview favorite.

A movie

is encoded

into

multiple formats.

Example

```text id="nf7611"
4K HDR

↓

1080p

↓

720p

↓

480p
```

Different codecs

may also

be generated.

Examples:

- H.264
- H.265 (HEVC)
- AV1

The client

chooses

the best version

it supports.

______________________________________________________________________

# Adaptive Streaming

Movies

are split

into

small segments.

```text id="nf7612"
Movie

↓

Chunk 1

Chunk 2

Chunk 3
```

The player

downloads

chunks

instead of

the entire movie.

______________________________________________________________________

# Adaptive Bitrate

Suppose

network speed

drops.

Playback

switches

automatically.

```text id="nf7613"
4K

↓

1080p

↓

720p
```

The user

experiences

minimal buffering.

______________________________________________________________________

# CDN

Interview favorite.

Streaming

every movie

from

one region

would create

huge latency.

Workflow

```text id="nf7614"
Object Storage

↓

CDN Edge

↓

Viewer
```

The nearest

edge server

streams

the content.

______________________________________________________________________

# Open Connect

Netflix

built

its own CDN

called

**Open Connect**.

Instead of

relying entirely

on third-party CDNs,

Netflix

deploys

cache servers

inside

Internet Service Providers (ISPs).

Benefits:

- Lower latency
- Reduced internet backbone traffic
- Better streaming quality

______________________________________________________________________

# Playback Flow

```text id="nf7615"
User

↓

Playback API

↓

Playback Token

↓

CDN

↓

Video Segments
```

The API

authorizes playback.

The video

is streamed

directly

from

the CDN.

______________________________________________________________________

# Continue Watching

Interview favorite.

Store

playback progress.

Example

```text id="nf7616"
user_id

movie_id

position

timestamp
```

If

the user

stops

at

45:20,

playback

resumes

from there.

______________________________________________________________________

# Recommendation System

One of

Netflix's

most important services.

Inputs include:

- Watch history
- Ratings
- Search history
- Watch duration
- Similar users
- Device type
- Time of day

Machine Learning

produces

personalized rankings.

______________________________________________________________________

# Search

Metadata

is indexed

using

Elasticsearch

or

OpenSearch.

Users

search

by:

- Title
- Actor
- Genre
- Director

______________________________________________________________________

# User Profiles

Each account

can contain

multiple profiles.

Example

```text id="nf7617"
Account

↓

Adult

↓

Kids
```

Recommendations

remain

independent

for each profile.

______________________________________________________________________

# Watch History

Schema

```text id="nf7618"
user_id

movie_id

watched_at

completion

device
```

History

is used

for:

- Recommendations
- Continue Watching
- Analytics

______________________________________________________________________

# Analytics

Playback events

should not

update

the database

synchronously.

Workflow

```text id="nf7619"
Playback Event

↓

Kafka

↓

Analytics Workers
```

Metrics include:

- Watch time
- Buffering
- Completion rate
- Device usage

______________________________________________________________________

# Caching

Redis stores:

- User sessions
- Movie metadata
- Continue Watching
- Popular content
- Recommendation cache

Large videos

are

never

stored

inside Redis.

______________________________________________________________________

# Multi-Region Deployment

Interview favorite.

Netflix

operates

across

multiple regions.

```text id="nf7620"
US-East

↔

Europe

↔

Asia
```

If

one region

fails,

traffic

is redirected

to

another region.

______________________________________________________________________

# Scaling

Scale independently:

- Playback Service
- Recommendation Service
- Search Service
- Analytics Workers

Object Storage

and

CDN

scale separately.

______________________________________________________________________

# AI/ML Example

Machine Learning

powers:

- Home page ranking
- Movie recommendations
- Thumbnail personalization
- Search ranking
- Content categorization

Modern systems

may use:

- Vector Databases
- Embedding Models
- LLMs

to improve

content discovery.

______________________________________________________________________

# Failure Scenario

Suppose

the Recommendation Service

fails.

Users

can still

watch movies.

The home page

falls back

to:

- Popular Movies
- Trending Content
- Recently Watched

The core service

remains available.

______________________________________________________________________

# Another Failure

Suppose

a CDN edge

goes offline.

DNS

or

traffic routing

redirects

users

to

the nearest

healthy edge.

Playback

continues

with

slightly higher latency.

______________________________________________________________________

# End-to-End Architecture

```text id="nf7621"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Playback Service

↓

Recommendation Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Analytics Workers

↓

Object Storage

↓

Open Connect CDN

↓

Search Service
```

______________________________________________________________________

# Trade-offs

CDN

vs

Origin Server

| CDN | Origin |
| ------------------ | ------------------- |
| Low latency | Higher latency |
| Edge caching | Source of truth |
| Better scalability | Centralized storage |

______________________________________________________________________

Synchronous

vs

Asynchronous Analytics

| Synchronous | Asynchronous |
| ----------------- | -------------------- |
| Higher latency | Faster playback |
| Immediate updates | Eventual consistency |

______________________________________________________________________

Recommendation Cache

vs

Real-Time Computation

| Cache | Real-Time |
| --------- | ------------------- |
| Faster | Fresher results |
| Lower CPU | Higher compute cost |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Netflix?

Start by separating the control plane from the data plane. Use APIs for authentication, playback authorization,
recommendations, and metadata, while streaming video directly from a CDN instead of application servers. Store original
videos in Object Storage and process them through an encoding pipeline to generate multiple resolutions and codecs for
adaptive streaming. Use a CDN such as Netflix's Open Connect to deliver video segments from edge locations close to
users. Store playback progress for the Continue Watching feature, process playback analytics asynchronously using Kafka,
use Elasticsearch for search, Redis for caching metadata and user state, and machine learning models for personalized
recommendations. Deploy services across multiple regions to ensure high availability and resilience.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Video encoding
- Adaptive streaming
- CDN
- Open Connect
- Playback architecture
- Continue Watching
- Recommendation System
- Multi-region deployment
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

You now understand the architecture behind the world's largest video streaming platform.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design **Spotify**, covering:

- Music streaming
- Playlist generation
- Audio encoding
- Recommendation engine
- Offline downloads
- Personalized playlists
- Podcast delivery
- Search

______________________________________________________________________

# What's Next

[Spotify System Design](77-spotify-system-design.md)
