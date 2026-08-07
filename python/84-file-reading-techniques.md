# Python Large File Processing

## 02. File Reading Techniques

> Target Audience: Python Backend Engineers (Beginner → Senior)
>
> Goal: Understand every major file reading technique available in Python, their memory usage, performance characteristics, and when to use each approach for production applications.

______________________________________________________________________

# Introduction

In the previous chapter,

we learned

why reading

an entire file

into memory

is a bad idea

for large files.

Now,

let's understand

the different ways

Python reads files

and when

each technique

should be used.

______________________________________________________________________

# Overview

Python provides

multiple ways

to read files.

```
read()

↓

readline()

↓

readlines()

↓

for line in file

↓

Chunk Reading

↓

Buffered Reading

↓

Memory Mapping (Later)
```

Each has

different

performance

and memory

characteristics.

______________________________________________________________________

# Opening a File

The most common way

to open a file

is

```python
with open("data.txt", "r") as file:
    ...
```

Using

```
with
```

ensures

the file

is automatically closed,

even if

an exception occurs.

______________________________________________________________________

# File Modes

| Mode | Description |
|------|-------------|
| r | Read |
| w | Write |
| a | Append |
| x | Create |
| rb | Read Binary |
| wb | Write Binary |
| r+ | Read & Write |

______________________________________________________________________

# Method 1

# read()

Example

```python
with open("data.txt") as file:
    data = file.read()
```

______________________________________________________________________

# What Happens?

```
Disk

↓

Entire File

↓

RAM

↓

Python String
```

______________________________________________________________________

# Advantages

- Simple
- Easy to use
- Good for small files

______________________________________________________________________

# Disadvantages

- Loads entire file into memory
- Poor for large files
- May cause OOM

______________________________________________________________________

# Memory Usage

Suppose

```
File Size

=

5 GB
```

Memory usage

becomes

approximately

```
5 GB
```

______________________________________________________________________

# When to Use

✔ Small configuration files

✔ Small JSON files

✔ Small text files

Avoid

large datasets.

______________________________________________________________________

# Method 2

# readline()

Example

```python
with open("logs.txt") as file:

    line = file.readline()

    print(line)
```

Reads

only

one line

at a time.

______________________________________________________________________

# What Happens?

```
Disk

↓

Single Line

↓

RAM
```

______________________________________________________________________

# Memory Usage

Very low.

______________________________________________________________________

# Advantages

- Memory efficient
- Simple

______________________________________________________________________

# Disadvantages

Reading

millions of lines

using

repeated

```
readline()
```

is

less readable

than iteration.

______________________________________________________________________

# Method 3

# readlines()

Example

```python
with open("data.txt") as file:

    lines = file.readlines()
```

______________________________________________________________________

# What Happens?

```
Disk

↓

Every Line

↓

Python List
```

______________________________________________________________________

Example

```python
[
    "Line1",
    "Line2",
    "Line3"
]
```

______________________________________________________________________

# Memory Usage

Very high.

Not only

is the file

loaded,

but every line

becomes

a separate string

inside

a Python list.

______________________________________________________________________

# When to Avoid

Large log files

Large CSVs

Large datasets

______________________________________________________________________

# Method 4

# File Iteration

Interview favorite.

Example

```python
with open("logs.txt") as file:

    for line in file:

        process(line)
```

______________________________________________________________________

# What Happens?

Python

automatically

reads

the next line

when needed.

```
Disk

↓

Buffer

↓

Line

↓

Process

↓

Discard

↓

Next Line
```

______________________________________________________________________

# Why Is This Better?

Memory usage

stays

almost constant

regardless

of file size.

______________________________________________________________________

# Example

```
100 GB File

↓

One Line

↓

Process

↓

Next Line
```

Still

low memory.

______________________________________________________________________

# This Is The Recommended Approach

Whenever

you need

to process

text files

line by line.

______________________________________________________________________

# Method 5

# Reading Fixed Size Chunks

Interview favorite.

Example

```python
CHUNK_SIZE = 1024

with open("video.mp4", "rb") as file:

    while True:

        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        process(chunk)
```

______________________________________________________________________

# What Happens?

```
Disk

↓

1 KB

↓

Process

↓

Discard

↓

Next 1 KB
```

______________________________________________________________________

# Choosing Chunk Size

Common values

```
4 KB

8 KB

64 KB

1 MB

4 MB
```

There is

no perfect value.

It depends on

- Disk speed
- Network
- CPU
- Workload

______________________________________________________________________

# Binary vs Text Mode

Text Mode

```python
open("data.txt", "r")
```

Returns

```
str
```

______________________________________________________________________

Binary Mode

```python
open("image.jpg", "rb")
```

Returns

```
bytes
```

______________________________________________________________________

# When To Use Binary Mode

- Images
- Videos
- PDFs
- ZIP files
- Executables

______________________________________________________________________

# File Pointer

Interview favorite.

Every file

has

a pointer.

Initially

```
Beginning

↓

|
```

After reading

```
Hello World
^^^^^
```

Pointer moves.

______________________________________________________________________

# tell()

Returns

the current

file position.

Example

```python
with open("data.txt") as file:

    print(file.tell())
```

Output

```
0
```

After reading

```python
file.read(5)
```

Output

```
5
```

______________________________________________________________________

# seek()

Moves

the file pointer.

Example

```python
file.seek(0)
```

Move

to

the beginning.

______________________________________________________________________

Example

```python
file.seek(100)
```

Move

to

byte

100.

______________________________________________________________________

# Why Use seek()?

Useful for

- Resuming processing
- Random access
- Reading headers
- Skipping sections

______________________________________________________________________

# Buffered Reading

Python

uses buffering

internally.

Instead of

reading

one byte

at a time,

it reads

larger blocks.

```
Disk

↓

8 KB Buffer

↓

Application
```

This greatly

improves performance.

______________________________________________________________________

# Manual Buffer Size

Example

```python
open(
    "data.txt",
    buffering=8192
)
```

Normally,

Python's default

buffering

is sufficient.

______________________________________________________________________

# Comparing Methods

| Method | Memory | Performance | Large Files |
|---------|--------|-------------|-------------|
| read() | Very High | Fast | ❌ |
| readline() | Very Low | Good | ✅ |
| readlines() | Very High | Good | ❌ |
| for line in file | Very Low | Excellent | ✅ |
| read(chunk) | Very Low | Excellent | ✅ |

______________________________________________________________________

# Choosing The Right Method

## Small Config File

```
read()
```

______________________________________________________________________

## Large Log File

```
for line in file
```

______________________________________________________________________

## Video Processing

```
read(chunk)
```

______________________________________________________________________

## CSV Processing

```
for line in file
```

or

```
csv.reader()
```

______________________________________________________________________

## Image Processing

```
Binary Mode

+

Chunk Reading
```

______________________________________________________________________

# Common Mistakes

## Using read()

For

10 GB files.

______________________________________________________________________

## Using readlines()

Creates

millions

of Python strings.

______________________________________________________________________

## Forgetting Binary Mode

Reading

images

or

videos

using

text mode.

______________________________________________________________________

## Ignoring File Closure

Bad

```python
file = open(...)
```

Better

```python
with open(...)
```

______________________________________________________________________

# Performance Tips

- Use `with open()`
- Prefer iteration for text files
- Use chunk reading for binary files
- Avoid `readlines()` on large files
- Choose appropriate chunk sizes
- Let Python handle buffering unless profiling suggests otherwise

______________________________________________________________________

# Common Interview Questions

## Which method is best for processing a 100 GB log file?

Using

```python
for line in file
```

or chunk-based reading because both maintain low memory usage.

______________________________________________________________________

## Why is `readlines()` memory intensive?

It loads the entire file into a Python list, where each line is stored as a separate string.

______________________________________________________________________

## When should you use binary mode?

When reading non-text files such as images, videos, PDFs, ZIP files, or any binary data.

______________________________________________________________________

## What is the purpose of `seek()`?

It moves the file pointer to a specific byte position, enabling random access within a file.

______________________________________________________________________

## Why does Python use buffering?

Buffering reduces the number of disk I/O operations by reading larger blocks of data instead of individual bytes,
significantly improving performance.

______________________________________________________________________

# Interview Deep Dive

## Question

You're asked to process a 50 GB log file. Which file reading technique would you choose and why?

### Answer

I would use file iteration (`for line in file`) because it streams the file line by line with constant memory usage. If
the file contains binary data instead of text, I would read it in fixed-size chunks using `read(chunk_size)`. I would
avoid `read()` and `readlines()` because they attempt to load the entire file into memory.

______________________________________________________________________

# Summary

Python provides

multiple techniques

for reading files,

but not all of them

are suitable

for production systems.

For large text files,

prefer

```
for line in file
```

For large binary files,

prefer

```
read(chunk_size)
```

Both approaches

keep memory usage

low

and scale

to files

much larger

than available RAM.

______________________________________________________________________

# Next

[03. Memory Efficient Processing](85-memory-efficient-processing.md)
