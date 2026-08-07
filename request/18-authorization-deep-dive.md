# Complete HTTP Request Lifecycle Deep Dive

## 18. Authorization Deep Dive

> Target Audience: Backend Engineers (Intermediate → Senior)
>
> Goal: Understand what authorization is, how it works after authentication, common authorization models, role-based and permission-based access control, and best practices for securing APIs.

______________________________________________________________________

# Introduction

In the previous chapter,

the backend

verified

the user's identity.

```
Authentication

↓

User Verified
```

Now,

the next question is

```
What is this user

allowed to do?
```

This process is called

```
Authorization
```

______________________________________________________________________

# What is Authorization?

Interview favorite.

Authorization determines

what resources

an authenticated user

can access

and

what actions

they can perform.

It answers

```
What are you allowed to do?
```

______________________________________________________________________

# Authentication vs Authorization

```
Authentication

↓

Who are you?
```

```
Authorization

↓

What can you do?
```

Example

```
Login

↓

Authentication

↓

User Identified

↓

Authorization

↓

Access Granted?
```

______________________________________________________________________

# Example

Suppose

two users

log in.

```
Admin

↓

Delete User

↓

Allowed
```

```
Normal User

↓

Delete User

↓

Denied
```

Both users

are authenticated,

but only one

is authorized.

______________________________________________________________________

# High Level Flow

```
Incoming Request

↓

Authentication

↓

User Identified

↓

Authorization

↓

Permission Check

↓

Business Logic
```

______________________________________________________________________

# Where Does Authorization Happen?

Authorization

can happen

at different levels.

- API Gateway
- Middleware
- Dependency
- Route Handler
- Business Logic

In FastAPI,

it is commonly

implemented

using

dependencies.

______________________________________________________________________

# Example

```python
@app.delete("/users/{id}")
async def delete_user(
    current_user=Depends(get_current_user)
):
    ...
```

After

authentication,

the application

checks

whether

`current_user`

has permission.

______________________________________________________________________

# Role-Based Access Control (RBAC)

Interview favorite.

Users

are assigned

roles.

Example

```
Admin

Manager

Employee

Customer
```

Permissions

are attached

to roles.

______________________________________________________________________

# RBAC Example

| Role | Permissions |
|------|-------------|
| Admin | Create, Update, Delete, View |
| Manager | Update, View |
| Employee | View |
| Customer | View Own Data |

______________________________________________________________________

# Authorization Flow

```
User

↓

Role

↓

Permission

↓

Access Decision
```

______________________________________________________________________

# Permission-Based Access Control

Instead of

checking roles,

the system

checks

specific permissions.

Example

```
user:create
```

```
user:update
```

```
user:delete
```

```
report:view
```

A user

may have

multiple permissions.

______________________________________________________________________

# Attribute-Based Access Control (ABAC)

Interview favorite.

Authorization

depends on

attributes.

Examples

- User Role
- Department
- Country
- Time
- Resource Owner

Example

```
Department

=

Finance

↓

Allow

Financial Reports
```

______________________________________________________________________

# Ownership Check

Very common

in APIs.

Example

```
GET /orders/123
```

The backend checks

```
Does this order

belong

to

the current user?
```

If not

```
403 Forbidden
```

______________________________________________________________________

# Admin Override

Some actions

are reserved

for administrators.

Example

```
Delete User

↓

Admin?

↓

Yes

↓

Proceed
```

______________________________________________________________________

# Resource-Level Authorization

Suppose

a user

tries to access

```
/users/5
```

Backend checks

```
Current User

↓

Owner?

↓

OR

Admin?
```

Only then

does it

return the data.

______________________________________________________________________

# Authorization in JWT

Many applications

store

basic authorization

information

inside the JWT.

Example

```json
{
    "sub": "123",
    "role": "admin"
}
```

The backend

can quickly

check

the user's role.

______________________________________________________________________

# Should Permissions Be Stored in JWT?

Small applications

often do.

Large systems

usually

retrieve

permissions

from

the database

or

a permission service.

This avoids

stale permissions

when roles change.

______________________________________________________________________

# Common HTTP Status Codes

```
401 Unauthorized
```

Means

the user

is not authenticated.

______________________________________________________________________

```
403 Forbidden
```

Means

the user

is authenticated

but lacks permission.

______________________________________________________________________

# Example

No Token

↓

```
401 Unauthorized
```

______________________________________________________________________

Valid Token

No Permission

↓

```
403 Forbidden
```

______________________________________________________________________

# Authorization Example

```python
if current_user.role != "admin":
    raise HTTPException(
        status_code=403
    )
```

______________________________________________________________________

# Policy-Based Authorization

Instead of

hardcoding rules,

some applications

define

authorization policies.

Example

```
Policy

↓

CanEditUser

↓

Evaluate

↓

Allow / Deny
```

This keeps

business rules

organized.

______________________________________________________________________

# Fine-Grained Authorization

Instead of

checking only

roles,

the application

checks

specific actions.

Example

```
Invoice

↓

View

↓

Allowed
```

```
Invoice

↓

Delete

↓

Denied
```

______________________________________________________________________

# Common Authorization Models

```
RBAC

↓

Role-Based
```

```
ABAC

↓

Attribute-Based
```

```
PBAC

↓

Policy-Based
```

```
ACL

↓

Access Control List
```

______________________________________________________________________

# Access Control List (ACL)

Every resource

stores

who

can access it.

Example

```
Document A

↓

Riyaz

Read

Write
```

```
Alice

↓

Read
```

Useful

for

document sharing

applications.

______________________________________________________________________

# Multi-Tenant Applications

Interview favorite.

Suppose

Company A

and

Company B

use

the same application.

Authorization checks

```
Tenant ID

↓

Matches?

↓

Allow
```

Users

must never

access

another tenant's data.

______________________________________________________________________

# Common Authorization Mistakes

## Trusting the Frontend

Never trust

buttons

or

hidden menus.

Even if

the UI hides

"Delete",

the backend

must still

check permissions.

______________________________________________________________________

## Hardcoding Roles

Avoid

scattering

role checks

throughout

the codebase.

Use

centralized policies

or

permission helpers.

______________________________________________________________________

## Missing Ownership Checks

Always verify

that users

can access

only

their own resources

unless

they have

elevated privileges.

______________________________________________________________________

# Best Practices

- Follow the Principle of Least Privilege
- Check permissions on every protected request
- Keep authorization logic centralized
- Log authorization failures
- Never rely on frontend validation
- Separate authentication from authorization

______________________________________________________________________

# Technologies Used

| Purpose | Technology |
|----------|------------|
| Framework | FastAPI |
| Authentication | JWT, OAuth2 |
| Authorization | RBAC, ABAC, ACL |
| Policy Engines | OPA (Open Policy Agent), Casbin |
| Identity Providers | Keycloak, Auth0 |

______________________________________________________________________

# Common Interview Questions

## What is the difference between Authentication and Authorization?

Authentication verifies the user's identity. Authorization determines what an authenticated user is allowed to access or
perform.

______________________________________________________________________

## What is RBAC?

Role-Based Access Control assigns permissions to roles, and users inherit permissions through their assigned roles.

______________________________________________________________________

## What is the difference between 401 and 403?

- **401 Unauthorized** means the user is not authenticated.
- **403 Forbidden** means the user is authenticated but does not have permission to perform the requested action.

______________________________________________________________________

## Why shouldn't the frontend enforce authorization?

Frontend controls can be bypassed. The backend must always perform authorization checks because it is the trusted
authority.

______________________________________________________________________

## When should permissions be stored in JWT?

For simple applications, storing roles or permissions in JWTs can improve performance. In larger systems where
permissions change frequently, permissions are usually retrieved from a database or authorization service.

______________________________________________________________________

# Interview Deep Dive

## Question

Explain how authorization works in a backend application.

### Answer

After a user is authenticated, the backend evaluates whether the user has permission to perform the requested action.
This may involve checking the user's role, permissions, ownership of the resource, or organizational policies. If the
authorization check succeeds, the request proceeds to the business logic. Otherwise, the server returns a **403
Forbidden** response.

______________________________________________________________________

# Summary

Authorization ensures

that authenticated users

can perform

only

the actions

they are permitted

to perform.

Common authorization models include

- Role-Based Access Control (RBAC)
- Permission-Based Access Control
- Attribute-Based Access Control (ABAC)
- Access Control Lists (ACL)
- Policy-Based Authorization

After authentication and authorization are complete,

the application is ready to execute

the actual business logic,

starting with validating and sanitizing user input.

______________________________________________________________________

# Next

[19. Validation and Sanitization](19-validation-and-sanitization.md)
