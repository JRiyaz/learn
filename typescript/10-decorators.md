# Decorators & Metadata

Decorators are one of the defining features of frameworks like **NestJS**.

Even if you never write your own decorators, you'll use them constantly.

Examples

```typescript
@Controller()

@Get()

@Post()

@Injectable()

@Module()
```

Understanding decorators helps you understand **how modern TypeScript backend frameworks work internally**.

> **Note:** Decorators are currently a language feature with evolving standards. Their behavior depends on the TypeScript version and project configuration. This chapter focuses on the concepts commonly used in today's backend frameworks like NestJS.

______________________________________________________________________

# What is a Decorator?

A decorator is a function that adds behavior or metadata to:

- Classes
- Methods
- Properties
- Parameters

Instead of modifying code directly,

we attach behavior externally.

Think of it as:

```
Original Class

↓

Decorator

↓

Enhanced Class
```

______________________________________________________________________

# Why Decorators?

Without decorators

```typescript
class UserController {

    getUsers() {

    }

}
```

Nothing indicates

- Route
- Authorization
- Validation
- Dependency Injection

With decorators

```typescript
@Controller("/users")

class UserController {

    @Get()

    getUsers() {

    }

}
```

Much more expressive.

______________________________________________________________________

# Enabling Decorators

In many TypeScript projects,

`tsconfig.json`

contains

```json
{

    "compilerOptions": {

        "experimentalDecorators": true

    }

}
```

Frameworks like NestJS usually configure this automatically.

______________________________________________________________________

# Class Decorator

A class decorator receives the constructor.

Example

```typescript
function Logger(

    constructor: Function

) {

    console.log(

        constructor.name

    );

}
```

Usage

```typescript
@Logger

class UserService {

}
```

Output

```
UserService
```

The decorator runs when the class is defined.

______________________________________________________________________

# How It Works

Conceptually

```typescript
@Logger

class UserService {}
```

becomes

```typescript
class UserService {}

Logger(UserService);
```

______________________________________________________________________

# Returning a New Class

A decorator can replace the original class.

```typescript
function Version(

    version: string

) {

    return function (

        constructor: Function

    ) {

        constructor.prototype.version = version;

    };

}
```

Usage

```typescript
@Version("1.0")

class UserService {

}
```

______________________________________________________________________

# Decorator Factory

Many decorators accept arguments.

Example

```typescript
@Controller("/users")
```

This is actually

```
Decorator Factory

↓

Returns

↓

Decorator
```

Example

```typescript
function Controller(

    path: string

) {

    return function (

        constructor: Function

    ) {

        console.log(path);

    };

}
```

______________________________________________________________________

# Method Decorator

Decorates methods.

```typescript
function Log(

    target: any,

    propertyKey: string,

    descriptor: PropertyDescriptor

) {

    console.log(propertyKey);

}
```

Usage

```typescript
class UserService {

    @Log

    getUsers() {

    }

}
```

Output

```
getUsers
```

______________________________________________________________________

# Modifying Methods

Example

```typescript
function Timer(

    target: any,

    propertyKey: string,

    descriptor: PropertyDescriptor

) {

    const original =

        descriptor.value;

    descriptor.value =

        function (

            ...args: any[]

        ) {

            console.time(propertyKey);

            const result =

                original.apply(

                    this,

                    args

                );

            console.timeEnd(propertyKey);

            return result;

        };

}
```

Usage

```typescript
class Service {

    @Timer

    process() {

        console.log("Running");

    }

}
```

Now execution time is logged automatically.

______________________________________________________________________

# Property Decorator

Decorates properties.

```typescript
function Required(

    target: any,

    propertyKey: string

) {

    console.log(propertyKey);

}
```

Usage

```typescript
class User {

    @Required

    name!: string;

}
```

______________________________________________________________________

# Parameter Decorator

Decorates method parameters.

```typescript
function CurrentUser(

    target: any,

    propertyKey: string,

    parameterIndex: number

) {

    console.log(

        parameterIndex

    );

}
```

Usage

```typescript
class Controller {

    get(

        @CurrentUser

        user: string

    ) {}

}
```

______________________________________________________________________

# Decorator Execution Order

Suppose

```typescript
@First

@Second

class User {}
```

Execution

```
Second

↓

First
```

The closest decorator executes first.

______________________________________________________________________

# Metadata

Decorators often attach metadata.

Example

```
Controller

↓

Route

↓

Methods

↓

Permissions
```

Frameworks read this metadata later.

______________________________________________________________________

# Reflect Metadata

Many frameworks use

```
reflect-metadata
```

to store metadata.

Install

```bash
npm install reflect-metadata
```

Import

```typescript
import "reflect-metadata";
```

______________________________________________________________________

# Defining Metadata

```typescript
Reflect.defineMetadata(

    "role",

    "ADMIN",

    UserService

);
```

______________________________________________________________________

# Reading Metadata

```typescript
const role =

Reflect.getMetadata(

    "role",

    UserService

);

console.log(role);
```

Output

```
ADMIN
```

______________________________________________________________________

# Why Metadata?

Imagine

```typescript
@Get("/users")
```

Internally

the framework stores

```
Route

↓

/users
```

Later,

when an HTTP request arrives,

the framework finds the correct method.

______________________________________________________________________

# NestJS Example

Controller

```typescript
@Controller("/users")

export class UserController {

    @Get()

    getUsers() {

    }

}
```

What NestJS internally knows

```
Controller

↓

/users

↓

GET

↓

getUsers()
```

No manual routing required.

______________________________________________________________________

# Dependency Injection

Another famous decorator.

```typescript
@Injectable()

class UserService {

}
```

This tells NestJS

```
Create

↓

Manage

↓

Inject
```

the service automatically.

______________________________________________________________________

# Module Decorator

```typescript
@Module({

    controllers: [

        UserController

    ],

    providers: [

        UserService

    ]

})
```

The framework reads this metadata to build the application.

______________________________________________________________________

# Parameter Decorator Example

NestJS

```typescript
@Get()

find(

    @Query()

    query: QueryDto

) {

}
```

The decorator tells NestJS

```
Read

↓

Query Parameters

↓

Convert

↓

Inject
```

______________________________________________________________________

# Multiple Decorators

```typescript
@Controller()

export class UserController {

    @Get()

    @Roles("ADMIN")

    @LogExecution()

    getUsers() {

    }

}
```

Each decorator contributes one responsibility.

______________________________________________________________________

# Real Backend Example

Authentication

```typescript
@UseGuards(

    JwtAuthGuard

)
```

Authorization

```typescript
@Roles(

    "ADMIN"

)
```

Validation

```typescript
@Body()
```

Request

```typescript
@Get()
```

One method,

multiple behaviors.

______________________________________________________________________

# Decorators vs Middleware

Decorators

```
Attached

to

specific

classes

or

methods
```

Middleware

```
Runs

before

requests

globally

or

per route
```

They solve different problems.

______________________________________________________________________

# Common Mistakes

## Putting Business Logic Inside Decorators

Decorators should add metadata or cross-cutting behavior.

Business logic belongs in services.

______________________________________________________________________

## Overusing Decorators

Too many decorators can make code difficult to understand.

Keep responsibilities clear.

______________________________________________________________________

## Forgetting Metadata Libraries

If using legacy decorator patterns that depend on metadata,

ensure required packages and compiler settings are configured.

______________________________________________________________________

# Best Practices

✅ Keep decorators focused on one responsibility.

✅ Use decorators for metadata and cross-cutting concerns.

✅ Keep business logic inside services.

✅ Prefer framework-provided decorators when available.

✅ Understand what a decorator does before creating custom ones.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a decorator?

### Answer

A decorator is a function that adds behavior or metadata to classes, methods, properties, or parameters. Frameworks use
decorators to implement features such as routing, dependency injection, validation, and authorization without modifying
the original class directly.

______________________________________________________________________

## Question

Why are decorators heavily used in NestJS?

### Answer

NestJS uses decorators to declare application structure declaratively. Decorators define routes, controllers, dependency
injection, modules, guards, validation, and request parameter binding. The framework reads this metadata during
application startup to configure behavior automatically.

______________________________________________________________________

## Question

What is metadata?

### Answer

Metadata is additional information attached to classes or class members. Frameworks store information such as routes,
permissions, or dependency injection configuration as metadata and later retrieve it to control runtime behavior.

______________________________________________________________________

## Question

What is the difference between a class decorator and a method decorator?

### Answer

A class decorator applies to an entire class and typically configures or enhances the class itself.

A method decorator applies to a specific method and is commonly used for routing, logging, authorization, caching, or
measuring execution time.

______________________________________________________________________

## Question

Should you create custom decorators frequently?

### Answer

Not usually. Most backend applications primarily use decorators provided by frameworks such as NestJS. Custom decorators
are useful when implementing reusable cross-cutting concerns like authorization, logging, auditing, or custom parameter
extraction.

______________________________________________________________________

# Practice Questions

1. What is a decorator?
1. Why do backend frameworks use decorators?
1. What is a decorator factory?
1. What is the difference between a class decorator and a method decorator?
1. What is metadata?
1. How does NestJS use decorators?
1. What is the purpose of `@Injectable()`?
1. What is the purpose of `@Controller()`?
1. When should custom decorators be created?
1. What is the difference between decorators and middleware?

______________________________________________________________________

# Summary

Decorators allow backend frameworks to express behavior declaratively while keeping business logic clean and focused.

In this chapter, you learned:

- What decorators are
- Why decorators exist
- Class decorators
- Method decorators
- Property decorators
- Parameter decorators
- Decorator factories
- Metadata
- Reflect Metadata
- NestJS examples
- Dependency Injection decorators
- Module decorators
- Decorator best practices

While you may rarely write complex decorators yourself, understanding how they work will help you read, debug, and
extend modern TypeScript backend frameworks such as NestJS.

______________________________________________________________________

# Next

[TypeScript for Node.js](11-nodejs-typescript.md)
