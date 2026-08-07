# Angular Overview

Now that you understand how the web works and why Single Page Applications exist, it's time to learn **Angular** itself.

Angular is much more than a UI library.

It is a **complete frontend framework** for building enterprise web applications.

______________________________________________________________________

# What is Angular?

Angular is an open-source frontend framework developed by **Google**.

It is used to build

- Single Page Applications (SPA)
- Enterprise Dashboards
- Internal Business Applications
- Admin Panels
- CRM Systems
- Banking Applications

Angular provides almost everything needed to build a modern frontend application.

______________________________________________________________________

# Why Was Angular Created?

Building large frontend applications using only JavaScript quickly became difficult.

Problems included

- No project structure
- Difficult state management
- Repeated code
- Manual DOM manipulation
- Hard-to-maintain applications

Angular solves these problems by providing

- Components
- Dependency Injection
- Routing
- HTTP Client
- Forms
- CLI
- Testing Support
- Build Tools

All included in one framework.

______________________________________________________________________

# Angular is Opinionated

Angular encourages a standard way of building applications.

Instead of asking

```
Which Router?

Which HTTP Library?

Which State Library?
```

Angular already provides them.

This makes large teams more consistent.

______________________________________________________________________

# Angular vs AngularJS

These are **different frameworks**.

| AngularJS | Angular |
|------------|----------|
| JavaScript | TypeScript |
| Released in 2010 | Released in 2016 |
| MVC | Component Based |
| Uses Controllers | Uses Components |
| Slower | Faster |
| No longer recommended | Current Angular |

If someone says

```
AngularJS
```

they are referring to the old framework.

Today,

when people say

```
Angular
```

they mean the modern version.

______________________________________________________________________

# Why Companies Choose Angular

Large organizations prefer Angular because it offers

- Consistent architecture
- Strong TypeScript support
- Excellent tooling
- Dependency Injection
- Long-term support
- Enterprise scalability

Companies commonly using Angular include

- Google
- Microsoft (some products)
- Deutsche Bank
- SAP
- IBM
- Enterprise consulting firms

______________________________________________________________________

# Angular Architecture

Everything revolves around

```
Components
```

```
Application

↓

Components

↓

Templates

↓

Services

↓

Backend APIs
```

Every screen is built using components.

______________________________________________________________________

# Angular Building Blocks

Angular applications are made of

```
Components

Services

Templates

Directives

Pipes

Routing

Dependency Injection
```

We'll learn each of these individually.

______________________________________________________________________

# Angular Application Flow

```
Browser

↓

index.html

↓

main.ts

↓

Bootstrap

↓

AppComponent

↓

Router

↓

Component

↓

HTTP Client

↓

Backend API
```

Everything starts from

```
main.ts
```

______________________________________________________________________

# Angular Project Structure

After creating a project,

you'll typically see

```
my-app/

├── src/

├── public/

├── angular.json

├── package.json

├── tsconfig.json

└── node_modules/
```

______________________________________________________________________

# src Folder

This contains your application code.

```
src/

├── app/

├── assets/

├── environments/

├── styles.css

├── index.html

└── main.ts
```

______________________________________________________________________

# app Folder

The heart of the application.

```
app/

├── app.component.ts

├── app.component.html

├── app.component.css

├── app.routes.ts

└── services/
```

As the application grows,

this folder contains

- Components
- Services
- Models
- Guards
- Interceptors
- Shared Code

______________________________________________________________________

# index.html

This is the only HTML page served initially.

Example

```html
<body>

    <app-root></app-root>

</body>
```

Angular replaces

```
<app-root>
```

with the application.

______________________________________________________________________

# main.ts

Application entry point.

Typical example

```typescript
import {

    bootstrapApplication

}

from "@angular/platform-browser";

import {

    AppComponent

}

from "./app/app.component";

bootstrapApplication(

    AppComponent

);
```

This starts Angular.

______________________________________________________________________

# AppComponent

Every Angular application begins here.

```typescript
@Component({

    selector: "app-root",

    templateUrl:

    "./app.component.html"

})

export class AppComponent {

}
```

Think of it as

```
Main Component
```

______________________________________________________________________

# Component Tree

Angular applications are trees of components.

Example

```
AppComponent

├── NavbarComponent

├── SidebarComponent

├── DashboardComponent

│

├── UserCardComponent

├── ChartComponent

└── FooterComponent
```

Every box is an Angular component.

______________________________________________________________________

# What is a Component?

A component controls a small part of the UI.

Example

```
Login Form

Profile Card

Navigation Bar

Dashboard

Product List

Shopping Cart
```

Everything is a component.

______________________________________________________________________

# Component Anatomy

Every component has

```
TypeScript

↓

Logic
```

```
HTML

↓

Template
```

```
CSS

↓

Styling
```

Together they create one reusable UI element.

______________________________________________________________________

# Example

```
UserCardComponent

├── user-card.component.ts

├── user-card.component.html

└── user-card.component.css
```

One feature.

Three files.

______________________________________________________________________

# Standalone Components

Modern Angular applications commonly use

```
Standalone Components
```

instead of the older NgModule-based approach.

Example

```typescript
@Component({

    standalone: true,

    selector: "app-user"

})
```

Standalone components reduce boilerplate and simplify project structure.

______________________________________________________________________

# Angular CLI

CLI

\=

Command Line Interface

Install

```bash
npm install -g @angular/cli
```

Check version

```bash
ng version
```

______________________________________________________________________

# Create Project

```bash
ng new employee-app
```

CLI automatically creates

- Folder structure
- Configuration
- TypeScript setup
- Build configuration

______________________________________________________________________

# Run Application

```bash
cd employee-app

ng serve
```

Output

```
http://localhost:4200
```

Open the browser,

Angular is running.

______________________________________________________________________

# Development Server

```
ng serve
```

starts a local development server.

Features

- Auto compilation
- Hot Reload
- Error reporting

______________________________________________________________________

# Hot Reload

Suppose you edit

```
app.component.html
```

Angular recompiles

↓

Browser refreshes automatically.

No manual reload required.

______________________________________________________________________

# Build Process

Development

```
TypeScript

↓

Angular Compiler

↓

JavaScript

↓

Browser
```

______________________________________________________________________

Production

```
ng build

↓

Optimization

↓

Minification

↓

Bundle

↓

Deployment
```

______________________________________________________________________

# angular.json

Main configuration file.

Contains

- Build configuration
- Assets
- Styles
- Scripts
- Output folder

You usually modify it only occasionally.

______________________________________________________________________

# package.json

Contains

- Dependencies
- Scripts
- Angular packages

Example

```json
{

"scripts": {

"start":

"ng serve",

"build":

"ng build"

}

}
```

______________________________________________________________________

# node_modules

Contains downloaded packages.

Never edit manually.

Never commit to Git.

______________________________________________________________________

# TypeScript Configuration

```
tsconfig.json
```

Controls

- Strict mode
- Compiler options
- Module resolution
- Output configuration

______________________________________________________________________

# Angular Packages

You'll often see

```
@angular/core

@angular/common

@angular/router

@angular/forms

@angular/common/http
```

Each package provides specific functionality.

______________________________________________________________________

# Angular Lifecycle (High Level)

```
Browser Opens

↓

Angular Starts

↓

AppComponent

↓

Load Components

↓

Render UI

↓

User Interaction

↓

HTTP Calls

↓

Update UI
```

______________________________________________________________________

# Communication with Backend

Angular does not connect to databases.

Instead

```
Angular

↓

HttpClient

↓

REST API

↓

Backend

↓

Database
```

Exactly the architecture we discussed in the previous chapter.

______________________________________________________________________

# Typical Enterprise Architecture

```
Browser

↓

Angular

↓

REST API

↓

Authentication

↓

Business Logic

↓

Database
```

Angular focuses only on the frontend.

______________________________________________________________________

# Common Mistakes

## Thinking Angular is a Library

Angular is a complete framework.

It includes routing, dependency injection, forms, HTTP client, testing tools, and much more.

______________________________________________________________________

## Thinking Every Component is a Page

Not true.

A page can contain dozens of reusable components.

______________________________________________________________________

## Editing node_modules

Never modify packages inside

```
node_modules
```

______________________________________________________________________

## Thinking Angular Communicates Directly with Database

Angular communicates only with backend APIs.

______________________________________________________________________

# Best Practices

✅ Keep components small and reusable.

✅ Let Angular CLI generate project structure.

✅ Keep business logic inside services.

✅ Use standalone components for new applications.

✅ Treat Angular as the frontend only.

______________________________________________________________________

# Interview Deep Dive

## Question

What is Angular?

### Answer

Angular is a TypeScript-based frontend framework developed by Google for building Single Page Applications. It provides
built-in support for components, routing, dependency injection, HTTP communication, forms, and other features required
for enterprise applications.

______________________________________________________________________

## Question

Why is Angular called a framework rather than a library?

### Answer

Angular provides a complete application architecture, including routing, dependency injection, forms, HTTP client, build
tools, and testing support. Unlike a library that solves one problem, Angular offers an integrated solution for building
entire applications.

______________________________________________________________________

## Question

What is Angular CLI?

### Answer

Angular CLI is the official command-line tool used to create, build, test, and serve Angular applications. It automates
project setup and common development tasks.

______________________________________________________________________

## Question

What is the role of `main.ts`?

### Answer

`main.ts` is the application's entry point. It bootstraps the root Angular component, which starts the application.

______________________________________________________________________

## Question

What is a component?

### Answer

A component is the basic building block of an Angular application. It combines TypeScript logic, an HTML template, and
optional CSS styles to control a specific part of the user interface.

______________________________________________________________________

# Practice Questions

1. What is Angular?
1. Why was Angular created?
1. Why is Angular considered a framework?
1. What are the major building blocks of Angular?
1. What is Angular CLI?
1. What is the purpose of `main.ts`?
1. What is `AppComponent`?
1. What is a standalone component?
1. What is the role of `angular.json`?
1. Explain how an Angular application starts from browser launch to rendering the first screen.

______________________________________________________________________

# Summary

Angular is a complete frontend framework designed for building large, maintainable Single Page Applications.

In this chapter, you learned:

- What Angular is
- Why Angular exists
- Angular vs AngularJS
- Angular architecture
- Components
- Standalone components
- Angular CLI
- Project structure
- `main.ts`
- `AppComponent`
- Build process
- Development server
- Angular packages
- Enterprise architecture

Now that you understand the overall architecture, the next step is learning the **TypeScript concepts used specifically
in Angular**, which will make reading Angular code much easier.

______________________________________________________________________

# Next

[TypeScript for Angular](04-typescript-for-angular.md)
