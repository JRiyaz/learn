# System Design - Part 67

# API Versioning

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What API Versioning is
- Why API Versioning exists
- Breaking vs Non-Breaking Changes
- Versioning Strategies
- URI Versioning
- Header Versioning
- Query Parameter Versioning
- Content Negotiation
- API Deprecation
- API Migration
- FastAPI examples
- Common interview questions

______________________________________________________________________

# Before We Start

Suppose

our **Library Management System**

provides

this API.

```http id="api6701"
GET /books
```

Thousands

of mobile apps

use it.

One day,

you decide

to change

the response.

Old response

```json id="api6702"
{
    "title": "Python"
}
```

New response

```json id="api6703"
{
    "book_title": "Python"
}
```

Question.

What happens

to

all existing

mobile applications?

They break.

______________________________________________________________________

# The Problem

Clients

depend

on

your API contract.

Even

a small change

can break

thousands

of applications.

Examples:

- Mobile apps
- Web apps
- Partner APIs
- Third-party integrations

You cannot

change APIs

carelessly.

______________________________________________________________________

# The Idea

Instead of

changing

the existing API,

create

a new version.

Old clients

continue

using

the old version.

New clients

move

to

the new version.

______________________________________________________________________

# What is API Versioning?

**API Versioning**

is the practice

of maintaining

multiple versions

of an API

so that

existing clients

continue working

while

new functionality

is introduced.

______________________________________________________________________

# Example

Instead of

```http id="api6704"
GET /books
```

Create

```http id="api6705"
GET /v1/books
```

Later

introduce

```http id="api6706"
GET /v2/books
```

Both versions

can coexist.

______________________________________________________________________

# Why Version APIs?

API Versioning

helps with:

- Backward compatibility
- Safe evolution
- Gradual migration
- Independent client upgrades

______________________________________________________________________

# Breaking Changes

Interview favorite.

A **Breaking Change**

requires

clients

to modify

their code.

Examples:

- Renaming fields
- Removing fields
- Changing data types
- Changing endpoint behavior
- Removing endpoints

______________________________________________________________________

# Non-Breaking Changes

A **Non-Breaking Change**

doesn't require

existing clients

to change.

Examples:

- Adding optional fields
- Adding new endpoints
- Improving performance
- Fixing bugs

Whenever possible,

prefer

non-breaking changes.

______________________________________________________________________

# URI Versioning

The most common

approach.

```http id="api6707"
GET /v1/books
```

```http id="api6708"
GET /v2/books
```

Advantages

✅ Easy to understand

✅ Easy to document

Disadvantages

❌ URLs change

______________________________________________________________________

# Query Parameter Versioning

Example

```http id="api6709"
GET /books?version=2
```

Advantages

✅ Simple

Disadvantages

❌ Less common

❌ Easy to forget

______________________________________________________________________

# Header Versioning

Version

is sent

inside

an HTTP header.

Example

```http id="api6710"
API-Version: 2
```

Advantages

✅ Clean URLs

Disadvantages

❌ Harder to discover

______________________________________________________________________

# Content Negotiation

Another approach

uses

the

Accept header.

Example

```http id="api6711"
Accept:

application/vnd.library.v2+json
```

Advantages

✅ REST-friendly

Disadvantages

❌ More complex

______________________________________________________________________

# Strategy Comparison

| Strategy | Example | Popularity |
| ------------------- | --------------- | ---------- |
| URI | `/v1/books` | ⭐⭐⭐⭐⭐ |
| Header | `API-Version:2` | ⭐⭐⭐ |
| Query | `?version=2` | ⭐⭐ |
| Content Negotiation | `Accept:` | ⭐⭐ |

For

public REST APIs,

URI Versioning

is

the most common.

______________________________________________________________________

# API Evolution

Suppose

Version 1

returns

```json id="api6712"
{
  "title": "Python"
}
```

Version 2

adds

an optional field.

```json id="api6713"
{
  "title": "Python",
  "publisher": "O'Reilly"
}
```

Old clients

continue working.

This is

a non-breaking change.

______________________________________________________________________

# Deprecation

Eventually,

Version 1

must be retired.

Don't remove it

immediately.

Instead,

announce

deprecation.

Example

```text id="api6714"
v1

Deprecated

↓

Migration Period

↓

Removal
```

Clients

need time

to migrate.

______________________________________________________________________

# Sunset Policy

Many companies

announce

a

**Sunset Date.**

Example

```text id="api6715"
v1 Support Ends

31 Dec 2027
```

After

the sunset date,

the API

is removed.

______________________________________________________________________

# Migration

Migration

should happen

gradually.

Workflow

```text id="api6716"
v1

↓

v2

↓

Deprecate v1

↓

Remove v1
```

Avoid

forcing

all clients

to upgrade

at once.

______________________________________________________________________

# FastAPI Example

```python id="api6717"
@app.get("/v1/books")

@app.get("/v2/books")
```

Each version

can evolve

independently.

______________________________________________________________________

# Microservices Example

Suppose

Service A

calls

Service B.

Instead of

breaking

Service A,

Service B

supports

both

v1

and

v2

during

migration.

This enables

independent deployments.

______________________________________________________________________

# AI/ML Example

Suppose

an AI API

changes

its response.

Old version

```json id="api6718"
{
  "answer": "..."
}
```

New version

```json id="api6719"
{
  "answer": "...",
  "confidence": 0.98
}
```

Adding

an optional field

is

backward compatible.

Renaming

`answer`

would be

a breaking change.

______________________________________________________________________

# Real Backend Example

Suppose

an e-commerce platform.

Mobile apps

from

two years ago

still use

```text id="api6720"
/v1/orders
```

New applications

use

```text id="api6721"
/v2/orders
```

Both APIs

run

simultaneously

until

old clients

upgrade.

______________________________________________________________________

# Versioning Databases?

Interview favorite.

Databases

are usually

not versioned

like APIs.

Instead,

schema changes

are managed

using

migration tools

such as:

- Flyway
- Liquibase
- Alembic

API Versioning

protects

clients.

Database migrations

protect

internal systems.

______________________________________________________________________

# API Versioning vs Database Migration

| API Versioning | Database Migration |
| ----------------- | ------------------ |
| External contract | Internal schema |
| Protects clients | Updates database |
| Multiple versions | Usually one schema |

These solve

different problems.

______________________________________________________________________

# Benefits

API Versioning provides:

✅ Backward compatibility

✅ Safer deployments

✅ Independent client upgrades

✅ Easier API evolution

______________________________________________________________________

# Drawbacks

It also introduces:

❌ Multiple versions

to maintain

❌ Documentation overhead

❌ Testing complexity

❌ Longer support lifecycle

______________________________________________________________________

# When NOT to Create a New Version

Avoid

creating

a new version

for:

- Bug fixes
- Performance improvements
- Optional fields
- Internal refactoring

Reserve

new versions

for

breaking changes.

______________________________________________________________________

# Best Practices

✅ Prefer non-breaking changes.

✅ Version only when necessary.

✅ Announce deprecations early.

✅ Give clients time to migrate.

______________________________________________________________________

# Common Mistakes

### Versioning Every Small Change

Not every change

requires

a new API version.

______________________________________________________________________

### Removing Old APIs Too Soon

Large customers

may need

months

to migrate.

Provide

a reasonable

deprecation period.

______________________________________________________________________

### Breaking Existing Clients

Never change

existing response fields

without

a migration strategy.

______________________________________________________________________

### Poor Documentation

Every version

must have

clear,

independent documentation.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is API Versioning important, and what is the most common strategy?

API Versioning allows applications to evolve without breaking existing clients. When an API introduces breaking changes,
such as removing fields or changing response formats, a new version is created while the old version continues to be
supported during a migration period. The most common strategy for REST APIs is URI Versioning (for example, `/v1/users`
and `/v2/users`) because it is simple, explicit, and easy to document. Good API versioning practices include minimizing
breaking changes, supporting multiple versions during migration, and communicating deprecation timelines clearly.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What API Versioning is
- Breaking vs Non-Breaking Changes
- URI Versioning
- Header Versioning
- Query Versioning
- Content Negotiation
- API Deprecation
- Migration Strategy
- Best practices

______________________________________________________________________

# 🧠 Security Module Progress

You have now completed the **Security** module:

- ✅ Authentication & Authorization
- ✅ Rate Limiting
- ✅ API Versioning

These topics ensure your APIs remain secure, scalable, and maintainable as they evolve.

______________________________________________________________________

# 🚀 What's Coming Next

Next, we'll begin the **Deployment & Operations** module.

You'll learn how companies deploy new software versions without downtime or risking all users at once.

We'll start with:

- Blue-Green Deployment
- Canary Deployment
- Rolling Deployment
- Feature Flags

______________________________________________________________________

# What's Next

[Blue-Green & Canary Deployments](68-blue-green-and-canary-deployments.md)
