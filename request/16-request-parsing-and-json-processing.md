# Complete HTTP Request Lifecycle Deep Dive

## 16. Request Parsing and Validation

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand how FastAPI converts an incoming HTTP request into Python objects, validates the data, handles errors, and prepares it for business logic.

______________________________________________________________________

# Introduction

After the request passes through

- Uvicorn
- ASGI
- Middleware

it reaches

your route handler.

However,

your endpoint

doesn't receive

raw JSON.

Instead,

FastAPI converts

the incoming data

into Python objects.

______________________________________________________________________

# High Level Flow

```
HTTP Request

↓

Request Body

↓

JSON Parsing

↓

Python Dictionary

↓

Pydantic Model

↓

Validation

↓

Route Handler
```

______________________________________________________________________

# Example Request

```
POST /users
```

Request Body

```json
{
    "name": "Riyaz",
    "email": "riyaz@gmail.com",
    "age": 25
}
```

______________________________________________________________________

# FastAPI Endpoint

```python
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

@app.post("/users")
async def create_user(user: UserCreate):
    return user
```

Notice

the endpoint

receives

a

`UserCreate`

object,

not

raw JSON.

______________________________________________________________________

# Step 1

# Read Request Body

FastAPI

reads

the request body

from

the ASGI server.

```
Bytes

↓

UTF-8 Text

↓

JSON
```

______________________________________________________________________

# Step 2

# Parse JSON

The JSON

is converted

into

a Python dictionary.

Example

```json
{
    "name":"Riyaz",
    "age":25
}
```

becomes

```python
{
    "name": "Riyaz",
    "age": 25
}
```

______________________________________________________________________

# Step 3

# Create Pydantic Model

FastAPI

creates

an instance

of

`UserCreate`

```python
user = UserCreate(
    name="Riyaz",
    email="riyaz@gmail.com",
    age=25
)
```

______________________________________________________________________

# Step 4

# Validation

Pydantic checks

every field.

Example

```
Name

↓

String?
```

```
Email

↓

Valid Email?
```

```
Age

↓

Integer?
```

If validation fails,

FastAPI

returns

```
422

Unprocessable Entity
```

______________________________________________________________________

# Example Validation Error

Request

```json
{
    "name": "Riyaz",
    "age": "twenty"
}
```

Response

```json
{
    "detail": [
        {
            "loc": ["body", "age"],
            "msg": "Input should be a valid integer"
        }
    ]
}
```

______________________________________________________________________

# Query Parameters

Example

```
GET /users?page=2&limit=20
```

```python
@app.get("/users")
async def get_users(
    page: int,
    limit: int
):
    ...
```

FastAPI

automatically converts

```
"2"

↓

2
```

______________________________________________________________________

# Path Parameters

```
GET /users/10
```

```python
@app.get("/users/{id}")
async def get_user(id: int):
    ...
```

If

```
/users/abc
```

FastAPI returns

```
422
```

because

`abc`

is not

an integer.

______________________________________________________________________

# Headers

Headers

can also

be validated.

```python
from fastapi import Header

async def demo(
    token: str = Header(...)
):
    ...
```

______________________________________________________________________

# Cookies

```python
from fastapi import Cookie

async def demo(
    session: str = Cookie(...)
):
    ...
```

______________________________________________________________________

# Default Values

```python
page: int = 1
```

If

the client

doesn't send

`page`,

FastAPI uses

```
1
```

______________________________________________________________________

# Optional Fields

```python
from typing import Optional

nickname: Optional[str] = None
```

Field

may be omitted.

______________________________________________________________________

# Validation Constraints

Example

```python
from pydantic import Field

age: int = Field(
    ge=18,
    le=100
)
```

Only values

between

18

and

100

are accepted.

______________________________________________________________________

# Common Data Types

```
str

int

float

bool

datetime

UUID

EmailStr

Decimal
```

______________________________________________________________________

# Nested Models

```python
class Address(BaseModel):
    city: str
    country: str

class User(BaseModel):
    name: str
    address: Address
```

FastAPI validates

nested objects

automatically.

______________________________________________________________________

# Lists

```python
tags: list[str]
```

Example

```json
{
    "tags": [
        "python",
        "fastapi"
    ]
}
```

______________________________________________________________________

# Response Models

Validation

also works

for responses.

```python
@app.get(
    "/users/{id}",
    response_model=User
)
```

Ensures

the response

matches

the expected schema.

______________________________________________________________________

# Benefits

- Automatic validation
- Cleaner code
- Better error messages
- Type safety
- API documentation

______________________________________________________________________

# Common Mistakes

## Trusting Client Data

Never assume

incoming data

is valid.

Always

validate it.

______________________________________________________________________

## Skipping Response Models

Response validation

helps prevent

accidentally exposing

internal fields.

______________________________________________________________________

## Overusing Optional Fields

Make fields

required

unless

they're truly optional.

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Framework | FastAPI |
| Validation | Pydantic |
| Serialization | JSON |
| Documentation | OpenAPI |

______________________________________________________________________

# Common Interview Questions

## Why does FastAPI use Pydantic?

Pydantic provides automatic validation, type conversion, serialization, and detailed error messages using Python type
hints.

______________________________________________________________________

## What status code is returned when request validation fails?

FastAPI returns **422 Unprocessable Entity**.

______________________________________________________________________

## Can FastAPI validate query parameters?

Yes.

FastAPI validates path parameters, query parameters, headers, cookies, and request bodies.

______________________________________________________________________

## Why use response models?

They ensure API responses follow the expected schema and help prevent exposing unwanted data.

______________________________________________________________________

# Interview Deep Dive

## Question

How does FastAPI process an incoming JSON request?

### Answer

FastAPI reads the request body, parses the JSON into a Python dictionary, creates a Pydantic model, validates all
fields, converts values to the correct Python types, and passes the validated object to the route handler. If validation
fails, it returns a 422 response with detailed error information.

______________________________________________________________________

# Summary

Before your business logic executes,

FastAPI ensures

that incoming data

is valid,

properly typed,

and safe to use.

This reduces boilerplate code

and helps prevent many common runtime errors.

______________________________________________________________________

# Next

[17. Authentication Deep Dive](17-authentication-deep-dive.md)
