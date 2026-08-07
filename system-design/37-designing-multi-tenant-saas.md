# Advanced Distributed Systems – Designing a Multi-Tenant SaaS

> Target Audience: Senior Backend Engineers (5–10 Years)
>
> Goal: Understand how to design a scalable Multi-Tenant SaaS platform similar to GitHub Enterprise, Jira Cloud, Slack, Salesforce, or Notion.

______________________________________________________________________

# Introduction

Most modern SaaS products

are

Multi-Tenant.

Examples

- Slack
- Notion
- GitHub
- Atlassian Cloud
- Salesforce
- Figma

Instead of

one application

per customer,

multiple customers

share

the same platform.

The biggest challenge

is

```
Isolation

without

wasting resources.
```

______________________________________________________________________

# What is Multi-Tenancy?

Multiple customers

share

the same application

while

their data

remains isolated.

Example

```
Company A

↓

Our SaaS

↓

Database
```

```
Company B

↓

Same SaaS

↓

Same Database
```

Neither company

can access

the other's data.

______________________________________________________________________

# Why Multi-Tenant?

Advantages

- Lower infrastructure cost
- Easier deployments
- Centralized monitoring
- Better resource utilization
- Faster onboarding

______________________________________________________________________

# Challenges

Need

- Data isolation
- Security
- Scalability
- Customization
- Billing
- Performance isolation

______________________________________________________________________

# Tenant

A tenant

is

a customer.

Example

```
Acme Inc.

↓

Tenant
```

```
Google

↓

Tenant
```

```
Microsoft

↓

Tenant
```

Every request

belongs

to

one tenant.

______________________________________________________________________

# Tenant Identification

Interview favorite.

How does

the application

know

which tenant

made

the request?

Several approaches.

______________________________________________________________________

## Option 1

Subdomain

```
acme.myapp.com
```

Tenant

↓

acme

Very common.

______________________________________________________________________

## Option 2

Custom Domain

```
portal.company.com
```

Maps

to

Tenant ID.

______________________________________________________________________

## Option 3

JWT

JWT

contains

```
tenant_id
```

Very common

for APIs.

______________________________________________________________________

## Option 4

HTTP Header

```
X-Tenant-ID
```

Mostly

used

internally.

______________________________________________________________________

# Request Flow

```
User

↓

Load Balancer

↓

API Gateway

↓

Authentication

↓

Tenant Resolver

↓

Business Logic
```

Every request

must resolve

its tenant

before

processing.

______________________________________________________________________

# Multi-Tenant Database Models

Interview favorite.

There are

three common

approaches.

______________________________________________________________________

# Model 1

Database Per Tenant

```
Tenant A

↓

DB A
```

```
Tenant B

↓

DB B
```

______________________________________________________________________

Advantages

- Excellent isolation
- Easy backup
- Easy migration

______________________________________________________________________

Disadvantages

- Expensive
- Hard to manage
- Thousands of databases

______________________________________________________________________

Best for

Enterprise SaaS.

______________________________________________________________________

# Model 2

Schema Per Tenant

```
Database

↓

Schema A

Schema B

Schema C
```

______________________________________________________________________

Advantages

- Better isolation
- Shared database

______________________________________________________________________

Disadvantages

- Large number

of schemas

becomes difficult

to manage.

______________________________________________________________________

# Model 3

Shared Database

Interview favorite.

```
Database

↓

Users Table
```

```
tenant_id

user_id

name
```

Every table

contains

```
tenant_id
```

______________________________________________________________________

Advantages

- Cheapest
- Simple scaling
- Easy deployment

______________________________________________________________________

Disadvantages

Security becomes

critical.

One bug

can expose

another tenant's data.

______________________________________________________________________

# Which Model Should You Choose?

| Company Size | Recommended |
|--------------|-------------|
| Startup | Shared Database |
| Growing SaaS | Shared DB + Sharding |
| Enterprise | Database Per Tenant |

______________________________________________________________________

# Data Isolation

Every query

must include

```
WHERE tenant_id = ?
```

Never trust

client input.

Always derive

tenant

from

authentication.

______________________________________________________________________

Wrong

```
GET /users?tenant=abc
```

Right

```
JWT

↓

Tenant

↓

Database Query
```

______________________________________________________________________

# Authorization

Authentication

identifies

the user.

Authorization

checks

whether

the user

belongs

to

that tenant.

______________________________________________________________________

# Caching

Interview favorite.

Cache keys

must include

tenant.

Wrong

```
user:123
```

Correct

```
tenant42:user123
```

Otherwise

Tenant A

may receive

Tenant B's data.

______________________________________________________________________

# File Storage

Object Storage

should separate

tenant data.

Example

```
tenant-123/

invoice.pdf
```

```
tenant-456/

invoice.pdf
```

______________________________________________________________________

# Search

Search indexes

must also

be isolated.

Example

```
tenant_id

↓

Elasticsearch Filter
```

Never search

globally

unless

business requirements

allow it.

______________________________________________________________________

# Background Jobs

Every job

must contain

```
tenant_id
```

Example

```
Generate Invoice

↓

Tenant 54
```

Workers

must preserve

tenant context.

______________________________________________________________________

# Rate Limiting

Limits

may differ

per tenant.

Example

Free

↓

100 RPM

Pro

↓

1000 RPM

Enterprise

↓

Unlimited

______________________________________________________________________

# Billing

Billing

is

usually

per tenant.

Examples

- Users
- API Calls
- Storage
- Projects

Usage

must be tracked

per tenant.

______________________________________________________________________

# Custom Branding

Many SaaS platforms

allow

tenant branding.

Examples

- Logo
- Theme
- Domain
- Email Templates

Configuration

should be

tenant-specific.

______________________________________________________________________

# Feature Flags

Different tenants

may have

different features.

```
Tenant A

↓

AI Enabled
```

```
Tenant B

↓

Disabled
```

Use

feature flags.

______________________________________________________________________

# Horizontal Scaling

```
Users

↓

Load Balancer

↓

API Servers

↓

Redis

↓

Database
```

API servers

remain

stateless.

______________________________________________________________________

# Sharding

Eventually

millions

of tenants

exist.

Shard

using

```
tenant_id
```

Excellent

partition key.

______________________________________________________________________

# Monitoring

Monitor

per tenant.

Examples

- API latency
- Storage
- Database usage
- Error rate
- CPU
- Memory
- Billing

______________________________________________________________________

# Failure Scenarios

## One Tenant Generates Massive Traffic

Problem

```
Noisy Neighbor
```

One tenant

consumes

most resources.

______________________________________________________________________

Solutions

- Rate Limiting
- Resource Quotas
- Dedicated Workers
- Dedicated Database
- Tenant Isolation

______________________________________________________________________

## Database Failure

Replica

becomes

new primary.

______________________________________________________________________

## Cache Failure

Fallback

to

database.

______________________________________________________________________

# Security

Interview favorite.

Never trust

tenant IDs

from

request parameters.

Always derive

tenant

from

authentication.

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
                     ▼
             Authentication
                     │
                     ▼
             Tenant Resolver
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    User Service Project Service Billing
         │           │           │
         ▼           ▼           ▼
        Redis     Database     Kafka
                     │
                     ▼
               Object Storage
```

______________________________________________________________________

# Common Interview Questions

## Why not create one application per customer?

Operating thousands of independent deployments becomes expensive and difficult to manage. Multi-tenancy improves
resource utilization while maintaining logical isolation.

______________________________________________________________________

## Why include tenant_id in cache keys?

Without tenant-specific cache keys, cached data from one tenant could be returned to another tenant, creating a serious
security issue.

______________________________________________________________________

## What is the Noisy Neighbor problem?

A single tenant with heavy traffic can consume disproportionate resources, affecting other tenants sharing the same
infrastructure.

______________________________________________________________________

## Which database model is best?

It depends on scale and customer requirements. Shared databases are cost-effective for startups, while
database-per-tenant offers stronger isolation for enterprise customers.

______________________________________________________________________

# Common Mistakes

## Trusting Tenant IDs

Never

trust

client-provided

tenant identifiers.

______________________________________________________________________

## Missing tenant_id

Every

database query,

cache key,

background job,

and search query

must preserve

tenant context.

______________________________________________________________________

## Global Cache Keys

Always

namespace

cache entries

by tenant.

______________________________________________________________________

## Shared File Paths

Separate

tenant data

in object storage.

______________________________________________________________________

## Ignoring Noisy Neighbors

Large tenants

may require

resource isolation.

______________________________________________________________________

# Best Practices

✅ Resolve tenant from authentication.

✅ Namespace cache keys.

✅ Use tenant-aware authorization.

✅ Monitor per tenant.

✅ Use feature flags.

✅ Plan for noisy neighbors.

✅ Shard using tenant_id.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the biggest challenge in a Multi-Tenant SaaS?

### Answer

Maintaining strong tenant isolation while maximizing infrastructure sharing. Every layer—including authentication,
authorization, caching, storage, search, and background jobs—must preserve tenant context to prevent data leakage.

______________________________________________________________________

## Question

When would you move from a shared database to database-per-tenant?

### Answer

Large enterprise customers may require stronger isolation, independent backups, custom maintenance windows, regulatory
compliance, or dedicated performance guarantees. Those requirements often justify database-per-tenant despite the higher
operational cost.

______________________________________________________________________

## Practice Exercise

Design

a SaaS platform

like

Jira Cloud.

Explain

1. Tenant identification
1. Authentication
1. Database model
1. Cache design
1. File storage
1. Billing
1. Feature flags
1. Sharding
1. Monitoring
1. Noisy neighbor handling
1. Failure recovery
1. Trade-offs

Present

your solution

within

45 minutes,

similar to

a Senior Backend Engineer

System Design interview.

______________________________________________________________________

# Summary

Multi-Tenant SaaS design is one of the most common advanced backend interview topics because nearly every cloud product
follows this architecture.

A strong solution should demonstrate

- Tenant isolation
- Authentication and authorization
- Database strategy
- Tenant-aware caching
- Feature flags
- Billing
- Sharding
- Monitoring
- Noisy neighbor mitigation
- Trade-off analysis

______________________________________________________________________

# Next

[Leader Election](38-leader-election.md)
