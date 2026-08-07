# Complete HTTP Request Lifecycle Deep Dive

## 19. Validation and Sanitization

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand the difference between validation and sanitization, why both are important, common validation techniques, input sanitization, and how they protect backend applications from security vulnerabilities.

______________________________________________________________________

# Introduction

The request has successfully passed

- Authentication
- Authorization

Now,

before

executing

the business logic,

the backend must ensure

that

the input

is

valid

and

safe.

This is done using

```
Validation

+

Sanitization
```

______________________________________________________________________

# High Level Flow

```
Incoming Request

↓

Validation

↓

Sanitization

↓

Business Logic

↓

Database
```

If validation fails,

the request

is rejected

before

any database query

or business logic

is executed.

______________________________________________________________________

# Validation vs Sanitization

Interview favorite.

## Validation

Checks whether

the input

is correct.

Example

```
Age

↓

Must be Integer
```

______________________________________________________________________

## Sanitization

Modifies

or cleans

the input

to make it safe.

Example

```
"   Riyaz   "

↓

"Riyaz"
```

______________________________________________________________________

# Example

Incoming Request

```json
{
    "email": "riyaz@gmail",
    "age": -5
}
```

Validation

detects

- Invalid email
- Invalid age

Request is rejected.

______________________________________________________________________

# Why Validation is Important

Without validation,

the application

may receive

- Invalid data
- Missing fields
- Unexpected types
- Malicious input

This can lead to

application errors

or

security vulnerabilities.

______________________________________________________________________

# Common Validation Types

## Required Fields

```python
name: str
```

If missing,

FastAPI returns

```
422
```

______________________________________________________________________

## Data Type Validation

```
Age

↓

Integer
```

```
Price

↓

Float
```

```
Email

↓

Email Format
```

______________________________________________________________________

## Length Validation

Example

```python
password: str = Field(
    min_length=8,
    max_length=50
)
```

______________________________________________________________________

## Range Validation

Example

```python
age: int = Field(
    ge=18,
    le=100
)
```

______________________________________________________________________

## Pattern Validation

Example

Phone Number

```
9876543210
```

Must match

a predefined pattern.

______________________________________________________________________

## Enum Validation

Example

```python
status: Literal[
    "pending",
    "completed",
    "cancelled"
]
```

Only

allowed values

are accepted.

______________________________________________________________________

# Cross-Field Validation

Sometimes

one field

depends

on another.

Example

```
Start Date

↓

End Date
```

End Date

must be

after

Start Date.

______________________________________________________________________

# Business Validation

Not all validation

is about

data types.

Example

```
Transfer Amount

↓

Available Balance?
```

Even if

the amount

is numeric,

the transaction

should fail

if funds

are insufficient.

______________________________________________________________________

# What is Sanitization?

Sanitization

cleans

the input

before

using it.

Examples

- Remove extra spaces
- Normalize case
- Remove dangerous characters
- Escape HTML

______________________________________________________________________

# Example

Input

```
"   Riyaz   "
```

Sanitized

```
"Riyaz"
```

______________________________________________________________________

# Lowercase Emails

Example

```
RIYAZ@GMAIL.COM

↓

riyaz@gmail.com
```

Helps

avoid

duplicate accounts.

______________________________________________________________________

# Removing Dangerous HTML

Suppose

the user submits

```html
<script>
alert("Hack")
</script>
```

The backend

should

sanitize

or reject

this input,

depending

on the application.

______________________________________________________________________

# SQL Injection

Interview favorite.

Suppose

the user enters

```
' OR 1=1 --
```

Never build

SQL queries

using string concatenation.

Bad

```python
query = f"""
SELECT *

FROM users

WHERE name='{name}'
"""
```

Good

Use

parameterized queries.

```python
SELECT *

FROM users

WHERE name = ?
```

ORMs

like SQLAlchemy

help prevent

SQL Injection

when used correctly.

______________________________________________________________________

# Cross-Site Scripting (XSS)

Suppose

a comment contains

```html
<script>
alert("XSS")
</script>
```

If rendered

without escaping,

the browser

executes it.

Mitigation

- Escape HTML
- Sanitize user content
- Use Content Security Policy (CSP)

______________________________________________________________________

# Command Injection

Never execute

user input

directly

as

system commands.

Bad

```python
os.system(user_input)
```

Use

safe APIs

and avoid

shell execution

whenever possible.

______________________________________________________________________

# File Upload Validation

Always validate

uploaded files.

Check

- File type
- File extension
- File size
- MIME type

Never trust

the filename alone.

______________________________________________________________________

# URL Validation

If users

submit URLs,

verify

that they

follow

expected formats.

Reject

invalid

or malformed URLs.

______________________________________________________________________

# Email Validation

Check

- Format
- Length
- Domain (if required)

Validation

does not guarantee

that

the email

actually exists.

______________________________________________________________________

# Password Validation

Good password rules

may include

- Minimum length
- Uppercase letter
- Lowercase letter
- Number
- Special character

Do not

store passwords

before hashing them.

______________________________________________________________________

# Client-Side vs Server-Side Validation

Interview favorite.

Client-side

validation

improves

user experience.

Server-side

validation

provides

security.

Always

validate

on the server,

even if

the frontend

already validates.

______________________________________________________________________

# Error Messages

Avoid exposing

internal details.

Good

```
Invalid credentials
```

Avoid

```
SQL Error

Column password not found
```

______________________________________________________________________

# Validation Libraries

Examples

- Pydantic
- Marshmallow
- Cerberus

FastAPI

primarily uses

Pydantic.

______________________________________________________________________

# Common Validation Mistakes

## Trusting Client Input

Never trust

incoming data.

Always validate

on the backend.

______________________________________________________________________

## Skipping Business Rules

Correct data types

do not guarantee

valid business logic.

______________________________________________________________________

## Using String Concatenation in SQL

Always use

parameterized queries

or an ORM.

______________________________________________________________________

## Relying Only on Frontend Validation

Attackers

can bypass

frontend validation

by calling

your API directly.

______________________________________________________________________

# Best Practices

- Validate every request
- Sanitize user input where appropriate
- Use parameterized queries
- Escape output when rendering HTML
- Validate uploaded files
- Keep validation rules centralized
- Return clear but safe error messages

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Validation | Pydantic |
| ORM | SQLAlchemy |
| HTML Sanitization | Bleach (Python) |
| Password Validation | Pydantic Validators |
| File Validation | python-magic |

______________________________________________________________________

# Common Interview Questions

## What is the difference between validation and sanitization?

Validation checks whether input is acceptable, while sanitization cleans or transforms input into a safe format.

______________________________________________________________________

## Why is server-side validation required if the frontend already validates input?

Frontend validation can be bypassed. Server-side validation is the trusted security layer and must validate every
request.

______________________________________________________________________

## How do ORMs help prevent SQL Injection?

ORMs use parameterized queries instead of concatenating user input into SQL statements, reducing the risk of SQL
Injection.

______________________________________________________________________

## Should all user input be sanitized?

Not always. Data should first be validated. Sanitization should be applied where appropriate, such as trimming
whitespace or escaping HTML before rendering.

______________________________________________________________________

## Why shouldn't detailed validation errors expose internal information?

Detailed internal errors may reveal implementation details that attackers can use to identify vulnerabilities.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain the difference between validation and sanitization with an example.

### Answer

Validation checks whether input meets predefined rules, such as ensuring an email is properly formatted or an age is
within an acceptable range. Sanitization modifies or cleans valid input, such as trimming whitespace, converting emails
to lowercase, or escaping HTML before displaying user-generated content. Validation ensures correctness, while
sanitization improves consistency and safety.

______________________________________________________________________

# Summary

Validation and sanitization work together to ensure

that incoming data

is both

correct

and

safe.

Validation rejects invalid input,

while sanitization cleans acceptable input before it is processed or stored.

These practices help protect applications from common attacks such as SQL Injection and Cross-Site Scripting (XSS).

______________________________________________________________________

# Next

[20. Business Logic Layer](20-business-logic-layer.md)
