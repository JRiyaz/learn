# Security - Part 3

# Cross-Site Scripting (XSS)

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Cross-Site Scripting (XSS) is
- Why it happens
- The different types of XSS
- How backend developers contribute to XSS prevention
- Vulnerable Python/FastAPI examples
- Secure implementations
- Best practices

______________________________________________________________________

# What is Cross-Site Scripting?

Cross-Site Scripting (XSS) is a vulnerability where an attacker manages to inject **JavaScript** into a web page viewed
by another user.

Instead of executing only the website's intended JavaScript,

the browser executes the attacker's JavaScript as well.

______________________________________________________________________

# Why Does It Happen?

Applications sometimes display user-provided content without properly escaping or sanitizing it.

Example:

```text id="xss301"
User Input

↓

Database

↓

Backend API

↓

Browser

↓

JavaScript Executes
```

The browser cannot distinguish between:

- Legitimate page content
- Malicious script

______________________________________________________________________

# Real-World Example

Imagine your Library application allows users to leave book reviews.

User submits:

```text id="xss302"
Great book!
```

Everything is fine.

But suppose someone submits malicious HTML or JavaScript instead.

If the application stores and later displays it without proper handling,

every user who views that review could be affected.

______________________________________________________________________

# Types of XSS

There are three common types.

```text id="xss303"
Stored XSS

↓

Reflected XSS

↓

DOM-based XSS
```

Let's understand each one.

______________________________________________________________________

# Stored XSS

The malicious content is stored permanently.

Example

```text id="xss304"
Attacker

↓

Submit Comment

↓

Database

↓

Another User Opens Page

↓

Script Executes
```

Stored XSS is generally considered the most dangerous because every visitor may receive the malicious content.

______________________________________________________________________

# Reflected XSS

The malicious content is immediately reflected back in the server's response.

Example

```text id="xss305"
Search

↓

Backend

↓

Response

↓

Browser
```

Nothing is stored in the database.

The malicious content exists only for that request.

______________________________________________________________________

# DOM-Based XSS

The backend may never see the malicious content.

Instead,

JavaScript running in the browser modifies the page using untrusted data.

```text id="xss306"
Browser

↓

JavaScript

↓

DOM Updated

↓

Script Executes
```

This is primarily a frontend issue,

but backend developers should know it exists.

______________________________________________________________________

# Vulnerable FastAPI Example

Suppose your API stores user comments.

```python id="xss307"
from fastapi import FastAPI

app = FastAPI()

comments = []

@app.post("/comments")
def add_comment(comment: str):
    comments.append(comment)
    return {"message": "Saved"}

@app.get("/comments")
def get_comments():
    return comments
```

______________________________________________________________________

# Why Can This Become a Problem?

The backend stores **exactly** what the user sends.

If a frontend application later renders those comments as HTML without escaping,

malicious content could execute.

Notice:

The FastAPI API itself isn't executing JavaScript.

The danger appears when another application displays the stored content unsafely.

______________________________________________________________________

# Secure Approach

The backend should:

- Validate input
- Limit accepted formats
- Treat user content as data
- Never assume downstream applications will sanitize it

Example validation using Pydantic.

```python id="xss308"
from pydantic import BaseModel, Field

class CommentRequest(BaseModel):
    comment: str = Field(
        max_length=500
    )
```

Input validation improves overall security,

although it is **not** a complete XSS defense.

______________________________________________________________________

# Escaping Output

The most important XSS protection happens when displaying data.

Instead of rendering raw HTML,

render escaped text.

```text id="xss309"
Unsafe

↓

Render HTML

Safe

↓

Render Text
```

Modern frontend frameworks usually escape output by default.

Problems arise when developers intentionally bypass those protections.

______________________________________________________________________

# Sanitizing HTML

Sometimes,

applications legitimately allow HTML.

Example:

- Blog editor
- Rich text editor
- Documentation platform

In those situations,

sanitize the HTML before storing or displaying it.

Only allow approved tags and attributes.

______________________________________________________________________

# Content Security Policy (CSP)

A Content Security Policy limits which scripts the browser may execute.

Example

```text id="xss310"
Browser

↓

CSP Rules

↓

Unknown Script

↓

Blocked
```

CSP does **not** replace proper validation,

but it provides another layer of defense.

______________________________________________________________________

# Why Backend Developers Should Care

Even if you don't build the frontend,

your API:

- Accepts user input
- Stores user content
- Returns user content

Poor handling at the backend can make frontend applications vulnerable.

Security is a shared responsibility.

______________________________________________________________________

# Best Practices

✅ Validate incoming data.

✅ Escape output before rendering.

✅ Sanitize HTML when HTML input is required.

✅ Use Content Security Policy.

✅ Avoid rendering raw HTML unnecessarily.

✅ Review rich text features carefully.

______________________________________________________________________

# Common Mistakes

### Assuming APIs Cannot Cause XSS

APIs often provide the data that web applications display.

Unsafe data from an API can still lead to XSS.

______________________________________________________________________

### Trusting User Input

Never assume comments,

usernames,

or descriptions are safe.

Treat all user-provided content as untrusted.

______________________________________________________________________

### Allowing Arbitrary HTML

Only allow HTML when absolutely necessary,

and sanitize it first.

______________________________________________________________________

### Depending Only on Validation

Validation alone is not sufficient.

Escaping and safe rendering are equally important.

______________________________________________________________________

# Quick Comparison

| Unsafe | Safe |
| ---------------- | ------------------------- |
| Render raw HTML | Escape output |
| Trust user input | Validate user input |
| Allow all HTML | Sanitize allowed HTML |
| No CSP | Use CSP where appropriate |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Cross-Site Scripting (XSS), and how can backend developers help prevent it?

Cross-Site Scripting (XSS) occurs when untrusted user input is interpreted as executable JavaScript in another user's
browser. Backend developers help prevent XSS by validating user input, storing user data safely, avoiding unnecessary
HTML support, sanitizing HTML when it is required, and ensuring that frontend applications receive data intended to be
rendered safely. Additional protections such as Content Security Policy provide defense in depth.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What XSS is
- Stored, Reflected, and DOM-based XSS
- Why backend developers should understand XSS
- Vulnerable FastAPI example
- Safe handling of user content
- Escaping and sanitization
- Content Security Policy
- Best practices

______________________________________________________________________

# What's Next

[Cross-Site Request Forgery (CSRF)](04-cross-site-request-forgery.md)
