# Security - Part 5

# Broken Authentication

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Broken Authentication is
- Why it happens
- Common authentication mistakes
- How attackers abuse weak authentication
- Secure authentication practices
- Password hashing with Python
- Secure FastAPI authentication patterns
- Best practices

______________________________________________________________________

# What is Broken Authentication?

Broken Authentication occurs when an application incorrectly verifies a user's identity or improperly manages
authentication credentials.

This can allow attackers to:

- Log in as another user
- Guess passwords
- Reuse stolen credentials
- Hijack user sessions
- Bypass authentication completely

______________________________________________________________________

# Authentication vs Authorization

Before we continue,

remember:

Authentication answers

```text id="auth501"
Who are you?
```

Authorization answers

```text id="auth502"
What can you do?
```

Broken Authentication happens **before** authorization.

If authentication fails,

everything else becomes meaningless.

______________________________________________________________________

# Typical Login Flow

```text id="auth503"
User

↓

Username

↓

Password

↓

Verify Password

↓

Generate Session/JWT

↓

Access Granted
```

Every step must be secure.

______________________________________________________________________

# Common Authentication Mistakes

The most common mistakes are:

- Plain-text passwords
- Weak password hashing
- Weak password policies
- Predictable session IDs
- Long-lived tokens
- No account lockout
- No MFA (where appropriate)
- Exposed authentication errors

We'll discuss each.

______________________________________________________________________

# Mistake 1

## Plain-Text Passwords

Suppose the database stores

```text id="auth504"
username

password

riyaz

password123
```

If the database is leaked,

every password is exposed.

Never store passwords like this.

______________________________________________________________________

# Secure Password Storage

Instead,

store a password hash.

```text id="auth505"
username

password_hash

riyaz

$2b$12$...
```

Even if the database is compromised,

the original password isn't directly revealed.

______________________________________________________________________

# Password Hashing with bcrypt

Example

```python id="auth506"
import bcrypt

password = b"password123"

hashed = bcrypt.hashpw(
    password,
    bcrypt.gensalt()
)
```

Verification

```python id="auth507"
bcrypt.checkpw(
    password,
    hashed
)
```

Notice:

You never compare plain-text passwords.

You compare

the password

against

the stored hash.

______________________________________________________________________

# Why Not SHA256?

Many beginners try:

```python id="auth508"
import hashlib

hashlib.sha256(
    password.encode()
)
```

This is **not recommended** for password storage.

SHA256 is designed to be fast.

Password hashing algorithms such as:

- bcrypt
- Argon2
- scrypt

are intentionally slow,

making brute-force attacks much more difficult.

______________________________________________________________________

# Mistake 2

## Weak Password Policy

Example

```text id="auth509"
123456

password

admin

qwerty
```

These passwords are easily guessed.

A secure application should encourage strong,

unique passwords.

______________________________________________________________________

# Mistake 3

## Unlimited Login Attempts

Suppose an attacker repeatedly guesses passwords.

```text id="auth510"
Login

↓

Wrong

↓

Wrong

↓

Wrong

↓

Wrong

↓

...
```

Without limits,

attackers can continue indefinitely.

______________________________________________________________________

# Secure Solution

Implement:

- Rate limiting
- Temporary account lockout
- Increasing delays after repeated failures
- Monitoring suspicious activity

We'll implement Redis-based rate limiting later in this course.

______________________________________________________________________

# Mistake 4

## Detailed Error Messages

Bad Example

```text id="auth511"
Username does not exist.
```

Another example

```text id="auth512"
Incorrect password.
```

These reveal unnecessary information.

An attacker can discover which usernames exist.

______________________________________________________________________

# Better Response

Always return something like:

```text id="auth513"
Invalid username or password.
```

This gives attackers less information.

______________________________________________________________________

# Mistake 5

## Long-Lived Tokens

Suppose your JWT never expires.

```text id="auth514"
Login

↓

Token

↓

Valid Forever
```

If stolen,

the attacker can continue using it indefinitely.

Always use token expiration.

We'll cover JWT security in detail later.

______________________________________________________________________

# Mistake 6

## Weak Session Management

For cookie-based authentication,

sessions should:

- Be random
- Be unpredictable
- Expire
- Be invalidated on logout

Predictable session identifiers are a serious security risk.

______________________________________________________________________

# FastAPI Login Example

Suppose your login endpoint receives

```python id="auth515"
class LoginRequest(BaseModel):
    username: str
    password: str
```

The typical workflow is

```text id="auth516"
Receive Credentials

↓

Find User

↓

Verify Password Hash

↓

Generate JWT

↓

Return Token
```

Never compare

plain-text passwords.

______________________________________________________________________

# Defense in Depth

Secure authentication isn't one feature.

It's several layers.

```text id="auth517"
HTTPS

↓

Password Hashing

↓

Rate Limiting

↓

JWT Expiration

↓

Logging

↓

Monitoring
```

______________________________________________________________________

# Best Practices

✅ Hash passwords using bcrypt or Argon2.

✅ Use HTTPS.

✅ Implement rate limiting.

✅ Use generic authentication error messages.

✅ Expire tokens.

✅ Store secrets securely.

✅ Log suspicious login attempts.

✅ Require strong passwords.

______________________________________________________________________

# Common Mistakes

### Storing Plain-Text Passwords

Never store passwords directly.

Always hash them.

______________________________________________________________________

### Writing Your Own Password Hashing Algorithm

Use proven libraries.

Never invent your own authentication algorithm.

______________________________________________________________________

### Unlimited Login Attempts

Protect login endpoints against brute-force attacks.

______________________________________________________________________

### Exposing Usernames

Avoid authentication messages that reveal whether an account exists.

______________________________________________________________________

### Long-Lived Sessions

Authentication credentials should eventually expire.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------------ | --------------------------- |
| Plain-text passwords | bcrypt / Argon2 |
| SHA256 for passwords | Password hashing algorithms |
| Unlimited login attempts | Rate limiting |
| Detailed login errors | Generic errors |
| Permanent tokens | Expiring tokens |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Broken Authentication, and how do you prevent it?

Broken Authentication occurs when an application improperly verifies user identities or manages authentication
credentials, allowing attackers to impersonate users or gain unauthorized access. Common defenses include hashing
passwords with algorithms such as bcrypt or Argon2, enforcing strong password policies, implementing rate limiting,
using HTTPS, expiring authentication tokens, protecting session identifiers, and avoiding overly detailed authentication
error messages.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Broken Authentication is
- Common authentication mistakes
- Password hashing
- Why bcrypt is preferred over SHA256 for passwords
- Rate limiting login attempts
- Secure authentication messages
- Session management
- Best practices

______________________________________________________________________

# What's Next

[Broken Access Control](06-broken-access-control.md)
