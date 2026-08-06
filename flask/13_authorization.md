# Authorization

> **Course:** Flask for Backend Engineers
>
> **Module:** 5
>
> **File:** `13_authorization.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- What Authorization is
- Authentication vs Authorization
- Authorization Flow
- Roles
- Permissions
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Resource Ownership
- Policy-Based Authorization
- Flask Authorization Techniques
- Best Practices
- Common Mistakes

______________________________________________________________________

# What is Authorization?

Authorization answers one question:

> **What are you allowed to do?**

After a user is authenticated,

the application determines whether the user has permission to perform a specific action.

______________________________________________________________________

# Authentication vs Authorization

Authentication

```
Who are you?
```

Authorization

```
What can you do?
```

Flow

```
Login

↓

Authentication

↓

Permission Check

↓

Authorization

↓

Business Logic
```

Authorization always happens **after authentication**.

______________________________________________________________________

# Real World Analogy

Airport

Step 1

```
Passport

↓

Identity Verified
```

(Authentication)

Step 2

```
Business Lounge Access?
```

(Authorization)

Not every passenger has access.

______________________________________________________________________

# Authorization Flow

```
Request

↓

Authenticated User

↓

Permission Check

↓

Allowed?

↓

Yes

↓

Business Logic

↓

Response
```

If permission is denied,

return

```
403 Forbidden
```

______________________________________________________________________

# Common Authorization Models

The most common approaches are:

- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Resource Ownership
- Policy-Based Authorization

______________________________________________________________________

# Role-Based Access Control (RBAC)

Users are assigned roles.

Example

```
User

↓

Role

↓

Permissions
```

Roles

```
Admin

Manager

Employee

Customer
```

______________________________________________________________________

# Example RBAC

```
Admin

↓

Create User

Delete User

View Reports

Manage Settings
```

```
Customer

↓

View Products

Place Orders
```

______________________________________________________________________

# Database Design

```
Users

↓

role

↓

admin
```

Simple,

but limited for large systems.

______________________________________________________________________

# Permission-Based Authorization

Instead of

```
Admin
```

Use

```
users:create

users:update

users:delete

orders:view
```

Permissions provide finer control.

______________________________________________________________________

# Database Example

```
User

↓

Role

↓

Permissions
```

or

```
User

↓

Permissions
```

depending on the application.

______________________________________________________________________

# Resource Ownership

Not every resource requires roles.

Example

```
User A

↓

Owns

↓

Profile
```

User B

↓

Cannot Edit It

Ownership is a common authorization rule.

______________________________________________________________________

# Example

```python
if post.author_id != current_user.id:

    abort(403)
```

The user is authenticated,

but not authorized.

______________________________________________________________________

# Attribute-Based Access Control (ABAC)

Authorization decisions are based on attributes.

Example

```
Department

↓

Finance
```

```
Resource

↓

Finance Report
```

Allow access only when attributes match.

______________________________________________________________________

# Policy-Based Authorization

Rules

```
IF

Role == Admin

↓

Allow
```

```
IF

Owner == Current User

↓

Allow
```

Policies centralize authorization logic.

______________________________________________________________________

# Flask Route Protection

Simple example

```python
@app.route("/admin")

@login_required

def admin():

    if current_user.role != "admin":

        abort(403)

    return "Admin"
```

______________________________________________________________________

# Using Decorators

Instead of repeating checks,

create decorators.

```python
from functools import wraps

from flask import abort

from flask_login import current_user
```

______________________________________________________________________

# Role Decorator

```python
def admin_required(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        if current_user.role != "admin":

            abort(403)

        return func(*args, **kwargs)

    return wrapper
```

Use

```python
@app.route("/admin")

@login_required

@admin_required

def dashboard():

    ...
```

Reusable.

Clean.

______________________________________________________________________

# Multiple Roles

```python
allowed = [

    "admin",

    "manager"

]

if current_user.role not in allowed:

    abort(403)
```

______________________________________________________________________

# Permission Check

```python
if "users:delete" not in current_user.permissions:

    abort(403)
```

More flexible than role checks.

______________________________________________________________________

# Authorization Architecture

```
Request

↓

Authentication

↓

Role

↓

Permission

↓

Business Logic
```

Authorization should happen before executing business logic.

______________________________________________________________________

# 401 vs 403

401

```
Unauthorized
```

Meaning

```
Not Authenticated
```

______________________________________________________________________

403

```
Forbidden
```

Meaning

```
Authenticated

↓

No Permission
```

Interviewers frequently ask this distinction.

______________________________________________________________________

# Resource-Level Authorization

Example

```
GET

/orders/100
```

Check

```
Does

current_user

own

Order 100?
```

Never trust the URL alone.

______________________________________________________________________

# Admin Panels

Typical permissions

```
Admin

↓

Manage Users

↓

Manage Products

↓

View Reports

↓

Manage Settings
```

Each feature should have explicit authorization checks.

______________________________________________________________________

# API Authorization

REST API

```
JWT

↓

Read User Claims

↓

Permission Check

↓

Execute Request
```

JWT identifies the user,

but authorization still happens inside the application.

______________________________________________________________________

# JWT Claims

Example

```json
{
    "sub": 10,
    "role": "admin"
}
```

Claims can assist authorization,

but critical permissions should be validated against trusted application data when appropriate.

______________________________________________________________________

# Centralized Authorization

Good

```
Decorator

↓

Permission Service

↓

Policy Engine
```

Bad

```
Random

if

Statements

Everywhere
```

Centralized logic is easier to maintain.

______________________________________________________________________

# Common Mistakes

❌ Trusting the client to enforce permissions

❌ Returning 401 instead of 403

❌ Hardcoding authorization logic throughout the application

❌ Forgetting ownership checks

❌ Assuming authentication automatically grants authorization

______________________________________________________________________

# Production Best Practices

- Separate authentication from authorization.
- Centralize permission checks.
- Prefer permissions over large role hierarchies for complex systems.
- Validate resource ownership.
- Log authorization failures.
- Apply least-privilege principles.
- Test authorization rules thoroughly.
- Never rely on client-side authorization.

______________________________________________________________________

# Interview Deep Dive

### Question

**Explain the difference between Role-Based Access Control (RBAC) and Permission-Based authorization.**

### Answer

RBAC assigns permissions indirectly through predefined roles such as `Admin` or `Manager`.

Example

```
Admin

↓

Create Users

Delete Users

View Reports
```

Permission-based authorization assigns permissions directly or through roles using fine-grained actions such as:

```
users:create

users:update

users:delete
```

RBAC is simpler to implement.

Permission-based systems provide greater flexibility and are often preferred for larger applications with more complex
authorization requirements.

______________________________________________________________________

# Summary

In this chapter you learned:

- Authorization
- Authentication vs Authorization
- RBAC
- Permissions
- Resource Ownership
- ABAC
- Policy-Based Authorization
- Flask Authorization
- Decorators
- 401 vs 403
- Best Practices

Authorization determines **what an authenticated user is allowed to do** and should be enforced consistently across
every protected resource.

______________________________________________________________________

# Practice Questions

## Fundamentals

1. What is authorization?
1. How is authorization different from authentication?
1. Why does authorization occur after authentication?

______________________________________________________________________

## RBAC

4. What is Role-Based Access Control?
1. What are the advantages of RBAC?
1. What are its limitations?

______________________________________________________________________

## Permissions

7. What is permission-based authorization?
1. Why might permissions be preferred over roles in large systems?
1. How would you model permissions in a database?

______________________________________________________________________

## Flask

10. How can routes be protected based on user roles?
01. Why are decorators useful for authorization?
01. Why should authorization logic be centralized?

______________________________________________________________________

## HTTP Status Codes

13. What is the difference between HTTP 401 and HTTP 403?
01. When should each be returned?

______________________________________________________________________

## Security

15. Why should ownership checks be performed?
01. Why should authorization never rely on client-side logic?

______________________________________________________________________

## Scenario-Based

17. A customer manually changes `/orders/10` to `/orders/11` in the browser. What authorization check should your application perform?
01. Your application contains hundreds of `if current_user.role == ...` statements scattered throughout the codebase. How would you improve the design?
01. A user successfully authenticates but attempts to delete another user's account. Which HTTP status code should be returned, and why?
01. Your application currently supports only `Admin` and `User`, but new requirements introduce dozens of independent permissions. Would RBAC alone still be sufficient? Explain your reasoning.
01. A mobile application includes a hidden "Delete User" button only for administrators. Why must the server still perform authorization checks even if regular users never see the button?

______________________________________________________________________

# Next

[Building REST APIs with Flask](14_rest_api.md)
