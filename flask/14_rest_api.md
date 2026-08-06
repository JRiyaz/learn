# Building REST APIs with Flask

> **Course:** Flask for Backend Engineers
>
> **Module:** 6
>
> **File:** `14_rest_api.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What REST is
- REST Principles
- Resources
- HTTP Methods
- URI Design
- Status Codes
- Request Validation
- JSON APIs
- API Versioning
- Pagination
- Filtering
- Sorting
- Idempotency
- REST Best Practices

______________________________________________________________________

# What is REST?

REST stands for

**Representational State Transfer**

It is an architectural style for designing web APIs.

Instead of exposing functions,

REST exposes **resources**.

Example

Bad

```
/getUsers
```

Good

```
/users
```

______________________________________________________________________

# What is a Resource?

A resource is any object managed by your application.

Examples

```
Users

Products

Orders

Payments

Invoices
```

Each resource is identified by a URI.

______________________________________________________________________

# REST Architecture

```
Client

↓

HTTP Request

↓

Flask API

↓

Business Logic

↓

Database

↓

JSON Response
```

Unlike server-rendered applications,

REST APIs primarily exchange JSON.

______________________________________________________________________

# REST Principles

A RESTful API should be:

- Client-Server
- Stateless
- Cacheable (where appropriate)
- Layered
- Resource-Oriented
- Consistent

______________________________________________________________________

# Stateless

Every request should contain everything needed to process it.

Good

```
Request

↓

JWT

↓

Authenticated
```

Bad

```
Server Memory

↓

Unknown State
```

Stateless APIs are easier to scale.

______________________________________________________________________

# HTTP Methods

| Method | Purpose |
|---------|----------|
| GET | Read |
| POST | Create |
| PUT | Replace |
| PATCH | Partial Update |
| DELETE | Delete |

______________________________________________________________________

# GET

Retrieve data.

```
GET /users
```

Response

```json
[
    {
        "id": 1,
        "name": "Alice"
    }
]
```

GET requests should not modify data.

______________________________________________________________________

# POST

Create a resource.

```
POST /users
```

Request

```json
{
    "name": "Riyaz"
}
```

Response

```
201 Created
```

______________________________________________________________________

# PUT

Replace an existing resource.

```
PUT /users/10
```

The client generally sends the full resource representation.

______________________________________________________________________

# PATCH

Update only part of a resource.

```
PATCH /users/10
```

Example

```json
{
    "email": "new@example.com"
}
```

Only the specified fields are updated.

______________________________________________________________________

# DELETE

```
DELETE /users/10
```

Response

```
204 No Content
```

The resource is removed.

______________________________________________________________________

# URI Design

Good

```
/users

/users/10

/orders

/orders/20/items
```

Bad

```
/getUsers

/deleteUser

/updateOrder
```

URIs represent nouns,

not actions.

______________________________________________________________________

# Nested Resources

Example

```
GET

/users/10/orders
```

Meaning

```
Orders

Belonging To

User 10
```

Avoid excessive nesting.

______________________________________________________________________

# Request Body

Create user

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com"
}
```

Read

```python
data = request.get_json()
```

Validate before processing.

______________________________________________________________________

# JSON Response

```python
return jsonify(

    {
        "id": 10,
        "name": "Riyaz"
    }

), 201
```

______________________________________________________________________

# HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

Choose status codes that accurately describe the outcome.

______________________________________________________________________

# Error Response

```json
{
    "success": false,
    "error": "User not found"
}
```

Keep error responses consistent.

______________________________________________________________________

# Success Response

```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Riyaz"
    }
}
```

A consistent response format simplifies client development.

______________________________________________________________________

# Request Validation

Always validate

- Required fields
- Types
- Length
- Business rules

Never trust client input.

______________________________________________________________________

# Pagination

Bad

```
GET /users
```

Returns

```
1 Million Users
```

______________________________________________________________________

Better

```
GET

/users?page=1&limit=20
```

Response

```
20 Users
```

______________________________________________________________________

# Filtering

```
GET

/users?active=true
```

______________________________________________________________________

# Searching

```
GET

/users?name=riyaz
```

______________________________________________________________________

# Sorting

```
GET

/users?sort=name
```

Descending

```
GET

/users?sort=-created_at
```

One convention is using a leading `-` for descending order.

______________________________________________________________________

# API Versioning

Example

```
/api/v1/users
```

Later

```
/api/v2/users
```

Versioning allows backward compatibility.

______________________________________________________________________

# Idempotency

An operation is **idempotent** if repeating it produces the same result.

Examples

```
GET
```

Always idempotent.

```
DELETE
```

Typically idempotent because deleting an already deleted resource does not create additional changes (the response code
may differ).

```
POST
```

Usually **not** idempotent.

______________________________________________________________________

# Content-Type

Request

```
Content-Type

application/json
```

Response

```
Content-Type

application/json
```

Clients and servers should agree on the payload format.

______________________________________________________________________

# Authentication

REST APIs commonly use

```
Authorization

Bearer TOKEN
```

Authentication is separate from the API design itself.

______________________________________________________________________

# Example Endpoint

```python
@app.route(

    "/users",

    methods=["POST"]

)
def create_user():

    data = request.get_json()

    return jsonify(data), 201
```

______________________________________________________________________

# API Layers

```
Route

↓

Validation

↓

Service

↓

Repository

↓

Database
```

Avoid placing business logic directly inside route functions.

______________________________________________________________________

# REST Flow

```
Client

↓

HTTP Request

↓

Validation

↓

Business Logic

↓

Database

↓

JSON Response
```

______________________________________________________________________

# Common Mistakes

❌ Using verbs in URLs

❌ Returning HTTP 200 for every outcome

❌ Ignoring request validation

❌ Returning inconsistent JSON

❌ Returning entire database tables without pagination

❌ Mixing business logic into route handlers

______________________________________________________________________

# Production Best Practices

- Use resource-oriented URLs.
- Return appropriate HTTP status codes.
- Validate all input.
- Keep JSON responses consistent.
- Support pagination.
- Support filtering and sorting.
- Version public APIs.
- Keep route handlers thin.
- Log important API requests and failures.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is `PATCH` different from `PUT`, and when should each be used?**

### Answer

`PUT` replaces the entire resource representation.

Clients typically send all fields, even those that are unchanged.

Example

```
PUT /users/10
```

`PATCH` performs a partial update.

Clients send only the fields that need to change.

Example

```
PATCH /users/10

{
    "email": "new@example.com"
}
```

`PATCH` is generally preferred for partial updates because it transfers less data and avoids unintentionally overwriting
unchanged fields.

______________________________________________________________________

# Summary

In this chapter you learned:

- REST
- Resources
- HTTP Methods
- URI Design
- Status Codes
- JSON APIs
- Validation
- Pagination
- Filtering
- Sorting
- Versioning
- Idempotency
- REST Best Practices

REST provides a consistent and scalable approach for designing web APIs that are easy for clients to understand and
integrate.

______________________________________________________________________

# Practice Questions

## REST Fundamentals

1. What is REST?
1. What is a resource?
1. Why should URLs use nouns instead of verbs?

______________________________________________________________________

## HTTP Methods

4. When should GET be used?
1. When should POST be used?
1. What is the difference between PUT and PATCH?
1. Why is DELETE generally considered idempotent?

______________________________________________________________________

## API Design

8. Why should APIs return JSON?
1. Why is request validation important?
1. Why should APIs return meaningful HTTP status codes?

______________________________________________________________________

## Scalability

11. Why is pagination necessary?
01. How are filtering and sorting typically implemented?
01. Why should public APIs be versioned?

______________________________________________________________________

## Architecture

14. Why should business logic remain outside route handlers?
01. What layers are commonly used in a Flask REST API architecture?

______________________________________________________________________

## Scenario-Based

16. Your endpoint is named `/deleteUser?id=10`. How would you redesign it to follow REST principles?
01. A GET endpoint accidentally updates a user's "last viewed" timestamp in the database. Why might this violate REST expectations?
01. Your API returns all 15 million products in a single request. What changes would you make?
01. Your mobile application expects the same JSON structure from every endpoint, but different endpoints return completely different formats. Why is this problematic?
01. A public API has been in use for years, but you need to introduce breaking changes. How would API versioning help?

______________________________________________________________________

# Next

[Error Handling](15_error_handling.md)
