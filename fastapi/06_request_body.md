# Request Body

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 1 - FastAPI Fundamentals
>
> **File:** `06_request_body.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What a Request Body is
- HTTP Methods that use Request Bodies
- Pydantic Models
- Automatic Validation
- Nested Objects
- Optional Fields
- Default Values
- Multiple Request Bodies
- Mixing Path, Query, and Body Parameters
- Best Practices

______________________________________________________________________

# What is a Request Body?

A **Request Body** is the data sent by the client inside an HTTP request.

Example

```
POST /users
```

Body

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "age": 28
}
```

The server reads this data to create or update resources.

______________________________________________________________________

# Why Do We Need a Request Body?

Imagine creating a user.

Without a request body

```
POST

/users

?
name=Riyaz

&
email=riyaz@example.com

&
age=28
```

This quickly becomes difficult to manage.

Instead

```
POST

/users
```

Body

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "age": 28
}
```

Much cleaner.

______________________________________________________________________

# HTTP Methods and Request Bodies

| Method | Request Body |
|---------|--------------|
| GET | Usually No |
| POST | Yes |
| PUT | Yes |
| PATCH | Yes |
| DELETE | Sometimes (depends on API design, but uncommon) |

______________________________________________________________________

# How FastAPI Reads a Request Body

FastAPI uses **Pydantic models**.

Example

```python
from pydantic import BaseModel

class User(

    BaseModel

):

    name: str

    email: str

    age: int
```

______________________________________________________________________

# Using the Model

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users")

def create_user(

    user: User

):

    return user
```

______________________________________________________________________

# Incoming Request

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "age": 28
}
```

______________________________________________________________________

# Response

```json
{
    "name": "Riyaz",
    "email": "riyaz@example.com",
    "age": 28
}
```

FastAPI automatically

- Parses JSON
- Validates fields
- Creates a Python object

______________________________________________________________________

# Internal Flow

```
HTTP Request

↓

JSON

↓

Pydantic Model

↓

Validation

↓

Python Object

↓

Route Function
```

______________________________________________________________________

# Accessing Fields

```python
@app.post("/users")

def create_user(

    user: User

):

    return {

        "name": user.name

    }
```

No dictionary access is required.

______________________________________________________________________

# Automatic Validation

Model

```python
class User(

    BaseModel

):

    age: int
```

Incoming

```json
{
    "age": "abc"
}
```

FastAPI returns

```
422

Validation Error
```

The route function never executes.

______________________________________________________________________

# Missing Required Fields

Model

```python
class User(

    BaseModel

):

    name: str

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

Because

```
email

↓

Missing
```

______________________________________________________________________

# Optional Fields

```python
from typing import Optional

class User(

    BaseModel

):

    phone: Optional[str] = None
```

Requests

```json
{
    "phone": "1234567890"
}
```

or

```json
{}
```

Both are valid.

______________________________________________________________________

# Default Values

```python
class User(

    BaseModel

):

    active: bool = True
```

Incoming

```json
{
    "name": "Riyaz"
}
```

Internally

```python
active == True
```

______________________________________________________________________

# Nested Models

Example

```python
class Address(

    BaseModel

):

    city: str

    country: str
```

User

```python
class User(

    BaseModel

):

    name: str

    address: Address
```

______________________________________________________________________

# Incoming JSON

```json
{
    "name": "Riyaz",
    "address": {
        "city": "Bangalore",
        "country": "India"
    }
}
```

Nested validation happens automatically.

______________________________________________________________________

# Lists

```python
from typing import List

class User(

    BaseModel

):

    skills: List[str]
```

JSON

```json
{
    "skills": [

        "Python",

        "FastAPI",

        "Docker"

    ]
}
```

______________________________________________________________________

# Dictionaries

```python
from typing import Dict

metadata: Dict[str, str]
```

Example

```json
{
    "metadata": {
        "team": "backend",
        "project": "api"
    }
}
```

______________________________________________________________________

# Multiple Models

```python
class Address(

    BaseModel

):

    city: str
```

```python
class Company(

    BaseModel

):

    name: str
```

Models can be reused across multiple endpoints.

______________________________________________________________________

# Multiple Request Bodies

FastAPI supports multiple body parameters.

Example

```python
class User(

    BaseModel

):

    name: str
```

```python
class Address(

    BaseModel

):

    city: str
```

Endpoint

```python
@app.post("/users")

def create(

    user: User,

    address: Address

):

    ...
```

Expected JSON

```json
{
    "user": {
        "name": "Riyaz"
    },
    "address": {
        "city": "Bangalore"
    }
}
```

______________________________________________________________________

# Mixing Path, Query and Body

Example

```python
@app.put(

"/users/{id}"

)

def update(

    id: int,

    notify: bool,

    user: User

):

    ...
```

Request

```
PUT

/users/10?notify=true
```

Body

```json
{
    "name": "Riyaz"
}
```

FastAPI automatically determines

```
id

↓

Path
```

```
notify

↓

Query
```

```
user

↓

Body
```

______________________________________________________________________

# Body()

Sometimes you want additional metadata.

```python
from fastapi import Body
```

Example

```python
name: str = Body(

    ...,

    min_length=3
)
```

Useful for primitive body values.

______________________________________________________________________

# Embed Request Body

Without embedding

```json
{
    "name": "Riyaz"
}
```

With

```python
Body(

    embed=True
)
```

JSON

```json
{
    "user": {
        "name": "Riyaz"
    }
}
```

Useful for APIs that require wrapped payloads.

______________________________________________________________________

# Request Body vs Query Parameters

Query

```
Filtering

Pagination

Sorting
```

Body

```
Create

Update

Complex Data
```

______________________________________________________________________

# Real Examples

Create User

```
POST

/users
```

Update User

```
PUT

/users/10
```

Update Email

```
PATCH

/users/10
```

All typically use request bodies.

______________________________________________________________________

# Validation Flow

```
Request

↓

JSON

↓

Pydantic

↓

Validation

↓

Python Object

↓

Route
```

No manual validation is required for standard type checking.

______________________________________________________________________

# Common Mistakes

❌ Accepting raw dictionaries everywhere

```python
dict
```

Instead

```python
User
```

______________________________________________________________________

❌ Performing manual validation

```python
if "name" not in data
```

Pydantic already validates required fields.

______________________________________________________________________

❌ Putting large objects into query parameters

Use the request body instead.

______________________________________________________________________

❌ Returning unvalidated input directly without considering response models

We'll discuss response models later.

______________________________________________________________________

# Production Best Practices

- Use Pydantic models for all request bodies.
- Keep request models focused on a single purpose.
- Reuse nested models where appropriate.
- Use optional fields carefully.
- Validate all incoming data.
- Separate request models from database models.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should FastAPI applications use Pydantic models instead of accepting raw dictionaries for request bodies?**

### Answer

Pydantic models provide:

- Automatic validation
- Type conversion
- Clear API documentation
- Better editor support
- Improved maintainability
- Consistent error responses

Compared to raw dictionaries, Pydantic significantly reduces manual validation code and catches invalid input before
business logic executes.

______________________________________________________________________

# Summary

In this chapter you learned:

- Request Bodies
- Pydantic Models
- Automatic Validation
- Nested Models
- Lists
- Optional Fields
- Default Values
- Multiple Request Bodies
- Body()
- Mixing Path, Query, and Body Parameters

Request bodies are the primary way clients send structured data to FastAPI, and Pydantic enables automatic validation,
parsing, and documentation with very little code.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a request body?
1. Which HTTP methods commonly use request bodies?
1. Why are request bodies preferred over query parameters for creating resources?

______________________________________________________________________

## Pydantic

4. What is a Pydantic model?
1. How does FastAPI use Pydantic during request processing?
1. What happens if a required field is missing?

______________________________________________________________________

## Validation

7. What happens if `"age": "abc"` is sent where an integer is expected?
1. Why does the route function not execute when validation fails?
1. How are nested objects validated?

______________________________________________________________________

## Models

10. Why should nested models be reused?
01. What is the purpose of optional fields?
01. When would you use `Body(embed=True)`?

______________________________________________________________________

## API Design

13. How does FastAPI distinguish between path, query, and body parameters?
01. Why should request models be separated from database models?
01. Why is accepting raw dictionaries generally discouraged?

______________________________________________________________________

## Scenario-Based

16. A developer accepts `dict` as the request body for every endpoint and manually checks for missing fields. How could Pydantic simplify this design?
01. Your endpoint receives a nested JSON object representing a user and their address. How would you model this in FastAPI?
01. An API currently sends 20 fields through query parameters when creating a product. How would you redesign the endpoint?
01. Your application receives invalid JSON where the `price` field is a string instead of a float. Describe what FastAPI does before the route function executes.
01. Your project uses the same `User` model for API requests, API responses, and database operations. Why can this become a maintenance and security problem?

______________________________________________________________________

# Next

[Response Models](07_response_model.md)
