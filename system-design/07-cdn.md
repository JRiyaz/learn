# CDN (Content Delivery Network)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how CDNs work, why they are essential for modern applications, and how to explain them confidently in System Design interviews.

______________________________________________________________________

# Introduction

Imagine

your application

is hosted in

```
Mumbai
```

A user

from

Germany

opens your website.

The request

travels

thousands of kilometers.

```
Germany

↓

Internet

↓

Mumbai Server

↓

Germany
```

Even if

your server

is extremely fast,

network latency

makes the application

feel slow.

How do companies like

Netflix,

YouTube,

Amazon,

and Instagram

solve this?

The answer is

```
CDN
```

______________________________________________________________________

# What Is A CDN?

CDN stands for

```
Content Delivery Network
```

A CDN

is a globally distributed network

of servers

that stores

copies

of your content

closer to users.

Instead of

```
Germany

↓

India
```

the request becomes

```
Germany

↓

Frankfurt CDN

↓

Response
```

Much faster.

______________________________________________________________________

# Why Do We Need A CDN?

Without CDN

```
User

↓

Origin Server

↓

Long Distance

↓

High Latency
```

With CDN

```
User

↓

Nearby CDN

↓

Low Latency
```

Benefits

- Lower latency
- Faster page loads
- Reduced bandwidth
- Lower origin server load
- Better availability
- Global scalability

______________________________________________________________________

# Real-World Example

Imagine

a popular bookstore

exists only

in Mumbai.

Every customer

from every country

must travel

to Mumbai.

Impossible.

Instead,

the bookstore

opens

small branches

around the world.

Customers

visit

their nearest branch.

That's exactly

how a CDN works.

______________________________________________________________________

# Basic Architecture

```
                Users
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 India User   Germany User   USA User
      │           │            │
      ▼           ▼            ▼
 Mumbai CDN  Frankfurt CDN  Virginia CDN
       \          |          /
        \         |         /
         └────────▼────────┘
            Origin Server
```

______________________________________________________________________

# Origin Server

The

Origin Server

contains

the original content.

Example

```
Application

↓

AWS S3

↓

Nginx

↓

Application Server
```

The CDN

does not create content.

It copies

content

from

the origin.

______________________________________________________________________

# Edge Server

Each CDN location

is called

an

```
Edge Server
```

or

```
Edge Location
```

Users

connect

to

the nearest

edge.

______________________________________________________________________

# Cache Hit

Suppose

an image

already exists

inside

the CDN.

```
User

↓

CDN

↓

Image Found

↓

Response
```

This is called

```
Cache Hit
```

Fast.

No request

reaches

the origin server.

______________________________________________________________________

# Cache Miss

Suppose

the CDN

doesn't have

the image.

```
User

↓

CDN

↓

Origin Server

↓

Image

↓

Store In CDN

↓

Response
```

This is called

```
Cache Miss
```

Future requests

become

cache hits.

______________________________________________________________________

# Cache Hit Ratio

One important metric

is

```
Cache Hit Ratio
```

Formula

```
Cache Hits

÷

Total Requests
```

Example

```
95%

Cache Hit
```

Excellent.

Only

5%

reach

the origin.

______________________________________________________________________

# Static Content

CDNs

work best

for

static files.

Examples

- Images
- CSS
- JavaScript
- Fonts
- PDFs
- Videos
- Audio

These files

rarely change.

______________________________________________________________________

# Dynamic Content

Dynamic content

changes

per user.

Examples

- Shopping cart
- Dashboard
- Bank balance
- User profile

Traditionally,

dynamic content

is served

by

the application.

Modern CDNs

can accelerate

certain dynamic requests,

but

they are still

most effective

for static assets.

______________________________________________________________________

# CDN Request Flow

```
Browser

↓

DNS

↓

Nearest CDN

↓

Cache Hit?

↓

Yes

↓

Return File
```

OR

```
Browser

↓

DNS

↓

Nearest CDN

↓

Cache Miss

↓

Origin Server

↓

Store Copy

↓

Return File
```

______________________________________________________________________

# TTL

Just like DNS,

CDNs

also use

TTL.

Example

```
Image

TTL

24 Hours
```

The CDN

keeps

the file

for

24 hours.

After TTL expires,

it requests

a fresh copy

from

the origin.

______________________________________________________________________

# Cache Invalidation

Suppose

you replace

```
logo.png
```

The CDN

still serves

the old version.

Problem.

Solutions

- Cache invalidation
- Cache purge
- Versioned filenames

Example

Instead of

```
logo.png
```

use

```
logo-v2.png
```

Very common.

______________________________________________________________________

# CDN And Images

Instagram

stores

images

inside

Object Storage.

Example

AWS S3.

Users

never

download

directly

from S3.

Instead

```
User

↓

CDN

↓

S3
```

Much faster.

______________________________________________________________________

# CDN And Videos

Netflix

cannot stream

every movie

from

one server.

Instead

popular videos

are cached

at edge locations

around the world.

This dramatically reduces

latency

and

backbone traffic.

______________________________________________________________________

# CDN And JavaScript

When you visit

a website,

files like

```
app.js

styles.css

logo.png
```

are excellent

CDN candidates.

______________________________________________________________________

# CDN And APIs

Generally

```
GET

↓

Cacheable
```

```
POST

↓

Not Cacheable
```

However,

public APIs

with infrequently changing data

can also benefit

from CDN caching.

______________________________________________________________________

# Geographic Routing

DNS

helps users

reach

the nearest

CDN edge.

Example

```
India User

↓

Mumbai Edge
```

```
Germany User

↓

Frankfurt Edge
```

```
USA User

↓

Virginia Edge
```

______________________________________________________________________

# Benefits For Origin Server

Without CDN

```
1 Million Requests

↓

Origin Server
```

With

95% Cache Hit

```
1 Million Requests

↓

50,000 Requests

↓

Origin
```

Huge reduction.

______________________________________________________________________

# CDN And Security

Modern CDNs

also provide

- DDoS protection
- Rate limiting
- WAF (Web Application Firewall)
- Bot protection
- HTTPS termination

Example

Cloudflare

combines

CDN

and

security services.

______________________________________________________________________

# Popular CDN Providers

Examples

- Amazon CloudFront
- Cloudflare
- Akamai
- Fastly
- Google Cloud CDN
- Azure CDN

Interviewers

care more

about concepts

than providers.

______________________________________________________________________

# CDN vs Load Balancer

Many candidates

confuse them.

CDN

```
Caches Content

↓

Closer To Users
```

Load Balancer

```
Distributes Requests

↓

Across Servers
```

Different purposes.

______________________________________________________________________

# CDN vs Cache

Cache

is a broad concept.

Redis

is a cache.

Browser cache

is a cache.

CDN

is

a geographically distributed

cache.

______________________________________________________________________

# When Should You Use A CDN?

Good candidates

- Images
- CSS
- JavaScript
- Videos
- Downloads
- Static websites
- Public assets

Avoid caching

- Bank balances
- User-specific data
- Frequently changing private information

unless appropriate cache controls exist.

______________________________________________________________________

# Typical System Design

```
User

↓

DNS

↓

CDN

↓

Load Balancer

↓

Application Servers

↓

Redis

↓

Database

↓

Object Storage
```

Notice

the CDN

comes before

the application.

______________________________________________________________________

# Common Interview Questions

## Why not serve images directly from the application server?

Because

application servers

should focus

on business logic.

Static content

is better served

through a CDN,

reducing bandwidth

and

CPU usage.

______________________________________________________________________

## What happens on a cache miss?

The CDN

retrieves

the content

from

the origin server,

stores a copy,

and returns it

to the user.

______________________________________________________________________

## Why doesn't a CDN cache everything?

Some content

is user-specific

or changes frequently.

Serving stale

or incorrect data

could create

functional or security issues.

______________________________________________________________________

## Does a CDN replace Redis?

No.

Redis

accelerates

backend data access.

A CDN

accelerates

content delivery

to end users.

Different layers.

______________________________________________________________________

# Common Mistakes

## Using CDN For Private Data

Be careful.

Sensitive,

user-specific responses

usually shouldn't be cached publicly.

______________________________________________________________________

## Forgetting Cache Invalidation

One of the hardest problems

is ensuring users receive

updated content

when files change.

______________________________________________________________________

## Thinking CDN Stores Original Data

The origin server

remains

the source of truth.

______________________________________________________________________

## Assuming Every Request Reaches Origin

A successful CDN

serves

most requests

directly

from edge locations.

______________________________________________________________________

# Best Practices

✅ Cache static assets aggressively.

✅ Use versioned filenames for static resources.

✅ Configure appropriate TTL values.

✅ Keep origin servers lightweight.

✅ Monitor cache hit ratio.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the primary purpose of a CDN?

### Answer

A CDN reduces latency by serving cached content from edge servers located close to users. It also reduces origin server
load, improves scalability, and enhances availability.

______________________________________________________________________

## Question

What is the difference between a Cache Hit and a Cache Miss?

### Answer

A **Cache Hit** occurs when the requested content is already available at the CDN edge server. A **Cache Miss** occurs
when the content isn't available, so the CDN retrieves it from the origin server, caches it, and returns it to the
client.

______________________________________________________________________

## Question

Should dynamic API responses always be cached?

### Answer

No. Dynamic responses often contain user-specific or rapidly changing data. Caching should only be used when the
response is safe to reuse and appropriate cache-control policies are in place.

______________________________________________________________________

# Practice Exercise

For each application,

identify

1. Which content should be cached?
1. Which content should never be cached?
1. Appropriate TTL values.
1. Whether cache invalidation is required.
1. Expected cache hit ratio.

Applications

- YouTube
- Instagram
- Netflix
- Banking App
- E-commerce Platform
- Online Learning Platform

______________________________________________________________________

# Summary

A CDN is a globally distributed cache that brings content closer to users.

It

- Reduces latency
- Improves scalability
- Decreases origin server load
- Delivers static content efficiently
- Works closely with DNS and Load Balancers

Understanding where a CDN fits in the request path—and what it should and shouldn't cache—is a key System Design
interview skill.

______________________________________________________________________

# Next

[Caching Fundamentals](08-caching-fundamentals.md)
