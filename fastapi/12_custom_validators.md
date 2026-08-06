# Custom Validators

> **Course:** FastAPI for Backend Engineers
>
> **Module:** 2 - Validation using Pydantic
>
> **File:** `12_custom_validators.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why Custom Validators are Needed
- Built-in Validation vs Custom Validation
- `field_validator()`
- `model_validator()`
- Before vs After Validation
- Cross-field Validation
- Data Transformation
- Raising Validation Errors
- Reusable Validation
- Production Best Practices

______________________________________________________________________

# Why Custom Validators?

Built-in validation can check things like

- Integer
- String
- Email
- URL
- Length
- Numeric Range

But business rules are often more complex.

Examples

- Age must be at least 18
- Passwords must contain special characters
- End date must be after start date
- Username cannot contain reserved words

These require custom validation.

______________________________________________________________________

# Built-in Validation

Example

```python
class User(

    BaseModel

):

    age: int = Field(

        ge=18
    )
```

Good for

- Length
- Range
- Pattern

Not enough for business logic.

______________________________________________________________________

# Pydantic Validators

Pydantic v2 provides two primary validator types.

```
field_validator()

↓

One Field
```

```
model_validator()

↓

Entire Model
```

______________________________________________________________________

# field_validator()

Use

```python
from pydantic import (

    BaseModel,

    field_validator

)
```

Example

```python
class User(

    BaseModel

):

    name: str

    @field_validator(

        "name"

    )

    @classmethod

    def validate_name(

        cls,

        value

    ):

        return value
```

______________________________________________________________________

# How field_validator Works

```
Incoming Value

↓

Validator

↓

Return Value

↓

Stored in Model
```

______________________________________________________________________

# Reject Empty Names

```python
@field_validator(

    "name"

)

@classmethod

def validate_name(

    cls,

    value

):

    if not value.strip():

        raise ValueError(

            "Name cannot be empty"

        )

    return value
```

______________________________________________________________________

# Convert Data

Validators can transform values.

Example

```python
@field_validator(

    "name"

)

@classmethod

def title_case(

    cls,

    value

):

    return value.title()
```

Input

```
riyaz
```

Stored

```
Riyaz
```

______________________________________________________________________

# Validate Username

```python
RESERVED = {

    "admin",

    "root",

    "system"

}
```

```python
@field_validator(

    "username"

)

@classmethod

def username(

    cls,

    value

):

    if value.lower() in RESERVED:

        raise ValueError(

            "Reserved username"

        )

    return value
```

______________________________________________________________________

# Password Validation

```python
@field_validator(

    "password"

)

@classmethod

def password(

    cls,

    value

):

    if len(value) < 8:

        raise ValueError(

            "Password too short"

        )

    return value
```

Additional checks can enforce

- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

______________________________________________________________________

# Before Validation

Sometimes input must be transformed before type conversion.

```python
@field_validator(

    "age",

    mode="before"

)

@classmethod

def clean_age(

    cls,

    value

):

    return value
```

Flow

```
Raw Input

↓

Before Validator

↓

Type Conversion

↓

Model
```

______________________________________________________________________

# After Validation

Default behavior

```
Input

↓

Type Conversion

↓

Validator

↓

Model
```

Useful when working with already-converted Python types.

______________________________________________________________________

# model_validator()

Some rules involve multiple fields.

Example

```
Password

↓

Confirm Password
```

One field alone isn't enough.

______________________________________________________________________

# Example

```python
from pydantic import (

    model_validator

)
```

```python
class Register(

    BaseModel

):

    password: str

    confirm_password: str

    @model_validator(

        mode="after"

    )

    def passwords_match(

        self

    ):

        if self.password != self.confirm_password:

            raise ValueError(

                "Passwords do not match"

            )

        return self
```

______________________________________________________________________

# Cross-field Validation

Example

```
Start Date

↓

End Date
```

Rule

```
End Date

>

Start Date
```

Requires model-level validation.

______________________________________________________________________

# Date Example

```python
from datetime import date
```

```python
class Event(

    BaseModel

):

    start: date

    end: date

    @model_validator(

        mode="after"

    )

    def validate_dates(

        self

    ):

        if self.end <= self.start:

            raise ValueError(

                "End date must be after start date"

            )

        return self
```

______________________________________________________________________

# Raising Validation Errors

Simply raise

```python
ValueError(

    "Invalid Input"

)
```

FastAPI converts it into

```
422

Validation Error
```

______________________________________________________________________

# Validation Flow

```
JSON

↓

Pydantic

↓

Field Validators

↓

Model Validator

↓

Model Created
```

______________________________________________________________________

# Reusable Validation

Instead of duplicating logic

```
User

↓

Username Validator
```

```
Admin

↓

Username Validator
```

Extract reusable functions where appropriate.

______________________________________________________________________

# Data Normalization

Validators are useful for normalization.

Example

```python
@field_validator(

    "email"

)

@classmethod

def normalize(

    cls,

    value

):

    return value.lower().strip()
```

Input

```
 RIYAZ@EXAMPLE.COM
```

Stored

```
riyaz@example.com
```

______________________________________________________________________

# Validation vs Business Logic

Validation

```
Email Format

Password Length

Required Fields
```

Business Logic

```
Email Already Exists

Account Balance

Inventory Available
```

Business logic belongs in the service layer,

not validators.

______________________________________________________________________

# Common Use Cases

Validators commonly handle

- Username normalization
- Email normalization
- Password strength
- Date comparisons
- Reserved keywords
- Business formatting rules

______________________________________________________________________

# Common Mistakes

❌ Querying the database inside validators

❌ Putting business logic into validators

❌ Duplicating validation across models

❌ Performing expensive operations inside validators

❌ Forgetting to return the validated value

______________________________________________________________________

# Production Best Practices

- Keep validators focused on validation only.
- Use `field_validator()` for single fields.
- Use `model_validator()` for multiple fields.
- Normalize input where appropriate.
- Keep database queries out of validators.
- Raise clear validation errors.

______________________________________________________________________

# Interview Deep Dive

### Question

**When should you use `field_validator()` instead of `model_validator()`?**

### Answer

Use **`field_validator()`** when validation depends on a single field.

Examples:

- Validate username format.
- Normalize email addresses.
- Check password length.

Use **`model_validator()`** when validation depends on multiple fields.

Examples:

- Password matches confirmation password.
- End date is after start date.
- At least one of two optional fields is provided.

Choosing the correct validator keeps validation logic simple, reusable, and easy to maintain.

______________________________________________________________________

# Summary

In this chapter you learned:

- Custom Validators
- `field_validator()`
- `model_validator()`
- Before Validation
- After Validation
- Cross-field Validation
- Data Normalization
- Validation Errors
- Production Best Practices

Custom validators allow you to enforce business-specific validation rules while keeping request validation declarative
and maintainable.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. Why are custom validators needed?
1. When is built-in validation sufficient?
1. What is the purpose of `field_validator()`?

______________________________________________________________________

## Validators

4. What is the difference between `field_validator()` and `model_validator()`?
1. What is the difference between `mode="before"` and `mode="after"`?
1. Why must a validator return a value?

______________________________________________________________________

## Cross-field Validation

7. Why can't password confirmation be validated with only a field validator?
1. When should `model_validator()` be used?
1. How would you validate that an end date occurs after a start date?

______________________________________________________________________

## Design

10. Why should validators avoid database queries?
01. Why should business logic remain outside validators?
01. How can validators normalize incoming data?

______________________________________________________________________

## Production

13. Why should validation errors be clear and specific?
01. Why is reusable validation preferable to duplicated code?
01. What kinds of logic belong in the service layer instead of validators?

______________________________________________________________________

## Scenario-Based

16. Your registration API should reject usernames such as `admin` and `root`. How would you implement this?
01. A user enters `JOHN@EXAMPLE.COM` as their email. How would you normalize it before storing it?
01. Your booking API allows an end date earlier than the start date. Which validator would you use to prevent this?
01. A developer checks whether an email already exists in the database inside a Pydantic validator. Why is this considered poor design?
01. Your application requires passwords to contain uppercase letters, lowercase letters, numbers, and special characters. Where would you implement these checks, and why?

______________________________________________________________________

# Next

[Request & Response Validation](13_request_response_validation.md)
