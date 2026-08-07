# Capacity Estimation

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to estimate system capacity during System Design interviews. Capacity estimation helps justify architectural decisions and demonstrates engineering thinking.

______________________________________________________________________

# Introduction

One of the biggest mistakes candidates make is

drawing architecture

without understanding

the scale.

Interviewers don't expect

perfect calculations.

They expect

reasonable assumptions.

______________________________________________________________________

# Why Capacity Estimation Matters

Capacity estimation helps answer

- How many servers?
- How much storage?
- How much bandwidth?
- Should we use caching?
- Do we need sharding?
- Can one database handle the load?

Without estimation,

architecture

becomes

guesswork.

______________________________________________________________________

# What Interviewers Are Actually Evaluating

They're not checking

your math.

They're checking

whether you can reason about

```
Traffic

↓

Storage

↓

Memory

↓

Network

↓

Growth
```

______________________________________________________________________

# Golden Rule

Don't waste

15 minutes

doing calculations.

Spend

3–5 minutes

making reasonable assumptions.

Always state

your assumptions.

Example

> I'll assume the application has around 50 million registered users and 5 million daily active users.

Perfectly acceptable.

______________________________________________________________________

# Common Assumptions

These are commonly used

during interviews.

| Metric | Typical Assumption |
|---------|-------------------|
| Registered Users | 100 Million |
| Daily Active Users | 10 Million |
| Concurrent Users | 5–10% of DAU |
| Read/Write Ratio | Depends on application |
| Average Request Size | 1 KB |
| Image Size | 500 KB–2 MB |
| Video Size | 50 MB–500 MB |
| Text Message | 100 Bytes |
| Availability | 99.99% |

Interviewers care more

about reasoning

than exact numbers.

______________________________________________________________________

# Step 1

# Estimate Users

Example

```
100 Million Registered Users

↓

10 Million Daily Active Users

↓

1 Million Concurrent Users
```

Concurrent users

are the ones

actually connected

at the same time.

______________________________________________________________________

# Step 2

# Estimate Requests Per Second (RPS)

Formula

```
Daily Requests

÷

Seconds Per Day
```

Example

10 Million users

Each user performs

20 requests/day.

```
10M × 20

=

200 Million Requests/Day
```

Seconds per day

```
24 × 60 × 60

=

86,400
```

Therefore

```
200,000,000

÷

86,400

≈

2,315 Requests/sec
```

Always round.

Say

```
~2,500 RPS
```

Good enough.

______________________________________________________________________

# Peak Traffic

Traffic

isn't constant.

Peak hours

may be

3–5×

higher.

Example

Average

```
2,500 RPS
```

Peak

```
10,000 RPS
```

Always design

for peak traffic.

______________________________________________________________________

# Step 3

# Estimate Storage

Example

Photo Sharing App

Each image

```
2 MB
```

Each user uploads

```
10 Images
```

Daily users

```
1 Million
```

Storage/day

```
1M

×

10

×

2MB

=

20 TB/day
```

Yearly

```
20 TB

×

365

≈

7.3 PB
```

Petabytes.

Now

Object Storage

becomes necessary.

______________________________________________________________________

# Step 4

# Estimate Database Size

Example

User Table

Each record

```
2 KB
```

100 Million Users

```
2 KB

×

100M

=

200 GB
```

Very manageable.

______________________________________________________________________

# Example

Chat Application

Message

```
100 Bytes
```

Daily Messages

```
1 Billion
```

Storage/day

```
100 Bytes

×

1B

=

100 GB/day
```

One year

```
≈36 TB
```

Still manageable

with proper storage.

______________________________________________________________________

# Step 5

# Estimate Bandwidth

Example

```
10,000 Requests/sec

↓

2 KB Response
```

Bandwidth

```
20 MB/sec
```

Per minute

```
1.2 GB
```

Per hour

```
72 GB
```

Bandwidth

helps determine

network requirements.

______________________________________________________________________

# Step 6

# Estimate Cache Size

Suppose

popular data

contains

```
5 Million Records
```

Each record

```
1 KB
```

Cache

```
5 GB
```

Redis

can easily

handle this.

______________________________________________________________________

# Step 7

# Estimate Memory

Example

Active Sessions

```
2 Million
```

Each session

```
1 KB
```

Memory

```
2 GB
```

Easy

for Redis.

______________________________________________________________________

# Step 8

# Estimate Number Of Servers

Suppose

one application server

handles

```
500 Requests/sec
```

Traffic

```
10,000 RPS
```

Servers

```
10,000

÷

500

=

20 Servers
```

Add redundancy.

Deploy

25–30 servers.

______________________________________________________________________

# Read vs Write

Example

YouTube

```
Reads

95%

Writes

5%
```

Caching

becomes

extremely valuable.

______________________________________________________________________

Chat Application

```
Reads

55%

Writes

45%
```

Very different

architecture.

______________________________________________________________________

# Storage Growth

Always estimate

future growth.

Example

```
20 TB/day

↓

7 PB/year

↓

35 PB

after

5 years
```

Growth

changes

architecture.

______________________________________________________________________

# Capacity Estimation Checklist

During interviews

estimate

```
Users

↓

DAU

↓

Concurrent Users

↓

RPS

↓

Peak RPS

↓

Storage

↓

Bandwidth

↓

Cache

↓

Memory

↓

Servers
```

This is enough

for most interviews.

______________________________________________________________________

# Example

Design Instagram

Assumptions

```
500M Registered Users

↓

100M DAU

↓

10M Concurrent Users
```

Traffic

```
100M Users

×

50 Requests/day

=

5 Billion Requests/day
```

RPS

```
≈58,000 RPS

Peak

≈250,000 RPS
```

Images

```
100M Photos/day

×

2MB

=

200 TB/day
```

Immediately

you know

Object Storage

CDN

Caching

are required.

______________________________________________________________________

# Example

Design URL Shortener

Assumptions

```
100M URLs

↓

500M Redirects/day
```

Storage

Small.

Traffic

Very high.

This becomes

```
Read Heavy
```

Use

Cache

Replication

Load Balancer.

______________________________________________________________________

# Common Interview Tricks

Interviewer

asks

```
Do we need

sharding?
```

Answer

depends

on

estimated data size.

Not

guessing.

______________________________________________________________________

# Approximation Is Fine

Don't calculate

```
2,314.81 RPS
```

Say

```
~2.5K RPS
```

Interviewers

prefer

fast reasoning.

______________________________________________________________________

# Common Mistakes

## Overcomplicated Math

Keep calculations

simple.

______________________________________________________________________

## Forgetting Peak Traffic

Always estimate

peak load.

______________________________________________________________________

## Ignoring Growth

Think

years,

not

today.

______________________________________________________________________

## No Assumptions

State assumptions

before calculating.

______________________________________________________________________

## Unrealistic Numbers

Don't say

```
Every user uploads

100 videos/day.
```

Use

reasonable values.

______________________________________________________________________

# Best Practices

✅ State assumptions.

✅ Round numbers.

✅ Estimate peak traffic.

✅ Consider future growth.

✅ Connect estimates to architecture.

______________________________________________________________________

# Capacity Estimation Cheat Sheet

```
Users

↓

DAU

↓

Concurrent Users

↓

Requests/day

↓

RPS

↓

Peak RPS

↓

Storage/day

↓

Bandwidth

↓

Cache

↓

Servers
```

Memorize

this sequence.

______________________________________________________________________

# Interview Deep Dive

## Question

Do interviewers expect exact calculations?

### Answer

No. They expect reasonable assumptions and logical estimation. Being able to justify architectural decisions based on
estimated traffic and storage is far more important than mathematical precision.

______________________________________________________________________

## Question

Why do we estimate peak traffic instead of average traffic?

### Answer

Systems usually fail during peak usage, not during average load. Designing for peak traffic ensures the system remains
responsive during busy periods.

______________________________________________________________________

## Question

When should I introduce sharding or caching?

### Answer

Only after your estimates justify them. Architectural components should solve demonstrated scaling problems rather than
being included by default.

______________________________________________________________________

# Practice Exercise

Estimate the following for each system.

1. WhatsApp
1. Instagram
1. YouTube
1. Uber
1. Food Delivery
1. Netflix
1. URL Shortener
1. Twitter/X

For each,

estimate

- Registered users
- Daily active users
- Concurrent users
- Requests per second
- Peak RPS
- Storage/day
- Cache size
- Number of servers
- Long-term storage growth

Don't focus on exact answers.

Focus on

reasonable assumptions

and

explaining your reasoning.

______________________________________________________________________

# Summary

Capacity estimation is one of the first steps in System Design.

It helps you decide

- Whether one server is enough
- Whether caching is required
- Whether the database needs sharding
- How much storage is needed
- How the system should evolve over time

Strong candidates use estimation to justify architecture—not to impress with complicated calculations.

______________________________________________________________________

# Next

[Load Balancers](05-load-balancers.md)
