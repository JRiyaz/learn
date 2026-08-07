# Advanced Types

One of the biggest advantages of TypeScript over JavaScript is its powerful type system.

Advanced types allow you to write APIs that are:

- Safer
- More expressive
- Easier to maintain
- Self-documenting

Many of these concepts are heavily used in frameworks like NestJS, Prisma, TypeORM, and modern backend libraries.

______________________________________________________________________

# Union Types

A variable can hold more than one type.

```typescript
let id: number | string;

id = 100;

id = "EMP001";
```

Both are valid.

______________________________________________________________________

# Why Union Types?

Backend APIs often receive IDs in different formats.

Example

```typescript
function findUser(

    id: number | string

) {

    console.log(id);

}
```

Usage

```typescript
findUser(10);

findUser("USR-100");
```

______________________________________________________________________

# Union of Objects

```typescript
type Success = {

    success: true;

    data: string;

};

type ErrorResponse = {

    success: false;

    message: string;

};

type ApiResponse =
    Success | ErrorResponse;
```

______________________________________________________________________

Usage

```typescript
const response: ApiResponse = {

    success: true,

    data: "User Created"

};
```

______________________________________________________________________

# Problem with Union Types

Consider

```typescript
let value:
    string | number;
```

Can we do

```typescript
value.toUpperCase();
```

Compilation Error.

TypeScript doesn't know whether

```
value

↓

string

or

number
```

______________________________________________________________________

# Type Narrowing

We must narrow the type first.

```typescript
if (typeof value === "string") {

    console.log(
        value.toUpperCase()
    );

}
```

Now TypeScript knows

```
value

↓

string
```

______________________________________________________________________

# typeof

Very common type guard.

```typescript
function print(

    value: string | number

) {

    if (typeof value === "string") {

        console.log(
            value.toUpperCase()
        );

    }

}
```

______________________________________________________________________

# instanceof

Used with classes.

```typescript
class User {}

class Admin {}

function print(

    person: User | Admin

) {

    if (person instanceof User) {

        console.log("User");

    }

}
```

______________________________________________________________________

# in Operator

Checks if a property exists.

```typescript
type Dog = {

    bark(): void;

};

type Cat = {

    meow(): void;

};
```

```typescript
function speak(

    animal: Dog | Cat

) {

    if ("bark" in animal) {

        animal.bark();

    }

}
```

Very common in backend code.

______________________________________________________________________

# Intersection Types

Intersection combines multiple types.

```typescript
type Person = {

    name: string;

};
```

```typescript
type Employee = {

    id: number;

};
```

Combine

```typescript
type Staff =

    Person

    &

    Employee;
```

Now

```typescript
const user: Staff = {

    name: "Alice",

    id: 100

};
```

Must satisfy both types.

______________________________________________________________________

# Union vs Intersection

Union

```
A

OR

B
```

Intersection

```
A

AND

B
```

Interview favorite.

______________________________________________________________________

# Literal Types

Restrict variables to fixed values.

```typescript
let role:

    "ADMIN"

    | "USER"

    | "MANAGER";
```

Allowed

```typescript
role = "ADMIN";
```

Wrong

```typescript
role = "CEO";
```

Compilation Error.

______________________________________________________________________

# Backend Example

```typescript
type HttpMethod =

    "GET"

    | "POST"

    | "PUT"

    | "DELETE";
```

Usage

```typescript
function request(

    method: HttpMethod

) {

}
```

Only valid HTTP methods are accepted.

______________________________________________________________________

# keyof

Returns property names as a union.

```typescript
type User = {

    id: number;

    name: string;

    age: number;

};
```

```typescript
type Keys =
    keyof User;
```

Equivalent to

```typescript
"id"

|

"name"

|

"age"
```

______________________________________________________________________

Usage

```typescript
function print(

    key: keyof User

) {

}
```

Allowed

```typescript
print("name");
```

Wrong

```typescript
print("salary");
```

Compilation Error.

______________________________________________________________________

# typeof

Gets the type of a variable.

```typescript
const user = {

    id: 1,

    name: "Alice"

};
```

```typescript
type User =

    typeof user;
```

Very useful for avoiding duplicate type definitions.

______________________________________________________________________

# Indexed Access Types

Extract property types.

```typescript
type User = {

    id: number;

    name: string;

};
```

```typescript
type NameType =

    User["name"];
```

Result

```typescript
string
```

______________________________________________________________________

# Type Assertions

Tell TypeScript what the type is.

```typescript
const value: unknown =
    "Hello";
```

Assertion

```typescript
const text =

    value as string;
```

Alternative

```typescript
const text =

    <string> value;
```

Prefer

```typescript
as
```

syntax.

______________________________________________________________________

# Non-null Assertion

Sometimes TypeScript believes something could be null.

```typescript
const element =

    document.getElementById("app");
```

Use

```typescript
element!.innerHTML = "Hello";
```

The

```
!
```

means

```
I know this isn't null.
```

Use carefully.

______________________________________________________________________

# Type Guards

A type guard narrows types safely.

Example

```typescript
function print(

    value:
        string | number

) {

    if (typeof value === "string") {

        console.log(
            value.toUpperCase()
        );

    }

}
```

______________________________________________________________________

# Custom Type Guard

Very useful.

```typescript
type User = {

    name: string;

};
```

```typescript
function isUser(

    value: any

): value is User {

    return value.name !== undefined;

}
```

Usage

```typescript
if (isUser(data)) {

    console.log(
        data.name
    );

}
```

Now TypeScript understands

```
data

↓

User
```

______________________________________________________________________

# Discriminated Unions ⭐⭐⭐⭐⭐

One of the most important TypeScript interview topics.

Example

```typescript
type Circle = {

    kind: "circle";

    radius: number;

};
```

```typescript
type Rectangle = {

    kind: "rectangle";

    width: number;

    height: number;

};
```

```typescript
type Shape =

    Circle

    |

    Rectangle;
```

______________________________________________________________________

Usage

```typescript
function area(

    shape: Shape

) {

    switch (shape.kind) {

        case "circle":

            return Math.PI *
                shape.radius *
                shape.radius;

        case "rectangle":

            return shape.width *
                shape.height;

    }

}
```

TypeScript automatically narrows the type based on

```
kind
```

This pattern is widely used in APIs and state management.

______________________________________________________________________

# Optional Chaining

Instead of

```typescript
if (

    user &&

    user.address &&

    user.address.city

) {

}
```

Use

```typescript
user?.address?.city
```

Cleaner.

Safer.

______________________________________________________________________

# Nullish Coalescing

Instead of

```typescript
const name =
    user.name || "Guest";
```

Use

```typescript
const name =
    user.name ?? "Guest";
```

Difference

```
||

↓

false

0

""

null

undefined
```

```
??

↓

null

undefined
```

Much safer.

______________________________________________________________________

# Optional Chaining + Nullish Coalescing

```typescript
const city =

    user?.address?.city

    ??

    "Unknown";
```

Very common in backend APIs.

______________________________________________________________________

# as const

Preserve literal values.

```typescript
const method =

    "GET" as const;
```

Without

```typescript
as const
```

Type

```
string
```

With

```typescript
as const
```

Type

```
"GET"
```

Useful for configuration objects.

______________________________________________________________________

# satisfies (TypeScript 4.9+)

Ensures an object satisfies a type **without changing the inferred type**.

```typescript
type Config = {

    port: number;

    host: string;

};
```

```typescript
const config = {

    port: 3000,

    host: "localhost"

} satisfies Config;
```

Excellent for configuration files.

______________________________________________________________________

# Backend Example

API response

```typescript
type Success = {

    success: true;

    user: {

        id: number;

        name: string;

    };

};
```

```typescript
type Failure = {

    success: false;

    error: string;

};
```

```typescript
type ApiResponse =

    Success

    |

    Failure;
```

Usage

```typescript
function handle(

    response: ApiResponse

) {

    if (response.success) {

        console.log(
            response.user.name
        );

    } else {

        console.log(
            response.error
        );

    }

}
```

Notice how TypeScript automatically narrows the type based on

```
success
```

______________________________________________________________________

# Common Mistakes

## Using Type Assertions Instead of Type Guards

Wrong

```typescript
const user =
    data as User;
```

Prefer validating first.

______________________________________________________________________

## Overusing Union Types

Large unions become difficult to maintain.

Consider interfaces or discriminated unions.

______________________________________________________________________

## Using ||

Wrong

```typescript
const port =
    config.port || 3000;
```

If

```
port = 0
```

Wrong result.

Better

```typescript
config.port ?? 3000;
```

______________________________________________________________________

## Ignoring keyof

Avoid

```typescript
function get(

    property: string

)
```

Prefer

```typescript
keyof
```

______________________________________________________________________

# Best Practices

✅ Prefer discriminated unions.

✅ Use `keyof` for property-safe APIs.

✅ Prefer type guards over assertions.

✅ Use optional chaining.

✅ Use nullish coalescing.

✅ Prefer `unknown` over `any`.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between a union type and an intersection type?

### Answer

A union type (`A | B`) allows a value to be one of several possible types.

An intersection type (`A & B`) combines multiple types into one, requiring the value to satisfy all constituent types
simultaneously.

______________________________________________________________________

## Question

What is type narrowing?

### Answer

Type narrowing is the process of reducing a broader type, such as a union, to a more specific type using checks like
`typeof`, `instanceof`, the `in` operator, or custom type guards.

______________________________________________________________________

## Question

What is a discriminated union?

### Answer

A discriminated union is a union of object types that share a common literal property (such as `kind` or `type`).
TypeScript uses this property to automatically narrow the object's type, making code safer and easier to maintain.

______________________________________________________________________

## Question

What is the difference between `||` and `??`?

### Answer

The `||` operator treats values such as `false`, `0`, and empty strings as falsy and falls back to the default value.

The `??` operator only falls back when the value is `null` or `undefined`, making it the preferred choice for default
values in most backend applications.

______________________________________________________________________

## Question

Why is `keyof` useful?

### Answer

`keyof` creates a union of an object's property names, enabling functions to accept only valid property keys. This
improves type safety and prevents invalid property access at compile time.

______________________________________________________________________

# Practice Questions

1. What is a union type?
1. What is an intersection type?
1. What is type narrowing?
1. Explain `typeof`, `instanceof`, and the `in` operator.
1. What is a custom type guard?
1. What is a discriminated union?
1. What does `keyof` return?
1. What is the difference between `||` and `??`?
1. When should you use optional chaining?
1. What is the purpose of `satisfies`?

______________________________________________________________________

# Summary

Advanced types are what make TypeScript much more powerful than plain JavaScript.

In this chapter, you learned:

- Union types
- Intersection types
- Literal types
- Type narrowing
- `typeof`
- `instanceof`
- `in` operator
- `keyof`
- `typeof` (type queries)
- Indexed access types
- Type assertions
- Custom type guards
- Discriminated unions
- Optional chaining
- Nullish coalescing
- `as const`
- `satisfies`

These features allow you to model complex backend APIs while maintaining excellent type safety. The next chapter
introduces **Generics**, one of the most important features for building reusable services, repositories, and utility
libraries.

______________________________________________________________________

# Next

[Generics](05-generics.md)
