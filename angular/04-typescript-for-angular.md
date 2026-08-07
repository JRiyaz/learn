# TypeScript for Angular

Angular is built using **TypeScript**.

Although we already covered TypeScript in detail earlier, Angular uses a specific subset of TypeScript features every
day.

This chapter focuses only on the TypeScript concepts that you'll encounter constantly while working with Angular.

______________________________________________________________________

# Why Does Angular Use TypeScript?

Angular applications become very large.

Imagine

```
300 Components

150 Services

100 Models

Thousands of Files
```

Without static typing,

maintaining such applications becomes difficult.

TypeScript provides

- Static typing
- Better IDE support
- Autocomplete
- Compile-time error detection
- Easier refactoring

______________________________________________________________________

# Typical Angular Class

Every Angular component is a TypeScript class.

Example

```typescript
export class UserComponent {

    title = "Users";

}
```

Angular builds almost everything around classes.

______________________________________________________________________

# Access Modifiers

You'll see these constantly.

## public

Accessible everywhere.

```typescript
public name = "Alice";
```

Usually written simply as

```typescript
name = "Alice";
```

because members are public by default.

______________________________________________________________________

## private

Accessible only inside the class.

```typescript
private users = [];
```

Other classes cannot access it.

______________________________________________________________________

## protected

Accessible inside

- Current class
- Child classes

```typescript
protected loading = false;
```

______________________________________________________________________

# Constructor

Angular uses constructors extensively.

Example

```typescript
export class UserComponent {

    constructor() {

        console.log(

            "Created"

        );

    }

}
```

______________________________________________________________________

# Constructor Injection

One of Angular's most important features.

Example

```typescript
constructor(

    private userService:

    UserService

) {

}
```

Notice

No

```typescript
new UserService()
```

Angular creates it automatically.

We'll study Dependency Injection later.

______________________________________________________________________

# Property Initialization

Instead of

```typescript
title: string;

constructor() {

    this.title = "Users";

}
```

We usually write

```typescript
title = "Users";
```

Cleaner.

______________________________________________________________________

# Interface

Interfaces describe data.

Example

```typescript
export interface User {

    id: number;

    name: string;

    email: string;

}
```

Used for

- API responses
- Request objects
- Models

______________________________________________________________________

# Using Interfaces

```typescript
users: User[] = [];
```

Now

```typescript
users.push({

    id: 1,

    name: "Alice",

    email: "[email protected]"

});
```

TypeScript checks the structure.

______________________________________________________________________

# Type Alias

Sometimes

```typescript
type
```

is a better choice.

Example

```typescript
type Status =

"ACTIVE"

|

"INACTIVE";
```

Useful for fixed values.

______________________________________________________________________

# Optional Properties

Not every property is mandatory.

```typescript
interface User {

    id: number;

    name: string;

    phone?: string;

}
```

Valid

```typescript
{

id:1,

name:"Alice"

}
```

______________________________________________________________________

# Readonly

Some values should never change.

```typescript
interface User {

    readonly id: number;

}
```

Attempting to modify

```typescript
user.id = 2;
```

causes a compile-time error.

______________________________________________________________________

# Array Types

Most Angular applications work with arrays.

```typescript
users: User[] = [];
```

Alternative

```typescript
Array<User>
```

Both are equivalent.

______________________________________________________________________

# Generics

Angular uses Generics everywhere.

Example

```typescript
HttpClient
```

```typescript
this.http.get<User[]>(

"/api/users"

);
```

The generic

```
<User[]>
```

tells TypeScript

what the backend returns.

______________________________________________________________________

# Generic Example

```typescript
function identity<T>(

    value: T

): T {

    return value;

}
```

Usage

```typescript
identity<User>(

user

);
```

______________________________________________________________________

# Decorators

Angular heavily relies on decorators.

Component

```typescript
@Component({

})
```

Service

```typescript
@Injectable({

})
```

Input

```typescript
@Input()
```

Output

```typescript
@Output()
```

Decorators add metadata to classes and properties.

______________________________________________________________________

# Class Decorator Example

```typescript
@Component({

    selector: "app-user",

    templateUrl:

    "./user.component.html"

})
```

This tells Angular

```
This class

↓

Is a Component
```

______________________________________________________________________

# Import and Export

Every Angular application is modular.

Export

```typescript
export class UserComponent {

}
```

Import

```typescript
import {

    UserComponent

}

from "./user.component";
```

You'll write imports constantly.

______________________________________________________________________

# Arrow Functions

Example

```typescript
users.forEach(

user =>

console.log(

user.name

)

);
```

Angular uses arrow functions extensively.

______________________________________________________________________

# Template Strings

Instead of

```typescript
"Hello "

+

name
```

Use

```typescript
`Hello ${name}`
```

Much cleaner.

______________________________________________________________________

# Destructuring

Instead of

```typescript
const name =

user.name;

const email =

user.email;
```

Use

```typescript
const {

    name,

    email

} = user;
```

Very common.

______________________________________________________________________

# Spread Operator

Create new object.

```typescript
const updated = {

    ...user,

    name: "Bob"

};
```

Angular encourages immutable updates.

______________________________________________________________________

# Optional Chaining

Instead of

```typescript
user.address.city
```

Use

```typescript
user?.address?.city
```

Avoids runtime errors.

______________________________________________________________________

# Nullish Coalescing

```typescript
const city =

user.city

??

"Unknown";
```

Used frequently in templates.

______________________________________________________________________

# Enums

Example

```typescript
enum Status {

    Active,

    Inactive

}
```

Many Angular projects instead prefer

```typescript
type Status =

"ACTIVE"

|

"INACTIVE";
```

______________________________________________________________________

# Async / Await

Angular communicates with APIs asynchronously.

Example

```typescript
async loadUsers() {

    const users =

        await api.getUsers();

}
```

Although Angular primarily uses **Observables**, you'll still encounter `async`/`await` in supporting code.

______________________________________________________________________

# Promise

```typescript
fetch(

"/api/users"

)
```

returns

```
Promise
```

Angular's `HttpClient`

returns

```
Observable
```

We'll compare them later.

______________________________________________________________________

# Modules

Every file is a module.

Example

```typescript
export interface User {

}
```

Another file

```typescript
import {

    User

}

from "./user";
```

______________________________________________________________________

# Strict Typing

Bad

```typescript
users: any[];
```

Good

```typescript
users: User[];
```

Always prefer explicit types.

______________________________________________________________________

# Angular Model

Create

```
models/

user.ts
```

```typescript
export interface User {

    id: number;

    name: string;

}
```

Reuse everywhere.

______________________________________________________________________

# DTO Example

Backend returns

```json
{

"id":1,

"name":"Alice"

}
```

Angular model

```typescript
interface User {

    id: number;

    name: string;

}
```

The structures match.

______________________________________________________________________

# Type Safety

Without TypeScript

```typescript
user.nmae
```

Runtime error.

With TypeScript

Compiler immediately reports

```
Property

'nmae'

does not exist.
```

______________________________________________________________________

# Immutability

Instead of

```typescript
user.name =

"Bob";
```

Prefer

```typescript
user = {

...user,

name:"Bob"

};
```

Especially useful with Angular change detection.

______________________________________________________________________

# Folder Example

```
app/

├── models/

│   └── user.ts

├── services/

├── components/

└── pages/
```

Models usually contain interfaces.

______________________________________________________________________

# Common Mistakes

## Using any

Wrong

```typescript
users: any[];
```

Always create interfaces.

______________________________________________________________________

## Forgetting Exports

Wrong

```typescript
interface User {

}
```

Correct

```typescript
export interface User {

}
```

Otherwise,

other files cannot import it.

______________________________________________________________________

## Creating Objects Without Interfaces

Bad

```typescript
const user = {

id:1,

name:"Alice"

};
```

Better

```typescript
const user: User = {

id:1,

name:"Alice"

};
```

______________________________________________________________________

## Ignoring Optional Properties

Always check

```typescript
user?.address
```

instead of assuming it exists.

______________________________________________________________________

# Best Practices

✅ Create interfaces for API models.

✅ Avoid `any`.

✅ Use constructor injection.

✅ Prefer immutable updates.

✅ Export reusable types.

✅ Keep models in a dedicated folder.

✅ Use Generics with `HttpClient`.

______________________________________________________________________

# Interview Deep Dive

## Question

Why does Angular use TypeScript?

### Answer

TypeScript provides static typing, compile-time error checking, better tooling, and easier refactoring. These features
make large Angular applications easier to develop and maintain.

______________________________________________________________________

## Question

Why are interfaces commonly used in Angular?

### Answer

Interfaces define the structure of application data, such as API requests and responses. They improve type safety and
help developers catch mistakes during compilation instead of at runtime.

______________________________________________________________________

## Question

Why is constructor injection used in Angular?

### Answer

Constructor injection allows Angular's Dependency Injection system to automatically provide dependencies such as
services, improving testability and reducing coupling.

______________________________________________________________________

## Question

Why does `HttpClient` use Generics?

### Answer

Generics tell TypeScript the expected response type from an API. This enables compile-time type checking, autocomplete,
and safer access to response data.

______________________________________________________________________

## Question

Why are immutable updates encouraged?

### Answer

Creating new objects instead of modifying existing ones makes state changes easier to track, reduces unintended side
effects, and works well with Angular's change detection mechanisms.

______________________________________________________________________

# Practice Questions

1. Why does Angular use TypeScript?
1. What is the purpose of interfaces?
1. What is constructor injection?
1. Why are decorators important in Angular?
1. Why should `any` be avoided?
1. How are Generics used with `HttpClient`?
1. What is the purpose of the spread operator?
1. Why is optional chaining useful?
1. What is the difference between a Promise and an Observable (high level)?
1. Why are immutable updates recommended?

______________________________________________________________________

# Summary

Angular is built on a practical subset of TypeScript features that you'll use every day.

In this chapter, you learned:

- Classes
- Access modifiers
- Constructors
- Constructor injection
- Interfaces
- Type aliases
- Generics
- Decorators
- Imports and exports
- Arrow functions
- Destructuring
- Spread operator
- Optional chaining
- Async programming
- Models
- DTOs
- Type safety
- Immutability

These concepts appear throughout every Angular application and form the foundation for components, services, routing,
forms, and HTTP communication.

______________________________________________________________________

# Next

[Components](05-components.md)
