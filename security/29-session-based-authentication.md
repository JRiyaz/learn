# Security - Part 29

# Session-Based Authentication

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Session-Based Authentication is
- How sessions work
- Cookies vs Sessions
- Session IDs
- Server-side session storage
- Redis-backed sessions
- Sessions vs JWT
- Best practices

______________________________________________________________________

# What is Session-Based Authentication?

Session-Based Authentication is an authentication mechanism where the **server remembers the logged-in user**.

Instead of sending the username and password on every request,

the client sends a **Session ID**.

The server uses this Session ID to identify the user.

______________________________________________________________________

# Typical Flow

```text id="sess2901"
Login

↓

Verify Username & Password

↓

Create Session

↓

Generate Session ID

↓

Send Session ID to Browser

↓

Browser Stores Cookie

↓

Future Requests Send Cookie
```

______________________________________________________________________

# How Does It Work?

Suppose the user logs in successfully.

The server creates a session.

Example

```text id="sess2902"
Session ID

↓

abc123xyz789
```

The server stores:

```text id="sess2903"
Session ID

↓

User ID

↓

Expiration Time
```

The browser receives only the Session ID.

______________________________________________________________________

# Where Is the Session Stored?

The important point is:

The **session data stays on the server**.

Example

```text id="sess2904"
Browser

↓

Session ID

↓

FastAPI

↓

Redis / Database / Memory

↓

Actual Session
```

The browser never stores

the user's permissions,

roles,

or profile.

Only the Session ID.

______________________________________________________________________

# Cookies vs Sessions

Many beginners think they are the same.

They are not.

## Cookie

A cookie is simply a small piece of data stored in the browser.

Example

```text id="sess2905"
session_id=abc123xyz789
```

______________________________________________________________________

## Session

A session is the data stored on the server.

Example

```text id="sess2906"
Session ID

↓

User ID

↓

Role

↓

Login Time

↓

Expiration
```

**Cookie = Identifier**

**Session = Server-side Data**

______________________________________________________________________

# Session Authentication Flow

```text id="sess2907"
Browser

↓

Cookie

↓

Session ID

↓

Server

↓

Lookup Session

↓

Authenticated User
```

______________________________________________________________________

# FastAPI Example

After login,

the server may return

```http id="sess2908"
Set-Cookie:

session_id=abc123xyz789
```

The browser automatically stores it.

Future requests include

```http id="sess2909"
Cookie:

session_id=abc123xyz789
```

Your application retrieves the session

using this ID.

______________________________________________________________________

# Where Should Sessions Be Stored?

For small applications,

sessions can be stored:

- In memory

For production,

prefer:

- Redis
- Database

Redis is the most common choice because it is:

- Fast
- Shared across multiple servers
- Supports expiration

______________________________________________________________________

# Redis-Based Sessions

Production architecture

```text id="sess2910"
Browser

↓

FastAPI 1

↓

Redis

↑

FastAPI 2

↓

FastAPI 3
```

Every application server

can access

the same session.

Without Redis,

users might be logged out

when requests reach a different server.

______________________________________________________________________

# Session Expiration

Sessions should expire.

Example

```text id="sess2911"
Login

↓

Session Created

↓

30 Minutes

↓

Session Expires
```

Expired sessions

must require

the user to log in again.

______________________________________________________________________

# Logging Out

Logout is straightforward.

```text id="sess2912"
User Clicks Logout

↓

Delete Session

↓

Invalidate Cookie
```

Once the session is removed,

the Session ID

no longer works.

This is one advantage

sessions have over JWT.

______________________________________________________________________

# Session vs JWT

| Sessions | JWT |
| ------------------------- | --------------------------------------- |
| Session stored on server | User data stored in token |
| Browser stores Session ID | Browser stores JWT |
| Easy logout | Requires token expiration or revocation |
| Server memory required | Stateless |
| Common for web apps | Common for REST APIs |

______________________________________________________________________

# Advantages of Sessions

✅ Easy logout

✅ Easy session revocation

✅ Simple permission updates

✅ Good browser support

______________________________________________________________________

# Disadvantages

❌ Requires server storage

❌ Harder to scale without Redis

❌ Additional infrastructure

______________________________________________________________________

# Sessions in Modern Applications

Typical architecture

```text id="sess2913"
Browser

↓

Cookie

↓

FastAPI

↓

Redis

↓

Database
```

This architecture

is used by many large web applications.

______________________________________________________________________

# Session Security

A Session ID

is effectively

the user's identity.

Anyone possessing the Session ID

can impersonate the user.

Therefore,

protect it carefully.

We'll discuss:

- Session Hijacking
- Session Fixation

in the next lessons.

______________________________________________________________________

# Secure Cookie Flags

Session cookies should include:

```http id="sess2914"
Secure

HttpOnly

SameSite=Lax
```

These reduce the risk of:

- XSS
- Session theft
- CSRF

We'll explain each flag shortly.

______________________________________________________________________

# Defense in Depth

Secure session authentication combines:

```text id="sess2915"
HTTPS

↓

Secure Cookies

↓

Redis Sessions

↓

Expiration

↓

Authorization

↓

Logging
```

______________________________________________________________________

# Best Practices

✅ Store sessions on the server.

✅ Use Redis in production.

✅ Expire inactive sessions.

✅ Delete sessions on logout.

✅ Use Secure cookies.

✅ Use HttpOnly cookies.

✅ Use SameSite cookies.

______________________________________________________________________

# Common Mistakes

### Storing Sensitive Data in Cookies

Cookies should contain

only a Session ID,

not user roles,

passwords,

or personal information.

______________________________________________________________________

### Never Expiring Sessions

Sessions should always have

reasonable expiration times.

______________________________________________________________________

### Using Memory Storage in Production

Memory-based sessions

don't work well

across multiple servers.

Redis is the preferred choice.

______________________________________________________________________

### Assuming Cookies Are Sessions

Cookies transport

the Session ID.

The session itself

remains on the server.

______________________________________________________________________

# Quick Comparison

| Sessions | JWT |
| --------------------- | -------------------------- |
| Server stores session | Client stores token |
| Easy logout | Harder logout |
| Redis for scaling | No shared storage required |
| Great for browsers | Great for APIs |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Session-Based Authentication, and how does it differ from JWT authentication?

Session-Based Authentication stores the user's authentication state on the server and sends only a Session ID to the
client, typically in a cookie. On each request, the server retrieves the session using that ID. JWT authentication, on
the other hand, stores user claims inside a signed token that the client sends with each request, allowing the server to
authenticate without maintaining session state. Sessions simplify logout and session revocation, while JWTs are better
suited for stateless APIs and distributed systems.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Session-Based Authentication is
- Cookies vs Sessions
- Session IDs
- Redis-backed sessions
- Session expiration
- Logout
- Sessions vs JWT
- Best practices

______________________________________________________________________

# What's Next

[Session Hijacking](30-session-hijacking.md)
