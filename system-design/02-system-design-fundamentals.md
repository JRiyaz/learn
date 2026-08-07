# System Design Fundamentals

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Understand what System Design really is, learn the terminology, and build the foundation required for all upcoming system design interviews.

______________________________________________________________________

# Introduction

Before designing

YouTube,

WhatsApp,

or Uber,

you must understand

the building blocks.

Think of this chapter as

learning the alphabet

before writing essays.

______________________________________________________________________

# What Is A System?

A system is simply

a collection of components

working together

to solve a problem.

Example

```
User

↓

Browser

↓

API

↓

Database

↓

Response
```

This entire flow

is a system.

______________________________________________________________________

# What Is System Design?

System Design is the process of deciding

```
What Components

↓

How They Communicate

↓

How They Scale

↓

How They Recover

↓

How They Stay Reliable
```

There is

no single

correct design.

There are

better

and

worse

trade-offs.

______________________________________________________________________

# Real Example

Suppose

someone asks

```
Design WhatsApp
```

They are NOT asking

```
Write the code.
```

They are asking

```
How should millions of users

exchange messages

reliably

and quickly?
```

______________________________________________________________________

# Functional Requirements

These describe

what

the system should do.

Examples

For YouTube

- Upload videos
- Watch videos
- Search videos
- Like videos
- Comment
- Subscribe

Focus

on features.

______________________________________________________________________

# Non-Functional Requirements

These describe

how well

the system should perform.

Examples

- Scalability
- Reliability
- Availability
- Performance
- Security
- Maintainability
- Fault Tolerance

These often determine

the architecture.

______________________________________________________________________

# Functional vs Non-Functional

| Functional | Non-Functional |
|------------|----------------|
| Login | 99.99% uptime |
| Upload Image | Response under 200ms |
| Send Message | Support 100M users |
| Watch Video | High availability |

One defines

features.

The other defines

quality.

______________________________________________________________________

# Why Requirements Matter

Bad candidates

immediately draw

architecture.

Good candidates

ask

questions first.

Example

```
Is the system

global?

↓

How many users?

↓

Read-heavy?

↓

Write-heavy?

↓

Real-time?

↓

Expected latency?
```

______________________________________________________________________

# Scale Matters

A system for

100 users

looks very different

from one

serving

100 million users.

Example

```
100 Users

↓

Single Server
```

vs

```
100 Million Users

↓

Load Balancer

↓

Multiple Servers

↓

Distributed Database

↓

Cache

↓

CDN
```

Scale changes everything.

______________________________________________________________________

# Read vs Write Heavy

Understanding workload

is critical.

______________________________________________________________________

## Read Heavy

Examples

- YouTube
- Netflix
- News websites
- Blogs

Millions

reading

few

writing.

Architecture

focuses on

Caching

CDN

Replication

______________________________________________________________________

## Write Heavy

Examples

- Chat application
- Payment system
- Ride booking
- Banking

Many

writes.

Architecture

focuses on

Consistency

Durability

Reliable Messaging

______________________________________________________________________

# Latency

Latency means

```
How long

it takes

to receive

a response.
```

Example

```
Click Login

↓

200 milliseconds

↓

Dashboard Opens
```

Latency

is

response time.

______________________________________________________________________

# Throughput

Throughput means

```
How much work

the system

can perform

per second.
```

Example

```
100,000 Requests

per second
```

High throughput

usually requires

horizontal scaling.

______________________________________________________________________

# Bandwidth

Bandwidth means

how much data

can travel

through the network.

Example

```
10 Mbps

vs

1 Gbps
```

Higher bandwidth

allows

more data

to move

simultaneously.

______________________________________________________________________

# Availability

Availability means

```
Is the service

accessible?
```

Example

```
Google Works

↓

High Availability
```

```
Website Down

↓

Low Availability
```

Companies often target

```
99.9%

99.99%

99.999%
```

uptime.

______________________________________________________________________

# Reliability

Availability

is not

the same

as reliability.

Example

A website

may always open,

but if

payments fail,

it isn't reliable.

Reliable systems

produce

correct results

consistently.

______________________________________________________________________

# Scalability

Scalability means

```
Can the system

handle more users

without breaking?
```

Example

```
1,000 Users

↓

10,000 Users

↓

100,000 Users

↓

1 Million Users
```

Can performance

remain acceptable?

______________________________________________________________________

# Vertical Scaling

Also called

```
Scale Up
```

Example

```
4 CPU

↓

16 CPU
```

Same server.

More powerful hardware.

Advantages

- Simple
- Easy

Disadvantages

- Hardware limit
- Expensive
- Single point of failure

______________________________________________________________________

# Horizontal Scaling

Also called

```
Scale Out
```

Example

```
Server

↓

2 Servers

↓

10 Servers

↓

100 Servers
```

Advantages

- Better scalability
- Better availability
- Fault tolerance

Disadvantages

- More complexity
- Load balancing required

Most modern systems

prefer

horizontal scaling.

______________________________________________________________________

# Fault Tolerance

Fault tolerance means

```
Can the system

continue working

when something fails?
```

Example

One server crashes.

Another server

continues serving requests.

Users

never notice.

______________________________________________________________________

# Redundancy

Redundancy means

keeping

extra resources.

Example

```
Database

↓

Replica Database
```

or

```
Server A

↓

Server B
```

If one fails,

another

takes over.

______________________________________________________________________

# Durability

Durability means

```
Once data is saved,

it should not

be lost.
```

Example

After transferring money,

a server crash

must not

erase

the transaction.

______________________________________________________________________

# Consistency

Consistency means

everyone

sees

the same data.

Example

```
Bank Balance

₹1000

↓

Transfer ₹500

↓

Everyone sees ₹500
```

Not

different balances

on different servers.

______________________________________________________________________

# Partition

A partition

is simply

a separate portion

of data.

Example

Instead of storing

all users

in one database,

store

```
Users A-M

↓

Database 1

Users N-Z

↓

Database 2
```

We'll revisit this

when discussing

sharding.

______________________________________________________________________

# Bottleneck

A bottleneck

is

the slowest part

of a system.

Example

```
Fast API

↓

Slow Database

↓

Entire System Slow
```

Optimizing

other components

won't help

until

the bottleneck

is addressed.

______________________________________________________________________

# Single Point Of Failure (SPOF)

A SPOF

is any component

whose failure

brings down

the system.

Example

```
Users

↓

One Server

↓

Crash

↓

Everything Stops
```

Goal

Remove SPOFs.

______________________________________________________________________

# High-Level Architecture

Most modern web systems

start like this.

```
Users

↓

DNS

↓

Load Balancer

↓

Application Servers

↓

Cache

↓

Database

↓

Storage
```

We'll study

every component

individually.

______________________________________________________________________

# Common Interview Terms

Know these well.

| Term | Meaning |
|------|----------|
| Latency | Response time |
| Throughput | Requests processed per second |
| Availability | Service accessibility |
| Reliability | Correctness over time |
| Scalability | Handle growth |
| Fault Tolerance | Continue after failures |
| Redundancy | Backup resources |
| Durability | Data survives failures |
| Consistency | Same data everywhere |
| Bottleneck | Slowest component |
| SPOF | Single Point of Failure |

Interviewers

expect

these definitions.

______________________________________________________________________

# Common Mistakes

## Confusing Availability With Reliability

Available

doesn't mean

correct.

______________________________________________________________________

## Ignoring Scale

Architecture

depends

on

traffic.

______________________________________________________________________

## Forgetting Non-Functional Requirements

System Design

isn't only

about features.

______________________________________________________________________

## Overengineering

Don't design

Google

for

100 users.

______________________________________________________________________

# Best Practices

✅ Ask questions first.

✅ Separate functional and non-functional requirements.

✅ Think about scale.

✅ Identify bottlenecks.

✅ Remove single points of failure.

✅ Explain trade-offs.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between functional and non-functional requirements?

### Answer

Functional requirements describe **what** the system should do, such as login or sending messages. Non-functional
requirements describe **how well** the system should perform, including scalability, availability, latency, security,
and reliability.

______________________________________________________________________

## Question

Why is scalability important?

### Answer

Scalability ensures that a system can continue serving increasing numbers of users without significant degradation in
performance or reliability.

______________________________________________________________________

## Question

Why shouldn't we design everything like Google?

### Answer

Architecture should match business requirements. Designing an extremely complex distributed system for a small
application increases cost and maintenance without providing meaningful benefits.

______________________________________________________________________

# Practice Exercise

For each application below,

identify

1. Functional requirements
1. Non-functional requirements
1. Read-heavy or write-heavy
1. Expected scalability challenges

Applications

- WhatsApp
- Netflix
- Instagram
- Banking System
- Uber
- Food Delivery
- Online Shopping
- URL Shortener

______________________________________________________________________

# Summary

Every System Design interview begins with understanding the problem.

Before discussing databases,

microservices,

or caching,

you must first understand

- Requirements
- Scale
- Performance expectations
- Reliability needs
- Business goals

These fundamentals will guide every design decision throughout the rest of the course.

______________________________________________________________________

# Next

[System Design Interview Framework](03-interview-framework.md)
