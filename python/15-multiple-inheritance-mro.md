# File: python/15-multiple-inheritance-mro.md

# Python Advanced - Lesson 15

# Multiple Inheritance & Method Resolution Order (MRO)

> **Course:** Backend Engineering Roadmap
>
> **Module:** Advanced OOP
>
> **Lesson:** 15
>
> **Difficulty:** ⭐⭐⭐⭐⭐
>
> **Estimated Time:** 100 Minutes

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- What multiple inheritance is
- Why Python supports multiple inheritance
- The Diamond Problem
- Method Resolution Order (MRO)
- How `super()` works with multiple inheritance
- Cooperative multiple inheritance
- Production use cases
- Best practices

______________________________________________________________________

# Recap

In the previous lesson, we learned about single inheritance.

```
Employee

↓

Developer
```

A child inherited from exactly one parent.

Python also allows this.

```
Employee

        ↑

Developer      Logger

        ↑

BackendDeveloper
```

One class can inherit from multiple parent classes.

This is called **Multiple Inheritance**.

______________________________________________________________________

# Why Multiple Inheritance Exists

Suppose you're building a backend application.

A service might need:

- Authentication
- Logging
- Caching

Instead of rewriting all three features,

Python allows one class to inherit them.

```
Authentication

        ↑

Logging

        ↑

Caching

        ↑

APIService
```

Each parent contributes behaviour.

______________________________________________________________________

# Basic Example

```python
class Logger:

    def log(self):

        print("Logging...")
```

```python
class Authentication:

    def authenticate(self):

        print("User Authenticated")
```

Child class

```python
class APIService(
    Logger,
    Authentication
):

    pass
```

Usage

```python
service = APIService()

service.log()

service.authenticate()
```

Output

```
Logging...

User Authenticated
```

The child inherited methods from both parents.

______________________________________________________________________

# What Happens When Parents Have the Same Method?

Suppose both classes define:

```python
process()
```

```python
class Logger:

    def process(self):

        print("Logger")
```

```python
class Authentication:

    def process(self):

        print("Authentication")
```

Child

```python
class APIService(
    Logger,
    Authentication
):

    pass
```

Usage

```python
service = APIService()

service.process()
```

Output

```
Logger
```

Why?

Python follows a specific search order.

This is called the **Method Resolution Order (MRO).**

______________________________________________________________________

# What is MRO?

MRO determines

> "Which method should Python call?"

Python searches classes in a predefined order.

For this example

```python
class APIService(
    Logger,
    Authentication
):
    pass
```

The order is

```
APIService

↓

Logger

↓

Authentication

↓

object
```

The first matching method wins.

______________________________________________________________________

# Inspecting the MRO

Python exposes the MRO.

```python
print(APIService.mro())
```

Output

```python
[
    APIService,
    Logger,
    Authentication,
    object
]
```

You can also inspect

```python
print(APIService.__mro__)
```

Both produce the same information.

______________________________________________________________________

# The Diamond Problem

Now consider this hierarchy.

```
          Animal
          /    \
         /      \
      Bird     Mammal
         \      /
          \    /
        FlyingBat
```

Both `Bird` and `Mammal`

inherit from `Animal`.

`FlyingBat`

inherits from both.

If every class defines

```python
speak()
```

which version should Python use?

This is known as the **Diamond Problem**.

______________________________________________________________________

# Example

```python
class Animal:

    def speak(self):

        print("Animal")
```

```python
class Bird(Animal):

    def speak(self):

        print("Bird")
```

```python
class Mammal(Animal):

    def speak(self):

        print("Mammal")
```

```python
class FlyingBat(
    Bird,
    Mammal
):

    pass
```

Usage

```python
bat = FlyingBat()

bat.speak()
```

Output

```
Bird
```

Python follows the MRO.

It does **not** call both methods automatically.

______________________________________________________________________

# How Python Calculates MRO

Python uses an algorithm called

**C3 Linearization**.

Fortunately,

you don't need to memorise the algorithm.

You do need to understand the result.

Python guarantees that:

- Parents appear before grandparents.
- Local inheritance order is respected.
- Every class appears only once.

______________________________________________________________________

# super() in Multiple Inheritance

Many developers assume

```python
super()
```

means

> "Call my parent."

That is **not** entirely correct.

It actually means

> "Call the next class in the MRO."

This distinction is extremely important.

______________________________________________________________________

# Example

```python
class A:

    def process(self):

        print("A")
```

```python
class B(A):

    def process(self):

        print("B")

        super().process()
```

```python
class C(A):

    def process(self):

        print("C")

        super().process()
```

```python
class D(
    B,
    C
):

    def process(self):

        print("D")

        super().process()
```

Usage

```python
D().process()
```

Output

```
D

B

C

A
```

Notice something interesting.

`super()` in `B`

did **not**

jump directly to `A`.

It called `C`.

Why?

Because `C` is next in the MRO.

______________________________________________________________________

# Visualising the Call Chain

For class

```python
class D(B, C)
```

MRO becomes

```
D

↓

B

↓

C

↓

A

↓

object
```

Every `super()` call follows this chain.

______________________________________________________________________

# Cooperative Multiple Inheritance

For multiple inheritance to work correctly,

every class must cooperate.

Each implementation should call

```python
super()
```

Example

```python
class Logger:

    def process(self):

        print("Logger")

        super().process()
```

Every class contributes its work,

then passes control to the next class.

This is called

**Cooperative Multiple Inheritance.**

______________________________________________________________________

# What Happens Without super()?

Suppose

```python
class B(A):

    def process(self):

        print("B")
```

No `super()`.

Now

```python
D().process()
```

Output

```
D

B
```

The chain stops.

Classes after `B`

never execute.

______________________________________________________________________

# When Should You Use Multiple Inheritance?

Good examples

- Logging
- Caching
- Authentication
- Validation
- Reusable mixins

Poor examples

```
Car

↓

House
```

If the relationship doesn't make sense,

don't use inheritance.

______________________________________________________________________

# Production Example - Mixins

A common pattern is

```
BaseModel

↑

TimestampMixin

↑

SoftDeleteMixin

↑

AuditMixin

↑

User
```

Each mixin contributes a small piece of behaviour.

We'll study mixins in detail later.

______________________________________________________________________

# Production Example

Imagine an API.

```python
class LoggingMixin:

    ...
```

```python
class AuthenticationMixin:

    ...
```

```python
class UserAPI(

    LoggingMixin,

    AuthenticationMixin

):
    ...
```

Each concern remains independent.

The final class combines them.

______________________________________________________________________

# Best Practices

✅ Keep inheritance hierarchies shallow.

✅ Prefer composition unless inheritance is clearly appropriate.

✅ Use `super()` consistently.

✅ Design parent classes to cooperate.

❌ Don't call parent classes directly when cooperative inheritance is intended.

❌ Don't build deep inheritance trees.

______________________________________________________________________

# Questions

### Question

> What is Multiple Inheritance?

### Answer

Multiple inheritance allows a class to inherit attributes and methods from more than one parent class. Python resolves
conflicts using the Method Resolution Order (MRO).

______________________________________________________________________

### Question

> What is the Diamond Problem?

### Answer

The Diamond Problem occurs when a class inherits from two classes that both inherit from the same parent. Python
resolves method lookup using its MRO algorithm, ensuring every class is visited only once.

______________________________________________________________________

### Question

> Does `super()` always call the immediate parent?

### Answer

No. `super()` calls the next class in the Method Resolution Order, not necessarily the immediate parent. This behaviour
enables cooperative multiple inheritance.

______________________________________________________________________

# Practical Lesson

Create a file:

```
multiple_inheritance.py
```

```python
class A:

    def process(self):

        print("A")


class B(A):

    def process(self):

        print("B")

        super().process()


class C(A):

    def process(self):

        print("C")

        super().process()


class D(B, C):

    def process(self):

        print("D")

        super().process()


application = D()

application.process()
```

Expected Output

```
D

B

C

A
```

Now print the MRO.

```python
print(D.mro())
```

Observe the order that Python follows.

______________________________________________________________________

# Questions

## Question 1

What is multiple inheritance?

### Answer

Multiple inheritance allows a class to inherit behaviour from more than one parent class.

______________________________________________________________________

## Question 2

What is Method Resolution Order (MRO)?

### Answer

MRO is the order in which Python searches classes to resolve methods and attributes during inheritance.

______________________________________________________________________

## Question 3

What is the Diamond Problem?

### Answer

It occurs when two parent classes inherit from the same base class and a child inherits from both parents. Python
resolves this ambiguity using its C3 Linearization algorithm.

______________________________________________________________________

## Question 4

Does `super()` always call the parent class?

### Answer

No. `super()` calls the next class in the Method Resolution Order, which may not be the immediate parent.

______________________________________________________________________

## Question 5

Why is cooperative multiple inheritance important?

### Answer

It ensures every class in the inheritance chain gets an opportunity to execute its implementation by consistently
calling `super()`.

______________________________________________________________________

# Assignment

## Exercise 1

Create three classes:

- Logger
- Validator
- APIService

Make `APIService` inherit from both.

Verify that methods from both parent classes are available.

______________________________________________________________________

## Exercise 2

Create the following hierarchy.

```
        A
       / \
      B   C
       \ /
        D
```

Implement a method called `display()` in every class.

Use `super()` and observe the execution order.

______________________________________________________________________

## Exercise 3

Print both:

```python
D.mro()
```

and

```python
D.__mro__
```

Compare the results.

______________________________________________________________________

## Exercise 4

Remove one `super()` call from the hierarchy.

Observe how the cooperative inheritance chain breaks.

Explain why.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ Why Python supports multiple inheritance.
- ✅ How Method Resolution Order (MRO) determines method lookup.
- ✅ The Diamond Problem and how Python solves it.
- ✅ Why `super()` follows the MRO instead of the immediate parent.
- ✅ Cooperative multiple inheritance.
- ✅ Production use cases such as mixins.
- ✅ Best practices for designing inheritance hierarchies.

______________________________________________________________________

# What's Next

**File:** [16-Composition-vs-Inheritance](16-composition-vs-inheritance.md)

Topics:

- Why Composition Exists
- "Has-a" vs "Is-a" Relationships
- Composition vs Inheritance
- Dependency Injection Through Composition
- Real-world Backend Examples
- When to Choose Composition
- Production Best Practices
