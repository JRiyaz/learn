# Field Validation

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 2 - Validation using Pydantic
>
> **File:** `10_field_validation.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Field Validation is Important
- The `Field()` Function
- Numeric Validation
- String Validation
- Regular Expression Validation
- Decimal Validation
- List Validation
- Default Values
- Field Metadata
- Validation Errors
- Best Practices

______________________________________________________________________

# Why Field Validation?

Suppose your API creates a user.

Incoming Request

```json
{
    "name": "",
    "age": -10,
    "email": "abc"
}
```

Without validation

```
Invalid Data

↓

Database

↓

Application Problems
```

With validation

```
Invalid Request

↓

422 Validation Error

↓

Database Protected
```

______________________________________________________________________

# What is Field()?

Pydantic provides

```python
Field()
```

to define validation rules and metadata for model fields.

Example

```python
from pydantic import BaseModel, Field
```

______________________________________________________________________

# Basic Example

```python
class User(

    BaseModel

):

    name: str = Field(

        min_length=3,

        max_length=50
    )
```

Now

```
"Al"
```

is rejected.

______________________________________________________________________

# Field Syntax

```python
Field(

    default,

    validation,

    metadata
)
```

It can specify

- Default Values
- Validation Rules
- Descriptions
- Examples
- Titles

______________________________________________________________________

# Minimum Length

```python
name: str = Field(

    min_length=3
)
```

Valid

```
Riyaz
```

Invalid

```
Al
```

______________________________________________________________________

# Maximum Length

```python
name: str = Field(

    max_length=50
)
```

Prevents excessively long input.

______________________________________________________________________

# Combined Example

```python
name: str = Field(

    min_length=3,

    max_length=50
)
```

______________________________________________________________________

# Numeric Validation

Example

```python
age: int = Field(

    ge=18,

    le=100
)
```

Meaning

```
Minimum

18
```

```
Maximum

100
```

______________________________________________________________________

# Numeric Constraints

| Parameter | Meaning |
|-----------|----------|
| gt | Greater Than |
| ge | Greater Than or Equal |
| lt | Less Than |
| le | Less Than or Equal |

______________________________________________________________________

# Example

```python
price: float = Field(

    gt=0
)
```

Valid

```
99.99
```

Invalid

```
0

-5
```

______________________________________________________________________

# Decimal Validation

Example

```python
from decimal import Decimal

price: Decimal = Field(

    gt=0,

    decimal_places=2
)
```

Useful for

- Payments
- Banking
- Billing

Avoid floating-point rounding issues in financial applications.

______________________________________________________________________

# Regular Expressions

Example

```python
username: str = Field(

    pattern="^[a-zA-Z0-9_]+$"
)
```

Allowed

```
riyaz_123
```

Rejected

```
riyaz@
```

______________________________________________________________________

# Email Validation

Instead of

```python
email: str
```

Use

```python
from pydantic import EmailStr

email: EmailStr
```

Valid

```
abc@example.com
```

Invalid

```
abc
```

> **Note:** `EmailStr` requires the optional `email-validator` package:
>
> ```bash
> pip install email-validator
> ```

______________________________________________________________________

# URL Validation

Example

```python
from pydantic import HttpUrl

website: HttpUrl
```

Valid

```
https://example.com
```

Invalid

```
example
```

______________________________________________________________________

# UUID Validation

Example

```python
from uuid import UUID

id: UUID
```

Pydantic validates the UUID format automatically.

______________________________________________________________________

# List Validation

```python
from typing import List

scores: List[int]
```

Input

```json
{
    "scores": [

        90,

        80,

        70
    ]
}
```

Every item is validated.

______________________________________________________________________

# Field Metadata

```python
name: str = Field(

    description="Full Name"
)
```

Swagger automatically displays

```
Full Name
```

______________________________________________________________________

# Example Values

```python
name: str = Field(

    examples=[

        "Riyaz"

    ]
)
```

Examples appear in the generated API documentation.

______________________________________________________________________

# Default Values

```python
active: bool = Field(

    default=True
)
```

Equivalent to

```python
active: bool = True
```

`Field()` is useful when additional metadata or validation is needed.

______________________________________________________________________

# Optional Fields

```python
from typing import Optional

phone:

Optional[str] = Field(

    default=None,

    min_length=10
)
```

If provided,

validation still applies.

______________________________________________________________________

# Multiple Fields

```python
class User(

    BaseModel

):

    name: str = Field(

        min_length=3

    )

    age: int = Field(

        ge=18

    )

    email: EmailStr
```

Each field has its own validation rules.

______________________________________________________________________

# Validation Flow

```
JSON

↓

Field Rules

↓

Validation

↓

Model

↓

Route
```

______________________________________________________________________

# Validation Errors

Input

```json
{
    "age": -10
}
```

Response

```json
{
    "detail": [
        {
            "loc": [

                "body",

                "age"

            ],

            "msg": "Input should be greater than or equal to 18"
        }
    ]
}
```

FastAPI generates structured error responses automatically.

______________________________________________________________________

# Common Validation Rules

| Type | Example |
|------|----------|
| Length | `min_length`, `max_length` |
| Number | `gt`, `ge`, `lt`, `le` |
| Regex | `pattern` |
| Email | `EmailStr` |
| URL | `HttpUrl` |
| UUID | `UUID` |
| Decimal | `Decimal` |

______________________________________________________________________

# Real Production Example

```python
class Product(

    BaseModel

):

    name: str = Field(

        min_length=3,

        max_length=100

    )

    price: Decimal = Field(

        gt=0

    )

    stock: int = Field(

        ge=0

    )

    description: str = Field(

        max_length=500
    )
```

This model prevents many invalid requests before business logic begins.

______________________________________________________________________

# Common Mistakes

❌ Validating data manually inside route functions

❌ Accepting empty strings for required fields

❌ Using `float` for monetary values

❌ Forgetting upper limits on pagination or string lengths

❌ Returning unclear validation errors instead of relying on Pydantic

______________________________________________________________________

# Production Best Practices

- Validate every external input.
- Use `Field()` for constraints and documentation.
- Use `EmailStr` for email addresses.
- Use `HttpUrl` for URLs.
- Use `Decimal` for financial values.
- Keep validation rules close to the model.
- Let FastAPI return standard validation errors.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why is validation at the API boundary considered a best practice?**

### Answer

The API boundary is the first point where external data enters the application.

Validating data immediately provides several benefits:

- Prevents invalid data from reaching business logic.
- Protects the database from inconsistent data.
- Produces consistent error responses.
- Reduces defensive checks throughout the application.
- Improves application security and reliability.

Pydantic allows these validations to be declared once in the model rather than repeated throughout the codebase.

______________________________________________________________________

# Summary

In this chapter you learned:

- `Field()`
- Numeric Validation
- String Validation
- Email Validation
- URL Validation
- UUID Validation
- Decimal Validation
- Metadata
- Validation Errors
- Production Best Practices

Field validation ensures that incoming data satisfies business and technical requirements before it reaches the
application's core logic.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is `Field()`?
1. Why is field validation important?
1. Where should validation occur in a FastAPI application?

______________________________________________________________________

## Validation Rules

4. What is the difference between `gt` and `ge`?
1. What is the difference between `lt` and `le`?
1. How do you validate string length?
1. How do you validate numeric ranges?

______________________________________________________________________

## Specialized Types

8. Why should `EmailStr` be used instead of `str`?
1. Why is `HttpUrl` useful?
1. Why is `Decimal` preferred over `float` for money?

______________________________________________________________________

## Metadata

11. How does `Field()` improve Swagger documentation?
01. What is the purpose of field descriptions and examples?

______________________________________________________________________

## Production

13. Why should validation rules be defined inside models instead of route functions?
01. Why should user input always be validated before business logic executes?
01. What kinds of data should always have validation constraints?

______________________________________________________________________

## Scenario-Based

16. Your product API accepts negative prices. How would you prevent this using Pydantic?
01. A user registers with the email `"not-an-email"`. How can Pydantic reject this automatically?
01. Your API accepts usernames containing spaces and special characters, but your business rules forbid them. How would you enforce this?
01. A developer uses `float` for storing currency values in payment APIs. What issues can arise, and what type would you recommend instead?
01. Your team validates request fields manually in every endpoint. How can `Field()` and Pydantic simplify the application architecture?

______________________________________________________________________

# Next

[Nested Models](11_nested_models.md)
