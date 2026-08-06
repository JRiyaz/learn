# Authentication

> **Course:** Flask for Backend Engineers
>
> **Module:** 5
>
> **File:** `12_authentication.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Authentication is
- Authentication vs Authorization
- Authentication Flow
- Username & Password Authentication
- Password Hashing
- Flask-Login
- Session Authentication
- Token Authentication
- JWT Authentication
- Refresh Tokens
- Password Reset
- Multi-Factor Authentication (MFA)
- Security Best Practices

______________________________________________________________________

# What is Authentication?

Authentication answers one question:

> **Who are you?**

When a user logs in,

the application verifies their identity.

Example

```
User

↓

Username

Password

↓

Database

↓

Identity Verified
```

______________________________________________________________________

# Authentication vs Authorization

Many developers confuse these concepts.

Authentication

```
Who are you?
```

Authorization

```
What are you allowed to do?
```

Example

```
Login

↓

Authentication

↓

Admin Permission

↓

Authorization
```

Authentication always happens first.

______________________________________________________________________

# Real World Analogy

Entering an office building.

Step 1

```
Show Employee ID

↓

Identity Verified
```

(Authentication)

Step 2

```
Allowed Into Server Room?
```

(Authorization)

______________________________________________________________________

# Authentication Flow

```
User

↓

Login Form

↓

Flask

↓

Database

↓

Password Verification

↓

Create Session/JWT

↓

Response
```

______________________________________________________________________

# Registration Flow

```
User

↓

Registration Form

↓

Validation

↓

Hash Password

↓

Store User

↓

Database
```

Passwords are **never stored in plain text**.

______________________________________________________________________

# Password Hashing

Never store

```text
password123
```

Instead

```
password123

↓

Hash Function

↓

$2b$12$...
```

Even if the database is compromised,

the original password is not directly exposed.

______________________________________________________________________

# Why Hash Passwords?

Imagine a database leak.

Bad

```
username

password123
```

Good

```
username

$2b$12$hM...
```

Attackers cannot simply read users' passwords.

______________________________________________________________________

# Hashing vs Encryption

Hashing

```
One-Way
```

Encryption

```
Two-Way
```

Passwords should be **hashed**, not encrypted.

______________________________________________________________________

# Werkzeug Password Utilities

Flask commonly uses Werkzeug.

Generate hash

```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash(
    "password123"
)
```

______________________________________________________________________

# Verify Password

```python
from werkzeug.security import check_password_hash

check_password_hash(
    password_hash,
    "password123"
)
```

Returns

```
True

or

False
```

______________________________________________________________________

# Login Flow

```
User

↓

Enter Password

↓

Retrieve Password Hash

↓

check_password_hash()

↓

Success

↓

Create Session
```

______________________________________________________________________

# Session Authentication

Traditional Flask applications often use sessions.

```
User Logs In

↓

Session Created

↓

Cookie

↓

Browser

↓

Future Requests
```

The browser automatically sends the session cookie.

______________________________________________________________________

# Flask Session

Store user ID

```python
from flask import session

session["user_id"] = user.id
```

Read

```python
session.get("user_id")
```

Logout

```python
session.clear()
```

______________________________________________________________________

# Flask-Login

Install

```bash
pip install flask-login
```

Provides

- Login management
- User session handling
- Login required decorators
- Current user access

______________________________________________________________________

# Initialize

```python
from flask_login import LoginManager

login_manager = LoginManager()

login_manager.init_app(app)
```

______________________________________________________________________

# User Model

A Flask-Login user typically inherits `UserMixin`.

```python
from flask_login import UserMixin

class User(
    UserMixin,
    db.Model
):
    ...
```

`UserMixin` provides commonly required authentication methods.

______________________________________________________________________

# Login User

```python
from flask_login import login_user

login_user(user)
```

Creates an authenticated session.

______________________________________________________________________

# Current User

```python
from flask_login import current_user

current_user.id
```

Available during authenticated requests.

______________________________________________________________________

# Protect Routes

```python
from flask_login import login_required

@app.route("/dashboard")

@login_required

def dashboard():

    ...
```

Unauthenticated users are redirected to the login page by default.

______________________________________________________________________

# Logout

```python
from flask_login import logout_user

logout_user()
```

Session ends.

______________________________________________________________________

# Token Authentication

Instead of sessions,

REST APIs often use tokens.

```
User

↓

Login

↓

JWT

↓

Client Stores Token

↓

Future Requests
```

______________________________________________________________________

# JWT

JWT

\=

JSON Web Token

Example

```
Header

.

Payload

.

Signature
```

JWTs are digitally signed to detect tampering.

______________________________________________________________________

# Login Response

```json
{
    "access_token": "..."
}
```

Client stores the token.

______________________________________________________________________

# Sending JWT

HTTP Header

```
Authorization

Bearer TOKEN
```

Every protected request includes this header.

______________________________________________________________________

# JWT Verification

```
Incoming Request

↓

Extract Token

↓

Verify Signature

↓

Read Claims

↓

Authenticated
```

If verification fails,

the request is rejected.

______________________________________________________________________

# Access Token vs Refresh Token

Access Token

- Short-lived
- Used for API requests

Refresh Token

- Longer-lived
- Used to obtain a new access token

Common flow

```
Login

↓

Access Token

↓

Expires

↓

Refresh Token

↓

New Access Token
```

______________________________________________________________________

# Password Reset

Typical flow

```
Forgot Password

↓

Generate Secure Token

↓

Email Link

↓

User Clicks Link

↓

Set New Password
```

Never email passwords.

______________________________________________________________________

# Multi-Factor Authentication (MFA)

Authentication

```
Password

+

One-Time Code
```

Second factors may include:

- Authenticator Apps
- Security Keys
- SMS (less preferred)

MFA significantly improves account security.

______________________________________________________________________

# Session vs JWT

| Sessions | JWT |
|-----------|-----|
| Browser apps | APIs |
| Server stores session state | Token carries claims |
| Cookie-based | Authorization header |
| Easy logout | Requires token lifecycle management |

Choose based on application requirements.

______________________________________________________________________

# Authentication Architecture

```
Client

↓

Login

↓

Database

↓

Verify Password

↓

Create Session / JWT

↓

Authenticated Requests
```

______________________________________________________________________

# Common Mistakes

❌ Storing plaintext passwords

❌ Comparing passwords directly

❌ Using weak password policies

❌ Long-lived access tokens

❌ Returning sensitive authentication errors

❌ Storing secrets in source code

______________________________________________________________________

# Production Best Practices

- Hash passwords using a strong password hashing algorithm.
- Enforce password complexity requirements.
- Use HTTPS for all authentication traffic.
- Use secure, HTTP-only cookies for session-based authentication.
- Keep access tokens short-lived.
- Protect refresh tokens.
- Support MFA where appropriate.
- Log authentication events.
- Rate-limit login attempts.

______________________________________________________________________

# Interview Deep Dive

### Question

**Why should passwords be hashed instead of encrypted?**

### Answer

Passwords should be hashed because authentication only requires verifying whether the submitted password matches the
stored value.

Hashing is a one-way operation.

During login:

1. The user submits a password.
1. The application hashes the submitted password.
1. The hash is compared with the stored password hash.

Encryption is reversible, which makes it unnecessary and less appropriate for password storage.

Using strong password hashing algorithms significantly reduces the impact of database breaches.

______________________________________________________________________

# Summary

In this chapter you learned:

- Authentication
- Authentication vs Authorization
- Password Hashing
- Flask-Login
- Sessions
- JWT
- Access Tokens
- Refresh Tokens
- Password Reset
- MFA
- Security Best Practices

Authentication is the foundation of application security and should always be implemented using secure password hashing,
encrypted transport (HTTPS), and well-designed token or session management.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is authentication?
1. What is the difference between authentication and authorization?
1. Why should passwords never be stored in plaintext?

______________________________________________________________________

## Passwords

4. What is password hashing?
1. How is hashing different from encryption?
1. Which Werkzeug functions are commonly used for password hashing and verification?

______________________________________________________________________

## Sessions

7. How does session-based authentication work?
1. What does Flask-Login provide?
1. What does `login_required` do?
1. What is `current_user`?

______________________________________________________________________

## JWT

11. What is a JWT?
01. How is a JWT typically sent with an API request?
01. What is the difference between an access token and a refresh token?

______________________________________________________________________

## Security

14. Why should HTTPS always be used for authentication?
01. Why should login attempts be rate-limited?
01. Why is MFA recommended?

______________________________________________________________________

## Scenario-Based

17. Your application stores passwords as plaintext in the database. What risks does this introduce, and how would you fix the design?
01. A REST API currently uses server-side sessions, but mobile applications also need to authenticate. Would JWT-based authentication be more appropriate? Why?
01. A user steals another user's JWT access token. What measures can reduce the impact of this compromise?
01. Your login endpoint reveals whether a username exists by returning different error messages for "user not found" and "incorrect password." Why can this be a security issue?
01. Your product manager requests a "forgot password" feature that emails the user's current password. Why is this impossible in a properly designed authentication system, and what should be implemented instead?

______________________________________________________________________

# Next

[Authorization](13_authorization.md)
