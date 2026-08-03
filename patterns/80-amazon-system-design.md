# System Design - Part 80

# Amazon E-Commerce System Design

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- Requirement gathering
- Capacity estimation
- API design
- High-Level Architecture
- Product Catalog
- Inventory Management
- Shopping Cart
- Checkout
- Order Processing
- Payment Integration
- Search
- Recommendations
- Scaling
- Trade-offs

______________________________________________________________________

# Before We Start

The interviewer says:

> **Design Amazon.**

Amazon

is much more

than

an online store.

It combines:

- Product Catalog
- Inventory
- Shopping Cart
- Orders
- Payments
- Recommendations
- Search
- Warehouses
- Delivery

Unlike Uber,

most operations

are

transactional.

Consistency

is critical.

______________________________________________________________________

# Step 1

# Clarify Requirements

Functional Requirements

- Browse products
- Search products
- Add to cart
- Remove from cart
- Checkout
- Payments
- Order tracking
- Reviews
- Recommendations

Optional

- Wishlist
- Coupons
- Returns
- Subscriptions

______________________________________________________________________

# Non-Functional Requirements

- High availability
- High scalability
- Strong consistency for orders
- Low search latency
- High durability

______________________________________________________________________

# Step 2

# Capacity Estimation

Suppose

Amazon has

400 Million users.

Daily Active Users

```text id="am8001"
120 Million
```

Orders

per day

```text id="am8002"
50 Million
```

Product Catalog

```text id="am8003"
1 Billion Products
```

Search Requests

```text id="am8004"
Several Billion/day
```

Observation.

Search

is read-heavy.

Checkout

is consistency-heavy.

______________________________________________________________________

# Step 3

# API Design

Search Products

```http id="am8005"
GET /products?q=laptop
```

______________________________________________________________________

Product Details

```http id="am8006"
GET /products/{id}
```

______________________________________________________________________

Add to Cart

```http id="am8007"
POST /cart/items
```

______________________________________________________________________

Checkout

```http id="am8008"
POST /checkout
```

______________________________________________________________________

Order Details

```http id="am8009"
GET /orders/{id}
```

______________________________________________________________________

# Step 4

# High-Level Architecture

```text id="am8010"
Customer

↓

API Gateway

↓

Catalog Service

↓

Cart Service

↓

Order Service

↓

Payment Service
```

Supporting services:

- Inventory Service
- Recommendation Service
- Search Service
- Notification Service
- Shipping Service

______________________________________________________________________

# Product Catalog

Interview favorite.

Product information

includes:

- Name
- Description
- Images
- Price
- Category
- Seller

Schema

```text id="am8011"
product_id

title

price

category

seller_id
```

Product images

should be stored

in

Object Storage,

not

the database.

______________________________________________________________________

# Search

Interview favorite.

Searching

billions

of products

using SQL

is slow.

Instead,

use

Elasticsearch

or

OpenSearch.

Search supports:

- Keywords
- Filters
- Categories
- Brands
- Price ranges

______________________________________________________________________

# Shopping Cart

Each user

has

their own cart.

Schema

```text id="am8012"
cart_id

user_id

product_id

quantity
```

Cart data

is temporary.

It is often

stored in

Redis

for fast access,

with periodic persistence

to a database.

______________________________________________________________________

# Inventory Management

Interview favorite.

Suppose

only

one laptop

remains.

Two customers

click

"Buy Now"

at

the same time.

Question.

Who gets it?

Inventory

must prevent

overselling.

______________________________________________________________________

# Inventory Reservation

Workflow

```text id="am8013"
Checkout

↓

Reserve Inventory

↓

Payment

↓

Confirm Order
```

If

payment fails,

release

the reserved inventory.

This avoids

locking stock

for too long.

______________________________________________________________________

# Checkout Flow

```text id="am8014"
Cart

↓

Inventory Check

↓

Payment

↓

Order Created

↓

Notification
```

Every step

must succeed

or

be compensated.

______________________________________________________________________

# Order Service

Schema

```text id="am8015"
order_id

user_id

status

amount

created_at
```

Order Status

```text id="am8016"
Created

↓

Paid

↓

Packed

↓

Shipped

↓

Delivered
```

Each transition

is tracked.

______________________________________________________________________

# Payment Integration

Interview favorite.

The Order Service

should **not**

process

payments directly.

Workflow

```text id="am8017"
Checkout

↓

Payment Gateway

↓

Success

↓

Create Order
```

Payment logic

is isolated

inside

the Payment Service.

______________________________________________________________________

# Saga Pattern

Interview favorite.

Checkout

involves

multiple services.

```text id="am8018"
Inventory

↓

Payment

↓

Order

↓

Shipping
```

If

Shipping fails,

the system

may need

to:

- Cancel Order
- Refund Payment
- Release Inventory

This is

a

Saga.

______________________________________________________________________

# Shipping Service

After

order creation,

publish

an event.

```text id="am8019"
Order Created

↓

Kafka

↓

Shipping Service
```

Shipping

runs

asynchronously.

______________________________________________________________________

# Notifications

Users receive:

- Order confirmation
- Payment confirmation
- Shipping updates
- Delivery confirmation

Workflow

```text id="am8020"
Event

↓

Kafka

↓

Notification Service

↓

Email / SMS / Push
```

______________________________________________________________________

# Recommendations

Recommendations

use:

- Purchase history
- Browsing history
- Similar customers
- Product embeddings

Examples:

```text id="am8021"
Customers Also Bought
```

```text id="am8022"
Recommended For You
```

Machine Learning

generates

personalized rankings.

______________________________________________________________________

# Caching

Redis stores:

- Product metadata
- Shopping carts
- Popular products
- Recommendation cache
- Session data

Inventory

should **not**

rely solely

on cache,

because

it changes

frequently.

______________________________________________________________________

# Scaling

Scale independently:

- Catalog Service
- Search Service
- Cart Service
- Order Service
- Inventory Service
- Recommendation Service

The Product Catalog

may require

database sharding.

______________________________________________________________________

# AI/ML Example

Amazon

uses ML

for:

- Product recommendations
- Fraud detection
- Dynamic pricing
- Inventory forecasting
- Search ranking
- Review moderation

Vector databases

can improve

semantic product search.

______________________________________________________________________

# Failure Scenario

Suppose

the Recommendation Service

fails.

Users

can still:

- Search
- Browse
- Purchase

The homepage

falls back

to:

- Best Sellers
- Trending Products
- Recently Viewed

______________________________________________________________________

# Another Failure

Suppose

Payment Gateway

is unavailable.

Orders

remain

in

"Payment Pending"

or

"Failed"

state.

Inventory reservations

expire

after

a timeout,

preventing

stock

from remaining locked.

______________________________________________________________________

# End-to-End Architecture

```text id="am8023"
Customer

↓

DNS

↓

Load Balancer

↓

API Gateway

↓

Catalog Service

↓

Search Service

↓

Cart Service

↓

Order Service

↓

Inventory Service

↓

Payment Service

↓

Redis

↓

PostgreSQL

↓

Kafka

↓

Shipping Service

↓

Notification Service

↓

Recommendation Service

↓

Object Storage
```

______________________________________________________________________

# Trade-offs

Redis

vs

Database

| Redis | Database |
| ------------- | ----------------- |
| Shopping cart | Persistent orders |
| Fast | Durable |
| Cache | Source of truth |

______________________________________________________________________

Inventory Reservation

vs

Direct Deduction

| Reservation | Direct Deduction |
| ---------------------- | -------------------- |
| Prevents overselling | Simpler |
| Requires timeout | Less complexity |
| Better user experience | Higher conflict risk |

______________________________________________________________________

SQL

vs

NoSQL

| SQL | NoSQL |
| ------------------ | -------------------------- |
| Orders | Product Catalog (optional) |
| ACID transactions | Flexible schema |
| Strong consistency | Horizontal scalability |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you design Amazon's checkout system?

Start by separating responsibilities into independent services such as Catalog, Cart, Inventory, Order, Payment, and
Shipping. During checkout, first validate and reserve inventory to prevent overselling. Then process payment through a
dedicated Payment Service. If payment succeeds, create the order and publish an event to Kafka so downstream services
such as Shipping and Notifications can process asynchronously. If any step fails after inventory reservation, use the
Saga pattern to execute compensating actions such as releasing inventory or issuing refunds. Store shopping carts in
Redis for low latency, orders in a relational database for ACID guarantees, product metadata in a scalable catalog, and
use Elasticsearch for fast product search.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Requirement gathering
- Product catalog
- Shopping cart
- Inventory reservation
- Checkout flow
- Order lifecycle
- Payment integration
- Saga pattern
- Recommendations
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
- ✅ Amazon

You now understand one of the world's largest e-commerce architectures, combining transactional consistency, distributed
services, search, recommendations, and asynchronous processing.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll design one of the most important backend systems used across nearly every modern application:

- Payment lifecycle
- Idempotency
- Payment states
- Webhooks
- Retries
- Double-spending prevention
- Reconciliation
- Ledger architecture

We'll design a **Payment Gateway (Stripe/Razorpay)**.

______________________________________________________________________

# What's Next

[Payment Gateway System Design](81-payment-gateway-system-design.md)
