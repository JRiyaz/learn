# API Versioning

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 3 - Routing
>
> **File:** `15_api_versioning.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What API Versioning is
- Why Versioning is Important
- Backward Compatibility
- Types of API Versioning
- URL Versioning
- Header Versioning
- Query Parameter Versioning
- Versioning with APIRouter
- Deprecating APIs
- Production Best Practices

______________________________________________________________________

# What is API Versioning?

API Versioning is the practice of maintaining multiple versions of an API simultaneously.

Example

```
v1

↓

Existing Clients
```

```
v2

↓

New Clients
```

Both versions continue to work independently.

______________________________________________________________________

# Why Do We Need Versioning?

Imagine your API returns

Version 1

```json
{
    "name": "Riyaz"
}
```

A mobile application depends on this format.

Now you change it to

Version 2

```json
{
    "first_name": "Riyaz",
    "last_name": "J"
}
```

Without versioning,

older clients break immediately.

______________________________________________________________________

# The Problem Without Versioning

```
Client

↓

Old API Contract

↓

Server Updated

↓

Application Fails
```

Versioning protects existing consumers.

______________________________________________________________________

# What is an API Contract?

An API contract defines

- Endpoints
- Request Format
- Response Format
- Status Codes
- Authentication
- Error Format

Clients depend on this contract.

Changing it unexpectedly is a breaking change.

______________________________________________________________________

# Breaking Changes

Examples

❌ Renaming fields

```
name

↓

full_name
```

______________________________________________________________________

❌ Removing fields

```
email

↓

Removed
```

______________________________________________________________________

❌ Changing data types

```
age

↓

int

↓

string
```

______________________________________________________________________

❌ Changing URL paths

```
/users

↓

/customers
```

______________________________________________________________________

# Non-Breaking Changes

Examples

✅ Adding optional fields

```json
{
    "name": "Riyaz",
    "phone": "1234567890"
}
```

Older clients ignore the new field.

______________________________________________________________________

✅ Adding new endpoints

```
/orders
```

does not affect

```
/users
```

______________________________________________________________________

# Versioning Strategies

Common approaches

- URL Versioning
- Header Versioning
- Query Parameter Versioning
- Content Negotiation

The most common approach is URL versioning.

______________________________________________________________________

# URL Versioning

Example

```
/api/v1/users

/api/v2/users
```

Easy to understand.

Easy to document.

Easy to debug.

______________________________________________________________________

# FastAPI Example

```python
v1 = APIRouter(

    prefix="/api/v1"
)

v2 = APIRouter(

    prefix="/api/v2"
)
```

Now both versions can coexist.

______________________________________________________________________

# Project Structure

```
app/

│

├── api/

│

│     v1/

│

│        users.py

│

│        orders.py

│

│

│     v2/

│

│        users.py

│

│        orders.py

│

└── main.py
```

Each version has its own routes.

______________________________________________________________________

# Including Routers

```python
app.include_router(

    v1_router

)

app.include_router(

    v2_router
)
```

Both APIs are active.

______________________________________________________________________

# URL Flow

```
Request

↓

/api/v1/users

↓

v1 Router
```

```
Request

↓

/api/v2/users

↓

v2 Router
```

______________________________________________________________________

# Header Versioning

Example

```
GET /users
```

Header

```
API-Version: 2
```

The endpoint stays the same,

the header determines the version.

______________________________________________________________________

# Advantages

- Cleaner URLs
- Flexible version selection

Disadvantages

- Harder to test manually
- Less visible
- More difficult to debug

______________________________________________________________________

# Query Parameter Versioning

Example

```
/users?version=2
```

Advantages

- Easy to implement

Disadvantages

- Rarely used in production
- Less explicit than URL versioning

______________________________________________________________________

# Content Negotiation

Example

```
Accept:

application/vnd.company.v2+json
```

Common in some enterprise APIs.

More complex than URL versioning.

______________________________________________________________________

# Which Strategy is Best?

| Strategy | Common Usage |
|-----------|--------------|
| URL | ✅ Most Common |
| Header | Common |
| Query Parameter | Less Common |
| Content Negotiation | Enterprise / Specialized |

______________________________________________________________________

# Versioning with APIRouter

Example

```python
v1_router = APIRouter(

    prefix="/api/v1/users",

    tags=["Users V1"]
)
```

```python
v2_router = APIRouter(

    prefix="/api/v2/users",

    tags=["Users V2"]
)
```

Swagger clearly separates versions.

______________________________________________________________________

# Supporting Multiple Versions

```
v1

↓

Bug Fixes
```

```
v2

↓

New Features
```

Existing users can migrate gradually.

______________________________________________________________________

# Deprecating an API

Typical lifecycle

```
Release v2

↓

Mark v1 Deprecated

↓

Notify Clients

↓

Migration Period

↓

Remove v1
```

Avoid removing versions immediately.

______________________________________________________________________

# Example Timeline

```
January

↓

v2 Released
```

```
March

↓

Deprecation Notice
```

```
September

↓

v1 Removed
```

Clients have time to migrate.

______________________________________________________________________

# Real Production Example

```
/api/v1/auth

/api/v1/users

/api/v1/orders
```

Later

```
/api/v2/auth

/api/v2/users

/api/v2/orders
```

Both versions operate independently.

______________________________________________________________________

# Backward Compatibility

Goal

```
New Server

↓

Old Client

↓

Still Works
```

Versioning minimizes unexpected client failures.

______________________________________________________________________

# Documentation

Swagger

```
Users V1

Users V2

Orders V1

Orders V2
```

Developers can easily explore supported versions.

______________________________________________________________________

# Common Mistakes

❌ Changing response structures without creating a new version

❌ Removing endpoints immediately

❌ Mixing v1 and v2 logic inside the same route

❌ Breaking existing API contracts

❌ Forgetting to communicate deprecation timelines

______________________________________________________________________

# Production Best Practices

- Prefer URL versioning for public APIs.
- Keep versions isolated.
- Maintain backward compatibility whenever practical.
- Deprecate before removing.
- Document version differences clearly.
- Give clients enough time to migrate.
- Avoid unnecessary version creation for non-breaking changes.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is URL versioning the most common API versioning strategy?**

### Answer

URL versioning is explicit, simple, and easy to understand.

Benefits include:

- Easy for developers to discover.
- Easy to test using browsers, Postman, or curl.
- Clear separation between API versions.
- Straightforward routing and documentation.
- Well supported by API gateways, proxies, and caching infrastructure.

Although other strategies exist, URL versioning is widely adopted because of its simplicity and operational clarity.

______________________________________________________________________

# Summary

In this chapter you learned:

- API Versioning
- Breaking Changes
- Backward Compatibility
- URL Versioning
- Header Versioning
- Query Parameter Versioning
- APIRouter Versioning
- Deprecation Strategy
- Production Best Practices

API versioning allows applications to evolve without breaking existing clients, making it an essential practice for
production APIs.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is API versioning?
1. Why is API versioning important?
1. What is an API contract?

______________________________________________________________________

## Breaking Changes

4. What is a breaking change?
1. Give three examples of breaking changes.
1. Give three examples of non-breaking changes.

______________________________________________________________________

## Versioning Strategies

7. What are the common API versioning strategies?
1. Why is URL versioning the most popular?
1. What are the advantages and disadvantages of header versioning?

______________________________________________________________________

## FastAPI

10. How can APIRouter be used to implement versioning?
01. Why should different API versions have separate routers?

______________________________________________________________________

## Production

12. What does backward compatibility mean?
01. Why should APIs be deprecated before removal?
01. Why shouldn't v1 and v2 logic be mixed in the same endpoint?

______________________________________________________________________

## Scenario-Based

15. Your mobile application uses `/api/v1/users`, but the response format needs to change in an incompatible way. How would you introduce the new format?
01. Your team renamed the `name` field to `full_name` in production without versioning. What problems might existing clients experience?
01. Your company wants to support both legacy and modern clients for one year. How would you organize the FastAPI project?
01. A teammate proposes using query parameters for versioning because it's easy to implement. What trade-offs would you discuss?
01. Your API documentation currently mixes endpoints from multiple versions together. How can router prefixes and tags improve clarity?
01. Your organization plans to retire v1 in six months. What steps would you take to help clients migrate successfully?

______________________________________________________________________

# Next

[Tags & Metadata](16_tags_metadata.md)
