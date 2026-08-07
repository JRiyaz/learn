# Authentication & Authorization

Authentication and Authorization are among the most important topics in Angular interviews.

Almost every enterprise Angular application has

- Login
- Logout
- JWT
- Protected Routes
- Role-based Access
- Refresh Tokens
- HTTP Interceptors

Understanding the complete authentication flow is essential.

______________________________________________________________________

# Authentication vs Authorization

These two terms are often confused.

## Authentication

Authentication answers

```
Who are you?
```

Example

```
Username

+

Password

↓

Verify Identity
```

______________________________________________________________________

## Authorization

Authorization answers

```
What are you allowed to do?
```

Example

```
Admin

↓

Delete User

✔ Allowed
```

```
Guest

↓

Delete User

✘ Not Allowed
```

______________________________________________________________________

# Real Life Example

Authentication

```
Airport Security

↓

Passport Check

↓

Who Are You?
```

Authorization

```
Business Lounge

↓

Do You Have Access?
```

______________________________________________________________________

# Authentication Flow

A typical Angular authentication flow

```
User

↓

Login Page

↓

Angular

↓

POST /login

↓

Backend

↓

Validate Credentials

↓

JWT Token

↓

Angular

↓

Store Token

↓

Dashboard
```

______________________________________________________________________

# Complete Request Flow

```
User Clicks Login

↓

Component

↓

AuthService

↓

HttpClient

↓

Backend

↓

JWT

↓

Store Token

↓

Navigate

↓

Dashboard
```

______________________________________________________________________

# Login Request

Example

```json
POST /login

{

"username":"riyaz",

"password":"password123"

}
```

______________________________________________________________________

# Backend Response

```json
{

"accessToken":"eyJhbGc...",

"refreshToken":"abcd1234",

"user":{

"id":1,

"name":"Riyaz",

"role":"ADMIN"

}

}
```

Angular now has everything needed.

______________________________________________________________________

# JWT

JWT

\=

JSON Web Token

It is a signed token that proves

```
Identity
```

The backend creates it.

Angular stores it.

______________________________________________________________________

# JWT Structure

```
Header

.

Payload

.

Signature
```

Example

```
xxxxx

.

yyyyy

.

zzzzz
```

______________________________________________________________________

# JWT Payload

Usually contains

```json
{

"sub":"123",

"name":"Riyaz",

"role":"ADMIN",

"exp":1720000000

}
```

Angular should **not** trust this payload for authorization decisions alone; the backend remains the source of truth.

______________________________________________________________________

# Why JWT?

Without JWT

```
Every Request

↓

Login Again
```

Impossible.

Instead

```
Login Once

↓

Receive JWT

↓

Send JWT

↓

Backend Verifies
```

______________________________________________________________________

# Token Storage

Common options

```
Memory

Local Storage

Session Storage

Cookies
```

______________________________________________________________________

# Local Storage

Example

```typescript
localStorage.setItem(

"token",

jwt

);
```

Simple,

but vulnerable to XSS if your application is compromised.

______________________________________________________________________

# Session Storage

Same API

```typescript
sessionStorage.setItem(...)
```

Cleared

when browser tab closes.

______________________________________________________________________

# HttpOnly Cookies

Many enterprise applications prefer

```
HttpOnly Cookies
```

Advantages

- JavaScript cannot read them
- Better protection against XSS

Trade-offs

- Requires CSRF protection
- Backend configuration

This is generally considered the preferred approach for sensitive applications.

______________________________________________________________________

# Which Storage Should You Use?

| Storage | Notes |
|----------|-------|
| Local Storage | Simple, but exposed to JavaScript |
| Session Storage | Cleared when tab closes |
| HttpOnly Cookie | Better security, requires backend support |

There is no universal answer.

It depends on

- Security requirements
- Backend architecture
- Organization standards

______________________________________________________________________

# AuthService

Authentication logic belongs in

```
AuthService
```

Example

```typescript
@Injectable({

providedIn:"root"

})

export class AuthService {

}
```

______________________________________________________________________

# Login Method

```typescript
login(

credentials:

LoginRequest

){

return this.http.post(

"/login",

credentials

);

}
```

Component

does not know

how authentication works.

______________________________________________________________________

# Login Component

```
Login Button

↓

AuthService

↓

Backend

↓

JWT

↓

Dashboard
```

______________________________________________________________________

# Storing User

Besides JWT,

applications often store

```
Current User
```

using

```
BehaviorSubject
```

Example

```
Current User

↓

Navbar

↓

Sidebar

↓

Profile
```

All components stay synchronized.

______________________________________________________________________

# Route Guards

Suppose

```
/dashboard
```

requires login.

```
User

↓

Route Guard

↓

Logged In?

↓

Yes

↓

Dashboard

No

↓

Login
```

______________________________________________________________________

# Functional Guard (Modern)

```typescript
export const authGuard =

() => {

return true;

};
```

Real applications check

authentication state.

______________________________________________________________________

# Registering Guard

```typescript
{

path:"dashboard",

canActivate:[

authGuard

]

}
```

Angular calls the guard

before loading the component.

______________________________________________________________________

# Guard Flow

```
Navigation

↓

Guard

↓

Allowed?

↓

Component

OR

Redirect
```

______________________________________________________________________

# Role-Based Authorization (RBAC)

Suppose

```
ADMIN

↓

Everything
```

```
MANAGER

↓

Reports
```

```
USER

↓

Profile
```

Different roles,

different permissions.

______________________________________________________________________

# Example

```
Admin

↓

/users/delete

✔
```

```
User

↓

/users/delete

✘
```

Backend must enforce this authorization even if Angular hides the button.

______________________________________________________________________

# Checking Role

Component

```
Current User

↓

Role

↓

Display UI
```

Example

```html
@if (

user.role ===

"ADMIN"

) {

<button>

Delete

</button>

}
```

This improves the UI,

but **is not a security boundary**.

______________________________________________________________________

# Logout

Logout

```
Remove JWT

↓

Clear User

↓

Navigate Login
```

______________________________________________________________________

# Logout Flow

```
Logout

↓

Clear Storage

↓

BehaviorSubject

↓

null

↓

Login Page
```

______________________________________________________________________

# Refresh Token

Access Tokens

expire quickly.

Instead of forcing users

to log in again,

applications use

```
Refresh Token
```

______________________________________________________________________

# Refresh Flow

```
Access Token Expired

↓

401

↓

Refresh Token

↓

New Access Token

↓

Retry Request
```

Usually handled automatically

by an interceptor.

______________________________________________________________________

# HTTP Interceptor

Instead of

adding JWT

to every request

manually,

Angular intercepts requests.

```
Component

↓

Interceptor

↓

JWT

↓

Backend
```

______________________________________________________________________

# Authorization Header

Every request becomes

```
GET /users

Authorization:

Bearer eyJ...
```

Automatically.

______________________________________________________________________

# Authentication Lifecycle

```
Login

↓

JWT

↓

Store

↓

Interceptor

↓

Backend

↓

401

↓

Refresh

↓

Continue
```

______________________________________________________________________

# Route Protection

Public Routes

```
/

/login

/register
```

Protected Routes

```
/dashboard

/users

/orders

/admin
```

______________________________________________________________________

# Session Expiration

If refresh fails

```
Backend

↓

401

↓

Logout

↓

Login Page
```

______________________________________________________________________

# Multiple Tabs

Suppose

User logs out

in one tab.

Applications should

keep authentication state

consistent across tabs.

Common approaches

- Storage events
- Shared state
- Backend session validation

______________________________________________________________________

# Enterprise Authentication Flow

```
Login

↓

JWT

↓

Interceptor

↓

API

↓

401

↓

Refresh

↓

Retry

↓

Logout

(if refresh fails)
```

______________________________________________________________________

# Backend Comparison

Spring Boot

```
POST /login

↓

JWT

↓

Filter

↓

Controller
```

Angular

```
Login Component

↓

AuthService

↓

Interceptor

↓

Backend
```

______________________________________________________________________

# Common Mistakes

## Storing Password

Never store

```
Password
```

Only tokens.

______________________________________________________________________

## Checking Authorization Only in Angular

Wrong

```
Hide Button

↓

Secure
```

No.

Backend must always enforce authorization.

______________________________________________________________________

## Adding JWT in Every Service

Wrong

```
Service

↓

Header

↓

Service

↓

Header
```

Use an interceptor.

______________________________________________________________________

## Long-Lived Access Tokens

Keep access tokens

short-lived.

Use refresh tokens

to maintain sessions.

______________________________________________________________________

# Best Practices

✅ Keep authentication logic inside `AuthService`.

✅ Use route guards for protected routes.

✅ Use interceptors for JWT headers.

✅ Use refresh tokens.

✅ Keep access tokens short-lived.

✅ Enforce authorization on the backend.

✅ Store minimal user information on the client.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between Authentication and Authorization?

### Answer

Authentication verifies a user's identity, while authorization determines what actions that authenticated user is
allowed to perform.

______________________________________________________________________

## Question

What is JWT?

### Answer

JWT (JSON Web Token) is a signed token issued by the backend after successful authentication. The client includes it
with subsequent requests so the backend can verify the user's identity.

______________________________________________________________________

## Question

Why are HTTP Interceptors used for authentication?

### Answer

Interceptors automatically attach authentication headers, centralize authentication logic, handle token refresh, and
avoid duplicating code across multiple services.

______________________________________________________________________

## Question

What is a Route Guard?

### Answer

A Route Guard determines whether navigation to a route should be allowed. It is commonly used to prevent unauthenticated
users from accessing protected pages.

______________________________________________________________________

## Question

Should Angular enforce authorization?

### Answer

Angular can improve the user experience by hiding unauthorized UI elements, but the backend must always enforce
authorization because client-side checks can be bypassed.

______________________________________________________________________

# Practice Questions

1. What is Authentication?
1. What is Authorization?
1. What is JWT?
1. Why are refresh tokens used?
1. What is an AuthService?
1. What is a Route Guard?
1. Why should JWT headers be added using an interceptor?
1. What is RBAC?
1. Where should authentication state be stored?
1. Explain the complete authentication flow from login to accessing a protected API.

______________________________________________________________________

# Summary

Authentication is a critical part of every enterprise Angular application.

In this chapter, you learned:

- Authentication vs Authorization
- JWT
- Login flow
- AuthService
- Token storage
- Route Guards
- RBAC
- Logout
- Refresh Tokens
- HTTP Interceptors
- Session expiration
- Enterprise authentication architecture
- Best practices

The next chapter takes a deeper look at **Services**, moving beyond dependency injection to cover service design, shared
state, caching, facade patterns, and enterprise service architecture.

______________________________________________________________________

# Next

[Services Deep Dive](15-services.md)
