# TypeScript vs Java

If you're coming from Java (or preparing for Java backend interviews), understanding the similarities and differences
between Java and TypeScript is extremely valuable.

Although both languages support object-oriented programming and static typing, they are fundamentally different in how
they execute, compile, and are used.

______________________________________________________________________

# High-Level Comparison

| TypeScript | Java |
|------------|------|
| Superset of JavaScript | Standalone programming language |
| Compiles to JavaScript | Compiles to Java Bytecode |
| Runs on Browser or Node.js | Runs on JVM |
| Structural Type System | Nominal Type System |
| Mostly Single-threaded Runtime (Node.js) | Multi-threaded Runtime |
| Optional Runtime Type Information | Rich Runtime Type Information |
| Used for Frontend & Backend | Primarily Backend & Android |

______________________________________________________________________

# Compilation

## TypeScript

```
TypeScript

↓

tsc

↓

JavaScript

↓

Browser / Node.js
```

______________________________________________________________________

## Java

```
Java Source

↓

javac

↓

Bytecode (.class)

↓

JVM

↓

Machine Code
```

______________________________________________________________________

# Runtime

TypeScript

```
Node.js

OR

Browser
```

Java

```
JVM
```

The runtime is one of the biggest differences between the two languages.

______________________________________________________________________

# Type System

## TypeScript

Structural Typing

"If it looks like the required type, it's accepted."

Example

```typescript
interface User {

    name: string;

}

const person = {

    name: "Alice",

    age: 30

};

const user: User = person;
```

Valid.

______________________________________________________________________

## Java

Nominal Typing

Types must explicitly match.

```java
class User {

    String name;

}

User user = new User();
```

Another class with the same fields is **not** considered compatible.

______________________________________________________________________

# Variables

TypeScript

```typescript
const name: string = "Alice";

let age: number = 25;
```

______________________________________________________________________

Java

```java
String name = "Alice";

int age = 25;
```

______________________________________________________________________

# Primitive Types

| TypeScript | Java |
|------------|------|
| number | byte, short, int, long, float, double |
| string | String |
| boolean | boolean |
| bigint | BigInteger (library) / long (primitive) |
| symbol | No direct equivalent |

Java has multiple numeric primitive types.

TypeScript has a single `number` type (IEEE 754 double precision).

______________________________________________________________________

# Null Handling

TypeScript

```typescript
string | null
```

Java

```java
String value = null;
```

Modern Java also provides

```java
Optional<T>
```

to reduce null-related errors.

______________________________________________________________________

# Functions

TypeScript

```typescript
function add(

    a: number,

    b: number

): number {

    return a + b;

}
```

______________________________________________________________________

Java

```java
public int add(

    int a,

    int b

) {

    return a + b;

}
```

______________________________________________________________________

# Arrow Functions

TypeScript

```typescript
const square =

(x: number) => x * x;
```

______________________________________________________________________

Java

```java
Function<Integer, Integer> square =

x -> x * x;
```

Java uses lambda expressions with functional interfaces.

______________________________________________________________________

# Classes

TypeScript

```typescript
class User {

    constructor(

        public name: string

    ) {}

}
```

______________________________________________________________________

Java

```java
class User {

    private String name;

    public User(

        String name

    ) {

        this.name = name;

    }

}
```

TypeScript supports constructor parameter shorthand.

Java requires explicit fields and constructors.

______________________________________________________________________

# Access Modifiers

| TypeScript | Java |
|------------|------|
| public | public |
| private | private |
| protected | protected |

Java also has

```
package-private
```

which TypeScript does not.

______________________________________________________________________

# Interfaces

TypeScript

```typescript
interface User {

    name: string;

}
```

______________________________________________________________________

Java

```java
interface User {

    String getName();

}
```

TypeScript interfaces describe **shape**.

Java interfaces define **contracts and behavior**.

______________________________________________________________________

# Inheritance

TypeScript

```typescript
class Admin

extends User {

}
```

______________________________________________________________________

Java

```java
class Admin

extends User {

}
```

Both support single class inheritance.

______________________________________________________________________

# Multiple Interfaces

TypeScript

```typescript
class User

implements A, B {

}
```

______________________________________________________________________

Java

```java
class User

implements A, B {

}
```

Both allow implementing multiple interfaces.

______________________________________________________________________

# Generics

TypeScript

```typescript
function identity<T>(

    value: T

): T {

    return value;

}
```

______________________________________________________________________

Java

```java
public <T> T identity(

    T value

) {

    return value;

}
```

The syntax differs slightly, but the concept is similar.

______________________________________________________________________

# Collections

TypeScript

```typescript
const users: User[] = [];
```

______________________________________________________________________

Java

```java
List<User> users =

new ArrayList<>();
```

______________________________________________________________________

# Maps

TypeScript

```typescript
const map =

new Map<number, User>();
```

______________________________________________________________________

Java

```java
Map<Integer, User> map =

new HashMap<>();
```

______________________________________________________________________

# Sets

TypeScript

```typescript
new Set<string>();
```

______________________________________________________________________

Java

```java
new HashSet<String>();
```

______________________________________________________________________

# Exceptions

TypeScript

```typescript
throw new Error(

    "Something went wrong"

);
```

______________________________________________________________________

Java

```java
throw new RuntimeException(

    "Something went wrong"

);
```

______________________________________________________________________

Handling

TypeScript

```typescript
try {

}

catch(error) {

}
```

______________________________________________________________________

Java

```java
try {

}

catch(Exception e) {

}
```

______________________________________________________________________

# Checked Exceptions

TypeScript

```
No
```

Checked Exceptions

______________________________________________________________________

Java

```
Yes
```

Example

```java
IOException
```

must often be declared or handled.

______________________________________________________________________

# Asynchronous Programming

TypeScript

```typescript
await fetchUsers();
```

______________________________________________________________________

Java

```java
CompletableFuture<User>
```

or

Reactive frameworks

such as

Spring WebFlux.

TypeScript has built-in `async/await`.

______________________________________________________________________

# Threading

Node.js

```
Single Thread

+

Event Loop
```

______________________________________________________________________

Java

```
Multiple Threads
```

Java has rich concurrency APIs.

______________________________________________________________________

# Memory Management

Both use

```
Garbage Collection
```

Java provides more tuning options for JVM GC.

______________________________________________________________________

# Reflection

Java

Has built-in reflection.

```java
Class<?> clazz = User.class;
```

______________________________________________________________________

TypeScript

Type information is mostly removed during compilation.

Frameworks like NestJS use decorators and metadata to provide limited runtime type information.

______________________________________________________________________

# Enums

TypeScript

```typescript
enum Status {

    Active,

    Inactive

}
```

______________________________________________________________________

Java

```java
enum Status {

    ACTIVE,

    INACTIVE

}
```

Modern TypeScript projects often prefer string literal unions instead of enums.

______________________________________________________________________

# Modules vs Packages

TypeScript

```
Files

+

Modules
```

______________________________________________________________________

Java

```
Packages
```

Example

```java
package com.example.user;
```

______________________________________________________________________

# Dependency Management

TypeScript

```
npm

pnpm

yarn
```

______________________________________________________________________

Java

```
Maven

Gradle
```

______________________________________________________________________

# Build Tools

TypeScript

- tsc
- Vite
- Webpack
- esbuild

______________________________________________________________________

Java

- Maven
- Gradle

______________________________________________________________________

# Backend Frameworks

TypeScript

- Express
- NestJS
- Fastify
- Hono

______________________________________________________________________

Java

- Spring Boot
- Micronaut
- Quarkus

______________________________________________________________________

# Dependency Injection

NestJS

```typescript
@Injectable()

class UserService {

}
```

______________________________________________________________________

Spring Boot

```java
@Service

class UserService {

}
```

Both rely heavily on Dependency Injection.

______________________________________________________________________

# API Example

TypeScript (Express)

```typescript
app.get(

    "/users",

    (

        req,

        res

    ) => {

        res.json(users);

    }

);
```

______________________________________________________________________

Java (Spring Boot)

```java
@GetMapping("/users")

public List<User> getUsers() {

    return users;

}
```

______________________________________________________________________

# Similarities

Both support

- Object-Oriented Programming
- Interfaces
- Classes
- Generics
- Exceptions
- Encapsulation
- Inheritance
- Polymorphism
- Dependency Injection (through frameworks)
- Strong tooling and IDE support

______________________________________________________________________

# Major Differences

| Feature | TypeScript | Java |
|---------|------------|------|
| Runtime | Browser / Node.js | JVM |
| Type System | Structural | Nominal |
| Compilation Target | JavaScript | Bytecode |
| Async Model | Event Loop + Promises | Threads + Executors + CompletableFuture |
| Threading | Mostly Single-threaded | Multi-threaded |
| Reflection | Limited | Rich |
| Package Manager | npm | Maven / Gradle |

______________________________________________________________________

# Which is Faster?

Generally,

Java offers higher raw throughput for CPU-intensive workloads due to the JVM's optimizations and mature multi-threading
support.

TypeScript running on Node.js performs extremely well for I/O-bound workloads because of its event-driven, non-blocking
architecture.

The right choice depends on the workload rather than the language alone.

______________________________________________________________________

# Common Mistakes

## Expecting Java-style Runtime Types

TypeScript's type information is primarily a compile-time feature.

Most types do not exist at runtime.

______________________________________________________________________

## Expecting Multiple Threads in Node.js

Node.js uses an event loop for JavaScript execution.

Long-running CPU tasks should be offloaded to worker threads or separate services when appropriate.

______________________________________________________________________

## Thinking Generics Work Identically

Both languages support generics, but Java uses type erasure, while TypeScript's generics exist only during compilation.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the biggest difference between TypeScript and Java?

### Answer

TypeScript compiles to JavaScript and runs in the browser or on Node.js, while Java compiles to bytecode and runs on the
JVM. They also differ in their type systems, runtime environments, and concurrency models.

______________________________________________________________________

## Question

What is the difference between structural typing and nominal typing?

### Answer

Structural typing determines compatibility based on an object's shape. If an object has the required properties, it is
considered compatible.

Nominal typing requires explicit type declarations or inheritance relationships. Two classes with identical fields are
not automatically compatible.

______________________________________________________________________

## Question

Why is asynchronous programming easier in TypeScript?

### Answer

TypeScript, through JavaScript, provides native support for Promises and `async/await`, making asynchronous code concise
and readable. Java traditionally relied on threads and callbacks, though modern Java also provides `CompletableFuture`
and reactive APIs.

______________________________________________________________________

## Question

Can TypeScript replace Java for backend development?

### Answer

Yes, many backend applications are successfully built with Node.js and TypeScript. However, Java remains a strong choice
for many enterprise systems, especially where mature JVM tooling, extensive ecosystem support, or high-performance
multi-threaded processing are priorities.

______________________________________________________________________

# Practice Questions

1. How does TypeScript differ from Java?
1. What is structural typing?
1. What is nominal typing?
1. How do the compilation processes differ?
1. What runtime executes TypeScript? What runtime executes Java?
1. How does asynchronous programming differ between the two?
1. What are the differences between Node.js's event loop and Java's threading model?
1. How are dependency management tools different?
1. Why doesn't most TypeScript type information exist at runtime?
1. When would you choose TypeScript over Java, and when might Java be a better fit?

______________________________________________________________________

# Next

[Frontend vs Backend](17-frontend-vs-backend.md)
