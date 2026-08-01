# Security - Part 36

# Security Headers & Timing Attacks

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What HTTP Security Headers are
- Why they are important
- HSTS
- CSP
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- What Timing Attacks are
- Constant-time comparison
- Python examples
- Best practices

______________________________________________________________________

# What are Security Headers?

When a server responds to a browser,

it can include additional HTTP headers.

These headers instruct the browser

to behave in a more secure manner.

Example

```http id="sh3601"
HTTP/1.1 200 OK

Content-Type: application/json
```

Additional security headers may also be included.

______________________________________________________________________

# Why Are Security Headers Important?

Security headers help reduce the risk of:

- Clickjacking
- MIME type confusion
- Information leakage
- Cross-Site Scripting (partially, through CSP)
- Insecure HTTP usage

They provide an **additional layer of defense**.

______________________________________________________________________

# 1. HSTS

HSTS stands for

**HTTP Strict Transport Security**.

Example

```http id="sh3602"
Strict-Transport-Security:

max-age=31536000;
includeSubDomains
```

Meaning:

```text id="sh3603"
Always use HTTPS
```

If a user types

```text id="sh3604"
http://library.example.com
```

the browser automatically upgrades

to HTTPS.

______________________________________________________________________

# 2. Content Security Policy (CSP)

CSP controls

which resources

a browser may load.

Example

```http id="sh3605"
Content-Security-Policy:

default-src 'self'
```

Meaning

```text id="sh3606"
Only load resources

from this website.
```

CSP significantly reduces

the impact of many XSS attacks.

______________________________________________________________________

# 3. X-Frame-Options

Used to prevent

Clickjacking.

Example

```http id="sh3607"
X-Frame-Options:

DENY
```

Meaning

```text id="sh3608"
Do not allow

iframes.
```

We discussed this

in the Clickjacking lesson.

______________________________________________________________________

# 4. X-Content-Type-Options

Example

```http id="sh3609"
X-Content-Type-Options:

nosniff
```

Browsers sometimes try to

"guess"

a file's content type.

Example

```text id="sh3610"
Uploaded File

↓

Browser Guesses

↓

Wrong Type
```

`nosniff`

tells the browser

to trust

the declared content type

instead of guessing.

______________________________________________________________________

# 5. Referrer-Policy

When users click links,

browsers may send

the previous URL

to the next website.

This is called the

**Referer** header.

Example

```http id="sh3611"
Referrer-Policy:

strict-origin-when-cross-origin
```

This reduces

the amount of information

shared with external websites.

______________________________________________________________________

# 6. Permissions-Policy

Modern browsers

allow websites

to control

certain browser features.

Example

```http id="sh3612"
Permissions-Policy:

camera=(),

microphone=(),

geolocation=()
```

This prevents

your website

from accessing

features

it doesn't need.

______________________________________________________________________

# Example Secure Response

```http id="sh3613"
Strict-Transport-Security

Content-Security-Policy

X-Frame-Options

X-Content-Type-Options

Referrer-Policy

Permissions-Policy
```

Many production applications

include all of these.

______________________________________________________________________

# FastAPI Example

Security headers

can be added

using middleware.

```python id="sh3614"
@app.middleware("http")
async def security_headers(
    request,
    call_next,
):
    response = await call_next(request)

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    return response
```

Additional headers

can be added

the same way.

______________________________________________________________________

# What is a Timing Attack?

A Timing Attack

is an attack

where an attacker

measures

how long an operation takes

to infer sensitive information.

Even tiny differences

in execution time

can reveal secrets.

______________________________________________________________________

# Example

Suppose your application compares

API keys.

Bad

```python id="sh3615"
if user_key == stored_key:
    ...
```

A typical string comparison

may stop

at the first mismatch.

Example

```text id="sh3616"
ABCDEF

↓

A ✔

↓

B ✔

↓

X ❌

↓

Stop
```

If an attacker measures

response times,

they may gradually infer

the correct value.

______________________________________________________________________

# Secure Comparison

Python provides

```python id="sh3617"
import hmac

hmac.compare_digest(
    user_key,
    stored_key,
)
```

`compare_digest()`

performs a **constant-time comparison**,

making timing analysis

much more difficult.

______________________________________________________________________

# When Should You Use It?

Use constant-time comparison

for sensitive values such as:

- API keys
- HMAC signatures
- Webhook signatures
- CSRF tokens
- Authentication tokens

Ordinary string comparisons

are acceptable

for non-sensitive values.

______________________________________________________________________

# Defense in Depth

Security headers

and timing protections

work alongside

other defenses.

```text id="sh3618"
HTTPS

↓

Security Headers

↓

Authentication

↓

Authorization

↓

Constant-Time Comparison

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Enable HSTS.

✅ Configure CSP.

✅ Set X-Frame-Options.

✅ Use X-Content-Type-Options.

✅ Configure Referrer-Policy.

✅ Configure Permissions-Policy.

✅ Use `hmac.compare_digest()` for sensitive comparisons.

______________________________________________________________________

# Common Mistakes

### Forgetting Security Headers

Browsers

cannot enforce protections

that are never sent.

______________________________________________________________________

### Weak CSP

A poorly configured CSP

may provide little protection.

Review it carefully.

______________________________________________________________________

### Using Normal String Comparison

For secrets,

prefer

`hmac.compare_digest()`.

______________________________________________________________________

### Assuming Security Headers Replace Secure Coding

Security headers

complement

secure coding practices.

They do not replace

authentication,

authorization,

or input validation.

______________________________________________________________________

# Quick Comparison

| Protection | Purpose |
| ---------------------- | -------------------------- |
| HSTS | Force HTTPS |
| CSP | Restrict loaded resources |
| X-Frame-Options | Prevent Clickjacking |
| X-Content-Type-Options | Prevent MIME sniffing |
| Referrer-Policy | Reduce information leakage |
| Permissions-Policy | Restrict browser features |
| `compare_digest()` | Reduce timing attack risk |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why are HTTP Security Headers important, and what is a Timing Attack?

HTTP Security Headers instruct browsers to enforce additional protections such as HTTPS-only communication, Clickjacking
prevention, MIME type validation, and Content Security Policies. These headers reduce the attack surface for
browser-based attacks. A Timing Attack occurs when an attacker measures how long sensitive operations take to infer
secret information. Developers can reduce this risk by using constant-time comparison functions such as Python's
`hmac.compare_digest()` for comparing secrets like API keys, HMAC signatures, and tokens.

______________________________________________________________________

# Summary

In this lesson, you learned:

- HTTP Security Headers
- HSTS
- CSP
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- Timing Attacks
- Constant-time comparison
- Best practices

______________________________________________________________________

# 🎉 Security Module Complete

Congratulations! You have now completed a comprehensive security curriculum covering:

- OWASP Top 10
- Authentication & Authorization
- JWT & OAuth2
- SQL Injection, XSS, CSRF, SSRF
- IDOR & Broken Access Control
- Command Injection
- Path Traversal
- File Upload Security
- API Security
- HTTPS & TLS
- Secrets Management
- Docker Security
- Dependency Security
- Logging & Monitoring
- CORS
- Sessions
- Basic Authentication
- Session Hijacking
- Session Fixation
- Replay Attacks
- Open Redirect
- Clickjacking
- DoS & DDoS
- Security Headers
- Timing Attacks

You now have a strong foundation for Python/FastAPI backend development and technical interviews.

______________________________________________________________________

# What's Next

[Design Pattern](../patterns/1.intro.md)
