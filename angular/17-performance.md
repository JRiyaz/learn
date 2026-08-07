# Performance & Change Detection

Performance is one of the most misunderstood topics in Angular.

Many developers think Angular is "slow."

In reality,

most performance problems come from

- Poor architecture
- Unnecessary rendering
- Inefficient templates
- Incorrect RxJS usage

Modern Angular (v17+) introduced several improvements, including **Signals**, that significantly improve performance.

This chapter explains how Angular updates the UI and how to optimize applications.

______________________________________________________________________

# What is Change Detection?

Angular continuously checks

```
Has Anything Changed?
```

If something changes,

Angular updates the UI.

This process is called

```
Change Detection
```

______________________________________________________________________

# Simple Example

Component

```typescript
counter = 0;
```

Template

```html
{{ counter }}
```

When

```typescript
counter++;
```

Angular automatically updates

```
0

↓

1
```

No manual DOM manipulation.

______________________________________________________________________

# Change Detection Flow

```
User Click

↓

Component State Changes

↓

Angular Detects Changes

↓

DOM Updates
```

______________________________________________________________________

# Why Change Detection Exists

Without Angular

```javascript
document.getElementById(...)

.innerHTML = ...
```

Developers manually update the DOM.

Angular automates this.

______________________________________________________________________

# Component Tree

```
AppComponent

├── Navbar

├── Sidebar

├── Dashboard

│   ├── Chart

│   ├── User Table

│   └── Statistics

└── Footer
```

Angular checks components

during change detection.

______________________________________________________________________

# Default Change Detection

Default strategy

```
User Event

↓

Angular

↓

Checks

EVERY

Component
```

Safe

but may become expensive

for very large applications.

______________________________________________________________________

# ChangeDetectionStrategy

Angular supports

```
Default

OnPush
```

______________________________________________________________________

# Default Strategy

```typescript
@Component({

changeDetection:

ChangeDetectionStrategy.Default

})
```

Angular checks frequently.

Easy to use.

______________________________________________________________________

# OnPush Strategy

```typescript
@Component({

changeDetection:

ChangeDetectionStrategy.OnPush

})
```

Angular performs fewer checks.

Better performance.

______________________________________________________________________

# When Does OnPush Run?

With `OnPush`,

Angular checks the component when

- An `@Input()` reference changes
- An event originates from the component
- An Observable used with the `async` pipe emits
- A Signal used in the template changes
- Change detection is triggered manually

______________________________________________________________________

# Default vs OnPush

| Default | OnPush |
|----------|---------|
| Frequent checks | Fewer checks |
| Simpler | More optimized |
| Good for small apps | Recommended for larger apps when appropriate |

______________________________________________________________________

# Immutability

OnPush works best with immutable data.

Bad

```typescript
user.name =

"John";
```

Good

```typescript
user = {

...user,

name:"John"

};
```

New reference

↓

Angular detects change.

______________________________________________________________________

# Track in @for

Suppose

```
1000 Users
```

Without tracking,

Angular may recreate

many DOM elements.

Modern Angular

```html
@for (

user of users;

track user.id

){

}
```

Angular knows

exactly

which item changed.

______________________________________________________________________

# Legacy trackBy

Older Angular

```html
*ngFor="

let user of users;

trackBy: trackUser
"
```

Modern Angular

prefers

```
track user.id
```

______________________________________________________________________

# Why Tracking Matters

Without track

```
1000 Rows

↓

Change One User

↓

Re-render Many Rows
```

With track

```
1000 Rows

↓

Change One User

↓

Update One Row
```

Huge performance improvement.

______________________________________________________________________

# Signals (Introduction)

Signals are one of the biggest additions to modern Angular.

A Signal is a reactive value.

Example

```typescript
count = signal(0);
```

Read

```typescript
count()
```

Update

```typescript
count.set(10);
```

______________________________________________________________________

# Signal Flow

```
Signal Changes

↓

Angular Knows

↓

Update Only

Affected UI
```

Unlike traditional change detection,

Signals provide fine-grained reactivity.

______________________________________________________________________

# Computed Signal

Derived values.

```typescript
price = signal(100);

tax = signal(18);

total = computed(() =>

price() +

tax()

);
```

Whenever

```
price

OR

tax
```

changes,

Angular recalculates

```
total
```

______________________________________________________________________

# Effect

Run side effects

when signals change.

```typescript
effect(() => {

console.log(

count()

);

});
```

Useful for

- Logging
- Analytics
- Synchronization

Avoid putting business logic inside effects.

______________________________________________________________________

# Signals vs BehaviorSubject

| Signal | BehaviorSubject |
|----------|----------------|
| Built into Angular | RxJS |
| Synchronous state | Observable stream |
| Great for UI state | Great for async streams |
| Simpler API | Rich RxJS operators |

We'll compare them in detail

in the Modern Angular chapter.

______________________________________________________________________

# Signals vs Change Detection

Traditional

```
State Change

↓

Angular Checks Tree
```

Signals

```
Signal Changes

↓

Angular Knows

Exactly

What Changed
```

More efficient.

______________________________________________________________________

# AsyncPipe

Instead of

```typescript
subscribe()
```

Prefer

```html
{{

users$

|

async

}}
```

Benefits

- Automatic subscription
- Automatic cleanup
- Better performance
- Less code

______________________________________________________________________

# Lazy Loading

Don't load

every feature

during startup.

```
Application Starts

↓

Home

↓

User Opens Reports

↓

Download Reports
```

Smaller bundle.

Faster startup.

______________________________________________________________________

# Deferred Loading (@defer)

Modern Angular supports

```html
@defer {

<app-chart/>

}
```

Angular loads the content

only when needed.

Useful for

- Large charts
- Maps
- Heavy dashboards

______________________________________________________________________

# Image Optimization

Avoid

```
5 MB Image
```

Use

- Compressed images
- Lazy loading
- Appropriate formats (WebP, AVIF where supported)

Frontend performance

is not only JavaScript.

______________________________________________________________________

# Virtual Scrolling

Suppose

```
100,000 Rows
```

Don't render

everything.

Instead

```
Viewport

↓

Visible Rows Only
```

Angular CDK provides

Virtual Scrolling.

______________________________________________________________________

# Avoid Heavy Methods

Wrong

```html
{{

calculateTotal()

}}
```

Angular may call it repeatedly.

Better

```typescript
total = 500;
```

Template

```html
{{ total }}
```

______________________________________________________________________

# Memoization

Expensive calculations

should be cached

or derived

using

```
computed()

```

or appropriate caching strategies.

______________________________________________________________________

# Avoid Unnecessary API Calls

Bad

```
Navigate

↓

Reload

↓

Navigate

↓

Reload
```

Good

```
Cache

↓

Reuse
```

______________________________________________________________________

# Memory Leaks

Wrong

```
subscribe()

↓

Never Unsubscribe
```

Better

- AsyncPipe
- takeUntil()
- Angular cleanup APIs

______________________________________________________________________

# Large Lists

Good

```html
@for (

user of users;

track user.id

){

}
```

Bad

Rendering

thousands of DOM nodes

without pagination

or virtualization.

______________________________________________________________________

# Bundle Size

Large bundles

↓

Slow startup.

Optimize by

- Lazy loading
- Tree shaking
- Code splitting
- Removing unused libraries

______________________________________________________________________

# Tree Shaking

Unused code

↓

Removed

during production build.

Angular CLI handles this automatically.

______________________________________________________________________

# Production Build

Development

```bash
ng serve
```

Production

```bash
ng build
```

The production build

- Minifies code
- Optimizes bundles
- Removes dead code

______________________________________________________________________

# Browser Rendering

```
Angular

↓

DOM

↓

Browser

↓

Paint Screen
```

Smaller DOM

means

better performance.

______________________________________________________________________

# Performance Checklist

```
OnPush

↓

track

↓

AsyncPipe

↓

Lazy Loading

↓

Signals

↓

Caching

↓

Small Components
```

______________________________________________________________________

# Angular DevTools

Angular provides

Angular DevTools

for

- Component tree inspection
- Change detection analysis
- Performance profiling

Useful for identifying unnecessary rendering.

______________________________________________________________________

# Enterprise Example

Dashboard

```
Charts

↓

Lazy Loaded

↓

Signals

↓

OnPush

↓

track

↓

Fast Rendering
```

______________________________________________________________________

# Backend Comparison

Backend optimization

```
Caching

↓

Indexes

↓

Connection Pool
```

Frontend optimization

```
OnPush

↓

Signals

↓

track

↓

Lazy Loading
```

Both aim to reduce unnecessary work.

______________________________________________________________________

# Common Mistakes

## Using Default Everywhere

OnPush

can improve performance

when components follow immutable patterns.

______________________________________________________________________

## Forgetting track

Always provide

```
track user.id
```

for lists.

______________________________________________________________________

## Heavy Template Methods

Avoid

```html
calculate()
```

inside templates.

______________________________________________________________________

## Subscribing Everywhere

Prefer

```
AsyncPipe
```

when displaying Observables.

______________________________________________________________________

## Rendering Huge Lists

Use

pagination

or

virtual scrolling.

______________________________________________________________________

# Best Practices

✅ Prefer immutable updates.

✅ Use `track` with `@for`.

✅ Consider `OnPush` for larger applications.

✅ Use `AsyncPipe` instead of manual subscriptions in templates.

✅ Lazy load feature areas.

✅ Use Signals for local UI state where appropriate.

✅ Cache expensive operations.

______________________________________________________________________

# Interview Deep Dive

## Question

What is Change Detection?

### Answer

Change Detection is Angular's mechanism for detecting changes in application state and updating the DOM to keep the user
interface synchronized with component data.

______________________________________________________________________

## Question

What is the difference between Default and OnPush change detection?

### Answer

The Default strategy checks components frequently during change detection, while OnPush reduces unnecessary checks by
running primarily when inputs change, events occur, Observables emit through the async pipe, Signals change, or change
detection is triggered manually.

______________________________________________________________________

## Question

Why should `track` be used with `@for`?

### Answer

The tracking expression allows Angular to identify individual list items, minimizing DOM updates and significantly
improving performance when rendering large collections.

______________________________________________________________________

## Question

What are Signals?

### Answer

Signals are Angular's built-in reactive primitives that store state and automatically notify Angular when their values
change, enabling fine-grained UI updates with a simpler API than many RxJS use cases.

______________________________________________________________________

## Question

When should Signals be used instead of RxJS?

### Answer

Signals are well suited for local UI state and derived values, while RxJS remains the preferred choice for asynchronous
streams such as HTTP requests, WebSockets, and complex event composition.

______________________________________________________________________

# Practice Questions

1. What is Change Detection?
1. What is the difference between Default and OnPush strategies?
1. Why is immutability important with OnPush?
1. Why should `track` be used with `@for`?
1. What are Signals?
1. What is a Computed Signal?
1. What is an Effect?
1. When should AsyncPipe be preferred?
1. How does lazy loading improve performance?
1. List five common Angular performance optimizations.

______________________________________________________________________

# Summary

Performance optimization in Angular is about reducing unnecessary work.

In this chapter, you learned:

- Change Detection
- Default strategy
- OnPush strategy
- Immutability
- `track` with `@for`
- Signals
- Computed Signals
- Effects
- AsyncPipe
- Lazy loading
- `@defer`
- Virtual scrolling
- Bundle optimization
- Tree shaking
- Angular DevTools
- Performance best practices

This chapter provides the performance foundation you'll use in every Angular application. Later in the course, the
**Modern Angular Features** chapter will revisit Signals in greater depth, including Signal Inputs, Signal-based
components, Zoneless Angular, and migration strategies from RxJS-based state.

______________________________________________________________________

# Next

[Module Federation Fundamentals](18-module-federation-fundamentals.md)
