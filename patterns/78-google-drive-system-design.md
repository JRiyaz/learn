# System Design - Part 78

# Google Drive System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- File Upload
- Chunked Uploads
- File Synchronization
- Folder Hierarchy
- Sharing & Permissions
- File Versioning
- Conflict Resolution
- Metadata Management
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Google Drive.**

Unlike

Netflix

or

Spotify,

Google Drive

isn't about

streaming.

Instead,

it focuses on:

- File storage
- File synchronization
- Collaboration
- Sharing
- Version history

The biggest challenge

is ensuring

that

the same file

remains consistent

across

multiple devices.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Upload files
- Download files
- Create folders
- Move files
- Rename files
- Delete files
- Share files
- Version history
- Multi-device sync

Optional

- Google Docs
- Real-time collaboration
- Offline mode
- File comments

______________________________________________________________________

# Non-Functional Requirements

- High availability
- Massive scalability
- Strong durability
- Low-latency synchronization
- Secure storage

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Google Drive

has

2 Billion users.

Daily Active Users

```text id="gd7801"
600 Million
```

New Files Uploaded

```text id="gd7802"
500 Million/day
```

Average File Size

```text id="gd7803"
10 MB
```

Storage Growth

```text id="gd7804"
Several PB/day
```

Observation.

Storage

is

the biggest challenge.

______________________________________________________________________

# Step 3

# API Design

Upload File

```http id="gd7805"
POST /files
```

______________________________________________________________________

Download File

```http id="gd7806"
GET /files/{id}
```

______________________________________________________________________

Create Folder

```http id="gd7807"
POST /folders
```

______________________________________________________________________

Share File

```http id="gd7808"
POST /files/{id}/share
```

______________________________________________________________________

List Files

```http id="gd7809"
GET /folders/{id}/files
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="gd7810"
Client

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Metadata Service

↓

Object Storage
```

Supporting services:

- Authentication Service
- Sync Service
- Notification Service
- Search Service
- Sharing Service

______________________________________________________________________

# File Upload

Interview favorite.

Large files

should **not**

pass through

application servers.

Workflow

```text id="gd7811"
Client

↓

Request Upload URL

↓

Presigned URL

↓

Object Storage
```

After

upload completes,

metadata

is stored

in

the database.

______________________________________________________________________

# Chunked Upload

Interview favorite.

Suppose

the user uploads

a

20 GB file.

Uploading

as one request

is risky.

Instead,

split

the file

into chunks.

```text id="gd7812"
20 GB

↓

Chunk 1

↓

Chunk 2

↓

Chunk 3

↓

Chunk N
```

Benefits:

- Resume uploads
- Retry failed chunks
- Parallel uploads

______________________________________________________________________

# Chunk Upload Flow

```text id="gd7813"
Client

↓

Upload Chunk

↓

Object Storage

↓

Repeat

↓

Merge Chunks
```

If

Chunk 8

fails,

only

Chunk 8

is retried.

______________________________________________________________________

# Metadata

Interview favorite.

Store

metadata,

not

the file itself.

Example

```text id="gd7814"
file_id

owner_id

filename

folder_id

size

version

created_at
```

The actual file

lives

inside

Object Storage.

______________________________________________________________________

# Folder Hierarchy

Folders

form

a tree.

```text id="gd7815"
Root

↓

Documents

↓

Projects

↓

Design.pdf
```

Each file

references

its parent folder.

______________________________________________________________________

# Sharing

Users

can share

files

with

other users.

Permissions

include:

- Viewer
- Commenter
- Editor
- Owner

Schema

```text id="gd7816"
file_id

user_id

permission
```

______________________________________________________________________

# File Synchronization

Interview favorite.

Suppose

the user edits

a file

on

their laptop.

The phone

must receive

the update.

Workflow

```text id="gd7817"
File Updated

↓

Sync Service

↓

Other Devices
```

Synchronization

keeps

devices

consistent.

______________________________________________________________________

# Change Detection

Each file

has

a version number.

Example

```text id="gd7818"
Version

15
```

When

a file changes,

the version

increments.

Clients

compare versions

to determine

whether

an update

is needed.

______________________________________________________________________

# File Versioning

Google Drive

keeps

multiple versions.

```text id="gd7819"
Version 1

↓

Version 2

↓

Version 3
```

Users

can restore

older versions.

______________________________________________________________________

# Conflict Resolution

Interview favorite.

Suppose

the same file

is edited

on

two laptops

while offline.

When

both devices

sync,

a conflict occurs.

Possible strategies:

- Last Write Wins
- Manual Conflict Resolution
- Merge Changes

For

binary files,

manual resolution

is common.

For

documents,

merging

may be possible.

______________________________________________________________________

# Search

Metadata

is indexed

inside

Elasticsearch

or

OpenSearch.

Users

can search

by:

- Filename
- Owner
- Folder
- File Type

Some systems

also support

content indexing

for PDFs

and documents.

______________________________________________________________________

# Notifications

When

a shared file

changes,

notify

collaborators.

Workflow

```text id="gd7820"
File Updated

↓

Kafka

↓

Notification Service

↓

Push / Email
```

______________________________________________________________________

# Download Flow

```text id="gd7821"
Client

↓

Metadata Service

↓

Authorization Check

↓

Signed Download URL

↓

Object Storage
```

Application servers

don't stream

large files.

______________________________________________________________________

# Caching

Redis stores:

- User sessions
- Folder metadata
- Recently accessed files
- Permission cache

Large files

remain

inside

Object Storage.

______________________________________________________________________

# Scaling

Scale independently:

- Metadata Service
- Sync Service
- Sharing Service
- Search Service

Object Storage

scales separately.

Metadata databases

may use:

- Replication
- Sharding

______________________________________________________________________

# AI/ML Example

Modern cloud storage

uses AI

for:

- Duplicate file detection
- Image classification
- OCR
- Smart search
- Document summarization

Embeddings

and

Vector Databases

can enable

semantic search.

______________________________________________________________________

# Failure Scenario

Suppose

Object Storage

becomes unavailable.

Users

can still:

- Browse folders
- View metadata
- Search files

New uploads

and downloads

will fail

until

storage recovers.

______________________________________________________________________

# Another Failure

Suppose

the Sync Service

fails.

Users

can continue

editing files

locally.

Changes

are synchronized

later

when

the service

recovers.

This is

eventual consistency.

______________________________________________________________________

# End-to-End Architecture

```text id="gd7822"
Users

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Authentication Service

↓

Metadata Service

↓

Sync Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Notification Service

↓

Search Service

↓

Object Storage
```

______________________________________________________________________

# Trade-offs

Object Storage

vs

Database

| Object Storage | Database |
| -------------- | --------------- |
| File content | Metadata |
| Cheap | Queryable |
| Highly durable | Structured data |

______________________________________________________________________

Chunk Upload

vs

Single Upload

| Chunked | Single |
| ---------------- | ---------------------- |
| Resume support | Restart from beginning |
| Parallel uploads | Simpler |
| More complexity | Less overhead |

______________________________________________________________________

File Versioning

vs

Overwrite

| Versioning | Overwrite |
| ----------------- | ------------ |
| Recover old files | Simpler |
| More storage | Less storage |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Google Drive?

Start by separating file metadata from file content. Store metadata such as filenames, owners, permissions, and folder
hierarchy in a relational database, while storing actual file contents in Object Storage. Upload large files using
presigned URLs and chunked uploads to support resumable transfers and parallel uploads. Use a Sync Service to propagate
file changes across devices, maintain version numbers for synchronization, and store historical versions for recovery.
Implement sharing through permission tables, use Elasticsearch for metadata search, Redis for caching frequently
accessed metadata, Kafka for asynchronous notifications, and scale metadata services independently from Object Storage.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Chunked uploads
- Object Storage
- Metadata management
- Folder hierarchy
- File synchronization
- Sharing & permissions
- File versioning
- Conflict resolution
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
- ✅ Google Drive

You now understand the architecture behind one of the world's largest cloud storage and synchronization platforms.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll move to the **Transportation** category with one of the most popular FAANG interview questions:

- Real-time location tracking
- Driver matching
- Geospatial indexing
- ETA calculation
- Surge pricing
- Trip lifecycle
- Live ride tracking

We'll design **Uber**.

______________________________________________________________________

# What's Next

[Uber System Design](79-uber-system-design.md)
