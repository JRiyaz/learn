# DNS (Domain Name System)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand how DNS works, why it is essential, and how it fits into modern distributed systems and System Design interviews.

______________________________________________________________________

# Introduction

Imagine

you want to visit

```
https://www.google.com
```

Your browser

doesn't actually

communicate using

```
google.com
```

Computers communicate

using

IP addresses.

Example

```
142.250.183.46
```

So,

how does

```
google.com
```

become

```
142.250.183.46
```

The answer is

```
DNS
```

______________________________________________________________________

# What Is DNS?

DNS

stands for

```
Domain Name System
```

It is

the Internet's

phone book.

Just as

your phone

maps

```
Mom

↓

+91XXXXXXXXXX
```

DNS maps

```
google.com

↓

142.250.xxx.xxx
```

Humans

remember names.

Computers

use IP addresses.

______________________________________________________________________

# Why Do We Need DNS?

Imagine

remembering

IP addresses

for every website.

```
Google

142.250.xxx.xxx

Amazon

52.xxx.xxx.xxx

GitHub

140.xxx.xxx.xxx
```

Impossible.

DNS solves

this problem.

______________________________________________________________________

# The Complete Flow

When you enter

```
www.example.com
```

your request

looks like

```
Browser

↓

Operating System Cache

↓

Browser Cache

↓

Local DNS Resolver

↓

Root DNS

↓

TLD DNS

↓

Authoritative DNS

↓

IP Address

↓

Browser Connects
```

Let's understand

every step.

______________________________________________________________________

# Step 1

## Browser Cache

Suppose

you visited

Google

30 seconds ago.

Your browser

already knows

its IP.

```
Browser

↓

Cache Hit

↓

Done
```

No network request

needed.

Fast.

______________________________________________________________________

# Step 2

## Operating System Cache

If the browser

doesn't know,

it asks

the operating system.

```
Chrome

↓

macOS / Windows

↓

DNS Cache
```

Again,

if found,

done.

______________________________________________________________________

# Step 3

## Local DNS Resolver

Still not found.

The request goes to

your ISP

or

public DNS.

Examples

- Google DNS (8.8.8.8)
- Cloudflare DNS (1.1.1.1)

This resolver

performs

the lookup.

______________________________________________________________________

# Step 4

## Root DNS Server

The resolver

asks

Root DNS

```
Where is

.com?
```

Root server

doesn't know

the IP.

It knows

who manages

```
.com
```

It replies

```
Ask

.com

TLD Server
```

______________________________________________________________________

# Step 5

## TLD Server

TLD

means

Top Level Domain.

Examples

```
.com

.org

.net

.io

.dev
```

The resolver asks

```
Where is

google.com?
```

The TLD server

responds

```
Ask

Google's

Authoritative DNS
```

______________________________________________________________________

# Step 6

## Authoritative DNS Server

This server

owns

the domain.

It replies

```
google.com

↓

142.250.xxx.xxx
```

Now

the resolver

knows

the answer.

______________________________________________________________________

# Step 7

## Cache Everything

The resolver

stores

the answer.

Browser

stores

the answer.

Operating system

stores

the answer.

Next lookup

becomes

much faster.

______________________________________________________________________

# Visual Flow

```
User

↓

Browser Cache

↓

OS Cache

↓

DNS Resolver

↓

Root DNS

↓

TLD DNS

↓

Authoritative DNS

↓

IP Address

↓

Server
```

Memorize

this diagram.

Interviewers

love asking it.

______________________________________________________________________

# What Is TTL?

TTL

means

```
Time To Live
```

Example

```
TTL

300 Seconds
```

DNS response

can be cached

for

5 minutes.

After TTL expires,

DNS lookup

happens again.

______________________________________________________________________

# Why Use TTL?

Without TTL

every request

would contact

Root DNS.

The Internet

would become

extremely slow.

Caching

reduces

billions

of requests.

______________________________________________________________________

# DNS Record Types

Different records

serve

different purposes.

______________________________________________________________________

# A Record

Maps

Domain

↓

IPv4

Example

```
google.com

↓

142.250.xxx.xxx
```

Most common.

______________________________________________________________________

# AAAA Record

Maps

Domain

↓

IPv6

Example

```
google.com

↓

2404:6800:4007::200e
```

______________________________________________________________________

# CNAME Record

Alias

for another domain.

Example

```
www.example.com

↓

example.com
```

Useful

for multiple subdomains.

______________________________________________________________________

# MX Record

Mail Exchange.

Tells

email servers

where to send

emails.

Example

```
gmail.com

↓

Mail Server
```

______________________________________________________________________

# TXT Record

Stores

text information.

Commonly used

for

- Domain verification
- SPF
- DKIM
- DMARC

Email security

depends heavily

on TXT records.

______________________________________________________________________

# NS Record

Specifies

which DNS servers

are authoritative

for the domain.

______________________________________________________________________

# Reverse DNS

Normally

DNS maps

```
Name

↓

IP
```

Reverse DNS

maps

```
IP

↓

Domain
```

Useful

for

email servers

and diagnostics.

______________________________________________________________________

# Recursive Resolver

The resolver

does all

the work

for the client.

Instead of

your browser

contacting

Root,

TLD,

and

Authoritative servers,

the resolver

handles everything.

Your browser

asks

only one server.

______________________________________________________________________

# DNS Caching

Caching exists

at multiple levels.

```
Browser

↓

Operating System

↓

Router

↓

ISP

↓

Public Resolver
```

This is why

DNS

is usually

very fast.

______________________________________________________________________

# DNS Load Balancing

DNS

can also

distribute traffic.

Example

```
example.com

↓

Server A

↓

Server B

↓

Server C
```

Different users

may receive

different IP addresses.

This is

simple

load balancing.

______________________________________________________________________

# Geo DNS

Users in

India

receive

Indian servers.

Users in

Germany

receive

German servers.

Example

```
India

↓

Mumbai

Server
```

```
Germany

↓

Frankfurt

Server
```

Lower latency.

Better user experience.

______________________________________________________________________

# DNS Failover

Suppose

Server A

fails.

DNS

can start returning

Server B.

Simple,

but

not immediate,

because

TTL

must expire.

______________________________________________________________________

# DNS vs Load Balancer

Many candidates

confuse them.

DNS

```
Find Server
```

Load Balancer

```
Choose Best Server
```

DNS

works

before

the connection.

Load Balancer

works

after

the connection.

______________________________________________________________________

# CDN & DNS

CDNs

often use

DNS

to direct users

to

the nearest

edge location.

Example

```
User

India

↓

Mumbai CDN
```

```
User

Germany

↓

Frankfurt CDN
```

______________________________________________________________________

# Common Interview Questions

## Why doesn't every request contact Root DNS?

Because

DNS responses

are cached

using TTL.

______________________________________________________________________

## Can DNS replace a Load Balancer?

No.

DNS

cannot monitor

server health,

active connections,

or response time.

Load Balancers

can.

______________________________________________________________________

## What happens if a DNS server fails?

Resolvers

typically use

multiple DNS servers.

Authoritative DNS

is also

highly redundant.

______________________________________________________________________

## Why is DNS so fast?

Because

of

multi-level caching

and

distributed infrastructure.

______________________________________________________________________

# DNS In System Design

Typical flow

```
User

↓

DNS

↓

Load Balancer

↓

Application Servers

↓

Database
```

DNS

is almost always

the first component

a client interacts with.

______________________________________________________________________

# Common Mistakes

## Thinking DNS Knows Everything

Root DNS

doesn't know

every IP.

It only knows

where to continue

the lookup.

______________________________________________________________________

## Ignoring Caching

Caching

is one of

DNS's biggest strengths.

______________________________________________________________________

## Confusing DNS With CDN

DNS

maps names

to IPs.

CDN

delivers content.

______________________________________________________________________

## Forgetting TTL

TTL

is frequently asked

during interviews.

Remember it.

______________________________________________________________________

# Best Practices

✅ Use low TTL during migrations.

✅ Use higher TTL for stable records.

✅ Configure multiple authoritative DNS servers.

✅ Use public DNS providers for reliability.

✅ Cache DNS responses whenever appropriate.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the purpose of DNS?

### Answer

DNS translates human-readable domain names into IP addresses so that clients can locate and communicate with servers
without remembering numerical addresses.

______________________________________________________________________

## Question

What is the difference between an A record and a CNAME record?

### Answer

An **A record** maps a domain directly to an IPv4 address. A **CNAME record** maps one domain name to another domain
name, acting as an alias.

______________________________________________________________________

## Question

Why is TTL important?

### Answer

TTL determines how long DNS responses may be cached. Proper TTL values reduce DNS lookup latency and lower the load on
DNS infrastructure while balancing the need for timely updates.

______________________________________________________________________

# Practice Exercise

For each scenario,

answer the following.

1. Which DNS records are required?
1. Should TTL be high or low?
1. Is Geo DNS useful?
1. Would DNS alone be enough, or is a Load Balancer also needed?

Scenarios

- Personal portfolio website
- E-commerce platform
- Global video streaming service
- Banking application
- Multiplayer online game
- Food delivery platform

______________________________________________________________________

# Summary

DNS is one of the foundational technologies of the Internet.

It

- Translates domain names to IP addresses
- Uses hierarchical lookups
- Relies heavily on caching
- Supports multiple record types
- Enables global traffic routing
- Works together with Load Balancers and CDNs

Understanding DNS is essential because almost every distributed system begins with a DNS lookup.

______________________________________________________________________

# Next

[CDN (Content Delivery Network)](07-cdn.md)
