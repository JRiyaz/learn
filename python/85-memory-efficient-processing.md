# Python Large File Processing

## 03. Memory Efficient Processing

> Target Audience: Python Backend Engineers (Intermediate → Senior)
>
> Goal: Learn how to process files using constant memory by leveraging generators, iterators, lazy evaluation, chunking, and streaming techniques. Understand why these concepts are fundamental in production systems.

______________________________________________________________________

# Introduction

In the previous chapter,

we learned

different ways

to read files.

Now,

we'll learn

how to process

those files

without consuming

large amounts

of memory.

This chapter

is one of

the most important

in the course.

______________________________________________________________________

# The Goal

Suppose

you receive

a

```
100 GB
```

CSV file.

Your server has

```
8 GB RAM
```

Can you process it?

Yes.

If you never try

to load

the entire file

into memory.

______________________________________________________________________

# Memory Efficient Processing

Instead of

```
100 GB File

↓

100 GB RAM
```

We want

```
100 GB File

↓

1 Line

↓

Process

↓

Discard

↓

Next Line
```

Memory usage

remains

almost constant.

______________________________________________________________________

# What is Lazy Evaluation?

Interview favorite.

Lazy Evaluation

means

data

is processed

only

when required.

Instead of

```
Load Everything

↓

Process
```

Python performs

```
Load Small Part

↓

Process

↓

Load Next Part
```

Nothing

is loaded

until

it's needed.

______________________________________________________________________

# Eager vs Lazy

## Eager

```python
numbers = list(range(1000000))
```

Memory

is allocated

for

one million numbers

immediately.

______________________________________________________________________

## Lazy

```python
numbers = range(1000000)
```

Numbers

are generated

only

when accessed.

Much lower

memory usage.

______________________________________________________________________

# What is a Generator?

Interview favorite.

A Generator

produces

values

one at a time.

Instead of

creating

an entire collection,

it generates

the next value

only

when requested.

______________________________________________________________________

# Normal Function

```python
def numbers():

    return [1,2,3]
```

Entire list

is created

before returning.

______________________________________________________________________

# Generator Function

```python
def numbers():

    yield 1

    yield 2

    yield 3
```

Each value

is produced

only

when requested.

______________________________________________________________________

# return vs yield

| return | yield |
|---------|--------|
| Ends function | Pauses function |
| Returns everything | Returns one value |
| Higher memory | Lower memory |

______________________________________________________________________

# How yield Works

Example

```python
def numbers():

    yield 1

    yield 2

    yield 3
```

Execution

```
Call Function

↓

yield 1

↓

Pause

↓

Resume

↓

yield 2

↓

Pause

↓

Resume

↓

yield 3

↓

End
```

Notice

the function

doesn't restart.

It resumes

where it stopped.

______________________________________________________________________

# Generator Example

```python
def read_file():

    with open("logs.txt") as file:

        for line in file:

            yield line
```

Now

only one line

exists

in memory

at a time.

______________________________________________________________________

# Using the Generator

```python
for line in read_file():

    process(line)
```

Memory usage

remains

very low.

______________________________________________________________________

# Generator Expression

Instead of

```python
squares = []

for i in range(10):

    squares.append(i*i)
```

Use

```python
squares = (
    i*i

    for i in range(10)
)
```

Nothing

is calculated

until needed.

______________________________________________________________________

# Iterator

Interview favorite.

An Iterator

is an object

that returns

the next value

when requested.

```
Iterator

↓

next()

↓

Value
```

______________________________________________________________________

# Example

```python
numbers = iter([1,2,3])

print(next(numbers))

print(next(numbers))
```

Output

```
1

2
```

______________________________________________________________________

# Relationship

```
Iterable

↓

Iterator

↓

Generator
```

Every Generator

is an Iterator.

Not every Iterator

is a Generator.

______________________________________________________________________

# File Objects are Iterators

Interview favorite.

This code

```python
for line in file:
```

works because

a file object

is already

an iterator.

Python

automatically reads

the next line

when required.

______________________________________________________________________

# Streaming Pipeline

Suppose

we want

to

- Read
- Filter
- Transform
- Save

Instead of

loading

everything,

build

a pipeline.

```
Read

↓

Filter

↓

Transform

↓

Write
```

Each stage

processes

one item

at a time.

______________________________________________________________________

# Example

```python
for line in file:

    if "ERROR" in line:

        write(line)
```

No extra list

is created.

______________________________________________________________________

# Bad Approach

```python
lines = file.readlines()

errors = []

for line in lines:

    if "ERROR" in line:

        errors.append(line)
```

Problems

- High memory
- Two large collections

______________________________________________________________________

# Better Approach

```python
for line in file:

    if "ERROR" in line:

        write(line)
```

Memory

stays constant.

______________________________________________________________________

# Chunk Processing

For binary files

we usually

process chunks.

Example

```python
CHUNK_SIZE = 1024 * 1024

with open(
    "video.mp4",
    "rb"
) as file:

    while True:

        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        process(chunk)
```

______________________________________________________________________

# Why Chunking?

Suppose

the file is

```
20 GB
```

Memory usage

is only

```
1 MB
```

if

```
CHUNK_SIZE

=

1 MB
```

______________________________________________________________________

# Batch Processing

Sometimes

processing

one record

at a time

is too slow.

Instead

process

small batches.

```
100 Records

↓

Process

↓

Next 100
```

Balances

speed

and

memory.

______________________________________________________________________

# Generator Pipeline

Interview favorite.

```python
Read File

↓

Generator

↓

Filter Generator

↓

Transform Generator

↓

Write Output
```

Each stage

receives

one item,

processes it,

then passes it

to the next stage.

______________________________________________________________________

# Advantages

- Constant memory
- Modular code
- Easy testing
- Reusable pipeline

______________________________________________________________________

# Real Production Example

Suppose

a bank

receives

```
50 Million Transactions
```

Pipeline

```
Read CSV

↓

Validate

↓

Fraud Detection

↓

Store Database

↓

Generate Report
```

At no point

are

50 million records

loaded

into memory.

______________________________________________________________________

# Memory Comparison

| Technique | Memory Usage |
|------------|--------------|
| read() | Very High |
| readlines() | Very High |
| List Comprehension | High |
| Generator | Very Low |
| Chunk Processing | Very Low |
| File Iteration | Very Low |

______________________________________________________________________

# Common Mistakes

## Building Huge Lists

Bad

```python
results = []

for line in file:

    results.append(process(line))
```

Memory grows

continuously.

______________________________________________________________________

## Forgetting Lazy Evaluation

Creating

lists

when

generators

would work.

______________________________________________________________________

## Using Tiny Chunks

Example

```
1 Byte
```

Too many

disk reads.

______________________________________________________________________

## Using Huge Chunks

Example

```
1 GB
```

Defeats

the purpose

of chunking.

______________________________________________________________________

# Best Practices

- Prefer generators over lists for streaming data.
- Process one record or one chunk at a time.
- Choose reasonable chunk sizes (64 KB–4 MB is common, depending on the workload).
- Build processing pipelines instead of accumulating data.
- Measure memory usage when processing large datasets.

______________________________________________________________________

# Common Interview Questions

## Why are generators memory efficient?

Generators produce values one at a time instead of creating the entire collection in memory.

______________________________________________________________________

## What is the difference between `return` and `yield`?

`return` ends the function and returns a value. `yield` pauses the function, preserves its state, and produces one value
at a time.

______________________________________________________________________

## Why are generators useful for large files?

They allow applications to process data incrementally with nearly constant memory usage, regardless of the total file
size.

______________________________________________________________________

## Why is `for line in file` memory efficient?

Because file objects are iterators. Python reads only the next line when needed instead of loading the entire file into
memory.

______________________________________________________________________

## When should you use batch processing instead of processing one record at a time?

Batch processing is useful when operations like database inserts, API calls, or disk writes have significant overhead.
Processing small batches often provides a good balance between memory usage and performance.

______________________________________________________________________

# Interview Deep Dive

## Question

How would you process a 200 GB log file without running out of memory?

### Answer

I would stream the file instead of loading it entirely into memory. For text files, I would iterate over the file line
by line using `for line in file`, or use generators to build a processing pipeline. For binary files, I would read
fixed-size chunks. This keeps memory usage nearly constant regardless of the total file size while allowing the
application to process arbitrarily large files efficiently.

______________________________________________________________________

# Summary

Memory-efficient processing

is based on one simple idea:

**Never load more data than you currently need.**

Python provides several features that make this easy:

- File Iterators
- Generators
- `yield`
- Lazy Evaluation
- Chunk Processing
- Batch Processing

These techniques form the foundation of scalable file processing systems used in production.

______________________________________________________________________

# Next

[04. Processing CSV, JSON and XML Efficiently](86-processing-csv-json-and-xml-efficiently.md)
