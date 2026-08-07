# Python Large File Processing

## 08. Large File Processing in Production Systems

> **Target Audience:** Python Backend Engineers (Intermediate → Senior)
>
> **Goal:** Learn how production systems process very large files (10 GB–10 TB), including uploads, downloads, storage, processing pipelines, fault tolerance, retries, progress tracking, and scalability.

______________________________________________________________________

# Introduction

Everything

we've learned so far

works well

on a single machine.

However,

real-world applications

process files

that are

much larger.

Examples

- 50 GB Database Backup
- 500 GB Log Files
- 2 TB Analytics Dataset
- 100 GB Video
- 1 TB CSV Export

A production system

must handle

these files

without

- Running out of memory
- Blocking users
- Losing progress
- Corrupting data

______________________________________________________________________

# Typical Production Flow

```
Client

↓

Upload API

↓

Object Storage

↓

Message Queue

↓

Background Workers

↓

Database

↓

Notification
```

Notice

the upload request

does **not**

process

the file immediately.

______________________________________________________________________

# Why Not Process During Upload?

Suppose

processing

takes

```
2 Hours
```

If the API waits

```
Client

↓

Upload

↓

Wait 2 Hours
```

The request

will timeout.

Instead

```
Upload

↓

Return Success

↓

Background Processing
```

______________________________________________________________________

# Complete Architecture

```
Client

↓

Nginx

↓

FastAPI

↓

Save File

↓

S3 / MinIO

↓

Publish Event

↓

Kafka / RabbitMQ

↓

Workers

↓

Database

↓

Notification
```

Every component

has

one responsibility.

______________________________________________________________________

# Step 1

# Upload File

Client uploads

```
sales.csv

25 GB
```

The API

streams

the upload

directly

to storage.

______________________________________________________________________

# Step 2

# Store Metadata

Before processing,

store

information

about the file.

Example

```
File ID

Filename

Status

Upload Time

User ID

Size
```

Example Table

| Field | Value |
|---------|--------|
| File ID | 123 |
| Name | sales.csv |
| Status | Uploaded |
| Size | 25 GB |

______________________________________________________________________

# Step 3

# Store File

Never store

large files

inside

PostgreSQL.

Instead

use

```
S3

MinIO

Azure Blob

Google Cloud Storage
```

Database stores

only

metadata.

______________________________________________________________________

# Why Object Storage?

Advantages

- Cheap
- Durable
- Scalable
- Easy Backup
- High Availability

______________________________________________________________________

# Step 4

# Publish Event

After upload

publish

an event.

```
File Uploaded
```

Example

```
File ID

↓

Kafka

↓

Workers
```

The upload API

is finished.

______________________________________________________________________

# Why Use Kafka?

The upload service

doesn't need

to know

how processing works.

It simply says

```
A file

is ready.
```

Workers

decide

what to do next.

______________________________________________________________________

# Step 5

# Background Workers

Workers

download

the file

and begin

processing.

```
Worker

↓

Read Chunk

↓

Validate

↓

Store Result

↓

Next Chunk
```

______________________________________________________________________

# Multiple Workers

Suppose

a file

contains

independent data.

```
Worker 1

↓

Chunk 1
```

```
Worker 2

↓

Chunk 2
```

```
Worker 3

↓

Chunk 3
```

Parallel processing

reduces

overall time.

______________________________________________________________________

# Chunk-Based Processing

Interview favorite.

Instead of

```
25 GB

↓

RAM
```

Workers process

```
5 MB

↓

Process

↓

Discard

↓

Next 5 MB
```

______________________________________________________________________

# Progress Tracking

Users

should know

processing status.

Database

stores

```
Uploaded

↓

Processing

↓

Completed

↓

Failed
```

Or

```
45%

Completed
```

______________________________________________________________________

# Progress API

Example

```
GET

/files/123/status
```

Response

```json
{
    "status":"processing",
    "progress":72
}
```

Frontend

polls

this endpoint.

______________________________________________________________________

# Error Handling

Suppose

processing fails

at

```
80%
```

Never restart

from

0%.

Instead

resume

from

the last

successful checkpoint.

______________________________________________________________________

# Checkpointing

Example

```
Chunk 1

✓
```

```
Chunk 2

✓
```

```
Chunk 3

✗
```

Restart

only

Chunk 3.

______________________________________________________________________

# Retry Mechanism

Temporary failures

can happen.

Example

```
Database Offline

↓

Retry

↓

Retry

↓

Success
```

Avoid

immediately

marking

the job

as failed.

______________________________________________________________________

# Dead Letter Queue (DLQ)

Interview favorite.

Suppose

processing

fails

after

multiple retries.

Instead of

losing the message,

move it

to

```
Dead Letter Queue
```

Engineers

can inspect

and reprocess it.

______________________________________________________________________

# Idempotency

Suppose

Kafka

delivers

the same message

twice.

Without protection

```
Same File

↓

Processed Twice
```

Bad.

Workers

should detect

duplicate processing.

______________________________________________________________________

# Logging

Every step

should be logged.

Example

```
Upload Started

↓

Upload Finished

↓

Processing Started

↓

Chunk 15 Failed

↓

Retry

↓

Completed
```

Useful

for debugging.

______________________________________________________________________

# Monitoring

Track

- Processing Time
- Queue Length
- Failed Jobs
- Average Throughput
- Active Workers

These metrics

help detect

performance issues.

______________________________________________________________________

# Notifications

When processing finishes

send

- Email
- WebSocket Event
- Push Notification

User

doesn't need

to refresh

continuously.

______________________________________________________________________

# Scaling Workers

Suppose

1000 files

arrive

simultaneously.

Instead of

one worker

```
Queue

↓

Worker 1
```

Scale

to

```
Queue

↓

Worker 1

Worker 2

Worker 3

Worker 4
```

Workers

can be added

or removed

based on load.

______________________________________________________________________

# Temporary Files

Sometimes

processing

requires

temporary storage.

Use

```
tempfile
```

instead of

hardcoded paths.

Always

clean up

temporary files

after processing.

______________________________________________________________________

# File Integrity

Interview favorite.

How do you know

the uploaded file

wasn't corrupted?

Use

checksums.

Example

```
SHA256

↓

Compare

↓

Match?
```

If hashes differ

the upload

is corrupted.

______________________________________________________________________

# Security

Always validate

- File type
- MIME type
- File size
- User permissions

Never trust

only

the filename.

______________________________________________________________________

# Virus Scanning

Many companies

scan uploads

before processing.

Example

```
Upload

↓

Virus Scan

↓

Safe?

↓

Process
```

______________________________________________________________________

# Common Architecture

```
Client

↓

Upload API

↓

Object Storage

↓

Queue

↓

Worker

↓

Database

↓

Notification
```

Simple,

scalable,

and fault tolerant.

______________________________________________________________________

# Common Mistakes

## Processing During Upload

Causes

long-running

HTTP requests.

______________________________________________________________________

## Saving Large Files in PostgreSQL

Use

object storage

instead.

______________________________________________________________________

## No Retry Mechanism

Temporary failures

become

permanent failures.

______________________________________________________________________

## No Progress Tracking

Users

don't know

whether

processing

is still running.

______________________________________________________________________

## No Checkpointing

Failures

restart

the entire job.

______________________________________________________________________

# Best Practices

- Stream uploads.
- Store files in object storage.
- Process files asynchronously.
- Use queues for communication.
- Implement retries.
- Use checkpoints.
- Track progress.
- Verify file integrity.
- Scale workers independently.

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Upload API | FastAPI |
| Storage | S3 / MinIO |
| Queue | Kafka / RabbitMQ |
| Workers | Celery |
| Cache | Redis |
| Database | PostgreSQL |
| Monitoring | Prometheus |
| Dashboard | Grafana |

______________________________________________________________________

# Common Interview Questions

## Why shouldn't large files be processed during the upload request?

Because processing may take minutes or hours, causing request timeouts and poor user experience. Uploading and
processing should be separated using background workers.

______________________________________________________________________

## Why store large files in object storage instead of PostgreSQL?

Object storage is designed for large binary files, provides better scalability, lower cost, and higher durability.
PostgreSQL should store only metadata.

______________________________________________________________________

## What is checkpointing?

Checkpointing records processing progress so that failed jobs can resume from the last successful point instead of
restarting from the beginning.

______________________________________________________________________

## Why is idempotency important?

Distributed systems may retry messages or deliver them more than once. Idempotent processing ensures the same file is
not processed multiple times.

______________________________________________________________________

## What is a Dead Letter Queue?

A Dead Letter Queue stores messages that repeatedly fail processing, allowing engineers to inspect and retry them later
without losing data.

______________________________________________________________________

# Interview Deep Dive

## Question

Design a system that processes a 100 GB CSV uploaded by users.

### Answer

The client streams the file to a FastAPI upload endpoint, which stores it in object storage such as Amazon S3 or MinIO
and records metadata in PostgreSQL. After the upload completes, the service publishes a message to Kafka or RabbitMQ.
Background workers consume the message, process the file incrementally in chunks, and periodically update processing
progress in the database or Redis. Failed chunks are retried, and persistent failures are moved to a Dead Letter Queue.
Once processing completes, the user is notified through email, WebSocket, or push notification.

______________________________________________________________________

# Summary

Production systems

treat

file upload

and

file processing

as separate operations.

The typical workflow is

- Stream the upload
- Store the file in object storage
- Publish an event
- Process asynchronously
- Track progress
- Retry failures
- Notify the user

This architecture scales from a few files to millions of files while remaining memory efficient and fault tolerant.

______________________________________________________________________

# Next

[09. Large File Processing System Design](09-large-file-processing-system-design.md)
