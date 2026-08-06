# Tags & Metadata

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 3 - Routing
>
> **File:** `16_tags_metadata.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What API Metadata is
- Why Metadata is Important
- API Title
- Description
- Version
- Contact Information
- License Information
- Tags
- Route-Level Metadata
- OpenAPI Customization
- Best Practices

______________________________________________________________________

# What is API Metadata?

Metadata is information **about your API**, not the business data it returns.

Example

```
API Name

↓

User Management API
```

```
Version

↓

1.0.0
```

```
Description

↓

REST API for User Management
```

Metadata makes APIs easier to understand and consume.

______________________________________________________________________

# Why Metadata Matters

Without metadata

```
Swagger

↓

Unnamed API

↓

Confusing Documentation
```

With metadata

```
Professional Documentation

↓

Clear Endpoints

↓

Better Developer Experience
```

______________________________________________________________________

# API Metadata

When creating a FastAPI application

```python
from fastapi import FastAPI

app = FastAPI(

    title="User API",

    description="REST API for user management.",

    version="1.0.0"
)
```

Swagger immediately displays this information.

______________________________________________________________________

# API Title

```python
title="E-Commerce API"
```

Appears at the top of Swagger UI.

______________________________________________________________________

# Description

```python
description="""

REST API for managing

products,

orders,

and customers.

"""
```

Markdown formatting is supported.

______________________________________________________________________

# Version

```python
version="2.1.0"
```

Useful for

- Documentation
- Releases
- Client Communication

______________________________________________________________________

# Contact Information

```python
contact={

    "name": "Backend Team",

    "email": "backend@example.com"
}
```

Swagger displays contact details.

______________________________________________________________________

# License Information

```python
license_info={

    "name": "MIT"
}
```

Useful for

- Open Source Projects
- Public APIs

______________________________________________________________________

# API Metadata Example

```python
app = FastAPI(

    title="Inventory API",

    description="Inventory Management Service",

    version="1.0.0",

    contact={

        "name": "Backend Team",

        "email": "backend@example.com"

    },

    license_info={

        "name": "MIT"

    }
)
```

______________________________________________________________________

# What are Tags?

Tags group related endpoints.

Without tags

```
100 Endpoints

↓

Mixed Together
```

With tags

```
Authentication

Users

Orders

Products

Payments
```

Swagger becomes much easier to navigate.

______________________________________________________________________

# Router-Level Tags

```python
router = APIRouter(

    prefix="/users",

    tags=["Users"]
)
```

Every route inside this router belongs to the **Users** group.

______________________________________________________________________

# Route-Level Tags

```python
@app.get(

    "/reports",

    tags=["Reports"]
)
```

Useful when only a single endpoint belongs to a different category.

______________________________________________________________________

# Multiple Tags

```python
@app.get(

    "/statistics",

    tags=[

        "Analytics",

        "Admin"

    ]
)
```

The endpoint appears in both groups.

______________________________________________________________________

# Route Summary

```python
@app.get(

    "/users",

    summary="List Users"
)
```

Swagger shows

```
List Users
```

instead of deriving a title automatically.

______________________________________________________________________

# Route Description

```python
@app.get(

    "/users",

    description="Returns all active users."
)
```

Detailed documentation appears beneath the endpoint.

Markdown is supported.

______________________________________________________________________

# Response Description

```python
@app.post(

    "/users",

    response_description="User created successfully"
)
```

Improves generated OpenAPI documentation.

______________________________________________________________________

# Operation ID

Every endpoint has an operation identifier.

Example

```python
@app.get(

    "/users",

    operation_id="get_users"
)
```

Useful when generating client SDKs.

______________________________________________________________________

# Deprecating an Endpoint

```python
@app.get(

    "/old-users",

    deprecated=True
)
```

Swagger marks the endpoint as deprecated.

Clients are informed that it should no longer be used.

______________________________________________________________________

# Endpoint Visibility

Hide internal endpoints.

```python
@app.get(

    "/internal",

    include_in_schema=False
)
```

The endpoint still works,

but it doesn't appear in Swagger.

Useful for

- Internal health endpoints
- Administrative APIs

______________________________________________________________________

# Route Metadata Example

```python
@app.get(

    "/users",

    tags=["Users"],

    summary="Get Users",

    description="Returns all users.",

    response_description="List of users"
)
```

______________________________________________________________________

# OpenAPI Flow

```
FastAPI

↓

Metadata

↓

OpenAPI Schema

↓

Swagger UI

↓

ReDoc
```

Everything is generated automatically.

______________________________________________________________________

# Real Production Example

```
Authentication

↓

Login

Logout

Refresh Token
```

```
Users

↓

Create

Update

Delete

List
```

```
Orders

↓

Create

Cancel

Track
```

Each section appears separately in Swagger.

______________________________________________________________________

# Documentation Before Metadata

```
GET /users

GET /orders

GET /products

...
```

Difficult to navigate.

______________________________________________________________________

# Documentation After Metadata

```
Users

GET

POST

PUT

DELETE

----------------

Orders

GET

POST

DELETE
```

Much more organized.

______________________________________________________________________

# Why Good Documentation Matters

Consumers include

- Frontend Teams
- Mobile Developers
- Third-party Integrators
- QA Engineers
- API Consumers

Clear documentation reduces misunderstandings and support requests.

______________________________________________________________________

# Common Mistakes

❌ Leaving the default API title

❌ Using one large tag called "API"

❌ Writing vague endpoint descriptions

❌ Forgetting to deprecate obsolete endpoints

❌ Exposing internal endpoints in public documentation

______________________________________________________________________

# Production Best Practices

- Give the API a meaningful title.
- Write concise but informative descriptions.
- Group endpoints using tags.
- Add summaries to important endpoints.
- Document responses.
- Mark deprecated endpoints.
- Hide internal endpoints when appropriate.
- Keep documentation up to date.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should production APIs include good metadata and documentation?**

### Answer

Good API documentation improves developer productivity and reduces integration errors.

Benefits include:

- Easier onboarding.
- Better API discoverability.
- Reduced support requests.
- Accurate client SDK generation.
- Clear communication of endpoint behavior.
- Better long-term maintainability.

FastAPI makes this easy by generating OpenAPI documentation directly from Python code and metadata.

______________________________________________________________________

# Summary

In this chapter you learned:

- API Metadata
- API Title
- Description
- Version
- Contact Information
- License Information
- Tags
- Route Metadata
- OpenAPI Integration
- Production Best Practices

Well-documented APIs are easier to understand, integrate, and maintain. FastAPI provides comprehensive documentation
generation with very little additional code.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is API metadata?
1. Why is metadata important?
1. What information should every production API expose?

______________________________________________________________________

## Documentation

4. What is the purpose of tags?
1. Why are route summaries useful?
1. Why are route descriptions useful?

______________________________________________________________________

## OpenAPI

7. How does FastAPI generate Swagger documentation?
1. What is an OpenAPI schema?
1. Why is `operation_id` useful?

______________________________________________________________________

## Endpoint Management

10. Why should deprecated endpoints be marked explicitly?
01. What does `include_in_schema=False` do?
01. When should an endpoint be hidden from documentation?

______________________________________________________________________

## Production

13. Why is API documentation valuable for frontend teams?
01. Why should internal endpoints not appear in public documentation?
01. How does good documentation reduce maintenance costs?

______________________________________________________________________

## Scenario-Based

16. Your Swagger documentation contains over 300 endpoints with no grouping. How would tags improve usability?
01. A legacy endpoint is still functional but should no longer be used by new clients. How would you communicate this through FastAPI?
01. Your API is used by external partners who frequently misunderstand endpoint behavior. What metadata would you improve?
01. Your team wants to generate a client SDK automatically. Why is having meaningful `operation_id` values beneficial?
01. An internal `/debug` endpoint appears in public Swagger documentation. How can you keep the endpoint accessible while hiding it from the generated schema?

______________________________________________________________________

# Next

[Path Operation Configuration](17_path_operation_configuration.md)
