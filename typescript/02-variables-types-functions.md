# Variables, Types & Functions

Variables, types, and functions form the foundation of TypeScript.

Unlike JavaScript, TypeScript allows us to explicitly define the type of data each variable can hold.

This enables:

- Better autocomplete
- Compile-time error checking
- Safer refactoring
- More readable code

______________________________________________________________________

# Variable Declaration

TypeScript supports three ways to declare variables.

```typescript
var
let
const
```

In modern TypeScript,

always prefer

```
let

const
```

Avoid

```
var
```

______________________________________________________________________

# var

Example

```typescript
var name = "Alice";

console.log(name);
```

Problems with `var`

- Function scoped
- Can be redeclared
- Can cause unexpected bugs

Example

```typescript
var value = 10;

var value = 20;

console.log(value);
```

Output

```
20
```

Avoid using `var` in modern code.

______________________________________________________________________

# let

```typescript
let age = 25;

age = 26;
```

Allowed.

Cannot redeclare.

```typescript
let age = 25;

let age = 30;
```

Compilation Error

______________________________________________________________________

# const

```typescript
const company = "OpenAI";
```

Cannot reassign.

```typescript
company = "Google";
```

Compilation Error

Always use `const` unless the value must change.

______________________________________________________________________

# Type Inference

TypeScript usually figures out the type automatically.

```typescript
let age = 25;
```

Equivalent to

```typescript
let age: number = 25;
```

The compiler inferred the type.

______________________________________________________________________

# Explicit Types

You can explicitly specify types.

```typescript
let username: string = "Riyaz";

let age: number = 30;

let active: boolean = true;
```

This improves readability in many cases.

______________________________________________________________________

# Primitive Types

The most common primitive types are:

```typescript
string

number

boolean

bigint

symbol

null

undefined
```

______________________________________________________________________

# string

```typescript
let language: string = "TypeScript";
```

String interpolation

```typescript
const name = "Alice";

console.log(`Hello ${name}`);
```

Output

```
Hello Alice
```

______________________________________________________________________

# number

Unlike Java,

TypeScript has a single numeric type.

```typescript
let age: number = 30;

let price: number = 99.99;
```

Both integers and floating-point numbers use `number`.

______________________________________________________________________

# boolean

```typescript
let isAdmin: boolean = true;

let isLoggedIn: boolean = false;
```

______________________________________________________________________

# null

```typescript
let value: null = null;
```

Represents an intentional empty value.

______________________________________________________________________

# undefined

```typescript
let value: undefined = undefined;
```

Usually means a value hasn't been assigned.

______________________________________________________________________

# any

One of the most discussed TypeScript types.

```typescript
let value: any;

value = 10;

value = "Hello";

value = true;
```

Everything is allowed.

______________________________________________________________________

Why avoid `any`?

The compiler stops checking types.

Example

```typescript
let user: any = "Alice";

user.run();
```

No compilation error.

Runtime failure.

______________________________________________________________________

# unknown

Safer alternative to `any`.

```typescript
let value: unknown;

value = 10;

value = "Hello";
```

Cannot use it directly.

Wrong

```typescript
value.toUpperCase();
```

Compilation Error

Need type checking first.

```typescript
if (typeof value === "string") {

    console.log(value.toUpperCase());

}
```

Much safer.

______________________________________________________________________

# any vs unknown

| any | unknown |
|------|----------|
| No type checking | Type checking required |
| Unsafe | Safe |
| Avoid when possible | Preferred |

Interview favorite.

______________________________________________________________________

# void

Used for functions that don't return anything.

```typescript
function printMessage(): void {

    console.log("Hello");

}
```

______________________________________________________________________

# never

Represents values that never occur.

Example

```typescript
function throwError(): never {

    throw new Error("Something went wrong");

}
```

Also used for infinite loops.

```typescript
function loopForever(): never {

    while (true) {

    }

}
```

______________________________________________________________________

# Arrays

Array of strings

```typescript
const names: string[] = [
    "Alice",
    "Bob"
];
```

Alternative syntax

```typescript
const names: Array<string> = [
    "Alice",
    "Bob"
];
```

Both are equivalent.

______________________________________________________________________

# Number Array

```typescript
const scores: number[] = [
    10,
    20,
    30
];
```

______________________________________________________________________

# Array Operations

```typescript
const numbers = [1, 2, 3];

numbers.push(4);

numbers.pop();

numbers.length;
```

______________________________________________________________________

# Readonly Array

```typescript
const names: readonly string[] = [
    "Alice",
    "Bob"
];
```

Now

```typescript
names.push("Charlie");
```

Compilation Error.

______________________________________________________________________

# Tuples

A tuple has a fixed number of elements with fixed types.

```typescript
let employee: [number, string];

employee = [1, "Alice"];
```

Wrong

```typescript
employee = ["Alice", 1];
```

Compilation Error.

______________________________________________________________________

Real-world example

```typescript
type ApiResponse = [
    number,
    string
];

const response: ApiResponse = [
    200,
    "Success"
];
```

______________________________________________________________________

# Enum

Enums represent fixed constants.

```typescript
enum Status {

    Pending,

    Processing,

    Completed

}
```

Usage

```typescript
const status = Status.Completed;
```

______________________________________________________________________

String Enum

```typescript
enum Role {

    Admin = "ADMIN",

    User = "USER"

}
```

______________________________________________________________________

# Type Alias

Create reusable types.

```typescript
type UserId = number;

let id: UserId = 100;
```

Object example

```typescript
type User = {

    id: number;

    name: string;

};
```

______________________________________________________________________

# Functions

Basic function

```typescript
function greet(name: string): string {

    return `Hello ${name}`;

}
```

Usage

```typescript
console.log(
    greet("Alice")
);
```

______________________________________________________________________

# Function Parameters

```typescript
function add(
    a: number,
    b: number
): number {

    return a + b;

}
```

______________________________________________________________________

# Optional Parameters

Use

```typescript
?
```

Example

```typescript
function greet(
    name: string,
    title?: string
) {

    console.log(name);

}
```

Allowed

```typescript
greet("Alice");

greet("Alice", "Dr.");
```

______________________________________________________________________

# Default Parameters

```typescript
function greet(
    name: string,
    title = "Mr."
) {

    console.log(title, name);

}
```

Usage

```typescript
greet("John");
```

Output

```
Mr. John
```

______________________________________________________________________

# Rest Parameters

Collect multiple arguments.

```typescript
function sum(
    ...numbers: number[]
): number {

    return numbers.reduce(
        (a, b) => a + b,
        0
    );

}
```

Usage

```typescript
sum(1, 2, 3, 4);
```

Output

```
10
```

______________________________________________________________________

# Arrow Functions

Traditional

```typescript
function square(
    x: number
): number {

    return x * x;

}
```

Arrow

```typescript
const square =
    (x: number): number => x * x;
```

______________________________________________________________________

Multiple parameters

```typescript
const add =
    (a: number, b: number) => a + b;
```

______________________________________________________________________

No parameters

```typescript
const hello =
    () => console.log("Hello");
```

______________________________________________________________________

# Function Type

Functions can be assigned to variables.

```typescript
let operation:
    (a: number, b: number) => number;
```

Assignment

```typescript
operation =
    (a, b) => a + b;
```

______________________________________________________________________

# Union Types

A variable can hold multiple types.

```typescript
let id:
    string | number;

id = 100;

id = "EMP001";
```

Very common in APIs.

______________________________________________________________________

# Literal Types

Restrict values.

```typescript
let method:

    "GET"

    | "POST"

    | "PUT"

    | "DELETE";
```

Now

```typescript
method = "PATCH";
```

Compilation Error.

______________________________________________________________________

# Backend Example

API request

```typescript
type HttpMethod =
    "GET"
    | "POST"
    | "PUT"
    | "DELETE";

function request(
    method: HttpMethod
) {

    console.log(method);

}
```

Usage

```typescript
request("GET");
```

______________________________________________________________________

# Common Mistakes

## Using any Everywhere

Wrong

```typescript
let user: any;
```

Prefer

```typescript
unknown
```

or proper types.

______________________________________________________________________

## Using var

Prefer

```typescript
let

const
```

______________________________________________________________________

## Forgetting Return Types

Instead of

```typescript
function add(a, b) {

}
```

Write

```typescript
function add(
    a: number,
    b: number
): number {

}
```

______________________________________________________________________

## Using Mutable Arrays

If values shouldn't change,

use

```typescript
readonly
```

______________________________________________________________________

# Best Practices

✅ Prefer `const` over `let`.

✅ Avoid `var`.

✅ Avoid `any`.

✅ Prefer `unknown` when type is uncertain.

✅ Use explicit types in public APIs.

✅ Use arrow functions for callbacks and short functions.

✅ Use type aliases for reusable types.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between `any` and `unknown`?

### Answer

`any` disables TypeScript's type checking, allowing any operation on the value without compiler errors. This can lead to
runtime failures.

`unknown` is a safer alternative that requires the developer to perform type checking or narrowing before using the
value. It preserves type safety while still allowing unknown data.

______________________________________________________________________

## Question

What is the difference between `let`, `const`, and `var`?

### Answer

`var` is function-scoped, allows redeclaration, and can lead to confusing behavior, making it unsuitable for modern
TypeScript.

`let` is block-scoped and allows reassignment but not redeclaration.

`const` is also block-scoped but does not allow reassignment, making it the preferred choice for values that should not
change.

______________________________________________________________________

## Question

What is a tuple?

### Answer

A tuple is an array with a fixed number of elements where each position has a predefined type. Unlike regular arrays,
tuples enforce both the order and type of each element.

______________________________________________________________________

## Question

What is a type alias?

### Answer

A type alias creates a reusable name for a type. It can represent primitive types, object shapes, unions, tuples, or
other complex types, improving readability and reducing duplication.

______________________________________________________________________

## Question

When should you use union types?

### Answer

Union types are useful when a value can legitimately have more than one type, such as an API identifier that may be
either a numeric database ID or a string UUID.

______________________________________________________________________

# Practice Questions

1. What is type inference?
1. What is the difference between `let`, `const`, and `var`?
1. What is the difference between `any` and `unknown`?
1. What is the purpose of the `never` type?
1. What is a tuple?
1. What is a type alias?
1. What are optional parameters?
1. What are rest parameters?
1. What are union types?
1. When should you use literal types?

______________________________________________________________________

# Summary

Variables, types, and functions are the building blocks of every TypeScript application.

In this chapter, you learned:

- Variable declarations
- Primitive types
- `any`, `unknown`, `void`, and `never`
- Arrays
- Readonly arrays
- Tuples
- Enums
- Type aliases
- Functions
- Optional and default parameters
- Rest parameters
- Arrow functions
- Union types
- Literal types

These concepts form the foundation of writing type-safe TypeScript code. The next chapter introduces objects,
interfaces, and classes—the core tools for building maintainable backend applications.

______________________________________________________________________

# Next

[Objects, Interfaces & Classes](03-objects-interfaces-classes.md)
