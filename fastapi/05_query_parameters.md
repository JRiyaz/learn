# Query Parameters

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `05_query_parameters.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Query Parameters are
- Path Parameters vs Query Parameters
- Required vs Optional Parameters
- Default Values
- Automatic Type Conversion
- Automatic Validation
- Query Metadata
- Multiple Query Parameters
- Lists
- Aliases
- Best Practices

______________________________________________________________________

# What are Query Parameters?

A **Query Parameter** is data sent after the `?` in a URL.

Example

```
/users?page=1
```

Here

```
page=1
```

is a query parameter.

Multiple parameters

```
/users?page=1&limit=20
```

______________________________________________________________________

# URL Structure

```
/users

?

page=1

&

limit=20

&

sort=name
```

Everything after

```
?
```

belongs to query parameters.

______________________________________________________________________

# Why Do We Use Query Parameters?

Query parameters modify or filter a request without changing the resource.

Examples

- Pagination
- Filtering
- Sorting
- Searching
- Optional settings

Examples

```
/users?page=2
```

```
/products?category=laptop
```

```
/orders?status=pending
```

______________________________________________________________________

# Path vs Query Parameters

Path Parameter

```
/users/10
```

Meaning

```
Resource

↓

User 10
```

______________________________________________________________________

Query Parameter

```
/users?page=2
```

Meaning

```
Modify

↓

Returned Data
```

______________________________________________________________________

# Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")

def get_users(

    page: int = 1

):

    return {

        "page": page

    }
```

Request

```
/users?page=3
```

Response

```json
{
    "page": 3
}
```

______________________________________________________________________

# Default Values

```python
def users(

    page: int = 1

)
```

No parameter

```
/users
```

Result

```python
page == 1
```

The default value is used.

______________________________________________________________________

# Optional Parameters

```python
from typing import Optional

def users(

    search: Optional[str] = None

):

    ...
```

Requests

```
/users
```

or

```
/users?search=riyaz
```

Both are valid.

______________________________________________________________________

# Required Query Parameters

Remove the default value.

```python
@app.get("/users")

def users(

    page: int

):

    ...
```

Request

```
/users
```

Response

```
422

Validation Error
```

Because

```
page

↓

Required
```

______________________________________________________________________

# Automatic Type Conversion

Example

```python
page: int
```

Incoming

```
?page=5
```

Inside Python

```python
page == 5
```

Type

```
int
```

______________________________________________________________________

# Automatic Validation

Incoming

```
?page=abc
```

Expected

```python
page: int
```

Response

```
422
```

The route function is never executed.

______________________________________________________________________

# Multiple Query Parameters

```python
@app.get("/users")

def users(

    page: int = 1,

    limit: int = 20

):

    return {

        "page": page,

        "limit": limit

    }
```

Request

```
/users?page=2&limit=50
```

______________________________________________________________________

# Pagination Example

```
GET

/users?page=3&limit=25
```

Meaning

```
Page

↓

3
```

```
Items

↓

25
```

______________________________________________________________________

# Searching

```
GET

/users?search=riyaz
```

Search term

```
riyaz
```

______________________________________________________________________

# Filtering

```
GET

/products?category=laptop
```

Only laptops are returned.

______________________________________________________________________

# Sorting

```
GET

/products?sort=price
```

Descending

```
/products?sort=-price
```

Using a leading `-` for descending order is a common convention.

______________________________________________________________________

# Boolean Parameters

Example

```python
active: bool = True
```

Requests

```
?active=true

?active=false

?active=1

?active=0
```

FastAPI converts them automatically.

______________________________________________________________________

# Float Parameters

```python
price: float
```

Request

```
?price=99.99
```

Result

```python
99.99
```

______________________________________________________________________

# Query Validation

Use

```python
from fastapi import Query
```

Example

```python
page: int = Query(

    1,

    ge=1
)
```

Now

```
?page=0
```

returns

```
422
```

______________________________________________________________________

# Limit Validation

```python
limit: int = Query(

    20,

    ge=1,

    le=100
)
```

Rules

```
Minimum

1
```

```
Maximum

100
```

______________________________________________________________________

# Length Validation

```python
search: str = Query(

    ...,

    min_length=3,

    max_length=50
)
```

Useful for search terms.

______________________________________________________________________

# Regular Expressions (Pattern)

```python
search: str = Query(

    ...,

    pattern="^[a-zA-Z]+$"
)
```

Only alphabetic input is accepted.

______________________________________________________________________

# Query Metadata

```python
page: int = Query(

    1,

    description="Page Number"
)
```

Swagger automatically displays

```
Page Number
```

______________________________________________________________________

# Aliases

Example

```python
page: int = Query(

    1,

    alias="pageNumber"
)
```

Request

```
?pageNumber=5
```

Python variable

```python
page
```

Aliases help maintain backward compatibility or external API conventions.

______________________________________________________________________

# List Parameters

Example

```python
from typing import List

tags: List[str] = Query(

    []
)
```

Request

```
/products?

tags=laptop

&

tags=gaming
```

Result

```python
["laptop", "gaming"]
```

______________________________________________________________________

# Combining Path and Query Parameters

```python
@app.get(

"/users/{id}"

)

def user(

    id: int,

    details: bool = False

):

    ...
```

Request

```
/users/10?details=true
```

Path

```
10
```

Query

```
details=true
```

______________________________________________________________________

# Real API Examples

```
GET

/users?page=1&limit=20
```

```
GET

/products?category=books
```

```
GET

/orders?status=completed
```

```
GET

/posts?author=riyaz
```

______________________________________________________________________

# REST Guidelines

Use Path Parameters for

```
Resource IDs
```

Use Query Parameters for

```
Filtering

Sorting

Searching

Pagination
```

______________________________________________________________________

# Common Mistakes

❌ Using query parameters for resource IDs

```
/user?id=10
```

Instead

```
/users/10
```

______________________________________________________________________

❌ Manually converting types

```python
int(page)
```

FastAPI already does this.

______________________________________________________________________

❌ Returning all records without pagination

```
GET

/users
```

Large datasets should support pagination.

______________________________________________________________________

❌ Ignoring validation

Always validate

- Page
- Limit
- Search length
- Allowed values

______________________________________________________________________

# Production Best Practices

- Use query parameters for optional request modifiers.
- Provide sensible default values.
- Validate all inputs using `Query()`.
- Limit page sizes.
- Support filtering, searching, and sorting consistently.
- Document parameters using metadata.

______________________________________________________________________

# Interview Deep Dive

### Question

**When should you use a path parameter instead of a query parameter?**

### Answer

Use a **path parameter** when identifying a specific resource.

Example

```
GET /users/10
```

Here, `10` uniquely identifies a user.

Use a **query parameter** when modifying the result set or providing optional behavior.

Examples

```
GET /users?page=2

GET /users?search=riyaz

GET /users?sort=name
```

A good rule is:

- **Path parameters identify resources.**
- **Query parameters filter, sort, paginate, or customize responses.**

______________________________________________________________________

# Summary

In this chapter you learned:

- Query Parameters
- Required vs Optional Parameters
- Default Values
- Automatic Validation
- Type Conversion
- Query Metadata
- Lists
- Aliases
- Pagination
- Filtering
- Sorting

Query parameters provide a flexible way to customize API responses while FastAPI automatically validates and documents
them using Python type hints.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a query parameter?
1. How is a query parameter different from a path parameter?
1. When should query parameters be used?

______________________________________________________________________

## Validation

4. How does FastAPI validate query parameters?
1. What happens if `"abc"` is provided where an integer is expected?
1. How can minimum and maximum values be enforced?

______________________________________________________________________

## Query()

7. What is the purpose of `Query()`?
1. How do you add descriptions to query parameters?
1. What is an alias?

______________________________________________________________________

## Collections

10. How are list query parameters handled?
01. Why are default values useful?
01. When should a query parameter be required instead of optional?

______________________________________________________________________

## REST Design

13. Why should pagination use query parameters?
01. Why should filtering use query parameters?
01. Why shouldn't resource identifiers be passed as query parameters?

______________________________________________________________________

## Scenario-Based

16. Your `/users` endpoint currently returns all one million users. How would you redesign the API to improve scalability?
01. Your API accepts a `limit` parameter, but clients can request one million records at once. How would you prevent this?
01. A developer manually converts `page = int(page)` inside every endpoint. Why is this unnecessary?
01. Your product catalog needs to support category filtering, price sorting, and pagination simultaneously. How would you design the endpoint?
01. Your endpoint is `GET /products/10?details=true`. Explain why the product ID belongs in the path while `details` belongs in the query string.

______________________________________________________________________

# Next

[Request Body](06_request_body.md)
