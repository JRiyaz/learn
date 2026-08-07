# Complete HTTP Request Lifecycle Deep Dive

## 06. CDN, Edge Network and Caching

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand how CDNs work, why companies use them, what happens internally when a request reaches a CDN, how caching works, how cache invalidation happens, and what technologies are used in production.

______________________________________________________________________

# Introduction

In the previous chapter,

the browser

successfully

established

a secure

TLS connection.

Now

it wants

to send

the HTTP request.

Most engineers think

the request

goes directly

to

the backend server.

In reality,

it usually doesn't.

For companies like

- Google
- Amazon
- Netflix
- Facebook
- Microsoft

the request

usually reaches

a

CDN

first.

______________________________________________________________________

# High Level Flow

```
Browser

↓

Internet

↓

Nearest CDN Edge Server

↓

Cache Hit?

↓

Yes

↓

Return Response

OR

↓

Cache Miss

↓

Origin Server

↓

Store In Cache

↓

Return Response
```

______________________________________________________________________

# Why Do We Need A CDN?

Imagine

Google

has only

one server

in

California.

User

in India

requests

```
google.com
```

```
India

↓

California

↓

India
```

Latency

might be

250 ms

Now imagine

Google

has

servers

in

Mumbai.

```
India

↓

Mumbai

↓

India
```

Latency

may reduce

to

10 ms.

______________________________________________________________________

# What Is A CDN?

CDN stands for

```
Content Delivery Network
```

A CDN

is

a distributed network

of servers

located

around

the world.

Purpose

```
Bring

the content

closer

to users.
```

______________________________________________________________________

# CDN Providers

Interview favorite.

Popular CDNs

```
Cloudflare

Amazon CloudFront

Fastly

Akamai

Azure CDN

Google Cloud CDN
```

______________________________________________________________________

# CDN Architecture

```
                    User

                      │

                      ▼

             Nearest Edge Server

          ┌───────────┴───────────┐

          ▼                       ▼

     Cache Hit               Cache Miss

          │                       │

          ▼                       ▼

     Return Data          Origin Server

                                   │

                                   ▼

                           Cache Response

                                   │

                                   ▼

                             Return Data
```

______________________________________________________________________

# What Is An Edge Server?

Interview favorite.

Edge Server

means

a server

physically

close

to the user.

Examples

```
Mumbai

Singapore

London

New York

Tokyo
```

When you

visit

```
amazon.com
```

you don't always

connect

to

Amazon's

main datacenter.

Instead,

you connect

to

the nearest

Edge Server.

______________________________________________________________________

# What Does The Browser Actually Do?

Browser sends

```
GET /

Host: amazon.com
```

DNS

already pointed

to

CloudFront.

Browser

doesn't even know

Amazon's backend

exists.

______________________________________________________________________

# Request Flow

```
Browser

↓

CloudFront

↓

Cache?

↓

Return

OR

↓

Origin Server
```

______________________________________________________________________

# Cache Hit

Interview favorite.

Suppose

the requested file

already exists

inside

the Edge Server.

```
Browser

↓

Edge Server

↓

File Exists

↓

Return Immediately
```

Backend server

is never contacted.

______________________________________________________________________

# Cache Miss

Suppose

the file

doesn't exist.

```
Browser

↓

Edge Server

↓

Origin Server

↓

Store In Cache

↓

Return Response
```

Next request

becomes

a Cache Hit.

______________________________________________________________________

# Example

First user

requests

```
logo.png
```

```
Edge

↓

Miss

↓

Origin

↓

Store

↓

Return
```

Second user

requests

the same file.

```
Edge

↓

Hit

↓

Immediate Response
```

No origin request.

______________________________________________________________________

# What Gets Cached?

Interview favorite.

Usually

```
Images

CSS

JavaScript

Fonts

Videos

PDF

HTML

API Responses
```

depending on

configuration.

______________________________________________________________________

# What Should NOT Be Cached?

Examples

```
Bank Balance

Shopping Cart

User Profile

Admin Pages

JWT Tokens
```

Personalized data

should

usually

not

be cached.

______________________________________________________________________

# Cache-Control Header

The server

controls

caching

using

HTTP headers.

Example

```
Cache-Control:

max-age=3600
```

Meaning

```
Cache

for

1 Hour
```

______________________________________________________________________

# Cache-Control Directives

Interview favorite.

```
public
```

Anyone

may cache.

______________________________________________________________________

```
private
```

Only browser

may cache.

______________________________________________________________________

```
no-cache
```

Must revalidate.

______________________________________________________________________

```
no-store
```

Never cache.

______________________________________________________________________

```
max-age
```

Expiration time.

______________________________________________________________________

# Example

```
Cache-Control:

public,

max-age=86400
```

```
86400

Seconds

=

1 Day
```

______________________________________________________________________

# ETag

Interview favorite.

Suppose

browser

already has

```
style.css
```

Browser asks

```
Has this file

changed?
```

Instead of

downloading

the whole file,

browser sends

```
If-None-Match

"abc123"
```

Server compares

ETag.

If unchanged

```
304

Not Modified
```

Very small response.

______________________________________________________________________

# Last Modified

Alternative

to

ETag.

Browser sends

```
If-Modified-Since

Tue,

12 Aug
```

Server replies

```
304

Not Modified
```

if nothing changed.

______________________________________________________________________

# Cache Keys

Interview favorite.

CDN

needs

a cache key.

Usually

```
URL

+

Query Parameters

+

Headers
```

Example

```
/products?id=10
```

Different

from

```
/products?id=20
```

Different cache entry.

______________________________________________________________________

# CDN Request Lifecycle

```
Browser

↓

Edge Server

↓

Cache Lookup

↓

Hit?

↓

Return

↓

Miss?

↓

Origin Server

↓

Receive Response

↓

Store

↓

Return
```

______________________________________________________________________

# Origin Server

Interview favorite.

Origin

means

your

real backend.

Examples

```
FastAPI

Spring Boot

Node.js

NGINX

S3 Bucket
```

CDN

simply

proxies

requests

to

the origin.

______________________________________________________________________

# Multiple Edge Locations

Suppose

your company

has

```
Mumbai

Singapore

Tokyo

London

Virginia
```

Each location

maintains

its own

cache.

______________________________________________________________________

# CDN Cache Expiration

Eventually

cached files

expire.

```
TTL Expired

↓

Remove Cache

↓

Next Request

↓

Origin
```

______________________________________________________________________

# Cache Invalidation

Interview favorite.

Suppose

you update

```
logo.png
```

CDN

still has

the old image.

Solutions

```
TTL

Expires
```

or

```
Manual Purge
```

or

```
Versioned File
```

______________________________________________________________________

# Versioning

Best practice.

Instead of

```
style.css
```

use

```
style.v2.css
```

Browser

downloads

the new file

immediately.

______________________________________________________________________

# Compression

CDNs

often compress

responses.

Examples

```
Gzip

Brotli
```

Reduces

network bandwidth.

______________________________________________________________________

# Image Optimization

Modern CDNs

can automatically

convert

```
PNG

↓

WebP

↓

AVIF
```

Smaller images

Faster websites.

______________________________________________________________________

# Video Streaming

Large video files

are delivered

in chunks.

Example

Netflix

doesn't download

an entire movie.

Instead

```
Chunk 1

↓

Chunk 2

↓

Chunk 3
```

Adaptive streaming.

______________________________________________________________________

# Dynamic Content

Interview favorite.

Dynamic APIs

can also

be cached.

Example

```
Top News

Weather

Trending Products
```

Cache

for

30 seconds

instead of

1 hour.

______________________________________________________________________

# CDN Security

CDNs

often provide

```
HTTPS

↓

DDoS Protection

↓

Bot Detection

↓

Rate Limiting

↓

WAF
```

Many attacks

are stopped

before

they reach

your servers.

______________________________________________________________________

# What Happens Internally?

```
Incoming Request

↓

Hash URL

↓

Cache Lookup

↓

Memory

↓

SSD

↓

Hit?

↓

Return

↓

Miss?

↓

Origin Request

↓

Receive

↓

Cache

↓

Return
```

Notice

many CDNs

keep

hot data

in RAM

for

very fast access.

______________________________________________________________________

# Cache Storage

Edge servers

may store

```
RAM

↓

SSD

↓

Distributed Storage
```

Frequently accessed

objects

stay

in memory.

______________________________________________________________________

# Load Balancing Inside CDN

CDNs

also

load balance

between

their own

Edge Servers.

```
Mumbai Edge 1

↓

Busy?

↓

Mumbai Edge 2
```

______________________________________________________________________

# Common Attacks

## Cache Poisoning

Interview favorite.

Attacker

tries

to insert

malicious data

into

the CDN cache.

Future users

receive

the poisoned response.

Mitigation

- Proper cache keys
- Header validation
- Signed URLs

______________________________________________________________________

## Cache Deception

Sensitive pages

are accidentally

cached.

Another user

receives

private data.

Mitigation

Correct

Cache-Control

headers.

______________________________________________________________________

## DDoS

Millions

of requests

target

the CDN.

Instead of

your servers,

the CDN

absorbs

the attack.

______________________________________________________________________

# Technologies Used

| Component | Technologies |
|------------|--------------|
| CDN | CloudFront, Cloudflare, Akamai, Fastly |
| Compression | Gzip, Brotli |
| Image Formats | WebP, AVIF |
| Cache Validation | ETag, Last-Modified |
| Storage | RAM, SSD |
| Streaming | HLS, MPEG-DASH |

______________________________________________________________________

# Common Interview Questions

## Why use a CDN?

A CDN reduces latency by serving content from edge locations closer to users. It also reduces origin server load,
improves availability, and provides security features such as DDoS protection.

______________________________________________________________________

## What is the difference between a Cache Hit and a Cache Miss?

A cache hit occurs when the requested content is already available in the CDN cache and is returned immediately. A cache
miss requires the CDN to fetch the content from the origin server before caching and returning it.

______________________________________________________________________

## What is an Origin Server?

The origin server is the actual backend server or storage system that owns the original content. The CDN retrieves data
from the origin whenever it experiences a cache miss.

______________________________________________________________________

## Why use ETag instead of downloading the file again?

ETags allow the browser to ask whether a resource has changed. If not, the server responds with **304 Not Modified**,
avoiding unnecessary data transfer.

______________________________________________________________________

## Why shouldn't user-specific pages be cached?

Caching personalized content such as account information or shopping carts could expose one user's private data to
another user. Such responses should typically use `Cache-Control: private` or `no-store`.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through what happens when a request reaches a CDN.

### Answer

The CDN edge server receives the request and generates a cache key. It checks whether the requested resource exists in
its local cache. If a valid cached copy exists, it returns the response immediately (cache hit). Otherwise, it forwards
the request to the origin server, receives the response, stores it according to cache rules, and returns it to the
client (cache miss).

______________________________________________________________________

# Summary

CDNs significantly improve performance by serving content from edge locations close to users.

Key concepts include

- Edge Servers
- Origin Servers
- Cache Hit
- Cache Miss
- Cache-Control
- ETag
- Last-Modified
- Cache Invalidation
- Versioning
- Compression
- DDoS Protection
- Cache Poisoning

In production systems, many requests are fully handled by the CDN and **never reach your backend**.

For requests that cannot be served from the CDN, the next component is typically a **Web Application Firewall (WAF)**,
which inspects and filters incoming traffic before it reaches your infrastructure.

______________________________________________________________________

# Next

[07. Web Application Firewall (WAF)](07-web-application-firewall-waf.md)
