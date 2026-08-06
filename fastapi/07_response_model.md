# Response Models

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `07_response_model.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Response Models are
- Why Response Models are Important
- Response Serialization
- Response Validation
- Filtering Response Data
- Multiple Response Models
- Response Status Codes
- Custom Responses
- Best Practices
- Common Mistakes

______________________________________________________________________

# What is a Response Model?

A **Response Model** defines the structure of the data your API sends back to the client.

Instead of returning arbitrary Python objects,

FastAPI validates and serializes the response according to a predefined schema.

______________________________________________________________________

# Why Do We Need Response Models?

Imagine your database contains

```python
{
    "id": 1,
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "password_hash": "$2b$...",
    "created_at": "...",
    "updated_at": "..."
}
```

Should the client receive everything?

**No.**

Only the required fields should be returned.

______________________________________________________________________

# Without a Response Model

```python
@app.get("/users/{id}")

def get_user(id: int):

    return database_user
```

Problem

```
Database Object

↓

Everything Returned
```

Including

- Password Hash
- Internal IDs
- Sensitive Information

______________________________________________________________________

# With a Response Model

```python
from pydantic import BaseModel

class UserResponse(

    BaseModel

):

    id: int

    name: str

    email: str
```

Endpoint

```python
@app.get(

    "/users/{id}",

    response_model=UserResponse

)

def get_user(id: int):

    return database_user
```

Only the declared fields are returned.

______________________________________________________________________

# Internal Flow

```
Database Object

↓

Response Model

↓

Validation

↓

Serialization

↓

JSON Response
```

______________________________________________________________________

# Example

Returned by database

```python
{
    "id": 1,
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "password_hash": "...",
    "is_admin": True
}
```

Response

```json
{
    "id": 1,
    "name": "Riyaz",
    "email": "riyaz@example.com"
}
```

Extra fields are excluded.

______________________________________________________________________

# Why Response Validation Matters

Suppose

```python
class UserResponse(

    BaseModel

):

    id: int

    age: int
```

But the route returns

```python
{
    "id": 1,

    "age": "twenty"
}
```

FastAPI validates the response.

If validation fails,

it indicates a bug in the application rather than incorrect client input.

______________________________________________________________________

# Response Serialization

Python Object

```python
UserResponse(

    id=1,

    name="Riyaz"

)
```

↓

JSON

```json
{
    "id": 1,
    "name": "Riyaz"
}
```

Serialization is automatic.

______________________________________________________________________

# Response Model vs Request Model

Request Model

```
Client

↓

Server
```

Response Model

```
Server

↓

Client
```

They often differ.

______________________________________________________________________

# Separate Request and Response Models

Example

```python
class UserCreate(

    BaseModel

):

    name: str

    email: str

    password: str
```

Response

```python
class UserResponse(

    BaseModel

):

    id: int

    name: str

    email: str
```

Notice

```
password

↓

Not Returned
```

______________________________________________________________________

# List Responses

Example

```python
from typing import List

@app.get(

    "/users",

    response_model=List[UserResponse]

)

def users():

    ...
```

Response

```json
[
    {
        "id": 1,
        "name": "Alice"
    },
    {
        "id": 2,
        "name": "Bob"
    }
]
```

______________________________________________________________________

# Nested Response Models

Example

```python
class Address(

    BaseModel

):

    city: str

    country: str
```

```python
class UserResponse(

    BaseModel

):

    name: str

    address: Address
```

Nested objects are serialized automatically.

______________________________________________________________________

# Optional Fields

```python
from typing import Optional

class UserResponse(

    BaseModel

):

    phone: Optional[str] = None
```

The field may be absent or `null`.

______________________________________________________________________

# Response Status Code

Example

```python
@app.post(

    "/users",

    status_code=201

)
```

Response

```
201 Created
```

______________________________________________________________________

# Common Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |

______________________________________________________________________

# Returning Custom Status Codes

```python
from fastapi import status

@app.post(

    "/users",

    status_code=status.HTTP_201_CREATED

)
```

Using the `status` module improves readability.

______________________________________________________________________

# Response Model Exclude

FastAPI supports excluding fields.

Example

```python
@app.get(

    "/users/{id}",

    response_model=UserResponse,

    response_model_exclude={

        "email"

    }

)
```

Useful for specific endpoints, though dedicated response models are often clearer.

______________________________________________________________________

# Response Model Include

Example

```python
response_model_include={

    "id",

    "name"

}
```

Only selected fields are returned.

______________________________________________________________________

# Excluding None Values

```python
response_model_exclude_none=True
```

Example

Without

```json
{
    "phone": null
}
```

With

```json
{}
```

______________________________________________________________________

# Custom Response

Sometimes JSON isn't enough.

FastAPI supports

- HTML
- Plain Text
- Streaming
- File Downloads
- Redirects

We'll cover these in later modules.

______________________________________________________________________

# OpenAPI Integration

Response models automatically appear in

```
Swagger

↓

Schemas
```

Clients immediately know what the endpoint returns.

______________________________________________________________________

# REST API Example

```
POST /users

↓

UserCreate

↓

Database

↓

UserResponse

↓

Client
```

Separate models improve security and maintainability.

______________________________________________________________________

# Common Mistakes

❌ Returning database models directly

❌ Using one model for requests and responses

❌ Returning password hashes

❌ Ignoring response validation

❌ Returning inconsistent JSON structures

______________________________________________________________________

# Production Best Practices

- Always define response models.
- Keep request and response models separate.
- Never expose internal database fields.
- Return appropriate HTTP status codes.
- Use response models for automatic documentation.
- Design stable API contracts.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should request models and response models be different in a production FastAPI application?**

### Answer

Request models describe the data clients are allowed to send.

Response models describe the data clients are allowed to receive.

Keeping them separate provides several benefits:

- Prevents accidental exposure of sensitive fields.
- Allows different validation rules for input and output.
- Makes API evolution easier.
- Improves readability and maintainability.
- Produces more accurate API documentation.

Using separate models is a common production practice.

______________________________________________________________________

# Summary

In this chapter you learned:

- Response Models
- Response Validation
- Response Serialization
- Nested Responses
- Lists
- Status Codes
- Response Filtering
- OpenAPI Integration
- Best Practices

Response models define the public contract of your API, ensuring consistent, secure, and well-documented responses while
preventing accidental exposure of internal data.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a response model?
1. Why are response models important?
1. How do response models differ from request models?

______________________________________________________________________

## Validation

4. What happens if the returned data doesn't match the response model?
1. Why is response validation useful?
1. How does FastAPI serialize Python objects into JSON?

______________________________________________________________________

## Models

7. Why should request and response models be separate?
1. How are nested response models handled?
1. How do you return a list of objects?

______________________________________________________________________

## Status Codes

10. How do you specify a custom response status code?
01. Why should REST APIs return meaningful status codes?
01. When should HTTP 201 be used instead of HTTP 200?

______________________________________________________________________

## Security

13. Why shouldn't database models be returned directly?
01. How do response models help prevent sensitive data leaks?
01. What kinds of fields should generally never appear in API responses?

______________________________________________________________________

## Scenario-Based

16. Your `User` database model contains `password_hash`, `is_admin`, and `last_login_ip`. How would you ensure these fields are never exposed to clients?
01. A developer uses the same `User` model for creating users and returning users from the API. What problems might this cause?
01. Your API returns different JSON structures for similar endpoints. How do response models improve consistency?
01. A route returns a string for the `age` field even though the response model expects an integer. What does FastAPI do?
01. Your public API is used by multiple mobile applications. Why is maintaining stable response models important for backward compatibility?

______________________________________________________________________

# Next

[Dependency Injection](08_dependency_injection.md)
