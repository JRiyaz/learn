# Generics

Generics are one of the most powerful features in TypeScript.

Without Generics, you often have to:

- Duplicate code
- Lose type safety
- Use `any`

Generics allow you to write reusable code **without sacrificing type safety**.

They are heavily used in:

- Express
- NestJS
- Axios
- Prisma
- TypeORM
- Utility libraries

If you've learned Java Generics, the concept is similar—but TypeScript's Generics are generally more flexible.

______________________________________________________________________

# Why Generics?

Suppose we want a function that returns its input.

Without Generics

```typescript
function identity(
    value: any
): any {

    return value;

}
```

Usage

```typescript
const name = identity("Alice");

const age = identity(25);
```

Works.

But

```
Type safety is lost.
```

______________________________________________________________________

# Problem with any

```typescript
const value = identity("Alice");

value.toFixed(2);
```

Compilation

```
No Error
```

Runtime

```
Failure
```

Because

```
value

↓

any
```

______________________________________________________________________

# Generic Function

```typescript
function identity<T>(
    value: T
): T {

    return value;

}
```

Usage

```typescript
const name =
    identity("Alice");

const age =
    identity(25);
```

Now

```
name

↓

string

age

↓

number
```

Completely type-safe.

______________________________________________________________________

# Generic Syntax

```typescript
<T>
```

`T`

means

```
Type
```

It can represent

- string
- number
- object
- array
- class
- interface

Anything.

______________________________________________________________________

# Explicit Generic

Normally

```typescript
identity("Alice");
```

TypeScript infers

```
T = string
```

You can also specify it explicitly.

```typescript
identity<string>("Alice");
```

Both are equivalent.

______________________________________________________________________

# Generic Arrays

```typescript
function first<T>(
    items: T[]
): T {

    return items[0];

}
```

Usage

```typescript
const value =
    first([1, 2, 3]);
```

Result

```
number
```

______________________________________________________________________

Another example

```typescript
const name =
    first([
        "Alice",
        "Bob"
    ]);
```

Result

```
string
```

______________________________________________________________________

# Generic Interface

```typescript
interface ApiResponse<T> {

    success: boolean;

    data: T;

}
```

Usage

```typescript
interface User {

    id: number;

    name: string;

}
```

```typescript
const response:

ApiResponse<User> = {

    success: true,

    data: {

        id: 1,

        name: "Alice"

    }

};
```

______________________________________________________________________

# Why Generic Interfaces?

Instead of creating

```typescript
UserResponse

OrderResponse

ProductResponse
```

One generic interface works for all.

______________________________________________________________________

# Generic Class

```typescript
class Box<T> {

    constructor(

        public value: T

    ) {}

}
```

Usage

```typescript
const box =
    new Box<string>(
        "Hello"
    );
```

Another

```typescript
const numberBox =
    new Box<number>(
        100
    );
```

______________________________________________________________________

# Multiple Generic Types

```typescript
class Pair<K, V> {

    constructor(

        public key: K,

        public value: V

    ) {}

}
```

Usage

```typescript
const pair =

    new Pair<number, string>(

        1,

        "Alice"

    );
```

______________________________________________________________________

# Generic Type Alias

```typescript
type Result<T> = {

    success: boolean;

    data: T;

};
```

Usage

```typescript
type User = {

    id: number;

};
```

```typescript
const response:

Result<User> = {

    success: true,

    data: {

        id: 10

    }

};
```

______________________________________________________________________

# Generic Constraints

Sometimes we want to restrict allowed types.

Example

```typescript
function printLength<T>(
    value: T
) {

    console.log(
        value.length
    );

}
```

Compilation Error.

Not every type has

```
length
```

______________________________________________________________________

# extends Constraint

```typescript
interface HasLength {

    length: number;

}
```

```typescript
function printLength

<T extends HasLength>(

    value: T

) {

    console.log(

        value.length

    );

}
```

Allowed

```typescript
printLength("Hello");

printLength([1,2,3]);
```

Not allowed

```typescript
printLength(100);
```

Compilation Error.

______________________________________________________________________

# Generic with keyof

Very common interview topic.

```typescript
interface User {

    id: number;

    name: string;

}
```

```typescript
function getValue<

    T,

    K extends keyof T

>(

    object: T,

    key: K

) {

    return object[key];

}
```

Usage

```typescript
const user = {

    id: 1,

    name: "Alice"

};
```

```typescript
getValue(
    user,
    "name"
);
```

Wrong

```typescript
getValue(
    user,
    "salary"
);
```

Compilation Error.

______________________________________________________________________

# Generic Repository

Very common backend example.

```typescript
interface Repository<T> {

    findById(
        id: number
    ): T;

    save(
        entity: T
    ): void;

}
```

Implementation

```typescript
interface User {

    id: number;

    name: string;

}
```

```typescript
class UserRepository

implements Repository<User> {

    findById(

        id: number

    ): User {

        return {

            id,

            name: "Alice"

        };

    }

    save(

        entity: User

    ): void {

        console.log(entity);

    }

}
```

Exactly how many backend libraries are designed.

______________________________________________________________________

# Generic Utility Function

```typescript
function wrap<T>(
    value: T
) {

    return {

        value

    };

}
```

Usage

```typescript
const user =
    wrap("Alice");
```

Result

```typescript
{
    value: "Alice"
}
```

______________________________________________________________________

# Generic API Response

Common backend pattern.

```typescript
type ApiResponse<T> = {

    success: boolean;

    data: T;

    message: string;

};
```

User

```typescript
interface User {

    id: number;

    name: string;

}
```

Usage

```typescript
const response:

ApiResponse<User> = {

    success: true,

    message: "Success",

    data: {

        id: 1,

        name: "Alice"

    }

};
```

______________________________________________________________________

# Generic Defaults

Provide default types.

```typescript
interface ApiResponse<T = string> {

    data: T;

}
```

Now

```typescript
ApiResponse
```

automatically means

```typescript
ApiResponse<string>
```

unless another type is supplied.

______________________________________________________________________

# Generic Constraints with Classes

```typescript
class Animal {

    speak() {}

}
```

```typescript
function print<

T extends Animal

>(

    animal: T

) {

    animal.speak();

}
```

Only subclasses of

```
Animal
```

are accepted.

______________________________________________________________________

# Conditional Generic (Overview)

A glimpse of an advanced feature.

```typescript
type Id<T> =

    T extends string

        ? string

        : number;
```

Conditional types are extremely powerful but are beyond the scope of this crash course.

______________________________________________________________________

# Real Backend Example

Repository

```typescript
interface Repository<T> {

    findAll(): T[];

}
```

Service

```typescript
class Service<T> {

    constructor(

        private repository:

        Repository<T>

    ) {}

    getAll() {

        return this.repository.findAll();

    }

}
```

Notice

One service works for

- Users
- Orders
- Products
- Payments

Only the type changes.

______________________________________________________________________

# Common Mistakes

## Using any Instead of Generics

Wrong

```typescript
function get(

    value: any

)
```

Better

```typescript
function get<T>(

    value: T

)
```

______________________________________________________________________

## Overusing Generics

Bad

```typescript
<T,U,V,W,X,Y>
```

Keep generic APIs simple.

______________________________________________________________________

## Forgetting Constraints

Wrong

```typescript
value.length
```

Without ensuring

```
length
```

exists.

______________________________________________________________________

## Naming Generics Poorly

Good

```typescript
T

K

V
```

Sometimes

```typescript
TUser

TResponse
```

improves readability.

______________________________________________________________________

# Best Practices

✅ Prefer Generics over `any`.

✅ Let TypeScript infer generic types when possible.

✅ Use `extends` to constrain types.

✅ Use `keyof` with Generics for property-safe APIs.

✅ Keep generic APIs simple and readable.

______________________________________________________________________

# Interview Deep Dive

## Question

What are Generics?

### Answer

Generics allow functions, classes, interfaces, and type aliases to work with different data types while preserving
compile-time type safety. They make code reusable without sacrificing strong typing.

______________________________________________________________________

## Question

Why should Generics be preferred over `any`?

### Answer

`any` disables type checking, allowing invalid operations that may fail at runtime. Generics preserve the specific type
information throughout the function or class, enabling compile-time validation and better IDE support.

______________________________________________________________________

## Question

What is a generic constraint?

### Answer

A generic constraint restricts the types that can be used with a generic parameter. Using `extends`, you can require
that a type provides certain properties or methods before it is accepted.

______________________________________________________________________

## Question

What is the purpose of `K extends keyof T`?

### Answer

`K extends keyof T` ensures that the second generic parameter is a valid property name of the first type. This enables
type-safe property access while preventing invalid keys at compile time.

______________________________________________________________________

## Question

Where are Generics commonly used in backend development?

### Answer

Generics are widely used in repositories, services, API response wrappers, database clients, HTTP libraries like Axios,
ORM frameworks, and reusable utility functions that operate on different data models.

______________________________________________________________________

# Practice Questions

1. What are Generics?
1. Why are Generics preferred over `any`?
1. What is a generic function?
1. What is a generic interface?
1. What is a generic class?
1. What are generic constraints?
1. What does `extends` do in Generics?
1. Explain `K extends keyof T`.
1. When should generic defaults be used?
1. Give a real-world backend use case for Generics.

______________________________________________________________________

# Summary

Generics allow you to build reusable, type-safe abstractions without sacrificing readability.

In this chapter, you learned:

- Generic functions
- Generic interfaces
- Generic classes
- Generic type aliases
- Multiple generic parameters
- Generic constraints
- `extends`
- `keyof`
- Generic repositories
- Generic API responses
- Generic defaults
- Backend design patterns

Generics are used throughout modern TypeScript libraries and frameworks. Once you become comfortable with them, you'll
find that much of the TypeScript ecosystem becomes easier to understand and work with.

______________________________________________________________________

# Next

[Modules & Project Structure](06-modules-project-structure.md)
