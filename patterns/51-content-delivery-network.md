# System Design - Part 51

# Content Delivery Network (CDN)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What a CDN is
- Why CDNs exist
- Origin Server
- Edge Servers
- Cache Hierarchy
- CDN Request Flow
- Cache-Control Headers
- Static vs Dynamic Content
- CDN vs Redis
- CDN vs Reverse Proxy
- Common interview questions

______________________________________________________________________

# Before We Start

Imagine

our **Library Management System**

is used

worldwide.

Users are located in:

- India
- USA
- Germany
- Australia
- Japan

The application

runs

only

in

India.

Question.

How long

does it take

for

a user

in

New York

to download

an image

from

a server

in Bengaluru?

Much longer

than

for

a user

inside India.

______________________________________________________________________

# The Problem

Suppose

every request

travels

to

one server.

```text id="cdn5101"
USA

↓

India
```

Even

static files

such as:

- Images
- CSS
- JavaScript
- Videos

must travel

across continents.

Problems:

❌ Higher latency

❌ Increased bandwidth

❌ Higher server load

______________________________________________________________________

# The Idea

Instead of

storing

files

in

one location,

copy them

to

servers

around

the world.

Users

download

from

the nearest server.

______________________________________________________________________

# What is a CDN?

A **Content Delivery Network (CDN)**

is a globally distributed

network

of edge servers

that caches

and delivers

content

from locations

close to users,

reducing latency

and improving performance.

______________________________________________________________________

# Architecture

```text id="cdn5102"
Origin Server

↓

CDN

↓

Edge Servers

↓

Users
```

The Origin Server

stores

the original content.

Edge Servers

store

cached copies.

______________________________________________________________________

# Origin Server

The **Origin Server**

is

the source

of truth

for

your content.

Example

```text id="cdn5103"
Application Server

↓

Images

↓

Videos

↓

CSS
```

If

an Edge Server

doesn't have

a file,

it fetches

it

from

the Origin.

______________________________________________________________________

# Edge Server

An **Edge Server**

is

a CDN server

located

near users.

Example

```text id="cdn5104"
India Edge

USA Edge

Japan Edge
```

Each Edge

stores

frequently requested

files.

______________________________________________________________________

# Request Flow

Suppose

a user

opens

your website.

```text id="cdn5105"
Browser

↓

Nearest Edge

↓

Cache Hit
```

The file

is returned

immediately.

______________________________________________________________________

# Cache Miss

Suppose

the Edge

doesn't have

the file.

```text id="cdn5106"
Browser

↓

Edge

↓

Origin Server

↓

Edge Cache

↓

Browser
```

Future requests

are served

directly

from

the Edge.

______________________________________________________________________

# Static Content

CDNs

work best

for

static content.

Examples:

- Images
- CSS
- JavaScript
- Fonts
- Videos
- PDFs

These files

change

infrequently.

______________________________________________________________________

# Dynamic Content

Can CDNs

cache

dynamic content?

Yes,

sometimes.

Examples:

- Public API responses
- Product pages
- News articles

However,

highly personalized

content

usually requires

special cache rules

or

bypasses

the CDN.

______________________________________________________________________

# Cache-Control Headers

Servers

tell

the CDN

how long

to cache

content.

Example

```http id="cdn5107"
Cache-Control:

max-age=3600
```

Meaning

cache

the response

for

one hour.

______________________________________________________________________

# Other Common Headers

```http id="cdn5108"
ETag
```

Helps

determine

whether

a file

has changed.

______________________________________________________________________

```http id="cdn5109"
Last-Modified
```

Allows browsers

and CDNs

to avoid

downloading

unchanged content.

______________________________________________________________________

# CDN Cache Invalidation

Suppose

you upload

a new logo.

The CDN

still serves

the old one.

How do you

update it?

Two common methods:

- Wait

for

TTL to expire.

- Purge

the cached object

manually.

Many CDNs

provide

cache invalidation APIs.

______________________________________________________________________

# CDN vs Redis

Interview favorite.

| CDN | Redis |
| ------------------- | ---------------------- |
| Static assets | Application data |
| Global edge servers | In-memory data store |
| Images, JS, CSS | Database query results |

Both

are caches,

but

they solve

different problems.

______________________________________________________________________

# CDN vs Browser Cache

| Browser Cache | CDN |
| ------------------------- | ------------------- |
| Inside the user's browser | Distributed network |
| Private to one user | Shared across users |

Many systems

use both

simultaneously.

______________________________________________________________________

# CDN vs Reverse Proxy

| CDN | Reverse Proxy |
| --------------------------- | ----------------------------- |
| Global network | Usually near origin |
| Optimized for edge delivery | Optimized for backend routing |
| Worldwide presence | Data-center level |

Some services,

such as Cloudflare,

combine

both capabilities.

______________________________________________________________________

# CDN + Load Balancer

A common

production architecture.

```text id="cdn5110"
Users

↓

CDN

↓

Load Balancer

↓

Application Servers
```

Static files

are served

by

the CDN.

Dynamic requests

continue

to

the backend.

______________________________________________________________________

# FastAPI Example

Suppose

your FastAPI application

serves

profile images.

Instead of

```text id="cdn5111"
/static/profile.png
```

from

your server,

store

the image

in object storage

and

serve it

through

a CDN.

Your FastAPI server

focuses

on

business logic,

not

large file transfers.

______________________________________________________________________

# Kubernetes Example

In Kubernetes,

applications

typically serve

dynamic APIs.

Static assets

are often

stored

outside

the cluster

and delivered

through

a CDN.

This reduces

traffic

to

application Pods.

______________________________________________________________________

# AI/ML Example

Suppose

your AI platform

hosts:

- Documentation
- Images
- Model downloads
- JavaScript assets

Serving

large model files

from

the application

is inefficient.

A CDN

can deliver

these files

from

edge locations,

improving

download speed

globally.

______________________________________________________________________

# Benefits

CDNs provide:

✅ Lower latency

✅ Reduced origin traffic

✅ Better scalability

✅ Lower bandwidth costs

✅ Faster page loads

______________________________________________________________________

# Additional Security Benefits

Many CDNs

also provide:

- DDoS protection
- Web Application Firewall (WAF)
- TLS termination
- Bot detection
- Rate limiting

Although

their primary role

is content delivery,

they often

serve

as

the first line

of defense

for web applications.

______________________________________________________________________

# Drawbacks

CDNs also introduce:

❌ Cache invalidation complexity

❌ Additional cost

❌ Eventual consistency

for cached content

❌ Configuration complexity

______________________________________________________________________

# Real Company Example

Video streaming platforms

deliver

movie posters,

thumbnails,

JavaScript,

and subtitles

through

a CDN.

The application servers

focus

on

authentication,

recommendations,

and streaming authorization,

while

edge servers

deliver

static assets.

______________________________________________________________________

# When NOT to Use a CDN

A CDN

may not provide

much value

for:

- Internal company tools
- Applications

used

only

within

one geographic region

- Highly personalized,

uncacheable content

______________________________________________________________________

# Best Practices

✅ Cache static assets.

✅ Use versioned filenames.

✅ Configure appropriate Cache-Control headers.

✅ Purge caches after critical updates.

______________________________________________________________________

# Common Mistakes

### Caching Sensitive Data

Never cache

private user data

unless

you fully understand

the cache scope

and

access controls.

______________________________________________________________________

### Forgetting Cache Invalidation

Deploying

a new file

doesn't automatically

remove

older cached copies.

______________________________________________________________________

### Serving Everything Through the Application

Large static files

consume

bandwidth

and

application resources.

Offload them

to

a CDN.

______________________________________________________________________

### Ignoring Browser Caching

Browser Cache

and

CDN Cache

complement

each other.

Configure

both appropriately.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is a CDN, and how does it improve application performance?

A Content Delivery Network (CDN) is a globally distributed network of edge servers that caches and delivers content from
locations close to end users. Instead of fetching static assets such as images, CSS, JavaScript, and videos from a
central origin server for every request, users receive them from the nearest edge location. This reduces latency, lowers
bandwidth consumption, decreases load on origin servers, and improves scalability. Modern CDNs also provide security
features such as DDoS protection, TLS termination, and Web Application Firewalls.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What a CDN is
- Origin Server
- Edge Servers
- Cache Hits and Misses
- Cache-Control Headers
- CDN vs Redis
- CDN vs Reverse Proxy
- FastAPI example
- AI/ML example
- Best practices

______________________________________________________________________

# 🧠 System Design Progress

You now understand three major performance building blocks:

- ✅ Load Balancers
- ✅ Caching
- ✅ CDN

These components are present in almost every large-scale web application and significantly reduce latency while
improving scalability.

______________________________________________________________________

# What's Next

[Database Replication](52-database-replication.md)
