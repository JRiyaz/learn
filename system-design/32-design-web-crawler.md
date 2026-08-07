# System Design – Web Crawler

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how large-scale web crawlers like Google Search, Bing, or Common Crawl discover, fetch, parse, and index billions of web pages while respecting web standards and scaling efficiently.

______________________________________________________________________

# Introduction

Every search engine

starts with

one problem.

```
How do we

discover

billions

of web pages?
```

The answer is

```
Web Crawler
```

A Web Crawler

continuously

visits web pages,

extracts links,

discovers new pages,

and sends data

to the indexing system.

______________________________________________________________________

# What Is A Web Crawler?

A Web Crawler

is a program

that automatically

visits web pages.

Its responsibilities

include

- Discover pages
- Download content
- Extract links
- Follow links
- Avoid duplicates
- Respect crawling rules

______________________________________________________________________

# Functional Requirements

Assume

our crawler

supports

- Crawl billions of pages
- Discover new URLs
- Revisit updated pages
- Avoid duplicate crawling
- Respect robots.txt
- Handle failures
- Scale horizontally

______________________________________________________________________

# Non-Functional Requirements

Need

- High Throughput
- Fault Tolerance
- Horizontal Scalability
- Politeness
- Reliability
- Low Duplicate Crawling

______________________________________________________________________

# Step 1

# High-Level Architecture

```
                 Seed URLs
                     │
                     ▼
               URL Frontier
                     │
                     ▼
              Crawl Scheduler
                     │
                     ▼
              Fetcher Workers
                     │
                     ▼
               HTML Parser
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     Link Extractor        Content Storage
          │
          ▼
     Duplicate Filter
          │
          ▼
      URL Frontier
```

______________________________________________________________________

# Core Components

The crawler

consists of

multiple services.

- URL Frontier
- Scheduler
- Fetcher
- HTML Parser
- Link Extractor
- Duplicate Detector
- Content Storage
- Metadata Database

______________________________________________________________________

# Step 2

# Seed URLs

Every crawler

starts

with

a small list.

Example

```
https://google.com

https://wikipedia.org

https://github.com
```

These are called

```
Seed URLs
```

______________________________________________________________________

# URL Frontier

Interview favorite.

The URL Frontier

stores

all URLs

waiting

to be crawled.

Think of it as

```
Queue

↓

Pending URLs
```

______________________________________________________________________

# Why A Queue?

URLs

must be processed

one at

a time

or

in batches.

```
URL

↓

Fetch

↓

Parse

↓

More URLs
```

______________________________________________________________________

# Step 3

# Crawl Scheduler

The scheduler

decides

which URL

to crawl

next.

Responsibilities

include

- Priority
- Retry
- Delay
- Domain fairness
- Crawl frequency

______________________________________________________________________

# Example

Priority Queue

```
High Priority

↓

News Websites
```

```
Medium

↓

Blogs
```

```
Low

↓

Archived Pages
```

______________________________________________________________________

# Step 4

# Fetcher

Fetcher

downloads

web pages.

```
URL

↓

HTTP Request

↓

HTML
```

Usually

many fetchers

work

in parallel.

______________________________________________________________________

# Parallel Crawling

Example

```
Worker 1

↓

google.com
```

```
Worker 2

↓

github.com
```

```
Worker 3

↓

wikipedia.org
```

Thousands

of workers

may operate

simultaneously.

______________________________________________________________________

# Step 5

# robots.txt

Interview favorite.

Before

crawling

a website,

check

```
robots.txt
```

Example

```
Disallow:

/admin
```

Crawler

must

respect

these rules.

______________________________________________________________________

# Crawl Delay

Some websites

request

a delay.

Example

```
Crawl-delay

10 seconds
```

Avoid

overloading

websites.

______________________________________________________________________

# Step 6

# HTML Parsing

After

downloading

the page

```
HTML

↓

Parser

↓

DOM
```

Extract

useful information.

______________________________________________________________________

# Link Extraction

Example

```
<a href="page2.html">
```

Extract

```
page2.html
```

Add

to

URL Frontier.

______________________________________________________________________

# Step 7

# Duplicate Detection

Interview favorite.

Suppose

multiple pages

link

to

```
example.com/page1
```

Should

we crawl

it

multiple times?

No.

Need

duplicate detection.

______________________________________________________________________

# URL Deduplication

Maintain

a set

of

already discovered

URLs.

```
URL Exists?

↓

Yes

↓

Ignore
```

______________________________________________________________________

# Content Deduplication

Different URLs

may contain

identical content.

Example

```
page?id=10
```

```
page?id=11
```

Same HTML.

Store

only

one copy.

______________________________________________________________________

# Hashing

Interview favorite.

Generate

a hash

of

page content.

Example

```
SHA-256

↓

Hash
```

If

hash

already exists,

skip storing

duplicate content.

______________________________________________________________________

# Step 8

# URL Normalization

Different URLs

may point

to

the same page.

Example

```
example.com
```

```
example.com/
```

```
https://example.com
```

Normalize

before

storing.

______________________________________________________________________

# Step 9

# Storage

Store

- HTML
- Metadata
- Headers
- Crawl time
- Status code

______________________________________________________________________

# Metadata

Example

```
URL

↓

Last Crawled

↓

HTTP Status

↓

Content Hash
```

Useful

for

future crawling.

______________________________________________________________________

# Step 10

# Recrawling

Interview favorite.

Pages

change

over time.

Need

periodic recrawling.

Examples

News

↓

Frequently

Wikipedia

↓

Moderately

Archived pages

↓

Rarely

______________________________________________________________________

# Freshness

Scheduler

assigns

crawl frequency

based on

how often

pages change.

______________________________________________________________________

# Step 11

# Distributed Crawling

One crawler

isn't enough.

```
Scheduler

↓

Worker A

Worker B

Worker C

Worker D
```

Scale

horizontally.

______________________________________________________________________

# URL Partitioning

Distribute

URLs

using

```
Hash(URL)
```

or

```
Domain
```

Each worker

owns

a subset

of URLs.

______________________________________________________________________

# Step 12

# Failure Handling

Suppose

website

returns

```
500
```

Retry later.

Suppose

```
404
```

Remove

from

future crawling,

unless

business requirements

suggest otherwise.

______________________________________________________________________

# Retry Strategy

Use

```
Exponential Backoff
```

Example

```
1 min

↓

5 min

↓

30 min
```

______________________________________________________________________

# Step 13

# Rate Limiting

Don't

overload

websites.

Limit

requests

per domain.

Example

```
2 Requests/sec
```

______________________________________________________________________

# Monitoring

Monitor

- URLs crawled/sec
- Failed requests
- Retry count
- Duplicate URLs
- Queue size
- Crawl latency

______________________________________________________________________

# Failure Scenarios

## Worker Crash

Another worker

continues

processing

remaining URLs.

______________________________________________________________________

## Queue Failure

Persist

URL Frontier

to avoid

losing URLs.

______________________________________________________________________

## Duplicate Crawl

Deduplication

prevents

wasted work.

______________________________________________________________________

## Network Failure

Retry

later

using

backoff.

______________________________________________________________________

# Typical Architecture

```
                  Seed URLs
                       │
                       ▼
                 URL Frontier
                       │
                       ▼
                 Crawl Scheduler
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Fetcher A    Fetcher B    Fetcher C
          │            │            │
          ▼            ▼            ▼
      HTML Parser  HTML Parser HTML Parser
          │            │            │
          └────────────┼────────────┘
                       ▼
               Link Extractor
                       │
                       ▼
              Duplicate Filter
                       │
                       ▼
                  URL Frontier
                       │
                       ▼
                 Content Storage
```

______________________________________________________________________

# Common Interview Questions

## Why use a URL Frontier?

The URL Frontier stores URLs waiting to be crawled and enables prioritization, retries, scheduling, and distributed
processing.

______________________________________________________________________

## Why respect robots.txt?

robots.txt communicates crawling preferences from website owners. Respecting it helps avoid crawling restricted paths
and reduces unnecessary load.

______________________________________________________________________

## Why detect duplicate URLs?

Without deduplication, the crawler would repeatedly fetch the same pages, wasting bandwidth, storage, and processing
resources.

______________________________________________________________________

## Why crawl pages again?

Web pages change over time. Periodic recrawling keeps the search index fresh and up to date.

______________________________________________________________________

## Why partition URLs?

Partitioning distributes work across multiple crawler workers, allowing horizontal scaling and reducing bottlenecks.

______________________________________________________________________

# Common Interview Mistakes

## Ignoring robots.txt

Professional crawlers

must respect

website rules.

______________________________________________________________________

## No Duplicate Detection

Results

in

wasted bandwidth

and storage.

______________________________________________________________________

## Crawling Too Fast

May overload

target websites.

Always

rate limit

per domain.

______________________________________________________________________

## Keeping Everything In Memory

Persist

important state

such as

URL Frontier

and crawl metadata.

______________________________________________________________________

## No Retry Strategy

Temporary failures

should not

permanently

remove pages.

______________________________________________________________________

# Best Practices

✅ Respect robots.txt.

✅ Use a URL Frontier.

✅ Crawl in parallel.

✅ Detect duplicate URLs and content.

✅ Rate limit per domain.

✅ Schedule intelligent recrawling.

✅ Monitor crawl health continuously.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is the URL Frontier important?

### Answer

The URL Frontier is the central queue of pending URLs. It enables prioritization, retry handling, distributed crawling,
and ensures URLs are processed efficiently without duplication.

______________________________________________________________________

## Question

How do you avoid crawling the same page repeatedly?

### Answer

Maintain a record of previously discovered URLs and normalize them before insertion. Additionally, hash page content to
detect duplicate pages served under different URLs.

______________________________________________________________________

## Question

How would you scale a Web Crawler to billions of pages?

### Answer

Distribute URLs across multiple crawler workers, partition work using hashing or domains, use a distributed URL
Frontier, apply per-domain rate limiting, detect duplicates, and schedule periodic recrawling based on page freshness.

______________________________________________________________________

# Practice Exercise

Design

a Web Crawler

for

Google Search.

Explain

1. URL Frontier
1. Crawl Scheduler
1. Parallel workers
1. robots.txt handling
1. Duplicate detection
1. Content storage
1. URL partitioning
1. Retry strategy
1. Monitoring
1. Failure recovery
1. Freshness strategy
1. Trade-offs

Present

your complete solution

within

45 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

A Web Crawler is the foundation of every large-scale search engine.

A strong design should demonstrate

- URL Frontier
- Scheduling
- Parallel fetching
- HTML parsing
- Link extraction
- Duplicate detection
- Distributed architecture
- Rate limiting
- Freshness management
- Monitoring
- Fault tolerance

Mastering the Web Crawler prepares you for interviews involving search engines, indexing systems, data pipelines, and
other large-scale distributed architectures.

______________________________________________________________________

# Next

[System Design Interview Framework](33-system-design-interview-framework.md)
