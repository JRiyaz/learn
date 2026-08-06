# Path Parameters

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `04_path_parameters.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Path Parameters are
- How FastAPI Handles Path Parameters
- Type Conversion
- Automatic Validation
- Multiple Path Parameters
- Optional Path Parameters
- Enum Path Parameters
- Path Validation
- Path Metadata
- Best Practices
- Common Mistakes

______________________________________________________________________

# What are Path Parameters?

A **Path Parameter** is a dynamic value embedded directly in the URL.

Example

```
/users/10
```

Here

```
10
```

is the path parameter.

Another example

```
/orders/100/items/5
```

Path Parameters

```
100

5
```

______________________________________________________________________

# Why Do We Use Path Parameters?

Instead of creating separate routes

Bad

```
/user1

/user2

/user3
```

We create one dynamic route

```
/users/{id}
```

FastAPI extracts the value automatically.

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")

def get_user(

    user_id: int

):

    return {

        "user_id": user_id

    }
```

Request

```
GET /users/10
```

Response

```json
{
    "user_id": 10
}
```

______________________________________________________________________

# How FastAPI Processes It

```
Incoming Request

↓

/users/10

↓

Route Match

↓

Extract

10

↓

Convert

↓

int

↓

Call Function
```

______________________________________________________________________

# Automatic Type Conversion

Example

```python
@app.get("/products/{id}")

def get_product(

    id: int

):

    return {

        "id": id

    }
```

Request

```
/products/25
```

Inside Python

```python
id == 25
```

Type

```python
int
```

No manual conversion is needed.

______________________________________________________________________

# Automatic Validation

Suppose

```python
id: int
```

Request

```
/products/abc
```

FastAPI automatically returns

```
422

Validation Error
```

The route function is **never executed**.

______________________________________________________________________

# Validation Response

Example

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": [
                "path",
                "id"
            ]
        }
    ]
}
```

FastAPI generates this automatically.

______________________________________________________________________

# Multiple Path Parameters

Example

```python
@app.get(

"/users/{user_id}/orders/{order_id}"

)

def get_order(

    user_id: int,

    order_id: int

):

    return {

        "user": user_id,

        "order": order_id

    }
```

Request

```
/users/10/orders/250
```

______________________________________________________________________

# Flow

```
URL

↓

users

↓

10

↓

orders

↓

250

↓

Route Function
```

______________________________________________________________________

# Path Parameter Types

Supported types

```python
int

float

str

bool

UUID
```

Example

```python
from uuid import UUID

@app.get("/users/{id}")

def get_user(

    id: UUID

):

    ...
```

FastAPI validates UUIDs automatically.

______________________________________________________________________

# String Parameters

```python
@app.get(

"/files/{filename}"

)

def file(

    filename: str

):

    return filename
```

Request

```
/files/report.pdf
```

______________________________________________________________________

# Float Parameters

```python
@app.get(

"/prices/{amount}"

)

def price(

    amount: float

):

    return amount
```

Request

```
/prices/99.95
```

______________________________________________________________________

# Enum Path Parameters

Example

```python
from enum import Enum

class Color(

    str,

    Enum

):

    red = "red"

    blue = "blue"
```

Route

```python
@app.get(

"/colors/{color}"

)

def get_color(

    color: Color

):

    return {

        "color": color

    }
```

Valid

```
/colors/red
```

Invalid

```
/colors/yellow
```

Returns

```
422
```

______________________________________________________________________

# Path Order Matters

Good

```python
@app.get("/users/me")
```

before

```python
@app.get("/users/{id}")
```

Otherwise

```
me

↓

treated as

↓

{id}
```

Route order matters when static and dynamic paths overlap.

______________________________________________________________________

# Optional Path Parameters?

Unlike query parameters,

path parameters are **required**.

Example

```
/users/{id}
```

There is no request like

```
/users/
```

that can omit `id`.

If a value is optional,

it usually belongs in a **query parameter**, not the path.

______________________________________________________________________

# Path Metadata

FastAPI provides the `Path` helper.

Example

```python
from fastapi import Path

@app.get(

"/users/{id}"

)

def get_user(

    id: int = Path(

        ...,

        gt=0,

        description="User ID"

    )

):

    return {

        "id": id

    }
```

______________________________________________________________________

# Validation Using Path

Example

```python
id: int = Path(

    ...,

    ge=1,

    le=1000
)
```

Rules

```
Minimum

1
```

```
Maximum

1000
```

______________________________________________________________________

# Metadata in Swagger

Because of

```python
description=

"User ID"
```

Swagger automatically shows

```
User ID
```

as documentation.

______________________________________________________________________

# Aliases

Example

```python
id: int = Path(

    ...,

    alias="userId"
)
```

Aliases are less common for path parameters than for query parameters or request bodies.

______________________________________________________________________

# Path vs Query Parameter

Example

```
/users/10
```

```
10

↓

Path Parameter
```

______________________________________________________________________

```
/users?page=2
```

```
page

↓

Query Parameter
```

______________________________________________________________________

# REST API Design

Good

```
GET

/users/10
```

Bad

```
GET

/getUser?id=10
```

REST APIs use

- Resources
- Path Parameters

instead of action names.

______________________________________________________________________

# Real Examples

```
GET

/products/100
```

```
GET

/orders/200
```

```
GET

/users/10/orders
```

```
DELETE

/posts/99
```

All use path parameters.

______________________________________________________________________

# Common Mistakes

❌ Using query parameters for resource identifiers

```
/user?id=10
```

Instead

```
/users/10
```

______________________________________________________________________

❌ Forgetting type hints

```python
id
```

instead of

```python
id: int
```

______________________________________________________________________

❌ Defining

```
/users/{id}
```

before

```
/users/me
```

______________________________________________________________________

❌ Performing manual validation

```python
int(id)
```

FastAPI already validates types.

______________________________________________________________________

# Production Best Practices

- Use path parameters for resource identifiers.
- Use descriptive parameter names.
- Always use type hints.
- Use `Path()` for validation and documentation.
- Keep route ordering in mind.
- Avoid unnecessary manual validation.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why does FastAPI return HTTP 422 instead of HTTP 400 when a path parameter fails validation?**

### Answer

FastAPI uses Pydantic to validate incoming request data.

When the request structure is syntactically valid but fails semantic validation (for example, a string is provided where
an integer is expected), FastAPI returns:

```
422 Unprocessable Entity
```

This indicates that the server understood the request but could not process it because the data did not satisfy the
expected schema.

This provides more precise error reporting than a generic `400 Bad Request`.

______________________________________________________________________

# Summary

In this chapter you learned:

- Path Parameters
- Automatic Type Conversion
- Automatic Validation
- Multiple Path Parameters
- Enum Parameters
- Path Metadata
- REST API Design
- Validation with `Path()`
- Best Practices

Path parameters are the primary mechanism for identifying resources in REST APIs, and FastAPI automatically validates
and documents them using Python type hints.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a path parameter?
1. How is a path parameter different from a query parameter?
1. Why are path parameters commonly used in REST APIs?

______________________________________________________________________

## Validation

4. How does FastAPI validate path parameters?
1. What happens if `"abc"` is sent where an integer is expected?
1. Why does FastAPI return HTTP 422 for validation failures?

______________________________________________________________________

## Types

7. Which Python types can be used as path parameters?
1. How are UUID path parameters validated?
1. Why are Enum path parameters useful?

______________________________________________________________________

## Path()

10. What is the purpose of the `Path()` helper?
01. How can you enforce minimum and maximum values?
01. How does `Path()` improve API documentation?

______________________________________________________________________

## REST Design

13. Why is `/users/10` preferred over `/getUser?id=10`?
01. Why are path parameters required?

______________________________________________________________________

## Scenario-Based

15. Your application has routes `/users/{id}` and `/users/me`. Why does the order of route declarations matter?
01. A developer manually converts `id = int(id)` inside every route. Why is this unnecessary in FastAPI?
01. Your endpoint accepts a product ID between 1 and 1000. How would you enforce this using FastAPI?
01. An API receives `/orders/not-a-number`, but the route expects an integer order ID. Describe the request lifecycle up to the point where FastAPI returns an error.
01. A product catalog currently uses `/getProduct?id=100`. How would you redesign it to better follow REST principles?
01. Why are path parameters considered resource identifiers rather than filters?

______________________________________________________________________

# Next

[Query Parameters](05_query_parameters.md)
