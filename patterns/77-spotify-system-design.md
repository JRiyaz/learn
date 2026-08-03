# System Design - Part 77

# Spotify System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Audio Upload Pipeline
- Audio Encoding
- Music Streaming
- Playlist Management
- Recommendation Engine
- Offline Downloads
- Search
- CDN
- Database Design
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Spotify.**

Spotify

looks similar

to

Netflix,

but

its workload

is different.

Instead of

large video files,

Spotify

streams

small audio files.

The biggest challenges

are:

- Low-latency music playback
- Personalized recommendations
- Playlist management
- Offline downloads
- Podcast streaming

Millions

of users

listen

to music

simultaneously.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Search songs
- Play songs
- Create playlists
- Like songs
- Follow artists
- Personalized recommendations
- Offline downloads
- Podcasts

Optional

- Lyrics
- Live audio
- Social sharing

______________________________________________________________________

# Non-Functional Requirements

- Low playback latency
- High availability
- High scalability
- Personalized experience
- Reliable streaming

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Spotify has

700 Million users.

Monthly Active Users

```text id="sp7701"
700 Million
```

Premium Users

```text id="sp7702"
300 Million
```

Concurrent Streams

```text id="sp7703"
20 Million
```

Observation.

Streaming

and

recommendation

are

the largest workloads.

______________________________________________________________________

# Step 3

# API Design

Search Song

```http id="sp7704"
GET /songs/search?q=believer
```

______________________________________________________________________

Play Song

```http id="sp7705"
POST /songs/{id}/play
```

______________________________________________________________________

Create Playlist

```http id="sp7706"
POST /playlists
```

______________________________________________________________________

Add Song

```http id="sp7707"
POST /playlists/{id}/songs
```

______________________________________________________________________

Like Song

```http id="sp7708"
POST /songs/{id}/like
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="sp7709"
Client

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Music Service

↓

Object Storage

↓

CDN
```

Supporting services:

- Playlist Service
- Recommendation Service
- Search Service
- User Service
- Analytics Service

______________________________________________________________________

# Audio Upload Pipeline

Artists

or record labels

upload

master audio files.

Workflow

```text id="sp7710"
Artist

↓

Upload

↓

Object Storage

↓

Encoding Pipeline
```

The upload

is handled

internally,

not

by listeners.

______________________________________________________________________

# Audio Encoding

Interview favorite.

Generate

multiple formats.

Example

```text id="sp7711"
FLAC

↓

320 kbps

↓

160 kbps

↓

96 kbps
```

Different codecs

may include:

- MP3
- AAC
- Ogg Vorbis
- Opus

Clients

select

the best version

based on

network speed

and

device support.

______________________________________________________________________

# Music Streaming

Songs

are divided

into

small segments.

```text id="sp7712"
Song

↓

Chunk 1

↓

Chunk 2

↓

Chunk 3
```

The player

downloads

segments

continuously,

enabling

quick startup

and

smooth playback.

______________________________________________________________________

# CDN

Interview favorite.

Audio files

are served

through

a CDN.

```text id="sp7713"
Object Storage

↓

CDN

↓

Listeners
```

Benefits:

- Low latency
- Reduced origin load
- Global delivery

______________________________________________________________________

# Playlist Service

Playlists

contain

references

to songs,

not

the audio itself.

Example Schema

```text id="sp7714"
playlist_id

user_id

name

created_at
```

Playlist Songs

```text id="sp7715"
playlist_id

song_id

position
```

______________________________________________________________________

# Search

Search

is powered

by

Elasticsearch

or

OpenSearch.

Users

can search

by:

- Song
- Album
- Artist
- Genre
- Playlist
- Podcast

______________________________________________________________________

# Recommendation Engine

Interview favorite.

Recommendations

use:

- Listening history
- Likes
- Skips
- Playlists
- Similar users
- Song embeddings
- ML models

Outputs include:

- Discover Weekly
- Daily Mix
- Release Radar

______________________________________________________________________

# Offline Downloads

Premium users

can download

songs

for offline playback.

Workflow

```text id="sp7716"
Song

↓

Encrypted Download

↓

Local Device
```

The app

periodically

verifies

the user's

subscription.

Downloaded files

remain encrypted

to prevent

unauthorized sharing.

______________________________________________________________________

# Continue Listening

Store

playback progress

for:

- Podcasts
- Audiobooks
- Long audio

Example

```text id="sp7717"
user_id

episode_id

position
```

Users

can resume

from

their last position.

______________________________________________________________________

# Analytics

Every playback

produces

events.

```text id="sp7718"
Play

↓

Pause

↓

Skip

↓

Complete
```

These events

are published

to Kafka.

Workers

process

them

asynchronously.

Analytics

powers:

- Royalty calculations
- Recommendations
- Trending charts

______________________________________________________________________

# Likes & Follows

When

a user

likes a song

or

follows an artist,

publish

an event.

```text id="sp7719"
Like Event

↓

Kafka

↓

Recommendation Service

↓

Analytics
```

The user

receives

an immediate response.

______________________________________________________________________

# Caching

Redis stores:

- User sessions
- Playlist metadata
- Popular songs
- Search suggestions
- Recommendation cache

Large audio files

are **not**

stored

inside Redis.

______________________________________________________________________

# Scaling

Scale independently:

- Music Service
- Playlist Service
- Search Service
- Recommendation Service
- Analytics Workers

Object Storage

and

CDN

scale independently.

______________________________________________________________________

# AI/ML Example

Spotify

uses ML

for:

- Song recommendations
- Playlist generation
- Podcast recommendations
- Personalized home page
- Similar artist suggestions

Modern systems

may use:

- Embedding Models
- Vector Databases
- LLMs

to improve

music discovery.

______________________________________________________________________

# Failure Scenario

Suppose

the Recommendation Service

fails.

Users

can still:

- Search songs
- Play music
- Access playlists

The application

falls back

to:

- Popular Songs
- Recently Played
- Editorial Playlists

______________________________________________________________________

# Another Failure

Suppose

the CDN

fails

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

```text id="sp7720"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Music Service

↓

Playlist Service

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

Search Service

↓

Object Storage

↓

CDN
```

______________________________________________________________________

# Trade-offs

CDN

vs

Origin

| CDN | Origin |
| --------------- | --------------- |
| Faster delivery | Higher latency |
| Edge caching | Source of truth |

______________________________________________________________________

Recommendation Cache

vs

Real-Time Computation

| Cache | Real-Time |
| ------------ | ---------------- |
| Faster | More accurate |
| Less compute | Higher CPU usage |

______________________________________________________________________

Playlist Storage

vs

Embedding Songs

| Store References | Embed Songs |
| ---------------- | --------------------- |
| Smaller storage | Massive duplication |
| Easier updates | Difficult maintenance |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Spotify?

Start by storing master audio files in Object Storage and processing them through an encoding pipeline to generate
multiple bitrates and codecs. Stream audio through a CDN using segmented streaming to reduce startup latency and improve
playback reliability. Store metadata, playlists, and user information in a relational database while using Redis to
cache popular metadata and recommendations. Use Elasticsearch for search and Kafka for asynchronous processing of
playback events, likes, follows, and analytics. Recommendation services powered by machine learning generate
personalized playlists such as Discover Weekly. Premium users can download encrypted songs for offline playback, with
periodic license verification to enforce subscription access.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Audio encoding
- Music streaming
- Playlist management
- Recommendation engine
- Offline downloads
- Search
- CDN
- Analytics
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
- ✅ Spotify

You now understand the architecture behind the world's largest music streaming platform.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll move to the **Cloud Storage** category with one of the most frequently asked interview problems:

- File uploads
- Folder hierarchy
- File sharing
- Permissions
- Chunked uploads
- Synchronization
- Conflict resolution
- Versioning

We'll design **Google Drive**.

______________________________________________________________________

# What's Next

[Google Drive System Design](78-google-drive-system-design.md)
