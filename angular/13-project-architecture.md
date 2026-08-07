# Project Architecture

As Angular applications grow,

good architecture becomes more important than writing code.

A small application with 5 components can survive poor organization.

An enterprise application with

- 500 Components
- 150 Services
- 80 Developers

cannot.

This chapter explains how real Angular applications are organized.

______________________________________________________________________

# Why Architecture Matters

Poor structure

```
app/

├── component1

├── component2

├── component3

├── service1

├── service2

├── service3

├── test

├── temp

├── old

├── new
```

Nobody knows where anything belongs.

______________________________________________________________________

Good structure

```
app/

├── core/

├── features/

├── shared/

├── layouts/

├── models/

├── services/

├── interceptors/

├── guards/
```

Everything has a place.

______________________________________________________________________

# Typical Enterprise Structure

```
src/

├── app/

│   ├── core/

│   ├── features/

│   ├── shared/

│   ├── layouts/

│   ├── guards/

│   ├── interceptors/

│   ├── services/

│   ├── models/

│   ├── pipes/

│   ├── directives/

│   └── app.routes.ts

├── assets/

├── environments/

├── styles.css

└── main.ts
```

This is a common structure used in enterprise Angular projects.

______________________________________________________________________

# Layered Architecture

```
User

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

Each layer has one responsibility.

______________________________________________________________________

# Feature-Based Architecture

Instead of grouping by file type,

group by feature.

Good

```
features/

├── users/

├── orders/

├── products/

├── reports/
```

Each feature contains everything it needs.

______________________________________________________________________

# Example

```
features/

└── users/

    ├── pages/

    ├── components/

    ├── services/

    ├── models/

    ├── routes/

    └── users.routes.ts
```

Everything related to Users stays together.

______________________________________________________________________

# Core Folder

Contains application-wide functionality.

Example

```
core/

├── auth/

├── interceptors/

├── guards/

├── config/

├── services/

└── layout/
```

Core should contain

- Authentication
- Global services
- Configuration
- Startup logic

______________________________________________________________________

# Shared Folder

Contains reusable code.

```
shared/

├── components/

├── directives/

├── pipes/

├── models/

├── utils/
```

Shared code

does not belong to a single feature.

______________________________________________________________________

# Feature Folder

Each business feature has

its own folder.

Example

```
orders/

├── components/

├── pages/

├── services/

├── models/

├── routes/

└── guards/
```

This makes scaling much easier.

______________________________________________________________________

# Layouts

Common layouts

```
layouts/

├── admin/

├── public/

├── dashboard/
```

Each layout may contain

```
Header

Sidebar

Footer
```

______________________________________________________________________

# Components Folder

```
components/

├── navbar/

├── footer/

├── loader/

├── modal/

├── button/
```

Reusable UI.

______________________________________________________________________

# Pages Folder

Pages correspond to routes.

Example

```
pages/

├── dashboard/

├── users/

├── reports/
```

Usually loaded through routing.

______________________________________________________________________

# Models

Store interfaces.

```
models/

├── user.ts

├── order.ts

├── product.ts
```

Never duplicate models.

______________________________________________________________________

# Services

```
services/

├── auth.service.ts

├── user.service.ts

├── order.service.ts
```

Each service

owns one business domain.

______________________________________________________________________

# Guards

```
guards/

├── auth.guard.ts

├── admin.guard.ts
```

Responsible only for navigation decisions.

______________________________________________________________________

# Interceptors

```
interceptors/

├── auth.interceptor.ts

├── error.interceptor.ts

├── logging.interceptor.ts
```

Intercept every HTTP request.

______________________________________________________________________

# Pipes

```
pipes/

├── currency.pipe.ts

├── truncate.pipe.ts
```

Transform displayed values.

______________________________________________________________________

# Directives

```
directives/

├── autofocus.directive.ts

├── permission.directive.ts
```

Reusable UI behavior.

______________________________________________________________________

# Assets

```
assets/

├── images/

├── icons/

├── fonts/

├── json/
```

Static resources.

______________________________________________________________________

# Environment Configuration

```
environments/

├── environment.ts

├── environment.development.ts

├── environment.production.ts
```

Example

```typescript
export const environment = {

    production: false,

    apiUrl:

    "http://localhost:8080"

};
```

Production

```typescript
export const environment = {

    production: true,

    apiUrl:

    "https://api.company.com"

};
```

Never hardcode URLs.

______________________________________________________________________

# Using Environment

```typescript
this.http.get(

`${environment.apiUrl}/users`

);
```

______________________________________________________________________

# Configuration Flow

```
Angular

↓

Environment

↓

API URL

↓

Backend
```

______________________________________________________________________

# Barrel Files

Instead of

```typescript
import {

User

}

from

"../../models/user";
```

Use

```
models/

index.ts
```

```typescript
export * from "./user";

export * from "./order";
```

Import

```typescript
import {

User

}

from "../models";
```

Cleaner imports.

______________________________________________________________________

# Path Aliases

Instead of

```typescript
../../../services
```

Use

```typescript
@services

@models

@shared
```

Configured in

```
tsconfig.json
```

Example

```json
"paths": {

"@models/*":[

"src/app/models/*"

]

}
```

Much easier to read.

______________________________________________________________________

# Smart Folder Organization

Bad

```
components/

↓

Everything
```

Good

```
features/

↓

orders/

↓

components
```

Keep code close to the feature that owns it.

______________________________________________________________________

# Lazy Loaded Features

```
Application

↓

Dashboard

↓

Users

↓

Reports

↓

Admin
```

Each feature loads

only when required.

Smaller bundle.

______________________________________________________________________

# State Ownership

Question

Where should data live?

Example

```
UserComponent

↓

UserService

↓

Backend
```

Not

```
UserComponent

↓

Global Variable
```

______________________________________________________________________

# Reusable Components

Good

```
ButtonComponent

LoaderComponent

ModalComponent

TableComponent
```

Can be reused

across the application.

______________________________________________________________________

# Naming Convention

Good

```
user-card.component.ts

auth.service.ts

order.model.ts
```

Bad

```
component.ts

test.ts

new.ts

temp.ts
```

Names should describe purpose.

______________________________________________________________________

# Folder Depth

Avoid

```
app/

↓

folder/

↓

folder/

↓

folder/

↓

folder/

↓

component
```

Too many nested folders

make navigation difficult.

______________________________________________________________________

# Application Flow

```
Browser

↓

Route

↓

Page

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

↓

Response

↓

Component

↓

UI
```

This flow appears repeatedly in enterprise applications.

______________________________________________________________________

# Logging

Instead of

```typescript
console.log()
```

Consider a dedicated logging service.

```
Component

↓

LoggerService

↓

Console

OR

Remote Logging
```

______________________________________________________________________

# Error Handling

Don't handle errors

inside every component.

Instead

```
Component

↓

Service

↓

Interceptor

↓

Global Error Handler
```

Centralized error handling is easier to maintain.

______________________________________________________________________

# Dependency Direction

Correct

```
Component

↓

Service

↓

HttpClient
```

Wrong

```
Service

↓

Component
```

Lower layers should not depend on higher layers.

______________________________________________________________________

# Enterprise Example

```
features/

└── users/

    ├── pages/

    │   └── users-page/

    ├── components/

    │   ├── user-table/

    │   ├── user-card/

    │   └── user-filter/

    ├── services/

    │   └── user.service.ts

    ├── models/

    │   └── user.ts

    └── users.routes.ts
```

Everything related to Users stays together.

______________________________________________________________________

# Backend Comparison

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

Very similar layering.

______________________________________________________________________

# Common Mistakes

## One Giant Components Folder

Wrong

```
components/

↓

400 Components
```

Group by feature.

______________________________________________________________________

## Hardcoding API URLs

Wrong

```
localhost
```

Use environment configuration.

______________________________________________________________________

## Shared Folder Becomes a Dumping Ground

Only place truly reusable code there.

Feature-specific code belongs with the feature.

______________________________________________________________________

## Circular Dependencies

Avoid

```
Feature A

↓

Feature B

↓

Feature A
```

Keep dependencies one-directional.

______________________________________________________________________

## Huge Services

Split services

by business domain.

______________________________________________________________________

# Best Practices

✅ Organize by feature.

✅ Keep reusable code in `shared`.

✅ Keep global services in `core`.

✅ Use environment files.

✅ Use lazy loading.

✅ Keep components small.

✅ Use path aliases.

✅ Keep dependencies one-directional.

______________________________________________________________________

# Interview Deep Dive

## Question

Why do enterprise Angular applications organize code by feature?

### Answer

Feature-based organization keeps related components, services, models, and routes together, making the application
easier to navigate, maintain, and scale as new features are added.

______________________________________________________________________

## Question

What is the difference between the `core` and `shared` folders?

### Answer

The `core` folder contains application-wide services and configuration used throughout the application, while the
`shared` folder contains reusable components, directives, pipes, and utilities that can be used by multiple features.

______________________________________________________________________

## Question

Why should API URLs be stored in environment files?

### Answer

Environment files allow applications to use different configurations for development, testing, and production without
changing application code.

______________________________________________________________________

## Question

Why are path aliases useful?

### Answer

Path aliases improve readability and maintainability by replacing long relative import paths with meaningful aliases
such as `@models` or `@services`.

______________________________________________________________________

## Question

What is lazy loading?

### Answer

Lazy loading loads feature code only when it is needed, reducing the application's initial bundle size and improving
startup performance.

______________________________________________________________________

# Practice Questions

1. Why is project architecture important?
1. What is feature-based architecture?
1. What belongs in the `core` folder?
1. What belongs in the `shared` folder?
1. Why should applications use environment files?
1. What are path aliases?
1. Why are barrel files useful?
1. What is the benefit of organizing by feature instead of file type?
1. Why should dependencies flow from components to services?
1. Describe a typical enterprise Angular project structure.

______________________________________________________________________

# Summary

Good architecture is one of the biggest differences between small Angular projects and enterprise applications.

In this chapter, you learned:

- Layered architecture
- Feature-based organization
- `core`
- `shared`
- Feature folders
- Layouts
- Models
- Services
- Guards
- Interceptors
- Pipes
- Directives
- Environment configuration
- Barrel files
- Path aliases
- Lazy loading
- Enterprise project structure
- Best practices

With the project structure in place, the next step is securing your application. We'll learn **Authentication &
Authorization**, covering JWT authentication, login flows, route guards, HTTP interceptors, refresh tokens, and
role-based access control (RBAC).

______________________________________________________________________

# Next

[Authentication & Authorization](14-authentication.md)
