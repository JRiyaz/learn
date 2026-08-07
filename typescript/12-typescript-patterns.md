# TypeScript Patterns

As applications grow, simply writing functions and classes isn't enough.

We need **design patterns** that help us build applications that are:

- Maintainable
- Testable
- Scalable
- Easy to extend

Most enterprise TypeScript applications—including NestJS, Express, Prisma, and TypeORM—use these patterns extensively.

> **Note**
>
> These are practical backend patterns, not academic design patterns.

______________________________________________________________________

# Why Design Patterns?

Imagine an application with:

- 50 APIs
- 20 developers
- 100 database tables

Without structure

```
Controller

↓

Database
```

becomes difficult to maintain.

Instead

```
Controller

↓

Service

↓

Repository

↓

Database
```

Each layer has one responsibility.

______________________________________________________________________

# Layered Architecture

Most backend applications follow this flow.

```
HTTP Request

↓

Controller

↓

Service

↓

Repository

↓

Database
```

Each layer should know only about the layer directly below it.

______________________________________________________________________

# Controller Pattern

Controllers handle HTTP.

Responsibilities

- Receive request
- Validate input
- Call service
- Return response

Example

```typescript
class UserController {

    constructor(

        private service:

        UserService

    ) {}

    async getUsers(

        req: Request,

        res: Response

    ) {

        const users =

            await this.service.findAll();

        res.json(users);

    }

}
```

Notice

No business logic.

______________________________________________________________________

# Service Pattern

Service contains business rules.

Example

```typescript
class UserService {

    constructor(

        private repository:

        UserRepository

    ) {}

    async findAll() {

        return this.repository.findAll();

    }

}
```

______________________________________________________________________

# Repository Pattern

Repository talks to database.

```typescript
class UserRepository {

    async findAll() {

        return database.users.findMany();

    }

}
```

Controllers never access the database directly.

______________________________________________________________________

# Why Repository Pattern?

Without repository

```
Controller

↓

Database
```

Hard to test.

Hard to replace database.

______________________________________________________________________

With repository

```
Controller

↓

Repository Interface

↓

Database
```

Easy to swap implementations.

______________________________________________________________________

# Generic Repository

Instead of writing

```
UserRepository

OrderRepository

ProductRepository
```

Use Generics.

```typescript
interface Repository<T> {

    findById(

        id: number

    ): Promise<T>;

    save(

        entity: T

    ): Promise<void>;

}
```

Reusable.

______________________________________________________________________

# DTO Pattern

DTO

\=

Data Transfer Object

Purpose

Transfer data between layers.

______________________________________________________________________

Create DTO

```typescript
interface CreateUserDto {

    name: string;

    email: string;

}
```

______________________________________________________________________

Response DTO

```typescript
interface UserResponse {

    id: number;

    name: string;

}
```

Notice

Password isn't exposed.

______________________________________________________________________

DTO vs Entity

Entity

```typescript
interface User {

    id: number;

    name: string;

    email: string;

    password: string;

}
```

DTO

```typescript
interface UserResponse {

    id: number;

    name: string;

}
```

Never expose entities directly.

______________________________________________________________________

# Factory Pattern

Creates objects.

Instead of

```typescript
new UserService();
```

Use

```typescript
class UserFactory {

    static create() {

        return new UserService();

    }

}
```

Useful when object creation becomes complex.

______________________________________________________________________

Real Example

Database connection

```typescript
const database =

DatabaseFactory.create(

    "postgres"

);
```

Later

```
Postgres

MySQL

MongoDB
```

can all be created from the same factory.

______________________________________________________________________

# Singleton Pattern

Only one instance exists.

```typescript
class Logger {

    private static instance:

    Logger;

    private constructor() {}

    static getInstance() {

        if (

            !Logger.instance

        ) {

            Logger.instance =

                new Logger();

        }

        return Logger.instance;

    }

}
```

Usage

```typescript
const logger =

Logger.getInstance();
```

Common examples

- Logger
- Configuration
- Database connection pools

______________________________________________________________________

# Builder Pattern

Useful when constructors have many parameters.

Bad

```typescript
new User(

1,

"Alice",

"alice@email.com",

true,

"ADMIN"

);
```

Builder

```typescript
class UserBuilder {

    private user = {

        id: 0,

        name: "",

        email: ""

    };

    setName(

        name: string

    ) {

        this.user.name =

            name;

        return this;

    }

    setEmail(

        email: string

    ) {

        this.user.email =

            email;

        return this;

    }

    build() {

        return this.user;

    }

}
```

Usage

```typescript
const user =

new UserBuilder()

.setName("Alice")

.setEmail(

    "alice@email.com"

)

.build();
```

Readable.

______________________________________________________________________

# Strategy Pattern

Different algorithms,

same interface.

```typescript
interface PaymentStrategy {

    pay(

        amount: number

    ): void;

}
```

Implementation

```typescript
class CardPayment

implements PaymentStrategy {

    pay(

        amount: number

    ) {

        console.log(

            "Card",

            amount

        );

    }

}
```

Another

```typescript
class PaypalPayment

implements PaymentStrategy {

    pay(

        amount: number

    ) {

        console.log(

            "Paypal",

            amount

        );

    }

}
```

Runtime selection.

______________________________________________________________________

# Dependency Injection

Instead of creating dependencies,

receive them.

Wrong

```typescript
class UserService {

    private repository =

        new UserRepository();

}
```

Better

```typescript
class UserService {

    constructor(

        private repository:

        UserRepository

    ) {}

}
```

Benefits

- Easy testing
- Loose coupling
- Easy mocking

______________________________________________________________________

# Composition over Inheritance

Bad

```
Employee

↓

Manager

↓

SeniorManager

↓

Director
```

Deep inheritance.

______________________________________________________________________

Better

```
User

+

Permissions

+

Logger

+

Validator
```

Compose behavior.

______________________________________________________________________

# Middleware Pattern

Runs before request reaches controller.

Example

```typescript
app.use(

    authenticate

);
```

Responsibilities

- Authentication
- Logging
- Rate limiting
- Request ID
- CORS

______________________________________________________________________

# Adapter Pattern

Converts one interface into another.

Example

Old API

↓

New Service

Adapter hides differences.

Useful during migrations.

______________________________________________________________________

# Facade Pattern

Provides one simple interface.

Instead of

```typescript
paymentService

emailService

inventoryService
```

Expose

```typescript
checkoutService.checkout();
```

Internally

```
Payment

↓

Inventory

↓

Email
```

Much simpler.

______________________________________________________________________

# Observer Pattern

One event

↓

Multiple listeners.

Example

```
User Registered

↓

Send Email

↓

Create Audit Log

↓

Notify Analytics
```

Common with EventEmitter.

______________________________________________________________________

# Event-Driven Pattern

```typescript
eventEmitter.emit(

    "user.created"

);
```

Listener

```typescript
eventEmitter.on(

    "user.created",

    sendWelcomeEmail

);
```

Useful for decoupling features.

______________________________________________________________________

# Dependency Injection in NestJS

```typescript
@Injectable()

class UserService {

}
```

Injected into

```typescript
@Controller()

class UserController {

    constructor(

        private service:

        UserService

    ) {}

}
```

NestJS automatically creates dependencies.

______________________________________________________________________

# Common Architecture

```
Routes

↓

Controller

↓

Service

↓

Repository

↓

Database
```

Supporting layers

```
Middleware

Validation

DTO

Logger

Config

Utilities
```

______________________________________________________________________

# Common Mistakes

## Fat Controllers

Wrong

```typescript
Controller

↓

Business Logic

↓

Database

↓

Validation
```

Controllers should stay thin.

______________________________________________________________________

## Skipping Services

Business logic belongs in services,

not controllers.

______________________________________________________________________

## Returning Entities

Always return DTOs.

______________________________________________________________________

## Creating Dependencies with new

Prefer dependency injection.

______________________________________________________________________

## Deep Inheritance

Favor composition whenever possible.

______________________________________________________________________

# Best Practices

✅ Keep controllers thin.

✅ Put business rules in services.

✅ Keep repositories responsible only for data access.

✅ Use DTOs between layers.

✅ Prefer dependency injection.

✅ Prefer composition over inheritance.

✅ Keep patterns simple.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the Repository pattern?

### Answer

The Repository pattern abstracts database access behind a dedicated class or interface. Services interact with
repositories instead of directly querying the database, making the application easier to test, maintain, and extend.

______________________________________________________________________

## Question

Why should controllers remain thin?

### Answer

Controllers should only coordinate HTTP requests and responses. Business logic belongs in services, while persistence
logic belongs in repositories. This separation of concerns improves maintainability and testability.

______________________________________________________________________

## Question

What is Dependency Injection?

### Answer

Dependency Injection is a design pattern where a class receives its dependencies from the outside rather than creating
them itself. This reduces coupling, simplifies testing, and improves flexibility.

______________________________________________________________________

## Question

Why should DTOs be used instead of entities?

### Answer

DTOs expose only the data required for communication between layers or with API clients. They prevent leaking internal
implementation details and help avoid exposing sensitive information such as passwords.

______________________________________________________________________

## Question

Why is composition preferred over inheritance?

### Answer

Composition builds objects by combining smaller, focused components rather than relying on deep inheritance hierarchies.
It provides greater flexibility, reduces coupling, and makes behavior easier to reuse and modify.

______________________________________________________________________

# Practice Questions

1. What is the Controller pattern?
1. What is the Service pattern?
1. What is the Repository pattern?
1. What is a DTO?
1. What is Dependency Injection?
1. What is the Singleton pattern?
1. What is the Factory pattern?
1. What is the Builder pattern?
1. Why is composition preferred over inheritance?
1. What is the Observer pattern?

______________________________________________________________________

# Summary

Design patterns help organize backend applications into maintainable, testable, and scalable systems.

In this chapter, you learned:

- Layered architecture
- Controller pattern
- Service pattern
- Repository pattern
- Generic repositories
- DTO pattern
- Factory pattern
- Singleton pattern
- Builder pattern
- Strategy pattern
- Dependency Injection
- Composition over inheritance
- Middleware pattern
- Adapter pattern
- Facade pattern
- Observer pattern
- Event-driven architecture

These patterns appear in almost every modern TypeScript backend framework and are frequently discussed in backend
interviews.

______________________________________________________________________

# Next

[Common Interview Coding Patterns](13-interview-coding-patterns.md)
