# TypeScript Best Practices

Writing TypeScript that **works** is one thing.

Writing TypeScript that is **clean, scalable, maintainable, and production-ready** is another.

This chapter covers practical best practices used in modern backend applications such as:

- NestJS
- Express
- Fastify
- Prisma
- TypeORM

These practices are frequently discussed in code reviews and interviews.

______________________________________________________________________

# Enable Strict Mode

Always enable

```json
{
    "compilerOptions": {

        "strict": true

    }
}
```

Why?

It enables:

- Null checks
- Better type inference
- Safer assignments
- Earlier error detection

Never disable it for production projects.

______________________________________________________________________

# Prefer const Over let

Good

```typescript
const user = {

    name: "Alice"

};
```

Bad

```typescript
let user = {

    name: "Alice"

};
```

Rule

```
Use const

unless reassignment

is required.
```

______________________________________________________________________

# Avoid var

Never use

```typescript
var
```

Use

```typescript
let

const
```

instead.

______________________________________________________________________

# Avoid any

Bad

```typescript
function print(

    value: any

) {

}
```

Good

```typescript
function print<T>(

    value: T

) {

}
```

or

```typescript
unknown
```

______________________________________________________________________

# Prefer unknown

Instead of

```typescript
let value: any;
```

Use

```typescript
let value: unknown;
```

Then

```typescript
if (

typeof value === "string"

) {

    console.log(

        value.toUpperCase()

    );

}
```

Safer.

______________________________________________________________________

# Use Interfaces for Object Contracts

Prefer

```typescript
interface User {

    id: number;

    name: string;

}
```

Use

```
type
```

for

- Unions
- Tuples
- Advanced types

______________________________________________________________________

# Use DTOs

Instead of exposing entities

```typescript
interface User {

    id: number;

    name: string;

    password: string;

}
```

Return

```typescript
interface UserResponse {

    id: number;

    name: string;

}
```

Never expose internal models directly.

______________________________________________________________________

# Prefer Readonly

Instead of

```typescript
id: number;
```

Use

```typescript
readonly id: number;
```

when values shouldn't change.

______________________________________________________________________

# Prefer Utility Types

Instead of creating

```
UpdateUser

CreateUser

PublicUser
```

Use

```typescript
Partial<User>

Omit<User, "password">

Pick<User, "id" | "name">
```

Less duplication.

______________________________________________________________________

# Keep Functions Small

Bad

```typescript
function createUser() {

    // 200 lines

}
```

Better

```typescript
validate();

save();

sendEmail();

log();
```

Each function should have one responsibility.

______________________________________________________________________

# Keep Classes Focused

Bad

```typescript
class UserService {

    login()

    logout()

    payment()

    email()

    report()

}
```

Better

```
UserService

EmailService

PaymentService

ReportService
```

______________________________________________________________________

# Prefer Composition

Instead of

```
Manager

↓

SeniorManager

↓

Director

↓

VP
```

Prefer

```
User

+

Permissions

+

Logger

+

Validator
```

Composition is more flexible.

______________________________________________________________________

# Use Dependency Injection

Bad

```typescript
class UserService {

    private repository =

        new UserRepository();

}
```

Good

```typescript
class UserService {

    constructor(

        private repository:

        UserRepository

    ) {}

}
```

Much easier to test.

______________________________________________________________________

# Handle Errors Properly

Bad

```typescript
catch(error) {

}
```

Never ignore errors.

______________________________________________________________________

Good

```typescript
catch(error) {

    logger.error(error);

    throw error;

}
```

______________________________________________________________________

# Prefer Async/Await

Instead of

```typescript
fetch()

.then(...)

.then(...)

.catch(...);
```

Prefer

```typescript
try {

    const data =

        await fetch();

}

catch(error) {

}
```

More readable.

______________________________________________________________________

# Don't Await Independent Tasks

Bad

```typescript
const users =

await getUsers();

const orders =

await getOrders();
```

Better

```typescript
const [

    users,

    orders

] =

await Promise.all([

    getUsers(),

    getOrders()

]);
```

Faster.

______________________________________________________________________

# Avoid Magic Numbers

Bad

```typescript
if (

status === 1

)
```

Better

```typescript
enum Status {

    Active = 1

}
```

or

```typescript
const ACTIVE_STATUS = 1;
```

______________________________________________________________________

# Use Enums Sparingly

For many modern projects,

literal unions are often simpler.

Instead of

```typescript
enum Role {

    Admin,

    User

}
```

Consider

```typescript
type Role =

"ADMIN"

|

"USER";
```

Especially useful when values come from APIs.

______________________________________________________________________

# Avoid Deep Nesting

Bad

```typescript
if(a){

    if(b){

        if(c){

        }

    }

}
```

Better

```typescript
if(!a) return;

if(!b) return;

if(!c) return;
```

Guard clauses improve readability.

______________________________________________________________________

# Name Things Clearly

Bad

```typescript
const x = 10;
```

Better

```typescript
const maxRetries = 10;
```

Names should explain intent.

______________________________________________________________________

# Organize Folders

Bad

```
utils.ts

↓

5000 lines
```

Better

```
utils/

logger.ts

date.ts

jwt.ts

hash.ts
```

______________________________________________________________________

# Keep Controllers Thin

Wrong

```typescript
Controller

↓

Validation

↓

Business Logic

↓

Database
```

Correct

```
Controller

↓

Service

↓

Repository
```

______________________________________________________________________

# Validate Input

Never trust incoming data.

Bad

```typescript
const email =

req.body.email;
```

Better

Validate before use.

Frameworks like NestJS often use validation libraries to enforce DTO rules.

______________________________________________________________________

# Avoid Duplicate Types

Bad

```typescript
User

UserDto

UserResponse

UpdateUser

CreateUser
```

Prefer utility types.

______________________________________________________________________

# Avoid Type Assertions

Bad

```typescript
const user =

data as User;
```

Prefer

Type Guards

or validation.

______________________________________________________________________

# Prefer Named Exports

Instead of

```typescript
export default
```

Prefer

```typescript
export
```

Benefits

- Easier refactoring
- Better autocomplete
- Consistent imports

______________________________________________________________________

# Use Path Aliases

Instead of

```typescript
../../../../services
```

Use

```typescript
@services/user
```

Much cleaner.

______________________________________________________________________

# Logging

Avoid

```typescript
console.log();
```

Prefer

```typescript
logger.info();

logger.warn();

logger.error();
```

Structured logging is essential in production.

______________________________________________________________________

# Configuration

Don't use

```typescript
process.env.PORT
```

throughout the application.

Create

```typescript
config.ts
```

Example

```typescript
export const config = {

    port:

    Number(

        process.env.PORT

    ) || 3000

};
```

______________________________________________________________________

# Consistent API Responses

Good

```typescript
{

    success: true,

    data: user

}
```

Error

```typescript
{

    success: false,

    message:

    "User not found"

}
```

Consistency simplifies frontend integration.

______________________________________________________________________

# Avoid Duplicate Business Logic

Instead of

```
Controller A

↓

Validation
```

and

```
Controller B

↓

Same Validation
```

Move shared logic into services or utility functions.

______________________________________________________________________

# Prefer Immutability

Bad

```typescript
user.name = "Bob";
```

Better

```typescript
const updatedUser = {

    ...user,

    name: "Bob"

};
```

Immutable updates reduce side effects.

______________________________________________________________________

# Write Self-Documenting Code

Bad

```typescript
calculate(a,b,c);
```

Better

```typescript
calculateInvoiceTotal(

subtotal,

tax,

discount

);
```

Good naming reduces the need for comments.

______________________________________________________________________

# Common Mistakes

## Using any Everywhere

Loses all benefits of TypeScript.

______________________________________________________________________

## Massive Controllers

Controllers should coordinate,

not implement business rules.

______________________________________________________________________

## Ignoring Strict Mode

Many bugs disappear before runtime when strict mode is enabled.

______________________________________________________________________

## Returning Database Entities

Always map entities to DTOs before sending responses.

______________________________________________________________________

## Mixing Responsibilities

A single class should have one clear responsibility.

______________________________________________________________________

# Production Checklist

Before shipping a TypeScript backend application:

- ✅ Strict mode enabled
- ✅ No unnecessary `any`
- ✅ DTOs for API requests/responses
- ✅ Thin controllers
- ✅ Business logic in services
- ✅ Repository layer for persistence
- ✅ Structured logging
- ✅ Centralized configuration
- ✅ Proper async error handling
- ✅ Consistent API responses
- ✅ Path aliases configured
- ✅ Utility types used where appropriate

______________________________________________________________________

# Interview Deep Dive

## Question

Why should `any` be avoided?

### Answer

`any` disables TypeScript's type checking, removing one of the language's biggest advantages. It allows invalid
operations that may fail at runtime and reduces IDE assistance such as autocomplete and refactoring support.

______________________________________________________________________

## Question

Why should controllers remain thin?

### Answer

Controllers should only receive requests, delegate work to services, and return responses. Keeping controllers thin
improves readability, testing, and separation of concerns.

______________________________________________________________________

## Question

Why is strict mode important?

### Answer

Strict mode enables additional compile-time checks that catch common programming mistakes early, including null
handling, unsafe assignments, and incorrect type usage.

______________________________________________________________________

## Question

Why should DTOs be used?

### Answer

DTOs define exactly what data enters and leaves an API. They help validate requests, hide internal implementation
details, and prevent sensitive information from being exposed.

______________________________________________________________________

## Question

Why is Dependency Injection considered a best practice?

### Answer

Dependency Injection reduces coupling by allowing classes to receive their dependencies instead of creating them
internally. This improves testability, flexibility, and maintainability.

______________________________________________________________________

# Practice Questions

1. Why should `strict` mode be enabled?
1. Why is `any` discouraged?
1. When should `unknown` be used?
1. Why are DTOs important?
1. Why should controllers remain thin?
1. Why is Dependency Injection beneficial?
1. Why should business logic live in services?
1. Why are utility types preferred over duplicate interfaces?
1. Why is immutable data often preferred?
1. What should a production-ready TypeScript backend include?

______________________________________________________________________

# Summary

Good TypeScript is not just about syntax—it's about building maintainable systems.

In this chapter, you learned:

- Strict mode
- Avoiding `any`
- Using `unknown`
- DTOs
- Dependency Injection
- Utility types
- Async best practices
- Error handling
- Immutability
- Folder organization
- Logging
- Configuration
- Clean architecture
- Production-ready coding practices

Following these practices will help you write cleaner code, perform better in code reviews, and build backend
applications that are easier to maintain and scale.

______________________________________________________________________

# Next

[TypeScript Interview Cheatsheet](15-typescript-interview-cheatsheet.md)
