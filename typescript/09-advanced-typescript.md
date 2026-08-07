# Advanced TypeScript Features

TypeScript includes several built-in utility types that make working with complex objects much easier.

Instead of rewriting object types,

you can transform existing ones.

These utility types are heavily used in:

- NestJS
- Prisma
- TypeORM
- Express
- React
- Internal TypeScript libraries

Understanding them is essential for reading modern TypeScript code.

______________________________________________________________________

# Why Utility Types?

Suppose we have

```typescript
interface User {

    id: number;

    name: string;

    email: string;

    age: number;

}
```

Now we need

- Create User
- Update User
- User Summary
- Public User

Instead of creating four new interfaces,

TypeScript provides utility types.

______________________________________________________________________

# Partial<T>

Makes every property optional.

```typescript
interface User {

    id: number;

    name: string;

    email: string;

}
```

```typescript
type UpdateUser =

Partial<User>;
```

Equivalent

```typescript
{

    id?: number;

    name?: string;

    email?: string;

}
```

______________________________________________________________________

Backend Example

PATCH request

```typescript
function updateUser(

    id: number,

    data: Partial<User>

) {

}
```

Now

```typescript
updateUser(

    1,

    {

        email:

        "new@email.com"

    }

);
```

Perfect.

______________________________________________________________________

# Required<T>

Opposite of

```
Partial
```

Makes every property required.

```typescript
interface User {

    id?: number;

    name?: string;

}
```

```typescript
type FullUser =

Required<User>;
```

Now

```typescript
{

    id: number;

    name: string;

}
```

______________________________________________________________________

# Readonly<T>

Every property becomes read-only.

```typescript
type ImmutableUser =

Readonly<User>;
```

Now

```typescript
user.name = "Bob";
```

Compilation Error.

______________________________________________________________________

# Pick\<T, K>

Select specific properties.

```typescript
interface User {

    id: number;

    name: string;

    email: string;

    age: number;

}
```

```typescript
type UserSummary =

Pick<

    User,

    "id"

    |

    "name"

>;
```

Equivalent

```typescript
{

    id: number;

    name: string;

}
```

______________________________________________________________________

Backend Example

API

```typescript
GET /users
```

May only return

```
id

name
```

Instead of entire user object.

______________________________________________________________________

# Omit\<T, K>

Removes selected properties.

```typescript
type PublicUser =

Omit<

    User,

    "password"

>;
```

Very common.

______________________________________________________________________

Real Example

```typescript
interface User {

    id: number;

    email: string;

    password: string;

}
```

API Response

```typescript
type UserResponse =

Omit<

    User,

    "password"

>;
```

Never expose passwords.

______________________________________________________________________

# Record\<K, V>

Already introduced,

but worth revisiting.

```typescript
type Scores =

Record<

    string,

    number

>;
```

Usage

```typescript
const scores:

Scores = {

    Alice: 90,

    Bob: 80

};
```

______________________________________________________________________

# Exclude\<T, U>

Removes types.

```typescript
type Role =

"ADMIN"

|

"USER"

|

"GUEST";
```

```typescript
type InternalRole =

Exclude<

    Role,

    "GUEST"

>;
```

Result

```typescript
"ADMIN"

|

"USER"
```

______________________________________________________________________

# Extract\<T, U>

Keeps only matching types.

```typescript
type Role =

"ADMIN"

|

"USER"

|

"GUEST";
```

```typescript
type Guest =

Extract<

    Role,

    "GUEST"

>;
```

Result

```
"GUEST"
```

______________________________________________________________________

# NonNullable<T>

Removes

```
null

undefined
```

Example

```typescript
type Value =

string

|

null

|

undefined;
```

```typescript
type SafeValue =

NonNullable<Value>;
```

Result

```
string
```

______________________________________________________________________

# ReturnType<T>

Extracts function return type.

```typescript
function createUser() {

    return {

        id: 1,

        name: "Alice"

    };

}
```

```typescript
type User =

ReturnType<

    typeof createUser

>;
```

Now

```
User
```

matches the function automatically.

______________________________________________________________________

# Parameters<T>

Gets function parameters.

```typescript
function login(

    username: string,

    password: string

) {}
```

```typescript
type LoginArgs =

Parameters<

    typeof login

>;
```

Equivalent

```typescript
[

    string,

    string

]
```

______________________________________________________________________

# ConstructorParameters<T>

Works with constructors.

```typescript
class User {

    constructor(

        public id: number,

        public name: string

    ) {}

}
```

```typescript
type Args =

ConstructorParameters<

typeof User

>;
```

Result

```typescript
[

    number,

    string

]
```

______________________________________________________________________

# InstanceType<T>

Gets instance type.

```typescript
class User {

}
```

```typescript
type UserType =

InstanceType<

typeof User

>;
```

Equivalent

```
User
```

______________________________________________________________________

# Awaited<T>

Extracts Promise result.

```typescript
async function getUser() {

    return {

        id: 1

    };

}
```

```typescript
type User =

Awaited<

ReturnType<

typeof getUser

>

>;
```

Result

```
{

    id: number

}
```

Very useful.

______________________________________________________________________

# Template Literal Types

Create types from strings.

```typescript
type Method =

"GET"

|

"POST";
```

```typescript
type Endpoint =

`${Method}_USER`;
```

Result

```
GET_USER

POST_USER
```

______________________________________________________________________

# Mapped Types

Transform every property.

```typescript
type ReadonlyUser = {

    readonly

    [

        K in keyof User

    ]:

    User[K];

};
```

Equivalent

```typescript
Readonly<User>
```

Utility types are built using mapped types.

______________________________________________________________________

# Conditional Types

```typescript
type Id<T> =

T extends string

?

string

:

number;
```

Usage

```typescript
type A =

Id<string>;
```

Result

```
string
```

______________________________________________________________________

# infer Keyword (Overview)

```typescript
type Return<T> =

T extends (

...args:any

)

=>

infer R

?

R

:

never;
```

TypeScript uses

```
infer
```

internally for many utility types.

Advanced topic,

but useful to recognize.

______________________________________________________________________

# Combining Utility Types

Example

```typescript
type UserUpdate =

Partial<

Pick<

User,

"name"

|

"email"

>

>;
```

Equivalent

```typescript
{

    name?: string;

    email?: string;

}
```

______________________________________________________________________

# Backend Example

DTO

```typescript
interface User {

    id: number;

    name: string;

    email: string;

    password: string;

}
```

Create DTO

```typescript
type CreateUser =

Omit<

User,

"id"

>;
```

Update DTO

```typescript
type UpdateUser =

Partial<

CreateUser

>;
```

Public DTO

```typescript
type PublicUser =

Omit<

User,

"password"

>;
```

One interface,

three DTOs.

Exactly how many backend frameworks are designed.

______________________________________________________________________

# Utility Type Summary

| Utility Type | Purpose |
|--------------|---------|
| `Partial<T>` | Make all properties optional |
| `Required<T>` | Make all properties required |
| `Readonly<T>` | Prevent modification |
| `Pick<T, K>` | Select properties |
| `Omit<T, K>` | Remove properties |
| `Record<K, V>` | Typed dictionary |
| `Exclude<T, U>` | Remove union members |
| `Extract<T, U>` | Keep matching union members |
| `NonNullable<T>` | Remove `null` and `undefined` |
| `ReturnType<T>` | Function return type |
| `Parameters<T>` | Function parameters |
| `ConstructorParameters<T>` | Constructor arguments |
| `InstanceType<T>` | Class instance type |
| `Awaited<T>` | Promise result type |

______________________________________________________________________

# Common Mistakes

## Creating Duplicate Interfaces

Wrong

```typescript
User

UserDto

UserSummary

UpdateUser

CreateUser
```

Prefer utility types.

______________________________________________________________________

## Forgetting Partial

PATCH requests

should almost always use

```typescript
Partial
```

______________________________________________________________________

## Returning Passwords

Always

```typescript
Omit<

User,

"password"

>
```

______________________________________________________________________

## Using any

Instead of

```typescript
any
```

use

```typescript
ReturnType

Parameters

Awaited
```

to infer types.

______________________________________________________________________

# Best Practices

✅ Use `Partial` for update DTOs.

✅ Use `Omit` to remove sensitive fields.

✅ Use `Pick` for lightweight API responses.

✅ Use `ReturnType` instead of duplicating return types.

✅ Use `Awaited` for async functions.

✅ Combine utility types when appropriate.

______________________________________________________________________

# Interview Deep Dive

## Question

What is `Partial<T>`?

### Answer

`Partial<T>` creates a new type where every property of `T` becomes optional. It is commonly used for update operations
such as HTTP PATCH requests.

______________________________________________________________________

## Question

What is the difference between `Pick<T, K>` and `Omit<T, K>`?

### Answer

`Pick<T, K>` creates a type containing only the selected properties.

`Omit<T, K>` creates a type by removing the specified properties from the original type.

______________________________________________________________________

## Question

Why is `Omit` commonly used in backend APIs?

### Answer

`Omit` is frequently used to exclude sensitive fields such as passwords, internal identifiers, or audit information
before returning objects to clients.

______________________________________________________________________

## Question

What does `ReturnType<T>` do?

### Answer

`ReturnType<T>` extracts the return type of a function, allowing developers to reuse inferred types instead of manually
duplicating them.

______________________________________________________________________

## Question

What is `Awaited<T>`?

### Answer

`Awaited<T>` extracts the resolved value type of a Promise. It is useful when working with asynchronous functions and
generic utilities that operate on Promise results.

______________________________________________________________________

# Practice Questions

1. What is `Partial<T>`?
1. What is `Required<T>`?
1. What is `Readonly<T>`?
1. What is the difference between `Pick` and `Omit`?
1. What does `Exclude<T, U>` do?
1. What does `Extract<T, U>` do?
1. What is `ReturnType<T>`?
1. What is `Parameters<T>`?
1. What is `Awaited<T>`?
1. How are utility types commonly used in backend DTOs?

______________________________________________________________________

# Summary

Utility types eliminate repetitive code while making TypeScript applications more expressive and maintainable.

In this chapter, you learned:

- `Partial`
- `Required`
- `Readonly`
- `Pick`
- `Omit`
- `Record`
- `Exclude`
- `Extract`
- `NonNullable`
- `ReturnType`
- `Parameters`
- `ConstructorParameters`
- `InstanceType`
- `Awaited`
- Template literal types
- Mapped types
- Conditional types
- Practical DTO design

These utility types are used throughout modern TypeScript codebases and are especially common in backend frameworks like
NestJS, Prisma, and TypeORM.

______________________________________________________________________

# Next

[Decorators & Metadata](10-decorators.md)
