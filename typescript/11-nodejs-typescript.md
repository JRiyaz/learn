# TypeScript for Node.js

TypeScript and Node.js are one of the most popular combinations for building modern backend applications.

Frameworks like

- Express
- NestJS
- Fastify
- Hono

all commonly use TypeScript.

This chapter focuses on building production-ready Node.js applications using TypeScript.

______________________________________________________________________

# Why TypeScript for Node.js?

Node.js is JavaScript at runtime.

TypeScript improves Node.js development by providing:

- Static typing
- Better IDE support
- Safer refactoring
- Better maintainability
- Easier collaboration

______________________________________________________________________

# Typical Project Structure

```
my-api/

├── src/
│
│   ├── controllers/
│
│   ├── services/
│
│   ├── repositories/
│
│   ├── middleware/
│
│   ├── routes/
│
│   ├── models/
│
│   ├── config/
│
│   ├── utils/
│
│   └── app.ts
│
├── dist/
│
├── package.json
│
├── tsconfig.json
│
└── .env
```

This structure works well for medium and large backend projects.

______________________________________________________________________

# Required Packages

Initialize project

```bash
npm init -y
```

Install dependencies

```bash
npm install express dotenv
```

Install development dependencies

```bash
npm install -D typescript ts-node @types/node @types/express nodemon
```

______________________________________________________________________

# package.json

```json
{
  "scripts": {
    "dev": "nodemon --exec ts-node src/app.ts",
    "build": "tsc",
    "start": "node dist/app.js"
  }
}
```

Development

```bash
npm run dev
```

Production

```bash
npm run build

npm start
```

______________________________________________________________________

# Basic Express Server

```typescript
import express from "express";

const app = express();

const PORT = 3000;

app.get("/", (

    req,

    res

) => {

    res.send("Hello TypeScript");

});

app.listen(PORT, () => {

    console.log(

        `Server running on ${PORT}`

    );

});
```

______________________________________________________________________

# Express Request & Response Types

```typescript
import {

    Request,

    Response

}

from "express";
```

```typescript
app.get(

    "/users",

    (

        req: Request,

        res: Response

    ) => {

        res.json({

            success: true

        });

    }

);
```

Typing improves autocomplete and compile-time safety.

______________________________________________________________________

# Parsing JSON

```typescript
app.use(

    express.json()

);
```

Now

```typescript
req.body
```

contains parsed JSON.

______________________________________________________________________

# Route Parameters

```typescript
app.get(

    "/users/:id",

    (

        req,

        res

    ) => {

        console.log(

            req.params.id

        );

    }

);
```

______________________________________________________________________

Typed Parameters

```typescript
interface Params {

    id: string;

}
```

```typescript
app.get(

"/users/:id",

(

req:

Request<Params>,

res

) => {

    console.log(

        req.params.id

    );

});
```

______________________________________________________________________

# Query Parameters

Example

```
GET /users?page=2
```

```typescript
app.get(

    "/users",

    (

        req,

        res

    ) => {

        console.log(

            req.query.page

        );

    }

);
```

______________________________________________________________________

Typed Query

```typescript
interface Query {

    page?: string;

    limit?: string;

}
```

```typescript
Request<

{}, {}, {}, Query

>
```

______________________________________________________________________

# Request Body

DTO

```typescript
interface CreateUser {

    name: string;

    email: string;

}
```

Usage

```typescript
Request<

{}, {}, CreateUser

>
```

Now

```typescript
req.body.name
```

is strongly typed.

______________________________________________________________________

# Response Type

```typescript
interface ApiResponse {

    success: boolean;

}
```

```typescript
Response<ApiResponse>
```

Useful for large APIs.

______________________________________________________________________

# Environment Variables

Create

```
.env
```

```text
PORT=3000

DB_HOST=localhost

JWT_SECRET=my-secret
```

______________________________________________________________________

Load

```typescript
import dotenv

from "dotenv";

dotenv.config();
```

______________________________________________________________________

Access

```typescript
process.env.PORT
```

Remember

```
Everything is

string

or

undefined
```

______________________________________________________________________

# Environment Helper

Instead of

```typescript
process.env.PORT
```

everywhere,

create

```typescript
export const config = {

    port:

        Number(

            process.env.PORT

        ) || 3000

};
```

Now

```typescript
config.port
```

is type-safe.

______________________________________________________________________

# Middleware

Simple logger

```typescript
import {

    Request,

    Response,

    NextFunction

}

from "express";
```

```typescript
function logger(

    req: Request,

    res: Response,

    next: NextFunction

) {

    console.log(

        req.method,

        req.url

    );

    next();

}
```

Register

```typescript
app.use(logger);
```

______________________________________________________________________

# Error Middleware

```typescript
function errorHandler(

    err: Error,

    req: Request,

    res: Response,

    next: NextFunction

) {

    res.status(500).json({

        message:

        err.message

    });

}
```

Register last

```typescript
app.use(

    errorHandler

);
```

______________________________________________________________________

# Async Route

Wrong

```typescript
app.get(

"/users",

async (

req,

res

) => {

    throw new Error();

});
```

Unhandled errors may crash the process depending on your setup.

______________________________________________________________________

Better

```typescript
app.get(

"/users",

async (

req,

res,

next

) => {

    try {

        const users =

            await getUsers();

        res.json(users);

    }

    catch(error) {

        next(error);

    }

});
```

______________________________________________________________________

# Async Wrapper

Avoid repeating

```
try

catch
```

```typescript
const asyncHandler =

(

fn: any

) =>

(

req: Request,

res: Response,

next: NextFunction

) =>

Promise.resolve(

fn(

req,

res,

next

)

).catch(next);
```

Usage

```typescript
app.get(

"/users",

asyncHandler(

async (

req,

res

) => {

    res.json(

        await getUsers()

    );

})

);
```

Very common.

______________________________________________________________________

# Service Layer

Service

```typescript
export class UserService {

    async findAll() {

        return [];

    }

}
```

Controller

```typescript
const service =

new UserService();

app.get(

"/users",

async (

req,

res

) => {

    res.json(

        await service.findAll()

    );

});
```

Keep business logic out of routes.

______________________________________________________________________

# Repository Layer

```typescript
class UserRepository {

    async findAll() {

        return [];

    }

}
```

Service

↓

Repository

Architecture

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

# DTO Pattern

Incoming request

```typescript
interface CreateUserDto {

    name: string;

    email: string;

}
```

Never expose database models directly.

______________________________________________________________________

# Validation

Simple validation

```typescript
if (

    !req.body.email

) {

    return res.status(400)

    .json({

        message:

        "Email required"

    });

}
```

Real projects usually use validation libraries.

______________________________________________________________________

# HTTP Status Codes

```typescript
res.status(200);

res.status(201);

res.status(204);

res.status(400);

res.status(401);

res.status(403);

res.status(404);

res.status(500);
```

Know these well for interviews.

______________________________________________________________________

# API Response Pattern

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

Consistent responses improve API usability.

______________________________________________________________________

# Logging

Avoid

```typescript
console.log()
```

everywhere.

Create

```typescript
logger.info();

logger.error();

logger.warn();
```

Production applications typically use dedicated logging libraries.

______________________________________________________________________

# Configuration Folder

```
config/

├── database.ts

├── server.ts

└── app.ts
```

Keep configuration centralized.

______________________________________________________________________

# Utility Folder

```
utils/

├── date.ts

├── jwt.ts

├── hash.ts

└── logger.ts
```

Avoid putting unrelated helper functions in one file.

______________________________________________________________________

# Error Class

```typescript
class ApiError

extends Error {

    constructor(

        public status:

        number,

        message: string

    ) {

        super(message);

    }

}
```

Usage

```typescript
throw new ApiError(

    404,

    "User not found"

);
```

______________________________________________________________________

# Folder Organization

```
src/

controllers/

services/

repositories/

routes/

middleware/

config/

models/

utils/
```

Keep each folder focused on one responsibility.

______________________________________________________________________

# Common Mistakes

## Business Logic Inside Routes

Wrong

```typescript
app.get(

"/users",

async (

req,

res

) => {

    // 200 lines

});
```

Move logic to services.

______________________________________________________________________

## Reading process.env Everywhere

Create

```
config.ts
```

instead.

______________________________________________________________________

## Ignoring Types

Wrong

```typescript
req.body
```

Use typed DTOs.

______________________________________________________________________

## Mixing Database Logic

Routes should not directly query the database.

Use a repository or service layer.

______________________________________________________________________

## Using console.log for Everything

Use a structured logger.

______________________________________________________________________

# Best Practices

✅ Type request parameters, query parameters, and request bodies.

✅ Keep controllers thin.

✅ Put business logic in services.

✅ Use repositories for database access.

✅ Centralize configuration.

✅ Handle async errors consistently.

✅ Return consistent API responses.

______________________________________________________________________

# Interview Deep Dive

## Question

Why is TypeScript useful for Node.js backend applications?

### Answer

TypeScript provides compile-time type checking, better tooling, safer refactoring, and improved maintainability. These
advantages reduce runtime errors and make large Node.js applications easier to develop and maintain.

______________________________________________________________________

## Question

Why should controllers remain thin?

### Answer

Controllers should focus on handling HTTP requests and responses. Business logic belongs in services, while database
access belongs in repositories. This separation improves maintainability, testing, and code reuse.

______________________________________________________________________

## Question

Why shouldn't you access `process.env` throughout the application?

### Answer

Centralizing environment variables in a configuration module improves type safety, validation, consistency, and makes
configuration changes easier to manage.

______________________________________________________________________

## Question

What is the Repository pattern?

### Answer

The Repository pattern abstracts data access behind a dedicated class or interface. Services interact with repositories
instead of directly accessing the database, making the application easier to test and maintain.

______________________________________________________________________

## Question

How should asynchronous errors be handled in Express?

### Answer

Asynchronous route handlers should either wrap logic in `try/catch` and call `next(error)` or use a reusable async
wrapper that automatically forwards rejected Promises to Express's error-handling middleware.

______________________________________________________________________

# Practice Questions

1. Why should TypeScript be used with Node.js?
1. What is the purpose of DTOs?
1. What belongs in a controller?
1. What belongs in a service?
1. What belongs in a repository?
1. Why should configuration be centralized?
1. How should Express request bodies be typed?
1. How should asynchronous errors be handled?
1. Why should API responses be consistent?
1. What are the advantages of a layered architecture?

______________________________________________________________________

# Summary

TypeScript and Node.js together provide a powerful foundation for building scalable backend applications.

In this chapter, you learned:

- Express setup
- Typed requests and responses
- Route parameters
- Query parameters
- DTOs
- Environment variables
- Middleware
- Error handling
- Async wrappers
- Service layer
- Repository layer
- Configuration management
- Logging
- Folder organization
- Backend architecture best practices

These patterns are widely used in production applications and are frequently discussed in backend interviews. The next
chapter explores **TypeScript Design Patterns**, where you'll learn how to structure larger applications using patterns
like Repository, Factory, Singleton, Builder, and Dependency Injection.

______________________________________________________________________

# Next

[TypeScript Patterns](12-typescript-patterns.md)
