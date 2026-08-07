# Single Page Application (SPA)

Before Angular, websites worked very differently.

Understanding **Single Page Applications (SPA)** is one of the most important concepts in frontend development.

Almost every Angular interview starts with one of these questions:

- What is SPA?
- Why was SPA introduced?
- How is it different from a traditional web application?
- How does Angular implement SPA?

This chapter answers all of them.

______________________________________________________________________

# What is a Traditional Web Application?

Before Angular, React, and Vue,

most websites were

```
Multi-Page Applications (MPA)
```

Every navigation requested a **new HTML page** from the server.

______________________________________________________________________

# Traditional Application Flow

Suppose a user visits

```
/home
```

```
Browser

↓

GET /home

↓

Backend

↓

Generate HTML

↓

Browser

↓

Render HTML
```

______________________________________________________________________

User clicks

```
Products
```

Again

```
Browser

↓

GET /products

↓

Backend

↓

Generate HTML

↓

Browser

↓

Entire page reloads
```

Every click reloads the page.

______________________________________________________________________

# Example

Imagine Amazon before SPA.

User opens

```
Home
```

↓

Backend sends HTML.

User clicks

```
Orders
```

↓

Backend generates another HTML page.

User clicks

```
Profile
```

↓

Another HTML page.

Each navigation causes a complete page refresh.

______________________________________________________________________

# Traditional Architecture

```
Browser

↓

GET /

↓

Backend

↓

HTML

↓

Browser

↓

Render

↓

User Click

↓

GET /users

↓

Backend

↓

New HTML

↓

Browser

↓

Entire Page Reload
```

______________________________________________________________________

# Problems with Traditional Applications

Every page navigation

- Downloads new HTML
- Reloads CSS
- Reloads JavaScript
- Recreates the page
- Loses UI state

This leads to

- Slower navigation
- More server work
- Poor user experience

______________________________________________________________________

# Example

Opening

```
Home

↓

Orders

↓

Profile

↓

Settings
```

Means

```
4 HTML Pages

4 Page Reloads

4 Rendering Cycles
```

______________________________________________________________________

# Why Was SPA Introduced?

Developers wanted applications that behaved more like desktop software.

Instead of

```
Reload

Reload

Reload
```

they wanted

```
Update

Update

Update
```

Only the changed content should update.

______________________________________________________________________

# What is a Single Page Application?

A Single Page Application loads **one HTML page** initially.

After that,

JavaScript updates the UI dynamically without reloading the page.

______________________________________________________________________

# SPA Architecture

```
Browser

↓

Load index.html

↓

Load Angular

↓

Angular Starts

↓

User Clicks

↓

API Call

↓

JSON

↓

Update UI
```

Notice

```
No HTML Reload
```

______________________________________________________________________

# Angular SPA Flow

When the application starts

```
Browser

↓

GET /

↓

Backend

↓

index.html

↓

Angular Bundle

↓

Browser

↓

Angular Bootstraps

↓

Application Ready
```

From now on,

Angular controls the UI.

______________________________________________________________________

# Navigation in Angular

User clicks

```
Products
```

Traditional Application

```
GET /products

↓

Backend

↓

HTML
```

Angular

```
Angular Router

↓

Products Component

↓

Update DOM
```

No page refresh.

______________________________________________________________________

# Complete SPA Request Flow

```
User

↓

Browser

↓

Angular

↓

GET /api/products

↓

Backend API

↓

Database

↓

JSON

↓

Angular

↓

Update DOM
```

Backend returns

```
JSON
```

instead of HTML.

______________________________________________________________________

# The Role of index.html

Every Angular application starts with one page.

```
index.html
```

This file usually contains very little HTML.

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

with the entire application.

______________________________________________________________________

# How Angular Starts

```
index.html

↓

main.ts

↓

bootstrapApplication()

↓

AppComponent

↓

Router

↓

Components
```

Everything begins from

```
main.ts
```

______________________________________________________________________

# Client-Side Routing

Traditional Routing

```
Browser

↓

Backend

↓

Controller

↓

HTML
```

Angular Routing

```
Browser

↓

Angular Router

↓

Component
```

This is called

```
Client-side Routing
```

______________________________________________________________________

# Example

User enters

```
/users
```

Angular Router says

```
Load

↓

UsersComponent
```

No request for HTML is made.

______________________________________________________________________

# Backend Routing vs Angular Routing

Backend Route

```
GET /users

↓

Controller

↓

JSON
```

Angular Route

```
/users

↓

UsersComponent
```

These are completely different.

______________________________________________________________________

# Does Angular Still Contact the Backend?

Yes.

But only for

```
Data
```

Example

```
Angular

↓

GET /api/users

↓

Backend

↓

JSON
```

Not

```
HTML
```

______________________________________________________________________

# What Does the Backend Return?

Traditional

```
HTML
```

Angular

```
JSON
```

Example

```json
[
    {
        "id": 1,
        "name": "Alice"
    }
]
```

Angular converts this into UI.

______________________________________________________________________

# Traditional vs SPA

## Traditional

```
Click

↓

Request HTML

↓

Reload Page

↓

Render
```

______________________________________________________________________

## SPA

```
Click

↓

Request JSON

↓

Update Component

↓

Done
```

Much faster.

______________________________________________________________________

# Where Does Angular Run?

Angular always runs inside the browser.

```
Browser

↓

JavaScript Engine

↓

Angular

↓

DOM
```

Backend never executes Angular.

______________________________________________________________________

# Why is SPA Faster?

Initial load

```
Slightly Slower
```

because Angular downloads

- JavaScript
- CSS
- Components

______________________________________________________________________

After loading

```
Navigation

↓

Very Fast
```

because only data changes.

______________________________________________________________________

# Browser History

Angular updates URLs.

Example

```
/users

↓

/orders

↓

/profile
```

The browser still supports

- Back button
- Forward button
- Refresh

because Angular updates the History API.

______________________________________________________________________

# Browser Refresh

Question

If Angular doesn't reload pages,

what happens when the user presses

```
F5
```

Answer

```
Browser

↓

GET /

↓

Backend

↓

index.html

↓

Angular Starts Again
```

The application restarts.

______________________________________________________________________

# Deep Linking

Suppose user opens

```
https://company.com/orders/100
```

Angular Router reads

```
orders/100
```

and loads

```
OrderComponent
```

Deep linking is fully supported.

______________________________________________________________________

# Advantages of SPA

- Fast navigation
- Better user experience
- Desktop-like feel
- Reduced server rendering
- Better separation of frontend and backend
- Reusable APIs
- Rich UI interactions

______________________________________________________________________

# Disadvantages of SPA

- Larger initial download
- JavaScript required
- More frontend complexity
- SEO requires additional techniques
- Routing configuration is more complex

______________________________________________________________________

# SPA and Backend

Backend no longer generates HTML.

Instead,

it becomes an

```
API Server
```

Responsibilities

- Authentication
- Business Logic
- Database
- JSON APIs

______________________________________________________________________

# REST API Example

Angular

```typescript
this.http.get<User[]>(

"/api/users"

);
```

Backend

```json
[
    {
        "id":1,
        "name":"Alice"
    }
]
```

Angular creates the UI.

______________________________________________________________________

# CSR vs SSR

## CSR

Client Side Rendering

```
Browser

↓

Angular

↓

Render UI
```

Default Angular behavior.

______________________________________________________________________

## SSR

Server Side Rendering

```
Browser

↓

Backend

↓

HTML

↓

Browser
```

Angular also supports SSR using **Angular SSR** (formerly Angular Universal).

SSR improves

- SEO
- Initial page load
- Social media previews

______________________________________________________________________

# Hydration (Overview)

With SSR

```
Server

↓

HTML

↓

Browser

↓

Angular Attaches

↓

Interactive Page
```

This process is called

```
Hydration
```

Angular reuses the server-rendered HTML instead of rebuilding it from scratch.

______________________________________________________________________

# SPA vs MPA

| Multi Page Application | Single Page Application |
|-------------------------|--------------------------|
| Multiple HTML pages | One HTML page |
| Page reloads | No page reloads |
| Server renders HTML | Browser renders UI |
| Backend returns HTML | Backend returns JSON |
| Navigation is slower | Navigation is faster |
| Simpler frontend | Rich frontend |
| Server-side routing | Client-side routing |

______________________________________________________________________

# Real-World Examples

Traditional Applications

- Older PHP websites
- JSP applications
- ASP.NET Web Forms
- Older Django applications

______________________________________________________________________

Single Page Applications

- Gmail
- Google Maps
- Netflix
- Facebook
- Twitter (X)
- Jira
- Slack Web
- Most modern Angular applications

______________________________________________________________________

# Common Mistakes

## Thinking Angular Eliminates Backend

Wrong.

Angular still depends heavily on backend APIs.

______________________________________________________________________

## Thinking URLs Always Mean Backend Routes

In Angular,

many URLs are handled entirely by the Angular Router.

______________________________________________________________________

## Thinking SPA Means One Screen

Single Page Application

does **not** mean

one page of content.

It means

one HTML document loaded initially,

with many views managed by JavaScript.

______________________________________________________________________

## Thinking Every Request Returns HTML

Angular applications primarily request

```
JSON
```

not HTML.

______________________________________________________________________

# Best Practices

✅ Keep the frontend responsible for presentation.

✅ Keep business logic on the backend.

✅ Design backend APIs around JSON.

✅ Use Angular Router for navigation.

✅ Avoid unnecessary full page reloads.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a Single Page Application (SPA)?

### Answer

A Single Page Application loads a single HTML page initially. After that, JavaScript dynamically updates the user
interface by communicating with backend APIs, avoiding full page reloads during navigation.

______________________________________________________________________

## Question

How is a SPA different from a traditional web application?

### Answer

Traditional applications request a new HTML page from the server for each navigation. SPAs load one HTML page initially
and then fetch data (typically JSON) from backend APIs while updating only the necessary parts of the page.

______________________________________________________________________

## Question

Why are SPAs generally faster after the initial load?

### Answer

Once the application and its JavaScript bundle are loaded, navigation typically requires only API calls for data instead
of downloading and rendering entirely new HTML pages.

______________________________________________________________________

## Question

Does Angular replace the backend?

### Answer

No. Angular handles the user interface in the browser, while the backend continues to provide authentication, business
logic, database access, and JSON APIs.

______________________________________________________________________

## Question

What is the difference between Angular routing and backend routing?

### Answer

Angular routing maps URLs to frontend components inside the browser. Backend routing maps HTTP requests to server-side
controllers or handlers that process requests and return responses.

______________________________________________________________________

# Practice Questions

1. What is a Single Page Application?
1. Why were SPAs introduced?
1. How does Angular implement a SPA?
1. What is the purpose of `index.html`?
1. What is client-side routing?
1. How does Angular communicate with the backend?
1. Why do Angular applications usually receive JSON instead of HTML?
1. What are the advantages of SPAs?
1. What are the disadvantages of SPAs?
1. Explain the complete lifecycle of an Angular SPA request from browser to backend and back.

______________________________________________________________________

# Summary

Single Page Applications changed how modern web applications are built.

In this chapter, you learned:

- Traditional Multi-Page Applications (MPA)
- Why SPAs were introduced
- SPA architecture
- Angular application lifecycle
- `index.html`
- Angular bootstrapping
- Client-side routing
- Backend routing
- JSON APIs
- CSR vs SSR
- Hydration (overview)
- SPA advantages and disadvantages

Understanding SPA architecture is the foundation for learning Angular. Now that you know **why Angular exists**, the
next step is to understand \*\*what Angular is, how it's organized internally, and how an Angular project is structured.

______________________________________________________________________

# Next

[Angular Overview](03-angular-overview.md)
