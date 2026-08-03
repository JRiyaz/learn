# System Design - Part 59

# Object Storage

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Object Storage is
- Why Object Storage exists
- Objects, Buckets, and Metadata
- Object Storage Architecture
- Object Storage vs File System
- Object Storage vs Block Storage
- Object Storage vs Database
- Amazon S3, MinIO, GCS, Azure Blob
- Versioning
- Lifecycle Policies
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

stores

the following files:

- Book Covers
- Member Photos
- PDF Books
- Audio Books
- Reports

Initially,

the application

stores

everything

inside

the application server.

```text id="obj5901"
Application

↓

/uploads
```

Everything works.

Until...

______________________________________________________________________

# The Problem

Suppose

your application

runs

on

five servers.

```text id="obj5902"
Server 1

Server 2

Server 3

Server 4

Server 5
```

A user

uploads

a PDF

to

Server 2.

Later,

another request

goes

to

Server 5.

Question.

Where

is the file?

Server 5

doesn't have it.

______________________________________________________________________

# Another Problem

Suppose

the server

crashes.

```text id="obj5903"
Application Server

❌
```

All uploaded files

stored

locally

are lost.

Clearly,

local storage

doesn't scale.

______________________________________________________________________

# The Idea

Store files

outside

the application

in

a dedicated

storage service.

Applications

store only

the file reference.

______________________________________________________________________

# What is Object Storage?

**Object Storage**

is a storage system

that stores

data

as

independent objects,

where

each object

contains:

- Data
- Metadata
- Unique Identifier

Unlike

traditional file systems,

objects

are not organized

into directories

on disk.

______________________________________________________________________

# What is an Object?

An object

contains

three parts.

```text id="obj5904"
Data

+

Metadata

+

Object ID
```

Example

```text id="obj5905"
book-cover.png

↓

Image Data

↓

Content-Type

↓

Created Time

↓

Object Key
```

______________________________________________________________________

# What is a Bucket?

A **Bucket**

is

a logical container

that stores objects.

Example

```text id="obj5906"
library-books
```

```text id="obj5907"
member-images
```

```text id="obj5908"
reports
```

Buckets

are similar

to

top-level folders,

but

internally,

object storage

doesn't use

traditional directories.

______________________________________________________________________

# Architecture

```text id="obj5909"
Application

↓

Object Storage

↓

Bucket

↓

Objects
```

The application

uploads

and downloads

objects

using APIs.

______________________________________________________________________

# Object Key

Every object

has

a unique key.

Example

```text id="obj5910"
books/123/cover.png
```

This

looks

like

a directory,

but

it's actually

just

a unique string.

Object Storage

doesn't care

about

folder structures.

______________________________________________________________________

# Upload Flow

```text id="obj5911"
Client

↓

FastAPI

↓

Object Storage

↓

Return Object URL
```

Instead of

storing

the file,

the database

stores

only

the object key.

______________________________________________________________________

# Download Flow

```text id="obj5912"
Client

↓

Application

↓

Object URL

↓

Object Storage
```

Large files

never pass

through

the application server.

______________________________________________________________________

# Metadata

Metadata

describes

the object.

Examples:

- File Size
- Content-Type
- Upload Time
- Owner
- Tags

Applications

can retrieve

metadata

without

downloading

the entire file.

______________________________________________________________________

# Object Storage vs File System

Interview favorite.

| File System | Object Storage |
| ------------------- | ------------------- |
| Directories | Buckets & Objects |
| Hierarchical | Flat namespace |
| Local server | Distributed storage |
| Limited scalability | Massive scalability |

______________________________________________________________________

# Object Storage vs Block Storage

Another

interview question.

| Block Storage | Object Storage |
| ----------------- | ----------------------- |
| Virtual disks | Individual objects |
| Operating systems | Applications |
| Low latency | High scalability |
| Random updates | Whole object operations |

Example

Operating System

uses

Block Storage.

Application uploads

use

Object Storage.

______________________________________________________________________

# Object Storage vs Database

| Database | Object Storage |
| ------------------ | -------------- |
| Structured records | Files |
| SQL queries | Object APIs |
| Small records | Large files |

Store

metadata

inside

the database.

Store

files

inside

Object Storage.

______________________________________________________________________

# Versioning

Suppose

someone

uploads

a new version

of

a document.

Instead of

overwriting,

Object Storage

can keep

both versions.

```text id="obj5913"
Version 1

↓

Version 2

↓

Version 3
```

Useful

for

accidental deletions

and

recovery.

______________________________________________________________________

# Lifecycle Policies

Suppose

old files

are rarely used.

Automatically

move them

to

cheaper storage.

Example

```text id="obj5914"
30 Days

↓

Archive
```

Later

```text id="obj5915"
365 Days

↓

Delete
```

This reduces

storage costs.

______________________________________________________________________

# Presigned URLs

Interview favorite.

Suppose

a user

uploads

a 5 GB video.

Should

the video

pass

through

your API?

No.

Instead,

generate

a **Presigned URL**.

```text id="obj5916"
Client

↓

Presigned URL

↓

Object Storage
```

The client

uploads

directly

to

Object Storage.

Your server

never handles

the file.

______________________________________________________________________

# FastAPI Example

Instead of

saving

uploads

to

```text id="obj5917"
/uploads
```

Upload

to

Object Storage.

Store

only

the object key

inside

PostgreSQL.

______________________________________________________________________

# AI/ML Example

Suppose

users upload

training datasets.

Object Storage

stores:

- Images
- Videos
- PDFs
- Audio
- Models
- Embeddings Backup

AI workers

download

only

the files

they need.

______________________________________________________________________

# Kubernetes Example

Pods

are ephemeral.

If

a Pod

stores

files locally,

those files

disappear

when

the Pod

is recreated.

Instead,

Pods

upload files

to

Object Storage,

making

the data

available

to all Pods.

______________________________________________________________________

# Amazon S3

Amazon S3

is

the most widely used

Object Storage service.

Features include:

- Buckets
- Versioning
- Lifecycle Policies
- Replication
- Encryption
- Presigned URLs

Many other

Object Storage systems

implement

the S3 API.

______________________________________________________________________

# Other Object Storage Systems

Examples:

- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- MinIO
- DigitalOcean Spaces

Many applications

can switch

between them

with

minimal code changes.

______________________________________________________________________

# Replication

Object Storage

can replicate

objects

across

multiple regions.

Benefits:

- Disaster Recovery
- High Availability
- Lower latency

______________________________________________________________________

# Security

Object Storage

supports:

- IAM Policies
- Bucket Policies
- Encryption at Rest
- TLS
- Presigned URLs
- Object-Level Permissions

Never expose

private buckets

publicly

without

proper controls.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Product images

are stored

in

Object Storage.

The database

contains:

```text id="obj5918"
product_id

image_key
```

The application

returns

the object URL.

The browser

downloads

the image

directly.

______________________________________________________________________

# Benefits

Object Storage provides:

✅ Massive scalability

✅ High durability

✅ Low storage cost

✅ Global availability

✅ Simple API access

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Higher latency

than local disk

❌ No SQL queries

❌ Whole-object updates

❌ Eventual consistency

for some operations

(depending on the provider)

______________________________________________________________________

# When NOT to Use Object Storage

Don't use

Object Storage

for:

- Database files
- Operating system disks
- Frequently updated small records
- Low-latency random writes

Use

Block Storage

or

Databases

instead.

______________________________________________________________________

# Best Practices

✅ Store only file references in databases.

✅ Use Presigned URLs.

✅ Enable Versioning.

✅ Configure Lifecycle Policies.

______________________________________________________________________

# Common Mistakes

### Storing Large Files in PostgreSQL

Databases

are optimized

for structured data,

not

large binary files.

Store

only

references.

______________________________________________________________________

### Uploading Through the API

Large uploads

consume

application resources.

Use

Presigned URLs

for direct uploads.

______________________________________________________________________

### Public Buckets

Never expose

private files

without

proper authentication

and authorization.

______________________________________________________________________

### Ignoring Lifecycle Policies

Unused files

increase

storage costs.

Automatically

archive

or delete

old data.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Object Storage, and why is Amazon S3 widely used?

Object Storage is a storage architecture where data is stored as independent objects containing the file itself,
metadata, and a unique identifier. Unlike traditional file systems, it uses a flat namespace organized into buckets and
scales horizontally to store billions of objects. Amazon S3 is widely used because it provides highly durable, scalable,
and cost-effective storage with features such as versioning, lifecycle policies, replication, encryption, and presigned
URLs. Modern applications typically store only object references in databases while keeping the actual files in Object
Storage.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Object Storage is
- Objects and Buckets
- Metadata
- Object Storage Architecture
- Versioning
- Lifecycle Policies
- Presigned URLs
- Amazon S3
- MinIO
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand modern storage solutions:

- ✅ Database Replication
- ✅ Database Sharding
- ✅ Object Storage

These are fundamental components used by nearly every cloud-native application.

______________________________________________________________________

# What's Next

[Search Engines (Elasticsearch & OpenSearch)](60-search-engines.md)
