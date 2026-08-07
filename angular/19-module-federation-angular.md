# Module Federation in Angular

In the previous chapter, we learned **what Module Federation is** and why large organizations use it.

Now it's time to build it in Angular.

By the end of this chapter, you'll understand how companies split one large Angular application into multiple
independently deployable applications.

> **Note:** The examples in this chapter use **modern Angular (Standalone Components)** together with **Webpack Module Federation** concepts. Many organizations use helper tooling (such as `@angular-architects/module-federation`) to simplify the setup, but understanding the underlying architecture is more important than memorizing configuration files.

______________________________________________________________________

# Final Architecture

Suppose our company has

```
E-Commerce Platform
```

We split it into

```
Shell

├── Home

├── Products

├── Orders

├── Payments

├── Admin
```

Each feature

is its own Angular application.

______________________________________________________________________

# Project Structure

```
workspace/

├── shell/

├── products/

├── orders/

├── payments/

└── admin/
```

Each folder

contains

a complete Angular application.

______________________________________________________________________

# Team Ownership

```
Products Team

↓

products/
```

```
Orders Team

↓

orders/
```

```
Payments Team

↓

payments/
```

No team

modifies

another team's code.

______________________________________________________________________

# Host Application

The

```
Shell
```

is the application's entry point.

Responsibilities

- Navigation
- Authentication
- Layout
- Loading Remotes
- Global Configuration

______________________________________________________________________

# Remote Application

A remote owns

one business capability.

Example

```
Orders

↓

Order List

↓

Order Details

↓

Invoices
```

Everything

belongs

to one team.

______________________________________________________________________

# Runtime Flow

```
Browser

↓

Shell

↓

Open Orders

↓

Download Orders Remote

↓

Display Orders
```

No rebuild.

No redeployment

of the shell.

______________________________________________________________________

# Angular Workspace

Usually

each application

is created separately.

Example

```
shell

orders

products

admin
```

Each has

its own

```
package.json

angular.json

src/
```

______________________________________________________________________

# Shell Responsibilities

The shell should contain

- Global Navigation
- Header
- Sidebar
- Authentication
- Layout
- Shared Theme
- Route Registration

It should **not**

contain

business features.

______________________________________________________________________

# Remote Responsibilities

Products Remote

```
Products

Categories

Inventory
```

Orders Remote

```
Orders

Invoices

Returns
```

Payments Remote

```
Transactions

Refunds

Settlement
```

______________________________________________________________________

# Exposing Modules

A remote decides

what other applications

can use.

Example

```
Orders

↓

Expose

OrderComponent
```

Not

the entire application.

______________________________________________________________________

# Remote Entry

Every remote

publishes

a

```
remoteEntry.js
```

This file

tells the shell

how to load

the remote application.

______________________________________________________________________

# Runtime Loading

Shell

```
Needs Orders
```

↓

Downloads

```
remoteEntry.js
```

↓

Loads

```
OrdersComponent
```

↓

Displays UI

______________________________________________________________________

# Shared Dependencies

Suppose

every application

ships

its own Angular runtime.

```
Angular

↓

Orders

Angular

↓

Products

Angular

↓

Admin
```

Huge waste.

______________________________________________________________________

Instead

share

```
Angular

RxJS

Common Libraries
```

One copy.

______________________________________________________________________

# Typical Shared Libraries

```
@angular/core

@angular/common

@angular/router

rxjs
```

Usually shared.

______________________________________________________________________

# Feature Routing

Shell routes

```
/

↓

Home
```

```
/products

↓

Products Remote
```

```
/orders

↓

Orders Remote
```

```
/payments

↓

Payments Remote
```

______________________________________________________________________

# Remote Routing

Inside Orders

```
orders/

↓

List

↓

Details

↓

History
```

The remote

manages

its own routes.

______________________________________________________________________

# Routing Flow

```
Browser

↓

Shell Router

↓

Orders Remote

↓

Orders Router

↓

Order Details
```

Routing

is hierarchical.

______________________________________________________________________

# Authentication

The shell

usually owns

authentication.

```
Login

↓

JWT

↓

Shell

↓

Load Remotes
```

Remotes

reuse

authentication state.

______________________________________________________________________

# Shared Authentication

```
Shell

↓

AuthService

↓

Orders

↓

Products

↓

Admin
```

One authentication system.

______________________________________________________________________

# Communication Between Remotes

Suppose

Orders

creates

a new order.

Cart

must update.

Possible approaches

```
Shared Service

Custom Events

Shared State Library

Backend Synchronization
```

Avoid

tight coupling.

______________________________________________________________________

# Shared UI Components

Instead of

copying buttons

into every remote

create

```
Design System

↓

Button

↓

Modal

↓

Table

↓

Loader
```

Every application

uses

the same UI.

______________________________________________________________________

# Shared Models

Example

```
User

Order

Product
```

Store them

inside

a shared library.

Avoid

duplicating interfaces.

______________________________________________________________________

# Shared Utilities

```
Date Formatter

Logger

Validation

Storage
```

Reusable

across

every application.

______________________________________________________________________

# Independent Deployment

Products Team

changes

```
Products Remote
```

↓

Deploy

Products Only.

Orders

continues

running

without deployment.

______________________________________________________________________

# Version Compatibility

Suppose

Shell

uses

Angular 20

Products

uses

Angular 17.

Possible

runtime issues.

Enterprise teams

usually

keep

major versions

aligned.

______________________________________________________________________

# Remote Failure

Suppose

Orders

is temporarily unavailable.

The shell

should handle it gracefully.

Example

```
Orders

Unavailable

Please Try Again Later
```

Instead of

crashing

the entire application.

______________________________________________________________________

# Loading Indicator

While downloading

a remote

show

```
Loading...

```

Better

user experience.

______________________________________________________________________

# Error Handling

Flow

```
Shell

↓

Load Remote

↓

Success

↓

Display

OR

Failure

↓

Fallback UI
```

Never expose

technical errors

to users.

______________________________________________________________________

# CI/CD

Every remote

has

its own pipeline.

```
Orders

↓

Build

↓

Test

↓

Deploy
```

Independent.

______________________________________________________________________

# Development

Teams

can develop

their remotes

independently.

```
Orders

Running

↓

localhost:4201
```

```
Products

Running

↓

localhost:4202
```

```
Shell

↓

Loads Both
```

______________________________________________________________________

# Enterprise Example

```
Shell

↓

Dashboard

↓

Products Remote

↓

Orders Remote

↓

Payments Remote

↓

Reports Remote
```

Looks

like

one application.

Actually

many applications.

______________________________________________________________________

# Performance

Benefits

```
Smaller Builds

↓

Independent Deployments

↓

Smaller Teams

↓

Scalable Development
```

______________________________________________________________________

# Challenges

Module Federation

introduces

new responsibilities.

- Dependency management
- Version compatibility
- Cross-team coordination
- Monitoring
- Shared library governance

Architecture

becomes

more important.

______________________________________________________________________

# Angular Project Organization

Example

```
shell/

products/

orders/

payments/

shared-ui/

shared-models/
```

Shared libraries

should remain

small

and stable.

______________________________________________________________________

# Deployment Architecture

```
Browser

↓

Shell

↓

CDN

↓

Orders Remote

↓

CDN

↓

Products Remote

↓

CDN

↓

Payments Remote
```

Each application

can be deployed

independently.

______________________________________________________________________

# Backend Comparison

Backend

```
API Gateway

↓

Microservices
```

Frontend

```
Shell

↓

Micro Frontends
```

The shell

plays a role

similar to

an API Gateway,

coordinating access

to independently owned features.

______________________________________________________________________

# Common Mistakes

## Making Every Feature a Remote

Not every feature

should become

its own application.

Choose boundaries

based on

business domains.

______________________________________________________________________

## Sharing Too Much

Only share

stable,

widely used libraries.

Too many shared libraries

increase coupling.

______________________________________________________________________

## Cross-Remote Imports

Avoid

```
Orders

↓

Import

Products

↓

Import

Orders
```

Communicate

through

well-defined interfaces.

______________________________________________________________________

## Large Shell

The shell

should coordinate,

not contain

business logic.

______________________________________________________________________

## Ignoring Failure Scenarios

Always plan for

```
Remote

Unavailable
```

and display

a meaningful fallback.

______________________________________________________________________

# Best Practices

✅ Keep remotes independent.

✅ Split by business capability.

✅ Let the shell own navigation and authentication.

✅ Share only stable libraries.

✅ Handle remote failures gracefully.

✅ Version shared dependencies carefully.

✅ Build and deploy remotes independently.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the role of the Shell application?

### Answer

The Shell is the host application that users open. It provides the application layout, navigation, authentication, and
dynamically loads remote applications at runtime.

______________________________________________________________________

## Question

What is a Remote application?

### Answer

A Remote is an independently built and deployed Angular application that exposes specific modules or components for the
Shell to load.

______________________________________________________________________

## Question

How do remote applications communicate?

### Answer

They should communicate through well-defined mechanisms such as shared services, browser events, shared state libraries,
backend APIs, or URL-based communication, while avoiding tight coupling.

______________________________________________________________________

## Question

What should be shared between remotes?

### Answer

Common frameworks such as Angular and RxJS, along with stable shared libraries like design systems, shared models, and
reusable utilities, are good candidates for sharing.

______________________________________________________________________

## Question

What are the biggest challenges of Module Federation?

### Answer

Managing shared dependencies, coordinating versions, handling failures gracefully, defining clear ownership boundaries,
and maintaining communication between independently developed applications.

______________________________________________________________________

# Practice Questions

1. What is the role of the Shell?
1. What is a Remote?
1. What is `remoteEntry.js`?
1. Why are shared libraries important?
1. How does routing work with Module Federation?
1. How should authentication be handled?
1. How should remotes communicate?
1. Why should each remote have its own CI/CD pipeline?
1. What happens if a remote application is unavailable?
1. Describe a complete Angular Micro Frontend architecture using Module Federation.

______________________________________________________________________

# Summary

Module Federation enables large Angular applications to scale across multiple teams by composing independently built and
deployed applications at runtime.

In this chapter, you learned:

- Shell application
- Remote applications
- Runtime loading
- `remoteEntry.js`
- Shared dependencies
- Routing
- Authentication
- Cross-remote communication
- Shared UI libraries
- Shared models
- Independent deployment
- CI/CD
- Error handling
- Enterprise architecture
- Best practices

You now understand both the **concepts** and the **Angular architecture** behind Module Federation. The next chapter
brings together everything you've learned by building a complete **Angular CRUD Application**, applying routing,
services, HttpClient, RxJS, authentication, forms, and project architecture in a real-world example.

______________________________________________________________________

# Next

[Building a CRUD Application](20-crud-application.md)
