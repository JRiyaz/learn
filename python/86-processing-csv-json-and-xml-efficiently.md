# Python Large File Processing

## 04. Processing CSV, JSON and XML Efficiently

> Target Audience: Python Backend Engineers (Intermediate → Senior)
>
> Goal: Learn how to efficiently process structured data formats like CSV, JSON, NDJSON, and XML without loading the entire file into memory. Understand the common mistakes developers make and the techniques used in production systems.

______________________________________________________________________

# Introduction

Most backend applications

don't process

plain text files.

Instead,

they deal with

structured formats

like

- CSV
- JSON
- NDJSON
- XML

Some of these formats

are naturally

streaming-friendly,

while others

are not.

Choosing

the wrong approach

can easily

consume

gigabytes

of RAM.

______________________________________________________________________

# File Formats

| Format | Streaming Friendly | Typical Use |
|---------|-------------------|-------------|
| CSV | ✅ Yes | Reports, ETL, Analytics |
| NDJSON | ✅ Yes | Logs, APIs |
| JSON Array | ❌ Difficult | API Responses |
| XML | ✅ Yes | Enterprise Systems |

______________________________________________________________________

# CSV Processing

CSV

is one of

the easiest formats

to process efficiently.

Example

```csv
id,name,age

1,Riyaz,25

2,Alice,30

3,Bob,27
```

______________________________________________________________________

# Wrong Approach

Many developers use

```python
data = file.read()
```

or

```python
lines = file.readlines()
```

Both

load

the complete file

into memory.

______________________________________________________________________

# Better Approach

Python provides

the

```
csv
```

module.

Example

```python
import csv

with open("users.csv") as file:

    reader = csv.reader(file)

    for row in reader:

        process(row)
```

Memory usage

remains

constant.

______________________________________________________________________

# csv.DictReader

Instead of

lists,

you can get

dictionaries.

Example

```python
import csv

with open("users.csv") as file:

    reader = csv.DictReader(file)

    for row in reader:

        print(row["name"])
```

Output

```python
{
    "id":"1",

    "name":"Riyaz",

    "age":"25"
}
```

______________________________________________________________________

# Why DictReader?

Advantages

- Readable
- Easy column access
- Less error-prone

______________________________________________________________________

# Processing Huge CSV Files

Example

```
100 GB CSV

↓

Read Row

↓

Validate

↓

Insert Database

↓

Next Row
```

Never

store

all rows

inside

a list.

______________________________________________________________________

# Batch Inserts

Instead of

```
Insert

↓

Insert

↓

Insert
```

Use

```
1000 Rows

↓

Single Insert
```

Benefits

- Faster
- Fewer database calls
- Lower network overhead

______________________________________________________________________

# JSON Processing

Interview favorite.

JSON

comes in

two common forms.

______________________________________________________________________

## JSON Object

Example

```json
{
    "name":"Riyaz"
}
```

Small.

Easy to process.

______________________________________________________________________

## JSON Array

Example

```json
[
    {...},
    {...},
    {...}
]
```

Problem

```
Large Array

↓

Must Parse

Entire Document
```

This

can consume

huge amounts

of memory.

______________________________________________________________________

# Why Large JSON Arrays Are Difficult

Suppose

the file contains

```
10 Million Objects
```

The parser

cannot process

only

the first object.

It must understand

the complete

JSON structure.

______________________________________________________________________

# Bad Example

```python
import json

with open("users.json") as file:

    data = json.load(file)
```

```
Entire JSON

↓

RAM
```

Bad

for

large files.

______________________________________________________________________

# Better Alternative

Use

```
NDJSON
```

instead.

______________________________________________________________________

# What is NDJSON?

Interview favorite.

NDJSON means

```
Newline Delimited JSON
```

Example

```json
{"id":1,"name":"Riyaz"}

{"id":2,"name":"Alice"}

{"id":3,"name":"Bob"}
```

Each line

is

an independent

JSON object.

______________________________________________________________________

# Why NDJSON?

Now

we can process

one object

at a time.

```
Read Line

↓

Parse JSON

↓

Process

↓

Next Line
```

Perfect

for

large datasets.

______________________________________________________________________

# NDJSON Example

```python
import json

with open("users.ndjson") as file:

    for line in file:

        user = json.loads(line)

        process(user)
```

Memory

stays low.

______________________________________________________________________

# Streaming JSON

Sometimes

you cannot

change

the format.

You receive

a huge

JSON array.

In that case,

use

streaming parsers.

Popular libraries

- ijson
- simdjson (Python bindings)

These libraries

parse

JSON

incrementally.

______________________________________________________________________

# XML Processing

Interview favorite.

Many enterprises

still use

XML.

Examples

- Banking
- Insurance
- Government
- SOAP APIs

______________________________________________________________________

# Wrong Approach

```python
tree = ET.parse("users.xml")
```

Loads

entire XML

into memory.

______________________________________________________________________

# Better Approach

Use

```
iterparse()
```

Example

```python
import xml.etree.ElementTree as ET

for event, element in ET.iterparse("users.xml"):

    process(element)
```

Processes

XML

incrementally.

______________________________________________________________________

# Memory Cleanup

While using

```
iterparse()
```

remember

to clear

processed elements.

Example

```python
element.clear()
```

Otherwise

memory usage

continues growing.

______________________________________________________________________

# Processing Compressed CSV

Example

```
users.csv.gz
```

Instead of

extracting

the entire file,

stream it.

```python
import gzip

with gzip.open(
    "users.csv.gz",
    "rt"
) as file:

    for line in file:

        process(line)
```

______________________________________________________________________

# Streaming API Responses

Suppose

an API

returns

millions

of records.

Instead of

building

one huge JSON,

many APIs

stream data.

Example

```
Client

↓

Record

↓

Record

↓

Record
```

Memory

stays low

on both sides.

______________________________________________________________________

# Real Production Example

Suppose

Amazon

exports

orders.

Instead of

```
orders.json
```

they may produce

```
orders.ndjson
```

Each worker

can process

records

independently.

______________________________________________________________________

# Which Format Should You Choose?

| Format | Large Data |
|---------|------------|
| CSV | ✅ Excellent |
| NDJSON | ✅ Excellent |
| JSON Array | ❌ Poor |
| XML iterparse | ✅ Good |

______________________________________________________________________

# Common Mistakes

## Using json.load()

For

very large files.

______________________________________________________________________

## Loading Entire CSV

Avoid

```python
list(reader)
```

on

huge datasets.

______________________________________________________________________

## Forgetting element.clear()

When parsing XML.

Causes

memory leaks.

______________________________________________________________________

## Using JSON Arrays for Huge Datasets

Prefer

NDJSON

for streaming.

______________________________________________________________________

# Best Practices

- Stream CSV files row by row.
- Prefer `csv.DictReader` when readability matters.
- Use NDJSON for large JSON datasets.
- Use streaming JSON parsers when handling massive JSON arrays.
- Use `iterparse()` for XML.
- Process data in batches when inserting into databases.

______________________________________________________________________

# Performance Comparison

| Format | Memory Usage | Streaming Support |
|----------|--------------|-------------------|
| CSV | Very Low | Excellent |
| NDJSON | Very Low | Excellent |
| JSON Array | Very High | Poor |
| XML + iterparse | Low | Good |

______________________________________________________________________

# Common Interview Questions

## Why is CSV easier to process than JSON?

CSV is naturally row-based, allowing records to be processed one at a time. Large JSON arrays typically require parsing
much more of the document before individual objects are available.

______________________________________________________________________

## What is NDJSON?

NDJSON (Newline Delimited JSON) stores one JSON object per line, making it ideal for streaming and processing large
datasets incrementally.

______________________________________________________________________

## Why use `csv.DictReader` instead of `csv.reader`?

`DictReader` maps column names to values, making the code easier to read and less dependent on column positions.

______________________________________________________________________

## Why should `element.clear()` be called during XML parsing?

It releases memory for elements that have already been processed, preventing memory usage from continuously increasing.

______________________________________________________________________

## When would you use a streaming JSON parser?

When you must process very large JSON documents that cannot fit comfortably into memory and the data format cannot be
changed to NDJSON.

______________________________________________________________________

# Interview Deep Dive

## Question

You receive a 50 GB file containing customer records. Which format would you prefer and why?

### Answer

If I have control over the format, I would choose NDJSON or CSV because both support streaming and can be processed one
record at a time with constant memory usage. If the input is a large JSON array, I would use a streaming JSON parser
such as `ijson` rather than `json.load()`. For XML, I would use `iterparse()` and clear processed elements to keep
memory usage low.

______________________________________________________________________

# Summary

Structured data formats

require different

processing strategies.

For large datasets,

prefer formats

that support

streaming.

Key takeaways

- CSV is naturally streaming-friendly.
- NDJSON is preferred over massive JSON arrays.
- Use streaming parsers for large JSON documents.
- Parse XML incrementally with `iterparse()`.
- Never load massive structured files entirely into memory unless you know they comfortably fit in available RAM.

______________________________________________________________________

# Next

[05. Parallel and Concurrent Large File Processing](87-parallel-and-concurrent-large-file-processing.md)
