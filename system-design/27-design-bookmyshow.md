# System Design Case Study – BookMyShow

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design a large-scale movie ticket booking platform like BookMyShow by understanding seat reservation, concurrency control, distributed locking, payments, notifications, and scalability.

______________________________________________________________________

# Introduction

BookMyShow

is one of

the most common

System Design interviews.

Unlike

Amazon,

the biggest challenge

is

```
Preventing

Double Booking
```

Thousands

of users

may try

to book

the same seat

at the same time.

The system

must ensure

```
One Seat

↓

One Booking
```

______________________________________________________________________

# Step 1

# Clarify Requirements

Always

start by

asking questions.

Example

```
Movie Booking?
```

```
Seat Selection?
```

```
Seat Hold?
```

```
Payment?
```

```
Booking History?
```

```
Cancellation?
```

```
Refund?
```

______________________________________________________________________

# Functional Requirements

Assume

the system

supports

- Search movies
- Search theatres
- View show timings
- Select seats
- Book tickets
- Make payment
- Cancel booking
- Receive notifications

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Low Latency
- Strong Consistency
- No Double Booking
- Fault Tolerance
- Horizontal Scalability

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
50 Million Users
```

Daily bookings

```
5 Million
```

Peak

during

weekends

or

popular releases.

Example

```
100,000

Booking Requests

Per Minute
```

Traffic

is bursty.

______________________________________________________________________

# Step 3

# High-Level Architecture

```
                     Users
                        │
                        ▼
                      DNS
                        │
                        ▼
                 Load Balancer
                        │
                        ▼
                  API Gateway
                        │
 ┌──────────┬──────────┬──────────────┐
 ▼          ▼          ▼
Movie   Booking   Payment Service
Service Service
 │          │
 ▼          ▼
Database  Redis
 │          │
 ▼          ▼
 RabbitMQ / Kafka
        │
        ▼
Notification Service
```

______________________________________________________________________

# Core Services

Split

the platform

into

microservices.

- User Service
- Movie Service
- Theatre Service
- Show Service
- Booking Service
- Seat Service
- Payment Service
- Notification Service

______________________________________________________________________

# APIs

Search Movies

```
GET /movies
```

Show Details

```
GET /shows/{id}
```

Reserve Seats

```
POST /reserve
```

Checkout

```
POST /checkout
```

Cancel Ticket

```
POST /cancel
```

______________________________________________________________________

# Step 4

# Database Design

Movies

| id | title |

Theatres

| id | city |

Shows

| id | movie | theatre |

Seats

| id | show_id | status |

Bookings

| id | user | status |

Payments

| booking | status |

______________________________________________________________________

# Step 5

# Search

Searching

movies

is mostly

read-heavy.

Cache

popular movies

and

show timings.

______________________________________________________________________

# Step 6

# Seat Selection

User

opens

seat map.

```
Show

↓

Seat Layout

↓

Available Seats
```

Many users

may view

the same seats

simultaneously.

Viewing

does not

lock seats.

______________________________________________________________________

# Step 7

# The Biggest Challenge

Suppose

Seat A10

is available.

```
User A

Clicks

Book
```

At

the same time

```
User B

Clicks

Book
```

Both

see

the seat

as available.

Who wins?

______________________________________________________________________

# Wrong Solution

Simply

checking

availability

is not enough.

```
Check

↓

Available

↓

Book
```

Both users

may pass

the check.

Result

```
Double Booking
```

______________________________________________________________________

# Step 8

# Seat Reservation

Correct flow

```
Check Seat

↓

Temporarily Reserve

↓

Payment

↓

Confirm Booking
```

Other users

cannot reserve

the seat

while

it is held.

______________________________________________________________________

# Reservation Timeout

Interview favorite.

Suppose

a user

reserves

a seat

but never pays.

Should

the seat

remain blocked?

No.

Example

```
Reserve

↓

10 Minutes

↓

Expire

↓

Available Again
```

______________________________________________________________________

# Step 9

# Distributed Lock

Interview favorite.

Only

one request

should reserve

a seat.

Possible approaches

- Database row locking
- Optimistic locking
- Distributed locking
- Atomic updates

The choice

depends on

architecture

and scale.

______________________________________________________________________

# Example

```
Seat A10

↓

Lock Acquired

↓

Reserved

↓

Lock Released
```

Second request

must wait

or fail.

______________________________________________________________________

# Step 10

# Payment Flow

```
Reserve Seat

↓

Payment

↓

Booking Confirmed
```

If payment fails

```
Release Seat
```

______________________________________________________________________

# Step 11

# Saga Pattern

Booking

crosses

multiple services.

```
Reserve Seat

↓

Payment

↓

Booking
```

Use

Saga

with

compensation.

______________________________________________________________________

# Compensation

Payment Failed

↓

Release Seat

↓

Cancel Booking

______________________________________________________________________

# Step 12

# Booking Confirmation

After

successful payment

```
Booking Confirmed

↓

Queue

↓

Notification

↓

Email

↓

SMS
```

Notifications

should be

asynchronous.

______________________________________________________________________

# Step 13

# Caching

Redis

stores

- Movie list
- Show timings
- Seat availability cache
- User sessions

Be careful

that

cached seat data

must remain

consistent

with reservations.

______________________________________________________________________

# Step 14

# Database Replication

```
Primary

↓

Replica

↓

Replica
```

Searches

may use

replicas.

Critical booking

writes

go

to

the primary.

______________________________________________________________________

# Step 15

# Sharding

As

bookings grow,

shard

using

```
Booking ID

or

Theatre Region
```

Large cities

may naturally

map

to different

regional clusters.

______________________________________________________________________

# Step 16

# Queue Usage

Queues

are useful

for

- Notifications
- Analytics
- Invoice generation
- Recommendation
- Audit logs

______________________________________________________________________

# Step 17

# Monitoring

Monitor

- Booking latency
- Payment failures
- Seat reservation failures
- Queue length
- API latency
- Error rate

______________________________________________________________________

# Failure Scenarios

## Payment Failure

Release

reserved seats.

______________________________________________________________________

## Booking Service Failure

Retry

using

another instance.

______________________________________________________________________

## Redis Failure

Fallback

to

database

for

seat availability,

though

response times

may increase.

______________________________________________________________________

## Notification Failure

Booking

remains valid.

Notification

can be

retried later.

______________________________________________________________________

# CAP Discussion

Seat booking

requires

strong consistency.

Notifications

can be

eventually consistent.

Analytics

can also

be eventually consistent.

Different services

have

different requirements.

______________________________________________________________________

# Preventing Double Booking

Interview favorite.

Possible techniques

- Row-level locking
- Optimistic locking
- Atomic UPDATE statements
- Distributed locks

The goal

is

that

only one request

can successfully

reserve

a seat.

______________________________________________________________________

# Optimistic Locking

Example

Seat

contains

```
Version = 5
```

Two users

read

Version 5.

User A

updates

Version 6

successfully.

User B

tries

to update

Version 5.

Update fails.

User B

must retry.

______________________________________________________________________

# Pessimistic Locking

Acquire

a lock

before

updating

the seat.

Other transactions

must wait

until

the lock

is released.

Higher consistency,

but

lower concurrency.

______________________________________________________________________

# Typical Architecture

```
                     Users
                        │
                        ▼
                 Load Balancer
                        │
                        ▼
                  API Gateway
                        │
      ┌──────────┬─────────────┬────────────┐
      ▼          ▼             ▼
 Movie Service Booking Service Payment Service
      │          │             │
      ▼          ▼             ▼
 Database     Redis      RabbitMQ / Kafka
                   │
                   ▼
          Notification Service
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## How do you prevent double booking?

Reserve the seat using an atomic operation or locking mechanism before payment. Only one request should be able to
successfully reserve the seat.

______________________________________________________________________

## Why not lock the seat forever?

Users may abandon checkout. Temporary reservations with expiration prevent seats from remaining unavailable
indefinitely.

______________________________________________________________________

## Why use Redis?

Redis is useful for caching frequently accessed movie and show data, but the source of truth for seat reservations
should remain consistent with the booking system.

______________________________________________________________________

## Why use Saga?

Booking spans multiple services such as seat reservation and payment. Saga coordinates these local transactions and
releases seats if payment fails.

______________________________________________________________________

## What happens if payment succeeds but notification fails?

The booking remains successful. Notifications are asynchronous and can be retried independently.

______________________________________________________________________

# Common Mistakes

## Locking Seats Too Early

Only

lock seats

during

reservation,

not

when users

view

the seating layout.

______________________________________________________________________

## Holding Locks Too Long

Long-running locks

reduce

system throughput.

______________________________________________________________________

## Making Notifications Synchronous

Never

delay

booking confirmation

while waiting

for email

or SMS.

______________________________________________________________________

## Ignoring Reservation Expiry

Abandoned checkouts

must not

block seats forever.

______________________________________________________________________

## Trusting Cached Seat Data Alone

Always

validate

seat availability

using

the authoritative booking system.

______________________________________________________________________

# Best Practices

✅ Use temporary seat reservations.

✅ Set reservation expiration.

✅ Use Saga for checkout.

✅ Process notifications asynchronously.

✅ Cache search data, not booking decisions.

✅ Prevent double booking using atomic reservation logic.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the hardest part of designing BookMyShow?

### Answer

Preventing double booking while maintaining high throughput. Multiple users may attempt to reserve the same seat
simultaneously, requiring atomic reservation logic or appropriate locking mechanisms.

______________________________________________________________________

## Question

Why not reserve seats after payment?

### Answer

If payment succeeds before the seat is reserved, another user may already have booked the seat. Reserving first ensures
availability before charging the customer.

______________________________________________________________________

## Question

Would you use optimistic or pessimistic locking?

### Answer

It depends on contention. Optimistic locking works well when conflicts are rare, while pessimistic locking is
appropriate when contention is high and preventing conflicts is more important than maximizing concurrency.

______________________________________________________________________

# Practice Exercise

Design BookMyShow

for

100 Million Users.

Explain

1. API design
1. Capacity estimation
1. Seat reservation
1. Locking strategy
1. Payment workflow
1. Saga implementation
1. Caching
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Trade-offs

Present

your solution

within

45–60 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

BookMyShow is one of the best interview problems for understanding concurrency and consistency.

A strong solution should demonstrate

- Requirement gathering
- Capacity estimation
- Seat reservation
- Locking strategies
- Payment workflow
- Saga Pattern
- Caching
- Replication
- Sharding
- High availability
- Trade-off analysis

Mastering BookMyShow prepares you for interviews involving reservation systems, inventory management, ticketing
platforms, and other high-concurrency transactional systems.

______________________________________________________________________

# Next

[System Design – Rate Limiter](28-design-rate-limiter.md)
