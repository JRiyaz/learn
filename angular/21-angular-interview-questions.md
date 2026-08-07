# Angular Interview Questions

Congratulations!

By this point, you've learned nearly everything needed to build enterprise Angular applications.

This chapter focuses on the kinds of questions commonly asked in Angular interviews, along with concise,
production-oriented answers.

______________________________________________________________________

# Angular Basics

## Question

What is Angular?

### Answer

Angular is a TypeScript-based frontend framework developed by Google for building Single Page Applications (SPAs). It
provides built-in features such as components, routing, dependency injection, forms, HTTP communication, and testing
support.

______________________________________________________________________

## Question

Why is Angular called a framework instead of a library?

### Answer

Angular is a complete framework because it provides an opinionated architecture and built-in solutions for routing,
dependency injection, forms, HTTP, compilation, and testing. A library typically focuses on solving one problem.

______________________________________________________________________

## Question

What is a Single Page Application?

### Answer

A Single Page Application loads one HTML page initially and dynamically updates the displayed content without performing
full page reloads.

______________________________________________________________________

## Question

What is Angular CLI?

### Answer

Angular CLI is the official command-line tool for creating, building, testing, and serving Angular applications.

______________________________________________________________________

# Components

## Question

What is a Component?

### Answer

A Component is the fundamental building block of an Angular application. It controls a portion of the user interface
using TypeScript, HTML, and CSS.

______________________________________________________________________

## Question

What does the `@Component` decorator do?

### Answer

The `@Component` decorator provides metadata that tells Angular how to create and render a component, including its
selector, template, styles, and configuration.

______________________________________________________________________

## Question

What is a selector?

### Answer

A selector defines the custom HTML tag that Angular uses to render a component.

Example

```html
<app-users></app-users>
```

______________________________________________________________________

## Question

What is the difference between smart and dumb components?

### Answer

Smart components contain business logic, API calls, and state management.

Dumb components receive data through inputs, emit events through outputs, and focus only on presentation.

______________________________________________________________________

# Data Binding

## Question

What are the four types of data binding?

### Answer

- Interpolation (`{{ }}`)
- Property Binding (`[]`)
- Event Binding (`()`)
- Two-way Binding (`[()]`)

______________________________________________________________________

## Question

What is interpolation?

### Answer

Interpolation displays component data inside templates using

```html
{{ value }}
```

______________________________________________________________________

## Question

What is property binding?

### Answer

Property binding sends data from the component to an HTML element or another component.

Example

```html
<img [src]="imageUrl">
```

______________________________________________________________________

## Question

What is event binding?

### Answer

Event binding allows templates to notify the component when a user interaction occurs.

Example

```html
<button (click)="save()">
```

______________________________________________________________________

## Question

What is two-way binding?

### Answer

Two-way binding synchronizes data between the component and the template using `[(ngModel)]`.

______________________________________________________________________

# Directives

## Question

What is a directive?

### Answer

A directive changes the behavior or structure of HTML elements.

______________________________________________________________________

## Question

What are the types of directives?

### Answer

- Components
- Structural Directives
- Attribute Directives

______________________________________________________________________

## Question

What is the difference between structural and attribute directives?

### Answer

Structural directives modify the DOM structure by adding or removing elements, while attribute directives modify the
behavior or appearance of existing elements.

______________________________________________________________________

## Question

What are the modern alternatives to `*ngIf` and `*ngFor`?

### Answer

Modern Angular uses

- `@if`
- `@for`
- `@switch`

______________________________________________________________________

# Services & Dependency Injection

## Question

What is a service?

### Answer

A service is a reusable class that contains business logic, shared functionality, state management, or API
communication.

______________________________________________________________________

## Question

What is Dependency Injection?

### Answer

Dependency Injection is a design pattern where Angular creates and supplies required objects instead of components
creating them manually.

______________________________________________________________________

## Question

Why should services be injected instead of created using `new`?

### Answer

Using Dependency Injection reduces coupling, improves testability, centralizes lifecycle management, and allows Angular
to manage dependencies.

______________________________________________________________________

## Question

What does `providedIn: 'root'` mean?

### Answer

It registers the service with Angular's root injector, creating a singleton instance shared throughout the application.

______________________________________________________________________

## Question

What is the difference between constructor injection and `inject()`?

### Answer

Constructor injection is the traditional approach for components and services. `inject()` is a newer API commonly used
in functional guards, interceptors, and other modern Angular APIs.

______________________________________________________________________

# Routing

## Question

What is Angular Routing?

### Answer

Angular Routing maps URLs to components and allows navigation without reloading the browser.

______________________________________________________________________

## Question

What is `router-outlet`?

### Answer

`router-outlet` is the placeholder where Angular renders the component associated with the current route.

______________________________________________________________________

## Question

Why should `routerLink` be used instead of `href`?

### Answer

`routerLink` performs client-side navigation without a full page reload, while `href` causes the browser to reload the
page.

______________________________________________________________________

## Question

What is lazy loading?

### Answer

Lazy loading delays downloading feature code until it is needed, reducing the application's initial bundle size.

______________________________________________________________________

## Question

What are route guards?

### Answer

Route guards determine whether navigation to a route should be allowed.

______________________________________________________________________

# HttpClient

## Question

What is HttpClient?

### Answer

HttpClient is Angular's built-in service for making HTTP requests to backend APIs.

______________________________________________________________________

## Question

Which HTTP methods does HttpClient support?

### Answer

- GET
- POST
- PUT
- PATCH
- DELETE

______________________________________________________________________

## Question

Why does HttpClient return an Observable?

### Answer

Observables support lazy execution, cancellation, multiple emissions, and integration with RxJS operators, making them
well suited for Angular applications.

______________________________________________________________________

## Question

What is an HTTP Interceptor?

### Answer

An HTTP Interceptor can inspect or modify every HTTP request and response. It is commonly used for authentication,
logging, and centralized error handling.

______________________________________________________________________

# RxJS

## Question

What is an Observable?

### Answer

An Observable is a lazy data stream that emits values over time.

______________________________________________________________________

## Question

What is the difference between a Promise and an Observable?

### Answer

Promises produce one value and cannot be cancelled. Observables are lazy, can emit multiple values, support
cancellation, and provide powerful composition through RxJS operators.

______________________________________________________________________

## Question

What is a BehaviorSubject?

### Answer

A BehaviorSubject stores the latest value and immediately emits it to new subscribers.

______________________________________________________________________

## Question

When should `switchMap()` be used?

### Answer

`switchMap()` is used when only the latest request matters, such as search or autocomplete, because it cancels previous
requests.

______________________________________________________________________

## Question

Why should the AsyncPipe be preferred?

### Answer

AsyncPipe automatically subscribes, updates the UI, and unsubscribes when the component is destroyed, reducing
boilerplate and preventing memory leaks.

______________________________________________________________________

# Authentication

## Question

What is the difference between Authentication and Authorization?

### Answer

Authentication verifies who the user is, while authorization determines what actions the authenticated user is allowed
to perform.

______________________________________________________________________

## Question

What is JWT?

### Answer

JWT (JSON Web Token) is a signed token used by the backend to identify authenticated users.

______________________________________________________________________

## Question

Why are refresh tokens used?

### Answer

Refresh tokens allow applications to obtain a new access token without requiring the user to log in again.

______________________________________________________________________

## Question

Why should authorization always be enforced by the backend?

### Answer

Client-side checks can improve the user experience but cannot provide security because users can modify client-side
code.

______________________________________________________________________

# Forms

## Question

What is the difference between Template-driven and Reactive Forms?

### Answer

Template-driven forms define most logic in the template and are suitable for simple forms. Reactive Forms define the
form model in TypeScript and are better for complex validation, dynamic forms, and enterprise applications.

______________________________________________________________________

## Question

Which form approach is preferred in enterprise Angular applications?

### Answer

Reactive Forms are generally preferred because they provide better scalability, testability, and programmatic control.

______________________________________________________________________

# Pipes

## Question

What is a Pipe?

### Answer

A Pipe transforms data for display in Angular templates without modifying the original value.

______________________________________________________________________

## Question

What is the difference between a Pure Pipe and an Impure Pipe?

### Answer

A Pure Pipe executes only when its input reference changes, while an Impure Pipe executes during every change detection
cycle.

______________________________________________________________________

## Question

What is AsyncPipe?

### Answer

AsyncPipe subscribes to Observables or Promises, updates the template automatically, and cleans up subscriptions when
the component is destroyed.

______________________________________________________________________

# Performance

## Question

What is Change Detection?

### Answer

Change Detection is Angular's mechanism for detecting changes in application state and updating the DOM.

______________________________________________________________________

## Question

What is OnPush Change Detection?

### Answer

OnPush reduces unnecessary checks by running change detection only when specific triggers occur, such as input reference
changes, events, or Observable/Signal updates.

______________________________________________________________________

## Question

Why should `track` be used with `@for`?

### Answer

It helps Angular identify which items changed, minimizing DOM updates and improving performance.

______________________________________________________________________

## Question

What are Signals?

### Answer

Signals are Angular's built-in reactive state primitives that enable fine-grained UI updates.

______________________________________________________________________

# Module Federation

## Question

What is Module Federation?

### Answer

Module Federation is a Webpack feature that allows independently built applications to share modules at runtime.

______________________________________________________________________

## Question

What is a Host application?

### Answer

The Host (or Shell) is the main application that loads remote applications.

______________________________________________________________________

## Question

What is a Remote application?

### Answer

A Remote is an independently built and deployed application that exposes modules for the Host to load.

______________________________________________________________________

## Question

How is Module Federation different from Lazy Loading?

### Answer

Lazy Loading splits one application into feature bundles, while Module Federation composes multiple independent
applications at runtime.

______________________________________________________________________

# Architecture

## Question

Why is feature-based architecture preferred?

### Answer

Feature-based architecture groups related components, services, models, and routes together, making large applications
easier to maintain and scale.

______________________________________________________________________

## Question

What belongs in the `core` folder?

### Answer

Application-wide services, authentication, configuration, interceptors, and guards.

______________________________________________________________________

## Question

What belongs in the `shared` folder?

### Answer

Reusable components, directives, pipes, models, and utilities.

______________________________________________________________________

# Coding & Best Practices

## Question

Why should components remain small?

### Answer

Small components are easier to understand, reuse, test, and maintain.

______________________________________________________________________

## Question

Why should business logic be placed in services?

### Answer

Separating business logic from UI logic improves maintainability, reusability, and testability.

______________________________________________________________________

## Question

Why should templates avoid complex logic?

### Answer

Templates are evaluated frequently during change detection. Keeping them simple improves readability and performance.

______________________________________________________________________

## Question

Why should responses be strongly typed?

### Answer

Strong typing improves autocomplete, compile-time error detection, refactoring, and overall code quality.

______________________________________________________________________

# Scenario-Based Questions

## Question

How would you structure a large enterprise Angular application?

### Answer

I would organize the project using feature-based architecture with separate `core`, `shared`, and `features` folders.
Each feature would contain its own components, services, models, and routes. Shared functionality such as
authentication, interceptors, and reusable UI components would be centralized appropriately.

______________________________________________________________________

## Question

How would you optimize a slow Angular application?

### Answer

I would identify unnecessary rendering using Angular DevTools, use `OnPush` where appropriate, add `track` expressions
for lists, lazy load feature modules, use AsyncPipe, optimize large lists with virtual scrolling or pagination, and
minimize unnecessary API calls through caching.

______________________________________________________________________

## Question

How would you share authentication across multiple components?

### Answer

I would create an `AuthService` that maintains the authenticated user state using a shared reactive mechanism (such as a
`BehaviorSubject` or Signals where appropriate), expose that state to components, and use an HTTP interceptor to attach
authentication tokens to outgoing requests.

______________________________________________________________________

## Question

How would you secure an Angular application?

### Answer

I would use route guards to protect navigation, HTTP interceptors to attach authentication tokens, short-lived access
tokens with refresh tokens, validate user input on the client for user experience, and always enforce authentication and
authorization on the backend.

______________________________________________________________________

# Final Interview Tips

✅ Explain **why**, not just **how**.

✅ Mention trade-offs when discussing architecture.

✅ Prefer modern Angular features (`@if`, `@for`, Standalone Components, Signals) while acknowledging legacy patterns.

✅ Keep business logic in services and presentation logic in components and templates.

✅ Demonstrate awareness of performance, maintainability, and scalability.

______________________________________________________________________

# Summary

This chapter reviewed the most frequently asked Angular interview questions across:

- Angular Fundamentals
- Components
- Data Binding
- Directives
- Dependency Injection
- Routing
- HttpClient
- RxJS
- Authentication
- Forms
- Pipes
- Performance
- Module Federation
- Architecture
- Enterprise Best Practices
- Scenario-Based Questions

Mastering these concepts will prepare you for the majority of Angular technical interviews, especially for
backend/full-stack engineering roles.

______________________________________________________________________

# Next

[Angular Cheatsheet](22-angular-cheatsheet.md)
