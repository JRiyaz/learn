# Security - Part 6

# Broken Access Control

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you'll know:

- What Broken Access Control is
- Why it happens
- Horizontal vs Vertical Privilege Escalation
- IDOR (Insecure Direct Object Reference)
- Secure FastAPI authorization
- Role-Based Access Control (RBAC)
- Ownership validation
- Best practices

______________________________________________________________________

# What is Broken Access Control?

Broken Access Control occurs when a user can perform actions or access resources they are **not authorized** to access.

Remember:

Authentication answers:

```text id="bac601"
Who are you?
```

Authorization answers:

```text id="bac602"
What are you allowed to do?
```

Broken Access Control is an **authorization** problem.

______________________________________________________________________

# Why Does It Happen?

Many developers check:

✅ Is the user logged in?

But forget to check:

❌ Is the user allowed to perform this action?

Being authenticated does **not** mean a user can access everything.

______________________________________________________________________

# Real-World Example

Suppose your application has:

```text id="bac603"
/users/1/profile

/users/2/profile

/users/3/profile
```

Alice logs in.

She should only access:

```text id="bac604"
/users/1/profile
```

Instead,

she changes the URL to:

```text id="bac605"
/users/2/profile
```

If the application returns Bob's profile,

it has Broken Access Control.

______________________________________________________________________

# Typical Flow

```text id="bac606"
Login

↓

JWT Verified

↓

Request Resource

↓

Authorization Check?

↓

Yes → Continue

No → Reject
```

Many vulnerable applications skip the authorization check.

______________________________________________________________________

# Types of Broken Access Control

The most common types are:

```text id="bac607"
Horizontal Privilege Escalation

↓

Vertical Privilege Escalation

↓

IDOR
```

Let's understand each.

______________________________________________________________________

# Horizontal Privilege Escalation

Users with the **same role**

access each other's resources.

Example

```text id="bac608"
Alice

↓

Views Bob's Orders
```

Both are normal users.

Alice simply accesses data that belongs to Bob.

______________________________________________________________________

# Vertical Privilege Escalation

A normal user gains administrator privileges.

Example

```text id="bac609"
User

↓

Admin Dashboard
```

Or

```text id="bac610"
DELETE /users/15
```

If a normal user can perform administrator actions,

the application has vertical privilege escalation.

______________________________________________________________________

# IDOR

IDOR stands for

**Insecure Direct Object Reference**.

Example

```text id="bac611"
GET /orders/101
```

User changes it to

```text id="bac612"
GET /orders/102
```

If order 102 belongs to another customer,

the API should reject the request.

If it returns the order,

the application is vulnerable.

IDOR is one of the most common backend security vulnerabilities.

______________________________________________________________________

# Vulnerable FastAPI Example

```python id="bac613"
@app.get("/users/{user_id}")
def get_user(user_id: int):

    user = db.query(User).get(user_id)

    return user
```

______________________________________________________________________

# Why is This Vulnerable?

The API only checks

whether the requested user exists.

It never verifies

whether the authenticated user

owns that resource.

Any authenticated user

can request any ID.

______________________________________________________________________

# Secure Version

Suppose authentication provides

the current user.

```python id="bac614"
@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user: User,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return current_user
```

Now,

users can only access

their own profile.

______________________________________________________________________

# Ownership Validation

One of the simplest authorization rules is:

> A user can only access resources they own.

Workflow

```text id="bac615"
Request Resource

↓

Who Owns It?

↓

Current User?

↓

Yes → Allow

No → Reject
```

This pattern appears everywhere:

- Orders
- Books
- Messages
- Files
- Payments
- Profiles

______________________________________________________________________

# Role-Based Access Control (RBAC)

Sometimes,

ownership isn't enough.

Different users have different roles.

Example

```text id="bac616"
Admin

↓

Delete Books

Manage Users

View Reports
```

```text id="bac617"
Librarian

↓

Manage Books

Cannot Delete Users
```

```text id="bac618"
Student

↓

Borrow Books

Return Books
```

The backend checks

the user's role

before allowing an action.

______________________________________________________________________

# FastAPI RBAC Example

```python id="bac619"
if current_user.role != "admin":
    raise HTTPException(
        status_code=403,
        detail="Forbidden",
    )
```

Only administrators

can continue.

______________________________________________________________________

# Authorization Should Be Everywhere

Don't authorize only at login.

Authorization should happen

every time

a protected resource is accessed.

```text id="bac620"
Every Request

↓

Authentication

↓

Authorization

↓

Business Logic
```

______________________________________________________________________

# Defense in Depth

Good authorization combines:

```text id="bac621"
JWT

↓

Ownership Check

↓

RBAC

↓

Database Permissions

↓

Audit Logging
```

If one layer fails,

others still provide protection.

______________________________________________________________________

# Database-Level Protection

Applications should not rely

only on application code.

Use database users

with the minimum permissions required.

Example

```text id="bac622"
Application

↓

Read

Write

↓

Cannot Drop Tables
```

______________________________________________________________________

# Best Practices

✅ Verify authorization on every protected request.

✅ Check resource ownership.

✅ Use RBAC where appropriate.

✅ Return HTTP 403 for unauthorized access.

✅ Apply least privilege.

✅ Log authorization failures.

______________________________________________________________________

# Common Mistakes

### Checking Authentication Only

Authentication proves identity.

Authorization determines permissions.

You need both.

______________________________________________________________________

### Trusting IDs from the Client

Never assume

a requested ID

belongs to the current user.

Always verify ownership.

______________________________________________________________________

### Hardcoding Admin Logic Everywhere

As applications grow,

centralize authorization logic

using dependencies,

middleware,

or authorization services.

______________________________________________________________________

### Forgetting Internal APIs

Even internal APIs

need authorization.

Never assume internal traffic is always trusted.

______________________________________________________________________

# Quick Comparison

| Vulnerable | Secure |
| ------------------ | --------------------------- |
| Check only login | Check login + authorization |
| Trust resource IDs | Verify ownership |
| No role checks | RBAC |
| Full permissions | Least privilege |

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is Broken Access Control?

Broken Access Control occurs when an application allows users to access resources or perform actions beyond their
authorized permissions. Common examples include Horizontal Privilege Escalation, Vertical Privilege Escalation, and
Insecure Direct Object References (IDOR). To prevent it, applications should verify authorization on every request,
enforce ownership validation, implement role-based access control, follow the Principle of Least Privilege, and log
unauthorized access attempts.

______________________________________________________________________

# Summary

In this lesson, you learned:

- What Broken Access Control is
- Authentication vs Authorization
- Horizontal Privilege Escalation
- Vertical Privilege Escalation
- IDOR
- Ownership validation
- RBAC
- FastAPI authorization patterns
- Best practices

______________________________________________________________________

# What's Next

[JWT Security](07-jwt-security.md)
