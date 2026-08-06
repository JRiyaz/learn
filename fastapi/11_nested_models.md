# Nested Models

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 2 - Validation using Pydantic
>
> **File:** `11_nested_models.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Nested Models are
- Why Nested Models are Important
- One-to-One Relationships
- One-to-Many Relationships
- Deeply Nested Models
- Lists of Models
- Optional Nested Objects
- Dictionaries of Models
- Nested Validation
- Best Practices

______________________________________________________________________

# What are Nested Models?

A **Nested Model** is a Pydantic model that contains another Pydantic model as one of its fields.

Instead of

```
User

↓

city

country

zipcode
```

We group related fields.

```
User

↓

Address

↓

city

country

zipcode
```

This produces cleaner, reusable models.

______________________________________________________________________

# Why Do We Need Nested Models?

Imagine an e-commerce application.

A customer has

- Name
- Email
- Shipping Address
- Billing Address

Instead of placing every field inside one large model,

we organize related data.

______________________________________________________________________

# Without Nested Models

```python
class User(

    BaseModel

):

    name: str

    city: str

    country: str

    zipcode: str
```

As applications grow,

models become difficult to maintain.

______________________________________________________________________

# With Nested Models

```python
from pydantic import BaseModel

class Address(

    BaseModel

):

    city: str

    country: str

    zipcode: str
```

User

```python
class User(

    BaseModel

):

    name: str

    address: Address
```

Cleaner and reusable.

______________________________________________________________________

# Incoming JSON

```json
{
    "name": "Riyaz",
    "address": {
        "city": "Bangalore",
        "country": "India",
        "zipcode": "560037"
    }
}
```

FastAPI automatically converts the JSON into nested Python objects.

______________________________________________________________________

# Internal Flow

```
JSON

↓

User

↓

Address

↓

Validation

↓

Python Object
```

______________________________________________________________________

# Accessing Nested Fields

```python
user.address.city
```

No dictionary access is required.

______________________________________________________________________

# Nested Validation

Suppose

```python
zipcode: int
```

Incoming

```json
{
    "zipcode": "ABC"
}
```

Validation fails.

FastAPI returns

```
422

Validation Error
```

The entire request is rejected.

______________________________________________________________________

# Validation Happens Recursively

```
User

↓

Address

↓

Validation

↓

Success
```

Every nested model is validated independently.

______________________________________________________________________

# Multiple Nested Models

Example

```python
class Company(

    BaseModel

):

    name: str
```

```python
class User(

    BaseModel

):

    company: Company

    address: Address
```

JSON

```json
{
    "company": {

        "name": "OpenAI"

    },
    "address": {

        "city": "Bangalore",

        "country": "India",

        "zipcode": "560037"

    }
}
```

______________________________________________________________________

# One-to-Many Relationships

Example

A user has multiple addresses.

```python
from typing import List

class User(

    BaseModel

):

    addresses:

    List[Address]
```

______________________________________________________________________

# JSON

```json
{
    "addresses": [

        {
            "city": "Bangalore",
            "country": "India",
            "zipcode": "560037"
        },
        {
            "city": "Hyderabad",
            "country": "India",
            "zipcode": "500001"
        }
    ]
}
```

Each item is validated as an `Address`.

______________________________________________________________________

# List Validation

Flow

```
List

↓

Item 1

↓

Address Validation

↓

Item 2

↓

Address Validation
```

Every object must be valid.

______________________________________________________________________

# Deeply Nested Models

Example

```
Company

↓

Departments

↓

Employees

↓

Addresses
```

Each level can be represented by its own Pydantic model.

______________________________________________________________________

# Example

```python
Company

↓

Department

↓

Employee

↓

Address
```

FastAPI validates every level automatically.

______________________________________________________________________

# Optional Nested Objects

Example

```python
from typing import Optional

class User(

    BaseModel

):

    address:

    Optional[Address] = None
```

Valid

```json
{
    "name": "Riyaz"
}
```

or

```json
{
    "name": "Riyaz",
    "address": {
        "city": "Bangalore",
        "country": "India",
        "zipcode": "560037"
    }
}
```

______________________________________________________________________

# Dictionary of Models

Example

```python
from typing import Dict

class User(

    BaseModel

):

    offices:

    Dict[str, Address]
```

JSON

```json
{
    "offices": {
        "india": {
            "city": "Bangalore",
            "country": "India",
            "zipcode": "560037"
        },
        "usa": {
            "city": "Seattle",
            "country": "USA",
            "zipcode": "98101"
        }
    }
}
```

Each dictionary value is validated as an `Address`.

______________________________________________________________________

# Reusing Models

Example

```
Address

↓

User

↓

Supplier

↓

Warehouse

↓

Employee
```

One model,

many uses.

______________________________________________________________________

# Response Models

Nested models work exactly the same for responses.

```python
@app.get(

    "/users/{id}",

    response_model=User

)

def get_user():

    ...
```

Nested objects are serialized automatically.

______________________________________________________________________

# Database vs API Models

Database

```
User Table

Address Table
```

API

```
UserResponse

↓

AddressResponse
```

Keep API models independent from ORM models.

______________________________________________________________________

# Recursive Validation

```
User

↓

Address

↓

Country

↓

Validation

↓

Success
```

Validation stops at the first detected error.

______________________________________________________________________

# OpenAPI

Nested models automatically appear in Swagger.

Example

```
User

↓

Address

↓

Schema
```

Clients can clearly understand complex request structures.

______________________________________________________________________

# Real Production Example

```
Order

↓

Customer

↓

Shipping Address

↓

Items

↓

Product

↓

Price
```

Every object has its own model.

This approach scales much better than a single large model.

______________________________________________________________________

# Common Mistakes

❌ Creating one massive model with hundreds of fields

❌ Duplicating address fields across multiple models

❌ Returning ORM objects directly

❌ Using dictionaries instead of typed nested models

❌ Ignoring nested validation errors

______________________________________________________________________

# Production Best Practices

- Break complex objects into reusable models.
- Reuse nested models across the application.
- Keep request and response models separate.
- Use lists for one-to-many relationships.
- Keep nesting logical and maintainable.
- Avoid deeply nested structures unless the domain requires them.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why are nested Pydantic models preferred over flat models in large applications?**

### Answer

Nested models organize related data into reusable components.

Benefits include:

- Better readability.
- Easier maintenance.
- Reduced duplication.
- Automatic recursive validation.
- Reusable request and response schemas.
- Clearer API documentation.

As applications grow, nested models make the codebase significantly easier to understand and evolve.

______________________________________________________________________

# Summary

In this chapter you learned:

- Nested Models
- One-to-One Relationships
- One-to-Many Relationships
- Lists of Models
- Optional Nested Objects
- Dictionaries of Models
- Recursive Validation
- OpenAPI Integration
- Production Best Practices

Nested models are one of the most powerful features of Pydantic because they allow complex real-world objects to be
represented cleanly while maintaining automatic validation and documentation.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is a nested Pydantic model?
1. Why are nested models useful?
1. How does FastAPI validate nested models?

______________________________________________________________________

## Relationships

4. How do you represent a one-to-one relationship?
1. How do you represent a one-to-many relationship?
1. How are lists of nested models validated?

______________________________________________________________________

## Validation

7. What happens if a nested field fails validation?
1. How does recursive validation work?
1. Can nested models be optional?

______________________________________________________________________

## Design

10. Why should address information be extracted into a separate model?
01. Why should API models be separated from database models?
01. Why should reusable models be preferred over duplicated fields?

______________________________________________________________________

## Documentation

13. How do nested models improve Swagger documentation?
01. How are nested response models serialized?

______________________________________________________________________

## Scenario-Based

15. Your application has `Customer`, `Supplier`, and `Warehouse` models, all containing the same address fields. How would nested models improve the design?
01. An API request contains a list of 100 products, and one product has an invalid price. What happens during validation?
01. Your team uses plain dictionaries instead of typed nested models throughout the codebase. What disadvantages does this introduce?
01. A user may or may not have a billing address. How would you model this using Pydantic?
01. Your API receives a deeply nested order containing customer, shipping address, items, and product details. How does Pydantic validate such a request?
01. As your application grows, request models become hundreds of lines long. How can nested models improve maintainability and readability?

______________________________________________________________________

# Next

[Custom Validators](12_custom_validators.md)
