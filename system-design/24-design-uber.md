# System Design Case Study – Uber

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design a large-scale ride-sharing platform like Uber by applying concepts such as geospatial indexing, location tracking, matching algorithms, event-driven architecture, caching, messaging, and distributed systems.

______________________________________________________________________

# Introduction

Uber

is one of

the most challenging

System Design interviews.

Unlike

Instagram

or

WhatsApp,

Uber deals with

```
Real-Time Location
```

The system

must continuously

track

millions of drivers,

find

the nearest driver,

calculate

routes,

handle

payments,

and

support

high availability.

______________________________________________________________________

# Step 1

# Clarify Requirements

Before

drawing architecture,

ask questions.

Example

```
Ride Booking?
```

```
Ride Cancellation?
```

```
Live Driver Tracking?
```

```
Estimated Fare?
```

```
Ride History?
```

```
Payments?
```

```
Ratings?
```

______________________________________________________________________

# Functional Requirements

Assume

Uber supports

- Rider registration
- Driver registration
- Driver location updates
- Ride booking
- Driver matching
- Live ride tracking
- Payments
- Ratings
- Ride history

______________________________________________________________________

# Non-Functional Requirements

Need

- Very low latency
- High availability
- Massive scalability
- Fault tolerance
- Accurate location updates
- Real-time communication

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
200 Million Users
```

```
10 Million Drivers
```

Suppose

each driver

sends

location updates

every

```
5 Seconds
```

Location updates

per second

```
≈2 Million/sec
```

This is

one of

Uber's biggest challenges.

______________________________________________________________________

# Ride Requests

Assume

```
30 Million Rides/day
```

Average

```
≈350 Rides/sec
```

Peak

may reach

several thousand

ride requests

per second.

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
      ┌──────────┬────────────┬────────────┐
      ▼          ▼            ▼
 Rider API  Driver API   Matching Service
      │          │            │
      ▼          ▼            ▼
 Redis      Location DB   Message Queue
      │                       │
      ▼                       ▼
 Payment Service       Notification Service
```

______________________________________________________________________

# Core Services

Split

the platform

into

independent services.

- User Service
- Driver Service
- Location Service
- Matching Service
- Ride Service
- Payment Service
- Notification Service
- Pricing Service
- Rating Service

______________________________________________________________________

# APIs

Book Ride

```
POST /rides
```

Update Location

```
POST /drivers/location
```

Ride Status

```
GET /rides/{id}
```

Cancel Ride

```
POST /rides/{id}/cancel
```

______________________________________________________________________

# Step 4

# Database Design

Drivers

| id | status | vehicle |

Rides

| id | rider | driver | status |

Locations

| driver_id | latitude | longitude | timestamp |

Payments

| ride_id | amount | status |

______________________________________________________________________

# Step 5

# Driver Location Updates

Drivers

send

GPS coordinates

every few seconds.

```
Driver

↓

Location Service

↓

Redis

↓

Geospatial Database
```

Location data

changes frequently.

______________________________________________________________________

# Why Redis?

Redis

supports

geospatial indexing

using

Geo commands,

making

nearby driver lookups

very fast.

______________________________________________________________________

# Step 6

# Geospatial Search

Interview favorite.

Suppose

a rider

requests

a ride.

```
Current Location

↓

Find Drivers

Within

5 km
```

Nearby drivers

are returned

almost instantly.

______________________________________________________________________

# Geohashing

Interview bonus.

Earth

is divided

into

small grids.

Nearby locations

often share

similar prefixes.

This allows

efficient

location-based searches.

Many systems

also use

spatial indexes

such as

R-trees,

QuadTrees,

or

S2 Geometry,

depending on

the technology stack.

______________________________________________________________________

# Step 7

# Driver Matching

Matching Service

finds

the best driver.

Factors

include

- Distance
- Driver availability
- Driver rating
- Vehicle type
- Estimated arrival time

______________________________________________________________________

# Matching Flow

```
Ride Request

↓

Nearby Drivers

↓

Rank Drivers

↓

Send Request

↓

Driver Accepts

↓

Ride Created
```

______________________________________________________________________

# Step 8

# Driver Acceptance

Suppose

the nearest driver

doesn't respond.

```
Driver A

↓

Timeout

↓

Driver B

↓

Timeout

↓

Driver C
```

Continue

until

someone accepts.

______________________________________________________________________

# Step 9

# Notifications

Ride requests

should be

asynchronous.

```
Matching Service

↓

RabbitMQ / Kafka

↓

Push Notification

↓

Driver
```

______________________________________________________________________

# Step 10

# Live Tracking

During

the ride,

driver locations

continue

to update.

```
Driver

↓

WebSocket

↓

Passenger
```

Real-time

movement.

______________________________________________________________________

# Why WebSockets?

Persistent

bidirectional communication

reduces latency

and avoids

continuous polling.

______________________________________________________________________

# Step 11

# Pricing Service

Estimated fare

depends on

- Distance
- Time
- Traffic
- Surge pricing

Pricing

should be

a separate service.

______________________________________________________________________

# Surge Pricing

Suppose

demand

exceeds

available drivers.

```
Demand ↑

Supply ↓

↓

Multiplier
```

Example

```
1.8×

```

Pricing

changes dynamically.

______________________________________________________________________

# Step 12

# Payments

After

ride completion

```
Ride Finished

↓

Payment Service

↓

Gateway

↓

Receipt
```

Payment processing

should be

independent

from

ride management.

______________________________________________________________________

# Step 13

# Ride Status

Typical flow

```
Requested

↓

Matched

↓

Driver Arriving

↓

Started

↓

Completed
```

Each transition

is

an event.

______________________________________________________________________

# Step 14

# Ratings

After

ride completion

both

driver

and rider

submit ratings.

```
Rating

↓

Database

↓

Driver Score Updated
```

______________________________________________________________________

# Step 15

# Caching

Redis

stores

- Driver locations
- Ride status
- Frequently accessed user profiles
- Surge pricing
- Session tokens

______________________________________________________________________

# Step 16

# Replication

```
Primary

↓

Replica

↓

Replica
```

Provides

high availability

for

ride history

and user data.

______________________________________________________________________

# Step 17

# Sharding

Eventually

billions

of rides

exist.

Shard

using

```
Ride ID

or

Region
```

Regional sharding

is common

because

rides

are naturally

location-based.

______________________________________________________________________

# Step 18

# Event-Driven Architecture

Ride lifecycle

produces events.

```
Ride Requested

↓

Ride Accepted

↓

Ride Started

↓

Ride Completed
```

Consumers

include

- Payments
- Notifications
- Analytics
- Fraud Detection

______________________________________________________________________

# Step 19

# Monitoring

Monitor

- Driver availability
- Matching latency
- Ride success rate
- GPS update delay
- API latency
- Payment failures

______________________________________________________________________

# Failure Scenarios

## Driver Disconnects

Driver

stops sending

location updates.

System

marks

driver

offline

after

a timeout.

______________________________________________________________________

## Matching Service Failure

Retry

matching

using

another instance.

______________________________________________________________________

## Redis Failure

Fallback

to

persistent storage,

though

nearby searches

become slower.

______________________________________________________________________

## Payment Failure

Ride

can still

complete.

Payment

may be

retried

or collected later,

depending on

business policy.

______________________________________________________________________

# CAP Discussion

Location updates

favor

Availability.

Small delays

are acceptable.

Payment

requires

strong consistency.

Different services

choose

different trade-offs.

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
      ┌──────────┬────────────┬────────────┐
      ▼          ▼            ▼
 Rider API  Driver API   Matching Service
      │          │            │
      ▼          ▼            ▼
 Redis Geo   Ride DB    RabbitMQ / Kafka
      │          │            │
      ▼          ▼            ▼
 Location DB Payment Service Notification Service
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why use Redis for driver locations?

Redis provides fast in-memory geospatial indexing, making nearby driver searches extremely efficient.

______________________________________________________________________

## Why not store GPS updates directly in SQL?

Driver locations change every few seconds. Constant updates would overload a traditional relational database. In-memory
storage is better suited for rapidly changing location data.

______________________________________________________________________

## How do you find the nearest driver?

Use a geospatial index to retrieve nearby drivers, then rank candidates based on distance, estimated arrival time,
availability, and other business rules.

______________________________________________________________________

## How do you prevent two riders from getting the same driver?

Use distributed locking or an atomic reservation mechanism so only one ride request can successfully assign a driver at
a time.

______________________________________________________________________

## How is surge pricing calculated?

Surge pricing is based on business rules that consider demand, available drivers, time, location, and other operational
factors.

______________________________________________________________________

# Common Mistakes

## Storing Live Locations In SQL

Use

an in-memory

geospatial solution

for

rapid updates.

______________________________________________________________________

## Ignoring Matching Latency

Driver matching

must happen

within

a few seconds.

______________________________________________________________________

## Forgetting Driver Availability

Only

available drivers

should participate

in matching.

______________________________________________________________________

## Tight Coupling

Payments,

notifications,

and analytics

should communicate

through events.

______________________________________________________________________

## Ignoring Concurrency

Multiple riders

may request

the same driver.

Atomic assignment

is essential.

______________________________________________________________________

# Best Practices

✅ Use geospatial indexing for nearby searches.

✅ Cache rapidly changing location data.

✅ Keep matching stateless and horizontally scalable.

✅ Use asynchronous notifications.

✅ Separate ride management from payment processing.

✅ Monitor matching latency continuously.

______________________________________________________________________

# Interview Deep Dive

## Question

How do you efficiently find nearby drivers?

### Answer

Store active driver locations in a geospatial index such as Redis GEO or another spatial indexing solution. Query for
drivers within a specified radius and rank them using business rules like distance, ETA, and availability.

______________________________________________________________________

## Question

Why shouldn't GPS updates go directly into MySQL?

### Answer

Driver locations change frequently, resulting in extremely high write rates. An in-memory geospatial store is better
suited for rapid updates and low-latency location queries, while persistent storage can be used for historical ride
data.

______________________________________________________________________

## Question

What is the hardest part of designing Uber?

### Answer

Real-time driver matching at scale is one of the biggest challenges. The system must quickly locate nearby drivers,
avoid assigning the same driver twice, handle continuous location updates, and remain highly available under heavy load.

______________________________________________________________________

# Practice Exercise

Design Uber

for

500 Million Users.

Explain

1. API design
1. Capacity estimation
1. Location tracking
1. Driver matching
1. Geospatial indexing
1. Payment architecture
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Surge pricing
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

Uber is one of the most comprehensive System Design problems because it combines

- Real-time location tracking
- Geospatial indexing
- Matching algorithms
- WebSockets
- Event-driven architecture
- Caching
- Payments
- Replication
- Sharding
- High availability

Mastering Uber prepares you for designing many location-aware and real-time distributed systems while demonstrating
strong System Design reasoning.

______________________________________________________________________

# Next

[System Design Case Study – Netflix](25-design-netflix.md)
