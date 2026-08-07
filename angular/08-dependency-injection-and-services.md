# Dependency Injection & Services

One of Angular's biggest strengths is its **Dependency Injection (DI)** system.

If you've worked with **Spring Boot**, you'll immediately notice the similarities.

| Spring Boot | Angular |
|-------------|----------|
| `@Service` | `@Injectable` |
| `@Autowired` / Constructor Injection | Constructor Injection |
| Bean Container | Dependency Injection Container |
| Singleton Bean | Singleton Service |

Angular's DI system automatically creates and manages objects for you.

______________________________________________________________________

# Why Do We Need Services?

Imagine a component that

- Calls APIs
- Calculates totals
- Validates users
- Sends emails
- Logs events

```
UserComponent

↓

1000 Lines
```

This becomes difficult to maintain.

Instead

```
Component

↓

Service

↓

Backend
```

Business logic belongs in services.

______________________________________________________________________

# What is a Service?

A service is a TypeScript class that contains

- Business logic
- API calls
- Shared data
- Utility functions

Unlike components,

services

- Have no HTML
- Have no CSS
- Are reusable

______________________________________________________________________

# Component vs Service

| Component | Service |
|------------|----------|
| Controls UI | Business Logic |
| HTML | No HTML |
| User Interaction | Data Processing |
| Display Data | Fetch Data |
| Usually Page-Specific | Reusable |

______________________________________________________________________

# Typical Architecture

```
User Click

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

The component should rarely communicate directly with the backend.

______________________________________________________________________

# Creating a Service

Angular CLI

```bash
ng generate service services/user
```

or

```bash
ng g s services/user
```

Angular creates

```
user.service.ts
```

______________________________________________________________________

# Service Example

```typescript
export class UserService {

    getUsers() {

        return [];

    }

}
```

Currently,

it's just a normal TypeScript class.

______________________________________________________________________

# @Injectable()

Angular recognizes services using

```typescript
@Injectable()
```

Example

```typescript
import {

    Injectable

}

from "@angular/core";

@Injectable({

    providedIn: "root"

})

export class UserService {

}
```

______________________________________________________________________

# What Does @Injectable() Do?

It tells Angular

```
This Class

↓

Can Be Injected
```

Angular becomes responsible for creating and managing the object.

______________________________________________________________________

# What Does providedIn: "root" Mean?

```typescript
@Injectable({

    providedIn: "root"

})
```

Means

```
Application

↓

One Instance

↓

Shared Everywhere
```

This is called a

```
Singleton Service
```

______________________________________________________________________

# What is a Singleton?

A singleton means

```
One Object

↓

Entire Application
```

Example

```
UserComponent

↓

UserService

↑

DashboardComponent
```

Both components receive the **same** instance.

______________________________________________________________________

# Why Singleton?

Imagine

```
Shopping Cart
```

If every component creates its own cart,

the application breaks.

Instead

```
One Cart Service

↓

Shared
```

Everyone sees the same data.

______________________________________________________________________

# Dependency Injection

Instead of writing

```typescript
const service =

new UserService();
```

Angular creates it.

Example

```typescript
constructor(

    private userService:

    UserService

) {

}
```

No

```typescript
new
```

required.

______________________________________________________________________

# Constructor Injection

Component

```typescript
@Component({

})

export class UserComponent {

    constructor(

        private userService:

        UserService

    ) {

    }

}
```

Angular automatically passes

```
UserService
```

into the constructor.

______________________________________________________________________

# How Dependency Injection Works

```
Angular

↓

Creates UserService

↓

Stores Instance

↓

Creates Component

↓

Injects Service
```

The component never creates the service itself.

______________________________________________________________________

# Visualizing DI

Without DI

```
Component

↓

new UserService()

↓

Tight Coupling
```

With DI

```
Angular

↓

Creates Service

↓

Injects Service

↓

Component
```

Much cleaner.

______________________________________________________________________

# Why Not Use new?

Wrong

```typescript
export class UserComponent {

    private service =

        new UserService();

}
```

Problems

- Hard to test
- Hard to replace
- Tight coupling

______________________________________________________________________

Correct

```typescript
constructor(

private service:

UserService

) {

}
```

Angular manages the lifecycle.

______________________________________________________________________

# inject() (Modern Angular)

Angular now also supports

```typescript
inject()
```

instead of constructor injection in some cases.

Example

```typescript
import {

    inject

}

from "@angular/core";

export class UserComponent {

    private userService =

        inject(

            UserService

        );

}
```

Useful for

- Functional Guards
- Functional Interceptors
- Utility functions
- Cleaner code in some scenarios

Constructor injection is still the most common approach for components and services.

______________________________________________________________________

# Service Calling Backend

Example

```typescript
@Injectable({

providedIn:"root"

})

export class UserService {

    constructor(

        private http:

        HttpClient

    ) {}

}
```

Later

```typescript
getUsers() {

}
```

will call the backend.

______________________________________________________________________

# Component Uses Service

```typescript
export class UserComponent {

    constructor(

        private userService:

        UserService

    ) {}

}
```

Notice

No HTTP code yet.

The component simply asks the service.

______________________________________________________________________

# Complete Flow

```
Button Click

↓

Component

↓

UserService

↓

HttpClient

↓

Backend

↓

Database

↓

JSON

↓

Service

↓

Component

↓

Template

↓

Browser
```

This is the standard Angular architecture.

______________________________________________________________________

# Sharing Data

Suppose

```
Navbar

↓

Shopping Cart
```

Both need

```
Cart Count
```

Instead of copying data,

both use

```
CartService
```

```
Navbar

↓

CartService

↑

Checkout
```

One shared source of truth.

______________________________________________________________________

# Real Enterprise Services

Examples

```
UserService

ProductService

OrderService

CartService

PaymentService

AuthService

NotificationService
```

Each service has one responsibility.

______________________________________________________________________

# Service Folder

Example

```
app/

├── services/

│   ├── user.service.ts

│   ├── auth.service.ts

│   ├── cart.service.ts

│   └── payment.service.ts
```

______________________________________________________________________

# Service Responsibilities

Good

```
UserService

↓

Users
```

Bad

```
UserService

↓

Users

↓

Payments

↓

Reports

↓

Authentication
```

Keep services focused.

______________________________________________________________________

# Service Lifetime

Default

```
Application Starts

↓

Create Service

↓

Reuse

↓

Application Ends
```

Singleton.

______________________________________________________________________

# Can Angular Create Multiple Instances?

Yes.

Although

```
providedIn:"root"
```

creates a singleton,

providers can also be configured at

- Component level
- Route level
- Feature level

creating separate instances.

For most applications,

singleton services are the default.

______________________________________________________________________

# Dependency Injection Hierarchy

Simplified

```
Application Injector

↓

Route Injector

↓

Component Injector
```

Angular searches upward until it finds a matching provider.

Most beginners only need to remember

```
providedIn:"root"

↓

Application-wide Singleton
```

______________________________________________________________________

# Spring Boot Comparison

Spring

```java
@Service

public class UserService {

}
```

Controller

```java
public UserController(

UserService service

)
```

Angular

```typescript
@Injectable({

providedIn:"root"

})

export class UserService {

}
```

Component

```typescript
constructor(

private service:

UserService

)
```

Almost identical concepts.

______________________________________________________________________

# Common Mistakes

## Creating Services with new

Wrong

```typescript
new UserService()
```

Always let Angular inject services.

______________________________________________________________________

## Business Logic in Components

Wrong

```
Component

↓

Validation

↓

Calculations

↓

API Calls
```

Move logic into services.

______________________________________________________________________

## One Huge Service

Don't create

```
AppService
```

containing everything.

Split responsibilities.

______________________________________________________________________

## Using inject() Everywhere

`inject()` is powerful,

but constructor injection remains the clearest and most common choice for components.

Use `inject()` where it naturally fits, such as functional APIs.

______________________________________________________________________

# Best Practices

✅ Keep services focused.

✅ Let Angular create services.

✅ Prefer constructor injection for components.

✅ Use `inject()` where appropriate in modern Angular.

✅ Use singleton services for shared application state.

✅ Keep API communication inside services.

______________________________________________________________________

# Interview Deep Dive

## Question

What is Dependency Injection?

### Answer

Dependency Injection is a design pattern where Angular creates and supplies required objects instead of classes creating
them manually. This reduces coupling, improves testability, and centralizes object creation.

______________________________________________________________________

## Question

What is a service in Angular?

### Answer

A service is a reusable TypeScript class that contains business logic, API communication, or shared functionality.
Services are injected into components using Angular's Dependency Injection system.

______________________________________________________________________

## Question

Why shouldn't components create services using `new`?

### Answer

Creating services manually tightly couples components to their dependencies and bypasses Angular's Dependency Injection
system. Using injection improves testing, flexibility, and lifecycle management.

______________________________________________________________________

## Question

What does `providedIn: 'root'` mean?

### Answer

It registers the service with the application's root injector, creating a single shared instance (singleton) that can be
injected anywhere in the application.

______________________________________________________________________

## Question

What is the difference between constructor injection and `inject()`?

### Answer

Constructor injection is the traditional and most common approach for components and services. The `inject()` function
is a newer API that's particularly useful in functional guards, interceptors, and other contexts where constructor
injection isn't available or would be less convenient.

______________________________________________________________________

# Practice Questions

1. What is a service?
1. What is Dependency Injection?
1. Why are services used?
1. What does `@Injectable()` do?
1. What does `providedIn: 'root'` mean?
1. What is a singleton service?
1. Why shouldn't services be created using `new`?
1. What is constructor injection?
1. What is the purpose of `inject()`?
1. Explain the complete flow from a component to the backend using a service.

______________________________________________________________________

# Summary

Dependency Injection is one of Angular's core features and one of the main reasons Angular scales well for enterprise
applications.

In this chapter, you learned:

- Services
- `@Injectable()`
- Dependency Injection
- Constructor injection
- `inject()`
- Singleton services
- `providedIn: 'root'`
- Service lifetime
- Dependency Injection hierarchy
- Service architecture
- Angular vs Spring Boot DI
- Best practices

Now that you know how Angular organizes business logic, the next step is learning **Routing**, where you'll see how
Angular navigates between screens without reloading the page using the Angular Router.

______________________________________________________________________

# Next

[Routing](09-routing.md)
