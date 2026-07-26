# File: python/python-advanced-16-composition-vs-inheritance.md

# Python Advanced - Lesson 16
# Composition vs Inheritance - Designing Flexible Object-Oriented Systems

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 16
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 90 Minutes

---

# Learning Objectives

By the end of this lesson, you will understand:

- What composition is
- The "has-a" relationship
- Composition vs inheritance
- Why modern software prefers composition
- Dependency Injection through composition
- Real-world backend examples
- Common design mistakes
- Production best practices
- Interview questions

---

# Recap

So far, we've learned about inheritance.

```
Employee
      ↑
Developer
```

A `Developer` **is an** `Employee`.

This relationship is called an **is-a** relationship.

Not every relationship fits this model.

Sometimes an object doesn't **is-a** another object.

Instead, it **has-a** another object.

This is where **composition** comes in.

---

# What is Composition?

Composition is an object-oriented design technique where one object contains another object instead of inheriting from it.

Instead of saying:

```
Developer
      ↑
Employee
```

we say

```
Developer

↓

DatabaseConnection
```

A developer **has a** database connection.

A developer is **not** a database connection.

---

# Understanding "Has-a"

Examples

```
Car
 ↓
Engine
```

A car **has an** engine.

---

```
Order
 ↓
Payment
```

An order **has a** payment.

---

```
Laptop
 ↓
Battery
```

A laptop **has a** battery.

---

```
UserService
 ↓
Database
```

A service **has a** database.

---

# A Bad Design

Suppose someone writes

```python
class Database:

    def connect(self):

        print("Connected")
```

Then

```python
class UserService(Database):

    pass
```

This compiles.

But it is wrong.

Why?

Because

```
UserService

IS A

Database
```

is not true.

The relationship is incorrect.

---

# Correct Design Using Composition

Instead,

```python
class Database:

    def connect(self):

        print("Connected")
```

```python
class UserService:

    def __init__(self):

        self.database = Database()
```

Usage

```python
service = UserService()

service.database.connect()
```

Output

```
Connected
```

Now the relationship is correct.

```
UserService

HAS A

Database
```

---

# Visualising Composition

```
UserService

      │

      ▼

Database
```

The service owns a database object.

It does not inherit from it.

---

# Why Composition is Better

Suppose tomorrow

the database changes.

Today

```
MySQL
```

Tomorrow

```
PostgreSQL
```

With composition,

only one object changes.

The service remains the same.

---

# Example

```python
class MySQLDatabase:

    def connect(self):

        print("MySQL Connected")
```

Later

```python
class PostgreSQLDatabase:

    def connect(self):

        print("PostgreSQL Connected")
```

The service can simply use a different database object.

No inheritance changes are required.

---

# Dependency Injection

Production systems rarely create dependencies directly.

Instead of

```python
class UserService:

    def __init__(self):

        self.database = Database()
```

we inject it.

```python
class UserService:

    def __init__(self, database):

        self.database = database
```

Usage

```python
database = Database()

service = UserService(database)
```

This is called **Dependency Injection (DI).**

---

# Why Dependency Injection?

Imagine testing.

Without dependency injection,

the service always uses a real database.

Testing becomes slow.

With dependency injection,

we can provide a fake database.

```python
class FakeDatabase:

    def connect(self):

        print("Fake Database")
```

Testing

```python
service = UserService(
    FakeDatabase()
)

service.database.connect()
```

Output

```
Fake Database
```

This makes unit testing much easier.

---

# Real Backend Example

Imagine a FastAPI application.

```
UserService

↓

UserRepository

↓

Database
```

The service doesn't know whether the repository uses:

- PostgreSQL
- MySQL
- MongoDB

It simply calls repository methods.

---

# Composition Chain

```
API

↓

Service

↓

Repository

↓

Database
```

Every layer has one responsibility.

This is called **Separation of Concerns.**

---

# Composition vs Inheritance

| Composition | Inheritance |
|-------------|-------------|
| Has-a relationship | Is-a relationship |
| Flexible | Less flexible |
| Loosely coupled | More tightly coupled |
| Easy to replace dependencies | Parent changes affect children |
| Preferred in modern software | Useful for genuine hierarchies |

---

# Real Example

Inheritance

```python
class Bird:

    def fly(self):

        ...
```

```python
class Penguin(Bird):

    pass
```

Problem

Penguins cannot fly.

The hierarchy is wrong.

---

Composition

```python
class FlyBehaviour:

    def fly(self):

        print("Flying")
```

```python
class Penguin:

    def __init__(self):

        self.fly_behaviour = None
```

```python
class Eagle:

    def __init__(self):

        self.fly_behaviour = FlyBehaviour()
```

Now behaviour is composed instead of inherited.

---

# The "Favor Composition Over Inheritance" Principle

One of the most famous object-oriented design principles is:

> **Favor composition over inheritance.**

This doesn't mean inheritance is bad.

It means:

- Use inheritance only when the relationship is truly **is-a**.
- Otherwise, compose objects together.

This produces software that is easier to extend and maintain.

---

# Production Example - Payment Gateway

Instead of

```python
class PaymentService(Stripe):
    ...
```

use

```python
class PaymentService:

    def __init__(self, gateway):

        self.gateway = gateway
```

Then

```python
StripeGateway()
```

or

```python
PayPalGateway()
```

can be injected.

No changes are needed in the service.

---

# Production Example - Logging

```python
class Logger:

    def log(self, message):

        print(message)
```

```python
class UserService:

    def __init__(self, logger):

        self.logger = logger
```

Tomorrow

replace

```
ConsoleLogger
```

with

```
CloudLogger
```

The service remains unchanged.

---

# Composition in Popular Frameworks

FastAPI

```
Route

↓

Service

↓

Repository
```

Django

```
View

↓

Service

↓

Model
```

Flask

```
Blueprint

↓

Service

↓

Repository
```

Almost every modern backend architecture relies heavily on composition.

---

# Common Mistakes

### Mistake 1

Using inheritance simply to reuse code.

```
UserService(Database)
```

Wrong.

---

### Mistake 2

Deep inheritance trees.

```
A

↓

B

↓

C

↓

D

↓

E

↓

F
```

These are difficult to understand and maintain.

---

### Mistake 3

Creating objects inside business logic.

```python
class UserService:

    def __init__(self):

        self.database = Database()
```

This tightly couples the service to a specific implementation.

Inject dependencies instead.

---

# Best Practices

✅ Prefer composition for reusable components.

✅ Use inheritance only for genuine **is-a** relationships.

✅ Inject dependencies rather than creating them.

✅ Keep objects focused on a single responsibility.

✅ Design components to be replaceable.

❌ Don't inherit simply to share code.

❌ Don't tightly couple business logic to infrastructure.

---

# Production Insight

If you examine the architecture of large backend applications, you'll notice that inheritance is used sparingly.

A typical production application looks like this:

```
Controller

↓

Service

↓

Repository

↓

Database
```

Each layer communicates with another through composition.

This design makes it easy to:

- Replace implementations
- Write unit tests
- Introduce caching
- Add logging
- Swap databases
- Scale independently

Composition is one of the key reasons modern backend systems remain maintainable as they grow.

---

# Interview Deep Dive

### Interviewer

> What is composition?

### Answer

Composition is an object-oriented design technique where one object contains another object to reuse functionality. It represents a "has-a" relationship.

---

### Interviewer

> What is the difference between composition and inheritance?

### Answer

Inheritance models an "is-a" relationship and allows one class to extend another. Composition models a "has-a" relationship by combining objects. Composition generally provides greater flexibility and lower coupling.

---

### Interviewer

> Why do modern applications prefer composition?

### Answer

Composition allows components to be replaced, tested and extended independently. It reduces coupling, improves maintainability and aligns well with principles such as dependency injection and single responsibility.

---

# Practical Lesson

Create a file:

```
composition_examples.py
```

```python
class Database:

    def connect(self):

        print("Connected")


class UserRepository:

    def __init__(self, database):

        self.database = database

    def get_users(self):

        self.database.connect()

        print("Fetching users")


class UserService:

    def __init__(self, repository):

        self.repository = repository

    def list_users(self):

        self.repository.get_users()


database = Database()

repository = UserRepository(database)

service = UserService(repository)

service.list_users()
```

Expected Output

```
Connected

Fetching users
```

Observe how each object depends on another through composition instead of inheritance.

---

# Interview Questions

## Question 1

What is composition?

### Answer

Composition is an object-oriented design pattern where a class contains instances of other classes to reuse functionality. It represents a "has-a" relationship.

---

## Question 2

When should inheritance be used?

### Answer

Inheritance should be used only when there is a genuine "is-a" relationship and the child is a specialised version of the parent.

---

## Question 3

Why is composition generally preferred?

### Answer

Composition creates loosely coupled systems that are easier to maintain, extend and test.

---

## Question 4

What is dependency injection?

### Answer

Dependency injection is the practice of providing dependencies to an object from the outside rather than allowing the object to create them itself.

---

## Question 5

Why does dependency injection improve testing?

### Answer

It allows real dependencies to be replaced with mock or fake implementations, enabling fast and isolated unit tests.

---

# Assignment

## Exercise 1

Create:

- `Database`
- `Repository`
- `Service`

Use composition to connect all three.

---

## Exercise 2

Replace the real database with a `FakeDatabase`.

Verify that the service continues to work without modification.

---

## Exercise 3

Design a notification system using composition.

Create:

- `EmailNotifier`
- `SMSNotifier`
- `NotificationService`

Inject different notifier implementations into the service.

---

## Exercise 4

Take one of your previous inheritance examples and redesign it using composition.

Explain why the new design is more flexible.

---

# Summary

In this lesson, you learned:

- ✅ What composition is.
- ✅ The difference between "has-a" and "is-a" relationships.
- ✅ Why modern software prefers composition.
- ✅ How dependency injection is built on composition.
- ✅ How backend architectures use composition extensively.
- ✅ Production best practices for building loosely coupled systems.

---

# What's Next

**File:**

`python/python-advanced-17-abstract-base-classes.md`

Topics:

- Why Abstract Base Classes (ABC) Exist
- Interfaces vs Abstract Classes
- The `abc` Module
- `ABC` and `@abstractmethod`
- Enforcing Contracts
- Polymorphism with ABCs
- Production Examples
- Interview Questions
