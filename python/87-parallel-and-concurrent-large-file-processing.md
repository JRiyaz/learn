# Python Large File Processing

## 05. Parallel and Concurrent Large File Processing

> **Target Audience:** Python Backend Engineers (Intermediate → Senior)
>
> **Goal:** Learn how to speed up large file processing using threads, processes, async programming, and producer-consumer architecture. Understand when each approach is appropriate and avoid common performance mistakes.

______________________________________________________________________

# Introduction

Until now,

we have learned

how to process

large files

using

constant memory.

But what if

processing

is still slow?

Example

```
100 GB Log File

↓

Single CPU Core

↓

3 Hours
```

Can we make it faster?

Sometimes yes.

Sometimes no.

It depends on

the bottleneck.

______________________________________________________________________

# The First Question

Interview favorite.

Before trying

parallel processing,

ask

```
What is

the bottleneck?
```

Is it

```
Disk I/O?

↓

CPU?

↓

Network?

↓

Database?
```

Adding more threads

doesn't always

make programs faster.

______________________________________________________________________

# CPU-Bound vs I/O-Bound

Interview favorite.

## CPU-Bound

Time is spent

doing calculations.

Examples

- Image Processing
- Encryption
- Compression
- Hashing
- Data Analysis

______________________________________________________________________

## I/O-Bound

Time is spent

waiting.

Examples

- Reading Files
- Database Calls
- HTTP Requests
- S3 Downloads

______________________________________________________________________

# Why Does This Matter?

Python has

the

```
Global Interpreter Lock (GIL)
```

Only one thread

can execute

Python bytecode

at a time.

Therefore

threads

are not ideal

for CPU-heavy work.

______________________________________________________________________

# Choosing the Right Tool

| Workload | Best Choice |
|-----------|-------------|
| File Reading | Threads |
| HTTP Requests | Async |
| Database Calls | Async / Threads |
| Image Processing | Processes |
| Compression | Processes |
| CSV Parsing | Depends |
| File Uploads | Async |

______________________________________________________________________

# Threading

Threading

allows

multiple tasks

to run

concurrently.

Example

```
Read File A

↓

Read File B

↓

Read File C
```

Useful

when

the program

waits frequently.

______________________________________________________________________

# Example

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:

    executor.map(process_file, files)
```

______________________________________________________________________

# When to Use Threads

- Reading many files
- Uploading files
- Downloading files
- Database calls
- API requests

______________________________________________________________________

# When NOT to Use Threads

Avoid

threads

for

heavy computation.

Example

```
SHA256

Image Resize

Video Encoding
```

Use

processes instead.

______________________________________________________________________

# Multiprocessing

Interview favorite.

Processes

have

their own

Python interpreter

and

their own memory.

Therefore

they are

not limited

by the GIL.

______________________________________________________________________

# Example

```python
from multiprocessing import Pool

with Pool() as pool:

    pool.map(process_file, files)
```

______________________________________________________________________

# Benefits

Processes

can fully utilize

multiple CPU cores.

Example

```
8-Core CPU

↓

8 Processes

↓

8x Faster

(ideal case)
```

______________________________________________________________________

# Drawbacks

Processes

consume

more memory

than threads.

Creating processes

is also

more expensive.

______________________________________________________________________

# Async Programming

Async

is useful

when

tasks spend

most of their time

waiting.

Example

```
Upload File

↓

Wait

↓

Download

↓

Wait

↓

Database

↓

Wait
```

Instead of waiting,

the event loop

works

on

other tasks.

______________________________________________________________________

# Async Example

```python
async def process():

    async with aiofiles.open(
        "logs.txt"
    ) as file:

        async for line in file:

            process_line(line)
```

______________________________________________________________________

# Async Is NOT Magic

Interview favorite.

Async

does NOT

make

CPU work

faster.

It only helps

when waiting

for

I/O operations.

______________________________________________________________________

# Producer-Consumer Pattern

Interview favorite.

Very common

in production systems.

```
Producer

↓

Queue

↓

Consumer
```

______________________________________________________________________

# Example

```
Read File

↓

Queue

↓

Workers

↓

Database
```

Instead of

one function

doing everything,

work is divided.

______________________________________________________________________

# Why Use a Queue?

The reader

should not

wait

for

database inserts.

Instead

```
Reader

↓

Queue

↓

Worker

↓

Database
```

Both run

independently.

______________________________________________________________________

# Real Example

Suppose

we have

a

50 GB CSV.

```
Reader

↓

Queue

↓

Validation Worker

↓

Database Worker

↓

Notification Worker
```

Each worker

does

one job.

______________________________________________________________________

# Pipeline Processing

Instead of

```
Read

↓

Validate

↓

Insert

↓

Repeat
```

Use

```
Reader

↓

Queue

↓

Validator

↓

Queue

↓

Database

↓

Queue

↓

Report
```

Each stage

works

independently.

______________________________________________________________________

# Parallel Chunk Processing

Suppose

a file

contains

independent records.

```
Chunk 1

↓

Worker 1
```

```
Chunk 2

↓

Worker 2
```

```
Chunk 3

↓

Worker 3
```

Results

are merged

after processing.

______________________________________________________________________

# When Chunking Doesn't Work

Some files

cannot

be split easily.

Example

```
JSON Array
```

Splitting

in the middle

may produce

invalid JSON.

______________________________________________________________________

# File Splitting

Suitable for

- CSV
- Log Files
- NDJSON

More difficult for

- XML
- JSON Arrays
- Binary Formats

______________________________________________________________________

# Database Inserts

Wrong

```
Read Row

↓

Insert

↓

Read Row

↓

Insert
```

Too many

database calls.

______________________________________________________________________

Better

```
Read 1000 Rows

↓

Insert Batch

↓

Repeat
```

Fewer

network round trips.

______________________________________________________________________

# Reading Multiple Files

Suppose

a directory

contains

```
1000 Log Files
```

Each file

can be processed

by

a different worker.

This is

embarrassingly parallel.

______________________________________________________________________

# Common Architecture

```
Files

↓

Producer

↓

Queue

↓

Workers

↓

Results

↓

Database
```

Used by

many

ETL systems.

______________________________________________________________________

# Common Mistakes

## Too Many Threads

Creating

1000 threads

usually hurts

performance.

______________________________________________________________________

## Too Many Processes

Processes

consume memory.

More processes

doesn't always

mean

more speed.

______________________________________________________________________

## Ignoring the GIL

Threads

won't significantly

speed up

CPU-heavy work.

______________________________________________________________________

## Tiny Tasks

Creating

a thread

for

every line

is inefficient.

Group work

into batches.

______________________________________________________________________

## Shared Data

Multiple workers

writing

to the same object

can cause

race conditions.

Use

queues

or

proper synchronization.

______________________________________________________________________

# Best Practices

- Identify the bottleneck before optimizing.
- Use threads for I/O-bound workloads.
- Use processes for CPU-bound workloads.
- Batch database operations.
- Use producer-consumer architecture.
- Measure performance before and after optimization.

______________________________________________________________________

# Performance Comparison

| Technique | CPU Work | I/O Work | Memory |
|------------|----------|----------|--------|
| Single Thread | Good | Good | Low |
| Threads | Poor | Excellent | Medium |
| Processes | Excellent | Good | High |
| Async | Poor | Excellent | Low |

______________________________________________________________________

# Common Interview Questions

## When should you use threads?

Threads are best for I/O-bound workloads where the program spends most of its time waiting for operations such as file
reads, network calls, or database queries.

______________________________________________________________________

## When should you use multiprocessing?

Multiprocessing is best for CPU-intensive work because each process has its own Python interpreter and is not limited by
the Global Interpreter Lock (GIL).

______________________________________________________________________

## Why doesn't async make CPU-bound code faster?

Async improves concurrency by allowing other tasks to run while waiting for I/O. It does not parallelize CPU execution.

______________________________________________________________________

## What is the Producer-Consumer pattern?

It separates the producer of work from the consumers using a queue, allowing different parts of the pipeline to work
independently and efficiently.

______________________________________________________________________

## Why use batch inserts instead of inserting one row at a time?

Batch inserts reduce the number of database round trips, improving throughput and reducing network overhead.

______________________________________________________________________

# Interview Deep Dive

## Question

You need to process a 200 GB CSV file and insert the records into PostgreSQL. How would you design the solution?

### Answer

I would stream the CSV file instead of loading it into memory. A producer would read the file in batches and place
records into a queue. Multiple worker threads or async tasks would validate the data and batch database inserts. If the
processing involved heavy CPU computation, I would use multiprocessing instead of threads. This approach keeps memory
usage low while maximizing throughput.

______________________________________________________________________

# Summary

Large file processing

can often be accelerated

using

parallel

and concurrent

techniques.

The key is

choosing

the right tool

for the workload.

Remember

- Threads → I/O-bound work
- Processes → CPU-bound work
- Async → Waiting for I/O
- Queues → Producer-Consumer pipelines
- Batching → Higher throughput

Optimization

should always

start by identifying

the actual bottleneck,

not by adding

more threads.

______________________________________________________________________

# Next

[06. Async File Processing and Streaming](88-async-file-processing-and-streaming.md)
