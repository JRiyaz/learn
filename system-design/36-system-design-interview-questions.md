# System Design Interview Questions

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Practice comprehensive System Design questions covering architecture, scalability, databases, caching, networking, messaging, distributed systems, and real-world design scenarios.

______________________________________________________________________

# Introduction

This file

contains

practice questions

similar to

those asked

during

System Design interviews.

Questions

are grouped

by topic.

There are

no answers.

Try answering

them yourself

before

reviewing

your notes.

______________________________________________________________________

# Section 1

# Requirement Gathering

## Question 1

How would you clarify requirements before designing Instagram?

______________________________________________________________________

## Question 2

What functional and non-functional requirements would you gather before designing WhatsApp?

______________________________________________________________________

## Question 3

How would your questions differ when designing Amazon instead of Uber?

______________________________________________________________________

## Question 4

Why is requirement gathering important in System Design interviews?

______________________________________________________________________

## Question 5

What assumptions should never be made without asking the interviewer?

______________________________________________________________________

# Section 2

# Capacity Estimation

## Question 6

Estimate storage required for

100 million users

uploading

3 images

per day.

______________________________________________________________________

## Question 7

Estimate requests per second for

20 million daily requests.

______________________________________________________________________

## Question 8

Estimate storage required for

a messaging application

serving

1 billion users.

______________________________________________________________________

## Question 9

Estimate bandwidth requirements for

50 million concurrent

video streams.

______________________________________________________________________

## Question 10

Why is capacity estimation important?

______________________________________________________________________

# Section 3

# API Design

## Question 11

Design REST APIs

for

Instagram.

______________________________________________________________________

## Question 12

Design APIs

for

BookMyShow.

______________________________________________________________________

## Question 13

Design APIs

for

an online payment platform.

______________________________________________________________________

## Question 14

How would you version APIs?

______________________________________________________________________

## Question 15

When would you choose

REST,

GraphQL,

or

gRPC?

______________________________________________________________________

# Section 4

# Database Design

## Question 16

When should you choose

SQL?

______________________________________________________________________

## Question 17

When should you choose

NoSQL?

______________________________________________________________________

## Question 18

Explain

Replication.

______________________________________________________________________

## Question 19

Explain

Sharding.

______________________________________________________________________

## Question 20

Difference between

Replication

and

Sharding.

______________________________________________________________________

## Question 21

How would you shard

Instagram?

______________________________________________________________________

## Question 22

How would you shard

WhatsApp?

______________________________________________________________________

## Question 23

What are

secondary indexes?

______________________________________________________________________

## Question 24

What are

database partitions?

______________________________________________________________________

## Question 25

What problems

can occur

after sharding?

______________________________________________________________________

# Section 5

# Caching

## Question 26

What is

Cache Aside?

______________________________________________________________________

## Question 27

Explain

Write Through

and

Write Behind.

______________________________________________________________________

## Question 28

What is

Cache Stampede?

______________________________________________________________________

## Question 29

What is

Cache Avalanche?

______________________________________________________________________

## Question 30

What is

Cache Penetration?

______________________________________________________________________

## Question 31

What is

TTL?

______________________________________________________________________

## Question 32

Explain

LRU,

LFU,

FIFO.

______________________________________________________________________

## Question 33

When should data

not be cached?

______________________________________________________________________

## Question 34

How would you maintain

cache consistency?

______________________________________________________________________

## Question 35

Why is Redis

used

as a cache?

______________________________________________________________________

# Section 6

# Load Balancing

## Question 36

What is

a Load Balancer?

______________________________________________________________________

## Question 37

Round Robin

vs

Least Connections.

______________________________________________________________________

## Question 38

Layer 4

vs

Layer 7

Load Balancer.

______________________________________________________________________

## Question 39

What happens

if

a Load Balancer

fails?

______________________________________________________________________

## Question 40

How do

health checks

work?

______________________________________________________________________

# Section 7

# CDN & Object Storage

## Question 41

Why use

Object Storage?

______________________________________________________________________

## Question 42

Why use

a CDN?

______________________________________________________________________

## Question 43

How does

Netflix

deliver

videos globally?

______________________________________________________________________

## Question 44

Why shouldn't

large images

be stored

inside MySQL?

______________________________________________________________________

## Question 45

How would you

design

image uploads?

______________________________________________________________________

# Section 8

# Messaging

## Question 46

RabbitMQ

vs

Kafka.

______________________________________________________________________

## Question 47

When should

Kafka

be preferred?

______________________________________________________________________

## Question 48

What is

a Dead Letter Queue?

______________________________________________________________________

## Question 49

How does

event-driven architecture

work?

______________________________________________________________________

## Question 50

Explain

Producer

Consumer

pattern.

______________________________________________________________________

# Section 9

# Distributed Systems

## Question 51

Explain

CAP Theorem.

______________________________________________________________________

## Question 52

Explain

Consistent Hashing.

______________________________________________________________________

## Question 53

Explain

Service Discovery.

______________________________________________________________________

## Question 54

Explain

Distributed Locking.

______________________________________________________________________

## Question 55

What is

Split Brain?

______________________________________________________________________

## Question 56

What is

Leader Election?

______________________________________________________________________

## Question 57

What is

Eventual Consistency?

______________________________________________________________________

## Question 58

What is

Strong Consistency?

______________________________________________________________________

## Question 59

What is

Quorum?

______________________________________________________________________

## Question 60

Explain

Distributed Transactions.

______________________________________________________________________

# Section 10

# Security

## Question 61

How would you

secure

an API?

______________________________________________________________________

## Question 62

Authentication

vs

Authorization.

______________________________________________________________________

## Question 63

JWT

vs

Sessions.

______________________________________________________________________

## Question 64

How would you

protect

against

DDoS?

______________________________________________________________________

## Question 65

How would you

secure

payment systems?

______________________________________________________________________

# Section 11

# Monitoring

## Question 66

Which metrics

would you monitor

for

Redis?

______________________________________________________________________

## Question 67

How would you

monitor

Kafka?

______________________________________________________________________

## Question 68

What metrics

would you

track

for APIs?

______________________________________________________________________

## Question 69

What should

be monitored

for databases?

______________________________________________________________________

## Question 70

What alerts

would you configure

for production?

______________________________________________________________________

# Section 12

# Failure Handling

## Question 71

Redis fails.

What happens?

______________________________________________________________________

## Question 72

Database fails.

What happens?

______________________________________________________________________

## Question 73

Queue fails.

What happens?

______________________________________________________________________

## Question 74

CDN fails.

What happens?

______________________________________________________________________

## Question 75

How would you

design

disaster recovery?

______________________________________________________________________

# Section 13

# Concurrency

## Question 76

How would you

prevent

double booking

in BookMyShow?

______________________________________________________________________

## Question 77

Optimistic Locking

vs

Pessimistic Locking.

______________________________________________________________________

## Question 78

How do

atomic operations

work?

______________________________________________________________________

## Question 79

What is

an Idempotency Key?

______________________________________________________________________

## Question 80

How do you

prevent

duplicate payments?

______________________________________________________________________

# Section 14

# Real-Time Systems

## Question 81

Why use

WebSockets?

______________________________________________________________________

## Question 82

WebSockets

vs

HTTP Polling.

______________________________________________________________________

## Question 83

How would you

design

WhatsApp?

______________________________________________________________________

## Question 84

How would you

track

driver locations

for Uber?

______________________________________________________________________

## Question 85

How would you

build

presence tracking?

______________________________________________________________________

# Section 15

# Search

## Question 86

How would you

design

Search Autocomplete?

______________________________________________________________________

## Question 87

Why use

Trie?

______________________________________________________________________

## Question 88

How would you

rank

search suggestions?

______________________________________________________________________

## Question 89

How would you

scale

search?

______________________________________________________________________

## Question 90

How would you

update

search indexes?

______________________________________________________________________

# Section 16

# Rate Limiting

## Question 91

Explain

Token Bucket.

______________________________________________________________________

## Question 92

Sliding Window

vs

Fixed Window.

______________________________________________________________________

## Question 93

How would you

build

a distributed

Rate Limiter?

______________________________________________________________________

## Question 94

Why use

Redis

for

Rate Limiting?

______________________________________________________________________

## Question 95

How would you

rate limit

login APIs?

______________________________________________________________________

# Section 17

# Notifications

## Question 96

How would you

design

a Notification System?

______________________________________________________________________

## Question 97

Why use

queues

for notifications?

______________________________________________________________________

## Question 98

How would you

retry

failed notifications?

______________________________________________________________________

## Question 99

What is

Exponential Backoff?

______________________________________________________________________

## Question 100

How would you

prevent

duplicate notifications?

______________________________________________________________________

# Section 18

# Complete Design Questions

## Question 101

Design Instagram.

______________________________________________________________________

## Question 102

Design WhatsApp.

______________________________________________________________________

## Question 103

Design Uber.

______________________________________________________________________

## Question 104

Design Netflix.

______________________________________________________________________

## Question 105

Design Amazon.

______________________________________________________________________

## Question 106

Design BookMyShow.

______________________________________________________________________

## Question 107

Design TinyURL.

______________________________________________________________________

## Question 108

Design Dropbox.

______________________________________________________________________

## Question 109

Design YouTube.

______________________________________________________________________

## Question 110

Design Google Drive.

______________________________________________________________________

## Question 111

Design Twitter (X).

______________________________________________________________________

## Question 112

Design Search Autocomplete.

______________________________________________________________________

## Question 113

Design Rate Limiter.

______________________________________________________________________

## Question 114

Design Distributed Cache.

______________________________________________________________________

## Question 115

Design Web Crawler.

______________________________________________________________________

## Question 116

Design URL Shortener.

______________________________________________________________________

## Question 117

Design Online Judge

(like LeetCode).

______________________________________________________________________

## Question 118

Design Food Delivery

Platform.

______________________________________________________________________

## Question 119

Design Ride Sharing

Platform.

______________________________________________________________________

## Question 120

Design Banking System.

______________________________________________________________________

# Section 19

# Advanced Follow-Up Questions

## Question 121

How would you

scale

your design

100×?

______________________________________________________________________

## Question 122

What is

the biggest

bottleneck

in your architecture?

______________________________________________________________________

## Question 123

How would you

monitor

your system?

______________________________________________________________________

## Question 124

What trade-offs

did you make?

______________________________________________________________________

## Question 125

What happens

if

Redis fails?

______________________________________________________________________

## Question 126

What happens

if

Kafka fails?

______________________________________________________________________

## Question 127

What happens

if

the database

becomes slow?

______________________________________________________________________

## Question 128

How would you

reduce

latency?

______________________________________________________________________

## Question 129

How would you

reduce

cost?

______________________________________________________________________

## Question 130

How would you

improve

availability?

______________________________________________________________________

# Final Challenge

Choose

one problem

at random.

Without

looking

at your notes,

design it

using

the interview framework.

Your explanation

should include

- Requirements
- Capacity Estimation
- APIs
- Data Model
- High-Level Architecture
- Deep Dive
- Scaling
- Monitoring
- Failure Handling
- Trade-offs

Target

a

45–60 minute

discussion,

just like

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

If you can confidently answer these **130 questions** and explain your reasoning clearly, you'll have strong coverage of
the most common topics asked in System Design interviews.

This question bank is intended for repeated practice. Revisit it regularly, explain your answers aloud, and refine your
thought process—not just the final architecture.

______________________________________________________________________

## Next

[Designing Multi-Tenant SaaS](37-designing-multi-tenant-saas.md)
