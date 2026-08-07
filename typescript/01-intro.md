# Introduction to TypeScript

TypeScript is one of the most popular programming languages for modern web and backend development.

It is essentially **JavaScript with static typing**.

If you already know Java and Python, you'll find TypeScript somewhere in the middle:

- Java's type safety
- Python's concise syntax
- JavaScript's ecosystem

This crash course is focused on **backend engineers**, so examples will use APIs, services, and backend-related code
rather than frontend frameworks.

______________________________________________________________________

# What is TypeScript?

TypeScript is an open-source programming language developed by Microsoft.

It is a **superset of JavaScript**, meaning:

- Every JavaScript program is valid TypeScript.
- TypeScript adds additional features.
- TypeScript is compiled into plain JavaScript before execution.

```
TypeScript

↓

TypeScript Compiler (tsc)

↓

JavaScript

↓

Node.js / Browser
```

______________________________________________________________________

# Why TypeScript?

JavaScript is extremely flexible.

Sometimes,

too flexible.

Example

```javascript
let age = 25;

age = "Twenty Five";

console.log(age);
```

Output

```
Twenty Five
```

No error.

The mistake is only discovered later.

______________________________________________________________________

TypeScript

```typescript
let age: number = 25;

age = "Twenty Five";
```

Compilation Error

```
Type 'string' is not assignable
to type 'number'
```

The compiler catches the mistake before your code runs.

______________________________________________________________________

# JavaScript vs TypeScript

| JavaScript | TypeScript |
|------------|------------|
| Dynamically typed | Statically typed |
| Runs directly | Compiles to JavaScript |
| Runtime errors | More compile-time errors |
| No interfaces | Interfaces available |
| No generics | Generics supported |
| Easier to start | Easier to maintain large projects |

______________________________________________________________________

# Why Companies Use TypeScript

Large applications contain:

- Thousands of files
- Hundreds of developers
- Millions of lines of code

Static typing helps by providing:

- Better autocomplete
- Safer refactoring
- Better IDE support
- Earlier error detection
- Easier maintenance

This is why frameworks like **NestJS**, **Angular**, and many Node.js backends use TypeScript.

______________________________________________________________________

# Compilation Process

```
app.ts

↓

tsc

↓

app.js

↓

node app.js
```

Example

TypeScript

```typescript
const message: string = "Hello";
```

Compiled JavaScript

```javascript
"use strict";

const message = "Hello";
```

Notice that the type information disappears after compilation.

______________________________________________________________________

# TypeScript is NOT a Runtime

Very important interview question.

Wrong understanding

```
Node.js executes TypeScript
```

Correct

```
TypeScript

↓

JavaScript

↓

Node.js executes JavaScript
```

Node.js does **not** understand `.ts` files directly.

______________________________________________________________________

# Installing TypeScript

Install globally

```bash
npm install -g typescript
```

Check version

```bash
tsc --version
```

Example

```
Version 5.x.x
```

______________________________________________________________________

# Creating Your First Project

Create folder

```bash
mkdir typescript-demo

cd typescript-demo
```

Initialize npm

```bash
npm init -y
```

Install TypeScript

```bash
npm install --save-dev typescript
```

Generate configuration

```bash
npx tsc --init
```

______________________________________________________________________

# Project Structure

```
typescript-demo/

├── src/
│   └── index.ts
│
├── dist/
│
├── package.json
│
├── tsconfig.json
│
└── node_modules/
```

This is the structure you'll commonly see in backend projects.

______________________________________________________________________

# Your First TypeScript Program

Create

```
src/index.ts
```

```typescript
const message: string = "Hello TypeScript";

console.log(message);
```

Compile

```bash
npx tsc
```

Run

```bash
node dist/index.js
```

Output

```
Hello TypeScript
```

______________________________________________________________________

# Running Without Compilation

Instead of compiling every time,

many developers use

```
ts-node
```

Install

```bash
npm install --save-dev ts-node
```

Run

```bash
npx ts-node src/index.ts
```

Much faster during development.

______________________________________________________________________

# tsconfig.json

The most important configuration file.

Example

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "strict": true,
    "rootDir": "./src",
    "outDir": "./dist"
  }
}
```

______________________________________________________________________

# Important Compiler Options

## target

Specifies JavaScript version.

Example

```json
"target": "ES2022"
```

______________________________________________________________________

## module

Defines module system.

Examples

```
CommonJS

ESNext

NodeNext
```

For most Node.js projects,

```
NodeNext
```

or

```
CommonJS
```

is used depending on the project setup.

______________________________________________________________________

## rootDir

Where source code lives.

```json
"rootDir": "./src"
```

______________________________________________________________________

## outDir

Where compiled JavaScript goes.

```json
"outDir": "./dist"
```

______________________________________________________________________

## strict ⭐⭐⭐⭐⭐

One of the most important settings.

```json
"strict": true
```

Enables

- strict typing
- null checking
- better error detection

Always enable this for production projects.

______________________________________________________________________

# TypeScript Playground

If you don't want to install anything,

Microsoft provides an online playground where you can write TypeScript and instantly see the generated JavaScript.

Great for experimenting with language features.

______________________________________________________________________

# How TypeScript Helps

Suppose you rename a function used in 300 files.

JavaScript

```
Hope nothing breaks.
```

TypeScript

```
Compiler tells you
every place that needs updating.
```

One reason large companies love TypeScript.

______________________________________________________________________

# TypeScript in Backend Development

You'll commonly see TypeScript in:

- Node.js
- Express
- NestJS
- Serverless Functions
- AWS Lambda
- REST APIs
- GraphQL APIs
- Microservices

It has become the standard language for many modern Node.js backend applications.

______________________________________________________________________

# Common Misconceptions

## TypeScript Makes JavaScript Faster

No.

TypeScript improves **developer experience**, not runtime performance.

Generated JavaScript runs at essentially the same speed.

______________________________________________________________________

## TypeScript Replaces JavaScript

No.

TypeScript compiles into JavaScript.

JavaScript is still the language executed by Node.js.

______________________________________________________________________

## TypeScript Prevents Every Bug

No.

TypeScript catches many mistakes during compilation,

but logical errors can still occur.

______________________________________________________________________

# Best Practices

✅ Enable `strict` mode.

✅ Keep source code inside `src`.

✅ Compile output into `dist`.

✅ Prefer local TypeScript installation over global for projects.

✅ Use `ts-node` during development.

______________________________________________________________________

# Interview Deep Dive

## Question

What is TypeScript?

### Answer

TypeScript is a statically typed superset of JavaScript developed by Microsoft. It adds features such as static typing,
interfaces, generics, and advanced tooling while compiling into standard JavaScript that can run in any JavaScript
environment.

______________________________________________________________________

## Question

Why do companies use TypeScript?

### Answer

TypeScript improves code quality through static type checking, better IDE support, safer refactoring, and earlier
detection of programming errors. These advantages become increasingly valuable as applications and development teams
grow.

______________________________________________________________________

## Question

Does Node.js execute TypeScript directly?

### Answer

No. TypeScript must first be compiled into JavaScript using the TypeScript compiler (`tsc`). Node.js executes the
generated JavaScript files, not the original TypeScript source.

______________________________________________________________________

## Question

What is `tsconfig.json`?

### Answer

`tsconfig.json` is the TypeScript configuration file. It defines compiler options such as the target JavaScript version,
module system, source directory, output directory, and strict type-checking rules.

______________________________________________________________________

## Question

Why should `strict` mode be enabled?

### Answer

`strict` mode enables a collection of compiler checks that detect potential bugs, including incorrect types, possible
null values, and unsafe assignments. It helps produce more reliable and maintainable applications.

______________________________________________________________________

# Practice Questions

1. What is TypeScript?
1. How is TypeScript different from JavaScript?
1. Why is TypeScript called a superset of JavaScript?
1. Explain the TypeScript compilation process.
1. Does Node.js execute TypeScript directly?
1. What is the purpose of `tsconfig.json`?
1. Why is `strict` mode recommended?
1. What is `ts-node`?
1. What are the benefits of static typing?
1. Where is TypeScript commonly used in backend development?

______________________________________________________________________

# Summary

TypeScript builds on JavaScript by adding static typing and powerful development tools while still compiling to plain
JavaScript.

In this chapter, you learned:

- What TypeScript is
- Why TypeScript exists
- TypeScript vs JavaScript
- Compilation process
- Installing TypeScript
- Project structure
- `tsconfig.json`
- Important compiler options
- `ts-node`
- Backend use cases

With this foundation in place, you're ready to start writing real TypeScript code. The next chapter introduces
variables, built-in types, functions, and the core language syntax you'll use every day.

______________________________________________________________________

# Next

[Variables, Types & Functions](02-variables-types-functions.md)
