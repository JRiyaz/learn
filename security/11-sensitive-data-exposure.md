# Security - Part 11

# Sensitive Data Exposure

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Sensitive Data Exposure is
- What data should be protected
- Common ways sensitive data leaks
- Secure handling in Python and FastAPI
- Logging best practices
- Data masking
- Best practices

______________________________________________________________________

# What is Sensitive Data Exposure?

Sensitive Data Exposure occurs when an application unintentionally reveals confidential information to unauthorized
people.

This doesn't always happen because of hackers.

Sometimes,

developers accidentally expose sensitive information through:

- API responses
- Logs
- Error messages
- URLs
- Git repositories
- Backups

______________________________________________________________________

# What is Sensitive Data?

Examples include:

- Passwords
- Password hashes
- JWT tokens
- API keys
- Database credentials
- Credit card numbers
- Aadhaar numbers
- PAN numbers
- Email addresses
- Phone numbers
- Medical records
- Personal documents

If leaking the data would harm users or your organization,

treat it as sensitive.

______________________________________________________________________

# Typical Flow

```text id="sde1101"
Sensitive Data

↓

Application

↓

Logs / API / Database

↓

Unauthorized Access
```

The goal is to ensure

only authorized users

can access sensitive information.

______________________________________________________________________

# Real-World Example

Suppose your login API returns:

```json id="sde1102"
{
    "username": "riyaz",
    "password": "password123",
    "jwt": "eyJhbGciOi..."
}
```

This API response exposes:

- Password
- JWT

Neither should ever be returned.

______________________________________________________________________

# Common Leak 1

## Returning Too Much Data

Imagine this SQLAlchemy model.

```python id="sde1103"
class User(Base):
    id: int
    username: str
    email: str
    password_hash: str
```

Bad Example

```python id="sde1104"
@app.get("/users/{id}")
def get_user():
    return user
```

The API may serialize

every field,

including

```text id="sde1105"
password_hash
```

______________________________________________________________________

# Secure Version

Return only

the required fields.

```python id="sde1106"
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
```

```python id="sde1107"
return UserResponse(
    id=user.id,
    username=user.username,
    email=user.email,
)
```

Never expose internal fields.

______________________________________________________________________

# Common Leak 2

## Logging Secrets

Bad Example

```python id="sde1108"
logger.info(
    f"User login: {password}"
)
```

Now every password

appears in your log files.

______________________________________________________________________

# Better

```python id="sde1109"
logger.info(
    "User login attempt"
)
```

Or

```python id="sde1110"
logger.info(
    "User %s logged in",
    username,
)
```

Never log:

- Passwords
- JWTs
- API keys
- Database passwords
- Secret keys

______________________________________________________________________

# Common Leak 3

## Hardcoding Secrets

Bad Example

```python id="sde1111"
JWT_SECRET = "secret123"

DATABASE_PASSWORD = "mypassword"
```

If the repository becomes public,

the secrets are compromised.

______________________________________________________________________

# Secure Version

```python id="sde1112"
import os

JWT_SECRET = os.getenv(
    "JWT_SECRET"
)
```

Even better,

use a secret manager.

______________________________________________________________________

# Common Leak 4

## Sensitive Data in URLs

Bad Example

```text id="sde1113"
/login?password=password123
```

URLs are commonly stored in:

- Browser history
- Proxy logs
- Server logs

Sensitive information should never appear in URLs.

Use the request body instead.

______________________________________________________________________

# Common Leak 5

## Verbose Error Messages

Bad Example

```text id="sde1114"
Database password:

library123

Connection failed.
```

This reveals internal configuration.

Instead,

return

```text id="sde1115"
Internal Server Error
```

Log the detailed error internally.

______________________________________________________________________

# Common Leak 6

## Public Git Repository

Developers accidentally commit:

```text id="sde1116"
.env

config.py

credentials.json
```

Then push them to GitHub.

Even if removed later,

the secrets may already be compromised.

______________________________________________________________________

# Secure Practice

Use

```text id="sde1117"
.gitignore
```

Example

```text id="sde1118"
.env

*.pem

credentials.json
```

Never commit secrets.

______________________________________________________________________

# Data Masking

Sometimes,

users need to see

part of the information.

Example

Instead of

```text id="sde1119"
4111111111111111
```

Display

```text id="sde1120"
************1111
```

Instead of

```text id="sde1121"
9876543210
```

Display

```text id="sde1122"
******3210
```

Only reveal

what is necessary.

______________________________________________________________________

# Encryption at Rest

Some sensitive data

must be encrypted

before storage.

Examples:

- Medical records
- Financial documents
- Personal files

Even if the database is compromised,

encrypted data remains protected.

Remember:

Passwords are hashed,

not encrypted.

______________________________________________________________________

# Principle of Least Exposure

Only expose

the minimum information required.

Example

Instead of returning

the complete user record,

return only

the fields needed

for that endpoint.

______________________________________________________________________

# Defense in Depth

Protect sensitive data using multiple layers.

```text id="sde1123"
HTTPS

↓

Authentication

↓

Authorization

↓

Encryption

↓

Logging Rules

↓

Secrets Management
```

______________________________________________________________________

# Best Practices

✅ Return only required fields.

✅ Use response models.

✅ Never log secrets.

✅ Store secrets outside source code.

✅ Use HTTPS.

✅ Encrypt sensitive information when required.

✅ Hash passwords.

✅ Review API responses regularly.

______________________________________________________________________

# Common Mistakes

### Returning Database Models Directly

Always create response models.

Never expose internal database objects directly.

______________________________________________________________________

### Logging Passwords

Logs are valuable,

but they should never contain secrets.

______________________________________________________________________

### Committing Secrets

Treat Git history

as permanent.

Once a secret is committed,

assume it is compromised.

______________________________________________________________________

### Sending Sensitive Data in URLs

Use request bodies

or headers

for confidential information.

______________________________________________________________________

### Forgetting Old Backups

Old database backups

also contain sensitive data.

Protect them

just like production databases.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| -------------------------- | -------------------------------------- |
| Return full database model | Use response models |
| Log passwords | Log events only |
| Secrets in Git | Environment variables / Secret manager |
| Password in URL | Password in request body |
| Plain sensitive data | Encrypt or mask when appropriate |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Sensitive Data Exposure, and how can backend developers prevent it?

Sensitive Data Exposure occurs when confidential information is unintentionally revealed through API responses, logs,
source code, URLs, backups, or other systems. Backend developers can prevent it by returning only necessary data, using
response models, avoiding logging secrets, storing secrets securely, using HTTPS, encrypting sensitive information where
appropriate, hashing passwords, and following the Principle of Least Exposure.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Sensitive Data Exposure is
- Common sources of data leaks
- Secure API responses
- Logging best practices
- Secret management
- Data masking
- Encryption at rest
- Best practices

______________________________________________________________________

# What's Next

[Server-Side Request Forgery (SSRF)](12-server-side-request-forgery.md)
