# Components

Components are the **heart of Angular**.

Everything you see on an Angular page is made of one or more components.

If you've worked with Spring Boot or FastAPI, think of components as the **frontend equivalent of controllers**, except
instead of returning JSON, they control a portion of the user interface.

______________________________________________________________________

# What is a Component?

A component is a reusable piece of UI that contains

- HTML (Template)
- TypeScript (Logic)
- CSS (Styling)

Together they represent one part of the application.

______________________________________________________________________

# Real World Example

Imagine Amazon.

```
Amazon Page

├── Header

├── Search Bar

├── Navigation Menu

├── Product List

│   ├── Product Card
│   ├── Product Card
│   └── Product Card

├── Shopping Cart

└── Footer
```

Each box can be an Angular component.

______________________________________________________________________

# Component Based Architecture

Instead of writing one huge HTML page,

Angular breaks everything into small reusable components.

```
Application

↓

Components

↓

Smaller Components

↓

Reusable UI
```

______________________________________________________________________

# Why Components?

Without components

```
home.html

↓

5000 Lines
```

Very difficult to maintain.

With components

```
Home

├── Header

├── Sidebar

├── Dashboard

├── User Table

└── Footer
```

Each component has a single responsibility.

______________________________________________________________________

# Component Anatomy

A component consists of three parts.

```
TypeScript

↓

Business/UI Logic
```

```
HTML

↓

Template
```

```
CSS

↓

Styles
```

______________________________________________________________________

# Example Component

```
user.component.ts

user.component.html

user.component.css
```

Three files.

One component.

______________________________________________________________________

# Component Decorator

Every component starts with

```typescript
@Component({

})
```

Example

```typescript
import {

    Component

}

from "@angular/core";

@Component({

    selector: "app-user",

    templateUrl:

    "./user.component.html",

    styleUrls: [

        "./user.component.css"

    ]

})

export class UserComponent {

}
```

______________________________________________________________________

# What Does @Component Do?

It tells Angular

```
This Class

↓

Is a Component
```

Angular reads the metadata

and knows

- HTML file
- CSS file
- Selector

______________________________________________________________________

# Component Metadata

```typescript
@Component({

    selector: "app-user",

    templateUrl:

    "./user.component.html",

    styleUrls: [

        "./user.component.css"

    ]

})
```

Meaning

| Property | Purpose |
|----------|----------|
| selector | HTML tag name |
| templateUrl | HTML template |
| styleUrls | CSS styles |

______________________________________________________________________

# Selector

Example

```typescript
selector:

"app-user"
```

Usage

```html
<app-user></app-user>
```

Angular replaces this tag with the component.

______________________________________________________________________

# Component Lifecycle

High-level lifecycle

```
Create Component

↓

Initialize

↓

Render

↓

User Interaction

↓

Destroy
```

Angular manages this automatically.

We'll study lifecycle hooks later.

______________________________________________________________________

# Root Component

Every application starts from

```
AppComponent
```

```
Browser

↓

main.ts

↓

AppComponent

↓

Other Components
```

Everything grows from the root component.

______________________________________________________________________

# Component Tree

Large applications become trees.

```
AppComponent

├── NavbarComponent

├── SidebarComponent

├── DashboardComponent

│   ├── ChartComponent
│   ├── UserTableComponent
│   └── NotificationComponent

└── FooterComponent
```

This hierarchy is called the

```
Component Tree
```

______________________________________________________________________

# Creating Components

Using Angular CLI

```bash
ng generate component users
```

or

```bash
ng g c users
```

CLI creates

```
users/

├── users.component.ts

├── users.component.html

├── users.component.css

└── users.component.spec.ts
```

______________________________________________________________________

# Standalone Components

Modern Angular encourages

```
Standalone Components
```

Example

```typescript
@Component({

    standalone: true,

    selector: "app-users",

    templateUrl:

    "./users.component.html"

})
```

Benefits

- Less boilerplate
- Simpler architecture
- No NgModule required

______________________________________________________________________

# Component Class

Example

```typescript
export class UserComponent {

    title = "Users";

}
```

The class contains

- Variables
- Methods
- Business logic
- API calls

______________________________________________________________________

# Component Template

HTML

```html
<h1>

Users

</h1>
```

Angular combines

```
HTML

+

TypeScript
```

to generate the final UI.

______________________________________________________________________

# Component Styles

Example

```css
h1 {

    color: blue;

}
```

Styles apply only to this component by default.

This is called

```
Style Encapsulation
```

______________________________________________________________________

# Component Communication

Components rarely work alone.

Example

```
Dashboard

↓

User Table

↓

User Card
```

Components communicate with each other.

There are two common directions.

______________________________________________________________________

# Parent → Child

```
Dashboard

↓

User Table
```

Parent passes data to child.

Angular uses

```
@Input()
```

We'll cover this in detail later.

______________________________________________________________________

# Child → Parent

```
User Table

↓

Dashboard
```

Child notifies parent.

Angular uses

```
@Output()
```

We'll study this later.

______________________________________________________________________

# Smart Components

Also called

```
Container Components
```

Responsibilities

- API calls
- Business logic
- State management

Example

```
DashboardComponent
```

______________________________________________________________________

# Dumb Components

Also called

```
Presentational Components
```

Responsibilities

- Display UI
- Receive data
- Emit events

Example

```
UserCardComponent
```

They should not directly call APIs.

______________________________________________________________________

# Reusable Components

Instead of copying HTML,

create reusable components.

Example

```
Product Card

↓

Reuse 100 Times
```

Instead of

```
100 HTML Copies
```

______________________________________________________________________

# Component Example

```
Dashboard

↓

User Card

↓

Name

↓

Image

↓

Role
```

One component,

many users.

______________________________________________________________________

# Component Folder Structure

Example

```
app/

├── components/

│   ├── navbar/

│   ├── footer/

│   ├── sidebar/

│   └── user-card/

├── pages/

└── services/
```

A common enterprise structure.

______________________________________________________________________

# Component Naming

Good

```
UserCardComponent

NavbarComponent

ProductTableComponent
```

Avoid

```
TestComponent

TempComponent

Component1
```

Names should describe responsibility.

______________________________________________________________________

# Component Responsibility

Good

```
UserCard

↓

Displays User
```

Bad

```
UserCard

↓

Displays User

↓

Calls APIs

↓

Authentication

↓

Payment

↓

Reports
```

Keep components focused.

______________________________________________________________________

# Backend Comparison

Spring Boot

```
Controller

↓

Returns JSON
```

Angular

```
Component

↓

Displays UI
```

Services perform business logic in both worlds.

______________________________________________________________________

# Component vs Service

| Component | Service |
|-----------|----------|
| Controls UI | Business logic |
| Displays data | Fetches/manages data |
| Handles user interaction | Reusable logic |
| Has HTML | No HTML |

A component should **use** a service instead of implementing complex logic itself.

______________________________________________________________________

# Complete Flow

```
User Click

↓

Component

↓

Service

↓

HttpClient

↓

Backend API

↓

JSON

↓

Service

↓

Component

↓

Update UI
```

This is one of the most common flows in Angular.

______________________________________________________________________

# Common Mistakes

## Huge Components

Wrong

```
Component

↓

1000 Lines
```

Split into smaller components.

______________________________________________________________________

## Calling Backend Everywhere

Bad

```
Every Component

↓

HttpClient
```

Prefer

```
Component

↓

Service

↓

HttpClient
```

______________________________________________________________________

## Duplicate UI

If the same UI appears multiple times,

create a reusable component.

______________________________________________________________________

## Putting Business Logic in Components

Components should focus on presentation and user interaction.

Move reusable business logic into services.

______________________________________________________________________

# Best Practices

✅ Build small reusable components.

✅ Give each component one responsibility.

✅ Keep business logic in services.

✅ Prefer standalone components for new projects.

✅ Organize components into feature folders.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a component in Angular?

### Answer

A component is the basic building block of an Angular application. It combines TypeScript logic, an HTML template, and
CSS styles to control a specific part of the user interface.

______________________________________________________________________

## Question

What is the purpose of the `@Component` decorator?

### Answer

The `@Component` decorator provides metadata that tells Angular how to create and render a component, including its
selector, template, and styles.

______________________________________________________________________

## Question

What is the role of a selector?

### Answer

A selector defines the custom HTML tag used to place a component inside another component's template. Angular replaces
that tag with the component's rendered output.

______________________________________________________________________

## Question

Why should components remain small?

### Answer

Small components are easier to understand, test, reuse, and maintain. Each component should have a single
responsibility.

______________________________________________________________________

## Question

What is the difference between a component and a service?

### Answer

A component manages the user interface and user interactions, while a service contains reusable business logic, data
access, or shared functionality that can be used by multiple components.

______________________________________________________________________

# Practice Questions

1. What is a component?
1. What are the three parts of a component?
1. What does the `@Component` decorator do?
1. What is a selector?
1. What is the component tree?
1. What are standalone components?
1. What is the difference between smart and dumb components?
1. Why should business logic not live inside components?
1. What is the difference between a component and a service?
1. Explain the flow from a button click to updating the UI after an API call.

______________________________________________________________________

# Summary

Components are the foundation of every Angular application.

In this chapter, you learned:

- What a component is
- Component-based architecture
- Component anatomy
- `@Component` decorator
- Metadata
- Selectors
- Component tree
- Root component
- Standalone components
- Parent and child components
- Smart vs dumb components
- Reusable components
- Component vs service
- Best practices

Now that you know how Angular organizes the UI into components, the next step is learning **how components display data
and respond to user interactions** through templates and data binding.

______________________________________________________________________

# Next

[Templates & Data Binding](06-templates-and-data-binding.md)
