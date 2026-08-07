# Python Large File Processing

## 07. Processing Compressed Files Efficiently

> **Target Audience:** Python Backend Engineers (Intermediate → Senior)
>
> **Goal:** Learn how to efficiently process compressed files such as GZIP, ZIP, BZIP2, TAR, and LZMA without extracting entire archives into memory. Understand streaming decompression, common production use cases, and performance considerations.

______________________________________________________________________

# Introduction

Large files

are often

compressed

before

being stored

or transferred.

Reasons include

- Save disk space
- Reduce network bandwidth
- Faster uploads
- Faster downloads
- Lower storage costs

Instead of

processing

```
users.csv
```

you'll often receive

```
users.csv.gz

users.zip

backup.tar.gz

logs.bz2
```

A common mistake

is

extracting

the entire archive

before processing.

Production systems

rarely do this.

______________________________________________________________________

# Why Compress Files?

Suppose

you have

a

```
20 GB CSV
```

After compression

it becomes

```
2 GB
```

Advantages

```
Smaller Storage

↓

Faster Transfer

↓

Lower Cloud Cost
```

______________________________________________________________________

# Common Compression Formats

| Format | Extension | Typical Use |
|---------|-----------|-------------|
| GZIP | .gz | Logs, CSV, Backups |
| ZIP | .zip | Documents, Multiple Files |
| TAR | .tar | Archive Multiple Files |
| TAR + GZIP | .tar.gz | Linux Backups |
| BZIP2 | .bz2 | Large Archives |
| LZMA/XZ | .xz | Maximum Compression |

______________________________________________________________________

# Processing GZIP Files

Interview favorite.

Python provides

the

```
gzip
```

module.

Example

```python
import gzip

with gzip.open(
    "users.csv.gz",
    "rt"
) as file:

    for line in file:

        process(line)
```

Notice

```
No Extraction

↓

Streaming

↓

Constant Memory
```

______________________________________________________________________

# What Actually Happens?

```
Compressed File

↓

Read Small Block

↓

Decompress

↓

Process

↓

Discard

↓

Next Block
```

Memory usage

remains low.

______________________________________________________________________

# Why Not Extract First?

Bad approach

```
Extract 50 GB

↓

Temporary Disk

↓

Read File

↓

Delete File
```

Problems

- Extra disk space
- Extra I/O
- Longer processing time

______________________________________________________________________

# Better Approach

```
Compressed File

↓

Stream

↓

Decompress

↓

Process

↓

Done
```

______________________________________________________________________

# Reading Compressed CSV

Example

```python
import csv
import gzip

with gzip.open(
    "users.csv.gz",
    "rt"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        process(row)
```

Compressed

and

memory efficient.

______________________________________________________________________

# ZIP Files

Unlike GZIP,

ZIP archives

can contain

multiple files.

Example

```
backup.zip

↓

users.csv

orders.csv

products.csv
```

______________________________________________________________________

# Reading ZIP Files

```python
import zipfile

with zipfile.ZipFile(
    "backup.zip"
) as archive:

    with archive.open(
        "users.csv"
    ) as file:

        process(file)
```

No extraction

required.

______________________________________________________________________

# Listing Files

Example

```python
with zipfile.ZipFile(
    "backup.zip"
) as archive:

    print(
        archive.namelist()
    )
```

Output

```
users.csv

orders.csv

products.csv
```

______________________________________________________________________

# TAR Archives

Linux systems

commonly use

```
.tar
```

or

```
.tar.gz
```

Example

```python
import tarfile

with tarfile.open(
    "backup.tar.gz"
) as archive:

    ...
```

______________________________________________________________________

# Reading TAR Members

```python
for member in archive:

    if member.isfile():

        file = archive.extractfile(member)

        process(file)
```

Again,

no need

to extract

everything first.

______________________________________________________________________

# BZIP2

Python supports

```
.bz2
```

using

```python
import bz2

with bz2.open(
    "logs.bz2",
    "rt"
) as file:

    ...
```

______________________________________________________________________

# LZMA / XZ

Example

```python
import lzma

with lzma.open(
    "backup.xz",
    "rt"
) as file:

    ...
```

Higher compression

than GZIP,

but

typically slower

to compress

and decompress.

______________________________________________________________________

# Streaming Pipeline

Suppose

you receive

```
logs.gz
```

Pipeline

```
Read Compressed File

↓

Decompress

↓

Parse

↓

Filter

↓

Store Database
```

Everything

is processed

incrementally.

______________________________________________________________________

# Real Production Example

Every hour

your application

downloads

```
logs-2026-08-08.gz
```

Instead of

```
Download

↓

Extract

↓

Read

↓

Delete
```

Use

```
Download

↓

Stream

↓

Process

↓

Store Results
```

Less disk usage.

Faster processing.

______________________________________________________________________

# Processing Huge Backups

Suppose

you receive

```
database.tar.gz

=

300 GB
```

Need only

```
users.csv
```

No need

to extract

everything.

Read only

the required file

inside

the archive.

______________________________________________________________________

# Compression Trade-Off

Compression

reduces

disk I/O,

but

increases

CPU usage.

```
Smaller File

↓

Less Disk Reading

↓

More CPU Decompression
```

Sometimes

overall performance

is still better.

______________________________________________________________________

# Which Format Should You Use?

| Format | Compression | Speed |
|----------|-------------|-------|
| GZIP | Good | Fast |
| ZIP | Good | Fast |
| BZIP2 | Better | Medium |
| XZ | Excellent | Slow |

______________________________________________________________________

# Production Best Practices

For logs

```
GZIP
```

For backups

```
TAR.GZ
```

For user uploads

```
ZIP
```

For archival storage

```
XZ
```

______________________________________________________________________

# Common Mistakes

## Extracting Everything

Avoid

```
Extract

↓

Read

↓

Delete
```

when

streaming

is possible.

______________________________________________________________________

## Loading Compressed Files into Memory

Bad

```python
data = gzip.open(...).read()
```

Good

```python
for line in file:
```

______________________________________________________________________

## Forgetting Text Mode

```
"rt"
```

returns

strings.

```
"rb"
```

returns

bytes.

Choose

the correct mode.

______________________________________________________________________

## Assuming Compression Always Improves Speed

Compression

reduces I/O

but

adds CPU work.

Benchmark

your workload.

______________________________________________________________________

# Best Practices

- Stream compressed files whenever possible.
- Avoid extracting large archives unnecessarily.
- Process archives incrementally.
- Use the appropriate compression format for the use case.
- Benchmark CPU and disk usage for your workload.

______________________________________________________________________

# Performance Comparison

| Format | Streaming | Multiple Files | Compression |
|----------|-----------|----------------|-------------|
| GZIP | ✅ | ❌ | Good |
| ZIP | ✅ | ✅ | Good |
| TAR | ✅ | ✅ | None |
| TAR.GZ | ✅ | ✅ | Good |
| BZIP2 | ✅ | ❌ | Better |
| XZ | ✅ | ❌ | Excellent |

______________________________________________________________________

# Common Interview Questions

## Why process compressed files without extracting them?

Streaming avoids temporary disk usage, reduces I/O, lowers storage requirements, and allows constant-memory processing.

______________________________________________________________________

## When should you use GZIP instead of ZIP?

GZIP is ideal for compressing a single large file, while ZIP is better when multiple files need to be packaged together.

______________________________________________________________________

## What is the advantage of `tar.gz`?

`tar` combines multiple files into one archive, while `gzip` compresses that archive, making it a common format for
Linux backups.

______________________________________________________________________

## Does compression always improve performance?

Not necessarily. Compression reduces disk and network I/O but increases CPU usage for compression and decompression. The
overall benefit depends on the workload.

______________________________________________________________________

## Can Python stream compressed files?

Yes. Modules such as `gzip`, `bz2`, `lzma`, `zipfile`, and `tarfile` allow compressed data to be processed incrementally
without extracting entire archives.

______________________________________________________________________

# Interview Deep Dive

## Question

Your application receives a 100 GB `users.csv.gz` file every night. How would you process it efficiently?

### Answer

I would avoid extracting the compressed file to disk. Instead, I would use Python's `gzip` module to stream the file
directly. Each row would be processed one at a time or in batches using `csv.DictReader`, and database inserts would be
batched for better performance. This approach keeps memory usage low, avoids temporary storage, and minimizes
unnecessary disk I/O.

______________________________________________________________________

# Summary

Compressed files

are common

in production systems

because they

reduce storage

and network costs.

Instead of

extracting

large archives,

Python allows

them to be

processed

incrementally

using streaming.

Key takeaways

- Use `gzip` for single compressed files.
- Use `zipfile` for archives containing multiple files.
- Use `tarfile` for Linux archives.
- Stream compressed files instead of extracting them.
- Balance CPU usage against I/O savings.

______________________________________________________________________

# Next

[08. Large File Processing in Production Systems](90-large-file-processing-in-production-systems.md)
