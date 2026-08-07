# TypeScript Interview Cheatsheet

This file is designed for **last-minute interview revision**.

It doesn't teach TypeScript from scratch.

Instead, it summarizes the most important concepts that are frequently asked in backend interviews.

______________________________________________________________________

# TypeScript Overview

- Superset of JavaScript
- Adds static typing
- Compiles to JavaScript
- Developed by Microsoft
- Improves developer productivity
- Excellent IDE support

______________________________________________________________________

# Compilation

```
TypeScript

↓

tsc

↓

JavaScript

↓

Node.js / Browser
```

Node.js does **not** execute TypeScript directly.

______________________________________________________________________

# Primitive Types

```typescript
string

number

boolean

null

undefined

symbol

bigint
```

______________________________________________________________________

# Special Types

## any

- Disables type checking
- Avoid when possible

______________________________________________________________________

## unknown

- Safer alternative to `any`
- Requires type checking

______________________________________________________________________

## void

Used for functions without return values.

______________________________________________________________________

## never

Used for

- Functions that never return
- Infinite loops
- Exhaustive switch statements

______________________________________________________________________

# Variable Declaration

Prefer

```typescript
const
```

Then

```typescript
let
```

Avoid

```typescript
var
```

______________________________________________________________________

# Arrays

```typescript
const users: User[] = [];
```

Alternative

```typescript
Array<User>
```

______________________________________________________________________

# Tuple

```typescript
const user:

[number, string]
```

Fixed size.

Fixed order.

______________________________________________________________________

# Enum

```typescript
enum Status {

    Active,

    Inactive

}
```

Modern projects often prefer

```typescript
type Status =

"ACTIVE"

|

"INACTIVE";
```

______________________________________________________________________

# Functions

```typescript
function add(

a:number,

b:number

):number{

return a+b;

}
```

______________________________________________________________________

Optional parameter

```typescript
name?: string
```

______________________________________________________________________

Default parameter

```typescript
count = 10
```

______________________________________________________________________

Rest parameter

```typescript
...numbers:number[]
```

______________________________________________________________________

# Arrow Function

```typescript
const add =

(a,b)=>a+b;
```

______________________________________________________________________

# Type Alias

```typescript
type UserId = number;
```

______________________________________________________________________

# Interface

Defines object contract.

```typescript
interface User {

id:number;

name:string;

}
```

______________________________________________________________________

# Interface vs Type

Interface

- Object contracts
- Declaration merging

Type

- Unions
- Tuples
- Primitives
- Advanced types

______________________________________________________________________

# Class

```typescript
class User {

constructor(

public id:number

){}

}
```

______________________________________________________________________

# Access Modifiers

```
public

private

protected
```

______________________________________________________________________

# readonly

Immutable property.

______________________________________________________________________

# Static

Belongs to class.

______________________________________________________________________

# Abstract Class

Cannot instantiate.

______________________________________________________________________

# Generics

Generic function

```typescript
function identity<T>(

value:T

):T{

return value;

}
```

______________________________________________________________________

Generic interface

```typescript
interface ApiResponse<T>{

data:T;

}
```

______________________________________________________________________

Constraint

```typescript
<T extends User>
```

______________________________________________________________________

Common interview

```typescript
K extends keyof T
```

______________________________________________________________________

# Union

```typescript
string

|

number
```

______________________________________________________________________

# Intersection

```typescript
A

&

B
```

______________________________________________________________________

# Literal Type

```typescript
"GET"

|

"POST"
```

______________________________________________________________________

# Type Guards

```
typeof

instanceof

in
```

Custom

```typescript
value is User
```

______________________________________________________________________

# keyof

Returns property names.

______________________________________________________________________

# typeof

Returns type of variable.

______________________________________________________________________

# Utility Types

## Partial

Everything optional.

______________________________________________________________________

## Required

Everything required.

______________________________________________________________________

## Readonly

Everything immutable.

______________________________________________________________________

## Pick

Keep properties.

______________________________________________________________________

## Omit

Remove properties.

______________________________________________________________________

## Record

Dictionary.

______________________________________________________________________

## Exclude

Remove union members.

______________________________________________________________________

## Extract

Keep union members.

______________________________________________________________________

## ReturnType

Function return type.

______________________________________________________________________

## Parameters

Function parameters.

______________________________________________________________________

## Awaited

Promise result.

______________________________________________________________________

# Collections

## Array

Ordered.

______________________________________________________________________

## Map

Key → Value

Any key type.

______________________________________________________________________

## Set

Unique values.

______________________________________________________________________

## Record

Typed object dictionary.

______________________________________________________________________

# Important Array Methods

```
map()

filter()

reduce()

find()

some()

every()

sort()

flat()

flatMap()
```

Know when to use each.

______________________________________________________________________

# Spread

```typescript
{

...user

}
```

______________________________________________________________________

# Rest

```typescript
...args
```

______________________________________________________________________

# Optional Chaining

```typescript
user?.address?.city
```

______________________________________________________________________

# Nullish Coalescing

```typescript
??

```

Only checks

```
null

undefined
```

______________________________________________________________________

# Promise

States

```
Pending

Fulfilled

Rejected
```

______________________________________________________________________

# async

Returns

```
Promise
```

______________________________________________________________________

# await

Waits for Promise.

______________________________________________________________________

# Promise.all()

Parallel execution.

Fails if one Promise fails.

______________________________________________________________________

# Promise.allSettled()

Waits for all Promises.

______________________________________________________________________

# Promise.race()

First completed Promise.

______________________________________________________________________

# Promise.any()

First successful Promise.

______________________________________________________________________

# Modules

Named export

```typescript
export
```

______________________________________________________________________

Default export

```typescript
export default
```

Named exports are generally preferred.

______________________________________________________________________

# tsconfig.json

Important options

```json
strict

target

module

rootDir

outDir
```

______________________________________________________________________

# Backend Project Structure

```
src/

controllers/

services/

repositories/

middleware/

models/

config/

utils/
```

______________________________________________________________________

# Layered Architecture

```
Controller

↓

Service

↓

Repository

↓

Database
```

______________________________________________________________________

# DTO

Used for

- Request
- Response

Never expose entities directly.

______________________________________________________________________

# Dependency Injection

Receive dependencies.

Don't create them.

______________________________________________________________________

# Repository Pattern

Encapsulates data access.

______________________________________________________________________

# Service Pattern

Contains business logic.

______________________________________________________________________

# Controller Pattern

Handles HTTP.

______________________________________________________________________

# Decorators

Examples

```typescript
@Controller()

@Get()

@Post()

@Injectable()

@Module()
```

Used heavily by NestJS.

______________________________________________________________________

# Configuration

Use

```
.env
```

Never hardcode secrets.

______________________________________________________________________

# Logging

Prefer

```typescript
logger.info()

logger.error()
```

over

```typescript
console.log()
```

______________________________________________________________________

# Error Handling

Prefer

```typescript
try

catch
```

Use centralized error middleware.

______________________________________________________________________

# Best Practices

- Enable strict mode.
- Prefer `const`.
- Avoid `any`.
- Prefer `unknown`.
- Use interfaces for object contracts.
- Use utility types.
- Keep controllers thin.
- Put business logic in services.
- Use repositories for database access.
- Prefer dependency injection.
- Prefer immutable updates.
- Use `Promise.all()` for independent async work.
- Validate all external input.
- Return consistent API responses.

______________________________________________________________________

# Frequently Asked Interview Questions

## TypeScript Basics

- What is TypeScript?
- Why use TypeScript?
- TypeScript vs JavaScript
- Type inference
- `any` vs `unknown`
- `null` vs `undefined`
- `never` vs `void`

______________________________________________________________________

## OOP

- Interface vs Type
- Interface vs Abstract Class
- Access modifiers
- Constructor shorthand
- `readonly`
- Static members

______________________________________________________________________

## Advanced Types

- Union vs Intersection
- Type guards
- `keyof`
- `typeof`
- Literal types
- Discriminated unions

______________________________________________________________________

## Generics

- Generic functions
- Generic interfaces
- Generic constraints
- `extends`
- `K extends keyof T`

______________________________________________________________________

## Utility Types

- Partial
- Pick
- Omit
- Readonly
- Record
- ReturnType
- Parameters
- Awaited

______________________________________________________________________

## Async

- Promise lifecycle
- async/await
- Promise.all
- Promise.allSettled
- Promise.race
- Promise.any

______________________________________________________________________

## Collections

- Array vs Map
- Map vs Record
- Set
- reduce()
- map()
- filter()
- sort()

______________________________________________________________________

## Backend

- DTO
- Repository Pattern
- Service Pattern
- Dependency Injection
- Middleware
- Configuration
- Logging

______________________________________________________________________

# 30-Second Revision

- TypeScript compiles to JavaScript.
- Prefer `const` over `let`; avoid `var`.
- Avoid `any`; prefer `unknown`.
- Use interfaces for object contracts.
- Use `type` for unions and advanced types.
- Use Generics instead of `any`.
- Prefer utility types (`Partial`, `Pick`, `Omit`) over duplicate interfaces.
- Use `async/await` with `try/catch`.
- Use `Promise.all()` for independent tasks.
- Keep controllers thin.
- Business logic belongs in services.
- Data access belongs in repositories.
- Never expose entities directly—use DTOs.
- Enable `strict` mode.
- Prefer dependency injection over creating dependencies manually.
- Use named exports and path aliases.
- Validate external input and centralize configuration.

______________________________________________________________________

# Summary

If you can confidently explain every topic in this cheatsheet—and justify **why** each concept exists—you'll be well
prepared for most TypeScript backend interviews involving Express, NestJS, Fastify, or general Node.js development.

______________________________________________________________________

# Next

[TypeScript vs Java](16-typescript-vs-java.md)
