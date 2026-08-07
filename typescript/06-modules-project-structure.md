# Modules & Project Structure

As applications grow, keeping all code in a single file becomes impossible.

TypeScript solves this using **Modules**.

Modules help organize code into reusable, maintainable units.

Every modern TypeScript backend project (Express, NestJS, Fastify, etc.) uses modules extensively.

______________________________________________________________________

# What is a Module?

A module is simply a file that exports or imports something.

Example

```
user.ts

↓

Exports User

↓

service.ts

↓

Imports User
```

Every file has its own scope.

Variables in one file are **not** automatically visible in another.

______________________________________________________________________

# Why Modules?

Imagine a backend application with

- Controllers
- Services
- Repositories
- DTOs
- Models
- Utilities

Without modules,

everything would be inside one giant file.

Modules solve this problem.

______________________________________________________________________

# Export

To make something available outside a file,

use

```typescript
export
```

Example

```typescript
export const company = "OpenAI";
```

Now other files can use it.

______________________________________________________________________

# Import

```typescript
import { company } from "./config";

console.log(company);
```

Output

```
OpenAI
```

______________________________________________________________________

# Exporting Functions

math.ts

```typescript
export function add(

    a: number,

    b: number

): number {

    return a + b;

}
```

Usage

```typescript
import {

    add

} from "./math";

console.log(

    add(10, 20)

);
```

Output

```
30
```

______________________________________________________________________

# Exporting Variables

config.ts

```typescript
export const PORT = 3000;
```

Usage

```typescript
import {

    PORT

} from "./config";

console.log(PORT);
```

______________________________________________________________________

# Exporting Classes

user.ts

```typescript
export class User {

    constructor(

        public name: string

    ) {}

}
```

Usage

```typescript
import {

    User

} from "./user";

const user =
    new User("Alice");
```

______________________________________________________________________

# Exporting Interfaces

```typescript
export interface User {

    id: number;

    name: string;

}
```

Usage

```typescript
import {

    User

} from "./user";
```

______________________________________________________________________

# Exporting Types

```typescript
export type UserId = number;
```

Usage

```typescript
import {

    UserId

} from "./types";
```

______________________________________________________________________

# Named Exports

Multiple exports.

math.ts

```typescript
export function add() {}

export function subtract() {}

export function multiply() {}
```

Import

```typescript
import {

    add,

    subtract,

    multiply

} from "./math";
```

______________________________________________________________________

# Alias Imports

```typescript
import {

    add as sum

} from "./math";
```

Usage

```typescript
sum(10, 20);
```

Useful when two modules export functions with the same name.

______________________________________________________________________

# Import Everything

```typescript
import * as MathUtils

from "./math";
```

Usage

```typescript
MathUtils.add(1,2);

MathUtils.subtract(5,2);
```

______________________________________________________________________

# Default Export

A module may have one default export.

math.ts

```typescript
export default function add(

    a: number,

    b: number

) {

    return a + b;

}
```

Import

```typescript
import add

from "./math";
```

Notice

```
No { }
```

______________________________________________________________________

# Default vs Named Export

Named

```typescript
export function add(){}
```

Import

```typescript
import {

    add

}
```

______________________________________________________________________

Default

```typescript
export default add;
```

Import

```typescript
import add
```

______________________________________________________________________

# Which Should You Prefer?

For backend projects,

named exports are generally preferred because:

- Easier refactoring
- Better autocomplete
- Easier to find usages
- Consistent imports

Many large codebases avoid default exports altogether.

______________________________________________________________________

# Re-exporting

Suppose

```
user.ts

order.ts

product.ts
```

Instead of

```typescript
import {

    User

} from "./user";

import {

    Order

} from "./order";
```

Create

```
index.ts
```

```typescript
export * from "./user";

export * from "./order";

export * from "./product";
```

Now

```typescript
import {

    User,

    Order

} from "./models";
```

Much cleaner.

______________________________________________________________________

# Barrel Exports

This technique is called a

```
Barrel Export
```

Folder

```
models/

├── user.ts

├── order.ts

├── product.ts

└── index.ts
```

Very common in backend applications.

______________________________________________________________________

# Project Structure

Small Project

```
src/

├── index.ts

├── user.ts

└── config.ts
```

______________________________________________________________________

Typical Express Project

```
src/

├── controllers/

├── services/

├── repositories/

├── models/

├── routes/

├── middleware/

├── utils/

├── config/

└── app.ts
```

______________________________________________________________________

Typical NestJS Project

```
src/

├── users/

│   ├── controller.ts

│   ├── service.ts

│   ├── module.ts

│   └── dto/

│

├── auth/

├── config/

└── main.ts
```

Notice that NestJS organizes code by **feature**, not by technical layer.

______________________________________________________________________

# tsconfig.json

Important options

```json
{

    "compilerOptions": {

        "rootDir": "./src",

        "outDir": "./dist",

        "strict": true,

        "module": "NodeNext",

        "target": "ES2022"

    }

}
```

______________________________________________________________________

# rootDir

Where source files live.

```json
"rootDir": "./src"
```

______________________________________________________________________

# outDir

Compiled JavaScript.

```json
"outDir": "./dist"
```

______________________________________________________________________

# module

Common values

```
NodeNext

CommonJS

ESNext
```

For modern Node.js,

```
NodeNext
```

is generally recommended.

______________________________________________________________________

# target

JavaScript version.

```
ES2022

ES2021

ES2020
```

______________________________________________________________________

# baseUrl

Simplifies imports.

Without

```typescript
../../../services
```

With

```json
"baseUrl":"./src"
```

Imports become

```typescript
import {

    UserService

}

from "services/userService";
```

______________________________________________________________________

# Path Aliases

Even better

```json
"paths": {

    "@services/*":[

        "services/*"

    ],

    "@models/*":[

        "models/*"

    ]

}
```

Now

```typescript
import {

    User

}

from "@models/user";
```

Cleaner imports.

______________________________________________________________________

# package.json

Typical scripts

```json
{

    "scripts": {

        "build":

        "tsc",

        "start":

        "node dist/index.js",

        "dev":

        "ts-node src/index.ts"

    }

}
```

Most projects also use a file watcher for development.

______________________________________________________________________

# Development Workflow

```
Write TS

↓

Compile

↓

Run JS
```

or

```
Write TS

↓

ts-node

↓

Run directly
```

______________________________________________________________________

# Environment Variables

Backend applications usually keep configuration separate from code.

Example

```
.env
```

```
PORT=3000

DB_HOST=localhost

JWT_SECRET=my-secret
```

Access

```typescript
process.env.PORT
```

We'll cover this in more detail in the Node.js chapter.

______________________________________________________________________

# Organizing Code

Bad

```
utils.ts

↓

5000 lines
```

Better

```
utils/

├── logger.ts

├── date.ts

├── validation.ts

└── index.ts
```

One responsibility per file.

______________________________________________________________________

# Feature-Based Structure

Instead of

```
controllers/

services/

repositories/
```

Some teams prefer

```
users/

orders/

payments/

auth/
```

Each folder contains everything related to one feature.

This is the default approach in NestJS and is increasingly common in large applications.

______________________________________________________________________

# Common Mistakes

## Circular Imports

Example

```
A imports B

↓

B imports A
```

This can lead to runtime issues and confusing bugs.

Try to keep dependencies flowing in one direction.

______________________________________________________________________

## Huge Files

Avoid files with thousands of lines.

Split responsibilities into smaller modules.

______________________________________________________________________

## Deep Relative Imports

Bad

```typescript
../../../../models
```

Prefer path aliases.

______________________________________________________________________

## Default Export Everywhere

Named exports make refactoring easier and reduce ambiguity in large codebases.

______________________________________________________________________

# Best Practices

✅ Organize by feature or domain.

✅ Prefer named exports.

✅ Use barrel exports for folders.

✅ Configure path aliases.

✅ Keep modules focused on one responsibility.

✅ Avoid circular dependencies.

______________________________________________________________________

# Interview Deep Dive

## Question

What is a TypeScript module?

### Answer

A module is any file that exports or imports values. Modules provide file-level scope and enable code organization
through reusable components.

______________________________________________________________________

## Question

What is the difference between a named export and a default export?

### Answer

A named export allows multiple exports from a file and must be imported using curly braces.

A default export allows only one primary export from a file and is imported without curly braces. Many large TypeScript
projects prefer named exports because they improve consistency and refactoring.

______________________________________________________________________

## Question

What is a barrel export?

### Answer

A barrel export is an `index.ts` file that re-exports members from multiple files. It simplifies imports by allowing
consumers to import everything from a single entry point instead of multiple individual files.

______________________________________________________________________

## Question

Why are path aliases useful?

### Answer

Path aliases eliminate long relative import paths, making imports easier to read and maintain. They also reduce errors
when files are moved within the project.

______________________________________________________________________

## Question

How should a backend TypeScript project be organized?

### Answer

Backend projects should separate responsibilities into focused modules. Common approaches include layer-based structures
(controllers, services, repositories) or feature-based structures (users, orders, auth). The choice depends on project
size and team preferences, but feature-based organization is increasingly common for large applications.

______________________________________________________________________

# Practice Questions

1. What is a TypeScript module?
1. What is the difference between named and default exports?
1. What is a barrel export?
1. Why are path aliases useful?
1. What is the purpose of `rootDir` and `outDir`?
1. What does the `module` compiler option control?
1. Why should circular imports be avoided?
1. What are the advantages of organizing projects by feature?
1. Why are named exports commonly preferred?
1. What is the purpose of `package.json` scripts?

______________________________________________________________________

# Summary

Modules are the foundation of scalable TypeScript applications.

In this chapter, you learned:

- Modules
- `export`
- `import`
- Named exports
- Default exports
- Re-exporting
- Barrel exports
- Project structure
- `tsconfig.json`
- `rootDir`
- `outDir`
- `module`
- `target`
- Path aliases
- `package.json`
- Feature-based organization
- Backend project best practices

A well-organized project is easier to maintain, test, and scale. The next chapter introduces **asynchronous
programming**, where you'll learn how `Promise`, `async/await`, and concurrent operations work in modern TypeScript
backend applications.

______________________________________________________________________

# Next

[Async Programming](07-async-programming.md)
