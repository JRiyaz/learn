# Security - Part 33

# Open Redirect

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What an Open Redirect is
- Why it is dangerous
- How attackers exploit it
- Vulnerable FastAPI examples
- Secure redirect techniques
- Redirect allowlists
- Best practices

______________________________________________________________________

# What is an Open Redirect?

An **Open Redirect** is a vulnerability where an application redirects users to a URL **controlled by the attacker**.

Instead of redirecting users to trusted pages,

the application trusts a URL supplied by the client.

______________________________________________________________________

# Why Is It Dangerous?

Open Redirects are commonly used for:

- Phishing attacks
- Credential theft
- Social engineering
- Bypassing user trust

The user believes they are interacting with your website,

but they are redirected to a malicious one.

______________________________________________________________________

# Real-World Scenario

Suppose your application redirects users after login.

Workflow

```text id="or3301"
User Logs In

↓

Redirect

↓

Dashboard
```

This is perfectly normal.

______________________________________________________________________

# Vulnerable Example

Suppose the application accepts a `next` parameter.

```text id="or3302"
/login?next=https://evil.com
```

After login,

the application redirects the user to:

```text id="or3303"
https://evil.com
```

The user may think

the destination is trusted

because the redirect started

from your website.

______________________________________________________________________

# Vulnerable FastAPI Example

```python id="or3304"
from fastapi.responses import RedirectResponse

@app.get("/login")
def login(next: str):
    return RedirectResponse(next)
```

The application

blindly trusts

user input.

______________________________________________________________________

# Why Is This Dangerous?

Suppose the attacker sends

this link:

```text id="or3305"
https://library.example.com/login?next=https://evil.com
```

The victim sees:

```text id="or3306"
library.example.com
```

and trusts it.

After logging in,

they are silently redirected

to the attacker's website.

This technique is frequently used

in phishing campaigns.

______________________________________________________________________

# The Root Problem

The application allows

the client

to choose

the redirect destination.

Instead,

the server

should decide

where redirects are allowed.

______________________________________________________________________

# Secure Solution 1

## Use Relative Paths

Instead of accepting

full URLs,

accept only

internal paths.

Example

Allowed

```text id="or3307"
/dashboard

/profile

/orders
```

Rejected

```text id="or3308"
https://evil.com

http://attacker.com
```

This ensures

users stay

within your application.

______________________________________________________________________

# Secure Solution 2

## Allowlist Destinations

If external redirects

are necessary,

maintain

an allowlist.

Example

```python id="or3309"
ALLOWED_URLS = {
    "https://partner.example.com",
    "https://payments.example.com",
}
```

Only redirect

to approved destinations.

Everything else

is rejected.

______________________________________________________________________

# Secure Solution 3

## Validate Redirect URLs

Before redirecting,

verify:

- Protocol
- Domain
- Port

Example

```text id="or3310"
https://library.example.com

↓

Allowed
```

```text id="or3311"
https://evil.com

↓

Rejected
```

______________________________________________________________________

# Better FastAPI Design

Instead of

```python id="or3312"
return RedirectResponse(next)
```

Use

```python id="or3313"
return RedirectResponse("/dashboard")
```

The application

chooses the destination,

not the client.

______________________________________________________________________

# OAuth Example

Open Redirects

are especially dangerous

in OAuth flows.

Example

```text id="or3314"
OAuth Login

↓

Redirect URI

↓

Validate

↓

Continue
```

OAuth providers

strictly validate

redirect URIs

to prevent token theft.

______________________________________________________________________

# User Experience

A common pattern is:

```text id="or3315"
User Requests

/orders

↓

Not Logged In

↓

Login

↓

Return to /orders
```

This is safe

when the application

stores

the original path

internally

instead of trusting

an arbitrary URL

from the user.

______________________________________________________________________

# Defense in Depth

Protect redirects using:

```text id="or3316"
Authentication

↓

Validation

↓

Allowlist

↓

Relative Paths

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Prefer relative paths.

✅ Use allowlists for external URLs.

✅ Validate redirect destinations.

✅ Avoid redirecting to arbitrary user-supplied URLs.

✅ Log unexpected redirect attempts.

______________________________________________________________________

# Common Mistakes

### Trusting the `next` Parameter

Never assume

the client provides

a safe destination.

______________________________________________________________________

### Allowing Any URL

Applications should control

where users

can be redirected.

______________________________________________________________________

### Skipping Validation

If external redirects

are unavoidable,

validate them carefully.

______________________________________________________________________

### Forgetting OAuth Redirect Validation

OAuth redirect URIs

must be registered

and validated.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| -------------------- | -------------------------- |
| Redirect to user URL | Redirect to internal path |
| No validation | Validate destination |
| Any external URL | Allowlisted URLs |
| Blind redirect | Server-controlled redirect |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is an Open Redirect vulnerability, and how can developers prevent it?

An Open Redirect vulnerability occurs when an application redirects users to a destination controlled by user input
without proper validation. Attackers can exploit this to create convincing phishing attacks or misuse trusted domains.
Developers can prevent Open Redirects by using server-controlled redirects, accepting only relative internal paths,
validating redirect destinations, and maintaining an allowlist for any external URLs that are genuinely required.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What an Open Redirect is
- Why it is dangerous
- Vulnerable FastAPI code
- Relative paths
- Allowlists
- Redirect validation
- OAuth considerations
- Best practices

______________________________________________________________________

# What's Next

[Clickjacking](34-clickjacking.md)
