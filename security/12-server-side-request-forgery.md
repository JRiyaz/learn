# Security - Part 12

# Server-Side Request Forgery (SSRF)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What SSRF is
- Why SSRF is dangerous
- How SSRF happens
- Vulnerable FastAPI code
- Secure implementations
- URL validation
- Allowlisting
- Best practices

______________________________________________________________________

# What is SSRF?

SSRF stands for

**Server-Side Request Forgery**.

It occurs when an attacker tricks your **backend server** into making HTTP requests to locations it was never intended
to access.

The important point is:

> The attacker is **not** making the request directly.

Instead,

they make **your server** send the request.

______________________________________________________________________

# Why Is This Dangerous?

Imagine your FastAPI application can access:

- Internal APIs
- Redis
- PostgreSQL
- Kubernetes API
- Cloud metadata service

Normally,

users on the Internet **cannot** reach these services.

But your backend can.

If an attacker can control where your backend sends requests,

they may access resources that should never be exposed.

______________________________________________________________________

# Typical Flow

```text id="ssrf1201"
Attacker

↓

Backend API

↓

Internal Server

↓

Sensitive Data
```

Instead of attacking the internal server directly,

the attacker abuses your backend as a proxy.

______________________________________________________________________

# Real-World Example

Suppose your application fetches profile pictures from a URL.

Workflow

```text id="ssrf1202"
User

↓

Image URL

↓

Backend Downloads Image

↓

Returns Image
```

This seems harmless.

But what if the supplied URL points to an internal service instead of a public image?

The backend may unintentionally expose internal resources.

______________________________________________________________________

# Vulnerable FastAPI Example

```python id="ssrf1203"
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/fetch")
def fetch(url: str):

    response = requests.get(url)

    return {
        "content": response.text
    }
```

______________________________________________________________________

# Why Is This Vulnerable?

The application accepts

**any URL**

from the client.

Workflow

```text id="ssrf1204"
User Input

↓

requests.get()

↓

Backend Makes Request
```

There is no validation.

The backend trusts the client completely.

______________________________________________________________________

# The Root Problem

The issue isn't

`requests.get()`.

The issue is

allowing users

to decide

where your server connects.

Whenever user input controls outbound requests,

SSRF should be considered.

______________________________________________________________________

# Common SSRF Targets

Attackers often try to reach:

```text id="ssrf1205"
Internal APIs

↓

localhost

↓

Redis

↓

Database Admin Panels

↓

Cloud Metadata Services
```

These systems are usually inaccessible from the public Internet,

making SSRF especially dangerous.

______________________________________________________________________

# Secure Solution 1

## Allowlist URLs

Instead of allowing every URL,

allow only trusted domains.

Example

```python id="ssrf1206"
ALLOWED_DOMAINS = {
    "images.example.com",
    "cdn.example.com",
}
```

If the domain isn't trusted,

reject the request.

This is the strongest defense.

______________________________________________________________________

# Secure Solution 2

## Validate the URL

Parse the URL

before making the request.

Example

```python id="ssrf1207"
from urllib.parse import urlparse

parsed = urlparse(url)

if parsed.scheme != "https":
    raise HTTPException(
        status_code=400,
        detail="Only HTTPS URLs are allowed",
    )
```

Basic validation should include:

- Scheme
- Host
- Port
- Format

Validation alone is **not sufficient**,

but it is an important first step.

______________________________________________________________________

# Secure Solution 3

## Block Internal Addresses

Reject requests targeting:

- localhost
- 127.0.0.1
- Private IP ranges
- Loopback addresses

Example

```text id="ssrf1208"
Private Network?

↓

Yes

↓

Reject
```

Your backend should never fetch arbitrary internal resources on behalf of users.

______________________________________________________________________

# Secure Solution 4

## Use Timeouts

Never allow outbound requests

to run indefinitely.

Example

```python id="ssrf1209"
response = requests.get(
    url,
    timeout=5,
)
```

Timeouts reduce the impact of slow or malicious endpoints.

______________________________________________________________________

# Secure Solution 5

## Restrict Redirects

Suppose

a trusted URL

redirects

to an internal address.

Your backend should detect

and reject such redirects.

Always review how your HTTP client handles redirects.

______________________________________________________________________

# FastAPI Example

A safer design

avoids user-supplied URLs entirely.

Instead of:

```text id="ssrf1210"
User Supplies URL
```

Prefer

```text id="ssrf1211"
User Supplies Image ID

↓

Backend Looks Up URL

↓

Trusted URL

↓

Download
```

Now,

users cannot control

the destination.

______________________________________________________________________

# Cloud Metadata Services

Many cloud providers expose metadata endpoints

that are only accessible from inside virtual machines.

These endpoints may contain:

- Temporary credentials
- Instance information
- Configuration

This is why SSRF has been involved

in several real-world cloud security incidents.

As a backend developer,

the important lesson is:

Never let users control internal network requests.

______________________________________________________________________

# Defense in Depth

Combine multiple protections.

```text id="ssrf1212"
Allowlist

↓

URL Validation

↓

HTTPS Only

↓

Private IP Blocking

↓

Timeouts

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Use allowlists instead of blocklists.

✅ Validate URLs.

✅ Restrict outbound destinations.

✅ Block internal IP ranges.

✅ Use HTTPS.

✅ Configure request timeouts.

✅ Log unexpected outbound requests.

______________________________________________________________________

# Common Mistakes

### Accepting Arbitrary URLs

Never let clients choose

where your backend connects

without validation.

______________________________________________________________________

### Depending Only on Regex

Checking that a string "looks like a URL"

doesn't make it safe.

Proper validation

and destination control

are still required.

______________________________________________________________________

### Forgetting Redirects

A trusted URL

can redirect

to an untrusted destination.

Review redirect behavior carefully.

______________________________________________________________________

### Ignoring Internal Networks

Private addresses

should generally never be reachable

through user-controlled requests.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| -------------------------- | ---------------------------- |
| Any URL accepted | Allowlisted domains |
| No validation | Validate scheme, host, port |
| Unlimited requests | Timeouts |
| Internal addresses allowed | Block private IPs |
| User controls destination | Backend controls destination |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Server-Side Request Forgery (SSRF), and how can it be prevented?

Server-Side Request Forgery (SSRF) occurs when an attacker tricks a backend server into making requests to unintended
destinations, often internal services that are inaccessible from the public Internet. Developers can prevent SSRF by
validating URLs, using allowlists for trusted domains, blocking requests to private or loopback addresses, enforcing
HTTPS, limiting redirects, using request timeouts, and avoiding designs where users directly control outbound request
destinations.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What SSRF is
- Why it is dangerous
- Vulnerable FastAPI code
- Allowlisting
- URL validation
- Blocking internal networks
- Request timeouts
- Defense in depth
- Best practices

______________________________________________________________________

# What's Next

[XML External Entity (XXE) - Overview](13-xml-external-entity.md)
