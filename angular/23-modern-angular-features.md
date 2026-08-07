# Modern Angular Features (Signals Deep Dive)

> **Target Version:** Angular 20+
>
> This chapter focuses on the modern Angular APIs introduced from Angular 16 onwards and expanded in Angular 17–20. These APIs represent the future direction of Angular development.

______________________________________________________________________

# Why Modern Angular?

Early Angular applications relied heavily on

- NgModules
- Zone.js
- RxJS for almost everything
- `*ngIf`
- `*ngFor`
- Constructor Injection

Modern Angular is

- Simpler
- Faster
- More reactive
- Easier to learn
- Less boilerplate

______________________________________________________________________

# Angular Evolution

```
Angular 2

↓

NgModules

↓

Angular 9

↓

Ivy

↓

Angular 14

↓

Standalone APIs

↓

Angular 16

↓

Signals

↓

Angular 17

↓

@if

@for

↓

Angular 18+

↓

Better SSR

↓

Angular 19+

↓

Improved Signals

↓

Angular 20+

↓

Signal-first Architecture
```

______________________________________________________________________

# Standalone Components

Before

```
Component

↓

NgModule

↓

Application
```

Now

```
Component

↓

Application
```

No module required.

______________________________________________________________________

Example

```typescript
@Component({

standalone:true,

selector:"app-user",

templateUrl:"user.html"

})
```

Much simpler.

______________________________________________________________________

# Standalone Bootstrap

Old

```typescript
platformBrowserDynamic()

.bootstrapModule(

AppModule

);
```

Modern

```typescript
bootstrapApplication(

AppComponent
);
```

______________________________________________________________________

# Standalone Routing

Old

```typescript
RouterModule.forRoot(...)
```

Modern

```typescript
provideRouter(

routes
)
```

______________________________________________________________________

# Standalone HTTP

Old

```typescript
HttpClientModule
```

Modern

```typescript
provideHttpClient()
```

______________________________________________________________________

# Functional Providers

Instead of

```
Modules
```

Angular now uses

```
Providers
```

Example

```typescript
providers:[

provideRouter(),

provideHttpClient()

]
```

______________________________________________________________________

# inject()

Instead of constructor injection

```typescript
constructor(

private service:

UserService

){}
```

Modern

```typescript
const service =

inject(

UserService

);
```

Useful in

- Functional Guards
- Functional Interceptors
- Utility functions
- Components
- Services

______________________________________________________________________

# Why inject()?

Allows

Dependency Injection

outside constructors.

Less boilerplate.

______________________________________________________________________

# Signals

One of the biggest additions

to Angular.

Create

```typescript
count =

signal(0);
```

Read

```typescript
count()
```

Update

```typescript
count.set(1);
```

______________________________________________________________________

# Signal Flow

```
Signal Changes

↓

Angular Knows

↓

Update UI
```

Unlike traditional change detection,

Angular knows exactly

what changed.

______________________________________________________________________

# Writable Signal

```typescript
const user =

signal<User | null>(

null

);
```

Update

```typescript
user.set(

newUser

);
```

______________________________________________________________________

# update()

Instead of

```typescript
count.set(

count()+1

);
```

Use

```typescript
count.update(

value =>

value + 1

);
```

Cleaner.

______________________________________________________________________

# mutate()

Earlier Signal APIs included mutation helpers, but modern Angular encourages immutable updates using `set()` and
`update()`.

Example

```typescript
users.update(

list => [

...list,

newUser

]

);
```

Prefer immutable updates.

______________________________________________________________________

# Computed Signals

Derived state.

Example

```typescript
price = signal(100);

tax = signal(18);

total = computed(

() =>

price()+tax()

);
```

Whenever

price changes

↓

total updates automatically.

______________________________________________________________________

# Computed Flow

```
Price

↓

Computed

↓

Total
```

Automatic.

______________________________________________________________________

# Effect

Effects execute

when signals change.

```typescript
effect(() => {

console.log(

count()

);

});
```

______________________________________________________________________

# Effect Flow

```
Signal

↓

Effect

↓

Side Effect
```

Examples

- Logging
- Analytics
- Local Storage
- Sync

Avoid business logic.

______________________________________________________________________

# Signal Input

Traditional

```typescript
@Input()

user!:User;
```

Modern Angular supports signal-based inputs.

```typescript
user = input<User>();
```

Read

```typescript
user()
```

______________________________________________________________________

# Signal Output

Angular still primarily uses

```
output()
```

for modern output declarations.

Example

```typescript
saved = output<User>();
```

Emit

```typescript
saved.emit(

user

);
```

Cleaner API.

______________________________________________________________________

# Model Inputs

Angular also provides

```
model()
```

for writable component inputs,

enabling cleaner two-way binding.

______________________________________________________________________

# Linked Signals

Signals

can depend

on

other signals.

```
Signal

↓

Computed

↓

Another Computed

↓

UI
```

Angular tracks

dependencies automatically.

______________________________________________________________________

# Resources

Modern Angular introduces

```
resource()
```

for asynchronous data.

Conceptually

```
Signal

↓

HTTP

↓

Loading

↓

Data

↓

Error
```

Resources simplify

async state management.

______________________________________________________________________

# Signals vs RxJS

| Signals | RxJS |
|-----------|------|
| UI State | Async Streams |
| Simpler | Powerful Operators |
| Synchronous | Asynchronous |
| Built into Angular | External Library |

______________________________________________________________________

# When To Use Signals

Good

- UI State
- Counters
- Theme
- Selected Item
- Form UI State
- Visibility

______________________________________________________________________

# When To Use RxJS

Good

- HTTP
- WebSockets
- Search
- Streaming Data
- Event Streams
- Complex Async Logic

______________________________________________________________________

# Signals + RxJS

Most enterprise apps

use both.

```
Backend

↓

Observable

↓

Signal

↓

UI
```

They complement each other.

______________________________________________________________________

# Signal Interop

Angular provides helper APIs to convert between Observables and Signals.

Typical flow

```
Observable

↓

Signal

↓

Template
```

This allows gradual migration.

______________________________________________________________________

# @if

Old

```html
*ngIf
```

Modern

```html
@if (

loggedIn

){

<h1>

Welcome

</h1>

}
```

Cleaner.

______________________________________________________________________

# @for

Old

```html
*ngFor
```

Modern

```html
@for (

user of users;

track user.id

){

}
```

______________________________________________________________________

# @switch

Old

```html
*ngSwitch
```

Modern

```html
@switch(

status

){

@case("SUCCESS"){

}

@default{

}

}
```

______________________________________________________________________

# @defer

Huge feature.

Example

```html
@defer {

<app-chart/>

}
```

Angular loads

the component

later.

Improves startup.

______________________________________________________________________

# Deferred Loading

```
Application Starts

↓

Small Bundle

↓

Later

↓

Load Charts
```

Very useful.

______________________________________________________________________

# Functional Guards

Old

```typescript
class AuthGuard
```

Modern

```typescript
export const authGuard=

() => true;
```

Smaller.

Cleaner.

______________________________________________________________________

# Functional Interceptors

Old

```
Class
```

Modern

```
Function
```

Less boilerplate.

Better tree-shaking.

______________________________________________________________________

# Zoneless Angular

Historically,

Angular relied on

```
Zone.js
```

to detect changes.

Angular now supports

zoneless applications

for improved performance,

especially when combined

with Signals.

______________________________________________________________________

# Hydration

SSR

renders HTML

on the server.

Hydration

allows Angular

to attach

client-side behavior

without rebuilding

the entire page.

______________________________________________________________________

# Server-Side Rendering (SSR)

Flow

```
Server

↓

HTML

↓

Browser

↓

Hydration

↓

Interactive App
```

Better SEO.

Faster first paint.

______________________________________________________________________

# Tree Shaking

Modern Angular

removes

unused code

during production builds.

Smaller bundles.

______________________________________________________________________

# Improved Control Flow

Instead of

```
*ngIf

*ngFor

*ngSwitch
```

Use

```
@if

@for

@switch
```

Cleaner templates.

______________________________________________________________________

# Modern Angular Stack

```
Standalone

↓

Signals

↓

@if

↓

@for

↓

inject()

↓

Functional APIs

↓

SSR

↓

Hydration
```

This is

modern Angular.

______________________________________________________________________

# Migration Strategy

Don't rewrite

everything.

Instead

```
Standalone

↓

Signals

↓

Control Flow

↓

Functional APIs
```

Migrate gradually.

______________________________________________________________________

# Enterprise Adoption

Most new Angular projects

start with

- Standalone Components
- Standalone Routing
- Functional APIs
- Modern Control Flow

Signals

are increasingly adopted,

especially for UI state,

while RxJS remains important

for asynchronous workflows.

______________________________________________________________________

# Common Mistakes

## Replacing RxJS Completely

Signals

are not

a replacement

for every Observable.

______________________________________________________________________

## Using Effects For Business Logic

Effects

should handle

side effects,

not application workflows.

______________________________________________________________________

## Ignoring Immutable Updates

Signals work best

with immutable data.

______________________________________________________________________

## Mixing Old And New Patterns Randomly

Adopt

modern APIs

consistently

where practical.

______________________________________________________________________

# Best Practices

✅ Prefer Standalone Components.

✅ Use `provideRouter()` and `provideHttpClient()`.

✅ Prefer `inject()` where appropriate.

✅ Use Signals for local UI state.

✅ Use Computed Signals for derived values.

✅ Use Effects only for side effects.

✅ Continue using RxJS for async streams.

✅ Prefer `@if`, `@for`, `@switch`, and `@defer`.

______________________________________________________________________

# Interview Deep Dive

## Question

What are Signals?

### Answer

Signals are Angular's built-in reactive primitives that store state and automatically notify Angular when their values
change, enabling fine-grained UI updates with a simple API.

______________________________________________________________________

## Question

What is the difference between Signals and RxJS?

### Answer

Signals are designed for synchronous UI state, while RxJS is designed for asynchronous data streams and event
composition. In enterprise Angular applications, both are commonly used together.

______________________________________________________________________

## Question

What are Standalone Components?

### Answer

Standalone Components remove the need for NgModules by allowing components to declare their own dependencies and be
bootstrapped directly.

______________________________________________________________________

## Question

Why was `inject()` introduced?

### Answer

`inject()` enables dependency injection outside constructors, making functional guards, interceptors, and other modern
Angular APIs simpler and more flexible.

______________________________________________________________________

## Question

What are the new template control flow blocks?

### Answer

Modern Angular replaces `*ngIf`, `*ngFor`, and `*ngSwitch` with the more readable `@if`, `@for`, and `@switch` syntax.

______________________________________________________________________

# Practice Questions

1. What are Standalone Components?
1. What is `bootstrapApplication()`?
1. What is `inject()`?
1. What are Signals?
1. What is the difference between `set()` and `update()`?
1. What is a Computed Signal?
1. What is an Effect?
1. When should Signals be used instead of RxJS?
1. What is `@defer`?
1. What are the benefits of the new control flow syntax?

______________________________________________________________________

# Summary

Modern Angular focuses on reducing boilerplate, improving performance, and making reactive programming simpler.

In this chapter, you learned:

- Standalone Components
- Standalone bootstrap
- Functional providers
- `inject()`
- Signals
- Writable Signals
- `set()` and `update()`
- Computed Signals
- Effects
- Signal inputs and outputs
- Resources
- Signals vs RxJS
- `@if`
- `@for`
- `@switch`
- `@defer`
- Functional Guards
- Functional Interceptors
- Zoneless Angular
- SSR and Hydration
- Migration strategy
- Best practices

You now have a strong understanding of Angular's modern development model. The next chapter explains how to migrate
legacy Angular applications that use NgModules and older APIs to the modern Standalone, Signal-first approach.

______________________________________________________________________

# Next

[Angular Migration Guide](24-angular-migration-guide.md)
