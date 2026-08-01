# Security - Part 34

# Clickjacking

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Clickjacking is
- How Clickjacking attacks work
- Why browsers are vulnerable
- Invisible iframes
- X-Frame-Options
- Content-Security-Policy (`frame-ancestors`)
- FastAPI configuration
- Best practices

______________________________________________________________________

# What is Clickjacking?

Clickjacking is an attack where a user is tricked into clicking something **different from what they believe they are
clicking**.

The attacker places your website inside an **invisible or transparent iframe** and overlays it with misleading content.

The user thinks they are clicking one thing,

but actually clicks a button on your website.

______________________________________________________________________

# Why Is It Dangerous?

Imagine a banking website.

There is a button:

```text id="cj3401"
Transfer ₹10,000
```

The attacker creates another webpage.

The bank's page is loaded inside an invisible iframe.

The attacker places a fake button over it.

```text id="cj3402"
🎁 Click Here to Win a Prize
```

The user clicks the visible button,

but the actual click reaches

the hidden banking page.

______________________________________________________________________

# Attack Flow

```text id="cj3403"
Victim Visits

↓

Attacker Website

↓

Hidden iframe

↓

Victim Clicks

↓

Real Button Clicked
```

The user unknowingly performs

an action

on the legitimate website.

______________________________________________________________________

# Why Does This Work?

Browsers normally allow

one website

to embed another website

inside an iframe.

Example

```html id="cj3404"
<iframe
    src="https://bank.example.com">
</iframe>
```

If the legitimate website

doesn't restrict framing,

the attacker can embed it.

______________________________________________________________________

# Real-World Targets

Clickjacking is especially dangerous for pages containing:

- Money transfers
- Delete account
- Change password
- Enable MFA
- Approve payment
- Administrative actions

Any action requiring a single click

is a potential target.

______________________________________________________________________

# Defense 1

## X-Frame-Options

The simplest defense

is the

```text id="cj3405"
X-Frame-Options
```

header.

Example

```http id="cj3406"
X-Frame-Options: DENY
```

Meaning:

```text id="cj3407"
Never allow

this page

inside an iframe.
```

______________________________________________________________________

# SAMEORIGIN

Another option is

```http id="cj3408"
X-Frame-Options: SAMEORIGIN
```

Meaning:

Only pages

from the same origin

may embed this page.

This is useful

when your own application

uses iframes internally.

______________________________________________________________________

# Defense 2

## Content-Security-Policy

Modern applications

prefer

```text id="cj3409"
Content-Security-Policy
```

Specifically,

the

```text id="cj3410"
frame-ancestors
```

directive.

Example

```http id="cj3411"
Content-Security-Policy:

frame-ancestors 'self'
```

Meaning:

Only your own website

may embed this page.

______________________________________________________________________

# Why CSP Is Preferred

Compared to

`X-Frame-Options`,

CSP offers:

- More flexibility
- Better browser support for modern policies
- Multiple allowed origins
- Fine-grained control

Many production systems

use CSP

as their primary mechanism.

______________________________________________________________________

# FastAPI Example

You can add security headers

using middleware.

Example

```python id="cj3412"
@app.middleware("http")
async def security_headers(
    request,
    call_next,
):
    response = await call_next(request)

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    return response
```

You can also add

Content-Security-Policy

in the same middleware.

______________________________________________________________________

# Can HTTPS Prevent Clickjacking?

No.

HTTPS encrypts communication.

It does **not** prevent

another website

from embedding your pages.

Clickjacking requires

security headers,

not encryption.

______________________________________________________________________

# Can Authentication Prevent Clickjacking?

Not always.

Suppose

the user

is already logged in.

Their browser automatically sends:

- Session cookies
- JWT cookies (if applicable)

The hidden iframe

uses the authenticated session.

Therefore,

authentication alone

doesn't stop Clickjacking.

______________________________________________________________________

# Defense in Depth

Protect web applications using:

```text id="cj3413"
HTTPS

↓

Authentication

↓

CSRF Protection

↓

X-Frame-Options

↓

Content-Security-Policy

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Set `X-Frame-Options: DENY` unless framing is required.

✅ Use `Content-Security-Policy: frame-ancestors`.

✅ Protect sensitive actions with CSRF defenses when using cookies.

✅ Require re-authentication for highly sensitive actions (e.g., changing passwords or deleting accounts).

✅ Log unusual administrative actions.

______________________________________________________________________

# Common Mistakes

### Not Sending Security Headers

Without

`X-Frame-Options`

or

`frame-ancestors`,

your pages may be embedded by other websites.

______________________________________________________________________

### Assuming HTTPS Prevents Clickjacking

HTTPS protects

communication,

not browser embedding.

______________________________________________________________________

### Ignoring Administrative Pages

Administrative pages

are common Clickjacking targets.

Protect them carefully.

______________________________________________________________________

### Using Only One Security Layer

Clickjacking defenses

should complement

authentication,

authorization,

and CSRF protection.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------------------------ | -------------------------------------- |
| Page can be embedded anywhere | `X-Frame-Options: DENY` |
| No CSP | `frame-ancestors` configured |
| Sensitive actions without protection | Re-authentication for critical actions |
| HTTPS only | HTTPS + Security Headers |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Clickjacking, and how can developers prevent it?

Clickjacking is an attack where a user is tricked into clicking hidden elements on a legitimate website embedded within
an invisible or transparent iframe. Developers can prevent Clickjacking by sending the `X-Frame-Options` header (such as
`DENY` or `SAMEORIGIN`) or the modern `Content-Security-Policy` header with the `frame-ancestors` directive. These
headers control which websites, if any, are allowed to embed the application. HTTPS alone does not prevent Clickjacking.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Clickjacking is
- How it works
- Invisible iframes
- `X-Frame-Options`
- `Content-Security-Policy`
- FastAPI security headers
- Best practices

______________________________________________________________________

# What's Next

[DoS & DDoS Attacks](35-dos-and-ddos.md)
