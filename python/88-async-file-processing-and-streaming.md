# Python Large File Processing

## 06. Async File Processing and Streaming

> **Target Audience:** Python Backend Engineers (Intermediate → Senior)
>
> **Goal:** Understand asynchronous file processing, streaming uploads/downloads, streaming HTTP responses, and when async programming actually improves performance.

______________________________________________________________________

# Introduction

In the previous chapter,

we learned

how to process

large files

using

threads,

processes,

and

producer-consumer architecture.

Now,

let's understand

where

```
async

await
```

fits into

large file processing.

One important fact:

> Async does **NOT** make file reading faster.

It makes your application

handle

many file operations

concurrently.

______________________________________________________________________

# What is Async?

Interview favorite.

Normally,

a program

executes

one statement

after another.

```
Task A

↓

Task B

↓

Task C
```

With async,

when one task

is waiting,

another task

can execute.

```
Task A

↓

Waiting

↓

Task B

↓

Waiting

↓

Task C
```

This improves

resource utilization.

______________________________________________________________________

# Why Async?

Suppose

a client uploads

a

```
10 GB File
```

The server spends

most of its time

waiting

for

network packets.

Instead of

waiting,

the event loop

can process

other requests.

______________________________________________________________________

# Async vs Threading

| Async | Threading |
|---------|-----------|
| One Event Loop | Multiple Threads |
| Lightweight | More Memory |
| Excellent for I/O | Good for I/O |
| No Context Switching | OS Context Switching |

______________________________________________________________________

# Async Is Not Parallelism

Interview favorite.

Async

is about

concurrency.

It is **not**

parallel execution.

```
Task A

↓

Wait

↓

Task B

↓

Wait

↓

Resume Task A
```

Only

one task

runs

at a time,

but

CPU isn't wasted

waiting.

______________________________________________________________________

# Event Loop

Everything

in async

is managed

by

the

```
Event Loop
```

```
Event Loop

↓

Task 1

↓

Task 2

↓

Task 3

↓

Task 4
```

Whenever

one task waits,

another begins.

______________________________________________________________________

# Blocking Example

```python
with open("large.txt") as file:

    data = file.read()
```

While

reading

the file,

the current thread

is blocked.

Nothing else

can execute.

______________________________________________________________________

# Async File Reading

Using

```
aiofiles
```

Example

```python
import aiofiles

async with aiofiles.open(
    "large.txt",
    "r"
) as file:

    async for line in file:

        process(line)
```

Notice

```
async for
```

instead of

```
for
```

______________________________________________________________________

# What Actually Happens?

```
Read File

↓

Waiting

↓

Event Loop

↓

Run Another Task

↓

Resume Reading
```

______________________________________________________________________

# Streaming Uploads

Interview favorite.

Suppose

a user uploads

```
20 GB Video
```

Wrong approach

```
Receive Entire File

↓

RAM

↓

Save
```

______________________________________________________________________

Better

```
Receive Chunk

↓

Write Disk

↓

Receive Next Chunk

↓

Repeat
```

Memory

remains

constant.

______________________________________________________________________

# FastAPI Upload

Example

```python
from fastapi import UploadFile

@app.post("/upload")
async def upload(
    file: UploadFile
):
    ...
```

`UploadFile`

does **not**

load

the entire file

into memory.

It supports

streaming.

______________________________________________________________________

# Saving Uploads

Example

```python
while chunk := await file.read(1024 * 1024):

    output.write(chunk)
```

Flow

```
Network

↓

1 MB

↓

Disk

↓

Next 1 MB
```

______________________________________________________________________

# Why Not Read Everything?

Suppose

100 users

upload

```
10 GB
```

simultaneously.

```
100 × 10 GB

=

1000 GB RAM
```

Impossible.

Streaming

solves

this problem.

______________________________________________________________________

# Streaming Downloads

Suppose

a client downloads

a

```
50 GB Backup
```

Instead of

```
Read Entire File

↓

RAM

↓

Send
```

Use

```
Read Chunk

↓

Send Chunk

↓

Repeat
```

______________________________________________________________________

# FastAPI StreamingResponse

Interview favorite.

Example

```python
from fastapi.responses import StreamingResponse

@app.get("/download")

def download():

    return StreamingResponse(
        open(
            "backup.zip",
            "rb"
        )
    )
```

FastAPI

sends

the file

incrementally.

______________________________________________________________________

# Streaming API Responses

Suppose

an endpoint

returns

millions

of records.

Instead of

building

one huge JSON,

stream

the response.

```
Database

↓

Record

↓

Client
```

Client

starts receiving

data immediately.

______________________________________________________________________

# Real-Time Log Streaming

Example

```
Application Logs

↓

FastAPI

↓

StreamingResponse

↓

Browser
```

The browser

receives logs

continuously,

similar to

```
tail -f
```

______________________________________________________________________

# Async Producer-Consumer

```
Upload

↓

Async Queue

↓

Workers

↓

Database
```

Producer

doesn't wait

for workers.

Workers

consume

tasks

independently.

______________________________________________________________________

# Backpressure

Interview favorite.

Suppose

the producer

creates data

faster

than consumers

can process it.

```
Producer

↓

↓↓↓↓↓

Queue

↓

Consumer
```

Queue

continues growing.

Eventually

memory

is exhausted.

______________________________________________________________________

# Solution

Limit

queue size.

Example

```
Queue Full

↓

Producer Waits

↓

Consumers Catch Up
```

This is called

```
Backpressure
```

______________________________________________________________________

# Async Limitations

Async

does NOT

help

when

the bottleneck

is

```
CPU
```

Example

```
Image Compression

Video Encoding

Encryption
```

Use

multiprocessing

instead.

______________________________________________________________________

# Async + Database

Suppose

processing

each line

requires

a database query.

```
Read Line

↓

Await Database

↓

Process Next Task
```

This is

an excellent

use case

for async.

______________________________________________________________________

# Async + HTTP Requests

Suppose

each record

requires

calling

another API.

Without async

```
Request

↓

Wait

↓

Request

↓

Wait
```

With async

```
Request A

↓

Waiting

↓

Request B

↓

Waiting

↓

Request C
```

Much better

throughput.

______________________________________________________________________

# Common Mistakes

## Using Async for CPU Work

Bad choice.

Use

multiprocessing.

______________________________________________________________________

## Reading Entire Upload

Never do

```python
await file.read()
```

on

very large files.

Read

in chunks.

______________________________________________________________________

## Unlimited Queues

Queues

that grow forever

can consume

all available memory.

______________________________________________________________________

## Blocking Calls

Avoid

```
time.sleep()
```

inside

async code.

Use

```python
await asyncio.sleep()
```

instead.

______________________________________________________________________

# Best Practices

- Stream uploads and downloads.
- Read files in chunks.
- Use `UploadFile` for large uploads.
- Use `StreamingResponse` for large downloads.
- Apply backpressure using bounded queues.
- Use async only for I/O-bound operations.

______________________________________________________________________

# Performance Comparison

| Technique | Large Uploads | Large Downloads | Memory |
|------------|---------------|-----------------|--------|
| read() | ❌ Poor | ❌ Poor | High |
| Chunk Streaming | ✅ Excellent | ✅ Excellent | Low |
| Async Streaming | ✅ Excellent | ✅ Excellent | Very Low |

______________________________________________________________________

# Common Interview Questions

## Does async make file reading faster?

No.

Disk speed remains the same. Async improves concurrency by allowing other tasks to execute while waiting for I/O.

______________________________________________________________________

## Why use `UploadFile` instead of reading the entire request body?

`UploadFile` streams uploaded data, preventing large files from consuming excessive memory.

______________________________________________________________________

## What is `StreamingResponse`?

`StreamingResponse` sends data to the client incrementally instead of building the entire response in memory first.

______________________________________________________________________

## What is backpressure?

Backpressure is a mechanism that slows down producers when consumers cannot keep up, preventing queues from growing
indefinitely and exhausting system memory.

______________________________________________________________________

## When should you avoid async?

Avoid async for CPU-intensive tasks such as image processing, video encoding, encryption, or compression.
Multiprocessing is a better choice for those workloads.

______________________________________________________________________

# Interview Deep Dive

## Question

How would you implement a FastAPI endpoint that allows users to upload 50 GB files?

### Answer

I would use FastAPI's `UploadFile`, which supports streaming uploads. Instead of reading the entire file into memory, I
would read it in fixed-size chunks (for example, 1 MB), writing each chunk directly to disk or object storage. This
keeps memory usage nearly constant regardless of file size. If additional processing is required, I would publish a
background task or queue message after the upload completes rather than processing the file during the request.

______________________________________________________________________

# Summary

Async programming

is most valuable

when applications

spend time

waiting for

I/O operations.

For large file processing,

async enables

- Streaming uploads
- Streaming downloads
- Concurrent file operations
- Responsive APIs
- Efficient resource utilization

However,

async is **not**

a replacement

for multiprocessing

when performing

CPU-intensive work.

______________________________________________________________________

# Next

[07. Processing Compressed Files Efficiently](89-processing-compressed-files-efficiently.md)
