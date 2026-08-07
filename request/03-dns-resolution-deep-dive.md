# Complete HTTP Request Lifecycle Deep Dive

## 03. DNS Resolution Deep Dive

> Target Audience: Backend Engineers (Beginner → Senior)
>
> Goal: Understand exactly what happens after the browser decides it needs to resolve a domain name. Learn how DNS works internally, how caching reduces latency, how DNS servers communicate, and what security attacks are possible.

______________________________________________________________________

# Introduction

In the previous chapter,

the browser

finished

parsing the URL.

Suppose

the user enters

```
https://www.google.com
```

The browser knows

```
Host

↓

www.google.com
```

But

it still

doesn't know

where Google

is located.

It needs

an IP address.

Example

```
www.google.com

↓

142.250.xxx.xxx
```

This conversion

is called

```
DNS Resolution
```

______________________________________________________________________

# What Is DNS?

DNS stands for

```
Domain Name System
```

Think of DNS

as

the Internet's

phone book.

Instead of remembering

```
142.250.183.68
```

we remember

```
www.google.com
```

DNS converts

human-friendly names

into

machine-friendly

IP addresses.

______________________________________________________________________

# Why Do We Need DNS?

Imagine

every website

required

remembering

an IP address.

```
Google

↓

142.250.xxx.xxx

Facebook

↓

157.240.xxx.xxx

Amazon

↓

54.xxx.xxx.xxx
```

Impossible

for humans.

DNS solves

this problem.

______________________________________________________________________

# High-Level Flow

```
Browser

↓

Browser DNS Cache

↓

Operating System Cache

↓

Hosts File

↓

Router Cache

↓

ISP DNS Resolver

↓

Root DNS

↓

TLD DNS

↓

Authoritative DNS

↓

IP Address

↓

Browser
```

This entire process

usually completes

within

a few milliseconds.

______________________________________________________________________

# Step 1

# Browser DNS Cache

Interview favorite.

The browser

first checks

its own

DNS cache.

```
google.com

↓

Already Cached?

↓

Yes

↓

Return IP
```

No network request

is made.

______________________________________________________________________

# Browser Cache Example

Suppose

you visited

Google

10 seconds ago.

The browser

may already know

```
www.google.com

↓

142.250.xxx.xxx
```

Instant result.

______________________________________________________________________

# Step 2

# Operating System DNS Cache

If

browser cache

misses,

the browser

asks

the Operating System.

Windows

Linux

macOS

all maintain

their own

DNS cache.

```
Chrome

↓

Operating System

↓

DNS Cache
```

______________________________________________________________________

# Step 3

# Hosts File

Interview favorite.

Before

contacting

the Internet,

the OS checks

the

Hosts File.

Example

Linux

```
/etc/hosts
```

Windows

```
C:\Windows\System32\
drivers\etc\hosts
```

Example

```
127.0.0.1

localhost
```

Or

```
192.168.1.20

internal.company.com
```

No DNS lookup

is needed.

______________________________________________________________________

# Why Hosts File Exists

Useful for

- Local development
- Internal testing
- Blocking websites
- Temporary overrides

______________________________________________________________________

# Step 4

# Router Cache

Some routers

maintain

their own

DNS cache.

If found

```
Router

↓

Returns IP
```

Otherwise

request continues.

______________________________________________________________________

# Step 5

# Recursive Resolver

Interview favorite.

Usually

your ISP

or

Cloudflare

or

Google

provides

a

Recursive Resolver.

Examples

```
8.8.8.8

Google
```

```
1.1.1.1

Cloudflare
```

```
9.9.9.9

Quad9
```

The resolver

does

the hard work

for you.

______________________________________________________________________

# Recursive Resolver

Responsibilities

- Query Root Servers
- Query TLD Servers
- Query Authoritative Servers
- Cache Results
- Return IP

______________________________________________________________________

# What If Resolver Already Knows?

Suppose

another user

recently requested

```
google.com
```

Resolver cache

contains

```
google.com

↓

142.xxx.xxx.xxx
```

Immediate response.

______________________________________________________________________

# Step 6

# Root DNS Server

Interview favorite.

If

resolver

doesn't know,

it asks

a Root DNS Server.

Question

```
Where is

google.com?
```

Root server

doesn't know

Google's IP.

Instead

it knows

where

the

```
.com
```

servers are.

Returns

```
Ask

.com

TLD Server
```

______________________________________________________________________

# Root Servers

There are

13 logical

Root Server clusters

distributed

worldwide.

They are

replicated

using

Anycast

for

high availability.

______________________________________________________________________

# Step 7

# TLD Server

TLD means

```
Top Level Domain
```

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

TLD server

responds

```
Ask

Google's

Authoritative Server
```

______________________________________________________________________

# Step 8

# Authoritative DNS

Interview favorite.

Only

the Authoritative Server

knows

the final answer.

Example

```
google.com

↓

142.xxx.xxx.xxx
```

Resolver

finally gets

the IP address.

______________________________________________________________________

# Step 9

# Return Response

The resolver

returns

the IP

to

the Operating System.

Operating System

returns it

to

Chrome.

Chrome now knows

where

Google lives.

______________________________________________________________________

# Complete DNS Flow

```
Chrome

↓

Browser Cache

↓

OS Cache

↓

Hosts File

↓

Router Cache

↓

Recursive Resolver

↓

Root Server

↓

TLD Server

↓

Authoritative DNS

↓

IP Address

↓

Browser
```

______________________________________________________________________

# What Actually Happens Internally?

Suppose

Chrome

needs

```
google.com
```

Chrome creates

a DNS query.

```
Query

↓

UDP Packet

↓

Port 53

↓

Router

↓

Recursive Resolver
```

The resolver

may generate

multiple

additional queries

before

returning

the answer.

______________________________________________________________________

# Why UDP?

Interview favorite.

DNS

normally uses

```
UDP

Port 53
```

Benefits

- Fast
- Connectionless
- Low overhead

______________________________________________________________________

# When Does DNS Use TCP?

TCP

is used

when

- Large responses
- Zone transfers
- DNSSEC
- Response truncation

Port

```
53
```

______________________________________________________________________

# DNS Caching

Caching happens

at

multiple levels.

```
Browser

↓

Operating System

↓

Router

↓

Resolver

↓

Authoritative
```

This dramatically

reduces

latency.

______________________________________________________________________

# TTL

Interview favorite.

TTL means

```
Time To Live
```

Example

```
TTL

300 Seconds
```

Resolver

may cache

the IP

for

5 minutes.

After TTL expires,

DNS

must be queried

again.

______________________________________________________________________

# Why TTL Matters

Short TTL

Benefits

- Faster updates

Disadvantages

- More DNS traffic

______________________________________________________________________

Long TTL

Benefits

- Faster responses

Disadvantages

- Slower propagation

______________________________________________________________________

# Multiple IP Addresses

Google

doesn't have

one server.

DNS may return

multiple IPs.

Example

```
142.xxx.xxx.1

142.xxx.xxx.2

142.xxx.xxx.3
```

This enables

Load Balancing.

______________________________________________________________________

# Anycast DNS

Interview bonus.

Many DNS servers

share

the same IP.

Internet routing

automatically sends

requests

to

the nearest

server.

Benefits

- Low latency
- High availability
- DDoS resistance

______________________________________________________________________

# DNS Record Types

Interview favorite.

## A Record

Maps

```
Domain

↓

IPv4
```

______________________________________________________________________

## AAAA Record

Maps

```
Domain

↓

IPv6
```

______________________________________________________________________

## CNAME

Alias.

Example

```
www.example.com

↓

example.com
```

______________________________________________________________________

## MX

Mail servers.

______________________________________________________________________

## TXT

Verification

SPF

DKIM

Domain ownership.

______________________________________________________________________

## NS

Nameserver

information.

______________________________________________________________________

# DNS Load Balancing

One domain

may return

multiple IPs.

```
google.com

↓

IP1

IP2

IP3
```

Client

chooses

one.

______________________________________________________________________

# Geo DNS

DNS

may return

different IPs

based on

location.

India

↓

Mumbai Server

Germany

↓

Frankfurt Server

USA

↓

Virginia Server

______________________________________________________________________

# Reverse DNS

Normal DNS

```
Domain

↓

IP
```

Reverse DNS

```
IP

↓

Domain
```

Used

for

email servers

and diagnostics.

______________________________________________________________________

# Common Attacks

## DNS Spoofing

Attacker

returns

a fake IP.

```
google.com

↓

Attacker Server
```

______________________________________________________________________

## DNS Cache Poisoning

Attacker

injects

incorrect entries

into

resolver cache.

Future users

receive

malicious IPs.

______________________________________________________________________

## DNS Amplification

Uses

open DNS resolvers

to perform

DDoS attacks.

______________________________________________________________________

## DNS Tunneling

Data

is hidden

inside

DNS requests.

Often used

to bypass

firewalls.

______________________________________________________________________

# DNS Security

Modern protections

include

- DNSSEC
- DNS over HTTPS (DoH)
- DNS over TLS (DoT)
- Query validation
- Cache validation

______________________________________________________________________

# DNSSEC

Interview favorite.

DNSSEC

adds

digital signatures

to DNS records.

Purpose

Verify

the response

hasn't been

modified.

It does NOT

encrypt

DNS traffic.

______________________________________________________________________

# DNS over HTTPS (DoH)

Traditional DNS

```
Plain Text
```

DoH

wraps

DNS

inside

HTTPS.

Benefits

- Privacy
- Encryption
- Prevents ISP snooping

______________________________________________________________________

# DNS over TLS (DoT)

Another

encrypted DNS

protocol.

Uses

TLS

instead of

plain UDP.

______________________________________________________________________

# Technologies Used

| Component | Technologies |
|------------|--------------|
| Browser Cache | Chrome, Firefox |
| OS Cache | Windows DNS Client, systemd-resolved |
| Resolver | Google DNS, Cloudflare DNS, Quad9 |
| Root Servers | Root DNS Clusters |
| DNS Software | BIND, PowerDNS, Unbound |
| Secure DNS | DNSSEC, DoH, DoT |

______________________________________________________________________

# Common Interview Questions

## Why doesn't every request contact the Root DNS servers?

Because DNS is heavily cached at multiple layers. Most requests are answered by the browser, operating system, router,
or recursive resolver without contacting Root or TLD servers.

______________________________________________________________________

## Why does DNS usually use UDP?

UDP has lower overhead because it doesn't require a connection handshake. DNS requests are typically small and benefit
from faster communication.

______________________________________________________________________

## What is TTL?

TTL defines how long a DNS record can be cached before it must be refreshed from the authoritative source.

______________________________________________________________________

## What is the difference between a Recursive Resolver and an Authoritative Server?

The recursive resolver searches for the answer on behalf of the client and caches results. The authoritative server owns
the official DNS records for a domain.

______________________________________________________________________

# Interview Deep Dive

## Question

Walk me through DNS resolution after typing `www.google.com`.

### Answer

The browser checks its DNS cache, followed by the operating system cache, hosts file, router cache, and recursive
resolver. If the resolver has no cached entry, it queries the Root DNS servers, then the appropriate TLD server, then
the authoritative DNS server. The authoritative server returns the IP address, which is cached according to its TTL and
sent back to the browser.

______________________________________________________________________

# Summary

DNS is one of the most heavily optimized systems on the Internet.

Key concepts include

- Multi-level caching
- Recursive resolution
- Root, TLD, and Authoritative servers
- UDP vs TCP
- TTL
- DNSSEC
- DoH
- Common DNS attacks

Only after DNS resolution completes does the browser know **which IP address to contact**, allowing the next
stage—establishing a TCP connection—to begin.

______________________________________________________________________

# Next

[04. TCP/IP and Network Routing](04-tcp-ip-and-network-routing.md)
