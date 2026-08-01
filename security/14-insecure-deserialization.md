# Security - Part 14

# Insecure Deserialization

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Serialization and Deserialization are
- What Insecure Deserialization is
- Why it is dangerous
- Python `pickle` risks
- Safe alternatives
- Secure FastAPI implementations
- Best practices

______________________________________________________________________

# What is Serialization?

Serialization is the process of converting an object into a format that can be stored or transmitted.

Example

```text id="ides1401"
Python Object

↓

JSON

↓

Network

↓

Another Application
```

Common serialization formats:

- JSON
- XML
- MessagePack
- Protocol Buffers
- Pickle (Python)

______________________________________________________________________

# What is Deserialization?

Deserialization is the reverse process.

```text id="ides1402"
JSON

↓

Python Object
```

Your FastAPI application does this every day.

Example

```json id="ides1403"
{
    "name": "Harry Potter",
    "author": "J.K. Rowling"
}
```

↓

```python id="ides1404"
Book(
    name="Harry Potter",
    author="J.K. Rowling"
)
```

This is completely normal.

______________________________________________________________________

# What is Insecure Deserialization?

Insecure Deserialization occurs when an application deserializes **untrusted data** using an unsafe format.

Some serialization formats

can execute code

while recreating objects.

This makes them extremely dangerous if the data comes from an untrusted source.

______________________________________________________________________

# Typical Flow

```text id="ides1405"
User Input

↓

Deserialize

↓

Object Created

↓

Unexpected Behavior
```

The vulnerability happens because

the application trusts

the serialized data.

______________________________________________________________________

# Why Is Python Pickle Dangerous?

Python provides

```text id="ides1406"
pickle
```

for serializing Python objects.

While `pickle` is useful internally,

it is **not safe for untrusted input**.

The official Python documentation explicitly warns against loading data from untrusted sources.

______________________________________________________________________

# Vulnerable Example

Suppose an application accepts uploaded serialized data.

```python id="ides1407"
import pickle

def load_data(data: bytes):
    return pickle.loads(data)
```

This looks simple,

but it's dangerous.

If `data`

comes from an untrusted user,

`pickle.loads()`

may execute unexpected code during deserialization.

______________________________________________________________________

# The Root Problem

The issue isn't

`pickle`.

The issue is

using it

on data

that an attacker controls.

Rule:

```text id="ides1408"
Trusted Data

↓

pickle

✓ Acceptable


Untrusted Data

↓

pickle

❌ Dangerous
```

______________________________________________________________________

# Safe Alternative 1

## JSON

JSON is the preferred format

for APIs.

Example

```python id="ides1409"
import json

book = json.loads(json_data)
```

JSON represents:

- Strings
- Numbers
- Lists
- Dictionaries

It does **not** recreate arbitrary Python objects.

______________________________________________________________________

# Safe Alternative 2

## Pydantic Models

FastAPI automatically validates JSON

using Pydantic.

Example

```python id="ides1410"
from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    author: str
```

The request body becomes

a validated Python object,

without unsafe deserialization.

______________________________________________________________________

# Safe Alternative 3

## Protocol Buffers

Large distributed systems

often use

```text id="ides1411"
Protocol Buffers
```

instead of Pickle.

Advantages:

- Language-independent
- Fast
- Compact
- Safe for network communication

We'll discuss Protocol Buffers later

during the Microservices module.

______________________________________________________________________

# FastAPI Example

Good workflow

```text id="ides1412"
JSON Request

↓

Pydantic Validation

↓

Python Object

↓

Business Logic
```

This is the recommended approach

for almost every FastAPI application.

______________________________________________________________________

# Internal vs External Data

Sometimes

`pickle`

is acceptable.

Example

```text id="ides1413"
Application

↓

Serialize Cache

↓

Application

↓

Deserialize
```

If **your own application**

created the data,

and no external user can modify it,

the risk is much lower.

The danger appears

when users supply the serialized data.

______________________________________________________________________

# Defense in Depth

Secure deserialization combines:

```text id="ides1414"
JSON

↓

Pydantic Validation

↓

Input Validation

↓

Authentication

↓

Authorization
```

______________________________________________________________________

# Best Practices

✅ Use JSON for APIs.

✅ Use Pydantic validation.

✅ Never use `pickle.loads()` on user input.

✅ Prefer language-independent formats.

✅ Validate every request.

______________________________________________________________________

# Common Mistakes

### Using Pickle for API Requests

Pickle should never be used

to receive data

from external users.

______________________________________________________________________

### Assuming Serialization Formats Are Equal

Not all formats

have the same security properties.

JSON and Pickle behave very differently.

______________________________________________________________________

### Skipping Validation

Even JSON

should still be validated.

Use Pydantic models.

______________________________________________________________________

### Trusting Client Data

Treat serialized data

like any other user input.

Never trust it.

______________________________________________________________________

# Quick Comparison

| Unsafe | Safe |
| ------------------------- | ---------------------------- |
| `pickle.loads(user_data)` | JSON + Pydantic |
| User-controlled Pickle | Validated JSON |
| Python-only format | Language-independent formats |
| No validation | Strong schema validation |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why is Python's `pickle` considered unsafe for untrusted input?

`pickle` can recreate arbitrary Python objects during deserialization. Because object reconstruction may execute
application-defined behavior, loading pickled data from an untrusted source can lead to unintended code execution or
other security issues. For network communication and APIs, developers should use safe formats such as JSON with Pydantic
validation instead of `pickle`.

______________________________________________________________________

# Summary

In this lesson, you learned:

- Serialization
- Deserialization
- Insecure Deserialization
- Why `pickle` is dangerous
- JSON vs Pickle
- Pydantic validation
- Safe alternatives
- Best practices

______________________________________________________________________

# What's Next

[Command Injection](15-command-injection.md)
