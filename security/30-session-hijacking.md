# Security - Part 30

# Session Hijacking

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Session Hijacking is
- How attackers steal sessions
- Common attack methods
- Cookie security
- HttpOnly
- Secure
- SameSite
- Session expiration
- Best practices

______________________________________________________________________

# What is Session Hijacking?

Session Hijacking occurs when an attacker steals a valid **Session ID** and uses it to impersonate the authenticated
user.

Remember:

The Session ID represents the user's identity.

If an attacker gets it,

they don't need the username or password.

______________________________________________________________________

# Typical Flow

```text id="sh3001"
User Logs In

↓

Session Created

↓

Session Cookie

↓

Attacker Steals Cookie

↓

Attacker Uses Session

↓

Authenticated
```

______________________________________________________________________

# Why Is It Dangerous?

Suppose the user logs into:

```text id="sh3002"
https://bank.example.com
```

The server creates

```text id="sh3003"
session_id=abc123
```

If an attacker obtains

```text id="sh3004"
abc123
```

the server cannot distinguish

between the real user

and the attacker.

______________________________________________________________________

# Common Ways Sessions Are Stolen

Attackers may obtain session cookies through:

- Cross-Site Scripting (XSS)
- Unencrypted HTTP traffic
- Malware
- Browser extensions
- Stolen devices
- Shared computers
- Session fixation (covered next)

______________________________________________________________________

# Attack Scenario

```text id="sh3005"
User

↓

Logs In

↓

Session Cookie

↓

Attacker Gets Cookie

↓

Attacker Sends Cookie

↓

Server Accepts Session
```

Notice:

The attacker never needs

the user's password.

______________________________________________________________________

# Defense 1

## HTTPS

Never send session cookies

over plain HTTP.

Bad

```text id="sh3006"
Cookie

↓

HTTP

↓

Visible
```

Good

```text id="sh3007"
Cookie

↓

HTTPS

↓

Encrypted
```

HTTPS prevents attackers

from easily intercepting cookies

while they are in transit.

______________________________________________________________________

# Defense 2

## HttpOnly Cookie

Example

```http id="sh3008"
Set-Cookie:

session_id=abc123;

HttpOnly
```

What does `HttpOnly` do?

It prevents JavaScript

from reading the cookie.

Without `HttpOnly`

an XSS attack might execute

```javascript id="sh3009"
document.cookie
```

and steal the session.

With `HttpOnly`,

JavaScript cannot access the cookie.

______________________________________________________________________

# Defense 3

## Secure Cookie

Example

```http id="sh3010"
Set-Cookie:

session_id=abc123;

Secure
```

The browser sends the cookie

only over HTTPS.

If the user accidentally visits

an HTTP version of the site,

the cookie is **not** transmitted.

______________________________________________________________________

# Defense 4

## SameSite Cookie

Example

```http id="sh3011"
Set-Cookie:

SameSite=Lax
```

Options:

| Value | Meaning |
| ------ | ------------------------------------------------------ |
| Strict | Sent only for same-site requests |
| Lax | Allows most normal navigation while reducing CSRF risk |
| None | Sent in cross-site requests (requires `Secure`) |

This helps reduce the risk of CSRF attacks.

______________________________________________________________________

# Secure Cookie Configuration

A production session cookie

typically includes

```http id="sh3012"
Set-Cookie:

session_id=...

HttpOnly

Secure

SameSite=Lax
```

This is a common secure configuration

for web applications.

______________________________________________________________________

# Defense 5

## Session Expiration

Sessions should not live forever.

Example

```text id="sh3013"
Login

↓

30 Minutes

↓

Expire Session
```

Shorter session lifetimes

reduce the usefulness

of stolen cookies.

______________________________________________________________________

# Defense 6

## Logout

When a user logs out,

delete the session.

```text id="sh3014"
Logout

↓

Delete Session

↓

Session Invalid
```

Even if someone later finds

the old Session ID,

it no longer works.

______________________________________________________________________

# Defense 7

## Regenerate Session ID

After login,

generate

a new Session ID.

```text id="sh3015"
Anonymous Session

↓

Login

↓

New Session ID
```

This helps prevent

Session Fixation,

which we'll discuss

in the next lesson.

______________________________________________________________________

# Suspicious Session Detection

Some applications monitor:

- Unusual locations
- New devices
- Impossible travel
- Sudden IP changes

If suspicious behavior is detected,

the application may:

- Require login again
- Ask for MFA
- Terminate the session

These checks improve security

but should be designed carefully because IP addresses and devices can legitimately change.

______________________________________________________________________

# Session Storage

Never store

session data

inside the browser.

The browser should only receive

the Session ID.

The actual session belongs

on the server.

______________________________________________________________________

# Defense in Depth

Secure session authentication uses:

```text id="sh3016"
HTTPS

↓

HttpOnly

↓

Secure Cookie

↓

SameSite

↓

Session Expiration

↓

Logging

↓

Monitoring
```

______________________________________________________________________

# Best Practices

✅ Use HTTPS.

✅ Set `HttpOnly`.

✅ Set `Secure`.

✅ Configure `SameSite`.

✅ Expire sessions.

✅ Delete sessions during logout.

✅ Regenerate Session IDs after login.

______________________________________________________________________

# Common Mistakes

### Storing Session Data in Cookies

Cookies should store

only the Session ID.

The server stores

the session itself.

______________________________________________________________________

### Missing HttpOnly

Without `HttpOnly`,

JavaScript may access cookies,

making XSS attacks more damaging.

______________________________________________________________________

### Never Expiring Sessions

Permanent sessions

increase the impact

of stolen cookies.

______________________________________________________________________

### Using HTTP

Session cookies

should never travel

over unencrypted connections.

______________________________________________________________________

### Ignoring Logout

Deleting the browser cookie

is not enough.

The server-side session

must also be invalidated.

______________________________________________________________________

# Quick Comparison

| Insecure | Secure |
| ------------------ | ------------------- |
| HTTP | HTTPS |
| No HttpOnly | HttpOnly enabled |
| No Secure flag | Secure enabled |
| No SameSite | SameSite configured |
| Permanent sessions | Expiring sessions |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Session Hijacking, and how can it be prevented?

Session Hijacking occurs when an attacker obtains a valid session identifier and uses it to impersonate an authenticated
user. Common causes include XSS, unencrypted HTTP traffic, malware, and stolen devices. Developers can reduce the risk
by using HTTPS, setting cookies with the `HttpOnly`, `Secure`, and `SameSite` attributes, expiring sessions after
inactivity, regenerating session IDs after login, invalidating sessions on logout, and monitoring for suspicious session
activity.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Session Hijacking is
- How sessions are stolen
- HTTPS protection
- HttpOnly
- Secure cookies
- SameSite
- Session expiration
- Secure logout
- Best practices

______________________________________________________________________

# What's Next

[Session Fixation](31-session-fixation.md)
