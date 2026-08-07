# Routing

One of the biggest advantages of Angular is that users can navigate between pages **without reloading the browser**.

This is possible because Angular uses **Client-Side Routing**.

If you've worked with Spring Boot or FastAPI, you'll notice that Angular routing looks similar—but it behaves very
differently.

______________________________________________________________________

# What is Routing?

Routing determines

```
URL

↓

Which Screen

Should Be Displayed
```

Example

```
/home

↓

HomeComponent
```

```
/users

↓

UsersComponent
```

```
/orders

↓

OrdersComponent
```

______________________________________________________________________

# Why Do We Need Routing?

Imagine an application without routing.

```
AppComponent

↓

Everything

↓

Home

↓

Users

↓

Orders

↓

Settings
```

One enormous component.

Very difficult to maintain.

Instead

```
URL

↓

Router

↓

Correct Component
```

______________________________________________________________________

# Traditional Routing

Traditional web applications

```
Browser

↓

GET /users

↓

Backend

↓

Generate HTML

↓

Browser

↓

Reload Page
```

Every navigation reloads the page.

______________________________________________________________________

# Angular Routing

Angular

```
Browser

↓

Angular Router

↓

UsersComponent

↓

Update DOM

↓

Done
```

Notice

```
No Page Reload
```

______________________________________________________________________

# Backend Routing vs Angular Routing

Backend

```
GET /users

↓

Controller

↓

JSON
```

Angular

```
/users

↓

UsersComponent
```

One returns

```
JSON
```

The other renders

```
UI
```

______________________________________________________________________

# Complete Flow

```
Browser

↓

Angular Router

↓

UsersComponent

↓

UserService

↓

Backend API

↓

JSON

↓

UsersComponent

↓

Template

↓

Browser
```

______________________________________________________________________

# Angular Router

Angular provides

```
Angular Router
```

to manage navigation.

You don't manually change HTML pages.

Angular changes components.

______________________________________________________________________

# Route Configuration

Modern Angular uses

```
app.routes.ts
```

Example

```typescript
import {

    Routes

}

from "@angular/router";

import {

    HomeComponent

}

from "./home/home.component";

import {

    UsersComponent

}

from "./users/users.component";

export const routes:

Routes = [

    {

        path: "",

        component:

        HomeComponent

    },

    {

        path: "users",

        component:

        UsersComponent

    }

];
```

______________________________________________________________________

# Route Table

```
URL

↓

Component
```

```
/

↓

HomeComponent
```

```
/users

↓

UsersComponent
```

```
/orders

↓

OrdersComponent
```

______________________________________________________________________

# Bootstrap Routing

Modern Angular

```typescript
bootstrapApplication(

AppComponent,

{

providers:[

provideRouter(

routes

)

]

}

);
```

This registers the router.

______________________________________________________________________

# router-outlet

Where should Angular display components?

Using

```html
<router-outlet>

</router-outlet>
```

Think of it as

```
Placeholder

↓

Current Component
```

______________________________________________________________________

# Example

AppComponent

```html
<h1>

My Application

</h1>

<router-outlet>

</router-outlet>
```

If user visits

```
/users
```

Angular renders

```
UsersComponent
```

inside

```
router-outlet
```

______________________________________________________________________

# Navigation

Angular provides

```html
routerLink
```

Example

```html
<a

routerLink="/users"

>

Users

</a>
```

Instead of

```html
<a

href="/users"

>
```

Use

```
routerLink
```

______________________________________________________________________

# Why Not href?

Using

```html
href
```

causes

```
Full Page Reload
```

Using

```html
routerLink
```

lets Angular handle navigation.

______________________________________________________________________

# Programmatic Navigation

Sometimes navigation happens in code.

Example

```typescript
constructor(

private router:

Router

) {

}
```

Navigate

```typescript
this.router.navigate(

["/users"]

);
```

______________________________________________________________________

# Route Parameters

Suppose URL

```
/users/10
```

Angular Route

```typescript
{

path:

"users/:id",

component:

UserComponent

}
```

______________________________________________________________________

# Reading Parameters

Example

```typescript
constructor(

private route:

ActivatedRoute

) {

}
```

Read parameter

```typescript
const id =

this.route.snapshot

.paramMap

.get("id");
```

Result

```
10
```

______________________________________________________________________

# Route Parameter Flow

```
/users/25

↓

Router

↓

UserComponent

↓

id = 25
```

______________________________________________________________________

# Query Parameters

Example

```
/users?page=2

&size=20
```

Route

```
UsersComponent
```

______________________________________________________________________

Read

```typescript
const page =

this.route.snapshot

.queryParamMap

.get("page");
```

______________________________________________________________________

# Difference

Route Parameter

```
/users/10
```

Usually identifies

```
One Resource
```

______________________________________________________________________

Query Parameter

```
?page=2

&sort=name
```

Usually filters,

sorts,

or paginates.

______________________________________________________________________

# Nested Routes

Large applications often have

```
Dashboard

├── Users

├── Orders

├── Reports
```

Routes

```
/dashboard

/dashboard/users

/dashboard/orders
```

______________________________________________________________________

Example

```typescript
{

path:

"dashboard",

component:

DashboardComponent,

children:[

{

path:"users",

component:

UsersComponent

},

{

path:"orders",

component:

OrdersComponent

}

]

}
```

______________________________________________________________________

# Child router-outlet

Nested routes require

another

```html
<router-outlet>

</router-outlet>
```

inside the parent component.

______________________________________________________________________

# Wildcard Route

Unknown URL

```
/abcxyz
```

Handle using

```typescript
{

path:"**",

component:

NotFoundComponent

}
```

Very common.

______________________________________________________________________

# Redirect Route

Example

```typescript
{

path:"",

redirectTo:"home",

pathMatch:"full"

}
```

User visits

```
/
```

↓

Automatically redirected.

______________________________________________________________________

# Lazy Loading

Suppose application has

```
Dashboard

Admin

Reports

Analytics

Billing
```

Loading everything immediately is slow.

Instead

```
Load

Only

When Needed
```

______________________________________________________________________

# Lazy Loading Flow

```
Application Starts

↓

Home

↓

User Opens Reports

↓

Download Reports Code

↓

Display Reports
```

Smaller initial bundle.

______________________________________________________________________

# Modern Lazy Loading

```typescript
{

path:"users",

loadComponent:()=>

import(

"./users/users.component"

)

.then(

m=>m.UsersComponent

)

}
```

Modern Angular prefers

```
loadComponent()
```

for standalone components.

______________________________________________________________________

# Route Guard

Suppose

```
/admin
```

should require login.

Flow

```
User

↓

Guard

↓

Allowed?

↓

Yes

↓

Component

No

↓

Login
```

______________________________________________________________________

# Modern Functional Guard

Example

```typescript
export const authGuard =

() => {

    return true;

};
```

Later

```typescript
{

path:"admin",

canActivate:[

authGuard

]

}
```

We'll cover authentication later.

______________________________________________________________________

# Resolver

Sometimes

data must be loaded

before the page appears.

```
Route

↓

Resolver

↓

Backend

↓

Data

↓

Component
```

User sees

ready data.

______________________________________________________________________

# Navigation Lifecycle

```
User Click

↓

Router

↓

Guard

↓

Resolver

↓

Component

↓

Template

↓

Browser
```

______________________________________________________________________

# Browser URL

Angular updates

```
URL
```

without refreshing

the page.

Browser still supports

- Back
- Forward
- Bookmark

______________________________________________________________________

# Route Organization

Large projects

```
routes/

app.routes.ts

admin.routes.ts

user.routes.ts

auth.routes.ts
```

Split routes

by feature.

______________________________________________________________________

# Enterprise Example

```
/

↓

Login

↓

Dashboard

↓

Users

↓

User Details

↓

Orders

↓

Reports
```

Each screen

has its own route.

______________________________________________________________________

# Spring Boot Comparison

Spring

```java
@GetMapping(

"/users"

)
```

returns

```
JSON
```

Angular

```typescript
{

path:"users"

}
```

loads

```
UsersComponent
```

______________________________________________________________________

# Common Mistakes

## Using href Instead of routerLink

Wrong

```html
<a href="/users">

Users

</a>
```

Correct

```html
<a

routerLink="/users"

>

Users

</a>
```

______________________________________________________________________

## Forgetting router-outlet

Without

```html
<router-outlet>
```

Angular has nowhere to display routed components.

______________________________________________________________________

## Putting Business Logic in Guards

Guards should decide

```
Can Navigate?
```

Business logic belongs elsewhere.

______________________________________________________________________

## Loading Everything Initially

Use lazy loading

for large applications.

______________________________________________________________________

# Best Practices

✅ Use standalone routing.

✅ Use `routerLink` instead of `href`.

✅ Use lazy loading for feature areas.

✅ Organize routes by feature.

✅ Protect secure pages with guards.

✅ Use wildcard routes for 404 pages.

______________________________________________________________________

# Interview Deep Dive

## Question

What is Angular Routing?

### Answer

Angular Routing is the mechanism that maps URLs to components, allowing users to navigate between views without
reloading the page. It is handled entirely within the browser using the Angular Router.

______________________________________________________________________

## Question

What is the purpose of `router-outlet`?

### Answer

`router-outlet` acts as a placeholder where Angular inserts the component associated with the current route.

______________________________________________________________________

## Question

What is the difference between `routerLink` and `href`?

### Answer

`routerLink` performs client-side navigation without reloading the page, while `href` instructs the browser to request a
new page from the server, causing a full page refresh.

______________________________________________________________________

## Question

What is lazy loading?

### Answer

Lazy loading delays downloading feature code until it is actually needed, reducing the application's initial bundle size
and improving startup performance.

______________________________________________________________________

## Question

What is the difference between route parameters and query parameters?

### Answer

Route parameters identify specific resources, such as `/users/10`, while query parameters provide optional information
such as filtering, sorting, or pagination, for example `/users?page=2`.

______________________________________________________________________

# Practice Questions

1. What is Angular Routing?
1. What is `router-outlet`?
1. Why should `routerLink` be used instead of `href`?
1. What is the purpose of `app.routes.ts`?
1. What are route parameters?
1. What are query parameters?
1. What is lazy loading?
1. What are route guards?
1. What is a resolver?
1. Explain the complete routing lifecycle from clicking a link to displaying a component.

______________________________________________________________________

# Summary

Routing is what makes Angular Single Page Applications feel fast and seamless.

In this chapter, you learned:

- Angular Router
- Route configuration
- `router-outlet`
- `routerLink`
- Programmatic navigation
- Route parameters
- Query parameters
- Nested routes
- Wildcard routes
- Redirects
- Lazy loading
- Functional guards
- Resolvers
- Routing lifecycle
- Modern standalone routing

Routing is one of the most important Angular concepts because almost every enterprise application relies on it. The next
chapter covers **Forms**, where you'll learn how Angular captures, validates, and processes user input using both
Template-Driven Forms and Reactive Forms.

______________________________________________________________________

# Next

[Forms](10-forms.md)
