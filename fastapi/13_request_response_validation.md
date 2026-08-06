# Request & Response Validation

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 2 - Validation using Pydantic
>
> **File:** `13_request_response_validation.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Request Validation
- Response Validation
- Request Lifecycle
- Response Lifecycle
- Validation Order
- Validation Errors
- Request vs Response Models
- Error Responses
- Common Validation Scenarios
- Production Best Practices

______________________________________________________________________

# Why Validation Matters

Every API communicates with the outside world.

```
Internet

↓

Your API

↓

Database
```

The internet is **untrusted**.

Every request should be validated before reaching your business logic.

Every response should be validated before leaving your application.

______________________________________________________________________

# Two Types of Validation

FastAPI performs two major validations.

```
Incoming Request

↓

Request Validation
```

```
Outgoing Response

↓

Response Validation
```

______________________________________________________________________

# Request Validation

Incoming Request

```json
{
    "name": "Riyaz",
    "age": 28
}
```

Flow

```
JSON

↓

Pydantic

↓

Validation

↓

Python Object

↓

Route Function
```

If validation fails,

the route is never executed.

______________________________________________________________________

# Response Validation

Route

```python
return user
```

Flow

```
Python Object

↓

Response Model

↓

Validation

↓

JSON

↓

Client
```

The client only receives validated data.

______________________________________________________________________

# Complete Lifecycle

```
HTTP Request

↓

Path Validation

↓

Query Validation

↓

Header Validation

↓

Cookie Validation

↓

Body Validation

↓

Dependency Injection

↓

Route

↓

Business Logic

↓

Response Model

↓

Serialization

↓

HTTP Response
```

______________________________________________________________________

# Request Example

Model

```python
class UserCreate(

    BaseModel

):

    name: str

    age: int
```

Endpoint

```python
@app.post("/users")

def create(

    user: UserCreate

):

    ...
```

Incoming

```json
{
    "name": "Riyaz",
    "age": "28"
}
```

Pydantic converts

```
"28"

↓

28
```

______________________________________________________________________

# Invalid Request

Incoming

```json
{
    "name": "Riyaz",
    "age": "abc"
}
```

Result

```
422

Validation Error
```

Business logic is skipped.

______________________________________________________________________

# Missing Fields

Expected

```python
email: str
```

Incoming

```json
{
    "name": "Riyaz"
}
```

Result

```
422
```

______________________________________________________________________

# Invalid Nested Object

```json
{
    "address": {

        "zipcode": "ABC"
    }
}
```

Expected

```python
zipcode: int
```

Validation fails recursively.

______________________________________________________________________

# Response Example

```python
class UserResponse(

    BaseModel

):

    id: int

    name: str
```

Endpoint

```python
@app.get(

    "/users/{id}",

    response_model=UserResponse

)

def get_user():

    return {

        "id": 1,

        "name": "Riyaz"
    }
```

Valid response.

______________________________________________________________________

# Invalid Response

Expected

```python
age: int
```

Returned

```python
{
    "age": "Twenty"
}
```

FastAPI detects the mismatch.

This indicates an application bug rather than client error.

______________________________________________________________________

# Validation Order

```
Request

↓

Path

↓

Query

↓

Headers

↓

Cookies

↓

Body

↓

Dependencies

↓

Route

↓

Business Logic

↓

Response Validation

↓

JSON
```

Understanding this order helps explain why certain code never executes when validation fails.

______________________________________________________________________

# Automatic Type Conversion

Incoming

```json
{
    "price": "99.99"
}
```

Expected

```python
price: float
```

Result

```python
99.99
```

Converted automatically.

______________________________________________________________________

# Validation Error Structure

Example

```json
{
    "detail": [
        {
            "loc": [

                "body",

                "age"

            ],
            "msg": "...",
            "type": "..."
        }
    ]
}
```

Fields

```
loc

↓

Where Error Occurred
```

```
msg

↓

Description
```

```
type

↓

Error Category
```

______________________________________________________________________

# Common Validation Locations

```
Path
```

```
Query
```

```
Header
```

```
Cookie
```

```
Body
```

FastAPI reports the exact location of the error.

______________________________________________________________________

# Request vs Response

Request

```
Client

↓

Server
```

Response

```
Server

↓

Client
```

Validation is performed in both directions.

______________________________________________________________________

# Separate Models

Example

Request

```python
class UserCreate(

    BaseModel

):

    password: str
```

Response

```python
class UserResponse(

    BaseModel

):

    id: int

    email: str
```

The password is accepted but never returned.

______________________________________________________________________

# Security Benefit

Database

```python
{
    "password_hash": "...",

    "api_key": "...",

    "last_login_ip": "..."
}
```

Response Model

```python
{
    "id": 1,

    "name": "Riyaz"
}
```

Sensitive data is filtered automatically.

______________________________________________________________________

# Validation Flow Diagram

```
Client

↓

HTTP Request

↓

Pydantic Validation

↓

Business Logic

↓

Response Validation

↓

JSON Response

↓

Client
```

______________________________________________________________________

# Why Response Validation?

Without response validation

```
Developer Returns

↓

Wrong Data

↓

Client Breaks
```

With response validation

```
Developer Returns

↓

Schema Check

↓

Consistent API
```

______________________________________________________________________

# API Documentation

Request Models

↓

Swagger Request Schema

Response Models

↓

Swagger Response Schema

FastAPI generates both automatically.

______________________________________________________________________

# Real Production Example

```
POST /users

↓

Validate Request

↓

Hash Password

↓

Store Database

↓

Create Response

↓

Validate Response

↓

Return JSON
```

______________________________________________________________________

# Common Mistakes

❌ Using the same model for requests and responses

❌ Returning ORM/database models directly

❌ Disabling validation to "improve performance"

❌ Performing manual validation for simple type checks

❌ Returning inconsistent response structures

______________________________________________________________________

# Production Best Practices

- Validate every request.
- Validate every response.
- Separate request and response models.
- Return consistent JSON structures.
- Never expose internal database fields.
- Use validation errors to identify application bugs early.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why does FastAPI validate both requests and responses?**

### Answer

Request validation protects the application from invalid client input.

Response validation protects API consumers from incorrect or inconsistent server output.

Together they provide:

- Better security.
- Consistent API contracts.
- Early detection of programming errors.
- Reliable automatic documentation.
- Easier maintenance as applications grow.

Validating both directions improves confidence that the API behaves exactly as documented.

______________________________________________________________________

# Summary

In this chapter you learned:

- Request Validation
- Response Validation
- Validation Lifecycle
- Validation Order
- Automatic Type Conversion
- Error Responses
- Request vs Response Models
- Security Benefits
- Production Best Practices

Validation is one of FastAPI's strongest features because it automatically protects both the application and its clients
while producing consistent APIs and excellent documentation.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is request validation?
1. What is response validation?
1. Why should both be used?

______________________________________________________________________

## Lifecycle

4. At what stage is request validation performed?
1. At what stage is response validation performed?
1. What happens if request validation fails?

______________________________________________________________________

## Validation

7. What information is included in FastAPI's validation error responses?
1. Why does FastAPI automatically convert compatible types?
1. Why is validation recursive for nested models?

______________________________________________________________________

## API Design

10. Why should request and response models be separate?
01. Why shouldn't ORM models be returned directly?
01. How do response models improve API consistency?

______________________________________________________________________

## Security

13. How do response models prevent sensitive data leaks?
01. Why is the internet considered an untrusted source of input?
01. Why should every external request be validated?

______________________________________________________________________

## Scenario-Based

16. Your API accepts `"price": "99.99"` while the model expects a float. What happens before the route executes?
01. A route accidentally returns a password hash because no response model is defined. How could this have been prevented?
01. Your API receives a nested object where one deeply nested field has the wrong type. How does FastAPI handle this?
01. A teammate suggests removing response validation to reduce latency. What trade-offs would you discuss?
01. Your public API is consumed by multiple frontend and mobile applications. Why is response validation particularly valuable in this situation?

______________________________________________________________________

# Next

[APIRouter](14_api_router.md)
