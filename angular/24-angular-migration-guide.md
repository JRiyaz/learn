# Angular Migration Guide (Legacy → Modern Angular)

> **Target Audience:** Developers maintaining Angular 2–15 applications who want to migrate to modern Angular (v20+).
>
> **Goal:** Understand what changed, why it changed, and how to migrate safely.

______________________________________________________________________

# Why Migrate?

Modern Angular provides

- Less boilerplate
- Better performance
- Simpler APIs
- Better tree shaking
- Better developer experience
- Smaller applications

Migration should be

```
Gradual

NOT

Big Bang
```

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

↓

Angular 20+

↓

Signal-first Development
```

______________________________________________________________________

# Migration Strategy

Do **NOT**

rewrite

the entire application.

Instead

```
Upgrade Angular

↓

Standalone Components

↓

Standalone Routing

↓

Modern Control Flow

↓

Signals

↓

Functional APIs

↓

Performance Improvements
```

Small,

incremental changes.

______________________________________________________________________

# Step 1

## Upgrade Angular Version

Always

upgrade

one major version

at a time.

Avoid

```
Angular 8

↓

Angular 20
```

Instead

```
8

↓

9

↓

10

↓

...

↓

20
```

______________________________________________________________________

# Step 2

## Remove NgModules

Old Angular

```
AppModule

↓

Components

↓

Application
```

Modern Angular

```
Component

↓

Application
```

______________________________________________________________________

# Old

```typescript
@NgModule({

declarations:[

AppComponent

]

})
```

______________________________________________________________________

# Modern

```typescript
@Component({

standalone:true

})
```

______________________________________________________________________

# Bootstrap

Old

```typescript
platformBrowserDynamic()

.bootstrapModule(

AppModule

);
```

______________________________________________________________________

Modern

```typescript
bootstrapApplication(

AppComponent
);
```

Simpler.

______________________________________________________________________

# Step 3

## Replace RouterModule

Old

```typescript
RouterModule

.forRoot(

routes

)
```

Modern

```typescript
provideRouter(

routes
)
```

______________________________________________________________________

# Step 4

## Replace HttpClientModule

Old

```typescript
imports:[

HttpClientModule

]
```

Modern

```typescript
provideHttpClient()
```

______________________________________________________________________

# Step 5

## Replace Constructor Injection

Old

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

Use where appropriate,

especially

functional APIs.

______________________________________________________________________

# Step 6

## Replace Class Guards

Old

```typescript
class AuthGuard

implements

CanActivate
```

Modern

```typescript
export const authGuard=

() => true;
```

Less boilerplate.

______________________________________________________________________

# Step 7

## Replace Class Interceptors

Old

```typescript
class AuthInterceptor
```

Modern

```typescript
export const authInterceptor=

(...)
```

Functional

interceptors.

______________________________________________________________________

# Step 8

## Replace \*ngIf

Old

```html
<div

*ngIf="loggedIn"

>

</div>
```

Modern

```html
@if (

loggedIn

){

<div>

</div>

}
```

Cleaner syntax.

______________________________________________________________________

# Step 9

## Replace \*ngFor

Old

```html
<li

*ngFor="

let user

of users

"

>

</li>
```

Modern

```html
@for (

user of users;

track user.id

){

<li>

</li>

}
```

______________________________________________________________________

# Step 10

## Replace \*ngSwitch

Old

```html
<div

[ngSwitch]

=

status

>
```

Modern

```html
@switch(

status

){

@case("SUCCESS"){

}

}
```

______________________________________________________________________

# Before

```
*ngIf

*ngFor

*ngSwitch
```

______________________________________________________________________

# After

```
@if

@for

@switch
```

______________________________________________________________________

# Step 11

## Introduce Signals

Old

```typescript
counter=0;
```

Modern

```typescript
counter =

signal(0);
```

______________________________________________________________________

Update

Old

```typescript
counter++;
```

Modern

```typescript
counter.update(

v =>

v + 1

);
```

______________________________________________________________________

# Step 12

## Replace Derived Values

Old

```typescript
get total(){

}
```

Modern

```typescript
total = computed(

() =>

price()+tax()

);
```

______________________________________________________________________

# Step 13

## Side Effects

Old

```typescript
ngOnChanges()
```

or

manual subscriptions.

Modern

```typescript
effect(() => {

});
```

Use

only

for side effects.

______________________________________________________________________

# Step 14

## Prefer AsyncPipe

Old

```typescript
subscribe()
```

Template

```html
{{

users$

|

async

}}
```

Cleaner.

Automatic cleanup.

______________________________________________________________________

# Step 15

## Use @defer

Old

```
Everything

Loads

Immediately
```

Modern

```html
@defer {

<heavy-chart/>

}
```

Improved startup.

______________________________________________________________________

# Step 16

## Prefer Standalone Routing

Instead of

```
FeatureModule
```

Create

```
feature.routes.ts
```

Each feature

owns

its own routes.

______________________________________________________________________

# Step 17

## Remove Shared Modules

Old Angular

often contained

```
SharedModule

CoreModule
```

Modern Angular

typically imports

dependencies directly

into standalone components.

> Large projects may still keep shared libraries for reusable code; the migration is about reducing unnecessary NgModule usage, not eliminating shared code.

______________________________________________________________________

# Step 18

## Use provide...

Old

```
imports
```

Modern

```
provideRouter()

provideHttpClient()

provideAnimations()
```

Provider-first configuration.

______________________________________________________________________

# Step 19

## Immutable Updates

Old

```typescript
user.name =

"John";
```

Modern

```typescript
user = {

...user,

name:"John"

};
```

Works better

with Signals

and OnPush.

______________________________________________________________________

# Step 20

## Use track

Old

```html
trackBy
```

Modern

```html
track user.id
```

Simpler.

______________________________________________________________________

# Legacy vs Modern

| Legacy | Modern |
|----------|---------|
| NgModule | Standalone |
| RouterModule | provideRouter |
| HttpClientModule | provideHttpClient |
| Constructor Injection | inject() (where appropriate) |
| \*ngIf | @if |
| \*ngFor | @for |
| \*ngSwitch | @switch |
| Class Guard | Functional Guard |
| Class Interceptor | Functional Interceptor |
| Mutable State | Signals + Immutable Updates |

______________________________________________________________________

# What Should NOT Be Replaced?

Some APIs

are still excellent.

Continue using

```
HttpClient

Reactive Forms

RxJS

Services

Dependency Injection

Routing
```

Modern Angular

builds upon them.

______________________________________________________________________

# Migration Priority

High

```
Standalone

Control Flow

provideRouter

provideHttpClient
```

Medium

```
inject()

Functional APIs

Signals
```

Optional

```
Zoneless

Advanced Signal APIs
```

______________________________________________________________________

# Enterprise Migration

Instead of

```
Rewrite

Entire App
```

Prefer

```
New Feature

↓

Modern Angular

↓

Old Features

↓

Gradually Migrated
```

Lower risk.

______________________________________________________________________

# Migration Flow

```
Upgrade Version

↓

Standalone

↓

Routing

↓

HTTP

↓

Control Flow

↓

Signals

↓

Performance
```

______________________________________________________________________

# Common Mistakes

## Rewriting Everything

Don't.

Incremental migration

is safer.

______________________________________________________________________

## Replacing Every Observable

Signals

do not replace

every Observable.

Keep RxJS

for async streams.

______________________________________________________________________

## Migrating Without Tests

Always

test

before

and after

migration.

______________________________________________________________________

## Ignoring Third-party Libraries

Check

that dependencies

support

your Angular version

before upgrading.

______________________________________________________________________

## Mixing Old and New Randomly

A gradual migration is good,

but adopt modern patterns

consistently

within newly migrated code.

______________________________________________________________________

# Best Practices

✅ Upgrade gradually.

✅ Prefer Standalone Components.

✅ Adopt modern control flow.

✅ Continue using RxJS where appropriate.

✅ Use Signals for UI state.

✅ Test every migration step.

✅ Avoid unnecessary rewrites.

______________________________________________________________________

# Interview Deep Dive

## Question

Why did Angular introduce Standalone Components?

### Answer

Standalone Components reduce boilerplate by removing the need for NgModules, making applications easier to understand,
develop, and tree-shake.

______________________________________________________________________

## Question

Should every Observable be replaced with Signals?

### Answer

No. Signals are ideal for local UI state and derived values, while RxJS remains the preferred solution for asynchronous
streams such as HTTP requests, WebSockets, and complex event handling.

______________________________________________________________________

## Question

What is the biggest migration mistake?

### Answer

Attempting to rewrite an entire application at once. Incremental migration reduces risk and allows teams to validate
changes gradually.

______________________________________________________________________

## Question

Can legacy and modern Angular coexist?

### Answer

Yes. Angular supports gradual adoption, allowing applications to contain both legacy and modern patterns during
migration.

______________________________________________________________________

## Question

Which migration should be done first?

### Answer

Start by upgrading Angular, then adopt Standalone Components and provider-based APIs, followed by modern control flow.
Introduce Signals where they provide clear benefits rather than replacing everything immediately.

______________________________________________________________________

# Practice Questions

1. Why should Angular applications migrate to modern APIs?
1. What replaces NgModules?
1. What replaces `RouterModule.forRoot()`?
1. What replaces `HttpClientModule`?
1. What replaces `*ngIf` and `*ngFor`?
1. Why were Signals introduced?
1. Should Signals replace RxJS?
1. Why should migration be incremental?
1. What are Functional Guards?
1. Describe a safe Angular migration strategy.

______________________________________________________________________

# Summary

Migrating to modern Angular is about simplifying applications while improving performance and maintainability.

In this chapter, you learned:

- Standalone Components
- Provider-based APIs
- Functional Guards
- Functional Interceptors
- Modern template control flow
- Signals
- Immutable updates
- `@defer`
- Migration priorities
- Enterprise migration strategy
- Common migration pitfalls
- Best practices

With the migration complete, you now understand both **legacy Angular** and **modern Angular**. The next chapter
compares **Angular and React**, explaining their philosophies, architectures, ecosystems, and trade-offs to help you
confidently discuss both frameworks in interviews.

______________________________________________________________________

# Next

[Angular vs React](25-angular-vs-react.md)
