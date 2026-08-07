# System Design Case Study – Amazon (E-Commerce Platform)

> Target Audience: Software Engineers with 3–8 years of experience
>
> Goal: Learn how to design a large-scale e-commerce platform like Amazon by applying concepts such as microservices, search, inventory management, shopping carts, checkout, payments, caching, distributed transactions, message queues, and distributed systems.

______________________________________________________________________

# Introduction

Amazon

is one of

the most comprehensive

System Design interviews.

It combines

almost every concept

covered

in this course.

- Microservices
- Distributed Databases
- Search
- Caching
- Inventory
- Payments
- Shopping Cart
- Order Processing
- Message Queues
- Distributed Transactions
- Recommendation Engine
- High Availability

Unlike

Netflix,

which is

read-heavy,

Amazon

must efficiently handle

both

heavy reads

and

critical writes.

______________________________________________________________________

# Step 1

# Clarify Requirements

Before

drawing architecture,

ask questions.

Example

```
User Registration?
```

```
Product Search?
```

```
Shopping Cart?
```

```
Checkout?
```

```
Payments?
```

```
Order Tracking?
```

```
Seller Support?
```

```
Recommendations?
```

______________________________________________________________________

# Functional Requirements

Assume

Amazon supports

- User registration
- Product search
- Product details
- Shopping cart
- Checkout
- Payment
- Order history
- Inventory management
- Reviews
- Recommendations

______________________________________________________________________

# Non-Functional Requirements

Need

- High Availability
- Low Latency
- Massive Scalability
- Strong Consistency for Orders
- Fault Tolerance
- Horizontal Scaling

______________________________________________________________________

# Step 2

# Capacity Estimation

Assumptions

```
400 Million Users
```

```
150 Million DAU
```

Daily Orders

```
20 Million
```

Product Catalog

```
500 Million Products
```

Searches

```
Billions/day
```

Clearly

Search

and

Caching

are critical.

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
 ┌────────┬────────┬─────────┬────────────┐
 ▼        ▼        ▼         ▼
Search  Product  Cart   Order Service
Service Service Service
 │        │        │         │
 ▼        ▼        ▼         ▼
Elastic  Redis   Redis   Database
Search
 │                          │
 ▼                          ▼
Inventory Service     RabbitMQ / Kafka
                        │
                        ▼
Payment Service   Notification Service
```

______________________________________________________________________

# Core Services

Separate

the platform

into

microservices.

- User Service
- Product Service
- Search Service
- Cart Service
- Inventory Service
- Order Service
- Payment Service
- Recommendation Service
- Review Service
- Notification Service

______________________________________________________________________

# APIs

Search

```
GET /products?q=laptop
```

Product

```
GET /products/{id}
```

Cart

```
POST /cart
```

Checkout

```
POST /checkout
```

Orders

```
GET /orders/{id}
```

______________________________________________________________________

# Step 4

# Product Catalog

Products

| id | title | brand | price |

Inventory

| product_id | stock |

Reviews

| user | product | rating |

Orders

| order_id | status |

______________________________________________________________________

# Step 5

# Product Search

Interview favorite.

Searching

millions

of products

using SQL

is expensive.

Instead

```
Search Service

↓

Elasticsearch
```

Provides

- Full-text search
- Ranking
- Filtering
- Faceting
- Auto-complete

______________________________________________________________________

# Step 6

# Product Page

When

opening

a product

retrieve

- Product details
- Images
- Price
- Stock
- Reviews
- Recommendations

Many responses

can be

cached.

______________________________________________________________________

# Step 7

# Shopping Cart

Interview favorite.

Cart

is temporary.

Excellent candidate

for

Redis.

```
User

↓

Redis

↓

Shopping Cart
```

Fast

reads

and

updates.

______________________________________________________________________

# Why Redis?

Shopping carts

change frequently.

Keeping them

in memory

provides

excellent performance.

Periodic persistence

or backup

may also

be used,

depending on

business requirements.

______________________________________________________________________

# Step 8

# Checkout

Checkout

is

the most important

workflow.

```
Cart

↓

Inventory

↓

Payment

↓

Order

↓

Notification
```

______________________________________________________________________

# Step 9

# Inventory Reservation

Interview favorite.

Suppose

only

one laptop

remains.

Two users

click

Buy Now

simultaneously.

Without

proper handling,

both orders

may succeed.

```
Overselling
```

______________________________________________________________________

# Solution

Reserve inventory

before

payment.

```
Reserve Stock

↓

Payment

↓

Confirm Order
```

If

payment fails

```
Release Stock
```

______________________________________________________________________

# Step 10

# Distributed Transaction

Checkout

involves

multiple services.

```
Inventory

↓

Payment

↓

Order
```

Use

```
Saga Pattern
```

with

compensation.

______________________________________________________________________

# Compensation

Inventory Reserved

↓

Payment Failed

↓

Release Inventory

↓

Cancel Order

______________________________________________________________________

# Step 11

# Payments

Payments

must be

isolated.

```
Checkout

↓

Payment Service

↓

Payment Gateway

↓

Success
```

Payment Service

should never

contain

inventory logic.

______________________________________________________________________

# Step 12

# Order Processing

After payment

```
Create Order

↓

Queue

↓

Warehouse

↓

Shipping

↓

Notification
```

Everything

after payment

can be

asynchronous.

______________________________________________________________________

# Step 13

# Message Queue

Used for

- Warehouse
- Shipping
- Notifications
- Emails
- Analytics
- Recommendations

______________________________________________________________________

# Step 14

# Notifications

```
Order Placed

↓

Kafka / RabbitMQ

↓

Notification Service

↓

Email

↓

SMS

↓

Push
```

Customer

doesn't wait

for

notification delivery.

______________________________________________________________________

# Step 15

# Caching

Redis

stores

- Product details
- Popular products
- Shopping carts
- User sessions
- Recommendations

______________________________________________________________________

# Step 16

# CDN

Product images

should be served

through

a CDN.

```
User

↓

CDN

↓

Object Storage
```

______________________________________________________________________

# Step 17

# Recommendation Engine

Recommendations

are generated

using

- Purchase history
- Browsing history
- Similar users
- Trending products

Updated

asynchronously.

______________________________________________________________________

# Step 18

# Database Replication

```
Primary

↓

Replica

↓

Replica
```

Reads

go

to replicas.

Writes

go

to primary.

______________________________________________________________________

# Step 19

# Database Sharding

Eventually

billions

of orders

exist.

Shard

using

```
Customer ID

or

Order ID
```

______________________________________________________________________

# Step 20

# Search Index Updates

Suppose

seller

changes

product price.

```
Database Updated

↓

Event

↓

Search Index Updated
```

Eventually

search

reflects

the latest data.

______________________________________________________________________

# Step 21

# Monitoring

Monitor

- Checkout latency
- Payment failures
- Search latency
- Inventory accuracy
- Cache hit ratio
- Order completion
- Queue length

______________________________________________________________________

# Failure Scenarios

## Redis Failure

Shopping carts

can be

recovered

from

persistent storage,

if implemented,

though

performance

may temporarily decrease.

______________________________________________________________________

## Payment Failure

Use

Saga

to

release inventory.

______________________________________________________________________

## Search Failure

Fallback

to

database search

with

reduced functionality,

or return

cached/popular results,

depending on

business requirements.

______________________________________________________________________

## Inventory Failure

Reject

new purchases

until

inventory

is available.

______________________________________________________________________

# CAP Discussion

Inventory

requires

strong consistency.

Recommendations

can be

eventually consistent.

Search indexing

can also

be eventually consistent.

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
 ┌──────────┬────────────┬───────────────┐
 ▼          ▼            ▼               ▼
Search   Product      Cart         Order Service
 │          │            │               │
 ▼          ▼            ▼               ▼
Elastic   Database     Redis      Inventory Service
Search                                  │
                                        ▼
                                  Payment Service
                                        │
                                        ▼
                                 RabbitMQ / Kafka
                                        │
        ┌───────────────────────────────┼──────────────────────┐
        ▼                               ▼                      ▼
 Notification Service           Warehouse Service      Analytics
```

______________________________________________________________________

# Common Interview Follow-Up Questions

## Why store the shopping cart in Redis?

Shopping carts are temporary, frequently updated, and require very fast reads and writes. Redis provides low-latency
in-memory storage, making it a strong fit.

______________________________________________________________________

## Why use Elasticsearch?

Product search requires full-text search, filtering, ranking, typo tolerance, and faceted navigation, which traditional
relational databases are not optimized to provide at large scale.

______________________________________________________________________

## How do you prevent overselling?

Reserve inventory using an atomic operation before payment. If payment fails, release the reserved inventory through a
compensation step.

______________________________________________________________________

## Why use Saga during checkout?

Checkout spans multiple independent services. Saga coordinates local transactions with compensation, avoiding the
scalability limitations of distributed ACID transactions.

______________________________________________________________________

## Why are notifications asynchronous?

Customers should receive order confirmation quickly. Email, SMS, and push notifications can be processed later through a
message queue.

______________________________________________________________________

# Common Mistakes

## Putting Everything Inside Checkout

Checkout

should coordinate

services,

not contain

all business logic.

______________________________________________________________________

## Updating Search Directly

Use

events

to update

the search index.

______________________________________________________________________

## Ignoring Inventory Reservation

Concurrent purchases

can cause

overselling.

______________________________________________________________________

## Synchronous Notifications

Always

process

notifications

asynchronously.

______________________________________________________________________

## Ignoring Caching

Popular products

should be

cached.

______________________________________________________________________

# Best Practices

✅ Use Redis for shopping carts.

✅ Use Elasticsearch for product search.

✅ Reserve inventory before payment.

✅ Use Saga for checkout.

✅ Use queues for post-order processing.

✅ Cache product information.

______________________________________________________________________

# Interview Deep Dive

## Question

Why shouldn't shopping carts be stored only in MySQL?

### Answer

Shopping carts experience frequent reads and updates. Redis provides much lower latency than disk-based databases and is
well suited for temporary session-like data.

______________________________________________________________________

## Question

How do you handle inventory when multiple users purchase the last item?

### Answer

Use an atomic inventory reservation mechanism before payment. Only one reservation should succeed. If payment fails,
release the reserved inventory using a compensation transaction.

______________________________________________________________________

## Question

What is the hardest part of designing Amazon?

### Answer

The checkout workflow is the most challenging because it coordinates inventory, payment, order creation, and
notifications while maintaining consistency, preventing overselling, and remaining highly available.

______________________________________________________________________

# Practice Exercise

Design Amazon

for

1 Billion Users.

Explain

1. API design
1. Capacity estimation
1. Product search
1. Shopping cart
1. Inventory reservation
1. Checkout workflow
1. Payment processing
1. Replication
1. Sharding
1. Monitoring
1. Failure recovery
1. Trade-offs

Present

your complete solution

within

60 minutes,

similar to

a real

Senior Software Engineer

System Design interview.

______________________________________________________________________

# Summary

Amazon is one of the richest System Design case studies because it combines

- Search
- Shopping carts
- Inventory management
- Payments
- Distributed transactions
- Recommendations
- Event-driven architecture
- Caching
- Replication
- Sharding
- High availability

Mastering Amazon prepares you for designing large-scale transactional systems and demonstrates a deep understanding of
distributed systems.

______________________________________________________________________

# Next

[System Design Case Study – BookMyShow](27-design-bookmyshow.md)
