# Async Programming

Modern backend applications spend most of their time waiting.

Waiting for:

- Database queries
- HTTP APIs
- File operations
- Message queues
- Redis
- S3 uploads
- Email services

If the application blocks while waiting, it cannot efficiently serve other requests.

This is why asynchronous programming is fundamental in Node.js and TypeScript.

______________________________________________________________________

# Synchronous vs Asynchronous

## Synchronous

Tasks execute one after another.

```
Task 1

↓

Task 2

↓

Task 3
```

Example

```typescript
console.log("Start");

console.log("Processing");

console.log("End");
```

Output

```
Start

Processing

End
```

______________________________________________________________________

## Asynchronous

A task starts,

continues in the background,

and the program keeps running.

```
Task 1

↓

Task 2 (Waiting)

↓

Task 3

↓

Task 2 completes
```

This is ideal for I/O operations.

______________________________________________________________________

# Why Async Matters

Suppose an API takes

```
5 seconds
```

Without async

```
Request

↓

Wait 5 seconds

↓

Continue
```

CPU is mostly idle.

______________________________________________________________________

With async

```
Request starts

↓

Continue doing other work

↓

Receive result later
```

Much more efficient.

______________________________________________________________________

# Callback (Historical)

Before Promises,

JavaScript used callbacks.

```typescript
function fetchUser(

    callback: (name: string) => void

) {

    setTimeout(() => {

        callback("Alice");

    }, 1000);

}
```

Usage

```typescript
fetchUser((user) => {

    console.log(user);

});
```

Output

```
Alice
```

______________________________________________________________________

# Callback Hell

Example

```typescript
login(() => {

    getUser(() => {

        getOrders(() => {

            getPayments(() => {

                console.log("Done");

            });

        });

    });

});
```

Very difficult to read.

Promises solve this.

______________________________________________________________________

# Promise

A Promise represents the eventual result of an asynchronous operation.

Think of it as:

```
"I promise I'll give you a value later."
```

______________________________________________________________________

# Promise States

```
Pending

↓

Fulfilled

OR

Rejected
```

______________________________________________________________________

# Creating a Promise

```typescript
const promise =

new Promise<string>(

    (resolve, reject) => {

        resolve("Success");

    }

);
```

______________________________________________________________________

# Consuming a Promise

```typescript
promise.then((result) => {

    console.log(result);

});
```

Output

```
Success
```

______________________________________________________________________

# Rejecting a Promise

```typescript
const promise =

new Promise((

    resolve,

    reject

) => {

    reject("Something went wrong");

});
```

Handle error

```typescript
promise.catch(

    (error) => {

        console.log(error);

    }

);
```

______________________________________________________________________

# then()

Executed when successful.

```typescript
promise.then(

    result =>

        console.log(result)

);
```

______________________________________________________________________

# catch()

Executed when rejected.

```typescript
promise.catch(

    error =>

        console.log(error)

);
```

______________________________________________________________________

# finally()

Runs regardless of success or failure.

```typescript
promise

.then(...)

.catch(...)

.finally(() => {

    console.log("Finished");

});
```

______________________________________________________________________

# Promise Chaining

```typescript
fetchUser()

.then(user => {

    return fetchOrders(user);

})

.then(orders => {

    console.log(orders);

});
```

Much cleaner than nested callbacks.

______________________________________________________________________

# async

Marks a function as asynchronous.

```typescript
async function greet() {

    return "Hello";

}
```

Even though a string is returned,

the actual return type is

```typescript
Promise<string>
```

______________________________________________________________________

# await

Waits for a Promise.

```typescript
async function print() {

    const user =

        await fetchUser();

    console.log(user);

}
```

Much easier to read.

______________________________________________________________________

# async + await

Example

```typescript
async function main() {

    const user =

        await fetchUser();

    console.log(user);

}
```

Looks synchronous,

but is asynchronous.

______________________________________________________________________

# Error Handling

Instead of

```typescript
promise.catch(...)
```

Use

```typescript
try {

    const user =

        await fetchUser();

}

catch(error) {

    console.log(error);

}
```

Cleaner.

Preferred.

______________________________________________________________________

# Complete Example

```typescript
async function loadUser() {

    try {

        const user =

            await fetchUser();

        console.log(user);

    }

    catch(error) {

        console.log(error);

    }

}
```

______________________________________________________________________

# Returning Promise

```typescript
async function getNumber()

: Promise<number> {

    return 100;

}
```

______________________________________________________________________

# Promise.all()

Run multiple async operations simultaneously.

Instead of

```typescript
const user =

    await getUser();

const orders =

    await getOrders();
```

Use

```typescript
const [

    user,

    orders

] = await Promise.all([

    getUser(),

    getOrders()

]);
```

Both run concurrently.

Much faster.

______________________________________________________________________

# Promise.all() Behavior

If **one Promise fails**,

the entire operation fails.

```
Task A

✓

Task B

✓

Task C

✗

↓

Promise.all fails
```

______________________________________________________________________

# Promise.allSettled()

Waits for every Promise,

even if some fail.

```typescript
const results =

await Promise.allSettled([

    getUser(),

    getOrders(),

    getPayments()

]);
```

Each result indicates

```
fulfilled

or

rejected
```

______________________________________________________________________

# Promise.race()

Returns the first completed Promise.

```typescript
const result =

await Promise.race([

    fastApi(),

    slowApi()

]);
```

Useful for

- Timeouts
- Competing requests

______________________________________________________________________

# Promise.any()

Returns the first successful Promise.

```typescript
const result =

await Promise.any([

    api1(),

    api2(),

    api3()

]);
```

Unlike `race()`,

failed Promises are ignored unless all fail.

______________________________________________________________________

# Sequential vs Parallel

Sequential

```typescript
const user =

    await getUser();

const orders =

    await getOrders();
```

Total

```
2 sec

+

2 sec

=

4 sec
```

______________________________________________________________________

Parallel

```typescript
await Promise.all([

    getUser(),

    getOrders()

]);
```

Total

```
2 sec
```

______________________________________________________________________

# Fetch API

Modern HTTP client.

```typescript
const response =

await fetch(

    "https://api.example.com/users"

);
```

Convert JSON

```typescript
const users =

await response.json();
```

______________________________________________________________________

# Typed Fetch

```typescript
interface User {

    id: number;

    name: string;

}
```

```typescript
const users:

User[] =

await response.json();
```

______________________________________________________________________

# Axios

Popular HTTP library.

Install

```bash
npm install axios
```

______________________________________________________________________

GET Request

```typescript
import axios

from "axios";

const response =

await axios.get<User[]>(

    "/users"

);

console.log(

    response.data

);
```

______________________________________________________________________

POST Request

```typescript
await axios.post(

    "/users",

    {

        name: "Alice"

    }

);
```

______________________________________________________________________

# Timeout Example

```typescript
const controller =

new AbortController();

setTimeout(

    () =>

        controller.abort(),

    5000

);

await fetch(url, {

    signal:

        controller.signal

});
```

Abort after

```
5 seconds
```

______________________________________________________________________

# Retry Pattern

Simple retry

```typescript
async function retry() {

    for (

        let i = 0;

        i < 3;

        i++

    ) {

        try {

            return await fetchUser();

        }

        catch {

        }

    }

}
```

Very common in backend services.

______________________________________________________________________

# Backend Example

Fetch user and orders simultaneously.

```typescript
const [

    user,

    orders

] =

await Promise.all([

    getUser(),

    getOrders()

]);
```

Return

```typescript
{

    user,

    orders

}
```

Exactly how many REST APIs work.

______________________________________________________________________

# Common Mistakes

## Forgetting await

Wrong

```typescript
const user =

    fetchUser();
```

Result

```
Promise
```

Not

```
User
```

______________________________________________________________________

## Await Inside Loop

Wrong

```typescript
for (

    const id of ids

) {

    await getUser(id);

}
```

Sequential.

Slow.

Prefer

```typescript
await Promise.all(

    ids.map(getUser)

);
```

______________________________________________________________________

## Ignoring Errors

Always use

```typescript
try

catch
```

______________________________________________________________________

## Using Promise.all()

When Partial Success is Acceptable

Sometimes

```
Promise.allSettled()
```

is better.

______________________________________________________________________

# Best Practices

✅ Prefer `async/await` over chained `.then()` for readability.

✅ Use `Promise.all()` for independent operations.

✅ Use `Promise.allSettled()` when partial failures are acceptable.

✅ Handle errors with `try/catch`.

✅ Avoid unnecessary sequential awaits.

✅ Use timeouts and retries for external services.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a Promise?

### Answer

A Promise represents the eventual completion or failure of an asynchronous operation. It can be in one of three states:
pending, fulfilled, or rejected. Promises provide a cleaner alternative to nested callbacks.

______________________________________________________________________

## Question

What is the difference between `async/await` and `.then()`?

### Answer

Both work with Promises. `async/await` is syntactic sugar over Promises that makes asynchronous code look like
synchronous code, improving readability and simplifying error handling with `try/catch`.

______________________________________________________________________

## Question

What is the difference between `Promise.all()` and `Promise.allSettled()`?

### Answer

`Promise.all()` resolves only if all Promises succeed. If any Promise rejects, the entire operation rejects immediately.

`Promise.allSettled()` waits for every Promise to complete and returns the status of each one, regardless of success or
failure.

______________________________________________________________________

## Question

When should you use `Promise.race()`?

### Answer

`Promise.race()` returns the result of the first Promise to settle, whether fulfilled or rejected. It is commonly used
to implement request timeouts or to use the fastest available response among multiple asynchronous operations.

______________________________________________________________________

## Question

Why is `Promise.all()` usually faster than awaiting multiple Promises one after another?

### Answer

Sequential `await` executes asynchronous operations one after another, causing their execution times to accumulate.

`Promise.all()` starts all independent operations concurrently, reducing the total waiting time to approximately the
duration of the longest operation.

______________________________________________________________________

# Practice Questions

1. What is asynchronous programming?
1. What are the three states of a Promise?
1. What is the difference between callbacks and Promises?
1. What is the difference between `async/await` and `.then()`?
1. When should you use `Promise.all()`?
1. What is `Promise.allSettled()`?
1. What is the purpose of `Promise.race()`?
1. Why should sequential `await` be avoided for independent tasks?
1. How should asynchronous errors be handled?
1. Why is `async/await` preferred in backend applications?

______________________________________________________________________

# Summary

Asynchronous programming is at the heart of modern Node.js and TypeScript backend development.

In this chapter, you learned:

- Synchronous vs asynchronous execution
- Callbacks
- Promises
- Promise states
- `then()`, `catch()`, and `finally()`
- `async/await`
- Error handling
- `Promise.all()`
- `Promise.allSettled()`
- `Promise.race()`
- `Promise.any()`
- Fetch API
- Axios
- Timeouts
- Retry patterns
- Backend concurrency best practices

Mastering these concepts will help you write efficient, non-blocking backend services and confidently answer one of the
most common topics in TypeScript and Node.js interviews.

______________________________________________________________________

# Next

[Built-in Types & Collections](08-built-in-types.md)
