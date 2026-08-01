# Security - Part 4

# Cross-Site Request Forgery (CSRF)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What CSRF is
- Why it happens
- When applications are vulnerable
- Why JWT-based APIs are usually different
- How to protect FastAPI applications
- Best practices
- Common mistakes

______________________________________________________________________

# What is CSRF?

Cross-Site Request Forgery (CSRF) is an attack where a malicious website tricks a user's browser into sending an
unwanted request to another website where the user is already authenticated.

The important point is:

> The attacker is **not stealing the user's credentials**.

Instead,

the attack abuses the fact that the browser automatically sends authentication information (such as cookies) with
requests.

______________________________________________________________________

# Why Does It Happen?

Imagine this situation.

```text id="csrf401"
User Logs In

↓

Browser Stores Session Cookie

↓

Visits Malicious Website

↓

Browser Automatically Sends Cookie

↓

Backend Thinks Request Is Legitimate
```

The backend sees a valid session cookie,

so it believes the request came from the real user.

______________________________________________________________________

# Real-World Example

Suppose you're logged into your banking website.

Your browser already has:

```text id="csrf402"
Session Cookie
```

Now you visit a malicious website.

Without your knowledge,

your browser sends a request to:

```text id="csrf403"
POST /transfer-money
```

Since the browser automatically includes your session cookie,

the bank thinks **you** initiated the transfer.

______________________________________________________________________

# Important Requirement

CSRF requires two things:

✅ The application authenticates users using **cookies**.

✅ The browser automatically sends those cookies.

If authentication is not automatic,

CSRF generally doesn't work.

______________________________________________________________________

# Typical Flow

```text id="csrf404"
User

↓

Bank Login

↓

Session Cookie

↓

Visits Evil Website

↓

Browser Sends Cookie

↓

Bank Accepts Request
```

Notice,

the user never intentionally visited the transfer endpoint.

______________________________________________________________________

# Are JWT APIs Vulnerable?

This depends on **how the JWT is stored**.

### Case 1

JWT stored in

```text id="csrf405"
Authorization Header
```

Example

```http id="csrf406"
Authorization: Bearer <token>
```

JavaScript must explicitly add this header.

The browser does **not** attach it automatically.

This approach is generally **not vulnerable to traditional CSRF attacks**.

______________________________________________________________________

### Case 2

JWT stored in

```text id="csrf407"
HttpOnly Cookie
```

The browser automatically sends the cookie.

Now CSRF protection is required,

just like session-based authentication.

______________________________________________________________________

# Vulnerable FastAPI Example

Suppose your application uses session cookies.

```python id="csrf408"
@app.post("/change-password")
def change_password():
    return {
        "message": "Password changed"
    }
```

If authentication depends only on a session cookie,

a malicious website may be able to trigger this endpoint through the victim's browser.

______________________________________________________________________

# Secure Solution 1

## CSRF Token

The server generates

a random,

unpredictable token.

```text id="csrf409"
Login

↓

Session Cookie

+

CSRF Token
```

Every sensitive request

must include both.

Example

```http id="csrf410"
POST /change-password

Cookie: session=...

X-CSRF-Token: random-token
```

The attacker cannot guess the CSRF token,

so the request is rejected.

______________________________________________________________________

# Why Does This Work?

A malicious website can cause the browser to send cookies,

but it **cannot** read your application's CSRF token and include it correctly in the forged request.

The server verifies that:

- Session is valid
- CSRF token matches

Both must be correct.

______________________________________________________________________

# Secure Solution 2

## SameSite Cookies

Modern browsers support

the

```text id="csrf411"
SameSite
```

cookie attribute.

Example

```http id="csrf412"
Set-Cookie:

session=abc123;

HttpOnly;

Secure;

SameSite=Lax
```

Common values:

| Value | Meaning |
| ------ | ---------------------------------------------------------------- |
| Strict | Cookie sent only from the same site |
| Lax | Allows most normal navigation while blocking many CSRF scenarios |
| None | Cookie sent in cross-site requests (must also use `Secure`) |

For many applications,

`Lax` provides a good balance.

______________________________________________________________________

# Secure Solution 3

## Verify Origin or Referer

The server can verify where the request originated.

Example

```text id="csrf413"
Request

↓

Origin Header

↓

Trusted Domain?

↓

Yes → Continue

No → Reject
```

This provides another layer of defense.

______________________________________________________________________

# Defense in Depth

Don't rely on one protection.

Use multiple layers.

```text id="csrf414"
HTTPS

↓

Secure Cookies

↓

SameSite

↓

CSRF Token

↓

Origin Validation
```

If one mechanism fails,

others still protect the application.

______________________________________________________________________

# FastAPI Considerations

Many modern FastAPI APIs use:

```text id="csrf415"
Authorization

↓

Bearer JWT
```

instead of cookie-based authentication.

In this architecture,

traditional CSRF attacks are generally not applicable,

because the browser does not automatically send the Authorization header.

However,

if your FastAPI application authenticates using cookies,

you should implement CSRF protection.

______________________________________________________________________

# Best Practices

✅ Use CSRF tokens for cookie-based authentication.

✅ Set `SameSite` on cookies.

✅ Mark cookies as `Secure`.

✅ Use `HttpOnly` where appropriate.

✅ Validate the `Origin` header for sensitive operations.

✅ Use HTTPS.

______________________________________________________________________

# Common Mistakes

### Thinking Every API Needs CSRF Tokens

If your API uses Bearer tokens in the Authorization header,

traditional CSRF protection is usually unnecessary.

Understand your authentication mechanism first.

______________________________________________________________________

### Forgetting SameSite

Many CSRF attacks become much harder

when cookies use appropriate `SameSite` settings.

______________________________________________________________________

### Disabling HTTPS

Always protect authentication cookies using HTTPS.

Without HTTPS,

cookies can be intercepted.

______________________________________________________________________

### Trusting Cookies Alone

A valid session cookie proves the user authenticated earlier.

It does **not** prove they intentionally initiated the current request.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| -------------------- | ---------------------- |
| Session cookie only | Session + CSRF token |
| No SameSite | SameSite=Lax or Strict |
| No Origin validation | Verify Origin |
| HTTP | HTTPS |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is CSRF, and how do you prevent it?

CSRF (Cross-Site Request Forgery) is an attack where a malicious website tricks a user's browser into sending
authenticated requests to another site using automatically included credentials such as cookies. The primary defenses
are CSRF tokens, `SameSite` cookies, verifying the `Origin` or `Referer` headers, using HTTPS, and storing
authentication in mechanisms that are not automatically sent by the browser, such as Bearer tokens in the Authorization
header where appropriate.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What CSRF is
- Why it happens
- Cookie-based authentication and CSRF
- JWT vs Session authentication
- CSRF tokens
- SameSite cookies
- Origin validation
- FastAPI considerations
- Best practices

______________________________________________________________________

# What's Next

[Broken Authentication](05-broken-authentication.md)
