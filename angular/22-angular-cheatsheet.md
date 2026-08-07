# Angular Cheatsheet

This cheatsheet is designed for **last-minute interview revision**.

If you have only **30–60 minutes before an interview**, this file should help you quickly refresh the most important
Angular concepts.

______________________________________________________________________

# Angular Architecture

```
Browser

↓

Angular

↓

Component

↓

Service

↓

HttpClient

↓

Backend

↓

Database
```

______________________________________________________________________

# Angular Building Blocks

```
Application

↓

Component

↓

Template

↓

Service

↓

Model

↓

Routing
```

______________________________________________________________________

# Component

```typescript
@Component({

selector:

"app-user"

})
```

Responsible for

- UI
- User interaction
- Calling services

______________________________________________________________________

# Service

```typescript
@Injectable({

providedIn:"root"

})
```

Responsible for

- Business Logic
- API Calls
- Shared State
- Data Transformation

______________________________________________________________________

# Data Binding

| Type | Syntax |
|-------|--------|
| Interpolation | `{{value}}` |
| Property | `[src]="image"` |
| Event | `(click)="save()"` |
| Two-way | `[(ngModel)]` |

______________________________________________________________________

# Component Communication

Parent

↓

```typescript
@Input()
```

Child

↓

```typescript
@Output()
```

______________________________________________________________________

# Directives

Modern Angular

```
@if

@for

@switch

@defer
```

Legacy

```
*ngIf

*ngFor

*ngSwitch
```

______________________________________________________________________

# Routing

Register

```typescript
provideRouter(

routes

)
```

Display

```html
<router-outlet>

</router-outlet>
```

Navigate

```html
routerLink="/users"
```

Programmatically

```typescript
this.router.navigate(

["/users"]

);
```

______________________________________________________________________

# Route Parameters

```
/users/10
```

Read

```typescript
this.route

.snapshot

.paramMap

.get("id");
```

______________________________________________________________________

# Query Parameters

```
?page=1

&size=20
```

Read

```typescript
queryParamMap
```

______________________________________________________________________

# HttpClient

GET

```typescript
http.get()
```

POST

```typescript
http.post()
```

PUT

```typescript
http.put()
```

PATCH

```typescript
http.patch()
```

DELETE

```typescript
http.delete()
```

______________________________________________________________________

# Common HTTP Status Codes

| Code | Meaning |
|------:|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

______________________________________________________________________

# Observable Flow

```
Observable

↓

subscribe()

↓

UI
```

______________________________________________________________________

# RxJS Operators

| Operator | Purpose |
|-----------|----------|
| map | Transform |
| filter | Filter |
| tap | Side Effects |
| switchMap | Cancel Previous |
| mergeMap | Parallel |
| concatMap | Sequential |
| exhaustMap | Ignore Duplicates |
| forkJoin | Wait For All |
| combineLatest | Latest Values |
| debounceTime | Delay |
| take | First N |
| takeUntil | Cleanup |
| catchError | Error Handling |
| retry | Retry |

______________________________________________________________________

# Subject Types

| Type | Description |
|------|-------------|
| Subject | No previous value |
| BehaviorSubject | Latest value |
| ReplaySubject | Multiple previous values |

______________________________________________________________________

# Dependency Injection

```
Component

↓

Inject Service

↓

Angular Creates Object
```

Never

```typescript
new UserService()
```

Use

```typescript
constructor(

private service:

UserService

){}
```

______________________________________________________________________

# Forms

Template-driven

```
Simple Forms
```

Reactive

```
Enterprise Forms
```

______________________________________________________________________

# Validators

```typescript
required

email

min

max

minLength

maxLength

pattern
```

______________________________________________________________________

# Pipes

```
uppercase

lowercase

titlecase

currency

date

decimal

percent

slice

json

async

keyvalue
```

______________________________________________________________________

# Custom Pipe

```typescript
transform(

value

){

}
```

______________________________________________________________________

# Authentication Flow

```
Login

↓

JWT

↓

Store Token

↓

Interceptor

↓

Backend
```

______________________________________________________________________

# Authorization

```
Authentication

↓

Who Are You?
```

```
Authorization

↓

What Can You Do?
```

______________________________________________________________________

# Route Guard

```
User

↓

Guard

↓

Allowed?

↓

Component
```

______________________________________________________________________

# HTTP Interceptor

```
Request

↓

Interceptor

↓

JWT

↓

Backend
```

______________________________________________________________________

# Change Detection

Strategies

```
Default

OnPush
```

______________________________________________________________________

# OnPush Triggers

- Input reference changes
- Component events
- AsyncPipe emissions
- Signal updates
- Manual change detection

______________________________________________________________________

# Signals

Create

```typescript
signal(0)
```

Read

```typescript
count()
```

Update

```typescript
count.set(5)
```

Computed

```typescript
computed(...)
```

Effect

```typescript
effect(...)
```

______________________________________________________________________

# AsyncPipe

Instead of

```typescript
subscribe()
```

Template

```html
{{

users$

|

async

}}
```

______________________________________________________________________

# Performance

Always

✅ OnPush

✅ track

✅ AsyncPipe

✅ Lazy Loading

✅ Signals

______________________________________________________________________

# Modern @for

```html
@for (

user of users;

track user.id

){

}
```

______________________________________________________________________

# Lazy Loading

```
Open Feature

↓

Download Code

↓

Display UI
```

______________________________________________________________________

# Services

One responsibility

per service.

Good

```
UserService

OrderService

AuthService
```

Bad

```
AppService
```

______________________________________________________________________

# Project Structure

```
core/

shared/

features/

layouts/

models/

services/

guards/

interceptors/
```

______________________________________________________________________

# Folder Responsibilities

| Folder | Purpose |
|---------|----------|
| core | Global functionality |
| shared | Reusable code |
| features | Business features |
| layouts | Page layouts |
| models | Interfaces |
| services | Business logic |
| guards | Route protection |
| interceptors | HTTP interception |

______________________________________________________________________

# Module Federation

```
Shell

↓

Remote Applications
```

Terminology

```
Host

Remote

Shared Library

remoteEntry.js
```

______________________________________________________________________

# CRUD Mapping

| Operation | HTTP |
|------------|------|
| Create | POST |
| Read | GET |
| Update | PUT / PATCH |
| Delete | DELETE |

______________________________________________________________________

# Angular Lifecycle (Most Common)

```
constructor()

↓

ngOnInit()

↓

ngOnDestroy()
```

Remember

- `constructor()` → Dependency Injection only
- `ngOnInit()` → Initialization logic
- `ngOnDestroy()` → Cleanup

______________________________________________________________________

# Standalone Components

Instead of

```
NgModule
```

Use

```typescript
standalone:true
```

______________________________________________________________________

# Modern Angular APIs

```
Standalone Components

Standalone Routing

Signals

inject()

@if

@for

@switch

@defer

Functional Guards

Functional Interceptors
```

______________________________________________________________________

# Enterprise Folder Example

```
features/

└── users/

    ├── pages/

    ├── components/

    ├── services/

    ├── models/

    └── users.routes.ts
```

______________________________________________________________________

# Angular Request Flow

```
Button Click

↓

Component

↓

Service

↓

HttpClient

↓

Interceptor

↓

Backend

↓

JSON

↓

Observable

↓

Template

↓

Browser
```

______________________________________________________________________

# Angular vs Spring Boot

Spring

```
Controller

↓

Service

↓

Repository
```

Angular

```
Component

↓

Service

↓

HttpClient
```

______________________________________________________________________

# Angular vs React

Angular

```
Framework
```

React

```
Library
```

(Detailed comparison in a later chapter.)

______________________________________________________________________

# Top Interview Questions

1. What is Angular?
1. What is a Component?
1. What is Dependency Injection?
1. What is a Service?
1. What is RxJS?
1. Observable vs Promise?
1. Subject vs BehaviorSubject?
1. Why HttpClient returns Observables?
1. What is OnPush?
1. What are Signals?
1. Pure vs Impure Pipes?
1. Route Guard?
1. HTTP Interceptor?
1. JWT Authentication Flow?
1. Lazy Loading vs Module Federation?
1. Feature-based Architecture?
1. Singleton Service?
1. Why AsyncPipe?
1. Why use `track` with `@for`?
1. Standalone Components?

______________________________________________________________________

# Common Best Practices

✅ Keep components small.

✅ Put business logic in services.

✅ Use Reactive Forms for complex forms.

✅ Return Observables from services.

✅ Use AsyncPipe in templates.

✅ Use `track` with `@for`.

✅ Prefer OnPush for performance-sensitive components.

✅ Use feature-based architecture.

✅ Keep HTTP logic inside services.

✅ Use interceptors for authentication.

______________________________________________________________________

# Things to Avoid

❌ API calls inside templates

❌ Business logic inside components

❌ `new` for injected services

❌ Large "God" services

❌ Hardcoded API URLs

❌ Impure pipes without need

❌ Nested subscriptions

❌ Manual DOM manipulation

❌ Missing loading/error states

❌ Forgetting to clean up long-lived subscriptions

______________________________________________________________________

# 10-Minute Interview Revision

Remember these keywords

```
Component

Service

Dependency Injection

Standalone

Routing

HttpClient

Observable

BehaviorSubject

Signals

AsyncPipe

Reactive Forms

JWT

Interceptor

Route Guard

OnPush

track

Lazy Loading

Module Federation

Feature-based Architecture
```

If you can confidently explain each of these topics with a practical example, you're well prepared for most Angular
interviews.

______________________________________________________________________

# Summary

This cheatsheet is a rapid revision guide covering:

- Core Angular concepts
- Routing
- Services
- Dependency Injection
- HttpClient
- RxJS
- Authentication
- Forms
- Pipes
- Performance
- Signals
- Module Federation
- Architecture
- Enterprise best practices

Use it before interviews to refresh the most important concepts in just a few minutes.

______________________________________________________________________

# Next

[Modern Angular Features (Signals Deep Dive)](23-modern-angular-features.md)
