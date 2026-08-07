# RxJS (Reactive Extensions for JavaScript)

If there is one topic that scares most Angular developers,

it's **RxJS**.

The good news is that for **90% of Angular applications**, you only need to understand a relatively small subset of
RxJS.

This chapter focuses on the parts you'll use every day in Angular and in interviews.

______________________________________________________________________

# What is RxJS?

RxJS is a library for handling

- Asynchronous programming
- Event streams
- Data streams

Angular uses RxJS extensively for

- HTTP Requests
- User Events
- Routing
- Forms
- WebSockets

______________________________________________________________________

# Why Do We Need RxJS?

Suppose a user

- Clicks a button
- Types in a search box
- Receives notifications
- Downloads data

These events happen over time.

Instead of handling each manually,

RxJS represents them as

```
Streams
```

______________________________________________________________________

# What is a Stream?

Imagine water flowing through a pipe.

```
~~~~~~~~~~~~~~>

Water
```

Data works the same way.

```
1

↓

2

↓

3

↓

4

↓

5
```

Instead of one value,

multiple values arrive over time.

This is called a

```
Stream
```

______________________________________________________________________

# Observable

The heart of RxJS.

An Observable produces data over time.

```
Observable

↓

1

↓

2

↓

3

↓

Completed
```

Think of it as

```
Data Producer
```

______________________________________________________________________

# Observer

The Observer receives values.

```
Observable

↓

Observer
```

Example

```typescript
observable.subscribe({

next: value =>

console.log(value)

});
```

______________________________________________________________________

# Observable Lifecycle

```
Create Observable

↓

Subscribe

↓

Receive Values

↓

Complete

OR

Error
```

______________________________________________________________________

# Observable vs Promise

| Promise | Observable |
|----------|------------|
| One Value | Multiple Values |
| Eager | Lazy |
| Cannot Cancel | Can Cancel |
| Native JavaScript | RxJS |
| No Operators | Rich Operators |

______________________________________________________________________

# Promise

```
Promise

↓

One Result

↓

Done
```

Example

```typescript
fetch("/users")
```

______________________________________________________________________

# Observable

```
Observable

↓

Value

↓

Value

↓

Value

↓

Complete
```

Much more flexible.

______________________________________________________________________

# Why Angular Uses Observables

Angular applications constantly deal with

- API calls
- Form changes
- Route changes
- Button clicks
- Timers

All of these naturally fit

```
Streams
```

______________________________________________________________________

# HttpClient Returns Observable

```typescript
this.http.get<User[]>(

"/api/users"

);
```

Notice

Nothing happens yet.

______________________________________________________________________

# Subscribe

Execution begins only after subscribing.

```typescript
this.http

.get<User[]>(

"/api/users"

)

.subscribe(users => {

console.log(users);

});
```

______________________________________________________________________

# Lazy Execution

Observable

```
Created

↓

Nothing Happens
```

Only after

```
subscribe()
```

does Angular send the HTTP request.

______________________________________________________________________

# Complete Flow

```
Component

↓

HttpClient

↓

Observable

↓

subscribe()

↓

Backend

↓

Response

↓

UI
```

______________________________________________________________________

# Observable States

```
next()

↓

next()

↓

next()

↓

complete()
```

or

```
next()

↓

error()
```

______________________________________________________________________

# Subject

A Subject is both

```
Observable

AND

Observer
```

It can

- Produce values
- Receive values

______________________________________________________________________

# Subject Example

```typescript
const subject =

new Subject<number>();
```

Send

```typescript
subject.next(10);
```

Receive

```typescript
subject.subscribe(

value =>

console.log(value)

);
```

______________________________________________________________________

# BehaviorSubject

Most common Subject in Angular.

Difference

```
Always remembers

Latest Value
```

Example

```typescript
const user$ =

new BehaviorSubject<User | null>(

null

);
```

______________________________________________________________________

# BehaviorSubject Example

```
Current User

↓

Login

↓

Updated User

↓

Logout

↓

null
```

Every subscriber immediately receives

the latest value.

______________________________________________________________________

# ReplaySubject

ReplaySubject remembers

multiple previous values.

Example

```
1

2

3
```

New subscriber receives

```
1

2

3
```

depending on buffer size.

______________________________________________________________________

# Subject Comparison

| Type | Remembers Previous Value? |
|--------|---------------------------|
| Subject | No |
| BehaviorSubject | Latest Value |
| ReplaySubject | Multiple Values |

______________________________________________________________________

# Common Angular Uses

Subject

```
Simple Events
```

BehaviorSubject

```
Authentication

Shopping Cart

Theme

Current User
```

ReplaySubject

```
Caching

Notifications

History
```

______________________________________________________________________

# Pipe

RxJS operators are applied using

```typescript
pipe()
```

Example

```typescript
this.http.get<User[]>(...)

.pipe(...);
```

Think of it as

```
Input

↓

Operator

↓

Operator

↓

Output
```

______________________________________________________________________

# map()

Transforms data.

```typescript
users$

.pipe(

map(users =>

users.length)

);
```

______________________________________________________________________

# filter()

Keeps matching values.

```typescript
numbers$

.pipe(

filter(

n =>

n > 10

)

);
```

______________________________________________________________________

# tap()

Useful for

logging

or debugging.

```typescript
tap(

value =>

console.log(value)

)
```

Does not modify data.

______________________________________________________________________

# switchMap()

One of the most important operators.

Suppose user searches

```
A

↓

AB

↓

ABC
```

Older requests become useless.

```
switchMap()

↓

Cancel Previous

↓

Keep Latest
```

Perfect for

- Search
- Autocomplete

______________________________________________________________________

# mergeMap()

Runs everything simultaneously.

```
A

↓

B

↓

C

↓

All Execute
```

Good for

independent requests.

______________________________________________________________________

# concatMap()

Runs requests

one after another.

```
A

↓

Complete

↓

B

↓

Complete

↓

C
```

Useful when order matters.

______________________________________________________________________

# exhaustMap()

Ignores new requests

until current request finishes.

Perfect for

```
Login Button

Submit Button
```

Prevent duplicate clicks.

______________________________________________________________________

# forkJoin()

Run multiple requests

in parallel.

```
Users API

↓

Orders API

↓

Products API

↓

Wait

↓

All Finished
```

Then continue.

______________________________________________________________________

Example

```typescript
forkJoin({

users:

this.userService.getUsers(),

orders:

this.orderService.getOrders()

});
```

______________________________________________________________________

# combineLatest()

Whenever any Observable changes,

combine latest values.

```
User

+

Settings

↓

Latest Combined Result
```

Useful for dashboards.

______________________________________________________________________

# debounceTime()

Search box.

Typing

```
A

AB

ABC

ABCD
```

Without debounce

```
4 API Calls
```

With

```typescript
debounceTime(500)
```

```
Wait

↓

One API Call
```

______________________________________________________________________

# take()

Receive only

first

N values.

```typescript
take(1)
```

Common with authentication state.

______________________________________________________________________

# takeUntil()

Automatically unsubscribe.

Very important.

Example

```typescript
takeUntil(

destroy$

)
```

Prevents memory leaks.

______________________________________________________________________

# Async Pipe

Instead of

```typescript
subscribe()
```

Angular templates can use

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

Prefer this whenever possible in templates.

______________________________________________________________________

# Memory Leaks

Wrong

```
Subscribe

↓

Never Unsubscribe
```

Memory keeps growing.

______________________________________________________________________

Solutions

- Async Pipe
- takeUntil()
- Angular lifecycle cleanup

______________________________________________________________________

# Error Handling

```typescript
catchError(...)
```

Used inside

```
pipe()
```

Example

```
API

↓

Error

↓

Fallback Value
```

______________________________________________________________________

# Retry

Temporary network failure?

```typescript
retry(3)
```

Retries automatically.

______________________________________________________________________

# Loading Indicator Example

```
Button

↓

Loading=true

↓

API

↓

Loading=false

↓

Update UI
```

Usually implemented with RxJS.

______________________________________________________________________

# Search Example

```
User Types

↓

debounceTime

↓

switchMap

↓

API

↓

Results
```

One of the most common interview examples.

______________________________________________________________________

# Dashboard Example

```
Users API

↓

Orders API

↓

Revenue API

↓

forkJoin()

↓

Dashboard
```

______________________________________________________________________

# Login Example

```
Click Login

↓

exhaustMap()

↓

Backend

↓

JWT

↓

BehaviorSubject

↓

Navbar Updates
```

______________________________________________________________________

# Operator Cheat Sheet

| Operator | Purpose |
|-----------|----------|
| map | Transform |
| filter | Filter Values |
| tap | Logging |
| switchMap | Cancel Previous |
| mergeMap | Parallel |
| concatMap | Sequential |
| exhaustMap | Ignore Duplicates |
| forkJoin | Wait for All |
| combineLatest | Combine Latest |
| debounceTime | Delay |
| take | First N Values |
| takeUntil | Auto Cleanup |
| catchError | Handle Errors |
| retry | Retry Request |

______________________________________________________________________

# Common Mistakes

## Nested subscribe()

Wrong

```typescript
subscribe(

users => {

subscribe(...);

} )
```

Use operators like

```
switchMap
```

instead.

______________________________________________________________________

## Forgetting Unsubscribe

Causes

```
Memory Leak
```

Use

- Async Pipe
- takeUntil()

______________________________________________________________________

## Using mergeMap for Search

Search should usually use

```
switchMap()
```

to cancel outdated requests.

______________________________________________________________________

## Not Using BehaviorSubject for Shared State

Authentication and user state are ideal use cases for

```
BehaviorSubject
```

______________________________________________________________________

# Best Practices

✅ Return Observables from services.

✅ Prefer the Async Pipe in templates.

✅ Use `switchMap()` for search and route-dependent requests.

✅ Use `forkJoin()` for independent parallel API calls.

✅ Use `BehaviorSubject` for shared application state.

✅ Avoid nested subscriptions.

✅ Clean up long-lived subscriptions.

______________________________________________________________________

# Interview Deep Dive

## Question

What is an Observable?

### Answer

An Observable is a lazy data stream that can emit zero, one, or many values over time. Angular uses Observables extensively for HTTP requests, events, forms, and routing.

______________________________________________________________________

## Question

What is the difference between an Observable and a Promise?

### Answer

A Promise produces a single value and begins execution immediately. An Observable is lazy, can emit multiple values, supports cancellation, and provides powerful composition through RxJS operators.

______________________________________________________________________

## Question

What is the difference between Subject and BehaviorSubject?

### Answer

A Subject emits values only to current subscribers. A BehaviorSubject stores the latest value and immediately emits it to new subscribers.

______________________________________________________________________

## Question

When should `switchMap()` be used?

### Answer

Use `switchMap()` when only the latest request matters, such as search boxes or route changes. It automatically cancels previous requests.

______________________________________________________________________

## Question

What is the purpose of the Async Pipe?

### Answer

The Async Pipe subscribes to an Observable in the template, updates the view when new values arrive, and automatically unsubscribes when the component is destroyed.

______________________________________________________________________

# Practice Questions

1. What is RxJS?
1. What is an Observable?
1. How is an Observable different from a Promise?
1. What is a Subject?
1. What is a BehaviorSubject?
1. What is the purpose of `pipe()`?
1. When should `switchMap()` be used?
1. What is the difference between `mergeMap()` and `concatMap()`?
1. Why is the Async Pipe preferred in templates?
1. How can you prevent memory leaks caused by subscriptions?

______________________________________________________________________

# Summary

RxJS is the foundation of asynchronous programming in Angular.

In this chapter, you learned:

- Observables
- Observers
- `subscribe()`
- Subjects
- BehaviorSubject
- ReplaySubject
- `pipe()`
- `map`
- `filter`
- `tap`
- `switchMap`
- `mergeMap`
- `concatMap`
- `exhaustMap`
- `forkJoin`
- `combineLatest`
- `debounceTime`
- `take`
- `takeUntil`
- Async Pipe
- Error handling
- Retry
- Memory leak prevention
- Best practices

With RxJS complete, you now understand how Angular handles asynchronous data. The next chapter brings everything together by exploring **Enterprise Angular Project Architecture**, where you'll learn how large Angular applications are organized, how to structure folders, separate features, manage environments, and build maintainable applications.

______________________________________________________________________

# Next

[Project Architecture](13-project-architecture.md)
