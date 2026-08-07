# Objects, Interfaces & Classes

Objects, Interfaces, and Classes are the foundation of almost every TypeScript backend application.

Frameworks like:

- Express
- NestJS
- Fastify
- TypeORM
- Prisma

all rely heavily on these concepts.

If you already know Java, you'll notice many similarities—but there are also important differences.

______________________________________________________________________

# Objects

The simplest way to store related data is using an object.

```typescript
const user = {

    id: 1,

    name: "Alice",

    active: true

};

console.log(user.name);
```

Output

```
Alice
```

______________________________________________________________________

# Object Type

Instead of letting TypeScript infer everything,

you can define the object's shape.

```typescript
const user: {

    id: number;

    name: string;

    active: boolean;

} = {

    id: 1,

    name: "Alice",

    active: true

};
```

Works,

but becomes difficult to reuse.

______________________________________________________________________

# Type Alias for Objects

Better approach

```typescript
type User = {

    id: number;

    name: string;

    active: boolean;

};
```

Usage

```typescript
const user: User = {

    id: 1,

    name: "Alice",

    active: true

};
```

Much cleaner.

______________________________________________________________________

# Optional Properties

Sometimes a property may not exist.

```typescript
type User = {

    id: number;

    name: string;

    email?: string;

};
```

Valid

```typescript
const user: User = {

    id: 1,

    name: "Alice"

};
```

______________________________________________________________________

# Readonly Properties

Prevent modification.

```typescript
type User = {

    readonly id: number;

    name: string;

};
```

Wrong

```typescript
user.id = 10;
```

Compilation Error.

______________________________________________________________________

# Nested Objects

```typescript
type Address = {

    city: string;

    country: string;

};

type User = {

    name: string;

    address: Address;

};
```

Usage

```typescript
const user: User = {

    name: "Alice",

    address: {

        city: "Bangalore",

        country: "India"

    }

};
```

______________________________________________________________________

# Interfaces

One of the most important TypeScript features.

An interface defines the **structure** of an object.

Example

```typescript
interface User {

    id: number;

    name: string;

    active: boolean;

}
```

Usage

```typescript
const user: User = {

    id: 1,

    name: "Alice",

    active: true

};
```

______________________________________________________________________

# Why Interfaces?

Imagine

```
100 API endpoints
```

all returning a user.

Without interfaces,

every object definition must be repeated.

Interfaces solve this problem.

______________________________________________________________________

# Interface vs Type Alias

Both work.

```typescript
interface User {

    id: number;

}
```

```typescript
type User = {

    id: number;

};
```

So why have both?

We'll compare them shortly.

______________________________________________________________________

# Extending Interfaces

Interfaces can inherit from other interfaces.

```typescript
interface Person {

    name: string;

}
```

```typescript
interface Employee
    extends Person {

    employeeId: number;

}
```

Usage

```typescript
const employee: Employee = {

    name: "Alice",

    employeeId: 100

};
```

______________________________________________________________________

# Multiple Interface Inheritance

Unlike Java classes,

interfaces can extend multiple interfaces.

```typescript
interface Flyable {

    fly(): void;

}
```

```typescript
interface Swimmable {

    swim(): void;

}
```

```typescript
interface Duck
    extends Flyable,
            Swimmable {

    name: string;

}
```

______________________________________________________________________

# Function Interfaces

Interfaces can describe functions.

```typescript
interface Calculator {

    (
        a: number,
        b: number
    ): number;

}
```

Implementation

```typescript
const add: Calculator =

    (a, b) => a + b;
```

______________________________________________________________________

# Classes

Classes are templates for creating objects.

```typescript
class User {

    id: number;

    name: string;

}
```

Create object

```typescript
const user = new User();
```

______________________________________________________________________

# Constructor

Initialize objects.

```typescript
class User {

    id: number;

    name: string;

    constructor(
        id: number,
        name: string
    ) {

        this.id = id;

        this.name = name;

    }

}
```

Usage

```typescript
const user =
    new User(1, "Alice");
```

______________________________________________________________________

# Constructor Shorthand

Very common in TypeScript.

Instead of

```typescript
class User {

    id: number;

    name: string;

    constructor(
        id: number,
        name: string
    ) {

        this.id = id;

        this.name = name;

    }

}
```

Use

```typescript
class User {

    constructor(

        public id: number,

        public name: string

    ) {}

}
```

Much shorter.

______________________________________________________________________

# Methods

```typescript
class User {

    constructor(

        public name: string

    ) {}

    greet() {

        console.log(
            `Hello ${this.name}`
        );

    }

}
```

______________________________________________________________________

# Access Modifiers

TypeScript supports

```
public

private

protected
```

Like Java.

______________________________________________________________________

# public

Default modifier.

```typescript
class User {

    public name: string;

}
```

Can be accessed everywhere.

______________________________________________________________________

# private

```typescript
class User {

    private password: string;

}
```

Cannot access outside the class.

______________________________________________________________________

# protected

Accessible

- inside class
- subclasses

Not outside.

______________________________________________________________________

# readonly

```typescript
class User {

    readonly id: number;

    constructor(id: number){

        this.id = id;

    }

}
```

After construction

```
Cannot change.
```

______________________________________________________________________

# Static Members

Belong to the class,

not the object.

```typescript
class User {

    static company =
        "OpenAI";

}
```

Usage

```typescript
console.log(
    User.company
);
```

No object needed.

______________________________________________________________________

# Inheritance

```typescript
class Person {

    constructor(

        public name: string

    ) {}

}
```

```typescript
class Employee
    extends Person {

    constructor(

        name: string,

        public id: number

    ) {

        super(name);

    }

}
```

Usage

```typescript
const employee =
    new Employee(
        "Alice",
        100
    );
```

______________________________________________________________________

# Method Overriding

```typescript
class Animal {

    speak() {

        console.log("Animal");

    }

}
```

```typescript
class Dog
    extends Animal {

    override speak() {

        console.log("Bark");

    }

}
```

The `override` keyword (TypeScript 4.3+) helps catch mistakes if the parent method changes.

______________________________________________________________________

# Abstract Classes

Cannot create objects directly.

```typescript
abstract class Animal {

    abstract speak(): void;

}
```

Wrong

```typescript
new Animal();
```

Compilation Error.

______________________________________________________________________

Implementation

```typescript
class Dog
    extends Animal {

    speak() {

        console.log("Bark");

    }

}
```

______________________________________________________________________

# Implementing Interfaces

Classes can implement interfaces.

```typescript
interface Payment {

    pay(): void;

}
```

```typescript
class CreditCard
    implements Payment {

    pay() {

        console.log(
            "Paid"
        );

    }

}
```

______________________________________________________________________

# Multiple Interfaces

A class can implement multiple interfaces.

```typescript
interface Flyable {

    fly(): void;

}
```

```typescript
interface Swimmable {

    swim(): void;

}
```

```typescript
class Duck
    implements Flyable,
               Swimmable {

    fly() {

        console.log("Flying");

    }

    swim() {

        console.log("Swimming");

    }

}
```

______________________________________________________________________

# Interface vs Type

| Interface | Type |
|------------|------|
| Object shapes | Objects, unions, tuples, primitives |
| Extendable | Extendable |
| Declaration merging | Supported |
| Common for APIs | More flexible |

General guideline

- Use **interface** for object contracts.
- Use **type** for unions, primitives, and complex combinations.

______________________________________________________________________

# Interface vs Abstract Class

| Interface | Abstract Class |
|------------|----------------|
| Defines contract | Defines contract + implementation |
| No implementation state | Can contain state |
| Multiple implementations | Single inheritance |
| No constructor | Constructor allowed |

Very similar to Java.

______________________________________________________________________

# Backend Example

DTO

```typescript
interface CreateUserRequest {

    name: string;

    email: string;

}
```

Entity

```typescript
class User {

    constructor(

        public id: number,

        public name: string,

        public email: string

    ) {}

}
```

Service

```typescript
function createUser(

    request: CreateUserRequest

): User {

    return new User(

        1,

        request.name,

        request.email

    );

}
```

This pattern is common in Express and NestJS applications.

______________________________________________________________________

# Common Mistakes

## Using Classes Everywhere

If you only need a data shape,

prefer

```
interface
```

or

```
type
```

______________________________________________________________________

## Using any

Wrong

```typescript
interface User {

    data: any;

}
```

Prefer specific types.

______________________________________________________________________

## Forgetting readonly

If a value should never change,

mark it

```typescript
readonly
```

______________________________________________________________________

## Forgetting override

Always use

```typescript
override
```

when overriding parent methods.

______________________________________________________________________

# Best Practices

✅ Use interfaces for API contracts.

✅ Use constructor shorthand.

✅ Keep classes focused.

✅ Prefer composition over inheritance.

✅ Mark immutable properties as `readonly`.

✅ Use `private` to protect implementation details.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between an interface and a type alias?

### Answer

Both can describe object shapes, but interfaces are primarily designed for object contracts and support declaration
merging. Type aliases are more flexible because they can represent primitive types, unions, intersections, tuples, and
complex type combinations. A common convention is to use interfaces for object models and type aliases for advanced type
compositions.

______________________________________________________________________

## Question

What is the difference between an interface and an abstract class?

### Answer

An interface defines only a contract that implementing classes must follow. It cannot maintain instance state or
constructors.

An abstract class can contain properties, constructors, implemented methods, and abstract methods, making it useful when
related classes share common implementation.

______________________________________________________________________

## Question

Why should constructor shorthand be preferred?

### Answer

Constructor shorthand automatically declares and initializes class properties, reducing boilerplate code while improving
readability.

______________________________________________________________________

## Question

Can a class implement multiple interfaces?

### Answer

Yes. A TypeScript class can implement multiple interfaces, allowing it to satisfy multiple contracts without using
multiple inheritance.

______________________________________________________________________

## Question

When should you use an interface instead of a class?

### Answer

Use an interface when you only need to describe the structure of data or define a contract between components. Use a
class when you need object creation, constructors, methods, or encapsulated behavior.

______________________________________________________________________

# Practice Questions

1. What is an interface?
1. What is the difference between an interface and a type alias?
1. What is constructor shorthand?
1. What is the purpose of `readonly`?
1. What are access modifiers in TypeScript?
1. What is the difference between `private` and `protected`?
1. Can a class implement multiple interfaces?
1. What is an abstract class?
1. When should you use a class instead of an interface?
1. Why is composition generally preferred over inheritance?

______________________________________________________________________

# Summary

Objects, interfaces, and classes are the backbone of TypeScript backend development.

In this chapter, you learned:

- Object types
- Type aliases for objects
- Interfaces
- Interface inheritance
- Function interfaces
- Classes
- Constructors
- Constructor shorthand
- Access modifiers
- `readonly`
- Static members
- Inheritance
- Method overriding
- Abstract classes
- Implementing interfaces
- Interface vs Type
- Interface vs Abstract Class

These concepts are used extensively in Express, NestJS, ORMs, and enterprise TypeScript applications. The next chapter
explores advanced type features that make TypeScript powerful for building flexible and type-safe APIs.

______________________________________________________________________

# Next

[Advanced Types](04-advanced-types.md)
