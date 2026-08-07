# Services Deep Dive

In the previous chapter, we learned what services are and how Angular's Dependency Injection (DI) works.

In this chapter, we'll go much deeper and understand how services are used in **real enterprise Angular applications**.

If Components are the **UI layer**,

Services are the **Business Layer**.

This chapter is especially important if you're coming from a Spring Boot or FastAPI background because the architecture
is very similar.

______________________________________________________________________

# Service Responsibilities

A service should contain

- Business Logic
- API Communication
- State Management
- Data Transformation
- Caching
- Shared Logic
- Utility Functions

A service should **NOT** contain

- HTML
- CSS
- UI Rendering

______________________________________________________________________

# Angular Architecture

```
Browser

↓

Component

↓

Service

↓

HttpClient

↓

Backend API

↓

Database
```

Notice

Every layer has one responsibility.

______________________________________________________________________

# Why Services Exist

Imagine an application without services.

```
Component

↓

Login

↓

Validation

↓

API Calls

↓

JWT

↓

Cart Logic

↓

Reports

↓

Notifications
```

One component

becomes

```
2000 Lines
```

Instead

```
Component

↓

Services

↓

Backend
```

Everything becomes reusable.

______________________________________________________________________

# Real Enterprise Example

Suppose we are building Amazon.

Instead of

```
AmazonComponent
```

we create

```
AuthService

↓

UserService

↓

ProductService

↓

CartService

↓

OrderService

↓

PaymentService

↓

NotificationService
```

Each service owns one business domain.

______________________________________________________________________

# Service Folder Structure

```
services/

├── auth.service.ts

├── cart.service.ts

├── order.service.ts

├── payment.service.ts

├── product.service.ts

├── report.service.ts

├── user.service.ts

└── notification.service.ts
```

Very common structure.

______________________________________________________________________

# Single Responsibility Principle

Each service should do

ONE thing.

Good

```
CartService

↓

Shopping Cart
```

Bad

```
CartService

↓

Cart

↓

Authentication

↓

Reports

↓

Payments
```

______________________________________________________________________

# Example Service

```typescript
@Injectable({

providedIn:"root"

})

export class UserService {

constructor(

private http:

HttpClient

){}

}
```

Simple.

Focused.

Reusable.

______________________________________________________________________

# Service Lifecycle

Angular creates services

using Dependency Injection.

```
Application Starts

↓

Angular Creates Service

↓

Inject Into Components

↓

Reuse Same Instance

↓

Application Ends
```

______________________________________________________________________

# Singleton Service

Most services are

```
Singletons
```

Meaning

```
One Object

↓

Entire Application
```

______________________________________________________________________

# Example

```
Navbar

↓

UserService

↑

Dashboard

↑

Profile
```

All components

share

the same service.

______________________________________________________________________

# Why Singleton?

Suppose

```
Shopping Cart
```

Without singleton

```
Navbar

↓

CartService #1

Checkout

↓

CartService #2
```

Different carts.

Broken application.

Singleton

↓

One shared cart.

______________________________________________________________________

# Component Scoped Service

Sometimes

each component

needs

its own instance.

Example

```typescript
@Component({

providers:[

UserService

]

})
```

Now

every component

gets

a different service instance.

______________________________________________________________________

# Singleton vs Component Provider

| Singleton | Component Provider |
|------------|-------------------|
| One Instance | Multiple Instances |
| Shared Data | Isolated Data |
| Default Choice | Rare Use Cases |

______________________________________________________________________

# Dependency Graph

```
Angular

↓

UserService

↓

HttpClient

↓

Backend
```

Angular automatically creates

the entire dependency tree.

______________________________________________________________________

# Calling Multiple Services

Example

```
Dashboard

↓

UserService

↓

OrderService

↓

RevenueService
```

Perfectly normal.

Components can use

multiple services.

______________________________________________________________________

# Service Collaboration

Sometimes

services call

other services.

Example

```
OrderService

↓

PaymentService

↓

NotificationService
```

Avoid making

deep dependency chains.

______________________________________________________________________

# Good Dependency Flow

```
Component

↓

OrderService

↓

PaymentService
```

______________________________________________________________________

# Bad Dependency Flow

```
Service A

↓

Service B

↓

Service C

↓

Service D

↓

Service A
```

Circular dependency.

Avoid this.

______________________________________________________________________

# Shared State

One of the biggest reasons

for services.

Example

```
Current User
```

```
Navbar

↓

AuthService

↑

Profile

↑

Dashboard
```

Everyone receives

the same data.

______________________________________________________________________

# Using BehaviorSubject

```typescript
private user$ =

new BehaviorSubject<User | null>(

null

);
```

Update

```typescript
this.user$.next(

user

);
```

Read

```typescript
this.user$.asObservable();
```

Very common pattern.

______________________________________________________________________

# State Flow

```
Login

↓

BehaviorSubject

↓

Navbar

↓

Profile

↓

Dashboard
```

UI updates automatically.

______________________________________________________________________

# Caching

Suppose

```
GET /countries
```

Countries

rarely change.

Instead of

```
API

↓

API

↓

API
```

Use cache.

```
API

↓

Cache

↓

Reuse
```

______________________________________________________________________

# Cache Example

```
User Opens Page

↓

API

↓

Cache Result

↓

Future Requests

↓

Return Cache
```

Faster.

Fewer backend calls.

______________________________________________________________________

# Facade Pattern

Large applications

sometimes introduce

a

```
Facade
```

```
Dashboard

↓

DashboardFacade

↓

UserService

↓

OrderService

↓

ReportService
```

Component

talks to

ONE object.

______________________________________________________________________

# Why Facade?

Without

```
Dashboard

↓

UserService

↓

OrderService

↓

RevenueService

↓

ChartService

↓

NotificationService
```

Component

becomes cluttered.

Facade simplifies it.

______________________________________________________________________

# Utility Services

Some services

don't call APIs.

Examples

```
LoggerService

DateService

StorageService

ThemeService

ValidationService
```

Reusable utilities.

______________________________________________________________________

# Auth Service

Responsibilities

```
Login

Logout

JWT

Current User

Refresh Token
```

Nothing else.

______________________________________________________________________

# Storage Service

Instead of

```typescript
localStorage
```

everywhere,

create

```
StorageService
```

Benefits

- Easier testing
- Centralized logic
- Easier migration

______________________________________________________________________

# Configuration Service

Suppose

application loads

feature flags

or

configuration.

```
ConfigService

↓

Backend

↓

Configuration

↓

Entire App
```

______________________________________________________________________

# Service Composition

Good

```
DashboardService

↓

UserService

↓

ReportService
```

Services can compose

other services.

Just avoid

circular references.

______________________________________________________________________

# Observable Services

Almost every Angular service

returns

```
Observable
```

Example

```typescript
getUsers(){

return this.http.get<User[]>(

"/users"

);

}
```

Service

does not

subscribe.

Component

decides

when to subscribe.

______________________________________________________________________

# Good Pattern

Service

```typescript
getUsers(){

return this.http.get<User[]>(...);

}
```

Component

```typescript
this.userService

.getUsers()

.subscribe(...);
```

______________________________________________________________________

# Bad Pattern

Service

```typescript
this.http

.get(...)

.subscribe(...);
```

Now

caller

cannot

control

the request.

______________________________________________________________________

# Error Handling

Instead of

every component

handling errors,

services can

transform

common backend responses.

Example

```
Backend

↓

404

↓

Service

↓

Friendly Error
```

Global concerns

belong in interceptors.

______________________________________________________________________

# Testing Services

Services are easier

to test

than components.

Why?

Because

they contain

business logic

without HTML.

______________________________________________________________________

# Enterprise Example

```
Login

↓

AuthService

↓

HttpClient

↓

Backend

↓

JWT

↓

BehaviorSubject

↓

Navbar Updates
```

Everything

flows

through services.

______________________________________________________________________

# Angular vs Spring Boot

Spring Boot

```
Controller

↓

Service

↓

Repository

↓

Database
```

Angular

```
Component

↓

Service

↓

HttpClient

↓

Backend
```

Very similar architecture.

______________________________________________________________________

# Common Mistakes

## API Calls Inside Components

Wrong

```
Component

↓

HttpClient
```

Always use services.

______________________________________________________________________

## Huge Services

Avoid

```
AppService
```

Split

by business domain.

______________________________________________________________________

## Shared State in Components

Wrong

```
Navbar

↓

Global Variable
```

Use

```
AuthService

CartService

ThemeService
```

______________________________________________________________________

## Circular Dependencies

Never create

```
A

↓

B

↓

C

↓

A
```

______________________________________________________________________

## Subscribing Inside Services

Prefer returning

```
Observable
```

unless the service is intentionally performing a side effect.

______________________________________________________________________

# Best Practices

✅ One responsibility per service

✅ Keep services reusable

✅ Return Observables

✅ Cache expensive requests

✅ Use BehaviorSubject for shared state

✅ Prefer singleton services

✅ Create utility services

✅ Keep UI logic out of services

______________________________________________________________________

# Interview Deep Dive

## Question

Why are services important in Angular?

### Answer

Services separate business logic from UI logic, making applications easier to maintain, test, and reuse. Components
focus on presentation while services handle data access, state management, and business rules.

______________________________________________________________________

## Question

What is the difference between a singleton service and a component-scoped service?

### Answer

A singleton service has one shared instance for the entire application, while a component-scoped service creates a
separate instance for each component that provides it.

______________________________________________________________________

## Question

Why should services return Observables instead of subscribing internally?

### Answer

Returning an Observable allows the caller to decide when and how to subscribe, compose operators, handle errors, and
cancel requests. This makes services more reusable and flexible.

______________________________________________________________________

## Question

What is the Facade pattern?

### Answer

A Facade provides a simplified interface over multiple services. Instead of a component depending on many services
directly, it interacts with a single facade that coordinates the underlying services.

______________________________________________________________________

## Question

When should BehaviorSubject be used?

### Answer

BehaviorSubject is useful for shared application state such as the authenticated user, shopping cart, theme, or other
data that multiple components need to access and react to.

______________________________________________________________________

# Practice Questions

1. Why do Angular applications use services?
1. What is a singleton service?
1. When would you use a component-scoped service?
1. Why should services return Observables?
1. What is the Facade pattern?
1. How do services share state between components?
1. When should data be cached in a service?
1. Why should services have a single responsibility?
1. What are utility services?
1. Compare Angular services with Spring Boot services.

______________________________________________________________________

# Summary

Services are the backbone of enterprise Angular applications.

In this chapter, you learned:

- Service responsibilities
- Service lifecycle
- Singleton vs component-scoped services
- Shared state
- BehaviorSubject
- Service collaboration
- Caching
- Facade pattern
- Utility services
- Observable best practices
- Enterprise architecture
- Angular vs Spring Boot services
- Common mistakes
- Best practices

With services fully covered, the next chapter focuses on **Pipes**, where you'll learn how Angular transforms data for
display using built-in pipes, custom pipes, pure vs impure pipes, and performance considerations.

______________________________________________________________________

# Next

[Pipes](16-pipes.md)
