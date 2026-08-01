# Security - Part 31

# Session Fixation

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Session Fixation is
- How it differs from Session Hijacking
- Real-world attack scenario
- Why it happens
- How to prevent it
- Secure session management
- Best practices

______________________________________________________________________

# What is Session Fixation?

Session Fixation is an attack where an attacker **forces a victim to use a Session ID that the attacker already knows**.

Later,

after the victim logs in,

the attacker uses the **same Session ID** to access the victim's account.

Unlike Session Hijacking,

the attacker doesn't steal the session.

Instead,

they make the victim use a session chosen by the attacker.

______________________________________________________________________

# Session Hijacking vs Session Fixation

This is one of the most common interview questions.

| Session Hijacking | Session Fixation |
| -------------------------------------- | --------------------------------------------- |
| Attacker steals an existing Session ID | Attacker supplies the Session ID before login |
| Session belongs to the victim | Session initially belongs to the attacker |
| Happens after login | Starts before login |
| Cookie theft is common | Predictable or reused Session IDs are common |

______________________________________________________________________

# Attack Scenario

Imagine this sequence.

### Step 1

The attacker visits your website.

The server creates

```text id="sf3101"
session_id=ABC123
```

______________________________________________________________________

### Step 2

The attacker somehow sends this Session ID

to the victim.

Examples:

- Malicious link
- Browser manipulation
- Shared computer
- Vulnerable application

______________________________________________________________________

### Step 3

The victim opens the website

using

```text id="sf3102"
session_id=ABC123
```

______________________________________________________________________

### Step 4

The victim logs in.

Bad application behavior:

```text id="sf3103"
Anonymous Session

↓

User Logs In

↓

Same Session ID
```

The server keeps

the existing Session ID.

______________________________________________________________________

### Step 5

The attacker already knows

```text id="sf3104"
ABC123
```

Now,

the attacker sends

that same Session ID.

The server believes

the attacker is the authenticated user.

______________________________________________________________________

# Why Does This Happen?

The application fails to generate

a **new Session ID**

after successful authentication.

Instead,

it upgrades

the anonymous session

into an authenticated session.

______________________________________________________________________

# Correct Behavior

After login,

always generate

a completely new Session ID.

```text id="sf3105"
Anonymous Session

↓

Login

↓

Old Session Destroyed

↓

New Session Created
```

The old Session ID

becomes useless.

______________________________________________________________________

# FastAPI Session Workflow

Secure authentication

should look like this.

```text id="sf3106"
Anonymous User

↓

Temporary Session

↓

Login

↓

Delete Old Session

↓

Generate New Session ID

↓

Authenticated Session
```

______________________________________________________________________

# Regenerate Session IDs

This is the most important defense.

Example

Bad

```text id="sf3107"
Before Login

↓

ABC123

↓

After Login

↓

ABC123
```

Good

```text id="sf3108"
Before Login

↓

ABC123

↓

After Login

↓

XYZ789
```

The attacker only knows

the old Session ID,

which is now invalid.

______________________________________________________________________

# Additional Defenses

Besides regenerating sessions,

also:

- Use HTTPS
- Set `HttpOnly`
- Set `Secure`
- Configure `SameSite`
- Expire inactive sessions
- Destroy sessions during logout

Session security

is built from multiple layers.

______________________________________________________________________

# Session Lifecycle

A secure session lifecycle

looks like this.

```text id="sf3109"
Visit Website

↓

Temporary Session

↓

Login

↓

New Session

↓

Use Application

↓

Logout

↓

Delete Session
```

______________________________________________________________________

# Real-World Example

Imagine an e-commerce website.

Anonymous visitors receive

shopping-cart sessions.

When users log in,

the application should:

- Create a new authenticated session.
- Migrate only the required cart data.
- Destroy the anonymous session.

The session identifier itself

should change.

______________________________________________________________________

# Why HTTPS Doesn't Prevent Session Fixation

HTTPS protects

data during transmission.

It does **not** prevent

an application

from reusing

an existing Session ID.

The application itself

must regenerate

the Session ID.

______________________________________________________________________

# Defense in Depth

Secure session management combines:

```text id="sf3110"
HTTPS

↓

Secure Cookies

↓

HttpOnly

↓

SameSite

↓

Regenerate Session ID

↓

Logout

↓

Expiration
```

______________________________________________________________________

# Best Practices

✅ Generate a new Session ID after login.

✅ Destroy anonymous sessions after authentication.

✅ Invalidate sessions on logout.

✅ Use HTTPS.

✅ Configure secure cookie attributes.

✅ Expire inactive sessions.

______________________________________________________________________

# Common Mistakes

### Reusing Session IDs

Never keep

the same Session ID

before and after login.

______________________________________________________________________

### Assuming HTTPS Solves Everything

HTTPS encrypts traffic.

It does not fix

poor session management.

______________________________________________________________________

### Keeping Old Sessions Alive

Old anonymous sessions

should be destroyed

once authentication succeeds.

______________________________________________________________________

### Forgetting Logout Cleanup

Logging out should remove

the server-side session,

not just delete the browser cookie.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| --------------------------- | -------------------------- |
| Same Session ID after login | New Session ID after login |
| Old session remains valid | Old session destroyed |
| HTTP | HTTPS |
| No expiration | Session expiration |
| No logout cleanup | Session invalidation |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Session Fixation, and how can developers prevent it?

Session Fixation is an attack where an attacker forces a victim to use a session identifier that the attacker already
knows. If the application keeps the same Session ID after the victim logs in, the attacker can reuse that Session ID to
access the authenticated session. Developers can prevent Session Fixation by regenerating the Session ID immediately
after successful authentication, destroying the previous anonymous session, using secure cookie settings, enforcing
HTTPS, and invalidating sessions during logout.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Session Fixation is
- Session Fixation vs Session Hijacking
- Why it happens
- Session regeneration
- Secure session lifecycle
- Best practices

______________________________________________________________________

# What's Next

[Replay Attacks](32-replay-attacks.md)
