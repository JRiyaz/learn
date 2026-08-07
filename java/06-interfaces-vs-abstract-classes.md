# Interfaces vs Abstract Classes

This is one of the most frequently asked Java interview topics.

Almost every Java developer knows what interfaces and abstract classes are.

Far fewer understand **when to use each**.

Modern Java applications, especially Spring Boot applications, rely heavily on interfaces.

Understanding the differences is essential for writing maintainable and loosely coupled applications.

______________________________________________________________________

# Why Do We Need Interfaces?

Imagine you're building a payment system.

Today you support:

- Credit Card
- UPI
- PayPal

Tomorrow you may need:

- Apple Pay
- Google Pay
- Bank Transfer

Instead of tightly coupling your application to one implementation, you define a common contract.

That contract is an **interface**.

______________________________________________________________________

# What is an Interface?

An interface defines **what** a class should do, not **how** it should do it.

Example

```java
interface Payment {

    void pay(double amount);

}
```

Notice

There is no implementation.

Only a method declaration.

______________________________________________________________________

# Implementing an Interface

```java
class CreditCardPayment implements Payment {

    @Override
    public void pay(double amount) {

        System.out.println("Paid using Credit Card");

    }

}
```

Another implementation

```java
class UpiPayment implements Payment {

    @Override
    public void pay(double amount) {

        System.out.println("Paid using UPI");

    }

}
```

______________________________________________________________________

# Using Interfaces

```java
Payment payment = new CreditCardPayment();

payment.pay(1000);
```

Later

```java
payment = new UpiPayment();

payment.pay(500);
```

Notice

Your application doesn't change.

Only the implementation changes.

This is one of the biggest advantages of interfaces.

______________________________________________________________________

# Why Interfaces Matter

Suppose your service depends directly on

```java
CreditCardPayment
```

```java
class OrderService {

    private CreditCardPayment payment =
        new CreditCardPayment();

}
```

Now changing payment methods requires modifying `OrderService`.

Instead

```java
class OrderService {

    private Payment payment;

}
```

Now any implementation works.

This is called **Programming to an Interface**.

______________________________________________________________________

# Multiple Implementations

```java
interface Notification {

    void send(String message);

}
```

```java
class EmailNotification
        implements Notification {

    @Override
    public void send(String message) {

        System.out.println("Email");

    }

}
```

```java
class SmsNotification
        implements Notification {

    @Override
    public void send(String message) {

        System.out.println("SMS");

    }

}
```

```java
class PushNotification
        implements Notification {

    @Override
    public void send(String message) {

        System.out.println("Push");

    }

}
```

One contract.

Multiple implementations.

______________________________________________________________________

# Interface Variables

Every variable declared inside an interface is automatically

```java
public static final
```

Example

```java
interface Constants {

    int MAX_USERS = 100;

}
```

Actually becomes

```java
public static final int MAX_USERS = 100;
```

These are constants.

They cannot change.

______________________________________________________________________

# Interface Methods

By default,

methods are

```java
public abstract
```

Example

```java
interface Animal {

    void sound();

}
```

Actually means

```java
public abstract void sound();
```

______________________________________________________________________

# Java 8 Default Methods

Before Java 8,

interfaces could not contain implementations.

Java 8 introduced

```java
default
```

methods.

Example

```java
interface Vehicle {

    default void start() {

        System.out.println("Starting...");

    }

}
```

Now implementing classes automatically inherit this implementation.

______________________________________________________________________

# Why Default Methods?

Suppose millions of classes implement an interface.

Adding a new method would break all of them.

Default methods solve this.

Existing implementations continue to work.

______________________________________________________________________

# Static Methods in Interfaces

Interfaces can also contain static methods.

```java
interface MathUtil {

    static int square(int x) {

        return x * x;

    }

}
```

Usage

```java
MathUtil.square(5);
```

______________________________________________________________________

# Private Methods (Java 9)

Interfaces can contain private helper methods.

```java
interface Logger {

    private void validate() {

    }

}
```

Used only inside default methods.

Rarely asked but useful to know.

______________________________________________________________________

# Multiple Interface Inheritance

A class can implement multiple interfaces.

```java
interface Flyable {

    void fly();

}
```

```java
interface Swimmable {

    void swim();

}
```

```java
class Duck implements Flyable,
                      Swimmable {

    @Override
    public void fly() {

    }

    @Override
    public void swim() {

    }

}
```

This is something Java allows.

______________________________________________________________________

# Why Multiple Interfaces?

Imagine

```java
Bird
```

can

- Fly
- Swim
- Walk

Instead of creating complicated inheritance trees,

we simply implement multiple capabilities.

______________________________________________________________________

# Diamond Problem

Java avoids the classic Diamond Problem because classes support only single inheritance.

However,

default methods can create conflicts.

Example

```java
interface A {

    default void print() {

        System.out.println("A");

    }

}
```

```java
interface B {

    default void print() {

        System.out.println("B");

    }

}
```

```java
class Demo implements A,B {

}
```

Compilation error.

Java doesn't know which implementation to choose.

______________________________________________________________________

# Resolving Default Method Conflicts

Override the method.

```java
class Demo implements A,B {

    @Override
    public void print() {

        A.super.print();

    }

}
```

Or provide your own implementation.

______________________________________________________________________

# Abstract Class

Unlike interfaces,

abstract classes can contain

- state
- constructors
- implemented methods
- abstract methods

Example

```java
abstract class Animal {

    String name;

    Animal(String name) {

        this.name = name;

    }

    void sleep() {

        System.out.println("Sleeping");

    }

    abstract void sound();

}
```

______________________________________________________________________

# Concrete Implementation

```java
class Dog extends Animal {

    Dog() {

        super("Dog");

    }

    @Override
    void sound() {

        System.out.println("Bark");

    }

}
```

______________________________________________________________________

# Key Difference

Interface

Defines a capability.

Example

```
Flyable

Serializable

Comparable

Runnable
```

Abstract Class

Represents a base object.

Example

```
Animal

Vehicle

Employee

Shape
```

______________________________________________________________________

# Interface vs Abstract Class

| Feature | Interface | Abstract Class |
|----------|-----------|----------------|
| Constructors | ❌ | ✅ |
| Instance Variables | ❌ | ✅ |
| Static Variables | ✅ | ✅ |
| Abstract Methods | ✅ | ✅ |
| Concrete Methods | ✅ (default/static) | ✅ |
| Multiple Inheritance | ✅ | ❌ |
| State | ❌ | ✅ |

______________________________________________________________________

# When Should You Use an Interface?

Use an interface when

- Multiple implementations are expected.
- You're defining a contract.
- Classes are unrelated.
- Loose coupling is important.
- Dependency Injection is used.

Examples

```text
Payment

Notification

Cache

Repository

AuthenticationProvider
```

______________________________________________________________________

# When Should You Use an Abstract Class?

Use an abstract class when

- Classes share state.
- Classes share implementation.
- Constructors are needed.
- Common fields exist.

Examples

```text
Animal

Vehicle

Employee

BaseController

BaseEntity
```

______________________________________________________________________

# Real Spring Boot Example

Repository

```java
public interface UserRepository {

    User findById(Long id);

}
```

Implementation

```java
public class UserRepositoryImpl
        implements UserRepository {

}
```

Service

```java
public class UserService {

    private UserRepository repository;

}
```

Notice

The service depends on the interface,

not the implementation.

This is exactly how Spring performs Dependency Injection.

______________________________________________________________________

# Programming to Interfaces

Instead of

```java
ArrayList<String> list =
    new ArrayList<>();
```

Prefer

```java
List<String> list =
    new ArrayList<>();
```

Instead of

```java
HashMap<String,Integer> map =
    new HashMap<>();
```

Prefer

```java
Map<String,Integer> map =
    new HashMap<>();
```

This allows implementations to change later without affecting client code.

______________________________________________________________________

# Common Mistakes

## Using Abstract Class Everywhere

If classes only share behavior,

use an interface.

______________________________________________________________________

## Using Interfaces for Shared State

Interfaces should not hold object state.

Use abstract classes instead.

______________________________________________________________________

## Depending on Concrete Classes

Bad

```java
HashMap<String,Integer> map =
    new HashMap<>();
```

Better

```java
Map<String,Integer> map =
    new HashMap<>();
```

______________________________________________________________________

## Forgetting Multiple Interface Support

A class cannot extend two classes.

But it can implement many interfaces.

______________________________________________________________________

# Best Practices

✅ Program to interfaces.

✅ Use interfaces for contracts.

✅ Use abstract classes for shared implementation.

✅ Prefer composition with interfaces.

✅ Keep interfaces focused.

✅ Follow the Interface Segregation Principle.

______________________________________________________________________

# Interview Deep Dive

## Question

What is the difference between an interface and an abstract class?

### Answer

An interface defines a contract that implementing classes must follow. It primarily specifies behavior and supports
multiple inheritance through `implements`.

An abstract class serves as a partially implemented base class. It can contain instance variables, constructors,
concrete methods, and abstract methods. It is useful when related classes share common state or behavior.

______________________________________________________________________

## Question

Can an interface have implemented methods?

### Answer

Yes. Since Java 8, interfaces can have `default` methods with implementations and `static` methods. Since Java 9, they
can also contain private helper methods.

______________________________________________________________________

## Question

Can a class implement multiple interfaces?

### Answer

Yes. A Java class can implement any number of interfaces, allowing it to combine multiple behaviors while avoiding the
complexity of multiple class inheritance.

______________________________________________________________________

## Question

Why do Spring applications use interfaces extensively?

### Answer

Interfaces promote loose coupling by allowing classes to depend on abstractions rather than concrete implementations.
This makes dependency injection, testing, mocking, and replacing implementations much easier.

______________________________________________________________________

## Question

Why should we program to interfaces instead of implementations?

### Answer

Programming to interfaces makes code more flexible and maintainable. Client code depends only on the contract, allowing
implementations to change without affecting consumers.

______________________________________________________________________

# Practice Questions

1. What is an interface?
1. What is the difference between an interface and an abstract class?
1. Can an interface have constructors?
1. Can an interface have variables?
1. What are default methods?
1. What is the purpose of static methods in interfaces?
1. Why does Java support multiple interfaces but not multiple class inheritance?
1. What is the Diamond Problem?
1. Why should we program to interfaces?
1. Give real-world examples of interfaces and abstract classes.

______________________________________________________________________

# Summary

Interfaces are the foundation of modern Java application design.

In this chapter, you learned:

- What interfaces are
- Implementing interfaces
- Default methods
- Static methods
- Multiple interface inheritance
- Diamond Problem
- Abstract classes
- Interface vs Abstract Class
- Programming to interfaces
- Real Spring Boot usage

Mastering interfaces is essential because almost every enterprise Java application depends on them for loose coupling,
dependency injection, testing, and maintainability.

______________________________________________________________________

# Next

[Exception Handling](07-exception-handling.md)
