# Pydantic Models

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 2 - Validation using Pydantic
>
> **File:** `09_pydantic_models.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Pydantic is
- Why FastAPI uses Pydantic
- BaseModel
- Type Validation
- Type Conversion
- Nested Models
- Optional Fields
- Default Values
- Lists & Dictionaries
- Model Methods
- Common Mistakes
- Production Best Practices

______________________________________________________________________

# What is Pydantic?

Pydantic is a Python library for

- Data Validation
- Data Parsing
- Data Serialization
- Type Conversion

FastAPI uses Pydantic as its validation engine.

______________________________________________________________________

# Why Was Pydantic Created?

Imagine receiving data from a client.

```json
{
    "name": "Riyaz",
    "age": "28"
}
```

Without validation

```
Application

↓

Unexpected Errors
```

With Pydantic

```
Incoming Data

↓

Validate

↓

Convert Types

↓

Python Object
```

______________________________________________________________________

# Why FastAPI Uses Pydantic

FastAPI automatically uses Pydantic to

- Validate Requests
- Validate Responses
- Parse JSON
- Generate API Documentation
- Convert Types

Developers rarely need manual validation.

______________________________________________________________________

# BaseModel

Every Pydantic model inherits from

```python
BaseModel
```

Example

```python
from pydantic import BaseModel

class User(

    BaseModel

):

    name: str

    age: int
```

______________________________________________________________________

# Creating an Object

```python
user = User(

    name="Riyaz",

    age=28
)
```

Access

```python
user.name

user.age
```

Like a normal Python object.

______________________________________________________________________

# Automatic Validation

Model

```python
class User(

    BaseModel

):

    age: int
```

Input

```python
User(

    age="abc"
)
```

Result

```
Validation Error
```

______________________________________________________________________

# Automatic Type Conversion

Input

```python
User(

    age="28"
)
```

Internally

```python
age == 28
```

Type

```python
int
```

Pydantic converts compatible values automatically.

______________________________________________________________________

# Required Fields

```python
class User(

    BaseModel

):

    name: str
```

Input

```python
{}
```

Result

```
Validation Error
```

Because

```
name

↓

Required
```

______________________________________________________________________

# Optional Fields

```python
from typing import Optional

class User(

    BaseModel

):

    phone:

    Optional[str] = None
```

Valid

```python
User()
```

or

```python
User(

    phone="1234567890"

)
```

______________________________________________________________________

# Default Values

```python
class User(

    BaseModel

):

    active: bool = True
```

Input

```python
User()
```

Result

```python
active == True
```

______________________________________________________________________

# Multiple Fields

```python
class User(

    BaseModel

):

    name: str

    age: int

    email: str

    active: bool
```

Every field is validated independently.

______________________________________________________________________

# Nested Models

Address

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

# Input

```json
{
    "name": "Riyaz",
    "address": {
        "city": "Bangalore",
        "country": "India"
    }
}
```

Nested models are validated recursively.

______________________________________________________________________

# Lists

```python
from typing import List

class User(

    BaseModel

):

    skills: List[str]
```

Input

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

# Dictionary

```python
from typing import Dict

class User(

    BaseModel

):

    metadata:

    Dict[str, str]
```

Input

```json
{
    "metadata": {

        "team": "backend",

        "role": "developer"

    }
}
```

______________________________________________________________________

# Boolean Conversion

Input

```python
active="true"
```

Result

```python
True
```

Also accepts

```
1

yes

on

false

0
```

depending on supported parsing rules.

______________________________________________________________________

# Model Dump

Pydantic v2

```python
user.model_dump()
```

Output

```python
{
    "name": "Riyaz",
    "age": 28
}
```

Converts the model into a dictionary.

______________________________________________________________________

# JSON Output

```python
user.model_dump_json()
```

Result

```json
{
    "name":"Riyaz",
    "age":28
}
```

______________________________________________________________________

# Copy Model

```python
new_user = user.model_copy()
```

Useful when modifying objects without changing the original instance.

______________________________________________________________________

# Model Validation

Pydantic v2

```python
User.model_validate(

    data

)
```

Creates a validated model from a Python object.

______________________________________________________________________

# Field Information

Every field has metadata.

Example

```python
class User(

    BaseModel

):

    age: int
```

Pydantic understands

- Name
- Type
- Required Status
- Default Value

This information is also used to generate OpenAPI schemas.

______________________________________________________________________

# Internal Flow

```
JSON

↓

Pydantic

↓

Validation

↓

Type Conversion

↓

Python Object
```

______________________________________________________________________

# Pydantic in FastAPI

```
HTTP Request

↓

JSON

↓

Pydantic

↓

Validated Model

↓

Route

↓

Response Model

↓

JSON
```

Pydantic powers both request and response validation.

______________________________________________________________________

# Pydantic vs Dataclass

Dataclass

```
Stores Data
```

Pydantic

```
Stores Data

+

Validation

+

Parsing

+

Serialization
```

For API development,

Pydantic provides many additional features.

______________________________________________________________________

# Common Mistakes

❌ Using dictionaries everywhere

❌ Writing manual validation

❌ Reusing one model for every purpose

❌ Ignoring validation errors

❌ Returning database models directly instead of response models

______________________________________________________________________

# Production Best Practices

- Use Pydantic models for all API contracts.
- Separate request and response models.
- Reuse nested models.
- Prefer strong typing.
- Let Pydantic handle validation instead of writing custom validation for simple cases.
- Keep models focused and easy to understand.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is Pydantic one of the core reasons FastAPI is productive?**

### Answer

Pydantic eliminates much of the manual work required when handling API data.

It automatically provides:

- Type validation
- Type conversion
- Serialization
- Parsing
- API schema generation
- Clear validation errors

This reduces boilerplate code, improves API reliability, and integrates seamlessly with FastAPI's automatic
documentation and dependency injection systems.

______________________________________________________________________

# Summary

In this chapter you learned:

- Pydantic
- BaseModel
- Validation
- Type Conversion
- Nested Models
- Lists
- Dictionaries
- Model Dump
- Model Validation
- Production Best Practices

Pydantic is the foundation of FastAPI's request validation, response serialization, and automatic documentation, making
it one of the framework's most powerful features.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is Pydantic?
1. Why does FastAPI use Pydantic?
1. What is `BaseModel`?

______________________________________________________________________

## Validation

4. How does Pydantic validate incoming data?
1. What happens if a required field is missing?
1. How does automatic type conversion work?

______________________________________________________________________

## Models

7. How are nested models validated?
1. How are lists handled?
1. How are dictionaries handled?

______________________________________________________________________

## Model Methods

10. What does `model_dump()` do?
01. What does `model_dump_json()` do?
01. What does `model_validate()` do?

______________________________________________________________________

## Design

13. Why should request and response models be separate?
01. Why is Pydantic preferred over raw dictionaries?
01. How does Pydantic contribute to OpenAPI documentation?

______________________________________________________________________

## Scenario-Based

16. Your API receives `"age": "30"` while the model expects an integer. What does Pydantic do before the route executes?
01. A developer manually checks for missing fields and converts types inside every endpoint. How can Pydantic simplify this code?
01. Your application receives a nested JSON object containing a user, address, and company information. How should this be modeled using Pydantic?
01. Your project currently returns SQLAlchemy models directly from every endpoint. What advantages would dedicated Pydantic response models provide?
01. Your team wants to introduce automatic API documentation without writing schemas manually. How does Pydantic make this possible?

______________________________________________________________________

# Next

[Field Validation](10_field_validation.md)
