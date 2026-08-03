# System Design - Part 79

# Uber System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Real-Time Location Tracking
- Driver Matching
- Geospatial Indexing
- ETA Calculation
- Ride Lifecycle
- Surge Pricing
- Trip Storage
- Payments
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Uber.**

Unlike

YouTube

or

Google Drive,

Uber

is a

real-time,

location-based

distributed system.

The biggest challenges

are:

- Millions of moving drivers
- Real-time matching
- Low-latency updates
- Accurate ETA
- Dynamic pricing

Every second,

drivers

change location.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Register/Login
- Book a ride
- Find nearby drivers
- Accept/Reject rides
- Live location tracking
- Ride status updates
- Payments
- Trip history
- Ratings

Optional

- Ride sharing
- Scheduled rides
- Food delivery

______________________________________________________________________

# Non-Functional Requirements

- Very low latency
- High availability
- Real-time updates
- Accurate driver matching
- Massive scalability

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Uber has

200 Million users.

Daily Active Users

```text id="uber7901"
80 Million
```

Active Drivers

```text id="uber7902"
8 Million
```

Location Updates

```text id="uber7903"
10/sec per driver
```

Total Location Updates

```text id="uber7904"
≈80 Million updates/sec
```

Observation.

The largest workload

is

continuous

location updates,

not

ride creation.

______________________________________________________________________

# Step 3

# API Design

Request Ride

```http id="uber7905"
POST /rides
```

______________________________________________________________________

Nearby Drivers

```http id="uber7906"
GET /drivers/nearby
```

______________________________________________________________________

Driver Location Update

```http id="uber7907"
POST /drivers/location
```

______________________________________________________________________

Accept Ride

```http id="uber7908"
POST /rides/{id}/accept
```

______________________________________________________________________

Ride Status

```http id="uber7909"
GET /rides/{id}
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="uber7910"
Passenger App

↓

API Gateway

↓

Ride Service

↓

Matching Service

↓

Driver Service

↓

Payment Service
```

Supporting services:

- Location Service
- Notification Service
- Pricing Service
- ETA Service

______________________________________________________________________

# Real-Time Location Tracking

Interview favorite.

Every driver

sends

their GPS location

every few seconds.

```text id="uber7911"
Driver

↓

Latitude

Longitude

↓

Location Service
```

These updates

are

temporary.

They should

not

be stored

immediately

inside

the main database.

______________________________________________________________________

# Where to Store Locations?

Current locations

change

every few seconds.

Store them

inside

Redis

or

an in-memory

location store.

Historical trips

belong

in

the database.

______________________________________________________________________

# Geospatial Indexing

Interview favorite.

Question.

How do

we quickly find

drivers

within

2 km

of a passenger?

Scanning

millions

of drivers

is impossible.

Use

Geospatial Indexing.

Popular approaches:

- GeoHash
- QuadTree
- R-Tree
- S2 Geometry

______________________________________________________________________

# GeoHash

Interview favorite.

GeoHash

converts

latitude

and

longitude

into

a string.

Example

```text id="uber7912"
12.9716

77.5946

↓

tdr1v9
```

Nearby locations

produce

similar prefixes.

This enables

fast

"nearby driver"

queries.

______________________________________________________________________

# Driver Matching

Workflow

```text id="uber7913"
Passenger

↓

Nearby Drivers

↓

ETA

↓

Choose Best Driver

↓

Offer Ride
```

Matching

considers:

- Distance
- ETA
- Driver Rating
- Vehicle Type
- Driver Availability

______________________________________________________________________

# Ride Lifecycle

Interview favorite.

A ride

moves through

multiple states.

```text id="uber7914"
Requested

↓

Accepted

↓

Driver Arriving

↓

Trip Started

↓

Trip Completed

↓

Payment
```

State transitions

must be

consistent.

______________________________________________________________________

# ETA Calculation

ETA

is not

simply

straight-line distance.

Inputs include:

- Traffic
- Road Network
- Speed Limits
- Historical Data
- Live Congestion

Many companies

use

mapping engines

to compute ETAs.

______________________________________________________________________

# Surge Pricing

Interview favorite.

Suppose

100 passengers

request rides,

but

only

20 drivers

are available.

Demand

exceeds

supply.

Increase prices.

```text id="uber7915"
Demand

>

Supply

↓

Surge
```

This encourages

more drivers

to become available.

______________________________________________________________________

# Notifications

Ride events

are asynchronous.

```text id="uber7916"
Ride Accepted

↓

Kafka

↓

Notification Service

↓

Passenger
```

Examples:

- Driver accepted
- Driver arrived
- Trip started
- Payment completed

______________________________________________________________________

# Live Ride Tracking

Passenger

and

driver

maintain

WebSocket

connections.

```text id="uber7917"
Passenger

↔

WebSocket

↔

Driver
```

Location updates

are pushed

in real time.

Polling

would generate

too much traffic.

______________________________________________________________________

# Trip Storage

Database Schema

```text id="uber7918"
trip_id

driver_id

passenger_id

pickup

destination

fare

status

created_at
```

Trips

are immutable

after completion,

making them

ideal

for analytics.

______________________________________________________________________

# Payments

After

trip completion,

publish

an event.

```text id="uber7919"
Trip Completed

↓

Kafka

↓

Payment Service
```

Payment processing

is independent

from

ride tracking.

Retries

can occur

without

affecting

the trip.

______________________________________________________________________

# Caching

Redis stores:

- Driver locations
- Driver availability
- Active rides
- ETA cache
- Surge pricing cache

Trip history

remains

inside

the database.

______________________________________________________________________

# Scaling

Scale independently:

- Matching Service
- Location Service
- Ride Service
- Payment Service
- Notification Service

Location updates

may require

partitioning

by

geographical region.

______________________________________________________________________

# AI/ML Example

Uber

uses ML

for:

- ETA prediction
- Driver matching
- Demand forecasting
- Surge pricing
- Fraud detection
- Route optimization

Models

continuously learn

from

historical trips.

______________________________________________________________________

# Failure Scenario

Suppose

the Matching Service

fails.

Passengers

can still

open the app,

but

new rides

cannot

be assigned.

Existing trips

continue

normally.

______________________________________________________________________

# Another Failure

Suppose

the Location Service

fails.

Existing trips

continue

using

the last known

driver location.

Drivers

retry

location updates

until

the service

recovers.

______________________________________________________________________

# End-to-End Architecture

```text id="uber7920"
Passenger App

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Ride Service

↓

Matching Service

↓

Location Service

↓

Redis (Geo)

↓

PostgreSQL

↓

Kafka

↓

Notification Service

↓

Payment Service

↓

Analytics Service
```

______________________________________________________________________

# Trade-offs

GeoHash

vs

Database Scan

| GeoHash | Database Scan |
| ------------------ | --------------- |
| Milliseconds | Very slow |
| Scalable | Doesn't scale |
| Geospatial queries | Full table scan |

______________________________________________________________________

WebSockets

vs

Polling

| WebSockets | Polling |
| ---------------------- | ----------------------- |
| Real-time | Delayed |
| Persistent connection | Repeated requests |
| Better user experience | Higher request overhead |

______________________________________________________________________

Redis

vs

Database

| Redis | Database |
| ------------------ | ------------------ |
| Live locations | Trip history |
| In-memory | Durable |
| Millisecond access | Persistent storage |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Uber?

Start by separating rapidly changing location data from durable trip data. Store live driver locations in an in-memory
geospatial store such as Redis using GeoHash-based indexing, while storing completed trips in a relational database.
When a passenger requests a ride, the Matching Service queries nearby drivers using geospatial indexes, calculates ETAs,
and selects the best driver based on distance, availability, and ratings. Use WebSockets for real-time ride tracking,
Kafka for asynchronous notifications and payment processing, Redis for caching active rides and surge pricing, and
deploy services independently so that matching, location tracking, payments, and notifications can scale based on
demand.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Geospatial indexing
- GeoHash
- Driver matching
- ETA calculation
- Surge pricing
- Ride lifecycle
- Live tracking
- Payments
- Scaling
- Trade-offs

______________________________________________________________________

# 🧠 Real System Design Progress

You have completed:

- ✅ TinyURL
- ✅ WhatsApp
- ✅ Instagram
- ✅ Twitter/X
- ✅ YouTube
- ✅ Netflix
- ✅ Spotify
- ✅ Google Drive
- ✅ Uber

You now understand one of the most complex real-time location-based distributed systems.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design one of the most common large-scale commerce systems:

- Product catalog
- Inventory management
- Shopping cart
- Checkout
- Orders
- Payments
- Search
- Recommendations

We'll design **Amazon**.

______________________________________________________________________

# What's Next

[Amazon System Design](80-amazon-system-design.md)
